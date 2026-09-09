"""Novelty freeze: |Δθ|>=0.05 and >=20 settled search windows. One exam at a time."""

from __future__ import annotations

import json
from typing import Any

from golf_offshoot.honer_15m.paths import (
    assert_honer_path,
    exam_state_path,
    freeze_log_path,
    trials_path,
)
from golf_offshoot.honer_15m.policy import load_policy
from golf_offshoot.honer_15m.theta import load_theta, save_theta
from golf_offshoot.localtime import now


def load_exam_state() -> dict[str, Any]:
    path = exam_state_path()
    if not path.is_file():
        return {"open": False, "n": 0, "parked": False, "frozen_theta": None}
    return json.loads(path.read_text(encoding="utf-8"))


def save_exam_state(state: dict[str, Any]) -> None:
    path = exam_state_path()
    assert_honer_path(path)
    path.write_text(json.dumps(state, indent=2), encoding="utf-8")


def exam_is_open() -> bool:
    state = load_exam_state()
    return bool(state.get("open")) and not state.get("parked")


def freeze_ready(theta_state: dict[str, Any] | None = None) -> bool:
    if exam_is_open():
        return False
    pol = load_policy()
    st = theta_state or load_theta()
    settled = int(st.get("search_settled_since_freeze") or 0)
    if settled < int(pol["freeze_min_search_settled"]):
        return False
    delta = abs(float(st["theta"]) - float(st.get("last_declared_theta", pol["start_theta"])))
    return delta >= float(pol["freeze_abs_delta"])


def load_trials() -> dict[str, Any]:
    path = trials_path()
    if not path.is_file():
        return {"trials_to_date": 0, "trials_log": [], "lane": "honer_15m"}
    return json.loads(path.read_text(encoding="utf-8"))


def _increment_k() -> int:
    path = trials_path()
    assert_honer_path(path)
    payload = load_trials()
    k = int(payload.get("trials_to_date") or 0) + 1
    payload["trials_to_date"] = k
    payload["lane"] = "honer_15m"
    log = list(payload.get("trials_log") or [])
    log.append(
        {
            "subject": "H-SKIP-RICH-YES",
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
    frozen = float(st["theta"])
    k = _increment_k()
    exam = {
        "open": True,
        "parked": False,
        "park_reason": "",
        "frozen_theta": frozen,
        "declared_at": now().isoformat(),
        "n": 0,
        "k_after": k,
        "lane": "honer_15m",
    }
    save_exam_state(exam)
    st["last_declared_theta"] = frozen
    st["search_settled_since_freeze"] = 0
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
