"""Original vs live edge, runners, collapsed edges."""

from __future__ import annotations

from golf_offshoot.config import (
    STRATEGY_EDGE_COLLAPSE_RATIO,
    STRATEGY_EDGE_IMPROVE_ABS,
    STRATEGY_RUNNER_PNL_FRAC,
)
from golf_offshoot.models.enums import BetType, StrategyMode, horizon_for
from golf_offshoot.models.schemas import PlayerOutput
from golf_offshoot.models.strategy import PositionMark, StrategyPosition
from golf_offshoot.strategy.cashout import bid_cashout_dollars, compare_cashout, min_sell_price


def mark_position(
    pos: StrategyPosition,
    row: PlayerOutput | None,
    *,
    cashout_quote: float | None = None,
    mode: StrategyMode = StrategyMode.STAY_SELECTIVE,
    ticket_screen: str = "both",
) -> PositionMark:
    live_model = pos.entry_model_p
    live_low = pos.entry_model_p
    live_high = pos.entry_model_p
    live_market = None
    live_edge = None
    width = 0.20
    rel = 0.40
    live_dec = None
    live_posted_edge = None
    if row is not None:
        h = horizon_for(pos.bet_type)
        hp = row.probabilities.horizons.get(h) if h is not None else None
        if hp is not None:
            live_model = hp.central
            live_low = hp.low
            live_high = hp.high
            width = float(hp.high - hp.low)
        rel = row.reliability.score
        live_market = row.market_implied_by_bet.get(pos.bet_type.value)
        live_edge = row.edge_by_bet.get(pos.bet_type.value)
        posted = row.posted_odds_by_bet.get(pos.bet_type.value)
        try:
            posted_f = float(posted) if posted is not None else None
        except (TypeError, ValueError):
            posted_f = None
        if posted_f is not None and posted_f > 1.0:
            live_dec = posted_f
        elif live_market and live_market > 0:
            live_dec = 1.0 / live_market
        if posted_f is not None and posted_f > 1.0:
            live_posted_edge = live_model - 1.0 / posted_f
    if live_edge is None and live_market is not None:
        live_edge = live_model - live_market

    live_bid = None
    shares = float(pos.shares) if pos.shares and pos.shares > 0 else None
    if row is not None:
        raw_bid = row.bid_by_bet.get(pos.bet_type.value)
        try:
            bid_f = float(raw_bid) if raw_bid is not None else None
        except (TypeError, ValueError):
            bid_f = None
        if bid_f is not None and 0.0 < bid_f < 1.0:
            live_bid = bid_f
    bid_quote = bid_cashout_dollars(shares, live_bid)
    typed = cashout_quote is not None and cashout_quote > 0
    quote = float(cashout_quote) if typed else bid_quote

    mtm = pos.stake
    mtm_is_cashout = False
    mtm_is_bid = False
    cmp = None
    if quote is not None and quote > 0:
        cmp = compare_cashout(
            stake=pos.stake,
            decimal_odds=pos.decimal_odds,
            live_model_p=live_model,
            live_model_low=live_low,
            live_model_high=live_high,
            quote=quote,
            mode=mode,
        )
        mtm = cmp.quote
        mtm_is_cashout = True
        mtm_is_bid = bool(bid_quote is not None and not typed)
    elif live_dec and live_dec > 1.0:
        mtm = pos.stake * (pos.decimal_odds / live_dec)
    pnl = mtm - pos.stake

    collapsed = False
    action_edge = live_edge
    if (ticket_screen or "both").lower() == "posted":
        action_edge = live_posted_edge
    unmarked = action_edge is None
    if action_edge is not None:
        floor = STRATEGY_EDGE_COLLAPSE_RATIO * max(pos.entry_edge, 0.01)
        collapsed = action_edge < floor or action_edge < 0.0
    improved = False
    if action_edge is not None:
        improved = action_edge >= pos.entry_edge + STRATEGY_EDGE_IMPROVE_ABS
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
        live_posted_edge=live_posted_edge,
        stake=pos.stake,
        mtm_value=float(mtm),
        unrealized_pnl=float(pnl),
        original_edge_collapsed=collapsed,
        live_edge_improved=improved,
        is_runner=runner,
        range_width=width,
        reliability=rel,
        live_model_low=live_low,
        live_model_high=live_high,
        cashout_quote=cmp.quote if cmp else None,
        hold_expected_payout=cmp.hold_central if cmp else None,
        hold_expected_payout_low=cmp.hold_low if cmp else None,
        hold_expected_payout_high=cmp.hold_high if cmp else None,
        cashout_threshold=cmp.threshold if cmp else None,
        cashout_beats_hold=cmp.beats_hold if cmp else None,
        mtm_is_cashout=mtm_is_cashout,
        mtm_is_bid=mtm_is_bid,
        live_bid=live_bid,
        shares=shares,
        min_sell_price=min_sell_price(cmp.threshold if cmp else None, shares),
        live_edge_unmarked=unmarked,
    )
