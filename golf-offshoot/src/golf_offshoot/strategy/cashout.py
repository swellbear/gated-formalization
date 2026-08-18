"""User-typed sportsbook cash-out vs remaining winner EV.

Not scraped. Optional. Never auto-bets. A missing quote leaves MTM as the
odds-ratio proxy. Applied paper sells without a typed quote may book an
estimated offer (odds-ratio MTM with a haircut) — still not Open Bets.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from golf_offshoot.config import (
    PAPER_ESTIMATED_CASHOUT_HAIRCUT,
    STRATEGY_CASHOUT_BUFFER_FRAC,
)
from golf_offshoot.data_feeds.names import last_first, match_name, normalize_name
from golf_offshoot.models.enums import StrategyMode
from golf_offshoot.models.strategy import StrategyPosition

_PAIR = re.compile(
    r"^\s*(.+?)\s*[=:]\s*\$?\s*([0-9]+(?:\.[0-9]+)?)\s*$",
    re.IGNORECASE,
)


def estimated_cashout_ledger_token(movement_id: str) -> str:
    return f"estimated-cashout:{movement_id}"


def typed_cashout_ledger_token(movement_id: str) -> str:
    return f"movement:{movement_id}"


def bid_cashout_dollars(shares: float | None, bid: float | None) -> float | None:
    """shares × Yes bid. None if either side is missing. Not a CLOB fill."""
    try:
        n = float(shares) if shares is not None else 0.0
        p = float(bid) if bid is not None else 0.0
    except (TypeError, ValueError):
        return None
    if n <= 0 or p <= 0.0 or p >= 1.0:
        return None
    return round(n * p, 2)


def min_sell_price(threshold: float | None, shares: float | None) -> float | None:
    """Sell-bar dollars / shares. The bid to beat, not an order."""
    try:
        bar = float(threshold) if threshold is not None else 0.0
        n = float(shares) if shares is not None else 0.0
    except (TypeError, ValueError):
        return None
    if bar <= 0 or n <= 0:
        return None
    return round(bar / n, 4)


def estimated_cashout_offer(
    sold_stake: float,
    entry_odds: float | None,
    live_odds: float | None,
    *,
    haircut: float | None = None,
) -> float | None:
    """Odds-ratio MTM on the sold slice, then keep (1 - haircut) of the gap.

    Not a scraped Open Bets quote. Returns None when live posted odds are
    missing or invalid so the caller can stay at cost.
    """
    sold = round(float(sold_stake), 2)
    if sold <= 0:
        return None
    try:
        entry = float(entry_odds) if entry_odds is not None else 0.0
        live = float(live_odds) if live_odds is not None else 0.0
    except (TypeError, ValueError):
        return None
    if entry <= 1.0 or live <= 1.0:
        return None
    h = PAPER_ESTIMATED_CASHOUT_HAIRCUT if haircut is None else float(haircut)
    h = min(1.0, max(0.0, h))
    mtm = sold * (entry / live)
    offered = sold + (1.0 - h) * (mtm - sold)
    return round(max(0.0, offered), 2)


@dataclass(frozen=True)
class CashoutCompare:
    quote: float
    stake: float
    full_payout: float
    hold_central: float
    hold_low: float
    hold_high: float
    threshold: float
    beats_hold: bool
    notes: tuple[str, ...]


def parse_cashout_cli(raw: list[str] | str | None) -> tuple[list[tuple[str, float]], list[str]]:
    """Parse --cash-out strings. Returns (name_or_id, dollars) pairs plus warnings."""
    chunks: list[str] = []
    if raw is None:
        return [], []
    if isinstance(raw, str):
        chunks = [raw]
    else:
        chunks = [str(x) for x in raw if str(x).strip()]
    pairs: list[tuple[str, float]] = []
    warnings: list[str] = []
    for chunk in chunks:
        for part in re.split(r"[;,]", chunk):
            text = part.strip()
            if not text:
                continue
            m = _PAIR.match(text)
            if not m:
                warnings.append(f"ignored cash-out fragment {text!r} (want Name=12.40)")
                continue
            label = m.group(1).strip()
            amount = float(m.group(2))
            if amount <= 0:
                warnings.append(f"ignored cash-out {label!r}: amount must be > 0")
                continue
            pairs.append((label, round(amount, 2)))
    return pairs, warnings


def bind_cashout_quotes(
    pairs: list[tuple[str, float]],
    positions: list[StrategyPosition],
) -> tuple[dict[str, float], list[str]]:
    """Map typed labels onto open tickets. Unmatched labels are warnings, not invented fills."""
    bound: dict[str, float] = {}
    warnings: list[str] = []
    if not pairs:
        return bound, warnings
    if not positions:
        warnings.append("cash-out quotes ignored: no open tickets to attach them to")
        return bound, warnings

    by_id = {p.player_id: p for p in positions}
    name_to_id = {normalize_name(p.player_name): p.player_id for p in positions if p.player_name}
    last_hits: dict[str, list[str]] = {}
    for p in positions:
        last, _ = last_first(p.player_name or p.player_id)
        if last:
            last_hits.setdefault(last, []).append(p.player_id)

    for label, amount in pairs:
        pid: str | None = None
        key = label.strip()
        if key in by_id:
            pid = key
        else:
            pid = match_name(key, name_to_id)
        if pid is None:
            last, _ = last_first(key)
            hits = last_hits.get(last) or []
            if len(hits) == 1:
                pid = hits[0]
        if pid is None:
            warnings.append(f"cash-out {label!r} ${amount:.2f} did not match an open ticket")
            continue
        if pid in bound and abs(bound[pid] - amount) > 0.009:
            warnings.append(
                f"cash-out for {by_id[pid].player_name or pid} replaced "
                f"${bound[pid]:.2f} with ${amount:.2f}"
            )
        bound[pid] = amount
    return bound, warnings


def compare_cashout(
    *,
    stake: float,
    decimal_odds: float,
    live_model_p: float,
    live_model_low: float,
    live_model_high: float,
    quote: float,
    mode: StrategyMode = StrategyMode.STAY_SELECTIVE,
) -> CashoutCompare:
    """Certain cash-out dollars vs expected full winner payout if you hold."""
    stake_f = max(0.0, float(stake))
    odds = max(1.0, float(decimal_odds))
    p = min(1.0, max(0.0, float(live_model_p)))
    lo = min(1.0, max(0.0, float(live_model_low)))
    hi = min(1.0, max(0.0, float(live_model_high)))
    if hi < p:
        hi = p
    if lo > p:
        lo = p
    full = stake_f * odds
    hold_c = p * full
    hold_lo = lo * full
    hold_hi = hi * full
    buf = STRATEGY_CASHOUT_BUFFER_FRAC
    if mode == StrategyMode.PROTECT_PROFITS:
        bar = hold_c
    elif mode == StrategyMode.PRESS_EDGES:
        bar = max(hold_hi * (1.0 + buf), hold_c * (1.0 + 1.5 * buf))
    else:
        bar = max(hold_c * (1.0 + buf), hold_hi)
    bar = min(bar, full)
    q = round(float(quote), 2)
    notes = [
        f"quoted cash-out ${q:.2f}",
        f"hold EV payout ${hold_c:.2f} (Win {p:.1%} x ${stake_f:.2f} x {odds:.2f})",
        f"Win interval payout ${hold_lo:.2f}-${hold_hi:.2f}",
        f"sell bar ${bar:.2f}",
    ]
    if q > full + 0.009:
        notes.append(
            f"quote exceeds max win payout ${full:.2f}; check the number you typed"
        )
    beats = q + 1e-9 >= bar
    return CashoutCompare(
        quote=q,
        stake=stake_f,
        full_payout=full,
        hold_central=hold_c,
        hold_low=hold_lo,
        hold_high=hold_hi,
        threshold=bar,
        beats_hold=beats,
        notes=tuple(notes),
    )
