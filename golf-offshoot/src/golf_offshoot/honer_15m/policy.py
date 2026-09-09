"""Dated honer policy. Load from HONER_15M_RULES.json when present."""

from __future__ import annotations

import json
from typing import Any

from golf_offshoot.honer_15m.paths import registry_path

START_THETA = 0.75
THETA_MIN = 0.55
THETA_MAX = 0.90
STEP = 0.02
STEP_RULE = "local_regret_v2"
STEP_BAND = 0.10
STEP_RULE_DECLARED_AT = "2026-09-09T15:08:00-04:00"
FREEZE_RULE = "in_band_v1"
FREEZE_RULE_DECLARED_AT = "2026-09-09T15:44:00-04:00"
FREEZE_ABS_DELTA = 0.05
FREEZE_ABS_DELTA_SPREAD = 0.02
FREEZE_MIN_SEARCH_SETTLED = 20
FREEZE_STABLE_WINDOWS = 5
CLIP_EXHAUST_WINDOWS = 20
SPREAD_BAND = 0.03
SPREAD_QUOTE_MIN_FRAC = 0.75
START_DELTA = 0.04
DELTA_MIN = 0.02
DELTA_MAX = 0.12
DELTA_STEP = 0.01
EXAM_N = 70
FUTILITY_LOOKS = (20, 40)
SEED_BANKROLL = 100.0
STAKE = 1.0
PERMUTATION_SEED = 20260909
DECLARED_AT = "2026-09-09T13:40:00-04:00"
RULE_ID = "H-SKIP-RICH-YES"
FAMILY_RICH = "H-SKIP-RICH-YES"
FAMILY_SPREAD = "H-SKIP-WIDE-SPREAD"


def load_policy() -> dict[str, Any]:
    defaults = {
        "start_theta": START_THETA,
        "theta_min": THETA_MIN,
        "theta_max": THETA_MAX,
        "step": STEP,
        "step_rule": STEP_RULE,
        "step_band": STEP_BAND,
        "step_rule_declared_at": STEP_RULE_DECLARED_AT,
        "freeze_rule": FREEZE_RULE,
        "freeze_rule_declared_at": FREEZE_RULE_DECLARED_AT,
        "freeze_abs_delta": FREEZE_ABS_DELTA,
        "freeze_abs_delta_spread": FREEZE_ABS_DELTA_SPREAD,
        "freeze_min_search_settled": FREEZE_MIN_SEARCH_SETTLED,
        "freeze_stable_windows": FREEZE_STABLE_WINDOWS,
        "clip_exhaust_windows": CLIP_EXHAUST_WINDOWS,
        "spread_band": SPREAD_BAND,
        "spread_quote_min_frac": SPREAD_QUOTE_MIN_FRAC,
        "start_delta": START_DELTA,
        "delta_min": DELTA_MIN,
        "delta_max": DELTA_MAX,
        "delta_step": DELTA_STEP,
        "exam_n": EXAM_N,
        "futility_looks": list(FUTILITY_LOOKS),
        "declared_at": DECLARED_AT,
        "permutation_seed": PERMUTATION_SEED,
        "id": RULE_ID,
    }
    path = registry_path()
    if not path.is_file():
        return defaults
    payload = json.loads(path.read_text(encoding="utf-8"))
    pol = payload.get("policy") or {}
    out = dict(defaults)
    out["start_theta"] = float(pol.get("start_theta", START_THETA))
    out["theta_min"] = float(pol.get("theta_min", THETA_MIN))
    out["theta_max"] = float(pol.get("theta_max", THETA_MAX))
    out["step"] = float(pol.get("step", STEP))
    out["step_rule"] = str(pol.get("step_rule") or STEP_RULE)
    out["step_band"] = float(pol.get("step_band", STEP_BAND))
    out["step_rule_declared_at"] = str(pol.get("step_rule_declared_at") or STEP_RULE_DECLARED_AT)
    out["freeze_rule"] = str(pol.get("freeze_rule") or FREEZE_RULE)
    out["freeze_rule_declared_at"] = str(pol.get("freeze_rule_declared_at") or FREEZE_RULE_DECLARED_AT)
    out["freeze_abs_delta"] = float(pol.get("freeze_abs_delta", FREEZE_ABS_DELTA))
    out["freeze_abs_delta_spread"] = float(pol.get("freeze_abs_delta_spread", FREEZE_ABS_DELTA_SPREAD))
    out["freeze_min_search_settled"] = int(pol.get("freeze_min_search_settled", FREEZE_MIN_SEARCH_SETTLED))
    out["freeze_stable_windows"] = int(pol.get("freeze_stable_windows", FREEZE_STABLE_WINDOWS))
    out["clip_exhaust_windows"] = int(pol.get("clip_exhaust_windows", CLIP_EXHAUST_WINDOWS))
    out["spread_band"] = float(pol.get("spread_band", SPREAD_BAND))
    out["spread_quote_min_frac"] = float(pol.get("spread_quote_min_frac", SPREAD_QUOTE_MIN_FRAC))
    out["start_delta"] = float(pol.get("start_delta", START_DELTA))
    out["delta_min"] = float(pol.get("delta_min", DELTA_MIN))
    out["delta_max"] = float(pol.get("delta_max", DELTA_MAX))
    out["delta_step"] = float(pol.get("delta_step", DELTA_STEP))
    out["exam_n"] = int(pol.get("exam_n", EXAM_N))
    out["futility_looks"] = [int(x) for x in (pol.get("futility_looks") or FUTILITY_LOOKS)]
    out["declared_at"] = str(pol.get("declared_at") or DECLARED_AT)
    out["permutation_seed"] = int(pol.get("permutation_seed") or PERMUTATION_SEED)
    out["id"] = str(pol.get("id") or RULE_ID)
    out["trials_to_date"] = int(payload.get("trials_to_date") or 0)
    return out


def clip_theta(theta: float, *, policy: dict[str, Any] | None = None) -> float:
    pol = policy or load_policy()
    lo = float(pol["theta_min"])
    hi = float(pol["theta_max"])
    return min(hi, max(lo, float(theta)))


def clip_delta(delta: float, *, policy: dict[str, Any] | None = None) -> float:
    pol = policy or load_policy()
    lo = float(pol["delta_min"])
    hi = float(pol["delta_max"])
    return min(hi, max(lo, float(delta)))


def knob_vector(*, family: str, theta: float, delta: float) -> dict[str, Any]:
    return {
        "family": str(family),
        "theta": round(float(theta), 4),
        "delta": round(float(delta), 4),
    }


def vectors_equal(left: dict[str, Any], right: dict[str, Any]) -> bool:
    return knob_vector(
        family=str(left.get("family") or ""),
        theta=float(left.get("theta") or 0.0),
        delta=float(left.get("delta") or 0.0),
    ) == knob_vector(
        family=str(right.get("family") or ""),
        theta=float(right.get("theta") or 0.0),
        delta=float(right.get("delta") or 0.0),
    )
