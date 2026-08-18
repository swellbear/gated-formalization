"""Record a real Polymarket fill on the independent paper path. Never CLOB. Never ledger.json."""

from __future__ import annotations

from golf_offshoot.compare.law import METHOD_LAW_V1
from golf_offshoot.data_feeds.field_fallback import provisional_player_id
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
) -> PaperBookFile:
    """Write a user fill onto `{event}_polymarket.json`. Does not place an order."""
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
    pid = _resolve_player_id(
        name,
        player_id=player_id,
        record=rec,
        ranked_names=ranked_names,
    )
    display = name
    if rec:
        for pos in rec.book.positions:
            if pos.player_id == pid and pos.player_name:
                display = pos.player_name
                break
    pos = StrategyPosition(
        position_id=new_id("fill"),
        player_id=pid,
        player_name=display,
        bet_type=bet,
        stake=round(spent, 2),
        decimal_odds=float(odds),
        entry_edge=0.0,
        entry_model_p=px,
        entry_market_p=px,
        notes="polymarket fill; user-typed; no CLOB order",
        user_recorded=True,
        proposed=False,
        shares=float(n),
        fill_price=px,
        cost_usd=round(spent, 2),
        intent=_fill_intent(intent),
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
    for old in positions:
        same = old.player_id == pid and old.bet_type == bet
        if same:
            replaced = old
            pos = pos.model_copy(update=_lock_entry_update(old, pos, px, intent))
            continue
        kept.append(old)
    kept.append(pos)
    rec.book = rec.book.model_copy(update={"positions": kept})
    kind = "fill_replace" if replaced is not None else "fill"
    replaced_obs = replaced is not None and not replaced.shares
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
            reason_plain=(
                f"Recorded Polymarket fill {n:g} shares @ {px:.4f} cost ${spent:.2f}. "
                "Not a CLOB order. Observation stub replaced."
                if replaced_obs
                else f"Recorded Polymarket fill {n:g} shares @ {px:.4f} cost ${spent:.2f}. Not a CLOB order."
            ),
            reason_technical=f"shares={n} fill={px} cost={spent} odds={odds:.4f}",
            shares=float(n),
        )
    ]
    rec.notes = list(rec.notes or [])
    rec.notes.append(
        f"fill {display} {bet.value} shares={n:g} @ {px:.4f} cost=${spent:.2f}"
        + (" (replaced observation)" if replaced_obs else "")
    )
    save_paper_book(rec)
    return rec


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
