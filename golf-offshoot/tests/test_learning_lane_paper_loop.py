import json

from golf_offshoot.data_feeds.kalshi_15m import parse_event, parse_market
from golf_offshoot.learning_lane_15m.loop import paper_autobet, run_loop, settle_join
from golf_offshoot.learning_lane_15m.paper import (
    iter_books,
    ledger_path,
    load_ledger,
    paper_autobet_open_markets,
)
from golf_offshoot.learning_lane_15m.paths import (
    golf_paper_dir,
    latest_dir_15m,
    paper_dir_15m,
    set_15m_root_override,
    settlements_dir_15m,
    shadow_dir_15m,
)
from golf_offshoot.learning_lane_15m.settle import (
    SETTLE_PENDING,
    SETTLE_SETTLED,
    classify_settle,
)
from golf_offshoot.operator_surface.observability import write_observability_exports
from golf_offshoot.strategy.paper_ledger import load_ledger as load_golf_ledger


EVENT_RAW = {
    "event_ticker": "KXBTC15M-26SEP071400",
    "series_ticker": "KXBTC15M",
    "title": "BTC 15 min",
    "settlement_sources": [{"name": "CF Benchmarks", "url": "https://www.cfbenchmarks.com/"}],
}

OPEN_RAW = {
    "ticker": "KXBTC15M-26SEP071415-15",
    "event_ticker": "KXBTC15M-26SEP071415",
    "status": "active",
    "result": "",
    "yes_ask_dollars": "0.4000",
    "yes_bid_dollars": "0.3800",
    "title": "BTC price up in next 15 mins?",
}

INITIALIZED_RAW = {
    "ticker": "KXBTC15M-26SEP071600-00",
    "event_ticker": "KXBTC15M-26SEP071600",
    "status": "initialized",
    "result": "",
    "yes_ask_dollars": None,
    "yes_bid_dollars": None,
    "title": "BTC price up in next 15 mins?",
}

SETTLED_RAW = {
    "ticker": "KXBTC15M-26SEP071400-00",
    "event_ticker": "KXBTC15M-26SEP071400",
    "status": "finalized",
    "result": "yes",
    "yes_ask_dollars": "0.6100",
    "title": "BTC price up in next 15 mins?",
}


def _feed(monkeypatch, events, markets):
    from golf_offshoot.data_feeds.kalshi_15m import Kalshi15mFeed

    feed = Kalshi15mFeed()

    def fake_get(url, *, label, ttl_seconds, refresh):
        if "events" in url:
            return {"events": events}
        return {"markets": markets}

    monkeypatch.setattr(feed, "_get", fake_get)
    return feed


def test_paper_autobet_writes_only_15m_root(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path / "golf")
    set_15m_root_override(tmp_path / "kalshi_15m")
    try:
        market = parse_market(OPEN_RAW, event=parse_event(EVENT_RAW))
        fills = paper_autobet_open_markets([market])
        assert len(fills) == 1
        assert fills[0].kind == "new_bet"
        assert fills[0].status == "applied"
        assert "No claimed edge" in fills[0].reason_plain or "not live trading" in fills[0].reason_plain.lower()
        led = load_ledger()
        assert led.bankroll == 100.0
        assert all(e.kind != "deposit" for e in led.entries)
        books = iter_books()
        fills_led = [e for e in led.entries if e.kind == "paper_fill"]
        assert len(fills_led) == 1
        assert fills_led[0].never_auto_bet is True
        assert fills_led[0].player_name == OPEN_RAW["ticker"]
        assert fills_led[0].event_id == OPEN_RAW["event_ticker"]
        assert "position_id=" in fills_led[0].note
        assert books[0].book.positions[0].position_id in fills_led[0].note
        assert len(books) == 1
        assert books[0].never_auto_bet is True
        assert books[0].paper_observation_only is True
        assert (paper_dir_15m() / "ledger.json").is_file()
        assert (shadow_dir_15m() / "advises.jsonl").is_file()
        assert not (tmp_path / "golf" / "paper" / "ledger.json").exists()
        golf_led = load_golf_ledger()
        assert golf_led.entries == []
        assert not ledger_path().is_relative_to(golf_paper_dir())
        again = paper_autobet_open_markets([market])
        assert again == []
    finally:
        set_15m_root_override(None)


