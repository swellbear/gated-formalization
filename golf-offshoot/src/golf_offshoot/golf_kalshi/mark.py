"""Mark open tickets. Collapse, fail-clock, bid pop. Kalshi bid is the cash-out."""

from __future__ import annotations

from typing import Any

from golf_offshoot.golf_kalshi.brain import PlayerBrain, p_for_market
from golf_offshoot.golf_kalshi.espn_bind import event_key_for
from golf_offshoot.golf_kalshi.fees import bid_covers_position, edge_after_fee, paper_exit_pnl
from golf_offshoot.golf_kalshi.paper import (
    OPEN_STATUSES,
    apply_close,
    load_ledger,
    open_tickets,
    save_ledger,
)
from golf_offshoot.golf_kalshi.recipe import WalletRecipe, fail_holes_for, recipe_v1
from golf_offshoot.golf_kalshi.sleeves import classify_sleeve, market_horizon
from golf_offshoot.localtime import isoformat_now


def _float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def player_holes(brain: PlayerBrain | None, player_id: str | None, event_key: str) -> int | None:
    if brain is None or not player_id:
        return None
    if hasattr(brain, "player_holes"):
        try:
            holes = brain.player_holes(player_id, event_key)
            if holes is not None:
                return int(holes)
        except Exception:
            pass
    cached = {}
    if hasattr(brain, "_cache"):
        cached = ((brain._cache.get("events") or {}).get(event_key) or {})  # noqa: SLF001
    for row in cached.get("espn_rows") or []:
        if str(row.get("id") or "") == str(player_id):
            thru = row.get("thru")
            if thru is not None:
                try:
                    return int(thru)
                except (TypeError, ValueError):
                    return None
    return None


def golf_started(
    market: dict[str, Any] | None,
    brain: PlayerBrain | None,
    *,
    event_key: str = "",
    player_id: str | None = None,
) -> bool:
    market = market or {}
    if market.get("in_play") or market.get("can_close_early"):
        return True
    key = event_key or event_key_for(market)
    if brain is not None and hasattr(brain, "event_started"):
        try:
            if brain.event_started(key):
                return True
        except Exception:
            pass
    holes = player_holes(brain, player_id, key)
    if holes is not None and holes > 0:
        return True
    if brain is not None and hasattr(brain, "_cache"):
        cached = ((brain._cache.get("events") or {}).get(key) or {})  # noqa: SLF001
        if int(cached.get("live_competitors") or 0) > 0:
            return True
        rows = cached.get("espn_rows") or []
        for row in rows:
            if row.get("thru") or row.get("place") or row.get("score") is not None:
                return True
    return False


def market_from_ticket(ticket: dict[str, Any], catalog: dict[str, Any] | None = None) -> dict[str, Any]:
    """Live catalog row, falling back to the ticket quote when the ticker is missing."""
    market = dict(catalog or {})
    quote = ticket.get("quote") if isinstance(ticket.get("quote"), dict) else {}
    for key in (
        "yes_ask",
        "yes_bid",
        "displayed_size",
        "fee_multiplier",
        "in_play",
        "can_close_early",
        "event_ticker",
        "series_ticker",
        "title",
        "yes_sub_title",
    ):
        if market.get(key) is None:
            val = ticket.get(key)
            if val is None:
                val = quote.get(key)
            if val is not None:
                market[key] = val
    market.setdefault("ticker", ticket.get("ticker"))
    if market.get("fee_multiplier") is not None:
        market.setdefault("fee_multiplier_present", True)
    return market


def live_model_p(
    ticket: dict[str, Any],
    market: dict[str, Any] | None,
    brain: PlayerBrain | None,
) -> float | None:
    if brain is None:
        return None
    pid = str(ticket.get("player_id") or "")
    if not pid:
        return None
    raw = p_for_market(brain, pid, market or ticket)
    if raw is None:
        return None
    src = str(ticket.get("field_source") or "")
    haircut = float(ticket.get("tour_haircut") or 1.0)
    if src == "kalshi_listed" and haircut == 1.0:
        from golf_offshoot.golf_kalshi.recipe import LISTED_HAIRCUT

        haircut = LISTED_HAIRCUT
    return float(raw) * haircut


