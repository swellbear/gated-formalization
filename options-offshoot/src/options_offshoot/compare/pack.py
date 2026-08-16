"""Batch pack + 00_full_readout.pdf. Open in Edge/Chrome/Adobe."""

from __future__ import annotations

from pathlib import Path

from options_offshoot.compare.fights import fights_document
from options_offshoot.compare.law import law_hash
from options_offshoot.config import EXPORT_DIR
from options_offshoot.data_feeds.local_env import package_root
from options_offshoot.fields.catalog import INDEX_MAP_DISCLAIMER
from options_offshoot.leftover import format_leftover_callout
from options_offshoot.localtime import filename_stamp
from options_offshoot.models.schemas import FieldRun, PaperBookFile
from options_offshoot.ranking.export_table import _write_pdf, format_table
from options_offshoot.strategy.paper_book import trigger_lines


def pack_dir(field_id: str, run_id: str) -> Path:
    root = package_root() / EXPORT_DIR / "packs"
    root.mkdir(parents=True, exist_ok=True)
    d = root / f"{field_id}_{filename_stamp()}_{run_id}_batch"
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


def write_batch_pack(
    *,
    run: FieldRun,
    lived: PaperBookFile | None,
    books: dict[str, PaperBookFile | None],
    fights: str,
    leftover: str,
) -> Path:
    folder = pack_dir(run.field_id, run.run_id)
    advice = lived.last_advice if lived else []
    trigger = "TRIGGER  " + run.field_id + "\n" + "\n".join(trigger_lines(advice))
    how = "\n".join(
        [
            "HOW TO READ",
            INDEX_MAP_DISCLAIMER,
            "Lived / A-replay / B-guts / B-nerves / B-full are separate $20k books.",
            "Sort is vs-ask, not P(ITM). n/a is not a fake mid.",
            "Settle at expiry. Never auto-trade.",
            f"law_hash={law_hash()}",
        ]
    )
    write_section(folder, "00_trigger", "Trigger", trigger)
    write_section(folder, "01_how_to_read", "How to read", how)
    write_section(folder, "02_fights", "Fights", fights)
    write_section(folder, "03_field", "Field table", format_table(run))
    write_section(folder, "04_leftover", "Leftover", leftover)
    order = ["lived", "a_replay", "b_guts", "b_nerves", "b_full"]
    for i, pid in enumerate(order, start=5):
        rec = books.get(pid)
        text = _book_text(pid, rec)
        write_section(folder, f"{i:02d}_{pid}", pid, text)
    readme = (
        f"Compare batch pack — {run.field_id}\n"
        "Mock / paper. Not real money. Never auto-trades.\n"
        "Open PDFs in Edge, Chrome, or Adobe — not as source in the editor.\n"
        f"{INDEX_MAP_DISCLAIMER}\n"
    )
    (folder / "00_README.txt").write_text(readme, encoding="utf-8")
    combo = []
    for p in sorted(folder.glob("*.txt")):
        if p.name in ("00_README.txt",):
            continue
        combo.append(p.read_text(encoding="utf-8"))
        combo.append("\n\n")
    full = "".join(combo)
    _write_pdf(folder / "00_full_readout.pdf", f"{run.field_id} full readout", full)
    (folder / "00_full_readout.txt").write_text(full, encoding="utf-8")
    return folder


def _book_text(pid: str, rec: PaperBookFile | None) -> str:
    if rec is None:
        return f"{pid}\n(empty)\nnever_auto_trade=true\n"
    lines = [
        f"{pid}  field={rec.field_id}",
        f"locked_at={rec.locked_at} run={rec.locked_from_run_id}",
        f"open ${sum(p.stake for p in rec.positions):.2f} / ${rec.bankroll:.2f} "
        f"(started ${rec.starting_bankroll:.0f}) n={len(rec.positions)}",
        "never_auto_trade=true  paper/mock only",
        "",
    ]
    for p in rec.positions:
        lines.append(
            f"  {p.underlying} {p.contract_type.value} {p.strike} {p.expiry} "
            f"${p.stake:.2f} ask={p.entry_ask}"
        )
    return "\n".join(lines)
