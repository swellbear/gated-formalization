"""Disagreement sheet across compare paths. Display only. Never auto-bets."""

from __future__ import annotations

import html
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from golf_offshoot.compare.law import METHOD_LAW_V1, law_hash
from golf_offshoot.compare.paths import COMPARE_LEDGERS, ComparePath, compare_allows_place, compare_markets_blurb, ledger_id
from golf_offshoot.config import MIN_EDGE_TO_CONSIDER
from golf_offshoot.data_feeds.http import package_data_dir
from golf_offshoot.models.enums import Horizon
from golf_offshoot.strategy.paper_book import PaperBookFile, load_paper_file, posted_price_edge

def _path_winner_only(path_id: str, event_id: str = "") -> bool:
    law = PATH_LAW.get(path_id) or {}
    if path_id == "lived":
        return False
    if compare_allows_place(event_id):
        return False
    return bool(law.get("winner_only", True))

PATH_LAW: dict[str, dict[str, str | bool]] = {
    "lived": {
        "label": "Lived museum",
        "winner_only": False,
        "screen": "both",
        "ranking": "current pipeline (A theta)",
    },
    "a_replay": {
        "label": "A-replay",
        "winner_only": True,
        "screen": "edgew",
        "ranking": "same theta as lived",
    },
    "b_guts": {
        "label": "B-guts",
        "winner_only": True,
        "screen": "edgew",
        "ranking": "honest theta",
    },
    "b_nerves": {
        "label": "B-nerves",
        "winner_only": True,
        "screen": "posted",
        "ranking": "A's theta",
    },
    "b_full": {
        "label": "B-full",
        "winner_only": True,
        "screen": "posted",
        "ranking": "honest theta",
    },
}


_T = MIN_EDGE_TO_CONSIDER
_PLACE = {"top_5", "top_10", "top_20", "make_cut"}


@dataclass
class HeldTicket:
    path_id: str
    player_id: str
    player_name: str
    bet_type: str
    stake: float
    entry_edge: float
    entry_model_p: float
    decimal_odds: float


@dataclass
class PathMove:
    path_id: str
    player_name: str
    kind: str
    reason_plain: str
    reason_technical: str
    edge_w: float | None
    posted_edge: float | None


@dataclass
class PathBookView:
    path_id: str
    n: int
    names: list[str]
    exposure: float
    bankroll: float
    notes: list[str] = field(default_factory=list)
    holdings: list[HeldTicket] = field(default_factory=list)
    movements: list[PathMove] = field(default_factory=list)


@dataclass
class FightEvent:
    as_of: str
    run_id: str
    player_name: str
    owned_by: list[str]
    missing_from: list[str]
    note: str = ""
    plain: str = ""
    technical: str = ""


def _bet_key(value) -> str:
    return str(getattr(value, "value", value) or "win").lower()


def _pp(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value * 100:+.1f}pp"


def _clears(screen: str, edge_w: float | None, posted_edge: float | None) -> bool | None:
    if screen == "edgew":
        return None if edge_w is None else edge_w >= _T
    if screen == "posted":
        return None if posted_edge is None else posted_edge >= _T
    if edge_w is None or posted_edge is None:
        return None
    return edge_w >= _T and posted_edge >= _T


