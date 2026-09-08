from golf_offshoot.learning_lane_15m.paths import set_15m_root_override
from golf_offshoot.learning_lane_15m.watch import PaperWatch, watch_interval_s


def test_watch_interval_default(monkeypatch):
    monkeypatch.delenv("GOLF_OFFSHOOT_15M_WATCH_S", raising=False)
    assert watch_interval_s() == 90.0
    monkeypatch.setenv("GOLF_OFFSHOOT_15M_WATCH_S", "45")
    assert watch_interval_s() == 45.0


def test_paper_watch_one_cycle(tmp_path, monkeypatch):
    monkeypatch.setattr("golf_offshoot.strategy.paper_book.package_data_dir", lambda: tmp_path / "golf")
    set_15m_root_override(tmp_path / "kalshi_15m")
    calls = {"n": 0}

    def fake_loop(*, refresh=True, feed=None):
        calls["n"] += 1
        return {
            "paper_autobet": {"fills": 0},
            "settle_join": {"settled": 0, "pending": 1},
        }

    monkeypatch.setattr("golf_offshoot.learning_lane_15m.loop.run_loop", fake_loop)
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.loop.format_loop_report",
        lambda payload: "report",
    )
    try:
        watch = PaperWatch(interval_s=999)
        watch._cycle()
        assert calls["n"] == 1
        assert watch.cycles == 1
        assert watch.last_ok is True
        assert "pending=1" in watch.last_summary
        assert watch.status()["trading_armed"] is False
    finally:
        set_15m_root_override(None)
