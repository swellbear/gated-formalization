"""Bets-made explanation page: why names, why amounts, why later moves."""

from __future__ import annotations

import html
from pathlib import Path

from golf_offshoot.config import MODEL_VERSION
from golf_offshoot.models.strategy import StrategyConfig
from golf_offshoot.ranking.export_table import (
    TableExportPaths,
    _pdf_text,
    _register_pdf_font,
    _require_fpdf2,
)
from golf_offshoot.strategy.paper_book import (
    PaperBookFile,
    PaperMovement,
    observation_plain,
    observation_technical,
    sizing_plain,
    sizing_technical,
    ticket_rows,
)


def write_bets_explained_files(
    record: PaperBookFile,
    *,
    directory: Path,
    advice: list[PaperMovement] | None = None,
    config: StrategyConfig | None = None,
) -> TableExportPaths:
    cfg = config or StrategyConfig(enabled=True, bankroll=record.bankroll)
    advice = advice if advice is not None else list(record.latest_advice)
    directory.mkdir(parents=True, exist_ok=True)
    title = f"Bets made — {record.tournament_name or record.tournament_id}"
    subtitle = (
        f"${record.bankroll:.0f} mock   {record.odds_book or 'book n/a'}   "
        f"{record.mode}/{record.risk}   run={record.locked_from_run_id or 'n/a'}   "
        f"model={MODEL_VERSION}"
    )
    txt = directory / "02_bets_explained.txt"
    html_path = directory / "02_bets_explained.html"
    pdf = directory / "02_bets_explained.pdf"
    body = bets_explained_document(record, advice=advice, config=cfg)
    txt.write_text(body, encoding="utf-8")
    html_path.write_text(
        render_bets_explained_html(record, title=title, subtitle=subtitle, advice=advice, config=cfg),
        encoding="utf-8",
    )
    write_bets_explained_pdf(pdf, record, title=title, subtitle=subtitle, advice=advice, config=cfg)
    return TableExportPaths(pdf=pdf, html=html_path, txt=txt)


def bets_explained_document(
    record: PaperBookFile,
    *,
    advice: list[PaperMovement],
    config: StrategyConfig,
) -> str:
    cash = record.bankroll - record.book.open_exposure
    lines = [
        f"BETS MADE  {record.tournament_name or record.tournament_id}",
        f"${record.bankroll:.0f} mock  never_auto_bet=true  {record.mode}/{record.risk}",
        f"open ${record.book.open_exposure:.2f}  cash ${cash:.2f}  tickets={len(record.book.positions)}",
        "",
        "Observation only",
        observation_plain(),
        observation_technical(),
        "",
        "Why the amounts",
        sizing_plain(config),
        sizing_technical(config),
        "",
        "Applied movements (in the paper book)",
    ]
    applied = [m for m in record.movements if m.status == "applied"]
    if not applied:
        lines.append("  (none recorded)")
    for m in applied:
        lines.extend(_movement_lines(m))
    lines.append("")
    lines.append("Live advice this snapshot (not applied unless you pass --apply-paper)")
    if not advice:
        lines.append("  (no hold/sell/add/reallocate advice on this snapshot)")
    for m in advice:
        lines.extend(_movement_lines(m))
    lines.append("")
    lines.append("Current tickets")
    for t in ticket_rows(record):
        lines.append(
            f"  {t.player_name} {t.market} ${t.stake:.2f} @ {t.posted:.2f} "
            f"EdgeW={t.edge_w:+.3f} vs_posted={t.posted_edge:+.3f}"
        )
        lines.append(f"    {t.screen}")
    lines.append("")
    lines.append("Paper / mock. Observation only. The system never auto-bets.")
    return "\n".join(lines)


def _movement_lines(m: PaperMovement) -> list[str]:
    after = f"${m.stake_after:.2f}" if m.stake_after is not None else "n/a"
    donor = f" from {m.from_player_name}" if m.from_player_name else ""
    return [
        f"  {m.kind.upper()} {m.status} {m.player_name}{donor} "
        f"delta={m.stake_delta:+.2f} after={after}",
        f"    why: {m.reason_plain}",
        f"    amount: {m.amount_plain}",
        f"    technical: {m.reason_technical} | {m.amount_technical}",
    ]


