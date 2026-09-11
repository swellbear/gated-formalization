"""Paper now. Live orders only if TRADING_ARMED + keys. Hub never grows cash buttons."""

from __future__ import annotations

from typing import Any, Protocol

from golf_offshoot.golf_kalshi.decide import GolfDecision
from golf_offshoot.golf_kalshi.paper import append_ticket, load_ledger, open_ticket_for
from golf_offshoot.golf_kalshi.paths import trading_is_armed
from golf_offshoot.golf_kalshi.recipe import LIVE_SCALE, LIVE_SCALE_UNTIL_N, recipe_v1
from golf_offshoot.localtime import isoformat_now


class UnarmedError(RuntimeError):
    """Live path refused: no TRADING_ARMED file and/or no keys."""


class OrderTransport(Protocol):
    def place_order(self, payload: dict[str, Any]) -> dict[str, Any]: ...


class RecordingTransport:
    """Tests only. Never a live Kalshi session."""

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def place_order(self, payload: dict[str, Any]) -> dict[str, Any]:
        self.calls.append(payload)
        return {"order_id": f"fake-{len(self.calls)}", "payload": payload}


def live_scale_for(ledger: dict[str, Any]) -> float:
    n = int(ledger.get("lived_fills_settled") or 0)
    if n >= LIVE_SCALE_UNTIL_N:
        return 1.0
    return LIVE_SCALE


def ticket_from_decision(decision: GolfDecision, *, backend: str, lived: bool = False) -> dict[str, Any]:
    rec = recipe_v1()
    return {
        "ticker": decision.ticker,
        "player_id": decision.player_id,
        "player": decision.player_name,
        "sleeve": decision.sleeve,
        "stake": decision.stake,
        "yes_ask": decision.yes_ask,
        "fee": decision.fee,
        "edge_after_fee": decision.edge_after_fee,
        "model_p": decision.model_p,
        "status": "open",
        "quote": decision.quote,
        "backend": backend,
        "lived": lived,
        "decision_at": (decision.quote or {}).get("declared_at") or isoformat_now(),
        "series_ticker": str((decision.market or {}).get("series_ticker") or ""),
        "event_ticker": str((decision.market or {}).get("event_ticker") or ""),
        "title": str((decision.market or {}).get("title") or ""),
        "field_source": decision.field_source or str((decision.market or {}).get("field_source") or ""),
        "recipe_id": rec.recipe_id,
        "tour_haircut": decision.tour_haircut,
    }


class PaperExecutor:
    def book(self, decision: GolfDecision) -> dict[str, Any] | None:
        if not decision.fill:
            return None
        led = load_ledger()
        if open_ticket_for(led, decision.ticker):
            return open_ticket_for(led, decision.ticker)
        ticket = ticket_from_decision(decision, backend="paper", lived=False)
        append_ticket(led, ticket)
        return ticket


class LiveExecutor:
    """Same decide intent. Hits /orders only through an injected transport when armed."""

    def __init__(self, transport: OrderTransport | None = None) -> None:
        self.transport = transport

    def book(self, decision: GolfDecision) -> dict[str, Any] | None:
        if not decision.fill:
            return None
        if not trading_is_armed():
            raise UnarmedError("TRADING_ARMED file is absent")
        if self.transport is None:
            raise UnarmedError("no live transport; unarmed default never calls /orders")
        payload = {
            "ticker": decision.ticker,
            "side": "yes",
            "stake": round(float(decision.stake), 2),
            "yes_ask": decision.yes_ask,
            "displayed_size": (decision.quote or {}).get("displayed_size"),
        }
        displayed = payload.get("displayed_size")
        if displayed is not None and decision.yes_ask:
            try:
                cap = float(displayed) * float(decision.yes_ask or 0)
                payload["stake"] = min(float(payload["stake"]), cap)
            except (TypeError, ValueError):
                pass
        placed = self.transport.place_order(payload)
        ticket = ticket_from_decision(decision, backend="live", lived=True)
        ticket["stake"] = payload["stake"]
        ticket["live_order"] = placed
        append_ticket(load_ledger(), ticket)
        return ticket


def executor_for(*, armed: bool | None = None, transport: OrderTransport | None = None) -> PaperExecutor | LiveExecutor:
    if armed is None:
        armed = trading_is_armed()
    if armed:
        return LiveExecutor(transport=transport)
    return PaperExecutor()
