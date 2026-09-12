"""Local Phase 1 operator shell. Stdlib HTTP + text dump. No new dependencies."""

from __future__ import annotations

import argparse
import html
import json
import os
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from golf_offshoot.learning_lane_15m.paths import LANE_15M, LANE_GOLF, PRIMARY_SERIES
from golf_offshoot.learning_lane_15m.watch import PaperWatch, load_watch_status
from golf_offshoot.operator_surface.artifacts import HonestyBundle, load_honesty
from golf_offshoot.operator_surface.hub_browser import refresh_existing_hub_window
from golf_offshoot.operator_surface.lanes import SELECTOR_FIELD, lane_header_name, parse_lane, desk_lane_from_query
from golf_offshoot.operator_surface.desk import DESK_CSS, DESK_JS, render_miss, watch_payload
from golf_offshoot.operator_surface.modes import (
    AI_NO_CASH,
    CASH_BADGE,
    NOT_ARMED,
    PAPER_ONLY,
    build_mode_walls,
)
from golf_offshoot.operator_surface.client_write import write_http_body
from golf_offshoot.operator_surface.notify import notify_run_complete
from golf_offshoot.operator_surface.paths import resolve_roots, safe_existing_file
from golf_offshoot.operator_surface.reload import (
    DEFAULT_DEBOUNCE_S,
    DEFAULT_POLL_S,
    REEXEC_CODE,
    HubWatcher,
    collect_snapshot,
    hub_child_command,
    is_hub_child,
    supervise_hub_child,
)
from golf_offshoot.operator_surface.runner import (
    OperatorSafetyError,
    RunRecord,
    format_run_record,
    refuse_forbidden,
    run_15m_ingest,
    run_15m_live,
    run_15m_loop,
    run_15m_shadow,
    run_golf_kalshi_tick,
    run_ingest,
    run_live,
    run_loop,
    run_shadow,
)
from golf_offshoot.operator_surface.viz import (
    SLOT_CALIBRATION,
    SLOT_SHADOW,
    SLOT_WC1_DATED_RECORD,
    VizWall,
    load_viz_wall,
    viz_file_for_serve,
)

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765

#: Plain-English one-liner per viz slot. The honest sublines in ``viz.py`` are the
#: display contract; these only translate them for a non-engineer reader.
SLOT_PLAIN_HELP = {
    SLOT_SHADOW: (
        "What the paper journal has been advising, and how honest those calls look so far. "
        "Not money and not settled results."
    ),
    SLOT_CALIBRATION: (
        "Whether re-fitted weights ever beat the hand-set expert weights. "
        "Every freeze so far says keep the expert weights."
    ),
    SLOT_WC1_DATED_RECORD: (
        "The dated record of the last weekly claim. It did not clear, so it is parked unproven "
        "and nothing was proved."
    ),
}

#: The one place the standing Hard NOs are stated as UI chrome. Enforcement lives in
#: ``modes``/``runner``; the page says it once, quietly, instead of on every card.
HARD_NO_STRIP = (
    f"Trading {NOT_ARMED} · {PAPER_ONLY} · {AI_NO_CASH} — {CASH_BADGE} · "
    "no Kalshi account, key, or wallet scope · do not add honer bankrolls to Lineage A"
)

#: (POST action value, button label, one-line help). POST values stay unchanged.
ACTION_BUTTONS = (
    ("ingest", "Pull latest data", "Pre-tournament run: fetch the field and build the ranked table."),
    ("live", "Update live ranks", "Live run on current scores and posted prices. Observation, not a bet."),
    ("shadow", "Check paper journal", "Re-read the paper (shadow) journal. Nothing is placed."),
    ("loop", "Do all three", "Pull data, then update live, then re-read the paper journal. One alert at the end."),
    ("refresh", "Reload files", "Re-read charts and saved files from disk. No run is started."),
)


def build_surface(
    *,
    event_id: str | None = None,
    artifact_root: Path | None = None,
    viz_root: Path | None = None,
    shadow_path: Path | None = None,
    environ: dict[str, str] | None = None,
    last_run: RunRecord | None = None,
    lane: str | None = None,
) -> dict:
    honesty = load_honesty(
        artifact_root=artifact_root,
        viz_root=viz_root,
        shadow_path=shadow_path,
        environ=environ,
        event_id=event_id,
    )
    live_data = honesty.ranked.status == "LIVE_TABLE_OK"
    walls = build_mode_walls(mock=False, live_data=live_data)
    if honesty.ranked.barred_mock or honesty.shadow.barred_mock:
        walls = build_mode_walls(mock=True)
    viz = load_viz_wall(honesty.roots)
    return {
        "walls": walls,
        "honesty": honesty,
        "viz": viz,
        "event_id": event_id or "",
        "last_run": last_run,
        "lane": parse_lane(lane),
    }


def render_text(surface: dict) -> str:
    walls = surface["walls"]
    honesty: HonestyBundle = surface["honesty"]
    viz: VizWall = surface["viz"]
    last: RunRecord | None = surface.get("last_run")
    lines = [
        walls.render_text(),
        "",
        f"lane={surface.get('lane') or LANE_GOLF}",
        f"event_id={surface.get('event_id') or '(none pinned)'}",
        f"artifact_root={honesty.roots.artifact_root} ({honesty.roots.artifact_source})",
        f"viz_root={honesty.roots.viz_root} ({honesty.roots.viz_source})",
        f"shadow_path={honesty.roots.shadow_path} ({honesty.roots.shadow_source})",
        "",
        "-- ranked LIVE table --",
        honesty.ranked.banner,
        honesty.ranked.text,
        "",
        "-- leftover (display only) --",
        honesty.leftover.text,
        "",
        "-- source inventory --",
        honesty.inventory.text,
        "",
        "-- shadow honesty --",
        honesty.shadow.text,
        "",
        "-- calibration --",
        honesty.calibration.text,
        "",
        "-- illustrator viz-wall (read-only) --",
    ]
    for slot in viz.slots:
        lines.append(f"{slot.title}: {slot.status}")
        lines.append(f"  {slot.subline}")
        lines.append("  " + " · ".join(slot.badges))
        if slot.path:
            lines.append(f"  file={slot.path} mtime={slot.mtime}")
        else:
            lines.append(f"  {slot.note}")
    if viz.manifest_error:
        lines.append(f"manifest error: {viz.manifest_error}")
    if last is not None:
        lines.extend(["", "-- last operator run --", format_run_record(last)])
        if last.paper:
            lines.extend(["", "-- paper observation (not trading) --", last.paper])
    return "\n".join(lines)


