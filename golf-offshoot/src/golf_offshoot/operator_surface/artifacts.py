"""Read-only honesty/export adapter. Missing is loud. Demo never fills operating SoT."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from golf_offshoot.audit.shadow_settle import (
    join_shadow_settles,
    normalize_settle_status,
    settle_banner_for_rows,
    settle_counts,
)
from golf_offshoot.operator_surface.modes import is_mock_or_demo_text
from golf_offshoot.operator_surface.paths import ResolvedRoots, resolve_roots, safe_existing_file
from golf_offshoot.operating import format_inventory
from golf_offshoot.ranking.leftover import leftover_from_audit

SHADOW_MISSING = "SHADOW_MISSING"
SHADOW_EMPTY = "SHADOW_EMPTY"
SETTLE_PENDING = "SETTLE_PENDING"
CALIB_MISSING = "CALIB_MISSING"
LIVE_TABLE_MISSING = "LIVE_TABLE_MISSING"
LEFTOVER_MISSING = "LEFTOVER_MISSING"
INVENTORY_MISSING = "INVENTORY_MISSING"

REQUIRED_SHADOW_FIELDS = (
    "timestamp",
    "tournament",
    "tournament_id",
    "player",
    "player_id",
    "market",
    "model_probability",
    "model_p_low",
    "model_p_high",
    "posted_decimal",
    "odds_as_of",
    "run_mode",
    "mode",
    "action_kind",
    "suggested_stake",
    "never_auto_bet",
    "paper_observation_only",
    "run_id",
    "recommendation_id",
)
SETTLE_STATUS_VALUES = frozenset({"paper_win", "paper_lose", "never_settled"})
_CALIB_NAME = re.compile(r"^weights_calib-v(\d+)\.json$")


@dataclass
class ShadowHonesty:
    status: str
    path: Path | None
    source: str
    rows: list[dict[str, Any]] = field(default_factory=list)
    missing_fields: list[str] = field(default_factory=list)
    settle_banner: str | None = None
    settle_counts: dict[str, int] = field(default_factory=dict)
    text: str = ""
    barred_mock: bool = False


@dataclass
class CalibrationHonesty:
    status: str
    path: Path | None = None
    version_id: str | None = None
    created_at: str | None = None
    recommendation: str | None = None
    no_future_leakage: bool | None = None
    weight_hash_expert: str | None = None
    weight_hash_calibrated: str | None = None
    metrics: dict[str, Any] = field(default_factory=dict)
    text: str = ""
    barred_mock: bool = False


@dataclass
class RankedExport:
    status: str
    path: Path | None = None
    html_path: Path | None = None
    pdf_path: Path | None = None
    text: str = ""
    banner: str = ""
    barred_mock: bool = False


@dataclass
class LeftoverView:
    status: str
    text: str = ""
    unconstrained: str = ""
    held_tickets: str = ""
    do_not_stuff_theta: str = ""
    barred_mock: bool = False


@dataclass
class InventoryView:
    status: str
    text: str = ""
    items: list[dict[str, Any]] = field(default_factory=list)
    barred_mock: bool = False


@dataclass
class HonestyBundle:
    roots: ResolvedRoots
    shadow: ShadowHonesty
    calibration: CalibrationHonesty
    ranked: RankedExport
    leftover: LeftoverView
    inventory: InventoryView


def load_honesty(
    *,
    artifact_root: Path | None = None,
    viz_root: Path | None = None,
    shadow_path: Path | None = None,
    environ: dict[str, str] | None = None,
    event_id: str | None = None,
    inspect_events=None,
) -> HonestyBundle:
    roots = resolve_roots(
        artifact_root=artifact_root,
        viz_root=viz_root,
        shadow_path=shadow_path,
        environ=environ,
    )
    return HonestyBundle(
        roots=roots,
        shadow=load_shadow_honesty(
            roots.shadow_path,
            source=roots.shadow_source,
            artifact_root=roots.artifact_root,
            inspect_events=inspect_events,
        ),
        calibration=load_calibration_honesty(roots.artifact_root),
        ranked=load_ranked_live_export(roots.artifact_root, event_id=event_id),
        leftover=load_leftover_view(roots.artifact_root, event_id=event_id),
        inventory=load_inventory_view(roots.artifact_root, event_id=event_id),
    )


def load_shadow_honesty(
    path: Path,
    *,
    source: str = "artifact_root",
    artifact_root: Path | None = None,
    inspect_events=None,
) -> ShadowHonesty:
    if not path.is_file():
        return ShadowHonesty(
            status=SHADOW_MISSING,
            path=path,
            source=source,
            text=(
                f"{SHADOW_MISSING}: no shadow journal at {path}. "
                "This is not zero-edge and not 'no advises'."
            ),
        )
    raw_text = path.read_text(encoding="utf-8")
    if is_mock_or_demo_text(raw_text):
        return ShadowHonesty(
            status="SHADOW_BARRED_MOCK",
            path=path,
            source=source,
            barred_mock=True,
            text="MOCK/DEMO shadow is barred from operating honesty SoT.",
        )
    rows: list[dict[str, Any]] = []
    missing: list[str] = []
    for line_no, line in enumerate(raw_text.splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        try:
            payload = json.loads(line)
        except ValueError:
            missing.append(f"line {line_no}: invalid json")
            continue
        if not isinstance(payload, dict):
            missing.append(f"line {line_no}: not an object")
            continue
        absent = [key for key in REQUIRED_SHADOW_FIELDS if key not in payload]
        if absent:
            missing.append(f"line {line_no}: missing {', '.join(absent)}")
        rows.append(payload)
    if not rows:
        return ShadowHonesty(
            status=SHADOW_EMPTY,
            path=path,
            source=source,
            missing_fields=missing,
            text=f"{SHADOW_EMPTY}: journal exists at {path} but has no advise rows.",
        )
    rows = join_shadow_settles(
        rows,
        artifact_root=artifact_root,
        inspect_events=inspect_events,
    )
    settle = settle_banner_for_rows(rows)
    counts = settle_counts(rows)
    return ShadowHonesty(
        status="SHADOW_OK",
        path=path,
        source=source,
        rows=rows,
        missing_fields=missing,
        settle_banner=settle,
        settle_counts=counts,
        text=_format_shadow_rows(rows, settle=settle, missing=missing, counts=counts),
    )


def _settle_status(row: dict[str, Any]) -> str | None:
    return normalize_settle_status(row.get("settle_status"))


def _format_shadow_rows(
    rows: list[dict[str, Any]],
    *,
    settle: str | None,
    missing: list[str],
    counts: dict[str, int] | None = None,
) -> str:
    lines = [
        "SHADOW JOURNAL (paper observation only — never auto-bet)",
        f"n={len(rows)}",
    ]
    counts = counts or settle_counts(rows)
    lines.append(
        "settle join: relevant="
        f"{counts.get('relevant', 0)} paper_win={counts.get('paper_win', 0)} "
        f"paper_lose={counts.get('paper_lose', 0)} never_settled={counts.get('never_settled', 0)} "
        f"absent_from_official_field={counts.get('absent_from_official_field', 0)} "
        f"missing={counts.get('missing', 0)}"
    )
    if settle:
        lines.append(
            f"{settle}: SETTLE_PENDING clears only when every relevant advise "
            "(win / top_5 / top_10 / top_20 / make_cut) is paper_win or paper_lose. "
            "never_settled and missing settle_status keep the weekly operating claim blocked, "
            "except never_settled source=espn_official_final:absent_from_official_field "
            "(player_id absent from the official STATUS_FINAL finisher list), which is "
            "excluded from the banner denominator and stays visible here. "
            "Honesty strip is not settled cash PnL."
        )
    else:
        lines.append(
            "settle banner off: every relevant advise is paper_win or paper_lose "
            "from official ESPN / paper-ledger / settled lived paper-book evidence. "
            "never_settled espn_official_final:absent_from_official_field rows are "
            "excluded from that denominator and remain visible on this strip."
        )
    for row in rows[-40:]:
        posted = row.get("posted_decimal")
        posted_s = f"{float(posted):.2f}" if isinstance(posted, (int, float)) else "n/a"
        p = row.get("model_probability")
        p_s = f"{float(p):.3f}" if isinstance(p, (int, float)) else "n/a"
        lo = row.get("model_p_low")
        hi = row.get("model_p_high")
        rng = ""
        if isinstance(lo, (int, float)) and isinstance(hi, (int, float)):
            rng = f" [{float(lo):.3f},{float(hi):.3f}]"
        settle_s = _settle_status(row) or "SETTLE_PENDING"
        source = row.get("settle_source") or ""
        source_s = f" source={source}" if source else ""
        settled_at = row.get("settled_at") or ""
        settled_s = f" settled_at={settled_at}" if settled_at else ""
        lines.append(
            f"{row.get('timestamp')} {row.get('mode')} {row.get('action_kind')} "
            f"{row.get('player')} {row.get('market')} posted={posted_s} model_p={p_s}{rng} "
            f"stake={row.get('suggested_stake')} odds_as_of={row.get('odds_as_of')} "
            f"settle_status={settle_s}{settled_s}{source_s}"
        )
        lines.append(
            f"    {row.get('tournament')} id={row.get('tournament_id')} "
            f"run={row.get('run_id')} rec={row.get('recommendation_id')} "
            f"never_auto_bet={row.get('never_auto_bet')} "
            f"paper_observation_only={row.get('paper_observation_only')}"
        )
    if missing:
        lines.append("field validation:")
        lines.extend(f"  {item}" for item in missing[:12])
    return "\n".join(lines)


def load_calibration_honesty(artifact_root: Path) -> CalibrationHonesty:
    calib_dir = artifact_root / "calibration"
    if not calib_dir.is_dir():
        return CalibrationHonesty(
            status=CALIB_MISSING,
            text=f"{CALIB_MISSING}: no calibration directory at {calib_dir}. Weights are not invented.",
        )
    candidates = [p for p in calib_dir.glob("weights_calib-v*.json") if p.is_file()]
    if not candidates:
        return CalibrationHonesty(
            status=CALIB_MISSING,
            text=f"{CALIB_MISSING}: no weights_calib-v*.json under {calib_dir}. Weights are not invented.",
        )
    ranked = sorted(candidates, key=_calib_sort_key, reverse=True)
    path = ranked[0]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return CalibrationHonesty(
            status=CALIB_MISSING,
            path=path,
            text=f"{CALIB_MISSING}: {path.name} is unreadable. Weights are not invented.",
        )
    if not isinstance(payload, dict) or is_mock_or_demo_text(json.dumps(payload)):
        return CalibrationHonesty(
            status="CALIB_BARRED_MOCK",
            path=path,
            barred_mock=True,
            text="MOCK/DEMO calibration is barred from operating honesty SoT.",
        )
    rec = str(payload.get("recommendation") or "")
    metrics = payload.get("metrics") if isinstance(payload.get("metrics"), dict) else {}
    text = "\n".join(
        [
            f"calibration {payload.get('version_id') or path.name}",
            f"recommendation={rec or 'n/a'}",
            f"no_future_leakage={payload.get('no_future_leakage')}",
            f"weight_hash_expert={payload.get('weight_hash_expert')}",
            f"weight_hash_calibrated={payload.get('weight_hash_calibrated')}",
            f"created_at={payload.get('created_at')}",
            "metrics=" + json.dumps(metrics, sort_keys=True) if metrics else "metrics=n/a",
            "keep_expert means fitted weights are stored, not selected. Edge is not established.",
        ]
    )
    return CalibrationHonesty(
        status="CALIB_OK",
        path=path,
        version_id=payload.get("version_id"),
        created_at=str(payload.get("created_at") or ""),
        recommendation=rec or None,
        no_future_leakage=bool(payload.get("no_future_leakage")) if "no_future_leakage" in payload else None,
        weight_hash_expert=payload.get("weight_hash_expert"),
        weight_hash_calibrated=payload.get("weight_hash_calibrated"),
        metrics=metrics,
        text=text,
    )


def _calib_sort_key(path: Path) -> tuple[int, str, str]:
    match = _CALIB_NAME.match(path.name)
    version_n = int(match.group(1)) if match else -1
    created = ""
    version_id = path.name
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            created = str(payload.get("created_at") or "")
            version_id = str(payload.get("version_id") or path.name)
    except (OSError, ValueError):
        pass
    return version_n, created, version_id


def load_ranked_live_export(artifact_root: Path, *, event_id: str | None = None) -> RankedExport:
    txt = _latest_live_file(artifact_root, suffix=".txt", event_id=event_id)
    if txt is None:
        return RankedExport(
            status=LIVE_TABLE_MISSING,
            banner="PHASE 1 OBSERVATION · observation only · never auto-bet",
            text=(
                f"{LIVE_TABLE_MISSING}: no real LIVE ranked table "
                f"(latest/*_live_*.txt or exports/*_live_*.txt) under {artifact_root}. "
                "Not a demo field."
            ),
        )
    body = txt.read_text(encoding="utf-8")
    if is_mock_or_demo_text(body):
        return RankedExport(
            status="LIVE_TABLE_BARRED_MOCK",
            path=txt,
            barred_mock=True,
            banner="OFFLINE DEMO — MOCK DATA",
            text="MOCK/DEMO ranked output is barred from operating honesty SoT.",
        )
    html = txt.with_suffix(".html") if txt.with_suffix(".html").is_file() else None
    pdf = txt.with_suffix(".pdf") if txt.with_suffix(".pdf").is_file() else None
    banner = "PHASE 1 OBSERVATION · observation only · never auto-bet · NOT ARMED"
    return RankedExport(
        status="LIVE_TABLE_OK",
        path=txt,
        html_path=html,
        pdf_path=pdf,
        text=body,
        banner=banner,
    )


def _latest_live_file(artifact_root: Path, *, suffix: str, event_id: str | None) -> Path | None:
    needles = []
    for folder in (artifact_root / "latest", artifact_root / "exports", artifact_root):
        if not folder.is_dir():
            continue
        needles.extend(folder.glob(f"*_live_*{suffix}"))
        needles.extend(folder.glob(f"*live*{suffix}"))
    files = []
    for path in needles:
        if not path.is_file():
            continue
        if path.suffix != suffix:
            continue
        if "pack" in path.parts:
            continue
        name = path.name.lower()
        if "leftover" in name or "leaderboard" in name or "preview" in name:
            continue
        if event_id and event_id not in path.name:
            continue
        files.append(path)
    if not files:
        return None
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return files[0]


def load_leftover_view(artifact_root: Path, *, event_id: str | None = None) -> LeftoverView:
    leftover_file = _latest_named_file(artifact_root, ("leftover",), suffixes=(".txt",))
    if leftover_file is not None:
        text = leftover_file.read_text(encoding="utf-8")
        if is_mock_or_demo_text(text):
            return LeftoverView(
                status="LEFTOVER_BARRED_MOCK",
                barred_mock=True,
                text="MOCK/DEMO leftover is barred from operating honesty SoT.",
            )
        return _leftover_from_text(text)
    audit = _latest_audit(artifact_root, event_id=event_id)
    if audit is None:
        return LeftoverView(
            status=LEFTOVER_MISSING,
            text=(
                f"{LEFTOVER_MISSING}: no leftover file and no operating snapshot under "
                f"{artifact_root}. Leftover is not invented."
            ),
        )
    name = str(getattr(audit, "tournament_id", "") or "")
    extra = getattr(audit, "extra", {}) or {}
    event_name = str(extra.get("event_name") or name)
    text = leftover_from_audit(audit, event_name)
    return _leftover_from_text(text)


def _leftover_from_text(text: str) -> LeftoverView:
    return LeftoverView(
        status="LEFTOVER_OK",
        text=text,
        unconstrained=_section(text, "still unconstrained"),
        held_tickets=_section(text, "on held tickets"),
        do_not_stuff_theta=_section(text, "do not stuff into theta"),
    )


def load_inventory_view(artifact_root: Path, *, event_id: str | None = None) -> InventoryView:
    audit = _latest_audit(artifact_root, event_id=event_id)
    if audit is None:
        return InventoryView(
            status=INVENTORY_MISSING,
            text=f"{INVENTORY_MISSING}: no operating snapshot inventory under {artifact_root}.",
        )
    raw = (audit.extra or {}).get("source_inventory") or []
    if not raw:
        return InventoryView(
            status=INVENTORY_MISSING,
            text=f"{INVENTORY_MISSING}: snapshot {audit.run_id} has no source_inventory.",
        )
    from golf_offshoot.models.schemas import SourceInventoryItem

    items = []
    parsed = []
    for row in raw:
        if isinstance(row, dict):
            items.append(row)
            parsed.append(SourceInventoryItem.model_validate(row))
            if str(row.get("source_kind") or "").lower() == "mock":
                return InventoryView(
                    status="INVENTORY_BARRED_MOCK",
                    barred_mock=True,
                    text="MOCK inventory is barred from operating honesty SoT.",
                )
    return InventoryView(
        status="INVENTORY_OK",
        text=format_inventory(parsed),
        items=items,
    )


def _latest_audit(artifact_root: Path, *, event_id: str | None = None):
    from pydantic import ValidationError

    from golf_offshoot.audit.journal import load_audit

    snap = artifact_root / "snapshots"
    if not snap.is_dir():
        return None
    best = None
    for path in snap.glob("*.json"):
        try:
            rec = load_audit(path)
        except (OSError, ValueError, KeyError, TypeError, ValidationError):
            continue
        if event_id and str(rec.tournament_id) != str(event_id):
            continue
        if best is None or rec.as_of > best.as_of:
            best = rec
    return best


def _latest_named_file(
    artifact_root: Path,
    needles: tuple[str, ...],
    *,
    suffixes: tuple[str, ...],
) -> Path | None:
    found: list[Path] = []
    for folder in (artifact_root / "latest", artifact_root / "exports", artifact_root):
        if not folder.is_dir():
            continue
        for path in folder.iterdir():
            if not path.is_file() or path.suffix not in suffixes:
                continue
            name = path.name.lower()
            if any(n in name for n in needles):
                found.append(path)
    if not found:
        return None
    found.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return found[0]


def _section(text: str, header: str) -> str:
    marker = f"== {header} =="
    start = text.find(marker)
    if start < 0:
        return ""
    rest = text[start + len(marker) :]
    nxt = rest.find("\n== ")
    return rest if nxt < 0 else rest[:nxt]


def export_file_for_serve(path: Path, roots: ResolvedRoots) -> Path | None:
    """Allow serving only real export/html/pdf/txt that stay inside the artifact root."""
    return safe_existing_file(path, roots.artifact_root)
