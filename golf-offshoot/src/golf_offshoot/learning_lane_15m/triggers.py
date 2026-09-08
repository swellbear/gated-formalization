"""Exception triggers — the events that owe a **judicial** role a turn.

Two opposite failures are fixed here.

Human ``digestor`` had no trigger at all after the figures split: nothing in
``ROLE_ORDER`` named it, so once the leftover owed line cleared the caveat
obligation became invisible. It is now owed on five enumerated exceptions —
the cases where the *generated figures cannot express what changed*. Not zero,
and not every settle.

``operator`` had the opposite problem: every routine settle named it. Ninety-six
windows a day across three roles is roughly 288 owed turns, and a
normally-settled window owes Operator nothing. It is now owed on six enumerated
exceptions.

Both lists are enumerated here **and** in PROTOCOL.md. Nothing in this module
rules, Softens, ADMITs, parks or scores. It reads files and raises an event.
When a check cannot read what it needs, it raises nothing and says so — it
never guesses a window into existence.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from golf_offshoot.learning_lane_15m.paths import paper_dir_15m
from golf_offshoot.localtime import now
from golf_offshoot.operator_surface.observability import repo_root

EVENT_PAPER_JOIN_MISSING_GREW = "paper_join_missing_grew"
EVENT_BOOK_OPEN_NO_JOIN = "book_open_no_join"
EVENT_WINDOW_SEQUENCE_GAP = "window_sequence_gap"
EVENT_SETTLE_CONTRADICTS_BOOK = "settle_contradicts_book"
EVENT_UNRECORDED_COST = "unrecorded_cost"
EVENT_PARK_AGED = "park_aged"
EVENT_RULE_REACHED_N = "rule_reached_n"
EVENT_FALSIFIER_FIRED = "falsifier_fired"
EVENT_LAB_PROPOSED = "lab_proposed"
EVENT_ARTIFACT_UNREVIEWED = "artifact_unreviewed"

WINDOW_S = 900
#: A crew park re-rules within roughly one day of active loop. Restating is
#: legitimate; silence is what is ruled against.
PARK_RERULE_S = 24 * 3600

PARK_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_METHOD_PARK.md"
CAVEATS_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_SOURCE_DIGEST_CAVEATS.md"
PROPOSED_GLOB = "LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_*.md"
REGISTRY_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_RULES.json"
BAR_JSON_REL = Path("golf-offshoot") / "docs" / "LEARNING_LANE_15M_EVIDENCE_BAR.json"


def _event(kind: str, ticker: str, detail: str, **extra: Any) -> dict[str, Any]:
    return {"kind": kind, "ticker": ticker, "window_id": extra.pop("window_id", ""), "detail": detail, **extra}


def _load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return payload if isinstance(payload, dict) else {}


# ------------------------------------------------------- digestor exceptions


def paper_join_missing_grew(
    previous: dict[str, Any] | None,
    current: dict[str, Any],
) -> list[dict[str, Any]]:
    """A new window with an official result and no book on this tree.

    Generated figures cannot express this: a window with no book has no pnl,
    and only a human caveat can say why without inventing one.
    """
    if not previous:
        return []
    before = {str(r.get("ticker") or "") for r in previous.get("paper_join_missing") or []}
    events = []
    for row in current.get("paper_join_missing") or []:
        ticker = str(row.get("ticker") or "")
        if not ticker or ticker in before:
            continue
        events.append(
            _event(
                EVENT_PAPER_JOIN_MISSING_GREW,
                ticker,
                "official result present and no paper book on this tree; "
                "the missing-join list grew",
                window_id=str(row.get("window_id") or ""),
            )
        )
    return events


def new_book_open_no_join(
    previous: dict[str, Any] | None,
    current: dict[str, Any],
) -> list[dict[str, Any]]:
    """A paper book open with no settle join written for it."""
    if not previous:
        return []

    def _open(scan: dict[str, Any]) -> set[str]:
        return {
            str(row.get("ticker") or row.get("window_id") or "")
            for row in scan.get("pending") or []
            if str(row.get("kind") or "") == "book_open_no_join"
        }

    before = _open(previous)
    return [
        _event(
            EVENT_BOOK_OPEN_NO_JOIN,
            key,
            "paper book is open on this window and no settle join has been written",
        )
        for key in sorted(_open(current) - before)
        if key
    ]


def _window_starts(scan: dict[str, Any]) -> list[tuple[datetime, str]]:
    out: list[tuple[datetime, str]] = []
    for ticker, row in (scan.get("settled") or {}).items():
        window_id = str(row.get("window_id") or "")
        match = re.search(r"__(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)__", window_id)
        if not match:
            continue
        try:
            out.append((datetime.fromisoformat(match.group(1).replace("Z", "+00:00")), ticker))
        except ValueError:
            continue
    return sorted(out)


def window_sequence_gaps(
    previous: dict[str, Any] | None,
    current: dict[str, Any],
) -> list[dict[str, Any]]:
    """A hole in the 15-minute sequence — the ``072245`` shape.

    A missing window is not a loss and is never backfilled. It is a caveat,
    because the figures will silently read as an unbroken run without one.
    """
    starts = _window_starts(current)
    before = {t for t, _ in _window_starts(previous or {})}
    events = []
    for (left, _), (right, ticker) in zip(starts, starts[1:]):
        span = (right - left).total_seconds()
        if span <= WINDOW_S:
            continue
        if right in before and left in before:
            continue
        missing = int(span // WINDOW_S) - 1
        events.append(
            _event(
                EVENT_WINDOW_SEQUENCE_GAP,
                ticker,
                f"{missing} window(s) missing between {left.isoformat()} and "
                f"{right.isoformat()}; the sequence is not unbroken. Do not backfill",
            )
        )
    return events


def settles_contradicting_their_book(
    previous: dict[str, Any] | None,
    current: dict[str, Any],
) -> list[dict[str, Any]]:
    """A settled book whose own numbers disagree with each other.

    Three ways it can contradict itself: the recorded winner disagrees with the
    official result, the pnl sign disagrees with the side taken, or the pnl
    magnitude disagrees with the odds the fill was booked at.
    """
    settled = current.get("settled") or {}
    if not settled:
        return []
    before = {str(r.get("ticker") or "") for r in (previous or {}).get("contradictions") or []}
    events: list[dict[str, Any]] = []
    for path in sorted(paper_dir_15m().glob("KXBTC15M-*.json")):
        book = _load_json(path)
        if not book.get("settled_at"):
            continue
        positions = ((book.get("book") or {}).get("positions")) or []
        if not positions:
            continue
        pos = positions[0]
        ticker = str(pos.get("player_id") or "")
        official = (settled.get(ticker) or {}).get("result")
        if not official or ticker in before:
            continue
        side = "yes" if str(pos.get("player_name") or "").upper().startswith("YES") else "no"
        winner = str(book.get("settlement_winner") or "").split(":")[-1].lower()
        pnl = book.get("settlement_pnl")
        stake = pos.get("stake")
        odds = pos.get("decimal_odds")
        if pnl is None or stake is None or odds is None:
            continue
        why = []
        if winner and winner != str(official).lower():
            why.append(f"book records winner {winner!r} but the official result is {official!r}")
        won = side == str(official).lower()
        if won != (float(pnl) > 0):
            why.append(
                f"book took {side.upper()} on an official {official!r} but recorded pnl {pnl}"
            )
        expected = float(stake) * (float(odds) - 1.0) if won else -float(stake)
        if abs(float(pnl) - expected) > 0.01:
            why.append(
                f"recorded pnl {pnl} does not match stake {stake} at decimal odds "
                f"{odds} (expected {expected:.2f})"
            )
        if why:
            events.append(
                _event(
                    EVENT_SETTLE_CONTRADICTS_BOOK,
                    ticker,
                    "; ".join(why),
                    window_id=str(book.get("tournament_id") or ""),
                )
            )
    return events


def unrecorded_cost(*, root: Path | None = None) -> list[dict[str, Any]]:
    """A measured cost the recorded book omits and the caveats do not cite.

    The fee is the live instance: ``settle.py`` pays ``stake x decimal_odds``
    with no fee term. The obligation is not "mention fees" — it is that every
    cost an Operator note has *measured* is acknowledged in the caveats, so the
    recorded totals are never read as complete.
    """
    base = root or repo_root()
    caveats = base / CAVEATS_REL
    caveat_text = caveats.read_text(encoding="utf-8", errors="replace").lower() if caveats.is_file() else ""
    events = []
    notes_dir = base / "golf-offshoot" / "docs"
    for note in sorted(notes_dir.glob(PROPOSED_GLOB)) if notes_dir.is_dir() else []:
        body = note.read_text(encoding="utf-8", errors="replace")
        if not re.search(r"measured", body, re.IGNORECASE):
            continue
        if "fee" in body.lower() and "fee" not in caveat_text:
            events.append(
                _event(
                    EVENT_UNRECORDED_COST,
                    note.name,
                    f"{note.name} measured a cost the recorded book omits and the "
                    "standing caveats do not acknowledge it; recorded totals would "
                    "read as complete",
                )
            )
    return events


# ------------------------------------------------------- operator exceptions


def park_aged(*, root: Path | None = None) -> list[dict[str, Any]]:
    """A crew park past its re-rule window returns to Operator for one line."""
    base = root or repo_root()
    path = base / PARK_REL
    if not path.is_file():
        return []
    cutoff = now() - timedelta(seconds=PARK_RERULE_S)
    events = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if "`crew`" not in line or not line.strip().startswith("|"):
            continue
        stamps = re.findall(r"\d{4}-\d{2}-\d{2}", line)
        if not stamps:
            continue
        try:
            newest = max(datetime.strptime(s, "%Y-%m-%d").replace(tzinfo=cutoff.tzinfo) for s in stamps)
        except ValueError:
            continue
        if newest >= cutoff:
            continue
        label = line.strip().strip("|").split("|")[0].strip()
        events.append(
            _event(
                EVENT_PARK_AGED,
                label,
                f"crew park last stamped {newest.date()} is past its ~1 day re-rule "
                "window; restate the trigger, reclassify it, or close it",
            )
        )
    return events


def rule_reached_n(
    current: dict[str, Any],
    *,
    root: Path | None = None,
) -> list[dict[str, Any]]:
    """A declared rule has accumulated the n its falsifier named."""
    base = root or repo_root()
    registry = _load_json(base / REGISTRY_REL)
    bar = _load_json(base / BAR_JSON_REL)
    target = (bar.get("looks") or {}).get("first_look_n")
    if not target:
        return []
    events = []
    for rule in registry.get("rules") or []:
        if not rule.get("selects"):
            continue
        declared = str(rule.get("declared_at") or "")
        if not declared:
            continue
        try:
            declared_dt = datetime.fromisoformat(declared)
        except ValueError:
            continue
        eligible = 0
        for _, ticker in _window_starts(current):
            row = (current.get("settled") or {}).get(ticker) or {}
            stamp = str(row.get("settlement_ts") or "")
            try:
                closed = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
            except ValueError:
                continue
            if closed > declared_dt:
                eligible += 1
        if eligible >= int(target) and not rule.get("scored_windows"):
            events.append(
                _event(
                    EVENT_RULE_REACHED_N,
                    str(rule.get("id") or ""),
                    f"{eligible} eligible windows since declared_at {declared}, at or "
                    f"past the declared n={target}; the falsifier is now rulable",
                )
            )
    return events


def falsifier_fired(*, root: Path | None = None) -> list[dict[str, Any]]:
    """A falsifier that fired is a complete, successful outcome — record it."""
    base = root or repo_root()
    registry = _load_json(base / REGISTRY_REL)
    events = []
    for rule in registry.get("rules") or []:
        if not rule.get("falsifier_fired"):
            continue
        if rule.get("falsifier_ruled_at"):
            continue
        events.append(
            _event(
                EVENT_FALSIFIER_FIRED,
                str(rule.get("id") or ""),
                "falsifier fired and has not been ruled; record it as a park closed "
                "on that falsifier. Do not delete it and do not score it as a failed turn",
            )
        )
    return events
