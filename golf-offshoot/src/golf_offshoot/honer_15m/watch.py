"""Honer watch thread. Must not raise into the hub. Not PaperWatch."""

from __future__ import annotations

import json
import os
import threading
import time
from typing import Any

from golf_offshoot.honer_15m.loop import run_tick
from golf_offshoot.honer_15m.paths import assert_honer_path, watch_status_path
from golf_offshoot.localtime import now

DEFAULT_INTERVAL_S = 90.0
FIRST_SLEEP_S = 45.0
ENV_INTERVAL = "GOLF_OFFSHOOT_HONER_WATCH_S"


def honer_interval_s(override: float | None = None) -> float:
    if override is not None and override > 0:
        return float(override)
    raw = os.environ.get(ENV_INTERVAL) or ""
    try:
        parsed = float(raw)
    except ValueError:
        parsed = 0.0
    return parsed if parsed > 0 else DEFAULT_INTERVAL_S


def load_watch_status() -> dict[str, Any]:
    path = watch_status_path()
    if not path.is_file():
        return {"running": False, "cycles": 0, "lane": "honer_15m"}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"running": False, "cycles": 0, "lane": "honer_15m"}


def _write_status(payload: dict[str, Any]) -> None:
    path = watch_status_path()
    assert_honer_path(path)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


class HonerWatch:
    def __init__(self, *, interval_s: float | None = None, first_sleep_s: float = FIRST_SLEEP_S) -> None:
        self.interval_s = honer_interval_s(interval_s)
        self.first_sleep_s = float(first_sleep_s)
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self.cycles = 0
        self.last_error = ""
        self.last_summary = ""

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._run, name="honer-15m-watch", daemon=True)
        self._thread.start()
        self._persist(running=True)

    def stop_watch(self) -> None:
        self._stop.set()
        self._persist(running=False)

    def _persist(self, *, running: bool, error: str = "") -> None:
        _write_status(
            {
                "running": running,
                "cycles": self.cycles,
                "interval_s": self.interval_s,
                "last_error": error or self.last_error,
                "last_summary": self.last_summary,
                "lane": "honer_15m",
                "at": now().isoformat(),
            }
        )

    def _run(self) -> None:
        if self.first_sleep_s > 0:
            self._stop.wait(self.first_sleep_s)
        while not self._stop.is_set():
            try:
                out = run_tick()
                self.cycles += 1
                self.last_error = ""
                self.last_summary = (
                    f"theta={out.get('search_theta')} froze={out.get('froze')} "
                    f"markets={out.get('markets')}"
                )
                self._persist(running=True)
            except Exception as exc:  # noqa: BLE001 — never kill 8765
                self.last_error = str(exc)
                self.last_summary = "tick failed"
                try:
                    self._persist(running=True, error=str(exc))
                except Exception:
                    pass
            self._stop.wait(self.interval_s)


def run_watch_forever(*, interval_s: float | None = None, once: bool = False) -> int:
    if once:
        run_tick()
        return 0
    watch = HonerWatch(interval_s=interval_s)
    watch.start()
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        watch.stop_watch()
    return 0
