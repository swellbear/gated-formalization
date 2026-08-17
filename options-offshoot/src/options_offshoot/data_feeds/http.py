"""Tiny HTTP GET with disk cache. Cache key never includes apiKey."""

from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse
from urllib.request import Request, urlopen

from options_offshoot.config import CACHE_DIR, HTTP_429_RETRIES, MAX_STALE_QUOTE_S
from options_offshoot.data_feeds.local_env import package_root

UA = "options-offshoot/0.2.0 (paper; never auto-trade)"


class StaleCacheError(RuntimeError):
    """Cached quote older than max stale and refetch failed."""


class HttpError(RuntimeError):
    def __init__(self, message: str, *, status: int | None = None) -> None:
        super().__init__(message)
        self.status = status


def cache_dir() -> Path:
    d = package_root() / CACHE_DIR
    d.mkdir(parents=True, exist_ok=True)
    return d


def url_without_api_key(url: str) -> str:
    parsed = urlparse(url)
    pairs = [
        (k, v)
        for k, v in parse_qsl(parsed.query, keep_blank_values=True)
        if k.lower() != "apikey"
    ]
    return urlunparse(parsed._replace(query=urlencode(pairs)))


def cache_key(url: str) -> str:
    return hashlib.sha256(url_without_api_key(url).encode("utf-8")).hexdigest()


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _parse_cached_at(raw: str | None) -> datetime | None:
    if not raw:
        return None
    text = raw.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _age_s(cached_at: datetime | None, mtime: float) -> float:
    if cached_at is not None:
        return max(0.0, (_now() - cached_at.astimezone(timezone.utc)).total_seconds())
    return max(0.0, time.time() - mtime)


def _unwrap(raw: dict, mtime: float) -> tuple[dict, float]:
    if isinstance(raw, dict) and "payload" in raw and "cached_at" in raw:
        return raw["payload"], _age_s(_parse_cached_at(str(raw.get("cached_at"))), mtime)
    return raw, _age_s(None, mtime)


def _fetch(url: str, timeout: float) -> dict:
    req = Request(url, headers={"User-Agent": UA})
    delay = 1.5
    last_exc: Exception | None = None
    for attempt in range(HTTP_429_RETRIES + 1):
        try:
            with urlopen(req, timeout=timeout) as resp:
                raw = resp.read().decode("utf-8")
            return json.loads(raw)
        except HTTPError as exc:
            last_exc = HttpError(f"http {exc.code} for {url_without_api_key(url)}", status=exc.code)
            if exc.code == 429 and attempt < HTTP_429_RETRIES:
                time.sleep(delay)
                delay *= 2
                continue
            raise last_exc from exc
        except URLError as exc:
            last_exc = HttpError(f"http fail for {url_without_api_key(url)}: {exc}")
            if attempt < HTTP_429_RETRIES:
                time.sleep(delay)
                delay *= 2
                continue
            raise last_exc from exc
    raise last_exc or HttpError(f"http fail for {url_without_api_key(url)}")


def get_json(
    url: str,
    *,
    timeout: float = 30.0,
    use_cache: bool = True,
    ttl_s: float | None = None,
    max_stale_s: float | None = MAX_STALE_QUOTE_S,
) -> dict:
    path = cache_dir() / f"{cache_key(url)}.json"
    cached_payload: dict | None = None
    age = None
    if use_cache and path.is_file():
        try:
            wrapped = json.loads(path.read_text(encoding="utf-8"))
            cached_payload, age = _unwrap(wrapped, path.stat().st_mtime)
        except (OSError, json.JSONDecodeError, TypeError, ValueError):
            cached_payload, age = None, None
        if cached_payload is not None and ttl_s is not None and age is not None and age <= ttl_s:
            return cached_payload
    try:
        data = _fetch(url, timeout)
    except HttpError as exc:
        if (
            cached_payload is not None
            and age is not None
            and max_stale_s is not None
            and age <= max_stale_s
        ):
            return cached_payload
        if cached_payload is not None and max_stale_s is not None and age is not None and age > max_stale_s:
            raise StaleCacheError(
                f"stale cache age={age:.0f}s max={max_stale_s:.0f}s for {url_without_api_key(url)}"
            ) from exc
        raise
    envelope = {"cached_at": _now().isoformat(), "payload": data}
    path.write_text(json.dumps(envelope), encoding="utf-8")
    return data
