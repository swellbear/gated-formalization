"""Worker-tick gate: one fire becomes the assigned desk role, or no-ops.

CoS assigns. This module only answers whether a worker automation fire
should run. It does not assign the next role, does not become CoS, and
does not persist to the gitignored wake. Done-state lives on the desk.
"""

from __future__ import annotations

from typing import Any

from golf_offshoot.learning_lane_15m.crew_tick import parse_desk

COS_ROLE = "chief-of-staff"

#: Roles a worker fire may become. CoS is deliberately absent.
WORKER_ROLES = frozenset(
    {
        "lab",
        "operator",
        "systems",
        "validator",
        "soften-critic",
        "digestor",
        "illustrator",
    }
)

SKILL_PATHS = {role: f".cursor/skills/gpf-{role}/SKILL.md" for role in WORKER_ROLES}

REASON_STATUS_NOT_ASSIGNED = "status_not_assigned"
REASON_EMPTY_ROLE = "empty_active_role"
REASON_COS_OWNS = "cos_owns_that"
REASON_UNKNOWN_ROLE = "unknown_role"
REASON_ASSIGNED_WORKER = "assigned_worker"


def decide_worker_tick(desk_text: str) -> dict[str, Any]:
    """Return whether this fire should become Active role.

    ``run`` is true only when desk Status is exactly ``assigned`` and
    Active role is one of ``WORKER_ROLES``. Unknown role is a no-op that
    may leave one desk thread line. Every other miss writes nothing.
    """
    desk = parse_desk(desk_text)
    status = desk["status"]
    role = desk["active_role"]
    base: dict[str, Any] = {
        "run": False,
        "role": role,
        "status": status,
        "skill": None,
        "roles_this_fire": [],
        "write_desk_thread": False,
        "thread_line": "",
        "next": "",
        "reason": REASON_STATUS_NOT_ASSIGNED,
    }

    if status != "assigned":
        return base

    if not role:
        return {**base, "reason": REASON_EMPTY_ROLE}

    if role == COS_ROLE:
        return {**base, "reason": REASON_COS_OWNS}

    if role not in WORKER_ROLES:
        return {
            **base,
            "reason": REASON_UNKNOWN_ROLE,
            "write_desk_thread": True,
            "thread_line": (
                f"worker-tick: unknown Active role={role}; no-op. next=chief-of-staff"
            ),
        }

    return {
        **base,
        "run": True,
        "reason": REASON_ASSIGNED_WORKER,
        "skill": SKILL_PATHS[role],
        "roles_this_fire": [role],
        "next": COS_ROLE,
    }


def lock_one_role(decision: dict[str, Any]) -> frozenset[str]:
    """Roles this fire may become. Size is 0 or 1 — never both Critic and Operator."""
    if not decision.get("run"):
        return frozenset()
    role = str(decision.get("role") or "").strip().lower()
    if role not in WORKER_ROLES:
        return frozenset()
    return frozenset({role})
