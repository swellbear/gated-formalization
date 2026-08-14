"""Dedicated paper-book PDF/HTML/txt. Not the full-field ranking table."""

from __future__ import annotations

import html
from datetime import timezone
from pathlib import Path

from golf_offshoot.config import MIN_EDGE_TO_CONSIDER, MODEL_VERSION
from golf_offshoot.ranking.export_table import (
    TableExportPaths,
    _pdf_text,
    _register_pdf_font,
    _require_fpdf2,
    default_export_dir,
)
from golf_offshoot.strategy.paper_book import (
    PaperBookFile,
    clocks_plain,
    observation_plain,
    observation_technical,
    save_paper_book,
    ticket_rows,
    _fmt_dec,
    _fmt_pct,
    _fmt_pp,
)


def write_paper_book_files(
    record: PaperBookFile,
    *,
    directory: Path | None = None,
    persist: bool = True,
    live_outputs=None,
    live_run_id: str = "",
) -> TableExportPaths:
    """Write a new paper-book artifact for this lock. Never reuse a ranking PDF."""
    d = directory or default_export_dir()
    d.mkdir(parents=True, exist_ok=True)
    stem = paper_export_stem(record)
    live_note = live_run_id or "n/a"
    title = f"Paper book — {record.tournament_name or record.tournament_id}"
    subtitle = (
        f"${record.bankroll:.0f} mock   {record.odds_book or 'book n/a'}   "
        f"locked {record.locked_at.strftime('%Y-%m-%d %H:%M UTC')}   "
        f"lock_run={record.locked_from_run_id or 'n/a'}   "
        f"live_run={live_note}   model={MODEL_VERSION}"
    )
    tickets = ticket_rows(record, live_outputs, live_run_id=live_run_id)
    txt = d / f"{stem}.txt"
    html_path = d / f"{stem}.html"
    pdf = d / f"{stem}.pdf"
    txt.write_text(paper_book_document(record, tickets=tickets, live_run_id=live_run_id), encoding="utf-8")
    html_path.write_text(
        render_paper_html(record, title=title, subtitle=subtitle, tickets=tickets),
        encoding="utf-8",
    )
    write_paper_pdf(pdf, record, title=title, subtitle=subtitle, tickets=tickets)
    record.export_pdf = str(pdf)
    record.export_html = str(html_path)
    record.export_txt = str(txt)
    if persist:
        save_paper_book(record)
    return TableExportPaths(pdf=pdf, html=html_path, txt=txt)


def paper_export_stem(record: PaperBookFile) -> str:
    ts = record.locked_at.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    tid = _safe(record.tournament_id)
    run = _safe(record.locked_from_run_id or "lock")
    return f"{tid}_paper_{ts}_{run}"


def paper_book_document(record: PaperBookFile, *, tickets=None, live_run_id: str = "") -> str:
    cash = record.bankroll - record.book.open_exposure
    frac = (record.book.open_exposure / record.bankroll) if record.bankroll else 0.0
    rows = tickets if tickets is not None else ticket_rows(record)
    lines = [
        f"PAPER BOOK  {record.tournament_name or record.tournament_id}",
        f"${record.bankroll:.0f} mock  |  {record.odds_book or 'book n/a'}  |  "
        f"locked {record.locked_at.isoformat()}  |  lock_run={record.locked_from_run_id or 'n/a'}  |  "
        f"live_run={live_run_id or 'n/a'}",
        f"open ${record.book.open_exposure:.2f} / ${record.bankroll:.2f} ({frac:.0%})  "
        f"cash ${cash:.2f}  tickets={len(record.book.positions)}",
        "Not real money. The system never places bets.",
        "",
        "Observation only",
        observation_plain(),
        observation_technical(),
        "",
        clocks_plain(),
        "",
        f"{'Player':<22} {'Mkt':<6} {'Stake':>8} {'If wins':>9}  "
        f"{'Ent post':>8} {'Ent mdl':>8} {'Ent EW':>8} {'Ent vs':>8}  "
        f"{'Live post':>9} {'Live mdl':>8} {'Live EW':>8} {'Live vs':>8}",
    ]
    for t in rows:
        lines.append(
            f"{t.lane + ' ' + t.player_name:<22} {t.market:<6} ${t.stake:>7.2f} ${t.if_wins:>8.2f}  "
            f"{t.posted:>8.2f} {t.model_win * 100:>7.1f}% {t.edge_w * 100:>+7.1f}pp "
            f"{t.posted_edge * 100:>+7.1f}pp  "
            f"{_fmt_dec(t.live_posted):>9} {_fmt_pct(t.live_model):>8} {_fmt_pp(t.live_edge_w):>8} "
            f"{_fmt_pp(t.live_posted_edge):>8}"
        )
    if not record.book.positions:
        lines.append("(no tickets locked)")
    lines.append("")
    lines.append("At entry Posted / EdgeW / Vs posted are the booked ticket.")
    lines.append("This live is the pack snapshot strategy used. n/a = no coupon for that market.")
    lines.append(
        f"Ticket screen (at entry) needs at least {MIN_EDGE_TO_CONSIDER * 100:.0f} percentage points "
        "on vs posted, not only on EdgeW."
    )
    lines.append("If wins = stake times entry posted decimal (stake returned plus profit).")
    lines.append("Observation only. Never auto-bet.")
    return "\n".join(lines)


