"""Front-of-pack trigger list: this snapshot's actions, nothing else."""

from __future__ import annotations

import html
from dataclasses import dataclass
from pathlib import Path

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
from golf_offshoot.strategy.paper_book import PaperBookFile, PaperMovement

# Collapse sells / reallocates are not a pull before anyone is on the board.
_PRE_TEE_BLOCKED = frozenset({"exit", "reduce", "reallocate"})

# Do-this-now first. HOLD last so the pull is at the top of the page.
_KIND_SECTION: dict[str, tuple[int, str]] = {
    "exit": (0, "SELL"),
    "reallocate": (1, "REALLOCATE"),
    "reduce": (2, "PARTIAL SELL"),
    "add": (3, "ADD"),
    "new_bet": (4, "NEW"),
    "lock": (4, "NEW"),
    "hold": (5, "HOLD"),
}

_MARKET = {
    "win": "Win",
    "top_5": "Top 5",
    "top_10": "Top 10",
    "top_20": "Top 20",
    "make_cut": "Make cut",
    "win_after_r1": "R1 leader",
    "win_after_r2": "R2 leader",
    "win_after_r3": "R3 leader",
}
_MARKET_ORDER = {
    "Win": 0,
    "Top 5": 1,
    "Top 10": 2,
    "Top 20": 3,
    "Make cut": 4,
    "R1 leader": 5,
    "R2 leader": 6,
    "R3 leader": 7,
}


@dataclass(frozen=True)
class TriggerRow:
    name: str
    market: str
    extra: str = ""
    amount: str = ""
    sort_stake: float = 0.0


@dataclass(frozen=True)
class TriggerSection:
    order: int
    label: str
    rows: list[TriggerRow]


def market_label(bet_type: str) -> str:
    key = (bet_type or "win").replace("-", "_").lower()
    return _MARKET.get(key, key.replace("_", " ").title())


def sanitize_pre_tee_advice(
    advice: list[PaperMovement],
    rows: list | None,
) -> list[PaperMovement]:
    """Pack/live reprint: quote drift before tee is HOLD, not SELL.

    Typed --cash-out (a real quote, not estimated, not a bid mark) can still EXIT.
    Blank or missing ESPN board is not in-play.
    """
    from golf_offshoot.strategy import explanations as X
    from golf_offshoot.strategy.live import golf_has_started

    if golf_has_started(list(rows or [])):
        return list(advice)
    out: list[PaperMovement] = []
    for m in advice:
        kind = (m.kind or "").lower()
        typed = (
            m.cashout_quote is not None
            and not m.cashout_estimated
            and not m.mtm_is_bid
        )
        if kind in _PRE_TEE_BLOCKED and not typed:
            out.append(
                m.model_copy(
                    update={
                        "kind": "hold",
                        "stake_delta": 0.0,
                        "reason_plain": X.pre_tee_hold(),
                        "amount_plain": "",
                    }
                )
            )
        else:
            out.append(m)
    return out


def pre_tee_trigger_note(moves: list[PaperMovement]) -> str:
    from golf_offshoot.strategy import explanations as X

    for m in moves:
        if (m.kind or "").lower() != "hold":
            continue
        if "has not started" in (m.reason_plain or "").lower():
            return X.pre_tee_hold()
    return ""


def trigger_movements(
    record: PaperBookFile,
    advice: list[PaperMovement] | None = None,
    *,
    run_id: str = "",
) -> list[PaperMovement]:
    """This snapshot only. Advice if present; else this run's applied opens."""
    if advice:
        return [m for m in advice if (m.kind or "").lower() in _KIND_SECTION]
    run = (run_id or "").strip()
    out: list[PaperMovement] = []
    for m in record.movements:
        if m.status != "applied":
            continue
        kind = (m.kind or "").lower()
        if kind not in _KIND_SECTION:
            continue
        if run and (m.run_id or "") != run:
            continue
        out.append(m)
    return out


