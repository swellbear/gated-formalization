"""Hashed golf-offshoot method constitution. Frozen morals; nerves (t) may move later."""

from __future__ import annotations

import hashlib
import json

METHOD_LAW_V1: dict = {
    "id": "method_law_v1",
    "never_auto_bet": True,
    "auto_apply_paper_is_mock_only": True,
    "operator_out_of_ticket_loop": True,
    "scores_predeclared": [
        "brier_win",
        "posted_price_pnl",
        "posted_price_pnl_win",
        "posted_price_pnl_place",
    ],
    "admitted_into_theta": [
        "espn_to_par_holes_when_live",
        "pga_sg_when_inventory_present",
        "recent_sg_when_event_only_or_datagolf",
        "bovada_or_named_book_posted_decimal",
        "yardage_par_course_type",
    ],
    "forbidden_in_theta": [
        "agronomy_schema_defaults",
        "sg_missing_as_zero",
        "narrative_stuffing",
        "invented_place_from_winner",
        "unnamed_injury_wire",
        "live_tee_pairing_unseeded",
    ],
    "ticket_bar": "posted",
    "display_edgew": True,
    "a_control_ticket_bar": "edgew",
    "lived_ticket_bar": "both",
    "starting_t": 0.03,
    "mode": "stay_selective",
    "risk": "conservative",
    "independent_compare_bankroll": 250.0,
    "compare_place_when_coupon_exists": True,
    "compare_place_markets": ["top_5", "top_10", "top_20"],
    "winner_only_event_ids": ["401811962"],
    "learner": {
        "keep_t_until_holdout": True,
        "min_events_to_move_t": 8,
        "reject_reasons": ["copy_a_edgew_because_a_won"],
        "this_week_keep_t": True,
    },
    "do_not_mutate_lived_lock": True,
}


def law_hash(law: dict | None = None) -> str:
    payload = json.dumps(law or METHOD_LAW_V1, sort_keys=True, default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def learner_may_move_t(*, n_events: int, reason: str) -> tuple[bool, str]:
    """Honesty gate on the threshold learner. Does not declare +EV established."""
    law = METHOD_LAW_V1["learner"]
    lowered = (reason or "").lower()
    for banned in law["reject_reasons"]:
        token = banned.replace("_", " ")
        if banned.replace("_", "") in lowered.replace("_", "").replace(" ", "") or token in lowered:
            return False, f"reject:{banned}"
        if "copy" in lowered and "edgew" in lowered:
            return False, "reject:copy_a_edgew_because_a_won"
    if law.get("this_week_keep_t"):
        return False, "keep_t:this_week_tape_only"
    if n_events < int(law["min_events_to_move_t"]):
        return False, f"keep_t:n_events={n_events}"
    if law.get("keep_t_until_holdout") and "holdout" not in lowered:
        return False, "keep_t:need_holdout"
    return True, "holdout_named"
