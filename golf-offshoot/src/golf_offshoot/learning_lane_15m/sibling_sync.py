"""Gym hub observes farm declarations from origin sibling.

Fetch only. Never reset, merge, checkout, or push. Never a master ref.
Not gated on RUNNER_ARMED or PUBLISH_ARMED. Fail-open so PaperWatch stays up.
Does not write origin bytes into working-tree LEARNING_LANE_15M_FARM.json.
"""

from __future__ import annotations

import json
import os
import subprocess
import time
from pathlib import Path
from typing import Any, Callable

from golf_offshoot.learning_lane_15m.paths import latest_dir_15m
from golf_offshoot.repo_paths import repo_root

SIBLING_BRANCH = "cursor/honer-15m-sibling"
ORIGIN_SIBLING = "origin/cursor/honer-15m-sibling"
FARM_BLOB = "golf-offshoot/docs/LEARNING_LANE_15M_FARM.json"
EXHAUSTED_BLOB = "golf-offshoot/docs/LEARNING_LANE_15M_FARM_MENU_EXHAUSTED.json"
CACHE_FARM_NAME = "origin_farm.json"
CACHE_META_NAME = "origin_farm_meta.json"
CACHE_EXHAUSTED_NAME = "origin_farm_exhausted.json"
DEBOUNCE_S = 300.0
FORBIDDEN_GIT_VERBS = frozenset({"push", "reset", "merge", "checkout", "rebase"})


def fetch_argv() -> list[str]:
    return ["fetch", "origin", SIBLING_BRANCH]


def show_farm_argv() -> list[str]:
    return ["show", f"{ORIGIN_SIBLING}:{FARM_BLOB}"]


def show_exhausted_argv() -> list[str]:
    return ["show", f"{ORIGIN_SIBLING}:{EXHAUSTED_BLOB}"]


def rev_parse_argv() -> list[str]:
    return ["rev-parse", ORIGIN_SIBLING]


def refuse_git_argv(argv: list[str]) -> str | None:
    """Refuse push/reset/merge/checkout and any master ref. Observe-only."""
    for token in argv:
        verb = token.lower().lstrip("-")
        if token.lower() in FORBIDDEN_GIT_VERBS or verb in FORBIDDEN_GIT_VERBS:
            return "forbidden_git_verb"
        ref = token.split(":", 1)[0]
        parts = [p.lower() for p in ref.replace("\\", "/").split("/") if p]
        if "master" in parts:
            return "master_ref"
        if token.lower() == "master" or token.lower().endswith(":master"):
            return "master_ref"
    return None


def origin_cache_dir(*, root: Path | None = None) -> Path:
    if root is not None:
        dest = Path(root) / "data" / "learning_lane_15m" / "latest"
        dest.mkdir(parents=True, exist_ok=True)
        return dest
    return latest_dir_15m()


def origin_farm_cache_path(*, root: Path | None = None) -> Path:
    return origin_cache_dir(root=root) / CACHE_FARM_NAME


def origin_farm_meta_path(*, root: Path | None = None) -> Path:
    return origin_cache_dir(root=root) / CACHE_META_NAME


def origin_farm_cache_paths(*, root: Path | None = None) -> tuple[Path, Path]:
    return origin_farm_cache_path(root=root), origin_farm_meta_path(root=root)


def _load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return payload if isinstance(payload, dict) else {}


def load_origin_farm_cache(*, root: Path | None = None) -> dict[str, Any]:
    return _load_json(origin_farm_cache_path(root=root))


def load_origin_farm_meta(*, root: Path | None = None) -> dict[str, Any]:
    return _load_json(origin_farm_meta_path(root=root))


def origin_notebooks(payload: dict[str, Any] | None) -> list[dict[str, Any]]:
    rows = (payload or {}).get("notebooks") if isinstance(payload, dict) else None
    if not isinstance(rows, list):
        return []
    return [row for row in rows if isinstance(row, dict)]


