"""Clerical runner: serve-on-proof, file kill switch, whitelist. Dry-run until Founder arms."""

import json

import pytest

from golf_offshoot.learning_lane_15m.learn import load_wake_state, mark_roles_served
from golf_offshoot.learning_lane_15m.paths import set_15m_root_override
from golf_offshoot.learning_lane_15m.runner import (
    CAVEATS_REL,
    CLERICAL_WHITELIST,
    DIGEST_REL,
    JUDICIAL_NEVER,
    MANIFEST_REL,
    PARK_REL,
    MODE_ARMED,
    MODE_DRY,
    MODE_OFF,
    artifact_path,
    proof_artifact_path,
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


def _wake(tmp_path, roles, *, reasons=None):
    latest = tmp_path / "latest"
    latest.mkdir(parents=True, exist_ok=True)
    payload = {
        "roles_owed": [
            {"role": role, "reasons": list((reasons or {}).get(role) or [])} for role in roles
        ],
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
            {"role": "digest-figures"},
            {"role": "validator"},
            {"role": "critic-invariants"},
            {"role": "digestor"},
            {"role": "operator"},
            {"role": "lab"},
            {"role": "soften-critic"},
        ]
    }
    plan = plan_from_wake(state)
    assert CLERICAL_WHITELIST == (
        "illustrator",
        "systems",
        "digest-figures",
        "validator",
        "critic-invariants",
    )
    assert "validator" not in JUDICIAL_NEVER
    assert "digestor" in JUDICIAL_NEVER
    assert plan["would_serve"] == list(CLERICAL_WHITELIST)
    assert plan["held_for_human"] == ["digestor", "operator", "lab", "soften-critic"]
    assert "operator" not in plan["would_serve"]
    assert "digestor" not in plan["would_serve"]
    # The mechanical half self-serves; the written attack never does.
    assert "critic-invariants" in plan["would_serve"]
    assert "soften-critic" not in plan["would_serve"]
    assert "soften-critic" in JUDICIAL_NEVER
    assert "validator" in plan["would_serve"]
    assert "digest-figures" in plan["would_serve"]


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
        _wake(tmp_path, ["digest-figures"])
        source = tmp_path / DIGEST_REL
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text("SOURCE v1\n", encoding="utf-8")

        def _write_source():
            source.write_text("SOURCE v2 — generated figures\n", encoding="utf-8")

        ok = serve_role("digest-figures", do_work=_write_source, root=tmp_path)
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
        _wake(tmp_path, ["digest-figures"])
        path = artifact_path("digest-figures", root=tmp_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("SOURCE same\n", encoding="utf-8")

        def _same():
            path.write_text("SOURCE same\n", encoding="utf-8")

        result = serve_role("digest-figures", do_work=_same, root=tmp_path)
        assert result["ok"] is False
        assert result["marked"] is False
        assert "heartbeat" in result["reason"] or "unchanged" in result["reason"]
        state = load_wake_state()
        assert state is not None
        assert [row["role"] for row in state["roles_owed"]] == ["digest-figures"]
        assert state.get("served") == []
    finally:
        set_15m_root_override(None)


def test_human_digestor_is_refused_by_the_runner(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        _wake(tmp_path, ["digestor"])
        result = serve_role("digestor", root=tmp_path)
        assert result["ok"] is False
        assert result["marked"] is False
        assert "not on the clerical whitelist" in result["reason"]
    finally:
        set_15m_root_override(None)


def test_dry_across_several_ticks_role_goes_owed_then_clears(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        _wake(tmp_path, ["operator"])
        tick1 = run_once(mode=MODE_DRY)
        assert tick1["would_serve"] == []
        assert tick1["held_for_human"] == ["operator"]

        _wake(tmp_path, ["digest-figures", "digestor", "operator"])
        tick2 = run_once(mode=MODE_DRY)
        assert tick2["would_serve"] == ["digest-figures"]
        assert tick2["held_for_human"] == ["digestor", "operator"]
        assert [row["role"] for row in (load_wake_state() or {}).get("roles_owed") or []] == [
            "digest-figures",
            "digestor",
            "operator",
        ]

        source = tmp_path / DIGEST_REL
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text("SOURCE v1\n", encoding="utf-8")
        caveats = tmp_path / CAVEATS_REL
        caveats.parent.mkdir(parents=True, exist_ok=True)
        caveats.write_text("caveat v1\n", encoding="utf-8")
        assert reconcile_owed_from_disk(root=tmp_path) == []

        def _write_figures():
            source.write_text("SOURCE v2 — figures only\n", encoding="utf-8")

        tick3 = run_once(
            mode=MODE_DRY,
            execute=True,
            root=tmp_path,
            do_work={"digest-figures": _write_figures},
        )
        assert tick3["served"] == ["digest-figures"]
        assert tick3["failed"] == []
        state = load_wake_state()
        assert state is not None
        assert [row["role"] for row in state["roles_owed"]] == ["digestor", "operator"]

        source.write_text("SOURCE v3 — still figures only\n", encoding="utf-8")
        tick4 = run_once(mode=MODE_DRY, root=tmp_path)
        assert "digest-figures" not in (tick4.get("human_cleared") or [])
        assert "digestor" not in (tick4.get("human_cleared") or [])
        state = load_wake_state()
        assert [row["role"] for row in (state or {}).get("roles_owed") or []] == [
            "digestor",
            "operator",
        ]

        caveats.write_text("caveat v2 — new honesty caveat\n", encoding="utf-8")
        tick5 = run_once(mode=MODE_DRY, root=tmp_path)
        assert "digestor" in (tick5.get("human_cleared") or [])
        state = load_wake_state()
        assert state is not None
        assert [row["role"] for row in state["roles_owed"]] == ["operator"]
        kinds = {row["role"]: row["served_kind"] for row in state["served"]}
        assert kinds["digest-figures"] == "auto"
        assert kinds["digestor"] == "human"
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
        _wake(tmp_path, ["digest-figures"])
        write_arm_file()
        source = tmp_path / DIGEST_REL
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text("SOURCE armed v1\n", encoding="utf-8")

        def _write_new():
            source.write_text("SOURCE armed v2\n", encoding="utf-8")

        entry = run_once(do_work={"digest-figures": _write_new}, root=tmp_path)
        assert entry["armed"] is True
        assert entry["mode"] == MODE_ARMED
        assert entry["served"] == ["digest-figures"]
        assert entry["failed"] == []
        state = load_wake_state()
        assert state is not None
        assert [row["role"] for row in state["roles_owed"]] == []
    finally:
        set_15m_root_override(None)


def test_human_artifact_change_clears_owed_and_keeps_kind(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        _wake(
            tmp_path,
            ["operator", "systems", "validator", "lab"],
            reasons={"operator": ["park_aged R-SKIP-COINFLIP"]},
        )
        park = tmp_path / PARK_REL
        park.parent.mkdir(parents=True, exist_ok=True)
        park.write_text("park v1\n", encoding="utf-8")
        manifest = tmp_path / MANIFEST_REL
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(json.dumps(_lane_manifest(headline="same")), encoding="utf-8")

        assert reconcile_owed_from_disk(root=tmp_path) == []
        still = [row["role"] for row in (load_wake_state() or {}).get("roles_owed") or []]
        assert still == ["operator", "systems", "validator", "lab"]

        park.write_text("park v2 — ruled R-SKIP-COINFLIP\n", encoding="utf-8")
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


def test_figures_only_refresh_leaves_digestor_owed(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        _wake(tmp_path, ["digest-figures", "digestor"])
        source = tmp_path / DIGEST_REL
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text("SOURCE still 18:03\n", encoding="utf-8")
        caveats = tmp_path / CAVEATS_REL
        caveats.parent.mkdir(parents=True, exist_ok=True)
        caveats.write_text("standing caveat\n", encoding="utf-8")
        assert proof_artifact_path("digestor", root=tmp_path) == caveats
        assert proof_artifact_path("digest-figures", root=tmp_path) == source
        assert reconcile_owed_from_disk(root=tmp_path) == []

        def _write_figures():
            source.write_text("SOURCE refreshed figures only\n", encoding="utf-8")

        result = serve_role("digest-figures", do_work=_write_figures, root=tmp_path)
        assert result["marked"] is True
        state = load_wake_state()
        assert [row["role"] for row in (state or {}).get("roles_owed") or []] == ["digestor"]
        assert reconcile_owed_from_disk(root=tmp_path) == []
        assert [row["role"] for row in (load_wake_state() or {}).get("roles_owed") or []] == [
            "digestor"
        ]
    finally:
        set_15m_root_override(None)


def test_only_a_new_caveat_clears_digestor(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        _wake(tmp_path, ["digestor"])
        source = tmp_path / DIGEST_REL
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text("SOURCE unchanged\n", encoding="utf-8")
        caveats = tmp_path / CAVEATS_REL
        caveats.parent.mkdir(parents=True, exist_ok=True)
        caveats.write_text("caveat v1\n", encoding="utf-8")
        from golf_offshoot.learning_lane_15m.runner import file_fingerprint

        source_fp = file_fingerprint(source)
        (tmp_path / "latest").mkdir(parents=True, exist_ok=True)
        (tmp_path / "latest" / "role_artifact_fps.json").write_text(
            json.dumps({"digestor": f"1178:oldasof|{source_fp}"}),
            encoding="utf-8",
        )
        assert reconcile_owed_from_disk(root=tmp_path) == []
        assert [row["role"] for row in (load_wake_state() or {}).get("roles_owed") or []] == [
            "digestor"
        ]

        source.write_text("SOURCE figures again\n", encoding="utf-8")
        assert reconcile_owed_from_disk(root=tmp_path) == []
        assert [row["role"] for row in (load_wake_state() or {}).get("roles_owed") or []] == [
            "digestor"
        ]

        caveats.write_text("caveat v2 — only this clears digestor\n", encoding="utf-8")
        marked = reconcile_owed_from_disk(root=tmp_path)
        assert [row["role"] for row in marked] == ["digestor"]
        assert [row["role"] for row in (load_wake_state() or {}).get("roles_owed") or []] == []
    finally:
        set_15m_root_override(None)


def test_validator_report_is_the_proof_artifact(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        _wake(tmp_path, ["validator"])
        report = tmp_path / "docs" / "observability-hub" / "data" / "validator_report.json"
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text('{"sha256": "aaa", "exit_code": 1}\n', encoding="utf-8")

        def _write_report():
            report.write_text('{"sha256": "bbb", "exit_code": 0}\n', encoding="utf-8")

        result = serve_role("validator", do_work=_write_report, root=tmp_path)
        assert result["ok"] is True
        assert result["marked"] is True
        assert proof_artifact_path("validator", root=tmp_path) == report
        state = load_wake_state()
        assert [row["role"] for row in (state or {}).get("roles_owed") or []] == []
        assert (state or {}).get("served", [{}])[0].get("served_kind") == "auto"
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
