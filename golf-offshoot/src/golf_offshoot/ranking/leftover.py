"""Leftover callout after live / ingest strategy. Display only. Do not stuff into theta."""

from __future__ import annotations

from pathlib import Path

from golf_offshoot.decision.layer import min_edge_for_bet
from golf_offshoot.models.enums import (
    BetType,
    CourseType,
    Horizon,
    RunMode,
    SourceKind,
    ROUND_LEADER_BETS,
    horizon_for,
)
from golf_offshoot.models.schemas import Course, SourceInventoryItem, Tournament, TournamentRunResult
from golf_offshoot.ranking.leaderboard import format_to_par


def format_leftover_callout(result: TournamentRunResult, open_book=None) -> str:
    """ASCII leftover block. No new feeds. Not a GPF residual menu."""
    inv = _inventory(result)
    by_name = {i.field_name: i for i in inv}
    used = _used_lines(result, by_name)
    unconstrained = _unconstrained_lines(by_name)
    held = _held_lines(result, open_book)
    lines = [
        "LEFTOVER CALLOUT  (display only; not GPF gates)",
        f"event={result.tournament.name}  mode={result.mode.value}  never_auto_bet=true",
        "",
        "== already used ==",
        *used,
        "",
        "== still unconstrained ==",
        *unconstrained,
        "",
        "== on held tickets ==",
        *held,
    ]
    lines.extend(
        ["", "== round-leader leftover (display; not a ticket) ==", *_round_leader_leftover_lines(result)]
    )
    from golf_offshoot.strategy.tape import climb_leftover_lines, fill_tape_lines

    lines.extend(
        [
            "",
            "== fill tape (display; not a sell) ==",
            *fill_tape_lines(
                open_book,
                ranked=result.ranked,
                moves=getattr(open_book, "latest_advice", None),
            ),
        ]
    )
    lines.extend(
        [
            "",
            "== fat Top 10 / skinny Win (display; not a ticket) ==",
            *climb_leftover_lines(result),
        ]
    )
    from golf_offshoot.strategy.flip import leftover_flip_heat_lines

    lines.extend(
        [
            "",
            "== flip heat (display; NEW if P>=0.20) ==",
            *leftover_flip_heat_lines(result.ranked),
        ]
    )
    lines.extend(
        [
            "",
            "== do not stuff into theta ==",
            "  Overrides stay documented (HumanOverride + audit) or they do not happen.",
            "  Do not add a live delta-theta CLI from this block.",
            "  Agronomy, tee pairing, narrative, and injury rumor stay leftover, not theta.",
            "",
            "== operator ==",
            *_operator_notes(polymarket=_is_polymarket(result, open_book)),
        ]
    )
    return "\n".join(lines)


def _inventory(result: TournamentRunResult) -> list[SourceInventoryItem]:
    raw = result.audit.extra.get("source_inventory") or []
    out: list[SourceInventoryItem] = []
    for item in raw:
        if isinstance(item, SourceInventoryItem):
            out.append(item)
        elif isinstance(item, dict):
            out.append(SourceInventoryItem.model_validate(item))
    return out


def _present(item: SourceInventoryItem | None) -> bool:
    if item is None:
        return False
    if item.source_kind == SourceKind.UNAVAILABLE:
        return False
    cov = (item.coverage or "").strip()
    if cov in {"0", "0/0"} or cov.startswith("0/0"):
        return False
    return True


