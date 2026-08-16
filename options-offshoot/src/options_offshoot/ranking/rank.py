"""Liquidity + vs-ask ranking. Sort key is vs_ask, never P(ITM)."""

from __future__ import annotations

from options_offshoot.compare.law import METHOD_LAW_V1
from options_offshoot.config import (
    MAX_RANGE_WIDTH,
    MAX_SPREAD_REL,
    MIN_EDGE_TO_CONSIDER,
    MIN_OPEN_INTEREST,
    MIN_RELIABILITY,
    MIN_VOLUME,
)
from options_offshoot.models.enums import TicketScreen
from options_offshoot.models.schemas import Contract, ModelView, RankedContract
from options_offshoot.pricing.simulate import simulate_view, years_to_expiry


def mark_liquid(contract: Contract) -> Contract:
    q = contract.quote
    reason_n_a = None
    if not q.has_real_ask:
        contract.liquid = False
        contract.notes = "no real ask"
        return contract
    oi = q.open_interest or 0
    vol = q.volume or 0
    if oi < MIN_OPEN_INTEREST and vol < max(MIN_VOLUME, 1):
        contract.liquid = False
        contract.notes = "below size floor"
        return contract
    spr = q.spread_rel
    if spr is None or spr > MAX_SPREAD_REL:
        contract.liquid = False
        contract.notes = "spread too wide"
        return contract
    if q.bid is None or q.bid <= 0:
        # ask without bid: still not a two-sided market we will treat as available
        contract.liquid = False
        contract.notes = "no real bid"
        return contract
    contract.liquid = True
    _ = reason_n_a
    return contract


def rank_contract(
    contract: Contract,
    *,
    honest: bool,
    t: float | None = None,
    today=None,
) -> RankedContract:
    mark_liquid(contract)
    if contract.years_to_expiry is None and today is not None:
        contract.years_to_expiry = years_to_expiry(contract.expiry, today)
    model = simulate_view(contract, honest=honest, today=today)
    bar = float(t if t is not None else METHOD_LAW_V1["starting_t"])
    n_a = None
    vs_ask = None
    vs_mid = None
    if not contract.liquid:
        n_a = contract.notes or "n/a"
    elif model.fair is None:
        n_a = "model unconstrained"
    else:
        if contract.quote.ask is not None:
            vs_ask = float(model.fair) - float(contract.quote.ask)
        else:
            n_a = "no real ask"
        mid = contract.quote.mid
        if mid is not None:
            vs_mid = float(model.fair) - float(mid)
        width = None
        if model.p_itm_low is not None and model.p_itm_high is not None:
            width = model.p_itm_high - model.p_itm_low
        if width is not None and width > MAX_RANGE_WIDTH:
            n_a = n_a or "range too wide"
        if model.reliability < MIN_RELIABILITY:
            n_a = n_a or "low reliability"
    clears_ask = vs_ask is not None and vs_ask >= bar and n_a is None
    clears_mid = vs_mid is not None and vs_mid >= bar and n_a is None
    if n_a is None and not contract.liquid:
        n_a = "n/a"
    return RankedContract(
        contract=contract,
        model=model,
        vs_ask=vs_ask,
        vs_mid=vs_mid,
        clears_ask=bool(clears_ask),
        clears_mid=bool(clears_mid),
        n_a_reason=n_a,
    )


def sort_rows(rows: list[RankedContract]) -> list[RankedContract]:
    """Law: sort_key is vs_ask. P(ITM) must not win."""
    assert METHOD_LAW_V1["sort_key"] == "vs_ask"
    return sorted(
        rows,
        key=lambda r: (
            r.vs_ask is None,
            -(r.vs_ask if r.vs_ask is not None else 0.0),
            r.contract.underlying,
            r.contract.strike,
        ),
    )


def clears_screen(row: RankedContract, screen: TicketScreen | str) -> bool:
    name = str(getattr(screen, "value", screen))
    if row.n_a_reason:
        return False
    if name == "ask":
        return row.clears_ask
    if name == "mid":
        return row.clears_mid
    if name == "both":
        return row.clears_ask and row.clears_mid
    return False
