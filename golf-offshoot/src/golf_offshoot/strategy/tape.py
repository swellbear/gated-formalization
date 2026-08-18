"""Display tape for fills: cost vs bid vs keep-to-win. Not a sell. Not a ticket."""

from __future__ import annotations

from golf_offshoot.models.enums import Horizon, horizon_for
from golf_offshoot.strategy.cashout import bid_cashout_dollars
from golf_offshoot.strategy.paper_book import _position_is_fill


def fill_tape_lines(
    record,
    *,
    ranked: list | None = None,
    moves: list | None = None,
) -> list[str]:
    """One line per fill. Offer vs cost is not a sell. Stay Selective still uses keep-to-win."""
    positions = _open_fills(record)
    if not positions:
        return [
            "  (no fills this pack; observation stubs have no bid tape)",
            "  Display only. Not a ticket. Not a take-profit.",
        ]
    by_id, by_name = _index_rows(ranked)
    by_move = _index_moves(moves)
    lines: list[str] = []
    for pos in positions:
        mark = by_move.get((pos.player_id, pos.bet_type.value)) or by_move.get(
            ("", pos.bet_type.value, (pos.player_name or "").lower())
        )
        row = by_id.get(pos.player_id) or by_name.get(pos.player_name or "")
        cost = _cost(pos)
        shares = float(pos.shares or 0.0)
        offer = _offer(mark, pos, row, shares)
        keep = _keep(mark, pos, row, shares)
        bid = _bid(mark, pos, row)
        min_sell = getattr(mark, "min_sell_price", None) if mark is not None else None
        tag = _pop_tag(cost, offer)
        bits = [
            f"  {pos.player_name or pos.player_id}  {pos.bet_type.value.replace('_', ' ')}",
            f"cost ${cost:.2f}",
        ]
        bits.append(f"offer ${offer:.2f}" if offer is not None else "offer n/a")
        bits.append(f"keep-to-win ${keep:.2f}" if keep is not None else "keep-to-win n/a")
        if bid is not None:
            bits.append(f"bid {bid:.3f}")
        if min_sell is not None:
            bits.append(f"min-sell {float(min_sell):.3f}")
        bits.append(tag)
        lines.append("  ".join(bits))
    lines.append(
        "  Offer vs cost is not a sell. Stay Selective still sells only if bid beats keep-to-win."
    )
    if any((getattr(pos, "intent", "hold") or "hold").lower() == "flip" for pos in positions):
        lines.append(
            "  Flip sleeve sells at fill+20% if still green next live, not keep-to-win."
        )
    return lines


def _open_fills(record) -> list:
    if record is None:
        return []
    inner = getattr(record, "book", None)
    raw = getattr(inner, "positions", None) if inner is not None else getattr(record, "positions", None)
    out = []
    for pos in raw or []:
        if getattr(pos, "proposed", False):
            continue
        if float(getattr(pos, "stake", 0) or 0) <= 0:
            continue
        if _position_is_fill(pos):
            out.append(pos)
    return out


def _index_rows(ranked: list | None) -> tuple[dict, dict]:
    by_id: dict = {}
    by_name: dict = {}
    for row in ranked or []:
        by_id[getattr(row, "player_id", "")] = row
        by_name[getattr(row, "name", "")] = row
    return by_id, by_name


def _index_moves(moves: list | None) -> dict:
    out: dict = {}
    for m in moves or []:
        pid = getattr(m, "player_id", "") or ""
        bet = getattr(m, "bet_type", "win") or "win"
        name = (getattr(m, "player_name", "") or "").lower()
        if pid:
            out[(pid, bet)] = m
        if name:
            out[("", bet, name)] = m
    return out


def _cost(pos) -> float:
    raw = getattr(pos, "cost_usd", None)
    if raw is not None and float(raw) > 0:
        return round(float(raw), 2)
    return round(float(pos.stake), 2)


def _bid(mark, pos, row) -> float | None:
    if mark is not None:
        b = getattr(mark, "live_bid", None)
        if b is not None and 0.0 < float(b) < 1.0:
            return float(b)
    if row is None:
        return None
    key = pos.bet_type.value
    raw = (getattr(row, "bid_by_bet", None) or {}).get(key)
    try:
        b = float(raw) if raw is not None else None
    except (TypeError, ValueError):
        return None
    if b is None or b <= 0.0 or b >= 1.0:
        return None
    return b


def _offer(mark, pos, row, shares: float) -> float | None:
    if mark is not None:
        q = getattr(mark, "cashout_quote", None)
        if q is not None and float(q) > 0:
            return round(float(q), 2)
    bid = _bid(mark, pos, row)
    return bid_cashout_dollars(shares if shares > 0 else None, bid)


def _keep(mark, pos, row, shares: float) -> float | None:
    if mark is not None:
        k = getattr(mark, "hold_expected_payout", None)
        if k is not None and float(k) > 0:
            return round(float(k), 2)
    if row is None:
        return None
    h = horizon_for(pos.bet_type)
    hp = row.probabilities.horizons.get(h) if h is not None else None
    if hp is None:
        hp = row.probabilities.horizons.get(Horizon.WIN)
    if hp is None:
        return None
    p = float(hp.central)
    if shares > 0:
        return round(shares * p, 2)
    odds = float(pos.decimal_odds or 0.0)
    if odds > 1.0:
        return round(float(pos.stake) * odds * p, 2)
    return None


def _pop_tag(cost: float, offer: float | None) -> str:
    if offer is None:
        return "n/a"
    if offer > cost + 0.005:
        return "pop vs cost (display; not a sell)"
    return "no pop"


def climb_leftover_lines(result) -> list[str]:
    """Fat model Top 10 vs skinny Winner Yes. Display only. Not a ticket."""
    ranked: list[tuple[float, str, float, float, float]] = []
    for row in getattr(result, "ranked", None) or []:
        hp_win = row.probabilities.horizons.get(Horizon.WIN)
        hp_t10 = row.probabilities.horizons.get(Horizon.TOP_10)
        if hp_win is None or hp_t10 is None:
            continue
        win = float(hp_win.central)
        t10 = float(hp_t10.central)
        if win <= 0.0 or t10 < 0.06 or t10 < 4.0 * win:
            continue
        raw = (row.posted_odds_by_bet or {}).get("win")
        try:
            posted = float(raw) if raw is not None else None
        except (TypeError, ValueError):
            posted = None
        if posted is None or posted <= 1.0:
            continue
        yes = 1.0 / posted
        if yes > 0.05:
            continue
        ranked.append((t10 / win, row.name, t10, win, yes))
    if not ranked:
        return [
            "  (none this snapshot; need a skinny Winner Yes and a fat model Top 10)",
            "  Display leftover. Not a ticket. Winner Yes is not a climb / cash-out bet.",
        ]
    ranked.sort(key=lambda t: t[0], reverse=True)
    lines = []
    for ratio, name, t10, win, yes in ranked[:8]:
        lines.append(
            f"  {name}  T10={t10:.3f}  Win={win:.3f}  Yes={yes:.3f}  T10/Win={ratio:.1f}x"
        )
    lines.append(
        "  Display leftover. Not a ticket. Winner Yes is not Top 10, and not a take-profit."
    )
    return lines
