"""Screen-then-allocate. Size 0.25 Kelly inside sleeve shares. Never rank the whole book by pnl."""

from __future__ import annotations

from typing import Any

from golf_offshoot.golf_kalshi.decide import GolfDecision
from golf_offshoot.golf_kalshi.fees import edge_after_fee, kelly_stake, quote_snapshot, taker_fee
from golf_offshoot.golf_kalshi.paper import (
    exposure_player,
    exposure_sleeve,
    exposure_total,
    open_event_count,
    open_ticket_for,
    rebuy_blocked,
)
from golf_offshoot.golf_kalshi.recipe import WalletRecipe, recipe_v1
from golf_offshoot.localtime import isoformat_now


def rec_seed(recipe: WalletRecipe, ledger: dict[str, Any]) -> float:
    return float(ledger.get("bankroll") or recipe.seed)


def week_overweight(ledger: dict[str, Any], recipe: WalletRecipe) -> bool:
    bank = rec_seed(recipe, ledger)
    return exposure_sleeve(ledger, "week") > recipe.sleeve_target("week", bank) + 1e-9


def sleeve_room(ledger: dict[str, Any], recipe: WalletRecipe, sleeve: str) -> float:
    bank = rec_seed(recipe, ledger)
    target = recipe.sleeve_target(sleeve, bank)
    used = exposure_sleeve(ledger, sleeve)
    room = float(target - used)
    if room <= 0:
        return room
    total_left = recipe.total_cap(bank) - exposure_total(ledger)
    if total_left >= room:
        return room
    # Total is at/over the 20% cap. Catch-up into empty sleeves only while week is overweight.
    if sleeve != "week" and week_overweight(ledger, recipe):
        return room
    return min(room, max(0.0, float(total_left)))


def displayed_room(market: dict[str, Any], yes_ask: float) -> float | None:
    displayed = market.get("displayed_size")
    if displayed is None:
        return None
    try:
        liq = float(displayed) * float(yes_ask)
    except (TypeError, ValueError):
        return None
    return liq if liq > 0 else None


def attach_stake(
    decision: GolfDecision,
    ledger: dict[str, Any],
    recipe: WalletRecipe | None = None,
    *,
    live_scale: float = 1.0,
) -> GolfDecision:
    rec = recipe or recipe_v1()
    if not decision.worthy or decision.model_p is None or decision.yes_ask is None:
        return decision
    if open_ticket_for(ledger, decision.ticker) is not None:
        decision.action = "skip"
        decision.reason = "already_open"
        decision.stake = 0.0
        return decision
    if rebuy_blocked(ledger, decision.ticker, decision.edge_after_fee, rec):
        decision.action = "skip"
        decision.reason = "mix_rebuy_blocked"
        decision.stake = 0.0
        return decision
    bank = rec_seed(rec, ledger)
    pid = str(decision.player_id or "")
    name_room = rec.single_name_frac * bank - exposure_player(ledger, pid)
    if name_room <= 0:
        decision.action = "skip"
        decision.reason = "same_player_cap"
        decision.stake = 0.0
        return decision
    event = str((decision.market or {}).get("event_ticker") or "")
    if event and open_event_count(ledger, event) >= rec.max_tickets_per_event:
        decision.action = "skip"
        decision.reason = "mix_event_cap"
        decision.stake = 0.0
        return decision
    room = sleeve_room(ledger, rec, decision.sleeve)
    if room < rec.min_stake:
        decision.action = "skip"
        decision.reason = "mix_sleeve_full" if decision.sleeve != "slow" else "sleeve_slow_cap"
        decision.stake = 0.0
        return decision
    unit = kelly_stake(bank, float(decision.model_p), float(decision.yes_ask), fraction=rec.kelly_fraction)
    stake = min(unit, name_room, room, rec.single_name_frac * bank)
    liq = displayed_room(decision.market or {}, float(decision.yes_ask))
    if liq is not None:
        stake = min(stake, liq)
    stake = stake * float(live_scale)
    if stake < rec.min_stake:
        decision.action = "skip"
        decision.reason = "stake_too_small"
        decision.stake = 0.0
        return decision
    fee = taker_fee(float(decision.yes_ask), stake, fee_multiplier=(decision.market or {}).get("fee_multiplier"))
    if fee is None:
        decision.action = "skip"
        decision.reason = "no_fee_multiplier"
        decision.stake = 0.0
        return decision
    edge = edge_after_fee(
        float(decision.model_p),
        float(decision.yes_ask),
        stake,
        fee_multiplier=(decision.market or {}).get("fee_multiplier"),
    )
    if edge is None or edge <= 0:
        decision.action = "skip"
        decision.reason = "no_edge"
        decision.stake = 0.0
        return decision
    decision.action = "fill"
    decision.reason = "edge_after_fee"
    decision.stake = round(float(stake), 2)
    decision.fee = fee
    decision.edge_after_fee = edge
    decision.quote = quote_snapshot(
        decision.market or {},
        stake=decision.stake,
        fee=fee,
        declared_at=(decision.quote or {}).get("declared_at") or isoformat_now(),
    )
    return decision


