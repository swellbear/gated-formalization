"""crew_tick doorbell: CoS starts when the board needs a brain, not every 90s."""

import json
from datetime import datetime, timezone

from golf_offshoot.learning_lane_15m.crew_tick import (
    REASON_A_DONE,
    REASON_A_IDLE,
    REASON_B,
    REASON_C,
    REASON_D_WATCH,
    REASON_D_HUB,
    REASON_E,
    REASON_F,
    REASON_H,
    REASON_K,
    compute_crew_tick,
    live_selecting_rule_ids,
    stamp_cos_closeout,
)
from golf_offshoot.learning_lane_15m.learn import mark_roles_served, record_learning_tick
from golf_offshoot.learning_lane_15m.paths import set_15m_root_override
from golf_offshoot.learning_lane_15m.runner import serve_role


def _desk(*, role="chief-of-staff", status="idle", job="factory closed. Lab not assigned.", thread=""):
    return (
        "# Agent desk\n\n"
        "| Field | Value |\n"
        "|-------|--------|\n"
        f"| Active role | {role} |\n"
        f"| Job | {job} |\n"
        f"| Status | {status} |\n"
        "| Handoff | — |\n\n"
        "## Thread\n\n"
        f"{thread or '- 2026-09-08 14:22 ET  chief-of-staff: factory closed. Lab not assigned.'}\n"
    )


def _watch(*, cycles="4", last_at=None, running=True, interval_s="90.0"):
    if last_at is None:
        last_at = datetime.now(timezone.utc).isoformat()
    return {
        "running": running,
        "cycles": cycles,
        "interval_s": interval_s,
        "last_at": last_at,
    }


def _owed(role, *, reasons=None, ticks=1, since="2026-09-08T14:00:00-04:00"):
    return {
        "role": role,
        "reasons": list(reasons or ["lab_proposed"]),
        "ticks_unanswered": ticks,
        "owed_since": since,
    }


def test_routine_settle_alone_is_quiet():
    """A new_settle names clerical roles only. That is not a CoS doorbell."""
    tick = compute_crew_tick(
        {
            "watch": _watch(),
            "roles_owed": [
                _owed("digest-figures", reasons=["new_settle KXBTC15M-26SEP081430-30"], ticks=1),
                _owed("systems", reasons=["new_settle KXBTC15M-26SEP081430-30"], ticks=1),
                _owed("validator", reasons=["new_settle KXBTC15M-26SEP081430-30"], ticks=1),
            ],
        },
        desk_text=_desk(role="systems", status="assigned", job="export the settle"),
        hub_ok=True,
    )
    assert tick["needed"] is False
    assert tick["quiet"] is True
    assert tick["reason_ids"] == []


def test_desk_done_next_cos_rings():
    tick = compute_crew_tick(
        {"watch": _watch(), "roles_owed": []},
        desk_text=_desk(
            role="operator",
            status="done",
            job="admit pass filed",
            thread="- 2026-09-08 14:05 ET  operator → chief-of-staff: admit pass. next=chief-of-staff",
        ),
        hub_ok=True,
    )
    assert tick["needed"] is True
    assert REASON_A_DONE in tick["reason_ids"]


def test_same_reasons_after_closeout_stamp_are_quiet():
    state = {
        "watch": _watch(),
        "roles_owed": [_owed("operator"), _owed("soften-critic", reasons=["artifact_unreviewed"])],
        "crew_tick": {},
    }
    desk = _desk()
    first = compute_crew_tick(state, desk_text=desk, leave_off_text="Lab not assigned.", hub_ok=True, honer_freeze_open=False)
    assert first["needed"] is True
    assert REASON_A_IDLE in first["reason_ids"]
    assert REASON_B in first["reason_ids"]
    assert REASON_E in first["reason_ids"]

    state["crew_tick"] = {
        "last_cos_at": "2026-09-08T14:40:00-04:00",
        "last_cos_commit": "testhash",
        "handled_reason_ids": list(first["reason_ids"]),
    }
    # Judicial owes older than the stamp are not "new" (B drops). A and E remain.
    silenced = compute_crew_tick(
        state,
        desk_text=desk,
        leave_off_text="Lab not assigned.",
        hub_ok=True,
        handled_reason_ids=list(first["reason_ids"]),
        honer_freeze_open=False,
    )
    assert silenced["needed"] is False
    assert silenced["quiet"] is True
    assert silenced["last_cos_commit"] == "testhash"


