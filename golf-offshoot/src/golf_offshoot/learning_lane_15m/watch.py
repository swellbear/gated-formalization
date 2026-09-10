"""Repeating 15m paper cycle. Founder does not click this.

Each tick is the crew cadence: researcher loop (ingest → paper autobet →
settle join) then Systems export (already inside run_loop). Trading NOT ARMED.
"""

from __future__ import annotations

import json
import os
import threading
from typing import Any, Callable

from golf_offshoot.learning_lane_15m.paths import (
    LANE_15M,
    PRIMARY_SERIES,
    assert_not_golf_path,
    latest_dir_15m,
)
from golf_offshoot.localtime import isoformat_now

DEFAULT_INTERVAL_S = 90.0
ENV_INTERVAL = "GOLF_OFFSHOOT_15M_WATCH_S"


def watch_interval_s(override: float | None = None) -> float:
    if override is not None and override > 0:
        return float(override)
    raw = os.environ.get(ENV_INTERVAL) or ""
    try:
        parsed = float(raw)
    except ValueError:
        parsed = 0.0
    return parsed if parsed > 0 else DEFAULT_INTERVAL_S


def watch_status_path():
    path = latest_dir_15m() / "watch.json"
    assert_not_golf_path(path)
    return path


def load_watch_status() -> dict[str, Any]:
    path = watch_status_path()
    if not path.is_file():
        return {"lane": LANE_15M, "running": False, "cycles": 0}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"lane": LANE_15M, "running": False, "cycles": 0}
    return payload if isinstance(payload, dict) else {"lane": LANE_15M, "running": False}


def write_watch_status(payload: dict[str, Any]) -> None:
    dest = watch_status_path()
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