def test_settle_join_pending_then_official(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path / "golf")
    set_15m_root_override(tmp_path / "kalshi_15m")
    try:
        ev = parse_event(EVENT_RAW)
        open_m = parse_market({**SETTLED_RAW, "result": "", "status": "active"}, event=ev)
        paper_autobet_open_markets([open_m])
        pending = settle_join([{**open_m, "result": ""}], [ev])
        assert pending["settled"] == 0
        assert pending["pending"] == 1
        assert pending["rows"][0]["settle_status"] == SETTLE_PENDING
        assert pending["rows"][0]["won"] is None
        books = iter_books()
        assert books[0].settled_at is None
        official = parse_market(SETTLED_RAW, event=ev)
        done = settle_join([official], [ev])
        assert done["settled"] == 1
        assert done["rows"][0]["settle_status"] == SETTLE_SETTLED
        assert done["rows"][0]["won"] is True
        assert done["rows"][0]["source_matched"] is True
        rec = iter_books()[0]
        assert rec.settled_at is not None
        led = load_ledger()
        assert led.betting_pnl != 0
        assert not (tmp_path / "golf" / "paper").exists() or not any(
            (tmp_path / "golf" / "paper").glob("*.json")
        )
    finally:
        set_15m_root_override(None)


def test_settle_no_result_is_yes_without_source():
    row = classify_settle({"ticker": "x", "result": "yes", "settlement_sources": []})
    assert row.won is None
    assert row.settle_status != SETTLE_SETTLED


def test_run_loop_end_to_end(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path / "golf")
    monkeypatch.setattr(
        "golf_offshoot.operator_surface.observability.hub_manifest_path",
        lambda: tmp_path / "hub" / "manifest.json",
    )
    set_15m_root_override(tmp_path / "kalshi_15m")
    try:
        live_and_settled = {
            **SETTLED_RAW,
            "status": "active",
            "result": "yes",
            "yes_ask_dollars": "0.6100",
        }
        feed = _feed(monkeypatch, [EVENT_RAW], [live_and_settled])
        result = run_loop(refresh=False, feed=feed)
        assert result["trading_armed"] is False
        assert result["series"] == "KXBTC15M"
        assert result["paper_autobet"]["fills"] == 1
        # active + result is still SETTLE_PENDING — only finalized/determined settle
        assert result["settle_join"]["settled"] == 0
        assert result["settle_join"]["pending"] >= 1
        assert "PHASE 1 OBSERVATION" in result["banner"]
        assert result["observability_export"]["hub_manifest"]
    finally:
        set_15m_root_override(None)


def test_disputed_and_under_review_stay_pending():
    sources = [{"name": "CF Benchmarks", "url": "https://www.cfbenchmarks.com/"}]
    for status in ("disputed", "under-review"):
        row = classify_settle(
            {
                "ticker": "KXBTC15M-26SEP071415-15",
                "event_ticker": "KXBTC15M-26SEP071400",
                "status": status,
                "result": "yes",
                "settlement_sources": sources,
            }
        )
        assert row.settle_status == SETTLE_PENDING
        assert row.won is None
        assert "disputed" in row.banner.lower() or "review" in row.banner.lower()


def test_close_time_move_rekeys_and_old_window_stays_pending(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path / "golf")
    set_15m_root_override(tmp_path / "kalshi_15m")
    try:
        ev = parse_event(EVENT_RAW)
        first_raw = {
            **OPEN_RAW,
            "event_ticker": "KXBTC15M-26SEP071400",
            "open_time": "2026-09-07T14:00:00Z",
            "close_time": "2026-09-07T14:15:00Z",
            "can_close_early": True,
            "yes_ask_dollars": "0.4000",
            "yes_bid_dollars": "0.3800",
        }
        first = parse_market(first_raw, event=ev)
        fills = paper_autobet_open_markets([first])
        assert len(fills) == 1
        assert first["window_id"].endswith("2026-09-07T14:15:00Z")
        pending = settle_join([{**first, "status": "closed", "result": ""}], [ev])
        assert pending["settled"] == 0
        moved = parse_market({**first_raw, "close_time": "2026-09-07T14:12:00Z"}, event=ev)
        assert moved["window_id"] != first["window_id"]
        paper_autobet_open_markets([moved])
        summary = settle_join([{**moved, "status": "closed", "result": ""}], [ev])
        assert summary["settled"] == 0
        books = iter_books()
        window_ids = {b.tournament_id for b in books}
        assert first["window_id"] in window_ids
        assert moved["window_id"] in window_ids
        assert all(b.settled_at is None for b in books)
    finally:
        set_15m_root_override(None)


