"""Accumulating paper bankroll. Seed $500. Fees + settles. No daily reset."""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from golf_offshoot.arm_hub.paths import (
    PAPER_BANKROLL_OPEN,
    assert_not_learning_lane_path,
    ledger_path,
)
from golf_offshoot.localtime import now

FEE_K = 0.07


def ceil_cent(amount: float) -> float:
    return math.ceil(round(float(amount) * 100.0, 9)) / 100.0


def fee_usd(*, stake: float, yes_price: float, k: float = FEE_K) -> float:
    """Kalshi-like taker fee: ``ceil_cent(k * stake * (1 - p))``."""
    p = min(max(float(yes_price), 0.0), 1.0)
    return ceil_cent(float(k) * float(stake) * (1.0 - p))


def _iso(ts: datetime | None = None) -> str:
    stamp = ts or now()
    return stamp.isoformat()


@dataclass
class LedgerEntry:
    at: str
    kind: str
    amount: float
    bankroll_after: float
    ticker: str = ""
    rule_id: str = ""
    note: str = ""
    fee_usd: float = 0.0


@dataclass
class PaperLedger:
    bankroll: float = PAPER_BANKROLL_OPEN
    starting_bankroll: float = PAPER_BANKROLL_OPEN
    peak_bankroll: float = PAPER_BANKROLL_OPEN
    deposits: float = 0.0
    withdrawals: float = 0.0
    betting_pnl: float = 0.0
    fees_paid: float = 0.0
    entries: list[dict[str, Any]] = field(default_factory=list)
    daily_realized_pnl: dict[str, float] = field(default_factory=dict)
    never_daily_reset: bool = True
    paper_observation_only: bool = True
    trading_armed: bool = False

    def to_json(self) -> dict[str, Any]:
        return asdict(self)


def empty_ledger(open_bankroll: float = PAPER_BANKROLL_OPEN) -> PaperLedger:
    seed = float(open_bankroll)
    return PaperLedger(
        bankroll=seed,
        starting_bankroll=seed,
        peak_bankroll=seed,
    )


def load_ledger(root: Path | None = None) -> PaperLedger:
    path = ledger_path(root)
    assert_not_learning_lane_path(path)
    if not path.is_file():
        led = empty_ledger()
        save_ledger(led, root)
        return led
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"ledger must be an object: {path}")
    return PaperLedger(
        bankroll=float(raw.get("bankroll", PAPER_BANKROLL_OPEN)),
        starting_bankroll=float(raw.get("starting_bankroll", PAPER_BANKROLL_OPEN)),
        peak_bankroll=float(raw.get("peak_bankroll", raw.get("bankroll", PAPER_BANKROLL_OPEN))),
        deposits=float(raw.get("deposits", 0.0)),
        withdrawals=float(raw.get("withdrawals", 0.0)),
        betting_pnl=float(raw.get("betting_pnl", 0.0)),
        fees_paid=float(raw.get("fees_paid", 0.0)),
        entries=list(raw.get("entries") or []),
        daily_realized_pnl=dict(raw.get("daily_realized_pnl") or {}),
        never_daily_reset=bool(raw.get("never_daily_reset", True)),
        paper_observation_only=bool(raw.get("paper_observation_only", True)),
        trading_armed=bool(raw.get("trading_armed", False)),
    )


def save_ledger(ledger: PaperLedger, root: Path | None = None) -> Path:
    path = ledger_path(root)
    assert_not_learning_lane_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ledger.to_json(), indent=2) + "\n", encoding="utf-8")
    return path


def _append(ledger: PaperLedger, entry: LedgerEntry) -> None:
    ledger.entries.append(asdict(entry))
    if ledger.bankroll > ledger.peak_bankroll:
        ledger.peak_bankroll = ledger.bankroll


def apply_fill(
    ledger: PaperLedger,
    *,
    stake: float,
    fee: float,
    ticker: str,
    rule_id: str,
    note: str = "",
) -> PaperLedger:
    debit = ceil_cent(float(stake) + float(fee))
    ledger.bankroll = ceil_cent(ledger.bankroll - debit)
    ledger.fees_paid = ceil_cent(ledger.fees_paid + float(fee))
    _append(
        ledger,
        LedgerEntry(
            at=_iso(),
            kind="fill",
            amount=-debit,
            bankroll_after=ledger.bankroll,
            ticker=ticker,
            rule_id=rule_id,
            note=note or "paper fill (stake+fee)",
            fee_usd=float(fee),
        ),
    )
    return ledger


def apply_settle(
    ledger: PaperLedger,
    *,
    payout: float,
    stake: float,
    fee: float,
    ticker: str,
    rule_id: str,
    won: bool,
    day_key: str,
) -> PaperLedger:
    credit = ceil_cent(float(payout))
    pnl = ceil_cent(credit - float(stake) - float(fee))
    ledger.bankroll = ceil_cent(ledger.bankroll + credit)
    ledger.betting_pnl = ceil_cent(ledger.betting_pnl + pnl)
    # Daily kill is a brake on new risk, not a bankroll reset.
    ledger.daily_realized_pnl[day_key] = ceil_cent(
        float(ledger.daily_realized_pnl.get(day_key, 0.0)) + pnl
    )
    _append(
        ledger,
        LedgerEntry(
            at=_iso(),
            kind="settle",
            amount=credit,
            bankroll_after=ledger.bankroll,
            ticker=ticker,
            rule_id=rule_id,
            note=f"{'win' if won else 'lose'} pnl={pnl:.2f} (accumulate; no daily reset)",
            fee_usd=float(fee),
        ),
    )
    return ledger


def drawdown_pct(ledger: PaperLedger) -> float:
    peak = float(ledger.peak_bankroll) or 1.0
    return max(0.0, (peak - float(ledger.bankroll)) / peak)


def daily_pnl(ledger: PaperLedger, day_key: str) -> float:
    return float(ledger.daily_realized_pnl.get(day_key, 0.0))
