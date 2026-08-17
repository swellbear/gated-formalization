"""IBKR venue ask overlay. Market data only. Never placeOrder."""

from __future__ import annotations

import os
from datetime import date
from typing import Any

from options_offshoot.config import (
    IBKR_CLIENT_ID_DEFAULT,
    IBKR_HOST_DEFAULT,
    IBKR_PORT_DEFAULT,
)
from options_offshoot.models.enums import ContractType, QuoteVenue
from options_offshoot.models.schemas import Contract

# Tests and leftover scan this module. Do not add an order API.
IBKR_MARKET_DATA_ONLY = True
PLACE_ORDER_FORBIDDEN = True


class IbkrUnavailable(RuntimeError):
    pass


def ibkr_settings() -> dict[str, Any]:
    return {
        "host": os.environ.get("IBKR_HOST", IBKR_HOST_DEFAULT).strip() or IBKR_HOST_DEFAULT,
        "port": int(os.environ.get("IBKR_PORT", str(IBKR_PORT_DEFAULT))),
        "client_id": int(os.environ.get("IBKR_CLIENT_ID", str(IBKR_CLIENT_ID_DEFAULT))),
    }


def occ_match(
    contract: Contract,
    *,
    symbol: str,
    expiry: date,
    strike: float,
    right: str,
) -> bool:
    side = "P" if contract.contract_type == ContractType.PUT else "C"
    want = str(right or "").strip().upper()[:1]
    return (
        contract.underlying.upper() == str(symbol).strip().upper()
        and contract.expiry == expiry
        and abs(float(contract.strike) - float(strike)) < 1e-6
        and side == want
    )


def apply_ibkr_quote(
    contract: Contract,
    *,
    bid: float | None,
    ask: float | None,
    con_id: int | None = None,
    delayed: bool = False,
) -> Contract:
    """Overlay venue bid/ask. Never copies Polygon last_quote under an IBKR label."""
    q = contract.quote.model_copy()
    q.bid = bid
    q.ask = ask
    q.venue = QuoteVenue.IBKR
    contract.quote = q
    contract.quote_venue = QuoteVenue.IBKR
    if con_id is not None:
        contract.ibkr_con_id = int(con_id)
    if delayed:
        note = "IBKR delayed-only; leftover, not live venue ask"
        contract.notes = f"{contract.notes}; {note}".strip("; ")
        q.bid = None
        q.ask = None
        contract.quote_venue = QuoteVenue.UNAVAILABLE
        q.venue = QuoteVenue.UNAVAILABLE
        contract.quote = q
    return contract


def fetch_ibkr_quotes(
    contracts: list[Contract],
    *,
    timeout: float = 8.0,
) -> tuple[dict[str, dict[str, Any]], list[str]]:
    """Return {contract_id: {bid, ask, con_id, delayed}} plus leftover notes.

    Optional ib_insync. Tests mock this. Never calls placeOrder.
    """
    notes: list[str] = []
    if not contracts:
        return {}, ["ibkr: no contracts"]
    try:
        from ib_insync import IB, Option  # type: ignore
    except Exception:
        return {}, ["ibkr: ib_insync not installed; venue ask unavailable"]

    cfg = ibkr_settings()
    ib = IB()
    try:
        ib.connect(cfg["host"], cfg["port"], clientId=cfg["client_id"], timeout=timeout)
    except Exception as exc:
        return {}, [f"ibkr: handshake fail ({exc}); venue ask unavailable"]

    out: dict[str, dict[str, Any]] = {}
    delayed_any = False
    unmatched = 0
    try:
        try:
            ib.reqMarketDataType(1)
        except Exception:
            pass
        for contract in contracts:
            right = "P" if contract.contract_type == ContractType.PUT else "C"
            spec = Option(
                contract.underlying,
                contract.expiry.strftime("%Y%m%d"),
                float(contract.strike),
                right,
                "SMART",
                currency="USD",
            )
            try:
                qualified = ib.qualifyContracts(spec)
            except Exception:
                unmatched += 1
                notes.append(
                    f"ibkr: unmatched conId {contract.underlying} "
                    f"{contract.expiry} {contract.strike}{right}"
                )
                continue
            if not qualified:
                unmatched += 1
                notes.append(
                    f"ibkr: unmatched conId {contract.underlying} "
                    f"{contract.expiry} {contract.strike}{right}"
                )
                continue
            qed = qualified[0]
            if not occ_match(
                contract,
                symbol=str(getattr(qed, "symbol", contract.underlying)),
                expiry=contract.expiry,
                strike=float(getattr(qed, "strike", contract.strike)),
                right=str(getattr(qed, "right", right)),
            ):
                unmatched += 1
                notes.append(
                    f"ibkr: conId mismatch, not filling neighbor {contract.contract_id}"
                )
                continue
            ticker = ib.reqMktData(qed, "", snapshot=True, regulatorySnapshot=False)
            ib.sleep(0.35)
            bid = _px(getattr(ticker, "bid", None))
            ask = _px(getattr(ticker, "ask", None))
            delayed = bool(getattr(ticker, "marketDataType", 1) not in (1, None, 0))
            if delayed:
                delayed_any = True
            out[contract.contract_id] = {
                "bid": bid,
                "ask": ask,
                "con_id": int(getattr(qed, "conId", 0) or 0) or None,
                "delayed": delayed,
            }
            try:
                ib.cancelMktData(qed)
            except Exception:
                pass
    finally:
        try:
            ib.disconnect()
        except Exception:
            pass
    if delayed_any:
        notes.append("ibkr: delayed-only (no OPRA live); venue ask unavailable")
    if unmatched:
        notes.append(f"ibkr: unmatched {unmatched} contracts; no neighbor fill")
    if not out and not notes:
        notes.append("ibkr: no quotes")
    return out, notes


def overlay_ibkr(
    contracts: list[Contract],
    quotes: dict[str, dict[str, Any]] | None = None,
    *,
    live_fetch: bool = False,
) -> tuple[list[Contract], list[str]]:
    notes: list[str] = []
    fetched = quotes
    if fetched is None and live_fetch:
        fetched, notes = fetch_ibkr_quotes(contracts)
    fetched = fetched or {}
    if not fetched:
        if not notes:
            notes.append("ibkr: venue ask unavailable")
        return contracts, notes
    out = []
    for c in contracts:
        row = fetched.get(c.contract_id)
        if not row:
            out.append(c)
            continue
        out.append(
            apply_ibkr_quote(
                c,
                bid=row.get("bid"),
                ask=row.get("ask"),
                con_id=row.get("con_id"),
                delayed=bool(row.get("delayed")),
            )
        )
    return out, notes


def _px(value: Any) -> float | None:
    try:
        if value is None:
            return None
        px = float(value)
        if px <= 0 or px != px or px > 1e8:
            return None
        return px
    except (TypeError, ValueError):
        return None