def _viz_wall_html(viz: VizWall) -> str:
    """Read-only chart wall. Missing slots stay 'not yet available'. Never invented."""
    cards = []
    for slot in viz.slots:
        if slot.path is not None:
            cache = int(slot.mtime or 0)
            src = f"/viz/{html.escape(slot.slot_id)}.png?t={cache}"
            title = html.escape(slot.title)
            # Plain link to the PNG, so the chart still enlarges when the overlay script
            # is unavailable. The overlay intercepts the click when it is available.
            body = (
                f'<a class="zoom" href="{src}" data-viz-zoom="1" data-viz-title="{title}" '
                f'aria-label="Enlarge {title}">'
                f'<img src="{src}" alt="{title}" width="1200"/>'
                f'<span class="zoom-hint">Click to enlarge</span>'
                f"</a>"
            )
        else:
            body = f'<p class="missing">{html.escape(slot.note)}</p>'
        plain = SLOT_PLAIN_HELP.get(slot.slot_id)
        plain_html = f'<p class="plain">{html.escape(plain)}</p>' if plain else ""
        cards.append(
            f'<section class="viz" id="viz-slot-{html.escape(slot.slot_id)}">'
            f"<h3>{html.escape(slot.title)}</h3>"
            f"{plain_html}"
            f'<p class="sub">{html.escape(slot.subline)}</p>'
            f"{body}</section>"
        )
    trailer = ""
    if viz.manifest_error:
        trailer = (
            f'<p class="missing">Chart list rejected: {html.escape(viz.manifest_error)}. '
            "No chart was invented in its place.</p>"
        )
    return f'<div class="viz-wall" id="viz-wall">{"".join(cards)}</div>{trailer}'


#: Overlay hints. The charts are tall dashboards, so fit-on-screen is only an
#: overview; full size is what actually makes the small print readable.
ZOOM_HINT_FIT = "Click the chart for full size · Esc or click outside to close"
ZOOM_HINT_FULL = "Click the chart to fit it on screen · Esc or click outside to close"


def _viz_lightbox_html(viz: VizWall) -> str:
    """Enlarged-chart overlay for the golf viz wall."""
    return _lightbox_html(any(slot.path is not None for slot in viz.slots))


def _lightbox_html(has_chart: bool) -> str:
    """Enlarged-chart overlay. Omitted entirely when no chart exists to enlarge."""
    if not has_chart:
        return ""
    return (
        '<div class="lightbox" id="viz-lightbox" hidden role="dialog" aria-modal="true" '
        'aria-label="Enlarged chart">'
        '<div class="lightbox-bar">'
        '<span class="lightbox-title" id="viz-lightbox-title"></span>'
        f'<span class="lightbox-hint" id="viz-lightbox-hint">{html.escape(ZOOM_HINT_FIT)}</span>'
        '<button type="button" class="lightbox-close" id="viz-lightbox-close">Close (Esc)</button>'
        "</div>"
        '<img id="viz-lightbox-img" src="" alt=""/>'
        "</div>"
    )


#: 15m board chrome. Display copy describing the PNG the Illustrator renders from
#: the join files — this module never derives a settle, a result or a bankroll.
CHART_15M_TITLE = "KXBTC15M paper windows — 15-minute board"
CHART_15M_PLAIN = (
    "One row per KXBTC15M window: the ticker, the settle status found on disk, and the official "
    "Kalshi result once Kalshi posts one. A window with no result on disk stays SETTLE_PENDING."
)
CHART_15M_SUB = (
    "Read-only PNG rendered from settlements/*.json, latest/journal.json and paper/*.json in "
    "learning_lane_15m. PAPER PNL is that window's own recorded figure on Lineage A only. "
    "Not a golf WC1 / Ill board. Not a combined bankroll."
)
#: Honer board is a sibling block on this lane, not a third parse_lane.
CHART_15M_MISSING = (
    "15m chart not yet available. The Illustrator regenerates it from the join files; nothing is "
    "drawn in its place. No golf WC1 / Ill here."
)
#: How many windows the caption names before it falls back to a count.
CHART_15M_NAMED = 6


def _chart_15m_path() -> Path | None:
    """The Illustrator's 15m PNG, when it is actually on disk."""
    try:
        from golf_offshoot.learning_lane_15m.illustrate import chart_png_path

        path = chart_png_path()
    except Exception:
        return None
    return path if path.is_file() else None


def _chart_honer_path() -> Path | None:
    try:
        from golf_offshoot.honer_15m.illustrate import maybe_render

        path = maybe_render()
    except Exception:
        try:
            from golf_offshoot.honer_15m.paths import board_png_path

            path = board_png_path()
        except Exception:
            return None
    return path if path is not None and path.is_file() else None


def _bold_stars(text: str) -> str:
    out = html.escape(text)
    while "**" in out:
        out = out.replace("**", "<strong>", 1).replace("**", "</strong>", 1)
    return out


def _spine_html() -> str:
    from golf_offshoot.operator_surface.this_window import factory_spine_blurb, factory_title

    return (
        '<section class="panel spine" id="spine">'
        "<h2>Two boxes — two books — two counters</h2>"
        '<p class="help">Neither book is a keep. Trading NOT ARMED. Do not add bankrolls.</p>'
        '<div class="spine-grid">'
        '<div class="spine-box book-factory" data-book="factory">'
        f"<h3>{html.escape(factory_title())}</h3>"
        f"<p>{html.escape(factory_spine_blurb())}</p>"
        '<p><a href="#factory">Jump to factory</a></p>'
        "</div>"
        '<div class="spine-box book-honer" data-book="honer">'
        "<h3>Honer — sibling</h3>"
        "<p>Own root, own money, own k. Search may move a cutoff. "
        "Only tickets within 0.10 of the line move it. "
        "Freeze counts only in-band tickets. "
        "Exam is a later frozen test. Never a keep. Do not add to factory.</p>"
        '<p><a href="#honer">Jump to honer</a></p>'
        "</div>"
        "</div>"
        "</section>"
    )


