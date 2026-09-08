"""Load the 15m evidence bar and burned-class registry.

Does not score a rule. Does not read window outcomes.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

BAR_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_EVIDENCE_BAR.json"
BURNED_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_BURNED_CLASSES.json"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def bar_path(*, root: Path | None = None) -> Path:
    return (Path(root) if root is not None else _repo_root()) / BAR_REL


def burned_path(*, root: Path | None = None) -> Path:
    return (Path(root) if root is not None else _repo_root()) / BURNED_REL


def load_evidence_bar(*, root: Path | None = None) -> dict[str, Any]:
    payload = json.loads(bar_path(root=root).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("evidence bar must be an object")
    return payload


def load_burned_classes(*, root: Path | None = None) -> dict[str, Any]:
    payload = json.loads(burned_path(root=root).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("burned-class registry must be an object")
    return payload


def bar_is_binding(*, root: Path | None = None) -> bool:
    return bool(load_evidence_bar(root=root).get("binding"))


def class_is_burned(name: str, *, root: Path | None = None) -> bool:
    """True if name matches a burned id or alias. FRAGILE-not-null is not burned."""
    needle = str(name or "").strip()
    if not needle:
        return False
    payload = load_burned_classes(root=root)
    upper = needle.upper()
    for row in payload.get("classes") or []:
        if not row.get("burned"):
            continue
        cid = str(row.get("id") or "")
        aliases = [str(a) for a in (row.get("aliases") or [])]
        names = [cid, *aliases]
        if any(upper == n.upper() or upper.replace("_", "-") == n.upper().replace("_", "-") for n in names):
            return True
    return False


def fragile_not_null(name: str, *, root: Path | None = None) -> bool:
    needle = str(name or "").strip().upper()
    payload = load_burned_classes(root=root)
    for row in payload.get("fragile_not_null") or []:
        if str(row.get("id") or "").upper() == needle:
            return True
    return False
