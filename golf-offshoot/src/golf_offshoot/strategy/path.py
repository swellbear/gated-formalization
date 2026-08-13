"""Original vs live edge, runners, collapsed edges."""

from __future__ import annotations

from golf_offshoot.config import (
    STRATEGY_EDGE_COLLAPSE_RATIO,
    STRATEGY_EDGE_IMPROVE_ABS,
    STRATEGY_RUNNER_PNL_FRAC,
)
from golf_offshoot.models.enums import BetType, Horizon
from golf_offshoot.models.schemas import PlayerOutput
from golf_offshoot.models.strategy import PositionMark, StrategyPosition

_H = {
    BetType.WIN: Horizon.WIN,
    BetType.TOP_5: Horizon.TOP_5,
    BetType.TOP_10: Horizon.TOP_10,
    BetType.TOP_20: Horizon.TOP_20,
    BetType.MAKE_CUT: Horizon.MAKE_CUT,
}


def mark_position(pos: StrategyPosition, row: PlayerOutput | None) -> PositionMark:
    live_model = pos.entry_model_p
    live_market = None
    live_edge = None
    width = 0.20
    rel = 0.40
    live_dec = None
    if row is not None:
        hp = row.probabilities.p(_H[pos.bet_type])
        live_model = hp.central
        width = float(hp.high - hp.low)
        rel = row.reliability.score
        live_market = row.market_implied_by_bet.get(pos.bet_type.value)
        live_edge = row.edge_by_bet.get(pos.bet_type.value)
        if live_market and live_market > 0:
            live_dec = 1.0 / live_market
    if live_edge is None and live_market is not None:
        live_edge = live_model - live_market

    mtm = pos.stake
    if live_dec and live_dec > 1.0:
        mtm = pos.stake * (pos.decimal_odds / live_dec)
    pnl = mtm - pos.stake

    collapsed = False
    if live_edge is not None:
        floor = STRATEGY_EDGE_COLLAPSE_RATIO * max(pos.entry_edge, 0.01)
        collapsed = live_edge < floor or live_edge < 0.0
    improved = False
    if live_edge is not None:
        improved = live_edge >= pos.entry_edge + STRATEGY_EDGE_IMPROVE_ABS
    runner = pnl >= STRATEGY_RUNNER_PNL_FRAC * pos.stake

    return PositionMark(
        position_id=pos.position_id,
        player_id=pos.player_id,
        bet_type=pos.bet_type,
        entry_edge=pos.entry_edge,
        live_edge=live_edge,
        entry_model_p=pos.entry_model_p,
        live_model_p=live_model,
        entry_market_p=pos.entry_market_p,
        live_market_p=live_market,
        live_decimal_odds=live_dec,
        stake=pos.stake,
        mtm_value=float(mtm),
        unrealized_pnl=float(pnl),
        original_edge_collapsed=collapsed,
        live_edge_improved=improved,
        is_runner=runner,
        range_width=width,
        reliability=rel,
    )
