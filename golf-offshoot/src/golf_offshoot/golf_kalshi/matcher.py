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
_CONNECTIVE = re.compile(r"\b(?:beats?|versus|vs\.?|to|and)\b", re.I)
_NONPERSON_TOKENS = frozenset(
    {
        "team",
        "tie",
        "united",
        "states",
        "europe",
        "usa",
        "us",
        "world",
        "international",
        "country",
        "america",
        "before",
        "after",
        "the",
        "field",
        "other",
        "others",
        "any",
        "rest",
        "yes",
        "no",
        "of",
    }
)


def names_a_golfer(title: str) -> bool:
    """True only when this string itself is a person name.

    Positive: two or more letter tokens, no digits, no `+`, no connective
    predicate (`beats` / `to` / `and` / `vs`). Closed-class team/country/tie
    tokens are not person names. Exact-match tote `_SKIP` is separate.
    """
    text = str(title or "").strip(" ?")
    if not text:
        return False
    if any(ch.isdigit() for ch in text) or "+" in text:
        return False
    if _CONNECTIVE.search(text):
        return False
    tokens = text.split()
    if len(tokens) < 2:
        return False
    for tok in tokens:
        core = tok.replace("-", "").replace("'", "").replace("’", "").replace(".", "")
        if not core or not core.isalpha():
            return False
        if core.casefold() in _NONPERSON_TOKENS:
            return False
    return True


def _real_name(name: str) -> str:
    text = str(name or "").strip(" ?")
    if not text or is_skip_field_name(text):
        return ""
    if not names_a_golfer(text):
        return ""
    return text


def extract_player_name(market: dict[str, Any] | None = None, *, title: str = "") -> str:
    """Listed identity is the yes_sub_title when that string names a golfer.

    A present sub-title that fails the shape check is unmatched. The title
    regex does not re-admit a player. Title fallback is only for rows with no
    sub-title (ESPN-style "Will X win …").
    """
    sub = str((market or {}).get("yes_sub_title") or "").strip()
    if sub:
        return _real_name(sub)
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
            hit = _real_name(m2.group(1))
            if hit:
                return hit
    return ""


def match_market_player(
    market: dict[str, Any],
    candidates: dict[str, str],
) -> str | None:
    """candidates: normalized_name -> player_id. None means quarantine, not a fill.

    A market whose yes_sub_title fails names_a_golfer does not match, even if
    the title names a golfer who is in the candidate map.
    """
    if not candidates:
        return None
    sub = str((market or {}).get("yes_sub_title") or "").strip()
    if sub and not names_a_golfer(sub):
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
