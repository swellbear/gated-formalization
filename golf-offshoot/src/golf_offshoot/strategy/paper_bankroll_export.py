"""Bankroll / week / lifetime readout for paper packs. Never real money."""

from __future__ import annotations

import html
from pathlib import Path

from golf_offshoot.config import MODEL_VERSION
from golf_offshoot.ranking.export_table import (
    TableExportPaths,
    _pdf_text,
    _register_pdf_font,
    _require_fpdf2,
)
from golf_offshoot.strategy.paper_book import PaperBookFile, format_paper_time, movement_clocks
from golf_offshoot.strategy.paper_ledger import EventWeek, PaperLedger, load_ledger


def write_bankroll_files(
    directory: Path,
    *,
    ledger: PaperLedger | None = None,
    record: PaperBookFile | None = None,
    week: EventWeek | None = None,
    title: str | None = None,
) -> TableExportPaths:
    ledger = ledger or load_ledger()
    directory.mkdir(parents=True, exist_ok=True)
    if not title:
        title = "Paper bankroll — week and lifetime"
        if record:
            title = f"Paper bankroll — {record.tournament_name or record.tournament_id}"
    subtitle = (
        f"current ${ledger.bankroll:.2f} mock   deposits ${ledger.deposits:.2f}   "
        f"withdrawals ${ledger.withdrawals:.2f}   betting P/L ${ledger.betting_pnl:+.2f}   "
        f"model={MODEL_VERSION}"
    )
    snap = _open_snapshot(ledger, record) if record else None
    if snap:
        open_exp, cash, settled = snap
        subtitle = (
            f"current ${ledger.bankroll:.2f} mock   open ${open_exp:.2f}   "
            f"cash ${cash:.2f}   settled={'yes' if settled else 'no'}   "
            f"deposits ${ledger.deposits:.2f}   betting P/L ${ledger.betting_pnl:+.2f}   "
            f"model={MODEL_VERSION}"
        )
    txt = directory / "05_bankroll.txt"
    html_path = directory / "05_bankroll.html"
    pdf = directory / "05_bankroll.pdf"
    txt.write_text(bankroll_document(ledger, record=record, week=week), encoding="utf-8")
    html_path.write_text(
        render_bankroll_html(ledger, title=title, subtitle=subtitle, record=record, week=week),
        encoding="utf-8",
    )
    write_bankroll_pdf(pdf, ledger, title=title, subtitle=subtitle, record=record, week=week)
    return TableExportPaths(pdf=pdf, html=html_path, txt=txt)


