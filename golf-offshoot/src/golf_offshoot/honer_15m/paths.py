"""Honer artifact root. Never the live 15m tree or kalshi_15m_exports."""

from __future__ import annotations

from pathlib import Path

LANE = "honer_15m"
SERIES = "KXBTC15M"
REPO_HONER_FALLBACK = Path(__file__).resolve().parents[3] / "data" / "honer_15m"
LIVE_15M_NAME = "learning_lane_15m"
FORBIDDEN_EXPORT = Path("/workspace/kalshi_15m_exports")

_ROOT_OVERRIDE: Path | None = None


def set_honer_root_override(path: Path | None) -> None:
    global _ROOT_OVERRIDE
    _ROOT_OVERRIDE = path


def honer_root() -> Path:
    if _ROOT_OVERRIDE is not None:
        _ROOT_OVERRIDE.mkdir(parents=True, exist_ok=True)
        assert_honer_path(_ROOT_OVERRIDE)
        return _ROOT_OVERRIDE
    REPO_HONER_FALLBACK.mkdir(parents=True, exist_ok=True)
    assert_honer_path(REPO_HONER_FALLBACK)
    return REPO_HONER_FALLBACK


def search_dir() -> Path:
    d = honer_root() / "search"
    d.mkdir(parents=True, exist_ok=True)
    return d


def exam_dir() -> Path:
    d = honer_root() / "exam"
    d.mkdir(parents=True, exist_ok=True)
    return d


def paper_dir(book: str) -> Path:
    d = (search_dir() if book == "search" else exam_dir()) / "paper"
    d.mkdir(parents=True, exist_ok=True)
    return d


def ledger_path(book: str) -> Path:
    return (search_dir() if book == "search" else exam_dir()) / "ledger.json"


def decisions_path(book: str) -> Path:
    return (search_dir() if book == "search" else exam_dir()) / "decisions.json"


def settlements_dir() -> Path:
    d = honer_root() / "settlements"
    d.mkdir(parents=True, exist_ok=True)
    return d


def latest_dir() -> Path:
    d = honer_root() / "latest"
    d.mkdir(parents=True, exist_ok=True)
    return d


def cache_dir() -> Path:
    d = honer_root() / "cache"
    d.mkdir(parents=True, exist_ok=True)
    return d


def theta_path() -> Path:
    return latest_dir() / "theta.json"


def exam_state_path() -> Path:
    return latest_dir() / "exam.json"


def freeze_log_path() -> Path:
    return latest_dir() / "freeze_log.json"


def trials_path() -> Path:
    return latest_dir() / "trials.json"


def watch_status_path() -> Path:
    return latest_dir() / "watch.json"


def board_png_path() -> Path:
    """Local honer strip. Never the Lineage A observability-hub PNG."""
    return latest_dir() / "honer_window_strip.png"


def registry_path() -> Path:
    return Path(__file__).resolve().parents[3] / "docs" / "HONER_15M_RULES.json"


def catalog_path() -> Path:
    return Path(__file__).resolve().parents[3] / "docs" / "HONER_15M_CATALOG.json"


def library_path() -> Path:
    return latest_dir() / "library.json"


def quote_quality_path() -> Path:
    return latest_dir() / "quote_quality.json"


def last_tick_path() -> Path:
    return latest_dir() / "last_tick.json"


def invariants_path() -> Path:
    return latest_dir() / "invariants.json"


def exam_score_path() -> Path:
    """Machine exam score/park artifact. Not a keep. Never a 15m path."""
    return latest_dir() / "exam_score.json"


def family_amend_path() -> Path:
    """File doorbell that HONER-FAMILY-AMEND is owed. Not pnl. Not a third family."""
    return latest_dir() / "family_amend.json"


def safe_artifact_stem(name: str, *, fallback: str = "event") -> str:
    safe = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in str(name or ""))
    return safe.strip("-") or fallback


def assert_honer_path(path: Path) -> None:
    resolved = path.resolve()
    parts = {p.lower() for p in resolved.parts}
    if LIVE_15M_NAME in parts:
        raise RuntimeError("honer_15m refused a learning_lane_15m path")
    try:
        if resolved == FORBIDDEN_EXPORT.resolve() or FORBIDDEN_EXPORT.resolve() in resolved.parents:
            raise RuntimeError("honer_15m refused kalshi_15m_exports")
    except OSError:
        if "kalshi_15m_exports" in parts:
            raise RuntimeError("honer_15m refused kalshi_15m_exports") from None
