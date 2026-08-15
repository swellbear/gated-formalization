"""Versioned calibration artifacts. Frozen weights are the production candidate."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from golf_offshoot.bayesian_engine.weights import complete_alpha, weight_hash
from golf_offshoot.calibration.optimize import CalibrationResult
from golf_offshoot.calibration.scoring import HorizonMetrics
from golf_offshoot.config import CALIBRATED_WEIGHTS_VERSION, MODEL_VERSION
from golf_offshoot.data_feeds.http import package_data_dir
from golf_offshoot.localtime import isoformat_now


def calibration_dir() -> Path:
    d = package_data_dir() / "calibration"
    d.mkdir(parents=True, exist_ok=True)
    return d


def default_weights_path() -> Path:
    return calibration_dir() / f"weights_{CALIBRATED_WEIGHTS_VERSION}.json"


def _metrics_dict(m: HorizonMetrics) -> dict[str, Any]:
    return {"n": m.n, "brier": m.brier, "logloss": m.logloss}


def result_to_payload(
    result: CalibrationResult,
    *,
    train_ids: list[str],
    holdout_ids: list[str],
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload = {
        "version_id": f"{MODEL_VERSION}-{CALIBRATED_WEIGHTS_VERSION}",
        "created_at": isoformat_now(),
        "no_future_leakage": True,
        "train_event_ids": train_ids,
        "holdout_event_ids": holdout_ids,
        "expert_alpha": result.expert_alpha,
        "calibrated_alpha": result.calibrated_alpha,
        "ard_scale": result.ard.ard_scale,
        "ard_relevance": result.ard.relevance,
        "ard_loo_delta_loss": result.ard.loo_delta_loss,
        "ard_notes": result.ard.notes,
        "bounds": [0.0, 1.2],
        "bounds_hit": result.bounds_hit,
        "n_evals": result.n_evals,
        "recommendation": result.recommendation,
        "notes": result.notes,
        "metrics": {
            "train_expert": _metrics_dict(result.train_expert),
            "train_fitted": _metrics_dict(result.train_fitted),
            "holdout_expert": _metrics_dict(result.holdout_expert),
            "holdout_fitted": _metrics_dict(result.holdout_fitted),
        },
        "weight_hash_expert": weight_hash(result.expert_alpha),
        "weight_hash_calibrated": weight_hash(result.calibrated_alpha, result.ard.ard_scale),
        "extra": extra or {},
    }
    return payload


def save_weights(payload: dict[str, Any], path: Path | None = None) -> Path:
    path = path or default_weights_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def load_weights(path: Path | None = None) -> dict[str, Any] | None:
    path = path or default_weights_path()
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def production_alpha(path: Path | None = None) -> tuple[dict[str, float], dict[str, float], str]:
    """Return (alpha, ard, source_note). Honors freeze recommendation."""
    payload = load_weights(path)
    if not payload:
        return complete_alpha(), {}, "expert-initialized (no calibration artifact)"
    rec = payload.get("recommendation") or "keep_expert"
    ard = payload.get("ard_scale") or {}
    if rec == "use_calibrated":
        return complete_alpha(payload.get("calibrated_alpha")), ard, f"frozen {payload.get('version_id')}"
    return complete_alpha(), {}, (
        f"expert-initialized; calibrated artifact {payload.get('version_id')} stored but not selected"
    )
