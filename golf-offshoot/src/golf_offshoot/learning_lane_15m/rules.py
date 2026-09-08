"""Dated paper rules. A window that closed before declaration is not OOS."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from golf_offshoot.localtime import to_eastern

REGISTRY_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_RULES.json"


def registry_path(*, root: Path | None = None) -> Path:
    if root is not None:
        return Path(root) / REGISTRY_REL
    return Path(__file__).resolve().parents[4] / REGISTRY_REL


def load_rules(*, root: Path | None = None) -> dict[str, Any]:
    path = registry_path(root=root)
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("rule registry must be an object")
    return payload


def _as_dt(value: str) -> datetime:
    text = str(value or "").strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError as exc:
        raise ValueError(f"unparseable timestamp {value!r}") from exc
    return to_eastern(parsed)


def window_is_oos(rule: dict[str, Any], *, close_at: str) -> bool:
    """True only when the window closed strictly after the rule was declared."""
    declared = _as_dt(str(rule.get("declared_at") or ""))
    closed = _as_dt(close_at)
    return closed > declared


def decide(
    rule: dict[str, Any],
    *,
    posted_yes: float,
    close_at: str,
) -> dict[str, Any]:
    """Express a fill-or-skip. Does not place anything. Does not invent pnl."""
    eligible = window_is_oos(rule, close_at=close_at)
    action = "ineligible"
    reason = "window closed at or before declared_at; not OOS for this rule"
    if eligible:
        kind = str(rule.get("kind") or "")
        if kind == "baseline" or not rule.get("selects"):
            action = "fill"
            reason = "baseline fill at posted mark"
        elif kind == "selection" and rule.get("id") == "R-SKIP-COINFLIP":
            if 0.45 < float(posted_yes) < 0.55:
                action = "skip"
                reason = "posted_yes inside (0.45, 0.55)"
            else:
                action = "fill"
                reason = "posted_yes outside coinflip band"
        else:
            action = "unknown"
            reason = f"no expression for {rule.get('id')}"
    return {
        "rule_id": rule.get("id"),
        "eligible": eligible,
        "action": action,
        "reason": reason,
        "execution": bool(rule.get("execution")),
    }
