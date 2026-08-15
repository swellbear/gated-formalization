"""Downloadable ESPN-style live scoreboard (PDF / HTML / txt). Not the Win% table."""

from __future__ import annotations

import html
from pathlib import Path

from golf_offshoot.config import MODEL_VERSION
from golf_offshoot.models.enums import RunMode
from golf_offshoot.models.schemas import TournamentRunResult
from golf_offshoot.ranking.export_table import (
    TableExportPaths,
    _pdf_text,
    _register_pdf_font,
    _require_fpdf2,
    default_export_dir,
    mark_pdf_printed,
    printed_at_utc,
    write_pdf_footer,
    write_pdf_print_stamp,
)
from golf_offshoot.ranking.leaderboard import LeaderboardView, format_leaderboard, leaderboard_view


def export_live_leaderboard(
    result: TournamentRunResult,
    *,
    held_ids: set[str] | None = None,
    directory: Path | None = None,
) -> TableExportPaths | None:
    if result.mode != RunMode.LIVE:
        return None
    d = directory or default_export_dir()
    d.mkdir(parents=True, exist_ok=True)
    n_rounds = int(result.tournament.n_rounds or 4)
    view = leaderboard_view(result.ranked, n_rounds=n_rounds, held_ids=held_ids)
    stem = _leaderboard_stem(result)
    title = f"{result.tournament.name} leaderboard (live snapshot)"
    subtitle = (
        f"id={result.tournament.tournament_id}   n={len(result.ranked)}   "
        f"run={result.run_id}   model={MODEL_VERSION}"
    )
    caption = (
        "ESPN place / to-par / thru at this run. Not model Win%. "
        "Round-by-round scores are not listed (not ingested). Observation only."
    )
    txt = d / f"{stem}.txt"
    html_path = d / f"{stem}.html"
    pdf = d / f"{stem}.pdf"
    body = format_leaderboard(result.ranked, n_rounds=n_rounds, held_ids=held_ids)
    txt.write_text(
        f"{title}\n{subtitle}\nprinted {printed_at_utc()}\n{caption}\n\n{body}\n",
        encoding="utf-8",
    )
    html_path.write_text(
        render_leaderboard_html(title=title, subtitle=subtitle, caption=caption, view=view),
        encoding="utf-8",
    )
    write_leaderboard_pdf(pdf, title=title, subtitle=subtitle, caption=caption, view=view)
    return TableExportPaths(pdf=pdf, html=html_path, txt=txt)


