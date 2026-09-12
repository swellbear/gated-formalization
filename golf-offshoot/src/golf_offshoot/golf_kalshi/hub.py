"""8765 golf observation board. Numbers, not a briefing."""

from __future__ import annotations

import html
import json
from typing import Any

from golf_offshoot.golf_kalshi.adapter import load_last_good_catalog
from golf_offshoot.golf_kalshi.catalog_view import group_catalog
from golf_offshoot.golf_kalshi.paper import (
    closed_tickets,
    halt_remaining_text,
    load_ledger,
    open_tickets,
    sizing_bank,
)
from golf_offshoot.golf_kalshi.paths import (
    board_png_path,
    last_tick_path,
    unmatched_path,
    watch_kill_path,
    watch_status_path,
)
from golf_offshoot.golf_kalshi.recipe import recipe_public, recipe_v1
from golf_offshoot.golf_kalshi.sleeves import classify_sleeve
from golf_offshoot.golf_kalshi.watch import load_watch_status
from golf_offshoot.localtime import format_eastern


def _read(path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return payload if isinstance(payload, dict) else {}


def golf_watch_label(watch: dict[str, Any], *, halt: bool = False, killed: bool = False) -> str:
    """on / off / stale / halt / killed from the sidecar file. Stale only while running."""
    if killed:
        return "killed"
    if halt:
        return "halt"
    running = bool(watch.get("running"))
    at = str(watch.get("at") or "")
    stale = False
    if running:
        if not at:
            stale = True
        else:
            try:
                from datetime import datetime

                from golf_offshoot.golf_kalshi.watch import DEFAULT_INTERVAL_S
                from golf_offshoot.localtime import now, to_eastern

                text = at[:-1] + "+00:00" if at.endswith("Z") else at
                stamped = to_eastern(datetime.fromisoformat(text))
                interval = float(watch.get("interval_s") or DEFAULT_INTERVAL_S)
                stale = (now() - stamped).total_seconds() > max(interval, 1.0) * 3
            except ValueError:
                stale = True
    if stale:
        return "stale"
    return "on" if running else "off"


def collect_board() -> dict[str, Any]:
    watch = load_watch_status()
    tick = _read(last_tick_path())
    unmatched = _read(unmatched_path())
    led = load_ledger()
    catalog = load_last_good_catalog()
    png = board_png_path()
    closed = closed_tickets(led)
    halt = bool(led.get("halted") or tick.get("halted"))
    remaining = halt_remaining_text(str(led.get("halt_until") or "")) if halt else ""
    watch_label = golf_watch_label(
        watch, halt=halt, killed=watch_kill_path().is_file()
    )
    bankroll = led.get("bankroll")
    rec = recipe_v1()
    bank = sizing_bank(led, rec)
    return {
        "watch": watch_label,
        "watch_age": format_eastern(watch.get("at") or tick.get("at")),
        "cycles": watch.get("cycles") or 0,
        "halt_reason": led.get("halt_reason") or "",
        "halt_until": led.get("halt_until") or "",
        "halt_remaining": remaining,
        "bankroll": bankroll,
        "pnl": led.get("betting_pnl"),
        "fees_paid": led.get("fees_paid"),
        "sleeves": led.get("sleeves") or {},
        "cap_fast": rec.sleeve_target("fast", bank),
        "cap_week": rec.sleeve_target("week", bank),
        "cap_slow": rec.sleeve_target("slow", bank),
        "tickets": open_tickets(led),
        "closed": closed,
        "halt_log": led.get("halt_log") or [],
        "catalog": catalog.get("markets") or [],
        "series": catalog.get("series") or [],
        "unmatched": unmatched.get("rows") or [],
        "recipe": recipe_public(),
        "png": png.is_file(),
        "png_name": board_png_path().name if png.is_file() else "",
        "last_tick": tick,
        "booked_tickers": {str(t.get("ticker") or "") for t in led.get("tickets") or []},
    }


def _chip(label: str, value: str, extra: str = "") -> str:
    css = "gk-chip" + (f" {html.escape(extra)}" if extra else "")
    return f'<span class="{css}"><b>{html.escape(label)}</b> {html.escape(str(value))}</span>'


def _pnl_class(value: str) -> str:
    raw = str(value or "").strip()
    if raw in {"", "—"}:
        return ""
    try:
        amount = float(raw)
    except ValueError:
        return ""
    if amount > 0:
        return "pnl-up"
    if amount < 0:
        return "pnl-down"
    return ""


def _bar(used: float, cap: float) -> str:
    pct = 0 if cap <= 0 else max(0, min(100, int(100 * used / cap)))
    return (
        f'<div class="gk-bar" title="{used:.2f} / {cap:.2f}">'
        f'<span style="width:{pct}%"></span></div>'
    )


def _table(headers: list[str], rows: list[list[str]], *, empty: str = "—") -> str:
    head = "".join(f"<th>{html.escape(h)}</th>" for h in headers)
    body = []
    for row in rows:
        tds = "".join(f"<td>{html.escape(str(c))}</td>" for c in row)
        body.append(f"<tr>{tds}</tr>")
    if not rows:
        body.append(f'<tr><td colspan="{len(headers)}">{html.escape(empty)}</td></tr>')
    return f'<div class="gk-table-wrap"><table class="gk-board"><thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'


def _hunt_copy(tick: dict[str, Any]) -> str:
    hunts = tick.get("field_hunt") if isinstance(tick.get("field_hunt"), list) else []
    bound = int(tick.get("hunt_bound") or 0)
    deferred = int(tick.get("brain_deferred") or 0)
    head = (
        f"Field hunt: bound {bound} · brain {tick.get('brain_runs') or 0}"
        f" · deferred {deferred}."
    )
    if not hunts:
        return (
            f'<p class="gk-nums">{html.escape(head)} Catalog is still the shelf. '
            "Open a series to load market rows.</p>"
        )
    bits = []
    for row in hunts[:12]:
        fam = str(row.get("family") or row.get("event_key") or "")
        src = str(row.get("field_source") or "miss")
        thin = " thin" if row.get("thin") else ""
        flag = " deferred" if row.get("deferred") or row.get("budget") else ""
        cached = " cached" if row.get("cached") else ""
        scored_bit = " scored" if row.get("scored") else ""
        bits.append(f"{fam} {src}{thin}{flag}{cached}{scored_bit}".strip())
    extra = f" · +{len(hunts) - 12} more" if len(hunts) > 12 else ""
    return (
        f'<p class="gk-nums">{html.escape(head)} '
        f"{html.escape(' · '.join(bits))}{html.escape(extra)}</p>"
    )


def _skip_bits(tick: dict[str, Any], *, max_reasons: int | None = None) -> str:
    reasons = tick.get("skip_reasons") if isinstance(tick.get("skip_reasons"), dict) else {}
    bits = [
        f"{key} {int(val)}"
        for key, val in sorted(reasons.items(), key=lambda kv: (-int(kv[1] or 0), str(kv[0])))
        if key
    ]
    if not bits:
        return ""
    shown = bits if max_reasons is None else bits[:max_reasons]
    extra = " · …" if max_reasons is not None and len(bits) > max_reasons else ""
    return (
        f"fills={tick.get('fills') or 0} skips={tick.get('skips') or 0} "
        f"({' · '.join(shown)}{extra})"
    )


def _ticket_skip_copy(tick: dict[str, Any], n_open: int) -> str:
    skip = _skip_bits(tick)
    summary = str(tick.get("summary") or "")
    if skip:
        detail = f"Last tick {skip}."
    elif summary:
        detail = f"Last tick {summary}."
    else:
        detail = "No finished golf tick with skip counts yet."
    open_bit = " Open tickets on Home are the book, not a skip." if n_open else ""
    return (
        f'<p class="gk-nums">{html.escape(detail)}{html.escape(open_bit)} '
        "Catalog Open markets are not paper tickets. Skip when the brain cannot see is recorded, not a fill.</p>"
    )


def _mix_copy(tick: dict[str, Any]) -> str:
    worthy = int(tick.get("worthy") or 0)
    picked = tick.get("picked") if isinstance(tick.get("picked"), dict) else {}
    line = (
        f"worthy {worthy} · picked {int(picked.get('fast') or 0)}/"
        f"{int(picked.get('week') or 0)}/{int(picked.get('slow') or 0)} · "
        f"exits {int(tick.get('exits') or 0)} · realloc {int(tick.get('realloc') or 0)} · "
        f"adds {int(tick.get('adds') or 0)}"
    )
    if tick.get("week_overweight"):
        line += " · week overweight catch-up"
    skip = _skip_bits(tick, max_reasons=4)
    if skip:
        line += f" · {skip}"
    return f'<p class="gk-nums">{html.escape(line)}</p>'


THIN_YES_ASK = 0.02


def _ask_float(ask: Any) -> float | None:
    if ask is None or ask == "":
        return None
    try:
        return float(ask)
    except (TypeError, ValueError):
        return None


def _dollar_edge(value: Any) -> str:
    if value is None:
        return "—"
    try:
        return f"{float(value):+.2f}"
    except (TypeError, ValueError):
        return "—"


def _edge_cell(*, ask: Any, live: Any, entry: Any) -> str:
    """Dollar EV after fee, not a 3pp fraction. Tiny winner quotes stay in Quote."""
    ask_f = _ask_float(ask)
    if ask_f is not None and ask_f < THIN_YES_ASK:
        return "thin"
    if live is None and entry is None:
        return ""
    return f"{_dollar_edge(live)} / {_dollar_edge(entry)}"


def _open_rows(b: dict[str, Any]) -> list[list[str]]:
    tick = b.get("last_tick") or {}
    tick_marks = tick.get("marks") if isinstance(tick.get("marks"), dict) else {}
    open_rows = []
    for t in b["tickets"]:
        q = t.get("quote") or {}
        mark = tick_marks.get(str(t.get("ticker") or "")) or {}
        live = mark.get("live_edge")
        entry = mark.get("entry_edge") if mark.get("entry_edge") is not None else t.get("edge_after_fee")
        ask = q.get("yes_ask")
        if ask is None:
            ask = t.get("yes_ask")
        open_rows.append(
            [
                t.get("player") or "",
                t.get("title") or t.get("ticker") or "",
                t.get("sleeve") or "",
                f"{float(t.get('stake') or 0):.2f}",
                "" if ask is None else ask,
                _edge_cell(ask=ask, live=live, entry=entry),
                t.get("status") or "",
            ]
        )
    return open_rows


def _money(value: Any, default: float = 0.0) -> float:
    if value is None or value == "":
        return float(default)
    return float(value)


def _closed_result(ticket: dict[str, Any]) -> str:
    status = str(ticket.get("status") or "")
    if status == "paper_win":
        return "win"
    if status == "paper_lose":
        return "lose"
    if status == "void":
        return "void"
    if status == "paper_exit":
        return str(ticket.get("exit_reason") or "exit").replace("_", " ")
    return status or "—"


def session_html(b: dict[str, Any] | None = None) -> str:
    b = b or collect_board()
    rec = b["recipe"]
    bank = _money(b.get("bankroll"), float(rec.get("seed") or 0))
    sleeves = b.get("sleeves") or {}
    cap_fast = _money(b.get("cap_fast"), float(rec.get("cap_fast") or 0))
    cap_week = _money(b.get("cap_week"), float(rec.get("cap_week") or 0))
    cap_slow = _money(b.get("cap_slow"), float(rec.get("cap_slow") or 0))
    n_open = len(b.get("tickets") or [])
    n_closed = len(b.get("closed") or [])
    pnl_s = f"{_money(b.get('pnl')):+.2f}"
    halt_bits = []
    if b.get("halt_reason"):
        halt_bits.append(str(b.get("halt_reason")))
    if b.get("halt_remaining"):
        halt_bits.append(str(b.get("halt_remaining")))
    halt_val = ("yes " + " ".join(halt_bits)).strip() if b["watch"] == "halt" else "no"
    if b["watch"] in {"halt", "stale"}:
        watch_cls = "desk-watch-halt"
    elif b["watch"] == "on":
        watch_cls = "desk-watch-on"
    else:
        watch_cls = "desk-watch-off"
    mix = _mix_copy(b.get("last_tick") or {})
    return (
        '<div id="desk-session" class="desk-session">'
        f'<span class="desk-chip {watch_cls}"><b>Watch</b> {html.escape(str(b["watch"]))}</span>'
        + _chip("Clock", str(b.get("watch_age") or "—"))
        + _chip("Bankroll", f"{bank:.2f}")
        + _chip("P/L", pnl_s, _pnl_class(pnl_s))
        + _chip("Fees", f"{_money(b.get('fees_paid')):.2f}")
        + _chip("Paper tickets", str(n_open))
        + _chip("Closed", str(n_closed))
        + _chip("Halt", halt_val)
        + '<div class="gk-sleeves desk-meters">'
        f'<div><span>Fast {cap_fast:.0f}</span>{_bar(float(sleeves.get("fast") or 0), cap_fast or 1)}</div>'
        f'<div><span>This week {cap_week:.0f}</span>{_bar(float(sleeves.get("week") or 0), cap_week or 1)}</div>'
        f'<div><span>Slow {cap_slow:.0f}</span>{_bar(float(sleeves.get("slow") or 0), cap_slow or 1)}</div>'
        "</div>"
        + mix
        + "</div>"
    )


def blotter_html(b: dict[str, Any] | None = None) -> str:
    b = b or collect_board()
    rows = _open_rows(b)
    empty = "no open tickets"
    table = _table(
        ["Player", "Market", "Sleeve", "Stake", "Quote", "Live/entry $", "Status"],
        rows,
        empty=empty,
    )
    return (
        '<div id="desk-blotter" class="desk-blotter" data-golf-kalshi="1">'
        '<section class="panel gk book-golf" id="golf-kalshi" data-book="golf">'
        "<h2>Open tickets</h2>"
        + table
        + "</section></div>"
    )


def cockpit_html(b: dict[str, Any] | None = None) -> str:
    b = b or collect_board()
    tick = b.get("last_tick") or {}
    n_open = len(b.get("tickets") or [])
    return (
        '<section class="panel desk-cockpit">'
        "<h2>Thinking</h2>"
        + _hunt_copy(tick)
        + _ticket_skip_copy(tick, n_open)
        + "</section>"
    )


def _recipe_cap_copy(rec: dict[str, Any]) -> str:
    """Ops only. Live fill gate is event dollars, not ticket count. Does not size."""
    try:
        pct = f"{float(rec.get('event_cap_frac')) * 100:.0f}"
    except (TypeError, ValueError):
        pct = "—"
    tickets = rec.get("max_tickets_per_event")
    ticket_bit = str(int(tickets)) if tickets is not None else "—"
    return (
        f"New fills: event dollars at {pct}% of bank (one-name). "
        f"{ticket_bit}-ticket trim was one-time on v1. mix_event_cap is that dollar gate."
    )


def ops_html(b: dict[str, Any] | None = None) -> str:
    b = b or collect_board()
    rec = b["recipe"]
    booked = b.get("booked_tickers") or set()
    tree = group_catalog(list(b.get("series") or []), list(b.get("catalog") or []), booked, include_markets=False)
    n_unmatched = len(b["unmatched"])
    return (
        '<section class="panel gk-ops book-golf" data-book="golf">'
        "<h3>Catalog</h3>"
        + _catalog_html(tree, booked)
        + _unmatched_html(n_unmatched)
        + "<h3>Recipe</h3>"
        f'<p class="gk-nums">{html.escape(str(rec.get("recipe")))} · {html.escape(str(rec.get("declared_at")))} · brain {html.escape(str(rec.get("player_brain")))}</p>'
        f'<p class="help">{html.escape(_recipe_cap_copy(rec))}</p>'
        + "</section>"
    )


def scoreboard_html(b: dict[str, Any] | None = None) -> str:
    b = b or collect_board()
    closed = list(b.get("closed") or [])
    wins = sum(1 for t in closed if t.get("status") == "paper_win")
    losses = sum(1 for t in closed if t.get("status") == "paper_lose")
    exits = sum(1 for t in closed if t.get("status") == "paper_exit")
    voids = sum(1 for t in closed if t.get("status") == "void")
    closed_pnl = sum(float(t.get("pnl_after_fee") or 0) for t in closed)
    body = []
    for t in closed:
        pnl = float(t.get("pnl_after_fee") or 0)
        cls = "pnl-up" if pnl > 0 else "pnl-down" if pnl < 0 else ""
        when = t.get("exited_at") or t.get("settled_at") or t.get("decision_at") or ""
        tds = [
            format_eastern(when) if when else "—",
            t.get("player") or "",
            t.get("title") or t.get("ticker") or "",
            t.get("sleeve") or "",
            f"{float(t.get('stake') or 0):.2f}",
            _closed_result(t),
        ]
        cells = "".join(f"<td>{html.escape(str(c))}</td>" for c in tds)
        pnl_td = f'<td class="{cls}">{pnl:+.2f}</td>'
        body.append(f"<tr>{cells}{pnl_td}</tr>")
    if not body:
        body.append('<tr><td colspan="7">no closed tickets</td></tr>')
    head = "".join(
        f"<th>{html.escape(h)}</th>"
        for h in ("When", "Player", "Market", "Sleeve", "Stake", "Result", "P/L")
    )
    tally = (
        f"win {wins} · lose {losses} · exit {exits}"
        + (f" · void {voids}" if voids else "")
        + f" · closed P/L {closed_pnl:+.2f}"
    )
    chart = ""
    if b.get("png"):
        chart = (
            '<figure class="gk-chart">'
            f'<img src="/viz-golf/{html.escape(str(b["png_name"]))}?t=1" alt="Golf Kalshi" width="1200"/>'
            "</figure>"
        )
    else:
        chart = '<div class="gk-chart-slot" aria-hidden="true"></div>'
    halt_rows = []
    for row in list(b.get("halt_log") or [])[-8:][::-1]:
        pause = row.get("seconds")
        pause_s = f"{int(pause)}s" if pause else str(row.get("mode") or "")
        halt_rows.append(
            [
                format_eastern(row.get("at")),
                row.get("reason") or "",
                f"{float(row.get('bankroll') or 0):.2f}",
                pause_s,
                format_eastern(row.get("until")) if row.get("until") else str(row.get("until") or ""),
            ]
        )
    halt_bit = ""
    if halt_rows:
        halt_bit = (
            '<section class="panel gk-halts book-golf" data-book="golf">'
            "<h2>Halts</h2>"
            '<p class="gk-nums">Paper pause is two minutes then the gym continues. Live uses the next UTC day.</p>'
            + _table(["When", "Reason", "Bankroll", "Pause", "Until"], halt_rows)
            + "</section>"
        )
    return (
        chart
        + '<section class="panel gk-closed book-golf" id="golf-closed" data-book="golf">'
        "<h2>Closed tickets</h2>"
        f'<p class="gk-nums">{html.escape(tally)}</p>'
        '<div class="gk-table-wrap"><table class="gk-board gk-closed">'
        f"<thead><tr>{head}</tr></thead><tbody>{''.join(body)}</tbody></table></div>"
        "</section>"
        + halt_bit
    )


def board_html() -> str:
    b = collect_board()
    return (
        session_html(b)
        + blotter_html(b)
        + cockpit_html(b)
        + ops_html(b)
        + scoreboard_html(b)
    )


def _px(value: Any) -> str:
    if value is None or value == "":
        return ""
    return str(value)


def _market_rows(markets: list[dict[str, Any]], booked: set[str]) -> list[list[str]]:
    rows = []
    for market in markets:
        ticker = str(market.get("ticker") or "")
        if ticker in booked:
            mark = "in the book"
        elif market.get("in_play"):
            mark = "in-play"
        else:
            mark = "watching"
        rows.append(
            [
                str(market.get("yes_sub_title") or market.get("title") or ""),
                ticker,
                classify_sleeve(market),
                _px(market.get("yes_ask")),
                _px(market.get("yes_bid")),
                _px(market.get("spread")),
                str(market.get("status") or ""),
                mark,
            ]
        )
    return rows


def _catalog_html(tree: dict[str, Any], booked: set[str]) -> str:
    chips = (
        '<div class="gk-chips">'
        + _chip("Series", str(tree.get("series_n") or 0))
        + _chip("Open markets", str(tree.get("open_n") or 0))
        + _chip("Settled", str(tree.get("settled_n") or 0))
        + _chip("In-play families", str(tree.get("in_play") or 0))
        + _chip("Booked series", str(tree.get("in_book") or 0))
        + "</div>"
        + '<p class="gk-nums">Tour family → series counts. Market rows load when you open a series. Unmatched is collapsed. Open markets are the catalog, not paper tickets.</p>'
    )
    blocks = []
    for fam in tree.get("families") or []:
        series_bits = [_series_html(row, booked, lazy=True) for row in fam.get("series") or []]
        summary = (
            f"{html.escape(str(fam.get('name') or ''))} · "
            f"{int(fam.get('series_n') or 0)} series · "
            f"{int(fam.get('open_n') or 0)} open · "
            f"{int(fam.get('settled_n') or 0)} settled"
        )
        if fam.get("in_play"):
            summary += " · in-play"
        if fam.get("in_book"):
            summary += " · in the book"
        blocks.append(
            f'<details class="gk-family"><summary>{summary}</summary>'
            + "".join(series_bits)
            + "</details>"
        )
    if not blocks:
        blocks.append('<p class="gk-nums">No golf series on the last catalog.</p>')
    return chips + '<div class="gk-catalog">' + "".join(blocks) + "</div>"


def _series_summary(row: dict[str, Any]) -> str:
    fee = row.get("fee_multiplier")
    fee_bit = f" · fee k={html.escape(str(fee))}" if fee is not None else ""
    sleeves = f" · {html.escape(str(row.get('sleeves') or ''))}" if row.get("sleeves") else ""
    live = " · in-play" if row.get("in_play") else ""
    book = " · in the book" if row.get("in_book") else ""
    preview = row.get("names_preview") or []
    names = f" · {html.escape(', '.join(str(n) for n in preview))}" if preview else ""
    return (
        f"{html.escape(str(row.get('series_ticker') or ''))} · "
        f"{html.escape(str(row.get('title') or ''))} · "
        f"{int(row.get('open_n') or 0)} open · {int(row.get('settled_n') or 0)} settled"
        f"{sleeves}{fee_bit}{live}{book}{names}"
    )


def _series_markets_html(row: dict[str, Any], booked: set[str]) -> str:
    headers = ["Name", "Ticker", "Sleeve", "Ask", "Bid", "Spread", "Status", "Mark"]
    open_tbl = _table(headers, _market_rows(list(row.get("open") or []), booked))
    settled_n = int(row.get("settled_n") or 0)
    settled_bit = ""
    if settled_n:
        settled_tbl = _table(headers, _market_rows(list(row.get("settled") or []), booked))
        settled_bit = (
            f'<details class="gk-settled"><summary>Settled {settled_n}</summary>{settled_tbl}</details>'
        )
    return open_tbl + settled_bit


def _series_html(row: dict[str, Any], booked: set[str], *, lazy: bool = False) -> str:
    summary = _series_summary(row)
    ticker = html.escape(str(row.get("series_ticker") or ""))
    if lazy:
        return (
            f'<details class="gk-series" data-series="{ticker}" data-loaded="0">'
            f"<summary>{summary}</summary>"
            '<div class="gk-series-body"></div>'
            "</details>"
        )
    return (
        f'<details class="gk-series"><summary>{summary}</summary>'
        + _series_markets_html(row, booked)
        + "</details>"
    )


def series_fragment_html(series_ticker: str) -> str | None:
    """One series' market rows. Golf last-good catalog only. Not 15m."""
    from golf_offshoot.golf_kalshi.adapter import is_crypto_or_15m_series

    ticker = str(series_ticker or "").strip()
    if not ticker or "/" in ticker or ".." in ticker or is_crypto_or_15m_series(ticker):
        return None
    catalog = load_last_good_catalog()
    series = [s for s in (catalog.get("series") or []) if str(s.get("series_ticker") or "") == ticker]
    markets = [m for m in (catalog.get("markets") or []) if str(m.get("series_ticker") or "") == ticker]
    if not series and not markets:
        return None
    booked = {str(t.get("ticker") or "") for t in load_ledger().get("tickets") or []}
    tree = group_catalog(
        series or [{"series_ticker": ticker, "title": ticker, "tags": ["Golf"]}],
        markets,
        booked,
        include_markets=True,
    )
    families = tree.get("families") or []
    rows = (families[0].get("series") or []) if families else []
    if not rows:
        return None
    return _series_markets_html(rows[0], booked)


def _unmatched_html(n: int) -> str:
    return (
        f'<details class="gk-unmatched" data-loaded="0">'
        f"<summary>Unmatched · {int(n)} names · not a fill</summary>"
        '<div class="gk-unmatched-body"></div>'
        "</details>"
    )


def unmatched_fragment_html() -> str:
    """Quarantine rows. Not paper tickets. Loaded when Unmatched is opened."""
    rows = [
        [r.get("player") or "", r.get("ticker") or "", r.get("reason") or ""]
        for r in (_read(unmatched_path()).get("rows") or [])
        if isinstance(r, dict)
    ]
    return _table(
        ["Name", "Ticker", "Reason"],
        rows,
        empty="None. Last tick had no unmatched names.",
    )
