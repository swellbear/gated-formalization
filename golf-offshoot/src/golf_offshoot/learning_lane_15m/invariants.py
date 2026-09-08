"""Invariant suite for ``learning_lane_15m``.

The ratchet: every flaw found by analysis becomes a permanent check here, so
it cannot recur silently. Each check writes a machine-readable result and is
printed on the tick. A failing invariant is loud, and prose never satisfies
one — a check passes because a file says so or it does not pass.

Nothing here Softens, ADMITs, scores a rule, or marks a role served. It reads
files and reports.

Seeded with the four failures that were live and invisible on 2026-09-08:

1. ``digest_matches_ledger`` — the SOURCE digest headline drifted $1.24 behind
   the live ledger for roughly ninety minutes with nothing saying so.
2. ``process_matches_disk`` — the hub kept serving a pre-#176 ``ROLE_ORDER``
   and whitelist after the code on disk changed. Roles silently stopped
   self-serving and the desk looked normal.
3. ``watch_is_collecting`` — a re-exec that fails to come back resets the
   cycle counter and stops collection with no visible symptom.
4. ``clerical_roles_clear`` — a whitelisted role owed for many ticks is either
   broken or misfiled as clerical. Either way it is not clerical in practice.
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from golf_offshoot.learning_lane_15m.paths import latest_dir_15m
from golf_offshoot.localtime import format_eastern, isoformat_now, now

INVARIANTS_NAME = "invariants.json"

PASS = "PASS"
FAIL = "FAIL"

#: A whitelisted role is served by the runner on the pass after it is named.
#: Two watch intervals is already generous; beyond that it is not clerical.
CLERICAL_ARREARS_TICKS = 2

#: The watch writes ``watch.json`` every cycle. Three missed cycles is a stop,
#: not jitter.
LIVENESS_TICKS = 3


def invariants_path() -> Path:
    return latest_dir_15m() / INVARIANTS_NAME


def load_invariants() -> dict[str, Any] | None:
    path = invariants_path()
    if not path.is_file():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return payload if isinstance(payload, dict) else None


def _check(
    check_id: str,
    title: str,
    ok: bool,
    detail: str,
    evidence: dict[str, Any],
) -> dict[str, Any]:
    return {
        "id": check_id,
        "title": title,
        "state": PASS if ok else FAIL,
        "detail": detail,
        "evidence": evidence,
    }


def _as_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _money_equal(left: Any, right: Any) -> bool:
    a, b = _as_float(left), _as_float(right)
    if a is None or b is None:
        return False
    return abs(a - b) < 0.005


# ------------------------------------------------------------------ 1. digest

_DIGEST_BANKROLL = re.compile(r"`bankroll`\s*([-+]?\d+(?:\.\d+)?)")
_DIGEST_PNL = re.compile(r"`betting_pnl`\s*([-+]?\d+(?:\.\d+)?)")


def check_digest_matches_ledger(*, root: Path | None = None) -> dict[str, Any]:
    """SOURCE digest headline figures must equal the live ledger.

    The digest is generated, so any gap means it was not regenerated after the
    book moved. A digest that disagrees with the book it cites is a false
    published figure, not a stale one.
    """
    from golf_offshoot.learning_lane_15m.digest import collect_figures, digest_path

    title = "SOURCE digest headline equals the live ledger"
    path = digest_path(root=root)
    if not path.is_file():
        return _check(
            "digest_matches_ledger",
            title,
            False,
            "no SOURCE digest on this tree",
            {"digest_path": str(path)},
        )
    try:
        figures = collect_figures(root=root)
    except Exception as exc:  # noqa: BLE001 — an unreadable book is a failure
        return _check(
            "digest_matches_ledger",
            title,
            False,
            f"could not read the live ledger: {type(exc).__name__}: {exc}",
            {"digest_path": str(path)},
        )
    text = path.read_text(encoding="utf-8", errors="replace")
    bank_match = _DIGEST_BANKROLL.search(text)
    pnl_match = _DIGEST_PNL.search(text)
    evidence = {
        "digest_path": str(path),
        "digest_bankroll": bank_match.group(1) if bank_match else None,
        "digest_betting_pnl": pnl_match.group(1) if pnl_match else None,
        "ledger_bankroll": figures.get("bankroll"),
        "ledger_betting_pnl": figures.get("betting_pnl"),
        "digest_evidence_asof": figures.get("journal_generated_at"),
    }
    if bank_match is None or pnl_match is None:
        return _check(
            "digest_matches_ledger",
            title,
            False,
            "digest does not state a bankroll and betting_pnl headline",
            evidence,
        )
    bank_ok = _money_equal(bank_match.group(1), figures.get("bankroll"))
    pnl_ok = _money_equal(pnl_match.group(1), figures.get("betting_pnl"))
    if bank_ok and pnl_ok:
        return _check(
            "digest_matches_ledger",
            title,
            True,
            (
                f"digest bankroll {bank_match.group(1)} / betting_pnl "
                f"{pnl_match.group(1)} equal the live ledger"
            ),
            evidence,
        )
    drift = _as_float(figures.get("bankroll"))
    digest_bank = _as_float(bank_match.group(1))
    gap = None if drift is None or digest_bank is None else round(drift - digest_bank, 2)
    evidence["bankroll_drift"] = gap
    return _check(
        "digest_matches_ledger",
        title,
        False,
        (
            f"digest says bankroll {bank_match.group(1)} / betting_pnl "
            f"{pnl_match.group(1)}; live ledger says {figures.get('bankroll')} / "
            f"{figures.get('betting_pnl')} (drift {gap}). Regenerate via "
            "digest-figures; do not hand-edit the figures"
        ),
        evidence,
    )


# ----------------------------------------------------------------- 2. process


def _disk_role_config() -> dict[str, list[str]]:
    """The role config as it exists in the source this process just imported."""
    from golf_offshoot.learning_lane_15m.learn import ROLE_ORDER
    from golf_offshoot.learning_lane_15m.runner import (
        CLERICAL_WHITELIST,
        JUDICIAL_NEVER,
    )

    return {
        "role_order": list(ROLE_ORDER),
        "clerical_whitelist": list(CLERICAL_WHITELIST),
        "judicial_never": list(JUDICIAL_NEVER),
    }


def runtime_stamp() -> dict[str, Any]:
    """What the process calling this actually loaded.

    The watch writes this into ``watch.json`` every cycle. A fresh process
    reading it can then tell whether the long-lived loop is running the code
    that is on disk.
    """
    import os

    from golf_offshoot.operator_surface.reload import read_git_tip

    stamp: dict[str, Any] = {"pid": os.getpid(), "stamped_at": isoformat_now()}
    stamp.update(_disk_role_config())
    try:
        stamp["git_tip"] = read_git_tip()
    except Exception:  # noqa: BLE001 — a missing git dir is not fatal here
        stamp["git_tip"] = ""
    return stamp


def check_process_matches_disk(watch_status: dict[str, Any] | None = None) -> dict[str, Any]:
    """The running loop's role config must equal the config on disk.

    A stale process is an honesty defect, not merely a freshness one: roles
    stop self-serving and nothing on the desk says why.
    """
    title = "running loop's role config equals the code on disk"
    if watch_status is None:
        from golf_offshoot.learning_lane_15m.watch import load_watch_status

        watch_status = load_watch_status()
    stamped = watch_status.get("runtime")
    disk = _disk_role_config()
    if not isinstance(stamped, dict) or not stamped.get("role_order"):
        return _check(
            "process_matches_disk",
            title,
            False,
            (
                "the watch has stamped no runtime config, so a stale loop cannot "
                "be ruled out. Restart is proven only by a stamp"
            ),
            {"disk": disk, "running": bool(watch_status.get("running"))},
        )
    divergent = {
        key: {"process": list(stamped.get(key) or []), "disk": value}
        for key, value in disk.items()
        if list(stamped.get(key) or []) != value
    }
    evidence = {
        "process_pid": stamped.get("pid"),
        "process_git_tip": stamped.get("git_tip"),
        "process_stamped_at": stamped.get("stamped_at"),
        "disk": disk,
        "divergent": divergent,
    }
    if not divergent:
        return _check(
            "process_matches_disk",
            title,
            True,
            f"loop pid {stamped.get('pid')} is running the role config on disk",
            evidence,
        )
    return _check(
        "process_matches_disk",
        title,
        False,
        (
            f"loop pid {stamped.get('pid')} is running stale code: "
            f"{', '.join(sorted(divergent))} differ from disk. Roles named by the "
            "old config cannot self-serve"
        ),
        evidence,
    )


# ---------------------------------------------------------------- 3. liveness


def _parse_iso(value: Any) -> datetime | None:
    text = str(value or "").strip()
    if not text:
        return None
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def check_watch_is_collecting(
    watch_status: dict[str, Any] | None = None,
    *,
    previous: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """The watch must still be writing cycles.

    A re-exec that does not come back leaves a plausible-looking status file
    with a frozen clock. Cycle count alone cannot see that, because a restart
    legitimately resets it to zero — the wall clock on the last cycle can.
    """
    title = "watch is still collecting cycles"
    if watch_status is None:
        from golf_offshoot.learning_lane_15m.watch import load_watch_status

        watch_status = load_watch_status()
    running = bool(watch_status.get("running"))
    interval = _as_float(watch_status.get("interval_s")) or 90.0
    cycles = watch_status.get("cycles")
    last_at = watch_status.get("last_at") or watch_status.get("started_at")
    stamped = _parse_iso(last_at)
    budget = interval * LIVENESS_TICKS
    age_s = None
    if stamped is not None:
        age_s = round((now() - stamped).total_seconds(), 1)
    prev_cycles = None
    if isinstance(previous, dict):
        prev_check = next(
            (c for c in previous.get("checks") or [] if c.get("id") == "watch_is_collecting"),
            None,
        )
        if prev_check:
            prev_cycles = (prev_check.get("evidence") or {}).get("cycles")
    evidence = {
        "running": running,
        "cycles": cycles,
        "previous_cycles": prev_cycles,
        "interval_s": interval,
        "last_at": last_at,
        "age_s": age_s,
        "budget_s": budget,
    }
    if not running:
        return _check(
            "watch_is_collecting",
            title,
            False,
            "watch reports running=false; the lane is not collecting",
            evidence,
        )
    if stamped is None:
        return _check(
            "watch_is_collecting",
            title,
            False,
            "watch reports running but stamped no last cycle time",
            evidence,
        )
    if age_s is not None and age_s > budget:
        return _check(
            "watch_is_collecting",
            title,
            False,
            (
                f"last cycle was {age_s}s ago, past {LIVENESS_TICKS} intervals "
                f"({budget}s). The loop claims running and is not collecting"
            ),
            evidence,
        )
    note = f"cycle {cycles} stamped {age_s}s ago, inside {budget}s"
    if prev_cycles is not None and _as_float(cycles) is not None:
        current_f = _as_float(cycles)
        prev_f = _as_float(prev_cycles)
        if prev_f is not None and current_f is not None and current_f < prev_f:
            note += f"; counter reset {prev_cycles} -> {cycles} (a re-exec came back)"
    return _check("watch_is_collecting", title, True, note, evidence)


# ----------------------------------------------------------------- 4. arrears


def check_clerical_roles_clear(
    state: dict[str, Any] | None = None,
    *,
    watch_status: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """A whitelisted role owed for many ticks is broken or misfiled.

    The runner serves the whitelist on the pass after a role is named. Arrears
    mean the worker is failing, the proof artifact never moves, or the role is
    not clerical in practice.
    """
    from golf_offshoot.learning_lane_15m.runner import CLERICAL_WHITELIST

    title = "no whitelisted role is in arrears"
    if state is None:
        from golf_offshoot.learning_lane_15m.learn import load_wake_state

        state = load_wake_state()
    if watch_status is None:
        from golf_offshoot.learning_lane_15m.watch import load_watch_status

        watch_status = load_watch_status()
    interval = _as_float(watch_status.get("interval_s")) or 90.0
    budget = interval * CLERICAL_ARREARS_TICKS
    arrears = []
    for entry in (state or {}).get("roles_owed") or []:
        role = str(entry.get("role") or "").strip().lower()
        if role not in CLERICAL_WHITELIST:
            continue
        age = _as_float(entry.get("age_s"))
        if age is not None and age > budget:
            arrears.append(
                {
                    "role": role,
                    "age_s": age,
                    "age_text": entry.get("age_text"),
                    "owed_since": entry.get("owed_since"),
                }
            )
    evidence = {
        "whitelist": list(CLERICAL_WHITELIST),
        "budget_s": budget,
        "arrears": arrears,
    }
    if not arrears:
        return _check(
            "clerical_roles_clear",
            title,
            True,
            f"no whitelisted role owed longer than {CLERICAL_ARREARS_TICKS} ticks ({budget}s)",
            evidence,
        )
    named = ", ".join(f"{row['role']} {row['age_text']}" for row in arrears)
    return _check(
        "clerical_roles_clear",
        title,
        False,
        (
            f"whitelisted role in arrears past {budget}s: {named}. Either the "
            "worker is failing or the role is not clerical"
        ),
        evidence,
    )


# --------------------------------------------------------------------- runner


def run_invariants(
    *,
    root: Path | None = None,
    state: dict[str, Any] | None = None,
    watch_status: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run every check. Read-only; writes nothing but its own report."""
    if watch_status is None:
        from golf_offshoot.learning_lane_15m.watch import load_watch_status

        watch_status = load_watch_status()
    previous = load_invariants()
    checks = [
        check_digest_matches_ledger(root=root),
        check_process_matches_disk(watch_status),
        check_watch_is_collecting(watch_status, previous=previous),
        check_clerical_roles_clear(state, watch_status=watch_status),
    ]
    failing = [c["id"] for c in checks if c["state"] != PASS]
    return {
        "schema": 1,
        "lane": "learning_lane_15m",
        "ran_at": isoformat_now(),
        "framing": (
            "Mechanical checks over files. Not an ADMIT, not a score, not a "
            "verdict. A failing check is not satisfied by prose."
        ),
        "passed": not failing,
        "failing": failing,
        "checks": checks,
    }


def write_invariants(payload: dict[str, Any] | None = None, **kwargs: Any) -> Path:
    """Run (or accept) the suite and persist it. This is the proof artifact."""
    report = payload if payload is not None else run_invariants(**kwargs)
    dest = invariants_path()
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(report, indent=2, default=str) + "\n", encoding="utf-8")
    return dest


def format_invariants(payload: dict[str, Any] | None) -> list[str]:
    """Tick lines. A failure names itself; it does not hide in a summary count."""
    if not payload:
        return ["invariants: not run on this tree yet"]
    checks = payload.get("checks") or []
    failing = [c for c in checks if c.get("state") != PASS]
    head = (
        f"invariants ({len(checks)})  "
        f"{'ALL PASS' if not failing else str(len(failing)) + ' FAILING'}  "
        f"ran {format_eastern(payload.get('ran_at'), with_seconds=True)}"
    )
    lines = [head]
    for check in checks:
        mark = "PASS" if check.get("state") == PASS else "FAIL"
        lines.append(f"  [{mark}] {check.get('id')} — {check.get('title')}")
        if check.get("state") != PASS:
            lines.append(f"         {check.get('detail')}")
    return lines