def book_view(record: PaperBookFile | None, path_id: str) -> PathBookView:
    if record is None:
        return PathBookView(path_id=path_id, n=0, names=[], exposure=0.0, bankroll=0.0)
    names: list[str] = []
    seen: set[str] = set()
    holdings: list[HeldTicket] = []
    for p in record.book.positions:
        holdings.append(
            HeldTicket(
                path_id=path_id,
                player_id=p.player_id,
                player_name=p.player_name,
                bet_type=_bet_key(p.bet_type),
                stake=float(p.stake),
                entry_edge=float(p.entry_edge),
                entry_model_p=float(p.entry_model_p),
                decimal_odds=float(p.decimal_odds),
            )
        )
        if p.player_name in seen:
            continue
        seen.add(p.player_name)
        names.append(p.player_name)
    moves: list[PathMove] = []
    for m in record.movements:
        if m.status and m.status != "applied":
            continue
        if m.kind not in {"exit", "reduce", "new_bet", "add"}:
            continue
        moves.append(
            PathMove(
                path_id=path_id,
                player_name=m.player_name,
                kind=m.kind,
                reason_plain=m.reason_plain or "",
                reason_technical=m.reason_technical or "",
                edge_w=m.edge_w,
                posted_edge=m.posted_edge,
            )
        )
    return PathBookView(
        path_id=path_id,
        n=len(names),
        names=names,
        exposure=float(record.book.open_exposure),
        bankroll=float(record.bankroll),
        notes=list(record.notes[-4:]),
        holdings=holdings,
        movements=moves,
    )


def fights_at(
    views: dict[str, PathBookView],
    *,
    as_of: str = "",
    run_id: str = "",
    live_outputs=None,
    event_id: str = "",
) -> list[FightEvent]:
    all_names: set[str] = set()
    owned: dict[str, set[str]] = {}
    for pid, view in views.items():
        owned[pid] = set(view.names)
        all_names.update(view.names)
    events: list[FightEvent] = []
    path_ids = list(views)
    for name in sorted(all_names):
        have = [p for p in path_ids if name in owned[p]]
        miss = [p for p in path_ids if name not in owned[p]]
        if have and miss:
            plain, technical = explain_disagreement(
                name, have, miss, views, live_outputs=live_outputs, event_id=event_id
            )
            events.append(
                FightEvent(
                    as_of=as_of,
                    run_id=run_id,
                    player_name=name,
                    owned_by=have,
                    missing_from=miss,
                    note=plain,
                    plain=plain,
                    technical=technical,
                )
            )
    return events


