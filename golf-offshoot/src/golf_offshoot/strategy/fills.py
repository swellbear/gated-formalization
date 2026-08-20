"""Record a real Polymarket fill on the independent paper path. Never CLOB. Never ledger.json."""

from __future__ import annotations

from dataclasses import dataclass

from golf_offshoot.compare.law import METHOD_LAW_V1
from golf_offshoot.data_feeds.field_fallback import is_provisional_player_id, provisional_player_id
from golf_offshoot.data_feeds.names import match_name, normalize_name
from golf_offshoot.data_feeds.polymarket import POLYMARKET_PATH_ID
from golf_offshoot.models.enums import BetType
from golf_offshoot.models.strategy import PortfolioState, StrategyPosition, new_id
from golf_offshoot.strategy.paper_book import (
    PaperBookFile,
    PaperMovement,
    load_paper_file,
    save_paper_book,
)

_PULL_FILL_KINDS = frozenset({"new_bet", "lock", "add"})
_PULL_SELL_KINDS = frozenset({"exit", "reduce"})

_MARKET_ALIASES = {
    "win": BetType.WIN,
    "winner": BetType.WIN,
    "outright": BetType.WIN,
    "top5": BetType.TOP_5,
    "top_5": BetType.TOP_5,
    "top 5": BetType.TOP_5,
    "top10": BetType.TOP_10,
    "top_10": BetType.TOP_10,
    "top 10": BetType.TOP_10,
    "top20": BetType.TOP_20,
    "top_20": BetType.TOP_20,
    "top 20": BetType.TOP_20,
    "cut": BetType.MAKE_CUT,
    "make_cut": BetType.MAKE_CUT,
    "make cut": BetType.MAKE_CUT,
    "win_after_r1": BetType.WIN_AFTER_R1,
    "win after r1": BetType.WIN_AFTER_R1,
    "win after round 1": BetType.WIN_AFTER_R1,
    "after round 1": BetType.WIN_AFTER_R1,
    "round 1": BetType.WIN_AFTER_R1,
    "r1": BetType.WIN_AFTER_R1,
    "win_after_r2": BetType.WIN_AFTER_R2,
    "win after r2": BetType.WIN_AFTER_R2,
    "win after round 2": BetType.WIN_AFTER_R2,
    "after round 2": BetType.WIN_AFTER_R2,
    "round 2": BetType.WIN_AFTER_R2,
    "r2": BetType.WIN_AFTER_R2,
    "win_after_r3": BetType.WIN_AFTER_R3,
    "win after r3": BetType.WIN_AFTER_R3,
    "win after round 3": BetType.WIN_AFTER_R3,
    "after round 3": BetType.WIN_AFTER_R3,
    "round 3": BetType.WIN_AFTER_R3,
    "r3": BetType.WIN_AFTER_R3,
}


class FillError(ValueError):
    """Bad fill input. Nothing was written."""


def parse_fill_market(raw: str) -> BetType:
    key = (raw or "win").strip().lower().replace("-", "_")
    key = " ".join(key.split())
    compact = key.replace(" ", "_")
    bet = _MARKET_ALIASES.get(key) or _MARKET_ALIASES.get(compact)
    if bet is None:
        raise FillError(
            f"unknown market {raw!r}; use win / top_5 / top_10 / top_20 / make_cut "
            "/ win_after_r1 / win_after_r2 / win_after_r3"
        )
    return bet


@dataclass(frozen=True)
class FillPull:
    """Last ntfy ADD / NEW that a typed fill should attach to."""

    kind: str
    player_id: str = ""
    player_name: str = ""
    bet_type: str = "win"
    intent: str = "hold"
    model_win: float | None = None
    edge_w: float | None = None
    posted_edge: float | None = None
    decimal_odds: float | None = None


