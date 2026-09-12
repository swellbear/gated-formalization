"""Dated catalog. File order is the picker. Never sorted from tape."""

from __future__ import annotations

import json
from typing import Any

from golf_offshoot.honer_15m.paths import catalog_path
from golf_offshoot.honer_15m.policy import FAMILY_RICH, FAMILY_SPREAD, FAMILY_THIN

CATALOG_IDS = (FAMILY_RICH, FAMILY_SPREAD, FAMILY_THIN)
#: Doorbell ``HONER-FAMILY-AMEND`` is taken once items exceed the original two.
ORIGINAL_DATED_FAMILIES = 2
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
ALLOWED_ACTIVATE = frozenset(
    {
        "",
        "start",
        "clip_exhaustion",
        "quote_quality_ok",
        "clip_exhaustion+quote_quality_ok",
        "search_starvation",
        "search_starvation+quote_quality_ok",
    }
)
FAMILY2_ACTIVATE = "clip_exhaustion+quote_quality_ok|search_starvation+quote_quality_ok"
FAMILY3_ACTIVATE = "clip_exhaustion+quote_quality_ok|search_starvation+quote_quality_ok"


class CatalogError(ValueError):
    """Dated catalog item is malformed or burned."""


def activate_allowed(activate: str) -> bool:
    token = str(activate or "")
    if token in ALLOWED_ACTIVATE:
        return True
    if "|" not in token:
        return False
    parts = [p.strip() for p in token.split("|")]
    return bool(parts) and all(p in ALLOWED_ACTIVATE and p not in {"", "start"} for p in parts)


def activate_needs_quotes(activate: str) -> bool:
    return "quote_quality_ok" in str(activate or "")


def _validate_item(item: dict[str, Any], *, index: int) -> None:
    ident = str(item.get("id") or "")
    if not ident:
        raise CatalogError(f"catalog item {index} missing id")
    if ident in BURNED_IDS or ident.upper() in BURNED_IDS:
        raise CatalogError(f"burned catalog id refused: {ident}")
    if not str(item.get("declared_at") or ""):
        raise CatalogError(f"catalog item {ident} missing declared_at")
    activate = str(item.get("activate") or ("start" if index == 0 else ""))
    if not activate_allowed(activate):
        raise CatalogError(f"catalog item {ident} activate {activate!r} is not file-derived")


def _default_catalog() -> dict[str, Any]:
    return {
        "schema": 1,
        "items": [
            {"id": FAMILY_RICH, "family": FAMILY_RICH, "activate": "start"},
            {
                "id": FAMILY_SPREAD,
                "family": FAMILY_SPREAD,
                "activate": FAMILY2_ACTIVATE,
            },
            {
                "id": FAMILY_THIN,
                "family": FAMILY_THIN,
                "activate": FAMILY3_ACTIVATE,
            },
        ],
    }


def load_catalog() -> dict[str, Any]:
    path = catalog_path()
    if not path.is_file():
        return _default_catalog()
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


def catalog_item(ident: str) -> dict[str, Any] | None:
    payload = load_catalog()
    for item in payload.get("items") or []:
        if isinstance(item, dict) and str(item.get("id") or "") == str(ident):
            return item
    return None


def item_activate(ident: str) -> str:
    item = catalog_item(ident)
    if not item:
        return ""
    return str(item.get("activate") or "")


def third_family_dated() -> bool:
    """True once a third catalog item exists. Answers HONER-FAMILY-AMEND."""
    return len(catalog_ids()) > ORIGINAL_DATED_FAMILIES


def next_family(active: str) -> str | None:
    ids = catalog_ids()
    try:
        idx = ids.index(str(active))
    except ValueError:
        return ids[0] if ids else None
    if idx + 1 >= len(ids):
        return None
    return ids[idx + 1]
