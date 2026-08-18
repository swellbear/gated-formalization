"""Compare-path ids. Lived museum stays `{event}.json`."""

from __future__ import annotations

from enum import Enum

from golf_offshoot.compare.law import METHOD_LAW_V1
from golf_offshoot.models.enums import BetType, RiskPreference, StrategyMode
from golf_offshoot.models.strategy import StrategyConfig


class ComparePath(str, Enum):
    LIVED = "lived"
    A_REPLAY = "a_replay"
    A_CONTROL = "a_control"
    B_GUTS = "b_guts"
    B_NERVES = "b_nerves"
    B_FULL = "b_full"


COMPARE_LEDGERS = (
    ComparePath.A_REPLAY,
    ComparePath.B_GUTS,
    ComparePath.B_NERVES,
    ComparePath.B_FULL,
)

COMPARE_PLACE_BETS = (BetType.TOP_5, BetType.TOP_10, BetType.TOP_20)


def compare_allows_place(event_id: str | None) -> bool:
    """St. Jude stays Winner-only. Later events ticket place when a real coupon exists."""
    if not METHOD_LAW_V1.get("compare_place_when_coupon_exists"):
        return False
    frozen = {str(x) for x in METHOD_LAW_V1.get("winner_only_event_ids") or []}
    return str(event_id or "") not in frozen


def allowed_compare_bets(event_id: str | None) -> list[BetType]:
    if compare_allows_place(event_id):
        names = list(METHOD_LAW_V1.get("compare_place_markets") or ["top_5", "top_10", "top_20"])
        extra: list[BetType] = []
        for name in names:
            try:
                extra.append(BetType(name))
            except ValueError:
                continue
        return [BetType.WIN, *extra]
    return [BetType.WIN]


def allowed_bets_for_quotes(event_id: str | None, quotes) -> list[BetType]:
    """Winner/place from method law, plus any other coupon that actually listed."""
    base = allowed_compare_bets(event_id)
    if not compare_allows_place(event_id):
        return base
    seen = list(base)
    have = set(seen)
    for q in quotes or []:
        bt = getattr(q, "bet_type", None)
        if isinstance(bt, str):
            try:
                bt = BetType(bt)
            except ValueError:
                continue
        if bt is None or bt in have:
            continue
        have.add(bt)
        seen.append(bt)
    return seen


def allowed_bets_from_rows(event_id: str | None, rows) -> list[BetType]:
    """Same as allowed_bets_for_quotes, reading posted coupons off ranked rows."""
    class _Q:
        def __init__(self, bet_type: BetType) -> None:
            self.bet_type = bet_type

    quotes = []
    for row in rows or []:
        for key in getattr(row, "posted_odds_by_bet", {}) or {}:
            try:
                quotes.append(_Q(BetType(key)))
            except ValueError:
                continue
    return allowed_bets_for_quotes(event_id, quotes)


def experiment_config(
    *,
    ticket_screen: str,
    bankroll: float | None = None,
    event_id: str | None = None,
) -> StrategyConfig:
    return StrategyConfig(
        enabled=True,
        mode=StrategyMode.STAY_SELECTIVE,
        risk=RiskPreference.CONSERVATIVE,
        bankroll=float(bankroll if bankroll is not None else METHOD_LAW_V1["independent_compare_bankroll"]),
        ticket_screen=ticket_screen,
        never_auto_bet=True,
        allowed_bet_types=allowed_compare_bets(event_id),
    )


def ledger_id(path: ComparePath) -> str:
    """A-control shares the A-replay ledger so the control stays one book."""
    if path == ComparePath.A_CONTROL:
        return ComparePath.A_REPLAY.value
    return path.value


def config_for(
    path: ComparePath,
    *,
    bankroll: float | None = None,
    event_id: str | None = None,
) -> StrategyConfig:
    if path in (ComparePath.B_NERVES, ComparePath.B_FULL):
        return experiment_config(ticket_screen="posted", bankroll=bankroll, event_id=event_id)
    if path in (ComparePath.A_REPLAY, ComparePath.A_CONTROL, ComparePath.B_GUTS):
        return experiment_config(ticket_screen="edgew", bankroll=bankroll, event_id=event_id)
    return experiment_config(ticket_screen="both", bankroll=bankroll, event_id=event_id)


def uses_honest_theta(path: ComparePath) -> bool:
    return path in (ComparePath.B_GUTS, ComparePath.B_FULL)


def posted_bar(path: ComparePath) -> bool:
    return path in (ComparePath.B_NERVES, ComparePath.B_FULL)


def compare_markets_blurb(event_id: str | None) -> str:
    if compare_allows_place(event_id):
        return "Winner plus Top 5/10/20 when a real coupon exists (never from Winner odds)"
    return "Winner-only (St. Jude freeze)"
