"""Market-relative layer: implied probability, overround, edge, movement."""

from __future__ import annotations

from golf_offshoot.models.enums import BetType, Horizon
from golf_offshoot.models.schemas import MarketQuote, MarketSnapshot, ProbabilityBundle


def american_to_decimal(american: int) -> float:
    if american > 0:
        return 1.0 + american / 100.0
    if american < 0:
        return 1.0 + 100.0 / abs(american)
    raise ValueError("american odds cannot be 0")


def decimal_to_implied(decimal_odds: float) -> float:
    if decimal_odds <= 1.0:
        raise ValueError("decimal odds must be > 1")
    return 1.0 / decimal_odds


def fill_quote(q: MarketQuote) -> MarketQuote:
    dec = q.decimal_odds
    if dec is None and q.american_odds is not None:
        dec = american_to_decimal(q.american_odds)
    implied = q.implied_raw
    if implied is None and dec is not None:
        implied = decimal_to_implied(dec)
    return q.model_copy(update={"decimal_odds": dec, "implied_raw": implied})


def remove_overround(quotes: list[MarketQuote], bet_type: BetType) -> tuple[list[MarketQuote], float]:
    filled = [fill_quote(q) for q in quotes if q.bet_type == bet_type]
    subset = [q for q in filled if q.implied_raw]
    total = sum(q.implied_raw or 0.0 for q in subset)
    if total <= 0:
        return subset, 0.0
    fair = []
    for q in subset:
        fair.append(q.model_copy(update={"implied_fair": (q.implied_raw or 0.0) / total}))
    return fair, total


def build_market_snapshot(
    tournament_id: str,
    quotes: list[MarketQuote],
    previous: MarketSnapshot | None = None,
) -> MarketSnapshot:
    filled = [fill_quote(q) for q in quotes]
    overround: dict[str, float] = {}
    fair_all: list[MarketQuote] = []
    for bt in BetType:
        fair, tot = remove_overround(filled, bt)
        if tot:
            overround[bt.value] = tot
            # replace matching
            ids = {q.player_id for q in fair}
            fair_all.extend(fair)
            fair_all.extend([q for q in filled if q.bet_type == bt and q.player_id not in ids])
        else:
            fair_all.extend([q for q in filled if q.bet_type == bt])
    movement: dict[str, float] = {}
    if previous:
        prev_map = {(q.player_id, q.bet_type.value): q.implied_fair or q.implied_raw for q in previous.quotes}
        for q in fair_all:
            key = (q.player_id, q.bet_type.value)
            old = prev_map.get(key)
            new = q.implied_fair or q.implied_raw
            if old is not None and new is not None:
                movement[f"{q.player_id}:{q.bet_type.value}"] = float(new - old)
    return MarketSnapshot(
        tournament_id=tournament_id,
        quotes=fair_all,
        overround=overround,
        movement_vs_open=movement,
    )


_BT_TO_H = {
    BetType.WIN: Horizon.WIN,
    BetType.TOP_5: Horizon.TOP_5,
    BetType.TOP_10: Horizon.TOP_10,
    BetType.TOP_20: Horizon.TOP_20,
    BetType.MAKE_CUT: Horizon.MAKE_CUT,
}


def edges_for_player(
    bundle: ProbabilityBundle,
    market: MarketSnapshot,
) -> tuple[dict[str, float], dict[str, float]]:
    """model_p - fair implied. Positive = model longer than market (model likes more)."""
    edge: dict[str, float] = {}
    implied: dict[str, float] = {}
    for q in market.quotes:
        if q.player_id != bundle.player_id:
            continue
        h = _BT_TO_H.get(q.bet_type)
        if h is None:
            continue
        mkt = q.implied_fair if q.implied_fair is not None else q.implied_raw
        if mkt is None:
            continue
        model_p = bundle.p(h).central
        implied[q.bet_type.value] = float(mkt)
        edge[q.bet_type.value] = float(model_p - mkt)
    return edge, implied
