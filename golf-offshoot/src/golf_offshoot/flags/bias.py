"""Bias and quality flags."""

from __future__ import annotations

from golf_offshoot.bayesian_engine.updates import ThetaState
from golf_offshoot.config import NARRATIVE_ABS_CAP, THIN_SAMPLE_N
from golf_offshoot.models.schemas import MarketSnapshot, PlayerInputs, ProbabilityBundle
from golf_offshoot.models.enums import Horizon

# Ticket vetoes. Missing venue history in the loaded years is not in this set.
PLAYER_HARD_PASS_FLAGS = frozenset({"thin_sample_overconfidence", "sparse_data"})
COURSE_HISTORY_MISSING = "course_history_missing"


def flag_player(
    player: PlayerInputs,
    theta: ThetaState,
    bundle: ProbabilityBundle,
) -> list[str]:
    flags: list[str] = []
    by_id = {c.factor_id: c for c in theta.contributions}
    rec = abs(by_id.get("recent_form").delta_theta) if by_id.get("recent_form") else 0.0
    trend = abs(by_id.get("short_term_trend").delta_theta) if by_id.get("short_term_trend") else 0.0
    talent_move = abs(theta.mean - player.talent_prior)
    if rec + trend > 0.55 * max(talent_move, 0.15) and rec + trend > 0.12:
        flags.append("recency_bias_risk")
    nar = by_id.get("narrative_momentum")
    if nar and abs(nar.delta_theta) >= NARRATIVE_ABS_CAP - 1e-6:
        flags.append("narrative_overweight")
    elif nar and abs(nar.delta_theta) > 0.20:
        flags.append("narrative_overweight")
    win = bundle.p(Horizon.WIN)
    width = win.high - win.low
    thin_player = bool(player.player.is_lesser_known)
    thin_course = player.course_history_rounds < THIN_SAMPLE_N
    if thin_player:
        if width < 0.04 and win.central > 0.03:
            flags.append("thin_sample_overconfidence")
        flags.append("sparse_data")
    elif thin_course:
        flags.append(COURSE_HISTORY_MISSING)
    return flags


def favorite_longshot_flags(
    bundles: dict[str, ProbabilityBundle],
    market: MarketSnapshot | None,
) -> list[str]:
    if not market:
        return []
    model_wins = sorted((b.p(Horizon.WIN).central for b in bundles.values()), reverse=True)
    implied = []
    for q in market.quotes:
        if q.bet_type.value == "win" and (q.implied_fair or q.implied_raw):
            implied.append(q.implied_fair or q.implied_raw)
    if len(model_wins) < 5 or len(implied) < 5:
        return []
    implied.sort(reverse=True)
    # peakedness: share of top-3
    m_top3 = sum(model_wins[:3])
    i_top3 = sum(implied[:3])
    out = []
    if m_top3 > i_top3 + 0.12:
        out.append("model_more_peaked_than_market_favorite_bias_risk")
    if m_top3 + 0.12 < i_top3:
        out.append("model_flatter_than_market_longshot_bias_risk")
    return out
