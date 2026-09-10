"""Desktop finish notify for 15m paper settles. Reuses golf ntfy; 15m paths only."""

from __future__ import annotations

import json
from pathlib import Path

from golf_offshoot.learning_lane_15m.paths import assert_not_golf_path, paper_dir_15m
from golf_offshoot.learning_lane_15m.settle import SETTLE_SETTLED, SettleJoinRow
from golf_offshoot.strategy.watch import WatchConfigError, publish_ntfy


def notify_state_path() -> Path:
    path = paper_dir_15m() / "watch_learning_lane_15m.json"
    assert_not_golf_path(path)
    return path


def _load_seen() -> set[str]:
    path = notify_state_path()
    if not path.is_file():
        return set()
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return set()
    rows = raw.get("seen") if isinstance(raw, dict) else None
    return {str(x) for x in rows} if isinstance(rows, list) else set()


def _save_seen(seen: set[str]) -> None:
    path = notify_state_path()
    path.write_text(json.dumps({"seen": sorted(seen)}, indent=2), encoding="utf-8")


def notify_settlements(
    rows: list[SettleJoinRow],
    *,
    dry_run: bool = False,
) -> str | None:
    """Ping ntfy when a 15m paper window officially settles. Fail open if unconfigured."""
    fresh = [
        r
        for r in rows
        if r.settle_status == SETTLE_SETTLED and r.won is not None
    ]
    if not fresh:
        return None
    seen = _load_seen()
    new_rows = [r for r in fresh if r.ticker not in seen]
    if not new_rows:
        return None
    body = "\n".join(
        [
            "LEARNING LANE 15m paper settle",
            "PHASE 1 OBSERVATION. Trading NOT ARMED. PAPER OBSERVATION ONLY.",
            *[
                f"{r.ticker} result={r.kalshi_result} won={r.won} pnl={r.pnl}"
                for r in new_rows
            ],
            "Mock paper. Not live cash. Not a golf ping.",
        ]
    )
    try:
        url = publish_ntfy(
            body,
            title="LEARNING LANE 15m settle (paper)",
            priority="default",
            dry_run=dry_run,
        )
    except WatchConfigError:
        return None
    seen.update(r.ticker for r in new_rows)
    _save_seen(seen)
    return url


HUB_LISTEN = ("127.0.0.1", 8765)


def ops_alert_state_path(*, latest_dir: Path | None = None) -> Path:
    from golf_offshoot.learning_lane_15m.paths import latest_dir_15m

    dest = (latest_dir or latest_dir_15m()) / "ops_alerts.json"
    assert_not_golf_path(dest)
    return dest


def _load_ops_state(*, latest_dir: Path | None = None) -> dict:
    path = ops_alert_state_path(latest_dir=latest_dir)
    if not path.is_file():
        return {"hub_down": False, "gaps": []}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"hub_down": False, "gaps": []}
    return raw if isinstance(raw, dict) else {"hub_down": False, "gaps": []}


def _save_ops_state(state: dict, *, latest_dir: Path | None = None) -> None:
    path = ops_alert_state_path(latest_dir=latest_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def hub_port_open(host: str = HUB_LISTEN[0], port: int = HUB_LISTEN[1]) -> bool:
    import socket

    try:
        with socket.create_connection((host, port), timeout=0.4):
            return True
    except OSError:
        return False


def _publish_ops(body: str, *, title: str, dry_run: bool) -> str | None:
    if dry_run:
        return "dry-run"
    try:
        return publish_ntfy(body, title=title, priority="high", dry_run=False)
    except WatchConfigError:
        return None


def notify_ops_alerts(
    *,
    invariants: dict | None = None,
    wake: dict | None = None,
    check_port: bool = True,
    dry_run: bool = False,
    latest_dir: Path | None = None,
    port_open: bool | None = None,
) -> dict:
    """Hub-down and first window_sequence_gap. Fail open if NTFY unset. Deduped.

    Does not backfill missing windows. One ping on the down transition, one ping
    per new gap ticker.
    """
    state = _load_ops_state(latest_dir=latest_dir)
    sent: list[str] = []
    collecting_fail = "watch_is_collecting" in list((invariants or {}).get("failing") or [])
    listening = hub_port_open() if port_open is None and check_port else (
        True if port_open is None else bool(port_open)
    )
    hub_down = bool(collecting_fail or (check_port and not listening))
    was_down = bool(state.get("hub_down"))
    if hub_down and not was_down:
        why = []
        if collecting_fail:
            why.append("watch_is_collecting FAIL")
        if check_port and not listening:
            why.append("127.0.0.1:8765 gone")
        url = _publish_ops(
            "\n".join(
                [
                    "LEARNING LANE 15m hub-down",
                    "PHASE 1 OBSERVATION. Trading NOT ARMED.",
                    *why,
                    "Do not start a second hub. Do not backfill.",
                ]
            ),
            title="LEARNING LANE 15m hub-down",
            dry_run=dry_run,
        )
        if url:
            sent.append("hub_down")
        state["hub_down"] = True
        state["hub_down_at"] = (invariants or {}).get("ran_at") or ""
        state["hub_down_why"] = why
    elif not hub_down and was_down:
        state["hub_down"] = False
        state["hub_down_why"] = []

    seen_gaps = {str(x) for x in (state.get("gaps") or [])}
    for event in (wake or {}).get("events") or []:
        if not isinstance(event, dict):
            continue
        if str(event.get("kind") or "") != "window_sequence_gap":
            continue
        ticker = str(event.get("ticker") or "")
        if not ticker or ticker in seen_gaps:
            continue
        url = _publish_ops(
            "\n".join(
                [
                    "LEARNING LANE 15m window_sequence_gap",
                    "PHASE 1 OBSERVATION. Trading NOT ARMED.",
                    ticker,
                    str(event.get("detail") or ""),
                    "Do not backfill.",
                ]
            ),
            title="LEARNING LANE 15m window gap",
            dry_run=dry_run,
        )
        if url:
            sent.append(f"gap:{ticker}")
        seen_gaps.add(ticker)
    state["gaps"] = sorted(seen_gaps)
    _save_ops_state(state, latest_dir=latest_dir)
    return {"sent": sent, "hub_down": hub_down, "gaps": sorted(seen_gaps)}
