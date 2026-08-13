"""In-process mock feeds so the pipeline runs without vendor keys."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from golf_offshoot.data_feeds.base import DataFeed
from golf_offshoot.models.enums import DataRole
from golf_offshoot.models.schemas import DataQuality, MarketQuote, Player, StrokesGainedProfile
from golf_offshoot.models.enums import BetType


def _q(name: str, score: float, n: int, role: DataRole = DataRole.MOCK) -> DataQuality:
    return DataQuality(
        score=score,
        role=role,
        source_name=name,
        as_of=datetime.now(timezone.utc),
        n_observations=n,
    )


class MockTalentFeed(DataFeed[dict[str, tuple[float, float]]]):
    name = "mock_talent"
    role = DataRole.MOCK

    def __init__(self, table: dict[str, tuple[float, float]] | None = None) -> None:
        self.table = table or {}

    def fetch(self, **kwargs: Any) -> tuple[dict[str, tuple[float, float]], DataQuality]:
        return self.table, _q(self.name, 0.80, len(self.table))


class MockSGFeed(DataFeed[dict[str, StrokesGainedProfile]]):
    name = "mock_sg"
    role = DataRole.MOCK

    def __init__(self, table: dict[str, StrokesGainedProfile] | None = None) -> None:
        self.table = table or {}

    def fetch(self, **kwargs: Any) -> tuple[dict[str, StrokesGainedProfile], DataQuality]:
        return self.table, _q(self.name, 0.75, len(self.table))


class MockWeatherFeed(DataFeed[dict[str, Any]]):
    name = "mock_weather"
    role = DataRole.MOCK

    def fetch(self, **kwargs: Any) -> tuple[dict[str, Any], DataQuality]:
        payload = {
            "wind_mph": 12.0,
            "gust_mph": 20.0,
            "rain_mm": 0.0,
            "summary": "moderate breeze, dry",
        }
        return payload, _q(self.name, 0.65, 1)


class MockOddsFeed(DataFeed[list[MarketQuote]]):
    name = "mock_odds"
    role = DataRole.MOCK

    def __init__(self, quotes: list[MarketQuote] | None = None) -> None:
        self.quotes = quotes or []

    def fetch(self, **kwargs: Any) -> tuple[list[MarketQuote], DataQuality]:
        return self.quotes, _q(self.name, 0.70, len(self.quotes))


class MockInjuryFeed(DataFeed[dict[str, float]]):
    name = "mock_injury"
    role = DataRole.MOCK

    def __init__(self, flags: dict[str, float] | None = None) -> None:
        self.flags = flags or {}

    def fetch(self, **kwargs: Any) -> tuple[dict[str, float], DataQuality]:
        # sparse by nature
        return self.flags, _q(self.name, 0.30 if self.flags else 0.15, max(1, len(self.flags)))


class MockFieldFeed(DataFeed[list[Player]]):
    name = "mock_field"
    role = DataRole.MOCK

    def __init__(self, players: list[Player] | None = None) -> None:
        self.players = players or []

    def fetch(self, **kwargs: Any) -> tuple[list[Player], DataQuality]:
        return self.players, _q(self.name, 0.90, len(self.players))


# Placeholder primary that always fails — used to test fallback
class UnreachablePrimary(DataFeed[dict]):
    name = "unreachable_primary"
    role = DataRole.PRIMARY

    def fetch(self, **kwargs: Any) -> tuple[dict, DataQuality]:
        raise RuntimeError("vendor timeout")
