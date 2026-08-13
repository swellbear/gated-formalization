"""Strategy status summary and heat / cooling-off checks."""

from __future__ import annotations

from golf_offshoot.models.enums import StrategyMode
from golf_offshoot.models.strategy import (
    ConcentrationSlice,
    PortfolioState,
    PositionMark,
    StrategyAction,
    StrategyConfig,
    StrategyStatusSummary,
)
from golf_offshoot.strategy.sizing import scaled_exposure_cap


def cooling_off(book: PortfolioState, config: StrategyConfig) -> bool:
    if config.bankroll <= 0:
        return True
    daily = -min(0.0, book.realized_pnl_today) / config.bankroll
    event = -min(0.0, book.realized_pnl_event) / config.bankroll
    if daily >= config.controls.max_daily_loss_frac:
        return True
    if event >= config.controls.cooling_off_drawdown_frac:
        return True
    return False


def status_summary(
    book: PortfolioState,
    marks: list[PositionMark],
    concentrations: list[ConcentrationSlice],
    actions: list[StrategyAction],
    config: StrategyConfig,
    cooling: bool,
) -> StrategyStatusSummary:
    exposure = book.open_exposure
    frac = exposure / config.bankroll if config.bankroll else 0.0
    upnl = sum(m.unrealized_pnl for m in marks)
    w_edge = 0.0
    w = 0.0
    for m in marks:
        if m.live_edge is not None:
            w_edge += m.live_edge * m.stake
            w += m.stake
    biggest = "none"
    biggest_f = 0.0
    if concentrations:
        top = max(concentrations, key=lambda c: c.fraction_of_book)
        biggest = f"{top.axis}: {top.label}"
        biggest_f = top.fraction_of_book
    return StrategyStatusSummary(
        open_exposure=exposure,
        exposure_frac=frac,
        unrealized_pnl=upnl,
        unrealized_edge_weighted=(w_edge / w) if w else 0.0,
        biggest_concentration=biggest,
        biggest_concentration_frac=biggest_f,
        posture=config.mode,
        cooling_off=cooling,
        n_positions=len(book.positions),
        n_suggested_actions=len(actions),
        layer_enabled=config.enabled,
    )


def format_status(s: StrategyStatusSummary) -> str:
    posture = {
        StrategyMode.PROTECT_PROFITS: "Protect",
        StrategyMode.PRESS_EDGES: "Press",
        StrategyMode.STAY_SELECTIVE: "Selective",
    }[s.posture]
    cool = " cooling-off" if s.cooling_off else ""
    return (
        f"Open exposure {s.open_exposure:.2f} ({s.exposure_frac:.0%} of bankroll) | "
        f"unrealized {s.unrealized_pnl:+.2f} | "
        f"weighted live edge {s.unrealized_edge_weighted:+.3f} | "
        f"concentration {s.biggest_concentration} {s.biggest_concentration_frac:.0%} | "
        f"posture {posture}{cool}"
    )


def over_exposure(book: PortfolioState, config: StrategyConfig) -> bool:
    return book.open_exposure >= config.bankroll * scaled_exposure_cap(config) - 1e-9
