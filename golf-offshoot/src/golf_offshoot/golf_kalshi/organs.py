"""Idle Golf Farm and Honer shells. Empty schema only. Not 15m. No crew_tick."""

from __future__ import annotations

import html
import json
from typing import Any

from golf_offshoot.golf_kalshi.paper import closed_tickets, load_ledger, open_tickets
from golf_offshoot.golf_kalshi.paths import (
    assert_golf_kalshi_path,
    farm_path,
    honer_status_path,
)
from golf_offshoot.golf_kalshi.watch import load_watch_status

LANE = "golf_kalshi"
FARM_IDLE = "No golf Farm notebooks."
HONER_IDLE = "Golf Honer is not consulting."
IDLE_NOTE = "No golf Farm notebooks. Paper tape lives on Home and Scoreboard."


def empty_farm() -> dict[str, Any]:
    return {
        "lane": LANE,
        "notebooks": [],
        "idle": True,
        "execution": False,
        "notes": IDLE_NOTE,
    }


def empty_honer() -> dict[str, Any]:
    return {
        "lane": LANE,
        "idle": True,
        "consults_15m": False,
        "consults_factory": False,
        "notes": IDLE_NOTE,
    }


def ensure_idle_organs() -> None:
    farm = farm_path()
    if not farm.is_file():
        assert_golf_kalshi_path(farm)
        farm.write_text(json.dumps(empty_farm(), indent=2) + "\n", encoding="utf-8")
    honer = honer_status_path()
    if not honer.is_file():
        assert_golf_kalshi_path(honer)
        honer.write_text(json.dumps(empty_honer(), indent=2) + "\n", encoding="utf-8")


def _read(path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _tape_line() -> str:
    led = load_ledger()
    n_open = len(open_tickets(led))
    n_closed = len(closed_tickets(led))
    watch = "on" if load_watch_status().get("running") else "off"
    if n_open or n_closed:
        return (
            f"Paper tape is on Home ({n_open} open) and Scoreboard ({n_closed} closed). "
            f"Watch {watch}."
        )
    return f"Home has no paper tickets yet. Watch {watch}."


def farm_panel_html() -> str:
    ensure_idle_organs()
    payload = _read(farm_path())
    n = len([row for row in (payload.get("notebooks") or []) if isinstance(row, dict)])
    extra = f" {n} dated notebooks sit idle." if n else ""
    return (
        '<section class="panel gk-organ" id="golf-farm">'
        "<h2>Golf Farm</h2>"
        f'<p class="loud">Idle. {html.escape(FARM_IDLE)} {html.escape(_tape_line())}{html.escape(extra)}</p>'
        "</section>"
    )


def honer_panel_html() -> str:
    ensure_idle_organs()
    return (
        '<section class="panel gk-organ" id="golf-honer">'
        "<h2>Golf Honer</h2>"
        f'<p class="loud">Idle. {html.escape(HONER_IDLE)} {html.escape(_tape_line())}</p>'
        "</section>"
    )
