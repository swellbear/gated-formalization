"""Post-tournament learning loop.

Compare model probabilities vs results. Track calibration, factor residuals,
and whether human overrides helped. Weight re-optimization is structured
(gradient on Brier / log-loss) but the first fitted pass is simplified.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from golf_offshoot.bayesian_engine.weights import DEFAULT_ALPHA, complete_alpha
from golf_offshoot.models.enums import Horizon
from golf_offshoot.models.schemas import AuditRecord, HumanOverride


@dataclass
class PlayerResult:
    player_id: str
    won: bool = False
    top_5: bool = False
    top_10: bool = False
    top_20: bool = False
    made_cut: bool = False
    finish: int | None = None


@dataclass
class CalibrationReport:
    n: int
    brier_win: float
    logloss_win: float
    reliability_bins: list[tuple[float, float, int]]
    override_delta_brier: float | None
    notes: list[str] = field(default_factory=list)


def _clip_p(p: float) -> float:
    return float(min(1 - 1e-6, max(1e-6, p)))


def brier(p: float, y: bool) -> float:
    return (p - float(y)) ** 2


def logloss(p: float, y: bool) -> float:
    p = _clip_p(p)
    return float(-(float(y) * np.log(p) + (1 - float(y)) * np.log(1 - p)))


def evaluate_run(audit: AuditRecord, results: list[PlayerResult]) -> CalibrationReport:
    by_id = {r.player_id: r for r in results}
    briers = []
    logs = []
    pairs: list[tuple[float, int]] = []
    notes = []
    for row in audit.outputs:
        res = by_id.get(row.player_id)
        if not res:
            continue
        p = row.probabilities.p(Horizon.WIN).central
        y = res.won
        briers.append(brier(p, y))
        logs.append(logloss(p, y))
        pairs.append((p, int(y)))
    if not pairs:
        return CalibrationReport(0, 1.0, 10.0, [], None, ["no matched results"])

    # reliability bins
    bins = []
    edges = np.linspace(0, 1, 6)
    arr = np.array(pairs)
    for i in range(len(edges) - 1):
        m = (arr[:, 0] >= edges[i]) & (arr[:, 0] < edges[i + 1])
        if i == len(edges) - 2:
            m = (arr[:, 0] >= edges[i]) & (arr[:, 0] <= edges[i + 1])
        if not np.any(m):
            continue
        bins.append((float(arr[m, 0].mean()), float(arr[m, 1].mean()), int(m.sum())))

    override_delta = None
    if audit.overrides:
        override_delta = _override_help(audit, by_id)
        notes.append("human overrides scored vs no-override counterfactual (θ shift undone approximately)")
    return CalibrationReport(
        n=len(pairs),
        brier_win=float(np.mean(briers)),
        logloss_win=float(np.mean(logs)),
        reliability_bins=bins,
        override_delta_brier=override_delta,
        notes=notes,
    )


def _override_help(audit: AuditRecord, results: dict[str, PlayerResult]) -> float:
    """Negative = overrides improved Brier (helped)."""
    by_out = {o.player_id: o for o in audit.outputs}
    deltas = []
    for ov in audit.overrides:
        row = by_out.get(ov.player_id)
        res = results.get(ov.player_id)
        if not row or not res:
            continue
        p = row.probabilities.p(Horizon.WIN).central
        # crude counterfactual: reverse a win-prob nudge proportional to Δθ
        p0 = _clip_p(p - 0.15 * ov.delta_theta)
        deltas.append(brier(p, res.won) - brier(p0, res.won))
    return float(np.mean(deltas)) if deltas else 0.0


def suggest_alpha_update(
    audits_and_results: list[tuple[AuditRecord, list[PlayerResult]]],
    step: float = 0.02,
) -> dict[str, float]:
    """Simplified gradient step on factor contributions vs win residuals.

    Full Bayesian optimization + ARD belongs here later; this is the hook.
    """
    alpha = complete_alpha()
    accum = {k: 0.0 for k in alpha}
    n = 0
    for audit, results in audits_and_results:
        res_map = {r.player_id: r for r in results}
        for row in audit.outputs:
            y = res_map.get(row.player_id)
            if not y or not row.explain:
                continue
            p = row.probabilities.p(Horizon.WIN).central
            residual = float(y.won) - p
            for c in row.explain.contributions:
                accum[c.factor_id] = accum.get(c.factor_id, 0.0) + residual * c.delta_theta
            n += 1
    if n == 0:
        return alpha
    updated = dict(alpha)
    for k, g in accum.items():
        if k not in updated:
            continue
        updated[k] = float(max(0.0, min(1.2, updated[k] + step * g / n)))
    return updated


def ard_scales_from_alpha(alpha: dict[str, float], floor: float = 0.05) -> dict[str, float]:
    """ARD-like: shrink tiny weights toward zero scale."""
    return {k: (1.0 if v >= floor else 0.15) for k, v in alpha.items()}
