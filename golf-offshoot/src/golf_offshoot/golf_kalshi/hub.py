"""8765 golf observation board. Numbers, not a briefing. Hard NOs live in the hub footer."""

from __future__ import annotations

import html
import json
from typing import Any

from golf_offshoot.golf_kalshi.adapter import load_last_good_catalog
from golf_offshoot.golf_kalshi.catalog_view import group_catalog
from golf_offshoot.golf_kalshi.paper import load_ledger, open_tickets
from golf_offshoot.golf_kalshi.paths import (
    board_png_path,
    last_tick_path,
    unmatched_path,
    watch_kill_path,
    watch_status_path,
)
from golf_offshoot.golf_kalshi.recipe import recipe_public
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


def collect_board() -> dict[str, Any]:
    watch = load_watch_status()
    tick = _read(last_tick_path())
    catalog = load_last_good_catalog()
    unmatched = _read(unmatched_path())
    led = load_ledger()
    png = board_png_path()
    halt = bool(led.get("halted") or tick.get("halted"))
    if watch_kill_path().is_file():
        watch_label = "killed"
    elif halt:
        watch_label = "halt"
    elif watch.get("running"):
        watch_label = "on"
    else:
        watch_label = "off"
    return {
        "watch": watch_label,
        "watch_age": format_eastern(watch.get("at") or tick.get("at")),
        "cycles": watch.get("cycles") or 0,
        "halt_reason": led.get("halt_reason") or "",
        "bankroll": led.get("bankroll"),
        "pnl": led.get("betting_pnl"),
        "fees_paid": led.get("fees_paid"),
        "sleeves": led.get("sleeves") or {},
        "tickets": open_tickets(led),
        "catalog": catalog.get("markets") or [],
        "series": catalog.get("series") or [],
        "unmatched": unmatched.get("rows") or [],
        "recipe": recipe_public(),
        "png": png.is_file(),
        "png_name": board_png_path().name if png.is_file() else "",
        "last_tick": tick,
        "booked_tickers": {str(t.get("ticker") or "") for t in led.get("tickets") or []},
    }


def _chip(label: str, value: str) -> str:
    return f'<span class="gk-chip"><b>{html.escape(label)}</b> {html.escape(str(value))}</span>'


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


def _ticket_skip_copy(tick: dict[str, Any], n_open: int) -> str:
    if n_open:
        return (
            '<p class="gk-nums">Paper fills from decide_golf. Catalog Open markets are Kalshi contracts, not this table.</p>'
        )
    reasons = tick.get("skip_reasons") if isinstance(tick.get("skip_reasons"), dict) else {}
    bits = [
        f"{key} {int(val)}"
        for key, val in sorted(reasons.items(), key=lambda kv: (-int(kv[1] or 0), str(kv[0])))
        if key
    ]
    summary = str(tick.get("summary") or "")
    if bits:
        detail = f"Last tick fills={tick.get('fills') or 0} skips={tick.get('skips') or 0} ({' · '.join(bits)})."
    elif summary:
        detail = f"Last tick {summary}."
    else:
        detail = "No finished golf tick with skip counts yet."
    return (
        f'<p class="gk-nums">{html.escape(detail)} '
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
    return f'<p class="gk-nums">{html.escape(line)}</p>'


def board_html() -> str:
    b = collect_board()
    rec = b["recipe"]
    bank = float(b.get("bankroll") or rec.get("seed") or 0)
    sleeves = b.get("sleeves") or {}
    booked = b.get("booked_tickers") or set()
    tick = b.get("last_tick") or {}
    tick_marks = tick.get("marks") if isinstance(tick.get("marks"), dict) else {}
    open_rows = []
    for t in b["tickets"]:
        q = t.get("quote") or {}
        mark = tick_marks.get(str(t.get("ticker") or "")) or {}
        live = mark.get("live_edge")
        entry = mark.get("entry_edge") if mark.get("entry_edge") is not None else t.get("edge_after_fee")
        edge_bit = ""
        if live is not None or entry is not None:
            live_s = f"{float(live):+.3f}" if live is not None else "—"
            entry_s = f"{float(entry):+.3f}" if entry is not None else "—"
            edge_bit = f"{live_s} / {entry_s}"
        open_rows.append(
            [
                t.get("player") or "",
                t.get("title") or t.get("ticker") or "",
                t.get("sleeve") or "",
                f"{float(t.get('stake') or 0):.2f}",
                f"{q.get('yes_ask') if q.get('yes_ask') is not None else ''}",
                edge_bit,
                t.get("status") or "",
            ]
        )
    tree = group_catalog(list(b.get("series") or []), list(b.get("catalog") or []), booked, include_markets=False)
    n_unmatched = len(b["unmatched"])
    png = ""
    if b.get("png"):
        png = (
            '<figure class="gk-chart">'
            f'<img src="/viz-golf/{html.escape(str(b["png_name"]))}?t=1" alt="Golf Kalshi" width="1200"/>'
            "</figure>"
        )
    else:
        png = '<div class="gk-chart-slot" aria-hidden="true"></div>'
    halt = f" {html.escape(str(b.get('halt_reason') or ''))}" if b.get("halt_reason") else ""
    return (
        '<section class="panel gk" id="golf-kalshi">'
        "<h2>Golf (Kalshi)</h2>"
        '<div class="gk-chips">'
        + _chip("Watch", f"{b['watch']} · {b['watch_age']}")
        + _chip("Bankroll", f"{bank:.2f}")
        + _chip("P/L", f"{float(b.get('pnl') or 0):+.2f}")
        + _chip("Fees", f"{float(b.get('fees_paid') or 0):.2f}")
        + _chip("Paper tickets", str(len(open_rows)))
        + _chip("Halt", "yes" + halt if b["watch"] == "halt" else "no")
        + "</div>"
        + _hunt_copy(tick)
        + _mix_copy(tick)
        + "<h3>Sleeves</h3>"
        '<div class="gk-sleeves">'
        f'<div><span>Fast {float(rec.get("cap_fast") or 0):.0f}</span>{_bar(float(sleeves.get("fast") or 0), float(rec.get("cap_fast") or 1))}</div>'
        f'<div><span>This week {float(rec.get("cap_week") or 0):.0f}</span>{_bar(float(sleeves.get("week") or 0), float(rec.get("cap_week") or 1))}</div>'
        f'<div><span>Slow {float(rec.get("cap_slow") or 0):.0f}</span>{_bar(float(sleeves.get("slow") or 0), float(rec.get("cap_slow") or 1))}</div>'
        "</div>"
        "<h3>Open tickets</h3>"
        + _ticket_skip_copy(tick, len(open_rows))
        + _table(
            ["Player", "Market", "Sleeve", "Stake", "Quote", "Live/entry edge", "Status"],
            open_rows,
            empty="None. Paper ledger has no fills.",
        )
        + "<h3>Catalog</h3>"
        + _catalog_html(tree, booked)
        + _unmatched_html(n_unmatched)
        + "<h3>Recipe</h3>"
        f'<p class="gk-nums">{html.escape(str(rec.get("recipe")))} · {html.escape(str(rec.get("declared_at")))} · brain {html.escape(str(rec.get("player_brain")))}</p>'
        + png
        + "</section>"
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
