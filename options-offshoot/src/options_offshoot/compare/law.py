"""Hashed options-offshoot method constitution. Frozen morals; t may move later."""

from __future__ import annotations

import hashlib
import json

METHOD_LAW_V1: dict = {
    "id": "method_law_v1",
    "never_auto_trade": True,
    "auto_apply_paper_is_mock_only": True,
    "operator_out_of_ticket_loop": True,
    "sits_beside_gpf": True,
    "does_not_import_golf_offshoot": True,
    "does_not_import_applications": True,
    "admitted_quotes": "polygon_options_snapshot",
    "venue_ask_later": "interactive_brokers_not_v1",
    "refuse_operating_quotes": ["yahoo", "html_scrape", "open_web"],
    "scores_predeclared": [
        "posted_ask_pnl",
        "expiry_settle_pnl",
    ],
    "admitted_into_theta": [
        "spot_from_named_vendor",
        "listed_chain_from_named_vendor",
        "bid_ask_oi_volume_from_named_vendor",
        "time_to_expiry",
        "realized_vol_from_predeclared_price_history",
    ],
    "forbidden_in_theta": [
        "earnings_narrative",
        "iv_from_blogs",
        "missing_greeks_as_zero",
        "invented_bid_from_last",
        "ticker_should_be_in",
        "unseeded_news",
        "schema_default_sigma_on_honest_path",
    ],
    "ticket_bar": "ask",
    "a_control_ticket_bar": "mid",
    "lived_ticket_bar": "both",
    "starting_t": 0.03,
    "mode": "stay_selective",
    "risk": "conservative",
    "independent_compare_bankroll": 20000.0,
    "bankroll_per_field_per_path": True,
    "leftover_callout_required": True,
    "hunter_in_v1": False,
    "index_is_map_only": True,
    "sort_key": "vs_ask",
    "not_sort_key": "p_itm",
    "settle": "expiry",
    "hold_no_ask_rides_to_expiry": True,
    "predeclared_fields": [
        "earnings_us_week",
        "spx_this_friday",
        "index_only",
    ],
    "learner": {
        "keep_t_until_holdout": True,
        "min_events_to_move_t": 8,
        "reject_reasons": [
            "copy_a_because_a_won",
            "shop_index_fattest_rows",
        ],
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
    collapsed = lowered.replace("_", "").replace(" ", "")
    for banned in law["reject_reasons"]:
        token = banned.replace("_", " ")
        if banned.replace("_", "") in collapsed or token in lowered:
            return False, f"reject:{banned}"
    if "shop" in lowered and "index" in lowered:
        return False, "reject:shop_index_fattest_rows"
    if "copy" in lowered and "won" in lowered:
        return False, "reject:copy_a_because_a_won"
    if law.get("this_week_keep_t"):
        return False, "keep_t:this_week_tape_only"
    if n_events < int(law["min_events_to_move_t"]):
        return False, f"keep_t:n_events={n_events}"
    if law.get("keep_t_until_holdout") and "holdout" not in lowered:
        return False, "keep_t:need_holdout"
    return True, "holdout_named"


def index_shop_forbidden(reason: str) -> bool:
    ok, code = learner_may_move_t(n_events=99, reason=reason)
    return (not ok) and "shop_index" in code
