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
    mark_pdf_printed,
    printed_at_utc,
    write_pdf_footer,
    write_pdf_print_stamp,
)
from golf_offshoot.strategy.paper_book import (
    PaperBookFile,
    PaperMovement,
    clocks_plain,
    format_paper_time,
    movement_clocks,
    observation_plain,
    observation_technical,
    sizing_plain,
    sizing_technical,
    ticket_rows,
    _fmt_dec,
    _fmt_pp,
)


def write_bets_explained_files(
    record: PaperBookFile,
    *,
    directory: Path,
    advice: list[PaperMovement] | None = None,
    config: StrategyConfig | None = None,
    live_outputs=None,
    live_run_id: str = "",
    title: str | None = None,
    subtitle: str | None = None,
) -> TableExportPaths:
    cfg = config or StrategyConfig(enabled=True, bankroll=record.bankroll)
    advice = advice if advice is not None else list(record.latest_advice)
    tickets = ticket_rows(record, live_outputs, live_run_id=live_run_id)
    directory.mkdir(parents=True, exist_ok=True)
    event = record.tournament_name or record.tournament_id
    title = title or f"Bets made — {event}"
    subtitle = subtitle or (
        f"${record.bankroll:.0f} mock   {record.odds_book or 'book n/a'}   "
        f"{record.mode}/{record.risk}   lock_run={record.locked_from_run_id or 'n/a'}   "
        f"live_run={live_run_id or 'n/a'}   model={MODEL_VERSION}"
    )
    txt = directory / "02_bets_explained.txt"
    html_path = directory / "02_bets_explained.html"
    pdf = directory / "02_bets_explained.pdf"
    body = bets_explained_document(
        record, advice=advice, config=cfg, tickets=tickets, heading=title
    )
    txt.write_text(body, encoding="utf-8")
    html_path.write_text(
        render_bets_explained_html(
            record,
            title=title,
            subtitle=subtitle,
            advice=advice,
            config=cfg,
            tickets=tickets,
        ),
        encoding="utf-8",
    )
    write_bets_explained_pdf(
        pdf,
        record,
        title=title,
        subtitle=subtitle,
        advice=advice,
        config=cfg,
        tickets=tickets,
    )
    return TableExportPaths(pdf=pdf, html=html_path, txt=txt)


