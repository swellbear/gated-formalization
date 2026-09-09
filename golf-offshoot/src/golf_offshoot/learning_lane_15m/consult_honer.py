"""AND-skip compositor for a dated honer consult.

Lives in the factory package. Reads ``latest/honer_consult.json`` only.
Never imports ``honer_15m``. Never reads ``honer_15m/latest/theta.json``.

Dark unless that snapshot exists and ``consult_enabled`` is exactly true.
Factory skip stays skip. Honer fill never forces a factory skip into a fill.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from golf_offshoot.learning_lane_15m.paths import latest_dir_15m

SNAPSHOT_NAME = "honer_consult.json"
FAMILY_RICH = "H-SKIP-RICH-YES"
FAMILY_SPREAD = "H-SKIP-WIDE-SPREAD"


def consult_snapshot_path(*, root: Path | None = None) -> Path:
    base = Path(root) if root is not None else latest_dir_15m()
    return base / SNAPSHOT_NAME


def load_consult_snapshot(*, root: Path | None = None) -> dict[str, Any] | None:
    path = consult_snapshot_path(root=root)
    if not path.is_file():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return payload if isinstance(payload, dict) else None


def consult_is_enabled(snapshot: dict[str, Any] | None) -> bool:
    return bool(snapshot) and snapshot.get("consult_enabled") is True


def market_spread(market: dict[str, Any] | None) -> float | None:
    if not market:
        return None
    try:
        bid = market.get("yes_bid")
        ask = market.get("yes_ask")
        if bid is None or ask is None:
            return None
        spread = float(ask) - float(bid)
    except (TypeError, ValueError):
        return None
    if spread < 0:
        return None
    return spread


def express_frozen_honer(
    snapshot: dict[str, Any],
    *,
    posted_yes: float,
    spread: float | None,
) -> tuple[str, str]:
    """Skip expression from frozen knobs. Mirrors honer families without importing them."""
    family = str(snapshot.get("family") or FAMILY_RICH)
    try:
        theta = float(snapshot.get("theta"))
    except (TypeError, ValueError) as exc:
        raise ValueError("honer consult snapshot is missing a numeric theta") from exc
    try:
        delta = float(snapshot.get("delta") or 0.0)
    except (TypeError, ValueError):
        delta = 0.0
    if family == FAMILY_SPREAD and spread is not None and float(spread) >= delta:
        return "skip", f"honer consult: spread {spread:g} >= delta {delta:g}"
    if float(posted_yes) >= theta:
        return "skip", f"honer consult: posted_yes >= theta {theta:g}"
    return "fill", f"honer consult: posted_yes below theta {theta:g}"


def compose_and_skip(
    factory_verdict: dict[str, Any],
    *,
    posted_yes: float,
    spread: float | None = None,
    root: Path | None = None,
    snapshot: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """AND-skip. Dark path returns the factory verdict object unchanged."""
    snap = snapshot if snapshot is not None else load_consult_snapshot(root=root)
    if not consult_is_enabled(snap):
        return factory_verdict
    assert snap is not None
    action = str(factory_verdict.get("action") or "")
    if action != "fill":
        return factory_verdict
    honer_action, honer_reason = express_frozen_honer(
        snap, posted_yes=posted_yes, spread=spread
    )
    if honer_action != "skip":
        return factory_verdict
    out = dict(factory_verdict)
    out["action"] = "skip"
    out["reason"] = honer_reason
    out["consult"] = "honer_and_skip"
    return out
