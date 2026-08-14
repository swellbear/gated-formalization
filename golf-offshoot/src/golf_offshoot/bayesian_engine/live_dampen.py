"""Round-1 / incomplete-round live dampening.

Live score already enters the MC as an observed to-par. The θ nudge
(`live_position`) must not treat 6 holes like a finished tournament.
"""

from __future__ import annotations

from golf_offshoot.config import DEFAULT_ROUNDS

HOLES_PER_ROUND = 18


def live_progress(
    holes_completed: int,
    n_rounds: int = DEFAULT_ROUNDS,
    holes_per_round: int = HOLES_PER_ROUND,
) -> dict[str, float]:
    total = max(int(n_rounds) * int(holes_per_round), 1)
    h = max(0, min(int(holes_completed), total))
    tournament_frac = h / total
    round1_frac = min(1.0, h / float(holes_per_round))
    # Until 18 holes are in, scale by both tournament share and round-1 share.
    # 6 holes: (6/72) * (6/18) = 0.028. End of R1: 18/72 = 0.25.
    if h < holes_per_round:
        dampen = tournament_frac * round1_frac
    else:
        dampen = tournament_frac
    quality = 0.30 + 0.65 * tournament_frac
    return {
        "holes": float(h),
        "total_holes": float(total),
        "tournament_frac": float(tournament_frac),
        "round1_frac": float(round1_frac),
        "dampen": float(dampen),
        "quality": float(min(0.95, quality)),
    }


def live_position_evidence(
    score_to_par: float,
    holes_completed: int,
    n_rounds: int = DEFAULT_ROUNDS,
) -> tuple[float, dict[str, float]]:
    prog = live_progress(holes_completed, n_rounds=n_rounds)
    raw = -float(score_to_par) / 3.0
    return float(raw * prog["dampen"]), prog


def remaining_totals(
    theta,
    current,
    live_holes,
    n_rounds: int,
    round_sigma: float,
    rng,
    holes_per_round: int = HOLES_PER_ROUND,
):
    """Bank observed to-par; simulate only unplayed holes.

    total = current + (-θ × remaining_rounds) + N(0, σ √remaining_rounds)

    Completed holes are not resimulated. Remaining noise scales with √holes
    left, not with a fraction of a full four-round draw (which understated
    residual variance and double-counted simulated completed-round luck).
    """
    import numpy as np

    total_holes = max(int(n_rounds) * int(holes_per_round), 1)
    rem_holes = np.clip(total_holes - np.asarray(live_holes, dtype=float), 0.0, float(total_holes))
    rem_rounds = rem_holes / float(holes_per_round)
    noise = rng.normal(0.0, 1.0, size=theta.shape)
    scale = round_sigma * np.sqrt(np.maximum(rem_rounds, 0.0))
    remaining = (-theta * rem_rounds[None, :]) + noise * scale[None, :]
    return np.asarray(current, dtype=float)[None, :] + remaining