def _clock_legend_html() -> str:
    from golf_offshoot.localtime import format_eastern, now

    rendered = html.escape(format_eastern(now()))
    factory_bit = "Factory PaperWatch: unavailable"
    honer_bit = "Honer watch: unavailable"
    journal_bit = "Factory journal: n/a"
    factory_png = "Lineage A PNG: n/a"
    honer_png = "Honer PNG: n/a"
    meter_bit = ""
    bus_bit = ""
    sidecar_bit = ""
    try:
        from golf_offshoot.learning_lane_15m.standing import factory_watch_clock

        clock = factory_watch_clock()
        stale = " stale" if clock.get("stale") else ""
        on = "on" if clock.get("running") else "off"
        factory_bit = (
            f"Factory PaperWatch: {on}{stale} · last {clock.get('last') or 'n/a'} · "
            f"{clock.get('at') or 'n/a'}"
        )
        journal_bit = f"Factory journal: {clock.get('journal_at') or 'n/a'}"
        factory_png = f"Lineage A PNG: {clock.get('png_mtime') or 'n/a'} · {clock.get('png_note') or 'n/a'}"
    except Exception:
        pass
    try:
        from golf_offshoot.honer_15m.board import freeze_meter, watch_clock

        clock = watch_clock()
        stale = " stale" if clock.get("stale") else ""
        on = "on" if clock.get("running") else "off"
        honer_bit = (
            f"Honer watch: {on}{stale} · last {clock.get('last') or 'n/a'} · "
            f"{clock.get('at') or 'n/a'}"
        )
        honer_png = f"Honer PNG: {clock.get('png_mtime') or 'n/a'}"
        meter_bit = freeze_meter()
        sidecar_on = "on" if clock.get("running") and not clock.get("stale") else "stale"
        sidecar_bit = (
            f"Honer sidecar: {sidecar_on} · pid {clock.get('pid') or 'n/a'}"
        )
    except Exception:
        pass
    try:
        from golf_offshoot.quote_bus import clock_line

        bus_bit = clock_line()
    except Exception:
        bus_bit = "Quote bus: missing — honer waits; does not fetch"
    meter_p = f"<p>{html.escape(meter_bit)}</p>" if meter_bit else ""
    bus_p = f"<p>{html.escape(bus_bit)}</p>" if bus_bit else ""
    sidecar_p = f"<p>{html.escape(sidecar_bit)}</p>" if sidecar_bit else ""
    return (
        '<section class="panel clocks" id="clocks">'
        "<h2>Clocks</h2>"
        f"<p>Page rendered at {rendered}.</p>"
        f"<p>{html.escape(factory_bit)}</p>"
        f"<p>{html.escape(honer_bit)}</p>"
        f"{sidecar_p}"
        f"{meter_p}"
        f"{bus_p}"
        f"<p>{html.escape(journal_bit)}</p>"
        f"<p>{html.escape(factory_png)}</p>"
        f"<p>{html.escape(honer_png)}</p>"
        "</section>"
    )


def _factory_standing_html() -> str:
    try:
        from golf_offshoot.learning_lane_15m.standing import collect_factory_standing

        standing = collect_factory_standing()
    except Exception as exc:
        return f'<p class="missing">Factory standing unavailable ({html.escape(str(exc))}).</p>'
    keep = f'<p class="loud">{html.escape(standing.not_a_keep)}</p>' if standing.not_a_keep else ""
    return (
        '<div class="standing">'
        "<h3>What it is</h3>"
        f"<p>{_bold_stars(standing.what_it_is)}</p>"
        "<h3>Where it stands</h3>"
        f"<p>{_bold_stars(standing.where_it_stands)}</p>"
        "<h3>Last thing that happened</h3>"
        f"<p>{_bold_stars(standing.last_happened)}</p>"
        "<h3>This book's money</h3>"
        f"<p>{html.escape(standing.this_book)}</p>"
        f"{keep}"
        "</div>"
    )


def _honer_viz_html() -> str:
    path = _chart_honer_path()
    if path is None:
        return (
            '<p class="missing">Honer chart not yet available. '
            "Rendered from honer files only. Nothing is invented in its place.</p>"
        )
    try:
        cache = int(path.stat().st_mtime)
    except OSError:
        cache = 0
    src = f"/viz-honer/honer_window_strip.png?t={cache}"
    title = "KXBTC15M honer search and exam board"
    badges = "".join(
        f'<span class="badge">{html.escape(text)}</span>'
        for text in ("HONER SIBLING", PAPER_ONLY, AI_NO_CASH)
    )
    return (
        '<div class="viz-wall">'
        '<section class="viz wide" id="viz-slot-honer-window-strip">'
        f"<h3>{html.escape(title)}</h3>"
        f'<div class="badge-row">{badges}</div>'
        "<p class=\"plain\">Search block above exam block. Skips are rows. Books do not merge.</p>"
        "<p class=\"sub\">Local honer PNG from golf-offshoot/data/honer_15m. "
        "Not Lineage A. Not published to Pages.</p>"
        "<figure>"
        f'<a class="zoom" href="{src}" data-viz-zoom="1" data-viz-title="{html.escape(title)}" '
        f'aria-label="Enlarge {html.escape(title)}">'
        f'<img src="{src}" alt="{html.escape(title)} — read-only board" width="1700"/>'
        '<span class="zoom-hint">Click to enlarge</span>'
        "</a>"
        '<figcaption><span class="src">Source: honer_15m search/exam files · click to enlarge</span></figcaption>'
        "</figure>"
        "</section>"
        "</div>"
    )


def _window_rows_15m() -> list:
    """Window rows as the Illustrator reads them. Display copy only, never written."""
    try:
        from golf_offshoot.learning_lane_15m.illustrate import collect_rows

        paper_rows, tape_rows = collect_rows()
    except Exception:
        return []
    return list(paper_rows) + list(tape_rows)


def _window_summary_15m(rows: list, *, limit: int = CHART_15M_NAMED) -> tuple[str, str]:
    """(counts line, named-windows line) for the caption.

    Every figure here is copied from a file. ``yes``/``no`` are Kalshi results that
    already exist on disk; anything else counts as pending rather than being guessed.
    """
    if not rows:
        return ("", "")
    yes = no = pending = 0
    named: list[str] = []
    for row in rows:
        result = str(getattr(row, "kalshi_result", "") or "").strip().lower()
        status = str(getattr(row, "settle_status", "") or "").strip() or "unknown"
        ticker = str(getattr(row, "ticker", "") or "")
        if result == "yes":
            yes += 1
        elif result == "no":
            no += 1
        else:
            pending += 1
        if ticker and len(named) < max(0, int(limit)):
            if result in ("yes", "no"):
                named.append(f"{ticker} · {status} · result={result}")
            elif status.upper() == "SETTLE_PENDING":
                named.append(f"{ticker} · SETTLE_PENDING")
            else:
                named.append(f"{ticker} · {status} · SETTLE_PENDING")
    joins = sum(1 for row in rows if getattr(row, "paper_join", False))
    counts = (
        f"{len(rows)} {PRIMARY_SERIES} window(s) on the board — {joins} paper-book join(s), "
        f"{len(rows) - joins} Kalshi-only journal row(s) · "
        f"settled result=yes {yes} · settled result=no {no} · SETTLE_PENDING {pending}"
    )
    if not named:
        return (counts, "")
    rest = len(rows) - len(named)
    tail = f" · +{rest} more on the board" if rest > 0 else ""
    return (counts, "Windows: " + "; ".join(named) + tail)


