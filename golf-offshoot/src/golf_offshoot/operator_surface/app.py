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
from golf_offshoot.learning_lane_15m.watch import PaperWatch
from golf_offshoot.operator_surface.artifacts import HonestyBundle, load_honesty
from golf_offshoot.operator_surface.hub_browser import refresh_existing_hub_window
from golf_offshoot.operator_surface.lane_15m_home import (
    ACTION_BUTTONS_15M,
    CHART_15M_MISSING,
    CHART_15M_NAMED,
    CHART_15M_PLAIN,
    CHART_15M_SUB,
    CHART_15M_TITLE,
    LANE_15M_CSS,
    LANE_15M_JS,
    chart_15m_path as _chart_15m_path,
    glance_strip_html,
    header_15m_html,
    live_payload as _15m_live_payload,
    main_15m_html,
    other_lane_tiles_html,
    role_strip_html,
    session_strip_html,
    tabs_nav_html,
    this_lane_now_html,
    viz_wall_15m_html as _viz_wall_15m_html,
    window_rows_15m as _window_rows_15m,
    window_summary_15m as _window_summary_15m,
)
from golf_offshoot.operator_surface import lane_golf_home as golf_home
from golf_offshoot.operator_surface.lanes import SELECTOR_FIELD, lane_header_name, parse_lane
from golf_offshoot.operator_surface.modes import (
    AI_NO_CASH,
    CASH_BADGE,
    NOT_ARMED,
    PAPER_ONLY,
    build_mode_walls,
)
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
    "no Kalshi account, key, or wallet scope"
)
HARD_NO_STRIP_GOLF = (
    HARD_NO_STRIP + " · do not add honer bankrolls to Lineage A"
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
        f'<span class="badge">{html.escape(CASH_BADGE)}</span>'
        '<button type="button" class="lightbox-close" id="viz-lightbox-close">Close (Esc)</button>'
        "</div>"
        '<img id="viz-lightbox-img" src="" alt=""/>'
        "</div>"
    )


# 15m board chrome lives in lane_15m_home. Re-exported so existing tests keep importing here.


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
    blurbs = ACTION_BUTTONS
    if lane == LANE_15M:
        blurbs = ACTION_BUTTONS_15M
    for value, label, blurb in blurbs:
        css = ' class="soft"' if value == "refresh" else ""
        buttons.append(f'<button{css} name="action" value="{value}">{html.escape(label)}</button>')
        help_rows.append(f"<li><b>{html.escape(label)}</b> — {html.escape(blurb)}</li>")
    if lane != LANE_15M:
        event_field = (
            "<label>Tournament id (ESPN)"
            f'<input name="event" type="text" value="{event}" placeholder="401811963"/>'
            "</label>"
        )
    else:
        event_field = '<p class="help">Series <code>KXBTC15M</code>. No ESPN pin. No Kalshi cash UI.</p>'
    return (
        _lane_switch_html(lane)
        + '<form class="row" method="post" action="/run">'
        f'<input type="hidden" name="{SELECTOR_FIELD}" value="{html.escape(lane)}"/>'
        f"{event_field}"
        f"{''.join(buttons)}"
        "</form>"
        f'<ul class="help">{"".join(help_rows)}</ul>'
    )


