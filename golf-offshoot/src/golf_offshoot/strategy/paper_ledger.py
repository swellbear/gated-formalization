"""Lifetime paper bankroll: deposits, withdrawals, weekend settlement. Never real money."""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, Field

from golf_offshoot.localtime import now

from golf_offshoot.models.enums import BetType, is_round_leader_bet
from golf_offshoot.models.strategy import new_id
from golf_offshoot.strategy.paper_book import PaperBookFile, load_paper_file, save_paper_book


class LedgerEntry(BaseModel):
    entry_id: str
    at: datetime = Field(default_factory=now)
    kind: str
    amount: float
    bankroll_after: float
    event_id: str = ""
    event_name: str = ""
    player_name: str = ""
    note: str = ""
    never_auto_bet: bool = True


class TicketResult(BaseModel):
    player_id: str = ""
    player_name: str
    bet_type: str
    stake: float
    decimal_odds: float
    finish: int | None = None
    won: bool
    payout: float
    pnl: float
    note: str = ""


class EventWeek(BaseModel):
    event_id: str
    event_name: str = ""
    settled_at: datetime = Field(default_factory=now)
    winner_id: str = ""
    winner_name: str = ""
    tickets: list[TicketResult] = Field(default_factory=list)
    moves_n: int = 0
    betting_pnl: float = 0.0
    bankroll_before: float = 0.0
    bankroll_after: float = 0.0
    deposits: float = 0.0
    withdrawals: float = 0.0
    never_auto_bet: bool = True


class PaperLedger(BaseModel):
    bankroll: float = 0.0
    starting_bankroll: float = 0.0
    deposits: float = 0.0
    withdrawals: float = 0.0
    betting_pnl: float = 0.0
    entries: list[LedgerEntry] = Field(default_factory=list)
    events: list[EventWeek] = Field(default_factory=list)
    never_auto_bet: bool = True
    paper_observation_only: bool = True


class SettleError(RuntimeError):
    """Event is not ready to settle, or already settled."""


class EventInspect(BaseModel):
    """ESPN (or test) snapshot used to decide whether an open book is finished."""

    completed: bool
    finishes: dict[str, tuple[int | None, str]] = Field(default_factory=dict)
    winner_ids: list[str] = Field(default_factory=list)
    event_name: str = ""
    status_note: str = ""


def ledger_path(path_id: str = "lived") -> Path:
    from golf_offshoot.strategy.paper_book import paper_dir

    if not path_id or path_id == "lived":
        return paper_dir() / "ledger.json"
    safe = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in str(path_id))
    return paper_dir() / f"ledger_{safe}.json"


def load_ledger(path_id: str = "lived") -> PaperLedger:
    path = ledger_path(path_id)
    if not path.is_file():
        return PaperLedger()
    return PaperLedger.model_validate_json(path.read_text(encoding="utf-8"))


