"""Monte Carlo field simulation → coherent multi-horizon probabilities.

Same latent θ feeds Make Cut, Top 20, Top 10, Top 5, Win.
Each round score ~ Normal(-θ, σ²). Cut after configured round.
Ranges from posterior draws of θ, not from a fake interval around a point.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from golf_offshoot.bayesian_engine.live_dampen import remaining_totals
from golf_offshoot.config import (
    DEFAULT_CUT_AFTER_ROUND,
    DEFAULT_CUT_PLACE,
    DEFAULT_N_SIMS,
    DEFAULT_ROUND_SIGMA,
    DEFAULT_ROUNDS,
)
from golf_offshoot.models.enums import Horizon, ROUND_LEADER_HORIZONS
from golf_offshoot.models.schemas import HorizonProbability, ProbabilityBundle


HORIZON_ORDER = (Horizon.WIN, Horizon.TOP_5, Horizon.TOP_10, Horizon.TOP_20, Horizon.MAKE_CUT)
LEAD_ROUNDS = (
    (Horizon.WIN_AFTER_R1, 1),
    (Horizon.WIN_AFTER_R2, 2),
    (Horizon.WIN_AFTER_R3, 3),
)


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
    """Force WIN ≤ TOP5 ≤ TOP10 ≤ TOP20 ≤ MAKE_CUT ≤ 1.

    Round-leader horizons stay off this chain. They are not 72-hole finishes.
    """
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


def _lead_after_n(
    scores,
    n_r: int,
    *,
    theta,
    live_score,
    live_holes,
    holes_per_round: int,
    round_sigma: float,
    rng,
    wd,
):
    """P(tied or sole lead after n_r rounds). Ties count as in the lead."""
    n_r = max(1, min(int(n_r), int(scores.shape[2])))
    after = scores[:, :, :n_r].sum(axis=2)
    if live_score is not None and live_holes is not None:
        holes_needed = float(n_r * holes_per_round)
        holes = np.asarray(live_holes, dtype=float)
        still = holes < holes_needed
        if np.any(still):
            capped = np.minimum(holes, holes_needed)
            live_after = remaining_totals(
                theta,
                np.asarray(live_score, dtype=float),
                capped,
                n_r,
                round_sigma,
                rng,
                holes_per_round=holes_per_round,
            )
            after = np.where(still[None, :], live_after, after)
    after = np.array(after, copy=True)
    after[:, wd] = 1e9
    best = np.min(after, axis=1, keepdims=True)
    return after <= best + 1e-9


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

    current = np.zeros(n, dtype=float)
    has_live_board = live_holes is not None and live_score is not None
    if has_live_board:
        current = live_score.astype(float)

    # Round scores: lower (more negative vs par encoding) is better.
    # We store strokes relative to par: -θ is expected scoring vs field mean 0.
    round_sigma = cfg.round_sigma
    scores = np.zeros((cfg.n_sims, n, cfg.n_rounds))
    for r in range(cfg.n_rounds):
        noise = rng.normal(0.0, round_sigma, size=(cfg.n_sims, n))
        scores[:, :, r] = -theta + noise

    # Live: bank observed to-par; simulate only unplayed holes (√holes noise).
    if has_live_board:
        total = remaining_totals(
            theta,
            current,
            live_holes,
            cfg.n_rounds,
            round_sigma,
            rng,
            holes_per_round=holes_per_round,
        )
    else:
        total = scores.sum(axis=2)

    # 36-hole cut (skipped when cut_after<=0 or cut_place covers the field)
    no_cut = cfg.cut_after <= 0 or cfg.cut_place >= n
    if no_cut:
        early = scores.sum(axis=2) * 0.0
        made = np.ones((cfg.n_sims, n), dtype=bool)
        made[:, wd] = False
    else:
        early = scores[:, :, : cfg.cut_after].sum(axis=2)
        if live_holes is not None:
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
    if no_cut:
        final = scores.sum(axis=2)
    else:
        weekend = scores[:, :, cfg.cut_after :].sum(axis=2)
        final = early + np.where(made, weekend, 0.0)
    if live_holes is not None:
        final = total
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

    lead = {}
    for h, n_r in LEAD_ROUNDS:
        if n_r <= cfg.n_rounds:
            lead[h] = _lead_after_n(
                scores,
                n_r,
                theta=theta,
                live_score=live_score if has_live_board else None,
                live_holes=live_holes if has_live_board else None,
                holes_per_round=holes_per_round,
                round_sigma=round_sigma,
                rng=rng,
                wd=wd,
            )

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
            *[(h, lead[h]) for h in ROUND_LEADER_HORIZONS if h in lead],
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
