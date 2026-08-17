"""Batch pack + 00_full_readout.pdf. Open in Edge/Chrome/Adobe."""

from __future__ import annotations

from pathlib import Path

from options_offshoot.compare.law import law_hash
from options_offshoot.config import EXPORT_DIR
from options_offshoot.data_feeds.local_env import package_root
from options_offshoot.fields.catalog import INDEX_MAP_DISCLAIMER
from options_offshoot.localtime import filename_stamp
from options_offshoot.models.schemas import FieldRun, PaperBookFile
from options_offshoot.ranking.export_table import _write_pdf, format_table
from options_offshoot.strategy.paper_book import advice_for_book
from options_offshoot.strategy.paper_trigger import trigger_document


def pack_dir(field_id: str, run_id: str, *, batch: bool) -> Path:
    root = package_root() / EXPORT_DIR / "packs"
    root.mkdir(parents=True, exist_ok=True)
    suffix = "_batch" if batch else ""
    d = root / f"{field_id}_{filename_stamp()}_{run_id}{suffix}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def write_section(folder: Path, stem: str, title: str, text: str) -> None:
    (folder / f"{stem}.txt").write_text(text, encoding="utf-8")
    (folder / f"{stem}.html").write_text(
        f"<!DOCTYPE html><html><body><pre>{_esc(text)}</pre></body></html>",
        encoding="utf-8",
    )
    _write_pdf(folder / f"{stem}.pdf", title, text)


def _esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;")


def _why_bets(run: FieldRun, rec: PaperBookFile | None) -> str:
    lines = [
        f"WHY-BETS  {run.field_id}",
        f"law_hash={law_hash()}",
        "vs-ask = model fair minus venue ask. Mid is never a cash-out.",
        "never_auto_trade=true",
        "",
    ]
    if rec is None or not rec.positions:
        lines.append("(no book)")
        return "\n".join(lines)
    by_id = {r.contract.contract_id: r for r in run.rows}
    for p in rec.positions:
        if p.settled:
            continue
        row = by_id.get(p.contract_id)
        vs = "n/a" if row is None or row.vs_ask is None else f"{row.vs_ask:+.3f}"
        lines.append(
            f"  {p.underlying} {p.contract_type.value} {p.strike} {p.expiry} "
            f"n={p.n_contracts} stake=${p.stake:.2f} entry_ask={p.entry_ask} "
            f"venue={p.quote_venue.value} vs_ask={vs}"
        )
        if row is not None and row.model.default_sigma:
            lines.append("    flag=default_sigma (A-path fill; ask bar decides)")
    return "\n".join(lines)


def write_live_pack(
    *,
    run: FieldRun,
    lived: PaperBookFile | None,
    leftover: str,
    advice: list | None = None,
) -> Path:
    folder = pack_dir(run.field_id, run.run_id, batch=False)
    moves = advice if advice is not None else (lived.last_advice if lived else [])
    trigger = trigger_document(moves, field_id=run.field_id)
    how = "\n".join(
        [
            "HOW TO READ",
            INDEX_MAP_DISCLAIMER,
            "Sort is vs-ask, not P(ITM). n/a is not a fake mid.",
            "Settle at expiry. HOLD with no bid rides to expiry, not edge intact.",
            "Never auto-trade.",
            f"law_hash={law_hash()}",
        ]
    )
    write_section(folder, "00_trigger", "Trigger", trigger)
    write_section(folder, "01_how_to_read", "How to read", how)
    write_section(folder, "02_field", "Field table", format_table(run))
    write_section(folder, "03_why_bets", "Why bets", _why_bets(run, lived))
    write_section(folder, "04_leftover", "Leftover", leftover)
    write_section(folder, "05_book", "Lived book", _book_text("lived", lived))
    _concat(folder, run.field_id)
    return folder


