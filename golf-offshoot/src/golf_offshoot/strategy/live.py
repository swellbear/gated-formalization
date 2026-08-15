"""Live Thursday→Sunday strategy management. Suggestions only."""

from __future__ import annotations

from golf_offshoot.models.enums import (
    BetType,
    Horizon,
    StrategyActionKind,
    StrategyMode,
)
from golf_offshoot.models.schemas import FieldSnapshot, PlayerOutput
from golf_offshoot.models.strategy import (
    PortfolioState,
    PositionMark,
    StrategyAction,
    StrategyConfig,
    StrategyPosition,
    new_id,
)
from golf_offshoot.strategy import explanations as X
from golf_offshoot.strategy.builder import build_pre_tournament
from golf_offshoot.strategy.correlation import concentrations, would_raise_cut_stack
from golf_offshoot.strategy.cashout import compare_cashout
from golf_offshoot.strategy.path import mark_position
from golf_offshoot.strategy.sizing import (
    remaining_exposure_capacity,
    scaled_cut_cap,
    suggested_stake,
    uncertainty_blocks_action,
)

_H = {
    BetType.WIN: Horizon.WIN,
    BetType.TOP_5: Horizon.TOP_5,
    BetType.TOP_10: Horizon.TOP_10,
    BetType.TOP_20: Horizon.TOP_20,
    BetType.MAKE_CUT: Horizon.MAKE_CUT,
}


def _reduce_frac(config: StrategyConfig, mark: PositionMark) -> float:
    if config.mode == StrategyMode.PROTECT_PROFITS:
        return 0.55 if mark.is_runner else 0.40
    if config.mode == StrategyMode.PRESS_EDGES:
        return 0.25
    return 0.40


def _cashout_fields(mark: PositionMark) -> dict:
    return {
        "cashout_quote": mark.cashout_quote,
        "hold_expected_payout": mark.hold_expected_payout,
        "cashout_threshold": mark.cashout_threshold,
    }


def _hold_reason(mark: PositionMark) -> str:
    if mark.live_edge_unmarked:
        return X.unmarked_ride_to_settle()
    return X.hold_edge_intact()