def _learning_card_html() -> str:
    """Generated card above the strip. Missing stays missing — no invented fallback."""
    from golf_offshoot.learning_lane_15m.learning_card import (
        MISSING_HUB_COPY,
        card_path,
    )

    path = card_path()
    if not path.is_file():
        body = f'<p class="missing">{html.escape(MISSING_HUB_COPY)}</p>'
    else:
        body = f"<pre>{html.escape(path.read_text(encoding='utf-8', errors='replace'))}</pre>"
    return (
        '<section class="learning-card">'
        "<h2>What is on trial (registry proof)</h2>"
        f"{body}"
        "</section>"
    )


def _viz_wall_15m_html() -> str:
    """The 15m board as a labelled figure. Missing stays 'not yet available'."""
    path = _chart_15m_path()
    if path is None:
        return f'<p class="missing">{html.escape(CHART_15M_MISSING)}</p>'
    try:
        cache = int(path.stat().st_mtime)
    except OSError:
        cache = 0
    src = f"/viz15/paper_window_strip.png?t={cache}"
    title = CHART_15M_TITLE
    counts, windows = _window_summary_15m(_window_rows_15m())
    caption_bits = []
    if counts:
        caption_bits.append(f'<span class="counts">{html.escape(counts)}</span>')
    if windows:
        caption_bits.append(f'<span class="windows">{html.escape(windows)}</span>')
    caption_bits.append(
        '<span class="src">Source: learning_lane_15m join files · click the board to enlarge</span>'
    )
    return (
        '<div class="viz-wall" id="viz-wall">'
        '<section class="viz wide" id="viz-slot-paper-window-strip">'
        f"<h3>{html.escape(title)}</h3>"
        f'<p class="plain">{html.escape(CHART_15M_PLAIN)}</p>'
        f'<p class="sub">{html.escape(CHART_15M_SUB)}</p>'
        "<figure>"
        f'<a class="zoom" href="{src}" data-viz-zoom="1" data-viz-title="{html.escape(title)}" '
        f'aria-label="Enlarge {html.escape(title)}">'
        f'<img src="{src}" alt="{html.escape(title)} — read-only board" width="1700"/>'
        '<span class="zoom-hint">Click to enlarge</span>'
        "</a>"
        f'<figcaption>{"".join(caption_bits)}</figcaption>'
        "</figure>"
        "</section>"
        "</div>"
    )


def _settle_banner_html(honesty: HonestyBundle) -> str:
    """Louder display of the existing settle rule. Does not change the rule."""
    shadow = honesty.shadow
    counts = shadow.settle_counts or {}
    tally = (
        f"paper wins {counts.get('paper_win', 0)} · paper losses {counts.get('paper_lose', 0)} · "
        f"never settled {counts.get('never_settled', 0)} · no result yet {counts.get('missing', 0)}"
    )
    if shadow.barred_mock:
        return (
            '<div class="settle">'
            f"<strong>{html.escape(shadow.status)}</strong> — the paper journal is labelled MOCK/DEMO, so it is "
            "barred from the honesty wall. Nothing in it settles anything."
            "</div>"
        )
    if shadow.status != "SHADOW_OK":
        return (
            '<div class="settle">'
            f"<strong>{html.escape(shadow.status)}</strong> — there is no usable paper journal to settle. "
            "That is not zero edge and not a claim of no advises."
            "</div>"
        )
    if shadow.settle_banner:
        return (
            '<div class="settle">'
            f"<strong>{html.escape(shadow.settle_banner)}</strong> — some paper advises still have no official "
            "win or loss result, so this week stays an unsettled claim. Nothing here is settled cash."
            f'<span class="tally">{html.escape(tally)}</span>'
            "</div>"
        )
    return (
        '<div class="settle clear">'
        "<strong>SETTLED ON PAPER</strong> — every relevant paper advise has a paper win or paper loss result. "
        "Still paper observation. Still not cash."
        f'<span class="tally">{html.escape(tally)}</span>'
        "</div>"
    )


def _lane_switch_html(lane: str) -> str:
    golf_css = ' class="active"' if lane != LANE_15M else ""
    m15_css = ' class="active"' if lane == LANE_15M else ""
    return (
        f'<form class="row lane-form" method="get" action="/">'
        f"<fieldset><legend>Lane</legend>"
        f'<button type="submit" name="{SELECTOR_FIELD}" value="{LANE_GOLF}"{golf_css}>Golf (Kalshi)</button>'
        f'<button type="submit" name="{SELECTOR_FIELD}" value="{LANE_15M}"{m15_css}>15-min Kalshi (learning)</button>'
        f"</fieldset></form>"
    )


def _actions_html(event: str, lane: str = LANE_GOLF) -> str:
    buttons = []
    help_rows = []
    if lane == LANE_15M:
        blurbs = (
            ("ingest", "Pull latest data", "Public KXBTC15M fetch. Observation only."),
            ("live", "Update live ranks", "Refresh 15m prices, then paper autobet and settle join."),
            ("shadow", "Check paper journal", "Re-read the 15m journal."),
            ("loop", "Do all three", "One extra cycle now. The 15m watch already repeats researcher → systems by itself."),
            ("refresh", "Reload files", "Re-read saved files from disk. No run is started."),
        )
    else:
        blurbs = (
            ("ingest", "Pull latest data", "One golf Kalshi tick. Does not write Phase 1 or Polymarket ledgers."),
            ("live", "Update live ranks", "One golf Kalshi tick. Paper fill if the brain can see."),
            ("shadow", "Check paper journal", "Re-read the golf Kalshi ledger."),
            ("loop", "Do all three", "One golf Kalshi tick."),
            ("refresh", "Reload files", "Re-read saved files from disk. No run is started."),
        )
    for value, label, blurb in blurbs:
        css = ' class="soft"' if value == "refresh" else ""
        buttons.append(f'<button{css} name="action" value="{value}">{html.escape(label)}</button>')
        help_rows.append(f"<li><b>{html.escape(label)}</b> — {html.escape(blurb)}</li>")
    if lane != LANE_15M:
        event_field = ""
    else:
        event_field = '<p class="help">Series <code>KXBTC15M</code>. No ESPN pin. No Kalshi cash UI.</p>'
    return (
        '<form class="row" method="post" action="/run">'
        f'<input type="hidden" name="{SELECTOR_FIELD}" value="{html.escape(lane)}"/>'
        f"{event_field}"
        f"{''.join(buttons)}"
        "</form>"
        f'<ul class="help">{"".join(help_rows)}</ul>'
    )


