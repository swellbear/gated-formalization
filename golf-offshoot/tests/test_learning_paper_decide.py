"""15m-3a: paper consults decide(); live selection stays off.

Does not flip R-SKIP-COINFLIP. Does not bind the bar. Does not touch golf_kalshi.
"""

from __future__ import annotations

import json
from pathlib import Path

from golf_offshoot.data_feeds.kalshi_15m import ALLOWED_SERIES, parse_event, parse_market
from golf_offshoot.learning_lane_15m.paper import (
    TRADING_ARMED,
    iter_books,
    load_ledger,
    paper_autobet_open_markets,
)
from golf_offshoot.learning_lane_15m.paths import paper_dir_15m, set_15m_root_override, shadow_dir_15m
from golf_offshoot.learning_lane_15m.rules import decide, load_rules, registry_path

EVENT_RAW = {
    "event_ticker": "KXBTC15M-26SEP081000",
    "series_ticker": "KXBTC15M",
    "title": "BTC 15 min",
    "settlement_sources": [{"name": "CF Benchmarks", "url": "https://www.cfbenchmarks.com/"}],
}

# 10:15 UTC = 06:15 EDT, strictly after declared_at 05:56 EDT.
ELIGIBLE_OPEN = "2026-09-08T10:00:00Z"
ELIGIBLE_CLOSE = "2026-09-08T10:15:00Z"
# 05:56 EDT on the nose — closed ≤ declared_at, not OOS.
INELIGIBLE_OPEN = "2026-09-08T09:41:00Z"
INELIGIBLE_CLOSE = "2026-09-08T09:56:00Z"


def _lane(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path / "golf"
    )
    set_15m_root_override(tmp_path / "kalshi_15m")


def _end():
    set_15m_root_override(None)


def _raw(
    *,
    ticker: str,
    event_ticker: str,
    yes_bid: str,
    yes_ask: str,
    open_time: str,
    close_time: str,
) -> dict:
    return {
        "ticker": ticker,
        "event_ticker": event_ticker,
        "status": "active",
        "result": "",
        "yes_bid_dollars": yes_bid,
        "yes_ask_dollars": yes_ask,
        "open_time": open_time,
        "close_time": close_time,
        "title": "BTC price up in next 15 mins?",
    }


def _market(**kwargs):
    raw = _raw(**kwargs)
    return parse_market(raw, event=parse_event({**EVENT_RAW, "event_ticker": raw["event_ticker"]}))


def _coinflip(**kwargs):
    defaults = dict(
        ticker="KXBTC15M-26SEP081015-15",
        event_ticker="KXBTC15M-26SEP081015",
        yes_bid="0.4900",
        yes_ask="0.5100",
        open_time=ELIGIBLE_OPEN,
        close_time=ELIGIBLE_CLOSE,
    )
    defaults.update(kwargs)
    return _market(**defaults)


def _outside(**kwargs):
    defaults = dict(
        ticker="KXBTC15M-26SEP081030-30",
        event_ticker="KXBTC15M-26SEP081030",
        yes_bid="0.6100",
        yes_ask="0.6300",
        open_time="2026-09-08T10:15:00Z",
        close_time="2026-09-08T10:30:00Z",
    )
    defaults.update(kwargs)
    return _market(**defaults)


def _throwaway_skip_on(root: Path) -> Path:
    """Temp registry: live rows, but R-SKIP-COINFLIP execution=true. Not the live file."""
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


def _assert_yes1_at_mark(pos, market) -> None:
    mark = float(market["paper_mark"])
    assert pos.stake == 1.0
    assert pos.entry_edge == 0.0
    assert pos.fill_price == mark
    assert pos.entry_model_p == mark
    assert pos.entry_market_p == mark


def test_live_registry_still_fill_all_at_mark_including_coinflip(tmp_path, monkeypatch):
    _lane(tmp_path, monkeypatch)
    try:
        skip = next(r for r in load_rules()["rules"] if r["id"] == "R-SKIP-COINFLIP")
        assert skip["execution"] is False
        coin = _coinflip()
        wide = _outside()
        assert 0.45 < float(coin["paper_mark"]) < 0.55
        assert not (0.45 < float(wide["paper_mark"]) < 0.55)
        fills = paper_autobet_open_markets([coin, wide])
        assert len(fills) == 2
        assert {f.player_id for f in fills} == {coin["ticker"], wide["ticker"]}
        assert all(f.edge_w == 0.0 and f.posted_edge == 0.0 for f in fills)
        by_ticker = {p.player_id: p for rec in iter_books() for p in rec.book.positions}
        _assert_yes1_at_mark(by_ticker[coin["ticker"]], coin)
        _assert_yes1_at_mark(by_ticker[wide["ticker"]], wide)
        led = load_ledger()
        filled = [e for e in led.entries if e.kind == "paper_fill"]
        assert {e.player_name for e in filled} == {coin["ticker"], wide["ticker"]}
        assert skip["execution"] is False
        assert ALLOWED_SERIES == "KXBTC15M"
        assert TRADING_ARMED is False
    finally:
        _end()


