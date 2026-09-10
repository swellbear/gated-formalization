"""Derived doorbell: should a CoS session start?

The wake already names ``roles_owed``. This block only answers whether a
Chief of Staff turn is owed. It is not a second SoT. The runner may write
it; the runner may not become CoS, open a chat, ADMIT, invent, or push.

needed is true when at least one of A–F holds. If unsure, needed stays true
and the reason says why. Same reason-id set after a CoS closeout stamp is a
heartbeat, not a doorbell. F_continuation is not silenced by that stamp unless
the desk is Status=assigned / lab.
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from golf_offshoot.localtime import isoformat_now, now
from golf_offshoot.repo_paths import repo_root

COS_ROLE = "chief-of-staff"

#: Judicial roles a CoS turn must route. Not clerical. The runner never serves these.
JUDICIAL_ROLES = frozenset({"operator", "lab", "digestor", "soften-critic"})

#: Desk Active-role values that count as a worker covering a job.
WORKER_ROLES = frozenset(
    {
        "operator",
        "lab",
        "digestor",
        "soften-critic",
        "systems",
        "illustrator",
        "validator",
        "hub-ui",
        "lane-15m",
        "digest-figures",
        "critic-invariants",
    }
)

REASON_A_DONE = "A_worker_done"
REASON_A_IDLE = "A_idle_uncovered_judicial"
REASON_B = "B_new_judicial"
REASON_C = "C_clerical_arrears"
REASON_D_WATCH = "D_watch_stuck"
REASON_D_HUB = "D_hub_liveness"
REASON_E = "E_idle_unassigned"
REASON_F = "F_continuation"

REGISTRY_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_RULES.json"
BURNED_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_BURNED_CLASSES.json"
SCORECARD_DIR_REL = Path("golf-offshoot") / "docs"

_BLANK_JOBS = frozenset({"", "—", "-", "–", "–"})

CLERICAL_ARREARS_TICKS = 2
WATCH_STUCK_INTERVALS = 3

_FIELD = re.compile(
    r"^\|\s*(Active role|Status|Job|Updated|Handoff|Waiting on Founder)\s*\|\s*(.*?)\s*\|",
    re.IGNORECASE,
)
_NEXT = re.compile(r"next\s*=\s*(chief-of-staff|cos)\b", re.IGNORECASE)
_ISO = re.compile(r"^\d{4}-\d{2}-\d{2}T")


def parse_desk(text: str) -> dict[str, Any]:
    """Read the live board header and whether the newest thread hands to CoS."""
    fields: dict[str, str] = {}
    for line in (text or "").splitlines():
        match = _FIELD.match(line.strip())
        if match:
            fields[match.group(1).strip().lower()] = match.group(2).strip()
    thread: list[str] = []
    in_thread = False
    for line in (text or "").splitlines():
        if line.startswith("## Thread"):
            in_thread = True
            continue
        if in_thread and line.startswith("## "):
            break
        if in_thread and line.startswith("- "):
            thread.append(line)
    newest = thread[0] if thread else ""
    return {
        "active_role": (fields.get("active role") or "").strip().lower(),
        "status": (fields.get("status") or "").strip().lower(),
        "job": fields.get("job") or "",
        "updated": fields.get("updated") or "",
        "next_cos": bool(_NEXT.search(newest) or _NEXT.search(text or "")),
        "newest_thread": newest,
    }


def _parse_iso(value: Any) -> datetime | None:
    text = str(value or "").strip()
    if not text:
        return None
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def _role(entry: dict[str, Any]) -> str:
    return str(entry.get("role") or "").strip().lower()


def _reason(rid: str, detail: str) -> dict[str, str]:
    return {"id": rid, "detail": detail}


def _job_is_blank(job: str) -> bool:
    return str(job or "").strip() in _BLANK_JOBS


def desk_assigned_lab(desk: dict[str, Any]) -> bool:
    return desk.get("status") == "assigned" and desk.get("active_role") == "lab"


def unoperated_lab_proposed(wake: dict[str, Any] | None) -> bool:
    """True when a Lab PROPOSED is sitting for Operator (not a new invent)."""
    for entry in (wake or {}).get("roles_owed") or []:
        for reason in entry.get("reasons") or []:
            text = str(reason or "").strip().lower()
            if text.startswith("lab_proposed"):
                return True
    return False


def _load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _burned_class_ids(*, root: Path | None = None) -> set[str]:
    payload = _load_json((root or repo_root()) / BURNED_REL)
    out: set[str] = set()
    for row in payload.get("classes") or []:
        if not isinstance(row, dict) or not row.get("burned"):
            continue
        cid = str(row.get("id") or "").strip()
        if cid:
            out.add(cid)
        for alias in row.get("aliases") or []:
            text = str(alias or "").strip()
            if text:
                out.add(text)
    return out


def _l1_scorecard_exists(rule_id: str, *, root: Path | None = None) -> bool:
    docs = (root or repo_root()) / SCORECARD_DIR_REL
    return (docs / f"LEARNING_LANE_15M_SCORECARD_{rule_id}_L1.json").is_file()


def live_selecting_rule_ids(
    *,
    root: Path | None = None,
    registry: dict[str, Any] | None = None,
) -> list[str]:
    """Executing selection rules that are still on trial (unscored, unburned).

    Favorite L1 PARK is dead: it has an L1 scorecard and its class is burned.
    ``R-SKIP-COINFLIP`` ``execution: false`` is not live.
    """
    payload = registry if registry is not None else _load_json((root or repo_root()) / REGISTRY_REL)
    burned = _burned_class_ids(root=root)
    live: list[str] = []
    for row in payload.get("rules") or []:
        if not isinstance(row, dict):
            continue
        if not row.get("execution") or not row.get("selects"):
            continue
        if str(row.get("kind") or "").strip().lower() != "selection":
            continue
        rid = str(row.get("id") or "").strip()
        if not rid:
            continue
        class_id = str(row.get("class") or "").strip()
        if rid in burned or class_id in burned:
            continue
        if _l1_scorecard_exists(rid, root=root):
            continue
        live.append(rid)
    return live


def gym_is_starved(
    desk: dict[str, Any],
    wake: dict[str, Any] | None,
    *,
    root: Path | None = None,
    registry: dict[str, Any] | None = None,
    live_trial_ids: list[str] | None = None,
) -> bool:
    """True when CoS should assign Lab: idle gym, no live trial, no un-operated PROPOSED."""
    status = str(desk.get("status") or "").strip().lower()
    role = str(desk.get("active_role") or "").strip().lower()
    job = str(desk.get("job") or "")
    assigned_worker = status == "assigned" and role in WORKER_ROLES
    if assigned_worker:
        return False
    cos_blank = role in {COS_ROLE, "cos"} and _job_is_blank(job)
    if status not in {"idle", ""} and not cos_blank:
        return False
    if unoperated_lab_proposed(wake):
        return False
    if live_trial_ids is not None:
        live = list(live_trial_ids)
    else:
        live = live_selecting_rule_ids(root=root, registry=registry)
    return not live


def _watch_stuck(watch: dict[str, Any], previous_watch: dict[str, Any] | None) -> str:
    """Empty string if healthy; a detail if the watch looks frozen."""
    watch = watch or {}
    interval = 90.0
    try:
        interval = float(watch.get("interval_s") or 90.0)
    except (TypeError, ValueError):
        interval = 90.0
    running = bool(watch.get("running"))
    last_at = _parse_iso(watch.get("last_at"))
    if running and last_at is not None:
        age = (now() - last_at).total_seconds()
        if age > interval * WATCH_STUCK_INTERVALS:
            return (
                f"watch claims running but last cycle is {age:.0f}s old "
                f"(budget {interval * WATCH_STUCK_INTERVALS:.0f}s)"
            )
    if previous_watch and running:
        if str(watch.get("cycles")) == str(previous_watch.get("cycles")) and str(
            watch.get("last_at")
        ) == str(previous_watch.get("last_at")):
            return (
                f"watch cycles stuck at {watch.get('cycles')} "
                f"last_at={watch.get('last_at')}"
            )
    if not running and watch:
        return "watch is not running"
    return ""


def compute_crew_tick(
    state: dict[str, Any] | None,
    *,
    desk_text: str = "",
    leave_off_text: str = "",
    hub_ok: bool | None = None,
    previous_watch: dict[str, Any] | None = None,
    handled_reason_ids: list[str] | None = None,
    root: Path | None = None,
    registry: dict[str, Any] | None = None,
    live_trial_ids: list[str] | None = None,
) -> dict[str, Any]:
    """Derive ``crew_tick`` from the wake, the desk, and the last CoS stamp.

    ``handled_reason_ids`` is the set the last closeout said it handled. The
    same set on a later 90s pass is quiet, not a re-ring.
    """
    state = state or {}
    previous = state.get("crew_tick") if isinstance(state.get("crew_tick"), dict) else {}
    handled = list(handled_reason_ids or previous.get("handled_reason_ids") or [])
    handled = [str(x) for x in handled]
    desk = parse_desk(desk_text)
    owed = list(state.get("roles_owed") or [])
    judicial = [e for e in owed if _role(e) in JUDICIAL_ROLES]
    try:
        from golf_offshoot.learning_lane_15m.runner import CLERICAL_WHITELIST
    except Exception:  # noqa: BLE001 — still decide; whitelist lives on disk
        CLERICAL_WHITELIST = ()
    clerical_arrears = []
    for entry in owed:
        if _role(entry) not in CLERICAL_WHITELIST:
            continue
        try:
            ticks = int(entry.get("ticks_unanswered") or 0)
        except (TypeError, ValueError):
            ticks = 0
        if ticks > CLERICAL_ARREARS_TICKS:
            clerical_arrears.append(entry)

    reasons: list[dict[str, str]] = []
    status = desk["status"]
    role = desk["active_role"]
    assigned_worker = status == "assigned" and role in WORKER_ROLES

    if status == "done" and (desk["next_cos"] or role in WORKER_ROLES):
        reasons.append(
            _reason(
                REASON_A_DONE,
                f"desk Status=done Active role={role or '?'} "
                f"{'next=chief-of-staff' if desk['next_cos'] else 'worker finished'}",
            )
        )

    uncovered = [
        e
        for e in judicial
        if not (assigned_worker and _role(e) == role)
    ]
    if status in {"idle", ""} and uncovered and role not in WORKER_ROLES:
        named = ", ".join(sorted({_role(e) for e in uncovered}))
        reasons.append(
            _reason(
                REASON_A_IDLE,
                f"desk Status={status or 'unset'} and judicial owe {named} is uncovered",
            )
        )

    last_cos_at = _parse_iso(previous.get("last_cos_at"))
    new_judicial = []
    for entry in judicial:
        since = _parse_iso(entry.get("owed_since"))
        if last_cos_at is None:
            new_judicial.append(entry)
            continue
        if since is None or since > last_cos_at:
            new_judicial.append(entry)
    if new_judicial and not (assigned_worker and all(_role(e) == role for e in new_judicial)):
        named = ", ".join(sorted({_role(e) for e in new_judicial}))
        reasons.append(
            _reason(
                REASON_B,
                f"judicial owe {named} appeared since last CoS closeout "
                f"({previous.get('last_cos_at') or 'none'})",
            )
        )

    for entry in clerical_arrears:
        reasons.append(
            _reason(
                REASON_C,
                f"{_role(entry)} owed {entry.get('ticks_unanswered')} ticks "
                f"(>{CLERICAL_ARREARS_TICKS})",
            )
        )

    stuck = _watch_stuck(state.get("watch") or {}, previous_watch)
    if stuck:
        reasons.append(_reason(REASON_D_WATCH, stuck))

    if hub_ok is False:
        reasons.append(_reason(REASON_D_HUB, "honesty hub-tree box would fail"))

    leave = leave_off_text or ""
    job = desk["job"]
    idle_unassigned = status == "idle" and (
        bool(uncovered)
        or "lab not assigned" in f"{job} {leave}".lower()
        or "next=" in leave.lower()
    )
    if idle_unassigned:
        reasons.append(
            _reason(
                REASON_E,
                "desk Status=idle while a judicial owe or leave-off Next is still open",
            )
        )

    if gym_is_starved(
        desk,
        state,
        root=root,
        registry=registry,
        live_trial_ids=live_trial_ids,
    ):
        reasons.append(
            _reason(
                REASON_F,
                "gym has no live 15m trial; CoS assigns Lab under the invent contract",
            )
        )

    # Dedup by id, keep first detail.
    seen: set[str] = set()
    unique: list[dict[str, str]] = []
    for row in reasons:
        if row["id"] in seen:
            continue
        seen.add(row["id"])
        unique.append(row)
    reason_ids = [row["id"] for row in unique]

    if assigned_worker and not clerical_arrears and not stuck and hub_ok is not False:
        # Healthy assigned worker: drop A/E/F noise. B stays if a *different*
        # judicial owe is new; C and D already excluded.
        unique = [
            row
            for row in unique
            if row["id"] not in {REASON_A_DONE, REASON_A_IDLE, REASON_E, REASON_F}
        ]
        if not new_judicial or all(_role(e) == role for e in new_judicial):
            unique = [row for row in unique if row["id"] != REASON_B]
        reason_ids = [row["id"] for row in unique]

    handled_quiet = list(handled)
    if REASON_F in reason_ids and not desk_assigned_lab(desk):
        handled_quiet = [x for x in handled_quiet if x != REASON_F]

    if reason_ids and handled_quiet and set(reason_ids) <= set(handled_quiet):
        # Same why, or a subset after the stamp itself retired B. Not a new doorbell.
        needed = False
        quiet = True
    else:
        needed = bool(reason_ids)
        quiet = not needed

    since = ""
    for entry in judicial + clerical_arrears:
        stamp = str(entry.get("owed_since") or "")
        if stamp and (not since or stamp < since):
            since = stamp
    if not since and unique:
        since = str(state.get("updated_at") or "")

    return {
        "needed": needed,
        "quiet": quiet,
        "reasons": unique,
        "reason_ids": reason_ids,
        "since": since,
        "last_cos_at": previous.get("last_cos_at") or "",
        "last_cos_commit": previous.get("last_cos_commit") or "",
        "handled_reason_ids": handled,
        "contract": (
            "crew_tick is a doorbell. It does not mark a role served, "
            "open a chat, ADMIT, invent, or push."
        ),
    }


def read_desk_text(*, root: Path | None = None) -> str:
    path = (root or repo_root()) / "docs" / "agents" / "DESK.md"
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def read_leave_off_text(*, root: Path | None = None) -> str:
    path = (root or repo_root()) / "docs" / "AGENT_LEAVE_OFF.md"
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def attach_crew_tick(
    state: dict[str, Any],
    *,
    desk_text: str | None = None,
    leave_off_text: str | None = None,
    hub_ok: bool | None = None,
    previous_watch: dict[str, Any] | None = None,
    root: Path | None = None,
) -> dict[str, Any]:
    """Write ``crew_tick`` onto a wake state. Does not persist."""
    if desk_text is None:
        desk_text = read_desk_text(root=root)
    if leave_off_text is None:
        leave_off_text = read_leave_off_text(root=root)
    if hub_ok is None:
        try:
            from golf_offshoot.learning_lane_15m.honesty import hub_trees

            hub_ok = bool(hub_trees().get("ok"))
        except Exception:  # noqa: BLE001 — blindness is a doorbell
            hub_ok = False
    # Carry last_cos_* by leaving them on state["crew_tick"] before compute.
    state["crew_tick"] = compute_crew_tick(
        state,
        desk_text=desk_text,
        leave_off_text=leave_off_text,
        hub_ok=hub_ok,
        previous_watch=previous_watch,
        root=root,
    )
    return state["crew_tick"]


def stamp_cos_closeout(
    *,
    commit: str,
    reason_ids: list[str] | None = None,
    at: str | None = None,
    root: Path | None = None,
) -> dict[str, Any] | None:
    """CoS writes the reason set it handled so the next 90s pass stays quiet.

    The runner must not call this. It does not mark CoS served.
    If the wake is missing (cloud clone) this returns None; write the desk
    ``last_cos_*`` table anyway.
    """
    from golf_offshoot.learning_lane_15m.wake_io import load_wake_state, save_wake_state

    state = load_wake_state()
    if state is None:
        return None
    current = state.get("crew_tick") if isinstance(state.get("crew_tick"), dict) else {}
    handled = [str(x) for x in (reason_ids if reason_ids is not None else current.get("reason_ids") or [])]
    desk = parse_desk(read_desk_text(root=root))
    if not desk_assigned_lab(desk):
        handled = [x for x in handled if x != REASON_F]
    carried = {
        "last_cos_at": at or isoformat_now(),
        "last_cos_commit": str(commit or ""),
        "handled_reason_ids": sorted(set(handled)),
    }
    state["crew_tick"] = {**current, **carried}
    attach_crew_tick(state, root=root)
    # Preserve the stamp even if attach recomputed last_cos from an empty previous.
    state["crew_tick"]["last_cos_at"] = carried["last_cos_at"]
    state["crew_tick"]["last_cos_commit"] = carried["last_cos_commit"]
    state["crew_tick"]["handled_reason_ids"] = carried["handled_reason_ids"]
    # Re-evaluate quiet against the stamp we just wrote.
    state["crew_tick"] = compute_crew_tick(
        state,
        desk_text=read_desk_text(root=root),
        leave_off_text=read_leave_off_text(root=root),
        hub_ok=True,
        handled_reason_ids=carried["handled_reason_ids"],
        root=root,
    )
    state["crew_tick"]["last_cos_at"] = carried["last_cos_at"]
    state["crew_tick"]["last_cos_commit"] = carried["last_cos_commit"]
    state["crew_tick"]["handled_reason_ids"] = carried["handled_reason_ids"]
    save_wake_state(state)
    return state["crew_tick"]


def format_crew_tick(block: dict[str, Any] | None) -> list[str]:
    block = block or {}
    flag = "NEEDED" if block.get("needed") else "quiet"
    lines = [
        f"crew_tick  needed={str(bool(block.get('needed'))).lower()}  {flag}  "
        f"quiet={str(bool(block.get('quiet'))).lower()}"
    ]
    for row in block.get("reasons") or []:
        lines.append(f"  {row.get('id')} — {row.get('detail')}")
    if block.get("last_cos_at") or block.get("last_cos_commit"):
        lines.append(
            f"  last_cos_at={block.get('last_cos_at') or '—'}  "
            f"commit={block.get('last_cos_commit') or '—'}"
        )
    if not block.get("reasons") and not block.get("needed"):
        lines.append("  no doorbell")
    return lines
