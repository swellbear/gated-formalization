"""Load golf-offshoot/.env into os.environ. Never override a non-empty variable."""

from __future__ import annotations

import os
from pathlib import Path

from golf_offshoot.data_feeds.http import package_data_dir


def local_env_path() -> Path:
    return package_data_dir().parent / ".env"


def load_local_env(*, path: Path | None = None, force: bool = False) -> Path | None:
    """Read KEY=VALUE lines. Skipped under pytest unless force=True."""
    if not force and os.environ.get("PYTEST_CURRENT_TEST"):
        return None
    env_path = path or local_env_path()
    if not env_path.is_file():
        return None
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        if not key:
            continue
        if not os.environ.get(key, "").strip():
            os.environ[key] = value
    return env_path
