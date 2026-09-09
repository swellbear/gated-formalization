"""Novelty + stability freeze. One exam at a time. Retired/spent vectors cannot freeze."""

from __future__ import annotations

import json
from typing import Any

from golf_offshoot.honer_15m.library import is_retired, is_spent, load_library
from golf_offshoot.honer_15m.paths import (
    assert_honer_path,
    exam_state_path,
    freeze_log_path,
    trials_path,
)
from golf_offshoot.honer_15m.policy import FAMILY_RICH, FAMILY_SPREAD, load_policy
from golf_offshoot.honer_15m.theta import current_vector, load_theta, save_theta
from golf_offshoot.localtime import now


def load_exam_state() -> dict[str, Any]:
    path = exam_state_path()
    if not path.is_file():
        return {
            "open": False,
            "n": 0,
            "parked": False,
            "frozen_theta": None,
            "frozen_delta": None,
            "frozen_family": None,
        }
    return json.loads(path.read_text(encoding="utf-8"))


def save_exam_state(state: dict[str, Any]) -> None:
    path = exam_state_path()
    assert_honer_path(path)
    path.write_text(json.dumps(state, indent=2), encoding="utf-8")


def exam_is_open() -> bool:
    state = load_exam_state()
    return bool(state.get("open")) and not state.get("parked")


def _novelty(st: dict[str, Any], pol: dict[str, Any]) -> bool:
    family = str(st.get("active_family") or FAMILY_RICH)
    if family == FAMILY_SPREAD:
        moved = abs(float(st.get("delta") or 0.0) - float(st.get("last_declared_delta") or pol["start_delta"]))
        return moved >= float(pol["freeze_abs_delta_spread"])
    moved = abs(float(st["theta"]) - float(st.get("last_declared_theta", pol["start_theta"])))
    return moved >= float(pol["freeze_abs_delta"])


def freeze_ready(theta_state: dict[str, Any] | None = None) -> bool:
    if exam_is_open():
        return False
    pol = load_policy()
    st = theta_state or load_theta()
    settled = int(st.get("in_band_settled") or 0)
    if settled < int(pol["freeze_min_search_settled"]):
        return False
    if not _novelty(st, pol):
        return False
    if int(st.get("in_band_stable") or 0) < int(pol["freeze_stable_windows"]):
        return False
    vector = current_vector(st)
    lib = load_library()
    if is_retired(vector, lib) or is_spent(vector, lib):
        return False
    return True


def load_trials() -> dict[str, Any]:
    path = trials_path()
    if not path.is_file():
        return {"trials_to_date": 0, "trials_log": [], "lane": "honer_15m"}
    return json.loads(path.read_text(encoding="utf-8"))


def _increment_k(family: str) -> int:
    path = trials_path()
    assert_honer_path(path)
    payload = load_trials()
    k = int(payload.get("trials_to_date") or 0) + 1
    payload["trials_to_date"] = k
    payload["lane"] = "honer_15m"
    log = list(payload.get("trials_log") or [])
    log.append(
        {
            "subject": str(family),
            "kind": "declaration",
            "at": now().isoformat(),
            "note": "exam snapshot freeze",
            "trials_to_date_after": k,
        }
    )
    payload["trials_log"] = log
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return k


def fire_freeze() -> dict[str, Any] | None:
    if not freeze_ready():
        return None
    st = load_theta()
    family = str(st.get("active_family") or FAMILY_RICH)
    frozen = float(st["theta"])
    frozen_delta = float(st.get("delta") or load_policy()["start_delta"])
    k = _increment_k(family)
    exam = {
        "open": True,
        "parked": False,
        "park_reason": "",
        "frozen_theta": frozen,
        "frozen_delta": frozen_delta,
        "frozen_family": family,
        "declared_at": now().isoformat(),
        "n": 0,
        "k_after": k,
        "lane": "honer_15m",
    }
    save_exam_state(exam)
    st["last_declared_theta"] = frozen
    st["last_declared_delta"] = frozen_delta
    st["search_settled_since_freeze"] = 0
    st["in_band_settled"] = 0
    st["in_band_stable"] = 0
    st["far_settled_since_freeze"] = 0
    st["stable_windows"] = 0
    save_theta(st)
    log_path = freeze_log_path()
    assert_honer_path(log_path)
    log = []
    if log_path.is_file():
        log = json.loads(log_path.read_text(encoding="utf-8"))
        if not isinstance(log, list):
            log = []
    log.append(dict(exam))
    log_path.write_text(json.dumps(log, indent=2), encoding="utf-8")
    return exam


def increment_exam_n() -> dict[str, Any]:
    state = load_exam_state()
    if not state.get("open") or state.get("parked"):
        return state
    state["n"] = int(state.get("n") or 0) + 1
    save_exam_state(state)
    return state


def park_exam(reason: str) -> dict[str, Any]:
    state = load_exam_state()
    state["open"] = False
    state["parked"] = True
    state["park_reason"] = reason
    save_exam_state(state)
    return state


def complete_exam() -> dict[str, Any]:
    state = load_exam_state()
    state["open"] = False
    state["completed"] = True
    save_exam_state(state)
    return state
