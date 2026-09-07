"""Lane-scoped artifact roots. Golf and 15-min journals never share a directory."""

from __future__ import annotations

from pathlib import Path

from golf_offshoot.data_feeds.http import package_data_dir

LANE_GOLF = "golf"
LANE_15M = "learning_lane_15m"
LANE_NAME = "learning_lane_15m"
PRIMARY_SERIES = "KXBTC15M"

# External default for this lane only. Golf paper/shadow stay under golf-offshoot/data/.
EXTERNAL_15M_ROOT = Path("/workspace/kalshi_15m_exports")
REPO_15M_FALLBACK = Path(__file__).resolve().parents[3] / "data" / "learning_lane_15m"

# Digestor boards are read-only reference. Do not rewrite. Do not invent docs.
DIGESTOR_LAB_ROOT = Path("/workspace/kalshi_15m_lab")
DIGESTOR_BOARDS = (
    DIGESTOR_LAB_ROOT / "SPINE_STAMP.md",
    DIGESTOR_LAB_ROOT / "SOURCE_INDEX.md",
    DIGESTOR_LAB_ROOT / "LIVING_SPINE_INDEX.md",
    DIGESTOR_LAB_ROOT / "SOURCE",
)

# Tests / operators may override. Production default prefers the external root.
_ROOT_OVERRIDE: Path | None = None


def set_15m_root_override(path: Path | None) -> None:
    """Test hook. None restores default resolution."""
    global _ROOT_OVERRIDE
    _ROOT_OVERRIDE = path


def golf_data_root() -> Path:
    """Golf Phase 1 artifacts. Untouched by the 15-min lane."""
    return package_data_dir()


def golf_paper_dir() -> Path:
    return golf_data_root() / "paper"


def golf_shadow_dir() -> Path:
    return golf_data_root() / "shadow"


def artifact_root_15m() -> Path:
    """15-min journal root only. Never golf-offshoot/data/paper."""
    if _ROOT_OVERRIDE is not None:
        _ROOT_OVERRIDE.mkdir(parents=True, exist_ok=True)
        return _ROOT_OVERRIDE
    if EXTERNAL_15M_ROOT.parent.is_dir():
        try:
            EXTERNAL_15M_ROOT.mkdir(parents=True, exist_ok=True)
            return EXTERNAL_15M_ROOT
        except OSError:
            pass
    REPO_15M_FALLBACK.mkdir(parents=True, exist_ok=True)
    return REPO_15M_FALLBACK


def paper_dir_15m() -> Path:
    d = artifact_root_15m() / "paper"
    d.mkdir(parents=True, exist_ok=True)
    return d


def shadow_dir_15m() -> Path:
    d = artifact_root_15m() / "shadow"
    d.mkdir(parents=True, exist_ok=True)
    return d


def snapshots_dir_15m() -> Path:
    d = artifact_root_15m() / "snapshots"
    d.mkdir(parents=True, exist_ok=True)
    return d


def latest_dir_15m() -> Path:
    d = artifact_root_15m() / "latest"
    d.mkdir(parents=True, exist_ok=True)
    return d


def settlements_dir_15m() -> Path:
    d = artifact_root_15m() / "settlements"
    d.mkdir(parents=True, exist_ok=True)
    return d


def assert_not_golf_path(path: Path) -> None:
    """Hard NO: 15-min writes must not land in the golf paper/shadow trees."""
    resolved = path.resolve()
    golf_paper = golf_paper_dir().resolve()
    golf_shadow = golf_shadow_dir().resolve()
    if resolved == golf_paper or golf_paper in resolved.parents:
        raise RuntimeError("15-min lane refused to write into golf paper/")
    if resolved == golf_shadow or golf_shadow in resolved.parents:
        raise RuntimeError("15-min lane refused to write into golf shadow/")


def journal_label(lane: str) -> str:
    return "15m" if lane == LANE_15M else "golf"