def test_paper_autobet_calls_decide(tmp_path, monkeypatch):
    _lane(tmp_path, monkeypatch)
    try:
        calls: list[tuple[str, float]] = []
        real = decide

        def wrapped(rule, *, posted_yes, close_at):
            calls.append((str(rule.get("id") or ""), float(posted_yes)))
            return real(rule, posted_yes=posted_yes, close_at=close_at)

        monkeypatch.setattr("golf_offshoot.learning_lane_15m.paper.decide", wrapped)
        coin = _coinflip()
        fills = paper_autobet_open_markets([coin])
        assert len(fills) == 1
        ids = [row[0] for row in calls]
        assert "R-BASELINE-FILL-ALL" in ids
        assert "R-SKIP-COINFLIP" in ids
        assert all(posted == float(coin["paper_mark"]) for _, posted in calls)
    finally:
        _end()


def test_throwaway_execution_true_skip_writes_no_position(tmp_path, monkeypatch):
    _lane(tmp_path, monkeypatch)
    try:
        repo = _throwaway_skip_on(tmp_path / "repo")
        live_skip = next(r for r in load_rules()["rules"] if r["id"] == "R-SKIP-COINFLIP")
        assert live_skip["execution"] is False
        coin = _coinflip()
        fills = paper_autobet_open_markets([coin], rules_root=repo)
        assert fills == []
        assert iter_books() == []
        led = load_ledger()
        assert all(e.kind != "paper_fill" for e in led.entries)
        assert not any(p.stake == 0 for rec in iter_books() for p in rec.book.positions)
        jsons = [p.name for p in paper_dir_15m().glob("*.json")]
        assert jsons == ["ledger.json"] or jsons == []
        shadow = shadow_dir_15m() / "advises.jsonl"
        assert not shadow.is_file()
        # Live file untouched.
        assert next(r for r in load_rules()["rules"] if r["id"] == "R-SKIP-COINFLIP")["execution"] is False
        assert registry_path().read_text(encoding="utf-8").count('"execution": false') >= 1
    finally:
        _end()


def test_throwaway_execution_true_outside_band_still_fills(tmp_path, monkeypatch):
    _lane(tmp_path, monkeypatch)
    try:
        repo = _throwaway_skip_on(tmp_path / "repo")
        wide = _outside()
        fills = paper_autobet_open_markets([wide], rules_root=repo)
        assert len(fills) == 1
        pos = iter_books()[0].book.positions[0]
        _assert_yes1_at_mark(pos, wide)
        assert pos.player_id == wide["ticker"]
    finally:
        _end()


def test_ineligible_closed_at_or_before_declared_fills_like_baseline(tmp_path, monkeypatch):
    _lane(tmp_path, monkeypatch)
    try:
        repo = _throwaway_skip_on(tmp_path / "repo")
        historic = _coinflip(
            ticker="KXBTC15M-26SEP080556-56",
            event_ticker="KXBTC15M-26SEP080556",
            open_time=INELIGIBLE_OPEN,
            close_time=INELIGIBLE_CLOSE,
        )
        assert 0.45 < float(historic["paper_mark"]) < 0.55
        verdict = decide(
            {
                "id": "R-SKIP-COINFLIP",
                "declared_at": "2026-09-08T05:56:00-04:00",
                "kind": "selection",
                "selects": True,
                "execution": True,
            },
            posted_yes=float(historic["paper_mark"]),
            close_at=INELIGIBLE_CLOSE,
        )
        assert verdict["eligible"] is False
        assert verdict["action"] == "ineligible"
        fills = paper_autobet_open_markets([historic], rules_root=repo)
        assert len(fills) == 1
        pos = iter_books()[0].book.positions[0]
        _assert_yes1_at_mark(pos, historic)
        live_m = _coinflip(
            ticker="KXBTC15M-26SEP080541-41",
            event_ticker="KXBTC15M-26SEP080541",
            open_time="2026-09-08T09:26:00Z",
            close_time="2026-09-08T09:41:00Z",
        )
        live = paper_autobet_open_markets([live_m])
        assert len(live) == 1
        live_pos = [p for rec in iter_books() for p in rec.book.positions if p.player_id == live_m["ticker"]]
        assert live_pos
        _assert_yes1_at_mark(live_pos[0], live_m)
    finally:
        _end()


def test_hook_does_not_consult_honer_or_copy_hour_close():
    src = (
        Path(__file__).resolve().parents[1]
        / "src"
        / "golf_offshoot"
        / "learning_lane_15m"
        / "paper.py"
    )
    text = src.read_text(encoding="utf-8")
    assert "honer" not in text.lower()
    assert "HOUR-CLOSE" not in text
    assert "golf_kalshi" not in text
    assert "consult_registry" not in text
    assert TRADING_ARMED is False
    skip = next(r for r in load_rules()["rules"] if r["id"] == "R-SKIP-COINFLIP")
    assert skip["execution"] is False
