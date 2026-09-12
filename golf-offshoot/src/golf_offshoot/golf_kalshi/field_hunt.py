"""Hunt a real field for one Kalshi golf event. ESPN first, then Kalshi-listed names. Never Polymarket."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from golf_offshoot.data_feeds.field_fallback import (
    attach_history_ids,
    history_name_ids,
    is_skip_field_name,
    provisional_player_id,
)
from golf_offshoot.data_feeds.names import normalize_name
from golf_offshoot.golf_kalshi.espn_bind import bind_espn_event, event_key_for
from golf_offshoot.golf_kalshi.matcher import extract_player_name


def history_floor_ok(n_names: int, n_recovered: int) -> bool:
    """Half the extracted names, or 20 recovered ids, whichever is smaller and at least 1."""
    n = int(n_names or 0)
    recovered = int(n_recovered or 0)
    if n <= 0 or recovered <= 0:
        return False
    need = min(max(1, n // 2), 20)
    return recovered >= need


def listed_name_candidates(
    names: list[str],
    recovered: dict[str, str] | None = None,
) -> dict[str, str]:
    """normalized_name -> id. Keep listed names even when history ids are thin or deferred."""
    recovered = dict(recovered or {})
    out: dict[str, str] = {}
    for raw in names:
        nm = str(raw or "").strip()
        if not nm or is_skip_field_name(nm):
            continue
        key = normalize_name(nm)
        if not key:
            continue
        out[key] = recovered.get(key) or provisional_player_id(nm)
    for key, pid in recovered.items():
        if key and pid:
            out[str(key)] = str(pid)
    return out


def kalshi_listed_names(markets: list[dict[str, Any]]) -> list[str]:
    seen: set[str] = set()
    names: list[str] = []
    for market in markets:
        name = extract_player_name(market)
        if not name or is_skip_field_name(name):
            continue
        key = normalize_name(name)
        if not key or key in seen:
            continue
        seen.add(key)
        names.append(name.strip())
    return names


def _attach_listed(names: list[str], history) -> tuple[dict[str, str], int, bool]:
    if not names:
        return {}, 0, True
    if history is None:
        return listed_name_candidates(names), 0, False
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    hist_ids = history_name_ids(history, before=day)
    attached = attach_history_ids(names, hist_ids)
    recovered = {normalize_name(nm): pid for nm, pid, ok in attached if ok}
    n_recovered = len(recovered)
    thin = not history_floor_ok(len(names), n_recovered)
    return listed_name_candidates(names, recovered), n_recovered, thin


def hunt_field(
    event_key: str,
    markets: list[dict[str, Any]],
    *,
    client=None,
    history=None,
    bind: dict[str, Any] | None = None,
    boards=None,
) -> dict[str, Any]:
    """ESPN bind if titles match. Else Kalshi open names + history ids. No invented players."""
    rows = [m for m in markets if event_key_for(m) == event_key]
    sample = rows[0] if rows else {"series_ticker": event_key, "event_ticker": event_key}
    bind = (
        bind
        if bind is not None
        else bind_espn_event(sample, client=client, boards=boards)
    )
    names = kalshi_listed_names(rows)
    espn_id = str(bind.get("espn_id") or "")
    listed, n_recovered, listed_thin = _attach_listed(names, history)
    out: dict[str, Any] = {
        "event_key": event_key,
        "family": bind.get("family") or "",
        "espn_id": espn_id,
        "espn_name": str(bind.get("espn_name") or ""),
        "league": str(bind.get("league") or ""),
        "field_source": "",
        "names": names,
        "n_names": len(names),
        "n_recovered": n_recovered,
        "candidates": dict(bind.get("candidates") or {}) if espn_id else dict(listed),
        "listed_candidates": listed,
        "espn_rows": list(bind.get("espn_rows") or []),
        "thin": False,
        "tried_leagues": list(bind.get("tried_leagues") or []),
        "live_competitors": int(bind.get("live_competitors") or 0),
        "awaiting_history": False,
    }
    if espn_id:
        out["field_source"] = "espn"
        if not out["live_competitors"]:
            out["live_competitors"] = len(out["espn_rows"])
        return out
    if not names:
        out["field_source"] = "miss"
        out["thin"] = True
        out["candidates"] = {}
        return out
    out["field_source"] = "kalshi_listed"
    if history is None:
        out["awaiting_history"] = True
        out["thin"] = False
        out["candidates"] = listed_name_candidates(names)
        out["listed_candidates"] = dict(out["candidates"])
        out["n_recovered"] = 0
        return out
    out["thin"] = listed_thin
    out["candidates"] = listed
    out["listed_candidates"] = dict(listed)
    return out
