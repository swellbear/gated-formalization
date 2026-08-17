"""Expiry settle. Stake = premium dollars. n = floor(stake / (entry_ask * multiplier))."""

from __future__ import annotations

from datetime import date

from options_offshoot.data_feeds.polygon import PolygonClient
from options_offshoot.localtime import now
from options_offshoot.models.enums import ContractType
from options_offshoot.models.schemas import PaperBookFile, PaperPosition
from options_offshoot.strategy.paper_book import mark_scores, save_paper_book


def intrinsic(spot: float, pos: PaperPosition) -> float:
    if pos.contract_type == ContractType.CALL:
        return max(0.0, float(spot) - float(pos.strike))
    return max(0.0, float(pos.strike) - float(spot))


def settle_position(pos: PaperPosition, spot: float) -> float:
    n = int(pos.n_contracts or 0)
    if n <= 0 and pos.entry_ask and pos.entry_ask > 0:
        n = int(pos.stake // (pos.entry_ask * pos.multiplier))
        pos.n_contracts = n
    value = intrinsic(spot, pos) * int(pos.multiplier) * n
    return float(value) - float(pos.stake)


def maybe_auto_settle(
    record: PaperBookFile,
    *,
    today: date | None = None,
    closes: dict[str, float] | None = None,
    client: PolygonClient | None = None,
    require_close: bool = False,
) -> PaperBookFile:
    """Settle when expiry date has passed AND an official close exists.

    paper-settle sets require_close=True and errors if a close is missing.
    """
    day = today or now().date()
    missing: list[str] = []
    px = dict(closes or {})
    cli = client
    changed = False
    for pos in record.positions:
        if pos.settled:
            continue
        if pos.expiry >= day:
            continue
        key = pos.underlying
        spot = px.get(key)
        if spot is None:
            try:
                if cli is None:
                    cli = PolygonClient()
                spot = cli.session_close(pos.underlying, pos.expiry)
            except Exception:
                spot = None
            if spot is not None:
                px[key] = spot
        if spot is None or pos.entry_ask is None:
            missing.append(f"{pos.contract_id} close/entry_ask missing; left open")
            continue
        pnl = settle_position(pos, float(spot))
        pos.settled = True
        pos.settle_pnl = pnl
        record.cash += float(spot and (intrinsic(float(spot), pos) * pos.multiplier * pos.n_contracts) or 0.0)
        record.realized_pnl += pnl
        changed = True
    if require_close and missing:
        raise RuntimeError("paper-settle: " + "; ".join(missing))
    if changed:
        record.notes.extend(missing)
        record.bankroll = record.cash + sum(p.stake for p in record.positions if not p.settled)
        mark_scores(record, None)
        save_paper_book(record)
    elif missing and require_close:
        raise RuntimeError("paper-settle: " + "; ".join(missing))
    return record
