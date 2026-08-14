"""Schemas for the optional Decision / Strategy layer.

Suggestions only. Nothing here places a bet.
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field

from golf_offshoot.config import (
    STRATEGY_COOLING_OFF_DRAWDOWN_FRAC,
    STRATEGY_MAX_CUT_RISK_CONCENTRATION,
    STRATEGY_MAX_DAILY_LOSS_FRAC,
    STRATEGY_MAX_SINGLE_POSITION_FRAC,
    STRATEGY_MAX_STYLE_CLUSTER_FRAC,
    STRATEGY_MAX_TOTAL_EXPOSURE_FRAC,
)
from golf_offshoot.models.enums import (
    BetType,
    RiskPreference,
    RunMode,
    StrategyActionKind,
    StrategyMode,
)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def new_id(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:10]}"


class DrawdownControls(BaseModel):
    """Heat / exposure limits. Conservative defaults."""

    max_daily_loss_frac: float = STRATEGY_MAX_DAILY_LOSS_FRAC
    max_total_exposure_frac: float = STRATEGY_MAX_TOTAL_EXPOSURE_FRAC
    cooling_off_drawdown_frac: float = STRATEGY_COOLING_OFF_DRAWDOWN_FRAC
    max_single_position_frac: float = STRATEGY_MAX_SINGLE_POSITION_FRAC
    max_cut_risk_concentration: float = STRATEGY_MAX_CUT_RISK_CONCENTRATION
    max_style_cluster_frac: float = STRATEGY_MAX_STYLE_CLUSTER_FRAC


class StrategyConfig(BaseModel):
    """On/off plus bankroll, risk, mode, allowed bet types."""

    enabled: bool = False
    mode: StrategyMode = StrategyMode.STAY_SELECTIVE
    risk: RiskPreference = RiskPreference.CONSERVATIVE
    bankroll: float = 1000.0
    allowed_bet_types: list[BetType] = Field(
        default_factory=lambda: [
            BetType.WIN,
            BetType.TOP_5,
            BetType.TOP_10,
            BetType.TOP_20,
            BetType.MAKE_CUT,
        ]
    )
    controls: DrawdownControls = Field(default_factory=DrawdownControls)
    never_auto_bet: bool = True


class StrategyPosition(BaseModel):
    """A user-recorded open (or proposed) stake. The system never books this."""

    position_id: str
    player_id: str
    player_name: str = ""
    bet_type: BetType
    stake: float
    decimal_odds: float
    entry_edge: float
    entry_model_p: float
    entry_market_p: float | None = None
    entered_at: datetime = Field(default_factory=_utcnow)
    round_entered: int = 0
    notes: str = ""
    user_recorded: bool = True
    proposed: bool = False


class PortfolioState(BaseModel):
    bankroll: float
    positions: list[StrategyPosition] = Field(default_factory=list)
    realized_pnl_today: float = 0.0
    realized_pnl_event: float = 0.0
    session_label: str = ""

    @property
    def open_exposure(self) -> float:
        return float(sum(p.stake for p in self.positions if p.stake > 0))


class PositionMark(BaseModel):
    """Original vs live edge, mark-to-market, path flags."""

    position_id: str
    player_id: str
    bet_type: BetType
    entry_edge: float
    live_edge: float | None
    entry_model_p: float
    live_model_p: float
    entry_market_p: float | None
    live_market_p: float | None
    live_decimal_odds: float | None
    stake: float
    mtm_value: float
    unrealized_pnl: float
    original_edge_collapsed: bool
    live_edge_improved: bool
    is_runner: bool
    range_width: float
    reliability: float


class ConcentrationSlice(BaseModel):
    axis: str
    label: str
    exposure: float
    fraction_of_book: float
    player_ids: list[str] = Field(default_factory=list)


class StrategyAction(BaseModel):
    action_id: str
    kind: StrategyActionKind
    player_id: str
    player_name: str = ""
    bet_type: BetType
    position_id: str | None = None
    suggested_stake_delta: float = 0.0
    suggested_unit: float = 0.0
    from_position_id: str | None = None
    to_player_id: str | None = None
    reason: str
    reasons_detail: list[str] = Field(default_factory=list)
    uncertainty_warning: str | None = None
    never_auto_bet: bool = True
    requires_user_confirmation: bool = True


class StrategyStatusSummary(BaseModel):
    open_exposure: float
    exposure_frac: float
    unrealized_pnl: float
    unrealized_edge_weighted: float
    biggest_concentration: str
    biggest_concentration_frac: float
    posture: StrategyMode
    cooling_off: bool
    n_positions: int
    n_suggested_actions: int
    layer_enabled: bool = True


class StrategyRecommendation(BaseModel):
    recommendation_id: str
    as_of: datetime = Field(default_factory=_utcnow)
    mode: StrategyMode
    run_mode: RunMode
    actions: list[StrategyAction] = Field(default_factory=list)
    proposed_new_positions: list[StrategyPosition] = Field(default_factory=list)
    marks: list[PositionMark] = Field(default_factory=list)
    concentrations: list[ConcentrationSlice] = Field(default_factory=list)
    status: StrategyStatusSummary
    cooling_off: bool = False
    enabled: bool = True
    never_auto_bet: bool = True
    notes: list[str] = Field(default_factory=list)


class UserStrategyDecision(BaseModel):
    """What the user actually did with a suggestion. Logged; not executed by us."""

    decision_id: str = Field(default_factory=lambda: new_id("usd"))
    recommendation_id: str
    action_id: str | None = None
    accepted: bool
    modified_stake: float | None = None
    note: str = ""
    operator: str = ""
    at: datetime = Field(default_factory=_utcnow)
    placed_by_user: bool = True
