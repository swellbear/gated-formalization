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

from golf_offshoot.operator_surface.artifacts import HonestyBundle, load_honesty
from golf_offshoot.operator_surface.modes import CASH_BADGE, NOT_ARMED, PAPER_ONLY, build_mode_walls
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
    }


def render_text(surface: dict) -> str:
    walls = surface["walls"]
    honesty: HonestyBundle = surface["honesty"]
    viz: VizWall = surface["viz"]
    last: RunRecord | None = surface.get("last_run")
    lines = [
        walls.render_text(),
        "",
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
        slot_badges = "".join(f'<span class="badge">{html.escape(b)}</span>' for b in slot.badges)
        cards.append(
            f'<section class="viz" id="viz-slot-{html.escape(slot.slot_id)}">'
            f"<h3>{html.escape(slot.title)}</h3>"
            f"{plain_html}"
            f'<p class="sub">{html.escape(slot.subline)}</p>'
            f'<p class="badges">{slot_badges}</p>'
            f"{body}</section>"
        )
    trailer = ""
    if viz.manifest_error:
        trailer = (
            f'<p class="missing">Chart list rejected: {html.escape(viz.manifest_error)}. '
            "No chart was invented in its place.</p>"
        )
    return f'<div class="viz-wall" id="viz-wall">{"".join(cards)}</div>{trailer}'


def _viz_lightbox_html(viz: VizWall) -> str:
    """Enlarged-chart overlay. Omitted entirely when no chart exists to enlarge."""
    if not any(slot.path is not None for slot in viz.slots):
        return ""
    return (
        '<div class="lightbox" id="viz-lightbox" hidden role="dialog" aria-modal="true" '
        'aria-label="Enlarged chart">'
        '<div class="lightbox-bar">'
        '<span class="lightbox-title" id="viz-lightbox-title"></span>'
        f'<span class="badge">{html.escape(CASH_BADGE)}</span>'
        '<button type="button" class="lightbox-close" id="viz-lightbox-close">Close (Esc)</button>'
        "</div>"
        '<img id="viz-lightbox-img" src="" alt=""/>'
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


def _actions_html(event: str) -> str:
    buttons = []
    help_rows = []
    for value, label, blurb in ACTION_BUTTONS:
        css = ' class="soft"' if value == "refresh" else ""
        buttons.append(f'<button{css} name="action" value="{value}">{html.escape(label)}</button>')
        help_rows.append(f"<li><b>{html.escape(label)}</b> — {html.escape(blurb)}</li>")
    return (
        '<form class="row" method="post" action="/run">'
        "<label>Tournament id (ESPN)"
        f'<input name="event" type="text" value="{event}" placeholder="401811963"/>'
        "</label>"
        f"{''.join(buttons)}"
        "</form>"
        f'<ul class="help">{"".join(help_rows)}</ul>'
    )


def render_html(surface: dict) -> str:
    walls = surface["walls"]
    honesty: HonestyBundle = surface["honesty"]
    viz: VizWall = surface["viz"]
    last: RunRecord | None = surface.get("last_run")
    event = html.escape(str(surface.get("event_id") or ""))
    wall_class = "mock" if walls.is_mock else "ops"
    badges = "".join(f'<span class="badge">{html.escape(b)}</span>' for b in walls.badges)
    wall_lines = "".join(f"<div>{html.escape(line)}</div>" for line in walls.lines)
    viz_wall = _viz_wall_html(viz)
    viz_lightbox = _viz_lightbox_html(viz)
    settle_banner = _settle_banner_html(honesty)
    actions = _actions_html(event)
    last_html = html.escape(format_run_record(last)) if last else "no operator run this session"
    paper_html = ""
    if last is not None and last.paper:
        paper_html = (
            '<section class="panel">'
            "<h2>Paper observation (not trading)</h2>"
            '<p class="help">A pretend bankroll kept so the model can be scored later. '
            "No ticket is placed, no money moves, and nothing here needs approval.</p>"
            f'<p class="loud">{html.escape(PAPER_ONLY)} · Trading {html.escape(NOT_ARMED)} · '
            f"{html.escape(CASH_BADGE)}</p>"
            '<p class="help">Paper bankroll auto-apply is paper observation only — it is '
            "not trading armed. No deposit, withdraw, transfer, cash-out, or one-tap bet control exists here.</p>"
            f"<pre>{html.escape(last.paper)}</pre>"
            "</section>"
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
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>golf-offshoot operator shell</title>
<style>
 body {{ font-family: Segoe UI, Helvetica, Arial, sans-serif; margin: 0; background: #f4f1ea; color: #1b1b1b; }}
 header.ops {{ background: #1f3b4d; color: #fff; padding: 16px 20px; }}
 header.mock {{ background: #7a0c0c; color: #fff; padding: 16px 20px; }}
 header h1 {{ margin: 0 0 8px; font-size: 26px; letter-spacing: 1px; }}
 header div {{ font-size: 14px; }}
 .badge {{ display: inline-block; margin: 4px 6px 0 0; padding: 3px 8px; background: #0e1f29; color: #f2e27a; font-size: 12px; font-weight: 700; }}
 header.mock .badge {{ background: #3b0000; color: #ffd2d2; }}
 main {{ padding: 0 20px 56px; max-width: 1100px; margin: 0 auto; }}
 form.row {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: end; margin: 4px 0 10px; }}
 label {{ font-size: 13px; display: flex; flex-direction: column; gap: 4px; }}
 input[type=text] {{ padding: 6px 8px; min-width: 180px; }}
 button {{ padding: 8px 12px; background: #1f3b4d; color: #fff; border: 0; cursor: pointer; font-size: 14px; }}
 button.soft {{ background: #55606b; }}
 button.warn {{ background: #7a0c0c; }}
 pre {{ white-space: pre-wrap; background: #fff; border: 1px solid #c9c2b2; padding: 12px; font-size: 13px; }}
 .missing {{ background: #f8e0a0; padding: 10px; border: 1px solid #c9a227; }}
 .cash {{ position: sticky; bottom: 0; background: #111; color: #f2e27a; padding: 8px 16px; font-weight: 700; }}
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
 .viz .sub {{ font-size: 12px; color: #4a4a4a; margin: 0 0 6px; }}
 .viz .badges {{ margin: 0 0 8px; }}
 .viz img {{ display: block; width: 100%; max-width: 100%; height: auto; border: 1px solid #c9c2b2; background: #111; }}
 .viz a.zoom {{ display: block; cursor: zoom-in; color: inherit; text-decoration: none; }}
 .viz a.zoom:focus-visible {{ outline: 3px solid #1f3b4d; outline-offset: 2px; }}
 .viz .zoom-hint {{ display: block; margin-top: 6px; font-size: 12px; color: #4a4a4a; }}
 .viz a.zoom:hover .zoom-hint, .viz a.zoom:focus .zoom-hint {{ color: #1f3b4d; text-decoration: underline; }}
 .lightbox {{ position: fixed; top: 0; right: 0; bottom: 0; left: 0; z-index: 100; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 10px; padding: 14px; background: rgba(12, 14, 16, 0.94); cursor: zoom-out; }}
 .lightbox[hidden] {{ display: none; }}
 .lightbox-bar {{ display: flex; flex-wrap: wrap; gap: 12px; align-items: center; justify-content: space-between; width: 100%; max-width: 1400px; color: #f4f1ea; font-size: 14px; }}
 .lightbox-title {{ font-weight: 700; }}
 .lightbox-close {{ background: #55606b; }}
 .lightbox img {{ max-width: 98vw; max-height: 86vh; width: auto; height: auto; border: 1px solid #c9c2b2; background: #111; }}
 body.viz-zoomed {{ overflow: hidden; }}
</style>
</head>
<body>
<header class="{wall_class}">
  <h1>{html.escape(walls.title)}</h1>
  {wall_lines}
  <div>{badges}</div>
</header>
{settle_banner}
<main>
  <section class="panel">
    <h2>Charts first — read-only chart wall</h2>
    <p class="help">These charts are what to look at before any table. Illustrator owns them; the hub only
    shows the files that exist. A missing chart stays {html.escape('not yet available')} and is never invented,
    and no edge badge is ever added. Phone alerts are notify-first; this hub stays local.</p>
    {viz_wall}
  </section>
  <section class="panel">
    <h2>What you can do here</h2>
    <p class="help">Five buttons, all read-and-recompute. Phase 1 observation only. Trading is
    {html.escape(NOT_ARMED)}. Paper bankroll auto-apply on live and on all-three is
    {html.escape(PAPER_ONLY)} — not trading armed. There is no deposit, withdraw, transfer,
    cash-out, or one-tap bet control on this page.</p>
    {actions}
  </section>
  <section class="panel">
    <h2>What the last run did</h2>
    <pre>{last_html}</pre>
  </section>
  {paper_html}
  <section class="panel">
    <h2>Ranked table — latest real live run</h2>
    <p class="loud">{html.escape(honesty.ranked.banner)}</p>
    {html_link}
    <pre>{ranked}</pre>
  </section>
  <section class="panel">
    <h2>Still unmeasured (display only)</h2>
    <p class="help">Things the model cannot see yet. Listed so they are not quietly folded into a rating.</p>
    <pre>{leftover}</pre>
  </section>
  <section class="panel">
    <h2>Where the numbers came from</h2>
    <pre>{inventory}</pre>
  </section>
  <section class="panel">
    <h2>Paper journal (shadow log)</h2>
    <p class="help">A written log of past paper advises and whether each one has an official result yet.
    It is not a bankroll and not settled cash.</p>
    <pre>{shadow}</pre>
  </section>
  <section class="panel">
    <h2>Calibration check</h2>
    <p class="help">Re-fitted weights are stored, not used, while the recommendation stays keep_expert.
    Edge is not established.</p>
    <pre>{calib}</pre>
  </section>
</main>
<div class="cash">{html.escape(CASH_BADGE)}</div>
{viz_lightbox}
<script>
(function(){{
  var box = document.getElementById('viz-lightbox');
  if (!box) return;
  var shown = document.getElementById('viz-lightbox-img');
  var caption = document.getElementById('viz-lightbox-title');
  function openBox(href, title){{
    shown.setAttribute('src', href);
    shown.setAttribute('alt', title);
    caption.textContent = title;
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
    if (!box.hidden) {{ closeBox(); return; }}
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
(function(){{
  var gen = null;
  function tick(){{
    fetch('/api/watch', {{cache:'no-store'}}).then(function(r){{return r.json();}}).then(function(s){{
      if (gen === null) {{ gen = s.generation; return; }}
      if (s.generation !== gen) location.reload();
    }}).catch(function(){{}});
  }}
  setInterval(tick, 3000);
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
            )
        self._state()["event_id"] = event
        self._state()["surface"] = build_surface(
            event_id=event or None,
            artifact_root=self._state()["artifact_root"],
            viz_root=self._state()["viz_root"],
            last_run=last,
        )
        self.send_response(303)
        self.send_header("Location", "/")
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
    """Open the hub in the default browser. Windows prefers os.startfile."""
    if sys.platform == "win32":
        startfile = getattr(os, "startfile", None)
        if callable(startfile):
            try:
                startfile(url)
                return True
            except OSError:
                pass
    try:
        return bool(webbrowser.open(url, new=0, autoraise=True))
    except Exception:
        return False


def maybe_open_hub_browser(url: str, *, enabled: bool) -> bool:
    if not enabled:
        return False
    print(f"Opening hub in your default browser: {url}")
    print("This console keeps the hub running — it is not the hub UI.")
    return open_hub_browser(url)


def rebuild_surface(state: dict, *, last_run: RunRecord | None | object = ...) -> None:
    keep = state["surface"].get("last_run") if last_run is ... else last_run
    state["surface"] = build_surface(
        event_id=state.get("event_id") or None,
        artifact_root=state.get("artifact_root"),
        viz_root=state.get("viz_root"),
        last_run=keep,
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
) -> int:
    if not is_hub_child():
        cmd = hub_child_command(
            host=host,
            port=port,
            event_id=event_id,
            open_browser=open_browser,
            artifact_root=artifact_root,
            viz_root=viz_root,
        )
        return supervise_hub_child(cmd)
    return run_http_server(
        host=host,
        port=port,
        event_id=event_id,
        open_browser=open_browser,
        artifact_root=artifact_root,
        viz_root=viz_root,
    )


def run_http_server(
    *,
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
    event_id: str | None = None,
    open_browser: bool = True,
    artifact_root: Path | None = None,
    viz_root: Path | None = None,
) -> int:
    state = {
        "event_id": event_id or "",
        "artifact_root": artifact_root,
        "viz_root": viz_root,
        "odds_book": "auto",
        "generation": 0,
        "reload_kind": "ok",
        "surface": build_surface(event_id=event_id, artifact_root=artifact_root, viz_root=viz_root),
    }
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
    args = parser.parse_args(argv)
    artifact = Path(args.artifact_root) if args.artifact_root else None
    viz = Path(args.viz_root) if args.viz_root else None
    event = args.event or None
    if args.install_desktop_shortcut:
        from golf_offshoot.operator_surface.desktop import SHORTCUT_STEM, write_desktop_launcher

        desktop = Path.home() / "Desktop"
        path = write_desktop_launcher(desktop=desktop)
        print(f"wrote Desktop launcher: {path}")
        print(f"Windows .lnk installer: scripts/windows/Install-Desktop-Shortcut.bat")
        print(f"{SHORTCUT_STEM}: PHASE 1 OBSERVATION. Trading NOT ARMED. {CASH_BADGE}")
        return 0
    if args.dump:
        print(render_text(build_surface(event_id=event, artifact_root=artifact, viz_root=viz)))
        return 0
    return serve(
        host=args.host,
        port=args.port,
        event_id=event,
        open_browser=not args.no_browser,
        artifact_root=artifact,
        viz_root=viz,
    )


if __name__ == "__main__":
    sys.exit(main())
