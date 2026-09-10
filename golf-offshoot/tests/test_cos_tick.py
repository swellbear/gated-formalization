"""CoS gate: do not invent score Jobs from name-clear owes."""

from golf_offshoot.learning_lane_15m.cos_tick import (
    ACTION_ASSIGN,
    ACTION_CLOSEOUT,
    ACTION_QUIET,
    decide_cos_action,
)
from golf_offshoot.learning_lane_15m.crew_tick import REASON_A_DONE, REASON_A_IDLE, REASON_B


def _desk(*, role="chief-of-staff", status="idle", job="—", thread=""):
    return (
        "# Agent desk\n\n"
        "| Field | Value |\n"
        "|-------|--------|\n"
        f"| Active role | {role} |\n"
        f"| Job | {job} |\n"
        f"| Status | {status} |\n"
        "| Handoff | — |\n\n"
        "## Thread\n\n"
        f"{thread or '- 2026-09-10 11:00 ET  chief-of-staff: idle. next=idle'}\n"
    )


def _owed(role, *, reasons=None, since="2026-09-10T10:41:25-04:00"):
    return {
        "role": role,
        "reasons": list(reasons or []),
        "ticks_unanswered": 1,
        "owed_since": since,
    }


def test_no_wake_does_not_invent_worker_done():
    decision = decide_cos_action(_desk(status="idle"))
    assert decision["action"] == ACTION_QUIET
    assert decision["reason"] == "no_wake_do_not_invent"
    assert decision["assign"] is False


def test_needed_false_is_quiet():
    wake = {
        "roles_owed": [],
        "crew_tick": {
            "needed": False,
            "quiet": True,
            "reason_ids": [],
            "handled_reason_ids": ["A_idle_uncovered_judicial"],
        },
    }
    decision = decide_cos_action(_desk(), wake=wake)
    assert decision["action"] == ACTION_QUIET
    assert decision["assign"] is False


def test_status_done_is_closeout():
    wake = {
        "roles_owed": [],
        "crew_tick": {
            "needed": True,
            "reason_ids": [REASON_A_DONE],
            "handled_reason_ids": [],
        },
    }
    decision = decide_cos_action(
        _desk(
            role="operator",
            status="done",
            thread="- 2026-09-10 10:40 ET  operator → chief-of-staff: park. next=chief-of-staff",
        ),
        wake=wake,
        crew_tick=wake["crew_tick"],
    )
    assert decision["action"] == ACTION_CLOSEOUT
    assert decision["reason"] == "worker_done"
    assert decision["assign"] is False


def test_operator_name_clear_is_closeout_not_score():
    wake = {
        "roles_owed": [
            _owed(
                "operator",
                reasons=[
                    "rule_reached_n R-SKIP-COINFLIP",
                    "rule_reached_n R-SKIP-2TO1-FAVORITE",
                ],
            )
        ],
        "crew_tick": {
            "needed": True,
            "reason_ids": [REASON_A_IDLE, REASON_B],
            "handled_reason_ids": [],
        },
    }
    decision = decide_cos_action(_desk(), wake=wake, crew_tick=wake["crew_tick"])
    assert decision["action"] == ACTION_CLOSEOUT
    assert decision["reason"] == "name_clear_not_score"
    assert decision["role"] is None
    assert decision["assign"] is False


def test_lab_owed_is_not_assigned():
    wake = {
        "roles_owed": [_owed("lab", reasons=["lab_proposed"])],
        "crew_tick": {
            "needed": True,
            "reason_ids": [REASON_A_IDLE],
            "handled_reason_ids": [],
        },
    }
    decision = decide_cos_action(_desk(job="one PROPOSED 03"), wake=wake, crew_tick=wake["crew_tick"])
    assert decision["action"] == ACTION_CLOSEOUT
    assert decision["assign"] is False
    assert decision["role"] != "lab"


def test_coinflip_score_job_is_forbidden():
    wake = {
        "roles_owed": [_owed("operator", reasons=["rule_reached_n R-SKIP-COINFLIP"])],
        "crew_tick": {
            "needed": True,
            "reason_ids": [REASON_A_IDLE],
            "handled_reason_ids": [],
        },
    }
    decision = decide_cos_action(
        _desk(job="score R-SKIP-COINFLIP L1"),
        wake=wake,
        crew_tick=wake["crew_tick"],
    )
    assert decision["action"] == ACTION_CLOSEOUT
    assert decision["reason"] == "forbidden_job"


def test_legal_soften_critic_is_assign():
    wake = {
        "roles_owed": [_owed("soften-critic", reasons=["artifact_unreviewed evidence_bar"])],
        "crew_tick": {
            "needed": True,
            "reason_ids": [REASON_A_IDLE, REASON_B],
            "handled_reason_ids": [],
        },
    }
    decision = decide_cos_action(_desk(), wake=wake, crew_tick=wake["crew_tick"])
    assert decision["action"] == ACTION_ASSIGN
    assert decision["role"] == "soften-critic"
    assert decision["assign"] is True


def test_assigned_worker_is_quiet():
    wake = {
        "roles_owed": [_owed("operator", reasons=["artifact_unreviewed evidence_bar"])],
        "crew_tick": {
            "needed": True,
            "reason_ids": [REASON_B],
            "handled_reason_ids": [],
        },
    }
    decision = decide_cos_action(
        _desk(role="operator", status="assigned", job="record CRITIC 20"),
        wake=wake,
        crew_tick=wake["crew_tick"],
    )
    assert decision["action"] == ACTION_QUIET
    assert decision["reason"] == "assigned_worker_covers"
