"""Quote-bus artifact root. Not learning_lane_15m. Not honer ledgers."""

from __future__ import annotations

from pathlib import Path

SERIES = "KXBTC15M"
REPO_FALLBACK = Path(__file__).resolve().parents[3] / "data" / "quote_bus"
LIVE_15M_NAME = "learning_lane_15m"
HONER_NAME = "honer_15m"

_ROOT_OVERRIDE: Path | None = None


def set_quote_bus_root_override(path: Path | None) -> None:
    global _ROOT_OVERRIDE
    _ROOT_OVERRIDE = path


def quote_bus_root() -> Path:
    root = _ROOT_OVERRIDE if _ROOT_OVERRIDE is not None else REPO_FALLBACK
    root.mkdir(parents=True, exist_ok=True)
    assert_quote_bus_path(root)
    return root


def latest_dir() -> Path:
    d = quote_bus_root() / "latest"
    d.mkdir(parents=True, exist_ok=True)
    return d


def snapshot_path() -> Path:
    return latest_dir() / f"{SERIES}.json"


def assert_quote_bus_path(path: Path) -> None:
    resolved = path.resolve()
    parts = {p.lower() for p in resolved.parts}
    if LIVE_15M_NAME in parts:
        raise RuntimeError("quote_bus refused a learning_lane_15m path")
    if HONER_NAME in parts and "quote_bus" not in parts:
        raise RuntimeError("quote_bus refused a honer ledger path")
