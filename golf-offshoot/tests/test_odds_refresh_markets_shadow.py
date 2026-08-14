import json
import time
from datetime import datetime, timezone
from pathlib import Path

from golf_offshoot.audit.shadow import append_shadow_advises, load_shadow
from golf_offshoot.bayesian_engine.engine import BayesianEngine
from golf_offshoot.bayesian_engine.simulate import SimConfig
from golf_offshoot.config import ODDS_LIVE_MAX_STALE_SECONDS
from golf_offshoot.data_feeds.base import FeedError
from golf_offshoot.data_feeds.bovada import BovadaOddsFeed, classify_market
from golf_offshoot.data_feeds.datagolf import DataGolfRecentSgFeed
from golf_offshoot.data_feeds.http import HttpCache
from golf_offshoot.demo import demo_field, demo_odds, demo_tournament
from golf_offshoot.market.coverage import market_coverage_report
from golf_offshoot.market.freshness import apply_odds_freshness
from golf_offshoot.models.enums import BetType, SourceKind, StrategyActionKind, StrategyMode
from golf_offshoot.models.schemas import DataQuality, MarketQuote
from golf_offshoot.models.strategy import StrategyAction, StrategyConfig
from golf_offshoot.pipeline import GolfOffshootPipeline


def test_classify_market_separates_winner_and_place():
    assert classify_market("Winner Live") == BetType.WIN
    assert classify_market("Top 10 Finish") == BetType.TOP_10
    assert classify_market("Top 5") == BetType.TOP_5
    assert classify_market("Top 20 Finish") == BetType.TOP_20
    assert classify_market("To Make The Cut") == BetType.MAKE_CUT
    assert classify_market("1st Round Leader") is None
    assert classify_market("2-Ball Matchup") is None
    assert classify_market("Place") is None  # never invent from an unlabeled place


def test_bovada_ingests_top10_when_coupon_lists_it():
    event = {
        "description": "FedEx St. Jude Championship",
        "lastModified": 1755100000000,
        "displayGroups": [
            {
                "markets": [
                    {
                        "description": "Winner Live",
                        "outcomes": [{"description": "Scottie Scheffler", "price": {"decimal": "5.50"}}],
                    },
                    {
                        "description": "Top 10 Finish",
                        "outcomes": [{"description": "Scottie Scheffler", "price": {"decimal": "1.80"}}],
                    },
                ]
            }
        ],
    }
    feed = BovadaOddsFeed()
    quotes, unmatched, markets = feed._quotes_from_event(
        event, {"scottie scheffler": "id-ss"}
    )
    assert unmatched == 0
    types = {q.bet_type for q in quotes}
    assert BetType.WIN in types
    assert BetType.TOP_10 in types
    assert any("Top 10" in m for m in markets)
    t10 = next(q for q in quotes if q.bet_type == BetType.TOP_10)
    assert t10.decimal_odds == 1.8
    assert t10.implied_raw == 1.0 / 1.8


def test_bovada_does_not_synthesize_top10_from_winner_only():
    event = {
        "description": "FedEx St. Jude Championship",
        "lastModified": 1755100000000,
        "displayGroups": [
            {
                "markets": [
                    {
                        "description": "Winner Live",
                        "outcomes": [{"description": "Scottie Scheffler", "price": {"decimal": "5.50"}}],
                    }
                ]
            }
        ],
    }
    feed = BovadaOddsFeed()
    quotes, _, _ = feed._quotes_from_event(event, {"scottie scheffler": "id-ss"})
    assert all(q.bet_type == BetType.WIN for q in quotes)
    cov = market_coverage_report(quotes, n_field=1)
    assert cov["synthesized"] is False
    assert "top_10" in cov["unavailable_markets"]
    assert "win" in cov["available_markets"]