def render_html(surface: dict) -> str:
    from golf_offshoot.golf_kalshi.hub import (
        blotter_html as golf_blotter_html,
        cockpit_html as golf_cockpit_html,
        ops_html as golf_ops_html,
        scoreboard_html as golf_scoreboard_html,
        session_html as golf_session_html,
    )
    from golf_offshoot.operator_surface.desk import render_page, session_blotter_15m
    from golf_offshoot.operator_surface.lanes import lookup_lane

    walls = surface["walls"]
    honesty: HonestyBundle = surface["honesty"]
    viz: VizWall = surface["viz"]
    last: RunRecord | None = surface.get("last_run")
    event = html.escape(str(surface.get("event_id") or ""))
    lane = parse_lane(surface.get("lane"))
    spec = lookup_lane(lane)
    if spec is None:
        spec = lookup_lane(LANE_GOLF)
    wall_class = "mock" if walls.is_mock else "ops"
    body_class = "lane-15m" if lane == LANE_15M else "lane-golf"
    mock_lines = ""
    if walls.is_mock:
        mock_lines = "".join(
            f"<div>{html.escape(line)}</div>" for line in (walls.title,) + walls.lines
        )
    actions = _actions_html(event, lane)
    last_html = html.escape(format_run_record(last)) if last else "no operator run this session"
    last_block = (
        f"<h3>Last operator cycle</h3><pre>{last_html}</pre>"
        if last
        else "<p class=\"help\">No operator cycle in this shell session yet. Journal is from disk.</p>"
    )

    if lane == LANE_15M:
        from golf_offshoot.learning_lane_15m.learn import format_wake_line, load_wake_state
        from golf_offshoot.learning_lane_15m.paper import format_15m_observation_board

        viz_wall = _viz_wall_15m_html()
        viz_lightbox = _lightbox_html(
            _chart_15m_path() is not None or _chart_honer_path() is not None
        )
        watch = load_watch_status()
        watch_line = (
            f"watch running={watch.get('running')} interval_s={watch.get('interval_s')} "
            f"cycles={watch.get('cycles')} last={watch.get('last_summary') or 'none'}"
        )
        journal_board = html.escape(
            "\n\n".join(
                (
                    watch_line,
                    format_wake_line(load_wake_state()),
                    format_15m_observation_board(),
                )
            )
        )
        try:
            from golf_offshoot.honer_15m.hub_block import sandbox_html

            honer_block = sandbox_html(extra_html=_honer_viz_html())
        except Exception:
            honer_block = (
                '<section class="panel honer-sandbox book-honer" id="honer" data-book="honer">'
                "<h2>honer_15m sandbox</h2>"
                "</section>"
            )
        try:
            from golf_offshoot.learning_lane_15m.farm_hub import farm_panel_html

            farm_block = farm_panel_html()
        except Exception:
            farm_block = (
                '<section class="panel farm-sandbox book-farm" id="farm" data-book="farm">'
                "<h2>Farm — discovery notebooks</h2>"
                "</section>"
            )
        session_html, blotter_html = session_blotter_15m()
        extras = (
            '<section class="panel" id="extras">'
            "<h2>Operator extras</h2>"
            '<p class="help">Watch is already looping this lane. Buttons are extras. '
            "paper autobet is paper observation only. No golf WC1 here.</p>"
            f"{actions}"
            f"{last_block}"
            '<p class="help">'
            '<a href="https://swellbear.github.io/gated-formalization/observability-hub/">'
            "Public observability hub</a>"
            " — Pages can lag this gym export. This 8765 book is the live book.</p>"
            "</section>"
        )
        from golf_offshoot.operator_surface.this_window import factory_title

        factory_box = (
            '<section class="panel factory-box book-factory" id="factory" data-book="factory">'
            f"<h2>{html.escape(factory_title())}</h2>"
            '<p class="help">KXBTC15M windows from the join files. No golf WC1 / Ill here.</p>'
            f"{viz_wall}"
            "</section>"
        )
        lab = (
            '<section class="panel book-lab" id="lab" data-book="lab">'
            f"{_learning_card_html()}"
            "<h3>Journal</h3>"
            f"<pre>{journal_board}</pre>"
            "</section>"
        )
        views = {
            "scoreboard": factory_box,
            "lab": lab,
            "ops": _spine_html() + _clock_legend_html() + extras,
            "farm": farm_block,
            "honer": honer_block,
        }
    else:
        viz_wall = _viz_wall_html(viz)
        viz_lightbox = _viz_lightbox_html(viz)
        try:
            session_html = golf_session_html()
            blotter_html = golf_blotter_html()
            cockpit = golf_cockpit_html()
            ops_cat = golf_ops_html()
            score = golf_scoreboard_html()
        except Exception:
            session_html = '<div id="desk-session" class="desk-session"></div>'
            blotter_html = (
                '<div id="desk-blotter" class="desk-blotter">'
                '<section class="panel gk book-golf" id="golf-kalshi" data-book="golf"><h2>Open tickets</h2></section>'
                "</div>"
            )
            cockpit = ""
            ops_cat = ""
            score = ""
        try:
            from golf_offshoot.golf_kalshi.organs import farm_panel_html, honer_panel_html

            golf_farm = farm_panel_html()
            golf_honer = honer_panel_html()
        except Exception:
            golf_farm = '<section class="panel gk-organ book-golf" id="golf-farm" data-book="golf"><h2>Golf Farm</h2></section>'
            golf_honer = '<section class="panel gk-organ book-honer" id="golf-honer" data-book="honer"><h2>Golf Honer</h2></section>'
        extras = (
            '<section class="panel" id="extras">'
            "<h2>Operator extras</h2>"
            f"{actions}"
            f"<pre>{last_html}</pre>"
            "</section>"
        )
        museum = (
            '<section class="panel book-golf" id="museum" data-book="golf">'
            "<h2>Previous golf claim</h2>"
            "<p>WC1 fail / not proven. Not this gym.</p>"
            f"{viz_wall}"
            "</section>"
        )
        views = {
            "scoreboard": score + cockpit,
            "ops": ops_cat + extras,
            "farm": golf_farm,
            "honer": golf_honer,
            "museum": museum,
        }

    return render_page(
        lane=lane,
        spec=spec,
        body_class=body_class,
        wall_class=wall_class,
        mock_lines=mock_lines,
        session_html=session_html,
        blotter_html=blotter_html,
        views=views,
        lightbox=viz_lightbox,
    )