def test_paper_autobet_skips_initialized_null_marks(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path / "golf")
    set_15m_root_override(tmp_path / "kalshi_15m")
    try:
        ev = parse_event(EVENT_RAW)
        initialized = parse_market(INITIALIZED_RAW, event=ev)
        open_m = parse_market(OPEN_RAW, event=ev)
        fills = paper_autobet_open_markets([initialized, open_m])
        assert len(fills) == 1
        assert fills[0].player_id == OPEN_RAW["ticker"]
        led = load_ledger()
        assert [e.kind for e in led.entries if e.kind == "paper_fill"]
        assert all(e.player_name != INITIALIZED_RAW["ticker"] for e in led.entries)
    finally:
        set_15m_root_override(None)


def test_journal_windows_from_paper_and_settlements(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path / "golf")
    monkeypatch.setattr(
        "golf_offshoot.operator_surface.observability.hub_manifest_path",
        lambda: tmp_path / "hub" / "manifest.json",
    )
    set_15m_root_override(tmp_path / "kalshi_15m")
    try:
        ev = parse_event(EVENT_RAW)
        first_raw = {
            **OPEN_RAW,
            "event_ticker": "KXBTC15M-26SEP071445",
            "ticker": "KXBTC15M-26SEP071445-45",
            "open_time": "2026-09-07T14:45:00Z",
            "close_time": "2026-09-07T15:00:00Z",
        }
        first = parse_market(first_raw, event=ev)
        assert paper_autobet_open_markets([first])
        paths = write_observability_exports(markets=[], hub_dir=tmp_path / "hub")
        journal = json.loads((latest_dir_15m() / "journal.json").read_text(encoding="utf-8"))
        assert journal["windows"], "windows must come from paper books when live markets are empty"
        events = {w["event_ticker"] for w in journal["windows"]}
        assert "KXBTC15M-26SEP071445" in events
        assert all("__" not in (w["event_ticker"] or "") for w in journal["windows"])
        assert paths["learning_lane_15m_journal"]
        settle_join(
            [
                {
                    **first,
                    "status": "finalized",
                    "result": "yes",
                    "settlement_sources": EVENT_RAW["settlement_sources"],
                    "source_is_cf_benchmarks": True,
                }
            ],
            [ev],
        )
        write_observability_exports(markets=[], hub_dir=tmp_path / "hub")
        journal2 = json.loads((latest_dir_15m() / "journal.json").read_text(encoding="utf-8"))
        assert journal2["windows"]
        assert any(w["event_ticker"] == "KXBTC15M-26SEP071445" for w in journal2["windows"])
    finally:
        set_15m_root_override(None)


def test_settlement_top_level_event_ticker_not_window_id(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path / "golf")
    set_15m_root_override(tmp_path / "kalshi_15m")
    try:
        ev = parse_event(EVENT_RAW)
        first_raw = {
            **OPEN_RAW,
            "event_ticker": "KXBTC15M-26SEP071445",
            "ticker": "KXBTC15M-26SEP071445-45",
            "open_time": "2026-09-07T14:45:00Z",
            "close_time": "2026-09-07T15:00:00Z",
        }
        first = parse_market(first_raw, event=ev)
        paper_autobet_open_markets([first])
        settle_join([{**first, "status": "closed", "result": ""}], [ev])
        files = list(settlements_dir_15m().glob("*.json"))
        assert files
        payload = json.loads(files[0].read_text(encoding="utf-8"))
        assert payload["event_ticker"] == "KXBTC15M-26SEP071445"
        assert "__" not in payload["event_ticker"]
        assert payload["event_ticker"] != payload.get("window_id")
        assert payload["window_id"].startswith("KXBTC15M-26SEP071445__")
        assert payload["rows"][0]["event_ticker"] == "KXBTC15M-26SEP071445"
    finally:
        set_15m_root_override(None)
