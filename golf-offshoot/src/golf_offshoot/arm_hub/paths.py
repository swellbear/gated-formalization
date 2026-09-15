"""ARM hub artifact roots. Never share trees with the learning-lane hub.

Hard NO: read or write ``data/learning_lane_15m/**``,
``/workspace/kalshi_15m_exports``, or ``/workspace/kalshi_15m_lab``.
"""

from __future__ import annotations

import os
from pathlib import Path

HUB_ID = "arm_hub"
SERIES_DEFAULT = "KXBTC15M"
PAPER_BANKROLL_OPEN = 500.0

# Fragments that identify the sacred learning-lane / leftover-hunt paper hub.
_LEARNING_LANE_MARKERS = (
    "learning_lane_15m",
    "kalshi_15m_exports",
    "kalshi_15m_lab",
)

_ROOT_OVERRIDE: Path | None = None


def package_dir() -> Path:
    return Path(__file__).resolve().parent


def golf_offshoot_root() -> Path:
    """``golf-offshoot/`` (the package checkout), not the git repo root."""
    return Path(__file__).resolve().parents[3]


def default_data_root() -> Path:
    return golf_offshoot_root() / "data" / "arm_hub"


def set_arm_hub_root_override(path: Path | None) -> None:
    """Test hook. None restores the default data tree."""
    global _ROOT_OVERRIDE
    _ROOT_OVERRIDE = path


def arm_hub_root() -> Path:
    if _ROOT_OVERRIDE is not None:
        root = _ROOT_OVERRIDE
    else:
        env = (os.environ.get("ARM_HUB_ROOT") or "").strip()
        root = Path(env) if env else default_data_root()
    root = root.resolve()
    assert_not_learning_lane_path(root)
    root.mkdir(parents=True, exist_ok=True)
    return root


def assert_not_learning_lane_path(path: Path | str) -> Path:
    """Refuse any path that lands in the learning-lane hub trees."""
    resolved = Path(path).expanduser()
    try:
        resolved = resolved.resolve()
    except OSError:
        resolved = Path(path)
    blob = str(resolved).replace("\\", "/").lower()
    parts = {p.lower() for p in resolved.parts}
    for marker in _LEARNING_LANE_MARKERS:
        if marker in parts or f"/{marker}/" in f"/{blob}/" or blob.endswith(f"/{marker}"):
            raise LearningLanePathRefused(
                f"ARM hub refused learning-lane path ({marker}): {path}"
            )
    return resolved


def paper_dir(root: Path | None = None) -> Path:
    d = (root or arm_hub_root()) / "paper"
    assert_not_learning_lane_path(d)
    d.mkdir(parents=True, exist_ok=True)
    return d


def fills_dir(root: Path | None = None) -> Path:
    d = paper_dir(root) / "fills"
    d.mkdir(parents=True, exist_ok=True)
    return d


def settlements_dir(root: Path | None = None) -> Path:
    d = paper_dir(root) / "settlements"
    d.mkdir(parents=True, exist_ok=True)
    return d


def latest_dir(root: Path | None = None) -> Path:
    d = (root or arm_hub_root()) / "latest"
    assert_not_learning_lane_path(d)
    d.mkdir(parents=True, exist_ok=True)
    return d


def strategies_dir(root: Path | None = None) -> Path:
    d = (root or arm_hub_root()) / "strategies"
    assert_not_learning_lane_path(d)
    d.mkdir(parents=True, exist_ok=True)
    return d


def audit_dir(root: Path | None = None) -> Path:
    d = (root or arm_hub_root()) / "audit"
    assert_not_learning_lane_path(d)
    d.mkdir(parents=True, exist_ok=True)
    return d


def ledger_path(root: Path | None = None) -> Path:
    return paper_dir(root) / "ledger.json"


def state_path(root: Path | None = None) -> Path:
    return latest_dir(root) / "state.json"


def arm_flag_path(root: Path | None = None) -> Path:
    return latest_dir(root) / "ARM.flag"


def kill_path(root: Path | None = None) -> Path:
    return latest_dir(root) / "KILL"


def pid_path(root: Path | None = None) -> Path:
    return latest_dir(root) / "watch.pid"


def policy_path(root: Path | None = None) -> Path:
    return strategies_dir(root) / "POLICY.json"


def shortlist_pin_path(root: Path | None = None) -> Path:
    return strategies_dir(root) / "shortlist_v1.json"


def shelf_pin_path(root: Path | None = None) -> Path:
    return strategies_dir(root) / "SHORTLIST_SHELF.json"


def config_path(root: Path | None = None) -> Path:
    return (root or arm_hub_root()) / "config.yaml"


def replay_tape_path(root: Path | None = None) -> Path:
    return (root or arm_hub_root()) / "fixtures" / "replay_tape.json"


class LearningLanePathRefused(RuntimeError):
    """ARM hub must not touch the sacred learning-lane trees."""
