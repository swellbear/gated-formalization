"""Golf Farm and Honer shells. Read the live golf tape. Empty notebooks until dated. Not 15m."""

from __future__ import annotations

import html
import json
from typing import Any

from golf_offshoot.golf_kalshi.paper import closed_tickets, load_ledger, open_tickets
from golf_offshoot.golf_kalshi.paths import (
    assert_golf_kalshi_path,
    farm_path,
    honer_status_path,
    last_tick_path,
)
from golf_offshoot.golf_kalshi.watch import load_watch_status

LANE = "golf_kalshi"
FARM_IDLE = "No golf Farm notebooks."
HONER_IDLE = "Golf Honer is not consulting."
IDLE_NOTE = "No golf Farm notebooks. Paper tape lives on Home and Scoreboard."


def _read(path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _write(path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    assert_golf_kalshi_path(path)
    path.write_text(json.dumps(payload, indent=2, default=str) + "\n", encoding="utf-8")


def tape_snapshot() -> dict[str, Any]:
    """Live golf ledger + last tick. Not 15m. Not an invented notebook."""
    led = load_ledger()
    tick = _read(last_tick_path())
    watch = load_watch_status()
    n_open = len(open_tickets(led))
    n_closed = len(closed_tickets(led))
    n_tickets = len([row for row in (led.get("tickets") or []) if isinstance(row, dict)])
    picked = tick.get("picked") if isinstance(tick.get("picked"), dict) else {}
    skip_reasons = tick.get("skip_reasons") if isinstance(tick.get("skip_reasons"), dict) else {}
    last_at = str(tick.get("at") or "")
    return {
        "n_tickets": n_tickets,
        "n_open": n_open,
        "n_closed": n_closed,
        "bankroll": led.get("bankroll"),
        "betting_pnl": led.get("betting_pnl"),
        "fees_paid": led.get("fees_paid"),
        "sleeves": led.get("sleeves") or {},
        "watch_running": bool(watch.get("running")),
        "last_tick_at": last_at,
        "last_tick_summary": str(tick.get("summary") or ""),
        "worthy": tick.get("worthy"),
        "picked": {
            "fast": int(picked.get("fast") or 0),
            "week": int(picked.get("week") or 0),
            "slow": int(picked.get("slow") or 0),
        },
        "skip_reasons": {str(key): int(val or 0) for key, val in skip_reasons.items()},
        "week_overweight": bool(tick.get("week_overweight")),
        "in_play": bool(tick.get("in_play")),
        "consulted_decide": bool(tick.get("consulted_decide")),
        "has_tape": bool(n_tickets or last_at or watch.get("running")),
    }


def _tape_line(tape: dict[str, Any] | None = None) -> str:
    snap = tape if tape is not None else tape_snapshot()
    n_open = int(snap.get("n_open") or 0)
    n_closed = int(snap.get("n_closed") or 0)
    watch = "on" if snap.get("watch_running") else "off"
    if n_open or n_closed:
        return (
            f"Paper tape is on Home ({n_open} open) and Scoreboard ({n_closed} closed). "
            f"Watch {watch}."
        )
    return f"Home has no paper tickets yet. Watch {watch}."


def _farm_notes(tape: dict[str, Any], notebooks: list[dict[str, Any]]) -> str:
    extra = f" {len(notebooks)} dated notebooks sit idle." if notebooks else ""
    return f"{FARM_IDLE} {_tape_line(tape)}{extra}"


def _honer_notes(tape: dict[str, Any]) -> str:
    return f"{HONER_IDLE} {_tape_line(tape)}"


def live_farm(*, existing: dict[str, Any] | None = None) -> dict[str, Any]:
    prev = existing if isinstance(existing, dict) else {}
    notebooks = [row for row in (prev.get("notebooks") or []) if isinstance(row, dict)]
    tape = tape_snapshot()
    return {
        "lane": LANE,
        "notebooks": notebooks,
        "idle": True,
        "execution": False,
        "notes": _farm_notes(tape, notebooks),
        "tape": tape,
    }


def live_honer() -> dict[str, Any]:
    tape = tape_snapshot()
    return {
        "lane": LANE,
        "idle": True,
        "consults_15m": False,
        "consults_factory": False,
        "notes": _honer_notes(tape),
        "tape": tape,
    }


def empty_farm() -> dict[str, Any]:
    return live_farm(existing={"notebooks": []})


def empty_honer() -> dict[str, Any]:
    return live_honer()


def refresh_organs() -> tuple[dict[str, Any], dict[str, Any]]:
    """Always rewrite farm/honer JSON from live ledger + last tick. Never 'no golf tape yet'."""
    farm = live_farm(existing=_read(farm_path()))
    honer = live_honer()
    _write(farm_path(), farm)
    _write(honer_status_path(), honer)
    return farm, honer


def ensure_idle_organs() -> None:
    refresh_organs()


def farm_panel_html() -> str:
    farm, _honer = refresh_organs()
    n = len(farm.get("notebooks") or [])
    extra = f" {n} dated notebooks sit idle." if n else ""
    return (
        '<section class="panel gk-organ book-golf" id="golf-farm" data-book="golf">'
        "<h2>Golf Farm</h2>"
        f'<p class="loud">Idle. {html.escape(FARM_IDLE)} {html.escape(_tape_line(farm.get("tape")))}{html.escape(extra)}</p>'
        "</section>"
    )


def honer_panel_html() -> str:
    _farm, honer = refresh_organs()
    return (
        '<section class="panel gk-organ book-honer" id="golf-honer" data-book="honer">'
        "<h2>Golf Honer</h2>"
        f'<p class="loud">Idle. {html.escape(HONER_IDLE)} {html.escape(_tape_line(honer.get("tape")))}</p>'
        "</section>"
    )
