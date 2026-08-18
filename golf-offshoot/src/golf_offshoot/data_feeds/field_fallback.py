"""Provisional field when ESPN competitors are empty. Not an official ESPN field."""

from __future__ import annotations

from typing import Any

from golf_offshoot.data_feeds.names import match_name, normalize_name
from golf_offshoot.models.enums import DataRole, SourceKind
from golf_offshoot.models.schemas import DataQuality

_SKIP = {
    "other",
    "field",
    "the field",
    "any other",
    "rest of field",
    "the rest of the field",
}


def is_skip_field_name(name: str) -> bool:
    return normalize_name(name) in _SKIP


def provisional_player_id(name: str) -> str:
    """Stable non-ESPN id. Never passed off as an athlete id."""
    slug = normalize_name(name).replace(" ", "-")
    return f"name:{slug or 'unknown'}"


def is_provisional_player_id(player_id: str) -> bool:
    return str(player_id or "").startswith("name:")


def history_name_ids(history, *, before: str, exclude_event_id: str | None = None) -> dict[str, str]:
    """normalized full name -> ESPN athlete id from completed events before tee."""
    out: dict[str, str] = {}
    for ev in history.prior(before, exclude_event_id=exclude_event_id):
        for row in ev.finishes:
            key = normalize_name(row.name)
            pid = str(row.player_id or "").strip()
            if not key or not pid or pid.startswith("name:"):
                continue
            out[key] = pid
    return out


def stub_competitor(name: str, player_id: str) -> dict[str, Any]:
    return {
        "id": player_id,
        "athlete": {"id": player_id, "displayName": name},
        "status": {"type": {"name": "STATUS_SCHEDULED"}},
    }


def attach_history_ids(
    names: list[str],
    history_ids: dict[str, str],
) -> list[tuple[str, str, bool]]:
    """(display name, player_id, recovered_espn_id). Skip Other/Field."""
    attached: list[tuple[str, str, bool]] = []
    seen: set[str] = set()
    for raw in names:
        nm = str(raw or "").strip()
        if not nm or is_skip_field_name(nm):
            continue
        key = normalize_name(nm)
        if not key or key in seen:
            continue
        seen.add(key)
        pid = match_name(nm, history_ids)
        if pid:
            attached.append((nm, pid, True))
        else:
            attached.append((nm, provisional_player_id(nm), False))
    return attached


def field_quality(
    *,
    n: int,
    source_name: str,
    history_matched: int,
    notes: str,
    provisional: bool,
) -> DataQuality:
    from golf_offshoot.localtime import now

    if n <= 0:
        return DataQuality(
            score=0.0,
            role=DataRole.PRIMARY,
            source_name="espn_field",
            as_of=now(),
            missing=True,
            source_kind=SourceKind.UNAVAILABLE,
            notes="ESPN leaderboard competitors empty; no provisional name list",
        )
    if not provisional:
        return DataQuality(
            score=0.92,
            role=DataRole.PRIMARY,
            source_name="espn_field",
            as_of=now(),
            n_observations=n,
            source_kind=SourceKind.REAL_LIVE,
            notes=notes or "ESPN leaderboard competitors",
        )
    return DataQuality(
        score=0.55,
        role=DataRole.FALLBACK,
        source_name=source_name,
        as_of=now(),
        n_observations=n,
        source_kind=SourceKind.DERIVED_FROM_REAL,
        notes=(
            f"{notes}; ESPN competitors empty; {history_matched}/{n} names recovered "
            "to ESPN history ids; not an official ESPN field"
        ).strip("; "),
    )


def list_provisional_names(
    *,
    tournament_name: str,
    odds_book: str,
    cache,
    refresh: bool = False,
) -> tuple[list[str], str]:
    """Names from the pinned book only. auto uses Bovada. Never mixes books."""
    from golf_offshoot.data_feeds.hardrock import resolve_odds_book

    book = resolve_odds_book(odds_book)
    try:
        if book == "hardrockbet":
            return [], "unavailable"
        if book == "polymarket":
            from golf_offshoot.data_feeds.polymarket import PolymarketOddsFeed

            names = PolymarketOddsFeed(cache=cache, refresh=refresh).list_winner_names(
                tournament_name, refresh=refresh
            )
            return names, "polymarket_outright_names"
        from golf_offshoot.data_feeds.bovada import BovadaOddsFeed

        names = BovadaOddsFeed(cache=cache, refresh=refresh).list_winner_names(
            tournament_name, refresh=refresh
        )
        return names, "bovada_outright_names"
    except Exception:
        return [], "unavailable"