def _used_lines(result: TournamentRunResult, by_name: dict[str, SourceInventoryItem]) -> list[str]:
    lines: list[str] = []
    field = by_name.get("player_identification_field")
    if _present(field):
        src = field.source_name or "espn_field"
        cov = field.coverage or "field"
        if src == "espn_field":
            lines.append(f"  ESPN field - {src} ({cov})")
        else:
            lines.append(f"  provisional field - {src} ({cov})")
    if result.mode == RunMode.LIVE:
        n_live = sum(1 for r in result.ranked if r.live_holes_completed or r.live_place is not None)
        if n_live:
            lines.append(
                "  ESPN live board - place / to-par / holes completed "
                f"({n_live} players with a board mark)"
            )
    recent = by_name.get("strokes_gained_recent_window")
    cats = by_name.get("strokes_gained_categories")
    if _present(recent):
        lines.append(
            f"  as-of SG - {recent.source_name or 'pga_tour_sg'} "
            f"({recent.coverage or 'present'})"
        )
    elif _present(cats):
        lines.append(
            f"  as-of SG - not a last-N window; long-term SG present "
            f"({cats.coverage})"
        )
    odds = by_name.get("market_odds")
    if _present(odds):
        src = odds.source_name or "odds"
        lines.append(f"  posted odds - {src} ({odds.coverage or 'quotes exist'})")
        cov = result.audit.extra.get("market_coverage") or {}
        avail = cov.get("available_markets") or []
        if src == "polymarket":
            notes = odds.notes or ""
            slugs = ""
            if "us_slugs=" in notes:
                slugs = notes.split("us_slugs=", 1)[1].split(";", 1)[0].strip()
            elif "gamma_slugs=" in notes:
                slugs = notes.split("gamma_slugs=", 1)[1].split(";", 1)[0].strip()
            if slugs:
                lines.append(f"  polymarket US slugs - {slugs}")
            if avail:
                lines.append(
                    "  polymarket US model markets - "
                    + ", ".join(avail)
                    + " (gateway.polymarket.us golf futures; not Gamma international Top 5/10/20)"
                )
            over = result.audit.extra.get("overround") or {}
            if over:
                bits = []
                for key in (
                    "win",
                    "top_5",
                    "top_10",
                    "top_20",
                    "win_after_r1",
                    "win_after_r2",
                    "win_after_r3",
                ):
                    if key in over:
                        bits.append(f"{key} {float(over[key]):.2f}")
                if bits:
                    lines.append(
                        "  polymarket Yes-ask sum - "
                        + ", ".join(bits)
                        + " (Win~1, lead-after-N~1; place cards are not on the US golf app)"
                    )
    return lines or ["  (nothing admitted this run)"]


def _unconstrained_lines(by_name: dict[str, SourceInventoryItem]) -> list[str]:
    agro = by_name.get("course_setup_agronomy")
    health = by_name.get("health_injury")
    sg = by_name.get("strokes_gained_categories")
    agro_note = (agro.notes or agro.impact_if_missing) if agro else "tightness/rough/stimp not evidence"
    health_note = (health.notes or health.impact_if_missing) if health else "no injury wire; WD status only"
    unmatched = _unmatched_note(sg)
    return [
        f"  agronomy - {agro_note}",
        "  tee/wave - live tee pairing unseeded; not in theta",
        f"  injury - {health_note} (ESPN WD is status, not a rumor feed)",
        "  narrative - forced to 0; not used",
        f"  unmatched SG - {unmatched}",
    ]


def _unmatched_note(sg: SourceInventoryItem | None) -> str:
    if sg is None:
        return "none listed this run"
    notes = sg.notes or ""
    low = notes.lower()
    if "unmatched" not in low:
        return sg.impact_if_missing or "none listed this run"
    idx = low.find("unmatched")
    return notes[idx:].strip() or "unmatched names stay unconstrained"


def _held_lines(result: TournamentRunResult, open_book) -> list[str]:
    positions = _open_positions(open_book)
    if result.mode != RunMode.LIVE or not positions:
        return ["  (none held)"]
    by_id = {r.player_id: r for r in result.ranked}
    by_name = {r.name: r for r in result.ranked}
    seen: set[str] = set()
    lines: list[str] = []
    for pos in positions:
        pid = getattr(pos, "player_id", "") or ""
        pname = getattr(pos, "player_name", "") or ""
        key = pid or pname
        if not key or key in seen:
            continue
        seen.add(key)
        row = by_id.get(pid) or by_name.get(pname)
        name = pname or (row.name if row else pid or "n/a")
        if row is None:
            lines.append(f"  {name} - no live row; residual, not extra theta")
            continue
        wp = row.probabilities.p(Horizon.WIN).central
        to_par = format_to_par(row.live_score_to_par)
        holes = int(row.live_holes_completed or 0)
        lines.append(f"  {name}  Win={wp:.3f}  to-par={to_par}  holes={holes}")
    if lines:
        lines.append(
            "  Win% is banked to-par plus remaining holes from current theta. "
            "A hot round / looking good is the operator's residual, not extra theta."
        )
    return lines or ["  (none held)"]


_RL_LABEL = {
    BetType.WIN_AFTER_R1: "R1 leader",
    BetType.WIN_AFTER_R2: "R2 leader",
    BetType.WIN_AFTER_R3: "R3 leader",
}


