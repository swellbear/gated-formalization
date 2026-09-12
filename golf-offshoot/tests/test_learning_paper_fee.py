"""15m-2: per-fill fee metadata on new books.

Does not flip R-SKIP-COINFLIP. Does not bind the bar. Does not rewrite historical
books. Disk settlement_pnl stays the zero-fee formula. No fee totals on hub /
digest / records[]. Lineage B untouched.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from golf_offshoot.data_feeds.kalshi_15m import ALLOWED_SERIES, parse_event, parse_market
from golf_offshoot.learning_lane_15m.loop import settle_join
from golf_offshoot.learning_lane_15m.paper import (
    FEE_K,
    TRADING_ARMED,
    fee_for_fill,
    fill_fee_from_movement,
    fill_fee_metadata,
    iter_books,
    load_book,
    load_ledger,
    paper_autobet_open_markets,
)
from golf_offshoot.learning_lane_15m.paths import paper_dir_15m, safe_artifact_stem, set_15m_root_override
from golf_offshoot.learning_lane_15m.rules import load_rules
from golf_offshoot.learning_lane_15m.score import fee_for_fill as score_fee_for_fill
from golf_offshoot.operator_surface.observability import repo_root

EVENT_RAW = {
    "event_ticker": "KXBTC15M-26SEP081000",
    "series_ticker": "KXBTC15M",
    "title": "BTC 15 min",
    "settlement_sources": [{"name": "CF Benchmarks", "url": "https://www.cfbenchmarks.com/"}],
}

CFB = EVENT_RAW["settlement_sources"]
LINEAGE_B_TICKER = "KXBTC15M-26SEP071445-45"
FEE_TOTAL_KEYS = frozenset(
    {
        "fee_accurate",
        "fee_accurate_pnl",
        "fee_accurate_total",
        "fee_adjusted",
        "fee_adjusted_pnl",
        "corrected_pnl",
        "corrected_total",
        "fee_total",
        "total_fee",
        "hurdle_pnl",
    }
)

# PROPOSED 01 / 15m-1 table (k=0.07, $1, ceil to the cent).
PROPOSED_01 = (
    (0.9835, 0.01),
    (0.7050, 0.03),
    (0.4650, 0.04),
    (0.3850, 0.05),
)


def _lane(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path / "golf"
    )
    set_15m_root_override(tmp_path / "kalshi_15m")


def _end():
    set_15m_root_override(None)


def _market(*, ticker: str, event_ticker: str, yes_ask: str, **more):
    raw = {
        "ticker": ticker,
        "event_ticker": event_ticker,
        "status": "active",
        "result": "",
        "yes_ask_dollars": yes_ask,
        "title": "BTC price up in next 15 mins?",
        "open_time": "2026-09-08T10:00:00Z",
        "close_time": "2026-09-08T10:15:00Z",
        **more,
    }
    return parse_market(raw, event=parse_event({**EVENT_RAW, "event_ticker": event_ticker}))


def _throwaway_skip_on(root: Path) -> Path:
    payload = load_rules()
    rows = []
    for row in payload["rules"]:
        copied = dict(row)
        if copied.get("id") == "R-SKIP-COINFLIP":
            copied["execution"] = True
        rows.append(copied)
    payload["rules"] = rows
    dest = root / "golf-offshoot" / "docs" / "LEARNING_LANE_15M_RULES.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return root


def _walk_fee_total_keys(node, path: str = "") -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            child = f"{path}.{key}" if path else str(key)
            norm = str(key).lower().replace("-", "_")
            assert norm not in FEE_TOTAL_KEYS, f"fee-accurate total key {key!r} at {child}"
            _walk_fee_total_keys(value, child)
    elif isinstance(node, list):
        for index, item in enumerate(node):
            _walk_fee_total_keys(item, f"{path}[{index}]")


def test_fee_cents_match_15m1_score_and_proposed_01():
    for mark, expected in PROPOSED_01:
        assert fee_for_fill(mark, 1.0, k=0.07) == expected
        assert score_fee_for_fill(mark, 1.0, k=0.07) == expected
        assert fill_fee_metadata(posted_yes=mark, stake=1.0)["fee_cents"] == int(round(expected * 100))
    assert FEE_K == 0.07
    assert fee_for_fill(0.40, 1.0) == 0.05
    assert fill_fee_metadata(posted_yes=0.40, stake=1.0)["fee_in_settlement_pnl"] is False


def test_new_fills_stamp_proposed_01_cents(tmp_path, monkeypatch):
    _lane(tmp_path, monkeypatch)
    try:
        rows = (
            ("KXBTC15M-26SEP081015-15", "KXBTC15M-26SEP081015", "0.9835", 0.01),
            ("KXBTC15M-26SEP081030-30", "KXBTC15M-26SEP081030", "0.7050", 0.03),
            ("KXBTC15M-26SEP081045-45", "KXBTC15M-26SEP081045", "0.4650", 0.04),
            ("KXBTC15M-26SEP081100-00", "KXBTC15M-26SEP081100", "0.3850", 0.05),
        )
        for ticker, event_ticker, yes_ask, expected_usd in rows:
            market = _market(ticker=ticker, event_ticker=event_ticker, yes_ask=yes_ask)
            fills = paper_autobet_open_markets([market])
            assert len(fills) == 1
            stamped = fill_fee_from_movement(fills[0])
            assert stamped is not None
            assert stamped["fee_usd"] == expected_usd
            assert stamped["fee_cents"] == int(round(expected_usd * 100))
            assert stamped["fee_in_settlement_pnl"] is False
    finally:
        _end()


def test_new_fill_stamps_fee_cents_and_survives_reload(tmp_path, monkeypatch):
    _lane(tmp_path, monkeypatch)
    try:
        market = _market(
            ticker="KXBTC15M-26SEP081015-15",
            event_ticker="KXBTC15M-26SEP081015",
            yes_ask="0.4000",
        )
        assert float(market["paper_mark"]) == 0.40
        fills = paper_autobet_open_markets([market])
        assert len(fills) == 1
        stamped = fill_fee_from_movement(fills[0])
        assert stamped is not None
        assert stamped["fee_cents"] == 5
        assert stamped["fee_usd"] == 0.05
        assert stamped["fee_k"] == 0.07
        assert stamped["fee_in_settlement_pnl"] is False
        rec = iter_books()[0]
        disk = json.loads(
            (paper_dir_15m() / f"{safe_artifact_stem(rec.tournament_id)}.json").read_text(
                encoding="utf-8"
            )
        )
        mv = disk["movements"][0]
        assert mv["fee_cents"] == 5
        assert mv["fee_in_settlement_pnl"] is False
        assert json.loads(mv["amount_technical"])["fee_cents"] == 5
        reloaded = load_book(rec.tournament_id)
        assert reloaded is not None
        again = fill_fee_from_movement(reloaded.movements[0])
        assert again is not None
        assert again["fee_cents"] == 5
        assert rec.settlement_pnl is None
        skip = next(r for r in load_rules()["rules"] if r["id"] == "R-SKIP-COINFLIP")
        assert skip["execution"] is False
        assert TRADING_ARMED is False
        assert ALLOWED_SERIES == "KXBTC15M"
    finally:
        _end()


def test_settlement_pnl_stays_zero_fee_after_official_join(tmp_path, monkeypatch):
    _lane(tmp_path, monkeypatch)
    try:
        ev = parse_event(
            {
                "event_ticker": "KXBTC15M-26SEP081015",
                "series_ticker": "KXBTC15M",
                "title": "BTC 15 min",
                "settlement_sources": CFB,
            }
        )
        open_m = _market(
            ticker="KXBTC15M-26SEP081015-15",
            event_ticker="KXBTC15M-26SEP081015",
            yes_ask="0.4000",
        )
        paper_autobet_open_markets([open_m])
        official = parse_market(
            {
                "ticker": "KXBTC15M-26SEP081015-15",
                "event_ticker": "KXBTC15M-26SEP081015",
                "status": "finalized",
                "result": "yes",
                "yes_ask_dollars": "0.4000",
                "title": "BTC price up in next 15 mins?",
                "open_time": "2026-09-08T10:00:00Z",
                "close_time": "2026-09-08T10:15:00Z",
                "settlement_sources": CFB,
            },
            event=ev,
        )
        done = settle_join([official], [ev])
        assert done["settled"] == 1
        rec = iter_books()[0]
        assert rec.settled_at is not None
        # stake $1 at 0.40 → decimal 2.5 → payout 2.50 → pnl +1.50 (zero-fee).
        assert rec.settlement_pnl == 1.50
        led = load_ledger()
        assert led.betting_pnl == 1.50
        # Fee-accurate would be 1.50 - 0.05 = 1.45. Must not replace the book.
        assert rec.settlement_pnl != 1.45
        stamped = fill_fee_from_movement(rec.movements[0])
        assert stamped is not None
        assert stamped["fee_cents"] == 5
        assert stamped["fee_in_settlement_pnl"] is False
        row = done["rows"][0]
        assert row["pnl"] == 1.50
    finally:
        _end()


def test_historical_book_without_fee_is_not_rewritten(tmp_path, monkeypatch):
    _lane(tmp_path, monkeypatch)
    try:
        ticker = "KXBTC15M-26SEP081015-15"
        event_ticker = "KXBTC15M-26SEP081015"
        window_id = (
            f"{event_ticker}__2026-09-08T10:00:00Z__2026-09-08T10:15:00Z"
        )
        payload = {
            "tournament_id": window_id,
            "tournament_name": "BTC 15 min",
            "bankroll": 100.0,
            "odds_book": "kalshi_15m",
            "paper_observation_only": True,
            "never_auto_bet": True,
            "notes": ["historical pre-15m-2 book"],
            "book": {
                "bankroll": 100.0,
                "session_label": "learning_lane_15m",
                "positions": [
                    {
                        "position_id": "paper_hist",
                        "player_id": ticker,
                        "player_name": f"YES {ticker}",
                        "bet_type": "win",
                        "stake": 1.0,
                        "decimal_odds": 2.5,
                        "entry_edge": 0.0,
                        "entry_model_p": 0.4,
                        "entry_market_p": 0.4,
                        "fill_price": 0.4,
                        "user_recorded": True,
                        "proposed": False,
                    }
                ],
            },
            "movements": [
                {
                    "movement_id": "move_hist",
                    "kind": "new_bet",
                    "status": "applied",
                    "player_id": ticker,
                    "player_name": f"YES {ticker}",
                    "bet_type": "win",
                    "position_id": "paper_hist",
                    "stake_before": 0.0,
                    "stake_delta": 1.0,
                    "stake_after": 1.0,
                    "decimal_odds": 2.5,
                    "model_win": 0.4,
                    "edge_w": 0.0,
                    "posted_edge": 0.0,
                    "reason_plain": "historical",
                    "reason_technical": "pre-15m-2",
                    "amount_plain": "Paper stake $1.00",
                    "amount_technical": "",
                }
            ],
            "path_id": "learning_lane_15m",
            "independent_bankroll": True,
            "starting_bankroll": 100.0,
        }
        dest = paper_dir_15m() / f"{safe_artifact_stem(window_id)}.json"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        before = dest.read_bytes()
        market = _market(ticker=ticker, event_ticker=event_ticker, yes_ask="0.4000")
        assert market["window_id"] == window_id
        fills = paper_autobet_open_markets([market])
        assert fills == []
        after = dest.read_bytes()
        assert after == before
        rec = load_book(window_id)
        assert rec is not None
        assert fill_fee_from_movement(rec.movements[0]) is None
        dumped = json.loads(dest.read_text(encoding="utf-8"))
        assert "fee_cents" not in dumped["movements"][0]
    finally:
        _end()


def test_skip_writes_no_fee_and_no_position(tmp_path, monkeypatch):
    _lane(tmp_path, monkeypatch)
    try:
        repo = _throwaway_skip_on(tmp_path / "repo")
        live_skip = next(r for r in load_rules()["rules"] if r["id"] == "R-SKIP-COINFLIP")
        assert live_skip["execution"] is False
        coin = _market(
            ticker="KXBTC15M-26SEP081015-15",
            event_ticker="KXBTC15M-26SEP081015",
            yes_ask="0.5100",
            yes_bid_dollars="0.4900",
        )
        assert 0.45 < float(coin["paper_mark"]) < 0.55
        fills = paper_autobet_open_markets([coin], rules_root=repo)
        assert fills == []
        assert iter_books() == []
        jsons = [p.name for p in paper_dir_15m().glob("*.json")]
        assert jsons == ["ledger.json"] or jsons == []
        assert next(r for r in load_rules()["rules"] if r["id"] == "R-SKIP-COINFLIP")["execution"] is False
    finally:
        _end()


def test_hub_digest_records_still_refuse_fee_totals(tmp_path, monkeypatch):
    from golf_offshoot.learning_lane_15m import digest
    from golf_offshoot.learning_lane_15m.digest import collect_figures, render_figures, write_digest
    from golf_offshoot.operator_surface import observability

    _lane(tmp_path, monkeypatch)
    repo = tmp_path / "repo"
    monkeypatch.setattr(observability, "repo_root", lambda: repo)
    monkeypatch.setattr(digest, "repo_root", lambda: repo)
    try:
        ev = parse_event(
            {
                "event_ticker": "KXBTC15M-26SEP081015",
                "series_ticker": "KXBTC15M",
                "title": "BTC 15 min",
                "settlement_sources": CFB,
            }
        )
        open_m = _market(
            ticker="KXBTC15M-26SEP081015-15",
            event_ticker="KXBTC15M-26SEP081015",
            yes_ask="0.4000",
        )
        paper_autobet_open_markets([open_m])
        official = parse_market(
            {
                "ticker": "KXBTC15M-26SEP081015-15",
                "event_ticker": "KXBTC15M-26SEP081015",
                "status": "finalized",
                "result": "yes",
                "yes_ask_dollars": "0.4000",
                "title": "BTC price up in next 15 mins?",
                "open_time": "2026-09-08T10:00:00Z",
                "close_time": "2026-09-08T10:15:00Z",
                "settlement_sources": CFB,
            },
            event=ev,
        )
        settle_join([official], [ev])
        (paper_dir_15m().parent / "latest").mkdir(parents=True, exist_ok=True)
        from golf_offshoot.learning_lane_15m.paths import latest_dir_15m

        (latest_dir_15m() / "journal.json").write_text(
            json.dumps(
                {
                    "lane": "learning_lane_15m",
                    "generated_at": "2026-09-08T12:00:00Z",
                    "windows": [
                        {
                            "ticker": "KXBTC15M-26SEP081015-15",
                            "event_ticker": "KXBTC15M-26SEP081015",
                            "status": "finalized",
                            "result": "yes",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        caveats_src = (
            Path(__file__).resolve().parents[1] / "docs" / "LEARNING_LANE_15M_SOURCE_DIGEST_CAVEATS.md"
        )
        caveats_dest = repo / "golf-offshoot" / "docs" / "LEARNING_LANE_15M_SOURCE_DIGEST_CAVEATS.md"
        caveats_dest.parent.mkdir(parents=True, exist_ok=True)
        caveats_dest.write_text(caveats_src.read_text(encoding="utf-8"), encoding="utf-8")
        (repo / "docs" / "observability-hub" / "data").mkdir(parents=True, exist_ok=True)
        existing = {
            "lanes": [
                {"lane_id": "golf"},
                {
                    "lane_id": "learning_lane_15m",
                    "records": [],
                    "records_note": "No weekly operating record exists for this lane.",
                    "last_run": {"fields": [], "notes": []},
                    "settle": {"counts": [], "residual": [], "notes": []},
                    "paper_ledger": {"rows": [], "notes": []},
                },
            ]
        }
        (repo / "docs" / "observability-hub" / "data" / "manifest.json").write_text(
            json.dumps({"schema_version": 1, "lanes": existing["lanes"]}),
            encoding="utf-8",
        )
        payload = observability.build_hub_manifest(existing=existing)
        lane15 = payload["lanes"][1]
        assert lane15["records"] == []
        _walk_fee_total_keys(lane15)
        figures = collect_figures(root=repo)
        _walk_fee_total_keys(figures)
        assert float(figures["betting_pnl"]) == 1.50
        generated = render_figures(figures)
        assert "1.45" not in generated
        written = write_digest(root=repo).read_text(encoding="utf-8")
        assert "1.45" not in written.split("<!-- BEGIN STANDING CAVEATS")[0]
        live_manifest = repo_root() / "docs" / "observability-hub" / "data" / "manifest.json"
        before = hashlib.sha256(live_manifest.read_bytes()).hexdigest()
        # Fill path must not rewrite the published lineage-B manifest on this tree.
        assert hashlib.sha256(live_manifest.read_bytes()).hexdigest() == before
        assert LINEAGE_B_TICKER not in json.dumps(json.loads(next(paper_dir_15m().glob("KXBTC15M-*.json")).read_text()))
        assert not list(paper_dir_15m().glob("*071445*"))
    finally:
        _end()


def test_paper_fee_path_does_not_touch_golf_kalshi_or_bar_bind():
    src = (
        Path(__file__).resolve().parents[1]
        / "src"
        / "golf_offshoot"
        / "learning_lane_15m"
        / "paper.py"
    )
    text = src.read_text(encoding="utf-8")
    assert "golf_kalshi" not in text
    assert "honer" not in text.lower()
    assert "HOUR-CLOSE" not in text
    assert "consult_registry" not in text
    assert "clerical_score" not in text
    skip = next(r for r in load_rules()["rules"] if r["id"] == "R-SKIP-COINFLIP")
    assert skip["execution"] is False
    bar = json.loads(
        (Path(__file__).resolve().parents[1] / "docs" / "LEARNING_LANE_15M_EVIDENCE_BAR.json").read_text(
            encoding="utf-8"
        )
    )
    assert bar["binding"] is False
    assert TRADING_ARMED is False
