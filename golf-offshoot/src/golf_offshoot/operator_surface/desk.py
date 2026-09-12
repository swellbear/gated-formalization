"""8765 desk chrome: document shell, miss page, lane-keyed watch fragments."""

from __future__ import annotations

import hashlib
import html
import re
from pathlib import Path
from typing import Any

from golf_offshoot.learning_lane_15m.paths import LANE_15M, LANE_GOLF
from golf_offshoot.operator_surface.lanes import (
    SELECTOR_FIELD,
    VIEW_LABELS,
    LaneSpec,
    lookup_lane,
    registered_lanes,
)

DESK_DIR = Path(__file__).resolve().parent
DESK_CSS = DESK_DIR / "desk.css"
DESK_JS = DESK_DIR / "desk.js"


def asset_mtime(path: Path) -> int:
    try:
        return int(path.stat().st_mtime)
    except OSError:
        return 0


def asset_href(name: str) -> str:
    path = DESK_CSS if name.endswith(".css") else DESK_JS
    return f"/{name}?t={asset_mtime(path)}"


def fragment_hash(session_html: str, blotter_html: str) -> str:
    blob = (session_html + "\n" + blotter_html).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:16]


def _lane_switch_html(active: str) -> str:
    buttons = []
    for spec in registered_lanes():
        css = ' class="active"' if spec.id == active else ""
        buttons.append(
            f'<button type="submit" name="{SELECTOR_FIELD}" value="{html.escape(spec.id)}"{css}>'
            f"{html.escape(spec.display_name)}</button>"
        )
    return (
        f'<form class="row lane-form" method="get" action="/">'
        f"<fieldset><legend>Lane</legend>"
        f"{''.join(buttons)}"
        f"</fieldset></form>"
    )


def _view_nav_html(spec: LaneSpec) -> str:
    bits = []
    for view_id in spec.views:
        label = VIEW_LABELS.get(view_id, view_id)
        bits.append(
            f'<button type="button" data-view-id="{html.escape(view_id)}">{html.escape(label)}</button>'
        )
    return f'<nav class="desk-views" aria-label="Desk views">{"".join(bits)}</nav>'


def render_page(
    *,
    lane: str,
    spec: LaneSpec,
    body_class: str,
    wall_class: str,
    mock_lines: str,
    session_html: str,
    blotter_html: str,
    views: dict[str, str],
    lightbox: str,
) -> str:
    title = spec.display_name
    view_blocks = []
    for view_id in spec.views:
        inner = views.get(view_id) or ""
        if view_id == "home":
            inner = session_html + blotter_html + inner
        view_blocks.append(f'<div class="desk-view desk-view-{html.escape(view_id)}">{inner}</div>')
    lane_chip = ""
    if lane == LANE_15M:
        lane_chip = '<span class="desk-paper">LEARNING LANE</span>'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="{asset_href('desk.css')}"/>
</head>
<body class="{html.escape(body_class)}" data-lane="{html.escape(lane)}" data-view="home">
<header class="desk-head {html.escape(wall_class)}">
  <h1>{html.escape(title)}</h1>
  <span class="desk-paper">PAPER</span>
  {lane_chip}
  {mock_lines}
</header>
<div class="lane-switch">{_lane_switch_html(lane)}</div>
{_view_nav_html(spec)}
<main>
  {''.join(view_blocks)}
</main>
{lightbox}
<script src="{asset_href('desk.js')}"></script>
</body>
</html>
"""


def render_miss(raw: str) -> str:
    asked = html.escape(str(raw or "").strip() or "(empty)")
    ids = ", ".join(spec.id for spec in registered_lanes())
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Lane not registered</title>
<link rel="stylesheet" href="{asset_href('desk.css')}"/>
</head>
<body class="desk-miss" data-lane="miss" data-view="home">
<header class="desk-head ops">
  <h1>Lane not registered</h1>
  <span class="desk-paper">PAPER</span>
</header>
<div class="lane-switch">{_lane_switch_html(LANE_GOLF)}</div>
<main>
  <p><code>{asked}</code> is not a registered lane. Registered: {html.escape(ids)}.</p>
</main>
</body>
</html>
"""


