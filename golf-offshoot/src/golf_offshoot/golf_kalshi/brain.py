"""Advisor player brain. Production stays keep_expert until a hold-out wins.

Does not import the other-venue golf book. Does not retune from the 15m tape.
Cache per event; rerun only when the scoreboard fingerprint moves.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Protocol

from golf_offshoot.golf_kalshi.espn_bind import event_key_for
from golf_offshoot.golf_kalshi.paths import assert_golf_kalshi_path, brain_cache_path
from golf_offshoot.golf_kalshi.sleeves import market_horizon
from golf_offshoot.localtime import isoformat_now

BRAIN_VERSION = "keep_expert"


class TickBudget:
    def __init__(self, seconds: float = 8.0, *, max_fills: int = 8, max_brain: int = 2) -> None:
        import time

        self.deadline = time.monotonic() + float(seconds)
        self.max_fills = int(max_fills)
        self.max_brain = int(max_brain)
        self.fills = 0
        self.brain_runs = 0

    def remaining(self) -> float:
        import time

        return self.deadline - time.monotonic()

    def can_fill(self) -> bool:
        """Paper fill cap. Clock is for Monte Carlo, not for applying cached p."""
        return self.fills < self.max_fills

    def can_brain(self) -> bool:
        return self.remaining() > 1.0 and self.brain_runs < self.max_brain

    def note_fill(self) -> None:
        self.fills += 1

    def note_brain(self) -> None:
        self.brain_runs += 1


class PlayerBrain(Protocol):
    def field_candidates(self, event_key: str) -> dict[str, str]:
        """normalized_name -> player_id. Empty means the brain cannot see the field."""

    def model_p(self, player_id: str, horizon: str, *, event_key: str = "") -> float | None: ...

    def scoreboard_fingerprint(self, event_key: str) -> str: ...

    def maybe_refresh(
        self,
        event_key: str,
        fingerprint: str,
        *,
        budget: TickBudget | None = None,
        markets: list[dict[str, Any]] | None = None,
    ) -> None: ...


class StaticBrain:
    """Injected map. Tests and first ticks that already have scores."""

    def __init__(
        self,
        candidates: dict[str, str] | None = None,
        probs: dict[str, dict[str, float]] | None = None,
        *,
        fingerprint: str = "static",
        field_source: str = "espn",
        holes: dict[str, int] | None = None,
        event_started: bool = False,
    ) -> None:
        self._candidates = dict(candidates or {})
        self._probs = {k: dict(v) for k, v in (probs or {}).items()}
        self._fp = fingerprint
        self._field_source = field_source
        self._holes = dict(holes or {})
        self._event_started = bool(event_started)

    def player_holes(self, player_id: str, event_key: str = "") -> int | None:
        del event_key
        holes = self._holes.get(str(player_id))
        return int(holes) if holes is not None else None

    def event_started(self, event_key: str = "") -> bool:
        del event_key
        return bool(self._event_started)

    def field_candidates(self, event_key: str) -> dict[str, str]:
        del event_key
        return dict(self._candidates)

    def model_p(self, player_id: str, horizon: str, *, event_key: str = "") -> float | None:
        del event_key
        row = self._probs.get(player_id) or {}
        if horizon in row:
            return float(row[horizon])
        return None

    def scoreboard_fingerprint(self, event_key: str) -> str:
        del event_key
        return self._fp

    def field_source(self, event_key: str) -> str:
        del event_key
        return self._field_source

    def maybe_refresh(
        self,
        event_key: str,
        fingerprint: str,
        *,
        budget: TickBudget | None = None,
        markets: list[dict[str, Any]] | None = None,
    ) -> None:
        del event_key, fingerprint, budget, markets


def fingerprint_scores(rows: list[dict[str, Any]]) -> str:
    blob = json.dumps(rows, sort_keys=True, default=str)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]


def load_brain_cache() -> dict[str, Any]:
    path = brain_cache_path()
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return payload if isinstance(payload, dict) else {}


def save_brain_cache(payload: dict[str, Any]) -> None:
    path = brain_cache_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    assert_golf_kalshi_path(path)
    payload = dict(payload)
    payload["brain_version"] = BRAIN_VERSION
    payload["saved_at"] = isoformat_now()
    path.write_text(json.dumps(payload, indent=2, default=str) + "\n", encoding="utf-8")


def _hunt_fp(hunt: dict[str, Any], fingerprint: str) -> str:
    rows = list(hunt.get("espn_rows") or [])
    if rows:
        return fingerprint_scores(rows)
    names = list(hunt.get("names") or [])
    if names:
        return fingerprint_scores([{"name": n} for n in names])
    return fingerprint or ""


class CachedExpertBrain:
    """Per-event hunt + cached expert p. Refresh only when the fingerprint moves.

    Missing field or missing p → decide_golf skips. That is the brain working.
    """

    def __init__(self, inner: PlayerBrain | None = None) -> None:
        self.inner = inner
        self._cache = load_brain_cache()
        self.hunts_this_tick: list[dict[str, Any]] = []
        self.n_bound = 0
        self._boards = None
        self._dirty = False

    def begin_tick(self, boards=None) -> None:
        self.hunts_this_tick = []
        self.n_bound = 0
        self._boards = boards
        self._dirty = False

    def end_tick(self) -> None:
        if self._dirty:
            save_brain_cache(self._cache)
            self._dirty = False

    def hunt_identity(self, event_key: str, markets: list[dict[str, Any]] | None = None) -> dict[str, Any]:
        """ESPN title-bind or Kalshi names. No history load. No MC."""
        from golf_offshoot.golf_kalshi.catalog_view import catalog_family
        from golf_offshoot.golf_kalshi.field_hunt import hunt_field

        if self.inner is not None:
            return {}
        hunt = hunt_field(event_key, list(markets or []), boards=self._boards)
        self.n_bound += 1
        row = dict((self._cache.get("events") or {}).get(event_key) or {})
        identity_fp = _hunt_fp(hunt, "")
        if row.get("identity_fp") != identity_fp:
            row.pop("probs", None)
            row.pop("fp", None)
        row["identity_fp"] = identity_fp
        row["espn_id"] = hunt.get("espn_id") or ""
        row["espn_name"] = hunt.get("espn_name") or ""
        row["family"] = hunt.get("family") or catalog_family(event_key)
        row["field_source"] = hunt.get("field_source") or "miss"
        row["names"] = list(hunt.get("names") or [])
        row["n_names"] = hunt.get("n_names") or 0
        row["n_recovered"] = hunt.get("n_recovered") or 0
        row["awaiting_history"] = bool(hunt.get("awaiting_history"))
        row["live_competitors"] = int(hunt.get("live_competitors") or 0)
        row["tried_leagues"] = list(hunt.get("tried_leagues") or [])
        if hunt.get("espn_rows"):
            row["espn_rows"] = list(hunt.get("espn_rows") or [])
        if hunt.get("espn_id"):
            row["candidates"] = dict(hunt.get("candidates") or {})
            row["thin"] = False
            row["field_source"] = "espn"
        elif hunt.get("awaiting_history"):
            row["candidates"] = {}
            row["thin"] = False
        else:
            row["candidates"] = dict(hunt.get("candidates") or {})
            row["thin"] = bool(hunt.get("thin"))
        self._cache.setdefault("events", {})[event_key] = row
        self._dirty = True
        return hunt

    def field_source(self, event_key: str) -> str:
        if self.inner is not None and hasattr(self.inner, "field_source"):
            return str(self.inner.field_source(event_key) or "")
        cached = (self._cache.get("events") or {}).get(event_key) or {}
        return str(cached.get("field_source") or "")

    def field_candidates(self, event_key: str) -> dict[str, str]:
        if self.inner is not None:
            return self.inner.field_candidates(event_key)
        cached = (self._cache.get("events") or {}).get(event_key) or {}
        if cached.get("thin") and not cached.get("probs"):
            return {}
        names = cached.get("candidates") or {}
        if isinstance(names, dict) and names:
            return {str(k): str(v) for k, v in names.items()}
        return {}

    def model_p(self, player_id: str, horizon: str, *, event_key: str = "") -> float | None:
        if self.inner is not None:
            return self.inner.model_p(player_id, horizon, event_key=event_key)
        events = self._cache.get("events") or {}
        row = ((events.get(event_key) or {}).get("probs") or {}).get(player_id) or {}
        if horizon in row:
            return float(row[horizon])
        return None

    def scoreboard_fingerprint(self, event_key: str) -> str:
        if self.inner is not None:
            return self.inner.scoreboard_fingerprint(event_key)
        return str(((self._cache.get("events") or {}).get(event_key) or {}).get("fp") or "")

    def maybe_refresh(
        self,
        event_key: str,
        fingerprint: str,
        *,
        budget: TickBudget | None = None,
        markets: list[dict[str, Any]] | None = None,
    ) -> None:
        if self.inner is not None:
            self.inner.maybe_refresh(event_key, fingerprint, budget=budget, markets=markets)
            return
        from golf_offshoot.golf_kalshi.catalog_view import catalog_family
        from golf_offshoot.golf_kalshi.field_hunt import history_floor_ok, hunt_field
        from golf_offshoot.golf_kalshi.score import (
            live_scoreboard_fp,
            score_espn_event,
            score_kalshi_listed,
            shared_ingestor,
        )

        cached = (self._cache.get("events") or {}).get(event_key) or {}
        if not cached.get("identity_fp") and not cached.get("espn_id") and not cached.get("names"):
            self.hunt_identity(event_key, markets)
            cached = (self._cache.get("events") or {}).get(event_key) or {}
        hunt_summary = {
            "event_key": event_key,
            "family": cached.get("family") or catalog_family(event_key),
            "field_source": cached.get("field_source") or "miss",
            "espn_id": cached.get("espn_id") or "",
            "espn_name": cached.get("espn_name") or "",
            "thin": bool(cached.get("thin")),
            "n_names": cached.get("n_names") or 0,
            "n_recovered": cached.get("n_recovered") or 0,
            "tried_leagues": cached.get("tried_leagues") or [],
        }
        espn_id = str(cached.get("espn_id") or "")
        if espn_id:
            live_fp = ""
            try:
                live_fp = live_scoreboard_fp(espn_id) or str(fingerprint or "")
            except Exception:
                live_fp = str(cached.get("fp") or "")
            if cached.get("probs") and live_fp and live_fp == cached.get("fp"):
                self.hunts_this_tick.append({**hunt_summary, "cached": True})
                return
            if budget is not None and not budget.can_brain():
                hunt_summary["deferred"] = True
                self.hunts_this_tick.append(hunt_summary)
                return
            if budget is not None:
                budget.note_brain()
            in_play = any(bool(m.get("in_play")) for m in (markets or [])) or int(cached.get("live_competitors") or 0) > 0
            scored = score_espn_event(espn_id, live=in_play)
            row = dict(cached)
            row["brain_version"] = BRAIN_VERSION
            if scored.get("probs") and int(scored.get("n_players") or 0) > 0:
                row["probs"] = scored.get("probs") or {}
                row["candidates"] = scored.get("candidates") or cached.get("candidates") or {}
                row["field_source"] = "espn"
                row["thin"] = False
                row["fp"] = scored.get("fp") or live_fp
                row["n_players"] = scored.get("n_players") or 0
                hunt_summary["field_source"] = "espn"
                hunt_summary["thin"] = False
                hunt_summary["scored"] = True
                self._store_event(event_key, row, hunt_summary)
                return
            hunt_summary["thin"] = True
            row["thin"] = True
            self._store_event(event_key, row, hunt_summary)
            return
        names = list(cached.get("names") or [])
        if not names:
            row = dict(cached)
            row["probs"] = {}
            row["thin"] = True
            row["field_source"] = cached.get("field_source") or "miss"
            hunt_summary["thin"] = True
            self._store_event(event_key, row, hunt_summary)
            return
        name_fp = _hunt_fp({"names": names}, fingerprint)
        if cached.get("probs") and cached.get("fp") == name_fp:
            self.hunts_this_tick.append({**hunt_summary, "cached": True})
            return
        if budget is not None and (not budget.can_brain() or budget.remaining() < 1.5):
            hunt_summary["deferred"] = True
            hunt_summary["field_source"] = "kalshi_listed"
            self.hunts_this_tick.append(hunt_summary)
            return
        if budget is not None:
            budget.note_brain()
        history = shared_ingestor().load_history(include_in_progress=False)
        hunt = hunt_field(event_key, list(markets or []), history=history, boards=self._boards)
        listed = hunt.get("listed_candidates") or hunt.get("candidates") or {}
        hunt_summary["n_recovered"] = hunt.get("n_recovered") or 0
        hunt_summary["field_source"] = "kalshi_listed"
        row = dict(cached)
        row["brain_version"] = BRAIN_VERSION
        row["awaiting_history"] = False
        row["n_recovered"] = hunt.get("n_recovered") or 0
        if hunt.get("thin") or not listed or not history_floor_ok(int(hunt.get("n_names") or 0), int(hunt.get("n_recovered") or 0)):
            row["probs"] = {}
            row["candidates"] = {}
            row["field_source"] = "kalshi_listed"
            row["thin"] = True
            hunt_summary["thin"] = True
            self._store_event(event_key, row, hunt_summary)
            return
        scored = score_kalshi_listed(names, listed, tour=str(hunt.get("family") or cached.get("family") or "PGA"))
        row["probs"] = scored.get("probs") or {}
        row["candidates"] = scored.get("candidates") or listed
        row["field_source"] = "kalshi_listed"
        row["thin"] = bool(scored.get("thin")) or not row["probs"]
        row["fp"] = scored.get("fp") or name_fp
        row["n_players"] = scored.get("n_players") or 0
        hunt_summary["thin"] = bool(row["thin"])
        hunt_summary["scored"] = True
        self._store_event(event_key, row, hunt_summary)

    def _store_event(self, event_key: str, row: dict[str, Any], hunt_summary: dict[str, Any]) -> None:
        self._cache.setdefault("events", {})[event_key] = row
        self._dirty = True
        self.hunts_this_tick.append(hunt_summary)


def p_for_market(brain: PlayerBrain, player_id: str, market: dict[str, Any]) -> float | None:
    horizon = market_horizon(market)
    key = event_key_for(market)
    return brain.model_p(player_id, horizon, event_key=key)
