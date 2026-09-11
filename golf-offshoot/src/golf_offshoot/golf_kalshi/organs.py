"""Idle Golf Farm and Honer shells. Empty schema only. Not 15m. No crew_tick."""

from __future__ import annotations

import html
import json
from typing import Any

from golf_offshoot.golf_kalshi.paths import (
    assert_golf_kalshi_path,
    farm_path,
    honer_status_path,
)

LANE = "golf_kalshi"
IDLE_NOTE = "no golf tape yet — wait for paper settles"


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


def farm_panel_html() -> str:
    ensure_idle_organs()
    payload = _read(farm_path())
    note = str(payload.get("notes") or IDLE_NOTE)
    n = len([row for row in (payload.get("notebooks") or []) if isinstance(row, dict)])
    extra = f" {n} dated notebooks sit idle." if n else ""
    return (
        '<section class="panel gk-organ" id="golf-farm">'
        "<h2>Golf Farm</h2>"
        '<p class="help">Discovery notebooks for this gym later (sleeve mix, tour haircut, unmatched rate). '
        "Not live. Not hour-close. Not 2-to-1. Not coinflip. Lab chair for 15m farm stays on 15m.</p>"
        f'<p class="loud">Idle. {html.escape(note)}{extra}</p>'
        "</section>"
    )


def honer_panel_html() -> str:
    ensure_idle_organs()
    payload = _read(honer_status_path())
    note = str(payload.get("notes") or IDLE_NOTE)
    return (
        '<section class="panel gk-organ" id="golf-honer">'
        "<h2>Golf Honer</h2>"
        '<p class="help">Own sandbox. Does not consult 15m decide(). No combined bankroll. No Lineage A.</p>'
        f'<p class="loud">Idle. {html.escape(note)}</p>'
        "</section>"
    )
