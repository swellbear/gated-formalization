"""Dated H-SKIP-RICH-YES policy. Load from HONER_15M_RULES.json when present."""

from __future__ import annotations

import json
from typing import Any

from golf_offshoot.honer_15m.paths import registry_path

START_THETA = 0.75
THETA_MIN = 0.55
THETA_MAX = 0.90
STEP = 0.02
FREEZE_ABS_DELTA = 0.05
FREEZE_MIN_SEARCH_SETTLED = 20
EXAM_N = 70
FUTILITY_LOOKS = (20, 40)
SEED_BANKROLL = 100.0
STAKE = 1.0
PERMUTATION_SEED = 20260909
DECLARED_AT = "2026-09-09T13:40:00-04:00"
RULE_ID = "H-SKIP-RICH-YES"


def load_policy() -> dict[str, Any]:
    path = registry_path()
    if not path.is_file():
        return {
            "start_theta": START_THETA,
            "theta_min": THETA_MIN,
            "theta_max": THETA_MAX,
            "step": STEP,
            "freeze_abs_delta": FREEZE_ABS_DELTA,
            "freeze_min_search_settled": FREEZE_MIN_SEARCH_SETTLED,
            "exam_n": EXAM_N,
            "futility_looks": list(FUTILITY_LOOKS),
            "declared_at": DECLARED_AT,
            "permutation_seed": PERMUTATION_SEED,
            "id": RULE_ID,
        }
    payload = json.loads(path.read_text(encoding="utf-8"))
    pol = payload.get("policy") or {}
    return {
        "start_theta": float(pol.get("start_theta", START_THETA)),
        "theta_min": float(pol.get("theta_min", THETA_MIN)),
        "theta_max": float(pol.get("theta_max", THETA_MAX)),
        "step": float(pol.get("step", STEP)),
        "freeze_abs_delta": float(pol.get("freeze_abs_delta", FREEZE_ABS_DELTA)),
        "freeze_min_search_settled": int(pol.get("freeze_min_search_settled", FREEZE_MIN_SEARCH_SETTLED)),
        "exam_n": int(pol.get("exam_n", EXAM_N)),
        "futility_looks": [int(x) for x in (pol.get("futility_looks") or FUTILITY_LOOKS)],
        "declared_at": str(pol.get("declared_at") or DECLARED_AT),
        "permutation_seed": int(pol.get("permutation_seed") or PERMUTATION_SEED),
        "id": str(pol.get("id") or RULE_ID),
        "trials_to_date": int(payload.get("trials_to_date") or 0),
    }


def clip_theta(theta: float, *, policy: dict[str, Any] | None = None) -> float:
    pol = policy or load_policy()
    lo = float(pol["theta_min"])
    hi = float(pol["theta_max"])
    return min(hi, max(lo, float(theta)))