def ranked_names_map(ranked_names) -> dict[str, str]:
    """normalized name -> player id. Accepts a dict or ranked PlayerOutput rows."""
    out: dict[str, str] = {}
    if not ranked_names:
        return out
    if isinstance(ranked_names, dict):
        items = ranked_names.items()
    else:
        items = []
        for row in ranked_names:
            items.append((getattr(row, "name", None), getattr(row, "player_id", None)))
    for name, pid in items:
        if name and pid:
            out[normalize_name(str(name))] = str(pid)
    return out


def parse_fill_pulls(raw) -> list[FillPull]:
    out: list[FillPull] = []
    for item in raw or []:
        if isinstance(item, FillPull):
            out.append(item)
            continue
        if isinstance(item, dict):
            kind = str(item.get("kind") or "")
            name = str(item.get("player_name") or "")
            bet = str(item.get("bet_type") or "win")
            pid = str(item.get("player_id") or "")
            intent = str(item.get("intent") or "hold")
            out.append(
                FillPull(
                    kind=kind,
                    player_id=pid,
                    player_name=name,
                    bet_type=bet,
                    intent=intent,
                    model_win=_opt_float(item.get("model_win")),
                    edge_w=_opt_float(item.get("edge_w")),
                    posted_edge=_opt_float(item.get("posted_edge")),
                    decimal_odds=_opt_float(item.get("decimal_odds")),
                )
            )
            continue
        kind = str(getattr(item, "kind", "") or "")
        out.append(
            FillPull(
                kind=kind,
                player_id=str(getattr(item, "player_id", "") or ""),
                player_name=str(getattr(item, "player_name", "") or ""),
                bet_type=str(getattr(item, "bet_type", "win") or "win"),
                intent=str(getattr(item, "intent", "hold") or "hold"),
                model_win=_opt_float(getattr(item, "model_win", None)),
                edge_w=_opt_float(getattr(item, "edge_w", None)),
                posted_edge=_opt_float(getattr(item, "posted_edge", None)),
                decimal_odds=_opt_float(getattr(item, "decimal_odds", None)),
            )
        )
    return out


def pulls_from_advice(movements) -> list[FillPull]:
    return parse_fill_pulls(movements)


def match_fill_pull(name: str, bet: BetType, pulls: list[FillPull]) -> FillPull | None:
    """Prefer ADD on this name+market over NEW/lock from the same ping."""
    want = normalize_name(name)
    market = bet.value
    hits = [
        p
        for p in pulls
        if p.kind in _PULL_FILL_KINDS
        and normalize_name(p.player_name) == want
        and str(p.bet_type or "win").replace("-", "_") == market
    ]
    adds = [p for p in hits if p.kind == "add"]
    if adds:
        return adds[-1]
    return hits[-1] if hits else None


def match_sell_pull(name: str, bet: BetType, pulls: list[FillPull]) -> FillPull | None:
    """Last ntfy SELL / PARTIAL SELL on this name+market."""
    want = normalize_name(name)
    market = bet.value
    hits = [
        p
        for p in pulls
        if p.kind in _PULL_SELL_KINDS
        and normalize_name(p.player_name) == want
        and str(p.bet_type or "win").replace("-", "_") == market
    ]
    exits = [p for p in hits if p.kind == "exit"]
    if exits:
        return exits[-1]
    return hits[-1] if hits else None


def relink_positions(positions, ranked_names) -> list:
    names = ranked_names_map(ranked_names)
    if not names:
        return list(positions or [])
    out = []
    for pos in positions or []:
        hit = match_name(pos.player_name, names) if pos.player_name else None
        if hit and hit != pos.player_id:
            out.append(pos.model_copy(update={"player_id": hit}))
        else:
            out.append(pos)
    return out