def _round_leader_leftover_lines(result: TournamentRunResult) -> list[str]:
    """Top vs-posted names per US end-of-round card. Display only. Not a ticket."""
    lines: list[str] = []
    any_quote = False
    for bet in ROUND_LEADER_BETS:
        ranked: list[tuple[float, str, float, float, float]] = []
        for row in result.ranked:
            raw = row.posted_odds_by_bet.get(bet.value)
            try:
                posted = float(raw) if raw is not None else None
            except (TypeError, ValueError):
                posted = None
            if posted is None or posted <= 1.0:
                continue
            any_quote = True
            h = horizon_for(bet)
            hp = row.probabilities.horizons.get(h) if h is not None else None
            if hp is None:
                continue
            posted_p = 1.0 / posted
            vs = hp.central - posted_p
            bar = min_edge_for_bet(bet, posted_p)
            ranked.append((vs, row.name, hp.central, posted_p, bar))
        if not ranked:
            continue
        ranked.sort(key=lambda t: t[0], reverse=True)
        label = _RL_LABEL.get(bet, bet.value)
        lines.append(
            f"  {label} — still must beat the Yes ask; bar is max(floor, min(3pp, scale × posted Yes))"
        )
        for vs, name, model, posted_p, bar in ranked[:5]:
            tag = "clears bar" if vs >= bar else "short of bar"
            lines.append(
                f"    {name}  model={model:.3f}  Yes={posted_p:.3f}  "
                f"vs-posted={vs * 100:+.1f}pp  bar={bar * 100:.1f}pp  {tag}"
            )
    if not any_quote or not lines:
        return [
            "  No R1/R2/R3 Yes quotes on this snapshot. Display leftover, not a ticket.",
            "  Rerun live when the US golf app lists Round 1/2/3 Yes. Tee/wave stays leftover, not theta.",
            "  Do not treat 18-hole lead as 72-hole Win.",
        ]
    lines.append(
        "  Display leftover. A fair ~1.04 Yes book can still print no NEW tickets. "
        "Do not treat 18-hole lead as 72-hole Win."
    )
    return lines


def _operator_notes(*, polymarket: bool) -> list[str]:
    lines = [
        "  After golf starts, rerun live when the ESPN board moves. Round 2/3 then use live to-par.",
        "  Tee/wave, agronomy, and injury rumor stay leftover, not theta.",
    ]
    if polymarket:
        lines[0:0] = [
            "  Observation stubs are tracking, not fills. After you buy Yes, paper-fill shares and price.",
            "  Fill tape (cost vs bid vs keep-to-win) is the journal. Offer vs cost is not a sell.",
            "  Flip sleeve: leftover P first on listed Yes (Win / R1 / R2 / R3 / place if quoted); "
            "NEW if P>=0.20; one flip per player; cap 6 open flips (no live refill); "
            "sell at fill+20% if still green next live.",
        ]
        lines.append(
            "  Polymarket cash: paper-deposit --book polymarket. That is not ledger.json. No CLOB orders."
        )
    return lines


def _is_polymarket(result: TournamentRunResult, open_book) -> bool:
    if open_book is not None and (getattr(open_book, "path_id", None) or "") == "polymarket":
        return True
    odds = result.audit.extra.get("market_coverage") or {}
    src = str(odds.get("source") or odds.get("book") or "").lower()
    return "polymarket" in src


