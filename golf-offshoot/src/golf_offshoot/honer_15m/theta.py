"""Durable search knobs. Restart must not snap θ back to 0.75."""

from __future__ import annotations

import json
from typing import Any

from golf_offshoot.honer_15m.paths import assert_honer_path, theta_path
from golf_offshoot.honer_15m.policy import (
    FAMILY_RICH,
    FAMILY_SPREAD,
    FREEZE_RULE,
    STEP_RULE,
    clip_delta,
    clip_theta,
    knob_vector,
    load_policy,
)
from golf_offshoot.localtime import now


def default_state(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    pol = policy or load_policy()
    start = float(pol["start_theta"])
    start_delta = float(pol["start_delta"])
    return {
        "theta": start,
        "last_declared_theta": start,
        "delta": start_delta,
        "last_declared_delta": start_delta,
        "search_settled_since_freeze": 0,
        "in_band_settled": 0,
        "in_band_stable": 0,
        "far_settled_since_freeze": 0,
        "stable_windows": 0,
        "clip_streak": 0,
        "family_starvations": {},
        "advance_owed": "",
        "starvation_pending": False,
        "step_rule": STEP_RULE,
        "freeze_rule": FREEZE_RULE,
        "active_family": FAMILY_RICH,
        "updated_at": now().isoformat(),
    }


def _needs_v2_migrate(payload: dict[str, Any]) -> bool:
    return str(payload.get("step_rule") or "") != STEP_RULE


def _needs_in_band_migrate(payload: dict[str, Any]) -> bool:
    return str(payload.get("freeze_rule") or "") != FREEZE_RULE


def _reset_freeze_clocks(state: dict[str, Any]) -> dict[str, Any]:
    state["search_settled_since_freeze"] = 0
    state["in_band_settled"] = 0
    state["in_band_stable"] = 0
    state["far_settled_since_freeze"] = 0
    state["stable_windows"] = 0
    state["clip_streak"] = 0
    return state


def migrate_v2(payload: dict[str, Any], *, policy: dict[str, Any] | None = None) -> dict[str, Any]:
    """Keep θ. Reset the freeze clock so v1 and v2 are not mixed."""
    pol = policy or load_policy()
    state = dict(payload)
    state["theta"] = clip_theta(float(state.get("theta", pol["start_theta"])), policy=pol)
    state.setdefault("last_declared_theta", float(pol["start_theta"]))
    state["delta"] = clip_delta(float(state.get("delta", pol["start_delta"])), policy=pol)
    state.setdefault("last_declared_delta", float(pol["start_delta"]))
    state["step_rule"] = STEP_RULE
    state.setdefault("active_family", FAMILY_RICH)
    _reset_freeze_clocks(state)
    state["freeze_rule"] = FREEZE_RULE
    return state


def migrate_in_band_v1(payload: dict[str, Any], *, policy: dict[str, Any] | None = None) -> dict[str, Any]:
    """Keep θ/δ/family. Reset freeze clocks so all-settle v2 and in-band v1 are not mixed."""
    pol = policy or load_policy()
    state = dict(payload)
    state["theta"] = clip_theta(float(state.get("theta", pol["start_theta"])), policy=pol)
    state.setdefault("last_declared_theta", float(pol["start_theta"]))
    state["delta"] = clip_delta(float(state.get("delta", pol["start_delta"])), policy=pol)
    state.setdefault("last_declared_delta", float(pol["start_delta"]))
    state.setdefault("step_rule", STEP_RULE)
    state.setdefault("active_family", FAMILY_RICH)
    _reset_freeze_clocks(state)
    state["freeze_rule"] = FREEZE_RULE
    return state


def load_theta() -> dict[str, Any]:
    path = theta_path()
    if not path.is_file():
        state = default_state()
        save_theta(state)
        return state
    payload = json.loads(path.read_text(encoding="utf-8"))
    pol = load_policy()
    if _needs_v2_migrate(payload):
        state = migrate_v2(payload, policy=pol)
        save_theta(state)
        return state
    if _needs_in_band_migrate(payload):
        state = migrate_in_band_v1(payload, policy=pol)
        save_theta(state)
        return state
    payload["theta"] = clip_theta(float(payload.get("theta", pol["start_theta"])), policy=pol)
    payload.setdefault("last_declared_theta", float(pol["start_theta"]))
    payload["delta"] = clip_delta(float(payload.get("delta", pol["start_delta"])), policy=pol)
    payload.setdefault("last_declared_delta", float(pol["start_delta"]))
    payload.setdefault("search_settled_since_freeze", 0)
    payload.setdefault("in_band_settled", 0)
    payload.setdefault("in_band_stable", 0)
    payload.setdefault("far_settled_since_freeze", 0)
    payload.setdefault("stable_windows", 0)
    payload.setdefault("clip_streak", 0)
    payload.setdefault("family_starvations", {})
    payload.setdefault("advance_owed", "")
    payload.setdefault("starvation_pending", False)
    payload.setdefault("step_rule", STEP_RULE)
    payload.setdefault("freeze_rule", FREEZE_RULE)
    payload.setdefault("active_family", FAMILY_RICH)
    return payload


def save_theta(state: dict[str, Any]) -> None:
    path = theta_path()
    assert_honer_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    state = dict(state)
    state["updated_at"] = now().isoformat()
    path.write_text(json.dumps(state, indent=2), encoding="utf-8")


def current_vector(state: dict[str, Any] | None = None) -> dict[str, Any]:
    st = state if state is not None else load_theta()
    pol = load_policy()
    return knob_vector(
        family=str(st.get("active_family") or FAMILY_RICH),
        theta=float(st.get("theta") or pol["start_theta"]),
        delta=float(st.get("delta") or pol["start_delta"]),
    )


def _in_band(value: float | None, center: float, band: float) -> bool:
    if value is None:
        return False
    return abs(float(value) - float(center)) <= float(band)


def _at_clip(value: float, lo: float, hi: float) -> bool:
    return float(value) <= float(lo) + 1e-12 or float(value) >= float(hi) - 1e-12


def step_search_theta(
    *,
    action: str,
    kalshi_result: str,
    posted_yes: float | None = None,
    spread: float | None = None,
) -> dict[str, Any]:
    """One local_regret_v2 discovery step. Pending/unknown result must not call this."""
    result = str(kalshi_result or "").strip().lower()
    if result not in {"yes", "no"}:
        raise ValueError("theta steps only on settled yes/no")
    pol = load_policy()
    state = load_theta()
    family = str(state.get("active_family") or FAMILY_RICH)
    moved = False
    if family == FAMILY_SPREAD:
        center = float(state.get("delta") or pol["start_delta"])
        step = float(pol["delta_step"])
        band = float(pol["spread_band"])
        near = _in_band(spread, center, band)
        delta = 0.0
        if near:
            if action == "fill" and result == "no":
                delta = -step
            elif action == "skip" and result == "yes":
                delta = step
        if delta:
            new = clip_delta(center + delta, policy=pol)
            moved = abs(new - center) > 1e-12
            state["delta"] = new
        lo, hi = float(pol["delta_min"]), float(pol["delta_max"])
        at_clip = _at_clip(float(state["delta"]), lo, hi)
    else:
        center = float(state.get("theta") or pol["start_theta"])
        step = float(pol["step"])
        band = float(pol["step_band"])
        near = _in_band(posted_yes, center, band)
        delta = 0.0
        if near:
            if action == "fill" and result == "no":
                delta = -step
            elif action == "skip" and result == "yes":
                delta = step
        if delta:
            new = clip_theta(center + delta, policy=pol)
            moved = abs(new - center) > 1e-12
            state["theta"] = new
        lo, hi = float(pol["theta_min"]), float(pol["theta_max"])
        at_clip = _at_clip(float(state["theta"]), lo, hi)
    state["search_settled_since_freeze"] = int(state.get("search_settled_since_freeze") or 0) + 1
    if near:
        state["in_band_settled"] = int(state.get("in_band_settled") or 0) + 1
        if moved:
            state["in_band_stable"] = 0
            state["stable_windows"] = 0
        else:
            state["in_band_stable"] = int(state.get("in_band_stable") or 0) + 1
            state["stable_windows"] = int(state.get("in_band_stable") or 0)
        if at_clip:
            state["clip_streak"] = int(state.get("clip_streak") or 0) + 1
        else:
            state["clip_streak"] = 0
    else:
        state["far_settled_since_freeze"] = int(state.get("far_settled_since_freeze") or 0) + 1
    state["step_rule"] = STEP_RULE
    state["freeze_rule"] = FREEZE_RULE
    save_theta(state)
    return state
