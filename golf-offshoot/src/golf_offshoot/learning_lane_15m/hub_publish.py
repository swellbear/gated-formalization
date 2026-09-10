"""Gym-only material hub publish. Allowlist to origin/master.

Never push sibling HEAD to master. Cloud CoS must not import this on the
stamp path. Fail-open on git/auth errors so PaperWatch stays up.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

from golf_offshoot.learning_lane_15m.paths import has_15m_root_override, latest_dir_15m, paper_dir_15m
from golf_offshoot.repo_paths import repo_root

ARM_NAME = "PUBLISH_ARMED"

ALLOWLIST = (
    Path("docs") / "observability-hub" / "data" / "manifest.json",
    Path("docs") / "observability-hub" / "data" / "charts" / "learning_lane_15m" / "paper_window_strip.png",
    Path("docs") / "observability-hub" / "data" / "validator_report.json",
)

FORBIDDEN_COPY_NEEDLES = (
    "scorecard",
    "SCORECARD",
    "LEARNING_LANE_15M_SCORECARD",
    "fee-accurate",
)

PUSH_REF = "HEAD:master"


def publish_arm_path() -> Path:
    return latest_dir_15m() / ARM_NAME


def founder_has_armed_publish() -> bool:
    return publish_arm_path().is_file()


def write_publish_arm_file() -> Path:
    path = publish_arm_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "armed\n"
        "allowlist=manifest.json,paper_window_strip.png,validator_report.json\n"
        "never_push_sibling_head_to_master\n",
        encoding="utf-8",
    )
    return path


def master_push_argv() -> list[str]:
    """Push dest is always worktree HEAD to origin/master. Never sibling HEAD."""
    return ["push", "origin", PUSH_REF]


def watch_collecting_passed(invariants: dict[str, Any] | None) -> bool:
    if not isinstance(invariants, dict):
        return False
    for check in invariants.get("checks") or []:
        if not isinstance(check, dict):
            continue
        if str(check.get("id") or "") == "watch_is_collecting":
            return bool(check.get("passed"))
    return False


def lineage_a_ledger_present(*, root: Path | None = None) -> bool:
    del root  # ledger lives under the 15m artifact root, not the git root
    return (paper_dir_15m() / "ledger.json").is_file()


def load_invariants_payload() -> dict[str, Any] | None:
    path = latest_dir_15m() / "invariants.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return payload if isinstance(payload, dict) else None


def evaluate_publish_gates(
    *,
    armed: bool,
    ledger_present: bool,
    watch_ok: bool,
    material_reasons: list[str],
    allowlist: tuple[Path, ...] = ALLOWLIST,
) -> dict[str, Any]:
    """Pure decision. Empty material_reasons is a heartbeat — do not publish."""
    if not armed:
        return {"ok": False, "publish": False, "reason": "unarmed"}
    if not ledger_present:
        return {"ok": False, "publish": False, "reason": "lineage_a_ledger_missing"}
    if not watch_ok:
        return {"ok": False, "publish": False, "reason": "watch_not_collecting"}
    if not material_reasons:
        return {"ok": False, "publish": False, "reason": "heartbeat"}
    leaked = [p.as_posix() for p in allowlist if any(n in p.as_posix() for n in FORBIDDEN_COPY_NEEDLES)]
    if leaked:
        return {"ok": False, "publish": False, "reason": "allowlist_would_copy_scorecard"}
    return {
        "ok": True,
        "publish": True,
        "reason": "material",
        "material_reasons": list(material_reasons),
    }


def _load_json(path: Path) -> dict[str, Any] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return payload if isinstance(payload, dict) else None


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
    )


def _origin_master_manifest(root: Path, git_run: Callable[..., subprocess.CompletedProcess[str]]) -> dict[str, Any] | None:
    fetched = git_run(["fetch", "origin", "master"], cwd=root)
    if fetched.returncode != 0:
        return None
    shown = git_run(
        ["show", "origin/master:docs/observability-hub/data/manifest.json"],
        cwd=root,
    )
    if shown.returncode != 0 or not (shown.stdout or "").strip():
        return None
    try:
        payload = json.loads(shown.stdout)
    except ValueError:
        return None
    return payload if isinstance(payload, dict) else None


def _validate_hub_strict(root: Path) -> bool:
    script = root / "docs" / "observability-hub" / "validate_hub.py"
    if not script.is_file():
        return False
    proc = subprocess.run(
        [sys.executable, str(script), "--strict"],
        cwd=str(root),
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    return proc.returncode == 0


def _copy_allowlist(src_root: Path, dest_root: Path) -> list[Path]:
    copied: list[Path] = []
    for rel in ALLOWLIST:
        src = src_root / rel
        dest = dest_root / rel
        if not src.is_file():
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        copied.append(rel)
    return copied


def _notify(body: str, title: str) -> str | None:
    try:
        from golf_offshoot.strategy.watch import WatchConfigError, publish_ntfy

        return publish_ntfy(body, title=title, priority="default")
    except Exception:  # noqa: BLE001 — fail-open; ntfy is optional
        return None


def maybe_publish_hub(
    *,
    root: Path | None = None,
    git_run: Callable[..., subprocess.CompletedProcess[str]] | None = None,
    validate: Callable[[Path], bool] | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """After a gym runner pass. Fail-open. Never force. Never sibling-HEAD-to-master."""
    result: dict[str, Any] = {
        "ok": False,
        "published": False,
        "pushed": False,
        "reason": "",
        "material_reasons": [],
        "push_argv": master_push_argv(),
    }
    root = root or repo_root()
    git_run = git_run or _git
    try:
        if has_15m_root_override():
            result["reason"] = "scratch_override"
            return result
        armed = founder_has_armed_publish()
        ledger_present = lineage_a_ledger_present(root=root)
        invariants = load_invariants_payload()
        watch_ok = watch_collecting_passed(invariants)
        early = evaluate_publish_gates(
            armed=armed,
            ledger_present=ledger_present,
            watch_ok=watch_ok,
            material_reasons=["pending"],  # placeholder until origin/master is readable
        )
        if not armed or not ledger_present or not watch_ok:
            result["reason"] = str(early["reason"])
            return result
        local_manifest = _load_json(root / ALLOWLIST[0])
        if local_manifest is None:
            result["reason"] = "local_manifest_missing"
            return result
        published = _origin_master_manifest(root, git_run)
        if published is None:
            # Fetch/show failed: fail-open, do not invent a first publish from blindness.
            result["reason"] = "origin_master_manifest_unreadable"
            return result
        from golf_offshoot.operator_surface.observability import material_publish_reasons

        reasons = material_publish_reasons(published, local_manifest)
        gates = evaluate_publish_gates(
            armed=armed,
            ledger_present=ledger_present,
            watch_ok=watch_ok,
            material_reasons=reasons,
        )
        result["reason"] = str(gates["reason"])
        result["material_reasons"] = list(gates.get("material_reasons") or reasons)
        if not gates.get("publish"):
            return result
        if not (validate or _validate_hub_strict)(root):
            result["reason"] = "validate_hub_failed"
            _notify(
                "15m hub publish skipped: validate_hub --strict failed",
                "15m hub Pages publish",
            )
            return result
        if dry_run:
            result["ok"] = True
            result["reason"] = "dry_run"
            return result

        worktree = Path(tempfile.mkdtemp(prefix="gpf-hub-pages-"))
        try:
            added = git_run(
                ["worktree", "add", "--detach", str(worktree), "origin/master"],
                cwd=root,
            )
            if added.returncode != 0:
                result["reason"] = "worktree_add_failed"
                _notify(
                    f"15m hub publish skipped: worktree add failed\n{(added.stderr or '')[:400]}",
                    "15m hub Pages publish",
                )
                return result
            copied = _copy_allowlist(root, worktree)
            if not copied:
                result["reason"] = "allowlist_copy_empty"
                return result
            add = git_run(["add", *[p.as_posix() for p in ALLOWLIST]], cwd=worktree)
            if add.returncode != 0:
                result["reason"] = "git_add_failed"
                return result
            commit = git_run(
                [
                    "commit",
                    "-m",
                    "hub: material 15m Pages allowlist (gym PUBLISH_ARMED)",
                ],
                cwd=worktree,
            )
            if commit.returncode != 0:
                result["reason"] = "nothing_to_commit"
                return result
            push_argv = master_push_argv()
            if "--force" in push_argv or "honer-15m-sibling" in " ".join(push_argv):
                result["reason"] = "refused_unsafe_push"
                return result
            pushed = git_run(push_argv, cwd=worktree)
            if push_argv != ["push", "origin", "HEAD:master"]:
                result["reason"] = "refused_unsafe_push"
                return result
            if pushed.returncode != 0:
                result["reason"] = "git_push_failed"
                _notify(
                    f"15m hub publish failed: git push origin HEAD:master\n{(pushed.stderr or '')[:400]}",
                    "15m hub Pages publish",
                )
                return result
            result["ok"] = True
            result["published"] = True
            result["pushed"] = True
            result["reason"] = "published"
            _notify(
                "15m hub Pages allowlist pushed to origin/master (material). Trading NOT ARMED.",
                "15m hub Pages publish",
            )
            return result
        finally:
            git_run(["worktree", "remove", "--force", str(worktree)], cwd=root)
            shutil.rmtree(worktree, ignore_errors=True)
    except Exception as exc:  # noqa: BLE001 — never take PaperWatch down
        result["reason"] = f"fail_open:{type(exc).__name__}:{exc}"
        return result