def test_clerical_role_owed_more_than_two_ticks_rings():
    tick = compute_crew_tick(
        {
            "watch": _watch(),
            "roles_owed": [
                _owed("systems", reasons=["new_settle X"], ticks=3),
            ],
        },
        desk_text=_desk(role="systems", status="assigned", job="export"),
        hub_ok=True,
    )
    assert tick["needed"] is True
    assert REASON_C in tick["reason_ids"]


def test_watch_cycles_stuck_rings():
    frozen = "2026-09-08T12:00:00-04:00"
    tick = compute_crew_tick(
        {
            "watch": _watch(cycles="2", last_at=frozen, running=True),
            "roles_owed": [],
        },
        desk_text=_desk(role="operator", status="assigned", job="park"),
        hub_ok=True,
        previous_watch=_watch(cycles="2", last_at=frozen, running=True),
    )
    assert tick["needed"] is True
    assert REASON_D_WATCH in tick["reason_ids"]


def test_runner_cannot_mark_cos_served(tmp_path):
    set_15m_root_override(tmp_path)
    try:
        latest = tmp_path / "latest"
        latest.mkdir(parents=True, exist_ok=True)
        (latest / "learning_wake.json").write_text(
            '{"roles_owed":[{"role":"chief-of-staff","reasons":["crew_tick"]}],"served":[]}',
            encoding="utf-8",
        )
        result = serve_role("chief-of-staff")
        assert result["marked"] is False
        assert "whitelist" in result["reason"]
        state = mark_roles_served(["chief-of-staff"], by="runner", note="must not")
        assert state is not None
        assert state["roles_owed"][0]["role"] == "chief-of-staff"
        assert state["served"] == []
    finally:
        set_15m_root_override(None)


def test_current_idle_cos_desk_rings_like_the_exhibit():
    """The 14:22 idle-CoS desk with uncovered judicial owes is a doorbell."""
    tick = compute_crew_tick(
        {
            "watch": _watch(),
            "updated_at": "2026-09-08T14:30:11-04:00",
            "roles_owed": [
                _owed("operator", reasons=["lab_proposed", "detector_blind <lambda>"]),
                _owed("soften-critic", reasons=["artifact_unreviewed evidence_bar"]),
            ],
        },
        desk_text=_desk(),
        leave_off_text="Turns 1–3 on 5dc4f24. Lab not assigned. Bar not binding.",
        hub_ok=True,
    )
    assert tick["needed"] is True
    assert REASON_A_IDLE in tick["reason_ids"]
    assert REASON_E in tick["reason_ids"]


def test_stamp_cos_closeout_silences_the_same_set(tmp_path, monkeypatch):
    set_15m_root_override(tmp_path)
    repo = tmp_path / "repo"
    (repo / "docs" / "agents").mkdir(parents=True)
    (repo / "docs" / "agents" / "DESK.md").write_text(_desk(), encoding="utf-8")
    (repo / "docs" / "AGENT_LEAVE_OFF.md").write_text("Lab not assigned.\n", encoding="utf-8")
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.crew_tick.repo_root", lambda: repo
    )
    monkeypatch.setattr(
        "golf_offshoot.learning_lane_15m.learn.repo_root", lambda: repo
    )
    try:
        from golf_offshoot.learning_lane_15m.learn import save_wake_state

        state = {
            "watch": _watch(),
            "roles_owed": [_owed("operator"), _owed("soften-critic", reasons=["artifact_unreviewed"])],
            "crew_tick": {},
        }
        first = compute_crew_tick(
            state, desk_text=_desk(), leave_off_text="Lab not assigned.", hub_ok=True
        )
        state["crew_tick"] = first
        save_wake_state(state)
        stamped = stamp_cos_closeout(commit="proofsha", reason_ids=list(first["reason_ids"]), root=repo)
        assert stamped is not None
        assert stamped["needed"] is False
        assert stamped["quiet"] is True
        assert stamped["last_cos_commit"] == "proofsha"
        assert sorted(stamped["handled_reason_ids"]) == sorted(first["reason_ids"])
    finally:
        set_15m_root_override(None)


def _idle_blank_desk():
    return _desk(role="chief-of-staff", status="idle", job="—")


def test_starved_idle_rings_f():
    tick = compute_crew_tick(
        {"watch": _watch(), "roles_owed": []},
        desk_text=_idle_blank_desk(),
        hub_ok=True,
        live_trial_ids=[],
        honer_freeze_open=False,
        farm_open=False,
        farm_promote=False,
    )
    assert tick["needed"] is True
    assert REASON_F in tick["reason_ids"]
    assert REASON_H not in tick["reason_ids"]


