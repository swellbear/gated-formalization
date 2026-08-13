"""Uncertainty decomposition and optimistic/pessimistic scenarios.

Leave-one-factor-out on θ, then map Δθ to a rough ΔP(win) via softmax
sensitivity so the range attribution is in probability units.
"""

from __future__ import annotations

import numpy as np

from golf_offshoot.bayesian_engine.updates import ThetaState, update_theta
from golf_offshoot.models.enums import FactorStatus, Horizon
from golf_offshoot.models.schemas import FreeParameterState


def softmax_win_share(theta: np.ndarray, temperature: float = 1.0) -> np.ndarray:
    z = (theta - theta.max()) / max(temperature, 1e-6)
    e = np.exp(z)
    return e / e.sum()


def decompose_win_range(
    player_index: int,
    boards: list[dict[str, FreeParameterState]],
    priors: list[tuple[float, float]],
    alpha: dict[str, float],
    field_theta: np.ndarray,
) -> dict[str, float]:
    """Share of this player's θ-uncertainty attributable to each factor."""
    board = boards[player_index]
    base = update_theta(priors[player_index][0], priors[player_index][1], board, alpha)
    parts: dict[str, float] = {}
    total_abs = 0.0
    for fid, st in board.items():
        if st.status == FactorStatus.PARKED:
            continue
        if abs(st.standardized_evidence) < 1e-9 and (
            st.quality is None or st.quality.score < 0.05
        ):
            # unconstrained width: use leftover variance proxy
            parts[fid] = max(st.importance * base.variance, 0.0)
            total_abs += parts[fid]
            continue
        muted = dict(board)
        muted_st = st.model_copy(deep=True)
        muted_st.standardized_evidence = 0.0
        muted[fid] = muted_st
        alt = update_theta(priors[player_index][0], priors[player_index][1], muted, alpha)
        parts[fid] = abs(base.mean - alt.mean)
        total_abs += parts[fid]
    if total_abs <= 1e-12:
        return {k: 0.0 for k in parts}
    return {k: v / total_abs for k, v in parts.items()}


def scenario_thetas(
    board: dict[str, FreeParameterState],
    prior_mean: float,
    prior_sd: float,
    alpha: dict[str, float],
    major_ids: list[str],
    shift: float = 0.85,
) -> tuple[ThetaState, ThetaState, ThetaState]:
    """Base, optimistic, pessimistic by pushing major unconstrained factors."""
    base = update_theta(prior_mean, prior_sd, board, alpha)

    def shifted(sign: float) -> dict[str, FreeParameterState]:
        out = dict(board)
        for fid in major_ids:
            if fid not in out:
                continue
            st = out[fid].model_copy(deep=True)
            if st.status == FactorStatus.CONSTRAINED:
                continue
            st.standardized_evidence = st.standardized_evidence + sign * shift
            out[fid] = st
        return out

    opt = update_theta(prior_mean, prior_sd, shifted(1.0), alpha)
    pes = update_theta(prior_mean, prior_sd, shifted(-1.0), alpha)
    return base, opt, pes


def attach_decomposition(
    bundles: dict[str, object],
    shares_by_player: dict[str, dict[str, float]],
    opt_p: dict[str, dict[str, float]],
    pes_p: dict[str, dict[str, float]],
) -> None:
    for pid, bundle in bundles.items():
        shares = shares_by_player.get(pid, {})
        for h, hp in bundle.horizons.items():
            hp.decomposition = dict(shares) if h == Horizon.WIN else {}
        bundle.scenario_optimistic = opt_p.get(pid, {})
        bundle.scenario_pessimistic = pes_p.get(pid, {})
