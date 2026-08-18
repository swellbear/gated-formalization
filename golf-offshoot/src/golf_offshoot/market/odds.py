"""Market-relative layer: implied probability, overround, edge, movement."""

from __future__ import annotations

from golf_offshoot.models.enums import BetType, horizon_for
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


def is_current_quote(q: MarketQuote) -> bool:
    return str(getattr(q, "line_role", "current") or "current") != "opening"


# Coherent Yes-ask sums: Win~1, T5~5, T10~10, T20~20, lead-after-N~1.
# Caps are ~2x that. Win allows more because live outrights already run ~2.5.
# A Gamma place/round-leader book summing to 16-40 is not a ticketable coupon.
YES_ASK_SUM_CAP: dict[BetType, float] = {
    BetType.WIN: 4.0,
    BetType.TOP_5: 12.0,
    BetType.TOP_10: 18.0,
    BetType.TOP_20: 32.0,
    BetType.MAKE_CUT: 90.0,
    BetType.WIN_AFTER_R1: 3.0,
    BetType.WIN_AFTER_R2: 3.0,
    BetType.WIN_AFTER_R3: 3.0,
}


def yes_ask_sum(decimals: list[float | None]) -> float:
    total = 0.0
    for d in decimals:
        if d is not None and d > 1.0:
            total += 1.0 / float(d)
    return total


def yes_book_is_ticketable(bet: BetType, ask_sum: float) -> bool:
    """False when the Yes book is too juiced to treat as that market."""
    if ask_sum <= 0:
        return False
    cap = YES_ASK_SUM_CAP.get(bet)
    if cap is None:
        return True
    return ask_sum <= cap


def remove_overround(quotes: list[MarketQuote], bet_type: BetType) -> tuple[list[MarketQuote], float]:
    """Proportional de-juice.

    implied_fair_i = implied_raw_i / Σ_j implied_raw_j

    This forces the book to a probability simplex. It does **not** create a
    price. Betting +EV still requires model_p > 1/decimal (the posted number).
    Live golf winner coupons often carry a large overround; fair probs then
    shrink longshots a lot — do not treat fair-minus-model as a ticket.
    """
    filled = [fill_quote(q) for q in quotes if q.bet_type == bet_type and is_current_quote(q)]
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
    current = [q for q in filled if is_current_quote(q)]
    opening = [q for q in filled if not is_current_quote(q)]
    overround: dict[str, float] = {}
    fair_all: list[MarketQuote] = []
    for bt in BetType:
        fair, tot = remove_overround(current, bt)
        if tot:
            overround[bt.value] = tot
            ids = {q.player_id for q in fair}
            fair_all.extend(fair)
            fair_all.extend([q for q in current if q.bet_type == bt and q.player_id not in ids])
        else:
            fair_all.extend([q for q in current if q.bet_type == bt])
    movement: dict[str, float] = {}
    open_map = {(q.player_id, q.bet_type.value): q.implied_raw for q in opening if q.implied_raw}
    if previous:
        for q in previous.quotes:
            if not is_current_quote(q):
                continue
            key = (q.player_id, q.bet_type.value)
            open_map.setdefault(key, q.implied_fair or q.implied_raw)
    for q in fair_all:
        key = (q.player_id, q.bet_type.value)
        old = open_map.get(key)
        new = q.implied_raw
        if old is not None and new is not None:
            movement[f"{q.player_id}:{q.bet_type.value}"] = float(new - old)
    return MarketSnapshot(
        tournament_id=tournament_id,
        quotes=opening + fair_all,
        overround=overround,
        movement_vs_open=movement,
    )


def edges_for_player(
    bundle: ProbabilityBundle,
    market: MarketSnapshot,
) -> tuple[dict[str, float], dict[str, float], dict[str, float], dict[str, float]]:
    """Return (edge_vs_fair, implied_fair, posted_decimal, yes_bid).

    Display edge is model − de-juiced market. Actionable +EV is model vs posted
    1/decimal, enforced in the decision layer. Yes bid is the sell side when a
    book posts one (Polymarket bestBid); never synthesized from the ask.
    """
    edge: dict[str, float] = {}
    implied: dict[str, float] = {}
    posted: dict[str, float] = {}
    bids: dict[str, float] = {}
    for q in market.quotes:
        if q.player_id != bundle.player_id:
            continue
        if not is_current_quote(q):
            continue
        h = horizon_for(q.bet_type)
        if h is None or h not in bundle.horizons:
            continue
        mkt = q.implied_fair if q.implied_fair is not None else q.implied_raw
        if mkt is None:
            continue
        model_p = bundle.p(h).central
        implied[q.bet_type.value] = float(mkt)
        edge[q.bet_type.value] = float(model_p - mkt)
        if q.decimal_odds and q.decimal_odds > 1.0:
            posted[q.bet_type.value] = float(q.decimal_odds)
        if q.bid_raw is not None and 0.0 < float(q.bid_raw) < 1.0:
            bids[q.bet_type.value] = float(q.bid_raw)
    return edge, implied, posted, bids
