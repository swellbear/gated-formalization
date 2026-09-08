"""Clerical learning runner. Dry-run until Founder arms it.

Reads ``roles_owed`` and may serve only a named whitelist of clerical jobs:
Illustrator re-render, Systems publish, Digestor digest. Judicial work
(ADMIT, RUN-ONLY, closing a park, lifting the HOLD) is never on the list.

Default mode is dry-run: log what would be served, serve nothing, never call
``mark_roles_served``. ``off`` is the kill switch — stop before inspecting owed
roles. ``armed`` is refused until Founder ships an explicit arm; the process
falls back to dry-run rather than serving.

Serve-on-proof (when later armed): mark a role served only after the artifact
it was meant to produce actually changed on disk. Exit code 0 is not proof.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from golf_offshoot.learning_lane_15m.learn import load_wake_state
from golf_offshoot.learning_lane_15m.paths import latest_dir_15m
from golf_offshoot.localtime import format_eastern, isoformat_now

MODE_DRY = "dry-run"
MODE_OFF = "off"
MODE_ARMED = "armed"
ENV_MODE = "GOLF_OFFSHOOT_LEARNING_RUNNER"

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

DIGEST_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_SOURCE_DIGEST.md"
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


def _artifact_for(role: str) -> str:
    return {
        "illustrator": str(PNG_REL),
        "systems": str(MANIFEST_REL),
        "digestor": str(DIGEST_REL),
    }.get(role, "")


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


def run_once(*, mode: str | None = None, now_iso: str | None = None) -> dict[str, Any]:
    """One runner pass. Default dry-run. Never writes a claim."""
    resolved = runner_mode(mode)
    at = now_iso or isoformat_now()
    entry: dict[str, Any] = {
        "at": at,
        "at_text": format_eastern(at, with_seconds=True),
        "mode": resolved,
        "armed": False,
        "served": [],
        "would_serve": [],
        "held_for_human": [],
        "mark_roles_served_called": False,
        "note": "",
    }
    if resolved == MODE_OFF:
        entry["note"] = "kill switch: runner stopped before reading roles_owed"
        _append_log(entry)
        return entry
    if resolved == MODE_ARMED:
        entry["note"] = (
            "Founder has not armed this runner. Falling back to dry-run. "
            "No role was served."
        )
        resolved = MODE_DRY
        entry["mode"] = MODE_DRY
        entry["armed_refused"] = True
    state = load_wake_state()
    plan = plan_from_wake(state)
    entry["owed"] = plan["owed"]
    entry["would_serve"] = plan["would_serve"]
    entry["held_for_human"] = plan["held_for_human"]
    entry["artifacts"] = {role: _artifact_for(role) for role in plan["would_serve"]}
    entry["note"] = entry["note"] or (
        "dry-run: logged clerical work that would be served; served nothing; "
        "did not call mark_roles_served"
    )
    _append_log(entry)
    return entry


def format_runner_line(entry: dict[str, Any]) -> str:
    mode = entry.get("mode")
    if mode == MODE_OFF:
        return f"learning runner  KILLED  {entry.get('at_text')}  {entry.get('note')}"
    would = ", ".join(entry.get("would_serve") or []) or "none"
    held = ", ".join(entry.get("held_for_human") or []) or "none"
    return (
        f"learning runner  mode={mode}  would_serve={would}  "
        f"held_for_human={held}  served=none  "
        f"mark_roles_served=no  {entry.get('at_text')}"
    )