def bankroll_document(
    ledger: PaperLedger,
    *,
    record: PaperBookFile | None = None,
    week: EventWeek | None = None,
) -> str:
    lines = [
        "PAPER BANKROLL  never_auto_bet=true  mock only",
        f"current ${ledger.bankroll:.2f}  starting ${ledger.starting_bankroll:.2f}  "
        f"deposits ${ledger.deposits:.2f}  withdrawals ${ledger.withdrawals:.2f}  "
        f"betting P/L ${ledger.betting_pnl:+.2f}",
        "",
        "In plain language: this is fake money that rolls from week to week. Wins add to "
        "the bankroll. Losses come out of it. Deposits you record are added. Withdrawals "
        "you record are subtracted. The system never places a real bet.",
        "Technical: bankroll changes only on deposit, withdrawal, settled ticket P/L "
        "(payout minus stake), and applied cash-out P/L (typed quote or estimated "
        "offer minus sold stake). Estimated sells keep 80% of the odds-ratio MTM gap "
        "(20% haircut) and are labeled estimated; they are not scraped Open Bets. "
        "Open tickets sit at cost until the event is official. "
        "live / paper-ledger / paper-export auto-settle when ESPN is clearly final with "
        "exactly one winner. Mid-round sells without live posted odds return stake at cost. "
        "A typed --cash-out quote still overrides the estimate.",
    ]
    if record:
        open_exp, cash, settled = _open_snapshot(ledger, record)
        lines += [
            "",
            f"This event: {record.tournament_name or record.tournament_id}",
            f"open tickets ${open_exp:.2f}  cash-at-cost ${cash:.2f}  "
            f"settled={'yes' if settled else 'no'}",
        ]
        if record.book.positions:
            for p in record.book.positions:
                kind = p.bet_type.value if hasattr(p.bet_type, "value") else str(p.bet_type)
                lines.append(
                    f"  open {p.player_name} {kind} ${p.stake:.2f} @ {p.decimal_odds:.2f} "
                    f"if_wins=${p.stake * p.decimal_odds:.2f}"
                )
        if record.settled_at:
            lines.append(
                f"settled_at={record.settled_at.isoformat()} winner={record.settlement_winner} "
                f"event P/L ${record.settlement_pnl or 0:+.2f}"
            )
        else:
            lines.append(
                "Not settled yet. live auto-settles when ESPN marks the event final "
                "with exactly one winner; or run paper-settle."
            )
        lines.append("This week's applied moves")
        if not record.movements:
            lines.append("  (none)")
        for m in record.movements:
            when, entered, exited = movement_clocks(record, m)
            lines.append(
                f"  {when} {m.kind} {m.status} {m.player_name} "
                f"entered={entered} exited={exited} delta={m.stake_delta:+.2f}  {m.reason_plain}"
            )
    week = week or _week_for(ledger, record)
    if week:
        lines += ["", f"Week settlement {week.event_name or week.event_id}  winner={week.winner_name}"]
        for t in week.tickets:
            lines.append(
                f"  {'WIN' if t.won else 'LOSS'} {t.player_name} {t.bet_type} "
                f"${t.stake:.2f} @ {t.decimal_odds:.2f} finish={t.finish if t.finish is not None else 'n/a'} "
                f"payout=${t.payout:.2f} pnl={t.pnl:+.2f}"
            )
        lines.append(
            f"  event P/L ${week.betting_pnl:+.2f}  bankroll {week.bankroll_before:.2f} -> {week.bankroll_after:.2f}"
        )
    lines += ["", "Lifetime events"]
    if not ledger.events:
        lines.append("  (none settled yet)")
    for ev in ledger.events:
        lines.append(
            f"  {ev.event_name or ev.event_id}  P/L ${ev.betting_pnl:+.2f}  "
            f"${ev.bankroll_before:.2f} -> ${ev.bankroll_after:.2f}  winner={ev.winner_name or 'n/a'}"
        )
    lines += ["", "Cash movements"]
    cash_kinds = {"deposit", "withdrawal", "cashout"}
    cash_rows = [e for e in ledger.entries if e.kind in cash_kinds]
    if not cash_rows:
        lines.append("  (none)")
    for e in cash_rows:
        lines.append(
            f"  {e.at.strftime('%Y-%m-%d')} {e.kind} {e.amount:+.2f} -> ${e.bankroll_after:.2f}  {e.note}"
        )
    lines.append("")
    lines.append("Paper / mock. Observation only. The system never auto-bets.")
    return "\n".join(lines)


def _open_snapshot(ledger: PaperLedger, record: PaperBookFile) -> tuple[float, float, bool]:
    open_exp = round(record.book.open_exposure, 2)
    base = record.bankroll if record.settled_at else ledger.bankroll
    cash = round(max(0.0, base - open_exp), 2)
    return open_exp, cash, bool(record.settled_at)


def _week_for(ledger: PaperLedger, record: PaperBookFile | None) -> EventWeek | None:
    if record is None:
        return ledger.events[-1] if ledger.events else None
    for ev in reversed(ledger.events):
        if ev.event_id == record.tournament_id:
            return ev
    return None