def group_trigger_actions(moves: list[PaperMovement]) -> list[TriggerSection]:
    buckets: dict[int, tuple[str, list[TriggerRow]]] = {}
    for m in moves:
        kind = (m.kind or "").lower()
        mapped = _KIND_SECTION.get(kind)
        if mapped is None:
            continue
        order, label = mapped
        extra = ""
        if kind == "reallocate" and m.from_player_name:
            extra = f"from {m.from_player_name}"
        extra = _bid_extra(m, extra)
        reason = f"{m.reason_plain or ''} {m.reason_technical or ''}".lower()
        if "take the pop" in reason:
            extra = "TAKE THE POP  " + extra if extra else "TAKE THE POP"
        elif "flip failed" in reason or "flip is dead" in reason:
            extra = "FLIP FAILED  " + extra if extra else "FLIP FAILED"
        elif (getattr(m, "intent", "") or "").lower() == "flip" and kind == "new_bet":
            extra = "FLIP  " + extra if extra else "FLIP"
        row = TriggerRow(
            name=(m.player_name or "").strip() or "n/a",
            market=market_label(m.bet_type),
            extra=extra,
            amount=_action_amount(m, kind),
            sort_stake=abs(float(m.stake_delta or 0.0)),
        )
        if order not in buckets:
            buckets[order] = (label, [])
        buckets[order][1].append(row)
    sections: list[TriggerSection] = []
    for order in sorted(buckets):
        label, rows = buckets[order]
        rows.sort(
            key=lambda r: (-r.sort_stake, r.name.lower(), _MARKET_ORDER.get(r.market, 9), r.market)
        )
        sections.append(TriggerSection(order=order, label=label, rows=rows))
    return sections


def _bid_extra(m: PaperMovement, extra: str) -> str:
    parts = [extra] if extra else []
    if m.live_bid is not None:
        parts.append(f"bid {m.live_bid:.3f}")
    if m.min_sell_price is not None:
        parts.append(f"min-sell {m.min_sell_price:.3f}")
    if m.cashout_quote is not None and m.mtm_is_bid:
        parts.append(f"offer ${m.cashout_quote:.2f}")
    return "  ".join(parts)


def _action_amount(m: PaperMovement, kind: str) -> str:
    """Dollars to move. Blank on HOLD."""
    if kind == "hold":
        return ""
    amt = abs(float(m.stake_delta or 0.0))
    if kind in {"exit", "reduce"}:
        if m.stake_before is not None and m.stake_after is not None:
            sold = max(0.0, float(m.stake_before) - float(m.stake_after))
            if sold > 0:
                amt = sold
        elif kind == "exit" and m.stake_before is not None and amt <= 0:
            amt = abs(float(m.stake_before))
    if amt <= 0:
        return ""
    return f"${amt:.2f}"


def trigger_headline(sections: list[TriggerSection]) -> str:
    if not sections:
        return "NO ACTIONS THIS SNAPSHOT"
    pull = [s for s in sections if s.label != "HOLD"]
    if not pull:
        return "NOTHING TO PULL — all HOLD"
    n = sum(len(s.rows) for s in pull)
    return f"PULL — {n}"


def trigger_document(
    record: PaperBookFile,
    *,
    advice: list[PaperMovement] | None = None,
    run_id: str = "",
    heading: str | None = None,
) -> str:
    from golf_offshoot.strategy.tape import fill_tape_lines

    moves = trigger_movements(record, advice, run_id=run_id)
    sections = group_trigger_actions(moves)
    note = pre_tee_trigger_note(moves)
    tape = fill_tape_lines(record, moves=moves)
    event = record.tournament_name or record.tournament_id
    lines = [
        heading or f"TRIGGER  {event}",
        f"printed {printed_at_utc()}",
        trigger_headline(sections),
        "",
    ]
    if note:
        lines.append(note)
        lines.append("")
    if not sections:
        lines.append("(none)")
    for section in sections:
        lines.append(section.label)
        for row in section.rows:
            extra = f"  {row.extra}" if row.extra else ""
            amt = f"  {row.amount}" if row.amount else ""
            lines.append(f"  {row.name}  {row.market}{amt}{extra}")
        lines.append("")
    lines.extend(["FILL TAPE  (display; not a sell)", *tape, ""])
    lines.append("This snapshot only. Mock. Never auto-bet.")
    return "\n".join(lines).rstrip() + "\n"


