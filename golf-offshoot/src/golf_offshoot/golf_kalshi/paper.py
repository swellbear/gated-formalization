"""One golf ledger. Not Phase 1 paper/. Not 15m. After-fee bankroll."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from golf_offshoot.golf_kalshi.paths import assert_golf_kalshi_path, decisions_path, ledger_path
from golf_offshoot.golf_kalshi.recipe import PREVIOUS_RECIPE_ID, RECIPE_ID, WalletRecipe, recipe_v1
from golf_offshoot.golf_kalshi.sleeves import SLEEVES, classify_sleeve
from golf_offshoot.localtime import isoformat_now

LANE = "golf_kalshi"
OPEN_STATUSES = {"open", "SETTLE_PENDING"}
CLOSED_STATUSES = {"paper_win", "paper_lose", "void", "paper_exit"}


def empty_ledger(recipe: WalletRecipe | None = None) -> dict[str, Any]:
    rec = recipe or recipe_v1()
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return {
        "lane": LANE,
        "recipe_id": rec.recipe_id,
        "bankroll": rec.seed,
        "seed": rec.seed,
        "peak_bankroll": rec.seed,
        "betting_pnl": 0.0,
        "fees_paid": 0.0,
        "sleeves": {"fast": 0.0, "week": 0.0, "slow": 0.0},
        "tickets": [],
        "halted": False,
        "halt_reason": "",
        "halt_until": "",
        "day_utc": day,
        "day_start_bankroll": rec.seed,
        "day_settled_pnl": 0.0,
        "lived_fills_settled": 0,
        "trading_armed": False,
        "event_cap_trimmed": True,
    }


def load_ledger() -> dict[str, Any]:
    path = ledger_path()
    if not path.is_file():
        return empty_ledger()
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return empty_ledger()
    if not isinstance(payload, dict):
        return empty_ledger()
    payload.setdefault("tickets", [])
    payload.setdefault("sleeves", {"fast": 0.0, "week": 0.0, "slow": 0.0})
    payload.setdefault("event_cap_trimmed", str(payload.get("recipe_id") or "") == RECIPE_ID)
    return payload


def save_ledger(ledger: dict[str, Any]) -> None:
    path = ledger_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    assert_golf_kalshi_path(path)
    ledger = dict(ledger)
    ledger["lane"] = LANE
    path.write_text(json.dumps(ledger, indent=2, default=str) + "\n", encoding="utf-8")


def load_decisions() -> dict[str, Any]:
    path = decisions_path()
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    rows = payload.get("decisions") if isinstance(payload, dict) else None
    return rows if isinstance(rows, dict) else {}


def record_tick_decisions(
    *,
    fills: list[dict[str, Any]] | None = None,
    unmatched: list[dict[str, Any]] | None = None,
    skip_reasons: dict[str, int] | None = None,
    n_decisions: int = 0,
) -> dict[str, Any]:
    """One write per tick. Fills + skip counts. Not 1721 per-ticker skip dumps."""
    payload = {
        "lane": LANE,
        "at": isoformat_now(),
        "n_decisions": int(n_decisions),
        "skip_reasons": dict(skip_reasons or {}),
        "fills": list(fills or []),
        "unmatched": list(unmatched or []),
    }
    path = decisions_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    assert_golf_kalshi_path(path)
    path.write_text(json.dumps(payload, indent=2, default=str) + "\n", encoding="utf-8")
    return payload


def record_decision(ticker: str, row: dict[str, Any]) -> dict[str, Any]:
    """Kept for a single fill row. The tick writes skip counts via record_tick_decisions."""
    rows = load_decisions()
    if not isinstance(rows, dict):
        rows = {}
    rows[str(ticker)] = row
    path = decisions_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    assert_golf_kalshi_path(path)
    path.write_text(
        json.dumps({"lane": LANE, "decisions": rows, "at": isoformat_now()}, indent=2, default=str)
        + "\n",
        encoding="utf-8",
    )
    return row


def open_tickets(ledger: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    led = ledger if ledger is not None else load_ledger()
    return [t for t in led.get("tickets") or [] if str(t.get("status") or "") in OPEN_STATUSES]


def exposure_total(ledger: dict[str, Any]) -> float:
    return float(sum(float(t.get("stake") or 0) for t in open_tickets(ledger)))


def exposure_player(ledger: dict[str, Any], player_id: str) -> float:
    pid = str(player_id or "")
    return float(
        sum(float(t.get("stake") or 0) for t in open_tickets(ledger) if str(t.get("player_id") or "") == pid)
    )


def exposure_sleeve(ledger: dict[str, Any], sleeve: str) -> float:
    return float(
        sum(float(t.get("stake") or 0) for t in open_tickets(ledger) if str(t.get("sleeve") or "") == sleeve)
    )


def uncommitted(ledger: dict[str, Any]) -> float:
    return float(ledger.get("bankroll") or 0) - exposure_total(ledger)


def roll_utc_day(ledger: dict[str, Any]) -> dict[str, Any]:
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if str(ledger.get("day_utc") or "") != day:
        ledger["day_utc"] = day
        ledger["day_start_bankroll"] = float(ledger.get("bankroll") or 0)
        ledger["day_settled_pnl"] = 0.0
        until = str(ledger.get("halt_until") or "")
        if ledger.get("halted") and until and until <= day:
            ledger["halted"] = False
            ledger["halt_reason"] = ""
            ledger["halt_until"] = ""
    return ledger


def halt_new_fills(ledger: dict[str, Any], recipe: WalletRecipe) -> tuple[bool, str]:
    led = roll_utc_day(ledger)
    if led.get("halted"):
        return True, str(led.get("halt_reason") or "halt")
    bank = float(led.get("bankroll") or 0)
    peak = max(float(led.get("peak_bankroll") or bank), bank)
    led["peak_bankroll"] = peak
    if peak > 0 and (peak - bank) / peak >= recipe.drawdown_frac:
        return True, "drawdown"
    start = float(led.get("day_start_bankroll") or bank)
    if start > 0 and float(led.get("day_settled_pnl") or 0) <= -recipe.daily_loss_frac * start:
        return True, "daily_loss"
    return False, ""


def engage_halt(ledger: dict[str, Any], reason: str, *, resume_rule: str) -> dict[str, Any]:
    led = dict(ledger)
    led["halted"] = True
    led["halt_reason"] = reason
    if resume_rule == "next_utc_day":
        from datetime import timedelta

        nxt = datetime.now(timezone.utc).date() + timedelta(days=1)
        led["halt_until"] = nxt.isoformat()
    else:
        led["halt_until"] = ""
    return led


def recompute_sleeves(ledger: dict[str, Any]) -> dict[str, Any]:
    sleeves = {name: 0.0 for name in SLEEVES}
    for ticket in open_tickets(ledger):
        sleeve = str(ticket.get("sleeve") or "week")
        if sleeve not in sleeves:
            sleeve = "week"
        sleeves[sleeve] = round(float(sleeves.get(sleeve) or 0) + float(ticket.get("stake") or 0), 4)
    ledger["sleeves"] = sleeves
    return ledger


def restamp_open_sleeves(ledger: dict[str, Any]) -> dict[str, Any]:
    """Label fix on a recipe bump. No pnl."""
    tickets = []
    for ticket in ledger.get("tickets") or []:
        row = dict(ticket)
        if str(row.get("status") or "") in OPEN_STATUSES:
            row["sleeve"] = classify_sleeve(row)
        tickets.append(row)
    ledger["tickets"] = tickets
    return recompute_sleeves(ledger)


def bump_recipe(ledger: dict[str, Any], recipe: WalletRecipe | None = None) -> dict[str, Any]:
    rec = recipe or recipe_v1()
    current = str(ledger.get("recipe_id") or "")
    if current == rec.recipe_id:
        return ledger
    if current == PREVIOUS_RECIPE_ID or current == "":
        ledger["event_cap_trimmed"] = False
    ledger["recipe_id"] = rec.recipe_id
    return restamp_open_sleeves(ledger)


def exposure_event(ledger: dict[str, Any], event_ticker: str) -> float:
    key = str(event_ticker or "")
    return float(
        sum(float(t.get("stake") or 0) for t in open_tickets(ledger) if str(t.get("event_ticker") or "") == key)
    )


def open_event_count(ledger: dict[str, Any], event_ticker: str) -> int:
    key = str(event_ticker or "")
    return sum(1 for t in open_tickets(ledger) if str(t.get("event_ticker") or "") == key)


def open_ticket_for(ledger: dict[str, Any], ticker: str) -> dict[str, Any] | None:
    for row in open_tickets(ledger):
        if str(row.get("ticker") or "") == ticker:
            return row
    return None


def latest_exit(ledger: dict[str, Any], ticker: str) -> dict[str, Any] | None:
    found = None
    for row in ledger.get("tickets") or []:
        if str(row.get("ticker") or "") == ticker and str(row.get("status") or "") == "paper_exit":
            found = row
    return found


def rebuy_blocked(ledger: dict[str, Any], ticker: str, live_edge: float | None, recipe: WalletRecipe) -> bool:
    if latest_exit(ledger, ticker) is None:
        return False
    if live_edge is None:
        return True
    return float(live_edge) < float(recipe.min_edge)


def apply_close(ledger: dict[str, Any], updated: dict[str, Any]) -> dict[str, Any]:
    """Official settle or paper_exit. Recompute sleeves from open tickets."""
    led = dict(ledger)
    ticker = str(updated.get("ticker") or "")
    tickets = []
    replaced = False
    for row in led.get("tickets") or []:
        if not replaced and str(row.get("ticker") or "") == ticker and str(row.get("status") or "") in OPEN_STATUSES:
            tickets.append(updated)
            replaced = True
        else:
            tickets.append(row)
    if not replaced:
        return ledger
    led["tickets"] = tickets
    pnl = float(updated.get("pnl_after_fee") or 0)
    led["bankroll"] = round(float(led.get("bankroll") or 0) + pnl, 4)
    led["betting_pnl"] = round(float(led.get("betting_pnl") or 0) + pnl, 4)
    led["day_settled_pnl"] = round(float(led.get("day_settled_pnl") or 0) + pnl, 4)
    led["peak_bankroll"] = max(float(led.get("peak_bankroll") or 0), float(led["bankroll"]))
    if updated.get("lived") and str(updated.get("status") or "") in {"paper_win", "paper_lose", "void"}:
        led["lived_fills_settled"] = int(led.get("lived_fills_settled") or 0) + 1
    exit_fee = float(updated.get("exit_fee") or 0)
    if exit_fee:
        led["fees_paid"] = round(float(led.get("fees_paid") or 0) + exit_fee, 4)
    recompute_sleeves(led)
    save_ledger(led)
    return led


def append_ticket(ledger: dict[str, Any], ticket: dict[str, Any]) -> dict[str, Any]:
    led = dict(ledger)
    tickets = list(led.get("tickets") or [])
    tickets.append(ticket)
    led["tickets"] = tickets
    led["fees_paid"] = float(led.get("fees_paid") or 0) + float(ticket.get("fee") or 0)
    recompute_sleeves(led)
    save_ledger(led)
    return led


def replace_ticket(ledger: dict[str, Any], ticker: str, ticket: dict[str, Any]) -> dict[str, Any]:
    led = dict(ledger)
    tickets = []
    replaced = False
    for row in led.get("tickets") or []:
        if not replaced and str(row.get("ticker") or "") == ticker and str(row.get("status") or "") in OPEN_STATUSES:
            tickets.append(ticket)
            replaced = True
        elif not replaced and str(row.get("ticker") or "") == ticker:
            tickets.append(ticket)
            replaced = True
        else:
            tickets.append(row)
    if not replaced:
        tickets.append(ticket)
    led["tickets"] = tickets
    save_ledger(led)
    return led


def add_to_ticket(ledger: dict[str, Any], ticker: str, extra_stake: float, extra_fee: float | None = None) -> dict[str, Any]:
    led = dict(ledger)
    tickets = []
    for row in led.get("tickets") or []:
        if str(row.get("ticker") or "") == ticker and str(row.get("status") or "") in OPEN_STATUSES:
            updated = dict(row)
            updated["stake"] = round(float(updated.get("stake") or 0) + float(extra_stake), 2)
            if extra_fee:
                updated["fee"] = round(float(updated.get("fee") or 0) + float(extra_fee), 4)
                led["fees_paid"] = round(float(led.get("fees_paid") or 0) + float(extra_fee), 4)
            adds = list(updated.get("adds") or [])
            adds.append({"stake": round(float(extra_stake), 2), "at": isoformat_now()})
            updated["adds"] = adds
            tickets.append(updated)
        else:
            tickets.append(row)
    led["tickets"] = tickets
    recompute_sleeves(led)
    save_ledger(led)
    return led


def ticket_by_ticker(ledger: dict[str, Any], ticker: str) -> dict[str, Any] | None:
    open_row = open_ticket_for(ledger, ticker)
    if open_row is not None:
        return open_row
    for row in ledger.get("tickets") or []:
        if str(row.get("ticker") or "") == ticker:
            return row
    return None
