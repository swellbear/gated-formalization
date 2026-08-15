"""One pack folder for a compare-method batch. Never auto-bets."""

from __future__ import annotations

import html
import json
import shutil
from pathlib import Path

from golf_offshoot.localtime import filename_stamp
from golf_offshoot.compare.fights import fights_at, load_path_views, write_fights
from golf_offshoot.compare.law import law_hash
from golf_offshoot.compare.paths import compare_markets_blurb
from golf_offshoot.compare.scores import event_scoreboard
from golf_offshoot.config import MODEL_VERSION
from golf_offshoot.models.strategy import StrategyConfig
from golf_offshoot.ranking.export_table import printed_at_utc
from golf_offshoot.strategy.paper_book import load_paper_file, load_snapshot_outputs
from golf_offshoot.strategy.paper_explain import write_bets_explained_files
from golf_offshoot.strategy.paper_export import write_paper_book_files
from golf_offshoot.strategy.paper_pack import (
    _copy_if_exists,
    _safe,
    packs_dir,
    write_combo_pdf,
)

# Reading order in 00_full_readout.pdf. A-control shares the a_replay ledger.
_PATH_SECTIONS = (
    ("lived", "05", "06"),
    ("a_replay", "07", "08"),
    ("b_guts", "09", "10"),
    ("b_nerves", "11", "12"),
    ("b_full", "13", "14"),
)

PATH_LABELS: dict[str, dict[str, str]] = {
    "lived": {
        "short": "Lived museum",
        "one_line": (
            "Lived museum — current pipeline · EdgeW AND vs-posted · "
            "place ladders allowed · not re-locked"
        ),
        "tickets": "Lived museum tickets",
        "explained": "Lived museum — why these bets",
    },
    "a_replay": {
        "short": "A-replay",
        "one_line": (
            "A-replay — same ranking as lived · Winner-only · EdgeW screen · "
            "independent $250 (A-control shares this book)"
        ),
        "tickets": "A-replay tickets (EdgeW, Winner-only)",
        "explained": "A-replay — why these bets",
    },
    "b_guts": {
        "short": "B-guts",
        "one_line": (
            "B-guts — honest theta · Winner-only · EdgeW screen · independent $250"
        ),
        "tickets": "B-guts tickets (honest theta, EdgeW)",
        "explained": "B-guts — why these bets",
    },
    "b_nerves": {
        "short": "B-nerves",
        "one_line": (
            "B-nerves — A's ranking · Winner-only · vs-posted (1/odds) · independent $250"
        ),
        "tickets": "B-nerves tickets (vs-posted, Winner-only)",
        "explained": "B-nerves — why these bets",
    },
    "b_full": {
        "short": "B-full",
        "one_line": (
            "B-full — honest theta · Winner-only · vs-posted (1/odds) · independent $250"
        ),
        "tickets": "B-full tickets (honest theta, vs-posted)",
        "explained": "B-full — why these bets",
    },
}


def _path_labels(event_id: str) -> dict[str, dict[str, str]]:
    markets = compare_markets_blurb(event_id)
    labels = {k: dict(v) for k, v in PATH_LABELS.items()}
    labels["a_replay"]["one_line"] = (
        f"A-replay — same ranking as lived · {markets} · EdgeW screen · "
        "independent $250 (A-control shares this book)"
    )
    labels["a_replay"]["tickets"] = f"A-replay tickets (EdgeW, {markets})"
    labels["b_guts"]["one_line"] = (
        f"B-guts — honest theta · {markets} · EdgeW screen · independent $250"
    )
    labels["b_guts"]["tickets"] = f"B-guts tickets (honest theta, EdgeW, {markets})"
    labels["b_nerves"]["one_line"] = (
        f"B-nerves — A's ranking · {markets} · vs-posted (1/odds) · independent $250"
    )
    labels["b_nerves"]["tickets"] = f"B-nerves tickets (vs-posted, {markets})"
    labels["b_full"]["one_line"] = (
        f"B-full — honest theta · {markets} · vs-posted (1/odds) · independent $250"
    )
    labels["b_full"]["tickets"] = f"B-full tickets (honest theta, vs-posted, {markets})"
    return labels

