"""Decision layer — separate from probability. Never auto-bets.

Considers edge, range width, reliability, and correlation with other
candidate bets. Residual judgment stays with the user.
"""

from __future__ import annotations

import numpy as np

from golf_offshoot.config import (
    KELLY_FRACTION_CAP,
    MAX_PORTFOLIO_CORR_TO_STACK,
    MAX_RANGE_WIDTH_TO_CONSIDER,
    MIN_EDGE_TO_CONSIDER,
    MIN_RELIABILITY_TO_CONSIDER,
)
from golf_offshoot.models.enums import BetType, DecisionAction, Horizon
from golf_offshoot.models.schemas import DecisionAdvice, PlayerOutput

_H = {
    BetType.WIN: Horizon.WIN,
    BetType.TOP_5: Horizon.TOP_5,
    BetType.TOP_10: Horizon.TOP_10,
    BetType.TOP_20: Horizon.TOP_20,
    BetType.MAKE_CUT: Horizon.MAKE_CUT,
}


def fractional_kelly(p: float, decimal_odds: float, fraction: float = 0.25) -> float:
    if decimal_odds <= 1.0 or p <= 0:
        return 0.0
    b = decimal_odds - 1.0
    q = 1.0 - p
    full = (b * p - q) / b
    return float(max(0.0, min(KELLY_FRACTION_CAP, fraction * full)))


def _range_width(row: PlayerOutput, bet: BetType) -> float:
    hp = row.probabilities.p(_H[bet])
    return float(hp.high - hp.low)


def advise_bet(
    row: PlayerOutput,
    bet: BetType,
    decimal_odds: float | None = None,
    portfolio_corr_max: float | None = None,
) -> DecisionAdvice:
    hp = row.probabilities.p(_H[bet])
    edge = row.edge_by_bet.get(bet.value)
    market_p = row.market_implied_by_bet.get(bet.value)
    width = _range_width(row, bet)
    rel = row.reliability.score
    reasons: list[str] = []
    action = DecisionAction.PASS

    if "thin_sample_overconfidence" in row.flags:
        reasons.append("thin-sample overconfidence flag — pass unless you override")
    if "narrative_overweight" in row.flags:
        reasons.append("narrative overweight flag")
    if edge is None:
        reasons.append("no market quote to compute edge")
    elif edge < MIN_EDGE_TO_CONSIDER:
        reasons.append(f"edge {edge:+.3f} below consider threshold {MIN_EDGE_TO_CONSIDER}")
    posted_p = None
    posted_edge = None
    if decimal_odds is not None and decimal_odds > 1.0:
        posted_p = 1.0 / decimal_odds
        posted_edge = hp.central - posted_p
        if posted_edge < MIN_EDGE_TO_CONSIDER:
            reasons.append(
                f"posted-price edge {posted_edge:+.3f} (model {hp.central:.3f} vs 1/odds {posted_p:.3f}) "
                f"below {MIN_EDGE_TO_CONSIDER} — de-juiced edge is not a ticket"
            )
    if width > MAX_RANGE_WIDTH_TO_CONSIDER:
        reasons.append(f"win/horizon range width {width:.3f} is wide")
    if rel < MIN_RELIABILITY_TO_CONSIDER:
        reasons.append(f"reliability {rel:.2f} below {MIN_RELIABILITY_TO_CONSIDER}")
    if portfolio_corr_max is not None and portfolio_corr_max > MAX_PORTFOLIO_CORR_TO_STACK:
        reasons.append("too correlated with existing book")

    ok_edge = edge is not None and edge >= MIN_EDGE_TO_CONSIDER
    ok_posted = posted_edge is None or posted_edge >= MIN_EDGE_TO_CONSIDER
    ok_width = width <= MAX_RANGE_WIDTH_TO_CONSIDER
    ok_rel = rel >= MIN_RELIABILITY_TO_CONSIDER
    ok_corr = portfolio_corr_max is None or portfolio_corr_max <= MAX_PORTFOLIO_CORR_TO_STACK
    ok_flags = "thin_sample_overconfidence" not in row.flags

    if ok_edge and ok_posted and ok_width and ok_rel and ok_corr and ok_flags:
        action = DecisionAction.STRONG_CONSIDER if edge and edge >= 2 * MIN_EDGE_TO_CONSIDER else DecisionAction.CONSIDER
        reasons.append("passes decision screens — still requires user confirmation")
    elif ok_edge and ok_posted and (ok_width or ok_rel):
        reasons.append("mixed screens; default pass unless you take residual judgment")

    kelly = 0.0
    if action != DecisionAction.PASS and decimal_odds:
        kelly = fractional_kelly(hp.central, decimal_odds)

    return DecisionAdvice(
        player_id=row.player_id,
        bet_type=bet,
        action=action,
        model_p=hp.central,
        market_p=market_p,
        edge=edge,
        range_width=width,
        reliability=rel,
        suggested_kelly_fraction=kelly,
        portfolio_correlation_max=portfolio_corr_max,
        reasons=reasons,
        never_auto_bet=True,
        requires_user_confirmation=True,
    )


def advise_field(
    rows: list[PlayerOutput],
    bet: BetType = BetType.WIN,
    odds_by_player: dict[str, float] | None = None,
    existing_theta: dict[str, float] | None = None,
) -> list[DecisionAdvice]:
    """Portfolio-aware: approximate correlation via latent θ proximity."""
    odds_by_player = odds_by_player or {}
    thetas = {r.player_id: r.probabilities.theta_mean for r in rows}
    existing = existing_theta or {}
    out: list[DecisionAdvice] = []
    for r in rows:
        corr = None
        if existing:
            diffs = [abs(thetas[r.player_id] - t) for t in existing.values()]
            # closer θ → more correlated outcomes in a one-winner market
            proximity = np.exp(-min(diffs) if diffs else 9.0)
            corr = float(proximity)
        out.append(advise_bet(r, bet, odds_by_player.get(r.player_id), corr))
    return out
