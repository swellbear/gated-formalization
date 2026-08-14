"""Pydantic schemas for freeze/audit JSON and in-memory contracts."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field, field_validator

from golf_offshoot.models.enums import (
    BetType,
    CourseType,
    DataRole,
    DecisionAction,
    FactorStatus,
    Horizon,
    RunMode,
    SourceKind,
)
from golf_offshoot.models.strategy import StrategyRecommendation, UserStrategyDecision


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class DataQuality(BaseModel):
    """Every ingested input carries a quality score in [0, 1]."""

    score: float = Field(ge=0.0, le=1.0)
    role: DataRole = DataRole.PRIMARY
    source_name: str
    as_of: datetime
    n_observations: int = 0
    lag_hours: float = 0.0
    notes: str = ""
    missing: bool = False
    source_kind: SourceKind = SourceKind.UNSPECIFIED

    @field_validator("score")
    @classmethod
    def _clip(cls, v: float) -> float:
        return float(min(1.0, max(0.0, v)))


class Player(BaseModel):
    player_id: str
    name: str
    country: str | None = None
    owgr: int | None = None
    is_lesser_known: bool = False


class Course(BaseModel):
    course_id: str
    name: str
    course_type: CourseType
    par: int = 72
    yardage: int = 7200
    coastal: bool = False
    altitude_m: float = 0.0
    firmness: float = Field(default=0.5, ge=0.0, le=1.0)
    rough_severity: float = Field(default=0.5, ge=0.0, le=1.0)
    green_speed: float = Field(default=0.5, ge=0.0, le=1.0)
    tightness: float = Field(default=0.5, ge=0.0, le=1.0)
    wind_exposure: float = Field(default=0.5, ge=0.0, le=1.0)
    grass: str = "bent"
    venue_cluster_id: str | None = None


class Tournament(BaseModel):
    tournament_id: str
    name: str
    course: Course
    start_date: str
    tour: str = "PGA"
    n_rounds: int = 4
    cut_place: int = 65
    cut_after_round: int = 2
    has_cut: bool = True
    is_major: bool = False
    purse_usd: float | None = None
    espn_event_id: str | None = None


class SourceInventoryItem(BaseModel):
    """Provenance row for one important operating-path field."""

    field_name: str
    source_kind: SourceKind
    source_name: str
    quality_score: float | None = None
    coverage: str = ""
    notes: str = ""
    impact_if_missing: str = ""


class FreeParameterDef(BaseModel):
    factor_id: str
    name: str
    description: str
    family: str
    base_impact: float = Field(ge=0.0, le=1.0)
    base_constrainingability: float = Field(ge=0.0, le=1.0)
    course_multipliers: dict[str, float] = Field(default_factory=dict)
    correlated_with: list[str] = Field(default_factory=list)
    live_only: bool = False
    narrative_capped: bool = False
    start_broad: bool = True


class FreeParameterState(BaseModel):
    factor_id: str
    status: FactorStatus = FactorStatus.UNCONSTRAINED
    standardized_evidence: float = 0.0  # typically ~[-3, 3]
    quality: DataQuality | None = None
    n_obs: int = 0
    importance: float = 0.0  # impact * constrainingability after course type
    open_question: str = ""
    notes: str = ""


class EvidenceItem(BaseModel):
    factor_id: str
    player_id: str
    value_raw: float | None = None
    standardized: float = 0.0
    quality: DataQuality
    borrowed: bool = False
    borrow_source: str | None = None


class StrokesGainedProfile(BaseModel):
    ott: float = 0.0
    app: float = 0.0
    arg: float = 0.0
    putt: float = 0.0
    total: float = 0.0
    driving_distance_yd: float | None = None
    driving_accuracy_pct: float | None = None
    quality: DataQuality | None = None


class PlayerInputs(BaseModel):
    player: Player
    talent_prior: float = 0.0
    talent_prior_sd: float = 1.0
    sg: StrokesGainedProfile = Field(default_factory=StrokesGainedProfile)
    recent_sg: StrokesGainedProfile | None = None
    course_history_rounds: int = 0
    course_history_sg: float | None = None
    recent_form_sg: float | None = None
    short_term_trend: float | None = None
    weather_fit: float | None = None
    health_flag: float = 0.0  # negative = concern
    narrative_momentum: float = 0.0
    rest_days: int | None = None
    factors: dict[str, FreeParameterState] = Field(default_factory=dict)
    live_score_to_par: float | None = None
    live_holes_completed: int = 0
    live_place: int | None = None
    live_place_display: str = ""
    live_status_name: str = ""
    live_made_cut: bool | None = None
    withdrawn: bool = False
    source_qualities: dict[str, DataQuality] = Field(default_factory=dict)
    course_fit_signal: float | None = None


class FieldSnapshot(BaseModel):
    tournament_id: str
    as_of: datetime = Field(default_factory=_utcnow)
    mode: RunMode = RunMode.PRE_TOURNAMENT
    players: list[PlayerInputs]
    weather_summary: str = ""
    notes: str = ""
    inventory: list[SourceInventoryItem] = Field(default_factory=list)
    operating: bool = False
    extra: dict[str, Any] = Field(default_factory=dict)


class HorizonProbability(BaseModel):
    horizon: Horizon
    central: float = Field(ge=0.0, le=1.0)
    low: float = Field(ge=0.0, le=1.0)
    high: float = Field(ge=0.0, le=1.0)
    decomposition: dict[str, float] = Field(default_factory=dict)

    @field_validator("high")
    @classmethod
    def _hi(cls, v: float, info):
        return v


class ProbabilityBundle(BaseModel):
    player_id: str
    horizons: dict[Horizon, HorizonProbability]
    theta_mean: float
    theta_sd: float
    scenario_optimistic: dict[str, float] = Field(default_factory=dict)
    scenario_pessimistic: dict[str, float] = Field(default_factory=dict)

    def p(self, h: Horizon) -> HorizonProbability:
        return self.horizons[h]


class MarketQuote(BaseModel):
    player_id: str
    bet_type: BetType
    decimal_odds: float | None = None
    american_odds: int | None = None
    implied_raw: float | None = None
    implied_fair: float | None = None
    book: str = "consensus"
    as_of: datetime = Field(default_factory=_utcnow)
    line_role: str = "current"  # current | opening — opening never synthesized from winner


class MarketSnapshot(BaseModel):
    tournament_id: str
    as_of: datetime = Field(default_factory=_utcnow)
    quotes: list[MarketQuote]
    overround: dict[str, float] = Field(default_factory=dict)
    movement_vs_open: dict[str, float] = Field(default_factory=dict)


class ReliabilityScore(BaseModel):
    player_id: str
    score: float = Field(ge=0.0, le=1.0)
    data_density: float = Field(ge=0.0, le=1.0)
    data_quality: float = Field(ge=0.0, le=1.0)
    input_stability: float = Field(ge=0.0, le=1.0)
    reasons: list[str] = Field(default_factory=list)


class FactorContribution(BaseModel):
    factor_id: str
    delta_theta: float
    evidence: float
    quality: float
    importance: float
    status: FactorStatus


class ExplainabilityReport(BaseModel):
    player_id: str
    player_name: str
    theta_mean: float
    theta_sd: float
    prior_theta: float
    contributions: list[FactorContribution]
    open_questions: list[str]
    borrowed_strength: list[str] = Field(default_factory=list)
    field_interaction_note: str = ""
    narrative: str = ""


class PlayerOutput(BaseModel):
    player_id: str
    name: str
    rank: int
    probabilities: ProbabilityBundle
    reliability: ReliabilityScore
    edge_by_bet: dict[str, float] = Field(default_factory=dict)
    market_implied_by_bet: dict[str, float] = Field(default_factory=dict)
    posted_odds_by_bet: dict[str, float] = Field(default_factory=dict)
    open_questions: list[str] = Field(default_factory=list)
    flags: list[str] = Field(default_factory=list)
    explain: ExplainabilityReport | None = None
    decision: DecisionAdvice | None = None
    live_score_to_par: float | None = None
    live_holes_completed: int = 0
    live_place: int | None = None
    live_place_display: str = ""
    live_status_name: str = ""
    live_made_cut: bool | None = None
    withdrawn: bool = False


class DecisionAdvice(BaseModel):
    player_id: str
    bet_type: BetType
    action: DecisionAction
    model_p: float
    market_p: float | None = None
    edge: float | None = None
    range_width: float
    reliability: float
    suggested_kelly_fraction: float = 0.0
    portfolio_correlation_max: float | None = None
    reasons: list[str] = Field(default_factory=list)
    never_auto_bet: bool = True
    requires_user_confirmation: bool = True


class ComparableBorrow(BaseModel):
    player_id: str
    neighbor_ids: list[str]
    weights: list[float]
    shrinkage: float
    reason: str


class VenueCluster(BaseModel):
    cluster_id: str
    name: str
    course_ids: list[str]
    centroid: dict[str, float] = Field(default_factory=dict)


class ModelVersionRecord(BaseModel):
    version_id: str
    family: str
    weight_hash: str
    config_hash: str
    created_at: datetime = Field(default_factory=_utcnow)
    notes: str = ""


class HumanOverride(BaseModel):
    player_id: str
    factor_id: str | None = None
    horizon: Horizon | None = None
    delta_theta: float = 0.0
    reason: str
    operator: str
    at: datetime = Field(default_factory=_utcnow)


class BetRecord(BaseModel):
    player_id: str
    bet_type: BetType
    stake: float
    decimal_odds: float
    book: str
    placed_at: datetime = Field(default_factory=_utcnow)
    notes: str = ""
    placed_by_user: bool = True


class AuditRecord(BaseModel):
    run_id: str
    tournament_id: str
    mode: RunMode
    model: ModelVersionRecord
    data_snapshot_hash: str
    as_of: datetime = Field(default_factory=_utcnow)
    outputs: list[PlayerOutput]
    overrides: list[HumanOverride] = Field(default_factory=list)
    bets_placed: list[BetRecord] = Field(default_factory=list)
    previous_run_id: str | None = None
    delta_notes: list[str] = Field(default_factory=list)
    extra: dict[str, Any] = Field(default_factory=dict)
    strategy: StrategyRecommendation | None = None
    user_strategy_decisions: list[UserStrategyDecision] = Field(default_factory=list)


class TournamentRunResult(BaseModel):
    run_id: str
    tournament: Tournament
    mode: RunMode
    ranked: list[PlayerOutput]
    market: MarketSnapshot | None = None
    audit: AuditRecord
    warnings: list[str] = Field(default_factory=list)
    never_auto_bet: bool = True
    strategy: StrategyRecommendation | None = None