def explain_disagreement(
    name: str,
    have: list[str],
    miss: list[str],
    views: dict[str, PathBookView],
    *,
    live_outputs=None,
    event_id: str = "",
) -> tuple[str, str]:
    holdings = [
        h
        for pid in have
        for h in views[pid].holdings
        if h.player_name == name
    ]
    markets = sorted({h.bet_type for h in holdings})
    win_hold = [h for h in holdings if h.bet_type == "win"]
    place_only = bool(markets) and not win_hold and all(m in _PLACE for m in markets)
    edge_w, posted_edge, model_p, decimal, source = _win_metrics(
        name, holdings, views, live_outputs
    )
    plain: list[str] = []
    tech: list[str] = []

    if place_only:
        labels = ", ".join(_label(p) for p in miss)
        mk = ", ".join(m.replace("_", " ") for m in markets)
        miss_winner_only = [p for p in miss if _path_winner_only(p, event_id)]
        if miss_winner_only and len(miss_winner_only) == len(miss):
            plain.append(
                f"{_label(have[0]) if len(have) == 1 else 'The holding book'} has {mk} "
                f"tickets. {labels} "
                f"{'is' if len(miss) == 1 else 'are'} Winner-only and cannot copy place ladders."
            )
            tech.append(
                f"holdings={markets}; missing={miss} allowed_bet_types=[win] "
                f"winner_only=true"
            )
        else:
            plain.append(
                f"{_label(have[0]) if len(have) == 1 else 'The holding book'} has {mk} "
                f"tickets. {labels} did not take this place market "
                "(no real coupon, screen failed, or cap). Place is never built from Winner odds."
            )
            tech.append(
                f"holdings={markets}; missing={miss} winner_only=false "
                f"place_when_coupon={compare_allows_place(event_id)}"
            )
        return " ".join(plain), "; ".join(tech)

    for pid in have:
        law = PATH_LAW.get(pid, {})
        hs = [h for h in views[pid].holdings if h.player_name == name]
        mk = ", ".join(h.bet_type.replace("_", " ") for h in hs) or "tickets"
        screen = str(law.get("screen") or "both")
        ranking = str(law.get("ranking") or pid)
        if hs and hs[0].bet_type == "win":
            h = hs[0]
            pe = posted_price_edge(h.entry_model_p, h.decimal_odds)
            if screen == "posted":
                plain.append(
                    f"{_label(pid)} holds Winner because vs-posted clears 3pp "
                    f"({_pp(pe)}) on {ranking}."
                )
            elif screen == "edgew":
                plain.append(
                    f"{_label(pid)} holds Winner because EdgeW clears 3pp "
                    f"({_pp(h.entry_edge)}) on {ranking}."
                )
            else:
                plain.append(
                    f"{_label(pid)} holds {mk} (EdgeW {_pp(h.entry_edge)}, "
                    f"vs-posted {_pp(pe)}; place ladders allowed)."
                )
            tech.append(
                f"{pid}: in screen={screen} ranking={ranking} bet={h.bet_type} "
                f"stake={h.stake:.2f} EdgeW={h.entry_edge:+.3f} vs_posted={pe:+.3f} "
                f"model_p={h.entry_model_p:.3f} decimal={h.decimal_odds:.2f}"
            )
        else:
            plain.append(f"{_label(pid)} holds {mk}.")
            tech.append(f"{pid}: in bets={[h.bet_type for h in hs]}")

    for pid in miss:
        law = PATH_LAW.get(pid, {})
        screen = str(law.get("screen") or "both")
        ranking = str(law.get("ranking") or pid)
        label = _label(pid)
        if _path_winner_only(pid, event_id) and place_only:
            continue
        exit_m = _latest_exit(views.get(pid), name)
        ok = _clears(screen, edge_w, posted_edge)
        if ok is False:
            if screen == "edgew":
                plain.append(
                    f"{label} is out because EdgeW is {_pp(edge_w)}, below the 3pp bar, "
                    f"on {ranking}."
                )
            elif screen == "posted":
                plain.append(
                    f"{label} is out because vs-posted is {_pp(posted_edge)}, below the 3pp bar "
                    f"(the posted price you would actually buy), on {ranking}. "
                    f"EdgeW {_pp(edge_w)} is not this book's ticket bar."
                )
            else:
                plain.append(
                    f"{label} is out because it needs EdgeW AND vs-posted at 3pp "
                    f"(EdgeW {_pp(edge_w)}, vs-posted {_pp(posted_edge)})."
                )
            tech.append(
                f"{pid}: out screen={screen} ranking={ranking} t={_T:.2f} "
                f"EdgeW={_num(edge_w)} vs_posted={_num(posted_edge)} "
                f"model_p={_num(model_p)} decimal={decimal if decimal is None else f'{decimal:.2f}'} "
                f"source={source} clears=false"
            )
        elif exit_m is not None:
            why = exit_m.reason_plain or exit_m.kind
            plain.append(f"{label} applied {exit_m.kind} on this name: {why}")
            tech.append(
                f"{pid}: out kind={exit_m.kind} EdgeW={_num(exit_m.edge_w)} "
                f"vs_posted={_num(exit_m.posted_edge)} {exit_m.reason_technical}".strip()
            )
        else:
            plain.append(
                f"{label} does not hold Winner ({ranking}; screen={screen})."
            )
            tech.append(
                f"{pid}: out screen={screen} ranking={ranking} "
                f"EdgeW={_num(edge_w)} vs_posted={_num(posted_edge)} source={source or 'n/a'}"
            )

    honest_in = [p for p in have if str(PATH_LAW.get(p, {}).get("ranking", "")).startswith("honest")]
    if honest_in and "a_replay" in miss and "b_nerves" not in have and not place_only:
        plain.append(
            "Honest-theta books and A-theta books can split on the same name "
            "because they do not share one ranking."
        )
        tech.append("ranking_split=honest_theta vs A_theta")

    return " ".join(plain), "; ".join(tech)


