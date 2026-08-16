"""Independent $20k paper books. Never auto-trade. Per field per path."""

from __future__ import annotations

import json
from pathlib import Path
from uuid import uuid4

from options_offshoot.compare.law import METHOD_LAW_V1, law_hash
from options_offshoot.compare.paths import config_for, ledger_id
from options_offshoot.config import PAPER_DIR
from options_offshoot.data_feeds.local_env import package_root
from options_offshoot.localtime import now
from options_offshoot.models.enums import AdviceKind, ComparePath
from options_offshoot.models.schemas import (
    FieldRun,
    PaperBookFile,
    PaperMovement,
    PaperPosition,
)
from options_offshoot.ranking.rank import clears_screen


def paper_dir() -> Path:
    d = package_root() / PAPER_DIR
    d.mkdir(parents=True, exist_ok=True)
    return d


def paper_path(field_id: str, path_id: str) -> Path:
    return paper_dir() / f"{field_id}_{path_id}.json"


def load_paper_file(field_id: str, path_id: str) -> PaperBookFile | None:
    path = paper_path(field_id, path_id)
    if not path.is_file():
        return None
    return PaperBookFile.model_validate_json(path.read_text(encoding="utf-8"))


def save_paper_book(record: PaperBookFile) -> Path:
    path = paper_path(record.field_id, record.path_id.value)
    path.write_text(record.model_dump_json(indent=2), encoding="utf-8")
    return path


def starting_bankroll() -> float:
    return float(METHOD_LAW_V1["independent_compare_bankroll"])


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
    positions: list[PaperPosition] = []
    cash = start
    unit = min(250.0, start * 0.01)
    for row in run.rows:
        if not clears_screen(row, cfg.ticket_screen):
            continue
        if cash < unit:
            break
        cash -= unit
        c = row.contract
        positions.append(
            PaperPosition(
                position_id=uuid4().hex[:12],
                contract_id=c.contract_id,
                underlying=c.underlying,
                expiry=c.expiry,
                strike=c.strike,
                contract_type=c.contract_type,
                stake=unit,
                entry_ask=c.quote.ask,
                entry_fair=row.model.fair,
            )
        )
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
        positions=positions,
        method_law_hash=law_hash(),
        notes=["paper lock; never auto-trade", f"screen={cfg.ticket_screen}"],
    )
    rec.last_advice = [
        PaperMovement(
            kind=AdviceKind.NEW,
            contract_id=p.contract_id,
            underlying=p.underlying,
            amount=p.stake,
            reason="lock",
        )
        for p in positions
    ]
    if write:
        save_paper_book(rec)
    return rec


def advice_for_book(record: PaperBookFile, run: FieldRun) -> list[PaperMovement]:
    by_id = {r.contract.contract_id: r for r in run.rows}
    out: list[PaperMovement] = []
    for pos in record.positions:
        row = by_id.get(pos.contract_id)
        if row is None:
            out.append(
                PaperMovement(
                    kind=AdviceKind.HOLD,
                    contract_id=pos.contract_id,
                    underlying=pos.underlying,
                    reason="No live row; ride to expiry. Not a cash-out.",
                )
            )
            continue
        if not row.contract.quote.has_real_ask:
            out.append(
                PaperMovement(
                    kind=AdviceKind.HOLD,
                    contract_id=pos.contract_id,
                    underlying=pos.underlying,
                    reason="No live ask; ride to expiry. Not a cash-out.",
                )
            )
            continue
        if row.n_a_reason and row.model.fair is None:
            out.append(
                PaperMovement(
                    kind=AdviceKind.HOLD,
                    contract_id=pos.contract_id,
                    underlying=pos.underlying,
                    reason="Model unconstrained; ride to expiry.",
                )
            )
            continue
        if row.vs_ask is not None and row.vs_ask < 0 and row.clears_ask is False:
            if pos.entry_fair is not None and row.model.fair is not None:
                if row.model.fair < 0.3 * pos.entry_fair:
                    out.append(
                        PaperMovement(
                            kind=AdviceKind.SELL,
                            contract_id=pos.contract_id,
                            underlying=pos.underlying,
                            amount=pos.stake,
                            reason="Original edge has collapsed",
                        )
                    )
                    continue
        out.append(
            PaperMovement(
                kind=AdviceKind.HOLD,
                contract_id=pos.contract_id,
                underlying=pos.underlying,
                reason="Original edge is still intact; no path reason to change size",
            )
        )
    return out


def actionable(advice: list[PaperMovement]) -> list[PaperMovement]:
    return [a for a in advice if a.kind != AdviceKind.HOLD]


def apply_advice(record: PaperBookFile, advice: list[PaperMovement]) -> PaperBookFile:
    """Mock apply only. Never a real trade."""
    if not actionable(advice):
        record.last_advice = advice
        return record
    keep = []
    cash = record.cash
    by_move = {a.contract_id: a for a in advice}
    for pos in record.positions:
        mv = by_move.get(pos.contract_id)
        if mv is not None and mv.kind in (AdviceKind.SELL, AdviceKind.EXIT):
            cash += pos.stake  # ride-to-expiry collapse books stake back at cost if no quote
            continue
        keep.append(pos)
    record.positions = keep
    record.cash = cash
    record.bankroll = cash + sum(p.stake for p in keep)
    record.last_advice = advice
    record.notes.append("applied paper advice (mock only; never auto-trade)")
    save_paper_book(record)
    return record


def trigger_lines(advice: list[PaperMovement]) -> list[str]:
    sells = [a for a in advice if a.kind in (AdviceKind.SELL, AdviceKind.EXIT)]
    holds = [a for a in advice if a.kind == AdviceKind.HOLD]
    news = [a for a in advice if a.kind == AdviceKind.NEW]
    adds = [a for a in advice if a.kind == AdviceKind.ADD]
    if not sells and not news and not adds:
        head = "NOTHING TO PULL — all HOLD"
    else:
        n = len(sells) + len(news) + len(adds)
        head = f"PULL — {n}"
    lines = [head, ""]
    if sells:
        lines.append("SELL")
        for a in sells:
            lines.append(f"  {a.underlying}  {a.contract_id}  ${a.amount:.2f}")
        lines.append("")
    if news:
        lines.append("NEW")
        for a in news:
            lines.append(f"  {a.underlying}  {a.contract_id}  ${a.amount:.2f}")
        lines.append("")
    if holds:
        lines.append("HOLD")
        for a in holds:
            lines.append(f"  {a.underlying}  {a.contract_id}")
    lines.append("")
    lines.append("This snapshot only. Mock. Never auto-trade.")
    return lines
