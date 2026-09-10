"""Gitignored ``learning_wake.json`` read/write. No pydantic.

Cloud CoS often has no wake file. ``stamp_cos_closeout`` then returns None and
the committed desk ``last_cos_*`` table is the stamp.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from golf_offshoot.learning_lane_15m.paths import assert_not_golf_path, latest_dir_15m

WAKE_FILE = "learning_wake.json"


def wake_state_path() -> Path:
    path = latest_dir_15m() / WAKE_FILE
    assert_not_golf_path(path)
    return path


def load_wake_state() -> dict[str, Any] | None:
    path = wake_state_path()
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return payload if isinstance(payload, dict) else None


def save_wake_state(state: dict[str, Any]) -> Path:
    dest = wake_state_path()
    dest.parent.mkdir(parents=True, exist_ok=True)
    assert_not_golf_path(dest)
    dest.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    return dest
