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
