"""YES-or-skip for one frozen P-* name. Never buy NO. Not 3^N. Not skip-together."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from golf_offshoot.learning_lane_15m.rules import close_minute
from golf_offshoot.localtime import to_eastern
from golf_offshoot.policy_family.library import PolicyFamilyError

ACTION_FILL = "fill"
ACTION_SKIP = "skip"
RICH_THETA = 0.75
WIDE_DELTA = 0.04
COINFLIP_LO = 0.45
COINFLIP_HI = 0.55
LAST_SECONDS = 60.0
#: Honer quote-bus stale cutoff. Named from that contract, not a tape walk.
STALE_QUOTE_S = 180.0
STALE_QUOTE_ID = "P-SKIP-STALE-QUOTE-180"
#: Fill cheap YES only. Frozen 0.40, not a 0.35/0.45 walk.
UNLESS_CHEAP_THETA = 0.40
UNLESS_CHEAP_ID = "P-SKIP-UNLESS-CHEAP-040"
#: Skip iff |last − mid| ≥ 0.02. Frozen 2¢, not a 1¢/3¢/5¢ walk.
LAST_VS_MID_DELTA = 0.02
LAST_VS_MID_ID = "P-SKIP-LAST-VS-MID-0200"
#: Skip iff close_at clock minute is 0 or 15. Frozen {0,15}, not civil {0,30}.
CLOSE_MINUTES_SKIP = frozenset({0, 15})
CLOSE_MINUTES_ID = "P-SKIP-CLOSE-MINUTES-0-15"
_LAST_KEYS = ("last", "last_price", "last_price_dollars")


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


def last_price(window: dict[str, Any]) -> float | None:
    """Kalshi last / last_price_dollars. Never posted_yes / paper_mark."""
    for key in _LAST_KEYS:
        value = _float_or_none(window.get(key))
        if value is not None:
            return value
    snapshot = window.get("quote_snapshot") or window.get("quote_bus")
    if isinstance(snapshot, dict):
        for key in _LAST_KEYS:
            value = _float_or_none(snapshot.get(key))
            if value is not None:
                return value
    return None


def quoted_mid(window: dict[str, Any]) -> float | None:
    """(yes_bid + yes_ask) / 2 when both sides exist. Not posted_yes."""
    bid = _float_or_none(window.get("yes_bid"))
    ask = _float_or_none(window.get("yes_ask"))
    if bid is None or ask is None:
        return None
    return (bid + ask) / 2.0


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


def quote_age_seconds(window: dict[str, Any]) -> float | None:
    """Age of the quote snapshot used at decision. Missing → None (fill, not skip)."""
    for key in ("quote_age_s", "quote_bus_age_s"):
        age = _float_or_none(window.get(key))
        if age is not None:
            return age
    fetched = None
    for key in ("quote_fetched_at", "quote_snapshot_at", "quote_at"):
        fetched = _parse_dt(window.get(key))
        if fetched is not None:
            break
    snapshot = window.get("quote_snapshot") or window.get("quote_bus")
    if fetched is None and isinstance(snapshot, dict):
        for key in ("fetched_at", "quote_fetched_at", "at"):
            fetched = _parse_dt(snapshot.get(key))
            if fetched is not None:
                break
    decision = _fill_stamp(window)
    if fetched is None or decision is None:
        return None
    return (decision - fetched).total_seconds()


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
    if ident == STALE_QUOTE_ID:
        age = quote_age_seconds(window)
        if age is None:
            return _verdict(ident, ACTION_FILL, "missing quote age/snapshot; fill YES")
        if age > STALE_QUOTE_S:
            return _verdict(ident, ACTION_SKIP, f"quote age {age:g}s > 180s")
        return _verdict(ident, ACTION_FILL, f"quote age {age:g}s <= 180s")
    if ident == UNLESS_CHEAP_ID:
        mark = posted_yes(window)
        if mark is None:
            return _verdict(ident, ACTION_FILL, "no posted_yes; fill YES")
        if mark <= UNLESS_CHEAP_THETA:
            return _verdict(ident, ACTION_FILL, "posted_yes <= 0.40; cheap YES")
        return _verdict(ident, ACTION_SKIP, "posted_yes > 0.40; skip unless cheap")
    if ident == LAST_VS_MID_ID:
        last = last_price(window)
        mid = quoted_mid(window)
        if last is None:
            return _verdict(ident, ACTION_FILL, "missing last; fill YES")
        if mid is None:
            return _verdict(ident, ACTION_FILL, "missing mid; fill YES")
        gap = abs(last - mid)
        if gap >= LAST_VS_MID_DELTA:
            return _verdict(ident, ACTION_SKIP, f"|last-mid| {gap:g} >= 0.02")
        return _verdict(ident, ACTION_FILL, f"|last-mid| {gap:g} < 0.02")
    if ident == CLOSE_MINUTES_ID:
        raw = window.get("close_at")
        if raw is None or str(raw).strip() == "":
            return _verdict(ident, ACTION_FILL, "missing close_at; fill YES")
        try:
            minute = close_minute(str(raw))
        except (ValueError, TypeError):
            return _verdict(ident, ACTION_FILL, "missing close_at; fill YES")
        if minute in CLOSE_MINUTES_SKIP:
            return _verdict(ident, ACTION_SKIP, f"close_minute {minute} in {{0, 15}}")
        return _verdict(ident, ACTION_FILL, f"close_minute {minute} not in {{0, 15}}")
    raise PolicyFamilyError(f"no expression for {ident}")
