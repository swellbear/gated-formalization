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
    WIN_AFTER_R1 = "win_after_r1"
    WIN_AFTER_R2 = "win_after_r2"
    WIN_AFTER_R3 = "win_after_r3"


class BetType(str, Enum):
    WIN = "win"
    TOP_5 = "top_5"
    TOP_10 = "top_10"
    TOP_20 = "top_20"
    MAKE_CUT = "make_cut"
    WIN_AFTER_R1 = "win_after_r1"
    WIN_AFTER_R2 = "win_after_r2"
    WIN_AFTER_R3 = "win_after_r3"


ROUND_LEADER_BETS = (BetType.WIN_AFTER_R1, BetType.WIN_AFTER_R2, BetType.WIN_AFTER_R3)
ROUND_LEADER_HORIZONS = (
    Horizon.WIN_AFTER_R1,
    Horizon.WIN_AFTER_R2,
    Horizon.WIN_AFTER_R3,
)


def horizon_for(bet: BetType | str) -> Horizon | None:
    """BetType and Horizon share values. Unknown labels stay unmapped."""
    key = bet.value if isinstance(bet, BetType) else str(bet or "")
    try:
        return Horizon(key)
    except ValueError:
        return None


def is_round_leader_bet(bet: BetType | str) -> bool:
    key = bet.value if isinstance(bet, BetType) else str(bet or "").lower()
    return key in {b.value for b in ROUND_LEADER_BETS}


class RunMode(str, Enum):
    PRE_TOURNAMENT = "pre_tournament"
    LIVE = "live"


class DataRole(str, Enum):
    PRIMARY = "primary"
    FALLBACK = "fallback"
    MOCK = "mock"
    MANUAL = "manual"


class SourceKind(str, Enum):
    """Provenance label for every important ingested field.

    MOCK is allowed only in unit tests and explicitly labeled offline demos.
    The operating path may never emit MOCK, and must not relabel mocks as live.
    """

    REAL_LIVE = "real_live"
    REAL_HISTORICAL = "real_historical"
    DERIVED_FROM_REAL = "derived_from_real"
    UNAVAILABLE = "unavailable"
    MOCK = "mock"
    UNSPECIFIED = "unspecified"  # legacy test helpers only


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
