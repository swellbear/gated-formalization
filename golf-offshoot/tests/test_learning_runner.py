"""Clerical runner: serve-on-proof, file kill switch, whitelist. Dry-run until Founder arms."""

import json

import pytest

from golf_offshoot.learning_lane_15m.learn import load_wake_state, mark_roles_served
from golf_offshoot.learning_lane_15m.paths import set_15m_root_override
from golf_offshoot.learning_lane_15m.runner import (
    CLERICAL_WHITELIST,
    MANIFEST_REL,
    PARK_REL,
    MODE_ARMED,
    MODE_DRY,
    MODE_OFF,
    artifact_path,
    format_runner_line,
    kill_switch_active,
    plan_from_wake,
    reconcile_owed_from_disk,
    run_forever,
    run_once,
    run_passes,
    runner_log_path,
    runner_mode,
    serve_role,
    write_arm_file,
    write_kill_switch,
)
from golf_offshoot.operator_surface.observability import repo_root


def _wake(tmp_path, roles):
    latest = tmp_path / "latest"
    latest.mkdir(parents=True, exist_ok=True)
    payload = {
        "roles_owed": [{"role": role} for role in roles],
        "served": [],
    }
    (latest / "learning_wake.json").write_text(json.dumps(payload), encoding="utf-8")


def test_runner_mode_defaults_to_dry_run(monkeypatch):
    monkeypatch.delenv("GOLF_OFFSHOOT_LEARNING_RUNNER", raising=False)
    assert runner_mode() == MODE_DRY
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
        _wake(tmp_path, ["illustrator", "operator"])
        entry = run_once(mode=MODE_DRY, now_iso="2026-09-07T21:40:00-04:00")
        assert entry["mode"] == MODE_DRY
        assert entry["would_serve"] == ["illustrator"]
        assert entry["held_for_human"] == ["operator"]
        assert entry["served"] == []
        assert entry["mark_roles_served_called"] is False
        log = runner_log_path().read_text(encoding="utf-8")
        assert "illustrator" in log
        line = format_runner_line(entry)
        assert "served=none" in line
        assert "would_serve=illustrator" in line
    finally:
        set_15m_root_override(None)


