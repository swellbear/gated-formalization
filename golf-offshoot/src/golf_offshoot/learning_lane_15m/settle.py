"""Settle-join for lane 15m. Honest Kalshi result + documented SOURCE only.

Official settle evidence = Kalshi result matched to documented SOURCE
(CF Benchmarks via event settlement_sources + CRYPTO15M 60s CFB RTI average rule).

Hard NOs:
- DIY CFB average as official settle without match-to-Kalshi result
- demo fills as settles
- invent win/lose
- golf artifact mix
- trading ARMED

# Digestor owns SOURCE honesty digest later.
# Leave this settle-rule SOURCE hook; do not invent Digestor docs.
# Read-only boards: /workspace/kalshi_15m_lab/SPINE_STAMP.md, SOURCE_INDEX.md,
# LIVING_SPINE_INDEX.md, SOURCE/ PDFs.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from golf_offshoot.data_feeds.kalshi_15m import (
    EXPECTED_SOURCE_NAME,
    parse_kalshi_result,
    source_is_cf_benchmarks,
)
from golf_offshoot.learning_lane_15m.paper import (
    TRADING_ARMED,
    iter_books,
    load_ledger,
    save_book,
    save_ledger,
)
from golf_offshoot.strategy.paper_ledger import EventWeek, LedgerEntry, TicketResult
from golf_offshoot.learning_lane_15m.paths import (
    LANE_15M,
    PRIMARY_SERIES,
    assert_not_golf_path,
    safe_artifact_stem,
    settlements_dir_15m,
)
from golf_offshoot.localtime import now
from golf_offshoot.models.strategy import new_id

SETTLE_SETTLED = "settled"
SETTLE_PENDING = "SETTLE_PENDING"
SETTLE_NEVER = "never_settled"

# CRYPTO15M documented rule — cited, never computed here as official settle.
CRYPTO15M_RULE = (
    "CRYPTO15M: official and final value is the simple average of 60 CF Benchmarks "
    "RTI prints in the last minute before expiration, rounded to 2 decimals. "
    "This adapter records the rule. It does not DIY that average as a settle."
)


SETTLE_READY_STATUSES = frozenset({"finalized", "determined", "settled"})
SETTLE_PENDING_STATUSES = frozenset({"active", "open", "closed", "initialized"})
SETTLE_DISPUTED_STATUSES = frozenset({"disputed", "under-review", "under_review", "review"})


class SettleJoinRow(BaseModel):
    ticker: str
    event_ticker: str = ""
    window_id: str = ""
    settle_status: str
    kalshi_result: str = ""
    source_matched: bool = False
    source_name: str = ""
    settlement_ts: str = ""
    settlement_value_dollars: float | None = None
    expiration_value: str = ""
    status: str = ""
    banner: str = ""
    won: bool | None = None
    pnl: float | None = None
    note: str = ""
    never_auto_bet: bool = True
    trading_armed: bool = False


class DiyCfbAverageRefused(RuntimeError):
    """Hard NO: a homemade CFB average is not official settle evidence."""


class DemoFillSettleRefused(RuntimeError):
    """Hard NO: demo / mock fills are not settles."""


def refuse_diy_cfb_average(*_args: Any, **_kwargs: Any) -> None:
    """Explicit refuse. Digestor SOURCE is Kalshi-matched, not a local average."""
    raise DiyCfbAverageRefused(
        "Hard NO: DIY CFB average is not official settle. "
        "Need Kalshi result matched to documented CF Benchmarks SOURCE."
    )


def official_source_matched(market: dict[str, Any], event: dict[str, Any] | None = None) -> bool:
    sources = list(market.get("settlement_sources") or [])
    if event is not None:
        sources = sources or list(event.get("settlement_sources") or [])
    if market.get("source_is_cf_benchmarks") or (event or {}).get("source_is_cf_benchmarks"):
        return True
    return source_is_cf_benchmarks(sources)


def classify_settle(
    market: dict[str, Any],
    *,
    event: dict[str, Any] | None = None,
    demo: bool = False,
) -> SettleJoinRow:
    """Record settle_status from honest fields only. Never invent win/lose."""
    if TRADING_ARMED:
        raise RuntimeError("trading NOT ARMED")
    if demo:
        raise DemoFillSettleRefused("Hard NO: demo fills are not settles")
    ticker = str(market.get("ticker") or "")
    event_ticker = str(market.get("event_ticker") or "")
    window = str(market.get("window_id") or "")
    result = parse_kalshi_result(market.get("result"))
    status = str(market.get("status") or "").strip().lower()
    matched = official_source_matched(market, event)
    source_name = EXPECTED_SOURCE_NAME if matched else ""
    support = {
        "settlement_ts": str(market.get("settlement_ts") or ""),
        "settlement_value_dollars": market.get("settlement_value_dollars"),
        "expiration_value": str(market.get("expiration_value") or ""),
        "status": status,
    }
    if bool(market.get("can_close_early")) and not result:
        return SettleJoinRow(
            ticker=ticker,
            event_ticker=event_ticker,
            window_id=window,
            settle_status=SETTLE_PENDING,
            source_matched=matched,
            source_name=source_name,
            banner="SETTLE_PENDING",
            note=(
                "SETTLE_PENDING: can_close_early is set. Wait for the Kalshi result. "
                "Do not invent from close_time or a DIY CFB average."
            ),
            **support,
        )
    if status in SETTLE_DISPUTED_STATUSES:
        return SettleJoinRow(
            ticker=ticker,
            event_ticker=event_ticker,
            window_id=window,
            settle_status=SETTLE_PENDING,
            kalshi_result=result,
            source_matched=matched,
            source_name=source_name,
            banner="SETTLE_PENDING — disputed / under review",
            note="SETTLE_PENDING: disputed or under review. Hard NO invent win/lose.",
            **support,
        )
    if not matched:
        return SettleJoinRow(
            ticker=ticker,
            event_ticker=event_ticker,
            window_id=window,
            settle_status=SETTLE_NEVER,
            kalshi_result=result,
            source_matched=False,
            note=(
                "never_settled: Kalshi result is not matched to documented "
                f"{EXPECTED_SOURCE_NAME} SOURCE on settlement_sources. {CRYPTO15M_RULE}"
            ),
            **support,
        )
    ready_status = status in SETTLE_READY_STATUSES or status == ""
    if result and ready_status:
        return SettleJoinRow(
            ticker=ticker,
            event_ticker=event_ticker,
            window_id=window,
            settle_status=SETTLE_SETTLED,
            kalshi_result=result,
            source_matched=True,
            source_name=source_name,
            note=(
                f"official Kalshi result={result} matched to {EXPECTED_SOURCE_NAME}. "
                f"{CRYPTO15M_RULE}"
            ),
            **support,
        )
    if status in SETTLE_PENDING_STATUSES or not result:
        return SettleJoinRow(
            ticker=ticker,
            event_ticker=event_ticker,
            window_id=window,
            settle_status=SETTLE_PENDING,
            kalshi_result=result,
            source_matched=True,
            source_name=source_name,
            banner="SETTLE_PENDING",
            note=(
                "SETTLE_PENDING: CF Benchmarks SOURCE is documented, but Kalshi "
                "result is not yet official (active/closed without result, or "
                "finalized/determined missing result). Do not invent win/lose. "
                "yes_bid/ask, last_price, and volume are display-only."
            ),
            **support,
        )
    return SettleJoinRow(
        ticker=ticker,
        event_ticker=event_ticker,
        window_id=window,
        settle_status=SETTLE_NEVER,
        kalshi_result=result,
        source_matched=matched,
        source_name=source_name,
        note="never_settled: status/result combination is not official. Hard NO invent.",
        **support,
    )


def event_ticker_from_book_id(book_id: str) -> str:
    """Window books are keyed by window_id. The event ticker is the prefix before __."""
    token = str(book_id or "")
    return token.split("__", 1)[0] if token else ""


def _event_ticker_from_book_id(book_id: str) -> str:
    return event_ticker_from_book_id(book_id)


def _event_for_book(
    rec,
    market: dict[str, Any] | None,
    by_event: dict[str, dict[str, Any]],
) -> dict[str, Any] | None:
    if market is not None:
        ev = by_event.get(str(market.get("event_ticker") or ""))
        if ev is not None:
            return ev
    tid = str(rec.tournament_id or "")
    if tid in by_event:
        return by_event[tid]
    return by_event.get(_event_ticker_from_book_id(tid))


def _market_for_book_position(
    pos,
    rec,
    by_ticker: dict[str, dict[str, Any]],
    by_window: dict[str, dict[str, Any]],
) -> dict[str, Any] | None:
    """Match a paper book to the Kalshi window it was opened on.

    Books are keyed by window_id (`event__open_utc__close_utc`). If close_time
    moves, that is a new window. The old book must stay SETTLE_PENDING.
    """
    book_id = str(rec.tournament_id or "")
    market = by_window.get(book_id)
    if market is None:
        market = by_ticker.get(pos.player_id)
    if market is None:
        return None
    market_window = str(market.get("window_id") or "")
    event_ticker = str(market.get("event_ticker") or "")
    if book_id and market_window and book_id == market_window:
        return market
    # No UTC bounds → window_id collapses to the event ticker.
    if book_id == event_ticker and market_window in {"", event_ticker}:
        return market
    return None


def _yes_ticket_won(kalshi_result: str) -> bool:
    return kalshi_result == "yes"


def settle_join_books(
    markets: list[dict[str, Any]],
    *,
    events: list[dict[str, Any]] | None = None,
) -> list[SettleJoinRow]:
    """Resolve 15m paper tickets from official Kalshi+SOURCE evidence only."""
    if TRADING_ARMED:
        raise RuntimeError("trading NOT ARMED")
    by_ticker = {str(m.get("ticker") or ""): m for m in markets if m.get("ticker")}
    by_window = {str(m.get("window_id") or ""): m for m in markets if m.get("window_id")}
    by_event = {str(e.get("event_ticker") or ""): e for e in (events or [])}
    rows: list[SettleJoinRow] = []
    ledger = load_ledger()
    for rec in iter_books():
        if rec.settled_at is not None:
            continue
        # One window book: settle only when every open ticket has official evidence.
        ticket_rows: list[SettleJoinRow] = []
        ready = True
        for pos in rec.book.positions:
            market = _market_for_book_position(pos, rec, by_ticker, by_window)
            event = _event_for_book(rec, market, by_event)
            if market is None:
                ticket_rows.append(
                    SettleJoinRow(
                        ticker=pos.player_id,
                        event_ticker=_event_ticker_from_book_id(rec.tournament_id),
                        window_id=str(rec.tournament_id or ""),
                        settle_status=SETTLE_PENDING,
                        banner="SETTLE_PENDING",
                        note=(
                            "SETTLE_PENDING: no Kalshi market payload for this window. "
                            "If close_time moved, the old window stays pending until "
                            "Kalshi result on this window_id. Hard NO invent."
                        ),
                    )
                )
                ready = False
                continue
            row = classify_settle(market, event=event)
            ticket_rows.append(row)
            if row.settle_status != SETTLE_SETTLED:
                ready = False
        rows.extend(ticket_rows)
        _write_join_artifact(rec.tournament_id, ticket_rows)
        if not ready or not rec.book.positions:
            continue
        _apply_official_settle(rec, ticket_rows, ledger)
        ledger = load_ledger()
    return rows


def _apply_official_settle(
    rec,
    ticket_rows: list[SettleJoinRow],
    ledger,
) -> None:
    by_ticker = {r.ticker: r for r in ticket_rows}
    bankroll_before = ledger.bankroll
    tickets: list[TicketResult] = []
    pnl_total = 0.0
    for pos in list(rec.book.positions):
        row = by_ticker[pos.player_id]
        won = _yes_ticket_won(row.kalshi_result)
        payout = round(pos.stake * pos.decimal_odds, 2) if won else 0.0
        pnl = round(payout - pos.stake, 2)
        pnl_total = round(pnl_total + pnl, 2)
        row.won = won
        row.pnl = pnl
        note = (
            f"{'HIT' if won else 'MISS'} kalshi_result={row.kalshi_result} "
            f"source={row.source_name} stake={pos.stake:.2f} @ {pos.decimal_odds:.2f} "
            f"payout={payout:.2f} pnl={pnl:+.2f}"
        )
        tickets.append(
            TicketResult(
                player_id=pos.player_id,
                player_name=pos.player_name,
                bet_type=pos.bet_type.value if hasattr(pos.bet_type, "value") else str(pos.bet_type),
                stake=pos.stake,
                decimal_odds=pos.decimal_odds,
                won=won,
                payout=payout,
                pnl=pnl,
                note=note,
            )
        )
        ledger.bankroll = round(ledger.bankroll + pnl, 2)
        ledger.entries.append(
            LedgerEntry(
                entry_id=new_id("led"),
                kind="settle_win" if won else "settle_loss",
                amount=pnl,
                bankroll_after=ledger.bankroll,
                event_id=rec.tournament_id,
                event_name=rec.tournament_name,
                player_name=pos.player_name,
                note=note,
            )
        )
    ledger.betting_pnl = round(ledger.betting_pnl + pnl_total, 2)
    week = EventWeek(
        event_id=rec.tournament_id,
        event_name=rec.tournament_name,
        winner_name=f"kalshi:{ticket_rows[0].kalshi_result}" if ticket_rows else "",
        tickets=tickets,
        betting_pnl=pnl_total,
        bankroll_before=bankroll_before,
        bankroll_after=ledger.bankroll,
        never_auto_bet=True,
    )
    ledger.events.append(week)
    save_ledger(ledger)
    rec.book = rec.book.model_copy(
        update={"positions": [], "realized_pnl_event": pnl_total, "bankroll": ledger.bankroll}
    )
    rec.settled_at = now()
    rec.settlement_pnl = pnl_total
    rec.settlement_winner = week.winner_name
    rec.bankroll = ledger.bankroll
    save_book(rec)


def _write_join_artifact(book_id: str, rows: list[SettleJoinRow]) -> Path:
    """Write one join file per window book. Top-level event_ticker is the event, not window_id."""
    event_ticker = ""
    window = str(book_id or "")
    for row in rows:
        if row.event_ticker:
            event_ticker = row.event_ticker
            break
        if row.window_id:
            window = row.window_id
    if not event_ticker:
        event_ticker = _event_ticker_from_book_id(book_id)
    if not window:
        window = str(book_id or event_ticker)
    dest = settlements_dir_15m() / f"{safe_artifact_stem(book_id)}.json"
    assert_not_golf_path(dest)
    dest.write_text(
        json.dumps(
            {
                "lane": LANE_15M,
                "series": PRIMARY_SERIES,
                "event_ticker": event_ticker,
                "window_id": window,
                "trading_armed": False,
                "digestor_source_hook": (
                    "Digestor owns SOURCE honesty digest later. "
                    "Official settle-rule SOURCE = Kalshi result matched to "
                    "CF Benchmarks settlement_sources + CRYPTO15M 60s RTI rule. "
                    "Do not invent Digestor docs."
                ),
                "rows": [r.model_dump() for r in rows],
                "as_of": now().isoformat(),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return dest