_COMBO_SECTIONS = (
    ("01_how_to_read.pdf", "How to read this pack"),
    ("02_fights.pdf", "Fights — who each book holds"),
    ("03_leaderboard.pdf", "ESPN leaderboard (place / to-par / thru)"),
    ("04_field_live.pdf", "Model field (Win%)"),
    ("04_field_pre.pdf", "Model field (pre-tournament)"),
    ("05_lived_tickets.pdf", PATH_LABELS["lived"]["tickets"]),
    ("06_lived_explained.pdf", PATH_LABELS["lived"]["explained"]),
    ("07_a_replay_tickets.pdf", PATH_LABELS["a_replay"]["tickets"]),
    ("08_a_replay_explained.pdf", PATH_LABELS["a_replay"]["explained"]),
    ("09_b_guts_tickets.pdf", PATH_LABELS["b_guts"]["tickets"]),
    ("10_b_guts_explained.pdf", PATH_LABELS["b_guts"]["explained"]),
    ("11_b_nerves_tickets.pdf", PATH_LABELS["b_nerves"]["tickets"]),
    ("12_b_nerves_explained.pdf", PATH_LABELS["b_nerves"]["explained"]),
    ("13_b_full_tickets.pdf", PATH_LABELS["b_full"]["tickets"]),
    ("14_b_full_explained.pdf", PATH_LABELS["b_full"]["explained"]),
    ("15_bankroll.pdf", "Lived lifetime bankroll"),
)


