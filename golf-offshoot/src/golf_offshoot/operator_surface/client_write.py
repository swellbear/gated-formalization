"""Write an HTTP body without dumping a traceback when the browser hangs up."""

from __future__ import annotations

import logging
import sys
from typing import Any

_LOG = logging.getLogger("golf_offshoot.operator_surface")

#: Windows: 10053 software abort, 10054 connection reset by peer.
_WIN_ABORT = frozenset({10053, 10054})
_ABORT = (ConnectionAbortedError, BrokenPipeError, ConnectionResetError)


def is_client_abort(exc: BaseException) -> bool:
    if isinstance(exc, _ABORT):
        return True
    if isinstance(exc, OSError) and getattr(exc, "winerror", None) in _WIN_ABORT:
        return True
    return False


def write_http_body(wfile: Any, body: bytes, *, log: Any | None = None) -> None:
    """``wfile.write`` that treats a mid-response browser abort as a quiet fact.

    A 200 that then hits WinError 10053 is not PaperWatch dying and not a
    second-hub event. One line; no traceback.
    """
    try:
        wfile.write(body)
    except Exception as exc:  # noqa: BLE001 — classified immediately
        if not is_client_abort(exc):
            raise
        msg = f"hub client abort during body write ({type(exc).__name__}); not a hub crash"
        writer = log if log is not None else _LOG.warning
        try:
            writer(msg)
        except Exception:  # noqa: BLE001 — logging must not take the hub down
            try:
                sys.stderr.write(f"hub: {msg}\n")
            except OSError:
                pass