def allocate(
    worthy: list[GolfDecision],
    ledger: dict[str, Any],
    recipe: WalletRecipe | None = None,
    *,
    live_scale: float = 1.0,
    max_fills: int | None = None,
    halted: bool = False,
) -> tuple[list[GolfDecision], list[GolfDecision]]:
    """Pick within each sleeve by edge_after_fee. Size into remaining sleeve room."""
    rec = recipe or recipe_v1()
    picks: list[GolfDecision] = []
    skipped: list[GolfDecision] = []
    if halted:
        for row in worthy:
            row.action = "skip"
            row.reason = "halt:" + str(ledger.get("halt_reason") or "halt")
            skipped.append(row)
        return picks, skipped
    remaining = 10**9 if max_fills is None else int(max_fills)
    by_sleeve: dict[str, list[GolfDecision]] = {"fast": [], "week": [], "slow": []}
    for row in worthy:
        by_sleeve.setdefault(row.sleeve, []).append(row)
    working = dict(ledger)
    working["tickets"] = list(ledger.get("tickets") or [])
    for sleeve in ("fast", "week", "slow"):
        rows = sorted(
            by_sleeve.get(sleeve) or [],
            key=lambda d: (-(float(d.edge_after_fee or 0)), str(d.ticker)),
        )
        for row in rows:
            if remaining <= 0:
                row.action = "skip"
                row.reason = "mix_not_picked"
                skipped.append(row)
                continue
            sized = attach_stake(row, working, rec, live_scale=live_scale)
            if sized.fill:
                working["tickets"] = list(working.get("tickets") or []) + [
                    {
                        "ticker": sized.ticker,
                        "player_id": sized.player_id,
                        "sleeve": sized.sleeve,
                        "stake": sized.stake,
                        "status": "open",
                        "event_ticker": str((sized.market or {}).get("event_ticker") or ""),
                    }
                ]
                picks.append(sized)
                remaining -= 1
            else:
                skipped.append(sized)
    return picks, skipped


def worst_open_in(
    ledger: dict[str, Any],
    *,
    sleeve: str,
    event_ticker: str | None = None,
    marks: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any] | None:
    marks = marks or {}
    candidates = []
    for ticket in ledger.get("tickets") or []:
        if str(ticket.get("status") or "") not in {"open", "SETTLE_PENDING"}:
            continue
        if str(ticket.get("sleeve") or "week") != sleeve:
            continue
        if event_ticker and str(ticket.get("event_ticker") or "") != event_ticker:
            continue
        ticker = str(ticket.get("ticker") or "")
        mark = marks.get(ticker) or {}
        live = mark.get("live_edge")
        if live is None:
            live = float("-inf")
        candidates.append((float(live), ticker, ticket))
    if not candidates:
        return None
    candidates.sort(key=lambda row: (row[0], row[1]))
    return candidates[0][2]