def relink_paper_player_ids(record: PaperBookFile | None, ranked_names) -> PaperBookFile | None:
    """Point name: slugs at this snapshot's ESPN ids. Same tickets, new ids."""
    if record is None:
        return record
    names = ranked_names_map(ranked_names)
    if not names:
        return record
    new_pos = relink_positions(record.book.positions, names)
    id_by_ticket = {p.position_id: p.player_id for p in new_pos}

    def _remap_mv(mv: PaperMovement) -> PaperMovement:
        pid = id_by_ticket.get(mv.position_id)
        if not pid:
            hit = match_name(mv.player_name, names) if mv.player_name else None
            pid = hit
        if pid and pid != mv.player_id:
            return mv.model_copy(update={"player_id": pid})
        return mv

    rec = record.model_copy(
        update={
            "book": record.book.model_copy(update={"positions": new_pos}),
            "movements": [_remap_mv(mv) for mv in record.movements],
            "latest_advice": [_remap_mv(mv) for mv in record.latest_advice],
        }
    )
    return rec


def _opt_float(raw) -> float | None:
    if raw is None or raw == "":
        return None
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def record_polymarket_fill(
    *,
    event_id: str,
    player_name: str,
    shares: float,
    fill: float,
    cost: float | None = None,
    market: str = "win",
    event_name: str = "",
    player_id: str | None = None,
    ranked_names: dict[str, str] | None = None,
    intent: str | None = None,
    pulls=None,
) -> PaperBookFile:
    """Write a user fill onto `{event}_polymarket.json`. Does not place an order.

    If the name+market was on the last ntfy ADD (or NEW), inherit that ESPN id,
    intent, and lock model. ADD adds shares onto the open ticket. Typed --intent
    still wins.
    """
    eid = str(event_id or "").strip()
    if not eid:
        raise FillError("event id is required")
    name = str(player_name or "").strip()
    if not name:
        raise FillError("player name is required")
    try:
        n = float(shares)
        px = float(fill)
    except (TypeError, ValueError) as exc:
        raise FillError("shares and fill must be numbers") from exc
    if n <= 0:
        raise FillError("shares must be > 0")
    if px <= 0.0 or px >= 1.0:
        raise FillError("fill is a Yes price in (0, 1), e.g. 0.034 not 3.4 cents")
    spent = float(cost) if cost is not None else n * px
    if spent <= 0:
        raise FillError("cost must be > 0")
    bet = parse_fill_market(market)
    odds = n / spent
    if odds <= 1.0:
        raise FillError("shares / cost must be > 1 (Yes pays $1)")

    rec = load_paper_file(eid, path_id=POLYMARKET_PATH_ID)
    names = ranked_names_map(ranked_names)
    rec = relink_paper_player_ids(rec, names) if rec is not None else rec
    pull_list = parse_fill_pulls(pulls)
    if rec is not None:
        pull_list = list(pull_list) + pulls_from_advice(rec.latest_advice)
    pull = match_fill_pull(name, bet, pull_list)
    pull_pid = (pull.player_id if pull else "") or ""
    if pull_pid and not is_provisional_player_id(pull_pid):
        pid = pull_pid
    else:
        pid = _resolve_player_id(
            name,
            player_id=player_id,
            record=rec,
            ranked_names=ranked_names,
        )
        hit = match_name(name, names) if names else None
        if hit:
            pid = hit
    if intent is not None:
        intent_final = _fill_intent(intent)
    elif pull and pull.intent:
        intent_final = _fill_intent(pull.intent)
    else:
        intent_final = None
    display = name
    if rec:
        for old in rec.book.positions:
            if _same_ticket(old, pid, name, bet) and old.player_name:
                display = old.player_name
                break
    entry_model = px
    entry_edge = 0.0
    entry_market = px
    notes = "polymarket fill; user-typed; no CLOB order"
    pull_tag = ""
    if pull:
        pull_tag = f"last ntfy {pull.kind}"
        notes = f"{notes}; {pull_tag}"
    if pull and pull.model_win and float(pull.model_win) > 0:
        entry_model = float(pull.model_win)
        if pull.posted_edge is not None:
            entry_edge = float(pull.posted_edge)
        elif pull.edge_w is not None:
            entry_edge = float(pull.edge_w)
        notes = f"{notes}; lock model {entry_model:.3f} from last ntfy pull"
    pos = StrategyPosition(
        position_id=new_id("fill"),
        player_id=pid,
        player_name=display,
        bet_type=bet,
        stake=round(spent, 2),
        decimal_odds=float(odds),
        entry_edge=entry_edge,
        entry_model_p=entry_model,
        entry_market_p=entry_market,
        notes=notes,
        user_recorded=True,
        proposed=False,
        shares=float(n),
        fill_price=px,
        cost_usd=round(spent, 2),
        intent=intent_final or "hold",
    )
    if rec is None:
        bankroll = float(METHOD_LAW_V1["independent_compare_bankroll"])
        rec = PaperBookFile(
            tournament_id=eid,
            tournament_name=event_name or eid,
            bankroll=bankroll,
            starting_bankroll=bankroll,
            odds_book="polymarket",
            paper_observation_only=False,
            path_id=POLYMARKET_PATH_ID,
            independent_bankroll=True,
            notes=[
                "PAPER / MOCK. Independent $250. Not ledger.json. No CLOB orders.",
                "Positions with shares are user-typed fills, not auto-lock observation stubs.",
            ],
            book=PortfolioState(bankroll=bankroll, positions=[], session_label="polymarket-fill"),
        )
    positions = list(rec.book.positions)
    replaced = None
    kept: list[StrategyPosition] = []
    added_onto_fill = False
    for old in positions:
        if _same_ticket(old, pid, name, bet):
            replaced = old
            if _should_accumulate_add(old, pull):
                pos = _accumulate_add(old, n, px, spent, pid, intent_final)
                added_onto_fill = True
            else:
                pos = pos.model_copy(update=_lock_entry_update(old, pos, px, intent_final))
            continue
        kept.append(old)
    kept.append(pos)
    rec.book = rec.book.model_copy(update={"positions": kept})
    if added_onto_fill:
        kind = "fill_add"
    elif replaced is not None:
        kind = "fill_replace"
    else:
        kind = "fill"
    replaced_obs = replaced is not None and not replaced.shares and not added_onto_fill
    rec.movements = list(rec.movements) + [
        PaperMovement(
            movement_id=new_id("move"),
            kind=kind,
            status="applied",
            player_id=pid,
            player_name=display,
            bet_type=bet.value,
            position_id=pos.position_id,
            stake_before=replaced.stake if replaced else 0.0,
            stake_delta=pos.stake - (replaced.stake if replaced else 0.0),
            stake_after=pos.stake,
            decimal_odds=pos.decimal_odds,
            reason_plain=_fill_reason_plain(n, px, spent, replaced_obs, added_onto_fill, pull),
            reason_technical=f"shares={n} fill={px} cost={spent} odds={pos.decimal_odds:.4f}",
            shares=float(pos.shares or n),
            intent=pos.intent,
            model_win=pos.entry_model_p,
            posted_edge=pos.entry_edge,
        )
    ]
    rec.notes = list(rec.notes or [])
    rec.notes.append(
        f"fill {display} {bet.value} shares={n:g} @ {px:.4f} cost=${spent:.2f}"
        + (" (replaced observation)" if replaced_obs else "")
        + (" (last ntfy ADD)" if added_onto_fill or (pull and pull.kind == "add") else "")
        + (f" ({pull_tag})" if pull_tag and not (pull and pull.kind == "add") else "")
    )
    save_paper_book(rec)
    return rec


