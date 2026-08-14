"""Data Golf connector. Recent as-of SG windows only when the API actually provides them.

Skill ratings are a long-term predictive estimate (typically ≥30 ShotLink rounds
in the last year). They are **not** a last-8-start window. This module never
copies PGA season-to-date tables into a fake recent-SG feature.
"""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

from golf_offshoot.data_feeds.base import DataFeed, FeedError, unavailable_quality
from golf_offshoot.data_feeds.http import DEFAULT_APP_UA, HttpCache
from golf_offshoot.models.enums import DataRole, SourceKind
from golf_offshoot.models.schemas import DataQuality

SKILL_RATINGS = "https://feeds.datagolf.com/preds/skill-ratings"
# Field names that would count as a true recent window if a payload includes them.
_RECENT_KEYS = (
    "sg_total_l8",
    "sg_ott_l8",
    "sg_app_l8",
    "sg_arg_l8",
    "sg_putt_l8",
    "sg_total_last_8",
    "last_8_sg_total",
    "l8_sg_total",
    "recent_sg_total",
)


def data_golf_api_key() -> str:
    return (
        os.environ.get("DATA_GOLF_API_KEY", "").strip()
        or os.environ.get("DATAGOLF_API_KEY", "").strip()
    )


def _missing_recent_quality(reason: str) -> DataQuality:
    return unavailable_quality(
        "datagolf_recent_sg",
        reason,
    )


class DataGolfRecentSgFeed(DataFeed[dict[str, Any]]):
    """True as-of recent SG windows. Missing key → unavailable, never proxied."""

    name = "datagolf_recent_sg"
    role = DataRole.PRIMARY

    def __init__(self, cache: HttpCache | None = None, api_key: str | None = None) -> None:
        self.cache = cache or HttpCache()
        self.api_key = api_key if api_key is not None else data_golf_api_key()

    def fetch(self, **kwargs: Any) -> tuple[dict[str, Any], DataQuality]:
        if not self.api_key:
            q = _missing_recent_quality(
                "DATA_GOLF_API_KEY / DATAGOLF_API_KEY not set; true as-of recent SG "
                "windows unavailable. PGA season StatDetails are not used as a last-8 proxy."
            )
            return {}, q
        url = f"{SKILL_RATINGS}?display=value&file_format=json&key={self.api_key}"
        try:
            body, meta = self.cache.get_json(
                url,
                headers={"User-Agent": DEFAULT_APP_UA, "Accept": "application/json"},
                ttl_seconds=6 * 3600,
                refresh=bool(kwargs.get("refresh", False)),
                label="datagolf_skill_ratings",
                allow_stale_on_error=True,
            )
        except FeedError as exc:
            q = _missing_recent_quality(f"Data Golf skill-ratings fetch failed: {exc}")
            return {}, q
        rows = _rows_from_skill_payload(body)
        recent_n = sum(1 for row in rows if _row_has_recent_window(row))
        if recent_n == 0:
            q = DataQuality(
                score=0.0,
                role=self.role,
                source_name=self.name,
                as_of=datetime.now(timezone.utc),
                n_observations=len(rows),
                missing=True,
                source_kind=SourceKind.UNAVAILABLE,
                notes=(
                    f"Data Golf skill-ratings reachable (n={len(rows)}, fetched_at={meta.get('fetched_at')}) "
                    "but payload has no last-8 / recent-window fields. Skill ratings are a long-term "
                    "predictive estimate, not a recent SG window. Recent-SG left unavailable "
                    "(not inferred from PGA season tables)."
                ),
            )
            return {"skill_ratings_n": len(rows), "recent_n": 0}, q
        q = DataQuality(
            score=0.86,
            role=self.role,
            source_name=self.name,
            as_of=datetime.now(timezone.utc),
            n_observations=recent_n,
            notes=f"Data Golf recent-window fields present for {recent_n}/{len(rows)} players",
            source_kind=SourceKind.REAL_HISTORICAL,
        )
        return {"skill_ratings_n": len(rows), "recent_n": recent_n, "rows": rows}, q


def _rows_from_skill_payload(body: Any) -> list[dict[str, Any]]:
    if isinstance(body, list):
        return [r for r in body if isinstance(r, dict)]
    if isinstance(body, dict):
        for key in ("players", "data", "skill_ratings"):
            val = body.get(key)
            if isinstance(val, list):
                return [r for r in val if isinstance(r, dict)]
    return []


def _row_has_recent_window(row: dict[str, Any]) -> bool:
    keys = {str(k).lower() for k in row.keys()}
    return any(k in keys for k in _RECENT_KEYS)