def render_bets_explained_html(
    record: PaperBookFile,
    *,
    title: str,
    subtitle: str,
    advice: list[PaperMovement],
    config: StrategyConfig,
) -> str:
    applied_rows = _html_movement_rows([m for m in record.movements if m.status == "applied"])
    advice_rows = _html_movement_rows(advice)
    ticket_rows_html = []
    for i, t in enumerate(ticket_rows(record)):
        stripe = ' class="alt"' if i % 2 else ""
        ticket_rows_html.append(
            f"<tr{stripe}><td class='txt'>{html.escape(t.player_name)}</td>"
            f"<td class='txt'>{html.escape(t.market)}</td>"
            f"<td class='num'>${t.stake:.2f}</td>"
            f"<td class='num'>{t.posted:.2f}</td>"
            f"<td class='num'>{t.edge_w * 100:+.1f}pp</td>"
            f"<td class='num'>{t.posted_edge * 100:+.1f}pp</td>"
            f"<td class='txt'>{html.escape(t.screen)}</td></tr>"
        )
    cash = record.bankroll - record.book.open_exposure
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>{html.escape(title)}</title>
<style>
  html {{ color-scheme: light; background: #fff; }}
  body {{ font-family: Segoe UI, Helvetica, Arial, sans-serif; margin: 20px; color: #12202a; }}
  h1 {{ font-size: 22px; margin: 0 0 4px; }}
  h2 {{ font-size: 16px; margin: 22px 0 8px; color: #1f3b4d; }}
  .sub, .caption, .foot {{ color: #445560; font-size: 12px; margin: 0 0 8px; }}
  table {{ border-collapse: collapse; width: 100%; font-size: 12px; }}
  th {{ background: #1f3b4d; color: #fff; padding: 6px 7px; text-align: left; }}
  td {{ padding: 6px 7px; border-bottom: 1px solid #d5dee4; vertical-align: top; }}
  tr.alt td {{ background: #eef3f6; }}
  .num {{ text-align: right; font-variant-numeric: tabular-nums; }}
  .txt {{ text-align: left; }}
  .foot {{ margin-top: 18px; }}
</style>
</head>
<body>
<h1>{html.escape(title)}</h1>
<p class="sub">{html.escape(subtitle)}</p>
<p class="caption"><strong>Observation only</strong></p>
<p class="caption">{html.escape(observation_plain())}</p>
<p class="caption">{html.escape(observation_technical())}</p>
<h2>Why the amounts</h2>
<p class="caption">{html.escape(sizing_plain(config))}</p>
<p class="caption">{html.escape(sizing_technical(config))}</p>
<p class="caption">Open ${record.book.open_exposure:.2f} / ${record.bankroll:.2f}.
Cash unallocated ${cash:.2f}. Not real money. Never auto-bet.</p>
<h2>Applied movements (in the paper book)</h2>
<table>
<thead><tr><th>Action</th><th>Player</th><th class="num">Delta</th><th class="num">After</th><th>Why this name</th><th>Why this amount</th></tr></thead>
<tbody>{applied_rows or "<tr><td colspan='6'>None recorded.</td></tr>"}</tbody>
</table>
<h2>Live advice this snapshot</h2>
<p class="caption">Hold / sell / add / reallocate suggestions. Not applied unless you pass --apply-paper.
Still mock. Still never a real bet.</p>
<table>
<thead><tr><th>Action</th><th>Player</th><th class="num">Delta</th><th class="num">After</th><th>Why this name</th><th>Why this amount</th></tr></thead>
<tbody>{advice_rows or "<tr><td colspan='6'>No advice on this snapshot.</td></tr>"}</tbody>
</table>
<h2>Current tickets</h2>
<table>
<thead><tr><th>Player</th><th>Market</th><th class="num">Stake</th><th class="num">Posted</th>
<th class="num">EdgeW</th><th class="num">Vs posted</th><th>Screen</th></tr></thead>
<tbody>{"".join(ticket_rows_html) or "<tr><td colspan='7'>No tickets.</td></tr>"}</tbody>
</table>
<p class="foot">Paper / mock bankroll. Observation only. The system never auto-bets.</p>
</body>
</html>
"""


def _html_movement_rows(items: list[PaperMovement]) -> str:
    rows = []
    for i, m in enumerate(items):
        stripe = ' class="alt"' if i % 2 else ""
        after = f"${m.stake_after:.2f}" if m.stake_after is not None else "n/a"
        name = m.player_name
        if m.from_player_name:
            name = f"{name} (from {m.from_player_name})"
        rows.append(
            f"<tr{stripe}><td class='txt'>{html.escape(m.kind)} / {html.escape(m.status)}</td>"
            f"<td class='txt'>{html.escape(name)}</td>"
            f"<td class='num'>{m.stake_delta:+.2f}</td>"
            f"<td class='num'>{html.escape(after)}</td>"
            f"<td class='txt'>{html.escape(m.reason_plain)}</td>"
            f"<td class='txt'>{html.escape(m.amount_plain)}</td></tr>"
        )
    return "".join(rows)


def write_bets_explained_pdf(
    path: Path,
    record: PaperBookFile,
    *,
    title: str,
    subtitle: str,
    advice: list[PaperMovement],
    config: StrategyConfig,
) -> Path:
    from fpdf import FPDF
    from fpdf.fonts import FontFace

    _require_fpdf2()
    applied = [m for m in record.movements if m.status == "applied"]
    cash = record.bankroll - record.book.open_exposure
    stats = (
        f"Open ${record.book.open_exposure:.2f} / ${record.bankroll:.2f}    "
        f"Cash ${cash:.2f}    Applied moves {len(applied)}    "
        f"Advice this snapshot {len(advice)}    Not real money. Never auto-bet."
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
                "bets made  |  paper / mock  |  observation only  |  never auto-bet  |  "
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

    def section(heading: str) -> None:
        pdf.set_x(pdf.l_margin)
        pdf.set_font(face, "B", 11)
        pdf.set_text_color(18, 32, 42)
        pdf.cell(0, 7, heading, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)

    def para(text: str) -> None:
        pdf.set_x(pdf.l_margin)
        pdf.set_font(face, "", 8)
        pdf.set_text_color(70, 85, 95)
        pdf.multi_cell(0, 4.3, _pdf_text(text, face))
        pdf.ln(1)

    section("Observation only")
    para(observation_plain())
    para(observation_technical())
    section("Why the amounts")
    para(sizing_plain(config))
    para(sizing_technical(config))
    pdf.set_font(face, "B", 8)
    pdf.set_text_color(18, 32, 42)
    pdf.multi_cell(0, 4.4, _pdf_text(stats, face))
    pdf.ln(2)

    headings_style = FontFace(emphasis="BOLD", color=(255, 255, 255), fill_color=(31, 59, 77))
    headers = ("Action", "Player", "Delta", "After", "Why this name", "Why this amount")
    aligns = ("LEFT", "LEFT", "RIGHT", "RIGHT", "LEFT", "LEFT")
    widths = [pdf.epw * w for w in (0.10, 0.12, 0.08, 0.08, 0.31, 0.31)]

    def movement_table(items: list[PaperMovement], empty: str) -> None:
        pdf.set_font(face, size=8)
        pdf.set_text_color(18, 32, 42)
        with pdf.table(
            col_widths=widths,
            text_align=aligns,
            headings_style=headings_style,
            cell_fill_color=(243, 246, 248),
            cell_fill_mode="ROWS",
            first_row_as_headings=True,
            line_height=4.2,
            padding=1.1,
            v_align="TOP",
            width=pdf.epw,
            repeat_headings=1,
        ) as table:
            header_row = table.row()
            for h in headers:
                header_row.cell(_pdf_text(h, face))
            if not items:
                row = table.row()
                row.cell(_pdf_text(empty, face))
                for _ in range(5):
                    row.cell("")
            else:
                for m in items:
                    row = table.row()
                    row.cell(_pdf_text(f"{m.kind} / {m.status}", face))
                    name = m.player_name
                    if m.from_player_name:
                        name = f"{name} (from {m.from_player_name})"
                    row.cell(_pdf_text(name, face))
                    row.cell(_pdf_text(f"{m.stake_delta:+.2f}", face))
                    after = f"${m.stake_after:.2f}" if m.stake_after is not None else "n/a"
                    row.cell(_pdf_text(after, face))
                    row.cell(_pdf_text(m.reason_plain, face))
                    row.cell(_pdf_text(m.amount_plain, face))
        pdf.set_x(pdf.l_margin)
        pdf.ln(4)

    section("Applied movements (in the paper book)")
    movement_table(applied, "None recorded.")
    section("Live advice this snapshot (not applied unless --apply-paper)")
    movement_table(advice, "No hold/sell/add/reallocate advice on this snapshot.")
    section("Current tickets")
    pdf.set_font(face, size=8)
    t_headers = ("Player", "Market", "Stake", "Posted", "EdgeW", "Vs posted", "Screen")
    t_aligns = ("LEFT", "LEFT", "RIGHT", "RIGHT", "RIGHT", "RIGHT", "LEFT")
    t_widths = [pdf.epw * w for w in (0.16, 0.08, 0.09, 0.09, 0.09, 0.10, 0.39)]
    with pdf.table(
        col_widths=t_widths,
        text_align=t_aligns,
        headings_style=headings_style,
        cell_fill_color=(243, 246, 248),
        cell_fill_mode="ROWS",
        first_row_as_headings=True,
        line_height=4.2,
        padding=1.1,
        v_align="TOP",
        width=pdf.epw,
        repeat_headings=1,
    ) as table:
        header_row = table.row()
        for h in t_headers:
            header_row.cell(_pdf_text(h, face))
        rows = ticket_rows(record)
        if not rows:
            row = table.row()
            row.cell(_pdf_text("No tickets.", face))
            for _ in range(6):
                row.cell("")
        else:
            for t in rows:
                row = table.row()
                row.cell(_pdf_text(t.player_name, face))
                row.cell(_pdf_text(t.market, face))
                row.cell(_pdf_text(f"${t.stake:.2f}", face))
                row.cell(_pdf_text(f"{t.posted:.2f}", face))
                row.cell(_pdf_text(f"{t.edge_w * 100:+.1f}pp", face))
                row.cell(_pdf_text(f"{t.posted_edge * 100:+.1f}pp", face))
                row.cell(_pdf_text(t.screen, face))
    pdf.set_x(pdf.l_margin)
    pdf.output(str(path))
    return path