def record_polymarket_sell(
    *,
    event_id: str,
    player_name: str,
    payout: float,
    market: str = "win",
    ranked_names: dict[str, str] | None = None,
    pulls=None,
    shares: float | None = None,
    fill: float | None = None,
    cost: float | None = None,
) -> PaperBookFile:
    """Record a user sell on the Polymarket paper path. Never a CLOB order.

    `--payout` is the USDC received (the confirmation Payout). If this name+market
    is not open yet, pass the original `--cost` / `--fill` / `--shares` so the
    buy is booked first, then sold.
    """
    eid = str(event_id or "").strip()
    if not eid:
        raise FillError("event id is required")
    name = str(player_name or "").strip()
    if not name:
        raise FillError("player name is required")
    try:
        received = float(payout)
    except (TypeError, ValueError) as exc:
        raise FillError("payout must be a number") from exc
    if received <= 0:
        raise FillError("payout must be > 0")
    bet = parse_fill_market(market)
    rec = load_paper_file(eid, path_id=POLYMARKET_PATH_ID)
    names = ranked_names_map(ranked_names)
    rec = relink_paper_player_ids(rec, names) if rec is not None else rec
    pull_list = parse_fill_pulls(pulls)
    if rec is not None:
        pull_list = list(pull_list) + pulls_from_advice(rec.latest_advice)
    sell_pull = match_sell_pull(name, bet, pull_list)
    pid = ""
    if sell_pull and sell_pull.player_id and not is_provisional_player_id(sell_pull.player_id):
        pid = sell_pull.player_id
    elif rec is not None:
        pid = _resolve_player_id(name, player_id=None, record=rec, ranked_names=ranked_names)
        hit = match_name(name, names) if names else None
        if hit:
            pid = hit
    pos = _find_open_ticket(rec, pid, name, bet)
    if pos is None:
        need_open = (
            (shares is not None and float(shares) > 0)
            or (fill is not None and float(fill) > 0)
            or (cost is not None and float(cost) > 0)
        )
        if not need_open:
            raise FillError(
                "no open ticket on that name+market; paper-fill first or pass "
                "--cost and --fill (and --shares if not cost/fill)"
            )
        rec = record_polymarket_fill(
            event_id=eid,
            player_name=name,
            shares=_shares_for_open(shares, fill, cost),
            fill=_fill_for_open(fill, shares, cost),
            cost=cost,
            market=market,
            ranked_names=ranked_names,
            pulls=pull_list or None,
        )
        pos = _find_open_ticket(rec, pid, name, bet)
    if rec is None or pos is None:
        raise FillError("no open ticket on that name+market")
    sold = round(float(pos.stake), 2)
    pnl = round(received - sold, 2)
    kept = [p for p in rec.book.positions if p.position_id != pos.position_id]
    rec.bankroll = round(float(rec.bankroll) + pnl, 2)
    rec.book = rec.book.model_copy(
        update={
            "positions": kept,
            "bankroll": rec.bankroll,
            "realized_pnl_event": round(float(rec.book.realized_pnl_event or 0.0) + pnl, 2),
            "realized_pnl_today": round(float(rec.book.realized_pnl_today or 0.0) + pnl, 2),
        }
    )
    pull_tag = f"last ntfy {sell_pull.kind}" if sell_pull else ""
    rec.movements = list(rec.movements) + [
        PaperMovement(
            movement_id=new_id("move"),
            kind="fill_sell",
            status="applied",
            player_id=pos.player_id,
            player_name=pos.player_name,
            bet_type=bet.value,
            position_id=pos.position_id,
            stake_before=sold,
            stake_delta=-sold,
            stake_after=0.0,
            decimal_odds=pos.decimal_odds,
            reason_plain=(
                f"Recorded Polymarket sell payout ${received:.2f} on ${sold:.2f} "
                f"cost (P/L ${pnl:+.2f}). Not a CLOB order."
                + (" Attached to last ntfy SELL." if sell_pull else "")
            ),
            reason_technical=f"payout={received} cost={sold} pnl={pnl}",
            cashout_quote=received,
            cashout_estimated=False,
            shares=pos.shares,
            live_bid=(received / float(pos.shares)) if pos.shares else None,
            mtm_is_bid=True,
            intent=pos.intent,
            model_win=pos.entry_model_p,
            posted_edge=pos.entry_edge,
        )
    ]
    rec.notes = list(rec.notes or [])
    rec.notes.append(
        f"sell {pos.player_name} {bet.value} payout=${received:.2f} cost=${sold:.2f} pnl=${pnl:+.2f}"
        + (f" ({pull_tag})" if pull_tag else "")
    )
    save_paper_book(rec)
    return rec