class OperatorHandler(BaseHTTPRequestHandler):
    server_version = "golf-offshoot-shell/1"

    def log_message(self, fmt: str, *args) -> None:
        sys.stderr.write("shell: " + (fmt % args) + "\n")

    def _state(self):
        return self.server.surface_state  # type: ignore[attr-defined]

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/":
            qs = parse_qs(parsed.query)
            raw_values = qs.get(SELECTOR_FIELD)
            if raw_values:
                raw_lane = raw_values[0]
                desk_id = desk_lane_from_query(raw_lane)
                if desk_id is None:
                    self._send_html(render_miss(raw_lane))
                    return
                apply_request_lane(self._state(), desk_id)
            else:
                desk_id = LANE_GOLF
            surface = dict(self._state()["surface"])
            surface["lane"] = desk_id
            self._send_html(render_html(surface))
            return
        if parsed.path == "/text":
            body = render_text(self._state()["surface"]).encode("utf-8")
            self._send(200, "text/plain; charset=utf-8", body)
            return
        if parsed.path == "/api/state":
            self._send(200, "application/json", json.dumps(_public_state(self._state()["surface"])).encode("utf-8"))
            return
        if parsed.path == "/api/watch":
            qs = parse_qs(parsed.query)
            raw_lane = (qs.get(SELECTOR_FIELD) or [self._state().get("lane") or LANE_GOLF])[0]
            desk_id = desk_lane_from_query(raw_lane) or parse_lane(raw_lane)
            self._send(
                200,
                "application/json",
                json.dumps(watch_payload(
                    generation=int(self._state().get("generation") or 0),
                    kind=str(self._state().get("reload_kind") or "ok"),
                    lane=desk_id,
                )).encode("utf-8"),
            )
            return
        if parsed.path == "/desk.css":
            self._send(200, "text/css; charset=utf-8", DESK_CSS.read_bytes())
            return
        if parsed.path == "/desk.js":
            self._send(200, "text/javascript; charset=utf-8", DESK_JS.read_bytes())
            return
        if parsed.path == "/export/html":
            honesty: HonestyBundle = self._state()["surface"]["honesty"]
            path = honesty.ranked.html_path
            if path is None:
                self._send(404, "text/plain; charset=utf-8", b"LIVE HTML not yet available\n")
                return
            safe = safe_existing_file(path, honesty.roots.artifact_root)
            if safe is None:
                self._send(404, "text/plain; charset=utf-8", b"export path rejected\n")
                return
            self._send(200, "text/html; charset=utf-8", safe.read_bytes())
            return
        if parsed.path == "/viz15/paper_window_strip.png":
            from golf_offshoot.learning_lane_15m.illustrate import chart_png_path

            path = chart_png_path()
            if path.is_file():
                self._send(200, "image/png", path.read_bytes())
            else:
                self._send(404, "text/plain; charset=utf-8", b"not yet available\n")
            return
        if parsed.path == "/viz-honer/honer_window_strip.png":
            from golf_offshoot.honer_15m.illustrate import chart_png_path

            path = chart_png_path()
            if path.is_file():
                self._send(200, "image/png", path.read_bytes())
            else:
                self._send(404, "text/plain; charset=utf-8", b"not yet available\n")
            return
        if parsed.path == "/golf-catalog/unmatched":
            from golf_offshoot.golf_kalshi.hub import unmatched_fragment_html

            self._send(200, "text/html; charset=utf-8", unmatched_fragment_html().encode("utf-8"))
            return
        if parsed.path == "/golf-catalog/series":
            from golf_offshoot.golf_kalshi.hub import series_fragment_html

            ticker = (parse_qs(parsed.query).get("ticker") or [""])[0]
            fragment = series_fragment_html(ticker)
            if fragment is None:
                self._send(404, "text/plain; charset=utf-8", b"unknown golf series\n")
                return
            self._send(200, "text/html; charset=utf-8", fragment.encode("utf-8"))
            return
        if parsed.path.startswith("/viz-golf/") and parsed.path.endswith(".png"):
            from golf_offshoot.golf_kalshi.paths import board_png_path

            path = board_png_path()
            if path.is_file() and path.name == Path(parsed.path).name:
                self._send(200, "image/png", path.read_bytes())
            else:
                self._send(404, "text/plain; charset=utf-8", b"\n")
            return
        if parsed.path.startswith("/viz/") and parsed.path.endswith(".png"):
            slot_id = Path(parsed.path).stem
            viz: VizWall = self._state()["surface"]["viz"]
            path = viz_file_for_serve(slot_id, viz)
            if path is None:
                self._send(404, "text/plain; charset=utf-8", b"not yet available\n")
                return
            self._send(200, "image/png", path.read_bytes())
            return
        self._send(404, "text/plain; charset=utf-8", b"not found\n")

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path != "/run":
            self._send(404, "text/plain; charset=utf-8", b"not found\n")
            return
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length).decode("utf-8") if length else ""
        form = parse_qs(raw)
        action = (form.get("action") or ["refresh"])[0]
        event = (form.get("event") or [self._state().get("event_id") or ""])[0].strip()
        lane = parse_lane((form.get(SELECTOR_FIELD) or [self._state().get("lane") or LANE_GOLF])[0])
        self._state()["lane"] = lane
        last = None
        try:
            if action != "refresh":
                refuse_forbidden(action)
                last = _dispatch(action, event, self._state())
        except OperatorSafetyError as exc:
            last = RunRecord(command=action, ok=False, event_id=event, error=str(exc))
            last.notice = notify_run_complete(
                command=action,
                ok=False,
                event_id=event,
                detail=str(exc),
                dry_run=True,
                lane=lane,
            )
        self._state()["event_id"] = event
        self._state()["surface"] = build_surface(
            event_id=event or None,
            artifact_root=self._state()["artifact_root"],
            viz_root=self._state()["viz_root"],
            last_run=last,
            lane=lane,
        )
        self.send_response(303)
        self.send_header("Location", f"/?{SELECTOR_FIELD}={lane}")
        self.end_headers()

    def _send_html(self, page: str) -> None:
        self._send(200, "text/html; charset=utf-8", page.encode("utf-8"))

    def _send(self, code: int, ctype: str, body: bytes) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        write_http_body(self.wfile, body, log=lambda msg: self.log_message("%s", msg))


