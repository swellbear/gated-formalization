"""Always-on ARM hub watcher. Own PID. No bot in the hot path.

Start once → leaves running. Reads POLICY.json / state / pins from disk every
tick. Never regenerates policy. Never writes the learning-lane KILL file.
"""

from __future__ import annotations

import os
import time
from pathlib import Path

from golf_offshoot.arm_hub.loop import load_config, run_once
from golf_offshoot.arm_hub.paths import kill_path, latest_dir, pid_path


def kill_is_set(root: Path | None = None) -> bool:
    return kill_path(root).is_file()


def write_kill(root: Path | None = None) -> Path:
    """Write ARM hub KILL only. Does not touch learning_lane_15m."""
    path = kill_path(root)
    latest_dir(root)
    path.write_text("stop\n", encoding="utf-8")
    return path


def clear_kill(root: Path | None = None) -> None:
    path = kill_path(root)
    if path.is_file():
        path.unlink()


def _write_pid(root: Path | None) -> Path:
    path = pid_path(root)
    path.write_text(str(os.getpid()) + "\n", encoding="utf-8")
    return path


def _clear_pid(root: Path | None) -> None:
    path = pid_path(root)
    if path.is_file():
        path.unlink()


def run_watch(
    root: Path | None = None,
    *,
    interval_s: float | None = None,
    max_ticks: int | None = None,
    quotes_source: str | None = None,
    sleep: bool = True,
) -> int:
    """Loop until KILL (or max_ticks for tests). Deterministic Python only."""
    cfg = load_config(root)
    delay = float(interval_s if interval_s is not None else cfg.get("interval_s") or 30)
    _write_pid(root)
    ticks = 0
    try:
        while True:
            if kill_is_set(root):
                return 0
            run_once(root, quotes_source=quotes_source, rebuild_policy=False)
            ticks += 1
            if max_ticks is not None and ticks >= max_ticks:
                return 0
            if kill_is_set(root):
                return 0
            if sleep and delay > 0:
                time.sleep(delay)
    finally:
        _clear_pid(root)