def test_kill_switch_is_a_file_reread_each_pass(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        _wake(tmp_path, ["illustrator"])
        first = run_once(mode=MODE_DRY)
        assert first["mode"] == MODE_DRY
        assert kill_switch_active() is False
        write_kill_switch()
        assert kill_switch_active() is True
        killed = run_once(mode=MODE_DRY)
        assert killed["mode"] == MODE_OFF
        assert "kill switch file" in killed["note"]
        assert "owed" not in killed
        assert killed["would_serve"] == []
    finally:
        set_15m_root_override(None)


def test_run_passes_stops_when_kill_file_appears(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        _wake(tmp_path, ["illustrator"])
        first = run_once(mode=MODE_DRY)
        write_kill_switch()
        rest = run_passes(3, mode=MODE_DRY)
        assert first["mode"] == MODE_DRY
        assert rest[0]["mode"] == MODE_OFF
        assert len(rest) == 1
        assert kill_switch_active() is True
    finally:
        set_15m_root_override(None)


def test_armed_is_refused_without_arm_file(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        _wake(tmp_path, ["systems"])
        entry = run_once(mode=MODE_ARMED, now_iso="2026-09-07T21:40:00-04:00")
        assert entry["mode"] == MODE_DRY
        assert entry.get("armed_refused") is True
        assert entry["served"] == []
        assert entry["mark_roles_served_called"] is False
    finally:
        set_15m_root_override(None)


def test_serve_on_proof_marks_only_when_hash_changes(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        _wake(tmp_path, ["digestor"])

        def _write_new():
            artifact_path("digestor").write_text(
                '{"pending": ["KXBTC15M-NEW"], "settled": []}\n',
                encoding="utf-8",
            )

        ok = serve_role("digestor", do_work=_write_new)
        assert ok["ok"] is True
        assert ok["marked"] is True
        assert ok["before"] != ok["after"]
        state = load_wake_state()
        assert state is not None
        assert state["roles_owed"] == []
        assert state["served"][0]["served_kind"] == "auto"
        assert state["served"][0]["served_by"] == "runner"
    finally:
        set_15m_root_override(None)


def test_unchanged_artifact_stays_owed_and_is_logged(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        _wake(tmp_path, ["digestor"])
        path = artifact_path("digestor")
        path.write_text('{"pending": ["A"]}\n', encoding="utf-8")

        def _same():
            path.write_text('{"pending": ["A"]}\n', encoding="utf-8")

        result = serve_role("digestor", do_work=_same)
        assert result["ok"] is False
        assert result["marked"] is False
        assert "unchanged" in result["reason"]
        state = load_wake_state()
        assert state is not None
        assert [row["role"] for row in state["roles_owed"]] == ["digestor"]
        assert state.get("served") == []
    finally:
        set_15m_root_override(None)


def test_dry_across_several_ticks_role_goes_owed_then_clears(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        _wake(tmp_path, ["operator"])
        tick1 = run_once(mode=MODE_DRY)
        assert tick1["would_serve"] == []
        assert tick1["held_for_human"] == ["operator"]

        _wake(tmp_path, ["digestor", "operator"])
        tick2 = run_once(mode=MODE_DRY)
        assert tick2["would_serve"] == ["digestor"]
        assert [row["role"] for row in (load_wake_state() or {}).get("roles_owed") or []] == [
            "digestor",
            "operator",
        ]

        def _write_new():
            artifact_path("digestor").write_text(
                '{"pending": ["CLEARED"], "settled": ["X"]}\n',
                encoding="utf-8",
            )

        tick3 = run_once(
            mode=MODE_DRY,
            execute=True,
            root=tmp_path,
            do_work={"digestor": _write_new},
        )
        assert tick3["served"] == ["digestor"]
        assert tick3["mark_roles_served_called"] is True
        state = load_wake_state()
        assert state is not None
        assert [row["role"] for row in state["roles_owed"]] == ["operator"]
        assert state["served"][0]["served_kind"] == "auto"

        tick4 = run_once(mode=MODE_DRY)
        assert tick4["would_serve"] == []
        assert tick4["held_for_human"] == ["operator"]
        assert tick4["mark_roles_served_called"] is False
    finally:
        set_15m_root_override(None)


def test_systems_heartbeat_does_not_clear_owed(tmp_path, monkeypatch):
    set_15m_root_override(tmp_path)
    try:
        _wake(tmp_path, ["systems"])
        manifest = tmp_path / "docs" / "observability-hub" / "data" / "manifest.json"
        manifest.parent.mkdir(parents=True, exist_ok=True)
        same_lane = {
            "lanes": [
                {
                    "lane_id": "learning_lane_15m",
                    "settle": {"headline": "same", "residual": [], "counts": []},
                    "last_run": {"headline": "same"},
                    "learning_status": {
                        "pending_windows": [],
                        "missing_paper_joins": [],
                        "published_history": [],
                    },
                    "charts": [],
                }
            ]
        }
        manifest.write_text(json.dumps(same_lane), encoding="utf-8")

        def _heartbeat():
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            payload["hub"] = {"generated_at": "later"}
            manifest.write_text(json.dumps(payload), encoding="utf-8")

        result = serve_role("systems", do_work=_heartbeat, root=tmp_path)
        assert result["marked"] is False
        assert "heartbeat" in result["reason"]
        state = load_wake_state()
        assert [row["role"] for row in (state or {}).get("roles_owed") or []] == ["systems"]
    finally:
        set_15m_root_override(None)


def test_mark_roles_served_records_human_vs_auto_provenance(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        _wake(tmp_path, ["illustrator"])
        state = mark_roles_served(["illustrator"], by="runner-test", served_kind="auto")
        assert state is not None
        assert state["roles_owed"] == []
        assert state["served"][0]["served_kind"] == "auto"
        assert state["served"][0]["served_by"] == "runner-test"
    finally:
        set_15m_root_override(None)


def _lane_manifest(*, headline: str) -> dict:
    return {
        "lanes": [
            {
                "lane_id": "learning_lane_15m",
                "settle": {"headline": headline, "residual": [], "counts": []},
                "last_run": {"headline": headline},
                "learning_status": {
                    "pending_windows": [],
                    "missing_paper_joins": [],
                    "published_history": [],
                },
                "charts": [],
            }
        ]
    }


def test_execute_true_requires_scratch_root_and_refuses_the_real_tree():
    with pytest.raises(RuntimeError, match="requires root="):
        run_once(execute=True)
    with pytest.raises(RuntimeError, match="cannot serve the real repo"):
        run_once(execute=True, root=repo_root())


def test_arm_file_is_enough_to_execute(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        _wake(tmp_path, ["digestor"])
        write_arm_file()

        def _write_new():
            artifact_path("digestor").write_text(
                '{"pending": ["ARMED"], "settled": []}\n',
                encoding="utf-8",
            )

        entry = run_once(do_work={"digestor": _write_new})
        assert entry["armed"] is True
        assert entry["mode"] == MODE_ARMED
        assert entry["served"] == ["digestor"]
        assert entry["mark_roles_served_called"] is True
        state = load_wake_state()
        assert state is not None
        assert state["roles_owed"] == []
        assert state["served"][0]["served_kind"] == "auto"
    finally:
        set_15m_root_override(None)


def test_human_artifact_change_clears_owed_and_keeps_kind(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        _wake(tmp_path, ["operator", "systems", "validator", "lab"])
        park = tmp_path / PARK_REL
        park.parent.mkdir(parents=True, exist_ok=True)
        park.write_text("park v1\n", encoding="utf-8")
        manifest = tmp_path / MANIFEST_REL
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(json.dumps(_lane_manifest(headline="same")), encoding="utf-8")

        assert reconcile_owed_from_disk(root=tmp_path) == []
        still = [row["role"] for row in (load_wake_state() or {}).get("roles_owed") or []]
        assert still == ["operator", "systems", "validator", "lab"]

        park.write_text("park v2 — operator ran\n", encoding="utf-8")
        manifest.write_text(
            json.dumps(_lane_manifest(headline="changed")),
            encoding="utf-8",
        )
        entry = run_once(mode=MODE_DRY, root=tmp_path)
        assert set(entry.get("human_cleared") or []) == {"operator", "systems"}
        state = load_wake_state()
        assert state is not None
        owed = [row["role"] for row in state["roles_owed"]]
        assert owed == ["validator", "lab"]
        kinds = {row["role"]: row["served_kind"] for row in state["served"]}
        assert kinds["operator"] == "human"
        assert kinds["systems"] == "human"
        assert "human_cleared=operator, systems" in format_runner_line(entry) or (
            "human_cleared=systems, operator" in format_runner_line(entry)
        )
    finally:
        set_15m_root_override(None)


def test_run_forever_stops_on_kill_file(tmp_path, monkeypatch):
    set_15m_root_override(tmp_path)
    try:
        _wake(tmp_path, ["illustrator"])
        sleeps = {"n": 0}

        def _sleep(_seconds):
            sleeps["n"] += 1
            write_kill_switch()

        monkeypatch.setattr("golf_offshoot.learning_lane_15m.runner.time.sleep", _sleep)
        run_forever(interval_s=5)
        assert sleeps["n"] == 1
        assert kill_switch_active() is True
    finally:
        set_15m_root_override(None)
