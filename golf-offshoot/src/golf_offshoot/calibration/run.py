"""End-to-end historical calibration. Real ESPN events + as-of SG when present."""

from __future__ import annotations

from golf_offshoot.bayesian_engine.weights import complete_alpha, weight_hash
from golf_offshoot.calibration.artifacts import result_to_payload, save_weights
from golf_offshoot.calibration.dataset import (
    build_event_dataset,
    feature_coverage,
    panel_is_materially_stronger,
    recent_sg_depth_stats,
    split_events,
)
from golf_offshoot.calibration.optimize import (
    MIN_RECENT_SG_COVERAGE,
    fit_weights,
    keys_for_coverage,
)
from golf_offshoot.config import CALIB_HISTORY_YEARS, CALIBRATED_WEIGHTS_VERSION, MODEL_VERSION
from golf_offshoot.data_feeds.ingest import RealIngestor
from golf_offshoot.localtime import isoformat_now


def run_calibration(
    *,
    refresh: bool = False,
    holdout_n: int = 3,
    burn_in: int = 8,
    n_random: int = 8,
    n_coord: int = 3,
    n_sims: int = 150,
    max_train_events: int | None = 12,
    max_hold_events: int | None = None,
) -> dict:
    ingestor = RealIngestor(refresh=refresh, history_years=CALIB_HISTORY_YEARS)
    idx = ingestor.load_history()
    print(f"history completed={len(idx.completed())}", flush=True)
    asof = ingestor.load_asof(2026)
    print(f"as-of SG pills={len(asof.pills)} dated={sum(1 for p in asof.pills if p.start_date)}", flush=True)
    train_ev, hold_ev = split_events(idx, burn_in=burn_in, holdout_n=holdout_n)
    if max_train_events is not None:
        train_ev = train_ev[-max_train_events:]
    if max_hold_events is not None:
        hold_ev = hold_ev[-max_hold_events:]
    train_ds = []
    hold_ds = []
    skipped = []
    for ev in train_ev:
        print(f"calib train attach {ev.name} {ev.start_date}", flush=True)
        ds = build_event_dataset(idx, ev, asof=asof)
        if ds is None:
            skipped.append(ev.event_id)
            continue
        train_ds.append(ds)
    for ev in hold_ev:
        print(f"calib hold attach {ev.name} {ev.start_date}", flush=True)
        ds = build_event_dataset(idx, ev, asof=asof)
        if ds is None:
            skipped.append(ev.event_id)
            continue
        hold_ds.append(ds)
    if not train_ds or not hold_ds:
        raise RuntimeError(f"dataset empty train={len(train_ds)} hold={len(hold_ds)} skipped={skipped}")
    cov = feature_coverage(train_ds + hold_ds)
    depth = recent_sg_depth_stats(train_ds + hold_ds)
    stronger, stronger_why = panel_is_materially_stronger(depth)
    extra = {
        "train_names": [d.event.name for d in train_ds],
        "holdout_names": [d.event.name for d in hold_ds],
        "skipped": skipped,
        "history_completed": len(idx.completed()),
        "max_train_events": max_train_events,
        "asof_coverage": cov,
        "recent_sg_depth": depth,
        "panel_materially_stronger": stronger,
        "panel_strength_notes": stronger_why,
        "search_ran": False,
        "window_requested": int(depth.get("window_requested") or 0),
    }
    skip_reason = ""
    if cov.get("recent_sg", 0.0) < MIN_RECENT_SG_COVERAGE:
        skip_reason = (
            "As-of recent SG coverage on the leakage-safe panel is below the "
            f"{MIN_RECENT_SG_COVERAGE:.0%} bar, so Bayesian search was not run. "
            "A finish-only refit is forbidden. Production stays expert-initialized."
        )
    elif not stronger:
        skip_reason = stronger_why
    if skip_reason:
        expert = complete_alpha()
        payload = {
            "version_id": f"{MODEL_VERSION}-{CALIBRATED_WEIGHTS_VERSION}",
            "created_at": isoformat_now(),
            "no_future_leakage": True,
            "train_event_ids": [d.event.event_id for d in train_ds],
            "holdout_event_ids": [d.event.event_id for d in hold_ds],
            "expert_alpha": expert,
            "calibrated_alpha": expert,
            "recommendation": "keep_expert",
            "search_ran": False,
            "n_evals": 0,
            "notes": [
                skip_reason,
                f"coverage={cov}",
                f"depth={depth}",
            ],
            "extra": extra,
            "weight_hash_expert": weight_hash(expert),
        }
        path = save_weights(payload)
        payload["artifact_path"] = str(path)
        print(f"calibration skipped: {skip_reason}", flush=True)
        return payload

    keys = keys_for_coverage(cov)
    extra["search_ran"] = True
    extra["fitted_keys"] = list(keys)
    result = fit_weights(train_ds, hold_ds, n_random=n_random, n_coord=n_coord, n_sims=n_sims, keys=keys)
    payload = result_to_payload(
        result,
        train_ids=[d.event.event_id for d in train_ds],
        holdout_ids=[d.event.event_id for d in hold_ds],
        extra=extra,
    )
    payload["search_ran"] = True
    path = save_weights(payload)
    payload["artifact_path"] = str(path)
    return payload
