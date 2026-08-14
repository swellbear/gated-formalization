"""Disk-cached JSON HTTP. Snapshots keep operating runs reproducible."""

from __future__ import annotations

import hashlib
import json
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from golf_offshoot.data_feeds.base import FeedError

DEFAULT_BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)
DEFAULT_APP_UA = "golf-offshoot/0.7 (research; never-auto-bet)"


def package_data_dir() -> Path:
    return Path(__file__).resolve().parents[3] / "data"


def default_cache_dir() -> Path:
    return package_data_dir() / "cache"


class HttpCache:
    def __init__(self, cache_dir: Path | None = None) -> None:
        self.cache_dir = cache_dir or default_cache_dir()
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _path(self, url: str, extra: str = "") -> Path:
        key = hashlib.sha256((url + extra).encode("utf-8")).hexdigest()
        return self.cache_dir / f"{key}.json"

    def get_json(
        self,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        timeout: float = 30.0,
        ttl_seconds: float | None = None,
        refresh: bool = False,
        label: str = "",
        allow_stale_on_error: bool = False,
    ) -> tuple[Any, dict[str, Any]]:
        """Return (payload, meta). meta includes cached flag, fetched_at, url."""
        return self._json_request(
            url,
            method="GET",
            payload=None,
            headers=headers,
            timeout=timeout,
            ttl_seconds=ttl_seconds,
            refresh=refresh,
            label=label,
            allow_stale_on_error=allow_stale_on_error,
        )

    def post_json(
        self,
        url: str,
        payload: Any,
        *,
        headers: dict[str, str] | None = None,
        timeout: float = 45.0,
        ttl_seconds: float | None = None,
        refresh: bool = False,
        label: str = "",
        allow_stale_on_error: bool = False,
    ) -> tuple[Any, dict[str, Any]]:
        """POST JSON; cache key is sha256(url + canonical body)."""
        return self._json_request(
            url,
            method="POST",
            payload=payload,
            headers=headers,
            timeout=timeout,
            ttl_seconds=ttl_seconds,
            refresh=refresh,
            label=label,
            allow_stale_on_error=allow_stale_on_error,
        )

    def _read_envelope(self, path: Path) -> dict[str, Any] | None:
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None

    def _meta_from_envelope(
        self,
        *,
        url: str,
        method: str,
        label: str,
        envelope: dict[str, Any],
        cached: bool,
        stale_fallback: bool,
        now: float,
    ) -> dict[str, Any]:
        fetched = float(envelope.get("fetched_epoch", 0.0))
        return {
            "url": url,
            "cached": cached,
            "path": str(self._path(url)),
            "fetched_at": envelope.get("fetched_at"),
            "fetched_epoch": fetched,
            "age_seconds": max(0.0, now - fetched) if fetched else 0.0,
            "label": label or envelope.get("label", ""),
            "method": method,
            "stale_fallback": stale_fallback,
        }

    def _json_request(
        self,
        url: str,
        *,
        method: str,
        payload: Any,
        headers: dict[str, str] | None,
        timeout: float,
        ttl_seconds: float | None,
        refresh: bool,
        label: str,
        allow_stale_on_error: bool = False,
    ) -> tuple[Any, dict[str, Any]]:
        extra = ""
        if payload is not None:
            extra = "\n" + json.dumps(payload, sort_keys=True, separators=(",", ":"))
        path = self._path(url, extra)
        now = time.time()
        envelope = None if refresh else self._read_envelope(path)
        if envelope is not None:
            fetched = float(envelope.get("fetched_epoch", 0))
            if ttl_seconds is None or (now - fetched) <= ttl_seconds:
                meta = self._meta_from_envelope(
                    url=url,
                    method=method,
                    label=label,
                    envelope=envelope,
                    cached=True,
                    stale_fallback=False,
                    now=now,
                )
                meta["path"] = str(path)
                return envelope["body"], meta
        hdrs = {
            "Accept": "application/json",
            "User-Agent": DEFAULT_APP_UA,
        }
        if method == "POST":
            hdrs["Content-Type"] = "application/json"
        if headers:
            hdrs.update(headers)
        data = None
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
                status = getattr(resp, "status", 200)
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError) as exc:
            if allow_stale_on_error:
                stale_env = self._read_envelope(path)
                if stale_env is not None and "body" in stale_env:
                    meta = self._meta_from_envelope(
                        url=url,
                        method=method,
                        label=label,
                        envelope=stale_env,
                        cached=True,
                        stale_fallback=True,
                        now=now,
                    )
                    meta["path"] = str(path)
                    meta["error"] = str(exc)
                    return stale_env["body"], meta
            if isinstance(exc, urllib.error.HTTPError):
                raise FeedError(f"HTTP {exc.code} for {url}") from exc
            if isinstance(exc, urllib.error.URLError):
                raise FeedError(f"network error for {url}: {exc.reason}") from exc
            raise FeedError(f"network error for {url}: {exc}") from exc
        try:
            body = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError as exc:
            if allow_stale_on_error:
                stale_env = self._read_envelope(path)
                if stale_env is not None and "body" in stale_env:
                    meta = self._meta_from_envelope(
                        url=url,
                        method=method,
                        label=label,
                        envelope=stale_env,
                        cached=True,
                        stale_fallback=True,
                        now=now,
                    )
                    meta["path"] = str(path)
                    meta["error"] = "non-JSON"
                    return stale_env["body"], meta
            raise FeedError(f"non-JSON from {url}") from exc
        fetched_at = datetime.now(timezone.utc).isoformat()
        envelope = {
            "url": url,
            "method": method,
            "fetched_at": fetched_at,
            "fetched_epoch": now,
            "status": status,
            "label": label,
            "body": body,
        }
        path.write_text(json.dumps(envelope), encoding="utf-8")
        return body, {
            "url": url,
            "cached": False,
            "path": str(path),
            "fetched_at": fetched_at,
            "fetched_epoch": now,
            "age_seconds": 0.0,
            "label": label,
            "method": method,
            "stale_fallback": False,
        }