def _dispatch(action: str, event: str, state: dict) -> RunRecord:
    if parse_lane(state.get("lane")) == LANE_15M:
        if action == "ingest":
            return run_15m_ingest(notify=True, refresh=True)
        if action == "live":
            return run_15m_live(notify=True, refresh=True)
        if action == "shadow":
            return run_15m_shadow(notify=False)
        if action == "loop":
            return run_15m_loop(notify=True, refresh=True)
        raise OperatorSafetyError(f"unknown operator action {action!r}")
    if action in {"ingest", "live", "loop"}:
        return run_golf_kalshi_tick(command=action, notify=True)
    if action == "shadow":
        from golf_offshoot.golf_kalshi.paper import load_ledger

        led = load_ledger()
        return RunRecord(
            command="shadow",
            ok=True,
            summary=f"golf kalshi bankroll={led.get('bankroll')}",
            extras={"lane": "golf_kalshi"},
        )
    raise OperatorSafetyError(f"unknown operator action {action!r}")


def _public_state(surface: dict) -> dict:
    honesty: HonestyBundle = surface["honesty"]
    viz: VizWall = surface["viz"]
    return {
        "event_id": surface.get("event_id"),
        "lane": surface.get("lane") or LANE_GOLF,
        "mode": surface["walls"].mode,
        "badges": list(surface["walls"].badges),
        "shadow": honesty.shadow.status,
        "calibration": honesty.calibration.status,
        "ranked": honesty.ranked.status,
        "leftover": honesty.leftover.status,
        "viz": {slot.slot_id: slot.status for slot in viz.slots},
    }


def _watch_state(state: dict) -> dict:
    return {
        "generation": int(state.get("generation") or 0),
        "kind": str(state.get("reload_kind") or "ok"),
    }


def hub_url(host: str, port: int) -> str:
    return f"http://{host}:{port}/"


def open_hub_browser(url: str) -> bool:
    """Refresh the tab that is already open. Only open a new one as a last resort.

    Windows startfile on http:// always opens a new tab, which stacked pages
    every hub re-exec. Even webbrowser.open(..., new=0) is only a request — most
    browsers ignore it and add a tab anyway. So look for the hub window first and
    drive it with F5; that is the path that actually reuses the founder's tab.
    """
    try:
        if refresh_existing_hub_window(url):
            print(f"Refreshed the hub tab already open at {url}")
            return True
    except Exception:
        pass
    try:
        return bool(webbrowser.open(url, new=0, autoraise=True))
    except Exception:
        return False


def maybe_open_hub_browser(url: str, *, enabled: bool) -> bool:
    if not enabled:
        return False
    if is_hub_child():
        # A re-exec child inherits the parent's argv, and a parent started before
        # --no-browser existed hands down open_browser=True forever. The child is
        # a restart of a hub the founder is already looking at, so it never gets
        # to launch a browser regardless of what argv said.
        print("Hub restarted in place. Reusing the tab you already have open.")
        return False
    print(f"Opening hub in your default browser: {url}")
    print("This console keeps the hub running — it is not the hub UI.")
    return open_hub_browser(url)


def _sync_paper_watch(state: dict) -> None:
    """Hub up keeps 15m PaperWatch, Honer, and golf watches on. Tab only changes the page."""
    watch = state.get("paper_watch")
    if watch is None:

        def _on_cycle(payload: dict) -> None:
            meta = payload.get("watch") or {}
            # The cycle records the wake itself. The journal panel draws the
            # current one, so this record only carries which roles it asked for.
            wake = payload.get("learning_wake") or {}
            rec = RunRecord(
                command="watch",
                ok=bool(meta.get("last_ok", True)),
                event_id=PRIMARY_SERIES,
                summary=str(meta.get("last_summary") or "15m watch cycle"),
                table=str(payload.get("report") or ""),
                error=str(meta.get("last_error") or ""),
                extras={
                    "lane": LANE_15M,
                    "watch_cycles": meta.get("cycles"),
                    "roles_owed": [str(row.get("role")) for row in wake.get("roles_owed") or []],
                    "wake_events": len(wake.get("new_events") or []),
                },
            )
            rebuild_surface(state, last_run=rec)
            state["reload_kind"] = "artifacts"

        watch = PaperWatch(on_cycle=_on_cycle)
        state["paper_watch"] = watch
    watch.start()
    _sync_honer_watch(state, running=True)
    _sync_golf_watch(state, running=True)


def _sync_honer_watch(state: dict, *, running: bool) -> None:
    """Sidecar process. Own root. Exceptions stay inside honer_15m.watch."""
    from golf_offshoot.honer_15m.watch import start_sidecar_process, stop_sidecar_process

    if running:
        state["honer_sidecar"] = start_sidecar_process(existing=state.get("honer_sidecar"))
    else:
        stop_sidecar_process(state.get("honer_sidecar"))
        state["honer_sidecar"] = None


def _sync_golf_watch(state: dict, *, running: bool) -> None:
    """Golf Kalshi sidecar. Kill file stops golf only. 15m/Honer stay up."""
    from golf_offshoot.golf_kalshi.watch import start_sidecar_process, stop_sidecar_process

    if running:
        state["golf_sidecar"] = start_sidecar_process(existing=state.get("golf_sidecar"))
    else:
        stop_sidecar_process(state.get("golf_sidecar"))
        state["golf_sidecar"] = None


def apply_request_lane(state: dict, raw: str | None) -> bool:
    """Keep PaperWatch in sync. Rebuild only when the lane actually changes.

    `/?lane=learning_lane_15m` is on every reload. Rebuilding the 15m surface on
    each GET made the page slower than the next generation bump, which aborted
    the body write and looped.
    """
    if raw is None or str(raw).strip() == "":
        return False
    new_lane = parse_lane(raw)
    current = parse_lane(state.get("lane"))
    state["lane"] = new_lane
    _sync_paper_watch(state)
    if new_lane == current:
        return False
    rebuild_surface(state)
    return True


