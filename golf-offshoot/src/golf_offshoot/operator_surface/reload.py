"""Detect hub/code/artifact changes and restart the Phase 1 shell.

Stdlib only. Polls git tip + hub module mtimes + honesty/viz artifact
mtimes. Debounces so editor temps do not thrash. Code/git changes
re-exec the hub so a stale process after `git pull` (e.g. missing #141
settle join) self-heals. Artifact-only changes soft-reload the UI.
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

from golf_offshoot.operator_surface.paths import ILL_PNG_NAMES, ResolvedRoots, git_repo_root

REEXEC_CODE = 75
HUB_CHILD_ENV = "GOLF_OFFSHOOT_HUB_CHILD"
DEFAULT_POLL_S = 2.0
DEFAULT_DEBOUNCE_S = 1.5

_NOISE_SUFFIXES = (".tmp", ".temp", ".swp", ".swo", ".bak", ".orig", ".pyc", ".pyo")
#: Packages the running hub executes in-process. ``learning_lane_15m`` is here
#: because PaperWatch and the clerical runner run inside the hub: a merge that
#: only touches the lane must still re-exec, or the process keeps serving the
#: old ROLE_ORDER and whitelist while the desk looks normal.
_CODE_PKG_DIRS = (
    "operator_surface",
    "learning_lane_15m",
)
_CODE_RELPATHS = (
    "__main__.py",
    "audit/shadow_settle.py",
)
_ARTIFACT_DIR_GLOBS = (
    ("latest", ("*_live_*", "*leftover*")),
    ("exports", ("*_live_*", "*leftover*")),
    ("calibration", ("weights_calib-v*.json",)),
    ("paper", ("ledger.json", "*.json")),
    ("settlements", ("*.json",)),
    ("snapshots", ("*.json",)),
    ("shadow", ("advises.jsonl",)),
)
_WATCH_DIR_NAMES = (
    "latest",
    "exports",
    "calibration",
    "paper",
    "settlements",
    "snapshots",
    "shadow",
)


@dataclass(frozen=True)
class WatchSnapshot:
    git_tip: str
    code: tuple[tuple[str, int], ...]
    artifacts: tuple[tuple[str, int], ...]

    def fingerprint(self) -> tuple[str, tuple[tuple[str, int], ...], tuple[tuple[str, int], ...]]:
        return (self.git_tip, self.code, self.artifacts)


@dataclass(frozen=True)
class ReloadDecision:
    kind: str  # "none" | "artifacts" | "code"
    reasons: tuple[str, ...] = ()

    @property
    def should_reexec(self) -> bool:
        return self.kind == "code"

    @property
    def should_soft_reload(self) -> bool:
        return self.kind == "artifacts"


def is_noise_name(name: str) -> bool:
    lowered = name.lower()
    if lowered.startswith(".") and lowered not in {".git"}:
        if lowered.endswith(".json") or lowered.endswith(".jsonl"):
            return False
        return True
    if lowered.endswith(_NOISE_SUFFIXES) or lowered.endswith("~"):
        return True
    if lowered in {"__pycache__", ".git"}:
        return True
    return False


def read_git_tip(repo: Path | None = None) -> str:
    """HEAD ref + resolved SHA from the filesystem. No git.exe required."""
    root = repo if repo is not None else git_repo_root()
    if root is None:
        return ""
    git_dir = _resolve_git_dir(root)
    if git_dir is None:
        return ""
    head_path = git_dir / "HEAD"
    try:
        head = head_path.read_text(encoding="utf-8").strip()
    except OSError:
        return ""
    if not head:
        return ""
    if head.startswith("ref:"):
        ref = head.split(":", 1)[1].strip()
        sha = _read_ref_sha(git_dir, ref)
        return f"{ref}@{sha}" if sha else f"{ref}@"
    return f"detached@{head}"


def _resolve_git_dir(repo: Path) -> Path | None:
    marker = repo / ".git"
    if marker.is_dir():
        return marker
    if not marker.is_file():
        return None
    try:
        text = marker.read_text(encoding="utf-8").strip()
    except OSError:
        return None
    if not text.lower().startswith("gitdir:"):
        return None
    raw = text.split(":", 1)[1].strip()
    path = Path(raw)
    if not path.is_absolute():
        path = (repo / path)
    try:
        return path.resolve()
    except OSError:
        return None


def _common_git_dir(git_dir: Path) -> Path | None:
    """The shared git dir behind a linked worktree.

    A worktree's git dir holds its own HEAD but no ``refs/heads`` and no
    ``packed-refs`` — those live in the common dir named by ``commondir``.
    Resolving only the worktree dir makes every branch SHA read as empty, so
    a commit on the current branch looks like no change at all.
    """
    marker = git_dir / "commondir"
    if not marker.is_file():
        return None
    try:
        raw = marker.read_text(encoding="utf-8").strip()
    except OSError:
        return None
    if not raw:
        return None
    path = Path(raw)
    if not path.is_absolute():
        path = git_dir / path
    try:
        resolved = path.resolve()
    except OSError:
        return None
    return resolved if resolved != git_dir else None


def _read_ref_sha(git_dir: Path, ref: str) -> str:
    search = [git_dir]
    common = _common_git_dir(git_dir)
    if common is not None:
        search.append(common)
    for base in search:
        ref_path = base / ref
        try:
            if ref_path.is_file():
                text = ref_path.read_text(encoding="utf-8").strip()
                if text:
                    return text
        except OSError:
            pass
    for base in search:
        try:
            body = (base / "packed-refs").read_text(encoding="utf-8")
        except OSError:
            continue
        for line in body.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or stripped.startswith("^"):
                continue
            parts = stripped.split()
            if len(parts) >= 2 and parts[1] == ref:
                return parts[0]
    return ""


def hub_code_files(pkg: Path | None = None) -> list[Path]:
    """Modules whose mtime means the running process may be stale."""
    base = pkg if pkg is not None else Path(__file__).resolve().parents[1]
    files: list[Path] = []
    for pkg_name in _CODE_PKG_DIRS:
        folder = base / pkg_name
        if not folder.is_dir():
            continue
        for path in sorted(folder.glob("*.py")):
            if not is_noise_name(path.name):
                files.append(path)
    for rel in _CODE_RELPATHS:
        path = base / rel
        if path.is_file():
            files.append(path)
    return files


def artifact_watch_files(roots: ResolvedRoots) -> list[Path]:
    files: list[Path] = [roots.shadow_path]
    art = roots.artifact_root
    for folder_name, patterns in _ARTIFACT_DIR_GLOBS:
        folder = art / folder_name
        if not folder.is_dir():
            continue
        for pattern in patterns:
            for path in folder.glob(pattern):
                if path.is_file() and not is_noise_name(path.name):
                    files.append(path)
    viz = roots.viz_root
    if viz.is_dir():
        for name in (*ILL_PNG_NAMES, "viz_wall_manifest.json"):
            candidate = viz / name
            if candidate.is_file():
                files.append(candidate)
    # The 15m board is published under docs/, not viz_root. Watch it too, so a
    # regenerated board refreshes the open tab without anyone clicking reload.
    try:
        from golf_offshoot.learning_lane_15m.illustrate import chart_png_path

        board = chart_png_path()
    except Exception:
        board = None
    if board is not None and board.is_file():
        files.append(board)
    # unique, stable
    seen: set[Path] = set()
    out: list[Path] = []
    for path in files:
        try:
            resolved = path.resolve()
        except OSError:
            continue
        if resolved in seen:
            continue
        seen.add(resolved)
        out.append(resolved)
    return out


def artifact_watch_dirs(roots: ResolvedRoots) -> list[Path]:
    dirs = [roots.artifact_root / name for name in _WATCH_DIR_NAMES]
    dirs.append(roots.viz_root)
    dirs.append(roots.shadow_path.parent)
    seen: set[Path] = set()
    out: list[Path] = []
    for path in dirs:
        try:
            resolved = path.resolve()
        except OSError:
            continue
        if resolved in seen:
            continue
        seen.add(resolved)
        out.append(resolved)
    return out


def _mtime_ns(path: Path) -> int:
    try:
        return int(path.stat().st_mtime_ns)
    except OSError:
        return 0


def collect_snapshot(
    *,
    repo: Path | None = None,
    code_files: list[Path] | None = None,
    artifact_files: list[Path] | None = None,
    artifact_dirs: list[Path] | None = None,
    roots: ResolvedRoots | None = None,
    pkg: Path | None = None,
) -> WatchSnapshot:
    git_tip = read_git_tip(repo)
    code_src = code_files if code_files is not None else hub_code_files(pkg)
    if artifact_files is None or artifact_dirs is None:
        resolved = roots
        if resolved is None:
            from golf_offshoot.operator_surface.paths import resolve_roots

            resolved = resolve_roots()
        if artifact_files is None:
            artifact_files = artifact_watch_files(resolved)
        if artifact_dirs is None:
            artifact_dirs = artifact_watch_dirs(resolved)
    code = tuple(sorted((str(path), _mtime_ns(path)) for path in code_src))
    art_entries = [(str(path), _mtime_ns(path)) for path in artifact_files]
    art_entries.extend((str(path) + "/", _mtime_ns(path)) for path in artifact_dirs)
    artifacts = tuple(sorted(art_entries))
    return WatchSnapshot(git_tip=git_tip, code=code, artifacts=artifacts)


def classify_change(previous: WatchSnapshot, current: WatchSnapshot) -> ReloadDecision:
    reasons: list[str] = []
    if previous.git_tip != current.git_tip:
        reasons.append("git_tip")
    if previous.code != current.code:
        reasons.append("hub_mtime")
    if reasons:
        return ReloadDecision(kind="code", reasons=tuple(reasons))
    if previous.artifacts != current.artifacts:
        return ReloadDecision(kind="artifacts", reasons=("artifact_mtime",))
    return ReloadDecision(kind="none")


class HubWatcher:
    """Poll snapshots and emit one decision after the tree is briefly stable."""

    def __init__(
        self,
        *,
        debounce_s: float = DEFAULT_DEBOUNCE_S,
        clock=time.monotonic,
        snapshot_fn=None,
    ) -> None:
        self.debounce_s = float(debounce_s)
        self._clock = clock
        self._snapshot_fn = snapshot_fn or collect_snapshot
        self.baseline: WatchSnapshot | None = None
        self._pending: WatchSnapshot | None = None
        self._pending_since: float | None = None

    def seed(self, snap: WatchSnapshot | None = None) -> WatchSnapshot:
        self.baseline = snap if snap is not None else self._snapshot_fn()
        self._pending = None
        self._pending_since = None
        return self.baseline

    def observe(self, snap: WatchSnapshot, *, now: float | None = None) -> ReloadDecision:
        t = self._clock() if now is None else now
        if self.baseline is None:
            self.baseline = snap
            return ReloadDecision(kind="none")
        change = classify_change(self.baseline, snap)
        if change.kind == "none":
            self._pending = None
            self._pending_since = None
            return change
        if self._pending is None or self._pending.fingerprint() != snap.fingerprint():
            self._pending = snap
            self._pending_since = t
            return ReloadDecision(kind="none")
        if t - float(self._pending_since or t) < self.debounce_s:
            return ReloadDecision(kind="none")
        accepted = classify_change(self.baseline, snap)
        self.baseline = snap
        self._pending = None
        self._pending_since = None
        return accepted

    def poll(self) -> ReloadDecision:
        return self.observe(self._snapshot_fn())


def hub_child_command(
    *,
    host: str,
    port: int,
    event_id: str | None = None,
    open_browser: bool = True,
    artifact_root: Path | None = None,
    viz_root: Path | None = None,
    executable: str | None = None,
    lane: str | None = None,
) -> list[str]:
    """Windows-friendly `python -m golf_offshoot shell` relaunch argv."""
    cmd = [executable or sys.executable, "-m", "golf_offshoot", "shell", "--host", str(host), "--port", str(port)]
    if event_id:
        cmd.extend(["--event", str(event_id)])
    if not open_browser:
        cmd.append("--no-browser")
    if artifact_root is not None:
        cmd.extend(["--artifact-root", str(artifact_root)])
    if viz_root is not None:
        cmd.extend(["--viz-root", str(viz_root)])
    if lane and str(lane) != "golf":
        cmd.extend(["--lane", str(lane)])
    return cmd


def supervise_hub_child(
    cmd: list[str],
    *,
    env: dict[str, str] | None = None,
    runner=subprocess.run,
) -> int:
    """Keep one parent process so the Windows .bat stays attached across restarts."""
    child_env = dict(os.environ if env is None else env)
    child_env[HUB_CHILD_ENV] = "1"
    while True:
        try:
            completed = runner(cmd, env=child_env)
        except KeyboardInterrupt:
            return 0
        code = getattr(completed, "returncode", completed)
        if int(code or 0) != REEXEC_CODE:
            return int(code or 0)


def is_hub_child(environ: dict[str, str] | None = None) -> bool:
    env = os.environ if environ is None else environ
    return (env.get(HUB_CHILD_ENV) or "").strip() == "1"