def bets_explained_document(
    record: PaperBookFile,
    *,
    advice: list[PaperMovement],
    config: StrategyConfig,
    tickets=None,
    heading: str | None = None,
) -> str:
    cash = record.bankroll - record.book.open_exposure
    rows = tickets if tickets is not None else ticket_rows(record)
    pid = getattr(record, "path_id", None) or "lived"
    lines = [
        heading or f"BETS MADE  {record.tournament_name or record.tournament_id}",
        f"path={pid}",
        f"printed {printed_at_utc()}",
        f"${record.bankroll:.0f} mock  never_auto_bet=true  {record.mode}/{record.risk}",
        f"open ${record.book.open_exposure:.2f}  cash ${cash:.2f}  tickets={len(record.book.positions)}",
        "",
        "Observation only",
        observation_plain(),
        observation_technical(),
        "",
        clocks_plain(),
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
        lines.extend(_movement_lines(m, record=record))
    lines.append("")
    lines.append("Live advice this snapshot (not applied unless you pass --apply-paper)")
    if not advice:
        lines.append("  (no hold/sell/add/reallocate advice on this snapshot)")
    for m in advice:
        lines.extend(_movement_lines(m, record=record))
    lines.append("")
    lines.append("Current tickets (at entry vs this live)")
    for t in rows:
        entered = format_paper_time(getattr(t, "entered_at", None))
        lines.append(
            f"  {t.lane} {t.player_name} {t.market} now={t.board_now} entered {entered} ${t.stake:.2f} "
            f"entry@{t.posted:.2f} EdgeW={t.edge_w:+.3f} vs={t.posted_edge:+.3f} "
            f"live@{_fmt_dec(t.live_posted)} EdgeW={_fmt_pp(t.live_edge_w)} "
            f"vs={_fmt_pp(t.live_posted_edge)}"
        )
        lines.append(f"    {t.screen}")
    lines.append("")
    lines.append("Paper / mock. Observation only. The system never auto-bets.")
    return "\n".join(lines)


def _movement_lines(m: PaperMovement, *, record: PaperBookFile | None = None) -> list[str]:
    after = f"${m.stake_after:.2f}" if m.stake_after is not None else "n/a"
    donor = f" from {m.from_player_name}" if m.from_player_name else ""
    when, entered, exited = movement_clocks(record, m)
    return [
        f"  {m.kind.upper()} {m.status} {m.player_name}{donor} "
        f"when={when} entered={entered} exited={exited} "
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
    tickets=None,
) -> str:
    applied_rows = _html_movement_rows(
        [m for m in record.movements if m.status == "applied"], record=record
    )
    advice_rows = _html_movement_rows(advice, record=record)
    rows = tickets if tickets is not None else ticket_rows(record)
    ticket_rows_html = []
    for i, t in enumerate(rows):
        stripe = ' class="alt"' if i % 2 else ""
        entered = format_paper_time(getattr(t, "entered_at", None))
        ticket_rows_html.append(
            f"<tr{stripe}><td class='txt'>{html.escape(t.player_name)}</td>"
            f"<td class='num'>{html.escape(t.live_place)}</td>"
            f"<td class='num'>{html.escape(t.live_to_par)}</td>"
            f"<td class='num'>{html.escape(t.live_thru)}</td>"
            f"<td class='txt entered'>{html.escape(entered)}</td>"
            f"<td class='txt'>{html.escape(t.market)}</td>"
            f"<td class='num'>${t.stake:.2f}</td>"
            f"<td class='num'>{t.posted:.2f}</td>"
            f"<td class='num'>{t.edge_w * 100:+.1f}pp</td>"
            f"<td class='num'>{t.posted_edge * 100:+.1f}pp</td>"
            f"<td class='num'>{html.escape(_fmt_dec(t.live_posted))}</td>"
            f"<td class='num'>{html.escape(_fmt_pp(t.live_edge_w))}</td>"
            f"<td class='num'>{html.escape(_fmt_pp(t.live_posted_edge))}</td></tr>"
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
  .entered {{ white-space: nowrap; }}
  .foot {{ margin-top: 18px; }}
</style>
</head>
<body>
<h1>{html.escape(title)}</h1>
<p class="sub">{html.escape(subtitle)}</p>
<p class="sub">printed {html.escape(printed_at_utc())}</p>
<p class="caption"><strong>Observation only</strong></p>
<p class="caption">{html.escape(observation_plain())}</p>
<p class="caption">{html.escape(observation_technical())}</p>
<p class="caption">{html.escape(clocks_plain())}</p>
<h2>Why the amounts</h2>
<p class="caption">{html.escape(sizing_plain(config))}</p>
<p class="caption">{html.escape(sizing_technical(config))}</p>
<p class="caption">Open ${record.book.open_exposure:.2f} / ${record.bankroll:.2f}.
Cash unallocated ${cash:.2f}. Not real money. Never auto-bet.</p>
<h2>Applied movements (in the paper book)</h2>
<table>
<thead><tr><th>When (ET)</th><th>Entered</th><th>Exited</th><th>Action</th><th>Status</th><th>Player</th><th class="num">Delta</th><th class="num">After</th><th>Why this name</th><th>Why this amount</th></tr></thead>
<tbody>{applied_rows or "<tr><td colspan='10'>None recorded.</td></tr>"}</tbody>
</table>
<h2>Live advice this snapshot</h2>
<p class="caption">Hold / sell / add / reallocate suggestions. Not applied unless you pass --apply-paper.
Still mock. Still never a real bet.</p>
<table>
<thead><tr><th>When (ET)</th><th>Entered</th><th>Exited</th><th>Action</th><th>Status</th><th>Player</th><th class="num">Delta</th><th class="num">After</th><th>Why this name</th><th>Why this amount</th></tr></thead>
<tbody>{advice_rows or "<tr><td colspan='10'>No advice on this snapshot.</td></tr>"}</tbody>
</table>
<h2>Current tickets</h2>
<table>
<thead>
<tr>
<th rowspan="2">Player</th>
<th class="num" rowspan="2">Place</th><th class="num" rowspan="2">ToPar</th><th class="num" rowspan="2">Thru</th>
<th rowspan="2">Entered</th><th rowspan="2">Market</th><th class="num" rowspan="2">Stake</th>
<th colspan="3">At entry</th><th colspan="3">This live</th>
</tr>
<tr>
<th class="num">Posted</th><th class="num">EdgeW</th><th class="num">Vs posted</th>
<th class="num">Posted</th><th class="num">EdgeW</th><th class="num">Vs posted</th>
</tr>
</thead>
<tbody>{"".join(ticket_rows_html) or "<tr><td colspan='13'>No tickets.</td></tr>"}</tbody>
</table>
<p class="foot">Paper / mock bankroll. Observation only. The system never auto-bets.</p>
</body>
</html>
"""


def _html_movement_rows(
    items: list[PaperMovement], *, record: PaperBookFile | None = None
) -> str:
    rows = []
    for i, m in enumerate(items):
        stripe = ' class="alt"' if i % 2 else ""
        after = f"${m.stake_after:.2f}" if m.stake_after is not None else "n/a"
        name = m.player_name
        if m.from_player_name:
            name = f"{name} (from {m.from_player_name})"
        when, entered, exited = movement_clocks(record, m)
        rows.append(
            f"<tr{stripe}><td class='txt entered'>{html.escape(when)}</td>"
            f"<td class='txt entered'>{html.escape(entered)}</td>"
            f"<td class='txt entered'>{html.escape(exited)}</td>"
            f"<td class='txt'>{html.escape(m.kind)}</td>"
            f"<td class='txt'>{html.escape(m.status)}</td>"
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
    tickets=None,
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
            write_pdf_print_stamp(self, face)
            if self.page_no() == 1:
                self.set_font(face, "B", 14)
                self.set_text_color(18, 32, 42)
                self.cell(0, 7, _pdf_text(title, face), new_x="LMARGIN", new_y="NEXT")
                self.set_font(face, "", 8)
                self.set_text_color(70, 85, 95)
                self.cell(0, 4.5, _pdf_text(subtitle, face), new_x="LMARGIN", new_y="NEXT")
                self.ln(2)
            else:
                self.set_font(face, "B", 9)
                self.set_text_color(18, 32, 42)
                self.cell(0, 6, _pdf_text(f"{title}  (continued)", face), new_x="LMARGIN", new_y="NEXT")
                self.ln(1)

        def footer(self) -> None:
            face = getattr(self, "_table_font", "Helvetica")
            write_pdf_footer(self, face, "bets made")

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
    para(clocks_plain())
    section("Why the amounts")
    para(sizing_plain(config))
    para(sizing_technical(config))
    pdf.set_font(face, "B", 8)
    pdf.set_text_color(18, 32, 42)
    pdf.multi_cell(0, 4.4, _pdf_text(stats, face))
    pdf.ln(2)

    headings_style = FontFace(emphasis="BOLD", color=(255, 255, 255), fill_color=(31, 59, 77))
    headers = (
        "When (ET)",
        "Entered",
        "Exited",
        "Action",
        "Status",
        "Player",
        "Delta",
        "Why",
    )
    aligns = ("LEFT", "LEFT", "LEFT", "LEFT", "LEFT", "LEFT", "RIGHT", "LEFT")
    widths = [pdf.epw * w for w in (0.13, 0.13, 0.12, 0.08, 0.08, 0.12, 0.07, 0.27)]

    def movement_table(items: list[PaperMovement], empty: str) -> None:
        pdf.set_font(face, size=7)
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
                for _ in range(7):
                    row.cell("")
            else:
                for m in items:
                    row = table.row()
                    when, entered, exited = movement_clocks(record, m)
                    name = m.player_name
                    if m.from_player_name:
                        name = f"{name} (from {m.from_player_name})"
                    row.cell(_pdf_text(when, face))
                    row.cell(_pdf_text(entered, face))
                    row.cell(_pdf_text(exited, face))
                    row.cell(_pdf_text(m.kind, face))
                    row.cell(_pdf_text(m.status, face))
                    row.cell(_pdf_text(name, face))
                    row.cell(_pdf_text(f"{m.stake_delta:+.2f}", face))
                    row.cell(_pdf_text(m.reason_plain, face))
        pdf.set_x(pdf.l_margin)
        pdf.ln(4)

    section("Applied movements (in the paper book)")
    movement_table(applied, "None recorded.")
    section("Live advice this snapshot (not applied unless --apply-paper)")
    movement_table(advice, "No hold/sell/add/reallocate advice on this snapshot.")
    section("Current tickets (at entry vs this live)")
    pdf.set_font(face, size=7)
    t_headers = (
        "Player",
        "Place",
        "ToPar",
        "Thru",
        "Entered",
        "Market",
        "Stake",
        "Entry posted",
        "Entry EdgeW",
        "Entry vs",
        "Live posted",
        "Live EdgeW",
        "Live vs",
    )
    t_aligns = (
        "LEFT", "RIGHT", "RIGHT", "RIGHT", "LEFT", "LEFT", "RIGHT",
        "RIGHT", "RIGHT", "RIGHT", "RIGHT", "RIGHT", "RIGHT",
    )
    t_widths = [pdf.epw * w for w in (0.13, 0.04, 0.04, 0.035, 0.155, 0.075, 0.065, 0.09, 0.07, 0.07, 0.075, 0.07, 0.085)]
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
        rows = tickets if tickets is not None else ticket_rows(record)
        if not rows:
            row = table.row()
            row.cell(_pdf_text("No tickets.", face))
            for _ in range(12):
                row.cell("")
        else:
            for t in rows:
                row = table.row()
                row.cell(_pdf_text(t.player_name, face))
                row.cell(_pdf_text(t.live_place, face))
                row.cell(_pdf_text(t.live_to_par, face))
                row.cell(_pdf_text(t.live_thru, face))
                row.cell(_pdf_text(format_paper_time(getattr(t, "entered_at", None)), face))
                row.cell(_pdf_text(t.market, face))
                row.cell(_pdf_text(f"${t.stake:.2f}", face))
                row.cell(_pdf_text(f"{t.posted:.2f}", face))
                row.cell(_pdf_text(f"{t.edge_w * 100:+.1f}pp", face))
                row.cell(_pdf_text(f"{t.posted_edge * 100:+.1f}pp", face))
                row.cell(_pdf_text(_fmt_dec(t.live_posted), face))
                row.cell(_pdf_text(_fmt_pp(t.live_edge_w), face))
                row.cell(_pdf_text(_fmt_pp(t.live_posted_edge), face))
    pdf.set_x(pdf.l_margin)
    pdf.output(str(path))
    return path
