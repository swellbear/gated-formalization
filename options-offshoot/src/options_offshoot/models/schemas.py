"""Pydantic schemas. Paper/mock only. Never auto-trades."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, Field

from options_offshoot.localtime import now
from options_offshoot.models.enums import AdviceKind, ComparePath, ContractType, RunMode, SourceKind


class DataQuality(BaseModel):
    score: float = 0.0
    source_kind: SourceKind = SourceKind.UNAVAILABLE
    source: str = ""
    missing: bool = True
    notes: str = ""
    n: int = 0


class SourceInventoryItem(BaseModel):
    name: str
    quality: DataQuality
    used: bool = False
    impact: str = ""


class Quote(BaseModel):
    bid: float | None = None
    ask: float | None = None
    last: float | None = None
    open_interest: int | None = None
    volume: int | None = None
    as_of: datetime = Field(default_factory=now)

    @property
    def mid(self) -> float | None:
        if self.bid is None or self.ask is None:
            return None
        if self.bid <= 0 or self.ask <= 0 or self.ask < self.bid:
            return None
        return 0.5 * (self.bid + self.ask)

    @property
    def spread_rel(self) -> float | None:
        m = self.mid
        if m is None or m <= 0 or self.bid is None or self.ask is None:
            return None
        return (self.ask - self.bid) / m

    @property
    def has_real_ask(self) -> bool:
        return self.ask is not None and self.ask > 0


class Contract(BaseModel):
    contract_id: str
    underlying: str
    expiry: date
    strike: float
    contract_type: ContractType
    quote: Quote = Field(default_factory=Quote)
    spot: float | None = None
    realized_vol: float | None = None
    years_to_expiry: float | None = None
    liquid: bool = False
    notes: str = ""


class ModelView(BaseModel):
    fair: float | None = None
    p_itm: float | None = None
    p_itm_low: float | None = None
    p_itm_high: float | None = None
    reliability: float = 0.0
    honest: bool = False
    sigma_used: float | None = None
    unconstrained_vol: bool = False


class RankedContract(BaseModel):
    contract: Contract
    model: ModelView
    vs_ask: float | None = None
    vs_mid: float | None = None
    clears_ask: bool = False
    clears_mid: bool = False
    n_a_reason: str | None = None

    @property
    def sort_vs_ask(self) -> float:
        if self.vs_ask is None:
            return float("-inf")
        return float(self.vs_ask)


class FieldRun(BaseModel):
    field_id: str
    run_id: str
    mode: RunMode
    as_of: datetime = Field(default_factory=now)
    honest: bool = False
    operating: bool = False
    underlyings: list[str] = Field(default_factory=list)
    rows: list[RankedContract] = Field(default_factory=list)
    inventory: list[SourceInventoryItem] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    extra: dict[str, Any] = Field(default_factory=dict)


class PaperPosition(BaseModel):
    position_id: str
    contract_id: str
    underlying: str
    expiry: date
    strike: float
    contract_type: ContractType
    stake: float
    entry_ask: float | None = None
    entry_fair: float | None = None
    locked_at: datetime = Field(default_factory=now)


class PaperMovement(BaseModel):
    kind: AdviceKind
    contract_id: str
    underlying: str
    amount: float = 0.0
    reason: str = ""


class PaperBookFile(BaseModel):
    field_id: str
    path_id: ComparePath
    event_name: str = ""
    locked_at: datetime | None = None
    locked_from_run_id: str = ""
    bankroll: float = 20000.0
    cash: float = 20000.0
    starting_bankroll: float = 20000.0
    never_auto_trade: bool = True
    positions: list[PaperPosition] = Field(default_factory=list)
    last_advice: list[PaperMovement] = Field(default_factory=list)
    method_law_hash: str = ""
    notes: list[str] = Field(default_factory=list)
