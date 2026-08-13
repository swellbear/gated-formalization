"""Data-feed contracts. Live vendors are not required; mocks implement the same interface.

Rules:
- Every payload carries DataQuality.
- Primary failure → fallback.
- Missing / delayed / low-quality data is explicit, never silently treated as zero evidence.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, Generic, TypeVar

from golf_offshoot.models.enums import DataRole
from golf_offshoot.models.schemas import DataQuality

T = TypeVar("T")

LOW_QUALITY_THRESHOLD = 0.35
STALE_HOURS = 36.0


class FeedError(RuntimeError):
    pass


class DataFeed(ABC, Generic[T]):
    name: str
    role: DataRole = DataRole.PRIMARY

    @abstractmethod
    def fetch(self, **kwargs: Any) -> tuple[T, DataQuality]:
        ...

    def quality_or_missing(self, **kwargs: Any) -> tuple[T | None, DataQuality]:
        try:
            payload, q = self.fetch(**kwargs)
        except Exception as exc:
            q = DataQuality(
                score=0.0,
                role=self.role,
                source_name=self.name,
                as_of=datetime.now(timezone.utc),
                missing=True,
                notes=f"fetch failed: {exc}",
            )
            return None, q
        if q.lag_hours > STALE_HOURS:
            q = q.model_copy(
                update={
                    "score": min(q.score, 0.40),
                    "notes": (q.notes + " stale").strip(),
                }
            )
        return payload, q


class FallbackChain(Generic[T]):
    def __init__(self, feeds: list[DataFeed[T]]) -> None:
        if not feeds:
            raise ValueError("need at least one feed")
        self.feeds = feeds

    def fetch(self, **kwargs: Any) -> tuple[T | None, DataQuality, str]:
        last_q: DataQuality | None = None
        for feed in self.feeds:
            payload, q = feed.quality_or_missing(**kwargs)
            last_q = q
            if payload is None or q.missing:
                continue
            if q.score < LOW_QUALITY_THRESHOLD and feed.role == DataRole.PRIMARY:
                # try fallback but keep this if nothing else works
                continue
            return payload, q, feed.name
        if last_q is None:
            last_q = DataQuality(
                score=0.0,
                source_name="none",
                as_of=datetime.now(timezone.utc),
                missing=True,
                notes="empty chain",
            )
        return None, last_q, "missing"
