"""Pre-tournament strategy construction. Suggestions only."""

from __future__ import annotations

from golf_offshoot.decision.layer import advise_bet
from golf_offshoot.market.odds import yes_ask_sum, yes_book_is_ticketable
from golf_offshoot.models.enums import BetType, DecisionAction, StrategyActionKind, horizon_for
from golf_offshoot.models.schemas import FieldSnapshot, PlayerOutput
from golf_offshoot.models.strategy import (
    StrategyAction,
    StrategyConfig,
    StrategyPosition,
    new_id,
)
from golf_offshoot.strategy import explanations as X
from golf_offshoot.strategy.correlation import would_raise_cut_stack, would_stack_win_proxy
from golf_offshoot.strategy.flip import build_flip_new
from golf_offshoot.strategy.sizing import (
    remaining_exposure_capacity,
    scaled_cut_cap,
    suggested_stake,
)

def _odds(row: PlayerOutput, bet: BetType, *, posted_only: bool = False) -> float | None:
    posted = row.posted_odds_by_bet.get(bet.value)
    if posted and posted > 1.0:
        return posted
    if posted_only:
        return None
    imp = row.market_implied_by_bet.get(bet.value)
    if imp and imp > 0:
        return 1.0 / imp
    return None


def _edge(row: PlayerOutput, bet: BetType) -> float | None:
    return row.edge_by_bet.get(bet.value)


def _posted_edge(row: PlayerOutput, bet: BetType) -> float | None:
    odds = _odds(row, bet, posted_only=True)
    if not odds or odds <= 1.0:
        return None
    return float(row.probabilities.p(horizon_for(bet)).central - 1.0 / odds)


def _score(row: PlayerOutput, bet: BetType, ticket_screen: str = "both") -> float:
    hp = row.probabilities.p(horizon_for(bet))
    width = max(hp.high - hp.low, 1e-6)
    if (ticket_screen or "both").lower() == "posted":
        e = _posted_edge(row, bet) or 0.0
    else:
        e = _edge(row, bet) or 0.0
    return e * row.reliability.score / (1.0 + 4.0 * width)


def build_pre_tournament(
    rows: list[PlayerOutput],
    config: StrategyConfig,
    field: FieldSnapshot | None = None,
) -> tuple[list[StrategyAction], list[StrategyPosition]]:
    """Suggested initial book. Does not mutate bankroll or place bets."""
    actions: list[StrategyAction] = []
    proposed: list[StrategyPosition] = []
    open_exp = 0.0
    by_id = {r.player_id: r for r in rows}

    candidates: list[tuple[float, PlayerOutput, BetType]] = []
    posted_only = (config.ticket_screen or "both").lower() == "posted"
    skip_bets = {
        bet
        for bet in config.allowed_bet_types
        if not yes_book_is_ticketable(
            bet,
            yes_ask_sum([_odds(r, bet, posted_only=True) for r in rows]),
        )
    }
    for row in rows:
        for bet in config.allowed_bet_types:
            if bet in skip_bets:
                continue
            if horizon_for(bet) not in row.probabilities.horizons:
                continue
            odds = _odds(row, bet, posted_only=posted_only)
            advice = advise_bet(
                row,
                bet,
                odds,
                ticket_screen=config.ticket_screen,
            )
            if advice.action == DecisionAction.PASS:
                continue
            if posted_only:
                pe = _posted_edge(row, bet)
                if pe is None or pe <= 0:
                    continue
            else:
                e = _edge(row, bet)
                if e is None or e <= 0:
                    continue
            candidates.append((_score(row, bet, config.ticket_screen), row, bet))
    candidates.sort(key=lambda t: t[0], reverse=True)

    for _, row, bet in candidates:
        cap = remaining_exposure_capacity(open_exp, config.bankroll, config)
        if cap <= 0:
            actions.append(
                StrategyAction(
                    action_id=new_id("act"),
                    kind=StrategyActionKind.NO_ACTION,
                    player_id=row.player_id,
                    player_name=row.name,
                    bet_type=bet,
                    reason=X.exposure_cap(),
                    reasons_detail=["Pre-tournament book already at exposure limit"],
                )
            )
            break
        hp = row.probabilities.p(horizon_for(bet))
        odds = _odds(row, bet, posted_only=posted_only)
        if not odds:
            continue
        stake, warn = suggested_stake(
            bankroll=config.bankroll,
            model_p=hp.central,
            low_p=hp.low,
            decimal_odds=odds,
            range_width=hp.high - hp.low,
            reliability=row.reliability.score,
            config=config,
            remaining_capacity=cap,
            bet_type=bet,
        )
        if stake <= 0:
            actions.append(
                StrategyAction(
                    action_id=new_id("act"),
                    kind=StrategyActionKind.NO_ACTION,
                    player_id=row.player_id,
                    player_name=row.name,
                    bet_type=bet,
                    reason=warn or X.range_too_wide(),
                    uncertainty_warning=warn,
                    reasons_detail=["Screened as a candidate but size blocked"],
                )
            )
            continue
        if would_raise_cut_stack(proposed, row.player_id, stake, by_id, scaled_cut_cap(config)):
            actions.append(
                StrategyAction(
                    action_id=new_id("act"),
                    kind=StrategyActionKind.NO_ACTION,
                    player_id=row.player_id,
                    player_name=row.name,
                    bet_type=bet,
                    reason=X.concentrated_cut(),
                    reasons_detail=["Skipped to avoid stacking correlated cut-risk"],
                )
            )
            continue
        if would_stack_win_proxy(proposed, row.player_id, bet):
            actions.append(
                StrategyAction(
                    action_id=new_id("act"),
                    kind=StrategyActionKind.NO_ACTION,
                    player_id=row.player_id,
                    player_name=row.name,
                    bet_type=bet,
                    reason=X.win_proxy_stack(),
                    reasons_detail=["Skipped Win / R2 / R3 stack on the same player; R1 may sit beside Win"],
                )
            )
            continue
        pid = new_id("pos")
        e = _edge(row, bet) or 0.0
        pos = StrategyPosition(
            position_id=pid,
            player_id=row.player_id,
            player_name=row.name,
            bet_type=bet,
            stake=stake,
            decimal_odds=odds,
            entry_edge=e,
            entry_model_p=hp.central,
            entry_market_p=row.market_implied_by_bet.get(bet.value),
            round_entered=0,
            notes="pre-tournament suggestion",
            proposed=True,
            user_recorded=False,
        )
        proposed.append(pos)
        open_exp += stake
        detail = [
            f"edge {e:+.3f}",
            f"reliability {row.reliability.score:.2f}",
            f"range {hp.low:.3f}–{hp.high:.3f}",
        ]
        actions.append(
            StrategyAction(
                action_id=new_id("act"),
                kind=StrategyActionKind.NEW_BET,
                player_id=row.player_id,
                player_name=row.name,
                bet_type=bet,
                position_id=pid,
                suggested_stake_delta=stake,
                suggested_unit=stake,
                reason=X.fresh_edge(),
                reasons_detail=detail,
                uncertainty_warning=warn or (X.noisy_inputs() if row.reliability.score < 0.45 else None),
            )
        )
    flip_actions, flip_pos = build_flip_new(rows, config, proposed, field)
    actions.extend(flip_actions)
    proposed.extend(flip_pos)
    return actions, proposed
