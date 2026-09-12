"""One golf Kalshi tick: settle first, then catalog, then decide. Advisor from tick one."""

from __future__ import annotations

import json
from collections import defaultdict
from typing import Any

from copy import copy

from golf_offshoot.golf_kalshi.adapter import GolfKalshiFeed, load_last_good_catalog
from golf_offshoot.golf_kalshi.brain import CachedExpertBrain, PlayerBrain, TickBudget
from golf_offshoot.golf_kalshi.allocate import allocate, attach_stake, sleeve_room, week_overweight, worst_open_in
from golf_offshoot.golf_kalshi.catalog_view import catalog_family, market_bucket
from golf_offshoot.golf_kalshi.decide import GolfDecision, screen_golf
from golf_offshoot.golf_kalshi.espn_bind import event_key_for
from golf_offshoot.golf_kalshi.executor import PaperExecutor, executor_for, live_scale_for
from golf_offshoot.golf_kalshi.fees import kelly_stake, taker_fee
from golf_offshoot.golf_kalshi.mark import apply_paper_exit, mark_ticket, market_from_ticket, path_action, trim_event_caps
from golf_offshoot.golf_kalshi.paper import (
    add_to_ticket,
    bump_recipe,
    engage_halt,
    exposure_player,
    halt_new_fills,
    load_ledger,
    open_tickets,
    record_tick_decisions,
    roll_utc_day,
    save_ledger,
)
from golf_offshoot.golf_kalshi.paths import (
    assert_golf_kalshi_path,
    last_tick_path,
    unmatched_path,
    watch_is_killed,
)
from golf_offshoot.golf_kalshi.recipe import recipe_v1
from golf_offshoot.golf_kalshi.settle import join_settles
from golf_offshoot.golf_kalshi.sleeves import classify_sleeve
from golf_offshoot.localtime import isoformat_now

LANE = "golf_kalshi"


def _decision_row(decision: GolfDecision, src: str = "") -> dict[str, Any]:
    return {
        "ticker": decision.ticker,
        "action": decision.action,
        "reason": decision.reason,
        "sleeve": decision.sleeve,
        "stake": decision.stake,
        "player_id": decision.player_id,
        "quote": decision.quote,
        "field_source": decision.field_source or src,
    }


def _realloc_hurdle(decision: GolfDecision, victim: dict[str, Any], market: dict[str, Any], rec) -> float:
    """Round-trip fees plus min_edge, as edge points."""
    hyst = float(rec.min_edge)
    fee_mult = market.get("fee_multiplier")
    if fee_mult is None:
        fee_mult = (victim.get("quote") or {}).get("fee_multiplier")
    bid = market.get("yes_bid")
    stake = float(victim.get("stake") or 0)
    if bid is not None and stake > 0:
        exit_fee = taker_fee(float(bid), stake, fee_multiplier=fee_mult)
        if exit_fee:
            hyst += float(exit_fee) / stake
    ask = decision.yes_ask
    if ask is not None:
        entry_fee = taker_fee(
            float(ask),
            rec.min_stake,
            fee_multiplier=(decision.market or {}).get("fee_multiplier"),
        )
        if entry_fee:
            hyst += float(entry_fee) / rec.min_stake
    return hyst


def _maybe_reallocate(
    decision: GolfDecision,
    ledger: dict[str, Any],
    rec,
    marks: dict[str, dict[str, Any]],
    markets_by_ticker: dict[str, dict[str, Any]],
) -> bool:
    probe = attach_stake(copy(decision), ledger, rec)
    if probe.fill:
        return False
    if probe.reason not in {"mix_sleeve_full", "sleeve_slow_cap", "mix_event_cap"}:
        return False
    event = str((decision.market or {}).get("event_ticker") or "") if probe.reason == "mix_event_cap" else None
    victim = worst_open_in(ledger, sleeve=decision.sleeve, event_ticker=event, marks=marks)
    if victim is None:
        return False
    if str(victim.get("ticker") or "") == decision.ticker:
        return False
    vmark = marks.get(str(victim.get("ticker") or "")) or {}
    victim_edge = vmark.get("live_edge")
    new_edge = decision.edge_after_fee
    if new_edge is None:
        return False
    market = market_from_ticket(victim, markets_by_ticker.get(str(victim.get("ticker") or "")))
    floor = (float(victim_edge) if victim_edge is not None else float("-inf")) + _realloc_hurdle(
        decision, victim, market, rec
    )
    if float(new_edge) < floor:
        return False
    closed = apply_paper_exit(victim, market, reason="mix_reallocate", ledger=ledger)
    return closed is not None