def _chip(label: str, value: str) -> str:
    return f'<span class="gk-chip"><b>{html.escape(label)}</b> {html.escape(str(value))}</span>'


def _bold_stars(text: str) -> str:
    out = html.escape(text)
    while "**" in out:
        out = out.replace("**", "<strong>", 1).replace("**", "</strong>", 1)
    return out


def session_blotter_15m() -> tuple[str, str]:
    from datetime import datetime

    from golf_offshoot.learning_lane_15m.watch import load_watch_status
    from golf_offshoot.localtime import format_eastern, now, to_eastern
    from golf_offshoot.operator_surface.this_window import factory_title, this_window_html

    watch = load_watch_status()
    running = bool(watch.get("running"))
    interval = float(watch.get("interval_s") or 90.0)
    at = str(watch.get("last_at") or watch.get("at") or "")
    stale = False
    if running:
        if not at:
            stale = True
        else:
            try:
                text = at[:-1] + "+00:00" if at.endswith("Z") else at
                stale = (now() - to_eastern(datetime.fromisoformat(text))).total_seconds() > max(
                    interval, 1.0
                ) * 2
            except ValueError:
                stale = True
    if stale:
        watch_label = "stale"
        watch_cls = "desk-watch-halt"
    elif running:
        watch_label = "on"
        watch_cls = "desk-watch-on"
    else:
        watch_label = "off"
        watch_cls = "desk-watch-off"
    summary = str(watch.get("last_summary") or "").strip()
    if summary:
        watch_label = f"{watch_label} · {summary}"
    last_stamp = format_eastern(at) if at else "—"
    bank = "—"
    pnl = "—"
    open_n = "—"
    closed_n = "—"
    try:
        from golf_offshoot.learning_lane_15m.paper import paper_session_counts

        counts = paper_session_counts()
        bank = f"{float(counts.get('bankroll') or 0):.2f}"
        pnl = f"{float(counts.get('pnl') or 0):+.2f}"
        open_n = str(int(counts.get("open") or 0))
        closed_n = str(int(counts.get("closed") or 0))
    except Exception:
        pass
    session = (
        '<div id="desk-session" class="desk-session">'
        f'<span class="desk-chip {watch_cls}"><b>Watch</b> {html.escape(watch_label)}</span>'
        + _chip("Clock", last_stamp)
        + _chip("Bankroll", bank)
        + _chip("P/L", pnl)
        + _chip("Open", open_n)
        + _chip("Closed", closed_n)
        + _chip("Halt", "no")
        + "</div>"
    )
    standing = _factory_standing_html()
    blotter = (
        '<div id="desk-blotter" class="desk-blotter">'
        + trial_glance_html()
        + this_window_html()
        + (
            f'<section class="panel" id="factory-home">'
            f"<h2>{html.escape(factory_title())}</h2>{standing}</section>"
        )
        + "</div>"
    )
    return session, blotter


_CARD_HEADING = re.compile(r"^##\s+(.+?)\s*$")
_TRIAL_GLANCE_SEE = "Not a verdict. Full card on Lab."


def _card_sections(text: str) -> dict[str, str]:
    found: dict[str, list[str]] = {}
    current: str | None = None
    for line in (text or "").splitlines():
        match = _CARD_HEADING.match(line.strip())
        if match:
            current = match.group(1).strip().lower()
            found[current] = []
            continue
        if current is not None:
            found[current].append(line)
    return {key: "\n".join(body).strip() for key, body in found.items()}


def _first_quote(section: str) -> str:
    for raw in (section or "").splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.lower().startswith("source:"):
            continue
        if line.startswith(">"):
            line = line.lstrip("> ").strip()
        line = line.replace("`", "").strip()
        if line:
            return line
    return ""