def _shares_for_open(shares, fill, cost) -> float:
    if shares is not None and float(shares) > 0:
        return float(shares)
    if fill is not None and cost is not None and float(fill) > 0 and float(cost) > 0:
        return float(cost) / float(fill)
    raise FillError("pass --shares, or both --cost and --fill, to book a missing buy before the sell")


def _fill_for_open(fill, shares, cost) -> float:
    if fill is not None and float(fill) > 0:
        return float(fill)
    if shares is not None and cost is not None and float(shares) > 0 and float(cost) > 0:
        px = float(cost) / float(shares)
        if 0.0 < px < 1.0:
            return px
    raise FillError("pass --fill in (0, 1), or --cost and --shares")


def _find_open_ticket(rec: PaperBookFile | None, pid: str, name: str, bet: BetType):
    if rec is None:
        return None
    for pos in rec.book.positions:
        if _same_ticket(pos, pid, name, bet):
            return pos
    return None


def _existing_is_fill(old) -> bool:
    try:
        return (
            old.shares is not None
            and float(old.shares) > 0
            and old.fill_price is not None
            and float(old.fill_price) > 0
        )
    except (TypeError, ValueError):
        return False


def _should_accumulate_add(old, pull: FillPull | None) -> bool:
    if pull is None or pull.kind != "add":
        return False
    return _existing_is_fill(old)


