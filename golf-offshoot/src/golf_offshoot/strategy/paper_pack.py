"""Clean batch package for one paper-book snapshot (tickets, field, bets made)."""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from golf_offshoot.models.strategy import StrategyConfig
from golf_offshoot.strategy.paper_book import (
    PaperBookFile,
    PaperMovement,
    ensure_lock_movements,
    save_paper_book,
)
from golf_offshoot.strategy.paper_bankroll_export import write_bankroll_files
from golf_offshoot.strategy.paper_explain import write_bets_explained_files
from golf_offshoot.strategy.paper_export import write_paper_book_files
from golf_offshoot.strategy.paper_ledger import ensure_opening_deposit, load_ledger

COMBO_PDF = "00_full_readout.pdf"
_PACK_PDF_SECTIONS = (
    ("01_paper_tickets.pdf", "Paper tickets"),
    ("02_bets_explained.pdf", "Bets explained"),
    ("03_leaderboard.pdf", "Live leaderboard"),
    ("03_field_live.pdf", "Field live"),
    ("03_field_pre.pdf", "Field pre-tournament"),
    ("05_bankroll.pdf", "Bankroll"),
)


def packs_dir() -> Path:
    from golf_offshoot.strategy.paper_book import package_data_dir as data_dir

    d = data_dir() / "exports" / "packs"
    d.mkdir(parents=True, exist_ok=True)
    return d


def write_paper_pack(
    record: PaperBookFile,
    *,
    extra_files: list[Path] | None = None,
    advice: list[PaperMovement] | None = None,
    directory: Path | None = None,
    config: StrategyConfig | None = None,
    run_id: str = "",
) -> Path:
    """Write a new folder with tickets, bets-made explanation, and any field tables."""
    cfg = config or StrategyConfig(enabled=True, bankroll=record.bankroll)
    ensure_lock_movements(record, cfg)
    advice = list(advice) if advice is not None else list(record.latest_advice)
    record.latest_advice = advice
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run = _safe(run_id or record.locked_from_run_id or "pack")
    pack_name = f"{_safe(record.tournament_id)}_{stamp}_{run}"
    root = (directory or packs_dir()) / pack_name
    root.mkdir(parents=True, exist_ok=True)

    # Always render tickets from the current book. Copying export_pdf froze the
    # lock-time sheet after apply/reduce/new_bet, so 01_paper_tickets lagged JSON.
    from golf_offshoot.strategy.paper_book import load_snapshot_outputs, package_data_dir as data_dir

    live_outputs = load_snapshot_outputs(run)
    ticket_paths = write_paper_book_files(
        record,
        directory=data_dir() / "exports",
        persist=False,
        live_outputs=live_outputs,
        live_run_id=run,
    )
    _copy_if_exists(ticket_paths.pdf, root / "01_paper_tickets.pdf")
    _copy_if_exists(ticket_paths.html, root / "01_paper_tickets.html")
    _copy_if_exists(ticket_paths.txt, root / "01_paper_tickets.txt")

    write_bets_explained_files(
        record,
        directory=root,
        advice=advice,
        config=cfg,
        live_outputs=live_outputs,
        live_run_id=run,
    )
    led = load_ledger()
    if not getattr(record, "independent_bankroll", False):
        if not led.entries:
            led = ensure_opening_deposit(
                record.bankroll,
                event_id=record.tournament_id,
                event_name=record.tournament_name,
                note="opening paper bankroll (pack)",
            )
        write_bankroll_files(root, ledger=led, record=record)
    else:
        (root / "05_bankroll.txt").write_text(
            (
                f"Independent compare path {getattr(record, 'path_id', '')}. "
                f"Mock ${record.bankroll:.0f}. Not the lived ledger.\n"
            ),
            encoding="utf-8",
        )

    copied: list[str] = []
    for src in extra_files or []:
        path = Path(src)
        if not path.is_file() or "_paper_" in path.name.lower():
            continue
        dest = root / _field_pack_name(path)
        shutil.copy2(path, dest)
        copied.append(dest.name)

    auto = find_related_exports(record.tournament_id, record.locked_from_run_id)
    for path in auto:
        dest = root / _field_pack_name(path)
        if dest.exists():
            continue
        shutil.copy2(path, dest)
        copied.append(dest.name)

    combo = write_combo_pdf(root)

    ledger = {
        "tournament_id": record.tournament_id,
        "tournament_name": record.tournament_name,
        "bankroll": record.bankroll,
        "never_auto_bet": True,
        "paper_observation_only": True,
        "locked_from_run_id": record.locked_from_run_id,
        "pack_run_id": run_id or record.locked_from_run_id,
        "open_exposure": record.book.open_exposure,
        "cash": record.bankroll - record.book.open_exposure,
        "applied_movements": [m.model_dump(mode="json") for m in record.movements],
        "advice_this_snapshot": [m.model_dump(mode="json") for m in advice],
    }
    (root / "04_movements.json").write_text(json.dumps(ledger, indent=2), encoding="utf-8")
    (root / "00_README.txt").write_text(
        _readme(record, copied, advice, combo=combo),
        encoding="utf-8",
    )
    record.latest_pack = str(root)
    save_paper_book(record)
    return root


def find_related_exports(event_id: str, run_id: str, *, export_dir: Path | None = None) -> list[Path]:
    from golf_offshoot.strategy.paper_book import package_data_dir as data_dir

    d = export_dir or (data_dir() / "exports")
    if not d.is_dir() or not run_id:
        return []
    stem = f"{_safe(event_id)}_live_{_safe(run_id)}"
    found: list[Path] = []
    for ext in (".pdf", ".html", ".txt"):
        path = d / f"{stem}{ext}"
        if path.is_file():
            found.append(path)
        board = d / f"{stem}_leaderboard{ext}"
        if board.is_file():
            found.append(board)
    return found