def _first_file_line(text: str) -> str:
    for raw in (text or "").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        return line.replace("`", "").strip()
    return ""


def _short_trial_quote(text: str) -> str:
    text = (text or "").replace("`", "").strip()
    if " — " in text:
        return text.split(" — ", 1)[0].strip()
    if len(text) > 88:
        return text[:85].rstrip() + "…"
    return text


def trial_glance_html() -> str:
    """One Home line from the generated card file. Does not write the card."""
    from golf_offshoot.learning_lane_15m.learning_card import (
        EMPTY_ON_TRIAL,
        MISSING_HUB_COPY,
        card_path,
    )

    def _p(line: str) -> str:
        return (
            '<p id="trial-glance" class="trial-glance">'
            f"{html.escape(line)} "
            f'<span class="help">{html.escape(_TRIAL_GLANCE_SEE)}</span>'
            "</p>"
        )

    try:
        path = card_path()
    except Exception:
        return _p(MISSING_HUB_COPY)
    if not path.is_file():
        return _p(MISSING_HUB_COPY)
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return _p(MISSING_HUB_COPY)
    sections = _card_sections(text)
    on_trial = _first_quote(sections.get("on trial", ""))
    if on_trial == EMPTY_ON_TRIAL:
        return _p(EMPTY_ON_TRIAL)
    bits: list[str] = []
    if on_trial:
        bits.append(f"On trial {_short_trial_quote(on_trial)}")
    else:
        fallback = _first_file_line(text)
        if fallback == EMPTY_ON_TRIAL:
            return _p(EMPTY_ON_TRIAL)
        if fallback:
            bits.append(fallback)
    implemented = _first_quote(sections.get("implemented?", ""))
    if implemented:
        bits.append(f"Implemented? {implemented}")
    verdict = _first_quote(sections.get("verdict", ""))
    if verdict:
        bits.append(f"Verdict {verdict}")
    if not bits:
        bits.append(MISSING_HUB_COPY)
    return _p(" · ".join(bits))


def _factory_standing_html() -> str:
    try:
        from golf_offshoot.learning_lane_15m.standing import cached_factory_standing

        standing = cached_factory_standing()
    except Exception as exc:
        return f'<p class="missing">Factory standing unavailable ({html.escape(str(exc))}).</p>'
    keep = f'<p class="loud">{html.escape(standing.not_a_keep)}</p>' if standing.not_a_keep else ""
    return (
        '<div class="standing">'
        '<details class="gk-fold">'
        "<summary>What it is / where it stands</summary>"
        "<h3>What it is</h3>"
        f"<p>{_bold_stars(standing.what_it_is)}</p>"
        "<h3>Where it stands</h3>"
        f"<p>{_bold_stars(standing.where_it_stands)}</p>"
        "</details>"
        "<h3>Last thing that happened</h3>"
        f"<p>{_bold_stars(standing.last_happened)}</p>"
        "<h3>This book's money</h3>"
        f"<p>{html.escape(standing.this_book)}</p>"
        f"{keep}"
        "</div>"
    )


def session_blotter_golf() -> tuple[str, str]:
    from golf_offshoot.golf_kalshi.hub import blotter_html, collect_board, session_html

    board = collect_board()
    return session_html(board), blotter_html(board)


def watch_payload(*, generation: int, kind: str, lane: str) -> dict[str, Any]:
    spec = lookup_lane(lane)
    if spec is None:
        session, blotter = "", ""
        resolved = str(lane or "")
    elif spec.id == LANE_15M:
        session, blotter = session_blotter_15m()
        resolved = LANE_15M
    else:
        session, blotter = session_blotter_golf()
        resolved = LANE_GOLF
    return {
        "generation": int(generation or 0),
        "kind": str(kind or "ok"),
        "lane": resolved,
        "hash": fragment_hash(session, blotter),
        "session_html": session,
        "blotter_html": blotter,
    }