class PaperWatch:
    """One background worker. Repeats the paper loop until stop()."""

    def __init__(
        self,
        *,
        interval_s: float | None = None,
        feed=None,
        on_cycle: Callable[[dict[str, Any]], None] | None = None,
    ) -> None:
        self.interval_s = watch_interval_s(interval_s)
        self.feed = feed
        self.on_cycle = on_cycle
        self.stop = threading.Event()
        self.lock = threading.Lock()
        self.thread: threading.Thread | None = None
        self.cycles = 0
        self.last_ok = True
        self.last_summary = ""
        self.last_error = ""
        self.last_at = ""
        self.last_wake_error = ""
        self.last_runner_error = ""
        self.last_hub_publish_error = ""
        self.last_invariants_error = ""
        self.last_fee_probe: dict[str, Any] = {}
        self.last_fee_probe_error = ""

    @property
    def running(self) -> bool:
        return self.thread is not None and self.thread.is_alive()

    def start(self) -> None:
        if self.running:
            return
        self.stop.clear()
        self.thread = threading.Thread(target=self._run, daemon=True, name="lane-15m-watch")
        self.thread.start()
        self._persist()

    def stop_watch(self) -> None:
        self.stop.set()
        self._persist()

    def status(self) -> dict[str, Any]:
        return {
            "lane": LANE_15M,
            "series": PRIMARY_SERIES,
            "running": self.running,
            "interval_s": self.interval_s,
            "cycles": self.cycles,
            "last_ok": self.last_ok,
            "last_summary": self.last_summary,
            "last_error": self.last_error,
            "last_at": self.last_at,
            "last_wake_error": self.last_wake_error,
            "last_runner_error": getattr(self, "last_runner_error", ""),
            "last_hub_publish_error": getattr(self, "last_hub_publish_error", ""),
            "last_invariants_error": getattr(self, "last_invariants_error", ""),
            "fee_probe": getattr(self, "last_fee_probe", None) or {},
            "last_fee_probe_error": getattr(self, "last_fee_probe_error", ""),
            "runner": "one clerical pass after each paper tick; survives this watch restart",
            # What this long-lived process actually loaded. A fresh reader
            # compares it to disk, which is the only way to see a loop that
            # kept serving an old ROLE_ORDER after a merge.
            "runtime": self._runtime_stamp(),
            "trading_armed": False,
            "note": (
                "Repeating paper observation. Founder does not start cycles. "
                "Official settle is Kalshi result only."
            ),
        }

    def _invariants_tick(self) -> dict[str, Any] | None:
        """Re-read the invariants once the runner has had its pass."""
        from golf_offshoot.learning_lane_15m.learn import refresh_invariants

        try:
            block = refresh_invariants(watch_status=self.status())
        except Exception as exc:  # noqa: BLE001 — never take the loop down
            self.last_invariants_error = str(exc)
            return None
        self.last_invariants_error = ""
        return block

    def _runtime_stamp(self) -> dict[str, Any]:
        try:
            from golf_offshoot.learning_lane_15m.invariants import runtime_stamp

            return runtime_stamp()
        except Exception as exc:  # noqa: BLE001 — never take the loop down
            return {"error": f"{type(exc).__name__}: {exc}"}

    def _persist(self) -> None:
        write_watch_status(self.status())

    def _learning_tick(self) -> dict[str, Any] | None:
        """Wake the crew half of the cadence. Names owed roles; serves none of them."""
        from golf_offshoot.learning_lane_15m.learn import record_learning_tick

        try:
            state = record_learning_tick(watch_status=self.status())
        except Exception as exc:
            # A wake failure is a wake failure. It never takes the paper loop down.
            self.last_wake_error = str(exc)
            return None
        self.last_wake_error = ""
        return state

    def _runner_tick(self) -> dict[str, Any] | None:
        """One clerical pass per paper tick. Survives a PaperWatch restart with this loop."""
        from golf_offshoot.learning_lane_15m.runner import run_once

        try:
            entry = run_once()
        except Exception as exc:
            self.last_runner_error = str(exc)
            return None
        self.last_runner_error = ""
        return entry

    def _hub_publish_tick(self) -> dict[str, Any] | None:
        """Gym-only material Pages allowlist. Fail-open. Never sibling-HEAD-to-master."""
        from golf_offshoot.learning_lane_15m.hub_publish import maybe_publish_hub

        try:
            return maybe_publish_hub()
        except Exception as exc:  # noqa: BLE001 — never take the paper loop down
            self.last_hub_publish_error = str(exc)
            return None

    def _run(self) -> None:
        self._cycle()
        while not self.stop.wait(max(5.0, self.interval_s)):
            self._cycle()
        self._persist()

    def _cycle(self) -> None:
        from golf_offshoot.learning_lane_15m.loop import format_loop_report, run_loop

        with self.lock:
            try:
                payload = run_loop(refresh=True, feed=self.feed)
            except Exception as exc:
                self.last_ok = False
                self.last_error = str(exc)
                self.last_summary = "watch cycle failed"
                self.last_at = isoformat_now()
                self._persist()
                return
            paper = payload.get("paper_autobet") or {}
            joined = payload.get("settle_join") or {}
            self.cycles += 1
            self.last_ok = True
            self.last_error = ""
            self.last_summary = (
                f"cycle={self.cycles} fills={paper.get('fills', 0)} "
                f"settled={joined.get('settled', 0)} pending={joined.get('pending', 0)}"
            )
            self.last_at = isoformat_now()
            payload["watch"] = self.status()
            payload["report"] = format_loop_report(payload)
            payload["fee"] = self._fee_tick(payload)
            self._persist()
            payload["learning_wake"] = self._learning_tick()
            payload["learning_runner"] = self._runner_tick()
            payload["leash"] = self._leash_tick()
            payload["hub_publish"] = self._hub_publish_tick()
            # The wake names roles, then the runner serves them. Invariants
            # read after both, or every settle reports a stale digest that the
            # same cycle already repaired — and a check that cries wolf on a
            # schedule is a check nobody reads.
            payload["learning_invariants"] = self._invariants_tick()
            payload["spread_profile"] = self._spread_tick(payload)
            payload["ops_alerts"] = self._ops_alerts_tick(payload)
            self._persist()
            if self.on_cycle is not None:
                self.on_cycle(payload)

    def _fee_tick(self, payload: dict[str, Any]) -> dict[str, Any] | None:
        """Gym fee pin + series M snapshot. Never takes the paper loop down."""
        from golf_offshoot.learning_lane_15m.evidence_bar import gym_fee_tick

        try:
            ingest = payload.get("ingest") or payload.get("live") or {}
            state = gym_fee_tick(ingest)
        except Exception as exc:  # noqa: BLE001 — a probe failure is a recorded fact
            self.last_fee_probe_error = str(exc)
            return None
        self.last_fee_probe_error = ""
        self.last_fee_probe = state
        return state

    def _leash_tick(self) -> dict[str, Any] | None:
        """Freeze photocopy + clerical executing score. Fail-open. Not arm."""
        from golf_offshoot.learning_lane_15m.leash import run_leash_tick

        try:
            return run_leash_tick()
        except Exception as exc:  # noqa: BLE001 — never take the paper loop down
            self.last_leash_error = str(exc)
            return None

    def _spread_tick(self, payload: dict[str, Any]) -> dict[str, Any] | None:
        """Append live bid/ask samples. Never takes the paper loop down."""
        from golf_offshoot.learning_lane_15m.spread_profile import record_live_quotes

        try:
            ingest = payload.get("ingest") or payload.get("live") or {}
            return record_live_quotes(ingest.get("markets") or [])
        except Exception as exc:  # noqa: BLE001 — a quote miss is not a hub crash
            self.last_spread_error = str(exc)
            return None

    def _ops_alerts_tick(self, payload: dict[str, Any]) -> dict[str, Any] | None:
        """Hub-down and first gap. Fail open. Never takes the paper loop down."""
        from golf_offshoot.learning_lane_15m.notify import notify_ops_alerts

        try:
            return notify_ops_alerts(
                invariants=payload.get("learning_invariants") or {},
                wake=payload.get("learning_wake") or {},
            )
        except Exception as exc:  # noqa: BLE001 — ntfy must not take the loop down
            self.last_ops_alert_error = str(exc)
            return None


def run_watch_forever(*, interval_s: float | None = None, feed=None) -> int:
    """CLI: keep the paper loop running until Ctrl+C. Founder does not babysit."""
    from golf_offshoot.learning_lane_15m.learn import format_wake_line

    def _on_cycle(payload: dict[str, Any]) -> None:
        print(format_wake_line(payload.get("learning_wake")))

    watch = PaperWatch(interval_s=interval_s, feed=feed, on_cycle=_on_cycle)
    watch.start()
    print(
        f"learning_lane_15m watch on. interval={watch.interval_s}s "
        f"series={PRIMARY_SERIES} trading_armed=false"
    )
    print("Founder does not start cycles. Ctrl+C stops this process only.")
    try:
        while not watch.stop.wait(1.0):
            if not watch.running:
                break
    except KeyboardInterrupt:
        print("watch stopped")
    watch.stop_watch()
    if watch.thread is not None:
        watch.thread.join(timeout=watch.interval_s + 5)
    return 0 if watch.last_ok else 2
