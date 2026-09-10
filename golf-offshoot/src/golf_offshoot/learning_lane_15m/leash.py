"""Factory leash tick: freeze photocopy, consult gates, clerical executing score.

Fail-open. Never arms. Never ADMITs. Does not steal a seated hour-close row.
"""

from __future__ import annotations

from typing import Any


def run_leash_tick() -> dict[str, Any]:
    out: dict[str, Any] = {"consult": {}, "clerical_score": {}}
    try:
        from golf_offshoot.learning_lane_15m.consult_honer import maybe_sync_and_enable

        out["consult"] = maybe_sync_and_enable()
    except Exception as exc:  # noqa: BLE001 — never take PaperWatch down
        out["consult"] = {"error": f"{type(exc).__name__}: {exc}"}
    try:
        from golf_offshoot.learning_lane_15m.clerical_score import maybe_score_executing

        out["clerical_score"] = maybe_score_executing()
    except Exception as exc:  # noqa: BLE001
        out["clerical_score"] = {"error": f"{type(exc).__name__}: {exc}"}
    return out
