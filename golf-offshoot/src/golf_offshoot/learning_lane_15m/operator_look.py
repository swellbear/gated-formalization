"""Operator L1 look: PARK or CONTINUE from the pushed card.

Never invents tape. No card → no mutation. Does not stop PaperWatch.
Does not arm. Look owner is Operator, not Systems.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from golf_offshoot.learning_lane_15m.clerical_score import (
    FORBIDDEN_SCORE_IDS,
    load_l1_card,
    operator_look_stamp,
    scorecard_path,
)
from golf_offshoot.learning_lane_15m.crew_tick import OPERATOR_LOOK_DONE, seated_selecting_for_look
from golf_offshoot.learning_lane_15m.rules import rule_by_id, set_selecting_execution
from golf_offshoot.localtime import isoformat_now

LOOK_PARK = "PARK"
LOOK_CONTINUE = "CONTINUE"
LOOK_NO_CARD = "no_card"


def _selecting_execution_is_true(rule_id: str, *, root: Path | None) -> bool:
    row = rule_by_id(rule_id, root=root)
    return bool(row) and row.get("selects") is True and row.get("execution") is True


def _drop_selecting_execution(rule_id: str, *, root: Path | None) -> bool:
    """Drop the chair. True when a write ran. Does not invent tape."""
    if not _selecting_execution_is_true(rule_id, root=root):
        return False
    set_selecting_execution(rule_id, False, root=root)
    return True


def apply_operator_look(
    *,
    root: Path | None = None,
    rule_id: str | None = None,
) -> dict[str, Any]:
    """Read the L1 card and PARK or CONTINUE. Never invent windows."""
    result: dict[str, Any] = {
        "ok": False,
        "verdict": LOOK_NO_CARD,
        "mutated": False,
        "invented_tape": False,
        "reason": "",
        "rule_id": rule_id or "",
    }
    seated = None
    if rule_id:
        seated = rule_by_id(rule_id, root=root)
    else:
        seated = seated_selecting_for_look(root=root)
    rid = str((seated or {}).get("id") or rule_id or "")
    result["rule_id"] = rid
    if not rid:
        result["reason"] = "no_selecting_rule"
        return result
    if rid in FORBIDDEN_SCORE_IDS:
        result["reason"] = f"forbidden {rid}"
        return result
    dest = scorecard_path(rid, root=root, look="L1")
    if not dest.is_file():
        result["reason"] = "no_card"
        result["verdict"] = LOOK_NO_CARD
        return result
    card = load_l1_card(rid, root=root)
    if not card:
        result["reason"] = "no_card"
        result["verdict"] = LOOK_NO_CARD
        return result
    existing = operator_look_stamp(card)
    if existing in OPERATOR_LOOK_DONE:
        result["ok"] = True
        result["verdict"] = existing
        result["reason"] = "already_stamped"
        if existing == LOOK_PARK:
            result["mutated"] = _drop_selecting_execution(rid, root=root)
        return result
    passes = card.get("passes_every_binding_clause") is True
    verdict = LOOK_CONTINUE if passes else LOOK_PARK
    # PARK: drop the chair before stamping so a failed registry write cannot
    # leave already_stamped with execution still true.
    if verdict == LOOK_PARK:
        result["mutated"] = _drop_selecting_execution(rid, root=root)
    card["operator_look"] = verdict
    card["operator_look_at"] = isoformat_now()
    dest.write_text(json.dumps(card, indent=2) + "\n", encoding="utf-8")
    result["verdict"] = verdict
    result["ok"] = True
    result["reason"] = verdict.lower()
    return result
