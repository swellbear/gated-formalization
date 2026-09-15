"""Pin + join leftover-hunt keepers → versioned POLICY.json.

Expected operator source (document only; not on this tree):
``C:\\Users\\bearh\\leftover_hunt_exam\\shortlist_grow_freeze\\``

Join: ``shortlist_v1`` ⨝ ``SHORTLIST_SHELF.per_id``
(see ``data/arm_hub/strategies/STRATEGY_BRIDGE_EXPORT_SHAPE.md``).

This module is an *offline* file tool. The watch loop never calls it.
It never asks a bot. Invent packs are refused for live intake.
"""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from golf_offshoot.arm_hub.paths import (
    SERIES_DEFAULT,
    assert_not_learning_lane_path,
    policy_path,
    shelf_pin_path,
    shortlist_pin_path,
    strategies_dir,
)

POLICY_VERSION_PREFIX = "arm-hub-policy"
INVENT_MARKERS = ("invent", "lab_invent", "proposed_invent")


class InventPackRefused(RuntimeError):
    """Invent packs are a Hard NO for live intake."""


def _read_json(path: Path) -> dict[str, Any]:
    assert_not_learning_lane_path(path)
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"expected object: {path}")
    return raw


def pin_from_operator_dir(src: Path, *, root: Path | None = None) -> dict[str, Path]:
    """Copy shortlist + shelf into ``data/arm_hub/strategies/``. Offline only."""
    src = assert_not_learning_lane_path(src)
    dest = strategies_dir(root)
    copied: dict[str, Path] = {}
    for name, dest_path in (
        ("shortlist_v1.json", shortlist_pin_path(root)),
        ("SHORTLIST_SHELF.json", shelf_pin_path(root)),
    ):
        candidate = src / name
        if not candidate.is_file():
            raise FileNotFoundError(f"missing {name} under {src}")
        shutil.copy2(candidate, dest_path)
        copied[name] = dest_path
    lean = src / "out"
    if lean.is_dir():
        dest_lean = dest / "out"
        if dest_lean.exists():
            shutil.rmtree(dest_lean)
        shutil.copytree(lean, dest_lean)
        copied["out"] = dest_lean
    return copied


def join_shortlist_shelf(
    shortlist: dict[str, Any],
    shelf: dict[str, Any],
    *,
    prefer_keep_only: bool = True,
) -> list[dict[str, Any]]:
    """``shortlist_v1`` rows ⨝ ``SHORTLIST_SHELF.per_id``."""
    per_id = shelf.get("per_id")
    if not isinstance(per_id, dict):
        per_id = {}
    rows = shortlist.get("rows") or shortlist.get("keepers") or shortlist.get("active") or []
    if not isinstance(rows, list):
        raise ValueError("shortlist_v1 rows must be a list")
    joined: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        kid = str(row.get("id") or "").strip()
        if not kid:
            continue
        shelf_row = per_id.get(kid) if isinstance(per_id.get(kid), dict) else {}
        label = str(shelf_row.get("shelf_label") or row.get("shelf_label") or "").upper()
        living = bool(shelf_row.get("living", True))
        if prefer_keep_only and label != "KEEP":
            continue
        if label == "DEAD" or living is False:
            continue
        rec = row.get("recommended") if isinstance(row.get("recommended"), dict) else {}
        if isinstance(shelf_row.get("recommended"), dict):
            rec = {**rec, **shelf_row["recommended"]}
        joined.append(
            {
                "id": kid,
                "claim": row.get("claim") or shelf_row.get("claim") or "",
                "dsl": row.get("dsl") or shelf_row.get("dsl") or "",
                "mode": row.get("mode") or shelf_row.get("mode") or "",
                "pack": row.get("pack") or shelf_row.get("pack") or "",
                "idea": row.get("idea") or shelf_row.get("idea") or "",
                "why_short": row.get("why_short") or shelf_row.get("why_short") or "",
                "shelf_label": label or "KEEP",
                "living": living,
                "path_rank": int(row.get("path_rank") or shelf_row.get("path_rank") or 99),
                "promote_bar": str(
                    shelf_row.get("promote_bar") or row.get("promote_bar") or "below"
                ),
                "recommended": rec,
                "verdict": "KEEP",
            }
        )
    joined.sort(key=lambda r: (int(r["path_rank"]), r["id"]))
    return joined


