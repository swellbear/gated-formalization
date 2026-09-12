"""Generated 15m learning card. Quotes and registry fields only.

Not a verdict. Operator notes remain the verdict SoT. This module may quote
them. It does not write the caveats file, the bar, or the registry.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from golf_offshoot.learning_lane_15m.paths import latest_dir_15m, paper_dir_15m
from golf_offshoot.operator_surface.observability import repo_root

CARD_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_LEARNING_CARD.md"
REGISTRY_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_RULES.json"
PARK_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_METHOD_PARK.md"
CAVEATS_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_SOURCE_DIGEST_CAVEATS.md"
DIGEST_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_SOURCE_DIGEST.md"

EMPTY_ON_TRIAL = "No selection rule on trial."
MISSING_HUB_COPY = "learning card not yet available"
NOT_YET_RULED = "not yet ruled."

_RULE_ID = re.compile(r"\bR-[A-Z0-9-]+\b")
_ASOF_LINE = re.compile(r"^\*\*As-of:\*\*|^journal generated_at=", re.IGNORECASE)
_WHY_HEAD = re.compile(
    r"^##\s+(Why we tried it|Why|1\.\s+The residual.*)$",
    re.IGNORECASE,
)
_FALSIFIER_HEAD = re.compile(r"^##\s+.*(falsifier|kill).*$", re.IGNORECASE)
_VERDICT = re.compile(r"\*\*Verdict:\*\*\s*\*\*(.+?)\*\*", re.IGNORECASE)
_NAMED_HORSE_NO = re.compile(r"not a new named horse", re.IGNORECASE)


def card_path(*, root: Path | None = None) -> Path:
    return (root or repo_root()) / CARD_REL


def _read(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def _sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _sha256_text(text: str) -> str:
    return _sha256_bytes(text.encode("utf-8"))


def _sha256_file(path: Path) -> str:
    if not path.is_file():
        return ""
    return _sha256_bytes(path.read_bytes())


def load_registry(*, root: Path | None = None) -> dict[str, Any]:
    path = (root or repo_root()) / REGISTRY_REL
    if not path.is_file():
        raise FileNotFoundError(f"registry missing: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("registry is not an object")
    return payload


def _rules(registry: dict[str, Any]) -> list[dict[str, Any]]:
    return [row for row in (registry.get("rules") or []) if isinstance(row, dict)]


def executing_rules(registry: dict[str, Any]) -> list[dict[str, Any]]:
    return [row for row in _rules(registry) if bool(row.get("execution"))]


def _is_selection(rule: dict[str, Any]) -> bool:
    return str(rule.get("kind") or "").strip().lower() == "selection" or bool(
        rule.get("selects")
    )


def _docs_dir(*, root: Path | None = None) -> Path:
    return (root or repo_root()) / "golf-offshoot" / "docs"


def _proposed_files(*, root: Path | None = None) -> list[Path]:
    docs = _docs_dir(root=root)
    if not docs.is_dir():
        return []
    return sorted(docs.glob("LEARNING_LANE_15M_LAB_PROPOSED_*.md"))


def _operator_notes(*, root: Path | None = None) -> list[Path]:
    docs = _docs_dir(root=root)
    if not docs.is_dir():
        return []
    return sorted(docs.glob("LEARNING_LANE_15M_OPERATOR_NOTE_*.md"))


def _scorecards(*, root: Path | None = None) -> list[Path]:
    found: list[Path] = []
    docs = _docs_dir(root=root)
    if docs.is_dir():
        found.extend(sorted(docs.glob("LEARNING_LANE_15M_*SCORE*.json")))
        found.extend(sorted(docs.glob("*scorecard*.json")))
    latest = latest_dir_15m()
    if latest.is_dir():
        found.extend(sorted(latest.glob("*scorecard*")))
    return [path for path in found if path.is_file()]


def _section_after(text: str, heading: re.Pattern[str]) -> str:
    lines = (text or "").splitlines()
    capturing = False
    body: list[str] = []
    for line in lines:
        if heading.match(line.strip()):
            capturing = True
            continue
        if capturing and line.startswith("## "):
            break
        if capturing:
            body.append(line)
    return "\n".join(body).strip()


def _first_sentences(text: str, n: int = 2) -> str:
    blob = " ".join((text or "").split())
    if not blob:
        return ""
    parts = re.split(r"(?<=[.!?])\s+", blob)
    return " ".join(parts[:n]).strip()


def _class_burned(name: str, *, root: Path | None = None) -> bool:
    if not name:
        return False
    try:
        from golf_offshoot.learning_lane_15m.evidence_bar import class_is_burned

        return bool(class_is_burned(name, root=root))
    except Exception:  # noqa: BLE001 — a blind burn file is not a silent trial
        return False


def _is_selection_proposed(
    text: str, registry: dict[str, Any], *, root: Path | None = None
) -> bool:
    if _NAMED_HORSE_NO.search(text or ""):
        return False
    rid = _trial_rule_id(text, registry)
    if rid and _class_burned(rid, root=root):
        return False
    if re.search(r"(?im)^(?:kind|selects)\s*[:=]\s*(selection|true)\b", text or ""):
        return True
    if re.search(r"(?i)\bselection rule\b", text or "") and _RULE_ID.search(text or ""):
        return True
    by_id = {str(row.get("id") or ""): row for row in _rules(registry)}
    for match in _RULE_ID.finditer(text or ""):
        rule = by_id.get(match.group(0))
        if rule and _is_selection(rule):
            return True
    return False


def latest_selection_proposed(
    *, root: Path | None = None, registry: dict[str, Any]
) -> Path | None:
    for path in reversed(_proposed_files(root=root)):
        if _is_selection_proposed(_read(path), registry, root=root):
            return path
    return None


def _matching_operator_note(proposed: Path | None, *, root: Path | None = None) -> Path | None:
    if proposed is None:
        return None
    stem = proposed.name.replace("LEARNING_LANE_15M_LAB_", "LEARNING_LANE_15M_OPERATOR_NOTE_")
    direct = _docs_dir(root=root) / stem
    if direct.is_file():
        return direct
    key = re.search(r"PROPOSED_(\d+)", proposed.name)
    if key:
        needle = key.group(0)
        for path in reversed(_operator_notes(root=root)):
            if needle in path.name:
                return path
    return None


def _trial_rule_id(text: str, registry: dict[str, Any]) -> str:
    by_id = {str(row.get("id") or ""): row for row in _rules(registry)}
    for match in _RULE_ID.finditer(text or ""):
        rid = match.group(0)
        rule = by_id.get(rid)
        if rule and _is_selection(rule):
            return rid
    match = _RULE_ID.search(text or "")
    return match.group(0) if match else ""


def _load_decisions(*, root: Path | None) -> dict[str, dict]:
    if root is not None:
        path = root / "paper" / "rule_decisions.json"
        if not path.is_file():
            path = paper_dir_15m() / "rule_decisions.json"
    else:
        path = paper_dir_15m() / "rule_decisions.json"
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    rows = payload.get("decisions") if isinstance(payload, dict) else None
    return rows if isinstance(rows, dict) else {}


def book_follow_counts(
    rule_id: str, *, root: Path | None = None
) -> dict[str, int]:
    rows = _load_decisions(root=root)
    fills = 0
    skips = 0
    for row in rows.values():
        if not isinstance(row, dict):
            continue
        if str(row.get("rule_id") or "") != rule_id:
            continue
        action = str(row.get("action") or "").strip().lower()
        if action == "fill":
            fills += 1
        elif action in {"skip", "no_rule", "ineligible"}:
            skips += 1
    return {"fills": fills, "skips": skips}


def _park_selection_excerpt(*, root: Path | None, rule_ids: list[str]) -> str:
    text = _read((root or repo_root()) / PARK_REL)
    if not text:
        return ""
    keep: list[str] = []
    for line in text.splitlines():
        if any(rid in line for rid in rule_ids) or re.search(
            r"(?i)selection rule", line
        ):
            keep.append(line)
    return "\n".join(keep)


def _journal_asof(*, root: Path | None = None) -> str:
    path = latest_dir_15m() / "journal.json"
    if root is not None:
        alt = root / "latest" / "journal.json"
        if alt.is_file():
            path = alt
    payload: dict[str, Any] = {}
    if path.is_file():
        try:
            loaded = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            loaded = {}
        if isinstance(loaded, dict):
            payload = loaded
    return str(payload.get("generated_at") or "")


def input_fingerprint(*, root: Path | None = None, registry: dict[str, Any] | None = None) -> str:
    """Hashes of the files that may change the card. Not the SOURCE digest."""
    registry = registry if registry is not None else load_registry(root=root)
    proposed = latest_selection_proposed(root=root, registry=registry)
    note = _matching_operator_note(proposed, root=root)
    executing_ids = [str(row.get("id") or "") for row in executing_rules(registry)]
    trial_id = _trial_rule_id(_read(proposed), registry) if proposed else ""
    count_ids = [rid for rid in executing_ids + [trial_id] if rid]
    counts = {rid: book_follow_counts(rid, root=root) for rid in count_ids}
    park = _park_selection_excerpt(root=root, rule_ids=count_ids)
    payload = {
        "registry": _sha256_file((root or repo_root()) / REGISTRY_REL),
        "proposed": _sha256_file(proposed) if proposed else "",
        "operator_note": _sha256_file(note) if note else "",
        "park_selection": _sha256_text(park),
        "scorecards": [_sha256_file(path) for path in _scorecards(root=root)],
        "counts": counts,
    }
    return _sha256_text(json.dumps(payload, sort_keys=True, default=str))


def card_proof_token(path: Path) -> str | None:
    """Card content minus as-of lines. A timestamp-only rewrite is a heartbeat."""
    if not path.is_file():
        return None
    kept = [
        line
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines()
        if not _ASOF_LINE.search(line)
    ]
    return hashlib.sha256("\n".join(kept).encode("utf-8")).hexdigest()


def build_card(*, root: Path | None = None) -> str:
    registry = load_registry(root=root)
    executing = executing_rules(registry)
    proposed = latest_selection_proposed(root=root, registry=registry)
    proposed_text = _read(proposed) if proposed else ""
    trial_id = _trial_rule_id(proposed_text, registry) if proposed else ""
    trial_rule = next(
        (row for row in _rules(registry) if str(row.get("id") or "") == trial_id),
        {},
    )
    note = _matching_operator_note(proposed, root=root)
    note_text = _read(note) if note else ""
    asof = _journal_asof(root=root) or "unknown"
    fp = input_fingerprint(root=root, registry=registry)

    exec_lines = []
    for row in executing:
        rid = str(row.get("id") or "")
        counts = book_follow_counts(rid, root=root)
        followed = ""
        if counts["fills"] or counts["skips"]:
            followed = (
                f" Book followed {rid}: {counts['fills']} fills, "
                f"{counts['skips']} skips (rule_decisions.json)."
            )
        exec_lines.append(
            f"- `{rid}` (`execution: {str(bool(row.get('execution'))).lower()}`"
            f", kind={row.get('kind') or '—'}).{followed}"
        )
    if not exec_lines:
        book_now = "No rule in the registry carries `execution: true`."
    else:
        book_now = "\n".join(exec_lines)

    if proposed is None:
        on_trial = EMPTY_ON_TRIAL
        why = "—"
        kill = "—"
        verdict = NOT_YET_RULED
        implemented = (
            "No selection rule has `execution: true`. "
            "Baseline fill-all is the executing book, not a selection trial."
        )
        why_src = "—"
        kill_src = "—"
        verdict_src = "—"
    else:
        on_trial = (
            f"`{trial_id or 'unregistered'}` — "
            f"{str(trial_rule.get('rule') or _first_sentences(proposed_text, 1) or '—')}"
        )
        why_body = _section_after(proposed_text, _WHY_HEAD) or proposed_text
        why = _first_sentences(why_body, 2) or "—"
        kill = str(trial_rule.get("falsifier") or "").strip()
        if not kill:
            kill = _first_sentences(_section_after(proposed_text, _FALSIFIER_HEAD), 2) or "—"
        verdict_match = _VERDICT.search(note_text)
        if verdict_match:
            verdict = verdict_match.group(1).strip()
        elif re.search(r"\bPARK(?:ED)?\b", note_text, re.IGNORECASE):
            verdict = "PARK"
        elif re.search(r"\bRUN-ONLY\b", note_text, re.IGNORECASE):
            verdict = "RUN-ONLY"
        elif note_text:
            verdict = _first_sentences(note_text, 1)
        else:
            verdict = NOT_YET_RULED
        exec_flag = bool(trial_rule.get("execution")) if trial_rule else False
        license_line = ""
        if note_text:
            license_line = _first_sentences(note_text, 1)
        implemented = (
            f"`execution: {str(exec_flag).lower()}`"
            + (f" — {license_line}" if license_line else "")
        )
        why_src = str(proposed.relative_to(root or repo_root())) if proposed else "—"
        kill_src = "registry `falsifier`" if trial_rule.get("falsifier") else why_src
        verdict_src = str(note.relative_to(root or repo_root())) if note else "—"

    sources = [
        f"- `{REGISTRY_REL.as_posix()}` sha256={_sha256_file((root or repo_root()) / REGISTRY_REL) or '—'}",
    ]
    if proposed:
        sources.append(
            f"- `{proposed.as_posix() if proposed.is_absolute() else proposed}` "
            f"sha256={_sha256_file(proposed)}"
        )
    if note:
        sources.append(f"- operator note sha256={_sha256_file(note)}")
    sources.append(f"- input_fp: {fp}")
    sources.append("- See Operator note for any fee arithmetic. Not reprinted here.")

    return (
        "# 15m learning card\n\n"
        "Figures from files. Not a verdict. Operator notes remain the verdict SoT.\n\n"
        f"**As-of:** journal generated_at={asof}\n\n"
        "## What the book is doing now\n\n"
        f"{book_now}\n\n"
        "## On trial\n\n"
        f"{on_trial}\n\n"
        "## Why we tried it\n\n"
        f"> {why}\n\n"
        f"Source: {why_src if proposed else '—'}\n\n"
        "## Kill / falsifier\n\n"
        f"> {kill}\n\n"
        f"Source: {kill_src if proposed else '—'}\n\n"
        "## Verdict\n\n"
        f"{verdict}\n\n"
        f"Source: {verdict_src if proposed else '—'}\n\n"
        "## Implemented?\n\n"
        f"{implemented}\n\n"
        "## Sources\n\n"
        + "\n".join(sources)
        + "\n"
    )


def write_learning_card(*, root: Path | None = None) -> Path:
    """Write the card. Never touches caveats, the bar, or the registry."""
    dest = card_path(root=root)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(build_card(root=root), encoding="utf-8")
    return dest


def stale_events(*, root: Path | None = None) -> list[dict[str, Any]]:
    """Owe learning-card when inputs moved or the card is missing.

    Raises if the registry cannot be read — silence is not a pass.
    """
    fp = input_fingerprint(root=root)
    dest = card_path(root=root)
    if not dest.is_file():
        return [
            {
                "kind": "learning_card_stale",
                "ticker": "learning-card",
                "window_id": "",
                "detail": "learning card file missing",
            }
        ]
    text = dest.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"input_fp:\s*([a-f0-9]{64})", text)
    if match and match.group(1) == fp:
        return []
    return [
        {
            "kind": "learning_card_stale",
            "ticker": "learning-card",
            "window_id": "",
            "detail": "learning card inputs moved (registry / proposed / note / park / counts)",
        }
    ]
