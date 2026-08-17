"""Pydantic schemas. Paper/mock only. Never auto-trades."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, Field

from options_offshoot.config import DEFAULT_MULTIPLIER
from options_offshoot.localtime import now
from options_offshoot.models.enums import (
    AdviceKind,
    ComparePath,
    ContractType,
    QuoteVenue,
    RunMode,
    SourceKind,
)


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
    venue: QuoteVenue = QuoteVenue.POLYGON

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

    @property
    def has_real_bid(self) -> bool:
        return self.bid is not None and self.bid > 0


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
    shares_per_contract: int | None = None
    multiplier_defaulted: bool = False
    listed_iv: float | None = None
    ibkr_con_id: int | None = None
    opening_ask: float | None = None
    quote_venue: QuoteVenue = QuoteVenue.POLYGON
    nonstandard_deliverable: bool = False

    @property
    def multiplier(self) -> int:
        if self.shares_per_contract is not None and self.shares_per_contract > 0:
            return int(self.shares_per_contract)
        return int(DEFAULT_MULTIPLIER)


class ModelView(BaseModel):
    fair: float | None = None
    p_itm: float | None = None
    p_itm_low: float | None = None
    p_itm_high: float | None = None
    reliability: float = 0.0
    honest: bool = False
    sigma_used: float | None = None
    unconstrained_vol: bool = False
    default_sigma: bool = False


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
    n_contracts: int = 0
    multiplier: int = DEFAULT_MULTIPLIER
    entry_ask: float | None = None
    opening_ask: float | None = None
    entry_fair: float | None = None
    quote_venue: QuoteVenue = QuoteVenue.POLYGON
    locked_at: datetime = Field(default_factory=now)
    settled: bool = False
    settle_pnl: float | None = None


class PaperMovement(BaseModel):
    kind: AdviceKind
    contract_id: str
    underlying: str
    amount: float = 0.0
    n_contracts: int = 0
    reason: str = ""
    from_contract_id: str = ""
    unmarked: bool = False


class PaperLedgerLine(BaseModel):
    kind: str
    amount: float
    note: str = ""
    at: datetime = Field(default_factory=now)


class PaperBookFile(BaseModel):
    field_id: str
    path_id: ComparePath
    event_name: str = ""
    locked_at: datetime | None = None
    locked_from_run_id: str = ""
    lock_identity: str = ""
    bankroll: float = 20000.0
    cash: float = 20000.0
    starting_bankroll: float = 20000.0
    never_auto_trade: bool = True
    quote_venue_pin: QuoteVenue = QuoteVenue.POLYGON
    positions: list[PaperPosition] = Field(default_factory=list)
    last_advice: list[PaperMovement] = Field(default_factory=list)
    last_advice_sig: str = ""
    method_law_hash: str = ""
    notes: list[str] = Field(default_factory=list)
    ledger: list[PaperLedgerLine] = Field(default_factory=list)
    realized_pnl: float = 0.0
    posted_ask_pnl: float | None = None
    expiry_settle_pnl: float | None = None