def write_batch_pack(
    *,
    run: FieldRun,
    lived: PaperBookFile | None,
    books: dict[str, PaperBookFile | None],
    fights: str,
    leftover: str,
    guts: FieldRun | None = None,
) -> Path:
    folder = pack_dir(run.field_id, run.run_id, batch=True)
    advice = []
    if lived is not None:
        advice = lived.last_advice or advice_for_book(lived, run)
    trigger = trigger_document(advice, field_id=run.field_id)
    how = "\n".join(
        [
            "HOW TO READ",
            INDEX_MAP_DISCLAIMER,
            "Lived / A-replay / B-guts / B-nerves / B-full are separate $20k books.",
            "Compare does not lock lived and does not write the lived ledger.",
            "Sort is vs-ask, not P(ITM). n/a is not a fake mid.",
            "A-control ticket bar is mid. Lived/B-nerves/B-full are ask.",
            "Settle at expiry. Never auto-trade.",
            f"law_hash={law_hash()}",
        ]
    )
    write_section(folder, "00_trigger", "Trigger", trigger)
    write_section(folder, "01_how_to_read", "How to read", how)
    write_section(folder, "02_fights", "Fights", fights)
    write_section(folder, "03_field", "Field table", format_table(run))
    write_section(folder, "04_why_bets", "Why bets", _why_bets(run, lived or books.get("a_replay")))
    write_section(folder, "05_leftover", "Leftover", leftover)
    order = ["lived", "a_replay", "b_guts", "b_nerves", "b_full"]
    for i, pid in enumerate(order, start=6):
        rec = books.get(pid)
        write_section(folder, f"{i:02d}_{pid}", pid, _book_text(pid, rec))
    bank = _book_text("lived_bankroll", lived)
    write_section(folder, "11_bankroll", "Bankroll", bank)
    readme = (
        f"Compare batch pack — {run.field_id}\n"
        "Mock / paper. Not real money. Never auto-trades.\n"
        "Open PDFs in Edge, Chrome, or Adobe — not as source in the editor.\n"
        f"law_hash={law_hash()}\n"
        f"{INDEX_MAP_DISCLAIMER}\n"
    )
    (folder / "00_README.txt").write_text(readme, encoding="utf-8")
    _concat(folder, run.field_id)
    return folder


def _concat(folder: Path, field_id: str) -> None:
    combo = []
    for p in sorted(folder.glob("*.txt")):
        if p.name in ("00_README.txt", "00_full_readout.txt"):
            continue
        combo.append(p.read_text(encoding="utf-8"))
        combo.append("\n\n")
    full = "".join(combo)
    _write_pdf(folder / "00_full_readout.pdf", f"{field_id} full readout", full)
    (folder / "00_full_readout.txt").write_text(full, encoding="utf-8")


def _book_text(pid: str, rec: PaperBookFile | None) -> str:
    if rec is None:
        return f"{pid}\n(empty)\nnever_auto_trade=true\nlaw_hash={law_hash()}\n"
    lines = [
        f"{pid}  field={rec.field_id}",
        f"locked_at={rec.locked_at} run={rec.locked_from_run_id} identity={rec.lock_identity}",
        f"open ${sum(p.stake for p in rec.positions if not p.settled):.2f} / ${rec.bankroll:.2f} "
        f"(started ${rec.starting_bankroll:.0f}) n={sum(1 for p in rec.positions if not p.settled)}",
        f"posted_ask_pnl={rec.posted_ask_pnl} expiry_settle_pnl={rec.expiry_settle_pnl}",
        f"venue_pin={rec.quote_venue_pin.value} law_hash={rec.method_law_hash or law_hash()}",
        "never_auto_trade=true  paper/mock only",
        "",
    ]
    for p in rec.positions:
        flag = " SETTLED" if p.settled else ""
        lines.append(
            f"  {p.underlying} {p.contract_type.value} {p.strike} {p.expiry} "
            f"n={p.n_contracts} ${p.stake:.2f} ask={p.entry_ask} "
            f"open_ask={p.opening_ask} venue={p.quote_venue.value}{flag}"
        )
    return "\n".join(lines)