def leftover_from_snapshot(
    record,
    run_id: str = "",
) -> str:
    """Pack leftover from a persisted snapshot. Missing snapshot stays honest, not invented."""
    from golf_offshoot.strategy.paper_book import load_snapshot_audit
    from golf_offshoot.strategy.tape import fill_tape_lines

    run = (run_id or getattr(record, "locked_from_run_id", None) or "").strip()
    audit = load_snapshot_audit(run) if run else None
    if audit is None:
        event = getattr(record, "tournament_name", None) or getattr(record, "tournament_id", None) or "n/a"
        lines = [
            "LEFTOVER CALLOUT  (display only; not GPF gates)",
            f"event={event}  never_auto_bet=true",
            "",
            "== already used ==",
            "  (no snapshot in this pack; rerun live to refresh leftover)",
            "",
            "== still unconstrained ==",
            "  agronomy - tightness/rough/stimp not evidence",
            "  tee/wave - live tee pairing unseeded; not in theta",
            "  injury - no injury wire; WD status only",
            "  narrative - forced to 0; not used",
            "",
            "== on held tickets ==",
            "  (see paper tickets; snapshot n/a)",
            "",
            "== round-leader leftover (display; not a ticket) ==",
            "  No snapshot in this pack; R1/R2/R3 leftover is not a ticket.",
            "  Rerun live when the ESPN board moves. Tee/wave stays leftover, not theta.",
            "",
            "== fill tape (display; not a sell) ==",
            *fill_tape_lines(record, moves=getattr(record, "latest_advice", None)),
            "",
            "== fat Top 10 / skinny Win (display; not a ticket) ==",
            "  No snapshot; climb leftover is display only, not a ticket.",
            "",
            "== flip heat (display; NEW if P>=0.20) ==",
            "  No snapshot; flip heat leftover is display only, not a ticket.",
            "  NEW only if P >= 0.20 on a listed Yes. Flip sells at fill+20%, not keep-to-win.",
            "",
            "== do not stuff into theta ==",
            "  Agronomy, tee pairing, narrative, and injury rumor stay leftover, not theta.",
            "",
            "== operator ==",
            *_operator_notes(polymarket=(getattr(record, "path_id", None) or "") == "polymarket"),
        ]
        return "\n".join(lines)
    result = _result_from_audit(audit, getattr(record, "tournament_name", "") or "")
    return format_leftover_callout(result, record)


def _result_from_audit(audit, event_name: str) -> TournamentRunResult:
    course = Course(course_id="n/a", name="n/a", course_type=CourseType.PARKLAND)
    tournament = Tournament(
        tournament_id=audit.tournament_id,
        name=event_name or audit.tournament_id,
        course=course,
        start_date="",
    )
    return TournamentRunResult(
        run_id=audit.run_id,
        tournament=tournament,
        mode=audit.mode,
        ranked=list(audit.outputs),
        audit=audit,
    )


def write_leftover_files(
    directory: Path,
    text: str,
    *,
    title: str = "Leftover (display; not a ticket)",
) -> None:
    """Pack leftover page. Display only. Not a ticket. Not theta."""
    from golf_offshoot.ranking.export_table import (
        _pdf_text,
        _register_pdf_font,
        _require_fpdf2,
        mark_pdf_printed,
        printed_at_utc,
        write_pdf_footer,
        write_pdf_print_stamp,
    )

    directory.mkdir(parents=True, exist_ok=True)
    body = text.rstrip() + "\n"
    (directory / "04_leftover.txt").write_text(body, encoding="utf-8")
    html = (
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        f"<title>{title}</title>"
        "<style>body{font-family:ui-monospace,Consolas,monospace;white-space:pre-wrap;"
        "margin:24px;max-width:1100px} h1{font-size:18px}</style></head><body>"
        f"<h1>{title}</h1>\n<pre>{_html_escape(body)}</pre></body></html>\n"
    )
    (directory / "04_leftover.html").write_text(html, encoding="utf-8")
    from fpdf import FPDF

    _require_fpdf2()

    class Report(FPDF):
        def header(self) -> None:
            face = getattr(self, "_table_font", "Helvetica")
            self.set_x(self.l_margin)
            write_pdf_print_stamp(self, face)
            if self.page_no() == 1:
                self.set_font(face, "B", 14)
                self.set_text_color(18, 32, 42)
                self.cell(0, 8, _pdf_text(title, face), new_x="LMARGIN", new_y="NEXT")
                self.set_font(face, "", 8)
                self.set_text_color(70, 85, 95)
                self.cell(0, 4, _pdf_text(printed_at_utc(), face), new_x="LMARGIN", new_y="NEXT")
                self.ln(2)

        def footer(self) -> None:
            face = getattr(self, "_table_font", "Helvetica")
            write_pdf_footer(self, face, "leftover display")

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
    pdf.set_font(face, size=8)
    pdf.set_text_color(18, 32, 42)
    pdf.multi_cell(0, 4.0, _pdf_text(body, face))
    pdf.output(str(directory / "04_leftover.pdf"))


def _html_escape(text: str) -> str:
    import html

    return html.escape(text)


def _open_positions(open_book) -> list:
    if open_book is None:
        return []
    inner = getattr(open_book, "book", None)
    raw = getattr(inner, "positions", None) if inner is not None else getattr(open_book, "positions", None)
    out = []
    for pos in raw or []:
        if getattr(pos, "proposed", False):
            continue
        if float(getattr(pos, "stake", 0) or 0) <= 0:
            continue
        out.append(pos)
    return out
