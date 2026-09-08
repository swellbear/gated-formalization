"""Clerical learning runner. Dry-run until Founder arms it.

Reads ``roles_owed`` and may serve only a named whitelist of clerical jobs:
Illustrator re-render, Systems publish, Digestor digest-asof. Judicial work
(ADMIT, RUN-ONLY, closing a park, lifting the HOLD) is never on the list.

Default mode is dry-run: log what would be served, serve nothing.

The kill switch is a file, ``latest/RUNNER_KILL``. The runner re-reads it at
the start of every pass. Touch the file to stop the runner mid-flight without
touching PaperWatch. Delete the file to let a later pass run. An env var is
not the switch.

Serve-on-proof: a role is marked served only after the artifact it was meant
to produce actually changed on disk (sha256). Exit code 0 is not proof. If
the artifact did not move, the role stays owed and the failure is logged.
``mark_roles_served(..., served_kind='auto')`` is the only serve call site.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any, Callable

from golf_offshoot.learning_lane_15m.learn import (
    load_wake_state,
    mark_roles_served,
    scan_learning_evidence,
)
from golf_offshoot.learning_lane_15m.paths import latest_dir_15m
from golf_offshoot.localtime import format_eastern, isoformat_now
from golf_offshoot.operator_surface.observability import (
    material_publish_reasons,
    repo_root,
)

MODE_DRY = "dry-run"
MODE_OFF = "off"
MODE_ARMED = "armed"
ENV_MODE = "GOLF_OFFSHOOT_LEARNING_RUNNER"

KILL_NAME = "RUNNER_KILL"
ARM_NAME = "RUNNER_ARMED"

# Enumerate what this process may ever do. A blacklist is not acceptable.
CLERICAL_WHITELIST = ("illustrator", "systems", "digestor")
JUDICIAL_NEVER = (
    "operator",
    "lab",
    "validator",
    "admit",
    "run-only",
    "park",
    "hold",
)

LOG_NAME = "learning_runner.jsonl"

DIGEST_ASOF_NAME = "digest_asof.json"
MANIFEST_REL = Path("docs") / "observability-hub" / "data" / "manifest.json"
PNG_REL = (
    Path("docs")
    / "observability-hub"
    / "data"
    / "charts"
    / "learning_lane_15m"
    / "paper_window_strip.png"
)


def runner_mode(raw: str | None = None) -> str:
    """Requested mode. The kill file overrides this to off on every pass."""
    value = str(raw if raw is not None else os.environ.get(ENV_MODE, MODE_DRY)).strip().lower()
    if value in {MODE_DRY, "dry", "dryrun"}:
        return MODE_DRY
    if value in {MODE_OFF, "kill", "killed", "stop"}:
        return MODE_OFF
    if value in {MODE_ARMED, "on", "live"}:
        return MODE_ARMED
    return MODE_DRY


def runner_log_path() -> Path:
    return latest_dir_15m() / LOG_NAME


def kill_switch_path() -> Path:
    return latest_dir_15m() / KILL_NAME


def arm_file_path() -> Path:
    return latest_dir_15m() / ARM_NAME


def kill_switch_active() -> bool:
    """Re-read from disk. Presence of the file is the switch."""
    return kill_switch_path().is_file()


def write_kill_switch() -> Path:
    path = kill_switch_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("off\n", encoding="utf-8")
    return path


def clear_kill_switch() -> None:
    path = kill_switch_path()
    if path.is_file():
        path.unlink()


def founder_has_armed() -> bool:
    return arm_file_path().is_file()


def _append_log(entry: dict[str, Any]) -> Path:
    path = runner_log_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=True) + "\n")
    return path


def _owed_roles(state: dict[str, Any] | None) -> list[str]:
    if not state:
        return []
    names: list[str] = []
    for entry in state.get("roles_owed") or []:
        role = str(entry.get("role") or "").strip().lower()
        if role and role not in names:
            names.append(role)
    return names


def artifact_path(role: str, *, root: Path | None = None) -> Path:
    if role == "digestor":
        return latest_dir_15m() / DIGEST_ASOF_NAME
    base = root or repo_root()
    rel = {
        "illustrator": PNG_REL,
        "systems": MANIFEST_REL,
    }.get(role)
    if rel is None:
        raise ValueError(f"no clerical artifact for role {role!r}")
    return base / rel


def file_fingerprint(path: Path) -> str | None:
    if not path.is_file():
        return None
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return f"{path.stat().st_size}:{digest}"


def plan_from_wake(state: dict[str, Any] | None) -> dict[str, Any]:
    owed = _owed_roles(state)
    would_serve = [role for role in CLERICAL_WHITELIST if role in owed]
    held_for_human = [role for role in owed if role not in CLERICAL_WHITELIST]
    return {
        "owed": owed,
        "would_serve": would_serve,
        "held_for_human": held_for_human,
        "whitelist": list(CLERICAL_WHITELIST),
        "judicial_never": list(JUDICIAL_NEVER),
    }


def _digest_asof_payload() -> dict[str, Any]:
    scan = scan_learning_evidence()
    pending = [
        str(row.get("ticker") or row.get("window_id") or "")
        for row in (scan.get("pending") or [])
        if isinstance(row, dict)
    ]
    missing = [
        str(row.get("ticker") or "")
        for row in (scan.get("paper_join_missing") or [])
        if isinstance(row, dict)
    ]
    settled = sorted(str(key) for key in (scan.get("settled") or {}))
    return {
        "lane": "learning_lane_15m",
        "framing": "clerical as-of stamp; not the SOURCE digest; not an ADMIT",
        "pending": pending,
        "paper_join_missing": missing,
        "settled": settled,
    }


def _default_do_illustrator() -> Path | None:
    from golf_offshoot.learning_lane_15m.illustrate import render_paper_window_strip

    return render_paper_window_strip()


def _default_do_systems() -> dict[str, str]:
    from golf_offshoot.operator_surface.observability import write_observability_exports

    return write_observability_exports()


def _default_do_digestor() -> Path:
    path = artifact_path("digestor")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_digest_asof_payload(), indent=2) + "\n", encoding="utf-8")
    return path


def _load_json(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) else None


def serve_role(
    role: str,
    *,
    do_work: Callable[[], Any] | None = None,
    root: Path | None = None,
) -> dict[str, Any]:
    """Run one clerical job. Mark served only if the artifact hash changed."""
    role = str(role).strip().lower()
    result: dict[str, Any] = {
        "role": role,
        "ok": False,
        "marked": False,
        "reason": "",
        "before": None,
        "after": None,
        "artifact": "",
    }
    if role not in CLERICAL_WHITELIST:
        result["reason"] = "not on the clerical whitelist"
        return result
    path = artifact_path(role, root=root)
    result["artifact"] = str(path)
    before = file_fingerprint(path)
    before_manifest = _load_json(path) if role == "systems" else None
    result["before"] = before
    workers = {
        "illustrator": _default_do_illustrator,
        "systems": _default_do_systems,
        "digestor": _default_do_digestor,
    }
    worker = do_work or workers[role]
    try:
        worker()
    except Exception as exc:  # noqa: BLE001 — failure stays owed
        result["reason"] = f"work raised {type(exc).__name__}: {exc}"
        return result
    after = file_fingerprint(path)
    result["after"] = after
    if after is None:
        result["reason"] = "artifact missing after work"
        return result
    if after == before:
        result["reason"] = "artifact hash unchanged; role stays owed"
        return result
    if role == "systems":
        after_manifest = _load_json(path)
        reasons = material_publish_reasons(before_manifest, after_manifest or {})
        result["material"] = reasons
        if not reasons:
            result["reason"] = "export was a heartbeat; role stays owed"
            return result
    note = f"artifact hash changed {before} -> {after}"
    mark_roles_served([role], by="runner", note=note, served_kind="auto")
    result["ok"] = True
    result["marked"] = True
    result["reason"] = note
    return result


def serve_owed_roles(
    *,
    state: dict[str, Any] | None = None,
    do_work: dict[str, Callable[[], Any]] | None = None,
    root: Path | None = None,
) -> list[dict[str, Any]]:
    """Dispatch whitelist roles that are owed. Re-reads the kill file between roles."""
    plan = plan_from_wake(state if state is not None else load_wake_state())
    results: list[dict[str, Any]] = []
    hooks = do_work or {}
    for role in plan["would_serve"]:
        if kill_switch_active():
            results.append(
                {
                    "role": role,
                    "ok": False,
                    "marked": False,
                    "reason": "kill switch file appeared mid-pass",
                    "before": None,
                    "after": None,
                }
            )
            break
        results.append(serve_role(role, do_work=hooks.get(role), root=root))
    return results


def run_once(
    *,
    mode: str | None = None,
    now_iso: str | None = None,
    execute: bool = False,
    do_work: dict[str, Callable[[], Any]] | None = None,
    root: Path | None = None,
) -> dict[str, Any]:
    """One runner pass. Re-reads the kill file first. Default dry-run."""
    at = now_iso or isoformat_now()
    entry: dict[str, Any] = {
        "at": at,
        "at_text": format_eastern(at, with_seconds=True),
        "mode": MODE_DRY,
        "armed": False,
        "served": [],
        "failed": [],
        "would_serve": [],
        "held_for_human": [],
        "mark_roles_served_called": False,
        "note": "",
    }
    if kill_switch_active():
        entry["mode"] = MODE_OFF
        entry["note"] = "kill switch file present; runner stopped before reading roles_owed"
        _append_log(entry)
        return entry
    requested = runner_mode(mode)
    if requested == MODE_OFF:
        write_kill_switch()
        entry["mode"] = MODE_OFF
        entry["note"] = "kill switch file written; runner stopped before reading roles_owed"
        _append_log(entry)
        return entry
    if requested == MODE_ARMED and not founder_has_armed():
        entry["armed_refused"] = True
        entry["note"] = (
            "Founder has not armed this runner. Falling back to dry-run. "
            "No role was served."
        )
        requested = MODE_DRY
    state = load_wake_state()
    plan = plan_from_wake(state)
    entry["owed"] = plan["owed"]
    entry["would_serve"] = plan["would_serve"]
    entry["held_for_human"] = plan["held_for_human"]
    entry["artifacts"] = {role: str(artifact_path(role, root=root)) for role in plan["would_serve"]}
    should_execute = execute or (requested == MODE_ARMED and founder_has_armed())
    if should_execute:
        entry["mode"] = MODE_ARMED if founder_has_armed() else "execute"
        entry["armed"] = founder_has_armed()
        served_results = serve_owed_roles(state=state, do_work=do_work, root=root)
        entry["results"] = served_results
        entry["served"] = [row["role"] for row in served_results if row.get("marked")]
        entry["failed"] = [row["role"] for row in served_results if not row.get("marked")]
        entry["mark_roles_served_called"] = any(row.get("marked") for row in served_results)
        entry["note"] = entry["note"] or (
            "serve-on-proof: marked only when artifact hash changed; "
            "unchanged artifacts stay owed"
        )
    else:
        entry["mode"] = MODE_DRY
        entry["note"] = entry["note"] or (
            "dry-run: logged clerical work that would be served; served nothing; "
            "did not call mark_roles_served"
        )
    _append_log(entry)
    return entry


def run_passes(
    n: int,
    *,
    mode: str | None = None,
    execute: bool = False,
    do_work: dict[str, Callable[[], Any]] | None = None,
    root: Path | None = None,
) -> list[dict[str, Any]]:
    """Several passes. Re-reads the kill file at the start of each one."""
    out: list[dict[str, Any]] = []
    for _ in range(max(0, int(n))):
        if kill_switch_active():
            out.append(
                run_once(mode=MODE_DRY, execute=False, do_work=do_work, root=root)
            )
            break
        out.append(run_once(mode=mode, execute=execute, do_work=do_work, root=root))
        if out[-1].get("mode") == MODE_OFF:
            break
    return out


def format_runner_line(entry: dict[str, Any]) -> str:
    mode = entry.get("mode")
    if mode == MODE_OFF:
        return f"learning runner  KILLED  {entry.get('at_text')}  {entry.get('note')}"
    would = ", ".join(entry.get("would_serve") or []) or "none"
    held = ", ".join(entry.get("held_for_human") or []) or "none"
    served = ", ".join(entry.get("served") or []) or "none"
    failed = ", ".join(entry.get("failed") or []) or "none"
    marked = "yes" if entry.get("mark_roles_served_called") else "no"
    return (
        f"learning runner  mode={mode}  would_serve={would}  "
        f"held_for_human={held}  served={served}  failed={failed}  "
        f"mark_roles_served={marked}  {entry.get('at_text')}"
    )
