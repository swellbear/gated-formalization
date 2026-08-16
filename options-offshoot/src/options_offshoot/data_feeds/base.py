"""Feed contract. Mocks banned on the operating path."""

from __future__ import annotations

from typing import Any, Protocol

from options_offshoot.models.enums import SourceKind
from options_offshoot.models.schemas import DataQuality


class FeedError(RuntimeError):
    pass


class MockOnOperatingPathError(RuntimeError):
    pass


def unavailable_quality(source: str, notes: str) -> DataQuality:
    return DataQuality(
        score=0.0,
        source_kind=SourceKind.UNAVAILABLE,
        source=source,
        missing=True,
        notes=notes,
    )


def mock_quality(source: str, notes: str = "demo mock") -> DataQuality:
    return DataQuality(
        score=0.4,
        source_kind=SourceKind.MOCK,
        source=source,
        missing=False,
        notes=notes,
    )


def real_quality(source: str, *, n: int = 0, notes: str = "") -> DataQuality:
    return DataQuality(
        score=0.8,
        source_kind=SourceKind.REAL_LIVE,
        source=source,
        missing=False,
        notes=notes,
        n=n,
    )


def assert_no_mocks(inventory: list, *, operating: bool) -> None:
    if not operating:
        return
    for item in inventory:
        q = getattr(item, "quality", None)
        kind = getattr(q, "source_kind", None) if q is not None else None
        if kind == SourceKind.MOCK:
            raise MockOnOperatingPathError(
                f"mock source on operating path: {getattr(item, 'name', item)}"
            )


class SnapshotClient(Protocol):
    def snapshot(self, underlying: str, expiry: str | None = None) -> dict[str, Any]:
        ...

    def realized_vol(self, underlying: str, lookback: int = 20) -> float | None:
        ...

    def earnings_tickers(self, start: str, end: str) -> list[str] | None:
        ...
