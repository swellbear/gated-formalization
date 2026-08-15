"""Open-Meteo weather connector (no API key). Forecast + archive are real sources."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from urllib.parse import quote

from golf_offshoot.data_feeds.base import DataFeed, unavailable_quality
from golf_offshoot.data_feeds.http import DEFAULT_APP_UA, HttpCache
from golf_offshoot.localtime import now
from golf_offshoot.models.enums import DataRole, SourceKind
from golf_offshoot.models.schemas import DataQuality

GEO = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST = "https://api.open-meteo.com/v1/forecast"
ARCHIVE = "https://archive-api.open-meteo.com/v1/archive"


class OpenMeteoClient:
    def __init__(self, cache: HttpCache | None = None, refresh: bool = False) -> None:
        self.cache = cache or HttpCache()
        self.refresh = refresh

    def _get(self, url: str, ttl: float | None, label: str) -> Any:
        body, _ = self.cache.get_json(
            url,
            headers={"User-Agent": DEFAULT_APP_UA, "Accept": "application/json"},
            ttl_seconds=ttl,
            refresh=self.refresh,
            label=label,
        )
        return body

    def geocode(self, city: str, region: str = "", country: str = "US") -> tuple[float, float] | None:
        if not city:
            return None
        q = quote(f"{city} {region}".strip())
        url = f"{GEO}?name={q}&count=5&language=en&format=json&country={quote(country)}"
        payload = self._get(url, ttl=None, label=f"geocode_{city}")
        results = payload.get("results") or []
        if not results:
            return None
        if region:
            region_l = region.lower()
            for row in results:
                admin = str(row.get("admin1") or "")
                if region_l in admin.lower() or admin.lower() in region_l:
                    return float(row["latitude"]), float(row["longitude"])
        row = results[0]
        return float(row["latitude"]), float(row["longitude"])

    def forecast(self, lat: float, lon: float, days: int = 5) -> dict[str, Any]:
        url = (
            f"{FORECAST}?latitude={lat:.4f}&longitude={lon:.4f}"
            f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,"
            f"wind_speed_10m_max,wind_gusts_10m_max"
            f"&timezone=auto&forecast_days={days}"
        )
        return self._get(url, ttl=3600, label="openmeteo_forecast")

    def archive(self, lat: float, lon: float, start: str, end: str) -> dict[str, Any]:
        url = (
            f"{ARCHIVE}?latitude={lat:.4f}&longitude={lon:.4f}"
            f"&start_date={start}&end_date={end}"
            f"&daily=temperature_2m_max,precipitation_sum,wind_speed_10m_max"
            f"&timezone=auto"
        )
        return self._get(url, ttl=None, label=f"openmeteo_archive_{start}")


def summarize_daily(daily: dict[str, Any]) -> dict[str, Any]:
    winds = [w for w in (daily.get("wind_speed_10m_max") or []) if w is not None]
    rains = [r for r in (daily.get("precipitation_sum") or []) if r is not None]
    tmax = [t for t in (daily.get("temperature_2m_max") or []) if t is not None]
    gusts = [g for g in (daily.get("wind_gusts_10m_max") or []) if g is not None]
    wind_kph = float(sum(winds) / len(winds)) if winds else None
    return {
        "wind_kph": wind_kph,
        "wind_mph": None if wind_kph is None else wind_kph / 1.609,
        "gust_kph": float(max(gusts)) if gusts else None,
        "rain_mm": float(sum(rains)) if rains else 0.0,
        "temp_c_max": float(max(tmax)) if tmax else None,
        "n_days": len(daily.get("time") or []),
    }


class OpenMeteoWeatherFeed(DataFeed[dict[str, Any]]):
    name = "open_meteo"
    role = DataRole.PRIMARY

    def __init__(self, client: OpenMeteoClient) -> None:
        self.client = client

    def fetch(self, **kwargs: Any) -> tuple[dict[str, Any], DataQuality]:
        city = str(kwargs.get("city") or "")
        region = str(kwargs.get("region") or "")
        start = kwargs.get("start_date")
        end = kwargs.get("end_date") or start
        historical = bool(kwargs.get("historical", False))
        coords = self.client.geocode(city, region)
        if coords is None:
            q = unavailable_quality(self.name, f"geocode failed for {city}, {region}")
            q.role = self.role
            return {}, q
        lat, lon = coords
        if historical and start:
            raw = self.client.archive(lat, lon, str(start), str(end))
            kind = SourceKind.REAL_HISTORICAL
            notes = f"Open-Meteo archive {start}..{end} at {lat:.3f},{lon:.3f}"
        else:
            raw = self.client.forecast(lat, lon)
            kind = SourceKind.REAL_LIVE
            notes = f"Open-Meteo forecast at {lat:.3f},{lon:.3f}"
        daily = raw.get("daily") or {}
        summary = summarize_daily(daily)
        summary["lat"] = lat
        summary["lon"] = lon
        summary["raw_daily"] = {k: daily.get(k) for k in ("time", "wind_speed_10m_max", "precipitation_sum")}
        wind = summary.get("wind_mph") or 0.0
        rain = summary.get("rain_mm") or 0.0
        summary["summary"] = f"wind ~{wind:.0f} mph, rain {rain:.1f} mm (Open-Meteo)"
        q = DataQuality(
            score=0.80,
            role=self.role,
            source_name=self.name,
            as_of=now(),
            n_observations=int(summary.get("n_days") or 1),
            notes=notes,
            missing=False,
            source_kind=kind,
        )
        return summary, q