def _label(path_id: str) -> str:
    law = PATH_LAW.get(path_id)
    if law:
        return str(law["label"])
    return path_id


def _num(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:+.3f}" if abs(value) < 10 else f"{value:.3f}"


def _win_metrics(name, holdings, views, live_outputs):
    by_id = {}
    by_name = {}
    for row in live_outputs or []:
        by_id[row.player_id] = row
        by_name[row.name] = row
    pid = next((h.player_id for h in holdings if h.player_id), "")
    row = by_id.get(pid) or by_name.get(name)
    if row is not None:
        posted = row.posted_odds_by_bet.get("win")
        try:
            posted_f = float(posted) if posted is not None else None
        except (TypeError, ValueError):
            posted_f = None
        hp = row.probabilities.horizons.get(Horizon.WIN)
        model = hp.central if hp is not None else None
        edge = row.edge_by_bet.get("win")
        pe = None
        if model is not None and posted_f is not None and posted_f > 1.0:
            pe = posted_price_edge(model, posted_f)
        return (
            float(edge) if edge is not None else None,
            pe,
            model,
            posted_f,
            "live snapshot",
        )
    win_h = next((h for h in holdings if h.bet_type == "win"), None)
    if win_h is not None:
        return (
            win_h.entry_edge,
            posted_price_edge(win_h.entry_model_p, win_h.decimal_odds),
            win_h.entry_model_p,
            win_h.decimal_odds,
            f"entry on {win_h.path_id}",
        )
    for view in views.values():
        move = _latest_exit(view, name)
        if move is not None and (move.edge_w is not None or move.posted_edge is not None):
            return move.edge_w, move.posted_edge, None, None, f"{move.kind} on {view.path_id}"
    return None, None, None, None, ""


def _latest_exit(view: PathBookView | None, name: str) -> PathMove | None:
    if view is None:
        return None
    for m in reversed(view.movements):
        if m.player_name == name and m.kind in {"exit", "reduce"}:
            return m
    return None


def load_path_views(event_id: str, paths: tuple[ComparePath, ...] | None = None) -> dict[str, PathBookView]:
    out: dict[str, PathBookView] = {}
    for path in paths or COMPARE_LEDGERS:
        pid = ledger_id(path)
        rec = load_paper_file(event_id, path_id=pid)
        out[pid] = book_view(rec, pid)
    lived = load_paper_file(event_id, path_id="lived")
    out["lived"] = book_view(lived, "lived")
    return out


