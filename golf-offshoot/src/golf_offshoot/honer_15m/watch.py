"""Honer sidecar watch. Own process. Own re-exec. Not PaperWatch. Not a second hub."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Any

from golf_offshoot.honer_15m.loop import run_tick
from golf_offshoot.honer_15m.paths import assert_honer_path, watch_status_path
from golf_offshoot.localtime import now

DEFAULT_INTERVAL_S = 90.0
FIRST_SLEEP_S = 45.0
ENV_INTERVAL = "GOLF_OFFSHOOT_HONER_WATCH_S"
HONER_CHILD_ENV = "GOLF_OFFSHOOT_HONER_CHILD"
REEXEC_CODE = 75
PKG = Path(__file__).resolve().parent
DOCS = Path(__file__).resolve().parents[3] / "docs"


def honer_interval_s(override: float | None = None) -> float:
    if override is not None and override > 0:
        return float(override)
    raw = os.environ.get(ENV_INTERVAL) or ""
    try:
        parsed = float(raw)
    except ValueError:
        parsed = 0.0
    return parsed if parsed > 0 else DEFAULT_INTERVAL_S


def honer_sidecar_command(*, executable: str | None = None) -> list[str]:
    return [executable or sys.executable, "-m", "golf_offshoot", "honer-15m", "--watch"]


def is_honer_child(environ: dict[str, str] | None = None) -> bool:
    env = os.environ if environ is None else environ
    return (env.get(HONER_CHILD_ENV) or "").strip() == "1"


def load_watch_status() -> dict[str, Any]:
    path = watch_status_path()
    if not path.is_file():
        return {"running": False, "cycles": 0, "lane": "honer_15m"}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"running": False, "cycles": 0, "lane": "honer_15m"}
    return payload if isinstance(payload, dict) else {"running": False, "cycles": 0, "lane": "honer_15m"}


def _write_status(payload: dict[str, Any]) -> None:
    path = watch_status_path()
    existing = load_watch_status()
    existing.update(payload)
    existing["lane"] = "honer_15m"
    existing["at"] = now().isoformat()
    assert_honer_path(path)
    path.write_text(json.dumps(existing, indent=2), encoding="utf-8")


def _honer_watch_files() -> list[Path]:
    files = sorted(p for p in PKG.glob("*.py") if p.is_file())
    for name in ("HONER_15M_RULES.json", "HONER_15M_CATALOG.json"):
        path = DOCS / name
        if path.is_file():
            files.append(path)
    return files


def honer_code_mtime() -> float:
    newest = 0.0
    for path in _honer_watch_files():
        try:
            newest = max(newest, path.stat().st_mtime)
        except OSError:
            continue
    return newest


def pid_alive(pid: int) -> bool:
    if int(pid or 0) <= 0:
        return False
    try:
        import psutil

        return bool(psutil.pid_exists(int(pid)))
    except Exception:
        try:
            os.kill(int(pid), 0)
        except OSError:
            return False
        return True


def sidecar_pid_is_honer(pid: int) -> bool:
    if not pid_alive(pid):
        return False
    try:
        import psutil

        proc = psutil.Process(int(pid))
        line = " ".join(str(a) for a in (proc.cmdline() or []))
        return "honer-15m" in line and "shell" not in line.split()
    except Exception:
        return True


def stop_pid(pid: int) -> None:
    if int(pid or 0) <= 0:
        return
    try:
        import psutil

        proc = psutil.Process(int(pid))
        kids = proc.children(recursive=True)
        proc.terminate()
        for child in kids:
            try:
                child.terminate()
            except Exception:
                pass
        gone, alive = psutil.wait_procs([proc, *kids], timeout=3)
        del gone
        for child in alive:
            try:
                child.kill()
            except Exception:
                pass
        return
    except Exception:
        pass
    try:
        os.kill(int(pid), 15)
    except OSError:
        return


class HonerWatch:
    """Inner tick loop. Runs inside the sidecar child, not inside 8765."""

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
                "sidecar": True,
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


def _run_child_loop(*, interval_s: float | None = None) -> int:
    watch = HonerWatch(interval_s=interval_s)
    watch.start()
    last = honer_code_mtime()
    try:
        while True:
            time.sleep(2.0)
            now_m = honer_code_mtime()
            if now_m > last + 1e-6:
                watch.stop_watch()
                return REEXEC_CODE
    except KeyboardInterrupt:
        watch.stop_watch()
        return 0


def supervise_honer_child(*, interval_s: float | None = None) -> int:
    cmd = honer_sidecar_command()
    env = dict(os.environ)
    env[HONER_CHILD_ENV] = "1"
    _write_status({"running": True, "pid": os.getpid(), "sidecar": True, "role": "supervisor"})
    while True:
        try:
            completed = subprocess.run(cmd, env=env, check=False)
        except KeyboardInterrupt:
            _write_status({"running": False})
            return 0
        code = int(getattr(completed, "returncode", completed) or 0)
        if code != REEXEC_CODE:
            _write_status({"running": False, "last_error": f"child exit {code}" if code else ""})
            return code
        _write_status({"running": True, "pid": os.getpid(), "sidecar": True, "reexec": True})


def run_watch_forever(*, interval_s: float | None = None, once: bool = False) -> int:
    if once:
        run_tick()
        try:
            from golf_offshoot.honer_15m.invariants import format_invariants, run_invariants

            print(format_invariants(run_invariants()))
        except Exception:
            pass
        return 0
    if is_honer_child():
        return _run_child_loop(interval_s=interval_s)
    return supervise_honer_child(interval_s=interval_s)


def start_sidecar_process(
    *,
    existing: subprocess.Popen[Any] | None = None,
    env: dict[str, str] | None = None,
) -> subprocess.Popen[Any] | None:
    if existing is not None and existing.poll() is None:
        return existing
    status = load_watch_status()
    pid = int(status.get("pid") or 0)
    if sidecar_pid_is_honer(pid):
        return existing
    child_env = dict(os.environ if env is None else env)
    kwargs: dict[str, Any] = {}
    if os.name == "nt":
        kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        kwargs["start_new_session"] = True
    proc = subprocess.Popen(honer_sidecar_command(), env=child_env, **kwargs)
    _write_status({"running": True, "pid": proc.pid, "sidecar": True, "role": "hub-launched"})
    return proc


def stop_sidecar_process(proc: subprocess.Popen[Any] | None) -> None:
    pid = 0
    if proc is not None and proc.poll() is None:
        pid = int(proc.pid)
    if not pid:
        pid = int(load_watch_status().get("pid") or 0)
    if pid:
        stop_pid(pid)
    if proc is not None and proc.poll() is None:
        try:
            proc.terminate()
            proc.wait(timeout=3)
        except Exception:
            try:
                proc.kill()
            except Exception:
                pass
    _write_status({"running": False})
