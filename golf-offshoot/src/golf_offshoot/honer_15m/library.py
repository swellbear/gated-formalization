"""Durable exam library. Labels compound. Pnl does not rank."""

from __future__ import annotations

import json
from typing import Any

from golf_offshoot.honer_15m.paths import assert_honer_path, library_path
from golf_offshoot.honer_15m.policy import (
    FAMILY_RICH,
    STEP_RULE,
    knob_vector,
    vectors_equal,
)
from golf_offshoot.localtime import now

OUTCOMES = ("parked", "completed_dead", "completed_unscored", "search_untestable")
RETIRE_OUTCOMES = frozenset({"parked", "completed_dead", "search_untestable"})


def default_library() -> dict[str, Any]:
    return {
        "step_rule": STEP_RULE,
        "active_family": FAMILY_RICH,
        "catalog_exhausted": False,
        "retired": [],
        "spent": [],
        "seed_theta": None,
        "rows": [],
        "updated_at": now().isoformat(),
    }


def load_library() -> dict[str, Any]:
    path = library_path()
    if not path.is_file():
        payload = default_library()
        save_library(payload)
        return payload
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload.setdefault("step_rule", STEP_RULE)
    payload.setdefault("active_family", FAMILY_RICH)
    payload.setdefault("catalog_exhausted", False)
    payload.setdefault("retired", [])
    payload.setdefault("spent", [])
    payload.setdefault("seed_theta", None)
    payload.setdefault("rows", [])
    return payload


def save_library(payload: dict[str, Any]) -> None:
    path = library_path()
    assert_honer_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = dict(payload)
    data["updated_at"] = now().isoformat()
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def search_is_parked(lib: dict[str, Any] | None = None) -> bool:
    """True when library.json catalog_exhausted is true. No new search fills."""
    payload = lib if lib is not None else load_library()
    return payload.get("catalog_exhausted") is True


def hunts_cannot_freeze() -> bool:
    """True when exam is closed, freeze cannot fire, and this hunt cannot continue.

    Gym has no clip-grid. File labels only. A next catalog family still queued
    (family 2 after a family-1 exam) keeps hunting. Does not read ledgers or exam d.
    """
    from golf_offshoot.honer_15m.catalog import next_family
    from golf_offshoot.honer_15m.freeze import exam_is_open, freeze_ready
    from golf_offshoot.honer_15m.theta import current_vector, load_theta

    if exam_is_open():
        return False
    if freeze_ready():
        return False
    st = load_theta()
    lib = load_library()
    active = str(st.get("active_family") or lib.get("active_family") or FAMILY_RICH)
    if next_family(active) is not None:
        return False
    vector = current_vector(st)
    if not is_retired(vector, lib) and not is_spent(vector, lib):
        return False
    return True


def mark_catalog_exhausted() -> dict[str, Any]:
    """Stamp catalog_exhausted from files when the two-item catalog cannot hunt.

    Does not date a third family. Does not peek exam pnl. Does not park while
    family 2 is still the next file-order family.
    """
    from golf_offshoot.honer_15m.catalog import catalog_ids, next_family
    from golf_offshoot.honer_15m.freeze import exam_is_open

    payload = load_library()
    if payload.get("catalog_exhausted") is True:
        return payload
    ids = catalog_ids()
    last = ids[-1] if ids else ""
    if last and next_family(last) is not None:
        return payload
    if exam_is_open():
        return payload
    if not hunts_cannot_freeze():
        return payload
    payload["catalog_exhausted"] = True
    save_library(payload)
    return payload


def _in_set(bucket: list[Any], vector: dict[str, Any]) -> bool:
    for item in bucket:
        if isinstance(item, dict) and vectors_equal(item, vector):
            return True
    return False


def is_retired(vector: dict[str, Any], lib: dict[str, Any] | None = None) -> bool:
    payload = lib if lib is not None else load_library()
    return _in_set(list(payload.get("retired") or []), vector)


def is_spent(vector: dict[str, Any], lib: dict[str, Any] | None = None) -> bool:
    payload = lib if lib is not None else load_library()
    return _in_set(list(payload.get("spent") or []), vector)


def last_unscored_seed_theta(lib: dict[str, Any] | None = None) -> float | None:
    payload = lib if lib is not None else load_library()
    for row in reversed(list(payload.get("rows") or [])):
        if not isinstance(row, dict):
            continue
        if row.get("outcome") != "completed_unscored":
            continue
        knobs = row.get("knobs") or {}
        if knobs.get("theta") is not None:
            return float(knobs["theta"])
    seed = payload.get("seed_theta")
    return float(seed) if seed is not None else None


def append_exam_row(
    *,
    k: int,
    family: str,
    knobs: dict[str, Any],
    outcome: str,
) -> dict[str, Any]:
    if outcome not in OUTCOMES:
        raise ValueError(f"unknown library outcome {outcome}")
    payload = load_library()
    vector = knob_vector(
        family=str(knobs.get("family") or family),
        theta=float(knobs.get("theta") or 0.0),
        delta=float(knobs.get("delta") or 0.0),
    )
    payload["rows"] = list(payload.get("rows") or [])
    payload["rows"].append(
        {
            "k": int(k),
            "family": str(family),
            "knobs": vector,
            "outcome": outcome,
            "at": now().isoformat(),
        }
    )
    if outcome in RETIRE_OUTCOMES:
        retired = list(payload.get("retired") or [])
        if not _in_set(retired, vector):
            retired.append(vector)
        payload["retired"] = retired
    else:
        spent = list(payload.get("spent") or [])
        if not _in_set(spent, vector):
            spent.append(vector)
        payload["spent"] = spent
        payload["seed_theta"] = float(vector["theta"])
    save_library(payload)
    from golf_offshoot.honer_15m.family_amend import stamp_family_amend

    stamp_family_amend()
    return payload


def append_search_untestable(*, family: str, knobs: dict[str, Any]) -> dict[str, Any]:
    """Retire a search vector the tape never visited. Does not increment exam k."""
    return append_exam_row(k=0, family=family, knobs=knobs, outcome="search_untestable")