def render_leaderboard_html(
    *,
    title: str,
    subtitle: str,
    caption: str | None,
    view: LeaderboardView,
) -> str:
    head_cells = "".join(
        f'<th class="{_align_class(a)}">{html.escape(h)}</th>' for h, a in zip(view.headers, view.aligns)
    )
    body_rows = []
    for i, cells in enumerate(view.rows):
        tds = "".join(
            f'<td class="{_align_class(a)}">{html.escape(c)}</td>'
            for c, a in zip(cells, view.aligns)
        )
        stripe = ' class="alt"' if i % 2 else ""
        body_rows.append(f"<tr{stripe}>{tds}</tr>")
    gloss = "".join(
        f"<tr><th>{html.escape(k)}</th><td>{html.escape(v)}</td></tr>" for k, v in view.glossary
    )
    cap = f"<p class='caption'>{html.escape(caption)}</p>" if caption else ""
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
  table.field {{ border-collapse: collapse; width: 100%; font-size: 12px; background: #fff; }}
  table.field th {{ background: #1f3b4d; color: #fff; padding: 6px 7px; font-weight: 600; }}
  table.field td {{ padding: 4px 7px; border-bottom: 1px solid #d5dee4; color: #12202a; background: #fff; }}
  table.field tr.alt td {{ background: #eef3f6; color: #12202a; }}
  .num {{ text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }}
  .txt {{ text-align: left; }}
  h2 {{ font-size: 16px; margin: 22px 0 8px; color: #12202a; }}
  table.gloss {{ border-collapse: collapse; width: 100%; font-size: 12px; background: #fff; }}
  table.gloss th {{ text-align: left; width: 90px; padding: 4px 8px 4px 0; vertical-align: top; color: #1f3b4d; background: #fff; }}
  table.gloss td {{ padding: 4px 0; color: #223; background: #fff; }}
  .foot {{ margin-top: 18px; }}
</style>
</head>
<body>
<h1>{html.escape(title)}</h1>
<p class="sub">{html.escape(subtitle)}</p>
<p class="sub">printed {html.escape(printed_at_utc())}</p>
{cap}
<table class="field">
<thead><tr>{head_cells}</tr></thead>
<tbody>
{"".join(body_rows)}
</tbody>
</table>
<h2>Column index</h2>
<table class="gloss">
{gloss}
</table>
<p class="foot">Observation only. The system never auto-bets. This is the golf board, not the model ranking.</p>
</body>
</html>
"""


def write_leaderboard_pdf(
    path: Path,
    *,
    title: str,
    subtitle: str,
    caption: str | None,
    view: LeaderboardView,
) -> Path:
    from fpdf import FPDF
    from fpdf.enums import TableBordersLayout
    from fpdf.fonts import FontFace

    _require_fpdf2()

    class Report(FPDF):
        def header(self) -> None:
            face = getattr(self, "_table_font", "Helvetica")
            self.set_x(self.l_margin)
            write_pdf_print_stamp(self, face)
            if self.page_no() == 1:
                self.set_font(face, "B", 14)
                self.set_text_color(18, 32, 42)
                self.cell(0, 7, _pdf_text(title, face), new_x="LMARGIN", new_y="NEXT")
                self.set_font(face, "", 8)
                self.set_text_color(70, 85, 95)
                self.cell(0, 4.5, _pdf_text(subtitle, face), new_x="LMARGIN", new_y="NEXT")
                if caption:
                    self.multi_cell(0, 4.5, _pdf_text(caption, face))
                self.set_text_color(18, 32, 42)
                self.ln(2)
            else:
                self.set_font(face, "B", 9)
                self.set_text_color(18, 32, 42)
                self.cell(0, 6, _pdf_text(f"{title}  (continued)", face), new_x="LMARGIN", new_y="NEXT")
                self.ln(1)

        def footer(self) -> None:
            face = getattr(self, "_table_font", "Helvetica")
            write_pdf_footer(self, face, "live scoreboard")

    pdf = Report(orientation="L", unit="mm", format="Letter")
    face = _register_pdf_font(pdf)
    pdf._table_font = face
    mark_pdf_printed(pdf)
    if face == "Helvetica":
        pdf.core_fonts_encoding = "cp1252"
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=16)
    pdf.set_margins(12, 12, 12)
    pdf.add_page()
    pdf.set_font(face, size=8)
    headings_style = FontFace(emphasis="BOLD", color=(255, 255, 255), fill_color=(31, 59, 77))
    aligns = tuple("RIGHT" if a == "right" else "LEFT" for a in view.aligns)
    widths = _col_widths_mm(pdf.epw)
    with pdf.table(
        col_widths=widths,
        text_align=aligns,
        headings_style=headings_style,
        cell_fill_color=(243, 246, 248),
        cell_fill_mode="ROWS",
        first_row_as_headings=True,
        line_height=4.4,
        padding=1.15,
        v_align="MIDDLE",
        width=pdf.epw,
        repeat_headings=1,
    ) as table:
        header_row = table.row()
        for h in view.headers:
            header_row.cell(_pdf_text(h, face))
        for cells in view.rows:
            row = table.row()
            for cell in cells:
                row.cell(_pdf_text(cell, face))
    pdf.set_x(pdf.l_margin)
    if pdf.get_y() > pdf.h - 42:
        pdf.add_page()
    else:
        pdf.ln(6)
    pdf.set_x(pdf.l_margin)
    pdf.set_font(face, "B", 11)
    pdf.set_text_color(18, 32, 42)
    pdf.cell(0, 7, "Column index", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)
    pdf.set_font(face, size=8)
    key_w = 28.0
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
        for name, meaning in view.glossary:
            row = glossary.row()
            row.cell(_pdf_text(name, face))
            row.cell(_pdf_text(meaning, face))
    pdf.output(str(path))
    return path


def _leaderboard_stem(result: TournamentRunResult) -> str:
    tid = result.tournament.espn_event_id or result.tournament.tournament_id
    return f"{_safe(tid)}_{_safe(result.mode.value)}_{_safe(result.run_id)}_leaderboard"


def _safe(value: str) -> str:
    out = []
    for ch in str(value):
        out.append(ch if ch.isalnum() or ch in "-_" else "-")
    return "".join(out).strip("-") or "table"


def _align_class(align: str) -> str:
    return "num" if align == "right" else "txt"


def _col_widths_mm(epw: float) -> list[float]:
    weights = (0.08, 0.28, 0.10, 0.10, 0.08, 0.16, 0.20)
    total = sum(weights)
    return [epw * w / total for w in weights]
