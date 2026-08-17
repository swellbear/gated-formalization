"""Independent $20k paper books. Never auto-trade. Per field per path."""

from __future__ import annotations

import hashlib
from uuid import uuid4

from options_offshoot.compare.law import METHOD_LAW_V1, law_hash
from options_offshoot.compare.paths import config_for, ledger_id
from options_offshoot.config import PAPER_DIR
from options_offshoot.data_feeds.local_env import package_root
from options_offshoot.localtime import now
from options_offshoot.models.enums import AdviceKind, ComparePath, QuoteVenue, StrategyMode
from options_offshoot.models.schemas import (
    FieldRun,
    PaperBookFile,
    PaperLedgerLine,
    PaperMovement,
    PaperPosition,
)
from options_offshoot.ranking.rank import clears_screen
from options_offshoot.strategy.engine import recommend
from options_offshoot.strategy.sizing import size_new


def paper_dir():
    d = package_root() / PAPER_DIR
    d.mkdir(parents=True, exist_ok=True)
    return d


def paper_path(field_id: str, path_id: str):
    return paper_dir() / f"{field_id}_{path_id}.json"


def load_paper_file(field_id: str, path_id: str) -> PaperBookFile | None:
    path = paper_path(field_id, path_id)
    if not path.is_file():
        return None
    return PaperBookFile.model_validate_json(path.read_text(encoding="utf-8"))


def save_paper_book(record: PaperBookFile):
    path = paper_path(record.field_id, record.path_id.value)
    path.write_text(record.model_dump_json(indent=2), encoding="utf-8")
    return path


def starting_bankroll() -> float:
    return float(METHOD_LAW_V1["independent_compare_bankroll"])


def make_lock_identity(record: PaperBookFile) -> str:
    ids = ",".join(sorted(p.contract_id for p in record.positions))
    raw = f"{record.field_id}|{record.path_id.value}|{record.locked_at}|{ids}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]


def lock_paper_positions(
    run: FieldRun,
    *,
    path: ComparePath,
    run_id: str,
    write: bool = True,
) -> PaperBookFile:
    cfg = config_for(path)
    start = starting_bankroll()
    existing = load_paper_file(run.field_id, ledger_id(path))
    if existing is not None and existing.locked_at is not None:
        existing.notes.append("lock frozen; live apply still mutates")
        return existing
    venue = QuoteVenue(str(run.extra.get("quote_venue") or QuoteVenue.POLYGON.value))
    if venue == QuoteVenue.MOCK:
        venue = QuoteVenue.POLYGON
    positions: list[PaperPosition] = []
    cash = start
    leftover: list[str] = []
    book = PaperBookFile(
        field_id=run.field_id,
        path_id=ComparePath(ledger_id(path)),
        event_name=run.field_id,
        bankroll=start,
        cash=cash,
        starting_bankroll=start,
        quote_venue_pin=venue,
        method_law_hash=law_hash(),
    )
    for row in run.rows:
        if not clears_screen(row, cfg.ticket_screen):
            continue
        n, stake, block = size_new(
            row, book, bankroll=start, cash=cash, leftover=leftover
        )
        if block or n < 1:
            continue
        cash -= stake
        c = row.contract
        positions.append(
            PaperPosition(
                position_id=uuid4().hex[:12],
                contract_id=c.contract_id,
                underlying=c.underlying,
                expiry=c.expiry,
                strike=c.strike,
                contract_type=c.contract_type,
                stake=stake,
                n_contracts=n,
                multiplier=c.multiplier,
                entry_ask=c.quote.ask,
                opening_ask=c.opening_ask if c.opening_ask is not None else c.quote.ask,
                entry_fair=row.model.fair,
                quote_venue=c.quote_venue if c.quote_venue != QuoteVenue.MOCK else venue,
            )
        )
        book.positions = positions
        book.cash = cash
    rec = PaperBookFile(
        field_id=run.field_id,
        path_id=ComparePath(ledger_id(path)),
        event_name=run.field_id,
        locked_at=now(),
        locked_from_run_id=run_id,
        bankroll=cash + sum(p.stake for p in positions),
        cash=cash,
        starting_bankroll=start,
        never_auto_trade=True,
        quote_venue_pin=venue,
        positions=positions,
        method_law_hash=law_hash(),
        notes=["paper lock; never auto-trade", f"screen={cfg.ticket_screen}", *leftover],
    )
    rec.lock_identity = make_lock_identity(rec)
    rec.last_advice = [
        PaperMovement(
            kind=AdviceKind.NEW,
            contract_id=p.contract_id,
            underlying=p.underlying,
            amount=p.stake,
            n_contracts=p.n_contracts,
            reason="lock",
        )
        for p in positions
    ]
    if write:
        save_paper_book(rec)
    return rec


def advice_for_book(
    record: PaperBookFile,
    run: FieldRun,
    *,
    cash_out: dict[str, float] | None = None,
    mode: StrategyMode | None = None,
) -> list[PaperMovement]:
    from options_offshoot.compare.paths import config_for as _cfg

    cfg = _cfg(record.path_id)
    leftover: list[str] = []
    moves = recommend(
        run,
        record,
        screen=cfg.ticket_screen,
        mode=mode or StrategyMode.STAY_SELECTIVE,
        cash_out=cash_out,
        leftover=leftover,
    )
    record.notes.extend(leftover)
    return moves


