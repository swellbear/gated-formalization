"""Clerical runner: dry-run, kill switch, whitelist. Serves nothing until Founder arms it."""

from golf_offshoot.learning_lane_15m.learn import mark_roles_served
from golf_offshoot.learning_lane_15m.paths import set_15m_root_override
from golf_offshoot.learning_lane_15m.runner import (
    CLERICAL_WHITELIST,
    MODE_ARMED,
    MODE_DRY,
    MODE_OFF,
    format_runner_line,
    plan_from_wake,
    runner_log_path,
    runner_mode,
    run_once,
)


def test_runner_mode_defaults_to_dry_run(monkeypatch):
    monkeypatch.delenv("GOLF_OFFSHOOT_LEARNING_RUNNER", raising=False)
    assert runner_mode() == MODE_DRY
    assert runner_mode("off") == MODE_OFF
    assert runner_mode("armed") == MODE_ARMED


def test_plan_serves_only_the_named_whitelist():
    state = {
        "roles_owed": [
            {"role": "illustrator"},
            {"role": "systems"},
            {"role": "digestor"},
            {"role": "operator"},
            {"role": "lab"},
        ]
    }
    plan = plan_from_wake(state)
    assert plan["would_serve"] == list(CLERICAL_WHITELIST)
    assert plan["held_for_human"] == ["operator", "lab"]
    assert "operator" not in plan["would_serve"]


def test_dry_run_logs_and_does_not_mark_served(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        (tmp_path / "latest").mkdir(parents=True)
        (tmp_path / "latest" / "learning_wake.json").write_text(
            '{"roles_owed": [{"role": "illustrator"}, {"role": "operator"}]}',
            encoding="utf-8",
        )
        entry = run_once(mode=MODE_DRY, now_iso="2026-09-07T21:40:00-04:00")
        assert entry["mode"] == MODE_DRY
        assert entry["would_serve"] == ["illustrator"]
        assert entry["held_for_human"] == ["operator"]
        assert entry["served"] == []
        assert entry["mark_roles_served_called"] is False
        log = runner_log_path().read_text(encoding="utf-8")
        assert "illustrator" in log
        assert "mark_roles_served_called" in log
        line = format_runner_line(entry)
        assert "served=none" in line
        assert "would_serve=illustrator" in line
    finally:
        set_15m_root_override(None)


def test_kill_switch_stops_before_reading_owed(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        (tmp_path / "latest").mkdir(parents=True)
        (tmp_path / "latest" / "learning_wake.json").write_text(
            '{"roles_owed": [{"role": "illustrator"}]}',
            encoding="utf-8",
        )
        entry = run_once(mode=MODE_OFF, now_iso="2026-09-07T21:40:00-04:00")
        assert entry["mode"] == MODE_OFF
        assert entry["would_serve"] == []
        assert "kill switch" in entry["note"]
        assert "owed" not in entry
    finally:
        set_15m_root_override(None)


def test_armed_is_refused_and_falls_back_to_dry_run(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        (tmp_path / "latest").mkdir(parents=True)
        (tmp_path / "latest" / "learning_wake.json").write_text(
            '{"roles_owed": [{"role": "systems"}]}',
            encoding="utf-8",
        )
        entry = run_once(mode=MODE_ARMED, now_iso="2026-09-07T21:40:00-04:00")
        assert entry["mode"] == MODE_DRY
        assert entry.get("armed_refused") is True
        assert entry["served"] == []
        assert entry["mark_roles_served_called"] is False
    finally:
        set_15m_root_override(None)


def test_mark_roles_served_records_human_vs_auto_provenance(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        (tmp_path / "latest").mkdir(parents=True)
        (tmp_path / "latest" / "learning_wake.json").write_text(
            '{"roles_owed": [{"role": "illustrator"}], "served": []}',
            encoding="utf-8",
        )
        state = mark_roles_served(["illustrator"], by="runner-test", served_kind="auto")
        assert state is not None
        assert state["roles_owed"] == []
        assert state["served"][0]["served_kind"] == "auto"
        assert state["served"][0]["served_by"] == "runner-test"
    finally:
        set_15m_root_override(None)
