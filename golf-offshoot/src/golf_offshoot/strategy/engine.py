"""Facade for the optional strategy layer. Never auto-bets."""

from __future__ import annotations

from golf_offshoot.models.enums import RunMode, StrategyActionKind
from golf_offshoot.models.schemas import FieldSnapshot, PlayerOutput
from golf_offshoot.models.strategy import (
    PortfolioState,
    StrategyConfig,
    StrategyRecommendation,
    UserStrategyDecision,
    new_id,
)
from golf_offshoot.strategy.builder import build_pre_tournament
from golf_offshoot.strategy.correlation import concentrations
from golf_offshoot.strategy.live import live_manage
from golf_offshoot.strategy.path import mark_position
from golf_offshoot.strategy.status import cooling_off, format_status, status_summary


def disabled_recommendation(config: StrategyConfig, run_mode: RunMode) -> StrategyRecommendation:
    empty = PortfolioState(bankroll=config.bankroll)
    st = status_summary(empty, [], [], [], config, cooling=False)
    st.layer_enabled = False
    return StrategyRecommendation(
        recommendation_id=new_id("rec"),
        mode=config.mode,
        run_mode=run_mode,
        status=st,
        enabled=False,
        never_auto_bet=True,
        notes=["Strategy layer off — pure analysis mode"],
    )


def run_strategy(
    rows: list[PlayerOutput],
    config: StrategyConfig,
    *,
    run_mode: RunMode,
    field: FieldSnapshot | None = None,
    book: PortfolioState | None = None,
    cashout_quotes: dict[str, float] | None = None,
) -> StrategyRecommendation:
    if not config.enabled:
        return disabled_recommendation(config, run_mode)

    book = book or PortfolioState(bankroll=config.bankroll)
    cooling = cooling_off(book, config)
    notes: list[str] = []
    if cooling:
        notes.append("Cooling-off after sharp drawdown — no new risk")
    if cashout_quotes:
        notes.append(
            "User-typed cash-out quotes used for this snapshot. Not scraped. "
            "Not a standing price. Take vs hold uses remaining winner EV."
        )

    if run_mode == RunMode.PRE_TOURNAMENT and not book.positions:
        actions, proposed = build_pre_tournament(rows, config, field)
        marks = [mark_position(p, next((r for r in rows if r.player_id == p.player_id), None)) for p in proposed]
        conc = concentrations(proposed, {r.player_id: r for r in rows}, field)
        tmp_book = PortfolioState(bankroll=config.bankroll, positions=proposed)
        st = status_summary(tmp_book, marks, conc, actions, config, cooling)
        return StrategyRecommendation(
            recommendation_id=new_id("rec"),
            mode=config.mode,
            run_mode=run_mode,
            actions=actions,
            proposed_new_positions=proposed,
            marks=marks,
            concentrations=conc,
            status=st,
            cooling_off=cooling,
            enabled=True,
            never_auto_bet=True,
            notes=notes,
        )

    actions, proposed, marks = live_manage(
        rows, book, config, field, cooling, cashout_quotes=cashout_quotes
    )
    conc = concentrations(book.positions, {r.player_id: r for r in rows}, field)
    st = status_summary(book, marks, conc, actions, config, cooling)
    return StrategyRecommendation(
        recommendation_id=new_id("rec"),
        mode=config.mode,
        run_mode=run_mode,
        actions=actions,
        proposed_new_positions=proposed,
        marks=marks,
        concentrations=conc,
        status=st,
        cooling_off=cooling,
        enabled=True,
        never_auto_bet=True,
        notes=notes,
    )


def record_user_decision(
    rec: StrategyRecommendation,
    action_id: str | None,
    accepted: bool,
    *,
    modified_stake: float | None = None,
    note: str = "",
    operator: str = "",
) -> UserStrategyDecision:
    """Log the user's choice. Does not place a bet."""
    return UserStrategyDecision(
        recommendation_id=rec.recommendation_id,
        action_id=action_id,
        accepted=accepted,
        modified_stake=modified_stake,
        note=note,
        operator=operator,
        placed_by_user=True,
    )


def format_recommendation(rec: StrategyRecommendation) -> str:
    lines = [
        f"strategy {rec.recommendation_id} enabled={rec.enabled} never_auto_bet={rec.never_auto_bet}",
        format_status(rec.status),
    ]
    for a in rec.actions:
        if a.kind == StrategyActionKind.NO_ACTION:
            continue
        extra = f" d{a.suggested_stake_delta:+.2f}" if a.suggested_stake_delta else ""
        warn = f" warn: {a.uncertainty_warning}" if a.uncertainty_warning else ""
        cash = ""
        if a.cashout_quote is not None:
            hold = f"{a.hold_expected_payout:.2f}" if a.hold_expected_payout is not None else "n/a"
            bar = f"{a.cashout_threshold:.2f}" if a.cashout_threshold is not None else "n/a"
            cash = f" cash-out ${a.cashout_quote:.2f} vs hold EV ${hold} sell-bar ${bar}"
        lines.append(
            f"  {a.kind.value:11} {a.player_name or a.player_id} {a.bet_type.value}{extra} -- {a.reason}{cash}{warn}"
        )
    if rec.cooling_off:
        lines.append("  (cooling-off: ADD / NEW_BET suppressed)")
    for n in rec.notes:
        lines.append(f"  note: {n}")
    return "\n".join(lines)
