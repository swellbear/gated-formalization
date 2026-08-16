"""Tiny HTTP GET with disk cache. No vendor swap."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from options_offshoot.data_feeds.local_env import package_root
from options_offshoot.config import CACHE_DIR

UA = "options-offshoot/0.1.0 (paper; never auto-trade)"


def cache_dir() -> Path:
    d = package_root() / CACHE_DIR
    d.mkdir(parents=True, exist_ok=True)
    return d


def _key(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:32]


def get_json(url: str, *, timeout: float = 30.0, use_cache: bool = True) -> dict:
    path = cache_dir() / f"{_key(url)}.json"
    if use_cache and path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    req = Request(url, headers={"User-Agent": UA})
    try:
        with urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
    except HTTPError as exc:
        raise RuntimeError(f"http {exc.code} for {url}") from exc
    except URLError as exc:
        raise RuntimeError(f"http fail for {url}: {exc}") from exc
    data = json.loads(raw)
    path.write_text(json.dumps(data), encoding="utf-8")
    return data