def test_assigned_worker_does_not_ring_f():
    tick = compute_crew_tick(
        {"watch": _watch(), "roles_owed": []},
        desk_text=_desk(role="lab", status="assigned", job="one 15m PROPOSED"),
        hub_ok=True,
        live_trial_ids=[],
        honer_freeze_open=True,
        farm_open=False,
        farm_promote=False,
    )
    assert REASON_F not in tick["reason_ids"]
    assert REASON_H not in tick["reason_ids"]


def test_unoperated_proposed_does_not_ring_f():
    tick = compute_crew_tick(
        {
            "watch": _watch(),
            "roles_owed": [_owed("operator", reasons=["lab_proposed"])],
        },
        desk_text=_idle_blank_desk(),
        hub_ok=True,
        live_trial_ids=[],
        honer_freeze_open=False,
        farm_open=False,
        farm_promote=False,
    )
    assert REASON_F not in tick["reason_ids"]


def test_sitting_lab_file_silences_f_even_when_execution_false(tmp_path):
    docs = tmp_path / "golf-offshoot" / "docs"
    docs.mkdir(parents=True)
    (docs / "LEARNING_LANE_15M_LAB_PROPOSED_04.md").write_text(
        "PROPOSED R-SKIP-CIVIL-BOUNDARIES execution=false\n",
        encoding="utf-8",
    )
    tick = compute_crew_tick(
        {"watch": _watch(), "roles_owed": []},
        desk_text=_idle_blank_desk(),
        hub_ok=True,
        live_trial_ids=[],
        honer_freeze_open=False,
        farm_open=False,
        farm_promote=False,
        root=tmp_path,
    )
    assert REASON_F not in tick["reason_ids"]


def test_live_trial_does_not_ring_f():
    tick = compute_crew_tick(
        {"watch": _watch(), "roles_owed": []},
        desk_text=_idle_blank_desk(),
        hub_ok=True,
        live_trial_ids=["R-SKIP-NEW"],
        honer_freeze_open=False,
        farm_open=False,
        farm_promote=False,
    )
    assert REASON_F not in tick["reason_ids"]


def test_hub_ok_false_still_rings_f():
    tick = compute_crew_tick(
        {"watch": _watch(), "roles_owed": []},
        desk_text=_idle_blank_desk(),
        hub_ok=False,
        live_trial_ids=[],
        honer_freeze_open=False,
        farm_open=False,
        farm_promote=False,
    )
    assert REASON_F in tick["reason_ids"]
    assert REASON_D_HUB in tick["reason_ids"]
    assert tick["needed"] is True


def test_stamping_f_without_assigning_lab_does_not_silence():
    state = {
        "watch": _watch(),
        "roles_owed": [],
        "crew_tick": {},
    }
    desk = _idle_blank_desk()
    first = compute_crew_tick(
        state, desk_text=desk, hub_ok=True, live_trial_ids=[], honer_freeze_open=False, farm_open=False, farm_promote=False
    )
    assert REASON_F in first["reason_ids"]
    state["crew_tick"] = {
        "last_cos_at": "2026-09-10T12:00:00-04:00",
        "last_cos_commit": "testhash",
        "handled_reason_ids": list(first["reason_ids"]),
    }
    again = compute_crew_tick(
        state,
        desk_text=desk,
        hub_ok=True,
        handled_reason_ids=list(first["reason_ids"]),
        live_trial_ids=[],
        honer_freeze_open=False,
        farm_open=False,
        farm_promote=False,
    )
    assert again["needed"] is True
    assert REASON_F in again["reason_ids"]


def test_this_tree_favorite_park_is_not_a_live_trial():
    assert live_selecting_rule_ids() == []