def render_paper_html(record: PaperBookFile, *, title: str, subtitle: str, tickets=None) -> str:
    rows = tickets if tickets is not None else ticket_rows(record)
    rows_html = []
    for i, t in enumerate(rows):
        stripe = ' class="alt"' if i % 2 else ""
        rows_html.append(
            "<tr"
            + stripe
            + ">"
            + f"<td class='txt'>{html.escape(t.lane + ' ' + t.player_name)}</td>"
            + f"<td class='txt'>{html.escape(t.market)}</td>"
            + f"<td class='num'>${t.stake:.2f}</td>"
            + f"<td class='num'>${t.if_wins:.2f}</td>"
            + f"<td class='num'>{t.posted:.2f}</td>"
            + f"<td class='num'>{t.model_win * 100:.1f}%</td>"
            + f"<td class='num'>{t.edge_w * 100:+.1f}pp</td>"
            + f"<td class='num'>{t.posted_edge * 100:+.1f}pp</td>"
            + f"<td class='num'>{html.escape(_fmt_dec(t.live_posted))}</td>"
            + f"<td class='num'>{html.escape(_fmt_pct(t.live_model))}</td>"
            + f"<td class='num'>{html.escape(_fmt_pp(t.live_edge_w))}</td>"
            + f"<td class='num'>{html.escape(_fmt_pp(t.live_posted_edge))}</td>"
            + "</tr>"
        )
    cash = record.bankroll - record.book.open_exposure
    frac = (record.book.open_exposure / record.bankroll) if record.bankroll else 0.0
    body = "".join(rows_html) or "<tr><td colspan='12'>No tickets locked.</td></tr>"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{html.escape(title)}</title>