def write_batch_pack(
    event_id: str,
    *,
    event_name: str = "",
    run_id: str = "",
    extra_files: list[Path] | None = None,
    directory: Path | None = None,
) -> Path:
    """How-to-read + fights + field + each book + bankroll + one 00_full_readout.pdf."""
    stamp = filename_stamp()
    run = _safe(run_id or "batch")
    pack_name = f"{_safe(event_id)}_{stamp}_{run}_batch"
    root = (directory or packs_dir()) / pack_name
    root.mkdir(parents=True, exist_ok=True)
    scratch = root / "_scratch"
    scratch.mkdir(parents=True, exist_ok=True)
    copied: list[str] = []

    live_outputs = load_snapshot_outputs(run_id)
    views = load_path_views(event_id)
    events = fights_at(views, run_id=run_id, live_outputs=live_outputs, event_id=event_id)
    write_how_to_read(root, event_id=event_id, event_name=event_name, run_id=run_id)

    fights_html = write_fights(
        event_id,
        event_name=event_name,
        views=views,
        events=events,
        extra_notes=[f"batch_run={run_id}", f"law_hash={law_hash()}"],
        directory=scratch,
        live_outputs=live_outputs,
    )
    _copy_if_exists(fights_html.with_suffix(".pdf"), root / "02_fights.pdf")
    _copy_if_exists(fights_html, root / "02_fights.html")
    _copy_if_exists(fights_html.with_suffix(".txt"), root / "02_fights.txt")

    for src in list(extra_files or []) + find_related_exports_safe(event_id, run_id):
        path = Path(src)
        if not path.is_file() or "_paper_" in path.name.lower() or "_fights_" in path.name.lower():
            continue
        dest_name, _label = _batch_context_dest(path)
        dest = root / dest_name
        if dest.exists():
            continue
        shutil.copy2(path, dest)
        copied.append(dest.name)

    event = event_name or event_id
    labels_by_path = _path_labels(event_id)
    for path_id, ticket_n, explained_n in _PATH_SECTIONS:
        rec = load_paper_file(event_id, path_id=path_id)
        if rec is None:
            continue
        labels = labels_by_path[path_id]
        meta = (
            f"{labels['one_line']}   ${rec.bankroll:.0f} mock   "
            f"{rec.odds_book or 'book n/a'}   live_run={run_id or 'n/a'}   "
            f"model={MODEL_VERSION}"
        )
        paths = write_paper_book_files(
            rec,
            directory=scratch,
            persist=False,
            live_outputs=live_outputs,
            live_run_id=run_id,
            title=f"{labels['tickets']} — {event}",
            subtitle=meta,
        )
        _copy_if_exists(paths.pdf, root / f"{ticket_n}_{path_id}_tickets.pdf")
        _copy_if_exists(paths.html, root / f"{ticket_n}_{path_id}_tickets.html")
        _copy_if_exists(paths.txt, root / f"{ticket_n}_{path_id}_tickets.txt")
        explained = write_bets_explained_files(
            rec,
            directory=scratch,
            advice=list(rec.latest_advice),
            config=StrategyConfig(enabled=True, bankroll=rec.bankroll),
            live_outputs=live_outputs,
            live_run_id=run_id,
            title=f"{labels['explained']} — {event}",
            subtitle=meta,
        )
        _copy_if_exists(explained.pdf, root / f"{explained_n}_{path_id}_explained.pdf")
        _copy_if_exists(explained.html, root / f"{explained_n}_{path_id}_explained.html")
        _copy_if_exists(explained.txt, root / f"{explained_n}_{path_id}_explained.txt")

    lived = load_paper_file(event_id, path_id="lived")
    if lived is not None and not lived.independent_bankroll:
        from golf_offshoot.strategy.paper_bankroll_export import write_bankroll_files
        from golf_offshoot.strategy.paper_ledger import load_ledger

        bank = write_bankroll_files(
            scratch,
            ledger=load_ledger(),
            record=lived,
            title="Lived lifetime bankroll — not used by A/B compare books",
        )
        _copy_if_exists(bank.pdf, root / "15_bankroll.pdf")
        _copy_if_exists(bank.html, root / "15_bankroll.html")
        _copy_if_exists(bank.txt, root / "15_bankroll.txt")

    shutil.rmtree(scratch, ignore_errors=True)
    combo_sources = _combo_sources(root)
    combo = write_combo_pdf(
        root,
        combo_sources,
        title=f"Compare batch readout — {event_name or event_id}",
    )
    (root / "16_movements.json").write_text(
        json.dumps(
            {
                "event_id": event_id,
                "event_name": event_name,
                "run_id": run_id,
                "method_law_hash": law_hash(),
                "never_auto_bet": True,
                "reading_order": [label for _path, label in combo_sources],
                "paths": {
                    pid: {
                        "n": views[pid].n,
                        "names": views[pid].names,
                        "exposure": views[pid].exposure,
                        "bankroll": views[pid].bankroll,
                        "label": _path_labels(event_id).get(pid, {}).get("one_line", pid),
                    }
                    for pid in views
                },
                "scores": event_scoreboard(event_id),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (root / "00_README.txt").write_text(
        _batch_readme(event_id, event_name=event_name, copied=copied, combo=combo, run_id=run_id),
        encoding="utf-8",
    )
    return root


def _combo_sources(root: Path) -> list[tuple[Path, str]]:
    found: list[tuple[Path, str]] = []
    for name, label in _COMBO_SECTIONS:
        path = root / name
        if path.is_file():
            found.append((path, label))
    return found


def find_related_exports_safe(event_id: str, run_id: str) -> list[Path]:
    from golf_offshoot.strategy.paper_pack import find_related_exports

    return find_related_exports(event_id, run_id)


def _batch_context_dest(path: Path) -> tuple[str, str]:
    name = path.name.lower()
    ext = path.suffix
    if "leaderboard" in name:
        return f"03_leaderboard{ext}", "ESPN leaderboard (place / to-par / thru)"
    if "_live_" in name:
        return f"04_field_live{ext}", "Model field (Win%)"
    if "pre_tournament" in name or "_pre-" in name:
        return f"04_field_pre{ext}", "Model field (pre-tournament)"
    return f"04_{path.name}", path.stem.replace("_", " ")


def write_how_to_read(
    root: Path,
    *,
    event_id: str,
    event_name: str,
    run_id: str,
) -> Path:
    event = event_name or event_id
    text = _how_to_read_text(event_id=event_id, event_name=event, run_id=run_id)
    txt = root / "01_how_to_read.txt"
    html_path = root / "01_how_to_read.html"
    pdf = root / "01_how_to_read.pdf"
    txt.write_text(text, encoding="utf-8")
    html_path.write_text(
        (
            "<!DOCTYPE html><html><head><meta charset='utf-8'>"
            f"<title>How to read this pack — {html.escape(event)}</title>"
            "<style>body{font-family:ui-monospace,Consolas,monospace;white-space:pre-wrap;"
            "margin:24px;max-width:1100px} h1{font-size:18px}</style></head><body>"
            f"<h1>How to read this pack — {html.escape(event)}</h1>\n"
            f"<pre>{html.escape(text)}</pre></body></html>\n"
        ),
        encoding="utf-8",
    )
    _write_how_to_read_pdf(pdf, text, title=f"How to read this pack — {event}")
    return pdf


def _how_to_read_text(*, event_id: str, event_name: str, run_id: str) -> str:
    markets = compare_markets_blurb(event_id)
    lines = [
        f"HOW TO READ THIS PACK  {event_name}",
        f"event={event_id}  run={run_id or 'n/a'}  law={law_hash()}",
        f"printed {printed_at_utc()}",
        "Paper / mock only. The system never places bets.",
        "",
        "This file is five mock books plus the board they saw. Read in this order:",
        "",
        "  1. This page          What each book is",
        "  2. Fights             Who each book holds, and where they disagree",
        "  3. ESPN leaderboard   Place / to-par / thru. Not model Win%.",
        "  4. Model field        Win% ranking from the live sim",
        "  5. Lived museum       Your real paper book (place ladders allowed)",
        f"  6. A-replay           Same ranking as lived. {markets}. EdgeW screen.",
        "                       A-control is not a second book; it shares A-replay.",
        f"  7. B-guts             Honest theta. {markets}. EdgeW screen.",
        f"  8. B-nerves           A's ranking. {markets}. vs-posted (1/odds).",
        f"  9. B-full             Honest theta. {markets}. vs-posted (1/odds).",
        " 10. Lived bankroll     Lifetime ledger. Compare books do not use this.",
        "",
        "Each ticket table is titled with the book name in the page header.",
        "A 'why these bets' page follows that book's tickets.",
        "",
        f"A/B markets: {markets}. Place only if the book lists Top 5/10/20 — never from Winner odds.",
        "Score Winner posted P/L and place posted P/L as two lines, not one blended book.",
        "t stays 0.03 this week. Learner may not copy A because A won.",
        "",
        "Open this PDF in Edge, Chrome, or Adobe — not as source in the editor.",
    ]
    return "\n".join(lines) + "\n"


def _write_how_to_read_pdf(path: Path, text: str, *, title: str) -> Path:
    from fpdf import FPDF

    from golf_offshoot.ranking.export_table import (
        _pdf_text,
        _register_pdf_font,
        _require_fpdf2,
        mark_pdf_printed,
        write_pdf_footer,
        write_pdf_print_stamp,
    )

    _require_fpdf2()

    class Report(FPDF):
        def header(self) -> None:
            face = getattr(self, "_table_font", "Helvetica")
            self.set_x(self.l_margin)
            write_pdf_print_stamp(self, face)
            self.set_font(face, "B", 14)
            self.set_text_color(18, 32, 42)
            self.cell(0, 8, _pdf_text(title, face), new_x="LMARGIN", new_y="NEXT")
            self.ln(2)

        def footer(self) -> None:
            face = getattr(self, "_table_font", "Helvetica")
            write_pdf_footer(self, face, "compare batch")

    pdf = Report(orientation="P", unit="mm", format="Letter")
    face = _register_pdf_font(pdf)
    pdf._table_font = face
    mark_pdf_printed(pdf)
    if face == "Helvetica":
        pdf.core_fonts_encoding = "cp1252"
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=16)
    pdf.set_margins(14, 16, 14)
    pdf.add_page()
    pdf.set_font(face, size=10)
    pdf.set_text_color(18, 32, 42)
    pdf.multi_cell(0, 5, _pdf_text(text, face))
    pdf.output(str(path))
    return path


def _batch_readme(
    event_id: str,
    *,
    event_name: str,
    copied: list[str],
    combo: Path | None,
    run_id: str,
) -> str:
    lines = [
        f"Compare batch pack — {event_name or event_id}",
        "Mock / paper. Not real money. The system never places bets.",
        "",
        "Open PDFs in Edge, Chrome, or Adobe — not as source in the editor.",
        "",
        "Read 00_full_readout.pdf in this order. Each ticket page is titled with the book.",
        "",
    ]
    if combo:
        lines.append("00_full_readout.pdf     One file: legend + fights + board + each book + bankroll")
    lines += [
        "00_README.txt           This index",
        "01_how_to_read.pdf      What each book is, and the reading order",
        "02_fights.pdf           Who each book holds, and where they disagree",
        "03_leaderboard.pdf      ESPN place / to-par / thru (not Win%)",
        "04_field_live.pdf       Model Win% ranking",
        "05_lived_tickets.pdf    Lived museum (EdgeW AND vs-posted; place ladders)",
        "06_lived_explained.pdf  Why those lived bets",
        "07_a_replay_tickets.pdf A-replay: same ranking as lived, EdgeW",
        "08_a_replay_explained.pdf",
        "09_b_guts_tickets.pdf   B-guts: honest theta, EdgeW",
        "10_b_guts_explained.pdf",
        "11_b_nerves_tickets.pdf B-nerves: A's ranking, vs-posted",
        "12_b_nerves_explained.pdf",
        "13_b_full_tickets.pdf   B-full: honest theta, vs-posted",
        "14_b_full_explained.pdf",
        "15_bankroll.pdf         Lived lifetime ledger (compare books are independent)",
        "16_movements.json       Path snapshot + Winner vs place scoreboard",
        "",
        "A-control is not a separate book. It shares A-replay.",
        f"A/B markets: {compare_markets_blurb(event_id)}.",
        "Winner posted P/L and place posted P/L stay separate.",
        "",
        f"run {run_id or 'n/a'}   law {law_hash()}   never_auto_bet=true",
    ]
    if copied:
        lines.append("Also copied: " + ", ".join(copied))
    return "\n".join(lines) + "\n"
