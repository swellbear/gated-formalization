"""Load options-offshoot/.env without exporting the key."""

from __future__ import annotations

import os
from pathlib import Path


def package_root() -> Path:
    return Path(__file__).resolve().parents[3]


def load_local_env() -> None:
    path = package_root() / ".env"
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        raw = line.strip()
        if not raw or raw.startswith("#") or "=" not in raw:
            continue
        key, _, val = raw.partition("=")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = val


def polygon_api_key() -> str:
    """Massive (formerly Polygon) key. Same vendor. Never print it."""
    load_local_env()
    return (
        os.environ.get("MASSIVE_API_KEY", "").strip()
        or os.environ.get("POLYGON_API_KEY", "").strip()
        or os.environ.get("POLYGON_KEY", "").strip()
    )


def quotes_mode() -> str:
    load_local_env()
    raw = os.environ.get("OPTIONS_QUOTES", "polygon").strip().lower()
    if raw in {"ibkr", "interactive_brokers", "tws"}:
        return "ibkr"
    return "polygon"


def feed_pause_s(default: float) -> float:
    load_local_env()
    raw = os.environ.get("OPTIONS_FEED_PAUSE", "").strip()
    if raw == "":
        return default
    try:
        return max(0.0, float(raw))
    except ValueError:
        return default