def write_combo_pdf(
    root: Path,
    sources: list[tuple[Path, str]] | None = None,
    *,
    title: str = "Paper pack full readout",
) -> Path | None:
    """Merge the numbered pack PDFs into one full readout. Leaves the parts in place."""
    sources = list(sources) if sources is not None else _pack_pdf_sources(root)
    dest = root / COMBO_PDF
    if dest.exists():
        dest.unlink()
    if not sources:
        return None
    from pypdf import PdfReader, PdfWriter

    writer = PdfWriter()
    for path, label in sources:
        try:
            reader = PdfReader(str(path))
            pages = list(reader.pages)
        except Exception:
            continue
        if not pages:
            continue
        start = len(writer.pages)
        for page in pages:
            writer.add_page(page)
        writer.add_outline_item(label, start)
    if not writer.pages:
        return None
    writer.add_metadata(
        {
            "/Title": title,
            "/Subject": "golf-offshoot observation only never auto-bet",
        }
    )
    with dest.open("wb") as handle:
        writer.write(handle)
    return dest


def _pack_pdf_sources(root: Path) -> list[tuple[Path, str]]:
    """Numbered PDFs in name order. Skips the combo file itself."""
    found: list[tuple[Path, str]] = []
    for path in sorted(root.glob("*.pdf")):
        name = path.name
        if name.lower() == COMBO_PDF.lower():
            continue
        if len(name) < 4 or not name[:2].isdigit() or name[2] != "_":
            continue
        if name.startswith("00_"):
            continue
        found.append((path, path.stem.replace("_", " ")))
    return found


def export_paper_pack(
    event_id: str,
    *,
    extra_files: list[Path] | None = None,
    directory: Path | None = None,
) -> Path:
    from golf_offshoot.strategy.paper_book import backfill_estimated_cashouts, load_paper_file

    record = load_paper_file(event_id)
    if record is None:
        raise FileNotFoundError(f"no paper book locked for event {event_id}")
    record = backfill_estimated_cashouts(record)
    return write_paper_pack(record, extra_files=extra_files, directory=directory)


def _readme(
    record: PaperBookFile,
    copied: list[str],
    advice: list[PaperMovement],
    *,
    combo: Path | None = None,
) -> str:
    cash = record.bankroll - record.book.open_exposure
    lines = [
        f"Paper pack — {record.tournament_name or record.tournament_id}",
        "Mock / paper bankroll. Not real money. The system never places bets.",
        "",
        "Open PDFs in Edge, Chrome, or Adobe — not as source in the editor.",
        "",
    ]
    if combo:
        lines.append("00_full_readout.pdf     Combined tickets + explanation + leaderboard + field + bankroll")
    lines += [
        "00_README.txt           This index",
        "01_paper_tickets.pdf    Current paper tickets (at entry vs this live snapshot)",
        "02_bets_explained.pdf   Why names were taken, why the amounts, sells/reallocates",
        "03_leaderboard.pdf      ESPN place / to-par / thru at this live snapshot (not Win%)",
        "05_bankroll.pdf         Week moves, wins/losses, deposits, lifetime rollover",
        "04_movements.json       Machine ledger for this snapshot",
    ]
    if copied:
        lines.append("03_*                     Full-field ranking table from the lock/live run")
        for name in copied:
            lines.append(f"                         {name}")
    else:
        lines.append("03_*                     Field table not found for this run (unavailable, not invented)")
    lines += [
        "",
        f"Bankroll ${record.bankroll:.0f}   open ${record.book.open_exposure:.2f}   cash ${cash:.2f}",
        f"Applied movements {len(record.movements)}   advice this snapshot {len(advice)}",
        f"Book {record.odds_book or 'n/a'}   lock run {record.locked_from_run_id or 'n/a'}",
        "",
        "00_full_readout.pdf is the one-file version of the numbered PDFs. The individual",
        "files stay in the folder. 03_leaderboard.pdf is the golf board at that live run;",
        "03_field_live.pdf is the model Win% ranking. 05_bankroll.pdf is the week + lifetime",
        "paper money readout. Wins add, losses subtract, deposits you record are added.",
        "live auto-settles a finished open week before the next lock so new caps use the",
        "rolled bankroll.",
        "",
        "01_paper_tickets.pdf splits At entry (booked ticket) from This live (this pack's",
        "snapshot — the numbers strategy used). n/a means that market had no posted coupon.",
        "",
        "Live advice in 02_bets_explained is not applied unless you rerun live with --apply-paper.",
        "Each lock or live snapshot writes a NEW pack folder. Old packs are left in place.",
    ]
    return "\n".join(lines) + "\n"


def _field_pack_name(path: Path) -> str:
    name = path.name.lower()
    ext = path.suffix
    if "_paper_" in name:
        return f"01_paper_tickets_source{ext}"
    if "leaderboard" in name:
        return f"03_leaderboard{ext}"
    if "_live_" in name:
        return f"03_field_live{ext}"
    if "pre_tournament" in name or "_pre-" in name:
        return f"03_field_pre{ext}"
    return f"03_{path.name}"


def _copy_if_exists(src: str | Path | None, dest: Path) -> bool:
    if not src:
        return False
    path = Path(src)
    if not path.is_file():
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, dest)
    return True


def _safe(value: str) -> str:
    out = []
    for ch in str(value):
        out.append(ch if ch.isalnum() or ch in "-_" else "-")
    return "".join(out).strip("-") or "pack"