def mark_ticket(
    ticket: dict[str, Any],
    market: dict[str, Any] | None,
    brain: PlayerBrain | None,
    recipe: WalletRecipe | None = None,
) -> dict[str, Any]:
    rec = recipe or recipe_v1()
    market = market or {}
    key = event_key_for(market or ticket)
    live_p = live_model_p(ticket, market, brain)
    ask = _float(market.get("yes_ask")) if market else None
    if ask is None:
        ask = _float(ticket.get("yes_ask") or (ticket.get("quote") or {}).get("yes_ask"))
    bid = _float(market.get("yes_bid")) if market else _float((ticket.get("quote") or {}).get("yes_bid"))
    stake = float(ticket.get("stake") or rec.min_stake)
    live_edge = None
    if live_p is not None and ask is not None:
        live_edge = edge_after_fee(
            live_p,
            ask,
            stake,
            fee_multiplier=market.get("fee_multiplier")
            if market.get("fee_multiplier") is not None
            else (ticket.get("quote") or {}).get("fee_multiplier"),
        )
    entry_edge = _float(ticket.get("edge_after_fee"))
    started = golf_started(market, brain, event_key=key, player_id=str(ticket.get("player_id") or ""))
    holes = player_holes(brain, str(ticket.get("player_id") or ""), key)
    horizon = market_horizon(market or ticket)
    fail_at = fail_holes_for(horizon)
    sleeve = str(ticket.get("sleeve") or classify_sleeve(market or ticket))
    cover = bid_covers_position(ticket, market) if market else False
    collapsed = False
    if live_edge is not None:
        floor = rec.collapse_ratio * max(float(entry_edge or 0), 0.01)
        collapsed = float(live_edge) < 0 or float(live_edge) < floor
    improved = False
    if live_edge is not None and entry_edge is not None:
        improved = float(live_edge) >= float(entry_edge) + rec.improve_abs
    proceeds = None
    if bid is not None:
        from golf_offshoot.golf_kalshi.fees import sell_proceeds

        proceeds = sell_proceeds(stake, float(ticket.get("yes_ask") or 0), bid)
    pop = bool(proceeds is not None and proceeds >= rec.flip_hurdle * stake)
    fail = bool(sleeve == "fast" and fail_at > 0 and holes is not None and int(holes) >= fail_at and not pop)
    return {
        "ticker": str(ticket.get("ticker") or ""),
        "live_p": live_p,
        "live_edge": live_edge,
        "entry_edge": entry_edge,
        "yes_ask": ask,
        "yes_bid": bid,
        "golf_started": started,
        "holes": holes,
        "fail_holes": fail_at,
        "sleeve": sleeve,
        "cover": cover,
        "collapsed": collapsed,
        "improved": improved,
        "pop": pop,
        "fail_clock": fail,
        "horizon": horizon,
    }


def apply_paper_exit(
    ticket: dict[str, Any],
    market: dict[str, Any],
    *,
    reason: str,
    ledger: dict[str, Any],
) -> dict[str, Any] | None:
    bid = _float(market.get("yes_bid"))
    if bid is None:
        return None
    if not bid_covers_position(ticket, market):
        return None
    fee_mult = market.get("fee_multiplier")
    if fee_mult is None:
        fee_mult = (ticket.get("quote") or {}).get("fee_multiplier")
    pnl = paper_exit_pnl(ticket, yes_bid=bid, fee_multiplier=fee_mult)
    if pnl is None:
        return None
    recorded, after, exit_fee = pnl
    out = dict(ticket)
    out["status"] = "paper_exit"
    out["exit_reason"] = reason
    out["exit_bid"] = bid
    out["exit_fee"] = exit_fee
    out["exited_at"] = isoformat_now()
    out["recorded_pnl"] = recorded
    out["pnl_after_fee"] = after
    apply_close(ledger, out)
    return out


def path_action(mark: dict[str, Any], *, halted: bool) -> str | None:
    """Return exit_reason or add or None (hold)."""
    if not mark.get("cover") and (mark.get("collapsed") or mark.get("fail_clock") or mark.get("pop")):
        return None
    if mark.get("pop") and mark.get("sleeve") == "fast":
        return "flip_pop"
    if mark.get("fail_clock") and mark.get("golf_started"):
        return "flip_fail"
    if mark.get("collapsed") and mark.get("golf_started"):
        return "edge_collapsed"
    if halted:
        return None
    if mark.get("improved") and mark.get("golf_started"):
        return "add"
    return None


def trim_event_caps(
    ledger: dict[str, Any],
    markets_by_ticker: dict[str, dict[str, Any]],
    brain: PlayerBrain | None,
    recipe: WalletRecipe | None = None,
) -> list[dict[str, Any]]:
    rec = recipe or recipe_v1()
    if ledger.get("event_cap_trimmed"):
        return []
    exits: list[dict[str, Any]] = []
    events: dict[str, list[dict[str, Any]]] = {}
    for ticket in list(open_tickets(ledger)):
        key = str(ticket.get("event_ticker") or "")
        events.setdefault(key, []).append(ticket)
    for event, rows in events.items():
        if not event or len(rows) <= rec.max_tickets_per_event:
            continue
        marked = []
        for ticket in rows:
            market = market_from_ticket(ticket, markets_by_ticker.get(str(ticket.get("ticker") or "")))
            mark = mark_ticket(ticket, market, brain, rec)
            live = mark.get("live_edge")
            marked.append((float(live) if live is not None else float("-inf"), str(ticket.get("ticker") or ""), ticket, mark, market))
        marked.sort(key=lambda row: (row[0], row[1]))
        extras = marked[: max(0, len(marked) - rec.max_tickets_per_event)]
        for _live, _ticker, ticket, mark, market in extras:
            if not mark.get("cover"):
                continue
            closed = apply_paper_exit(ticket, market, reason="recipe_event_cap", ledger=ledger)
            if closed is not None:
                exits.append(closed)
                ledger = load_ledger()
    ledger = load_ledger()
    ledger["event_cap_trimmed"] = True
    save_ledger(ledger)
    return exits