def test_chair_stays_occupied_with_l1_until_parked(tmp_path):
    docs = tmp_path / "golf-offshoot" / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "LEARNING_LANE_15M_RULES.json").write_text(
        json.dumps(
            {
                "rules": [
                    {
                        "id": "R-LIVE-CLOCK",
                        "kind": "selection",
                        "selects": True,
                        "execution": True,
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    (docs / "LEARNING_LANE_15M_BURNED_CLASSES.json").write_text(
        json.dumps({"classes": []}),
        encoding="utf-8",
    )
    (docs / "LEARNING_LANE_15M_SCORECARD_R-LIVE-CLOCK_L1.json").write_text(
        json.dumps({"n": 70, "passes_every_binding_clause": False}),
        encoding="utf-8",
    )
    assert live_selecting_rule_ids(root=tmp_path) == ["R-LIVE-CLOCK"]
    from golf_offshoot.learning_lane_15m.farm import live_look_closed

    assert live_look_closed(root=tmp_path) is False


def test_look_due_rings_when_lab_assigned(tmp_path):
    docs = tmp_path / "golf-offshoot" / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "LEARNING_LANE_15M_RULES.json").write_text(
        json.dumps(
            {
                "rules": [
                    {
                        "id": "R-LIVE-CLOCK",
                        "kind": "selection",
                        "selects": True,
                        "execution": True,
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    (docs / "LEARNING_LANE_15M_SCORECARD_R-LIVE-CLOCK_L1.json").write_text(
        json.dumps({"n": 70, "passes_every_binding_clause": False}),
        encoding="utf-8",
    )
    tick = compute_crew_tick(
        {"watch": _watch(), "roles_owed": []},
        desk_text=_desk(role="lab", status="assigned", job="invent next farm kind"),
        hub_ok=True,
        live_trial_ids=["R-LIVE-CLOCK"],
        honer_freeze_open=False,
        farm_open=True,
        farm_promote=False,
        root=tmp_path,
    )
    assert REASON_K in tick["reason_ids"]
    assert tick["needed"] is True
    assert REASON_F not in tick["reason_ids"]


def test_rule_reached_n_skips_when_l1_exists(tmp_path):
    from golf_offshoot.learning_lane_15m.triggers import rule_reached_n

    docs = tmp_path / "golf-offshoot" / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "LEARNING_LANE_15M_RULES.json").write_text(
        json.dumps(
            {
                "rules": [
                    {
                        "id": "R-SKIP-HOUR-CLOSE",
                        "selects": True,
                        "execution": True,
                        "declared_at": "2026-09-01T00:00:00-04:00",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    (docs / "LEARNING_LANE_15M_EVIDENCE_BAR.json").write_text(
        json.dumps({"looks": {"first_look_n": 70}}),
        encoding="utf-8",
    )
    settled = {}
    for i in range(80):
        hour, minute = divmod(i, 60)
        ticker = f"KXBTC15M-{i}"
        settled[ticker] = {
            "window_id": f"w__2026-09-12T{hour:02d}:{minute:02d}:00Z__",
            "settlement_ts": "2026-09-12T12:00:00-04:00",
        }
    current = {"settled": settled}
    assert [e["ticker"] for e in rule_reached_n(current, root=tmp_path)] == ["R-SKIP-HOUR-CLOSE"]
    (docs / "LEARNING_LANE_15M_SCORECARD_R-SKIP-HOUR-CLOSE_L1.json").write_text(
        "{}\n",
        encoding="utf-8",
    )
    assert rule_reached_n(current, root=tmp_path) == []


def _write_honer_exam(root, *, open_exam=True, parked=False):
    latest = root / "golf-offshoot" / "data" / "honer_15m" / "latest"
    latest.mkdir(parents=True, exist_ok=True)
    (latest / "exam.json").write_text(
        json.dumps(
            {
                "open": open_exam,
                "parked": parked,
                "frozen_family": "H-SKIP-RICH-YES",
                "frozen_theta": 0.81,
                "frozen_delta": 0.04,
                "declared_at": "2026-09-10T14:00:00-04:00",
            }
        ),
        encoding="utf-8",
    )


def test_freeze_open_live_trial_rings_h(tmp_path):
    set_15m_root_override(tmp_path / "kalshi_15m")
    try:
        _write_honer_exam(tmp_path)
        tick = compute_crew_tick(
            {"watch": _watch(), "roles_owed": []},
            desk_text=_idle_blank_desk(),
            hub_ok=True,
            live_trial_ids=["R-SKIP-HOUR-CLOSE"],
            root=tmp_path,
        )
        assert REASON_H in tick["reason_ids"]
        assert REASON_F not in tick["reason_ids"]
        assert tick["needed"] is True
        assert tick["honer_freeze"]["frozen_family"] == "H-SKIP-RICH-YES"
    finally:
        set_15m_root_override(None)


def test_no_freeze_starved_still_rings_f(tmp_path):
    set_15m_root_override(tmp_path / "kalshi_15m")
    try:
        (tmp_path / "golf-offshoot" / "data" / "honer_15m" / "latest").mkdir(parents=True)
        tick = compute_crew_tick(
            {"watch": _watch(), "roles_owed": []},
            desk_text=_idle_blank_desk(),
            hub_ok=True,
            live_trial_ids=[],
            root=tmp_path,
        )
        assert REASON_F in tick["reason_ids"]
        assert REASON_H not in tick["reason_ids"]
    finally:
        set_15m_root_override(None)


def test_assigned_operator_does_not_ring_h(tmp_path):
    set_15m_root_override(tmp_path / "kalshi_15m")
    try:
        _write_honer_exam(tmp_path)
        tick = compute_crew_tick(
            {"watch": _watch(), "roles_owed": []},
            desk_text=_desk(role="operator", status="assigned", job="RUN-ONLY PROPOSED 03"),
            hub_ok=True,
            live_trial_ids=["R-SKIP-HOUR-CLOSE"],
            root=tmp_path,
        )
        assert REASON_H not in tick["reason_ids"]
    finally:
        set_15m_root_override(None)


def test_consult_enabled_does_not_ring_h(tmp_path):
    set_15m_root_override(tmp_path / "kalshi_15m")
    try:
        _write_honer_exam(tmp_path)
        snap = tmp_path / "golf-offshoot" / "data" / "learning_lane_15m" / "latest"
        snap.mkdir(parents=True)
        (snap / "honer_consult.json").write_text(
            json.dumps({"consult_enabled": True}),
            encoding="utf-8",
        )
        tick = compute_crew_tick(
            {"watch": _watch(), "roles_owed": []},
            desk_text=_idle_blank_desk(),
            hub_ok=True,
            live_trial_ids=["R-SKIP-HOUR-CLOSE"],
            root=tmp_path,
        )
        assert REASON_H not in tick["reason_ids"]
    finally:
        set_15m_root_override(None)


def test_consult_candidate_does_not_ring_h(tmp_path):
    set_15m_root_override(tmp_path / "kalshi_15m")
    try:
        _write_honer_exam(tmp_path)
        from golf_offshoot.learning_lane_15m.consult_honer import write_consult_candidate
        from golf_offshoot.learning_lane_15m.paths import latest_dir_15m

        exam = {
            "frozen_family": "H-SKIP-RICH-YES",
            "frozen_theta": 0.81,
            "frozen_delta": 0.04,
            "declared_at": "2026-09-10T14:00:00-04:00",
        }
        dest = latest_dir_15m() / "honer_consult.json"
        dest.parent.mkdir(parents=True, exist_ok=True)
        write_consult_candidate(exam, dest=dest, consult_enabled=False)
        tick = compute_crew_tick(
            {"watch": _watch(), "roles_owed": []},
            desk_text=_idle_blank_desk(),
            hub_ok=True,
            live_trial_ids=["R-SKIP-HOUR-CLOSE"],
            root=tmp_path,
        )
        assert REASON_H not in tick["reason_ids"]
    finally:
        set_15m_root_override(None)


def test_lab_proposed_does_not_count_as_freeze_name(tmp_path):
    """A Lab note is not the freeze name. H still rings until the photocopy exists."""
    set_15m_root_override(tmp_path / "kalshi_15m")
    try:
        _write_honer_exam(tmp_path)
        docs = tmp_path / "golf-offshoot" / "docs"
        docs.mkdir(parents=True)
        (docs / "LEARNING_LANE_15M_LAB_PROPOSED_04.md").write_text(
            "HONER-FROZEN-CONSULT frozen_family H-SKIP-RICH-YES frozen_theta=0.81\n",
            encoding="utf-8",
        )
        tick = compute_crew_tick(
            {"watch": _watch(), "roles_owed": []},
            desk_text=_idle_blank_desk(),
            hub_ok=True,
            live_trial_ids=["R-SKIP-HOUR-CLOSE"],
            root=tmp_path,
        )
        assert REASON_H in tick["reason_ids"]
    finally:
        set_15m_root_override(None)


def test_stamping_h_without_assigning_lab_does_not_silence(tmp_path):
    set_15m_root_override(tmp_path / "kalshi_15m")
    try:
        _write_honer_exam(tmp_path)
        state = {"watch": _watch(), "roles_owed": [], "crew_tick": {}}
        desk = _idle_blank_desk()
        first = compute_crew_tick(
            state,
            desk_text=desk,
            hub_ok=True,
            live_trial_ids=["R-SKIP-HOUR-CLOSE"],
            root=tmp_path,
        )
        assert REASON_H in first["reason_ids"]
        again = compute_crew_tick(
            state,
            desk_text=desk,
            hub_ok=True,
            handled_reason_ids=list(first["reason_ids"]),
            live_trial_ids=["R-SKIP-HOUR-CLOSE"],
            root=tmp_path,
        )
        assert again["needed"] is True
        assert REASON_H in again["reason_ids"]
    finally:
        set_15m_root_override(None)
