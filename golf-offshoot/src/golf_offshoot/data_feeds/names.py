"""Normalize player names so ESPN, Bovada, Hard Rock Bet, and PGA Tour rows can join."""

from __future__ import annotations

import re
import unicodedata


def normalize_name(name: str) -> str:
    text = unicodedata.normalize("NFKD", name or "")
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower().replace(".", " ")
    text = re.sub(r"[^a-z0-9 ]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    aliases = {
        "ludvig aberg": "ludvig aberg",
        "siwoo kim": "si woo kim",
        "sungjae im": "sungjae im",
        "sung jae im": "sungjae im",
        "minwoo lee": "min woo lee",
        "min woo lee": "min woo lee",
        "jj spaun": "j j spaun",
        "j j spaun": "j j spaun",
    }
    return aliases.get(text, text)


def last_first(name: str) -> tuple[str, str]:
    parts = normalize_name(name).split()
    if not parts:
        return "", ""
    return parts[-1], " ".join(parts[:-1])


def match_name(query: str, candidates: dict[str, str]) -> str | None:
    """candidates: normalized_name -> id. Exact, then unique last+first-initial."""
    nq = normalize_name(query)
    if nq in candidates:
        return candidates[nq]
    q_last, q_first = last_first(query)
    if not q_last:
        return None
    hits = []
    for cand, cid in candidates.items():
        c_last, c_first = last_first(cand)
        if c_last == q_last and c_first[:1] == q_first[:1]:
            hits.append(cid)
    if len(hits) == 1:
        return hits[0]
    return None