def observed_farm_payload(*, root: Path | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
    """Origin cache when it has notebooks; else local FARM.json. Never overlays RULES.json."""
    from golf_offshoot.learning_lane_15m.farm import load_farm

    cache = load_origin_farm_cache(root=root)
    notebooks = origin_notebooks(cache)
    if notebooks:
        meta = load_origin_farm_meta(root=root)
        meta = dict(meta) if meta else {}
        meta.setdefault("source", "origin")
        meta.setdefault("ref", ORIGIN_SIBLING)
        return cache, meta
    local = load_farm(root=root)
    return local, {"source": "local", "ref": None, "sha": None}


def _git(
    argv: list[str],
    *,
    cwd: Path,
    timeout: float = 60.0,
) -> subprocess.CompletedProcess[str]:
    refused = refuse_git_argv(argv)
    if refused:
        return subprocess.CompletedProcess(["git", *argv], 1, "", refused)
    return subprocess.run(
        ["git", *argv],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )


def _write_cache(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def maybe_fetch_origin_farm(
    *,
    root: Path | None = None,
    now: float | None = None,
    git_run: Callable[..., subprocess.CompletedProcess[str]] | None = None,
    force: bool = False,
    debounce_s: float = DEBOUNCE_S,
) -> dict[str, Any]:
    """Fetch sibling and cache FARM.json. Keep last good cache on failure.

    Not gated on RUNNER_ARMED. Does not reset or push. Does not arm.
    """
    result: dict[str, Any] = {
        "ok": False,
        "updated": False,
        "reason": "",
        "sha": None,
        "fetch_argv": fetch_argv(),
        "show_argv": show_farm_argv(),
    }
    if git_run is None and os.environ.get("PYTEST_CURRENT_TEST"):
        result["ok"] = True
        result["reason"] = "pytest_skip"
        return result
    git_root = root if root is not None and (Path(root) / ".git").exists() else repo_root()
    git_run = git_run or _git
    t = time.time() if now is None else float(now)
    meta = load_origin_farm_meta(root=root)
    last = meta.get("fetched_at_unix")
    if not force and last is not None:
        try:
            if t - float(last) < float(debounce_s):
                result["ok"] = True
                result["reason"] = "debounce"
                result["sha"] = meta.get("sha")
                return result
        except (TypeError, ValueError):
            pass
    try:
        for argv in (fetch_argv(), show_farm_argv(), rev_parse_argv(), show_exhausted_argv()):
            refused = refuse_git_argv(argv)
            if refused:
                result["reason"] = refused
                return result
        fetched = git_run(fetch_argv(), cwd=git_root)
        if getattr(fetched, "returncode", 1) != 0:
            result["reason"] = "fetch_failed"
            return result
        shown = git_run(show_farm_argv(), cwd=git_root)
        if getattr(shown, "returncode", 1) != 0 or not (getattr(shown, "stdout", "") or "").strip():
            result["reason"] = "farm_blob_unreadable"
            return result
        try:
            payload = json.loads(shown.stdout)
        except ValueError:
            result["reason"] = "farm_blob_not_json"
            return result
        if not isinstance(payload, dict):
            result["reason"] = "farm_blob_not_object"
            return result
        parsed = git_run(rev_parse_argv(), cwd=git_root)
        sha = (getattr(parsed, "stdout", "") or "").strip() or None
        _write_cache(origin_farm_cache_path(root=root), payload)
        exhausted = git_run(show_exhausted_argv(), cwd=git_root)
        if getattr(exhausted, "returncode", 1) == 0 and (getattr(exhausted, "stdout", "") or "").strip():
            try:
                exh = json.loads(exhausted.stdout)
            except ValueError:
                exh = None
            if isinstance(exh, dict):
                _write_cache(origin_cache_dir(root=root) / CACHE_EXHAUSTED_NAME, exh)
        new_meta = {
            "source": "origin",
            "ref": ORIGIN_SIBLING,
            "sha": sha,
            "fetched_at_unix": t,
            "farm_blob": FARM_BLOB,
        }
        _write_cache(origin_farm_meta_path(root=root), new_meta)
        result["ok"] = True
        result["updated"] = True
        result["reason"] = "updated"
        result["sha"] = sha
        return result
    except Exception as exc:  # noqa: BLE001 — fail-open, keep last cache
        result["reason"] = f"{type(exc).__name__}: {exc}"
        return result