def test_bovada_unions_winner_and_finishes_events():
    groups = [
        {
            "path": [{"description": "PGA Tour"}, {"description": "FedEx St. Jude Championship"}],
            "events": [
                {
                    "id": "w1",
                    "description": "FedEx St. Jude Championship Winner Live",
                    "lastModified": 1755100000000,
                    "displayGroups": [
                        {
                            "markets": [
                                {
                                    "description": "Winner Live",
                                    "outcomes": [
                                        {"description": "Scottie Scheffler", "price": {"decimal": "5.50"}}
                                    ],
                                }
                            ]
                        }
                    ],
                },
                {
                    "id": "f1",
                    "description": "FedEx St. Jude Championship Finishes",
                    "lastModified": 1755100100000,
                    "displayGroups": [
                        {
                            "markets": [
                                {
                                    "description": "Top 10 Finish",
                                    "outcomes": [
                                        {"description": "Scottie Scheffler", "price": {"decimal": "1.91"}}
                                    ],
                                }
                            ]
                        }
                    ],
                },
            ],
        }
    ]
    feed = BovadaOddsFeed()
    events = feed._matching_events(groups, "FedEx St. Jude Championship")
    assert len(events) == 2
    quotes, _, markets = feed._quotes_from_events(events, {"scottie scheffler": "id-ss"}, live=True)
    types = {q.bet_type for q in quotes if q.line_role != "opening"}
    assert types == {BetType.WIN, BetType.TOP_10}
    assert any("Winner" in m for m in markets)
    assert any("Top 10" in m for m in markets)


def test_bovada_tags_prematch_as_opening_when_live_winner_exists():
    groups = [
        {
            "path": [{"description": "PGA Tour"}, {"description": "FedEx St. Jude Championship"}],
            "events": [
                {
                    "id": "pre",
                    "description": "FedEx St. Jude Championship",
                    "lastModified": 1755000000000,
                    "displayGroups": [
                        {
                            "markets": [
                                {
                                    "description": "Winner",
                                    "outcomes": [
                                        {"description": "Scottie Scheffler", "price": {"decimal": "6.00"}}
                                    ],
                                }
                            ]
                        }
                    ],
                },
                {
                    "id": "live",
                    "description": "FedEx St. Jude Championship Winner Live",
                    "lastModified": 1755100000000,
                    "displayGroups": [
                        {
                            "markets": [
                                {
                                    "description": "Winner Live",
                                    "outcomes": [
                                        {"description": "Scottie Scheffler", "price": {"decimal": "4.50"}}
                                    ],
                                }
                            ]
                        }
                    ],
                },
            ],
        }
    ]
    feed = BovadaOddsFeed()
    events = feed._matching_events(groups, "FedEx St. Jude Championship")
    quotes, _, _ = feed._quotes_from_events(events, {"scottie scheffler": "id-ss"}, live=True)
    current = [q for q in quotes if q.line_role != "opening"]
    opening = [q for q in quotes if q.line_role == "opening"]
    assert len(current) == 1
    assert current[0].book == "bovada_live"
    assert current[0].decimal_odds == 4.5
    assert len(opening) == 1
    assert opening[0].book == "bovada"
    assert opening[0].decimal_odds == 6.0
    cov = market_coverage_report(quotes, n_field=1)
    assert cov["opening_available"] is True
    assert cov["by_market"]["win"]["n"] == 1


def test_live_only_coupon_is_not_claimed_as_opening():
    event = {
        "description": "FedEx St. Jude Championship Winner Live",
        "lastModified": 1755100000000,
        "displayGroups": [
            {
                "markets": [
                    {
                        "description": "Winner Live",
                        "outcomes": [{"description": "Scottie Scheffler", "price": {"decimal": "5.50"}}],
                    }
                ]
            }
        ],
    }
    feed = BovadaOddsFeed()
    quotes, _, _ = feed._quotes_from_events([event], {"scottie scheffler": "id-ss"}, live=True)
    assert all(q.line_role == "current" for q in quotes)
    cov = market_coverage_report(quotes, n_field=1)
    assert cov["opening_available"] is False