def _action_for_open(
    mark: PositionMark,
    pos: StrategyPosition,
    config: StrategyConfig,
    cooling: bool,
) -> StrategyAction:
    name = pos.player_name
    details = [
        f"entry edge {mark.entry_edge:+.3f}",
        f"live edge {mark.live_edge:+.3f}" if mark.live_edge is not None else "live edge n/a",
        f"unrealized {mark.unrealized_pnl:+.2f}",
    ]
    if mark.cashout_quote is not None:
        cmp = compare_cashout(
            stake=pos.stake,
            decimal_odds=pos.decimal_odds,
            live_model_p=mark.live_model_p,
            live_model_low=mark.live_model_low if mark.live_model_low is not None else mark.live_model_p,
            live_model_high=mark.live_model_high if mark.live_model_high is not None else mark.live_model_p,
            quote=mark.cashout_quote,
            mode=config.mode,
        )
        details.extend(cmp.notes)
        if mark.mtm_is_cashout:
            details.append("MTM is the typed cash-out, not the odds-ratio proxy")
        if cmp.beats_hold:
            return StrategyAction(
                action_id=new_id("act"),
                kind=StrategyActionKind.EXIT,
                player_id=pos.player_id,
                player_name=name,
                bet_type=pos.bet_type,
                position_id=pos.position_id,
                suggested_stake_delta=-pos.stake,
                suggested_unit=pos.stake,
                reason=X.cashout_beats_hold(),
                reasons_detail=details,
                uncertainty_warning=X.noisy_inputs(mark) if mark.reliability < 0.45 else None,
                **_cashout_fields(mark),
            )
        # Real quote exists and loses to hold EV: do not invent a better sell.
        if cooling:
            return StrategyAction(
                action_id=new_id("act"),
                kind=StrategyActionKind.HOLD,
                player_id=pos.player_id,
                player_name=name,
                bet_type=pos.bet_type,
                position_id=pos.position_id,
                reason=X.cooling_off(),
                reasons_detail=details + [X.cashout_below_hold()],
                **_cashout_fields(mark),
            )
        if mark.live_edge_improved and not cooling:
            if config.mode == StrategyMode.STAY_SELECTIVE and (mark.live_edge or 0) < 0.05:
                return StrategyAction(
                    action_id=new_id("act"),
                    kind=StrategyActionKind.HOLD,
                    player_id=pos.player_id,
                    player_name=name,
                    bet_type=pos.bet_type,
                    position_id=pos.position_id,
                    reason=X.cashout_below_hold(),
                    reasons_detail=details + [X.selective_not_strong()],
                    **_cashout_fields(mark),
                )
            if config.mode == StrategyMode.PROTECT_PROFITS:
                return StrategyAction(
                    action_id=new_id("act"),
                    kind=StrategyActionKind.HOLD,
                    player_id=pos.player_id,
                    player_name=name,
                    bet_type=pos.bet_type,
                    position_id=pos.position_id,
                    reason=X.cashout_below_hold(),
                    reasons_detail=details + ["Protect Profits: do not add into a live move"],
                    **_cashout_fields(mark),
                )
            block = uncertainty_blocks_action(mark.range_width, mark.reliability)
            if block and config.mode != StrategyMode.PRESS_EDGES:
                return StrategyAction(
                    action_id=new_id("act"),
                    kind=StrategyActionKind.HOLD,
                    player_id=pos.player_id,
                    player_name=name,
                    bet_type=pos.bet_type,
                    position_id=pos.position_id,
                    reason=X.cashout_below_hold(),
                    uncertainty_warning=block,
                    reasons_detail=details,
                    **_cashout_fields(mark),
                )
            add = pos.stake * (0.40 if config.mode == StrategyMode.PRESS_EDGES else 0.20)
            return StrategyAction(
                action_id=new_id("act"),
                kind=StrategyActionKind.ADD,
                player_id=pos.player_id,
                player_name=name,
                bet_type=pos.bet_type,
                position_id=pos.position_id,
                suggested_stake_delta=add,
                suggested_unit=add,
                reason=X.live_improved(),
                reasons_detail=details + [X.cashout_below_hold()],
                uncertainty_warning=block,
                **_cashout_fields(mark),
            )
        extra = []
        if mark.original_edge_collapsed:
            extra.append("live edge collapsed vs market, but the typed cash-out still loses to hold EV")
        return StrategyAction(
            action_id=new_id("act"),
            kind=StrategyActionKind.HOLD,
            player_id=pos.player_id,
            player_name=name,
            bet_type=pos.bet_type,
            position_id=pos.position_id,
            reason=X.cashout_below_hold(),
            reasons_detail=details + extra,
            uncertainty_warning=X.noisy_inputs(mark) if mark.reliability < 0.45 else None,
            **_cashout_fields(mark),
        )

    if mark.original_edge_collapsed:
        kind = StrategyActionKind.EXIT
        if config.mode == StrategyMode.PRESS_EDGES and mark.live_edge is not None and mark.live_edge > -0.01:
            kind = StrategyActionKind.REDUCE
            delta = -pos.stake * 0.5
        else:
            delta = -pos.stake
        return StrategyAction(
            action_id=new_id("act"),
            kind=kind,
            player_id=pos.player_id,
            player_name=name,
            bet_type=pos.bet_type,
            position_id=pos.position_id,
            suggested_stake_delta=delta,
            suggested_unit=abs(delta),
            reason=X.collapsed(),
            reasons_detail=details,
            uncertainty_warning=X.noisy_inputs(mark) if mark.reliability < 0.45 else None,
        )

    if cooling:
        if mark.is_runner and config.mode == StrategyMode.PROTECT_PROFITS:
            delta = -pos.stake * 0.5
            return StrategyAction(
                action_id=new_id("act"),
                kind=StrategyActionKind.REDUCE,
                player_id=pos.player_id,
                player_name=name,
                bet_type=pos.bet_type,
                position_id=pos.position_id,
                suggested_stake_delta=delta,
                suggested_unit=abs(delta),
                reason=X.cooling_off(),
                reasons_detail=details + [X.runner_lock()],
            )
        return StrategyAction(
            action_id=new_id("act"),
            kind=StrategyActionKind.HOLD,
            player_id=pos.player_id,
            player_name=name,
            bet_type=pos.bet_type,
            position_id=pos.position_id,
            reason=X.cooling_off(),
            reasons_detail=details,
        )

    if mark.is_runner:
        if config.mode == StrategyMode.PROTECT_PROFITS:
            delta = -pos.stake * _reduce_frac(config, mark)
            return StrategyAction(
                action_id=new_id("act"),
                kind=StrategyActionKind.REDUCE,
                player_id=pos.player_id,
                player_name=name,
                bet_type=pos.bet_type,
                position_id=pos.position_id,
                suggested_stake_delta=delta,
                suggested_unit=abs(delta),
                reason=X.runner_lock(),
                reasons_detail=details,
            )
        if config.mode == StrategyMode.STAY_SELECTIVE and (mark.live_edge or 0) < 0.04:
            delta = -pos.stake * 0.35
            return StrategyAction(
                action_id=new_id("act"),
                kind=StrategyActionKind.REDUCE,
                player_id=pos.player_id,
                player_name=name,
                bet_type=pos.bet_type,
                position_id=pos.position_id,
                suggested_stake_delta=delta,
                suggested_unit=abs(delta),
                reason=X.selective_not_strong(),
                reasons_detail=details,
            )
        # Press: hold runner; add only if live edge improved (handled below)
        if config.mode == StrategyMode.PRESS_EDGES and mark.live_edge_improved:
            block = uncertainty_blocks_action(mark.range_width, mark.reliability)
            if block:
                return StrategyAction(
                    action_id=new_id("act"),
                    kind=StrategyActionKind.HOLD,
                    player_id=pos.player_id,
                    player_name=name,
                    bet_type=pos.bet_type,
                    position_id=pos.position_id,
                    reason=block,
                    reasons_detail=details,
                    uncertainty_warning=block,
                )
            add = pos.stake * 0.35
            return StrategyAction(
                action_id=new_id("act"),
                kind=StrategyActionKind.ADD,
                player_id=pos.player_id,
                player_name=name,
                bet_type=pos.bet_type,
                position_id=pos.position_id,
                suggested_stake_delta=add,
                suggested_unit=add,
                reason=X.live_improved(),
                reasons_detail=details,
            )
        return StrategyAction(
            action_id=new_id("act"),
            kind=StrategyActionKind.HOLD,
            player_id=pos.player_id,
            player_name=name,
            bet_type=pos.bet_type,
            position_id=pos.position_id,
            reason=_hold_reason(mark),
            reasons_detail=details,
        )

    if mark.live_edge_improved and not cooling:
        if config.mode == StrategyMode.STAY_SELECTIVE and (mark.live_edge or 0) < 0.05:
            return StrategyAction(
                action_id=new_id("act"),
                kind=StrategyActionKind.HOLD,
                player_id=pos.player_id,
                player_name=name,
                bet_type=pos.bet_type,
                position_id=pos.position_id,
                reason=X.selective_not_strong(),
                reasons_detail=details,
            )
        if config.mode == StrategyMode.PROTECT_PROFITS:
            return StrategyAction(
                action_id=new_id("act"),
                kind=StrategyActionKind.HOLD,
                player_id=pos.player_id,
                player_name=name,
                bet_type=pos.bet_type,
                position_id=pos.position_id,
                reason=X.live_improved_generic(),
                reasons_detail=details + ["Protect Profits: do not add into a live move"],
            )
        block = uncertainty_blocks_action(mark.range_width, mark.reliability)
        if block and config.mode != StrategyMode.PRESS_EDGES:
            return StrategyAction(
                action_id=new_id("act"),
                kind=StrategyActionKind.HOLD,
                player_id=pos.player_id,
                player_name=name,
                bet_type=pos.bet_type,
                position_id=pos.position_id,
                reason=block,
                uncertainty_warning=block,
                reasons_detail=details,
            )
        add = pos.stake * (0.40 if config.mode == StrategyMode.PRESS_EDGES else 0.20)
        return StrategyAction(
            action_id=new_id("act"),
            kind=StrategyActionKind.ADD,
            player_id=pos.player_id,
            player_name=name,
            bet_type=pos.bet_type,
            position_id=pos.position_id,
            suggested_stake_delta=add,
            suggested_unit=add,
            reason=X.live_improved(),
            reasons_detail=details,
            uncertainty_warning=block,
        )

    return StrategyAction(
        action_id=new_id("act"),
        kind=StrategyActionKind.HOLD,
        player_id=pos.player_id,
        player_name=name,
        bet_type=pos.bet_type,
        position_id=pos.position_id,
        reason=_hold_reason(mark),
        reasons_detail=details,
        uncertainty_warning=X.noisy_inputs(mark) if mark.reliability < 0.45 else None,
    )


