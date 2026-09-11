"""In-memory keep_expert MC for the Kalshi gym. Never run_operating. Never write Phase 1 paper."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from golf_offshoot.golf_kalshi.paths import cache_dir
from golf_offshoot.models.enums import Horizon, RunMode

GOLF_KALSHI_SIMS = 400

_INGESTOR = None
_PLAYER_INPUTS: dict[str, Any] = {}


def shared_ingestor():
    """Reuse SG/history HTTP across ticks. Own cache root. Not Phase 1 paper/."""
    global _INGESTOR
    if _INGESTOR is None:
        from golf_offshoot.data_feeds.http import HttpCache
        from golf_offshoot.data_feeds.ingest import RealIngestor

        _INGESTOR = RealIngestor(cache=HttpCache(cache_dir=cache_dir()), refresh=False)
    return _INGESTOR


def _probs_from_bundles(bundles: dict[str, Any]) -> dict[str, dict[str, float]]:
    out: dict[str, dict[str, float]] = {}
    for pid, bundle in (bundles or {}).items():
        row: dict[str, float] = {}
        for horizon in Horizon:
            try:
                row[horizon.value] = float(bundle.p(horizon).central)
            except Exception:
                continue
        if row:
            out[str(pid)] = row
    return out


def _fingerprint_field(players: list[Any], names: list[str]) -> str:
    from golf_offshoot.golf_kalshi.brain import fingerprint_scores

    rows = []
    for player in players:
        rows.append(
            {
                "id": getattr(getattr(player, "player", None), "player_id", "") or "",
                "score": getattr(player, "live_score_to_par", None),
                "thru": getattr(player, "live_holes_completed", None),
            }
        )
    if rows:
        return fingerprint_scores(rows)
    return fingerprint_scores([{"name": n} for n in names])


def live_scoreboard_fp(espn_id: str) -> str:
    """Cheap live thru fingerprint. Does not run MC."""
    from golf_offshoot.data_feeds.espn import parse_event_payload
    from golf_offshoot.golf_kalshi.brain import fingerprint_scores
    from golf_offshoot.golf_kalshi.espn_bind import espn_score_rows

    if not str(espn_id or "").strip():
        return ""
    try:
        payload = shared_ingestor().espn.event_leaderboard(str(espn_id), live=True)
        event = parse_event_payload(payload if isinstance(payload, dict) else {})
    except Exception:
        return ""
    return fingerprint_scores(espn_score_rows(event))


def _espn_competitor_count(espn_id: str) -> int:
    from golf_offshoot.data_feeds.espn import iter_competitors, parse_event_payload

    if not str(espn_id or "").strip():
        return 0
    try:
        payload = shared_ingestor().espn.event_leaderboard(str(espn_id), live=True)
        event = parse_event_payload(payload if isinstance(payload, dict) else {})
    except Exception:
        return 0
    return len([c for c in iter_competitors(event) if c.get("athlete")])


def score_espn_event(espn_id: str, *, live: bool = True) -> dict[str, Any]:
    """Ingest one ESPN event with no odds venue. Score with keep_expert α. No persist."""
    from golf_offshoot.data_feeds.names import normalize_name
    from golf_offshoot.operating import make_engine
    from golf_offshoot.pipeline import GolfOffshootPipeline

    if not str(espn_id or "").strip():
        return {"probs": {}, "candidates": {}, "fp": "", "field_source": "miss", "n_players": 0}
    if _espn_competitor_count(espn_id) <= 0:
        return {
            "probs": {},
            "candidates": {},
            "fp": "",
            "field_source": "espn",
            "espn_id": str(espn_id),
            "n_players": 0,
        }
    ingestor = shared_ingestor()
    mode = RunMode.LIVE if live else RunMode.PRE_TOURNAMENT
    tournament, field, _quotes, _inv = ingestor.ingest(
        str(espn_id),
        mode=mode,
        include_odds=False,
        include_season_stats=True,
    )
    engine = make_engine(sims=GOLF_KALSHI_SIMS)
    prepared = GolfOffshootPipeline(engine=engine, apply_decisions=False).prepare_field(tournament, field)
    bundles, _thetas, _warn = engine.run(tournament, prepared)
    candidates = {
        normalize_name(p.player.name): p.player.player_id
        for p in prepared.players
        if p.player.name and p.player.player_id
    }
    for player in prepared.players:
        pid = str(player.player.player_id or "")
        if pid:
            _PLAYER_INPUTS[pid] = player
    return {
        "probs": _probs_from_bundles(bundles),
        "candidates": candidates,
        "fp": _fingerprint_field(prepared.players, list(candidates.keys())),
        "field_source": "espn",
        "espn_id": str(espn_id),
        "n_players": len(prepared.players),
    }


def _display_for(pid: str, names: list[str], candidates: dict[str, str]) -> str:
    from golf_offshoot.data_feeds.names import normalize_name

    for name in names:
        if candidates.get(normalize_name(name)) == pid:
            return name
    for key, val in (candidates or {}).items():
        if val == pid:
            return key
    return pid


def score_kalshi_listed(
    names: list[str],
    candidates: dict[str, str],
    *,
    tour: str = "PGA",
) -> dict[str, Any]:
    """History-id field only. No live thru. keep_expert MC. Skip tote / unrecovered ids."""
    from golf_offshoot.data_feeds.field_fallback import is_provisional_player_id, stub_competitor
    from golf_offshoot.data_feeds.names import normalize_name
    from golf_offshoot.models.enums import CourseType
    from golf_offshoot.models.schemas import Course, FieldSnapshot, Tournament
    from golf_offshoot.operating import make_engine
    from golf_offshoot.pipeline import GolfOffshootPipeline

    recovered = [
        (name, pid)
        for name, pid in (candidates or {}).items()
        if pid and not is_provisional_player_id(pid)
    ]
    if not recovered:
        return {
            "probs": {},
            "candidates": dict(candidates or {}),
            "fp": "",
            "field_source": "kalshi_listed",
            "thin": True,
            "n_players": 0,
        }
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    course = Course(
        course_id="kalshi-listed",
        name="Kalshi listed field",
        course_type=CourseType.PARKLAND,
    )
    tournament = Tournament(
        tournament_id=f"kalshi-listed-{tour}",
        name=f"{tour} Kalshi listed",
        course=course,
        start_date=day,
        tour=str(tour or "PGA"),
        espn_event_id=None,
    )
    ingestor = shared_ingestor()
    history = ingestor.load_history(include_in_progress=False)
    players = []
    for _norm, pid in recovered:
        cached = _PLAYER_INPUTS.get(pid)
        if cached is not None:
            players.append(cached)
            continue
        display = _display_for(pid, names, candidates)
        comp = stub_competitor(display, pid)
        try:
            player = ingestor._player_inputs(  # noqa: SLF001
                comp,
                tournament,
                history,
                None,
                mode=RunMode.PRE_TOURNAMENT,
                include_season_stats=True,
            )
        except Exception:
            continue
        _PLAYER_INPUTS[pid] = player
        players.append(player)
    if not players:
        return {
            "probs": {},
            "candidates": dict(candidates or {}),
            "fp": "",
            "field_source": "kalshi_listed",
            "thin": True,
            "n_players": 0,
        }
    field = FieldSnapshot(
        tournament_id=tournament.tournament_id,
        mode=RunMode.PRE_TOURNAMENT,
        players=players,
        notes="kalshi_listed",
    )
    engine = make_engine(sims=GOLF_KALSHI_SIMS)
    prepared = GolfOffshootPipeline(engine=engine, apply_decisions=False).prepare_field(tournament, field)
    bundles, _thetas, _warn = engine.run(tournament, prepared)
    cand = dict(candidates or {})
    for p in prepared.players:
        if p.player.name and p.player.player_id:
            cand[normalize_name(p.player.name)] = p.player.player_id
    return {
        "probs": _probs_from_bundles(bundles),
        "candidates": cand,
        "fp": _fingerprint_field(prepared.players, names),
        "field_source": "kalshi_listed",
        "n_players": len(prepared.players),
    }