def exposure_overweight(ledger: dict[str, Any], rec) -> bool:
    return week_overweight(ledger, rec)


def _write_json(path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    assert_golf_kalshi_path(path)
    path.write_text(json.dumps(payload, indent=2, default=str) + "\n", encoding="utf-8")


def _priority(market: dict[str, Any]) -> tuple[int, int, str]:
    sleeve = classify_sleeve(market)
    in_play = 0 if market.get("in_play") else 1
    order = {"fast": 0, "week": 1, "slow": 2}.get(sleeve, 3)
    return (in_play, order, str(market.get("ticker") or ""))


def _read_last_tick() -> dict[str, Any]:
    path = last_tick_path()
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _notify_halt(reason: str) -> None:
    try:
        from golf_offshoot.operator_surface.notify import notify_run_complete

        notify_run_complete(
            command="golf-kalshi-halt",
            ok=True,
            detail=reason,
            lane="golf",
        )
    except Exception:
        pass


def _notify_settle(joined: int) -> None:
    if joined <= 0:
        return
    try:
        from golf_offshoot.operator_surface.notify import notify_run_complete

        notify_run_complete(
            command="golf-kalshi-settle",
            ok=True,
            detail=f"joined {joined}",
            lane="golf",
        )
    except Exception:
        pass


def _group_open(markets: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for market in markets:
        key = event_key_for(market)
        if key:
            groups[key].append(market)
    return groups


def _in_play(rows: list[dict[str, Any]]) -> bool:
    return any(bool(m.get("in_play")) for m in rows)


def _slow_only(rows: list[dict[str, Any]]) -> bool:
    return (not _in_play(rows)) and all(classify_sleeve(m) == "slow" for m in rows)


def _espn_bound_live(brain: PlayerBrain | None, event_key: str) -> bool:
    if brain is None or not hasattr(brain, "field_source"):
        return False
    try:
        if str(brain.field_source(event_key) or "") != "espn":
            return False
        cached = {}
        if hasattr(brain, "_cache"):
            cached = ((brain._cache.get("events") or {}).get(event_key) or {})  # noqa: SLF001
        return int(cached.get("live_competitors") or 0) > 0
    except Exception:
        return False


def _brain_order(
    groups: dict[str, list[dict[str, Any]]],
    rr_cursor: int,
    brain: PlayerBrain | None = None,
    held_keys: list[str] | None = None,
) -> tuple[list[str], int]:
    in_play: list[tuple[str, str]] = []
    mid: list[str] = []
    slow: list[str] = []
    for key, rows in groups.items():
        family = catalog_family(str((rows[0] or {}).get("series_ticker") or key))
        live = _in_play(rows) or _espn_bound_live(brain, key)
        if live:
            in_play.append((family, key))
        elif _slow_only(rows):
            slow.append(key)
        else:
            mid.append(key)
    families: list[str] = []
    seen: set[str] = set()
    for fam, _key in in_play:
        if fam not in seen:
            families.append(fam)
            seen.add(fam)
    next_rr = rr_cursor
    if families:
        start = rr_cursor % len(families)
        families = families[start:] + families[:start]
        next_rr = rr_cursor + 1
        ordered: list[str] = []
        for fam in families:
            for f, key in in_play:
                if f == fam:
                    ordered.append(key)
        ordered.extend(mid)
        ordered.extend(slow)
    else:
        rest = mid + slow
        if rest:
            start = rr_cursor % len(rest)
            next_rr = rr_cursor + 1
            ordered = rest[start:] + rest[:start]
        else:
            ordered = []
    if held_keys:
        front = [k for k in held_keys if k in groups]
        rest = [k for k in ordered if k not in set(front)]
        ordered = front + rest
    return ordered, next_rr


def run_tick(
    *,
    feed: GolfKalshiFeed | None = None,
    brain: PlayerBrain | None = None,
    executor: Any | None = None,
    budget: TickBudget | None = None,
    catalog: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Settle always. Catalog on its own TTL. Clock is for Monte Carlo. Fill cap is count."""
    killed = watch_is_killed()
    rec = recipe_v1()
    led = roll_utc_day(load_ledger())
    save_ledger(led)
    feed = feed or GolfKalshiFeed()
    brain = brain or CachedExpertBrain()
    executor = executor or executor_for()
    if catalog is None:
        try:
            catalog = feed.fetch_catalog()
        except Exception:
            catalog = load_last_good_catalog()
    markets = list(catalog.get("markets") or [])
    settle = join_settles(markets)
    led = settle.get("ledger") or load_ledger()
    led = bump_recipe(led, rec)
    save_ledger(led)
    halted, halt_why = halt_new_fills(led, rec)
    if halted and not led.get("halted"):
        led = engage_halt(led, halt_why, recipe=rec)
        _notify_halt(halt_why)
    save_ledger(led)
    if settle.get("joined"):
        _notify_settle(int(settle["joined"]))
        try:
            from golf_offshoot.golf_kalshi.learn import maybe_promote

            maybe_promote(holdout_beats_expert=False)
        except Exception:
            pass
    budget = budget or TickBudget()
    decisions: list[dict[str, Any]] = []
    unmatched: list[dict[str, str]] = []
    fill_rows: list[dict[str, Any]] = []
    fills = 0
    skips = 0
    skip_reasons: dict[str, int] = {}
    hunts: list[dict[str, Any]] = []
    hunt_bound = 0
    brain_deferred = 0
    n_exits = 0
    n_realloc = 0
    n_adds = 0
    n_worthy = 0
    picked = {"fast": 0, "week": 0, "slow": 0}
    week_over = False
    marks: dict[str, dict[str, Any]] = {}
    live_markets = [m for m in markets if market_bucket(m) == "open"]
    markets_by_ticker = {str(m.get("ticker") or ""): m for m in markets}
    prev = _read_last_tick()
    rr = int(prev.get("brain_rr") or 0)
    next_rr = rr
    summary = "killed"
    if not killed:
        from golf_offshoot.golf_kalshi.espn_bind import EspnLeagueBoards

        boards = EspnLeagueBoards()
        if hasattr(brain, "begin_tick"):
            try:
                brain.begin_tick(boards)
            except TypeError:
                brain.begin_tick()
        groups = _group_open(live_markets)
        if hasattr(brain, "hunt_identity"):
            for event_key, rows in groups.items():
                if not rows:
                    continue
                try:
                    brain.hunt_identity(event_key, rows)
                except Exception:
                    skip_reasons["brain_error"] = skip_reasons.get("brain_error", 0) + 1
            hunt_bound = int(getattr(brain, "n_bound", 0) or 0)
        held_keys = []
        for ticket in open_tickets(led):
            key = event_key_for(ticket) or str(ticket.get("event_ticker") or "")
            if key and key not in held_keys:
                held_keys.append(key)
        order, next_rr = _brain_order(groups, rr, brain, held_keys=held_keys)
        for event_key in order:
            rows = groups.get(event_key) or []
            if not rows:
                continue
            try:
                brain.maybe_refresh(event_key, "", budget=budget, markets=rows)
            except TypeError:
                try:
                    brain.maybe_refresh(event_key, brain.scoreboard_fingerprint(event_key), budget=budget)
                except Exception:
                    skip_reasons["brain_error"] = skip_reasons.get("brain_error", 0) + 1
            except Exception:
                skip_reasons["brain_error"] = skip_reasons.get("brain_error", 0) + 1
        if hasattr(brain, "end_tick"):
            try:
                brain.end_tick()
            except Exception:
                pass
        if hasattr(brain, "hunts_this_tick"):
            hunts = list(brain.hunts_this_tick or [])
        brain_deferred = sum(1 for h in hunts if h.get("deferred") or h.get("budget"))
        trim_event_caps(led, markets_by_ticker, brain, rec)
        led = load_ledger()
        closed: set[str] = set()
        for ticket in list(open_tickets(led)):
            ticker = str(ticket.get("ticker") or "")
            market = market_from_ticket(ticket, markets_by_ticker.get(ticker))
            mark = mark_ticket(ticket, market, brain, rec)
            marks[ticker] = mark
            action = path_action(mark, halted=halted)
            if action in {"edge_collapsed", "flip_fail", "flip_pop"} and ticker not in closed:
                if apply_paper_exit(ticket, market, reason=str(action), ledger=led) is not None:
                    closed.add(ticker)
                    n_exits += 1
                    led = load_ledger()
                    skip_reasons[str(action)] = skip_reasons.get(str(action), 0) + 1
        if not halted:
            for ticket in list(open_tickets(load_ledger())):
                if n_adds >= rec.max_adds_per_tick:
                    break
                ticker = str(ticket.get("ticker") or "")
                market = market_from_ticket(ticket, markets_by_ticker.get(ticker))
                mark = marks.get(ticker) or mark_ticket(ticket, market, brain, rec)
                if path_action(mark, halted=False) != "add":
                    continue
                sleeve = str(ticket.get("sleeve") or "week")
                room = sleeve_room(led, rec, sleeve)
                if room < rec.min_stake:
                    continue
                ask = mark.get("yes_ask")
                if ask is None:
                    ask = ticket.get("yes_ask")
                model_p = mark.get("live_p")
                if model_p is None or ask is None or float(ask) <= 0:
                    continue
                ask_f = float(ask)
                bank = float(led.get("bankroll") or rec.seed)
                pid = str(ticket.get("player_id") or "")
                name_room = rec.single_name_frac * bank - exposure_player(led, pid)
                extra = kelly_stake(bank, float(model_p), ask_f, fraction=rec.kelly_fraction)
                extra = min(extra, room, max(0.0, name_room))
                if extra < rec.min_stake:
                    continue
                fee = taker_fee(
                    ask_f,
                    extra,
                    fee_multiplier=market.get("fee_multiplier")
                    or (ticket.get("quote") or {}).get("fee_multiplier"),
                )
                add_to_ticket(led, ticker, extra, extra_fee=fee)
                n_adds += 1
                led = load_ledger()
        scale = live_scale_for(led) if not isinstance(executor, PaperExecutor) else 1.0
        worthy: list[GolfDecision] = []
        for market in sorted(live_markets, key=_priority):
            event_key = event_key_for(market)
            src = ""
            if hasattr(brain, "field_source"):
                try:
                    src = str(brain.field_source(event_key) or "")
                except Exception:
                    src = ""
            decision = screen_golf(
                market,
                led,
                rec,
                brain,
                budget_blocked=False,
                live_scale=scale,
                field_source=src,
                halt_fills=False,
            )
            row = _decision_row(decision, src)
            decisions.append(row)
            if decision.quarantine:
                unmatched.append(decision.quarantine)
            if decision.worthy:
                n_worthy += 1
                worthy.append(decision)
            else:
                skips += 1
                skip_reasons[decision.reason] = skip_reasons.get(decision.reason, 0) + 1
        if not halted:
            ranked = sorted(worthy, key=lambda d: (-(float(d.edge_after_fee or 0)), str(d.ticker)))
            for decision in ranked:
                if n_realloc >= rec.max_reallocates_per_tick:
                    break
                if _maybe_reallocate(decision, led, rec, marks, markets_by_ticker):
                    n_realloc += 1
                    n_exits += 1
                    led = load_ledger()
                    skip_reasons["mix_reallocate"] = skip_reasons.get("mix_reallocate", 0) + 1
        remaining_fills = max(0, budget.max_fills - fills)
        picks, skipped = allocate(
            worthy,
            led,
            rec,
            live_scale=scale,
            max_fills=remaining_fills,
            halted=halted,
        )
        for sized in skipped:
            skips += 1
            skip_reasons[sized.reason] = skip_reasons.get(sized.reason, 0) + 1
            decisions.append(_decision_row(sized))
        for decision in picks:
            try:
                executor.book(decision)
                budget.note_fill()
                fills += 1
                picked[decision.sleeve] = picked.get(decision.sleeve, 0) + 1
                fill_rows.append(_decision_row(decision))
                led = load_ledger()
            except Exception as exc:
                skips += 1
                skip_reasons["book_error"] = skip_reasons.get("book_error", 0) + 1
                decisions.append({**_decision_row(decision), "book_error": str(exc)})
        week_over = exposure_overweight(led, rec)
        summary = (
            f"fills={fills} skips={skips} joined={settle.get('joined')} "
            f"worthy={n_worthy} picked={picked.get('fast', 0)}/{picked.get('week', 0)}/{picked.get('slow', 0)} "
            f"exits={n_exits} realloc={n_realloc} adds={n_adds}"
            f"{' week overweight catch-up' if week_over else ''}"
        )
        record_tick_decisions(
            fills=fill_rows,
            unmatched=unmatched,
            skip_reasons=skip_reasons,
            n_decisions=len(decisions),
        )
    _write_json(
        unmatched_path(),
        {"lane": LANE, "rows": unmatched, "at": isoformat_now()},
    )
    kalshi_live = any(m.get("in_play") for m in markets) or any(
        t.get("in_play") for t in (led.get("tickets") or [])
    )
    espn_live = any(int(h.get("live_competitors") or 0) > 0 for h in hunts)
    if not espn_live and hasattr(brain, "_cache"):
        try:
            espn_live = any(
                int((row or {}).get("live_competitors") or 0) > 0
                for row in (brain._cache.get("events") or {}).values()  # noqa: SLF001
            )
        except Exception:
            espn_live = False
    in_play = bool(kalshi_live or espn_live)
    remaining = 0.0
    try:
        remaining = float(budget.remaining())
    except Exception:
        remaining = 0.0
    tick = {
        "lane": LANE,
        "at": isoformat_now(),
        "killed": killed,
        "halted": bool(led.get("halted")),
        "halt_reason": led.get("halt_reason") or "",
        "fills": fills,
        "skips": skips,
        "decisions": len(decisions),
        "settle": {"joined": settle.get("joined"), "pending": settle.get("pending")},
        "markets": len(live_markets) if not killed else len(markets),
        "catalog_markets": len(markets),
        "skip_reasons": skip_reasons,
        "field_hunt": hunts,
        "hunt_bound": hunt_bound,
        "brain_deferred": brain_deferred,
        "brain_rr": next_rr,
        "brain_runs": getattr(budget, "brain_runs", 0),
        "budget_remaining": remaining,
        "in_play": bool(in_play),
        "worthy": n_worthy,
        "picked": picked,
        "exits": n_exits,
        "realloc": n_realloc,
        "adds": n_adds,
        "week_overweight": week_over,
        "marks": {
            key: {"live_edge": row.get("live_edge"), "entry_edge": row.get("entry_edge")}
            for key, row in marks.items()
        },
        "summary": summary,
        "consulted_decide": True,
    }
    _write_json(last_tick_path(), tick)
    return tick
