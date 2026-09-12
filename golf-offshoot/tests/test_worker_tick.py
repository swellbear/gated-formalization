"""Worker tick: no-op unless Status=assigned; one role per fire."""

from golf_offshoot.learning_lane_15m.worker_tick import (
    REASON_ASSIGNED_WORKER,
    REASON_COS_OWNS,
    REASON_EMPTY_ROLE,
    REASON_STATUS_NOT_ASSIGNED,
    REASON_UNKNOWN_ROLE,
    SKILL_PATHS,
    decide_worker_tick,
    lock_one_role,
)


def _desk(*, role="lab", status="assigned", job="one PROPOSED selection rule"):
    return (
        "# Agent desk\n\n"
        "| Field | Value |\n"
        "|-------|--------|\n"
        f"| Active role | {role} |\n"
        f"| Job | {job} |\n"
        f"| Status | {status} |\n"
        "| Handoff | — |\n\n"
        "## Thread\n\n"
        "- 2026-09-08 14:58 ET  chief-of-staff → lab: one PROPOSED. next=lab\n"
    )


def test_idle_is_noop():
    decision = decide_worker_tick(_desk(status="idle", role="lab"))
    assert decision["run"] is False
    assert decision["reason"] == REASON_STATUS_NOT_ASSIGNED
    assert decision["roles_this_fire"] == []
    assert decision["write_desk_thread"] is False
    assert lock_one_role(decision) == frozenset()


def test_done_working_and_empty_status_write_nothing():
    for status in ("done", "working", "waiting-founder", ""):
        decision = decide_worker_tick(_desk(status=status, role="operator"))
        assert decision["run"] is False
        assert decision["reason"] == REASON_STATUS_NOT_ASSIGNED
        assert decision["write_desk_thread"] is False
        assert decision["thread_line"] == ""


def test_assigned_lab_reads_lab_skill_only():
    decision = decide_worker_tick(_desk(status="assigned", role="lab"))
    assert decision["run"] is True
    assert decision["reason"] == REASON_ASSIGNED_WORKER
    assert decision["role"] == "lab"
    assert decision["skill"] == ".cursor/skills/gpf-lab/SKILL.md"
    assert decision["skill"] == SKILL_PATHS["lab"]
    assert decision["roles_this_fire"] == ["lab"]
    assert decision["next"] == "chief-of-staff"
    assert lock_one_role(decision) == frozenset({"lab"})
    assert "gpf-operator" not in (decision["skill"] or "")
    assert "gpf-soften-critic" not in (decision["skill"] or "")


def test_assigned_chief_of_staff_is_noop():
    decision = decide_worker_tick(_desk(status="assigned", role="chief-of-staff"))
    assert decision["run"] is False
    assert decision["reason"] == REASON_COS_OWNS
    assert decision["skill"] is None
    assert decision["write_desk_thread"] is False
    assert lock_one_role(decision) == frozenset()


def test_empty_active_role_writes_nothing():
    decision = decide_worker_tick(_desk(status="assigned", role=""))
    assert decision["run"] is False
    assert decision["reason"] == REASON_EMPTY_ROLE
    assert decision["write_desk_thread"] is False


def test_unknown_role_noops_and_asks_for_a_thread_line():
    decision = decide_worker_tick(_desk(status="assigned", role="foundry"))
    assert decision["run"] is False
    assert decision["reason"] == REASON_UNKNOWN_ROLE
    assert decision["write_desk_thread"] is True
    assert "unknown Active role=foundry" in decision["thread_line"]
    assert lock_one_role(decision) == frozenset()


def test_same_fire_cannot_be_soften_critic_and_operator():
    for role in ("operator", "soften-critic", "lab", "systems"):
        locked = lock_one_role(decide_worker_tick(_desk(status="assigned", role=role)))
        assert len(locked) <= 1
        assert not {"soften-critic", "operator"} <= locked


def test_live_14_58_lab_assign_would_run_lab_only():
    """The exhibit: CoS assigned; worker fire becomes lab; this authoring turn does not."""
    desk = (
        "# Agent desk\n\n"
        "| Field | Value |\n"
        "|-------|--------|\n"
        "| Active role | lab |\n"
        "| Job | One PROPOSED selection rule on KXBTC15M paper only. |\n"
        "| Status | assigned |\n"
        "| Handoff | — |\n"
        "| Waiting on Founder | **N** |\n"
    )
    decision = decide_worker_tick(desk)
    assert decision["run"] is True
    assert decision["role"] == "lab"
    assert decision["skill"] == ".cursor/skills/gpf-lab/SKILL.md"
    assert lock_one_role(decision) == frozenset({"lab"})
