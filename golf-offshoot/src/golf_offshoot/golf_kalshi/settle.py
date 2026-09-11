"""Settle SoT is Kalshi result. ESPN finish is not enough."""

from __future__ import annotations

import json
from typing import Any

from golf_offshoot.data_feeds.kalshi_15m import parse_kalshi_result
from golf_offshoot.golf_kalshi.fees import fee_adjust, series_k
from golf_offshoot.golf_kalshi.paper import apply_close, load_ledger, replace_ticket, save_ledger
from golf_offshoot.golf_kalshi.paths import assert_golf_kalshi_path, safe_artifact_stem, settlements_dir
from golf_offshoot.localtime import isoformat_now

LANE = "golf_kalshi"


class SettleError(ValueError):
    """Refused an unofficial settle."""


def apply_kalshi_result(
    ticket: dict[str, Any],
    *,
    kalshi_result: str,
    espn_finish: Any = None,
) -> dict[str, Any]:
    token = parse_kalshi_result(kalshi_result)
    if not token:
        if espn_finish is not None:
            raise SettleError("settle SoT is Kalshi result; ESPN finish is not enough")
        out = dict(ticket)
        out["status"] = "SETTLE_PENDING"
        return out
    stake = float(ticket.get("stake") or 0)
    yes_ask = float(ticket.get("yes_ask") or (ticket.get("quote") or {}).get("yes_ask") or 0)
    if token == "yes":
        recorded = (stake / yes_ask) - stake if yes_ask else 0.0
        status = "paper_win"
    elif token == "no":
        recorded = -stake
        status = "paper_lose"
    else:
        recorded = 0.0
        status = "void"
    k = series_k((ticket.get("quote") or {}).get("fee_multiplier") if ticket.get("quote") else ticket.get("fee_multiplier"))
    pnl = fee_adjust(recorded, yes_ask, stake, k=k) if k is not None else recorded
    out = dict(ticket)
    out["status"] = status
    out["kalshi_result"] = token
    out["settled_at"] = isoformat_now()
    out["recorded_pnl"] = round(recorded, 4)
    out["pnl_after_fee"] = round(float(pnl), 4)
    return out


def write_settlement(ticket: dict[str, Any]) -> None:
    ticker = str(ticket.get("ticker") or "market")
    path = settlements_dir() / f"{safe_artifact_stem(ticker)}.json"
    assert_golf_kalshi_path(path)
    payload = {"lane": LANE, "ticket": ticket}
    path.write_text(json.dumps(payload, indent=2, default=str) + "\n", encoding="utf-8")


def join_settles(catalog_markets: list[dict[str, Any]]) -> dict[str, Any]:
    """Apply official Kalshi results. Always runs even when the fill budget is spent."""
    led = load_ledger()
    by_ticker = {str(m.get("ticker") or ""): m for m in catalog_markets}
    joined = 0
    pending = 0
    for ticket in list(led.get("tickets") or []):
        if str(ticket.get("status") or "") not in {"open", "SETTLE_PENDING"}:
            continue
        market = by_ticker.get(str(ticket.get("ticker") or ""))
        result = str((market or {}).get("result") or "")
        try:
            updated = apply_kalshi_result(ticket, kalshi_result=result)
        except SettleError:
            pending += 1
            continue
        if updated.get("status") == "SETTLE_PENDING":
            pending += 1
            replace_ticket(led, str(ticket.get("ticker") or ""), updated)
            led = load_ledger()
            continue
        apply_close(led, updated)
        led = load_ledger()
        led = load_ledger()
        write_settlement(updated)
        joined += 1
    save_ledger(led)
    return {"joined": joined, "pending": pending, "ledger": led}