def write_trigger_files(
    record: PaperBookFile,
    *,
    directory: Path,
    advice: list[PaperMovement] | None = None,
    run_id: str = "",
    stem: str = "00_trigger",
    title: str | None = None,
) -> TableExportPaths:
    from golf_offshoot.strategy.tape import fill_tape_lines

    directory.mkdir(parents=True, exist_ok=True)
    event = record.tournament_name or record.tournament_id
    title = title or f"TRIGGER  {event}"
    moves = trigger_movements(record, advice, run_id=run_id)
    sections = group_trigger_actions(moves)
    note = pre_tee_trigger_note(moves)
    tape = fill_tape_lines(record, moves=moves)
    body = trigger_document(record, advice=advice, run_id=run_id, heading=title)
    txt = directory / f"{stem}.txt"
    html_path = directory / f"{stem}.html"
    pdf = directory / f"{stem}.pdf"
    txt.write_text(body, encoding="utf-8")
    html_path.write_text(
        _render_trigger_html(title=title, sections=sections, note=note, tape=tape),
        encoding="utf-8",
    )
    write_trigger_pdf(pdf, title=title, sections=sections, note=note, tape=tape)
    return TableExportPaths(pdf=pdf, html=html_path, txt=txt)


def _render_trigger_html(
    *, title: str, sections: list[TriggerSection], note: str = "", tape: list[str] | None = None
) -> str:
    headline = trigger_headline(sections)
    blocks = [f"<h1>{html.escape(title)}</h1>", f"<p class='when'>printed {html.escape(printed_at_utc())}</p>"]
    blocks.append(f"<p class='head'>{html.escape(headline)}</p>")
    if note:
        blocks.append(f"<p class='empty'>{html.escape(note)}</p>")
    if not sections:
        blocks.append("<p class='empty'>(none)</p>")
    for section in sections:
        blocks.append(f"<h2>{html.escape(section.label)}</h2>")
        blocks.append("<ul>")
        for row in section.rows:
            extra = f" <span class='extra'>{html.escape(row.extra)}</span>" if row.extra else ""
            amt = (
                f"<span class='amt'>{html.escape(row.amount)}</span>"
                if row.amount
                else "<span class='amt'></span>"
            )
            blocks.append(
                "<li><span class='name'>"
                f"{html.escape(row.name)}</span>"
                f"<span class='mkt'>{html.escape(row.market)}</span>"
                f"{amt}{extra}</li>"
            )
        blocks.append("</ul>")
    if tape:
        blocks.append("<h2>FILL TAPE</h2>")
        blocks.append("<p class='empty'>display only — not a sell</p>")
        blocks.append("<ul>")
        for line in tape:
            blocks.append(f"<li class='tape'>{html.escape(line.strip())}</li>")
        blocks.append("</ul>")
    return (
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        f"<title>{html.escape(title)}</title>"
        "<style>"
        "body{font-family:Georgia,'Times New Roman',serif;margin:36px auto;max-width:640px;"
        "color:#12202a}"
        "h1{font-size:28px;letter-spacing:.08em;margin:0 0 6px}"
        ".when{color:#46555f;font-size:13px;margin:0 0 18px}"
        ".head{font-size:20px;font-weight:700;margin:0 0 22px}"
        "h2{font-size:13px;letter-spacing:.14em;margin:22px 0 8px;color:#1f3b4d}"
        "ul{list-style:none;margin:0;padding:0}"
        "li{display:flex;gap:16px;font-size:20px;line-height:1.45;"
        "border-bottom:1px solid #e6eaed;padding:6px 0}"
        "li.tape{display:block;font-size:14px;color:#5a646c}"
        ".name{flex:1}"
        ".mkt{width:6.5rem;text-align:right;color:#1f3b4d}"
        ".amt{width:5.5rem;text-align:right;font-weight:700}"
        ".extra{color:#5a646c;font-size:14px;align-self:center}"
        ".empty{color:#5a646c}"
        "</style></head><body>"
        + "\n".join(blocks)
        + "<p style='margin-top:28px;color:#5a646c;font-size:12px'>"
        "This snapshot only. Mock. Never auto-bet.</p>"
        "</body></html>\n"
    )