def _is_invent_pack(row: dict[str, Any]) -> bool:
    pack = str(row.get("pack") or "").lower()
    mode = str(row.get("mode") or "").lower()
    rec = row.get("recommended") if isinstance(row.get("recommended"), dict) else {}
    if rec.get("invent") is True:
        return True
    blob = f"{pack} {mode}"
    return any(m in blob for m in INVENT_MARKERS)


def rule_from_keeper(row: dict[str, Any]) -> dict[str, Any]:
    rec = row.get("recommended") if isinstance(row.get("recommended"), dict) else {}
    return {
        "id": row["id"],
        "verdict": "KEEP",
        "path_rank": row.get("path_rank", 99),
        "promote_bar": row.get("promote_bar", "below"),
        "shelf_label": row.get("shelf_label", "KEEP"),
        "claim": row.get("claim", ""),
        "dsl": row.get("dsl", ""),
        "mode": row.get("mode", ""),
        "pack": row.get("pack", ""),
        "idea": row.get("idea", ""),
        "why_short": row.get("why_short", ""),
        "invent_pack": _is_invent_pack(row),
        "when": {
            "secs_to_expiry_min": int(rec.get("secs_to_expiry_min", 60)),
            "secs_to_expiry_max": int(rec.get("secs_to_expiry_max", 600)),
            "yes_price_min": float(rec.get("yes_price_min", 0.05)),
            "yes_price_max": float(rec.get("yes_price_max", 0.95)),
        },
        "side": str(rec.get("side") or "yes").lower(),
        "size_pct_bankroll": float(rec.get("size_pct_bankroll", 0.02)),
        "weight": float(rec.get("weight", 1.0)),
        "enabled": not _is_invent_pack(row),
    }


def build_policy(
    keepers: list[dict[str, Any]],
    *,
    source_note: str,
    series: str = SERIES_DEFAULT,
) -> dict[str, Any]:
    rules = [rule_from_keeper(k) for k in keepers]
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return {
        "policy_version": f"{POLICY_VERSION_PREFIX}-{stamp}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "series": series,
        "source_note": source_note,
        "apply_requires_go": True,
        "unattended_loop_must_not_regenerate": True,
        "rules": rules,
    }


def load_pins(root: Path | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
    shortlist = _read_json(shortlist_pin_path(root))
    shelf = _read_json(shelf_pin_path(root))
    return shortlist, shelf


def load_or_build_policy(
    root: Path | None = None,
    *,
    prefer_keep_only: bool = True,
    rebuild: bool = False,
) -> dict[str, Any]:
    """Read pinned POLICY.json, or build it once from pinned shortlist+shelf.

    Rebuild is an explicit offline action (``--pin`` / tests). The watch loop
    passes rebuild=False and only reads the file.
    """
    dest = policy_path(root)
    if dest.is_file() and not rebuild:
        return _read_json(dest)
    shortlist, shelf = load_pins(root)
    keepers = join_shortlist_shelf(shortlist, shelf, prefer_keep_only=prefer_keep_only)
    policy = build_policy(
        keepers,
        source_note="pinned shortlist_v1 ⨝ SHORTLIST_SHELF.per_id (KEEP preferred)",
    )
    write_policy(policy, root)
    return policy


def write_policy(policy: dict[str, Any], root: Path | None = None) -> Path:
    dest = policy_path(root)
    assert_not_learning_lane_path(dest)
    dest.write_text(json.dumps(policy, indent=2) + "\n", encoding="utf-8")
    return dest


def live_allowlist(policy: dict[str, Any]) -> list[dict[str, Any]]:
    """Promote-bar pass + non-invent + KEEP only. Used when mode=live."""
    out: list[dict[str, Any]] = []
    for rule in policy.get("rules") or []:
        if not isinstance(rule, dict):
            continue
        if rule.get("invent_pack"):
            continue
        if str(rule.get("promote_bar") or "").lower() != "pass":
            continue
        if str(rule.get("shelf_label") or "").upper() != "KEEP":
            continue
        if rule.get("enabled") is False:
            continue
        out.append(rule)
    return out


def assert_not_invent_for_live(rule: dict[str, Any]) -> None:
    if rule.get("invent_pack") or _is_invent_pack(rule):
        raise InventPackRefused(
            f"invent pack refused for live intake: {rule.get('id')}"
        )
