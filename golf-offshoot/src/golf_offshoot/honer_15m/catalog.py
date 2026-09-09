"""Dated two-item catalog. File order is the picker. Never sorted from tape."""

from __future__ import annotations

import json
from typing import Any

from golf_offshoot.honer_15m.paths import catalog_path
from golf_offshoot.honer_15m.policy import FAMILY_RICH, FAMILY_SPREAD

CATALOG_IDS = (FAMILY_RICH, FAMILY_SPREAD)
BURNED_IDS = frozenset(
    {
        "FLIP",
        "PERSIST",
        "SEAS-DIR",
        "SHRINK",
        "LOGIT",
        "RETUNE-COINFLIP-BAND",
        "FEE-AS-SIGNAL",
        "SUM-LINEAGES",
        "BACKFILL-GAP",
        "BASELINE-AS-EDGE",
    }
)
ALLOWED_ACTIVATE = frozenset({"", "start", "clip_exhaustion", "quote_quality_ok", "clip_exhaustion+quote_quality_ok"})


class CatalogError(ValueError):
    """Dated catalog item is malformed or burned."""


def _validate_item(item: dict[str, Any], *, index: int) -> None:
    ident = str(item.get("id") or "")
    if not ident:
        raise CatalogError(f"catalog item {index} missing id")
    if ident in BURNED_IDS or ident.upper() in BURNED_IDS:
        raise CatalogError(f"burned catalog id refused: {ident}")
    if not str(item.get("declared_at") or ""):
        raise CatalogError(f"catalog item {ident} missing declared_at")
    activate = str(item.get("activate") or ("start" if index == 0 else ""))
    if activate not in ALLOWED_ACTIVATE:
        raise CatalogError(f"catalog item {ident} activate {activate!r} is not file-derived")


def load_catalog() -> dict[str, Any]:
    path = catalog_path()
    if not path.is_file():
        return {
            "schema": 1,
            "items": [
                {"id": FAMILY_RICH, "family": FAMILY_RICH, "activate": "start"},
                {
                    "id": FAMILY_SPREAD,
                    "family": FAMILY_SPREAD,
                    "activate": "clip_exhaustion+quote_quality_ok",
                },
            ],
        }
    payload = json.loads(path.read_text(encoding="utf-8"))
    items = list(payload.get("items") or [])
    for i, item in enumerate(items):
        if isinstance(item, dict):
            _validate_item(item, index=i)
    return payload


def catalog_ids() -> list[str]:
    payload = load_catalog()
    ids = []
    for item in payload.get("items") or []:
        if isinstance(item, dict) and item.get("id"):
            ids.append(str(item["id"]))
    return ids or list(CATALOG_IDS)


def next_family(active: str) -> str | None:
    ids = catalog_ids()
    try:
        idx = ids.index(str(active))
    except ValueError:
        return ids[0] if ids else None
    if idx + 1 >= len(ids):
        return None
    return ids[idx + 1]