<style>
  @page {{ size: landscape; margin: 12mm; }}
  html {{ color-scheme: light; background: #fff; }}
  body {{ font-family: Segoe UI, Helvetica, Arial, sans-serif; margin: 20px; color: #12202a; background: #fff; }}
  h1 {{ font-size: 22px; margin: 0 0 4px; color: #12202a; }}
  .sub, .caption, .foot {{ color: #445560; font-size: 12px; margin: 0 0 8px; }}
  .stats {{ font-size: 13px; margin: 0 0 12px; }}
  table.field {{ border-collapse: collapse; width: 100%; font-size: 11px; background: #fff; }}
  table.field th {{ background: #1f3b4d; color: #fff; padding: 5px 6px; font-weight: 600; }}
  table.field th.group {{ text-align: center; }}
  table.field td {{ padding: 4px 6px; border-bottom: 1px solid #d5dee4; color: #12202a; background: #fff; }}
  table.field tr.alt td {{ background: #eef3f6; color: #12202a; }}
  .num {{ text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }}
  .txt {{ text-align: left; }}
  h2 {{ font-size: 16px; margin: 22px 0 8px; color: #12202a; }}
  table.gloss {{ border-collapse: collapse; width: 100%; font-size: 12px; background: #fff; }}
  table.gloss th {{ text-align: left; width: 110px; padding: 4px 8px 4px 0; vertical-align: top; color: #1f3b4d; background: #fff; }}
  table.gloss td {{ padding: 4px 0; color: #223; background: #fff; }}
  .foot {{ margin-top: 18px; }}
</style>
</head>
<body>
<h1>{html.escape(title)}</h1>
<p class="sub">{html.escape(subtitle)}</p>
<p class="caption"><strong>Observation only</strong></p>
<p class="caption">{html.escape(observation_plain())}</p>
<p class="caption">{html.escape(observation_technical())}</p>
<p class="caption">{html.escape(clocks_plain())}</p>
<p class="stats">Open ${record.book.open_exposure:.2f} / ${record.bankroll:.2f} ({frac:.0%})
&nbsp;&nbsp; Cash unallocated ${cash:.2f}
&nbsp;&nbsp; Tickets {len(record.book.positions)}
&nbsp;&nbsp; Not real money. Never auto-bet.</p>
<table class="field">
<thead>
<tr>
<th class="txt" rowspan="2">Player</th><th class="txt" rowspan="2">Market</th>
<th class="num" rowspan="2">Stake</th><th class="num" rowspan="2">If wins</th>
<th class="group" colspan="4">At entry</th>
<th class="group" colspan="4">This live</th>
</tr>
<tr>
<th class="num">Posted</th><th class="num">Model</th><th class="num">EdgeW</th><th class="num">Vs posted</th>
<th class="num">Posted</th><th class="num">Model</th><th class="num">EdgeW</th><th class="num">Vs posted</th>
</tr>
</thead>
<tbody>
{body}
</tbody>
</table>
<h2>What the columns mean</h2>
<table class="gloss">
{"".join(f"<tr><th>{html.escape(k)}</th><td>{html.escape(v)}</td></tr>" for k, v in _glossary())}
</table>
<p class="foot">Paper / mock bankroll. Observation only. The system never auto-bets.
This file is the paper book, not the full-field ranking table.</p>
</body>
</html>
"""


def write_paper_pdf(
    path: Path,
    record: PaperBookFile,
    *,
    title: str,
    subtitle: str,
    tickets=None,
) -> Path:
    from fpdf import FPDF
    from fpdf.enums import TableBordersLayout
    from fpdf.fonts import FontFace

    _require_fpdf2()
    rows = tickets if tickets is not None else ticket_rows(record)
    cash = record.bankroll - record.book.open_exposure
    frac = (record.book.open_exposure / record.bankroll) if record.bankroll else 0.0
    stats = (
        f"Open ${record.book.open_exposure:.2f} / ${record.bankroll:.2f} ({frac:.0%})    "
        f"Cash unallocated ${cash:.2f}    Tickets {len(record.book.positions)}    "
        "Not real money. Never auto-bet."
    )

    class Report(FPDF):
        def header(self) -> None:
            face = getattr(self, "_table_font", "Helvetica")
            self.set_x(self.l_margin)
            self.set_text_color(18, 32, 42)
            if self.page_no() == 1:
                self.set_font(face, "B", 14)
                self.cell(0, 7, _pdf_text(title, face), new_x="LMARGIN", new_y="NEXT")
                self.set_font(face, "", 8)
                self.set_text_color(70, 85, 95)
                self.cell(0, 4.5, _pdf_text(subtitle, face), new_x="LMARGIN", new_y="NEXT")
                self.ln(2)
            else:
                self.set_font(face, "B", 9)
                self.cell(0, 6, _pdf_text(f"{title}  (continued)", face), new_x="LMARGIN", new_y="NEXT")
                self.ln(1)

        def footer(self) -> None:
            face = getattr(self, "_table_font", "Helvetica")
            self.set_x(self.l_margin)
            self.set_y(-12)
            self.set_font(face, "I", 7)
            self.set_text_color(90, 100, 110)
            self.cell(
                0,
                6,
                "paper book  |  mock bankroll  |  observation only  |  never auto-bet  |  "
                f"page {self.page_no()} of {{nb}}",
                align="C",
            )

    pdf = Report(orientation="L", unit="mm", format="Letter")
    face = _register_pdf_font(pdf)
    pdf._table_font = face
    if face == "Helvetica":
        pdf.core_fonts_encoding = "cp1252"
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=16)
    pdf.set_margins(12, 12, 12)
    pdf.add_page()
    pdf.set_font(face, "B", 11)
    pdf.set_text_color(18, 32, 42)
    pdf.cell(0, 7, "Observation only", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font(face, "", 8)
    pdf.set_text_color(70, 85, 95)
    pdf.multi_cell(0, 4.4, _pdf_text(observation_plain(), face))
    pdf.ln(1)
    pdf.multi_cell(0, 4.4, _pdf_text(observation_technical(), face))
    pdf.ln(1)
    pdf.multi_cell(0, 4.4, _pdf_text(clocks_plain(), face))
    pdf.ln(2)
    pdf.set_text_color(18, 32, 42)
    pdf.set_font(face, "B", 8)
    pdf.multi_cell(0, 4.4, _pdf_text(stats, face))
    pdf.ln(2)
    pdf.set_font(face, size=7)
    headings_style = FontFace(emphasis="BOLD", color=(255, 255, 255), fill_color=(31, 59, 77))
    headers = (
        "Player",
        "Market",
        "Stake",
        "If wins",
        "Entry posted",
        "Entry model",
        "Entry EdgeW",
        "Entry vs",
        "Live posted",
        "Live model",
        "Live EdgeW",
        "Live vs",
    )
    aligns = (
        "LEFT",
        "LEFT",
        "RIGHT",
        "RIGHT",
        "RIGHT",
        "RIGHT",
        "RIGHT",
        "RIGHT",
        "RIGHT",
        "RIGHT",
        "RIGHT",
        "RIGHT",
    )
    widths = _paper_col_widths(pdf.epw)
    with pdf.table(
        col_widths=widths,
        text_align=aligns,
        headings_style=headings_style,
        cell_fill_color=(243, 246, 248),
        cell_fill_mode="ROWS",
        first_row_as_headings=True,
        line_height=4.2,
        padding=0.9,
        v_align="MIDDLE",
        width=pdf.epw,
        repeat_headings=1,
    ) as table:
        header_row = table.row()
        for h in headers:
            header_row.cell(_pdf_text(h, face))
        if rows:
            for t in rows:
                row = table.row()
                row.cell(_pdf_text(f"{t.lane} {t.player_name}", face))
                row.cell(_pdf_text(t.market, face))
                row.cell(_pdf_text(f"${t.stake:.2f}", face))
                row.cell(_pdf_text(f"${t.if_wins:.2f}", face))
                row.cell(_pdf_text(f"{t.posted:.2f}", face))
                row.cell(_pdf_text(f"{t.model_win * 100:.1f}%", face))
                row.cell(_pdf_text(f"{t.edge_w * 100:+.1f}pp", face))
                row.cell(_pdf_text(f"{t.posted_edge * 100:+.1f}pp", face))
                row.cell(_pdf_text(_fmt_dec(t.live_posted), face))
                row.cell(_pdf_text(_fmt_pct(t.live_model), face))
                row.cell(_pdf_text(_fmt_pp(t.live_edge_w), face))
                row.cell(_pdf_text(_fmt_pp(t.live_posted_edge), face))
        else:
            row = table.row()
            row.cell(_pdf_text("No tickets locked.", face))
            for _ in range(11):
                row.cell("")
    pdf.set_x(pdf.l_margin)
    if pdf.get_y() > pdf.h - 48:
        pdf.add_page()
    else:
        pdf.ln(6)
    pdf.set_x(pdf.l_margin)
    pdf.set_font(face, "B", 11)
    pdf.set_text_color(18, 32, 42)
    pdf.cell(0, 7, "What the columns mean", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)
    pdf.set_font(face, size=8)
    key_w = 32.0
    with pdf.table(
        col_widths=(key_w, pdf.epw - key_w),
        text_align=("LEFT", "LEFT"),
        first_row_as_headings=False,
        line_height=4.6,
        padding=1.0,
        v_align="TOP",
        width=pdf.epw,
        borders_layout=TableBordersLayout.NONE,
    ) as glossary:
        for name, meaning in _glossary():
            row = glossary.row()
            row.cell(_pdf_text(name, face))
            row.cell(_pdf_text(meaning, face))
    pdf.output(str(path))
    return path


def _glossary() -> list[tuple[str, str]]:
    return [
        (
            "At entry",
            "The booked ticket: posted decimal, model, EdgeW, and vs posted at lock or apply. Never rewritten when live runs.",
        ),
        (
            "This live",
            "This pack's snapshot — the numbers strategy used. n/a if that market had no posted coupon on this run.",
        ),
        (
            "Posted",
            "The actual Bovada (or chosen book) decimal price. Not a fair/de-juiced number.",
        ),
        (
            "Model",
            "The model's chance on this ticket's market (win / top 5 / top 10 / top 20).",
        ),
        (
            "EdgeW",
            "Model minus a fair market after stripping the book's extra juice. Can look better than the real ticket.",
        ),
        (
            "Vs posted",
            "Model minus 1/posted odds. This is the gap versus the number you would actually buy.",
        ),
        (
            "Screen",
            f"Cleared at entry only if vs posted is at least {MIN_EDGE_TO_CONSIDER * 100:.0f} percentage points. "
            "Live juice often fails this even when EdgeW looks good. Lane tags on the player name are at-entry.",
        ),
        (
            "If wins",
            "Stake times entry posted decimal (stake comes back plus profit). Not a live mark-to-market.",
        ),
        (
            "Paper",
            "Mock bankroll. Not real money. The system never places bets.",
        ),
    ]


def _paper_col_widths(epw: float) -> list[float]:
    weights = (0.14, 0.07, 0.07, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08)
    total = sum(weights)
    return [epw * w / total for w in weights]


def _safe(value: str) -> str:
    out = []
    for ch in str(value):
        out.append(ch if ch.isalnum() or ch in "-_" else "-")
    return "".join(out).strip("-") or "paper"


def export_existing_paper_book(event_id: str, *, directory: Path | None = None) -> TableExportPaths:
    """Write a new PDF for a book already on disk without changing the tickets."""
    from golf_offshoot.strategy.paper_book import load_paper_file, load_snapshot_outputs

    record = load_paper_file(event_id)
    if record is None:
        raise FileNotFoundError(f"no paper book locked for event {event_id}")
    live_run = ""
    if record.latest_advice:
        live_run = record.latest_advice[0].run_id or ""
    live_run = live_run or record.locked_from_run_id
    return write_paper_book_files(
        record,
        directory=directory,
        live_outputs=load_snapshot_outputs(live_run),
        live_run_id=live_run,
    )
