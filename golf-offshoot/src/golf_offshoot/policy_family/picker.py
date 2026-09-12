"""P-FAMILY-SEARCH doorbell from files. Unused named P-*, file order.

Same shape as the honer file doorbell: owed off files, not pnl, does not
date a factory row, does not ping Lab. Finite picker. Not 3^N. Not a clip walk.
"""

from __future__ import annotations

import json
from typing import Any

from golf_offshoot.localtime import now
from golf_offshoot.policy_family.library import (
    CATALOG_KIND,
    COMPARISON_ID,
    PolicyFamilyError,
    lessons_path,
    load_library,
    picker_path,
    policy_ids,
    registry_path,
)

REASON_UNUSED = "unused_named"
MONEY_KEYS = frozenset({"pnl", "d", "bankroll", "winner", "mean_d", "exam_pnl", "betting_pnl"})
RETIRED_CARDS = frozenset({"density_fail", "undecidable", "park_vs_fill_all", "untestable"})


def _load_json(path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _named_skip_ids(*, root=None) -> list[str]:
    """File order, comparison book excluded. Pnl does not rank."""
    return [ident for ident in policy_ids(root=root) if ident != COMPARISON_ID]


def _lessons_by_id(*, root=None) -> dict[str, dict[str, Any]]:
    payload = _load_json(lessons_path(root=root))
    out: dict[str, dict[str, Any]] = {}
    for row in payload.get("rows") or []:
        if not isinstance(row, dict):
            continue
        ident = str(row.get("id") or "").strip()
        if ident:
            out[ident] = row
    return out


def _taken_ids(*, root=None) -> set[str]:
    """Factory registry ids only. Does not write the registry. R-* does not take P-*."""
    payload = _load_json(registry_path(root=root))
    out: set[str] = set()
    for row in payload.get("rules") or []:
        if isinstance(row, dict) and row.get("id"):
            out.add(str(row["id"]))
    return out


def retired_named_from_files(*, root=None) -> list[str]:
    """Search-done names (density-fail / park). Do not retune. Not a factory PARK."""
    lessons = _lessons_by_id(root=root)
    retired: list[str] = []
    for ident in _named_skip_ids(root=root):
        card = str((lessons.get(ident) or {}).get("card") or "")
        if card in RETIRED_CARDS:
            retired.append(ident)
    return retired


def unused_named_from_files(*, root=None) -> list[str]:
    """Unused named P-* in file order. Comparison is never a pick. Not tape-sorted."""
    taken = _taken_ids(root=root)
    retired = set(retired_named_from_files(root=root))
    unused: list[str] = []
    for ident in _named_skip_ids(root=root):
        if ident in taken or ident in retired:
            continue
        unused.append(ident)
    return unused


def next_named_from_files(*, root=None) -> str | None:
    unused = unused_named_from_files(root=root)
    return unused[0] if unused else None


def picker_reasons_from_files(*, root=None) -> list[str]:
    if unused_named_from_files(root=root):
        return [REASON_UNUSED]
    return []


def picker_owed_from_files(*, root=None) -> bool:
    return bool(picker_reasons_from_files(root=root))


def stamp_picker(*, root=None) -> dict[str, Any]:
    """Write gitignored picker stamp. Does not date a factory row. No money keys."""
    load_library(root=root)
    unused = unused_named_from_files(root=root)
    reasons = picker_reasons_from_files(root=root)
    payload = {
        "schema": 1,
        "lane": "learning_lane_15m",
        "kind": CATALOG_KIND,
        "owed": bool(reasons),
        "reasons": reasons,
        "unused": unused,
        "next": unused[0] if unused else None,
        "retired": retired_named_from_files(root=root),
        "comparison": COMPARISON_ID,
        "lab_admits": False,
        "trading_armed": False,
        "ping_lab": False,
        "framing": (
            "Doorbell from files (unused named P-* in POLICY_FAMILY.json file order). "
            "Not pnl. This sidecar does not date a factory row. Lab still gates seating "
            "and may refuse. Do not ping Lab."
        ),
        "updated_at": now().isoformat(),
    }
    for key in MONEY_KEYS:
        if key in payload:
            raise PolicyFamilyError(f"picker stamp refused money key {key}")
        payload.pop(key, None)
    path = picker_path(root=root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload
