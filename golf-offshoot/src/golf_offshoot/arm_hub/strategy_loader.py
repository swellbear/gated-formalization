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
DEAD_LABELS = frozenset({"DEAD", "LIKELY_DEAD", "STRUCTURAL_DEAD"})
KEEP_ALIASES = {"KEEP": "KEEP", "KEEP_WATCH": "KEEP"}


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


def _normalize_shelf_label(raw: str) -> str:
    token = str(raw or "").strip().upper().replace(" ", "_")
    if token in KEEP_ALIASES:
        return KEEP_ALIASES[token]
    return token


def _shortlist_items(shortlist: dict[str, Any]) -> list[Any]:
    for key in ("rows", "items", "keepers", "active"):
        rows = shortlist.get(key)
        if isinstance(rows, list):
            return rows
    return []


def join_shortlist_shelf(
    shortlist: dict[str, Any],
    shelf: dict[str, Any],
    *,
    prefer_keep_only: bool = True,
    require_dsl: bool = True,
    drop_invent: bool = True,
) -> list[dict[str, Any]]:
    """``shortlist_v1`` items ⨝ ``SHORTLIST_SHELF.per_id[id]``.

    Pull filter: KEEP only (``KEEP_WATCH`` maps to KEEP); drop DEAD /
    LIKELY_DEAD / STRUCTURAL_DEAD; require ``dsl``; invent packs out.
    """
    per_id = shelf.get("per_id")
    if not isinstance(per_id, dict):
        per_id = {}
    rows = _shortlist_items(shortlist)
    joined: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        kid = str(row.get("id") or "").strip()
        if not kid:
            continue
        shelf_row = per_id.get(kid) if isinstance(per_id.get(kid), dict) else {}
        label = _normalize_shelf_label(
            str(shelf_row.get("shelf_label") or row.get("shelf_label") or "")
        )
        living = bool(shelf_row.get("living", True))
        if label in DEAD_LABELS or living is False:
            continue
        if prefer_keep_only and label != "KEEP":
            continue
        dsl = str(row.get("dsl") or shelf_row.get("dsl") or "").strip()
        if require_dsl and not dsl:
            continue
        rec = row.get("recommended") if isinstance(row.get("recommended"), dict) else {}
        if isinstance(shelf_row.get("recommended"), dict):
            rec = {**rec, **shelf_row["recommended"]}
        packed = {
            "id": kid,
            "claim": row.get("claim") or shelf_row.get("claim") or "",
            "dsl": dsl,
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
        if drop_invent and _is_invent_pack(packed):
            continue
        joined.append(packed)
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


def keepers_jsonl_path(root: Path | None = None) -> Path:
    return strategies_dir(root) / "strategy_bridge_keepers.jsonl"


def write_keepers_jsonl(keepers: list[dict[str, Any]], root: Path | None = None) -> Path:
    dest = keepers_jsonl_path(root)
    assert_not_learning_lane_path(dest)
    lines = [json.dumps(row, ensure_ascii=False) for row in keepers]
    dest.write_text(("\n".join(lines) + ("\n" if lines else "")), encoding="utf-8")
    return dest


def rule_from_keeper(row: dict[str, Any]) -> dict[str, Any]:
    rec = row.get("recommended") if isinstance(row.get("recommended"), dict) else {}
    guard = rec.get("guardrails") if isinstance(rec.get("guardrails"), dict) else {}
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
        "url": rec.get("url") or row.get("url") or "",
        "digestor_label": rec.get("digestor_label") or row.get("digestor_label") or "",
        "fill_to_30": rec.get("fill_to_30"),
        "stamp_binding": rec.get("stamp_binding") or row.get("stamp_binding") or "",
        "lab_admits": False,
        "trading_armed": False,
        "hub_untouched": True,
        "size_hint": rec.get("size_hint") or row.get("size_hint") or "",
        "guardrails": {
            "require_plus96_keep": bool(guard.get("require_plus96_keep", True)),
            "require_path_rank_keeper": bool(guard.get("require_path_rank_keeper", True)),
            "require_size": bool(guard.get("require_size", True)),
            "forbid_invent_pack": bool(guard.get("forbid_invent_pack", True)),
        },
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
    write_keepers_jsonl(keepers, root)
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
