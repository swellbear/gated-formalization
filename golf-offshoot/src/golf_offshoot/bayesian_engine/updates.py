"""Evidence-weighted latent-skill updates with correlation discounting.

θ is a latent "better-than-field" skill (higher = better). Weak quality
and low constrainingability shrink the move. Correlated factors are not
allowed to stack at full strength.

Variance: each useful observation reduces posterior variance; missing or
low-quality evidence leaves it wide.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from golf_offshoot.bayesian_engine.weights import complete_alpha
from golf_offshoot.config import MIN_QUALITY_TO_UPDATE, NARRATIVE_ABS_CAP
from golf_offshoot.free_parameters.catalog import CATALOG_BY_ID
from golf_offshoot.models.enums import FactorStatus
from golf_offshoot.models.schemas import FactorContribution, FreeParameterState


@dataclass
class ThetaState:
    mean: float
    variance: float
    contributions: list[FactorContribution] = field(default_factory=list)

    @property
    def sd(self) -> float:
        return float(np.sqrt(max(self.variance, 1e-8)))


def _quality_of(state: FreeParameterState) -> float:
    if state.quality is None or state.quality.missing:
        return 0.0
    return float(state.quality.score)


def _correlation(a: str, b: str) -> float:
    if a == b:
        return 1.0
    da, db = CATALOG_BY_ID.get(a), CATALOG_BY_ID.get(b)
    if not da or not db:
        return 0.0
    if b in da.correlated_with or a in db.correlated_with:
        return 0.45
    return 0.0


def _stacking_discount(factor_id: str, already: list[str]) -> float:
    """If related factors already moved θ, shrink this move."""
    if not already:
        return 1.0
    rhos = [_correlation(factor_id, prev) for prev in already]
    max_rho = max(rhos) if rhos else 0.0
    return float(max(0.25, 1.0 - 0.65 * max_rho))


def update_theta(
    prior_mean: float,
    prior_sd: float,
    board: dict[str, FreeParameterState],
    alpha: dict[str, float] | None = None,
    ard_scale: dict[str, float] | None = None,
) -> ThetaState:
    """Apply all non-parked factors. Talent prior is the starting mean."""
    alpha = complete_alpha(alpha)
    ard = ard_scale or {}
    mean = float(prior_mean)
    var = float(prior_sd**2)
    contribs: list[FactorContribution] = []
    applied: list[str] = []

    # Apply talent as the prior location; still record a contribution of 0 extra
    talent = board.get("talent_prior")
    if talent:
        contribs.append(
            FactorContribution(
                factor_id="talent_prior",
                delta_theta=0.0,
                evidence=talent.standardized_evidence,
                quality=_quality_of(talent),
                importance=talent.importance,
                status=talent.status,
            )
        )

    ordered = sorted(
        (fid for fid in board if fid != "talent_prior"),
        key=lambda fid: board[fid].importance,
        reverse=True,
    )

    for fid in ordered:
        st = board[fid]
        defn = CATALOG_BY_ID.get(fid)
        if st.status == FactorStatus.PARKED:
            continue
        q = _quality_of(st)
        if q < MIN_QUALITY_TO_UPDATE and st.status == FactorStatus.UNCONSTRAINED:
            contribs.append(
                FactorContribution(
                    factor_id=fid,
                    delta_theta=0.0,
                    evidence=st.standardized_evidence,
                    quality=q,
                    importance=st.importance,
                    status=st.status,
                )
            )
            continue

        a = alpha.get(fid, 0.08) * ard.get(fid, 1.0)
        constrain = defn.base_constrainingability if defn else 0.4
        if st.status == FactorStatus.UNCONSTRAINED:
            constrain *= 0.15
        elif st.status == FactorStatus.PARTIALLY_CONSTRAINED:
            constrain *= 0.55

        raw = a * q * constrain * st.standardized_evidence
        raw *= _stacking_discount(fid, applied)
        if defn and defn.narrative_capped:
            raw = float(np.clip(raw, -NARRATIVE_ABS_CAP, NARRATIVE_ABS_CAP))

        mean += raw
        # Strong, high-quality, constrained evidence reduces variance.
        shrink = 1.0 - 0.18 * q * constrain
        var *= float(max(0.35, shrink))
        applied.append(fid)
        contribs.append(
            FactorContribution(
                factor_id=fid,
                delta_theta=float(raw),
                evidence=st.standardized_evidence,
                quality=q,
                importance=st.importance,
                status=st.status,
            )
        )

    return ThetaState(mean=float(mean), variance=float(max(var, 0.04)), contributions=contribs)