def render_html(surface: dict) -> str:
    walls = surface["walls"]
    honesty: HonestyBundle = surface["honesty"]
    viz: VizWall = surface["viz"]
    last: RunRecord | None = surface.get("last_run")
    lane = parse_lane(surface.get("lane"))
    wall_class = "mock" if walls.is_mock else "ops"
    is_15m = lane == LANE_15M
    body_class = "lane-15m" if is_15m else "lane-golf"
    view_attr = ' data-view="home"'
    market_lock = PRIMARY_SERIES if is_15m else golf_home.DATA_MARKET
    charts_help = (
        "KXBTC15M windows from the join files. No golf WC1 / Ill here."
        if is_15m
        else (
            "Illustrator boards that exist on disk. A missing chart stays not yet available and is "
            "never invented, and no edge badge is ever added. Phone alerts are notify-first; this "
            "hub stays local."
        )
    )
    # A barred MOCK/DEMO path still states itself in full. The operating path does not:
    # it is an observation page, and the standing Hard NOs are the one footer strip.
    wall_lines = "".join(f"<div>{html.escape(line)}</div>" for line in walls.lines) if walls.is_mock else ""
    if walls.is_mock:
        wall_lines = f"<div>{html.escape(walls.title)}</div>" + wall_lines
    lane_line = f"Active lane: {lane_header_name(lane)}"
    extra_css = ""
    extra_js = ""
    page_title = "golf-offshoot operator shell"
    switch_bar = f'<div class="lane-switch">{_lane_switch_html(lane)}</div>'
    paper_html = ""
    golf_home_panels = ""
    if is_15m:
        lane_line = f"{lane_line} — LEARNING LANE"
        viz_wall = _viz_wall_15m_html()
        # The 15m board carries its own overlay. Deriving it from the golf viz wall
        # left this lane with no lightbox at all whenever golf had no chart on disk.
        viz_lightbox = _lightbox_html(_chart_15m_path() is not None)
        settle_banner = (
            switch_bar
            + glance_strip_html()
            + session_strip_html()
            + tabs_nav_html()
            + this_lane_now_html()
            + other_lane_tiles_html()
            + role_strip_html()
        )
        header_block = header_15m_html(lane_line=lane_line, wall_lines=wall_lines)
        extra_css = LANE_15M_CSS
        extra_js = LANE_15M_JS
        page_title = "KXBTC15M paper watch"
        lane_body = main_15m_html(last_run=last)
        hard_no = HARD_NO_STRIP
    else:
        viz_wall = _viz_wall_html(viz)
        viz_lightbox = _viz_lightbox_html(viz)
        header_block = golf_home.header_golf_html(
            lane_line=lane_line, wall_lines=wall_lines, wall_class=wall_class
        )
        extra_css = LANE_15M_CSS + golf_home.LANE_GOLF_CSS
        extra_js = golf_home.LANE_GOLF_JS
        page_title = golf_home.HEADER_TITLE
        settle_banner = (
            switch_bar
            + golf_home.glance_strip_html()
            + golf_home.session_strip_html()
            + golf_home.tabs_nav_html()
            + golf_home.this_lane_now_html()
            + golf_home.other_lane_tiles_html()
            + golf_home.role_strip_html()
        )
        ranked = html.escape(honesty.ranked.text)
        leftover = html.escape(honesty.leftover.text)
        inventory = html.escape(honesty.inventory.text)
        shadow = html.escape(honesty.shadow.text)
        calib = html.escape(honesty.calibration.text)
        html_link = ""
        if honesty.ranked.html_path:
            html_link = (
                f'<p>Full export: <a href="/export/html">{html.escape(str(honesty.ranked.html_path))}</a></p>'
            )
        last_html = html.escape(format_run_record(last)) if last else "no operator run this session"
        if last is not None and last.paper and not golf_home._is_15m_run(last):
            paper_block = (
                "<h3>Paper observation (not trading)</h3>"
                '<p class="help">A pretend bankroll kept so the model can be scored later. '
                "No ticket is placed, no money moves, and nothing here needs approval. "
                "Paper bankroll auto-apply is paper observation only — it is "
                "not trading armed.</p>"
                f"<pre>{html.escape(last.paper)}</pre>"
            )
        else:
            paper_block = ""
        honesty_blocks = (
            f'<p class="help">{html.escape(charts_help)}</p>'
            '<section class="panel">'
            "<h2>Ranked table — latest real live run</h2>"
            f'<p class="loud">{html.escape(honesty.ranked.banner)}</p>'
            f"{html_link}"
            f"<pre>{ranked}</pre>"
            "</section>"
            '<section class="panel">'
            "<h2>Still unmeasured (display only)</h2>"
            '<p class="help">Things the model cannot see yet. Listed so they are not quietly folded into a rating.</p>'
            f"<pre>{leftover}</pre>"
            "</section>"
            '<section class="panel">'
            "<h2>Where the numbers came from</h2>"
            f"<pre>{inventory}</pre>"
            "</section>"
            '<section class="panel">'
            "<h2>Paper journal (shadow log)</h2>"
            '<p class="help">A written log of past paper advises and whether each one has an official result yet. '
            "It is not a bankroll and not settled cash.</p>"
            f"<pre>{shadow}</pre>"
            "</section>"
            '<section class="panel">'
            "<h2>Calibration check</h2>"
            '<p class="help">Re-fitted weights are stored, not used, while the recommendation stays keep_expert. '
            "Edge is not established.</p>"
            f"<pre>{calib}</pre>"
            "</section>"
            f"{paper_block}"
        )
        lane_body = golf_home.main_golf_html(
            last_run=last,
            viz_wall=viz_wall,
            honesty_blocks=honesty_blocks,
            settle_banner=_settle_banner_html(honesty),
        )
        hard_no = HARD_NO_STRIP_GOLF
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{html.escape(page_title)}</title>
<style>
 body {{ font-family: Segoe UI, Helvetica, Arial, sans-serif; margin: 0; background: #f4f1ea; color: #1b1b1b; }}
 header.ops {{ background: #1f3b4d; color: #fff; padding: 16px 20px; }}
 header.mock {{ background: #7a0c0c; color: #fff; padding: 16px 20px; }}
 header h1 {{ margin: 0; font-size: 26px; letter-spacing: 1px; }}
 header div {{ font-size: 14px; margin-top: 8px; }}
 header .lane-line {{ font-size: 13px; opacity: 0.85; margin-top: 6px; }}
 .badge {{ display: inline-block; margin: 4px 6px 0 0; padding: 3px 8px; background: #0e1f29; color: #f2e27a; font-size: 12px; font-weight: 700; }}
 main {{ padding: 0 20px 56px; max-width: 1100px; margin: 0 auto; }}
 /* The 15m board is a wide table-and-strip figure. Give it room to be read in
    place instead of making the lightbox the only legible view. */
 body.lane-15m main {{ max-width: 1560px; }}
 body.lane-golf main {{ max-width: 1400px; }}
 form.row {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: end; margin: 4px 0 10px; }}
 form.lane-form fieldset {{ border: 1px solid #c9c2b2; padding: 8px 10px; }}
 form.lane-form legend {{ font-size: 13px; font-weight: 700; }}
 form.lane-form button.active {{ outline: 2px solid #f2e27a; }}
 label {{ font-size: 13px; display: flex; flex-direction: column; gap: 4px; }}
 input[type=text] {{ padding: 6px 8px; min-width: 180px; }}
 button {{ padding: 8px 12px; background: #1f3b4d; color: #fff; border: 0; cursor: pointer; font-size: 14px; }}
 button.soft {{ background: #55606b; }}
 button.warn {{ background: #7a0c0c; }}
 pre {{ white-space: pre-wrap; background: #fff; border: 1px solid #c9c2b2; padding: 12px; font-size: 13px; }}
 .missing {{ background: #f8e0a0; padding: 10px; border: 1px solid #c9a227; }}
 .hard-no {{ position: sticky; bottom: 0; background: #1b1b1b; color: #d8d2c2; padding: 6px 16px; font-size: 12px; }}
 .settle {{ background: #7a0c0c; color: #fff; padding: 12px 20px; font-size: 15px; }}
 .settle.clear {{ background: #14532d; }}
 .settle .tally {{ display: block; margin-top: 4px; font-size: 13px; opacity: 0.9; }}
 .panel {{ background: #fff; border: 1px solid #c9c2b2; padding: 14px 16px; margin: 18px 0; }}
 .panel h2 {{ margin: 0; font-size: 20px; }}
 .panel .help {{ font-size: 13px; color: #4a4a4a; margin: 6px 0 10px; }}
 ul.help {{ font-size: 13px; color: #4a4a4a; margin: 6px 0 0; padding-left: 20px; }}
 .loud {{ font-weight: 700; margin: 6px 0; }}
 .viz-wall {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px; }}
 .viz {{ margin: 0; padding: 12px; background: #fff; border: 1px solid #c9c2b2; }}
 .viz h3 {{ margin: 0 0 6px; font-size: 17px; }}
 .viz .plain {{ font-size: 13px; color: #333; margin: 0 0 6px; }}
 .viz .sub {{ font-size: 12px; color: #4a4a4a; margin: 0 0 8px; }}
 .viz img {{ display: block; width: 100%; max-width: 100%; height: auto; border: 1px solid #c9c2b2; background: #111; }}
 .viz.wide {{ grid-column: 1 / -1; }}
 .viz .badge-row {{ margin: 0 0 8px; }}
 .viz figure {{ margin: 0; }}
 .viz figcaption {{ margin-top: 8px; font-size: 12px; color: #4a4a4a; line-height: 1.55; }}
 .viz figcaption span {{ display: block; }}
 .viz figcaption .counts {{ margin-bottom: 4px; font-size: 13px; font-weight: 700; color: #1b1b1b; }}
 .viz figcaption .windows {{ margin-bottom: 4px; font-family: Consolas, "Courier New", monospace; color: #333; }}
 .viz figcaption .src {{ font-style: italic; }}
 .viz a.zoom {{ display: block; cursor: zoom-in; color: inherit; text-decoration: none; }}
 .viz a.zoom:focus-visible {{ outline: 3px solid #1f3b4d; outline-offset: 2px; }}
 .viz .zoom-hint {{ display: block; margin-top: 6px; font-size: 12px; color: #4a4a4a; }}
 .viz a.zoom:hover .zoom-hint, .viz a.zoom:focus .zoom-hint {{ color: #1f3b4d; text-decoration: underline; }}
 .lightbox {{ position: fixed; top: 0; right: 0; bottom: 0; left: 0; z-index: 100; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 10px; padding: 0 14px 14px; overflow: hidden; background: rgba(12, 14, 16, 0.94); }}
 .lightbox[hidden] {{ display: none; }}
 .lightbox.full {{ justify-content: flex-start; overflow: auto; }}
 .lightbox-bar {{ position: sticky; top: 0; z-index: 1; display: flex; flex-wrap: wrap; gap: 12px; align-items: center; justify-content: space-between; width: 100%; padding: 10px 0; background: rgba(12, 14, 16, 0.94); color: #f4f1ea; font-size: 14px; }}
 .lightbox-title {{ font-weight: 700; }}
 .lightbox-hint {{ font-size: 12px; opacity: 0.85; }}
 .lightbox-close {{ background: #55606b; }}
 .lightbox img {{ max-width: 100%; max-height: 86vh; width: auto; height: auto; cursor: zoom-in; border: 1px solid #c9c2b2; background: #111; }}
 .lightbox.full img {{ width: 100%; max-width: 100%; max-height: none; height: auto; cursor: zoom-out; }}
 body.viz-zoomed {{ overflow: hidden; }}
{extra_css}
</style>
</head>
<body class="{body_class}" data-lane="{html.escape(lane)}" data-market="{html.escape(market_lock)}"{view_attr}>
{header_block}
{settle_banner}
<main>
  {golf_home_panels}
  {paper_html}
  {lane_body}
</main>
<div class="hard-no">{html.escape(hard_no)}</div>
{viz_lightbox}
<script>
(function(){{
  var box = document.getElementById('viz-lightbox');
  if (!box) return;
  var shown = document.getElementById('viz-lightbox-img');
  var caption = document.getElementById('viz-lightbox-title');
  var hint = document.getElementById('viz-lightbox-hint');
  function setFull(on){{
    box.classList.toggle('full', on);
    hint.textContent = on ? {json.dumps(ZOOM_HINT_FULL)} : {json.dumps(ZOOM_HINT_FIT)};
    box.scrollTop = 0;
  }}
  function openBox(href, title){{
    shown.setAttribute('src', href);
    shown.setAttribute('alt', title);
    caption.textContent = title;
    setFull(false);
    box.hidden = false;
    document.body.classList.add('viz-zoomed');
  }}
  function closeBox(){{
    if (box.hidden) return;
    box.hidden = true;
    shown.setAttribute('src', '');
    document.body.classList.remove('viz-zoomed');
  }}
  document.addEventListener('click', function(ev){{
    if (!box.hidden) {{
      if (ev.target === shown) setFull(!box.classList.contains('full'));
      else closeBox();
      return;
    }}
    if (ev.button || ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.altKey) return;
    var link = ev.target && ev.target.closest ? ev.target.closest('a.zoom') : null;
    if (!link) return;
    ev.preventDefault();
    openBox(link.getAttribute('href'), link.getAttribute('data-viz-title') || '');
  }});
  document.addEventListener('keydown', function(ev){{
    if (ev.key === 'Escape' || ev.key === 'Esc') closeBox();
  }});
}})();
{extra_js}
(function(){{
  // Same-tab refresh. Nobody clicks reload: a hub restart bounces /api/watch,
  // and this tab reloads itself as soon as the port answers again.
  // Watch heartbeats patch the glance. Full reload is only after
  // the hub process itself went away (code re-exec).
  var boot = null;
  var lost = false;
  var is15 = document.body.classList.contains('lane-15m');
  var isGolf = document.body.classList.contains('lane-golf');
  function normHtml(html){{
    return String(html || '').replace(/(data-close-epoch="[^"]*">)[^<]*/g, '$1');
  }}
  function setHtml(el, html){{
    if (!el || html == null) return;
    if (normHtml(el.innerHTML) === normHtml(html)) return;
    var opened = [];
    el.querySelectorAll('details').forEach(function(d){{ opened.push(d.open); }});
    el.innerHTML = html;
    el.querySelectorAll('details').forEach(function(d, i){{
      if (opened[i] !== undefined) d.open = opened[i];
    }});
  }}
  function applyHome(home){{
    if (!home) return;
    setHtml(document.getElementById('glance-strip'), home.glance_html);
    setHtml(document.getElementById('session-strip'), home.session_html);
    setHtml(document.getElementById('lane-now'), home.now_html);
    setHtml(document.getElementById('lane-tiles'), home.tiles_html);
    setHtml(document.getElementById('role-strip'), home.roles_html);
    setHtml(document.getElementById('journal-exceptions'), home.exceptions_html);
    setHtml(document.getElementById('chart-15m-caption'), home.caption_html);
    var src = home.chart_src;
    if (src) {{
      document.querySelectorAll('#viz-slot-paper-window-strip img').forEach(function(img){{
        if (img.getAttribute('src') === src) return;
        img.setAttribute('src', src);
        var zoom = img.closest('a.zoom');
        if (zoom) zoom.setAttribute('href', src);
      }});
    }}
    setHtml(document.getElementById('tab-lab-body'), home.lab_html);
    setHtml(document.getElementById('tab-bot-body'), home.bot_html);
    setHtml(document.getElementById('tab-scoreboard-body'), home.scoreboard_html);
    setHtml(document.getElementById('tab-ops-watch'), home.ops_watch_html);
    setHtml(document.getElementById('gk-tickets-home'), home.tickets_html);
    setHtml(document.getElementById('gk-sleeves-slot'), home.sleeves_html);
    setHtml(document.getElementById('golf-farm-body'), home.farm_html);
    setHtml(document.getElementById('golf-honer-body'), home.honer_html);
    var rail = document.getElementById('cockpit-rail');
    if (rail && home.cockpit_html) {{
      var box = document.createElement('div');
      box.innerHTML = home.cockpit_html;
      var next = box.firstElementChild;
      if (next) setHtml(rail, next.innerHTML);
    }}
  }}
  function tick(){{
    fetch('/api/watch', {{cache:'no-store'}}).then(function(r){{
      if (!r.ok) throw new Error('hub ' + r.status);
      return r.json();
    }}).then(function(s){{
      if (is15 || isGolf) {{
        if (lost && boot !== null && s.boot != null && String(s.boot) !== String(boot)) {{
          location.reload();
          return;
        }}
        lost = false;
        if (s.boot != null) boot = s.boot;
        applyHome(s.home);
        return;
      }}
    }}).catch(function(){{ lost = true; }});
  }}
  setInterval(tick, 1500);
  tick();
}})();
</script>
</body>
</html>
"""


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
            if qs.get(SELECTOR_FIELD):
                self._state()["lane"] = parse_lane(qs.get(SELECTOR_FIELD)[0])
                _sync_paper_watch(self._state())
                rebuild_surface(self._state())
            self._send_html(render_html(self._state()["surface"]))
            return
        if parsed.path == "/text":
            body = render_text(self._state()["surface"]).encode("utf-8")
            self._send(200, "text/plain; charset=utf-8", body)
            return
        if parsed.path == "/api/state":
            self._send(200, "application/json", json.dumps(_public_state(self._state()["surface"])).encode("utf-8"))
            return
        if parsed.path == "/api/watch":
            self._send(200, "application/json", json.dumps(_watch_state(self._state())).encode("utf-8"))
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
        if parsed.path.startswith("/viz/") and parsed.path.endswith(".png"):
            slot_id = Path(parsed.path).stem
            viz: VizWall = self._state()["surface"]["viz"]
            path = viz_file_for_serve(slot_id, viz)
            if path is None:
                self._send(404, "text/plain; charset=utf-8", b"not yet available\n")
                return
            self._send(200, "image/png", path.read_bytes())
            return
        if parsed.path == "/golf-catalog/series":
            qs = parse_qs(parsed.query)
            ticker = (qs.get("ticker") or [""])[0]
            body, status = golf_home.golf_catalog_series_html(ticker)
            self._send(status, "text/html; charset=utf-8", body.encode("utf-8"))
            return
        if parsed.path == "/golf-catalog/unmatched":
            body, status = golf_home.golf_catalog_unmatched_html()
            self._send(status, "text/html; charset=utf-8", body.encode("utf-8"))
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
        self.wfile.write(body)


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
    kwargs = {
        "event_id": event or None,
        "odds_book": state.get("odds_book") or "auto",
        "notify": True,
    }
    if action == "ingest":
        return run_ingest(**kwargs)
    if action == "live":
        return run_live(**kwargs)
    if action == "shadow":
        return run_shadow(notify=False)
    if action == "loop":
        return run_loop(**kwargs)
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
    lane = parse_lane(state.get("lane") or LANE_GOLF)
    payload = {
        "generation": int(state.get("generation") or 0),
        "kind": str(state.get("reload_kind") or "ok"),
        "lane": lane,
        "cycle": int(state.get("watch_cycles") or 0),
        "boot": os.getpid(),
    }
    if lane == LANE_15M:
        try:
            payload["home"] = _15m_live_payload(state)
        except Exception as exc:
            payload["home_error"] = str(exc)
    elif lane == LANE_GOLF:
        try:
            payload["home"] = golf_home.live_payload(state)
        except Exception as exc:
            payload["home_error"] = str(exc)
    return payload


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
    """15m starts PaperWatch. Golf chrome never stops it. Founder does not click."""
    watch = state.get("paper_watch")
    keep = bool(state.get("paper_watch_keep"))
    on_15m = parse_lane(state.get("lane")) == LANE_15M
    if not on_15m and not keep:
        return

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
            state["watch_cycles"] = int(meta.get("cycles") or 0)
            # A 90s heartbeat is not a reason to full-page reload the tab.
            if state.get("reload_kind") != "code":
                state["reload_kind"] = "watch"

        watch = PaperWatch(on_cycle=_on_cycle)
        state["paper_watch"] = watch
    watch.start()
    state["paper_watch_keep"] = True


def rebuild_surface(state: dict, *, last_run: RunRecord | None | object = ...) -> None:
    keep = state["surface"].get("last_run") if last_run is ... else last_run
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
            state["generation"] = int(state.get("generation") or 0) + 1
            sys.stderr.write("shell: artifacts updated; UI will refresh\n")


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
        "paper_watch_keep": False,
        "watch_cycles": 0,
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
