"""Whole-lot sizing. Frozen law. Not Kelly. Never a ticket."""

from __future__ import annotations

from options_offshoot.compare.law import METHOD_LAW_V1
from options_offshoot.config import DEFAULT_MULTIPLIER
from options_offshoot.models.schemas import PaperBookFile, RankedContract


def haircut() -> float:
    return float(METHOD_LAW_V1["conservative_haircut"])


def single_cap(bankroll: float) -> float:
    return float(bankroll) * float(METHOD_LAW_V1["max_single_position_frac"]) * haircut()


def same_underlying_cap(bankroll: float) -> float:
    return float(bankroll) * float(METHOD_LAW_V1["max_same_underlying_frac"]) * haircut()


def total_cap(bankroll: float) -> float:
    return float(bankroll) * float(METHOD_LAW_V1["max_total_exposure_frac"]) * haircut()


def lot_cost(ask: float | None, multiplier: int | None) -> float | None:
    if ask is None or ask <= 0:
        return None
    m = int(multiplier or DEFAULT_MULTIPLIER)
    if m <= 0:
        return None
    return float(ask) * m


def exposure_by_underlying(book: PaperBookFile | None) -> dict[str, float]:
    out: dict[str, float] = {}
    if book is None:
        return out
    for p in book.positions:
        if p.settled:
            continue
        out[p.underlying] = out.get(p.underlying, 0.0) + float(p.stake)
    return out


def open_exposure(book: PaperBookFile | None) -> float:
    if book is None:
        return 0.0
    return sum(p.stake for p in book.positions if not p.settled)


def size_new(
    row: RankedContract,
    book: PaperBookFile | None,
    *,
    bankroll: float,
    cash: float,
    leftover: list[str] | None = None,
) -> tuple[int, float, str | None]:
    """Return (n_contracts, stake, block_reason). n is whole lots only."""
    ask = row.contract.quote.ask
    cost = lot_cost(ask, row.contract.multiplier)
    notes = leftover if leftover is not None else []
    if cost is None:
        return 0, 0.0, "no venue ask"
    cap_single = single_cap(bankroll)
    cap_und = same_underlying_cap(bankroll)
    cap_tot = total_cap(bankroll)
    used_und = exposure_by_underlying(book).get(row.contract.underlying, 0.0)
    used_tot = open_exposure(book)
    room = min(cash, cap_single, cap_und - used_und, cap_tot - used_tot)
    if room < cost:
        notes.append(
            f"can't size {row.contract.underlying} {row.contract.contract_id}: "
            f"one lot ${cost:.2f} exceeds remaining cap/cash ${room:.2f}"
        )
        return 0, 0.0, "can't size"
    n = int(room // cost)
    if n < 1:
        notes.append(f"can't size {row.contract.contract_id}: residual below one lot")
        return 0, 0.0, "can't size"
    stake = n * cost
    return n, stake, None
