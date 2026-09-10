from golf_offshoot.learning_lane_15m.notify import notify_ops_alerts


def test_hub_down_pings_once_then_dedupes(tmp_path):
    latest = tmp_path / "latest"
    latest.mkdir()
    first = notify_ops_alerts(
        invariants={"failing": ["watch_is_collecting"]},
        wake={},
        check_port=False,
        dry_run=True,
        latest_dir=latest,
        port_open=True,
    )
    assert "hub_down" in first["sent"]
    second = notify_ops_alerts(
        invariants={"failing": ["watch_is_collecting"]},
        wake={},
        check_port=False,
        dry_run=True,
        latest_dir=latest,
        port_open=True,
    )
    assert second["sent"] == []


def test_first_gap_pings_then_dedupes(tmp_path):
    latest = tmp_path / "latest"
    latest.mkdir()
    wake = {
        "events": [
            {
                "kind": "window_sequence_gap",
                "ticker": "KXBTC15M-26SEP100515-15",
                "detail": "eight windows missing; do not backfill",
            }
        ]
    }
    first = notify_ops_alerts(
        invariants={"failing": []},
        wake=wake,
        check_port=False,
        dry_run=True,
        latest_dir=latest,
        port_open=True,
    )
    assert any(item.startswith("gap:") for item in first["sent"])
    second = notify_ops_alerts(
        invariants={"failing": []},
        wake=wake,
        check_port=False,
        dry_run=True,
        latest_dir=latest,
        port_open=True,
    )
    assert second["sent"] == []
