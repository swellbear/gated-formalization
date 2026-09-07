"""Read-only Illustrator viz-wall hook. Never generate or fabricate charts."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from golf_offshoot.operator_surface.modes import is_mock_or_demo_text
from golf_offshoot.operator_surface.paths import PathUnsafeError, ResolvedRoots, safe_under

SLOT_SHADOW = "shadow_honesty_strip"
SLOT_CALIBRATION = "calibration_weather"
NOT_YET_AVAILABLE = "not yet available"

VIZ_BADGES = (
    "PHASE 1 OBSERVATION",
    "AI: NO CASH IN/OUT",
    "PAPER OBSERVATION ONLY",
)

SLOT_SPECS = {
    SLOT_SHADOW: {
        "title": "Shadow honesty strip",
        "filename": "shadow_honesty_strip.png",
        "subline": "Live-book paper journal — not settled PnL · not Kalshi demo",
    },
    SLOT_CALIBRATION: {
        "title": "Calibration weather",
        "filename": "calibration_weather.png",
        "subline": "All freezes keep_expert (v1→v3) — not edge established",
    },
}

ALLOWED_IMAGE_SUFFIXES = {".png"}
MANIFEST_NAME = "viz_wall_manifest.json"


@dataclass(frozen=True)
class VizSlot:
    slot_id: str
    title: str
    subline: str
    badges: tuple[str, ...]
    status: str
    path: Path | None
    mtime: float | None
    note: str


@dataclass(frozen=True)
class VizWall:
    root: Path
    source: str
    manifest_path: Path | None
    manifest_error: str | None
    slots: tuple[VizSlot, ...]
    refreshed_from_mtime: float | None

    def slot(self, slot_id: str) -> VizSlot | None:
        for item in self.slots:
            if item.slot_id == slot_id:
                return item
        return None


def load_viz_wall(roots: ResolvedRoots) -> VizWall:
    root = roots.viz_root
    manifest_path = root / MANIFEST_NAME
    declared: dict[str, Any] = {}
    manifest_error = None
    used_manifest = None
    if manifest_path.is_file():
        try:
            declared, used_manifest = _read_manifest(manifest_path, root)
        except (ValueError, PathUnsafeError, OSError) as exc:
            manifest_error = str(exc)
            declared = {}
            used_manifest = None
    slots = []
    mtimes: list[float] = []
    for slot_id, spec in SLOT_SPECS.items():
        override = declared.get(slot_id) if isinstance(declared.get(slot_id), dict) else {}
        filename = str(override.get("path") or override.get("file") or spec["filename"])
        slot = _render_slot(root, slot_id, spec, filename)
        slots.append(slot)
        if slot.mtime is not None:
            mtimes.append(slot.mtime)
    if used_manifest is not None and used_manifest.is_file():
        mtimes.append(used_manifest.stat().st_mtime)
    return VizWall(
        root=root,
        source=roots.viz_source,
        manifest_path=used_manifest,
        manifest_error=manifest_error,
        slots=tuple(slots),
        refreshed_from_mtime=max(mtimes) if mtimes else None,
    )


def _read_manifest(path: Path, root: Path) -> tuple[dict[str, Any], Path]:
    raw = path.read_text(encoding="utf-8")
    if is_mock_or_demo_text(raw):
        raise ValueError("viz manifest is MOCK/DEMO and is barred from the honesty wall")
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise ValueError("viz manifest must be a JSON object")
    slots = payload.get("slots") or payload.get("panels") or payload
    if not isinstance(slots, dict):
        raise ValueError("viz manifest slots must be an object")
    cleaned: dict[str, Any] = {}
    for key, value in slots.items():
        if key not in SLOT_SPECS:
            continue
        if not isinstance(value, dict):
            raise ValueError(f"viz slot {key} must be an object")
        rel = str(value.get("path") or value.get("file") or SLOT_SPECS[key]["filename"])
        if Path(rel).suffix.lower() not in ALLOWED_IMAGE_SUFFIXES:
            raise ValueError(f"viz slot {key} must be a PNG")
        safe_under(Path(rel), root)
        cleaned[key] = {"path": rel}
    return cleaned, path


def _render_slot(root: Path, slot_id: str, spec: dict[str, str], filename: str) -> VizSlot:
    title = spec["title"]
    subline = spec["subline"]
    try:
        candidate = safe_under(Path(filename), root)
    except PathUnsafeError:
        return VizSlot(
            slot_id=slot_id,
            title=title,
            subline=subline,
            badges=VIZ_BADGES,
            status=NOT_YET_AVAILABLE,
            path=None,
            mtime=None,
            note="path rejected (traversal or unsafe). Chart not invented.",
        )
    if not candidate.is_file():
        return VizSlot(
            slot_id=slot_id,
            title=title,
            subline=subline,
            badges=VIZ_BADGES,
            status=NOT_YET_AVAILABLE,
            path=None,
            mtime=None,
            note=f"{NOT_YET_AVAILABLE} — Illustrator owns regeneration. No chart generated.",
        )
    if candidate.suffix.lower() not in ALLOWED_IMAGE_SUFFIXES:
        return VizSlot(
            slot_id=slot_id,
            title=title,
            subline=subline,
            badges=VIZ_BADGES,
            status=NOT_YET_AVAILABLE,
            path=None,
            mtime=None,
            note="non-PNG viz file ignored. Chart not invented.",
        )
    return VizSlot(
        slot_id=slot_id,
        title=title,
        subline=subline,
        badges=VIZ_BADGES,
        status="available",
        path=candidate,
        mtime=candidate.stat().st_mtime,
        note=f"read-only PNG · mtime={candidate.stat().st_mtime}",
    )


def viz_file_for_serve(slot_id: str, wall: VizWall) -> Path | None:
    slot = wall.slot(slot_id)
    if slot is None or slot.path is None:
        return None
    try:
        return safe_under(slot.path, wall.root)
    except PathUnsafeError:
        return None
