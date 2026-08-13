"""Correlation / concentration of an open book."""

from __future__ import annotations

import math

from golf_offshoot.models.enums import BetType, Horizon
from golf_offshoot.models.schemas import FieldSnapshot, PlayerInputs, PlayerOutput
from golf_offshoot.models.strategy import ConcentrationSlice, StrategyPosition


def _style_vec(p: PlayerInputs) -> tuple[float, float, float, float]:
    sg = p.sg
    return (sg.ott, sg.app, sg.arg, sg.putt)


def _cosine(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    da = math.sqrt(sum(x * x for x in a))
    db = math.sqrt(sum(x * x for x in b))
    if da < 1e-9 or db < 1e-9:
        return 0.0
    return sum(x * y for x, y in zip(a, b)) / (da * db)


def cut_risk(row: PlayerOutput | None) -> float:
    if row is None:
        return 0.5
    return float(1.0 - row.probabilities.p(Horizon.MAKE_CUT).central)


def concentrations(
    positions: list[StrategyPosition],
    rows: dict[str, PlayerOutput],
    field: FieldSnapshot | None,
) -> list[ConcentrationSlice]:
    if not positions:
        return []
    total = sum(p.stake for p in positions) or 1.0
    by_id = {p.player.player_id: p for p in field.players} if field else {}

    cut_ids = []
    cut_exp = 0.0
    weather_ids = []
    weather_exp = 0.0
    for pos in positions:
        row = rows.get(pos.player_id)
        cr = cut_risk(row)
        if cr >= 0.40 or pos.bet_type == BetType.MAKE_CUT:
            cut_ids.append(pos.player_id)
            cut_exp += pos.stake
        inp = by_id.get(pos.player_id)
        if inp and inp.weather_fit is not None and abs(inp.weather_fit) >= 0.08:
            weather_ids.append(pos.player_id)
            weather_exp += pos.stake

    slices = [
        ConcentrationSlice(
            axis="cut_risk",
            label="cut-risk / make-cut bets",
            exposure=cut_exp,
            fraction_of_book=cut_exp / total,
            player_ids=sorted(set(cut_ids)),
        ),
        ConcentrationSlice(
            axis="weather",
            label="weather-dependent players",
            exposure=weather_exp,
            fraction_of_book=weather_exp / total,
            player_ids=sorted(set(weather_ids)),
        ),
    ]

    # greedy style clusters
    remaining = list(positions)
    used: set[str] = set()
    best_cluster: list[StrategyPosition] = []
    while remaining:
        seed = remaining[0]
        seed_in = by_id.get(seed.player_id)
        cluster = [seed]
        if seed_in:
            sv = _style_vec(seed_in)
            for other in remaining[1:]:
                oin = by_id.get(other.player_id)
                if oin and _cosine(sv, _style_vec(oin)) >= 0.85:
                    cluster.append(other)
        if len(cluster) > len(best_cluster):
            best_cluster = cluster
        remaining = [p for p in remaining if p.position_id not in {c.position_id for c in cluster}]
        used.update(c.position_id for c in cluster)
    if best_cluster:
        exp = sum(p.stake for p in best_cluster)
        slices.append(
            ConcentrationSlice(
                axis="style",
                label="same-style cluster",
                exposure=exp,
                fraction_of_book=exp / total,
                player_ids=[p.player_id for p in best_cluster],
            )
        )

    # talent band via theta
    bands: dict[str, list[StrategyPosition]] = {"hot": [], "mid": [], "long": []}
    for pos in positions:
        row = rows.get(pos.player_id)
        th = row.probabilities.theta_mean if row else 0.0
        key = "hot" if th >= 1.2 else ("long" if th < 0.4 else "mid")
        bands[key].append(pos)
    best_band = max(bands.items(), key=lambda kv: sum(p.stake for p in kv[1]))
    if best_band[1]:
        exp = sum(p.stake for p in best_band[1])
        slices.append(
            ConcentrationSlice(
                axis="talent_band",
                label=f"talent-band {best_band[0]}",
                exposure=exp,
                fraction_of_book=exp / total,
                player_ids=[p.player_id for p in best_band[1]],
            )
        )
    return slices


def would_raise_cut_stack(
    positions: list[StrategyPosition],
    candidate_player: str,
    candidate_stake: float,
    rows: dict[str, PlayerOutput],
    cap: float,
) -> bool:
    total = sum(p.stake for p in positions) + candidate_stake
    if total <= 0:
        return False
    cut_exp = 0.0
    for p in positions:
        if cut_risk(rows.get(p.player_id)) >= 0.40 or p.bet_type == BetType.MAKE_CUT:
            cut_exp += p.stake
    cand = rows.get(candidate_player)
    if cut_risk(cand) >= 0.40:
        cut_exp += candidate_stake
    return (cut_exp / total) > cap