def live_manage(
    rows: list[PlayerOutput],
    book: PortfolioState,
    config: StrategyConfig,
    field: FieldSnapshot | None,
    cooling: bool,
    cashout_quotes: dict[str, float] | None = None,
) -> tuple[list[StrategyAction], list[StrategyPosition], list[PositionMark]]:
    by_id = {r.player_id: r for r in rows}
    quotes = cashout_quotes or {}
    marks = [
        mark_position(
            p,
            by_id.get(p.player_id),
            cashout_quote=quotes.get(p.player_id),
            mode=config.mode,
            ticket_screen=config.ticket_screen,
        )
        for p in book.positions
    ]
    actions: list[StrategyAction] = []

    for pos, mark in zip(book.positions, marks):
        actions.append(_action_for_open(mark, pos, config, cooling))

    # concentration: reduce worst live-edge cut-risk stack
    conc = concentrations(book.positions, by_id, field)
    cut = next((c for c in conc if c.axis == "cut_risk"), None)
    if cut and cut.fraction_of_book > scaled_cut_cap(config):
        worst = None
        worst_e = 9.0
        for pos, mark in zip(book.positions, marks):
            if pos.player_id in cut.player_ids:
                e = mark.live_edge if mark.live_edge is not None else -1.0
                if e < worst_e:
                    worst_e = e
                    worst = pos
        if worst:
            actions.append(
                StrategyAction(
                    action_id=new_id("act"),
                    kind=StrategyActionKind.REDUCE,
                    player_id=worst.player_id,
                    player_name=worst.player_name,
                    bet_type=worst.bet_type,
                    position_id=worst.position_id,
                    suggested_stake_delta=-0.4 * worst.stake,
                    suggested_unit=0.4 * worst.stake,
                    reason=X.concentrated_cut(),
                    reasons_detail=[f"cut-risk share {cut.fraction_of_book:.0%} of open book"],
                )
            )

    proposed: list[StrategyPosition] = []
    if cooling:
        return actions, proposed, marks

    held_keys = {(p.player_id, p.bet_type) for p in book.positions}
    new_actions, new_pos = build_pre_tournament(rows, config, field)
    open_exp = book.open_exposure
    for act, pos in zip(
        [a for a in new_actions if a.kind == StrategyActionKind.NEW_BET],
        new_pos,
    ):
        if (pos.player_id, pos.bet_type) in held_keys:
            continue
        cap = remaining_exposure_capacity(open_exp, config.bankroll, config)
        if cap <= 0:
            if not marks:
                continue
            donor = min(marks, key=lambda m: m.live_edge if m.live_edge is not None else 9.0)
            if donor.live_edge is not None and (pos.entry_edge - donor.live_edge) >= 0.03:
                take = min(pos.stake, 0.5 * donor.stake)
                actions.append(
                    StrategyAction(
                        action_id=new_id("act"),
                        kind=StrategyActionKind.REALLOCATE,
                        player_id=pos.player_id,
                        player_name=pos.player_name,
                        bet_type=pos.bet_type,
                        from_position_id=donor.position_id,
                        to_player_id=pos.player_id,
                        suggested_stake_delta=take,
                        suggested_unit=take,
                        reason="Reallocate into a better live opportunity",
                        reasons_detail=[
                            f"from {donor.player_id} live edge {donor.live_edge:+.3f}",
                            f"into {pos.player_id} edge {pos.entry_edge:+.3f}",
                        ],
                    )
                )
                proposed.append(pos.model_copy(update={"stake": take, "notes": "live reallocate suggestion"}))
            continue
        if would_raise_cut_stack(book.positions + proposed, pos.player_id, pos.stake, by_id, scaled_cut_cap(config)):
            act = act.model_copy(
                update={
                    "kind": StrategyActionKind.NO_ACTION,
                    "reason": X.concentrated_cut(),
                    "suggested_stake_delta": 0.0,
                }
            )
            actions.append(act)
            continue
        row = by_id.get(pos.player_id)
        if row:
            hp = row.probabilities.p(_H[pos.bet_type])
            stake, warn = suggested_stake(
                bankroll=config.bankroll,
                model_p=hp.central,
                low_p=hp.low,
                decimal_odds=pos.decimal_odds,
                range_width=hp.high - hp.low,
                reliability=row.reliability.score,
                config=config,
                remaining_capacity=cap,
            )
            if stake <= 0:
                continue
            pos = pos.model_copy(update={"stake": stake, "notes": "live new-bet suggestion"})
            act = act.model_copy(
                update={
                    "suggested_stake_delta": stake,
                    "suggested_unit": stake,
                    "uncertainty_warning": warn,
                    "reason": X.fresh_edge() if not warn else warn,
                }
            )
        actions.append(act)
        proposed.append(pos)
        open_exp += pos.stake
        held_keys.add((pos.player_id, pos.bet_type))

    return actions, proposed, marks