def write_trigger_pdf(
    path: Path,
    *,
    title: str,
    sections: list[TriggerSection],
    note: str = "",
    tape: list[str] | None = None,
) -> Path:
    from fpdf import FPDF

    _require_fpdf2()
    headline = trigger_headline(sections)

    class Report(FPDF):
        def header(self) -> None:
            face = getattr(self, "_table_font", "Helvetica")
            self.set_x(self.l_margin)
            write_pdf_print_stamp(self, face)
            self.set_font(face, "B", 18)
            self.set_text_color(18, 32, 42)
            self.cell(0, 10, _pdf_text(title, face), new_x="LMARGIN", new_y="NEXT")
            self.ln(1)

        def footer(self) -> None:
            face = getattr(self, "_table_font", "Helvetica")
            write_pdf_footer(self, face, "trigger")

    pdf = Report(orientation="P", unit="mm", format="Letter")
    face = _register_pdf_font(pdf)
    pdf._table_font = face
    mark_pdf_printed(pdf)
    if face == "Helvetica":
        pdf.core_fonts_encoding = "cp1252"
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(18, 16, 18)
    pdf.add_page()
    pdf.set_font(face, "B", 14)
    pdf.set_text_color(18, 32, 42)
    pdf.cell(0, 8, _pdf_text(headline, face), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    if note:
        pdf.set_font(face, "I", 10)
        pdf.set_text_color(70, 85, 95)
        pdf.multi_cell(0, 5, _pdf_text(note, face))
        pdf.ln(2)
    if not sections:
        pdf.set_font(face, "", 12)
        pdf.set_text_color(90, 100, 110)
        pdf.cell(0, 8, "(none)", new_x="LMARGIN", new_y="NEXT")
    amt_w = 24.0
    mkt_w = 28.0
    name_w = pdf.epw - amt_w - mkt_w
    for section in sections:
        pdf.set_x(pdf.l_margin)
        pdf.set_font(face, "B", 11)
        pdf.set_text_color(31, 59, 77)
        pdf.cell(0, 8, _pdf_text(section.label, face), new_x="LMARGIN", new_y="NEXT")
        pdf.set_draw_color(31, 59, 77)
        pdf.set_line_width(0.4)
        y = pdf.get_y()
        pdf.line(pdf.l_margin, y, pdf.l_margin + pdf.epw, y)
        pdf.ln(2)
        pdf.set_text_color(18, 32, 42)
        for row in section.rows:
            pdf.set_x(pdf.l_margin)
            pdf.set_font(face, "", 13)
            label = row.name
            if row.extra:
                label = f"{row.name}  {row.extra}"
            pdf.cell(name_w, 8, _pdf_text(label, face), align="L")
            pdf.set_font(face, "B", 13)
            pdf.cell(mkt_w, 8, _pdf_text(row.market, face), align="R")
            pdf.cell(amt_w, 8, _pdf_text(row.amount, face), align="R", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(4)
    if tape:
        pdf.set_x(pdf.l_margin)
        pdf.set_font(face, "B", 11)
        pdf.set_text_color(31, 59, 77)
        pdf.cell(0, 8, "FILL TAPE  (display; not a sell)", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font(face, "", 9)
        pdf.set_text_color(18, 32, 42)
        for line in tape:
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(0, 4.2, _pdf_text(line, face))
        pdf.ln(2)
    pdf.set_font(face, "I", 8)
    pdf.set_text_color(90, 100, 110)
    pdf.cell(0, 6, "This snapshot only. Mock. Never auto-bet.", new_x="LMARGIN", new_y="NEXT")
    pdf.output(str(path))
    return path
