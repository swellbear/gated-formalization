"""Join operating shadow advises to real paper/ESPN settles. Never invents outcomes."""

from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from datetime import datetime
from pathlib import Path
from typing import Any

from golf_offshoot.models.enums import is_round_leader_bet
from golf_offshoot.operator_surface.modes import is_mock_or_demo_text
from golf_offshoot.strategy.paper_ledger import EventInspect, PaperLedger, ticket_hit

SETTLE_PAPER_WIN = "paper_win"
SETTLE_PAPER_LOSE = "paper_lose"
SETTLE_NEVER = "never_settled"
SETTLE_STATUS_VALUES = frozenset({SETTLE_PAPER_WIN, SETTLE_PAPER_LOSE, SETTLE_NEVER})

SOURCE_LEDGER_TICKET = "paper_ledger_ticket"
SOURCE_ESPN_OFFICIAL = "espn_official_final"
SOURCE_PAPER_BOOK_WINNER = "paper_book_official_winner"
SOURCE_FINISH_UNKNOWN = "espn_official_final:finish_unknown"
SOURCE_ROUND_LEADER = "espn_official_final:round_leader_not_72_hole"

SETTLEABLE_MARKETS = frozenset({"win", "top_5", "top_10", "top_20", "make_cut"})

_KALSHI_MARKERS = ("KALSHI", "KALSHI_DEMO", "KALSHI DEMO")


InspectMap = Mapping[str, EventInspect]
InspectFn = Callable[..., EventInspect]


def normalize_settle_status(raw: Any) -> str | None:
    if raw is None or raw == "":
        return None
    value = str(raw).strip()
    if value in SETTLE_STATUS_VALUES:
        return value
    return None


def is_relevant_advise(row: Mapping[str, Any]) -> bool:
    """72-hole markets that can take paper_win / paper_lose from an official finish."""
    return str(row.get("market") or "").strip().lower() in SETTLEABLE_MARKETS


def settle_banner_for_rows(rows: list[Mapping[str, Any]]) -> str | None:
    """SETTLE_PENDING unless every relevant advise is paper_win or paper_lose.

    never_settled and missing settle_status both keep the weekly operating claim
    blocked. Round-leader / non-settleable markets are not relevant.
    """
    relevant = [row for row in rows if is_relevant_advise(row)]
    if not relevant:
        return "SETTLE_PENDING"
    if all(normalize_settle_status(row.get("settle_status")) in {SETTLE_PAPER_WIN, SETTLE_PAPER_LOSE} for row in relevant):
        return None
    return "SETTLE_PENDING"


def settle_counts(rows: list[Mapping[str, Any]]) -> dict[str, int]:
    counts = {
        SETTLE_PAPER_WIN: 0,
        SETTLE_PAPER_LOSE: 0,
        SETTLE_NEVER: 0,
        "missing": 0,
        "relevant": 0,
        "irrelevant": 0,
    }
    for row in rows:
        status = normalize_settle_status(row.get("settle_status"))
        if is_relevant_advise(row):
            counts["relevant"] += 1
        else:
            counts["irrelevant"] += 1
        if status is None:
            counts["missing"] += 1
        else:
            counts[status] += 1
    return counts


def join_shadow_settles(
    rows: list[dict[str, Any]],
    *,
    artifact_root: Path | None = None,
    inspect_events: EventInspect | InspectMap | InspectFn | None = None,
    ledger: PaperLedger | None = None,
) -> list[dict[str, Any]]:
    """Enrich copies of advise dicts. Does not rewrite the journal file.

    Precedence for a row that does not already have a valid settle_status:
    1. Lived paper ledger ticket (player_id + market on that event)
    2. Official ESPN-shaped inspect (completed + exactly one official winner)
    3. Settled lived paper book winner name, win market only

    Unofficial / playoff / inspect failure → leave unset (SETTLE_PENDING).
    Official but finish unknown or round-leader market → never_settled.
    MOCK/DEMO and Kalshi-shaped blobs are not sources.
    """
    if not rows:
        return []
    ledger_obj = ledger if ledger is not None else _load_lived_ledger(artifact_root)
    books = _load_settled_lived_books(artifact_root)
    cached = _load_settlement_inspects(artifact_root)
    out: list[dict[str, Any]] = []
    for row in rows:
        enriched = dict(row)
        if normalize_settle_status(enriched.get("settle_status")) is not None:
            out.append(enriched)
            continue
        if _is_barred_blob(enriched):
            out.append(enriched)
            continue
        joined = _join_one(
            enriched,
            ledger=ledger_obj,
            books=books,
            cached=cached,
            inspect_events=inspect_events,
        )
        out.append(joined)
    return out


