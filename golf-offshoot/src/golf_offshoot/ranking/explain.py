"""Explainability: one-call report of why the number is what it is."""

from __future__ import annotations

from golf_offshoot.bayesian_engine.updates import ThetaState
from golf_offshoot.free_parameters.board import unconstrained_ids
from golf_offshoot.free_parameters.catalog import CATALOG_BY_ID
from golf_offshoot.models.schemas import ExplainabilityReport, PlayerInputs


def explain_player(
    player: PlayerInputs,
    theta: ThetaState,
    borrowed: list[str] | None = None,
    field_note: str = "",
) -> ExplainabilityReport:
    open_q = []
    for fid in unconstrained_ids(player.factors):
        st = player.factors[fid]
        name = CATALOG_BY_ID[fid].name if fid in CATALOG_BY_ID else fid
        open_q.append(st.open_question or f"{name} still open")
    contrib_sorted = sorted(theta.contributions, key=lambda c: abs(c.delta_theta), reverse=True)
    top = contrib_sorted[:8]
    bits = []
    for c in top:
        if abs(c.delta_theta) < 0.02 and c.factor_id != "talent_prior":
            continue
        name = CATALOG_BY_ID[c.factor_id].name if c.factor_id in CATALOG_BY_ID else c.factor_id
        bits.append(f"{name} {c.delta_theta:+.3f}θ (q={c.quality:.2f})")
    if not bits:
        bits.append("mostly the long-term prior; little extra evidence moved the needle")
    narrative = (
        f"{player.player.name}: prior θ={player.talent_prior:.2f} → "
        f"posterior {theta.mean:.2f} ± {theta.sd:.2f}. " + "; ".join(bits) + "."
    )
    return ExplainabilityReport(
        player_id=player.player.player_id,
        player_name=player.player.name,
        theta_mean=theta.mean,
        theta_sd=theta.sd,
        prior_theta=player.talent_prior,
        contributions=theta.contributions,
        open_questions=open_q[:8],
        borrowed_strength=borrowed or [],
        field_interaction_note=field_note,
        narrative=narrative,
    )