def save_ledger(ledger: PaperLedger, path_id: str = "lived") -> Path:
    path = ledger_path(path_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(ledger.model_dump_json(indent=2), encoding="utf-8")
    return path


def _post(ledger: PaperLedger, kind: str, amount: float, **kwargs) -> LedgerEntry:
    ledger.bankroll = round(ledger.bankroll + amount, 2)
    entry = LedgerEntry(
        entry_id=new_id("led"),
        kind=kind,
        amount=round(amount, 2),
        bankroll_after=ledger.bankroll,
        **kwargs,
    )
    ledger.entries.append(entry)
    return entry


def ensure_opening_deposit(
    amount: float,
    *,
    event_id: str = "",
    event_name: str = "",
    note: str = "",
) -> PaperLedger:
    ledger = load_ledger()
    if ledger.entries:
        return ledger
    amt = round(float(amount), 2)
    ledger.starting_bankroll = amt
    ledger.deposits = amt
    _post(
        ledger,
        "deposit",
        amt,
        event_id=event_id,
        event_name=event_name,
        note=note or "opening paper bankroll",
    )
    save_ledger(ledger)
    return ledger


def record_deposit(
    amount: float, *, note: str = "", event_id: str = "", path_id: str = "lived"
) -> PaperLedger:
    amt = round(float(amount), 2)
    if amt <= 0:
        raise ValueError("deposit amount must be positive")
    if path_id and path_id != "lived":
        return _record_path_cash("deposit", amt, note=note or "paper deposit", event_id=event_id, path_id=path_id)
    ledger = load_ledger()
    if not ledger.entries:
        ledger.starting_bankroll = amt
    ledger.deposits = round(ledger.deposits + amt, 2)
    _post(ledger, "deposit", amt, event_id=event_id, note=note or "paper deposit")
    save_ledger(ledger)
    return ledger


def record_withdrawal(
    amount: float, *, note: str = "", event_id: str = "", path_id: str = "lived"
) -> PaperLedger:
    amt = round(float(amount), 2)
    if amt <= 0:
        raise ValueError("withdrawal amount must be positive")
    if path_id and path_id != "lived":
        return _record_path_cash("withdrawal", amt, note=note or "paper withdrawal", event_id=event_id, path_id=path_id)
    ledger = load_ledger()
    if amt > ledger.bankroll + 1e-9:
        raise ValueError(f"cannot withdraw ${amt:.2f}; paper bankroll is ${ledger.bankroll:.2f}")
    ledger.withdrawals = round(ledger.withdrawals + amt, 2)
    _post(ledger, "withdrawal", -amt, event_id=event_id, note=note or "paper withdrawal")
    save_ledger(ledger)
    return ledger


def _record_path_cash(
    kind: str,
    amount: float,
    *,
    note: str,
    event_id: str,
    path_id: str,
) -> PaperLedger:
    rec = _path_record(path_id, event_id)
    if rec is None:
        raise ValueError(
            f"no {path_id} paper book to {kind}. Pass --event <espn_id> after a lock, "
            "and use --book polymarket. This is not ledger.json."
        )
    cash = round(float(rec.bankroll) - rec.book.open_exposure, 2)
    if kind == "withdrawal" and amount > cash + 1e-9:
        raise ValueError(
            f"cannot withdraw ${amount:.2f}; {path_id} cash at cost is ${cash:.2f}"
        )
    delta = amount if kind == "deposit" else -amount
    stored = load_ledger(path_id)
    rec.bankroll = round(float(rec.bankroll) + delta, 2)
    rec.book.bankroll = rec.bankroll
    save_paper_book(rec)
    if kind == "deposit":
        stored.deposits = round(stored.deposits + amount, 2)
    else:
        stored.withdrawals = round(stored.withdrawals + amount, 2)
    stored.entries.append(
        LedgerEntry(
            entry_id=new_id("led"),
            kind=kind,
            amount=delta,
            bankroll_after=rec.bankroll,
            event_id=rec.tournament_id,
            event_name=rec.tournament_name,
            note=f"{note}. Independent {path_id} mock. Not ledger.json.",
        )
    )
    stored.bankroll = rec.bankroll
    save_ledger(stored, path_id)
    from golf_offshoot.strategy.paper_bankroll_export import overlay_path_cash

    return overlay_path_cash(rec, stored)


def _path_record(path_id: str, event_id: str = ""):
    if event_id:
        return load_paper_file(event_id, path_id=path_id)
    unsettled = [r for r in iter_compare_unsettled(path_id)]
    if unsettled:
        return max(unsettled, key=lambda r: r.locked_at)
    return None


def iter_compare_unsettled(path_id: str):
    from golf_offshoot.strategy.paper_book import iter_compare_paper_files

    for rec in iter_compare_paper_files():
        if (rec.path_id or "") != path_id:
            continue
        if rec.settled_at is None:
            yield rec


def cashout_recorded_for(movement_id: str) -> bool:
    """True if this paper movement already posted a cash-out ledger row."""
    if not movement_id:
        return False
    from golf_offshoot.strategy.cashout import (
        estimated_cashout_ledger_token,
        typed_cashout_ledger_token,
    )

    tokens = (
        estimated_cashout_ledger_token(movement_id),
        typed_cashout_ledger_token(movement_id),
    )
    ledger = load_ledger()
    for entry in ledger.entries:
        if entry.kind != "cashout":
            continue
        note = entry.note or ""
        if any(token in note for token in tokens):
            return True
    return False


def record_cashout(
    *,
    stake: float,
    cashout: float,
    event_id: str = "",
    event_name: str = "",
    player_name: str = "",
    note: str = "",
) -> PaperLedger:
    """Book P/L from a cash-out. Stake was already inside ledger bankroll at cost.

    `cashout` may be a typed Open Bets quote or an estimated offer. The note
    should include a movement token so the same sell cannot post twice.
    """
    pnl = round(float(cashout) - float(stake), 2)
    ledger = load_ledger()
    if not ledger.entries:
        return ledger
    ledger.betting_pnl = round(ledger.betting_pnl + pnl, 2)
    _post(
        ledger,
        "cashout",
        pnl,
        event_id=event_id,
        event_name=event_name,
        player_name=player_name,
        note=note or f"paper cash-out ${float(cashout):.2f} vs stake ${float(stake):.2f}",
    )
    save_ledger(ledger)
    return ledger


def event_already_settled(ledger: PaperLedger, event_id: str) -> bool:
    return any(w.event_id == str(event_id) for w in ledger.events)


def ticket_hit(bet_type: str, finish: int | None, winner_ids: set[str], player_id: str) -> bool:
    if finish is None:
        return False
    kind = (bet_type or "win").lower()
    if kind == BetType.WIN.value:
        return player_id in winner_ids
    if kind == BetType.TOP_5.value:
        return finish <= 5
    if kind == BetType.TOP_10.value:
        return finish <= 10
    if kind == BetType.TOP_20.value:
        return finish <= 20
    if kind == BetType.MAKE_CUT.value:
        return finish > 0
    if is_round_leader_bet(kind):
        return False
    return False


def _split_ticket_pnl(tickets: list[TicketResult]) -> tuple[float, float]:
    win = 0.0
    place = 0.0
    place_keys = {"top_5", "top_10", "top_20", "make_cut"}
    for t in tickets:
        if (t.bet_type or "win") in place_keys:
            place = round(place + t.pnl, 2)
        else:
            win = round(win + t.pnl, 2)
    return win, place


def settle_paper_event(
    event_id: str,
    *,
    finishes: dict[str, tuple[int | None, str]],
    completed: bool,
    status_note: str = "",
    winner_ids: list[str] | None = None,
    event_name: str = "",
) -> tuple[PaperLedger, PaperBookFile, EventWeek]:
    """Book mock P/L for remaining tickets. Does not place a real bet."""
    record = load_paper_file(event_id)
    if record is None:
        raise SettleError(f"no paper book locked for event {event_id}")
    if getattr(record, "settled_at", None):
        raise SettleError(f"event {event_id} already settled on the paper book")
    ledger = load_ledger()
    if event_already_settled(ledger, event_id):
        raise SettleError(f"event {event_id} already settled on the lifetime ledger")
    if not completed:
        raise SettleError(
            f"event is not final yet ({status_note or 'status unavailable'}). "
            "Do not invent a winner."
        )
    winners = set(winner_ids if winner_ids is not None else [
        pid for pid, (place, _n) in finishes.items() if place == 1
    ])
    if len(winners) != 1:
        raise SettleError(
            f"need exactly one official winner to settle win tickets; got {len(winners)}. "
            "Playoff unresolved stays unsettled."
        )
    winner_id = next(iter(winners))
    winner_name = finishes.get(winner_id, (None, winner_id))[1]
    bankroll_before = ledger.bankroll
    tickets: list[TicketResult] = []
    pnl_total = 0.0
    for pos in list(record.book.positions):
        place, _nm = finishes.get(pos.player_id, (None, pos.player_name))
        if is_round_leader_bet(pos.bet_type.value):
            payout = round(pos.stake, 2)
            pnl = 0.0
            won = False
            note = (
                f"VOID at cost; round-leader is not settled from 72-hole finish "
                f"stake={pos.stake:.2f} @ {pos.decimal_odds:.2f} payout={payout:.2f} pnl={pnl:+.2f}"
            )
        else:
            won = ticket_hit(pos.bet_type.value, place, winners, pos.player_id)
            payout = round(pos.stake * pos.decimal_odds, 2) if won else 0.0
            pnl = round(payout - pos.stake, 2)
            note = (
                f"{'HIT' if won else 'MISS'} finish={place if place is not None else 'n/a'} "
                f"stake={pos.stake:.2f} @ {pos.decimal_odds:.2f} payout={payout:.2f} pnl={pnl:+.2f}"
            )
        pnl_total = round(pnl_total + pnl, 2)
        tickets.append(
            TicketResult(
                player_id=pos.player_id,
                player_name=pos.player_name,
                bet_type=pos.bet_type.value,
                stake=pos.stake,
                decimal_odds=pos.decimal_odds,
                finish=place,
                won=won,
                payout=payout,
                pnl=pnl,
                note=note,
            )
        )
        _post(
            ledger,
            "settle_win" if won else ("settle_void" if is_round_leader_bet(pos.bet_type.value) else "settle_loss"),
            pnl,
            event_id=str(event_id),
            event_name=event_name or record.tournament_name,
            player_name=pos.player_name,
            note=note,
        )
    ledger.betting_pnl = round(ledger.betting_pnl + pnl_total, 2)
    week = EventWeek(
        event_id=str(event_id),
        event_name=event_name or record.tournament_name,
        winner_id=winner_id,
        winner_name=winner_name,
        tickets=tickets,
        moves_n=len(record.movements),
        betting_pnl=pnl_total,
        bankroll_before=bankroll_before,
        bankroll_after=ledger.bankroll,
        never_auto_bet=True,
    )
    ledger.events.append(week)
    save_ledger(ledger)
    record.book = record.book.model_copy(
        update={"positions": [], "realized_pnl_event": pnl_total}
    )
    record.settled_at = now()
    record.settlement_pnl = pnl_total
    win_pnl, place_pnl = _split_ticket_pnl(tickets)
    record.settlement_pnl_win = win_pnl
    record.settlement_pnl_place = place_pnl
    record.settlement_winner = winner_name
    record.bankroll = ledger.bankroll
    record.book = record.book.model_copy(update={"bankroll": ledger.bankroll})
    save_paper_book(record)
    return ledger, record, week


def settle_independent_compare_event(
    event_id: str,
    path_id: str,
    *,
    finishes: dict[str, tuple[int | None, str]],
    completed: bool,
    status_note: str = "",
    winner_ids: list[str] | None = None,
    event_name: str = "",
) -> PaperBookFile:
    """Settle one A/B book onto its own bankroll. Does not write ledger.json."""
    record = load_paper_file(event_id, path_id=path_id)
    if record is None:
        raise SettleError(f"no compare paper book {path_id} for event {event_id}")
    if getattr(record, "settled_at", None):
        raise SettleError(f"{path_id} event {event_id} already settled")
    if not completed:
        raise SettleError(
            f"event is not final yet ({status_note or 'status unavailable'}). "
            "Do not invent a winner."
        )
    winners = set(winner_ids if winner_ids is not None else [
        pid for pid, (place, _n) in finishes.items() if place == 1
    ])
    if len(winners) != 1:
        raise SettleError(
            f"need exactly one official winner to settle win tickets; got {len(winners)}. "
            "Playoff unresolved stays unsettled."
        )
    winner_id = next(iter(winners))
    winner_name = finishes.get(winner_id, (None, winner_id))[1]
    tickets: list[TicketResult] = []
    pnl_total = 0.0
    for pos in list(record.book.positions):
        place, _nm = finishes.get(pos.player_id, (None, pos.player_name))
        if is_round_leader_bet(pos.bet_type.value):
            won = False
            payout = round(pos.stake, 2)
            pnl = 0.0
        else:
            won = ticket_hit(pos.bet_type.value, place, winners, pos.player_id)
            payout = round(pos.stake * pos.decimal_odds, 2) if won else 0.0
            pnl = round(payout - pos.stake, 2)
        pnl_total = round(pnl_total + pnl, 2)
        tickets.append(
            TicketResult(
                player_id=pos.player_id,
                player_name=pos.player_name,
                bet_type=pos.bet_type.value,
                stake=pos.stake,
                decimal_odds=pos.decimal_odds,
                finish=place,
                won=won,
                payout=payout,
                pnl=pnl,
            )
        )
    win_pnl, place_pnl = _split_ticket_pnl(tickets)
    bankroll_after = round(float(record.bankroll) + pnl_total, 2)
    record.book = record.book.model_copy(
        update={"positions": [], "realized_pnl_event": pnl_total, "bankroll": bankroll_after}
    )
    record.settled_at = now()
    record.settlement_pnl = pnl_total
    record.settlement_pnl_win = win_pnl
    record.settlement_pnl_place = place_pnl
    record.settlement_winner = winner_name
    record.bankroll = bankroll_after
    save_paper_book(record)
    return record


def other_open_exposure(*, except_event_id: str | None = None) -> float:
    """Stake still at cost on unsettled books other than this event."""
    from golf_offshoot.strategy.paper_book import unsettled_paper_files

    total = 0.0
    for rec in unsettled_paper_files():
        if except_event_id and str(rec.tournament_id) == str(except_event_id):
            continue
        total += rec.book.open_exposure
    return round(total, 2)


def working_bankroll(*, except_event_id: str | None = None) -> float:
    """Ledger bankroll minus other events' open tickets. Next week's caps use this."""
    ledger = load_ledger()
    return round(max(0.0, ledger.bankroll - other_open_exposure(except_event_id=except_event_id)), 2)


def inspect_espn_event(event_id: str, *, refresh: bool = False) -> EventInspect:
    from golf_offshoot.data_feeds.espn import (
        EspnClient,
        event_completed,
        event_finish_table,
        official_winner_ids,
        parse_event_payload,
    )

    client = EspnClient(refresh=refresh)
    payload = client.event_leaderboard(str(event_id), live=True)
    event = parse_event_payload(payload)
    done, status_note = event_completed(event)
    finishes = event_finish_table(event)
    winners = official_winner_ids(finishes)
    name = str(event.get("name") or event.get("shortName") or "")
    return EventInspect(
        completed=done,
        finishes=finishes,
        winner_ids=winners,
        event_name=name,
        status_note=status_note,
    )


def fetch_and_settle(event_id: str, *, refresh: bool = False) -> tuple[PaperLedger, PaperBookFile, EventWeek]:
    info = inspect_espn_event(event_id, refresh=refresh)
    return settle_paper_event(
        str(event_id),
        finishes=info.finishes,
        completed=info.completed,
        status_note=info.status_note,
        winner_ids=info.winner_ids,
        event_name=info.event_name,
    )


def settle_finished_open_books(
    *,
    refresh: bool = False,
    inspect_event: Callable[..., EventInspect] | None = None,
) -> tuple[
    list[tuple[PaperLedger, PaperBookFile, EventWeek]],
    list[tuple[PaperBookFile, str]],
]:
    """Settle every open paper book ESPN (or inspect_event) shows as clearly finished.

    Does not invent a winner. Playoff / not-final / inspect failure leaves the book open.
    """
    from golf_offshoot.strategy.paper_book import unsettled_paper_files

    look = inspect_event or inspect_espn_event
    settled: list[tuple[PaperLedger, PaperBookFile, EventWeek]] = []
    skipped: list[tuple[PaperBookFile, str]] = []
    for rec in unsettled_paper_files():
        try:
            info = look(rec.tournament_id, refresh=refresh)
        except TypeError:
            try:
                info = look(rec.tournament_id)
            except Exception as exc:
                skipped.append((rec, f"could not inspect ESPN ({exc})"))
                continue
        except Exception as exc:
            skipped.append((rec, f"could not inspect ESPN ({exc})"))
            continue
        try:
            result = settle_paper_event(
                rec.tournament_id,
                finishes=info.finishes,
                completed=info.completed,
                status_note=info.status_note,
                winner_ids=info.winner_ids,
                event_name=info.event_name or rec.tournament_name,
            )
            settled.append(result)
        except SettleError as exc:
            skipped.append((rec, str(exc)))
    from golf_offshoot.strategy.paper_book import unsettled_compare_paper_files

    for rec in unsettled_compare_paper_files():
        try:
            info = look(rec.tournament_id, refresh=refresh)
        except TypeError:
            try:
                info = look(rec.tournament_id)
            except Exception as exc:
                skipped.append((rec, f"could not inspect ESPN ({exc})"))
                continue
        except Exception as exc:
            skipped.append((rec, f"could not inspect ESPN ({exc})"))
            continue
        try:
            settle_independent_compare_event(
                rec.tournament_id,
                rec.path_id,
                finishes=info.finishes,
                completed=info.completed,
                status_note=info.status_note,
                winner_ids=info.winner_ids,
                event_name=info.event_name or rec.tournament_name,
            )
        except SettleError as exc:
            skipped.append((rec, str(exc)))
    return settled, skipped


def format_ledger(ledger: PaperLedger, *, week: EventWeek | None = None) -> str:
    lines = [
        f"PAPER LEDGER  bankroll=${ledger.bankroll:.2f}  never_auto_bet=true",
        f"starting ${ledger.starting_bankroll:.2f}  deposits ${ledger.deposits:.2f}  "
        f"withdrawals ${ledger.withdrawals:.2f}  betting P/L ${ledger.betting_pnl:+.2f}",
    ]
    if week:
        lines.append("")
        lines.append(
            f"WEEK {week.event_name or week.event_id}  winner={week.winner_name or 'n/a'}  "
            f"P/L ${week.betting_pnl:+.2f}  {week.bankroll_before:.2f} -> {week.bankroll_after:.2f}"
        )
        for t in week.tickets:
            lines.append(
                f"  {'WIN' if t.won else 'LOSS'} {t.player_name} {t.bet_type} "
                f"${t.stake:.2f} @ {t.decimal_odds:.2f} finish={t.finish if t.finish is not None else 'n/a'} "
                f"payout=${t.payout:.2f} pnl={t.pnl:+.2f}"
            )
    if ledger.events:
        lines.append("")
        lines.append("Lifetime events")
        for ev in ledger.events:
            lines.append(
                f"  {ev.event_name or ev.event_id}  P/L ${ev.betting_pnl:+.2f}  "
                f"bankroll ${ev.bankroll_after:.2f}"
            )
    lines.append("Paper / mock. Observation only. The system never auto-bets.")
    return "\n".join(lines)
