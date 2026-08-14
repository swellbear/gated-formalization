"""Paper-observation log of strategy advises. Never places a bet."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel

from golf_offshoot.data_feeds.http import package_data_dir
from golf_offshoot.models.enums import BetType, Horizon, StrategyActionKind, StrategyMode
from golf_offshoot.models.schemas import MarketSnapshot, TournamentRunResult
from golf_offshoot.models.strategy import StrategyAction, StrategyRecommendation

SHADOW_KINDS = {
    StrategyActionKind.NEW_BET,
    StrategyActionKind.ADD,
    StrategyActionKind.REDUCE,
    StrategyActionKind.EXIT,
    StrategyActionKind.REALLOCATE,
}

_H = {
    BetType.WIN: Horizon.WIN,
    BetType.TOP_5: Horizon.TOP_5,
    BetType.TOP_10: Horizon.TOP_10,
    BetType.TOP_20: Horizon.TOP_20,
    BetType.MAKE_CUT: Horizon.MAKE_CUT,
}


class ShadowAdvise(BaseModel):
    timestamp: datetime
    tournament: str
    tournament_id: str
    player: str
    player_id: str
    market: str
    posted_decimal: float | None = None
    model_probability: float | None = None
    model_p_low: float | None = None
    model_p_high: float | None = None
    suggested_stake: float = 0.0
    mode: str
    run_mode: str
    reason: str
    odds_as_of: datetime | None = None
    run_id: str
    recommendation_id: str
    action_kind: str
    never_auto_bet: bool = True
    paper_observation_only: bool = True


def default_shadow_path() -> Path:
    path = package_data_dir() / "shadow" / "advises.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def append_shadow_advises(
    result: TournamentRunResult,
    *,
    path: Path | None = None,
    market: MarketSnapshot | None = None,
) -> list[ShadowAdvise]:
    rec = result.strategy
    if rec is None or not rec.enabled:
        return []
    rows = _entries_from_recommendation(
        rec,
        tournament_name=result.tournament.name,
        tournament_id=result.tournament.tournament_id,
        run_id=result.run_id,
        ranked=result.ranked,
        market=market if market is not None else result.market,
    )
    if not rows:
        return []
    dest = path or default_shadow_path()
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("a", encoding="utf-8") as fh:
        for row in rows:
            fh.write(row.model_dump_json() + "\n")
    return rows


def load_shadow(path: Path | None = None) -> list[ShadowAdvise]:
    dest = path or default_shadow_path()
    if not dest.exists():
        return []
    out: list[ShadowAdvise] = []
    for line in dest.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        out.append(ShadowAdvise.model_validate_json(line))
    return out


def format_shadow_review(rows: list[ShadowAdvise], *, n: int = 40) -> str:
    if not rows:
        return "shadow journal empty — no new_bet/add/reduce/exit/reallocate advises logged"
    lines = [
        "SHADOW JOURNAL (paper observation only — never auto-bet)",
        f"n={len(rows)} showing last {min(n, len(rows))}",
        "",
    ]
    for row in rows[-n:]:
        dec = f"{row.posted_decimal:.2f}" if row.posted_decimal else "n/a"
        p = f"{row.model_probability:.3f}" if row.model_probability is not None else "n/a"
        rng = ""
        if row.model_p_low is not None and row.model_p_high is not None:
            rng = f" [{row.model_p_low:.3f},{row.model_p_high:.3f}]"
        odds_at = row.odds_as_of.isoformat() if row.odds_as_of else "unavailable"
        lines.append(
            f"{row.timestamp.isoformat()} {row.mode} {row.action_kind} "
            f"{row.player} {row.market} posted={dec} model_p={p}{rng} "
            f"stake={row.suggested_stake:.2f} odds_as_of={odds_at}"
        )
        lines.append(f"    {row.tournament} run={row.run_id} — {row.reason}")
    lines.append("")
    lines.append(
        "Review later: compare posted_decimal at odds_as_of to the settlement result "
        "for that player/market. This file is not a betting bot ledger."
    )
    return "\n".join(lines)


def _entries_from_recommendation(
    rec: StrategyRecommendation,
    *,
    tournament_name: str,
    tournament_id: str,
    run_id: str,
    ranked,
    market: MarketSnapshot | None,
) -> list[ShadowAdvise]:
    by_id = {r.player_id: r for r in ranked}
    quote_map: dict[tuple[str, str], tuple[float | None, datetime | None]] = {}
    if market:
        for q in market.quotes:
            if q.line_role == "opening":
                continue
            quote_map[(q.player_id, q.bet_type.value)] = (q.decimal_odds, q.as_of)
    out: list[ShadowAdvise] = []
    now = rec.as_of or datetime.now(timezone.utc)
    for act in rec.actions:
        if act.kind not in SHADOW_KINDS:
            continue
        out.append(
            _from_action(
                act,
                rec=rec,
                tournament_name=tournament_name,
                tournament_id=tournament_id,
                run_id=run_id,
                by_id=by_id,
                quote_map=quote_map,
                timestamp=now,
            )
        )
    return out


def _from_action(
    act: StrategyAction,
    *,
    rec: StrategyRecommendation,
    tournament_name: str,
    tournament_id: str,
    run_id: str,
    by_id,
    quote_map: dict[tuple[str, str], tuple[float | None, datetime | None]],
    timestamp: datetime,
) -> ShadowAdvise:
    row = by_id.get(act.player_id)
    hp = None
    if row is not None:
        horizon = _H.get(act.bet_type)
        if horizon is not None:
            hp = row.probabilities.p(horizon)
    posted, odds_as_of = quote_map.get((act.player_id, act.bet_type.value), (None, None))
    if posted is None and row is not None:
        posted = row.posted_odds_by_bet.get(act.bet_type.value)
    return ShadowAdvise(
        timestamp=timestamp,
        tournament=tournament_name,
        tournament_id=tournament_id,
        player=act.player_name or (row.name if row else act.player_id),
        player_id=act.player_id,
        market=act.bet_type.value,
        posted_decimal=posted,
        model_probability=hp.central if hp else None,
        model_p_low=hp.low if hp else None,
        model_p_high=hp.high if hp else None,
        suggested_stake=float(act.suggested_stake_delta or act.suggested_unit or 0.0),
        mode=rec.mode.value if isinstance(rec.mode, StrategyMode) else str(rec.mode),
        run_mode=rec.run_mode.value,
        reason=act.reason,
        odds_as_of=odds_as_of,
        run_id=run_id,
        recommendation_id=rec.recommendation_id,
        action_kind=act.kind.value,
        never_auto_bet=True,
        paper_observation_only=True,
    )
