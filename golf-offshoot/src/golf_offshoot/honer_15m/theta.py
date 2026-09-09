"""Durable search θ. Restart must not snap back to 0.75."""

from __future__ import annotations

import json
from typing import Any

from golf_offshoot.honer_15m.paths import assert_honer_path, theta_path
from golf_offshoot.honer_15m.policy import clip_theta, load_policy
from golf_offshoot.localtime import now


def default_state(policy: dict[str, Any] | None = None) -> dict[str, Any]:
    pol = policy or load_policy()
    start = float(pol["start_theta"])
    return {
        "theta": start,
        "last_declared_theta": start,
        "search_settled_since_freeze": 0,
        "updated_at": now().isoformat(),
    }


def load_theta() -> dict[str, Any]:
    path = theta_path()
    if not path.is_file():
        state = default_state()
        save_theta(state)
        return state
    payload = json.loads(path.read_text(encoding="utf-8"))
    pol = load_policy()
    payload["theta"] = clip_theta(float(payload.get("theta", pol["start_theta"])), policy=pol)
    payload.setdefault("last_declared_theta", float(pol["start_theta"]))
    payload.setdefault("search_settled_since_freeze", 0)
    return payload


def save_theta(state: dict[str, Any]) -> None:
    path = theta_path()
    assert_honer_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    state = dict(state)
    state["updated_at"] = now().isoformat()
    path.write_text(json.dumps(state, indent=2), encoding="utf-8")


def step_search_theta(*, action: str, kalshi_result: str) -> dict[str, Any]:
    """One discovery step. Pending/unknown result must not call this."""
    result = str(kalshi_result or "").strip().lower()
    if result not in {"yes", "no"}:
        raise ValueError("theta steps only on settled yes/no")
    pol = load_policy()
    state = load_theta()
    delta = 0.0
    if action == "fill" and result == "no":
        delta = float(pol["step"])
    elif action == "skip" and result == "yes":
        delta = -float(pol["step"])
    if delta:
        state["theta"] = clip_theta(float(state["theta"]) + delta, policy=pol)
    state["search_settled_since_freeze"] = int(state.get("search_settled_since_freeze") or 0) + 1
    save_theta(state)
    return state
