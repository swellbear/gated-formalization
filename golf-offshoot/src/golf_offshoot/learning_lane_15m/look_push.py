"""Gym look-push: L1 scorecard onto the honer sibling. Ride RUNNER_ARMED.

Sibling worktree of ``cursor/honer-15m-sibling``. Allowlist
``LEARNING_LANE_15M_SCORECARD_{id}_L1.json`` only. Never ledger, fills, or
fee totals. Never ``HEAD:master``. Fail-open so PaperWatch stays up.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Callable

from golf_offshoot.learning_lane_15m.paths import has_15m_root_override
from golf_offshoot.repo_paths import repo_root

SIBLING_BRANCH = "cursor/honer-15m-sibling"
ORIGIN_SIBLING = "origin/cursor/honer-15m-sibling"
PUSH_REF = f"HEAD:{SIBLING_BRANCH}"
SCORECARD_DIR_REL = Path("golf-offshoot") / "docs"
L1_NAME_RE = re.compile(r"^LEARNING_LANE_15M_SCORECARD_[A-Za-z0-9._-]+_L1\.json$")
L1_REL_RE = re.compile(
    r"^golf-offshoot/docs/LEARNING_LANE_15M_SCORECARD_[A-Za-z0-9._-]+_L1\.json$"
)
#: Cloud Operator stamps. Gym must not copy over these or CONTINUE cannot stick.
PROTECTED_OPERATOR_STAMPS = frozenset({"PARK", "CONTINUE"})


def sibling_push_argv() -> list[str]:
    return ["push", "origin", PUSH_REF]


def is_l1_allowlist_rel(rel: Path | str) -> bool:
    posix = rel.as_posix() if isinstance(rel, Path) else str(rel).replace("\\", "/")
    return bool(L1_REL_RE.match(posix))


def evaluate_look_push_gates(
    *,
    armed: bool,
    rels: list[Path],
) -> dict[str, Any]:
    if not armed:
        return {"ok": False, "push": False, "reason": "unarmed"}
    leaked = [p.as_posix() for p in rels if not is_l1_allowlist_rel(p)]
    extra = [
        p.as_posix()
        for p in rels
        if any(n.lower() in p.as_posix().lower() for n in ("ledger", "fills", "fee-accurate", "fee_total"))
    ]
    if leaked or extra:
        return {
            "ok": False,
            "push": False,
            "reason": "allowlist_refused",
            "leaked": leaked or extra,
        }
    if not rels:
        return {"ok": False, "push": False, "reason": "nothing_to_push"}
    return {"ok": True, "push": True, "reason": "l1_allowlist", "rels": [p.as_posix() for p in rels]}


def sibling_l1_stamp_blocks_overwrite(dest: Path) -> bool:
    """True when dest already has Operator PARK/CONTINUE. Do not copy over it."""
    if not dest.is_file():
        return False
    try:
        payload = json.loads(dest.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    if not isinstance(payload, dict):
        return False
    stamp = str(payload.get("operator_look") or "").strip().upper()
    return stamp in PROTECTED_OPERATOR_STAMPS


def copy_allowlisted_l1(
    *,
    src_root: Path,
    dest_root: Path,
    rels: list[Path],
) -> dict[str, list[str]]:
    """Copy gym L1 JSON onto a sibling tree. Never clobber PARK/CONTINUE."""
    copied: list[str] = []
    preserved: list[str] = []
    for rel in rels:
        if not is_l1_allowlist_rel(rel):
            continue
        src = src_root / rel
        dest = dest_root / rel
        if not src.is_file():
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        if sibling_l1_stamp_blocks_overwrite(dest):
            preserved.append(rel.as_posix())
            continue
        shutil.copy2(src, dest)
        copied.append(rel.as_posix())
    return {"copied": copied, "preserved": preserved}


def l1_scorecard_rels(*, root: Path | None = None) -> list[Path]:
    docs = (root or repo_root()) / SCORECARD_DIR_REL
    if not docs.is_dir():
        return []
    out: list[Path] = []
    for path in sorted(docs.glob("LEARNING_LANE_15M_SCORECARD_*_L1.json")):
        rel = SCORECARD_DIR_REL / path.name
        if L1_NAME_RE.match(path.name) and is_l1_allowlist_rel(rel):
            out.append(rel)
    return out


def _runner_armed() -> bool:
    try:
        from golf_offshoot.learning_lane_15m.runner import founder_has_armed

        return bool(founder_has_armed())
    except Exception:  # noqa: BLE001 — unarmed if the arm file cannot be read
        return False


def _git(
    argv: list[str],
    *,
    cwd: Path,
    timeout: float = 60.0,
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.setdefault("GIT_AUTHOR_NAME", "Cursor Agent")
    env.setdefault("GIT_AUTHOR_EMAIL", "cursoragent@cursor.com")
    env.setdefault("GIT_COMMITTER_NAME", "Cursor Agent")
    env.setdefault("GIT_COMMITTER_EMAIL", "cursoragent@cursor.com")
    return subprocess.run(
        ["git", *argv],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
        env=env,
    )


def maybe_push_look(
    *,
    root: Path | None = None,
    git_run: Callable[..., subprocess.CompletedProcess[str]] | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Copy L1 JSON onto a sibling worktree and push. Fail-open. Never master."""
    result: dict[str, Any] = {
        "ok": False,
        "pushed": False,
        "reason": "",
        "push_argv": sibling_push_argv(),
        "rels": [],
    }
    root = root or repo_root()
    if git_run is None and os.environ.get("PYTEST_CURRENT_TEST"):
        result["reason"] = "pytest_skip"
        return result
    git_run = git_run or _git
    try:
        if has_15m_root_override():
            result["reason"] = "scratch_override"
            return result
        armed = _runner_armed()
        rels = l1_scorecard_rels(root=root)
        gates = evaluate_look_push_gates(armed=armed, rels=rels)
        result["reason"] = str(gates["reason"])
        result["rels"] = list(gates.get("rels") or [p.as_posix() for p in rels])
        if not gates.get("push"):
            return result
        push_argv = sibling_push_argv()
        joined = " ".join(push_argv)
        if "--force" in push_argv or "HEAD:master" in joined or joined.endswith(" master"):
            result["reason"] = "refused_unsafe_push"
            return result
        if push_argv != ["push", "origin", PUSH_REF]:
            result["reason"] = "refused_unsafe_push"
            return result
        if dry_run:
            result["ok"] = True
            result["reason"] = "dry_run"
            return result
        fetched = git_run(["fetch", "origin", SIBLING_BRANCH], cwd=root)
        if getattr(fetched, "returncode", 1) != 0:
            result["reason"] = "fetch_failed"
            return result
        worktree = Path(tempfile.mkdtemp(prefix="gpf-l1-look-"))
        try:
            added = git_run(
                ["worktree", "add", "--detach", str(worktree), ORIGIN_SIBLING],
                cwd=root,
            )
            if getattr(added, "returncode", 1) != 0:
                result["reason"] = "worktree_add_failed"
                return result
            copied_info = copy_allowlisted_l1(src_root=root, dest_root=worktree, rels=rels)
            copied = [Path(p) for p in copied_info["copied"]]
            result["preserved"] = list(copied_info["preserved"])
            if not copied:
                result["reason"] = (
                    "stamp_preserved" if copied_info["preserved"] else "allowlist_copy_empty"
                )
                return result
            add = git_run(["add", *[p.as_posix() for p in copied]], cwd=worktree)
            if getattr(add, "returncode", 1) != 0:
                result["reason"] = "git_add_failed"
                return result
            commit = git_run(
                [
                    "commit",
                    "-m",
                    "15m: L1 scorecard look-push (RUNNER_ARMED, sibling allowlist)",
                ],
                cwd=worktree,
            )
            if getattr(commit, "returncode", 1) != 0:
                result["reason"] = "nothing_to_commit"
                return result
            pushed = git_run(push_argv, cwd=worktree)
            if getattr(pushed, "returncode", 1) != 0:
                result["reason"] = "git_push_failed"
                return result
            result["ok"] = True
            result["pushed"] = True
            result["reason"] = "pushed"
            result["rels"] = [p.as_posix() for p in copied]
            return result
        finally:
            git_run(["worktree", "remove", "--force", str(worktree)], cwd=root)
            shutil.rmtree(worktree, ignore_errors=True)
    except Exception as exc:  # noqa: BLE001 — never take PaperWatch down
        result["reason"] = f"fail_open:{type(exc).__name__}:{exc}"
        return result
