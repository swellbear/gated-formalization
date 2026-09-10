"""CoS gate: assign only a legal next worker, or idle.

Cloud CoS that only reads ``crew_tick.needed`` will assign Operator to
score because the wake still names ``rule_reached_n`` for favorite
(already PARK) and coinflip (Hard NO). That is the opposite of
unattended-and-smart.

Forbidden assigns (code + skill): lab, score R-SKIP-COINFLIP, re-score
PARK'd R-SKIP-2TO1-FAVORITE, consult_enabled, HOLD lift, arm, bind, git
push to master.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from golf_offshoot.learning_lane_15m.crew_tick import (
    JUDICIAL_ROLES,
    WORKER_ROLES,
    compute_crew_tick,
    parse_desk,
)

ACTION_QUIET = "quiet"
ACTION_CLOSEOUT = "closeout"
ACTION_ASSIGN = "assign"

#: CoS must never assign Lab. No PROPOSED 03 without Founder.
FORBIDDEN_ASSIGN_ROLES = frozenset({"lab"})

#: Wake subjects that are name-clear bookkeeping, not a score Job.
NAME_CLEAR_SUBJECTS = frozenset(
    {
        "R-SKIP-COINFLIP",
        "R-SKIP-2TO1-FAVORITE",
    }
)

LEGAL_ASSIGN_ROLES = frozenset(
    {
        "operator",
        "digestor",
        "soften-critic",
        "systems",
        "illustrator",
        "validator",
    }
)

FORBIDDEN_JOB_NEEDLES = (
    "consult_enabled",
    "enable consult",
    "consult enabled",
    "lift the hold",
    "lift hold",
    "hold lift",
    "arm trading",
    "trading_armed",
    "bind the bar",
    "binding: true",
    "git push to master",
    "push to master",
    "score r-skip-coinflip",
    "score r-skip-2to1-favorite",
    "re-score r-skip-2to1-favorite",
)


def _role(entry: dict[str, Any]) -> str:
    return str(entry.get("role") or "").strip().lower()


def _reasons(entry: dict[str, Any]) -> list[str]:
    return [str(r).strip() for r in (entry.get("reasons") or []) if str(r).strip()]


def operator_owed_reasons(wake: dict[str, Any] | None) -> list[str]:
    out: list[str] = []
    for entry in (wake or {}).get("roles_owed") or []:
        if _role(entry) == "operator":
            out.extend(_reasons(entry))
    return out


def is_name_clear_reason(reason: str) -> bool:
    text = (reason or "").strip()
    if not text.lower().startswith("rule_reached_n"):
        return False
    subject = text.split(" ", 1)[1].strip() if " " in text else ""
    return subject in NAME_CLEAR_SUBJECTS


def only_name_clear_reasons(reasons: list[str]) -> bool:
    if not reasons:
        return False
    return all(is_name_clear_reason(r) for r in reasons)


def _parse_iso(value: Any) -> datetime | None:
    text = str(value or "").strip()
    if not text:
        return None
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def _stale_unreviewed_critic_only(
    owed: list[dict[str, Any]],
    uncovered_roles: list[str],
    *,
    last_cos_at: str = "",
) -> bool:
    """Zero-objection stop: do not assign another attack already seen at last CoS."""
    leftover = [r for r in uncovered_roles if r != "operator"]
    if leftover != ["soften-critic"]:
        return False
    reasons: list[str] = []
    since_stamp = None
    for entry in owed:
        if _role(entry) != "soften-critic":
            continue
        reasons.extend(_reasons(entry))
        since_stamp = _parse_iso(entry.get("owed_since"))
    if not reasons or not all(r.startswith("artifact_unreviewed") for r in reasons):
        return False
    last = _parse_iso(last_cos_at)
    if last is None or since_stamp is None:
        return True
    return since_stamp <= last


def job_is_forbidden(job: str) -> bool:
    low = (job or "").lower()
    return any(needle in low for needle in FORBIDDEN_JOB_NEEDLES)


def _base(*, action: str, reason: str, role: str | None = None, job: str | None = None) -> dict[str, Any]:
    return {
        "action": action,
        "role": role,
        "job": job,
        "reason": reason,
        "skill": f".cursor/skills/gpf-{role}/SKILL.md" if role else None,
        "assign": action == ACTION_ASSIGN,
    }


def decide_cos_action(
    desk_text: str,
    *,
    wake: dict[str, Any] | None = None,
    crew_tick: dict[str, Any] | None = None,
    leave_off_text: str = "",
) -> dict[str, Any]:
    """Return quiet / closeout / assign. Never invent A_worker_done from an empty VM."""
    desk = parse_desk(desk_text)
    status = desk["status"]
    active = desk["active_role"]
    job = desk["job"]

    if wake is None and crew_tick is None:
        if status == "done":
            return _base(action=ACTION_CLOSEOUT, reason="worker_done")
        return _base(action=ACTION_QUIET, reason="no_wake_do_not_invent")

    tick = crew_tick
    if tick is None:
        tick = compute_crew_tick(
            wake,
            desk_text=desk_text,
            leave_off_text=leave_off_text,
            hub_ok=True,
        )
    tick = tick or {}
    reason_ids = [str(x) for x in (tick.get("reason_ids") or [])]
    handled = [str(x) for x in (tick.get("handled_reason_ids") or [])]
    needed = bool(tick.get("needed"))

    if status == "assigned" and active in WORKER_ROLES:
        return _base(action=ACTION_QUIET, reason="assigned_worker_covers", role=active, job=job)

    if not needed or (reason_ids and set(reason_ids) <= set(handled)):
        return _base(action=ACTION_QUIET, reason="quiet_or_handled")

    if status == "done":
        return _base(action=ACTION_CLOSEOUT, reason="worker_done")

    if job_is_forbidden(job):
        return _base(action=ACTION_CLOSEOUT, reason="forbidden_job")

    owed = list((wake or {}).get("roles_owed") or [])
    judicial = [e for e in owed if _role(e) in JUDICIAL_ROLES]
    uncovered_roles = sorted({_role(e) for e in judicial})
    op_reasons = operator_owed_reasons(wake)

    if "lab" in uncovered_roles:
        uncovered_roles = [r for r in uncovered_roles if r != "lab"]
        if not uncovered_roles and only_name_clear_reasons(op_reasons):
            return _base(action=ACTION_CLOSEOUT, reason="forbidden_lab")
        if not uncovered_roles:
            return _base(action=ACTION_CLOSEOUT, reason="forbidden_lab")

    if only_name_clear_reasons(op_reasons):
        uncovered_roles = [r for r in uncovered_roles if r != "operator"]
        if not uncovered_roles:
            return _base(
                action=ACTION_CLOSEOUT,
                reason="name_clear_not_score",
            )

    if _stale_unreviewed_critic_only(
        owed,
        uncovered_roles,
        last_cos_at=str(tick.get("last_cos_at") or ""),
    ):
        return _base(action=ACTION_CLOSEOUT, reason="zero_objection_stop")

    legal = [r for r in uncovered_roles if r in LEGAL_ASSIGN_ROLES and r not in FORBIDDEN_ASSIGN_ROLES]
    if "operator" in legal and only_name_clear_reasons(op_reasons):
        legal = [r for r in legal if r != "operator"]

    if not legal:
        return _base(action=ACTION_CLOSEOUT, reason="uncovered_not_legal")

    # One worker. Prefer Operator for genuine judicial work, else the first legal name.
    role = "operator" if "operator" in legal else legal[0]
    if role in FORBIDDEN_ASSIGN_ROLES:
        return _base(action=ACTION_CLOSEOUT, reason="forbidden_role")
    return _base(action=ACTION_ASSIGN, reason="legal_next_worker", role=role, job=job)