def _accumulate_add(old, shares: float, fill: float, spent: float, pid: str, intent: str | None):
    old_shares = float(old.shares)
    old_cost = float(old.cost_usd if old.cost_usd is not None else old.stake)
    n2 = old_shares + shares
    spent2 = old_cost + spent
    note = (old.notes or "").rstrip(";")
    note = f"{note}; add fill {shares:g} @ {fill:.4f} cost ${spent:.2f} (last ntfy ADD)"
    return old.model_copy(
        update={
            "player_id": pid or old.player_id,
            "shares": n2,
            "cost_usd": round(spent2, 2),
            "stake": round(spent2, 2),
            "fill_price": spent2 / n2,
            "decimal_odds": n2 / spent2,
            "user_recorded": True,
            "proposed": False,
            "notes": note,
            "intent": _fill_intent(intent) if intent else (old.intent or "hold"),
        }
    )


def _fill_reason_plain(n, px, spent, replaced_obs, added_onto_fill, pull) -> str:
    base = f"Recorded Polymarket fill {n:g} shares @ {px:.4f} cost ${spent:.2f}. Not a CLOB order."
    if added_onto_fill:
        return base + " Added onto the open ticket from last ntfy ADD."
    if replaced_obs:
        return base + " Observation stub replaced."
    if pull and pull.kind == "add":
        return base + " Attached to last ntfy ADD."
    return base


def _same_ticket(old, pid: str, name: str, bet: BetType) -> bool:
    if old.bet_type != bet:
        return False
    if pid and old.player_id == pid:
        return True
    if name and normalize_name(old.player_name) == normalize_name(name):
        return True
    return False


def _fill_intent(raw: str | None) -> str:
    key = (raw or "hold").strip().lower()
    if key not in {"hold", "flip"}:
        raise FillError("intent must be hold or flip")
    return key


