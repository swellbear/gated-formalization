"""CoS gate: assign only a legal next worker, or idle.

Cloud CoS that only reads ``crew_tick.needed`` will assign Operator to
score because the wake still names ``rule_reached_n`` for favorite
(already PARK) and coinflip (Hard NO). That is the opposite of
unattended-and-smart.

Forbidden assigns (code + skill): score R-SKIP-COINFLIP, re-score
PARK'd R-SKIP-2TO1-FAVORITE, arm, bind, git push to master. Lab is legal:
F_continuation assigns one 15m PROPOSED. I_farm_open assigns Lab to date farm
notebooks (hunger). J_farm_promote dates the queued keeper then Operator RUN-ONLY.
H_honer_freeze is clerical
(freeze photocopy); CoS does not assign Lab to retype theta. This fold
does not enable consult unless file gates already hold.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from golf_offshoot.learning_lane_15m.crew_tick import (
    JUDICIAL_ROLES,
    REASON_F,
    REASON_H,
    REASON_I,
    REASON_J,
    REASON_K,
    WORKER_ROLES,
    compute_crew_tick,
    desk_lab_done_owes_operator,
    parse_desk,
)

ACTION_QUIET = "quiet"
ACTION_CLOSEOUT = "closeout"
ACTION_ASSIGN = "assign"

#: CoS may assign Lab when F_continuation is owed. CoS does not author the
#: PROPOSED. Score / arm / bind / master push stay forbidden.
FORBIDDEN_ASSIGN_ROLES = frozenset()

LAB_INVENT_JOB = (
    "one 15m PROPOSED under the invent contract (mechanism catalog, density "
    "floor 10/n, kill anatomy, unburned including RETUNE-CLOCK-MINUTE, "
    "HONER-FAMILY-AMEND only after a dead honer exam or catalog exhaust — "
    "do not append a third family until the two dated families finish exams; "
    "HONER-FROZEN-REPLACE only after consult has lived and hour-close is not "
    "the live trial; do not retype freeze theta; pre-reg, live falsifier); "
    "handoff operator"
)

LAB_FARM_OPEN_JOB = (
    "date every currently legal unused catalog slot as farm notebooks in one fire "
    "(LEARNING_LANE_15M_FARM.json, execution false, do not steal the chair); "
    "if none unused, invent the next kind (product-structure skip rate, unburned, "
    "not a clone) and date it as a farm notebook; if you cannot name another kind, "
    "write LEARNING_LANE_15M_FARM_MENU_EXHAUSTED.json so I stops; do not retype "
    "freeze theta; do not set execution true; handoff operator"
)

LAB_FARM_PROMOTE_JOB = (
    "date the next queued farm keeper (declared_at head, not richest pnl) as a "
    "PROPOSED executing row with execution still false; Operator RUN-ONLY flips "
    "execution; do not arm; do not ADMIT; do not score; handoff operator"
)

OPERATOR_LOOK_JOB = (
    "PARK or CONTINUE from the L1 scorecard; never invent tape; "
    "do not stop PaperWatch; do not arm"
)

OPERATOR_LAB_PROPOSED_JOB = (
    "RUN-ONLY the sitting Lab PROPOSED; do not ADMIT; do not arm; do not score"
)

#: Hard-NO / already-PARK'd ids whose rule_reached_n is bookkeeping without files.
#: Hour-close (or any executing look) is NOT frozen here — name-clear is from files.
NAME_CLEAR_SUBJECTS = frozenset(
    {
        "R-SKIP-COINFLIP",
        "R-SKIP-2TO1-FAVORITE",
    }
)

LEGAL_ASSIGN_ROLES = frozenset(
    {
        "lab",
        "operator",
        "digestor",
        "soften-critic",
        "systems",
        "illustrator",
        "validator",
    }
)

FORBIDDEN_JOB_NEEDLES = (
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


def is_name_clear_reason(
    reason: str,
    *,
    root: Path | None = None,
    registry: dict[str, Any] | None = None,
) -> bool:
    """Name-clear from files, not a frozen hour-close subject list.

    Hard NO (coinflip) and PARK'd+L1 (favorite) are bookkeeping. An executing
    selecting rule without operator_look PARK/CONTINUE is the look, not closeout.
    """
    from golf_offshoot.learning_lane_15m.clerical_score import (
        FORBIDDEN_SCORE_IDS,
        load_l1_card,
        operator_look_stamp,
    )
    from golf_offshoot.learning_lane_15m.crew_tick import OPERATOR_LOOK_DONE

    text = (reason or "").strip()
    if not text.lower().startswith("rule_reached_n"):
        return False
    subject = text.split(" ", 1)[1].strip() if " " in text else ""
    if not subject:
        return False
    row = None
    if registry is not None:
        for item in registry.get("rules") or []:
            if isinstance(item, dict) and str(item.get("id") or "") == subject:
                row = item
                break
    elif root is not None:
        try:
            from golf_offshoot.learning_lane_15m.rules import rule_by_id

            row = rule_by_id(subject, root=root)
        except Exception:  # noqa: BLE001 — missing registry is not name-clear for a live look
            row = None
    if row is None:
        return subject in NAME_CLEAR_SUBJECTS or subject in FORBIDDEN_SCORE_IDS
    card = load_l1_card(subject, root=root)
    stamp = operator_look_stamp(card)
    if row.get("execution") is True:
        return stamp in OPERATOR_LOOK_DONE
    if subject in FORBIDDEN_SCORE_IDS or subject in NAME_CLEAR_SUBJECTS:
        return True
    return bool(card) or stamp in OPERATOR_LOOK_DONE


def only_name_clear_reasons(
    reasons: list[str],
    *,
    root: Path | None = None,
    registry: dict[str, Any] | None = None,
) -> bool:
    if not reasons:
        return False
    return all(is_name_clear_reason(r, root=root, registry=registry) for r in reasons)


def operator_owed_lab_proposed(
    wake: dict[str, Any] | None,
    *,
    root: Path | None = None,
) -> bool:
    for reason in operator_owed_reasons(wake):
        if str(reason).strip().lower().startswith("lab_proposed"):
            return True
    if root is None:
        return False
    from golf_offshoot.learning_lane_15m.triggers import lab_proposed

    try:
        return bool(lab_proposed(root=root))
    except Exception:  # noqa: BLE001 — blindness still owes Operator, not invent
        return True


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


def _critic_new_hash(
    owed: list[dict[str, Any]],
    *,
    last_cos_at: str = "",
) -> bool:
    """True when Soften Critic is owed artifact_unreviewed newer than last CoS."""
    last = _parse_iso(last_cos_at)
    for entry in owed:
        if _role(entry) != "soften-critic":
            continue
        reasons = _reasons(entry)
        if not reasons or not all(r.startswith("artifact_unreviewed") for r in reasons):
            continue
        since_stamp = _parse_iso(entry.get("owed_since"))
        if last is None:
            return True
        if since_stamp is not None and since_stamp > last:
            return True
    return False


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


def _assign_lab() -> dict[str, Any]:
    return _base(
        action=ACTION_ASSIGN,
        reason="continuation_assign_lab",
        role="lab",
        job=LAB_INVENT_JOB,
    )


def _assign_lab_farm_open() -> dict[str, Any]:
    return _base(
        action=ACTION_ASSIGN,
        reason="farm_open_assign_lab",
        role="lab",
        job=LAB_FARM_OPEN_JOB,
    )


def _assign_lab_farm_promote() -> dict[str, Any]:
    return _base(
        action=ACTION_ASSIGN,
        reason="farm_promote_assign_lab",
        role="lab",
        job=LAB_FARM_PROMOTE_JOB,
    )


def _assign_operator_lab_proposed() -> dict[str, Any]:
    return _base(
        action=ACTION_ASSIGN,
        reason="lab_proposed_operator_first",
        role="operator",
        job=OPERATOR_LAB_PROPOSED_JOB,
    )


def lab_honer_freeze_job(snap: dict[str, Any] | None) -> str:
    """Deprecated: H is clerical. Kept so old tests can import the name."""
    snap = snap or {}
    family = snap.get("frozen_family") or snap.get("family") or "?"
    return (
        "clerical freeze photocopy (not a Lab invent): "
        f"family={family}; do not invent theta; do not enable consult"
    )


def _assign_lab_honer(snap: dict[str, Any] | None = None) -> dict[str, Any]:
    return _base(
        action=ACTION_CLOSEOUT,
        reason="honer_freeze_clerical",
        job=lab_honer_freeze_job(snap),
    )


def decide_cos_action(
    desk_text: str,
    *,
    wake: dict[str, Any] | None = None,
    crew_tick: dict[str, Any] | None = None,
    leave_off_text: str = "",
    root: Path | None = None,
) -> dict[str, Any]:
    """Return quiet / closeout / assign. Never invent A_worker_done from an empty VM."""
    desk = parse_desk(desk_text)
    status = desk["status"]
    active = desk["active_role"]
    job = desk["job"]

    if wake is None and crew_tick is None:
        if desk_lab_done_owes_operator(desk):
            return _assign_operator_lab_proposed()
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
            root=root,
        )
    tick = tick or {}
    reason_ids = [str(x) for x in (tick.get("reason_ids") or [])]
    handled = [str(x) for x in (tick.get("handled_reason_ids") or [])]
    needed = bool(tick.get("needed"))
    f_owed = REASON_F in reason_ids
    h_owed = REASON_H in reason_ids
    i_owed = REASON_I in reason_ids
    j_owed = REASON_J in reason_ids
    k_owed = REASON_K in reason_ids
    freeze_snap = tick.get("honer_freeze") if isinstance(tick.get("honer_freeze"), dict) else None

    if k_owed and not (status == "assigned" and active == "operator"):
        return _base(
            action=ACTION_ASSIGN,
            reason="look_due_operator",
            role="operator",
            job=OPERATOR_LOOK_JOB,
        )

    if status == "assigned" and active in WORKER_ROLES:
        return _base(action=ACTION_QUIET, reason="assigned_worker_covers", role=active, job=job)

    sitting = operator_owed_lab_proposed(wake, root=root) or desk_lab_done_owes_operator(desk)
    if sitting:
        return _assign_operator_lab_proposed()

    if not needed:
        return _base(action=ACTION_QUIET, reason="quiet_or_handled")
    if (
        reason_ids
        and set(reason_ids) <= set(handled)
        and REASON_F not in reason_ids
        and REASON_H not in reason_ids
        and REASON_I not in reason_ids
        and REASON_J not in reason_ids
        and REASON_K not in reason_ids
    ):
        return _base(action=ACTION_QUIET, reason="quiet_or_handled")

    if status == "done":
        return _base(action=ACTION_CLOSEOUT, reason="worker_done")

    if job_is_forbidden(job):
        return _base(action=ACTION_CLOSEOUT, reason="forbidden_job")

    owed = list((wake or {}).get("roles_owed") or [])
    judicial = [e for e in owed if _role(e) in JUDICIAL_ROLES]
    uncovered_roles = sorted({_role(e) for e in judicial})
    op_reasons = operator_owed_reasons(wake)

    # Wake may name Lab by mistake; invent is F_continuation, not a Lab owe.
    if "lab" in uncovered_roles:
        uncovered_roles = [r for r in uncovered_roles if r != "lab"]

    if only_name_clear_reasons(op_reasons, root=root):
        uncovered_roles = [r for r in uncovered_roles if r != "operator"]
        if not uncovered_roles and not f_owed and not h_owed and not i_owed and not j_owed and not k_owed:
            return _base(
                action=ACTION_CLOSEOUT,
                reason="name_clear_not_score",
            )

    critic_new = _critic_new_hash(owed, last_cos_at=str(tick.get("last_cos_at") or ""))
    if critic_new and "soften-critic" in uncovered_roles:
        return _base(
            action=ACTION_ASSIGN,
            reason="legal_next_worker",
            role="soften-critic",
            job=job if job and job.strip() not in {"", "—"} else "attack the new artifact hash",
        )

    if _stale_unreviewed_critic_only(
        owed,
        uncovered_roles,
        last_cos_at=str(tick.get("last_cos_at") or ""),
    ):
        if f_owed:
            return _assign_lab()
        if i_owed:
            return _assign_lab_farm_open()
        if j_owed:
            return _assign_lab_farm_promote()
        if h_owed:
            return _assign_lab_honer(freeze_snap)
        return _base(action=ACTION_CLOSEOUT, reason="zero_objection_stop")

    if f_owed:
        return _assign_lab()
    if i_owed:
        return _assign_lab_farm_open()
    if j_owed:
        return _assign_lab_farm_promote()
    if h_owed:
        return _assign_lab_honer(freeze_snap)

    legal = [r for r in uncovered_roles if r in LEGAL_ASSIGN_ROLES and r not in FORBIDDEN_ASSIGN_ROLES]
    if "operator" in legal and only_name_clear_reasons(op_reasons, root=root):
        legal = [r for r in legal if r != "operator"]

    if not legal:
        return _base(action=ACTION_CLOSEOUT, reason="uncovered_not_legal")

    # One worker. Prefer Operator for genuine judicial work, else the first legal name.
    role = "operator" if "operator" in legal else legal[0]
    if role in FORBIDDEN_ASSIGN_ROLES:
        return _base(action=ACTION_CLOSEOUT, reason="forbidden_role")
    assign_job = LAB_INVENT_JOB if role == "lab" else job
    if role == "operator" and any(
        str(r).strip().lower().startswith("rule_reached_n")
        and not is_name_clear_reason(r, root=root)
        for r in op_reasons
    ):
        assign_job = OPERATOR_LOOK_JOB
    return _base(action=ACTION_ASSIGN, reason="legal_next_worker", role=role, job=assign_job)