def actionable(advice: list[PaperMovement]) -> list[PaperMovement]:
    return [a for a in advice if a.kind != AdviceKind.HOLD]


def apply_advice(
    record: PaperBookFile,
    advice: list[PaperMovement],
    run: FieldRun | None = None,
) -> PaperBookFile:
    """Mock apply only. Never a real trade."""
    if not actionable(advice):
        record.last_advice = advice
        return record
    by_row = {r.contract.contract_id: r for r in (run.rows if run else [])}
    keep = {p.contract_id: p for p in record.positions if not p.settled}
    cash = record.cash

    def _new_pos(mv: PaperMovement) -> PaperPosition | None:
        row = by_row.get(mv.contract_id)
        if row is None:
            return None
        c = row.contract
        return PaperPosition(
            position_id=uuid4().hex[:12],
            contract_id=c.contract_id,
            underlying=c.underlying,
            expiry=c.expiry,
            strike=c.strike,
            contract_type=c.contract_type,
            stake=mv.amount,
            n_contracts=mv.n_contracts,
            multiplier=c.multiplier,
            entry_ask=c.quote.ask,
            opening_ask=c.opening_ask if c.opening_ask is not None else c.quote.ask,
            entry_fair=row.model.fair,
            quote_venue=record.quote_venue_pin,
        )

    for mv in advice:
        if mv.kind in (AdviceKind.SELL, AdviceKind.EXIT):
            pos = keep.pop(mv.contract_id, None)
            if pos is None:
                continue
            cash += mv.amount if mv.amount else pos.stake
            continue
        if mv.kind == AdviceKind.REDUCE:
            pos = keep.get(mv.contract_id)
            if pos is None or mv.n_contracts <= 0:
                continue
            sold = min(max(pos.n_contracts - 1, 0), mv.n_contracts)
            if sold <= 0:
                continue
            frac = sold / pos.n_contracts
            cash += mv.amount if mv.amount else pos.stake * frac
            pos.n_contracts -= sold
            pos.stake = pos.stake * (1.0 - frac)
            continue
        if mv.kind == AdviceKind.ADD:
            pos = keep.get(mv.contract_id)
            if pos is None or mv.n_contracts <= 0 or cash < mv.amount:
                continue
            cash -= mv.amount
            pos.n_contracts += mv.n_contracts
            pos.stake += mv.amount
            continue
        if mv.kind == AdviceKind.NEW:
            if mv.n_contracts <= 0 or cash < mv.amount:
                continue
            pos = _new_pos(mv)
            if pos is None:
                continue
            cash -= mv.amount
            keep[mv.contract_id] = pos
            continue
        if mv.kind == AdviceKind.REALLOCATE:
            src = keep.pop(mv.from_contract_id, None)
            if src is not None:
                cash += src.stake
            if mv.n_contracts > 0 and cash >= mv.amount:
                pos = _new_pos(mv)
                if pos is None:
                    if src is not None:
                        keep[src.contract_id] = src
                        cash -= src.stake
                    continue
                cash -= mv.amount
                keep[mv.contract_id] = pos
    settled = [p for p in record.positions if p.settled]
    record.positions = settled + list(keep.values())
    record.cash = cash
    record.bankroll = cash + sum(p.stake for p in record.positions if not p.settled)
    record.last_advice = advice
    record.notes.append("applied paper advice (mock only; never auto-trade)")
    save_paper_book(record)
    return record


def deposit(record: PaperBookFile, amount: float, note: str = "") -> PaperBookFile:
    amt = float(amount)
    record.cash += amt
    record.bankroll += amt
    record.starting_bankroll += amt
    record.ledger.append(PaperLedgerLine(kind="deposit", amount=amt, note=note or "paper-deposit"))
    save_paper_book(record)
    return record


def withdraw(record: PaperBookFile, amount: float, note: str = "") -> PaperBookFile:
    amt = float(amount)
    if amt > record.cash + 1e-9:
        raise ValueError(f"withdraw ${amt:.2f} exceeds cash ${record.cash:.2f}")
    record.cash -= amt
    record.bankroll -= amt
    record.starting_bankroll -= amt
    record.ledger.append(PaperLedgerLine(kind="withdraw", amount=-amt, note=note or "paper-withdraw"))
    save_paper_book(record)
    return record


def mark_scores(record: PaperBookFile, run: FieldRun | None) -> PaperBookFile:
    by_id = {r.contract.contract_id: r for r in (run.rows if run else [])}
    posted = 0.0
    have = False
    for pos in record.positions:
        if pos.settled:
            continue
        row = by_id.get(pos.contract_id)
        if row is None or not row.contract.quote.has_real_ask or pos.n_contracts <= 0:
            continue
        have = True
        mark = float(row.contract.quote.ask) * int(pos.multiplier) * int(pos.n_contracts)
        posted += mark - pos.stake
    record.posted_ask_pnl = posted if have else None
    settled = [p.settle_pnl for p in record.positions if p.settled and p.settle_pnl is not None]
    record.expiry_settle_pnl = sum(settled) if settled else None
    return record


def trigger_lines(advice: list[PaperMovement]) -> list[str]:
    from options_offshoot.strategy.paper_trigger import trigger_lines as _lines

    return _lines(advice)
