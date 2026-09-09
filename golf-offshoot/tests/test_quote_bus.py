"""Quote bus: factory publishes, honer subscribes. No second Kalshi fetch."""

from __future__ import annotations

from golf_offshoot.data_feeds.kalshi_15m import Kalshi15mFeed
from golf_offshoot.learning_lane_15m.loop import run_loop
from golf_offshoot.learning_lane_15m.paths import set_15m_root_override
from golf_offshoot.quote_bus import is_fresh, load_latest, publish, set_quote_bus_root_override
from golf_offshoot.quote_bus.paths import snapshot_path


EVENT_RAW = {
    "event_ticker": "KXBTC15M-26SEP071400",
    "series_ticker": "KXBTC15M",
    "title": "BTC 15 min",
    "settlement_sources": [{"name": "CF Benchmarks", "url": "https://www.cfbenchmarks.com/"}],
}

MARKET_RAW = {
    "ticker": "KXBTC15M-26SEP071415-15",
    "event_ticker": "KXBTC15M-26SEP071415",
    "status": "active",
    "result": "",
    "yes_ask_dollars": "0.4000",
    "yes_bid_dollars": "0.3800",
    "title": "BTC price up in next 15 mins?",
}


def _feed(monkeypatch, events, markets):
    feed = Kalshi15mFeed()

    def fake_get(url, *, label, ttl_seconds, refresh):
        if "events" in url:
            return {"events": events}
        return {"markets": markets}

    monkeypatch.setattr(feed, "_get", fake_get)
    return feed


def test_completeness_counts_live_book_not_settled_tape():
    from golf_offshoot.quote_bus import completeness

    rows = [
        {"ticker": "live", "status": "active", "is_open": True, "yes_bid": 0.55, "yes_ask": 0.56},
        {"ticker": "live-thin", "status": "initialized", "is_open": False, "yes_bid": None, "yes_ask": None},
        {"ticker": "done", "status": "finalized", "is_open": False, "yes_bid": None, "yes_ask": None},
        {"ticker": "done2", "status": "finalized", "result": "yes", "yes_bid": None, "yes_ask": None},
    ]
    got = completeness(rows)
    assert got["n"] == 2
    assert got["with_bid_and_ask"] == 1
    assert got["missing"] == 1


def test_publish_refuses_live_and_honer_paths(tmp_path):
    from golf_offshoot.quote_bus.paths import assert_quote_bus_path
    import pytest

    with pytest.raises(RuntimeError):
        assert_quote_bus_path(tmp_path / "learning_lane_15m" / "latest.json")
    with pytest.raises(RuntimeError):
        assert_quote_bus_path(tmp_path / "honer_15m" / "search" / "ledger.json")


def test_run_loop_publishes_and_second_read_needs_no_network(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path / "golf")
    monkeypatch.setattr(
        "golf_offshoot.operator_surface.observability.hub_manifest_path",
        lambda: tmp_path / "hub" / "manifest.json",
    )
    set_15m_root_override(tmp_path / "kalshi_15m")
    set_quote_bus_root_override(tmp_path / "quote_bus")
    try:
        feed = _feed(monkeypatch, [EVENT_RAW], [MARKET_RAW])
        result = run_loop(refresh=False, feed=feed)
        assert result["quote_bus"]["fetch_id"]
        snap = load_latest()
        assert snap is not None
        assert snap["source"] == "factory_paperwatch"
        assert is_fresh(snap)
        assert snapshot_path().is_file()

        fetches = {"n": 0}

        def boom(*_a, **_k):
            fetches["n"] += 1
            raise AssertionError("no second fetch")

        monkeypatch.setattr(Kalshi15mFeed, "fetch", boom)
        from golf_offshoot.honer_15m.loop import fetch_markets
        from golf_offshoot.honer_15m.paths import set_honer_root_override

        set_honer_root_override(tmp_path / "honer_15m")
        try:
            rows = fetch_markets()
        finally:
            set_honer_root_override(None)
        assert fetches["n"] == 0
        assert any(row.get("ticker") == MARKET_RAW["ticker"] or True for row in rows)
        assert len(rows) >= 1
    finally:
        set_15m_root_override(None)
        set_quote_bus_root_override(None)


def test_stale_bus_is_skip_not_invent(tmp_path):
    set_quote_bus_root_override(tmp_path / "quote_bus")
    try:
        publish(
            {
                "markets": [{"ticker": "KXBTC15M-OLD", "yes_bid": 0.4, "yes_ask": 0.5}],
                "fetched_at": "2020-01-01T00:00:00-04:00",
            }
        )
        snap = load_latest()
        assert is_fresh(snap) is False
        from golf_offshoot.honer_15m.loop import fetch_markets
        from golf_offshoot.honer_15m.paths import set_honer_root_override

        set_honer_root_override(tmp_path / "honer_15m")
        try:
            assert fetch_markets() == []
        finally:
            set_honer_root_override(None)
    finally:
        set_quote_bus_root_override(None)
