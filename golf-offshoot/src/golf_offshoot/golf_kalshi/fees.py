"""After-fee golf edge. Cites the same Founder PDF pin as 15m. Never assume multiplier ×1."""

from __future__ import annotations

from typing import Any

from golf_offshoot.learning_lane_15m.evidence_bar import fee_adjust, fee_for_fill, fee_k

FEE_PIN_SOURCE = "founder_browser_bytes"
FEE_SCHEDULE_FILE = "golf-offshoot/docs/kalshi-fee-schedule.pdf"
FEE_SCHEDULE_SHA256 = "c326a69f596a11e8f8be2620402d39a8d4823920c21cc97c93a114d862699601"
FEE_SCHEDULE_BYTES = 281129
FEE_ADJUST_PATH = "golf_offshoot.learning_lane_15m.evidence_bar.fee_adjust"


def series_k(fee_multiplier: float | None) -> float | None:
    """Effective k. Missing multiplier is not ×1 — caller must skip."""
    if fee_multiplier is None:
        return None
    try:
        mult = float(fee_multiplier)
    except (TypeError, ValueError):
        return None
    if mult <= 0:
        return None
    return float(fee_k()) * mult


def taker_fee(yes_ask: float, stake: float, *, fee_multiplier: float | None) -> float | None:
    k = series_k(fee_multiplier)
    if k is None:
        return None
    return fee_for_fill(float(yes_ask), float(stake), k=k)


def edge_after_fee(
    model_p: float,
    yes_ask: float,
    stake: float,
    *,
    fee_multiplier: float | None,
) -> float | None:
    """model_p vs yes ask after entry fee. Skip if fee cannot be seen."""
    fee = taker_fee(yes_ask, stake, fee_multiplier=fee_multiplier)
    if fee is None:
        return None
    # Gross expected pnl on a YES taker: model_p * (stake/yes_ask) - stake, then minus fee.
    if yes_ask <= 0 or yes_ask >= 1:
        return None
    payout = stake / float(yes_ask)
    recorded = model_p * payout - stake
    return fee_adjust(recorded, yes_ask, stake, k=series_k(fee_multiplier))


def kelly_stake(bank: float, model_p: float, yes_ask: float, *, fraction: float) -> float:
    """0.25 Kelly as a dollar unit. Caps applied by the caller."""
    from golf_offshoot.decision.layer import fractional_kelly

    if yes_ask <= 0 or yes_ask >= 1 or bank <= 0:
        return 0.0
    frac = fractional_kelly(float(model_p), 1.0 / float(yes_ask), fraction=float(fraction))
    return max(0.0, float(frac) * float(bank))


def sell_contracts(stake: float, entry_ask: float) -> float | None:
    if entry_ask is None:
        return None
    try:
        ask = float(entry_ask)
    except (TypeError, ValueError):
        return None
    if ask <= 0:
        return None
    return float(stake) / ask


def sell_proceeds(stake: float, entry_ask: float, yes_bid: float) -> float | None:
    contracts = sell_contracts(stake, entry_ask)
    if contracts is None:
        return None
    try:
        bid = float(yes_bid)
    except (TypeError, ValueError):
        return None
    if bid <= 0 or bid >= 1:
        return None
    return contracts * bid


def bid_covers_position(ticket: dict[str, Any], market: dict[str, Any]) -> bool:
    bid = market.get("yes_bid")
    try:
        bid_f = float(bid) if bid is not None else None
    except (TypeError, ValueError):
        bid_f = None
    if bid_f is None or bid_f <= 0:
        return False
    entry = ticket.get("yes_ask") or (ticket.get("quote") or {}).get("yes_ask")
    contracts = sell_contracts(float(ticket.get("stake") or 0), float(entry or 0))
    if contracts is None:
        return False
    displayed = market.get("displayed_size")
    if displayed is None:
        displayed = (ticket.get("quote") or {}).get("displayed_size")
    if displayed is not None:
        try:
            if float(displayed) + 1e-9 < contracts:
                return False
        except (TypeError, ValueError):
            return False
    return True


def paper_exit_pnl(
    ticket: dict[str, Any],
    *,
    yes_bid: float,
    fee_multiplier: float | None,
) -> tuple[float, float, float] | None:
    """(recorded, pnl_after_fee, exit_fee) or None if fee cannot be seen."""
    entry = float(ticket.get("yes_ask") or (ticket.get("quote") or {}).get("yes_ask") or 0)
    stake = float(ticket.get("stake") or 0)
    proceeds = sell_proceeds(stake, entry, yes_bid)
    if proceeds is None:
        return None
    recorded = proceeds - stake
    k = series_k(fee_multiplier)
    if k is None:
        return None
    fee = taker_fee(yes_bid, stake, fee_multiplier=fee_multiplier)
    if fee is None:
        return None
    pnl = fee_adjust(recorded, float(yes_bid), stake, k=k)
    return round(float(recorded), 4), round(float(pnl), 4), round(float(fee), 4)


def quote_snapshot(market: dict[str, Any], *, stake: float, fee: float | None, declared_at: str) -> dict[str, Any]:
    return {
        "yes_ask": market.get("yes_ask"),
        "yes_bid": market.get("yes_bid"),
        "displayed_size": market.get("displayed_size"),
        "spread": market.get("spread"),
        "fee": fee,
        "fee_multiplier": market.get("fee_multiplier"),
        "declared_at": declared_at,
    }
