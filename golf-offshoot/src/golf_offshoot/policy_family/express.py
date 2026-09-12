"""YES-or-skip for one frozen P-* name. Never buy NO. Not 3^N. Not skip-together."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from golf_offshoot.localtime import to_eastern
from golf_offshoot.policy_family.library import PolicyFamilyError

ACTION_FILL = "fill"
ACTION_SKIP = "skip"
RICH_THETA = 0.75
WIDE_DELTA = 0.04
COINFLIP_LO = 0.45
COINFLIP_HI = 0.55
LAST_SECONDS = 60.0


def _parse_dt(value: Any) -> datetime | None:
    text = str(value or "").strip()
    if not text:
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    return to_eastern(parsed)


def _float_or_none(value: Any) -> float | None:
    if value is None or value == "":
        return None
    if isinstance(value, str) and value.strip().lower() in {"none", "null", "n/a"}:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def posted_yes(window: dict[str, Any]) -> float | None:
    return _float_or_none(window.get("posted_yes"))


def quoted_spread(window: dict[str, Any]) -> float | None:
    """Quoted yes_ask − yes_bid. Missing either side is None (fill, not skip)."""
    raw = window.get("spread")
    if raw is not None and raw != "":
        spread = _float_or_none(raw)
        if spread is None or spread < 0:
            return None
        return spread
    bid = _float_or_none(window.get("yes_bid"))
    ask = _float_or_none(window.get("yes_ask"))
    if bid is None or ask is None:
        return None
    spread = ask - bid
    if spread < 0:
        return None
    return spread


def _fill_stamp(window: dict[str, Any]) -> datetime | None:
    for key in ("fill_at", "decision_at", "at"):
        parsed = _parse_dt(window.get(key))
        if parsed is not None:
            return parsed
    return None


def _verdict(policy_id: str, action: str, reason: str) -> dict[str, str]:
    if action not in {ACTION_FILL, ACTION_SKIP}:
        raise PolicyFamilyError(f"{policy_id} expressed {action!r}; only fill or skip")
    return {"policy_id": policy_id, "action": action, "reason": reason}


def express(policy: dict[str, Any], window: dict[str, Any]) -> dict[str, str]:
    """Fill YES or skip. Missing evidence fills; it never invents a skip or a NO."""
    ident = str(policy.get("id") or "")
    if not ident:
        raise PolicyFamilyError("policy missing id")
    if ident == "P-FILL-ALL-YES":
        return _verdict(ident, ACTION_FILL, "comparison fill YES at posted mark")
    if ident == "P-SKIP-COINFLIP":
        mark = posted_yes(window)
        if mark is None:
            return _verdict(ident, ACTION_FILL, "no posted_yes; fill YES")
        if COINFLIP_LO < mark < COINFLIP_HI:
            return _verdict(ident, ACTION_SKIP, "posted_yes inside (0.45, 0.55)")
        return _verdict(ident, ACTION_FILL, "posted_yes outside coinflip band")
    if ident == "P-SKIP-RICH-075":
        mark = posted_yes(window)
        if mark is None:
            return _verdict(ident, ACTION_FILL, "no posted_yes; fill YES")
        if mark >= RICH_THETA:
            return _verdict(ident, ACTION_SKIP, "posted_yes >= 0.75")
        return _verdict(ident, ACTION_FILL, "posted_yes below 0.75")
    if ident == "P-SKIP-WIDE-0400":
        spread = quoted_spread(window)
        if spread is None:
            return _verdict(ident, ACTION_FILL, "missing bid/ask; fill YES")
        if spread >= WIDE_DELTA:
            return _verdict(ident, ACTION_SKIP, f"spread {spread:g} >= 0.04")
        return _verdict(ident, ACTION_FILL, f"spread {spread:g} < 0.04")
    if ident == "P-SKIP-LAST-SECONDS-60":
        close_at = _parse_dt(window.get("close_at"))
        fill_at = _fill_stamp(window)
        if close_at is None or fill_at is None:
            return _verdict(ident, ACTION_FILL, "no fill/close stamp; fill YES")
        remaining = (close_at - fill_at).total_seconds()
        if 0 < remaining < LAST_SECONDS:
            return _verdict(ident, ACTION_SKIP, f"fill {remaining:.3f}s before close")
        return _verdict(ident, ACTION_FILL, "fill not in last 60s before close")
    if ident == "P-SKIP-INELIGIBLE-CLOSED":
        close_at = _parse_dt(window.get("close_at"))
        decision_at = _fill_stamp(window)
        if close_at is None or decision_at is None:
            return _verdict(ident, ACTION_FILL, "no decision/close stamp; fill YES")
        if decision_at >= close_at:
            return _verdict(ident, ACTION_SKIP, "close_at already passed at decision stamp")
        return _verdict(ident, ACTION_FILL, "decision stamp is before close_at")
    raise PolicyFamilyError(f"no expression for {ident}")