def rebuild_surface(state: dict, *, last_run: RunRecord | None | object = ...) -> None:
    keep = state["surface"].get("last_run") if last_run is ... else last_run
    try:
        from golf_offshoot.two_brains import sync as sync_two_brains

        sync_two_brains()
    except Exception:
        pass
    state["surface"] = build_surface(
        event_id=state.get("event_id") or None,
        artifact_root=state.get("artifact_root"),
        viz_root=state.get("viz_root"),
        last_run=keep,
        lane=state.get("lane") or LANE_GOLF,
    )


class _HubServer(ThreadingHTTPServer):
    allow_reuse_address = True


def _watch_loop(httpd: ThreadingHTTPServer, state: dict, stop: threading.Event) -> None:
    poll_s = float(os.environ.get("GOLF_OFFSHOOT_HUB_POLL") or DEFAULT_POLL_S)
    debounce_s = float(os.environ.get("GOLF_OFFSHOOT_HUB_DEBOUNCE") or DEFAULT_DEBOUNCE_S)

    def _snap():
        return collect_snapshot(
            roots=resolve_roots(
                artifact_root=state.get("artifact_root"),
                viz_root=state.get("viz_root"),
            )
        )

    watcher = HubWatcher(debounce_s=debounce_s, snapshot_fn=_snap)
    watcher.seed()
    while not stop.wait(max(0.2, poll_s)):
        decision = watcher.poll()
        if decision.kind == "none":
            continue
        if decision.should_reexec:
            state["reload_kind"] = "code"
            state["generation"] = int(state.get("generation") or 0) + 1
            sys.stderr.write("shell: git/code updated; restarting hub\n")
            httpd.shutdown()
            return
        if decision.should_soft_reload:
            rebuild_surface(state)
            state["reload_kind"] = "artifacts"
            sys.stderr.write("shell: artifacts updated; UI will patch\n")


def serve(
    *,
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
    event_id: str | None = None,
    open_browser: bool = True,
    artifact_root: Path | None = None,
    viz_root: Path | None = None,
    lane: str | None = None,
) -> int:
    if not is_hub_child():
        # Parent opens the browser once. Children never do — a code re-exec
        # used to call startfile again and spawn a new Chrome tab every time.
        if open_browser:
            maybe_open_hub_browser(hub_url(host, port), enabled=True)
        cmd = hub_child_command(
            host=host,
            port=port,
            event_id=event_id,
            open_browser=False,
            artifact_root=artifact_root,
            viz_root=viz_root,
            lane=lane,
        )
        return supervise_hub_child(cmd)
    return run_http_server(
        host=host,
        port=port,
        event_id=event_id,
        open_browser=open_browser,
        artifact_root=artifact_root,
        viz_root=viz_root,
        lane=lane,
    )


def run_http_server(
    *,
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
    event_id: str | None = None,
    open_browser: bool = True,
    artifact_root: Path | None = None,
    viz_root: Path | None = None,
    lane: str | None = None,
) -> int:
    start_lane = parse_lane(lane)
    state = {
        "event_id": event_id or "",
        "artifact_root": artifact_root,
        "viz_root": viz_root,
        "odds_book": "auto",
        "lane": start_lane,
        "generation": 0,
        "reload_kind": "ok",
        "surface": build_surface(
            event_id=event_id,
            artifact_root=artifact_root,
            viz_root=viz_root,
            lane=start_lane,
        ),
        "paper_watch": None,
    }
    _sync_paper_watch(state)
    httpd = _HubServer((host, port), OperatorHandler)
    httpd.surface_state = state  # type: ignore[attr-defined]
    url = hub_url(host, port)
    print(build_mode_walls(live_data=True).render_text())
    print(f"operator shell {url}")
    print(f"PHASE 1 OBSERVATION. Trading {NOT_ARMED}. {PAPER_ONLY}. {CASH_BADGE}")
    maybe_open_hub_browser(url, enabled=open_browser)
    stop = threading.Event()
    watcher = threading.Thread(target=_watch_loop, args=(httpd, state, stop), daemon=True, name="hub-watch")
    watcher.start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("shell stopped")
        stop.set()
        httpd.shutdown()
        return 0
    finally:
        stop.set()
        httpd.server_close()
        try:
            _sync_honer_watch(state, running=False)
            _sync_golf_watch(state, running=False)
        except Exception:
            pass
    if state.get("reload_kind") == "code":
        return REEXEC_CODE
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Phase 1 operator shell (observation only)")
    parser.add_argument("--event", default="", help="ESPN event id")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--print", action="store_true", dest="dump", help="print the surface and exit")
    parser.add_argument(
        "--install-desktop-shortcut",
        action="store_true",
        help="write a Desktop launcher for the Phase 1 hub and exit",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="do not open the default browser (the browser is the hub UI)",
    )
    parser.add_argument("--artifact-root", default="", help="override data/artifact SoT root")
    parser.add_argument("--viz-root", default="", help="override Illustrator viz-wall root")
    parser.add_argument(
        "--lane",
        default=LANE_GOLF,
        choices=[LANE_GOLF, LANE_15M],
        help="exact lane=golf|learning_lane_15m. No bare 15m alias.",
    )
    args = parser.parse_args(argv)
    artifact = Path(args.artifact_root) if args.artifact_root else None
    viz = Path(args.viz_root) if args.viz_root else None
    event = args.event or None
    lane = parse_lane(args.lane)
    if args.install_desktop_shortcut:
        from golf_offshoot.operator_surface.desktop import SHORTCUT_STEM, write_desktop_launcher

        desktop = Path.home() / "Desktop"
        path = write_desktop_launcher(desktop=desktop)
        print(f"wrote Desktop launcher: {path}")
        print(f"Windows .lnk installer: scripts/windows/Install-Desktop-Shortcut.bat")
        print(f"{SHORTCUT_STEM}: PHASE 1 OBSERVATION. Trading NOT ARMED. {CASH_BADGE}")
        return 0
    if args.dump:
        print(render_text(build_surface(event_id=event, artifact_root=artifact, viz_root=viz, lane=lane)))
        return 0
    return serve(
        host=args.host,
        port=args.port,
        event_id=event,
        open_browser=not args.no_browser,
        artifact_root=artifact,
        viz_root=viz,
        lane=lane,
    )


if __name__ == "__main__":
    sys.exit(main())
