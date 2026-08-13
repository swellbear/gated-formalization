from __future__ import annotations

from enum import Enum


class CourseType(str, Enum):
    PARKLAND = "parkland"
    LINKS = "links"
    DESERT = "desert"
    TROPICAL = "tropical"
    STADIUM = "stadium"
    HEATHLAND = "heathland"
    MOUNTAIN = "mountain"
    MAJOR_SETUP = "major_setup"


class Horizon(str, Enum):
    MAKE_CUT = "make_cut"
    TOP_20 = "top_20"
    TOP_10 = "top_10"
    TOP_5 = "top_5"
    WIN = "win"


class BetType(str, Enum):
    WIN = "win"
    TOP_5 = "top_5"
    TOP_10 = "top_10"
    TOP_20 = "top_20"
    MAKE_CUT = "make_cut"


class RunMode(str, Enum):
    PRE_TOURNAMENT = "pre_tournament"
    LIVE = "live"


class DataRole(str, Enum):
    PRIMARY = "primary"
    FALLBACK = "fallback"
    MOCK = "mock"
    MANUAL = "manual"


class FactorStatus(str, Enum):
    UNCONSTRAINED = "unconstrained"
    PARTIALLY_CONSTRAINED = "partially_constrained"
    CONSTRAINED = "constrained"
    PARKED = "parked"


class DecisionAction(str, Enum):
    PASS = "pass"
    CONSIDER = "consider"
    STRONG_CONSIDER = "strong_consider"
    # Never EXECUTE — residual judgment stays with the user.


class StrategyMode(str, Enum):
    PROTECT_PROFITS = "protect_profits"
    PRESS_EDGES = "press_edges"
    STAY_SELECTIVE = "stay_selective"


class RiskPreference(str, Enum):
    CONSERVATIVE = "conservative"
    NORMAL = "normal"
    AGGRESSIVE = "aggressive"


class StrategyActionKind(str, Enum):
    HOLD = "hold"
    REDUCE = "reduce"
    EXIT = "exit"
    ADD = "add"
    REALLOCATE = "reallocate"
    NEW_BET = "new_bet"
    NO_ACTION = "no_action"
