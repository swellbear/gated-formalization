"""Golf Kalshi artifact root. Never the 15m tree, Honer, or Phase 1 Polymarket paper."""

from __future__ import annotations

from pathlib import Path

LANE = "golf_kalshi"
LIVE_15M_NAME = "learning_lane_15m"
HONER_NAME = "honer_15m"
PHASE1_PAPER = "paper"
FORBIDDEN_EXPORT = Path("/workspace/kalshi_15m_exports")
REPO_FALLBACK = Path(__file__).resolve().parents[3] / "data" / "golf_kalshi"

_ROOT_OVERRIDE: Path | None = None


def set_golf_kalshi_root_override(path: Path | None) -> None:
    global _ROOT_OVERRIDE
    _ROOT_OVERRIDE = path


def golf_kalshi_root() -> Path:
    if _ROOT_OVERRIDE is not None:
        _ROOT_OVERRIDE.mkdir(parents=True, exist_ok=True)
        assert_golf_kalshi_path(_ROOT_OVERRIDE)
        return _ROOT_OVERRIDE
    REPO_FALLBACK.mkdir(parents=True, exist_ok=True)
    assert_golf_kalshi_path(REPO_FALLBACK)
    return REPO_FALLBACK


def latest_dir() -> Path:
    d = golf_kalshi_root() / "latest"
    d.mkdir(parents=True, exist_ok=True)
    return d


def paper_dir() -> Path:
    d = golf_kalshi_root() / "paper"
    d.mkdir(parents=True, exist_ok=True)
    return d


def settlements_dir() -> Path:
    d = golf_kalshi_root() / "settlements"
    d.mkdir(parents=True, exist_ok=True)
    return d


def cache_dir() -> Path:
    d = golf_kalshi_root() / "cache"
    d.mkdir(parents=True, exist_ok=True)
    return d


def ledger_path() -> Path:
    return paper_dir() / "ledger.json"


def decisions_path() -> Path:
    return paper_dir() / "decisions.json"


def catalog_path() -> Path:
    return latest_dir() / "catalog.json"


def watch_status_path() -> Path:
    return latest_dir() / "watch.json"


def last_tick_path() -> Path:
    return latest_dir() / "last_tick.json"


def unmatched_path() -> Path:
    return latest_dir() / "unmatched.json"


def brain_cache_path() -> Path:
    return latest_dir() / "brain_cache.json"


def recipe_exam_path() -> Path:
    return latest_dir() / "recipe_exam.json"


def brain_score_path() -> Path:
    return latest_dir() / "brain_score.json"


def board_png_path() -> Path:
    return latest_dir() / "golf_window_strip.png"


def farm_path() -> Path:
    return latest_dir() / "farm.json"


def honer_dir() -> Path:
    d = golf_kalshi_root() / "honer"
    d.mkdir(parents=True, exist_ok=True)
    assert_golf_kalshi_path(d)
    return d


def honer_status_path() -> Path:
    return honer_dir() / "status.json"


def watch_kill_path() -> Path:
    return latest_dir() / "WATCH_KILL"


def trading_armed_path() -> Path:
    return latest_dir() / "TRADING_ARMED"


def trading_is_armed() -> bool:
    return trading_armed_path().is_file()


def watch_is_killed() -> bool:
    return watch_kill_path().is_file()


def safe_artifact_stem(name: str, *, fallback: str = "market") -> str:
    safe = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in str(name or ""))
    return safe.strip("-") or fallback


def assert_golf_kalshi_path(path: Path) -> None:
    resolved = path.resolve()
    parts = {p.lower() for p in resolved.parts}
    if LIVE_15M_NAME in parts:
        raise RuntimeError("golf_kalshi refused a learning_lane_15m path")
    if HONER_NAME in parts:
        raise RuntimeError("golf_kalshi refused a honer_15m path")
    if "polymarket" in parts:
        raise RuntimeError("golf_kalshi refused a polymarket path")
    try:
        if resolved == FORBIDDEN_EXPORT.resolve() or FORBIDDEN_EXPORT.resolve() in resolved.parents:
            raise RuntimeError("golf_kalshi refused kalshi_15m_exports")
    except OSError:
        if "kalshi_15m_exports" in parts:
            raise RuntimeError("golf_kalshi refused kalshi_15m_exports") from None
    # Phase 1 lived paper lives at data/paper, not data/golf_kalshi/paper.
    try:
        phase1 = Path(__file__).resolve().parents[3] / "data" / PHASE1_PAPER
        if resolved == phase1.resolve() or phase1.resolve() in resolved.parents:
            raise RuntimeError("golf_kalshi refused Phase 1 paper/")
    except OSError:
        pass
