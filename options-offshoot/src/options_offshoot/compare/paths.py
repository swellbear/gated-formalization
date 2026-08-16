"""Compare-path ids and ticket screens."""

from __future__ import annotations

from dataclasses import dataclass

from options_offshoot.compare.law import METHOD_LAW_V1
from options_offshoot.models.enums import ComparePath, TicketScreen

COMPARE_LEDGERS = (
    ComparePath.A_REPLAY,
    ComparePath.B_GUTS,
    ComparePath.B_NERVES,
    ComparePath.B_FULL,
)


@dataclass(frozen=True)
class PathConfig:
    path: ComparePath
    ticket_screen: str
    honest: bool


def ledger_id(path: ComparePath) -> str:
    return path.value


def uses_honest_theta(path: ComparePath) -> bool:
    return path in (ComparePath.B_GUTS, ComparePath.B_FULL)


def config_for(path: ComparePath) -> PathConfig:
    if path in (ComparePath.B_NERVES, ComparePath.B_FULL):
        screen = TicketScreen.ASK.value
    elif path in (ComparePath.A_REPLAY, ComparePath.B_GUTS):
        screen = TicketScreen.MID.value
    else:
        screen = TicketScreen.BOTH.value
    return PathConfig(
        path=path,
        ticket_screen=screen,
        honest=uses_honest_theta(path),
    )


def starting_bankroll() -> float:
    return float(METHOD_LAW_V1["independent_compare_bankroll"])