def test_champions_finishes_are_not_attached_to_pga_event():
    groups = [
        {
            "path": [{"description": "Boeing Classic - Finishes"}, {"description": "Champions Tour"}],
            "events": [
                {
                    "id": "boeing-fin",
                    "description": "Finishes",
                    "lastModified": 1755100000000,
                    "displayGroups": [
                        {
                            "markets": [
                                {
                                    "description": "Top 10 Finish",
                                    "outcomes": [
                                        {"description": "Scottie Scheffler", "price": {"decimal": "1.80"}}
                                    ],
                                }
                            ]
                        }
                    ],
                }
            ],
        },
        {
            "path": [{"description": "FedEx St. Jude Championship"}, {"description": "PGA Tour"}],
            "events": [
                {
                    "id": "stj",
                    "description": "FedEx St. Jude Championship",
                    "lastModified": 1755100000000,
                    "displayGroups": [
                        {
                            "markets": [
                                {
                                    "description": "Winner Live",
                                    "outcomes": [
                                        {"description": "Scottie Scheffler", "price": {"decimal": "5.50"}}
                                    ],
                                }
                            ]
                        }
                    ],
                }
            ],
        },
    ]
    feed = BovadaOddsFeed()
    events = feed._matching_events(groups, "FedEx St. Jude Championship")
    assert [ev.get("id") for ev in events] == ["stj"]
    quotes, _, markets = feed._quotes_from_events(events, {"scottie scheffler": "id-ss"}, live=True)
    assert all(q.bet_type == BetType.WIN for q in quotes)
    assert not any("Top 10" in m for m in markets)


def test_opening_archive_never_stores_live_and_merges_prematch(tmp_path: Path):
    from golf_offshoot.data_feeds.openings import (
        load_opening_quotes,
        merge_archived_openings,
        persist_prematch_openings,
    )

    live = MarketQuote(
        player_id="id-ss",
        bet_type=BetType.WIN,
        decimal_odds=4.5,
        implied_raw=1.0 / 4.5,
        book="bovada_live",
        line_role="current",
    )
    pre = MarketQuote(
        player_id="id-ss",
        bet_type=BetType.WIN,
        decimal_odds=6.0,
        implied_raw=1.0 / 6.0,
        book="bovada",
        line_role="current",
    )
    assert persist_prematch_openings("401811962", "FedEx St. Jude Championship", [live], directory=tmp_path) is None
    assert load_opening_quotes("401811962", directory=tmp_path) == []
    saved = persist_prematch_openings("401811962", "FedEx St. Jude Championship", [pre], directory=tmp_path)
    assert saved is not None
    # Second persist must not overwrite the first prematch snapshot with live.
    persist_prematch_openings("401811962", "FedEx St. Jude Championship", [live], directory=tmp_path)
    merged = merge_archived_openings([live], "401811962", directory=tmp_path)
    opening = [q for q in merged if q.line_role == "opening"]
    current = [q for q in merged if q.line_role != "opening"]
    assert len(current) == 1 and current[0].book == "bovada_live"
    assert len(opening) == 1 and opening[0].decimal_odds == 6.0
    assert opening[0].book == "bovada"



def test_http_cache_stale_fallback_on_error(tmp_path: Path):
    cache = HttpCache(tmp_path)
    url = "https://127.0.0.1:1/odds.json"
    path = cache._path(url)
    fetched = time.time() - 80
    path.write_text(
        json.dumps(
            {
                "url": url,
                "method": "GET",
                "fetched_at": "2026-08-13T18:00:00+00:00",
                "fetched_epoch": fetched,
                "status": 200,
                "label": "test",
                "body": {"ok": True},
            }
        ),
        encoding="utf-8",
    )
    body, meta = cache.get_json(
        url, refresh=True, allow_stale_on_error=True, timeout=1.0, ttl_seconds=45
    )
    assert body == {"ok": True}
    assert meta["stale_fallback"] is True
    assert meta["cached"] is True
    assert meta["age_seconds"] >= 70
    try:
        cache.get_json(url, refresh=True, allow_stale_on_error=False, timeout=1.0)
        raised = False
    except FeedError:
        raised = True
    assert raised


