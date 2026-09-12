"""Kalshi golf gym. Own ledger. Advisor on tick one. 15m stays up."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from golf_offshoot.data_feeds.kalshi_15m import ALLOWED_SERIES, PrivateEndpointRefused
from golf_offshoot.data_feeds.names import normalize_name
from golf_offshoot.golf_kalshi.adapter import (
    GolfKalshiFeed,
    GolfSeriesRefused,
    assert_golf_public_url,
    golf_only_catalog,
    is_golf_series,
    parse_market,
    parse_series,
)
from golf_offshoot.golf_kalshi.brain import StaticBrain, TickBudget
from golf_offshoot.golf_kalshi.decide import decide_golf
from golf_offshoot.golf_kalshi.executor import LiveExecutor, PaperExecutor, RecordingTransport, UnarmedError
from golf_offshoot.golf_kalshi.loop import run_tick
from golf_offshoot.golf_kalshi.paper import empty_ledger, load_ledger, save_ledger
from golf_offshoot.golf_kalshi.paths import (
    ledger_path,
    set_golf_kalshi_root_override,
    trading_armed_path,
    watch_kill_path,
)
from golf_offshoot.golf_kalshi.recipe import recipe_v1
from golf_offshoot.golf_kalshi.settle import SettleError, apply_kalshi_result
from golf_offshoot.golf_kalshi.sleeves import classify_sleeve
from golf_offshoot.golf_kalshi.watch import start_sidecar_process
from golf_offshoot.operator_surface.app import (
    apply_request_lane,
    build_surface,
    render_html,
    _sync_paper_watch,
)
from golf_offshoot.operator_surface.lanes import lane_header_name


@pytest.fixture
def gk_root(tmp_path):
    root = tmp_path / "golf_kalshi"
    set_golf_kalshi_root_override(root)
    try:
        yield root
    finally:
        set_golf_kalshi_root_override(None)


def _market(**kwargs) -> dict:
    row = {
        "ticker": "KXPGA-26-SSCHEFF",
        "event_ticker": "KXPGA-26",
        "series_ticker": "KXPGA",
        "title": "Will Scottie Scheffler win the Masters?",
        "yes_sub_title": "Scottie Scheffler",
        "yes_ask": 0.08,
        "yes_bid": 0.07,
        "displayed_size": 500.0,
        "spread": 0.01,
        "fee_multiplier": 1.0,
        "fee_multiplier_present": True,
        "status": "open",
        "result": "",
        "in_play": False,
    }
    row.update(kwargs)
    return row


def _brain() -> StaticBrain:
    return StaticBrain(
        {normalize_name("Scottie Scheffler"): "scottie"},
        {"scottie": {"win": 0.22}},
    )


def test_15m_allowlist_unchanged():
    assert ALLOWED_SERIES == "KXBTC15M"


def test_adapter_refuses_crypto_and_private():
    assert is_golf_series("KXPGA", category="Sports", title="PGA Tour Golf")
    assert is_golf_series("KXLIVTOP10", category="Sports", title="Liv Top 10 Finisher", tags=["Golf"])
    assert is_golf_series("KXPGAALBATROSS", category="Sports", title="Golf Albatross", tags=[])
    assert not is_golf_series("KXBTC15M", category="Crypto", title="Bitcoin")
    assert not is_golf_series(
        "KXLEAGUESCUPGAME", category="Sports", title="Leagues Cup Game", tags=["Soccer"]
    )
    assert not is_golf_series("CAPGAIN", category="Politics", title="Capital gains tax increase")
    assert not is_golf_series(
        "KXMCMMEN", category="Sports", title="ATP Monte-Carlo Masters Winner", tags=["Tennis"]
    )
    assert not is_golf_series(
        "KXUSOPENCUP", category="Sports", title="US Open Cup Soccer", tags=["Soccer"]
    )
    with pytest.raises(PrivateEndpointRefused):
        assert_golf_public_url("https://api.elections.kalshi.com/trade-api/v2/portfolio/orders")
    with pytest.raises(GolfSeriesRefused):
        assert_golf_public_url(
            "https://api.elections.kalshi.com/trade-api/v2/markets?series_ticker=KXBTC15M"
        )
    with pytest.raises(GolfSeriesRefused):
        assert_golf_public_url(
            "https://api.elections.kalshi.com/trade-api/v2/markets?limit=1000&status=open"
        )
    assert_golf_public_url(
        "https://api.elections.kalshi.com/trade-api/v2/markets?series_ticker=KXPGA&status=open"
    )
    assert parse_series({"ticker": "KXBTC15M", "title": "Bitcoin", "category": "Crypto"}) is None
    assert parse_market({"ticker": "KXMV-1", "series_ticker": "", "title": "yes Chelsea"}) is None
    m = parse_market(
        {
            "ticker": "KXPGA-1",
            "series_ticker": "KXPGA",
            "title": "Will X win",
            "yes_ask_dollars": "0.12",
            "fee_multiplier": 1,
        },
        series={"series_ticker": "KXPGA", "title": "PGA Golf", "category": "Sports", "tags": ["Golf"]},
    )
    assert m is not None
    assert m["yes_ask"] == pytest.approx(0.12)


def test_catalog_drops_nongolf_dump():
    cleaned = golf_only_catalog(
        {
            "series": [
                {"ticker": "KXPGA", "title": "PGA Tour", "category": "Sports", "tags": ["Golf"]},
                {
                    "ticker": "KXLEAGUESCUPGAME",
                    "title": "Leagues Cup Game",
                    "category": "Sports",
                    "tags": ["Soccer"],
                },
            ],
            "markets": [
                {
                    "ticker": "KXMVECROSSCATEGORY-1",
                    "series_ticker": "",
                    "title": "yes Chelsea,yes Liverpool",
                },
                {
                    "ticker": "KXPGA-1",
                    "series_ticker": "KXPGA",
                    "title": "Will Scottie Scheffler win?",
                    "yes_ask": 0.08,
                },
            ],
        }
    )
    assert [s["series_ticker"] for s in cleaned["series"]] == ["KXPGA"]
    assert [m["ticker"] for m in cleaned["markets"]] == ["KXPGA-1"]


def test_fetch_catalog_is_per_series_not_global_open_book(gk_root):
    urls: list[str] = []

    def fake_get(url, *, label, ttl_seconds, refresh):
        del label, ttl_seconds, refresh
        urls.append(url)
        assert_golf_public_url(url)
        if "/series?" in url and "tags=" in url:
            return {
                "series": [
                    {
                        "ticker": "KXPGA",
                        "title": "PGA Tour",
                        "category": "Sports",
                        "tags": ["Golf"],
                        "fee_type": "quadratic",
                        "fee_multiplier": 1,
                    },
                    {
                        "ticker": "KXLEAGUESCUPGAME",
                        "title": "Leagues Cup Game",
                        "category": "Sports",
                        "tags": ["Soccer"],
                    },
                ]
            }
        if "series_ticker=KXPGA" in url:
            return {
                "markets": [
                    {
                        "ticker": "KXPGA-1",
                        "series_ticker": "KXPGA",
                        "title": "Will Scottie Scheffler win?",
                        "yes_ask": 0.08,
                        "status": "open",
                    }
                ]
            }
        return {"series": [], "markets": []}

    feed = GolfKalshiFeed()
    feed._get = fake_get  # noqa: SLF001
    catalog = feed.fetch_catalog(refresh=True)
    assert catalog["series"][0]["series_ticker"] == "KXPGA"
    assert [m["ticker"] for m in catalog["markets"]] == ["KXPGA-1"]
    assert all("limit=1000" not in u for u in urls)
    assert all(("/markets?" not in u) or ("series_ticker=" in u) for u in urls)
    assert any("series_ticker=KXPGA" in u for u in urls)
    assert any("status=settled" in u for u in urls)


def test_tick_decides_open_markets_only(gk_root):
    from golf_offshoot.golf_kalshi.adapter import SETTLED_MAX_PAGES

    assert SETTLED_MAX_PAGES == 1
    catalog = {
        "markets": [
            _market(ticker="SETTLED-1", status="settled", result="no"),
            _market(ticker="NOQUOTE", yes_ask=None),
            _market(),
        ]
    }
    out = run_tick(brain=_brain(), executor=PaperExecutor(), catalog=catalog)
    assert out["catalog_markets"] == 3
    assert out["markets"] == 2
    assert out["fills"] == 1
    assert out["skip_reasons"].get("no_quote") == 1
    assert "SETTLED-1" not in str(out.get("skip_reasons") or {})
    led = load_ledger()
    assert any(t.get("ticker") == "KXPGA-26-SSCHEFF" and t.get("status") == "open" for t in led["tickets"])
    assert not any(t.get("ticker") == "SETTLED-1" for t in led["tickets"])


def test_lane_switch_is_at_top_not_in_extras(gk_root, tmp_path):
    golf = render_html(build_surface(artifact_root=tmp_path, viz_root=tmp_path / "viz", lane="golf"))
    page = render_html(
        build_surface(artifact_root=tmp_path, viz_root=tmp_path / "viz", lane="learning_lane_15m")
    )
    for html_page in (golf, page):
        assert html_page.count('<form class="row lane-form"') == 1
        assert html_page.count("<fieldset><legend>Lane</legend>") == 1
        assert html_page.index('class="lane-switch"') < html_page.index("<main>")
        extras = html_page[html_page.index('id="extras"') :]
        assert "lane-form" not in extras
    assert golf.index('class="lane-switch"') < golf.index('id="golf-kalshi"')
    assert "no open tickets" in golf
    assert "Catalog Open markets are not paper tickets" in golf
    assert page.index('class="lane-switch"') < page.index("Operator extras")


def test_golf_kalshi_does_not_import_polymarket():
    pkg = Path(__file__).resolve().parents[1] / "src" / "golf_offshoot" / "golf_kalshi"
    for path in pkg.glob("*.py"):
        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith(("import ", "from ")):
                assert "polymarket" not in stripped.lower()


def test_unmatched_and_no_field_skip(gk_root):
    book = empty_ledger()
    d = decide_golf(_market(), book, recipe_v1(), StaticBrain({}, {}))
    assert d.action == "skip"
    assert d.reason == "no_field"
    deferred = decide_golf(
        _market(),
        book,
        recipe_v1(),
        StaticBrain({normalize_name("Scottie Scheffler"): "scottie"}, {}, field_gate="field_deferred"),
    )
    assert deferred.action == "skip"
    assert deferred.reason == "field_deferred"
    assert deferred.reason != "no_field"
    d2 = decide_golf(_market(), book, recipe_v1(), StaticBrain({normalize_name("rory mcilroy"): "rory"}, {}))
    assert d2.action == "skip"
    assert d2.reason == "unmatched"
    assert d2.quarantine is not None


def test_sleeve_slow_cap_and_same_player(gk_root):
    rec = recipe_v1()
    book = empty_ledger(rec)
    book["tickets"] = [
        {
            "ticker": "OLD-SLOW",
            "player_id": "other",
            "sleeve": "slow",
            "stake": 300.0,
            "status": "open",
        }
    ]
    slow = _market(title="Will Scottie Scheffler win a major this year?")
    assert classify_sleeve(slow) == "slow"
    slow_brain = StaticBrain(
        {normalize_name("Scottie Scheffler"): "scottie"},
        {"scottie": {"season": 0.22, "win": 0.22}},
    )
    d = decide_golf(slow, book, rec, slow_brain)
    assert d.action == "skip"
    assert d.reason == "sleeve_slow_cap"

    book2 = empty_ledger(rec)
    book2["tickets"] = [
        {
            "ticker": "FIRST",
            "player_id": "scottie",
            "sleeve": "week",
            "stake": 50.0,
            "status": "open",
        }
    ]
    d2 = decide_golf(_market(ticker="KXPGA-26-CUT"), book2, rec, _brain())
    assert d2.action == "skip"
    assert d2.reason == "same_player_cap"


def test_fill_stamps_decision_quote(gk_root):
    d = decide_golf(_market(), empty_ledger(), recipe_v1(), _brain())
    assert d.action == "fill"
    assert d.quote.get("yes_ask") == pytest.approx(0.08)
    assert "declared_at" in d.quote
    assert d.quote.get("fee") is not None
    PaperExecutor().book(d)
    led = load_ledger()
    ticket = led["tickets"][0]
    assert ticket["quote"]["yes_ask"] == pytest.approx(0.08)
    assert ticket["quote"]["declared_at"]
    assert "learning_lane_15m" not in str(ledger_path())


def test_halt_skips_fills_and_still_settles(gk_root):
    rec = recipe_v1()
    book = empty_ledger(rec)
    book["bankroll"] = 900.0
    book["peak_bankroll"] = 1000.0
    book["halted"] = True
    book["halt_reason"] = "drawdown"
    book["tickets"] = [
        {
            "ticker": "OPEN-1",
            "player_id": "rory",
            "sleeve": "week",
            "stake": 10.0,
            "yes_ask": 0.5,
            "fee": 0.01,
            "quote": {"yes_ask": 0.5, "fee_multiplier": 1.0},
            "status": "open",
        }
    ]
    save_ledger(book)
    catalog = {
        "markets": [
            _market(),
            _market(ticker="OPEN-1", result="no", yes_ask=0.5, fee_multiplier=1.0),
        ]
    }
    out = run_tick(brain=_brain(), executor=PaperExecutor(), catalog=catalog)
    assert out["consulted_decide"] is True
    led = load_ledger()
    assert led.get("halted") is True
    settled = [t for t in led["tickets"] if t.get("ticker") == "OPEN-1"][0]
    assert settled["status"] == "paper_lose"
    assert not any(t.get("ticker") == "KXPGA-26-SSCHEFF" and t.get("status") == "open" for t in led["tickets"])


def test_espn_finish_is_not_a_settle(gk_root):
    ticket = {"ticker": "X", "stake": 10, "yes_ask": 0.5, "status": "open"}
    with pytest.raises(SettleError):
        apply_kalshi_result(ticket, kalshi_result="", espn_finish=1)
    pending = apply_kalshi_result(ticket, kalshi_result="")
    assert pending["status"] == "SETTLE_PENDING"


def test_decide_same_on_paper_and_fake_live(gk_root):
    book = empty_ledger()
    a = decide_golf(_market(), book, recipe_v1(), _brain())
    b = decide_golf(_market(), book, recipe_v1(), _brain(), live_scale=1.0)
    assert a.action == b.action
    assert a.stake == b.stake
    assert a.reason == b.reason


def test_unarmed_never_orders_live_scale_haircut(gk_root):
    d = decide_golf(_market(), empty_ledger(), recipe_v1(), _brain())
    PaperExecutor().book(d)
    live = LiveExecutor(transport=None)
    with pytest.raises(UnarmedError):
        live.book(d)
    transport = RecordingTransport()
    trading_armed_path().write_text("1\n", encoding="utf-8")
    live2 = LiveExecutor(transport=transport)
    d2 = decide_golf(_market(ticker="KXPGA-26-B"), empty_ledger(), recipe_v1(), _brain(), live_scale=0.1)
    live2.book(d2)
    assert transport.calls
    assert transport.calls[0]["stake"] == pytest.approx(d2.stake)
    assert "/orders" not in str(transport.calls)


def test_budget_still_settles(gk_root):
    rec = recipe_v1()
    book = empty_ledger(rec)
    book["tickets"] = [
        {
            "ticker": "OPEN-1",
            "player_id": "rory",
            "sleeve": "week",
            "stake": 10.0,
            "yes_ask": 0.4,
            "quote": {"yes_ask": 0.4, "fee_multiplier": 1.0},
            "status": "open",
        }
    ]
    save_ledger(book)
    markets = [_market(ticker="OPEN-1", result="no", yes_ask=0.4)] + [
        _market(ticker=f"KX-JUNK-{i}", title="Will Nobody win the Masters?") for i in range(40)
    ]
    out = run_tick(
        brain=_brain(),
        executor=PaperExecutor(),
        catalog={"markets": markets},
        budget=TickBudget(seconds=30, max_fills=0),
    )
    assert out["settle"]["joined"] == 1
    led = load_ledger()
    assert load_ledger()["tickets"][0]["status"] == "paper_lose"


def test_kill_file_stops_golf_only(gk_root, monkeypatch):
    watch_kill_path().write_text("1\n", encoding="utf-8")
    popped = []
    monkeypatch.setattr("golf_offshoot.golf_kalshi.watch.subprocess.Popen", lambda *a, **k: popped.append(1) or SimpleNamespace(pid=1, poll=lambda: None))
    assert start_sidecar_process() is None
    assert popped == []
    out = run_tick(brain=_brain(), executor=PaperExecutor(), catalog={"markets": [_market()]})
    assert out["killed"] is True
    assert out["fills"] == 0


def test_hub_start_starts_all_watches_on_golf_lane(monkeypatch):
    started = []

    class FakeWatch:
        def start(self):
            started.append("15m")

        def stop_watch(self):
            started.append("15m-stop")

    honer = []
    golf = []
    monkeypatch.setattr("golf_offshoot.operator_surface.app.PaperWatch", lambda on_cycle=None: FakeWatch())
    monkeypatch.setattr(
        "golf_offshoot.operator_surface.app._sync_honer_watch",
        lambda state, running: honer.append(running),
    )
    monkeypatch.setattr(
        "golf_offshoot.operator_surface.app._sync_golf_watch",
        lambda state, running: golf.append(running),
    )
    state = {"lane": "golf", "paper_watch": None}
    _sync_paper_watch(state)
    assert started == ["15m"]
    assert honer == [True]
    assert golf == [True]


def test_golf_html_is_observation_board(gk_root, tmp_path):
    page = render_html(build_surface(artifact_root=tmp_path, viz_root=tmp_path / "viz", lane="golf"))
    assert "Golf (Kalshi)" in page
    assert "Watch" in page
    assert "Clock" in page
    assert "Bankroll" in page
    assert "Open tickets" in page
    assert "Paper tickets" in page
    assert "Closed" in page
    assert "Closed tickets" in page
    assert "Previous golf claim" in page
    assert "Ranked table — latest real live run" not in page
    assert "Still unmeasured" not in page
    assert page.count('class="hard-no"') == 0
    assert "never_auto_bet" not in page
    assert 'value="paper-deposit"' not in page
    assert 'value="place"' not in page
    assert lane_header_name("golf") == "Golf (Kalshi)"


def test_catalog_is_tour_tree_not_flat_list(gk_root):
    from golf_offshoot.golf_kalshi.adapter import save_catalog
    from golf_offshoot.golf_kalshi.catalog_view import catalog_family, group_catalog
    from golf_offshoot.golf_kalshi.hub import board_html

    assert catalog_family("KXPGAR3LEAD") == "PGA Tour"
    assert catalog_family("KXLIVTOP10") == "LIV"
    assert catalog_family("KXDPWTTOP10") == "DP World"
    tree = group_catalog(
        [
            {"series_ticker": "KXPGAR3LEAD", "title": "Round 3 leader", "tags": ["Golf"]},
            {"series_ticker": "KXLIVTOP10", "title": "Liv Top 10", "tags": ["Golf"]},
        ],
        [
            {
                "ticker": "KXPGA-A",
                "series_ticker": "KXPGAR3LEAD",
                "title": "Player A leads at the end of Round 3",
                "yes_sub_title": "Player A",
                "status": "open",
                "in_play": True,
            },
            {
                "ticker": "KXPGA-B",
                "series_ticker": "KXPGAR3LEAD",
                "title": "Player B leads",
                "status": "settled",
                "result": "no",
            },
            {
                "ticker": "KXLIV-1",
                "series_ticker": "KXLIVTOP10",
                "title": "Player C top 10",
                "status": "open",
            },
        ],
        {"KXPGA-A"},
    )
    names = [f["name"] for f in tree["families"]]
    assert names[0] == "PGA Tour"
    assert "LIV" in names
    assert tree["series_n"] == 2
    assert tree["open_n"] == 2
    assert tree["settled_n"] == 1
    save_catalog(
        {
            "series": [
                {"ticker": "KXPGAR3LEAD", "title": "Round 3 leader", "category": "Sports", "tags": ["Golf"]},
                {"ticker": "KXLIVTOP10", "title": "Liv Top 10", "category": "Sports", "tags": ["Golf"]},
            ],
            "markets": [
                {
                    "ticker": "KXPGA-A",
                    "series_ticker": "KXPGAR3LEAD",
                    "title": "Player A leads at the end of Round 3",
                    "yes_sub_title": "Player A",
                    "status": "open",
                    "in_play": True,
                },
                {
                    "ticker": "KXLIV-1",
                    "series_ticker": "KXLIVTOP10",
                    "title": "Player C top 10",
                    "status": "open",
                },
            ],
        }
    )
    page = board_html()
    assert 'class="gk-family"' in page
    assert 'class="gk-series"' in page
    assert "PGA Tour" in page
    assert "LIV" in page
    assert "KXPGAR3LEAD" in page
    assert "KXLIVTOP10" in page
    assert "KXPGA-A" not in page
    assert "KXLIV-1" not in page
    assert "Player A" not in page
    assert 'data-series="KXPGAR3LEAD"' in page
    assert 'class="gk-family" open' not in page
    assert 'class="gk-series" open' not in page
    assert 'class="gk-unmatched"' in page
    assert 'class="gk-unmatched" open' not in page
    from golf_offshoot.golf_kalshi.hub import series_fragment_html, unmatched_fragment_html
    from golf_offshoot.golf_kalshi.paths import unmatched_path

    fragment = series_fragment_html("KXPGAR3LEAD")
    assert fragment is not None
    assert "KXPGA-A" in fragment
    assert "Player A" in fragment
    assert series_fragment_html("KXBTC15M") is None
    unmatched_path().write_text(
        json.dumps({"lane": "golf_kalshi", "rows": [{"player": "Nobody Here", "ticker": "KX-JUNK-1", "reason": "no_field"}]}),
        encoding="utf-8",
    )
    assert "Nobody Here" not in board_html()
    assert "Nobody Here" in unmatched_fragment_html()


def test_golf_get_same_lane_does_not_rebuild(monkeypatch):
    rebuilt: list[int] = []
    monkeypatch.setattr(
        "golf_offshoot.operator_surface.app.rebuild_surface",
        lambda state, **kwargs: rebuilt.append(1),
    )
    monkeypatch.setattr("golf_offshoot.operator_surface.app._sync_paper_watch", lambda state: None)
    state = {"lane": "golf", "surface": {}}
    assert apply_request_lane(state, "golf") is False
    assert rebuilt == []


def test_dispatch_does_not_write_phase1_paper(gk_root, tmp_path, monkeypatch):
    from golf_offshoot.operator_surface.app import _dispatch

    calls = []
    monkeypatch.setattr(
        "golf_offshoot.operator_surface.runner.run_operating",
        lambda **kwargs: calls.append(kwargs) or (_ for _ in ()).throw(RuntimeError("no")),
    )
    monkeypatch.setattr(
        "golf_offshoot.golf_kalshi.loop.run_tick",
        lambda **kwargs: {"summary": "ok", "fills": 0, "skips": 0, "consulted_decide": True},
    )
    rec = _dispatch("loop", "401811963", {"lane": "golf", "odds_book": "polymarket"})
    assert rec.extras.get("lane") == "golf_kalshi"
    assert calls == []
    phase1 = Path(__file__).resolve().parents[1] / "data" / "paper" / "ledger.json"
    assert "golf_kalshi" in str(ledger_path())
    assert phase1 != ledger_path()


def test_first_tick_consults_decide(gk_root):
    out = run_tick(brain=_brain(), executor=PaperExecutor(), catalog={"markets": [_market()]})
    assert out["consulted_decide"] is True
    assert out["decisions"] >= 1


def test_learn_clocks_not_pnl(gk_root):
    from golf_offshoot.golf_kalshi.learn import maybe_promote, recipe_exam

    exam = recipe_exam()
    assert exam["not_pnl_ranked"] is True
    assert exam["promote_by"] == "declared_at"
    out = maybe_promote(holdout_beats_expert=False)
    assert out["brain_score"]["production"] == "keep_expert"
    assert out["brain_score"]["promote"] is False


def test_espn_leagues_are_not_pga_only():
    from golf_offshoot.golf_kalshi.espn_bind import leagues_for_family, titles_bind

    src = Path(__file__).resolve().parents[1] / "src" / "golf_offshoot" / "data_feeds" / "espn.py"
    text = src.read_text(encoding="utf-8")
    assert "league=pga" in text
    assert "def leaderboard_for_league" in text
    assert leagues_for_family("DP World") == ("eur",)
    assert leagues_for_family("LIV")[0] == "liv"
    assert leagues_for_family("LPGA") == ("lpga",)
    assert titles_bind("DP World Tour Championship", "DP World Tour Championship")
    assert not titles_bind("PGA Tour Players", "Chevron Championship")
    assert "def leaderboard_for_league" in text


def test_maybe_refresh_writes_probs_once(gk_root, monkeypatch):
    from golf_offshoot.golf_kalshi.brain import CachedExpertBrain

    hunt = {
        "event_key": "KXPGA-26",
        "espn_id": "401",
        "espn_name": "Masters",
        "family": "PGA Tour",
        "field_source": "espn",
        "names": ["Scottie Scheffler"],
        "n_names": 1,
        "n_recovered": 1,
        "candidates": {normalize_name("Scottie Scheffler"): "pid"},
        "listed_candidates": {},
        "espn_rows": [{"id": "pid", "score": -4, "thru": 18, "name": "Scottie Scheffler"}],
        "thin": False,
        "tried_leagues": ["pga"],
    }
    runs: list[str] = []

    def fake_hunt(*_a, **_k):
        return hunt

    def fake_score(espn_id, **_k):
        runs.append(str(espn_id))
        return {
            "probs": {"pid": {"win": 0.2}},
            "candidates": hunt["candidates"],
            "fp": "ignored",
            "field_source": "espn",
            "n_players": 1,
        }

    monkeypatch.setattr("golf_offshoot.golf_kalshi.field_hunt.hunt_field", fake_hunt)
    monkeypatch.setattr("golf_offshoot.golf_kalshi.score.score_espn_event", fake_score)
    monkeypatch.setattr("golf_offshoot.golf_kalshi.score.live_scoreboard_fp", lambda *_a, **_k: "ignored")
    brain = CachedExpertBrain()
    brain.maybe_refresh("KXPGA-26", "", markets=[_market()])
    brain.maybe_refresh("KXPGA-26", "", markets=[_market()])
    assert runs == ["401"]
    assert brain.model_p("pid", "win", event_key="KXPGA-26") == pytest.approx(0.2)
    assert brain.field_source("KXPGA-26") == "espn"


def test_espn_miss_uses_kalshi_listed_names(gk_root, monkeypatch):
    from golf_offshoot.golf_kalshi.espn_bind import reset_league_probe
    from golf_offshoot.golf_kalshi.field_hunt import hunt_field

    reset_league_probe()
    monkeypatch.setattr(
        "golf_offshoot.golf_kalshi.espn_bind.bind_espn_event",
        lambda *a, **k: {
            "espn_id": "",
            "espn_name": "",
            "league": "",
            "family": "LIV",
            "field_source": "",
            "espn_rows": [],
            "candidates": {},
            "tried_leagues": ["liv", "pga"],
        },
    )

    class Hist:
        def prior(self, before, exclude_event_id=None):
            del before, exclude_event_id
            return [
                SimpleNamespace(
                    finishes=[
                        SimpleNamespace(name="Jon Rahm", player_id="1"),
                        SimpleNamespace(name="Brooks Koepka", player_id="2"),
                    ]
                )
            ]

    markets = [
        _market(
            ticker="KXLIV-1",
            event_ticker="KXLIV-26",
            series_ticker="KXLIV",
            yes_sub_title="Jon Rahm",
        ),
        _market(
            ticker="KXLIV-2",
            event_ticker="KXLIV-26",
            series_ticker="KXLIV",
            yes_sub_title="Brooks Koepka",
        ),
    ]
    hunt = hunt_field("KXLIV-26", markets, history=Hist())
    assert hunt["field_source"] == "kalshi_listed"
    assert hunt["thin"] is False
    assert hunt["n_recovered"] >= 2


def test_history_id_floor_blocks_paper_fill(gk_root, monkeypatch):
    from golf_offshoot.golf_kalshi.brain import CachedExpertBrain
    from golf_offshoot.golf_kalshi.field_hunt import history_floor_ok, hunt_field

    assert history_floor_ok(4, 1) is False
    assert history_floor_ok(4, 2) is True
    assert history_floor_ok(50, 20) is True
    monkeypatch.setattr(
        "golf_offshoot.golf_kalshi.espn_bind.bind_espn_event",
        lambda *a, **k: {
            "espn_id": "",
            "espn_name": "",
            "league": "",
            "family": "LIV",
            "espn_rows": [],
            "candidates": {},
            "tried_leagues": ["liv"],
        },
    )

    class Hist:
        def prior(self, before, exclude_event_id=None):
            del before, exclude_event_id
            return [SimpleNamespace(finishes=[SimpleNamespace(name="Alpha Player", player_id="1")])]

    markets = [
        _market(ticker=f"T{i}", event_ticker="KXLIV-1", series_ticker="KXLIV", yes_sub_title=name)
        for i, name in enumerate(["Alpha Player", "Bravo Player", "Charlie Player", "Delta Player"])
    ]
    hunt = hunt_field("KXLIV-1", markets, history=Hist())
    assert hunt["thin"] is True
    assert hunt["n_recovered"] == 1
    assert normalize_name("Alpha Player") in hunt["candidates"]
    assert len(hunt["candidates"]) == 4
    monkeypatch.setattr("golf_offshoot.golf_kalshi.field_hunt.hunt_field", lambda *a, **k: hunt)
    monkeypatch.setattr(
        "golf_offshoot.golf_kalshi.score.shared_ingestor",
        lambda: SimpleNamespace(load_history=lambda **k: Hist()),
    )
    brain = CachedExpertBrain()
    brain.maybe_refresh("KXLIV-1", "", markets=markets)
    d = decide_golf(markets[0], empty_ledger(), recipe_v1(), brain)
    assert d.action == "skip"
    assert d.reason == "thin"
    assert d.reason != "no_field"


def test_deferred_listed_keeps_candidates_not_no_field(gk_root, monkeypatch):
    from golf_offshoot.golf_kalshi.brain import CachedExpertBrain

    names = [
        "Alpha Player",
        "Bravo Player",
        "Charlie Player",
    ]
    hunt = {
        "event_key": "KXCHAMPIONSSAI-26",
        "espn_id": "",
        "espn_name": "",
        "family": "Champions",
        "field_source": "kalshi_listed",
        "names": names,
        "n_names": len(names),
        "n_recovered": 0,
        "candidates": {},
        "listed_candidates": {},
        "espn_rows": [],
        "thin": False,
        "awaiting_history": True,
        "tried_leagues": ["champ"],
    }
    monkeypatch.setattr("golf_offshoot.golf_kalshi.field_hunt.hunt_field", lambda *a, **k: hunt)
    monkeypatch.setattr(
        "golf_offshoot.golf_kalshi.score.shared_ingestor",
        lambda: SimpleNamespace(load_history=lambda **k: (_ for _ in ()).throw(AssertionError("history"))),
    )
    markets = [
        _market(
            ticker=f"SAI-{i}",
            event_ticker="KXCHAMPIONSSAI-26",
            series_ticker="KXCHAMPIONSSAI",
            yes_sub_title=name,
            title=f"Will {name} win the Senior i?",
        )
        for i, name in enumerate(names)
    ]
    brain = CachedExpertBrain()
    spent = TickBudget(seconds=0.0, max_fills=8, max_brain=2)
    brain.maybe_refresh("KXCHAMPIONSSAI-26", "", budget=spent, markets=markets)
    row = ((brain._cache.get("events") or {}).get("KXCHAMPIONSSAI-26") or {})
    assert row.get("deferred") is True
    assert row.get("thin") is not True
    kept = brain.field_candidates("KXCHAMPIONSSAI-26")
    assert len(kept) == 3
    assert normalize_name("Alpha Player") in kept
    d = decide_golf(markets[0], empty_ledger(), recipe_v1(), brain)
    assert d.action == "skip"
    assert d.reason == "field_deferred"
    assert d.reason != "no_field"


def test_thin_listed_field_candidates_not_empty(gk_root):
    from golf_offshoot.golf_kalshi.brain import CachedExpertBrain

    brain = CachedExpertBrain()
    brain._cache = {
        "events": {
            "SAI26": {
                "names": ["Alpha Player", "Bravo Player"],
                "n_names": 2,
                "candidates": {},
                "thin": True,
                "probs": {},
                "field_source": "kalshi_listed",
            }
        }
    }
    kept = brain.field_candidates("SAI26")
    assert normalize_name("Alpha Player") in kept
    d = decide_golf(
        _market(event_ticker="SAI26", series_ticker="SAI26", yes_sub_title="Alpha Player"),
        empty_ledger(),
        recipe_v1(),
        brain,
    )
    assert d.reason == "thin"
    assert d.reason != "no_field"


def test_tick_writes_skip_reason_counts_not_per_market_files(gk_root):
    from golf_offshoot.golf_kalshi.paths import decisions_path

    markets = [
        _market(ticker=f"KX-JUNK-{i}", yes_sub_title="Nobody Here", title="Will Nobody Here win?")
        for i in range(40)
    ]
    out = run_tick(brain=_brain(), executor=PaperExecutor(), catalog={"markets": markets})
    assert out["skips"] == 40
    payload = json.loads(decisions_path().read_text(encoding="utf-8"))
    assert payload["skip_reasons"].get("unmatched") == 40
    assert "decisions" not in payload
    assert len(payload.get("fills") or []) == 0


def test_no_name_and_season_long_skip(gk_root):
    from golf_offshoot.golf_kalshi.sleeves import market_horizon

    d = decide_golf(
        _market(yes_sub_title="The Field", title="Will the field win the Masters?"),
        empty_ledger(),
        recipe_v1(),
        _brain(),
    )
    assert d.action == "skip"
    assert d.reason == "unmatched"
    season = _market(title="Will Scottie Scheffler win a major this year?")
    assert market_horizon(season) == "season"
    d2 = decide_golf(season, empty_ledger(), recipe_v1(), _brain())
    assert d2.reason == "no_model_p"


def test_listed_field_haircut_and_field_source_stamp(gk_root):
    espn = decide_golf(_market(), empty_ledger(), recipe_v1(), _brain())
    listed_brain = StaticBrain(
        {normalize_name("Scottie Scheffler"): "scottie"},
        {"scottie": {"win": 0.22}},
        field_source="kalshi_listed",
    )
    listed = decide_golf(_market(ticker="KXPGA-26-B"), empty_ledger(), recipe_v1(), listed_brain)
    assert espn.action == "fill"
    assert listed.action == "fill"
    assert listed.model_p == pytest.approx(espn.model_p * 0.5)
    assert listed.stake < espn.stake
    assert listed.field_source == "kalshi_listed"
    PaperExecutor().book(listed)
    ticket = load_ledger()["tickets"][0]
    assert ticket["field_source"] == "kalshi_listed"


def test_score_include_odds_false_no_operating_no_provisional():
    pkg = Path(__file__).resolve().parents[1] / "src" / "golf_offshoot" / "golf_kalshi"
    score = (pkg / "score.py").read_text(encoding="utf-8")
    assert "include_odds=False" in score
    assert "run_operating(" not in score
    for path in pkg.glob("*.py"):
        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith(("import ", "from ")):
                assert "list_provisional_names" not in stripped
                assert "polymarket" not in stripped.lower()


def test_golf_hub_has_idle_farm_honer(gk_root, tmp_path, monkeypatch):
    def boom(*_a, **_k):
        raise AssertionError("MC")

    monkeypatch.setattr("golf_offshoot.operating.make_engine", boom)
    page = render_html(build_surface(artifact_root=tmp_path, viz_root=tmp_path / "viz", lane="golf"))
    assert 'id="golf-farm"' in page
    assert 'id="golf-honer"' in page
    assert "no golf tape yet" not in page
    assert "No golf Farm notebooks" in page
    assert "Home has no paper tickets yet" in page
    assert "Golf Honer is not consulting" in page
    assert '<section class="panel farm-sandbox" id="farm">' not in page
    assert '<section class="panel honer-sandbox" id="honer">' not in page
    assert "R-SKIP-HOUR-CLOSE" not in page
    assert "R-SKIP-2TO1" not in page
    assert "R-SKIP-COINFLIP" not in page
    assert "Field hunt:" in page


def test_golf_tick_does_not_write_phase1_paper(gk_root, monkeypatch):
    called = []
    monkeypatch.setattr(
        "golf_offshoot.operating.run_operating",
        lambda **kwargs: called.append(kwargs),
    )
    run_tick(brain=_brain(), executor=PaperExecutor(), catalog={"markets": [_market()]})
    assert called == []
    phase1 = Path(__file__).resolve().parents[1] / "data" / "paper" / "ledger.json"
    assert ledger_path() != phase1


def test_learn_listed_fills_are_observation(gk_root):
    from golf_offshoot.golf_kalshi.learn import player_brain_score
    from golf_offshoot.golf_kalshi.paper import empty_ledger, save_ledger

    book = empty_ledger()
    book["tickets"] = [
        {
            "ticker": "ESPN-1",
            "status": "paper_win",
            "model_p": 0.4,
            "field_source": "espn",
        },
        {
            "ticker": "LIST-1",
            "status": "paper_win",
            "model_p": 0.9,
            "field_source": "kalshi_listed",
        },
    ]
    save_ledger(book)
    score = player_brain_score()
    assert score["n"] == 1
    assert score["n_listed_observation"] == 1
    assert score["production"] == "keep_expert"
    assert score["promote"] is False


def test_open_is_listed_not_in_play():
    series = {"series_ticker": "KXPGA", "title": "PGA Golf", "category": "Sports", "tags": ["Golf"]}
    raw = {
        "ticker": "KXPGA-1",
        "series_ticker": "KXPGA",
        "title": "Will X win",
        "yes_ask_dollars": "0.12",
        "fee_multiplier": 1,
        "status": "open",
    }
    listed = parse_market(raw, series=series)
    live = parse_market({**raw, "can_close_early": True}, series=series)
    assert listed is not None and listed["in_play"] is False
    assert listed["can_close_early"] is False
    assert live is not None and live["in_play"] is True


def test_catalog_freshness_skips_walk(gk_root):
    from golf_offshoot.golf_kalshi.adapter import catalog_is_fresh, load_last_good_catalog, save_catalog

    save_catalog(
        {
            "series": [{"ticker": "KXPGA", "title": "PGA Tour", "category": "Sports", "tags": ["Golf"]}],
            "markets": [
                {
                    "ticker": "KXPGA-1",
                    "series_ticker": "KXPGA",
                    "title": "Will X win",
                    "status": "open",
                    "fee_multiplier": 1,
                }
            ],
        }
    )
    last = load_last_good_catalog()
    assert catalog_is_fresh(last)
    assert not catalog_is_fresh(
        {"saved_at": "2020-01-01T00:00:00-05:00", "markets": [1], "series": [1]}
    )


def test_clock_spent_still_fills_cached_p(gk_root):
    budget = TickBudget(seconds=0.0, max_fills=8, max_brain=2)
    assert budget.can_fill() is True
    assert budget.can_brain() is False
    out = run_tick(brain=_brain(), executor=PaperExecutor(), catalog={"markets": [_market()]}, budget=budget)
    assert out["fills"] == 1
    assert out["skip_reasons"].get("budget") in (None, 0)


def test_budget_miss_does_not_poison_listed_cache(gk_root, monkeypatch):
    from golf_offshoot.golf_kalshi.brain import CachedExpertBrain

    hunt = {
        "event_key": "KXLIV-1",
        "espn_id": "",
        "espn_name": "",
        "family": "LIV",
        "field_source": "kalshi_listed",
        "names": ["Alpha Player", "Bravo Player"],
        "n_names": 2,
        "n_recovered": 0,
        "candidates": {},
        "listed_candidates": {},
        "espn_rows": [],
        "thin": False,
        "awaiting_history": True,
        "tried_leagues": ["liv"],
    }
    history_calls: list[int] = []
    monkeypatch.setattr("golf_offshoot.golf_kalshi.field_hunt.hunt_field", lambda *a, **k: hunt)
    monkeypatch.setattr(
        "golf_offshoot.golf_kalshi.score.shared_ingestor",
        lambda: SimpleNamespace(load_history=lambda **k: history_calls.append(1) or []),
    )
    brain = CachedExpertBrain()
    spent = TickBudget(seconds=0.0, max_fills=8, max_brain=2)
    brain.maybe_refresh("KXLIV-1", "", budget=spent, markets=[_market(series_ticker="KXLIV")])
    assert history_calls == []
    row = ((brain._cache.get("events") or {}).get("KXLIV-1") or {})
    assert row.get("awaiting_history") is True
    assert row.get("thin") is False
    assert row.get("deferred") is True
    assert not row.get("probs")
    kept = brain.field_candidates("KXLIV-1")
    assert normalize_name("Alpha Player") in kept
    assert normalize_name("Bravo Player") in kept
    room = TickBudget(seconds=30, max_fills=8, max_brain=2)
    brain.maybe_refresh("KXLIV-1", "", budget=room, markets=[_market(series_ticker="KXLIV")])
    assert history_calls == [1]


def test_espn_boards_read_each_league_once():
    from golf_offshoot.golf_kalshi.espn_bind import EspnLeagueBoards, reset_league_probe

    reset_league_probe()
    calls: list[str] = []

    class Client:
        def leaderboard_for_league(self, league):
            calls.append(league)
            return {
                "events": [
                    {"id": "1", "name": "DP World Tour Championship", "competitions": [{"competitors": []}]}
                ]
            }

    boards = EspnLeagueBoards(client=Client())
    a = boards.bind({"series_ticker": "KXDPWORLD", "title": "DP World Tour Championship"})
    b = boards.bind({"series_ticker": "KXDPWTTOP10", "title": "DP World Tour Championship top 10"})
    assert a["espn_id"] == "1"
    assert b["espn_id"] == "1"
    assert calls == ["eur"]


def _ticket(**kwargs):
    row = {
        "ticker": "T1",
        "player_id": "scottie",
        "player": "Scottie Scheffler",
        "sleeve": "week",
        "stake": 10.0,
        "yes_ask": 0.08,
        "fee": 0.01,
        "edge_after_fee": 0.05,
        "model_p": 0.22,
        "status": "open",
        "quote": {"yes_ask": 0.08, "yes_bid": 0.07, "fee_multiplier": 1.0, "displayed_size": 500.0},
        "event_ticker": "KXPGA-26",
        "title": "Will Scottie Scheffler win the Masters?",
        "field_source": "espn",
        "recipe_id": "golf-kalshi-recipe-v1",
    }
    row.update(kwargs)
    return row


def test_week_names_share_week_slice(gk_root):
    from golf_offshoot.golf_kalshi.allocate import allocate
    from golf_offshoot.golf_kalshi.decide import screen_golf

    rec = recipe_v1()
    brain = StaticBrain(
        {
            normalize_name("Scottie Scheffler"): "scottie",
            normalize_name("Rory McIlroy"): "rory",
        },
        {"scottie": {"win": 0.22}, "rory": {"win": 0.18}},
    )
    book = empty_ledger(rec)
    a = screen_golf(_market(ticker="A"), book, rec, brain)
    b = screen_golf(
        _market(ticker="B", yes_sub_title="Rory McIlroy", title="Will Rory McIlroy win the Masters?"),
        book,
        rec,
        brain,
    )
    assert a.worthy and b.worthy
    picks, _skipped = allocate([a, b], book, rec)
    assert len(picks) == 2
    assert sum(p.stake for p in picks) <= rec.sleeve_target("week", rec.seed) + 0.01
    assert all(p.stake < 90 for p in picks)


def test_cent_longshot_picks_by_edge_inside_sleeve(gk_root):
    from golf_offshoot.golf_kalshi.allocate import allocate
    from golf_offshoot.golf_kalshi.decide import screen_golf

    rec = recipe_v1()
    brain = StaticBrain(
        {
            normalize_name("Scottie Scheffler"): "scottie",
            normalize_name("Rory McIlroy"): "rory",
        },
        {"scottie": {"win": 0.22}, "rory": {"win": 0.08}},
    )
    book = empty_ledger(rec)
    leader = screen_golf(_market(ticker="LEAD"), book, rec, brain)
    longshot = screen_golf(
        _market(
            ticker="CENT",
            yes_ask=0.01,
            yes_bid=0.01,
            yes_sub_title="Rory McIlroy",
            title="Will Rory McIlroy win the Masters?",
        ),
        book,
        rec,
        brain,
    )
    assert leader.worthy and longshot.worthy
    first = sorted(
        [leader, longshot],
        key=lambda d: (-(float(d.edge_after_fee or 0)), str(d.ticker)),
    )[0].ticker
    picks, _skipped = allocate([longshot, leader], book, rec)
    assert picks[0].ticker == first
    assert sum(p.stake for p in picks) <= rec.sleeve_target("week", rec.seed) + 0.01
    assert all(p.stake <= rec.sleeve_target("week", rec.seed) + 0.01 for p in picks)


def test_overweight_week_still_fills_fast(gk_root):
    rec = recipe_v1()
    book = empty_ledger(rec)
    book["tickets"] = [_ticket(stake=198.0, player_id="other")]
    save_ledger(book)
    fast = _market(
        ticker="FAST-1",
        title="Scottie Scheffler round 1 leader",
        yes_sub_title="Scottie Scheffler",
        event_ticker="KXPGA-R1",
    )
    brain = StaticBrain(
        {normalize_name("Scottie Scheffler"): "scottie"},
        {"scottie": {"win": 0.22, "win_after_r1": 0.22}},
    )
    out = run_tick(brain=brain, executor=PaperExecutor(), catalog={"markets": [fast, _market()]})
    led = load_ledger()
    assert any(t.get("ticker") == "FAST-1" and t.get("status") == "open" for t in led["tickets"])
    assert not any(t.get("ticker") == "KXPGA-26-SSCHEFF" and t.get("status") == "open" for t in led["tickets"])
    assert led["bankroll"] == pytest.approx(1000.0)
    assert out["fills"] >= 1


def test_event_cap_fourth_fills_when_event_dollars_under_name_cap(gk_root):
    rec = recipe_v1()
    book = empty_ledger(rec)
    book["tickets"] = [_ticket(ticker=f"E{i}", player_id=f"p{i}", stake=5.0) for i in range(3)]
    save_ledger(book)
    d = decide_golf(_market(ticker="FOURTH"), book, rec, _brain())
    assert d.action == "fill"
    bank = rec.seed
    name_cap = rec.single_name_frac * bank
    assert d.stake >= rec.min_stake
    assert 15.0 + d.stake <= name_cap + 1e-9


def test_event_cap_skips_when_event_dollars_at_name_cap(gk_root):
    rec = recipe_v1()
    book = empty_ledger(rec)
    book["tickets"] = [
        _ticket(ticker="E0", player_id="p0", stake=20.0),
        _ticket(ticker="E1", player_id="p1", stake=20.0),
        _ticket(ticker="E2", player_id="p2", stake=10.0),
    ]
    save_ledger(book)
    d = decide_golf(_market(ticker="FOURTH"), book, rec, _brain())
    assert d.action == "skip"
    assert d.reason == "mix_event_cap"
    assert sum(1 for t in book["tickets"] if t.get("status") == "open") == 3


def test_event_cap_sizes_into_remaining_event_room(gk_root):
    rec = recipe_v1()
    book = empty_ledger(rec)
    cap = rec.single_name_frac * rec.seed
    book["tickets"] = [_ticket(ticker="E0", player_id="p0", stake=cap - 2.0)]
    save_ledger(book)
    d = decide_golf(_market(ticker="FOURTH"), book, rec, _brain())
    assert d.action == "fill"
    assert d.stake == pytest.approx(2.0)


def test_dollar_event_cap_does_not_retrim_open_tickets(gk_root):
    from golf_offshoot.golf_kalshi.mark import trim_event_caps

    rec = recipe_v1()
    book = empty_ledger(rec)
    book["event_cap_trimmed"] = True
    book["tickets"] = [
        _ticket(ticker=f"E{i}", player_id=f"p{i}", stake=20.0, edge_after_fee=0.01 * i) for i in range(6)
    ]
    save_ledger(book)
    markets = {f"E{i}": _market(ticker=f"E{i}", yes_bid=0.07, displayed_size=500.0) for i in range(6)}
    exits = trim_event_caps(book, markets, _brain(), rec)
    led = load_ledger()
    assert exits == []
    open_n = sum(1 for t in led["tickets"] if t.get("status") == "open")
    assert open_n == 6
    d = decide_golf(_market(ticker="FOURTH"), led, rec, _brain())
    assert d.action == "skip"
    assert d.reason == "mix_event_cap"
    assert sum(1 for t in led["tickets"] if t.get("status") == "open") == 6


def test_recipe_bump_trims_event_cap(gk_root):
    from golf_offshoot.golf_kalshi.mark import trim_event_caps
    from golf_offshoot.golf_kalshi.recipe import PREVIOUS_RECIPE_ID

    rec = recipe_v1()
    book = empty_ledger(rec)
    book["recipe_id"] = PREVIOUS_RECIPE_ID
    book["event_cap_trimmed"] = False
    book["tickets"] = [
        _ticket(ticker=f"E{i}", player_id=f"p{i}", stake=5.0, edge_after_fee=0.01 * i) for i in range(11)
    ]
    save_ledger(book)
    markets = {f"E{i}": _market(ticker=f"E{i}", yes_bid=0.07, displayed_size=500.0) for i in range(11)}
    exits = trim_event_caps(book, markets, _brain(), rec)
    led = load_ledger()
    assert led["event_cap_trimmed"] is True
    open_n = sum(1 for t in led["tickets"] if t.get("status") == "open")
    assert open_n == 3
    assert len(exits) == 8
    assert led["bankroll"] > 0


def test_captain_restamp_to_slow(gk_root):
    from golf_offshoot.golf_kalshi.paper import restamp_open_sleeves

    rec = recipe_v1()
    book = empty_ledger(rec)
    book["tickets"] = [
        _ticket(
            ticker="CAP",
            sleeve="week",
            title="2027 Ryder Cup USA captain",
            event_ticker="KXRYDER-27",
        )
    ]
    assert classify_sleeve(book["tickets"][0]) == "slow"
    restamp_open_sleeves(book)
    assert book["tickets"][0]["sleeve"] == "slow"
    assert book["sleeves"]["slow"] > 0
    assert book["sleeves"]["week"] == 0


def test_pretee_hold_and_in_play_collapse(gk_root):
    from golf_offshoot.golf_kalshi.mark import apply_paper_exit, mark_ticket, path_action

    rec = recipe_v1()
    ticket = _ticket(edge_after_fee=0.10)
    market = _market(yes_ask=0.40, yes_bid=0.38, in_play=False)
    brain = StaticBrain(
        {normalize_name("Scottie Scheffler"): "scottie"},
        {"scottie": {"win": 0.02}},
        event_started=False,
    )
    mark = mark_ticket(ticket, market, brain, rec)
    assert mark["golf_started"] is False
    assert path_action(mark, halted=False) is None
    live = _market(yes_ask=0.40, yes_bid=0.38, in_play=True)
    started = StaticBrain(
        {normalize_name("Scottie Scheffler"): "scottie"},
        {"scottie": {"win": 0.02}},
        event_started=True,
        holes={"scottie": 12},
    )
    mark2 = mark_ticket(ticket, live, started, rec)
    assert mark2["golf_started"] is True
    assert mark2["collapsed"] is True
    assert path_action(mark2, halted=False) == "edge_collapsed"
    book = empty_ledger(rec)
    book["tickets"] = [ticket]
    save_ledger(book)
    closed = apply_paper_exit(ticket, live, reason="edge_collapsed", ledger=book)
    assert closed is not None
    assert closed["status"] == "paper_exit"
    assert closed["exit_reason"] == "edge_collapsed"
    tiny = _market(yes_ask=0.40, yes_bid=0.38, displayed_size=0.0, in_play=True)
    book2 = empty_ledger(rec)
    book2["tickets"] = [_ticket()]
    save_ledger(book2)
    assert apply_paper_exit(_ticket(), tiny, reason="edge_collapsed", ledger=book2) is None


def test_reallocate_when_cap_binds_else_keep_both(gk_root):
    from golf_offshoot.golf_kalshi.allocate import allocate
    from golf_offshoot.golf_kalshi.decide import screen_golf
    from golf_offshoot.golf_kalshi.loop import _maybe_reallocate

    rec = recipe_v1()
    brain = StaticBrain(
        {
            normalize_name("Scottie Scheffler"): "scottie",
            normalize_name("Rory McIlroy"): "rory",
        },
        {"scottie": {"win": 0.22}, "rory": {"win": 0.30}},
    )
    room = empty_ledger(rec)
    a = screen_golf(_market(ticker="KEEP"), room, rec, brain)
    b = screen_golf(
        _market(ticker="NEW", yes_sub_title="Rory McIlroy", title="Will Rory McIlroy win the Masters?"),
        room,
        rec,
        brain,
    )
    picks, _ = allocate([a, b], room, rec)
    assert len(picks) == 2
    book = empty_ledger(rec)
    book["tickets"] = [_ticket(ticker="OLD", stake=100.0, edge_after_fee=0.02, player_id="other")]
    save_ledger(book)
    new = screen_golf(
        _market(ticker="BETTER", yes_sub_title="Rory McIlroy", title="Will Rory McIlroy win the Masters?"),
        book,
        rec,
        brain,
    )
    assert new.worthy
    marks = {"OLD": {"live_edge": 0.01}}
    markets = {"OLD": _market(ticker="OLD", yes_bid=0.07, displayed_size=5000)}
    assert _maybe_reallocate(new, book, rec, marks, markets) is True
    led = load_ledger()
    assert any(t.get("ticker") == "OLD" and t.get("status") == "paper_exit" for t in led["tickets"])
    assert any(t.get("exit_reason") == "mix_reallocate" for t in led["tickets"])


def test_add_when_improved_not_when_overweight(gk_root):
    from golf_offshoot.golf_kalshi.mark import mark_ticket, path_action

    rec = recipe_v1()
    ticket = _ticket(edge_after_fee=0.04, stake=10.0)
    brain = StaticBrain(
        {normalize_name("Scottie Scheffler"): "scottie"},
        {"scottie": {"win": 0.40}},
        event_started=True,
        holes={"scottie": 9},
    )
    mark = mark_ticket(ticket, _market(yes_ask=0.08, in_play=True), brain, rec)
    assert mark["improved"] is True
    assert path_action(mark, halted=False) == "add"
    book = empty_ledger(rec)
    book["tickets"] = [_ticket(stake=198.0)]
    save_ledger(book)
    out = run_tick(
        brain=_brain(),
        executor=PaperExecutor(),
        catalog={"markets": [_market(ticker="WEEK-NEW")]},
    )
    assert out["adds"] == 0


def test_fast_fail_clock_and_pop(gk_root):
    from golf_offshoot.golf_kalshi.mark import apply_paper_exit, mark_ticket, path_action

    rec = recipe_v1()
    ticket = _ticket(
        ticker="FAST",
        sleeve="fast",
        stake=10.0,
        yes_ask=0.20,
        title="Scottie Scheffler round 1 leader",
        quote={"yes_ask": 0.20, "yes_bid": 0.19, "fee_multiplier": 1.0, "displayed_size": 500.0},
    )
    brain = StaticBrain(
        {normalize_name("Scottie Scheffler"): "scottie"},
        {"scottie": {"win_after_r1": 0.22, "win": 0.22}},
        event_started=True,
        holes={"scottie": 18},
    )
    market = _market(
        ticker="FAST",
        title="Scottie Scheffler round 1 leader",
        yes_ask=0.20,
        yes_bid=0.19,
        in_play=True,
    )
    mark = mark_ticket(ticket, market, brain, rec)
    assert mark["fail_clock"] is True
    assert path_action(mark, halted=False) == "flip_fail"
    pop_market = dict(market)
    pop_market["yes_bid"] = 0.28
    mark_pop = mark_ticket(ticket, pop_market, brain, rec)
    assert mark_pop["pop"] is True
    assert path_action(mark_pop, halted=False) == "flip_pop"
    book = empty_ledger(rec)
    book["tickets"] = [ticket]
    save_ledger(book)
    closed = apply_paper_exit(ticket, pop_market, reason="flip_pop", ledger=book)
    assert closed["exit_reason"] == "flip_pop"


def test_halt_collapses_but_does_not_add(gk_root):
    rec = recipe_v1()
    book = empty_ledger(rec)
    book["halted"] = True
    book["halt_reason"] = "drawdown"
    book["tickets"] = [_ticket(stake=10.0, edge_after_fee=0.10, yes_ask=0.08)]
    save_ledger(book)
    brain = StaticBrain(
        {normalize_name("Scottie Scheffler"): "scottie"},
        {"scottie": {"win": 0.02}},
        event_started=True,
        holes={"scottie": 12},
    )
    catalog = {"markets": [_market(yes_ask=0.40, yes_bid=0.38, in_play=True, displayed_size=500.0)]}
    out = run_tick(brain=brain, executor=PaperExecutor(), catalog=catalog)
    led = load_ledger()
    assert led.get("halted") is True
    assert any(t.get("status") == "paper_exit" and t.get("exit_reason") == "edge_collapsed" for t in led["tickets"])
    assert out["adds"] == 0
    assert out["fills"] == 0


def test_brier_ignores_paper_exit_and_promote_on_join(gk_root):
    from golf_offshoot.golf_kalshi.learn import player_brain_score
    from golf_offshoot.golf_kalshi.paths import brain_score_path

    rec = recipe_v1()
    book = empty_ledger(rec)
    book["tickets"] = [
        _ticket(ticker="WIN", status="paper_win", field_source="espn", model_p=0.22),
        _ticket(
            ticker="EXIT",
            status="paper_exit",
            field_source="espn",
            model_p=0.22,
            exit_reason="edge_collapsed",
        ),
    ]
    save_ledger(book)
    score = player_brain_score()
    assert score["n"] == 1
    book2 = empty_ledger(rec)
    book2["tickets"] = [
        {
            **_ticket(ticker="OPEN-1"),
            "yes_ask": 0.5,
            "quote": {"yes_ask": 0.5, "fee_multiplier": 1.0},
        }
    ]
    save_ledger(book2)
    out = run_tick(
        brain=_brain(),
        executor=PaperExecutor(),
        catalog={"markets": [_market(ticker="OPEN-1", result="no", yes_ask=0.5)]},
    )
    assert out["settle"]["joined"] == 1
    assert brain_score_path().is_file()


def test_held_event_is_first_in_brain_order():
    from golf_offshoot.golf_kalshi.loop import _brain_order

    groups = {
        "OTHER": [_market(ticker="O", event_ticker="OTHER", series_ticker="KXLIV")],
        "HELD": [_market(ticker="H", event_ticker="HELD", series_ticker="KXPGA")],
    }
    order, _rr = _brain_order(groups, 0, held_keys=["HELD"])
    assert order[0] == "HELD"


def test_hub_shows_mix_and_cap_shares(gk_root, tmp_path):
    from golf_offshoot.golf_kalshi.hub import board_html
    from golf_offshoot.golf_kalshi.paths import last_tick_path
    from golf_offshoot.golf_kalshi.recipe import recipe_public

    rec = recipe_public()
    assert rec["cap_fast"] == 50.0
    assert rec["cap_week"] == 100.0
    assert rec["cap_slow"] == 50.0
    assert rec["event_cap_frac"] == rec["single_name"]
    last_tick_path().parent.mkdir(parents=True, exist_ok=True)
    last_tick_path().write_text(
        '{"worthy": 4, "picked": {"fast": 1, "week": 0, "slow": 0}, "exits": 1, "realloc": 0, "adds": 0}\n',
        encoding="utf-8",
    )
    page = board_html()
    assert "worthy 4" in page
    assert "Live/entry $" in page
    assert "Live/entry edge" not in page
    assert "Fast 50" in page
    assert "This week 100" in page
    assert "Closed tickets" in page
    assert "no closed tickets" in page
    home = page[page.index("Open tickets") : page.index("Thinking")]
    ops = page[page.index("<h3>Recipe</h3>") :]
    assert "event dollars at 5% of bank" in ops
    assert "ticket trim was one-time on v1" in ops
    assert "mix_event_cap is that dollar gate" in ops
    assert "event dollars at 5% of bank" not in home


def test_hub_thin_quote_hides_noisy_dollar_edge(gk_root):
    from golf_offshoot.golf_kalshi.hub import blotter_html
    from golf_offshoot.golf_kalshi.paper import empty_ledger, save_ledger
    from golf_offshoot.golf_kalshi.paths import last_tick_path

    book = empty_ledger()
    book["tickets"] = [
        _ticket(
            ticker="KXPGA-26-LNORRIS",
            player="Lando Norris",
            yes_ask=0.001,
            edge_after_fee=788.199,
            quote={"yes_ask": 0.001, "yes_bid": 0.0, "fee_multiplier": 1.0, "displayed_size": 10.0},
        )
    ]
    save_ledger(book)
    last_tick_path().parent.mkdir(parents=True, exist_ok=True)
    last_tick_path().write_text(
        json.dumps(
            {
                "marks": {
                    "KXPGA-26-LNORRIS": {"live_edge": 788.199, "entry_edge": 788.199},
                }
            }
        ),
        encoding="utf-8",
    )
    page = blotter_html()
    assert "Live/entry $" in page
    assert "Live/entry edge" not in page
    assert "788" not in page
    assert "thin" in page
    assert "0.001" in page
    assert "Lando Norris" in page


def test_hub_open_ticket_dollar_edge_two_decimals(gk_root):
    from golf_offshoot.golf_kalshi.hub import blotter_html
    from golf_offshoot.golf_kalshi.paper import empty_ledger, save_ledger

    book = empty_ledger()
    book["tickets"] = [_ticket(edge_after_fee=0.0512)]
    save_ledger(book)
    page = blotter_html()
    assert "Live/entry $" in page
    assert "— / +0.05" in page
    assert "thin" not in page
    assert "0.08" in page


def test_hub_home_mix_shows_skips_when_tickets_open(gk_root):
    from golf_offshoot.golf_kalshi.hub import cockpit_html, session_html
    from golf_offshoot.golf_kalshi.paper import empty_ledger, save_ledger
    from golf_offshoot.golf_kalshi.paths import last_tick_path

    book = empty_ledger()
    book["tickets"] = [_ticket(status="SETTLE_PENDING")]
    save_ledger(book)
    last_tick_path().parent.mkdir(parents=True, exist_ok=True)
    last_tick_path().write_text(
        json.dumps(
            {
                "worthy": 8,
                "picked": {"fast": 0, "week": 0, "slow": 0},
                "exits": 0,
                "realloc": 0,
                "adds": 0,
                "fills": 0,
                "skips": 12,
                "skip_reasons": {"no_field": 9, "mix_event_cap": 3},
            }
        )
        + "\n",
        encoding="utf-8",
    )
    home = session_html()
    think = cockpit_html()
    assert "worthy 8" in home
    assert "picked 0/0/0" in home
    assert "fills=0 skips=12" in home
    assert "no_field 9" in home
    assert "Paper fills from decide_golf" not in think
    assert "Last tick fills=0 skips=12" in think
    assert "Open tickets on Home are the book" in think


def test_hub_sleeve_meters_follow_sizing_bank(gk_root):
    from golf_offshoot.golf_kalshi.hub import session_html
    from golf_offshoot.golf_kalshi.paper import empty_ledger, save_ledger

    rec = recipe_v1()
    book = empty_ledger(rec)
    book["bankroll"] = 833.694
    book["betting_pnl"] = -166.306
    save_ledger(book)
    page = session_html()
    live_fast = rec.sleeve_target("fast", 833.694)
    live_week = rec.sleeve_target("week", 833.694)
    live_slow = rec.sleeve_target("slow", 833.694)
    assert "Fast 50" not in page
    assert "This week 100" not in page
    assert f"Fast {live_fast:.0f}" in page
    assert f"This week {live_week:.0f}" in page
    assert f"Slow {live_slow:.0f}" in page
    assert f"{live_fast:.2f}" in page
    assert f"{live_week:.2f}" in page


def test_golf_farm_points_at_home_tape(gk_root):
    from golf_offshoot.golf_kalshi.organs import farm_panel_html, honer_panel_html
    from golf_offshoot.golf_kalshi.paper import empty_ledger, save_ledger

    book = empty_ledger()
    book["tickets"] = [
        _ticket(status="SETTLE_PENDING"),
        _ticket(ticker="T2", status="paper_lose"),
    ]
    save_ledger(book)
    farm = farm_panel_html()
    honer = honer_panel_html()
    assert "no golf tape yet" not in farm
    assert "no golf tape yet" not in honer
    assert "Paper tape is on Home (1 open) and Scoreboard (1 closed)" in farm
    assert "Paper tape is on Home (1 open) and Scoreboard (1 closed)" in honer
    assert "Golf Honer is not consulting" in honer
    assert "No golf Farm notebooks" in farm


def test_paper_halt_expires_without_retrip(gk_root):
    from datetime import datetime, timedelta, timezone

    from golf_offshoot.golf_kalshi.paper import engage_halt, halt_new_fills

    rec = recipe_v1()
    book = empty_ledger(rec)
    book["bankroll"] = 833.0
    book["peak_bankroll"] = 1000.0
    halted, why = halt_new_fills(book, rec)
    assert halted is True
    assert why == "drawdown"
    led = engage_halt(book, why, recipe=rec)
    assert led["halted"] is True
    assert led["halt_log"]
    assert led["halt_log"][-1]["mode"] == "paper"
    assert led["halt_log"][-1]["seconds"] == 120
    still, _ = halt_new_fills(led, rec)
    assert still is True
    past = datetime.now(timezone.utc) - timedelta(seconds=1)
    led["halt_until"] = past.isoformat()
    after, _ = halt_new_fills(led, rec)
    assert after is False
    assert led["halted"] is False
    assert led["peak_bankroll"] == pytest.approx(833.0)
    again, _ = halt_new_fills(led, rec)
    assert again is False


def test_recipe_bump_releases_old_next_day_halt(gk_root):
    from golf_offshoot.golf_kalshi.paper import bump_recipe, halt_new_fills

    rec = recipe_v1()
    book = empty_ledger(rec)
    book["recipe_id"] = "golf-kalshi-recipe-v1.1"
    book["halted"] = True
    book["halt_reason"] = "drawdown"
    book["halt_until"] = "2026-09-12"
    book["bankroll"] = 833.0
    book["peak_bankroll"] = 1000.0
    book["day_settled_pnl"] = -166.0
    out = bump_recipe(book, rec)
    assert out["recipe_id"] == rec.recipe_id
    assert out["halted"] is False
    assert out["peak_bankroll"] == pytest.approx(833.0)
    halted, _ = halt_new_fills(out, rec)
    assert halted is False


def test_negative_paper_bankroll_still_fills(gk_root):
    rec = recipe_v1()
    book = empty_ledger(rec)
    book["bankroll"] = -50.0
    book["peak_bankroll"] = 1000.0
    book["day_settled_pnl"] = -1050.0
    save_ledger(book)
    from golf_offshoot.golf_kalshi.paper import halt_new_fills

    halted, _ = halt_new_fills(book, rec)
    assert halted is False
    d = decide_golf(_market(), book, rec, _brain())
    assert d.action == "fill"
    assert d.stake >= rec.min_stake


def test_live_halt_is_next_utc_day(gk_root):
    from datetime import datetime, timedelta, timezone

    from golf_offshoot.golf_kalshi.paper import engage_halt, halt_new_fills

    trading_armed_path().write_text("1\n", encoding="utf-8")
    rec = recipe_v1()
    book = empty_ledger(rec)
    book["bankroll"] = 833.0
    book["peak_bankroll"] = 1000.0
    halted, why = halt_new_fills(book, rec)
    assert halted is True
    led = engage_halt(book, why, recipe=rec)
    assert led["halt_log"][-1]["mode"] == "live"
    expect = (datetime.now(timezone.utc).date() + timedelta(days=1)).isoformat()
    assert led["halt_until"] == expect
    still, _ = halt_new_fills(led, rec)
    assert still is True
    assert led["peak_bankroll"] == pytest.approx(1000.0)


def test_golf_watch_label_stale_only_while_running():
    from golf_offshoot.golf_kalshi.hub import golf_watch_label
    from golf_offshoot.localtime import now

    assert golf_watch_label({"running": False, "at": "2020-01-01T00:00:00-04:00"}) == "off"
    assert (
        golf_watch_label(
            {"running": True, "at": "2020-01-01T00:00:00-04:00", "interval_s": 120}
        )
        == "stale"
    )
    assert golf_watch_label({"running": True, "at": ""}) == "stale"
    assert golf_watch_label({"running": True, "at": now().isoformat(), "interval_s": 120}) == "on"
    assert golf_watch_label({"running": True, "at": now().isoformat()}, halt=True) == "halt"


def test_closed_tickets_on_scoreboard_not_home(gk_root, tmp_path):
    rec = recipe_v1()
    book = empty_ledger(rec)
    book["tickets"] = [
        _ticket(
            ticker="LOSE-1",
            player="Antoine Rozner",
            status="paper_lose",
            pnl_after_fee=-26.74,
            settled_at="2026-09-11T16:06:57.409702-04:00",
        )
    ]
    save_ledger(book)
    page = render_html(build_surface(artifact_root=tmp_path, viz_root=tmp_path / "viz", lane="golf"))
    home = page[page.index("desk-view-home") : page.index("desk-view-scoreboard")]
    score = page[page.index("desk-view-scoreboard") : page.index("desk-view-ops")]
    assert "Open tickets" in home
    assert "Closed tickets" not in home
    assert ">Closed<" in home or "<b>Closed</b>" in home
    assert "Antoine Rozner" not in home
    assert "Closed tickets" in score
    assert "Antoine Rozner" in score
    assert "lose" in score
    assert "-26.74" in score
