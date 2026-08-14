"""Downloadable ranked-table artifacts: formatted PDF, HTML preview, and txt."""

from __future__ import annotations

import html
import os
from dataclasses import dataclass
from pathlib import Path

from golf_offshoot.config import MODEL_VERSION
from golf_offshoot.data_feeds.http import package_data_dir
from golf_offshoot.models.schemas import PlayerOutput, TournamentRunResult
from golf_offshoot.ranking.display import RankedTableView, format_table, movement_note, ranked_table_view


@dataclass(frozen=True)
class TableExportPaths:
    pdf: Path
    html: Path
    txt: Path


def default_export_dir() -> Path:
    return package_data_dir() / "exports"


def ranked_table_document(
    result: TournamentRunResult,
    *,
    baseline: list[PlayerOutput] | None = None,
    caption: str | None = None,
) -> str:
    lines = [
        f"{result.tournament.name}  ({result.mode.value})",
        f"id={result.tournament.tournament_id}  n={len(result.ranked)}  run={result.run_id}",
        f"model={MODEL_VERSION}  never_auto_bet=true  observation only",
    ]
    if caption:
        lines.append(caption)
    lines.append("")
    lines.append(format_table(result.ranked, n=len(result.ranked), baseline=baseline))
    return "\n".join(lines)


def write_ranked_table_files(
    result: TournamentRunResult,
    *,
    baseline: list[PlayerOutput] | None = None,
    caption: str | None = None,
    directory: Path | None = None,
) -> TableExportPaths:
    d = directory or default_export_dir()
    d.mkdir(parents=True, exist_ok=True)
    stem = _export_stem(result)
    view = ranked_table_view(result.ranked, n=len(result.ranked), baseline=baseline)
    title = f"{result.tournament.name} ({result.mode.value})"
    subtitle = (
        f"id={result.tournament.tournament_id}   n={len(result.ranked)}   "
        f"run={result.run_id}   model={MODEL_VERSION}"
    )
    txt = d / f"{stem}.txt"
    html_path = d / f"{stem}.html"
    pdf = d / f"{stem}.pdf"
    txt.write_text(ranked_table_document(result, baseline=baseline, caption=caption), encoding="utf-8")
    html_path.write_text(
        render_ranked_html(title=title, subtitle=subtitle, caption=caption, view=view),
        encoding="utf-8",
    )
    write_ranked_pdf(pdf, title=title, subtitle=subtitle, caption=caption, view=view)
    return TableExportPaths(pdf=pdf, html=html_path, txt=txt)


def export_operating_table(
    result: TournamentRunResult,
    *,
    baseline: list[PlayerOutput] | None = None,
    baseline_run_id: str | None = None,
    directory: Path | None = None,
) -> TableExportPaths:
    caption = None
    if result.mode.value == "live":
        caption = movement_note(baseline_run_id)
    return write_ranked_table_files(
        result,
        baseline=baseline if result.mode.value == "live" else None,
        caption=caption,
        directory=directory,
    )


def render_ranked_html(
    *,
    title: str,
    subtitle: str,
    caption: str | None,
    view: RankedTableView,
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
<p class="foot">Observation only. The system never auto-bets.</p>
</body>
</html>
"""


def write_ranked_pdf(
    path: Path,
    *,
    title: str,
    subtitle: str,
    caption: str | None,
    view: RankedTableView,
) -> Path:
    from fpdf import FPDF
    from fpdf.enums import TableBordersLayout
    from fpdf.fonts import FontFace

    _require_fpdf2()

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
                if caption:
                    self.multi_cell(0, 4.5, _pdf_text(caption, face))
                self.set_text_color(18, 32, 42)
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
                "golf-offshoot  |  observation only  |  never auto-bet  |  "
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
    pdf.set_font(face, size=8)
    headings_style = FontFace(emphasis="BOLD", color=(255, 255, 255), fill_color=(31, 59, 77))
    aligns = tuple("RIGHT" if a == "right" else "LEFT" for a in view.aligns)
    widths = _col_widths_mm(view.headers, pdf.epw)
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
    # pdf.table() leaves the cursor at the right margin. A following cell()+multi_cell
    # glossary then paints labels on the far right and a nearly blank last page.
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


def _require_fpdf2() -> None:
    import fpdf
    from fpdf import FPDF

    if not hasattr(FPDF, "table"):
        raise RuntimeError(
            "PDF export requires fpdf2. Uninstall the old PyFPDF package "
            "(`pip uninstall fpdf`) and `pip install fpdf2`."
        )
    version = str(getattr(fpdf, "__version__", "0"))
    try:
        major = int(version.split(".", 1)[0])
    except ValueError:
        major = 0
    if major < 2:
        raise RuntimeError(f"PDF export requires fpdf2>=2, got {version}")


def _register_pdf_font(pdf) -> str:
    fonts = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"
    regular = fonts / "arial.ttf"
    bold = fonts / "arialbd.ttf"
    italic = fonts / "ariali.ttf"
    if regular.is_file() and bold.is_file():
        pdf.add_font("TableSans", "", str(regular))
        pdf.add_font("TableSans", "B", str(bold))
        pdf.add_font("TableSans", "I", str(italic if italic.is_file() else regular))
        return "TableSans"
    return "Helvetica"


def _col_widths_mm(headers: tuple[str, ...], epw: float) -> list[float]:
    weights = {
        "#": 0.035,
        "Player": 0.17,
        "Win": 0.16,
        "dWin": 0.065,
        "Pre#": 0.05,
        "dRnk": 0.055,
        "T10": 0.06,
        "Cut": 0.06,
        "EdgeW": 0.065,
        "EdgeT10": 0.07,
        "Rel": 0.05,
        "Flags": 0.17,
    }
    raw = [weights.get(h, 0.08) for h in headers]
    total = sum(raw) or 1.0
    return [epw * w / total for w in raw]


def _align_class(align: str) -> str:
    return "num" if align == "right" else "txt"


def _pdf_text(value: str, face: str) -> str:
    text = str(value or "")
    if face == "Helvetica":
        return text.encode("cp1252", "replace").decode("cp1252")
    return text


def _winansi(value: str) -> str:
    return _pdf_text(value, "Helvetica")


def _export_stem(result: TournamentRunResult) -> str:
    tid = result.tournament.espn_event_id or result.tournament.tournament_id
    return f"{_safe(tid)}_{_safe(result.mode.value)}_{_safe(result.run_id)}"


def _safe(value: str) -> str:
    out = []
    for ch in str(value):
        out.append(ch if ch.isalnum() or ch in "-_" else "-")
    return "".join(out).strip("-") or "table"