def test_http_cache_ttl_hit_is_not_stale_fallback(tmp_path: Path):
    cache = HttpCache(tmp_path)
    url = "https://example.invalid/fresh.json"
    path = cache._path(url)
    path.write_text(
        json.dumps(
            {
                "url": url,
                "fetched_at": "2026-08-13T18:00:00+00:00",
                "fetched_epoch": time.time() - 10,
                "body": {"fresh": 1},
                "label": "t",
            }
        ),
        encoding="utf-8",
    )
    body, meta = cache.get_json(url, ttl_seconds=45, refresh=False)
    assert body == {"fresh": 1}
    assert meta["cached"] is True
    assert meta["stale_fallback"] is False


def test_live_odds_too_old_are_suppressed_not_silently_used():
    q = DataQuality(
        score=0.78,
        source_name="bovada",
        as_of=datetime.now(timezone.utc),
        n_observations=1,
        lag_hours=(ODDS_LIVE_MAX_STALE_SECONDS + 60) / 3600.0,
        notes="STALE_FALLBACK age_s=2000",
        source_kind=SourceKind.REAL_LIVE,
    )
    quotes = [
        MarketQuote(player_id="x", bet_type=BetType.WIN, decimal_odds=5.0, implied_raw=0.2, book="bovada")
    ]
    out, q2 = apply_odds_freshness(quotes, q, live=True)
    assert out == []
    assert q2.missing is True
    assert q2.source_kind == SourceKind.UNAVAILABLE
    assert "EDGES_SUPPRESSED_STALE" in q2.notes


def test_live_odds_mild_stale_kept_with_confidence_cut():
    q = DataQuality(
        score=0.78,
        source_name="bovada",
        as_of=datetime.now(timezone.utc),
        n_observations=1,
        lag_hours=8 / 60.0,
        notes="STALE_FALLBACK age_s=480",
        source_kind=SourceKind.REAL_LIVE,
    )
    quotes = [
        MarketQuote(player_id="x", bet_type=BetType.WIN, decimal_odds=5.0, implied_raw=0.2, book="bovada")
    ]
    out, q2 = apply_odds_freshness(quotes, q, live=True)
    assert len(out) == 1
    assert q2.score <= 0.55
    assert "confidence_cut" in q2.notes


def test_datagolf_missing_key_leaves_recent_sg_unavailable():
    feed = DataGolfRecentSgFeed(api_key="")
    payload, q = feed.fetch()
    assert q.missing is True
    assert q.source_kind == SourceKind.UNAVAILABLE
    assert "not inferred" in q.notes.lower() or "not used as a last-8" in q.notes.lower()
    assert payload == {}


def test_shadow_journal_logs_new_bet_only(tmp_path: Path):
    engine = BayesianEngine(sim=SimConfig(n_sims=400, seed=1))
    pipe = GolfOffshootPipeline(
        engine=engine,
        snapshot_dir=None,
        strategy_config=StrategyConfig(enabled=True, mode=StrategyMode.PRESS_EDGES, bankroll=2000),
    )
    result = pipe.run(
        demo_tournament(),
        demo_field(),
        market_quotes=demo_odds(demo_field()),
        persist=False,
    )
    path = tmp_path / "advises.jsonl"
    if result.strategy and not any(a.kind == StrategyActionKind.NEW_BET for a in result.strategy.actions):
        result.strategy.actions.append(
            StrategyAction(
                action_id="act-test",
                kind=StrategyActionKind.NEW_BET,
                player_id=result.ranked[0].player_id,
                player_name=result.ranked[0].name,
                bet_type=BetType.WIN,
                suggested_stake_delta=4.0,
                reason="test advise",
            )
        )
    rows = append_shadow_advises(result, path=path)
    assert rows
    assert all(r.never_auto_bet and r.paper_observation_only for r in rows)
    loaded = load_shadow(path)
    assert len(loaded) == len(rows)
    assert loaded[0].market
    assert loaded[0].tournament
