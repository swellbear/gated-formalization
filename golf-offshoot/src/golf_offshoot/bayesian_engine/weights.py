"""Calibratable factor weights. Keys match free-parameter factor_id.

These are starting values for later Bayesian optimization + ARD. ARD would
drive unused factor weights toward zero; the structure is a vector `alpha`
plus per-factor length-scales `ell` stored here as `ard_scale` (1.0 = active).
"""

from __future__ import annotations

import hashlib
import json

from golf_offshoot.free_parameters.catalog import CATALOG_BY_ID

# Mean-shift scale: Δθ ≈ alpha[f] * quality * evidence
DEFAULT_ALPHA: dict[str, float] = {
    "talent_prior": 0.55,
    "course_fit": 0.28,
    "recent_form": 0.22,
    "short_term_trend": 0.10,
    "sg_match": 0.32,
    "weather_suitability": 0.16,
    "health_setup": 0.40,
    "narrative_momentum": 0.08,
    "course_history": 0.18,
    "driving_distance": 0.12,
    "driving_accuracy": 0.14,
    "approach_sg": 0.26,
    "around_green": 0.12,
    "putting": 0.14,
    "scrambling": 0.10,
    "bogey_avoidance": 0.12,
    "par5_scoring": 0.08,
    "wind_history": 0.12,
    "rest_travel": 0.08,
    "comparable_player_borrow": 0.10,
    "venue_cluster_borrow": 0.10,
    "field_interaction": 0.14,
    "live_position": 0.85,
    "live_tee_pairing": 0.06,
}

DEFAULT_ARD_SCALE: dict[str, float] = {k: 1.0 for k in DEFAULT_ALPHA}


def complete_alpha(overrides: dict[str, float] | None = None) -> dict[str, float]:
    alpha = dict(DEFAULT_ALPHA)
    if overrides:
        alpha.update(overrides)
    for fid in CATALOG_BY_ID:
        alpha.setdefault(fid, 0.08)
    return alpha


def weight_hash(alpha: dict[str, float], ard: dict[str, float] | None = None) -> str:
    payload = {"alpha": {k: round(v, 6) for k, v in sorted(alpha.items())}}
    if ard:
        payload["ard"] = {k: round(v, 6) for k, v in sorted(ard.items())}
    raw = json.dumps(payload, sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16]
