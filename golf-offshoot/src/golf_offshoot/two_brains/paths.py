"""Two-brains journal root. Not a ledger. Not under either book's money tree."""

from __future__ import annotations

from pathlib import Path

REPO_FALLBACK = Path(__file__).resolve().parents[3] / "data" / "two_brains"
LIVE_15M_NAME = "learning_lane_15m"
HONER_NAME = "honer_15m"

_ROOT_OVERRIDE: Path | None = None


def set_two_brains_root_override(path: Path | None) -> None:
    global _ROOT_OVERRIDE
    _ROOT_OVERRIDE = path


def two_brains_root() -> Path:
    root = _ROOT_OVERRIDE if _ROOT_OVERRIDE is not None else REPO_FALLBACK
    root.mkdir(parents=True, exist_ok=True)
    assert_two_brains_path(root)
    return root


def latest_dir() -> Path:
    d = two_brains_root() / "latest"
    d.mkdir(parents=True, exist_ok=True)
    return d


def journal_path() -> Path:
    return latest_dir() / "journal.jsonl"


def assert_two_brains_path(path: Path) -> None:
    resolved = path.resolve()
    parts = {p.lower() for p in resolved.parts}
    if LIVE_15M_NAME in parts:
        raise RuntimeError("two_brains refused a learning_lane_15m path")
    if HONER_NAME in parts:
        raise RuntimeError("two_brains refused a honer ledger path")