def fights_document(
    event_id: str,
    *,
    event_name: str = "",
    views: dict[str, PathBookView] | None = None,
    events: list[FightEvent] | None = None,
    extra_notes: list[str] | None = None,
    live_outputs=None,
) -> str:
    views = views if views is not None else load_path_views(event_id)
    events = events or fights_at(views, live_outputs=live_outputs, event_id=event_id)
    markets = compare_markets_blurb(event_id)
    lines = [
        f"FIGHTS  {event_name or event_id}",
        f"event={event_id}",
        f"method_law={METHOD_LAW_V1['id']} hash={law_hash()}",
        f"as_of={datetime.now(timezone.utc).isoformat()}",
        "never_auto_bet=true  paper/mock only",
        "",
        "== what these books are ==",
        "  lived      Museum book. Current pipeline. EdgeW AND vs-posted. Place ladders allowed. Not re-locked.",
        f"  a_replay   A-replay / A-control (one book). Same ranking as lived. {markets}. EdgeW screen. Independent $250.",
        f"  b_guts     Honest theta. {markets}. EdgeW screen. Independent $250.",
        f"  b_nerves   A's ranking. {markets}. vs-posted (1/odds). Independent $250.",
        f"  b_full     Honest theta. {markets}. vs-posted (1/odds). Independent $250.",
        "  t=0.03     Ticket bar this week. EdgeW = model minus fair implied. vs-posted = model minus 1/decimal.",
        "",
        "== books (who is held right now) ==",
    ]
    for pid, view in views.items():
        names = ", ".join(view.names) if view.names else "(empty)"
        lines.append(
            f"  {pid:12} n={view.n:2d}  ${view.exposure:.2f} / ${view.bankroll:.0f}  {names}"
        )
    lines += ["", "== disagreements =="]
    if not events:
        lines.append("  none this snapshot")
    for ev in events:
        lines.append(
            f"  {ev.player_name}: in [{', '.join(ev.owned_by)}]  out [{', '.join(ev.missing_from)}]"
        )
        if ev.plain:
            lines.append(f"      plain: {ev.plain}")
        if ev.technical:
            lines.append(f"      technical: {ev.technical}")
        if ev.run_id:
            lines.append(f"      run={ev.run_id} as_of={ev.as_of}")
    lines += ["", "== notes =="]
    lines.append("  B never tickets on EdgeW alone. Posted bar is 1/decimal.")
    lines.append("  t stays 0.03 this week (n=1). Learner may not copy A because A won.")
    lines.append("  Lived paper is a museum. Compare ledgers are independent $250 books.")
    lines.append(f"  A/B markets: {compare_markets_blurb(event_id)}.")
    lines.append("  Winner posted P/L and place posted P/L are scored separately.")
    from golf_offshoot.compare.scores import scoreboard_lines

    for line in scoreboard_lines(event_id):
        lines.append(f"  {line}")
    for n in extra_notes or []:
        lines.append(f"  {n}")
    return "\n".join(lines) + "\n"


def fights_html(text: str, *, title: str) -> str:
    body = html.escape(text)
    return (
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        f"<title>{html.escape(title)}</title>"
        "<style>body{font-family:ui-monospace,Consolas,monospace;white-space:pre-wrap;"
        "margin:24px;max-width:1100px} h1{font-size:18px}</style></head><body>"
        f"<h1>{html.escape(title)}</h1>\n{body}</body></html>\n"
    )


def write_fights(
    event_id: str,
    *,
    event_name: str = "",
    views: dict[str, PathBookView] | None = None,
    events: list[FightEvent] | None = None,
    extra_notes: list[str] | None = None,
    directory: Path | None = None,
    live_outputs=None,
) -> Path:
    d = directory or (package_data_dir() / "exports")
    d.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    safe = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in str(event_id))
    stem = f"{safe}_fights_{stamp}"
    text = fights_document(
        event_id,
        event_name=event_name,
        views=views,
        events=events,
        extra_notes=extra_notes,
        live_outputs=live_outputs,
    )
    txt = d / f"{stem}.txt"
    html_path = d / f"{stem}.html"
    txt.write_text(text, encoding="utf-8")
    html_path.write_text(
        fights_html(
            text,
            title=f"Fights — who each book holds, and why — {event_name or event_id}",
        ),
        encoding="utf-8",
    )
    pdf = d / f"{stem}.pdf"
    write_fights_pdf(
        pdf,
        text,
        title=f"Fights — who each book holds, and why — {event_name or event_id}",
    )
    return html_path


def write_fights_pdf(path: Path, text: str, *, title: str) -> Path:
    from fpdf import FPDF

    from golf_offshoot.ranking.export_table import _pdf_text, _register_pdf_font, _require_fpdf2

    _require_fpdf2()

    class Report(FPDF):
        def header(self) -> None:
            face = getattr(self, "_table_font", "Helvetica")
            self.set_x(self.l_margin)
            self.set_text_color(18, 32, 42)
            self.set_font(face, "B", 12)
            self.cell(0, 7, _pdf_text(title, face), new_x="LMARGIN", new_y="NEXT")
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
                "fights  |  paper / mock  |  observation only  |  never auto-bet  |  "
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
    pdf.set_text_color(18, 32, 42)
    pdf.multi_cell(0, 4.2, _pdf_text(text, face))
    pdf.output(str(path))
    return path
