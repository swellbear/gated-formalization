"""Run modes, contract side, compare paths."""

from __future__ import annotations

from enum import Enum


class RunMode(str, Enum):
    DEMO = "demo"
    INGEST = "ingest"
    LIVE = "live"


class ContractType(str, Enum):
    CALL = "call"
    PUT = "put"


class ComparePath(str, Enum):
    LIVED = "lived"
    A_REPLAY = "a_replay"
    B_GUTS = "b_guts"
    B_NERVES = "b_nerves"
    B_FULL = "b_full"


class TicketScreen(str, Enum):
    ASK = "ask"
    MID = "mid"
    BOTH = "both"


class SourceKind(str, Enum):
    REAL_LIVE = "real_live"
    REAL_HISTORICAL = "real_historical"
    DERIVED_FROM_REAL = "derived_from_real"
    UNAVAILABLE = "unavailable"
    MOCK = "mock"


class AdviceKind(str, Enum):
    HOLD = "hold"
    SELL = "sell"
    ADD = "add"
    NEW = "new"
    EXIT = "exit"
