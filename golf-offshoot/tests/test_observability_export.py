from golf_offshoot.learning_lane_15m.paths import LANE_15M, LANE_GOLF, set_15m_root_override
from golf_offshoot.operator_surface.observability import (
    FORBIDDEN_KEYS,
    HUB_MANIFEST_REL,
    SCHEMA_VERSION,
    WC1_STATUS,
    build_hub_manifest,
    collect_journal_windows,
    hub_manifest_path,
    write_observability_exports,
)


def _lane(payload, lane_id):
    found = [ln for ln in payload["lanes"] if ln["lane_id"] == lane_id]
    assert len(found) == 1
    return found[0]


def test_hub_manifest_matches_pr151_schema(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path / "golf")
    set_15m_root_override(tmp_path / "kalshi_15m")
    try:
        payload = build_hub_manifest(
            markets=[
                {
                    "ticker": "KXBTC15M-26SEP071415-15",
                    "event_ticker": "KXBTC15M-26SEP071400",
                    "window_id": "KXBTC15M-26SEP071400__2026-09-07T14:00:00Z__2026-09-07T14:15:00Z",
                    "status": "active",
                    "result": "",
                }
            ]
        )
        assert payload["schema_version"] == SCHEMA_VERSION
        assert isinstance(payload["lanes"], list)
        assert [ln["lane_id"] for ln in payload["lanes"]] == [LANE_GOLF, LANE_15M]
        golf = _lane(payload, LANE_GOLF)
        lane15 = _lane(payload, LANE_15M)
        assert golf["lane_badge"] == "PHASE 1 OBSERVATION"
        assert any(rec.get("record_id") == "WC1" for rec in golf["records"])
        assert golf["records"][0]["verdict"] == "FAIL"
        assert WC1_STATUS.split(" / ")[0] == "FAIL"
        assert "wc1" not in lane15
        assert lane15["lane_badge"] == "LEARNING LANE"
        assert "LEARNING LANE" in lane15["badges"]
        assert not any(str(rec.get("record_id") or "").lower() == "wc1" for rec in lane15["records"])
        field_values = {row["label"]: row["value"] for row in lane15["last_run"]["fields"]}
        assert field_values["Series"] == "KXBTC15M"
        assert field_values["CF index"] == "BRTI"
        assert field_values["CFB websocket average"] == "observe only"
        assert all(isinstance(row["value"], str) for row in lane15["paper_ledger"]["rows"])
        assert "bankroll" not in lane15["paper_ledger"]
        assert "autobet" not in lane15

        def walk_keys(node):
            if isinstance(node, dict):
                for key, value in node.items():
                    assert key.lower() not in FORBIDDEN_KEYS
                    walk_keys(value)
            elif isinstance(node, list):
                for item in node:
                    walk_keys(item)

        walk_keys(payload)
        assert HUB_MANIFEST_REL.as_posix() == "docs/observability-hub/data/manifest.json"
        assert hub_manifest_path().as_posix().endswith(
            "docs/observability-hub/data/manifest.json"
        )

        paths = write_observability_exports(markets=[], hub_dir=tmp_path / "hub")
        assert (tmp_path / "hub" / "manifest.json").is_file()
        assert "hub_manifest" in paths
        assert "learning_lane_15m_journal" in paths
        assert not str(paths["learning_lane_15m_journal"]).startswith(str(tmp_path / "golf"))
    finally:
        set_15m_root_override(None)


def test_export_keeps_published_15m_when_local_journal_is_thinner(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path / "golf")
    set_15m_root_override(tmp_path / "kalshi_15m")
    try:
        existing = {
            "lanes": [
                {"lane_id": LANE_GOLF, "records": []},
                {
                    "lane_id": LANE_15M,
                    "settle": {
                        "counts": [
                            {"label": "Pending windows", "value": "1"},
                            {"label": "Settled windows", "value": "1"},
                            {"label": "paper_win", "value": "1"},
                        ]
                    },
                    "last_run": {"status": "published export"},
                    "records": [],
                },
            ]
        }
        payload = build_hub_manifest(markets=[], existing=existing)
        lane15 = _lane(payload, LANE_15M)
        # Published paper rows now name their book, so match on the base label.
        counts = {
            row["label"].removeprefix("Lineage B · "): row["value"]
            for row in lane15["settle"]["counts"]
        }
        assert counts["Settled windows"] == "1"
        assert counts["paper_win"] == "1"
        labels = [row["label"] for row in lane15["settle"]["counts"]]
        assert "Lineage B · paper_win" in labels
    finally:
        set_15m_root_override(None)


def test_collect_journal_windows_from_paper_when_live_empty(tmp_path, monkeypatch):
    from golf_offshoot.data_feeds.kalshi_15m import parse_event, parse_market
    from golf_offshoot.learning_lane_15m.paper import paper_autobet_open_markets

    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path / "golf")
    set_15m_root_override(tmp_path / "kalshi_15m")
    try:
        ev = parse_event(
            {
                "event_ticker": "KXBTC15M-26SEP071445",
                "series_ticker": "KXBTC15M",
                "settlement_sources": [{"name": "CF Benchmarks", "url": "https://www.cfbenchmarks.com/"}],
            }
        )
        market = parse_market(
            {
                "ticker": "KXBTC15M-26SEP071445-45",
                "event_ticker": "KXBTC15M-26SEP071445",
                "status": "active",
                "yes_ask_dollars": "0.4000",
                "yes_bid_dollars": "0.3800",
                "open_time": "2026-09-07T14:45:00Z",
                "close_time": "2026-09-07T15:00:00Z",
            },
            event=ev,
        )
        paper_autobet_open_markets([market])
        windows = collect_journal_windows([])
        assert windows
        assert any(w["event_ticker"] == "KXBTC15M-26SEP071445" for w in windows)
        assert any(w["ticker"] == "KXBTC15M-26SEP071445-45" for w in windows)
    finally:
        set_15m_root_override(None)