def backfill_shadow_settles(
    path: Path,
    *,
    artifact_root: Path | None = None,
    inspect_events: EventInspect | InspectMap | InspectFn | None = None,
    ledger: PaperLedger | None = None,
) -> int:
    """Write settle fields only when a real paper_win / paper_lose is known.

    never_settled / pending stay view-loud and are not invented onto disk.
    Existing settle_status values are left untouched.
    """
    if not path.is_file():
        return 0
    raw_text = path.read_text(encoding="utf-8")
    if _is_barred_text(raw_text):
        raise ValueError("MOCK/DEMO or Kalshi-shaped shadow is barred from settle backfill")
    original_rows: list[dict[str, Any]] = []
    raw_lines: list[str] = []
    for line in raw_text.splitlines():
        if not line.strip():
            continue
        raw_lines.append(line)
        original_rows.append(json.loads(line))
    joined = join_shadow_settles(
        original_rows,
        artifact_root=artifact_root,
        inspect_events=inspect_events,
        ledger=ledger,
    )
    changed = 0
    out_lines: list[str] = []
    for raw_line, before, after in zip(raw_lines, original_rows, joined):
        if normalize_settle_status(before.get("settle_status")) is not None:
            out_lines.append(raw_line)
            continue
        status = normalize_settle_status(after.get("settle_status"))
        if status not in {SETTLE_PAPER_WIN, SETTLE_PAPER_LOSE}:
            out_lines.append(raw_line)
            continue
        payload = json.loads(raw_line)
        payload["settle_status"] = status
        if after.get("settled_at"):
            payload["settled_at"] = after["settled_at"]
        if after.get("settle_source"):
            payload["settle_source"] = after["settle_source"]
        out_lines.append(json.dumps(payload, default=str))
        changed += 1
    if changed:
        path.write_text("\n".join(out_lines) + ("\n" if out_lines else ""), encoding="utf-8")
    return changed


def _join_one(
    row: dict[str, Any],
    *,
    ledger: PaperLedger | None,
    books: dict[str, Any],
    cached: dict[str, EventInspect],
    inspect_events: EventInspect | InspectMap | InspectFn | None,
) -> dict[str, Any]:
    event_id = str(row.get("tournament_id") or "").strip()
    player_id = str(row.get("player_id") or "").strip()
    market = str(row.get("market") or "").strip().lower()
    if not event_id or not market:
        return row

    ticket = _ledger_ticket(ledger, event_id, player_id, row.get("player"), market)
    if ticket is not None:
        won = bool(ticket.get("won"))
        row["settle_status"] = SETTLE_PAPER_WIN if won else SETTLE_PAPER_LOSE
        if ticket.get("settled_at"):
            row["settled_at"] = ticket["settled_at"]
        row["settle_source"] = SOURCE_LEDGER_TICKET
        return row

    inspect = _resolve_inspect(event_id, inspect_events, cached)
    if inspect is not None:
        return _apply_official_inspect(row, inspect, event_id, player_id, market)

    book = books.get(event_id)
    if book is not None and market == "win":
        winner_name = str(getattr(book, "settlement_winner", "") or "")
        settled_at = getattr(book, "settled_at", None)
        if winner_name and settled_at is not None:
            hit = _name_is_winner(row.get("player"), winner_name)
            row["settle_status"] = SETTLE_PAPER_WIN if hit else SETTLE_PAPER_LOSE
            row["settled_at"] = _stamp(settled_at)
            row["settle_source"] = SOURCE_PAPER_BOOK_WINNER
            return row
    return row


def _apply_official_inspect(
    row: dict[str, Any],
    inspect: EventInspect,
    event_id: str,
    player_id: str,
    market: str,
) -> dict[str, Any]:
    if _is_barred_blob(
        {
            "event_name": inspect.event_name,
            "status_note": inspect.status_note,
        }
    ):
        return row
    if not inspect.completed:
        return row
    winners = set(inspect.winner_ids or [])
    if not winners:
        winners = {pid for pid, (place, _n) in inspect.finishes.items() if place == 1}
    if len(winners) != 1:
        return row
    if is_round_leader_bet(market):
        row["settle_status"] = SETTLE_NEVER
        row["settle_source"] = SOURCE_ROUND_LEADER
        return row
    if player_id not in inspect.finishes:
        row["settle_status"] = SETTLE_NEVER
        row["settle_source"] = SOURCE_FINISH_UNKNOWN
        return row
    place, _name = inspect.finishes[player_id]
    if place is None:
        row["settle_status"] = SETTLE_NEVER
        row["settle_source"] = SOURCE_FINISH_UNKNOWN
        return row
    won = ticket_hit(market, place, winners, player_id)
    row["settle_status"] = SETTLE_PAPER_WIN if won else SETTLE_PAPER_LOSE
    row["settle_source"] = SOURCE_ESPN_OFFICIAL
    return row


