"""Thin HTTP hub. Query/form field is only `lane=golf|learning_lane_15m`."""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from golf_offshoot.operator_surface.client_write import write_http_body
from golf_offshoot.operator_surface.hub import render_hub
from golf_offshoot.operator_surface.lanes import DEFAULT_LANE, SELECTOR_FIELD, parse_lane


class HubHandler(BaseHTTPRequestHandler):
    def _lane(self) -> str:
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)
        raw = (qs.get(SELECTOR_FIELD) or [DEFAULT_LANE])[0]
        return parse_lane(raw)

    def do_GET(self) -> None:  # noqa: N802
        body = render_hub(self._lane()).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        write_http_body(self.wfile, body)

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length).decode("utf-8") if length else ""
        form = parse_qs(raw)
        lane = parse_lane((form.get(SELECTOR_FIELD) or [DEFAULT_LANE])[0])
        self.send_response(303)
        self.send_header("Location", f"/?{SELECTOR_FIELD}={lane}")
        self.end_headers()

    def log_message(self, fmt: str, *args) -> None:
        return


def serve_hub(*, host: str = "127.0.0.1", port: int = 8765) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), HubHandler)
