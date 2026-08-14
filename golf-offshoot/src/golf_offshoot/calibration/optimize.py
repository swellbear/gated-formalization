"""Bayesian search + ARD for factor weights. Train only; holdout is frozen."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from golf_offshoot.bayesian_engine.engine import BayesianEngine
from golf_offshoot.bayesian_engine.simulate import SimConfig
from golf_offshoot.bayesian_engine.weights import DEFAULT_ALPHA, DEFAULT_ARD_SCALE, complete_alpha
from golf_offshoot.calibration.dataset import EventDataset
from golf_offshoot.calibration.scoring import HorizonMetrics, aggregate, scalar_loss, score_event

# Factors that receive pre-event evidence. SG keys are added only when as-of
# THROUGH_EVENT / EVENT_ONLY coverage on the panel is real.
FINISH_KEYS = (
    "recent_form",
    "short_term_trend",
    "course_history",
    "course_fit",
    "weather_suitability",
    "field_interaction",
    "comparable_player_borrow",
)
SG_KEYS = (
    "sg_match",
    "approach_sg",
    "around_green",
    "putting",
)
CALIB_KEYS = FINISH_KEYS
MIN_RECENT_SG_COVERAGE = 0.30
MIN_LONG_SG_COVERAGE = 0.40


def keys_for_coverage(coverage: dict[str, float]) -> tuple[str, ...]:
    keys = list(FINISH_KEYS)
    if coverage.get("long_term_sg", 0.0) >= MIN_LONG_SG_COVERAGE:
        keys.extend(SG_KEYS)
    return tuple(keys)


BOUNDS = (0.0, 1.2)


@dataclass
class ArdReport:
    relevance: dict[str, float]
    ard_scale: dict[str, float]
    loo_delta_loss: dict[str, float]
    notes: list[str] = field(default_factory=list)


@dataclass
class CalibrationResult:
    expert_alpha: dict[str, float]
    calibrated_alpha: dict[str, float]
    ard: ArdReport
    train_expert: HorizonMetrics
    train_fitted: HorizonMetrics
    holdout_expert: HorizonMetrics
    holdout_fitted: HorizonMetrics
    bounds_hit: list[str]
    n_evals: int
    recommendation: str
    notes: list[str]


def _clip(v: float) -> float:
    return float(min(BOUNDS[1], max(BOUNDS[0], v)))


def _engine(alpha: dict[str, float], ard: dict[str, float] | None, n_sims: int, seed: int) -> BayesianEngine:
    return BayesianEngine(
        alpha=complete_alpha(alpha),
        ard_scale=ard or {},
        sim=SimConfig(n_sims=n_sims, seed=seed),
    )


def evaluate_alpha(
    alpha: dict[str, float],
    datasets: list[EventDataset],
    *,
    ard: dict[str, float] | None = None,
    n_sims: int = 220,
    seed: int = 11,
) -> HorizonMetrics:
    engine = _engine(alpha, ard, n_sims, seed)
    mets = [score_event(ds, engine, n_sims=n_sims, seed=seed) for ds in datasets]
    return aggregate(mets)


def _sample_around(
    rng: np.random.Generator,
    mu: dict[str, float],
    ell: dict[str, float],
    keys: tuple[str, ...],
) -> dict[str, float]:
    out = dict(DEFAULT_ALPHA)
    out.update(mu)
    for k in keys:
        scale = max(float(ell.get(k, 0.18)), 0.04)
        out[k] = _clip(float(rng.normal(float(mu.get(k, DEFAULT_ALPHA.get(k, 0.1))), scale)))
    return out


def fit_weights(
    train: list[EventDataset],
    holdout: list[EventDataset],
    *,
    n_random: int = 18,
    n_coord: int = 4,
    n_sims: int = 200,
    seed: int = 20260813,
    keys: tuple[str, ...] | None = None,
) -> CalibrationResult:
    keys = keys or CALIB_KEYS
    rng = np.random.default_rng(seed)
    expert = complete_alpha()
    notes = [
        "Search is Bayesian in the sense of sampling from an independent-Gaussian prior "
        "centered on expert α, then updating per-coordinate mean/variance (ARD).",
        "Hold-out events are never used to accept a candidate.",
        f"Fitted keys: {', '.join(keys)}.",
    ]
    if any(k in keys for k in SG_KEYS):
        notes.append("SG category weights are in the search because as-of THROUGH_EVENT coverage is real.")
    else:
        notes.append("SG category weights are not moved: long-term as-of coverage was too thin.")
    train_expert = evaluate_alpha(expert, train, n_sims=n_sims, seed=seed)
    hold_expert = evaluate_alpha(expert, holdout, n_sims=n_sims, seed=seed)

    mu = {k: expert[k] for k in keys}
    ell = {k: 0.22 for k in keys}
    best_alpha = dict(expert)
    best_loss = scalar_loss(train_expert)
    n_evals = 1
    observations: list[tuple[dict[str, float], float]] = [(dict(mu), best_loss)]

    for i in range(n_random):
        cand = _sample_around(rng, mu, ell, keys)
        m = evaluate_alpha(cand, train, n_sims=n_sims, seed=seed + i + 1)
        n_evals += 1
        loss = scalar_loss(m)
        observations.append(({k: cand[k] for k in keys}, loss))
        if loss < best_loss:
            best_loss = loss
            best_alpha = cand
            for k in keys:
                mu[k] = 0.6 * mu[k] + 0.4 * cand[k]
        else:
            for k in keys:
                ell[k] *= 0.97
        print(f"bo {i+1}/{n_random} loss={loss:.4f} best={best_loss:.4f}", flush=True)
        _update_ard_scales(ell, observations, keys)

    for k in keys:
        base = dict(best_alpha)
        for delta in np.linspace(-0.18, 0.18, n_coord):
            trial = dict(base)
            trial[k] = _clip(base[k] + float(delta))
            if abs(trial[k] - base[k]) < 1e-6:
                continue
            m = evaluate_alpha(trial, train, n_sims=n_sims, seed=seed + 100)
            n_evals += 1
            loss = scalar_loss(m)
            observations.append(({kk: trial[kk] for kk in keys}, loss))
            if loss < best_loss:
                best_loss = loss
                best_alpha = trial
                mu[k] = trial[k]

    train_fitted = evaluate_alpha(best_alpha, train, n_sims=n_sims, seed=seed)
    hold_fitted = evaluate_alpha(best_alpha, holdout, n_sims=n_sims, seed=seed)
    n_evals += 2

    ard = _ard_report(best_alpha, train, n_sims=max(120, n_sims // 2), seed=seed, keys=keys)
    bounds_hit = [k for k in keys if abs(best_alpha[k] - BOUNDS[0]) < 1e-6 or abs(best_alpha[k] - BOUNDS[1]) < 1e-6]

    rec = "keep_expert"
    if scalar_loss(hold_fitted) < scalar_loss(hold_expert) - 0.001:
        rec = "use_calibrated"
        notes.append("Hold-out proper score improved vs expert initialization.")
    else:
        notes.append(
            "Hold-out did not clearly beat expert α; default recommendation is to keep expert "
            "weights in production and store the fitted vector for comparison."
        )

    return CalibrationResult(
        expert_alpha=expert,
        calibrated_alpha=complete_alpha(best_alpha),
        ard=ard,
        train_expert=train_expert,
        train_fitted=train_fitted,
        holdout_expert=hold_expert,
        holdout_fitted=hold_fitted,
        bounds_hit=bounds_hit,
        n_evals=n_evals,
        recommendation=rec,
        notes=notes,
    )


def _update_ard_scales(
    ell: dict[str, float],
    observations: list[tuple[dict[str, float], float]],
    keys: tuple[str, ...],
) -> None:
    if len(observations) < 5:
        return
    losses = np.array([o[1] for o in observations], dtype=float)
    losses = losses - losses.mean()
    for k in keys:
        xs = np.array([o[0][k] for o in observations], dtype=float)
        xs = xs - xs.mean()
        denom = float(np.dot(xs, xs))
        if denom < 1e-9:
            ell[k] = max(0.05, ell[k] * 0.9)
            continue
        corr = abs(float(np.dot(xs, losses) / (np.sqrt(denom) * (np.linalg.norm(losses) + 1e-9))))
        ell[k] = float(max(0.04, min(0.35, 0.08 + 0.28 * corr)))


def _ard_report(
    alpha: dict[str, float],
    train: list[EventDataset],
    *,
    n_sims: int,
    seed: int,
    keys: tuple[str, ...] | None = None,
) -> ArdReport:
    keys = keys or CALIB_KEYS
    full = evaluate_alpha(alpha, train, n_sims=n_sims, seed=seed)
    base = scalar_loss(full)
    loo = {}
    rel = {}
    scales = dict(DEFAULT_ARD_SCALE)
    notes = []
    for k in keys:
        trial = dict(alpha)
        trial[k] = 0.0
        m = evaluate_alpha(trial, train, n_sims=n_sims, seed=seed)
        delta = scalar_loss(m) - base
        loo[k] = float(delta)
        rel[k] = float(max(0.0, delta))
        scales[k] = float(max(0.05, min(1.0, rel[k] / (rel[k] + 0.004))))
        if rel[k] < 0.002:
            notes.append(f"{k}: near-zero leave-one-out relevance (ARD shrink)")
    s = sum(rel.values()) or 1.0
    rel = {k: v / s for k, v in rel.items()}
    return ArdReport(relevance=rel, ard_scale=scales, loo_delta_loss=loo, notes=notes)