def render_bankroll_html(
    ledger: PaperLedger,
    *,
    title: str,
    subtitle: str,
    record: PaperBookFile | None,
    week: EventWeek | None,
) -> str:
    week = week or _week_for(ledger, record)
    ticket_rows = ""
    if week:
        parts = []
        for i, t in enumerate(week.tickets):
            stripe = ' class="alt"' if i % 2 else ""
            parts.append(
                f"<tr{stripe}><td>{html.escape('WIN' if t.won else 'LOSS')}</td>"
                f"<td>{html.escape(t.player_name)}</td><td>{html.escape(t.bet_type)}</td>"
                f"<td class='num'>${t.stake:.2f}</td><td class='num'>{t.decimal_odds:.2f}</td>"
                f"<td class='num'>{t.finish if t.finish is not None else 'n/a'}</td>"
                f"<td class='num'>${t.payout:.2f}</td><td class='num'>{t.pnl:+.2f}</td></tr>"
            )
        ticket_rows = "".join(parts)
    event_rows = ""
    for i, ev in enumerate(ledger.events):
        stripe = ' class="alt"' if i % 2 else ""
        event_rows += (
            f"<tr{stripe}><td>{html.escape(ev.event_name or ev.event_id)}</td>"
            f"<td>{html.escape(ev.winner_name or 'n/a')}</td>"
            f"<td class='num'>{ev.betting_pnl:+.2f}</td>"
            f"<td class='num'>${ev.bankroll_before:.2f}</td>"
            f"<td class='num'>${ev.bankroll_after:.2f}</td></tr>"
        )
    move_rows = ""
    if record:
        for i, m in enumerate(record.movements):
            stripe = ' class="alt"' if i % 2 else ""
            move_rows += (
                f"<tr{stripe}><td>{html.escape(format_paper_time(m.at))}</td>"
                f"<td>{html.escape(movement_clocks(record, m)[1])}</td>"
                f"<td>{html.escape(movement_clocks(record, m)[2])}</td>"
                f"<td>{html.escape(m.kind)}</td><td>{html.escape(m.status)}</td>"
                f"<td>{html.escape(m.player_name)}</td>"
                f"<td class='num'>{m.stake_delta:+.2f}</td>"
                f"<td>{html.escape(m.reason_plain)}</td></tr>"
            )
    cash_rows = ""
    for i, e in enumerate(e for e in ledger.entries if e.kind in {"deposit", "withdrawal", "cashout"}):
        stripe = ' class="alt"' if i % 2 else ""
        cash_rows += (
            f"<tr{stripe}><td>{html.escape(e.at.strftime('%Y-%m-%d'))}</td>"
            f"<td>{html.escape(e.kind)}</td><td class='num'>{e.amount:+.2f}</td>"
            f"<td class='num'>${e.bankroll_after:.2f}</td><td>{html.escape(e.note)}</td></tr>"
        )
    settled = "yes" if record and record.settled_at else "no"
    open_block = ""
    if record:
        open_exp, cash, settled_flag = _open_snapshot(ledger, record)
        pos_parts = []
        for i, p in enumerate(record.book.positions):
            stripe = ' class="alt"' if i % 2 else ""
            kind = p.bet_type.value if hasattr(p.bet_type, "value") else str(p.bet_type)
            pos_parts.append(
                f"<tr{stripe}><td>{html.escape(p.player_name)}</td>"
                f"<td>{html.escape(format_paper_time(p.entered_at))}</td>"
                f"<td>{html.escape(kind)}</td>"
                f"<td class='num'>${p.stake:.2f}</td>"
                f"<td class='num'>{p.decimal_odds:.2f}</td>"
                f"<td class='num'>${p.stake * p.decimal_odds:.2f}</td></tr>"
            )
        pos_body = "".join(pos_parts) or "<tr><td colspan='6'>No open tickets.</td></tr>"
        open_block = f"""
<h2>Open exposure</h2>
<p class="caption">Open tickets ${open_exp:.2f} sit at cost. Cash at cost ${cash:.2f}.
Settled: {'yes' if settled_flag else 'no'}.</p>
<table><thead><tr><th>Player</th><th>Entered</th><th>Market</th><th class="num">Stake</th>
<th class="num">Posted</th><th class="num">If wins</th></tr></thead>
<tbody>{pos_body}</tbody></table>
"""
    week_block = ""
    if week:
        week_block = f"""
<h2>Week settlement</h2>
<p class="caption">Winner: {html.escape(week.winner_name or 'n/a')}. Event P/L ${week.betting_pnl:+.2f}.
Bankroll ${week.bankroll_before:.2f} to ${week.bankroll_after:.2f}.</p>
<table><thead><tr><th>Result</th><th>Player</th><th>Market</th><th class="num">Stake</th>
<th class="num">Posted</th><th class="num">Finish</th><th class="num">Payout</th><th class="num">P/L</th></tr></thead>
<tbody>{ticket_rows or "<tr><td colspan='8'>No tickets settled.</td></tr>"}</tbody></table>
"""
    moves_block = ""
    if record:
        moves_block = f"""
<h2>This week's applied moves</h2>
<table><thead><tr><th>When (UTC)</th><th>Entered</th><th>Exited</th><th>Action</th><th>Status</th><th>Player</th><th class="num">Delta</th><th>Why</th></tr></thead>
<tbody>{move_rows or "<tr><td colspan='8'>None.</td></tr>"}</tbody></table>
"""
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/><title>{html.escape(title)}</title>
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
</style></head><body>
<h1>{html.escape(title)}</h1>
<p class="sub">{html.escape(subtitle)}</p>
<p class="caption"><strong>Observation only.</strong> Fake money that rolls week to week.
Wins add to the bankroll. Losses come out. Deposits you record are added. The system never places a real bet.</p>
<p class="caption">Technical: bankroll changes on deposit, withdrawal, settled ticket P/L (payout minus stake),
and applied cash-out P/L (typed quote or estimated offer minus sold stake).
Estimated sells haircut 20% of the odds-ratio MTM gap and are not scraped Open Bets.
Open tickets sit at cost until ESPN is clearly final. live / paper-ledger / paper-export auto-settle then. Settled this event: {settled}.</p>
{open_block}
{moves_block}
{week_block}
<h2>Lifetime events</h2>
<table><thead><tr><th>Event</th><th>Winner</th><th class="num">P/L</th><th class="num">Before</th><th class="num">After</th></tr></thead>
<tbody>{event_rows or "<tr><td colspan='5'>None settled yet.</td></tr>"}</tbody></table>
<h2>Deposits, withdrawals, and cash-outs</h2>
<table><thead><tr><th>Date</th><th>Kind</th><th class="num">Amount</th><th class="num">Bankroll after</th><th>Note</th></tr></thead>
<tbody>{cash_rows or "<tr><td colspan='5'>None.</td></tr>"}</tbody></table>
<p class="foot">Paper / mock. Observation only. The system never auto-bets.</p>
</body></html>
"""


def write_bankroll_pdf(
    path: Path,
    ledger: PaperLedger,
    *,
    title: str,
    subtitle: str,
    record: PaperBookFile | None,
    week: EventWeek | None,
) -> Path:
    from fpdf import FPDF
    from fpdf.fonts import FontFace

    _require_fpdf2()
    week = week or _week_for(ledger, record)

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
                "paper bankroll  |  mock  |  observation only  |  never auto-bet  |  "
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
    headings_style = FontFace(emphasis="BOLD", color=(255, 255, 255), fill_color=(31, 59, 77))

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
    para(
        "In plain language: this is fake money that rolls from week to week. Wins add to "
        "the bankroll. Losses come out of it. Deposits you record are added. Withdrawals "
        "you record are subtracted. The system never places a real bet."
    )
    para(
        "Technical: bankroll changes only on deposit, withdrawal, settled ticket P/L "
        "(payout minus stake), and applied cash-out P/L (typed quote or estimated "
        "offer minus sold stake). Estimated sells keep 80% of the odds-ratio MTM gap "
        "(20% haircut) and are labeled estimated; they are not scraped Open Bets. "
        "Open tickets sit at cost until ESPN is clearly final. "
        "live / paper-ledger / paper-export auto-settle then."
    )
    stats = (
        f"Current ${ledger.bankroll:.2f}    starting ${ledger.starting_bankroll:.2f}    "
        f"deposits ${ledger.deposits:.2f}    withdrawals ${ledger.withdrawals:.2f}    "
        f"betting P/L ${ledger.betting_pnl:+.2f}    never auto-bet"
    )
    if record:
        open_exp, cash, settled = _open_snapshot(ledger, record)
        stats = (
            f"Current ${ledger.bankroll:.2f}    open tickets ${open_exp:.2f}    "
            f"cash at cost ${cash:.2f}    settled={'yes' if settled else 'no'}    "
            f"deposits ${ledger.deposits:.2f}    betting P/L ${ledger.betting_pnl:+.2f}"
        )
    pdf.set_font(face, "B", 8)
    pdf.set_text_color(18, 32, 42)
    pdf.multi_cell(0, 4.4, _pdf_text(stats, face))
    pdf.ln(2)

    def table(headers: tuple[str, ...], aligns: tuple[str, ...], widths: list[float], rows: list[list[str]], empty: str) -> None:
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
        ) as tbl:
            header_row = tbl.row()
            for h in headers:
                header_row.cell(_pdf_text(h, face))
            if not rows:
                row = tbl.row()
                row.cell(_pdf_text(empty, face))
                for _ in range(len(headers) - 1):
                    row.cell("")
            else:
                for cells in rows:
                    row = tbl.row()
                    for cell in cells:
                        row.cell(_pdf_text(cell, face))
        pdf.set_x(pdf.l_margin)
        pdf.ln(4)

    if record:
        open_exp, cash, settled = _open_snapshot(ledger, record)
        section("Open exposure")
        para(
            f"Open tickets ${open_exp:.2f} sit at cost on this event. "
            f"Cash at cost ${cash:.2f}. Settled: {'yes' if settled else 'no'}."
        )
        table(
            ("Player", "Entered", "Market", "Stake", "Posted", "If wins"),
            ("LEFT", "LEFT", "LEFT", "RIGHT", "RIGHT", "RIGHT"),
            [pdf.epw * w for w in (0.20, 0.18, 0.12, 0.14, 0.16, 0.20)],
            [
                [
                    p.player_name,
                    format_paper_time(p.entered_at),
                    p.bet_type.value if hasattr(p.bet_type, "value") else str(p.bet_type),
                    f"${p.stake:.2f}",
                    f"{p.decimal_odds:.2f}",
                    f"${p.stake * p.decimal_odds:.2f}",
                ]
                for p in record.book.positions
            ],
            "No open tickets.",
        )
    if record and record.movements:
        section("This week's applied moves")
        table(
            ("When UTC", "Entered", "Exited", "Action", "Status", "Player", "Delta", "Why"),
            ("LEFT", "LEFT", "LEFT", "LEFT", "LEFT", "LEFT", "RIGHT", "LEFT"),
            [pdf.epw * w for w in (0.13, 0.13, 0.10, 0.08, 0.08, 0.12, 0.08, 0.28)],
            [
                [
                    *movement_clocks(record, m),
                    m.kind,
                    m.status,
                    m.player_name,
                    f"{m.stake_delta:+.2f}",
                    m.reason_plain,
                ]
                for m in record.movements
            ],
            "None.",
        )
    if week:
        section(f"Week settlement — {week.event_name or week.event_id}")
        para(
            f"Winner {week.winner_name or 'n/a'}. Event P/L ${week.betting_pnl:+.2f}. "
            f"Bankroll ${week.bankroll_before:.2f} to ${week.bankroll_after:.2f}."
        )
        table(
            ("Result", "Player", "Market", "Stake", "Posted", "Finish", "Payout", "P/L"),
            ("LEFT", "LEFT", "LEFT", "RIGHT", "RIGHT", "RIGHT", "RIGHT", "RIGHT"),
            [pdf.epw * w for w in (0.09, 0.18, 0.10, 0.10, 0.10, 0.10, 0.16, 0.17)],
            [
                [
                    "WIN" if t.won else "LOSS",
                    t.player_name,
                    t.bet_type,
                    f"${t.stake:.2f}",
                    f"{t.decimal_odds:.2f}",
                    str(t.finish) if t.finish is not None else "n/a",
                    f"${t.payout:.2f}",
                    f"{t.pnl:+.2f}",
                ]
                for t in week.tickets
            ],
            "No tickets settled.",
        )
    elif record and not record.settled_at:
        section("Week settlement")
        para("Not settled yet. live auto-settles when ESPN is clearly final with one winner. Do not invent a winner.")

    section("Lifetime events")
    table(
        ("Event", "Winner", "P/L", "Before", "After"),
        ("LEFT", "LEFT", "RIGHT", "RIGHT", "RIGHT"),
        [pdf.epw * w for w in (0.36, 0.22, 0.14, 0.14, 0.14)],
        [
            [
                ev.event_name or ev.event_id,
                ev.winner_name or "n/a",
                f"{ev.betting_pnl:+.2f}",
                f"${ev.bankroll_before:.2f}",
                f"${ev.bankroll_after:.2f}",
            ]
            for ev in ledger.events
        ],
        "None settled yet.",
    )
    section("Deposits, withdrawals, and cash-outs")
    cash = [e for e in ledger.entries if e.kind in {"deposit", "withdrawal", "cashout"}]
    table(
        ("Date", "Kind", "Amount", "Bankroll after", "Note"),
        ("LEFT", "LEFT", "RIGHT", "RIGHT", "LEFT"),
        [pdf.epw * w for w in (0.14, 0.14, 0.14, 0.16, 0.42)],
        [
            [
                e.at.strftime("%Y-%m-%d"),
                e.kind,
                f"{e.amount:+.2f}",
                f"${e.bankroll_after:.2f}",
                e.note,
            ]
            for e in cash
        ],
        "None.",
    )
    pdf.output(str(path))
    return path
