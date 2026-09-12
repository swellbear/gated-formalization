"""Factory leash tick: executing L1, then farm notebooks, then freeze photocopy / consult.

Score the seated selecting rule's first 70 before consult may join. Farm cards
are discovery, off hub. Fail-open. Never arms. Never ADMITs. Does not steal a
seated selecting row.
"""

from __future__ import annotations

from typing import Any


def run_leash_tick() -> dict[str, Any]:
    out: dict[str, Any] = {
        "clerical_score": {},
        "look_push": {},
        "sibling_execution": {},
        "farm": {},
        "consult": {},
    }
    try:
        from golf_offshoot.learning_lane_15m.clerical_score import maybe_score_executing

        out["clerical_score"] = maybe_score_executing()
    except Exception as exc:  # noqa: BLE001 — never take PaperWatch down
        out["clerical_score"] = {"error": f"{type(exc).__name__}: {exc}"}
    try:
        from golf_offshoot.learning_lane_15m.look_push import maybe_push_look

        out["look_push"] = maybe_push_look()
    except Exception as exc:  # noqa: BLE001 — never take PaperWatch down
        out["look_push"] = {"error": f"{type(exc).__name__}: {exc}"}
    try:
        from golf_offshoot.learning_lane_15m.sibling_sync import (
            maybe_fetch_origin_farm,
            maybe_observe_sibling_execution,
        )

        maybe_fetch_origin_farm()
        out["sibling_execution"] = maybe_observe_sibling_execution()
    except Exception as ext:  # noqa: BLE001 — never take PaperWatch down
        out["sibling_execution"] = {"error": f"{type(ext).__name__}: {ext}"}
    try:
        from golf_offshoot.learning_lane_15m.clerical_score import maybe_score_farm

        out["farm"] = maybe_score_farm()
    except Exception as exc:  # noqa: BLE001 — never take PaperWatch down
        out["farm"] = {"error": f"{type(exc).__name__}: {exc}"}
    try:
        from golf_offshoot.learning_lane_15m.consult_honer import maybe_sync_and_enable

        out["consult"] = maybe_sync_and_enable()
    except Exception as exc:  # noqa: BLE001 — never take PaperWatch down
        out["consult"] = {"error": f"{type(exc).__name__}: {exc}"}
    return out