def _ledger_ticket(
    ledger: PaperLedger | None,
    event_id: str,
    player_id: str,
    player_name: Any,
    market: str,
) -> dict[str, Any] | None:
    if ledger is None:
        return None
    if _is_barred_blob(ledger.model_dump(mode="json")):
        return None
    name = str(player_name or "").strip().casefold()
    for week in ledger.events:
        if str(week.event_id) != event_id:
            continue
        if _is_barred_blob(week.model_dump(mode="json")):
            continue
        for ticket in week.tickets:
            same_player = (player_id and ticket.player_id == player_id) or (
                name and str(ticket.player_name or "").strip().casefold() == name
            )
            if not same_player:
                continue
            if str(ticket.bet_type or "").strip().lower() != market:
                continue
            return {
                "won": ticket.won,
                "settled_at": _stamp(week.settled_at),
            }
    return None


def _resolve_inspect(
    event_id: str,
    inspect_events: EventInspect | InspectMap | InspectFn | None,
    cached: dict[str, EventInspect],
) -> EventInspect | None:
    if isinstance(inspect_events, EventInspect):
        return inspect_events
    if isinstance(inspect_events, Mapping):
        found = inspect_events.get(event_id)
        if found is not None:
            return found
    elif callable(inspect_events):
        try:
            found = inspect_events(event_id, refresh=False)
        except TypeError:
            try:
                found = inspect_events(event_id)
            except Exception:
                found = None
        except Exception:
            found = None
        if isinstance(found, EventInspect):
            return found
    return cached.get(event_id)


def _load_lived_ledger(artifact_root: Path | None) -> PaperLedger | None:
    if artifact_root is None:
        return None
    path = artifact_root / "paper" / "ledger.json"
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    if _is_barred_text(text):
        return None
    try:
        return PaperLedger.model_validate_json(text)
    except (OSError, ValueError, KeyError, TypeError):
        return None


def _load_settled_lived_books(artifact_root: Path | None) -> dict[str, Any]:
    out: dict[str, Any] = {}
    if artifact_root is None:
        return out
    paper = artifact_root / "paper"
    if not paper.is_dir():
        return out
    from golf_offshoot.strategy.paper_book import PaperBookFile

    for path in paper.glob("*.json"):
        name = path.name.lower()
        if name == "ledger.json" or name.startswith("ledger_"):
            continue
        text = path.read_text(encoding="utf-8")
        if _is_barred_text(text):
            continue
        try:
            rec = PaperBookFile.model_validate_json(text)
        except (OSError, ValueError, KeyError, TypeError):
            continue
        if (rec.path_id or "lived") != "lived":
            continue
        if rec.settled_at is None:
            continue
        out[str(rec.tournament_id)] = rec
    return out


def _load_settlement_inspects(artifact_root: Path | None) -> dict[str, EventInspect]:
    out: dict[str, EventInspect] = {}
    if artifact_root is None:
        return out
    folder = artifact_root / "settlements"
    if not folder.is_dir():
        return out
    for path in folder.glob("*.json"):
        text = path.read_text(encoding="utf-8")
        if _is_barred_text(text):
            continue
        inspect = _inspect_from_payload(text)
        if inspect is None:
            continue
        event_id = path.stem
        try:
            payload = json.loads(text)
            if isinstance(payload, dict) and payload.get("event_id"):
                event_id = str(payload["event_id"])
        except ValueError:
            pass
        out[event_id] = inspect
    return out


def _inspect_from_payload(text: str) -> EventInspect | None:
    try:
        payload = json.loads(text)
    except ValueError:
        return None
    if not isinstance(payload, dict):
        return None
    finishes_raw = payload.get("finishes") or {}
    finishes: dict[str, tuple[int | None, str]] = {}
    if isinstance(finishes_raw, dict):
        for pid, item in finishes_raw.items():
            if isinstance(item, (list, tuple)) and item:
                place = item[0]
                name = str(item[1]) if len(item) > 1 else str(pid)
                finishes[str(pid)] = (int(place) if place is not None else None, name)
    winners = payload.get("winner_ids") or []
    if not isinstance(winners, list):
        winners = []
    return EventInspect(
        completed=bool(payload.get("completed")),
        finishes=finishes,
        winner_ids=[str(x) for x in winners],
        event_name=str(payload.get("event_name") or ""),
        status_note=str(payload.get("status_note") or ""),
    )


def _name_is_winner(player: Any, winner_name: str) -> bool:
    left = str(player or "").strip().casefold()
    right = str(winner_name or "").strip().casefold()
    return bool(left and right and left == right)


def _stamp(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.isoformat()
    text = str(value).strip()
    return text or None


def _is_barred_text(text: str) -> bool:
    if is_mock_or_demo_text(text):
        return True
    blob = text.upper()
    return any(marker in blob for marker in _KALSHI_MARKERS)


def _is_barred_blob(payload: Any) -> bool:
    try:
        text = json.dumps(payload, default=str)
    except (TypeError, ValueError):
        text = str(payload)
    return _is_barred_text(text)
