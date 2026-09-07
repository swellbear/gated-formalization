"""Local Phase 1 operator shell. Stdlib HTTP + text dump. No new dependencies."""

from __future__ import annotations

import argparse
import html
import json
import sys
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from golf_offshoot.operator_surface.artifacts import HonestyBundle, load_honesty
from golf_offshoot.operator_surface.modes import CASH_BADGE, NOT_ARMED, PAPER_ONLY, build_mode_walls
from golf_offshoot.operator_surface.notify import notify_run_complete
from golf_offshoot.operator_surface.paths import ResolvedRoots, resolve_roots, safe_existing_file
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
from golf_offshoot.operator_surface.viz import VizWall, load_viz_wall, viz_file_for_serve

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765


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


def render_html(surface: dict) -> str:
    walls = surface["walls"]
    honesty: HonestyBundle = surface["honesty"]
    viz: VizWall = surface["viz"]
    last: RunRecord | None = surface.get("last_run")
    event = html.escape(str(surface.get("event_id") or ""))
    wall_class = "mock" if walls.is_mock else "ops"
    badges = "".join(f"<span class='badge'>{html.escape(b)}</span>" for b in walls.badges)
    wall_lines = "".join(f"<div>{html.escape(line)}</div>" for line in walls.lines)
    viz_blocks = []
    for slot in viz.slots:
        img = ""
        if slot.path is not None:
            cache = int(slot.mtime or 0)
            img = (
                f"<img src='/viz/{html.escape(slot.slot_id)}.png?t={cache}' "
                f"alt='{html.escape(slot.title)}' width='1200'/>"
            )
        else:
            img = f"<p class='missing'>{html.escape(slot.note)}</p>"
        viz_blocks.append(
            "<section class='viz'>"
            f"<h3>{html.escape(slot.title)}</h3>"
            f"<p class='sub'>{html.escape(slot.subline)}</p>"
            f"<p class='badges'>{html.escape(' · '.join(slot.badges))}</p>"
            f"{img}</section>"
        )
    last_html = html.escape(format_run_record(last)) if last else "no operator run this session"
    paper_html = ""
    if last is not None and last.paper:
        paper_html = (
            "<h2>Paper observation (not trading)</h2>"
            f"<p>Paper bankroll auto-apply is {html.escape(PAPER_ONLY)} — not trading armed. "
            f"{html.escape(NOT_ARMED)}. {html.escape(CASH_BADGE)}.</p>"
            f"<pre>{html.escape(last.paper)}</pre>"
        )
    ranked = html.escape(honesty.ranked.text)
    leftover = html.escape(honesty.leftover.text)
    inventory = html.escape(honesty.inventory.text)
    shadow = html.escape(honesty.shadow.text)
    calib = html.escape(honesty.calibration.text)
    html_link = ""
    if honesty.ranked.html_path:
        html_link = (
            f"<p>HTML: <a href='/export/html'>{html.escape(str(honesty.ranked.html_path))}</a></p>"
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
 .badge {{ display: inline-block; margin: 4px 6px 0 0; padding: 3px 8px; background: #0e1f29; color: #f2e27a; font-size: 12px; }}
 header.mock .badge {{ background: #3b0000; color: #ffd2d2; }}
 main {{ padding: 16px 20px 48px; max-width: 1200px; }}
 form.row {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: end; margin: 12px 0 20px; }}
 label {{ font-size: 13px; display: block; }}
 input[type=text] {{ padding: 6px 8px; min-width: 180px; }}
 button {{ padding: 8px 12px; background: #1f3b4d; color: #fff; border: 0; cursor: pointer; }}
 button.warn {{ background: #7a0c0c; }}
 pre {{ white-space: pre-wrap; background: #fff; border: 1px solid #c9c2b2; padding: 12px; }}
 .missing {{ background: #f8e0a0; padding: 10px; border: 1px solid #c9a227; }}
 .cash {{ position: sticky; bottom: 0; background: #111; color: #f2e27a; padding: 8px 16px; font-weight: 700; }}
 .viz {{ margin: 16px 0 28px; padding: 12px; background: #fff; border: 1px solid #c9c2b2; }}
 .viz img {{ display: block; width: 100%; max-width: 100%; height: auto; border: 1px solid #c9c2b2; background: #111; }}
 h2 {{ margin-top: 28px; }}
</style>
</head>
<body>
<header class="{wall_class}">
  <h1>{html.escape(walls.title)}</h1>
  {wall_lines}
  <div>{badges}</div>
</header>
<main>
  <form class="row" method="post" action="/run">
    <label>ESPN event id
      <input name="event" type="text" value="{event}" placeholder="401811963"/>
    </label>
    <button name="action" value="ingest">ingest</button>
    <button name="action" value="live">live</button>
    <button name="action" value="shadow">shadow</button>
    <button name="action" value="loop">ingest → live → shadow</button>
    <button name="action" value="refresh">reload artifacts</button>
  </form>
  <p>Phase 1 observation only. Trading {html.escape('NOT ARMED')}. Paper bankroll auto-apply on live/loop is {html.escape('PAPER OBSERVATION ONLY')} — not trading armed. No deposit / withdraw / transfer / one-tap bet / cash-out controls.</p>
  <h2>Last run</h2>
  <pre>{last_html}</pre>
  {paper_html}
  <h2>Latest real LIVE ranked table</h2>
  <p>{html.escape(honesty.ranked.banner)}</p>
  {html_link}
  <pre>{ranked}</pre>
  <h2>Leftover callout (display only)</h2>
  <pre>{leftover}</pre>
  <h2>Source inventory</h2>
  <pre>{inventory}</pre>
  <h2>Shadow journal</h2>
  <pre>{shadow}</pre>
  <h2>Calibration</h2>
  <pre>{calib}</pre>
  <h2>Illustrator viz-wall (Ill 1 / Ill 2 / WC1 dated record)</h2>
  <p>Read-only PNGs when present. Missing charts stay {html.escape('not yet available')} — never invented. Phone is notify-first; this hub is local.</p>
  {''.join(viz_blocks)}
</main>
<div class="cash">{html.escape(CASH_BADGE)}</div>
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


def serve(
    *,
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
    event_id: str | None = None,
    open_browser: bool = False,
    artifact_root: Path | None = None,
    viz_root: Path | None = None,
) -> int:
    state = {
        "event_id": event_id or "",
        "artifact_root": artifact_root,
        "viz_root": viz_root,
        "odds_book": "auto",
        "surface": build_surface(event_id=event_id, artifact_root=artifact_root, viz_root=viz_root),
    }
    httpd = ThreadingHTTPServer((host, port), OperatorHandler)
    httpd.surface_state = state  # type: ignore[attr-defined]
    url = f"http://{host}:{port}/"
    print(build_mode_walls(live_data=True).render_text())
    print(f"operator shell {url}")
    print(f"PHASE 1 OBSERVATION. Trading {NOT_ARMED}. {PAPER_ONLY}. {CASH_BADGE}")
    if open_browser:
        webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("shell stopped")
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
    parser.add_argument("--no-browser", action="store_true")
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