def _lock_entry_update(old, pos, fill_px: float, intent: str | None) -> dict:
    """Keep lock model/edge on a fill so the ticket still says why it was booked."""
    update = {
        "position_id": old.position_id,
        "entered_at": old.entered_at,
        "round_entered": old.round_entered,
        "intent": _fill_intent(intent) if intent else (old.intent or "hold"),
    }
    if not _should_keep_lock_model(old, fill_px):
        return update
    note = (pos.notes or "").rstrip(";")
    update.update(
        {
            "entry_model_p": old.entry_model_p,
            "entry_edge": old.entry_edge,
            "entry_market_p": old.entry_market_p,
            "notes": f"{note}; lock model {old.entry_model_p:.3f} kept",
        }
    )
    return update


def _should_keep_lock_model(old, fill_px: float) -> bool:
    try:
        model = float(old.entry_model_p)
    except (TypeError, ValueError):
        return False
    if model <= 0.0:
        return False
    try:
        old_fill = float(old.fill_price) if old.fill_price is not None else None
    except (TypeError, ValueError):
        old_fill = None
    if old_fill is not None and abs(model - old_fill) < 0.002 and abs(float(old.entry_edge or 0.0)) < 0.002:
        return False
    if old_fill is None and abs(model - float(fill_px)) < 0.002 and abs(float(old.entry_edge or 0.0)) < 0.002:
        return False
    return True


def backfill_lock_entry_on_fills(record):
    """If a fill flattened entry to the fill price, restore model/edge from the lock snapshot."""
    from golf_offshoot.models.enums import horizon_for
    from golf_offshoot.strategy.paper_book import load_snapshot_audit, save_paper_book

    run = (getattr(record, "locked_from_run_id", None) or "").strip()
    if not run:
        return record
    audit = load_snapshot_audit(run)
    if audit is None:
        return record
    by_id = {o.player_id: o for o in audit.outputs}
    by_name = {o.name: o for o in audit.outputs}
    changed = False
    kept = []
    for pos in record.book.positions:
        if not _entry_looks_like_fill_price(pos):
            kept.append(pos)
            continue
        row = by_id.get(pos.player_id) or by_name.get(pos.player_name)
        if row is None:
            kept.append(pos)
            continue
        h = horizon_for(pos.bet_type)
        hp = row.probabilities.horizons.get(h) if h is not None else None
        if hp is None:
            kept.append(pos)
            continue
        edge = (row.edge_by_bet or {}).get(pos.bet_type.value)
        mkt = (row.market_implied_by_bet or {}).get(pos.bet_type.value)
        note = pos.notes or ""
        if "lock model" not in note:
            note = f"{note}; lock model {hp.central:.3f} restored".strip("; ")
        kept.append(
            pos.model_copy(
                update={
                    "entry_model_p": float(hp.central),
                    "entry_edge": float(edge) if edge is not None else pos.entry_edge,
                    "entry_market_p": float(mkt) if mkt is not None else pos.entry_market_p,
                    "notes": note,
                }
            )
        )
        changed = True
    if not changed:
        return record
    rec = record.model_copy(update={"book": record.book.model_copy(update={"positions": kept})})
    save_paper_book(rec)
    return rec


def _entry_looks_like_fill_price(pos) -> bool:
    from golf_offshoot.strategy.paper_book import _position_is_fill

    if not _position_is_fill(pos):
        return False
    try:
        fill = float(pos.fill_price)
        model = float(pos.entry_model_p)
        edge = float(pos.entry_edge or 0.0)
    except (TypeError, ValueError):
        return False
    return abs(model - fill) < 0.002 and abs(edge) < 0.002


def _resolve_player_id(
    name: str,
    *,
    player_id: str | None,
    record: PaperBookFile | None,
    ranked_names: dict[str, str] | None,
) -> str:
    if player_id:
        return str(player_id)
    names: dict[str, str] = {}
    if record:
        for pos in record.book.positions:
            if pos.player_name:
                names.setdefault(normalize_name(pos.player_name), pos.player_id)
    if ranked_names:
        for label, pid in ranked_names.items():
            names.setdefault(normalize_name(label), pid)
    hit = match_name(name, names) if names else None
    return hit or provisional_player_id(name)
