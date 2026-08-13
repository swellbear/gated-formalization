"""Per-player reliability — separate from the probability range.

Density, quality, stability of inputs. A tight range with low reliability
is a bias flag, not a reason to bet harder.
"""

from __future__ import annotations

from golf_offshoot.config import (
    RELIABILITY_DENSITY_WEIGHT,
    RELIABILITY_QUALITY_WEIGHT,
    RELIABILITY_STABILITY_WEIGHT,
    THIN_SAMPLE_N,
)
from golf_offshoot.models.enums import FactorStatus
from golf_offshoot.models.schemas import PlayerInputs, ReliabilityScore


def reliability_for(player: PlayerInputs, prev_theta: float | None = None, theta: float | None = None) -> ReliabilityScore:
    qualities = []
    n_obs = []
    unconstrained = 0
    constrained = 0
    for st in player.factors.values():
        if st.status == FactorStatus.PARKED:
            continue
        if st.quality and not st.quality.missing:
            qualities.append(st.quality.score)
            n_obs.append(st.n_obs)
        if st.status == FactorStatus.UNCONSTRAINED:
            unconstrained += 1
        if st.status == FactorStatus.CONSTRAINED:
            constrained += 1
    q = sum(qualities) / len(qualities) if qualities else 0.25
    dens_raw = 0.0
    if n_obs:
        dens_raw = min(1.0, (sum(n_obs) / max(len(n_obs), 1)) / 20.0)
    if player.course_history_rounds >= THIN_SAMPLE_N:
        dens_raw = min(1.0, dens_raw + 0.15)
    if player.player.is_lesser_known:
        dens_raw *= 0.65
        q *= 0.85
    # stability: few unconstrained + small theta jump vs last run
    frac_open = unconstrained / max(unconstrained + constrained, 1)
    stab = 1.0 - 0.55 * frac_open
    if prev_theta is not None and theta is not None:
        jump = abs(theta - prev_theta)
        stab *= max(0.3, 1.0 - jump / 2.0)
    score = (
        RELIABILITY_QUALITY_WEIGHT * q
        + RELIABILITY_DENSITY_WEIGHT * dens_raw
        + RELIABILITY_STABILITY_WEIGHT * stab
    )
    reasons = []
    if player.player.is_lesser_known:
        reasons.append("lesser-known player: thinner public record")
    if player.course_history_rounds < THIN_SAMPLE_N:
        reasons.append(f"only {player.course_history_rounds} rounds at this venue")
    if frac_open > 0.45:
        reasons.append("many free parameters still open")
    if q < 0.4:
        reasons.append("average input quality is low")
    return ReliabilityScore(
        player_id=player.player.player_id,
        score=float(min(1.0, max(0.0, score))),
        data_density=float(dens_raw),
        data_quality=float(q),
        input_stability=float(max(0.0, min(1.0, stab))),
        reasons=reasons,
    )
