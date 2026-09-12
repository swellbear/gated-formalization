"""Kalshi title vs ESPN names. Unmatched stays unmatched — never a guessed bet."""

from __future__ import annotations

import re
from typing import Any

from golf_offshoot.data_feeds.field_fallback import is_skip_field_name
from golf_offshoot.data_feeds.names import match_name, normalize_name

_WILL_WIN = re.compile(r"will\s+(.+?)\s+win\b", re.I)
_NAME_CUT = re.compile(r"will\s+(.+?)\s+make\s+(?:the\s+)?cut", re.I)
_NAME_FINISH = re.compile(r"will\s+(.+?)\s+(?:finish|lead|be)\b", re.I)
_TOP_OR_LEAD = ("top 5", "top five", "top 10", "top ten", "top 20", "top twenty", "lead")


def _real_name(name: str) -> str:
    text = str(name or "").strip(" ?")
    if not text or is_skip_field_name(text):
        return ""
    if len(text.split()) < 2:
        return ""
    return text


def extract_player_name(market: dict[str, Any] | None = None, *, title: str = "") -> str:
    sub = str((market or {}).get("yes_sub_title") or "").strip()
    real_sub = _real_name(sub)
    if real_sub:
        return real_sub
    blob = title or str((market or {}).get("title") or "")
    low = blob.lower()
    m = _WILL_WIN.search(blob) or _NAME_CUT.search(blob)
    if m:
        hit = _real_name(m.group(1))
        if hit:
            return hit
    if any(tok in low for tok in _TOP_OR_LEAD):
        m2 = _NAME_FINISH.search(blob)
        if m2:
            hit = _real_name(m.group(1))
            if hit:
                return hit
    return ""


def match_market_player(
    market: dict[str, Any],
    candidates: dict[str, str],
) -> str | None:
    """candidates: normalized_name -> player_id. None means quarantine, not a fill."""
    if not candidates:
        return None
    name = extract_player_name(market)
    if not name or is_skip_field_name(name):
        return None
    hit = match_name(name, candidates)
    if hit:
        return hit
    nq = normalize_name(name)
    return candidates.get(nq)


def quarantine_row(market: dict[str, Any], *, reason: str) -> dict[str, str]:
    return {
        "ticker": str(market.get("ticker") or ""),
        "title": str(market.get("title") or ""),
        "player": extract_player_name(market),
        "reason": reason,
    }
