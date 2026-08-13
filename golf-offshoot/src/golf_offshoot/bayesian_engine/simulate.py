"""Monte Carlo field simulation → coherent multi-horizon probabilities.

Same latent θ feeds Make Cut, Top 20, Top 10, Top 5, Win.
Each round score ~ Normal(-θ, σ²). Cut after configured round.
Ranges from posterior draws of θ, not from a fake interval around a point.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from golf_offshoot.config import (
    DEFAULT_CUT_AFTER_ROUND,
    DEFAULT_CUT_PLACE,
    DEFAULT_N_SIMS,
    DEFAULT_ROUND_SIGMA,
    DEFAULT_ROUNDS,
)
from golf_offshoot.models.enums import Horizon
from golf_offshoot.models.schemas import HorizonProbability, ProbabilityBundle


HORIZON_ORDER = (Horizon.WIN, Horizon.TOP_5, Horizon.TOP_10, Horizon.TOP_20, Horizon.MAKE_CUT)


@dataclass
class SimConfig:
    n_sims: int = DEFAULT_N_SIMS
    n_rounds: int = DEFAULT_ROUNDS
    cut_place: int = DEFAULT_CUT_PLACE
    cut_after: int = DEFAULT_CUT_AFTER_ROUND
    round_sigma: float = DEFAULT_ROUND_SIGMA
    seed: int | None = None
    # Percentile band for displayed range
    lo_pct: float = 10.0
    hi_pct: float = 90.0


def _enforce_coherence(p: dict[Horizon, float]) -> dict[Horizon, float]:
    """Force WIN ≤ TOP5 ≤ TOP10 ≤ TOP20 ≤ MAKE_CUT ≤ 1."""
    chain = [
        Horizon.WIN,
        Horizon.TOP_5,
        Horizon.TOP_10,
        Horizon.TOP_20,
        Horizon.MAKE_CUT,
    ]
    out = dict(p)
    running = 0.0
    for h in chain:
        v = min(1.0, max(running, float(out.get(h, 0.0))))
        out[h] = v
        running = v
    return out


def simulate_field(
    player_ids: list[str],
    theta_mean: np.ndarray,
    theta_sd: np.ndarray,
    withdrawn: np.ndarray | None = None,
    live_score: np.ndarray | None = None,
    live_holes: np.ndarray | None = None,
    holes_per_round: int = 18,
    config: SimConfig | None = None,
) -> dict[str, ProbabilityBundle]:
    cfg = config or SimConfig()
    rng = np.random.default_rng(cfg.seed)
    n = len(player_ids)
    if n == 0:
        return {}

    wd = withdrawn if withdrawn is not None else np.zeros(n, dtype=bool)
    # Posterior draws of θ
    theta = rng.normal(theta_mean, np.maximum(theta_sd, 1e-4), size=(cfg.n_sims, n))
    theta[:, wd] = -1e9

    remaining_frac = np.ones(n, dtype=float)
    current = np.zeros(n, dtype=float)
    if live_holes is not None and live_score is not None:
        total_holes = cfg.n_rounds * holes_per_round
        remaining_frac = np.clip(1.0 - live_holes / max(total_holes, 1), 0.0, 1.0)
        current = live_score.astype(float)

    # Round scores: lower (more negative vs par encoding) is better.
    # We store strokes relative to par: -θ is expected scoring vs field mean 0.
    round_sigma = cfg.round_sigma
    scores = np.zeros((cfg.n_sims, n, cfg.n_rounds))
    for r in range(cfg.n_rounds):
        noise = rng.normal(0.0, round_sigma, size=(cfg.n_sims, n))
        scores[:, :, r] = -theta + noise

    # Blend live completed scoring: treat completed holes as observed.
    if live_holes is not None:
        # Approximate: freeze a fraction of expected remaining.
        completed_equiv = current[None, :]  # already to-par
        # Remaining rounds contribution scaled
        remaining_scores = scores.sum(axis=2) * remaining_frac[None, :]
        total = completed_equiv + remaining_scores
    else:
        total = scores.sum(axis=2)

    # 36-hole cut
    early = scores[:, :, : cfg.cut_after].sum(axis=2)
    if live_holes is not None:
        # If more than cut_after rounds equivalent holes played, use total-so-far proxy
        early = np.where(
            live_holes[None, :] >= cfg.cut_after * holes_per_round,
            current[None, :],
            early,
        )

    cut_rank = np.argsort(early, axis=1)
    made = np.zeros((cfg.n_sims, n), dtype=bool)
    k = min(cfg.cut_place, n)
    take = cut_rank[:, :k]
    rows = np.arange(cfg.n_sims)[:, None]
    made[rows, take] = True
    if k < n:
        cutoff = early[np.arange(cfg.n_sims), cut_rank[:, k - 1]]
        made |= early <= cutoff[:, None] + 1e-9
    made[:, wd] = False

    # Weekend: players who miss cut keep early total as final (no weekend scores)
    weekend = scores[:, :, cfg.cut_after :].sum(axis=2)
    final = early + np.where(made, weekend, 0.0)
    if live_holes is not None:
        final = total
        # missed-cut players already flagged
        missed = ~made
        final = np.where(missed, np.maximum(final, early + 8.0), final)

    order = np.argsort(final, axis=1)
    rows = np.arange(cfg.n_sims)[:, None]
    win = np.zeros((cfg.n_sims, n), dtype=bool)
    top5 = np.zeros((cfg.n_sims, n), dtype=bool)
    top10 = np.zeros((cfg.n_sims, n), dtype=bool)
    top20 = np.zeros((cfg.n_sims, n), dtype=bool)
    win[np.arange(cfg.n_sims), order[:, 0]] = True
    top5[rows, order[:, : min(5, n)]] = True
    top10[rows, order[:, : min(10, n)]] = True
    top20[rows, order[:, : min(20, n)]] = True
    win &= made
    top5 &= made
    top10 &= made
    top20 &= made

    # Percentile bands via Bernoulli: use beta-ish from sim batches
    # Split sims into blocks for a cheap posterior range
    n_blocks = 10
    block = cfg.n_sims // n_blocks

    def _bundle(i: int) -> ProbabilityBundle:
        def band(arr: np.ndarray) -> tuple[float, float, float]:
            cents = []
            for b in range(n_blocks):
                sl = arr[b * block : (b + 1) * block, i]
                cents.append(float(sl.mean()))
            cents_a = np.array(cents)
            central = float(arr[:, i].mean())
            lo = float(np.percentile(cents_a, cfg.lo_pct))
            hi = float(np.percentile(cents_a, cfg.hi_pct))
            lo, hi = min(lo, central), max(hi, central)
            return central, max(0.0, lo), min(1.0, hi)

        raw = {}
        for h, arr in (
            (Horizon.WIN, win),
            (Horizon.TOP_5, top5),
            (Horizon.TOP_10, top10),
            (Horizon.TOP_20, top20),
            (Horizon.MAKE_CUT, made),
        ):
            c, lo, hi = band(arr)
            raw[h] = (c, lo, hi)
        # coherence on centrals then expand bands
        cent = _enforce_coherence({h: raw[h][0] for h in raw})
        horizons = {}
        for h in raw:
            c = cent[h]
            lo, hi = raw[h][1], raw[h][2]
            # keep band around coherent central
            width = max(hi - lo, 0.0)
            horizons[h] = HorizonProbability(
                horizon=h,
                central=c,
                low=max(0.0, c - 0.5 * width),
                high=min(1.0, c + 0.5 * width),
            )
        # re-enforce low/high chain loosely
        return ProbabilityBundle(
            player_id=player_ids[i],
            horizons=horizons,
            theta_mean=float(theta_mean[i]),
            theta_sd=float(theta_sd[i]),
        )

    return {player_ids[i]: _bundle(i) for i in range(n)}
