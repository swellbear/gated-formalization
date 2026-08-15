"""Compare-path ids. Lived museum stays `{event}.json`."""

from __future__ import annotations

from enum import Enum

from golf_offshoot.compare.law import METHOD_LAW_V1
from golf_offshoot.models.enums import BetType, RiskPreference, StrategyMode
from golf_offshoot.models.strategy import StrategyConfig


class ComparePath(str, Enum):
    LIVED = "lived"
    A_REPLAY = "a_replay"
    A_CONTROL = "a_control"
    B_GUTS = "b_guts"
    B_NERVES = "b_nerves"
    B_FULL = "b_full"


COMPARE_LEDGERS = (
    ComparePath.A_REPLAY,
    ComparePath.B_GUTS,
    ComparePath.B_NERVES,
    ComparePath.B_FULL,
)


def experiment_config(*, ticket_screen: str, bankroll: float | None = None) -> StrategyConfig:
    return StrategyConfig(
        enabled=True,
        mode=StrategyMode.STAY_SELECTIVE,
        risk=RiskPreference.CONSERVATIVE,
        bankroll=float(bankroll if bankroll is not None else METHOD_LAW_V1["independent_compare_bankroll"]),
        ticket_screen=ticket_screen,
        never_auto_bet=True,
        allowed_bet_types=[BetType.WIN],
    )


def ledger_id(path: ComparePath) -> str:
    """A-control shares the A-replay ledger so the control stays one book."""
    if path == ComparePath.A_CONTROL:
        return ComparePath.A_REPLAY.value
    return path.value


def config_for(path: ComparePath, *, bankroll: float | None = None) -> StrategyConfig:
    if path in (ComparePath.B_NERVES, ComparePath.B_FULL):
        return experiment_config(ticket_screen="posted", bankroll=bankroll)
    if path in (ComparePath.A_REPLAY, ComparePath.A_CONTROL, ComparePath.B_GUTS):
        return experiment_config(ticket_screen="edgew", bankroll=bankroll)
    return experiment_config(ticket_screen="both", bankroll=bankroll)


def uses_honest_theta(path: ComparePath) -> bool:
    return path in (ComparePath.B_GUTS, ComparePath.B_FULL)


def posted_bar(path: ComparePath) -> bool:
    return path in (ComparePath.B_NERVES, ComparePath.B_FULL)
