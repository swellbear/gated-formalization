"""Paper (mock) bankroll for one event. Never auto-bets. Never real money."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel, Field

from golf_offshoot.config import (
    MIN_EDGE_TO_CONSIDER,
    PAPER_ESTIMATED_CASHOUT_HAIRCUT,
    PAPER_OBSERVATION_STAKE_FRAC,
)
from golf_offshoot.data_feeds.http import package_data_dir
from golf_offshoot.models.enums import BetType, Horizon, StrategyActionKind
from golf_offshoot.models.schemas import PlayerOutput
from golf_offshoot.models.strategy import (
    PortfolioState,
    StrategyConfig,
    StrategyPosition,
    StrategyRecommendation,
    new_id,
)
from golf_offshoot.strategy.cashout import estimated_cashout_offer
from golf_offshoot.strategy.sizing import (
    remaining_exposure_capacity,
    scaled_exposure_cap,
    scaled_single_cap,
)

_HARD_PASS = {"thin_sample_overconfidence", "sparse_data"}
_BET_HORIZON = {
    BetType.WIN: Horizon.WIN,
    BetType.TOP_5: Horizon.TOP_5,
    BetType.TOP_10: Horizon.TOP_10,
    BetType.TOP_20: Horizon.TOP_20,
    BetType.MAKE_CUT: Horizon.MAKE_CUT,
}


class PaperMovement(BaseModel):
    """One paper lock, sell, add, or reallocate. Never a real-money fill."""

    movement_id: str
    at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    kind: str
    status: str = "applied"
    player_id: str = ""
    player_name: str = ""
    bet_type: str = "win"
    position_id: str = ""
    from_player_name: str = ""
    stake_before: float | None = None
    stake_delta: float = 0.0
    stake_after: float | None = None
    decimal_odds: float | None = None
    model_win: float | None = None
    edge_w: float | None = None
    posted_edge: float | None = None
    run_id: str = ""
    reason_plain: str = ""
    reason_technical: str = ""
    amount_plain: str = ""
    amount_technical: str = ""
    never_auto_bet: bool = True
    cashout_quote: float | None = None
    cashout_estimated: bool = False
    hold_expected_payout: float | None = None
    cashout_threshold: float | None = None


class PaperBookFile(BaseModel):
    tournament_id: str
    tournament_name: str = ""
    bankroll: float
    locked_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    locked_from_run_id: str = ""
    odds_book: str = ""
    paper_observation_only: bool = True
    never_auto_bet: bool = True
    risk: str = "conservative"
    mode: str = "stay_selective"
    notes: list[str] = Field(default_factory=list)
    book: PortfolioState
    movements: list[PaperMovement] = Field(default_factory=list)
    latest_advice: list[PaperMovement] = Field(default_factory=list)
    export_pdf: str = ""
    export_html: str = ""
    export_txt: str = ""
    latest_pack: str = ""
    settled_at: datetime | None = None
    settlement_pnl: float | None = None
    settlement_winner: str = ""
    path_id: str = "lived"
    last_advice_sig: str = ""
    independent_bankroll: bool = False
    method_law_hash: str = ""


@dataclass(frozen=True)
class PaperTicketRow:
    player_name: str
    market: str
    stake: float
    posted: float
    model_win: float
    edge_w: float
    posted_edge: float
    if_wins: float
    screen: str
    cleared: bool
    lane: str = "[observation]"
    live_posted: float | None = None
    live_model: float | None = None
    live_edge_w: float | None = None
    live_posted_edge: float | None = None
    live_run_id: str = ""
    entered_at: datetime | None = None


def format_paper_time(value: datetime | None) -> str:
    if value is None:
        return "n/a"
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _bet_key(value) -> str:
    return str(getattr(value, "value", value) or "win").lower().replace(" ", "_")


def entry_time_for(
    record: PaperBookFile | None,
    *,
    player_id: str = "",
    player_name: str = "",
    bet_type: str = "win",
) -> datetime | None:
    """First lock/add on this player+market, else the open position's entered_at."""
    if record is None:
        return None
    bet = _bet_key(bet_type)
    for p in record.book.positions:
        same = (player_id and p.player_id == player_id) or (
            player_name and p.player_name == player_name
        )
        if same and _bet_key(p.bet_type) == bet:
            return p.entered_at
    first: datetime | None = None
    for mv in record.movements:
        if mv.status and mv.status not in {"applied"}:
            continue
        if mv.kind not in {"lock", "new_bet", "add"}:
            continue
        same = (player_id and mv.player_id == player_id) or (
            player_name and mv.player_name == player_name
        )
        if not same or _bet_key(mv.bet_type) != bet:
            continue
        if first is None or (mv.at and first and mv.at < first):
            first = mv.at
    return first


def movement_clocks(
    record: PaperBookFile | None, m: PaperMovement
) -> tuple[str, str, str]:
    """When this row happened, when the ticket was entered, when it exited (or open)."""
    when = format_paper_time(getattr(m, "at", None))
    entered_dt = entry_time_for(
        record,
        player_id=m.player_id,
        player_name=m.player_name,
        bet_type=m.bet_type or "win",
    )
    if entered_dt is None and m.kind in {"lock", "new_bet", "add"}:
        entered_dt = m.at
    entered = format_paper_time(entered_dt)
    if m.kind == "exit" and (not m.status or m.status == "applied"):
        exited = when
    elif m.kind == "exit":
        exited = "n/a"
    else:
        exited = "open"
    return when, entered, exited


def _fmt_dec(value: float | None) -> str:
    return f"{value:.2f}" if value is not None else "n/a"


def _fmt_pct(value: float | None) -> str:
    return f"{value * 100:.1f}%" if value is not None else "n/a"


def _fmt_pp(value: float | None) -> str:
    return f"{value * 100:+.1f}pp" if value is not None else "n/a"


def observation_plain() -> str:
    return (
        "In plain language: the sportsbook takes a cut on live winner odds, so every "
        "price is a little worse than a fair coin-flip market. A player can look like "
        "a good bet after we remove that cut, but still fail the check against the "
        "actual number you would buy. That is not the ranking breaking. It means we "
        "would not treat the ticket as cleared. This paper book still records the best "
        "remaining clean names so we can track them with fake money."
    )


def observation_technical() -> str:
    return (
        "Technical: EdgeW = model_p minus implied_fair (overround stripped). "
        "Ticket screen = model_p minus 1/decimal_odds, and must be at least "
        f"{MIN_EDGE_TO_CONSIDER:.2f} ({MIN_EDGE_TO_CONSIDER * 100:.0f}pp) to consider. "
        "Live winner boards often carry overround about 1.29-1.37; that extra cut is "
        "live juice. A paper lock is residual judgment on clean positive posted-edge "
        "names, not DecisionAction.CONSIDER clearance, and not a real-money ticket."
    )


def clocks_plain() -> str:
    return (
        "At entry is the booked ticket and is never rewritten. This live is this "
        "pack's snapshot only - the numbers strategy used. n/a means that market "
        "had no posted coupon on this run (Winner Live is not used as a place price). "
        "Stake and If wins stay on the entry decimal."
    )


def posted_price_edge(model_p: float, decimal_odds: float) -> float:
    if decimal_odds <= 1.0:
        return model_p
    return float(model_p) - 1.0 / float(decimal_odds)


def screen_cleared(edge_w: float, posted_edge: float) -> bool:
    return edge_w >= MIN_EDGE_TO_CONSIDER and posted_edge >= MIN_EDGE_TO_CONSIDER


def lane_tag(cleared: bool) -> str:
    return "[cleared]" if cleared else "[observation]"


def screen_plain(edge_w: float, posted_edge: float) -> str:
    if screen_cleared(edge_w, posted_edge):
        return "Cleared — model still beats the posted price by at least 3 percentage points"
    if posted_edge > 0:
        return (
            f"Short of 3pp vs the posted price ({posted_edge * 100:+.1f}pp). "
            "Live juice makes the number you would actually buy harder to beat than the fair EdgeW."
        )
    return "Does not beat the posted price. The book is already shorter than the model."


def ticket_rows(
    record: PaperBookFile,
    live_outputs: list[PlayerOutput] | None = None,
    *,
    live_run_id: str = "",
) -> list[PaperTicketRow]:
    """At-entry blotter plus optional this-live marks from one snapshot.

    Live posted / EdgeW / vs-posted stay n/a unless that snapshot has a real
    posted coupon for the ticket's market. Winner Live is never used as a
    stand-in for Top 5 / 10 / 20. Entry decimals are never rewritten.
    """
    by_id = {r.player_id: r for r in (live_outputs or [])}
    rows: list[PaperTicketRow] = []
    for p in record.book.positions:
        posted_edge = posted_price_edge(p.entry_model_p, p.decimal_odds)
        live_posted = None
        live_model = None
        live_edge_w = None
        live_vs = None
        row = by_id.get(p.player_id)
        if row is not None:
            horizon = _BET_HORIZON.get(p.bet_type)
            if horizon is not None:
                hp = row.probabilities.horizons.get(horizon)
                if hp is not None:
                    live_model = hp.central
            raw = row.posted_odds_by_bet.get(p.bet_type.value)
            try:
                posted_f = float(raw) if raw is not None else None
            except (TypeError, ValueError):
                posted_f = None
            if posted_f is not None and posted_f > 1.0 and live_model is not None:
                live_posted = posted_f
                live_vs = posted_price_edge(live_model, posted_f)
                edge = row.edge_by_bet.get(p.bet_type.value)
                if edge is not None:
                    live_edge_w = float(edge)
        rows.append(
            PaperTicketRow(
                player_name=p.player_name,
                market=p.bet_type.value.replace("_", " ").title(),
                stake=p.stake,
                posted=p.decimal_odds,
                model_win=p.entry_model_p,
                edge_w=p.entry_edge,
                posted_edge=posted_edge,
                if_wins=p.stake * p.decimal_odds,
                screen=screen_plain(p.entry_edge, posted_edge),
                cleared=screen_cleared(p.entry_edge, posted_edge),
                lane=lane_tag(screen_cleared(p.entry_edge, posted_edge)),
                live_posted=live_posted,
                live_model=live_model,
                live_edge_w=live_edge_w,
                live_posted_edge=live_vs,
                live_run_id=live_run_id,
                entered_at=p.entered_at,
            )
        )
    return rows


def load_snapshot_outputs(run_id: str, *, directory: Path | None = None) -> list[PlayerOutput] | None:
    """Outputs from one persisted run. Missing file is n/a, not invented."""
    if not run_id:
        return None
    from golf_offshoot.audit.journal import load_audit
    from pydantic import ValidationError

    d = directory or (package_data_dir() / "snapshots")
    safe = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in str(run_id))
    path = d / f"{safe}.json"
    if not path.is_file():
        return None
    try:
        rec = load_audit(path)
    except (OSError, ValueError, KeyError, TypeError, ValidationError):
        return None
    return list(rec.outputs)


def _bet_terms_from_row(row: PlayerOutput, bet: str) -> dict:
    key = bet or "win"
    posted = row.posted_odds_by_bet.get(key)
    try:
        posted_f = float(posted) if posted is not None else None
    except (TypeError, ValueError):
        posted_f = None
    if posted_f is None or posted_f <= 1.0:
        imp = row.market_implied_by_bet.get(key)
        posted_f = (1.0 / float(imp)) if imp and imp > 0 else None
    model = None
    try:
        bt = BetType(key)
        model = row.probabilities.p(_BET_HORIZON[bt]).central
    except (ValueError, KeyError):
        pass
    edge = row.edge_by_bet.get(key)
    posted_edge = None
    if model is not None and posted_f is not None and posted_f > 1.0:
        posted_edge = model - 1.0 / posted_f
    out: dict = {}
    if posted_f is not None and posted_f > 1.0:
        out["decimal_odds"] = posted_f
    if model is not None:
        out["model_win"] = model
    if edge is not None:
        out["edge_w"] = edge
    if posted_edge is not None:
        out["posted_edge"] = posted_edge
    return out


def hydrate_new_bet_movement(mv: PaperMovement) -> PaperMovement:
    """Fill posted odds / model on a new_bet from its snapshot. Do not invent a coupon."""
    needs_odds = mv.decimal_odds is None or mv.decimal_odds <= 1.0
    needs_model = mv.model_win is None
    if not needs_odds and not needs_model:
        return mv
    rows = load_snapshot_outputs(mv.run_id)
    if not rows:
        return mv
    row = next((r for r in rows if r.player_id and r.player_id == mv.player_id), None)
    if row is None:
        row = next((r for r in rows if r.name == mv.player_name), None)
    if row is None:
        return mv
    terms = _bet_terms_from_row(row, mv.bet_type or "win")
    if not terms:
        return mv
    return mv.model_copy(update=terms)


def sizing_plain(config: StrategyConfig) -> str:
    unit = config.bankroll * scaled_single_cap(config)
    obs = unit * PAPER_OBSERVATION_STAKE_FRAC
    total = config.bankroll * scaled_exposure_cap(config)
    return (
        f"Cleared names (EdgeW and vs-posted both at least {MIN_EDGE_TO_CONSIDER * 100:.0f}pp) "
        f"are capped at {scaled_single_cap(config):.1%} of the "
        f"${config.bankroll:.0f} paper bankroll (${unit:.2f}). That is a 5% single-name "
        "ceiling times the risk haircut. Observation names (positive vs-posted but short of "
        f"the 3pp ticket screen) get {PAPER_OBSERVATION_STAKE_FRAC:.0%} of that unit "
        f"(${obs:.2f}). It is a concentration rule, not a fitted Kelly size. "
        "Two cleared names can get the same dollar amount because both hit the per-name "
        "ceiling, not because they have the same edge. Cash left is unused room under the "
        f"{scaled_exposure_cap(config):.0%} total cap (${total:.2f}) plus everything above it."
    )


def sizing_technical(config: StrategyConfig) -> str:
    return (
        "scaled_single_cap = max_single_position_frac (0.05) * risk haircut "
        f"(conservative 0.70). Observation stake = unit * {PAPER_OBSERVATION_STAKE_FRAC}. "
        "scaled_exposure_cap = 0.20 * risk haircut. "
        "Advisory size is fractional Kelly (0.25) * range haircut * reliability * risk * "
        "mode, then min(unit, remaining total cap). The paper lock does not use "
        "that Kelly figure as the stake; cleared uses the unit cap, observation uses 25% of it."
    )


def lock_movement_for_ticket(
    ticket: PaperTicketRow,
    *,
    position_id: str,
    player_id: str,
    config: StrategyConfig,
    run_id: str,
) -> PaperMovement:
    unit = config.bankroll * scaled_single_cap(config)
    tag = lane_tag(ticket.cleared)
    why_name_plain = (
        f"{tag} {ticket.player_name} is in the book because the winner quote was real and "
        f"still beat the posted number on a {'cleared' if ticket.cleared else 'tracking'} "
        f"ticket (model {ticket.model_win * 100:.1f}% vs 1/odds "
        f"{(1.0 / ticket.posted) * 100:.1f}%, EdgeW {ticket.edge_w * 100:+.1f}pp, "
        f"vs posted {ticket.posted_edge * 100:+.1f}pp). {ticket.screen}"
    )
    why_name_tech = (
        f"kind=lock status=applied lane={tag} bet=win posted={ticket.posted:.2f} "
        f"model_p={ticket.model_win:.3f} EdgeW={ticket.edge_w:+.3f} "
        f"posted_edge={ticket.posted_edge:+.3f} screen_cleared={ticket.cleared}"
    )
    obs_unit = unit * PAPER_OBSERVATION_STAKE_FRAC
    if ticket.cleared:
        hit_cap = abs(ticket.stake - unit) < 0.02
        amount_plain = (
            f"{tag} ${ticket.stake:.2f} is the single-name cap "
            f"({scaled_single_cap(config):.1%} of ${config.bankroll:.0f})."
            if hit_cap
            else f"{tag} ${ticket.stake:.2f} is what remained under the total exposure cap."
        )
        amount_plain += " Kelly after the uncertainty haircut would usually be smaller."
    else:
        amount_plain = (
            f"{tag} ${ticket.stake:.2f} is {PAPER_OBSERVATION_STAKE_FRAC:.0%} of the "
            f"single-name unit (${unit:.2f} → ${obs_unit:.2f}) because the posted-price "
            "screen is short of 3pp. Not the same dollars as a cleared name."
        )
    amount_tech = (
        f"stake={ticket.stake:.2f} unit_cap={unit:.2f} "
        f"total_cap={config.bankroll * scaled_exposure_cap(config):.2f} "
        f"mode={config.mode.value} risk={config.risk.value} lane={tag}"
    )
    return PaperMovement(
        movement_id=new_id("move"),
        kind="lock",
        status="applied",
        player_id=player_id,
        player_name=ticket.player_name,
        bet_type=ticket.market.lower().replace(" ", "_"),
        position_id=position_id,
        stake_before=0.0,
        stake_delta=ticket.stake,
        stake_after=ticket.stake,
        decimal_odds=ticket.posted,
        model_win=ticket.model_win,
        edge_w=ticket.edge_w,
        posted_edge=ticket.posted_edge,
        run_id=run_id,
        reason_plain=why_name_plain,
        reason_technical=why_name_tech,
        amount_plain=amount_plain,
        amount_technical=amount_tech,
    )


def ensure_lock_movements(record: PaperBookFile, config: StrategyConfig | None = None) -> PaperBookFile:
    """Fill a lock ledger from current tickets if an older file has none."""
    if record.movements:
        return record
    cfg = config or StrategyConfig(
        enabled=True,
        bankroll=record.bankroll,
    )
    tickets = ticket_rows(record)
    by_name = {p.player_name: p for p in record.book.positions}
    record.movements = [
        lock_movement_for_ticket(
            t,
            position_id=by_name[t.player_name].position_id if t.player_name in by_name else "",
            player_id=by_name[t.player_name].player_id if t.player_name in by_name else "",
            config=cfg,
            run_id=record.locked_from_run_id,
        )
        for t in tickets
    ]
    return record


_ACTION_PLAIN = {
    "hold": (
        "Keep this paper ticket. The original reason is still intact; there is no path "
        "reason to sell or add."
    ),
    "reduce": (
        "Sell part of this paper ticket. The cut is a fraction of the current stake, "
        "not a new Kelly from scratch."
    ),
    "exit": (
        "Sell the whole paper ticket. If you typed a cash-out quote that beats "
        "remaining winner EV, this is taking that quote; otherwise the original "
        "edge has collapsed versus the live market."
    ),
    "add": (
        "Add to this paper ticket, still under the single-name cap. This is still mock money."
    ),
    "reallocate": (
        "Move paper stake from a worse live edge onto a better name. Total exposure does "
        "not go up; the dollars just change seats."
    ),
    "new_bet": (
        "Open a new paper ticket on a name that is not already in the book."
    ),
}


def advice_from_recommendation(
    record: PaperBookFile,
    rec: StrategyRecommendation,
    *,
    run_id: str = "",
) -> list[PaperMovement]:
    by_pos = {p.position_id: p for p in record.book.positions}
    out: list[PaperMovement] = []
    for act in rec.actions:
        if act.kind == StrategyActionKind.NO_ACTION:
            continue
        pos = by_pos.get(act.position_id or "")
        mark = next((m for m in rec.marks if m.position_id == act.position_id), None)
        before = pos.stake if pos else 0.0
        delta = float(act.suggested_stake_delta or 0.0)
        after = None
        if act.kind == StrategyActionKind.EXIT:
            after = 0.0
            delta = -before
        elif act.kind == StrategyActionKind.HOLD:
            after = before
            delta = 0.0
        elif pos:
            after = max(0.0, before + delta)
        kind = act.kind.value
        donor = ""
        if act.from_position_id and act.from_position_id in by_pos:
            donor = by_pos[act.from_position_id].player_name
        details = "; ".join(act.reasons_detail) if act.reasons_detail else ""
        warn = f" {act.uncertainty_warning}" if act.uncertainty_warning else ""
        plain = _ACTION_PLAIN.get(kind, act.reason)
        if act.reason:
            plain = f"{plain} Strategy reason: {act.reason}."
        if details:
            plain = f"{plain} {details}."
        live_posted = (
            mark.live_decimal_odds
            if mark and mark.live_decimal_odds and mark.live_decimal_odds > 1.0
            else None
        )
        proposed = next(
            (
                p
                for p in rec.proposed_new_positions
                if kind == "new_bet"
                and p.player_id == act.player_id
                and p.bet_type == act.bet_type
            ),
            None,
        )
        if kind in {"reduce", "exit"}:
            decimal_odds = live_posted
        elif live_posted is not None:
            decimal_odds = live_posted
        elif pos:
            decimal_odds = pos.decimal_odds
        elif proposed and proposed.decimal_odds and proposed.decimal_odds > 1.0:
            decimal_odds = proposed.decimal_odds
        else:
            decimal_odds = None
        model_win = mark.live_model_p if mark else (proposed.entry_model_p if proposed else None)
        edge_w = mark.live_edge if mark else (proposed.entry_edge if proposed else None)
        posted_edge = mark.live_posted_edge if mark else None
        if posted_edge is None and model_win is not None and decimal_odds and decimal_odds > 1.0:
            posted_edge = model_win - 1.0 / decimal_odds
        estimated_offer = None
        if kind in {"reduce", "exit"} and pos and decimal_odds and act.cashout_quote is None:
            estimated_offer = estimated_cashout_offer(
                abs(delta),
                pos.decimal_odds,
                decimal_odds,
            )
        amount_plain = _advice_amount_plain(
            kind,
            before,
            delta,
            after,
            cashout_quote=act.cashout_quote,
            hold_expected_payout=act.hold_expected_payout,
            estimated_offer=estimated_offer,
        )
        out.append(
            PaperMovement(
                movement_id=act.action_id or new_id("move"),
                kind=kind,
                status="advised",
                player_id=act.player_id,
                player_name=act.player_name or (pos.player_name if pos else ""),
                bet_type=act.bet_type.value,
                position_id=act.position_id or "",
                from_player_name=donor,
                stake_before=before,
                stake_delta=delta,
                stake_after=after,
                decimal_odds=decimal_odds,
                model_win=model_win,
                edge_w=edge_w,
                posted_edge=posted_edge,
                run_id=run_id,
                reason_plain=plain,
                reason_technical=f"kind={kind} reason={act.reason}{warn} details={details}",
                amount_plain=amount_plain,
                amount_technical=(
                    f"delta={delta:+.2f} unit={act.suggested_unit:.2f} "
                    f"before={before:.2f} after={after if after is not None else 'n/a'}"
                    + (
                        f" cashout={act.cashout_quote:.2f} hold_ev={act.hold_expected_payout:.2f}"
                        if act.cashout_quote is not None and act.hold_expected_payout is not None
                        else (
                            f" estimated_cashout={estimated_offer:.2f}"
                            if estimated_offer is not None
                            else ""
                        )
                    )
                ),
                cashout_quote=act.cashout_quote,
                cashout_estimated=False,
                hold_expected_payout=act.hold_expected_payout,
                cashout_threshold=act.cashout_threshold,
            )
        )
    return out


def _advice_amount_plain(
    kind: str,
    before: float,
    delta: float,
    after: float | None,
    *,
    cashout_quote: float | None = None,
    hold_expected_payout: float | None = None,
    estimated_offer: float | None = None,
) -> str:
    if kind == "hold":
        if cashout_quote is not None:
            hold = f"${hold_expected_payout:.2f}" if hold_expected_payout is not None else "n/a"
            return (
                f"Stake stays ${before:.2f}. Typed cash-out ${cashout_quote:.2f} "
                f"does not beat hold EV {hold}."
            )
        return f"Stake stays ${before:.2f}. Hold is a size of zero change, not a new bet."
    if kind == "exit":
        if cashout_quote is not None:
            hold = f"${hold_expected_payout:.2f}" if hold_expected_payout is not None else "n/a"
            return (
                f"Take quoted cash-out ${cashout_quote:.2f} on the ${before:.2f} ticket "
                f"(paper). Hold EV {hold}. After = $0.00."
            )
        if estimated_offer is not None:
            return (
                f"Sell ${before:.2f} back to cash (paper). "
                f"Estimated cash-out ${estimated_offer:.2f} "
                f"({PAPER_ESTIMATED_CASHOUT_HAIRCUT:.0%} haircut on MTM gap; "
                "not scraped Open Bets). After = $0.00."
            )
        return f"Sell ${before:.2f} back to cash (paper). After = $0.00."
    if kind == "reduce":
        after_s = f"${after:.2f}" if after is not None else "n/a"
        text = (
            f"Sell ${abs(delta):.2f} of the ${before:.2f} ticket "
            f"(after {after_s} if applied). Fraction of current stake, not a Kelly resize."
        )
        if estimated_offer is not None:
            text += (
                f" Estimated paper cash-out ${estimated_offer:.2f} "
                f"({PAPER_ESTIMATED_CASHOUT_HAIRCUT:.0%} haircut on MTM gap; "
                "not scraped Open Bets)."
            )
        return text
    if kind == "add":
        after_s = f"${after:.2f}" if after is not None else "n/a"
        return (
            f"Add ${delta:.2f} to the ${before:.2f} ticket "
            f"(after {after_s} if applied), still under the single-name cap."
        )
    if kind == "reallocate":
        return (
            f"Move ${abs(delta):.2f} of paper stake onto this name. "
            "The donor ticket shrinks by the same dollars."
        )
    if kind == "new_bet":
        return f"New paper stake ${delta:.2f} if you apply the advice."
    return f"Suggested delta {delta:+.2f} from ${before:.2f}."


def _sold_from_movement(mv: PaperMovement) -> float:
    if mv.stake_before is not None and mv.stake_after is not None:
        return round(max(0.0, float(mv.stake_before) - float(mv.stake_after)), 2)
    return round(abs(float(mv.stake_delta or 0.0)), 2)


def _estimated_amount_suffix(offer: float | None, estimated: bool, existing: str) -> str:
    if not estimated or offer is None:
        return ""
    if existing and "Estimated paper cash-out" in existing:
        return ""
    return (
        f" Estimated paper cash-out ${offer:.2f} "
        f"({PAPER_ESTIMATED_CASHOUT_HAIRCUT:.0%} haircut on MTM gap; "
        "not scraped Open Bets)."
    )


def _cashout_apply_update(
    mv: PaperMovement,
    offer: float | None,
    estimated: bool,
) -> dict:
    if offer is None:
        return {}
    extra = _estimated_amount_suffix(offer, estimated, mv.amount_plain or "")
    return {
        "cashout_quote": offer,
        "cashout_estimated": estimated,
        "amount_plain": (mv.amount_plain or "") + extra,
    }


def _maybe_post_sell_cashout(
    *,
    record: PaperBookFile,
    mv: PaperMovement,
    sold: float,
    entry_odds: float | None,
    player_name: str,
) -> tuple[float | None, bool, bool]:
    """Returns (offer, estimated, posted_to_ledger). Missing live posted stays at cost."""
    from golf_offshoot.strategy.cashout import (
        estimated_cashout_ledger_token,
        typed_cashout_ledger_token,
    )
    from golf_offshoot.strategy.paper_ledger import (
        cashout_recorded_for,
        load_ledger,
        record_cashout,
    )

    sold_f = round(float(sold), 2)
    if sold_f <= 0:
        return None, False, False
    typed = (
        mv.cashout_quote is not None
        and mv.cashout_quote > 0
        and not mv.cashout_estimated
    )
    if typed:
        offer = round(float(mv.cashout_quote), 2)
        estimated = False
    else:
        offer = estimated_cashout_offer(sold_f, entry_odds, mv.decimal_odds)
        if offer is None:
            return None, False, False
        if abs(offer - sold_f) < 0.005:
            return None, False, False
        estimated = True
    if cashout_recorded_for(mv.movement_id):
        return offer, estimated, False
    if getattr(record, "independent_bankroll", False):
        record.bankroll = round(float(record.bankroll) + (offer - sold_f), 2)
        return offer, estimated, False
    led = load_ledger()
    if not led.entries:
        return offer, estimated, False
    if estimated:
        live = float(mv.decimal_odds or 0.0)
        entry = float(entry_odds or 0.0)
        token = estimated_cashout_ledger_token(mv.movement_id)
        note = (
            f"estimated paper cash-out ${offer:.2f} on sold ${sold_f:.2f} "
            f"@ {entry:.2f} live {live:.2f} haircut={PAPER_ESTIMATED_CASHOUT_HAIRCUT:.0%} "
            f"(not scraped Open Bets) {token}"
        )
    else:
        token = typed_cashout_ledger_token(mv.movement_id)
        entry = float(entry_odds or 0.0)
        note = (
            f"paper cash-out ${offer:.2f} on ${sold_f:.2f} "
            f"@ {entry:.2f} {token}"
        )
    record_cashout(
        stake=sold_f,
        cashout=offer,
        event_id=record.tournament_id,
        event_name=record.tournament_name,
        player_name=player_name,
        note=note,
    )
    return offer, estimated, True


def _entry_odds_for(record: PaperBookFile, position_id: str) -> float | None:
    for pos in record.book.positions:
        if pos.position_id == position_id and pos.decimal_odds and pos.decimal_odds > 1.0:
            return float(pos.decimal_odds)
    for mv in record.movements:
        if mv.kind == "lock" and mv.position_id == position_id:
            if mv.decimal_odds and mv.decimal_odds > 1.0:
                return float(mv.decimal_odds)
    return None


def backfill_estimated_cashouts(record: PaperBookFile) -> PaperBookFile:
    """Book estimated cash-out P/L for applied reduce/exit that never got a quote.

    Idempotent via the movement token on the ledger note. Does not change remaining
    ticket stakes. Typed quotes are left alone.
    """
    from golf_offshoot.strategy.paper_ledger import load_ledger

    updated: list[PaperMovement] = []
    posted_any = False
    for mv in record.movements:
        if mv.status != "applied" or mv.kind not in {"reduce", "exit"}:
            updated.append(mv)
            continue
        if mv.cashout_quote is not None and mv.cashout_quote > 0 and not mv.cashout_estimated:
            updated.append(mv)
            continue
        sold = _sold_from_movement(mv)
        entry = _entry_odds_for(record, mv.position_id)
        offer, estimated, posted = _maybe_post_sell_cashout(
            record=record,
            mv=mv,
            sold=sold,
            entry_odds=entry,
            player_name=mv.player_name,
        )
        posted_any = posted_any or posted
        if offer is None:
            updated.append(mv)
            continue
        updated.append(mv.model_copy(update=_cashout_apply_update(mv, offer, estimated)))
    record.movements = updated
    if posted_any:
        led = load_ledger()
        if led.entries:
            record.bankroll = led.bankroll
            record.book = record.book.model_copy(update={"bankroll": led.bankroll})
        note = (
            "Backfilled estimated paper cash-out on applied sells "
            f"({PAPER_ESTIMATED_CASHOUT_HAIRCUT:.0%} MTM-gap haircut; not scraped Open Bets)."
        )
        if note not in record.notes:
            record.notes = list(record.notes) + [note]
    return record


def apply_advice(record: PaperBookFile, advice: list[PaperMovement]) -> PaperBookFile:
    """Apply advised sells/adds/reallocates to the mock book. Still never real money."""
    from golf_offshoot.strategy.paper_ledger import load_ledger

    positions = list(record.book.positions)
    by_id = {p.position_id: i for i, p in enumerate(positions)}
    applied: list[PaperMovement] = []
    booked_cashout = False
    for mv in advice:
        if mv.kind == "hold":
            continue
        if mv.kind == "exit" and mv.position_id in by_id:
            i = by_id[mv.position_id]
            pos = positions[i]
            sold = round(pos.stake, 2)
            offer, estimated, posted = _maybe_post_sell_cashout(
                record=record,
                mv=mv,
                sold=sold,
                entry_odds=pos.decimal_odds,
                player_name=pos.player_name,
            )
            booked_cashout = booked_cashout or posted
            applied.append(
                mv.model_copy(
                    update={
                        "status": "applied",
                        "stake_after": 0.0,
                        "stake_delta": -sold,
                        **_cashout_apply_update(mv, offer, estimated),
                    }
                )
            )
            positions.pop(i)
            by_id = {p.position_id: j for j, p in enumerate(positions)}
            continue
        if mv.kind == "reduce" and mv.position_id in by_id:
            i = by_id[mv.position_id]
            pos = positions[i]
            after = round(max(0.0, pos.stake + mv.stake_delta), 2)
            if after < 0.002 * record.bankroll:
                sold = round(pos.stake, 2)
                after = 0.0
                popped = True
            else:
                sold = round(pos.stake - after, 2)
                popped = False
            offer, estimated, posted = _maybe_post_sell_cashout(
                record=record,
                mv=mv,
                sold=sold,
                entry_odds=pos.decimal_odds,
                player_name=pos.player_name,
            )
            booked_cashout = booked_cashout or posted
            update = {
                "status": "applied",
                "stake_after": after,
                **_cashout_apply_update(mv, offer, estimated),
            }
            if popped:
                update["stake_delta"] = -sold
                positions.pop(i)
            else:
                positions[i] = pos.model_copy(update={"stake": after, "notes": f"{pos.notes}; paper reduce"})
            applied.append(mv.model_copy(update=update))
            by_id = {p.position_id: j for j, p in enumerate(positions)}
            continue
        if mv.kind == "add" and mv.position_id in by_id:
            i = by_id[mv.position_id]
            pos = positions[i]
            cap = record.bankroll * scaled_single_cap(
                StrategyConfig(enabled=True, bankroll=record.bankroll)
            )
            after = round(min(cap, pos.stake + max(0.0, mv.stake_delta)), 2)
            positions[i] = pos.model_copy(update={"stake": after, "notes": f"{pos.notes}; paper add"})
            applied.append(mv.model_copy(update={"status": "applied", "stake_after": after, "stake_delta": after - pos.stake}))
            continue
        if mv.kind == "new_bet" and mv.stake_delta > 0:
            filled = hydrate_new_bet_movement(mv)
            if filled.decimal_odds is None or filled.decimal_odds <= 1.0:
                continue
            bet = BetType(filled.bet_type) if filled.bet_type in {b.value for b in BetType} else BetType.WIN
            if any(p.player_id == filled.player_id and p.bet_type == bet for p in positions):
                continue
            positions.append(
                StrategyPosition(
                    position_id=new_id("paper"),
                    player_id=filled.player_id,
                    player_name=filled.player_name,
                    bet_type=bet,
                    stake=round(filled.stake_delta, 2),
                    decimal_odds=filled.decimal_odds,
                    entry_edge=filled.edge_w or 0.0,
                    entry_model_p=filled.model_win or 0.0,
                    notes="paper new_bet applied from advice",
                    user_recorded=True,
                    proposed=False,
                )
            )
            applied.append(filled.model_copy(update={"status": "applied", "stake_after": round(filled.stake_delta, 2)}))
            continue
        if mv.kind == "reallocate" and mv.stake_delta > 0:
            take = abs(mv.stake_delta)
            donor_i = None
            if mv.from_player_name:
                for j, p in enumerate(positions):
                    if p.player_name == mv.from_player_name:
                        donor_i = j
                        break
            if donor_i is not None:
                donor = positions[donor_i]
                take = min(take, donor.stake)
                left = round(donor.stake - take, 2)
                if left < 0.002 * record.bankroll:
                    positions.pop(donor_i)
                else:
                    positions[donor_i] = donor.model_copy(update={"stake": left})
            target = next((j for j, p in enumerate(positions) if p.player_id == mv.player_id), None)
            if target is None:
                positions.append(
                    StrategyPosition(
                        position_id=new_id("paper"),
                        player_id=mv.player_id,
                        player_name=mv.player_name,
                        bet_type=BetType.WIN,
                        stake=round(take, 2),
                        decimal_odds=mv.decimal_odds or 0.0,
                        entry_edge=mv.edge_w or 0.0,
                        entry_model_p=mv.model_win or 0.0,
                        notes="paper reallocate applied from advice",
                        user_recorded=True,
                        proposed=False,
                    )
                )
            else:
                pos = positions[target]
                positions[target] = pos.model_copy(update={"stake": round(pos.stake + take, 2)})
            applied.append(mv.model_copy(update={"status": "applied", "stake_delta": take}))
    book_update = {"positions": positions}
    if booked_cashout and not getattr(record, "independent_bankroll", False):
        led = load_ledger()
        if led.entries:
            record.bankroll = led.bankroll
            book_update["bankroll"] = led.bankroll
    elif getattr(record, "independent_bankroll", False):
        book_update["bankroll"] = record.bankroll
    record.book = record.book.model_copy(update=book_update)
    record.movements = list(record.movements) + applied
    return record


def paper_dir() -> Path:
    d = package_data_dir() / "paper"
    d.mkdir(parents=True, exist_ok=True)
    return d


def paper_book_path(event_id: str, path_id: str = "lived") -> Path:
    safe = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in str(event_id))
    stem = safe or "event"
    if not path_id or path_id == "lived":
        return paper_dir() / f"{stem}.json"
    return paper_dir() / f"{stem}_{path_id}.json"


def load_paper_book(event_id: str, path_id: str = "lived") -> PortfolioState | None:
    rec = load_paper_file(event_id, path_id=path_id)
    return rec.book if rec else None


def load_paper_file(event_id: str, path_id: str = "lived") -> PaperBookFile | None:
    path = paper_book_path(event_id, path_id)
    if not path.is_file():
        return None
    return PaperBookFile.model_validate_json(path.read_text(encoding="utf-8"))


def save_paper_book(record: PaperBookFile) -> Path:
    path = paper_book_path(record.tournament_id, getattr(record, "path_id", None) or "lived")
    path.write_text(record.model_dump_json(indent=2), encoding="utf-8")
    return path


def iter_paper_files() -> list[PaperBookFile]:
    """All per-event paper books. Skips the lifetime ledger file."""
    out: list[PaperBookFile] = []
    if not paper_dir().is_dir():
        return out
    for path in sorted(paper_dir().glob("*.json")):
        if path.name.lower() == "ledger.json":
            continue
        try:
            rec = PaperBookFile.model_validate_json(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if (rec.path_id or "lived") != "lived":
            continue
        out.append(rec)
    return out


def unsettled_paper_files() -> list[PaperBookFile]:
    return [rec for rec in iter_paper_files() if rec.settled_at is None]


def _posted(row: PlayerOutput, bet: BetType = BetType.WIN) -> float | None:
    posted = row.posted_odds_by_bet.get(bet.value)
    if posted and posted > 1.0:
        return float(posted)
    return None


def _hard_pass(row: PlayerOutput) -> bool:
    return bool(_HARD_PASS.intersection(row.flags))


def paper_candidates(
    rows: list[PlayerOutput],
    bet: BetType = BetType.WIN,
    *,
    require_cleared: bool = False,
    ticket_screen: str = "both",
    min_edge: float = MIN_EDGE_TO_CONSIDER,
) -> list[PlayerOutput]:
    """Clean names with a real quote, screened by ticket law.

    both (lived): EdgeW > 0 and vs-posted > 0; cleared first, then observation.
    edgew (A-replay / B-guts): EdgeW >= min_edge; vs-posted may be short.
    posted (B-nerves / B-full): vs-posted >= min_edge; EdgeW-only names are out.
    require_cleared=True drops observation names on the lived both-screen.
    """
    screen = (ticket_screen or "both").lower()
    cleared: list[tuple[float, PlayerOutput]] = []
    observation: list[tuple[float, PlayerOutput]] = []
    for row in rows:
        if _hard_pass(row):
            continue
        odds = _posted(row, bet)
        if not odds:
            continue
        edge = row.edge_by_bet.get(bet.value)
        hp = row.probabilities.p(_BET_HORIZON[bet])
        posted_edge = hp.central - 1.0 / odds
        if screen == "edgew":
            if edge is None or edge < min_edge:
                continue
            bucket = cleared
            key = float(edge)
        elif screen == "posted":
            if posted_edge < min_edge:
                continue
            bucket = cleared
            key = float(posted_edge)
        else:
            if edge is None or edge <= 0:
                continue
            if posted_edge <= 0:
                continue
            bucket = cleared if screen_cleared(edge, posted_edge) else observation
            key = float(edge)
        bucket.append((key, row))
    cleared.sort(key=lambda t: t[0], reverse=True)
    observation.sort(key=lambda t: t[0], reverse=True)
    if require_cleared or screen == "posted":
        return [r for _, r in cleared]
    return [r for _, r in cleared] + [r for _, r in observation]


def lock_paper_positions(
    rows: list[PlayerOutput],
    config: StrategyConfig,
    *,
    event_id: str,
    event_name: str = "",
    run_id: str = "",
    odds_book: str = "",
    extra_export_files: list[Path] | None = None,
    require_cleared: bool = False,
    path_id: str = "lived",
    independent_bankroll: bool = False,
    write_exports: bool = True,
    method_law_hash: str = "",
) -> PaperBookFile:
    """Accept a mock book at conservative caps. Does not place a real bet."""
    from golf_offshoot.strategy.paper_ledger import (
        ensure_opening_deposit,
        load_ledger,
        working_bankroll,
    )

    if not independent_bankroll:
        existing = load_ledger()
        if existing.entries:
            config = config.model_copy(
                update={"bankroll": working_bankroll(except_event_id=str(event_id))}
            )
    unit = config.bankroll * scaled_single_cap(config)
    positions: list[StrategyPosition] = []
    open_exp = 0.0
    screen = (config.ticket_screen or "both").lower()
    notes = [
        "PAPER / MOCK bankroll. Not real money. The system never places bets.",
        "Locked so a later live run can suggest hold, sell, add, or reallocate.",
        observation_plain(),
        observation_technical(),
        (
            f"Cleared stake = full unit ${unit:.2f}. Observation stake = "
            f"{PAPER_OBSERVATION_STAKE_FRAC:.0%} of unit "
            f"${unit * PAPER_OBSERVATION_STAKE_FRAC:.2f}."
        ),
        f"path_id={path_id} ticket_screen={screen} independent_bankroll={independent_bankroll}",
    ]
    for row in paper_candidates(
        rows,
        require_cleared=require_cleared,
        ticket_screen=screen,
    ):
        cap = remaining_exposure_capacity(open_exp, config.bankroll, config)
        odds = _posted(row) or 0.0
        hp = row.probabilities.p(Horizon.WIN)
        posted_edge = posted_price_edge(hp.central, odds)
        edge = row.edge_by_bet.get("win") or 0.0
        if screen in ("edgew", "posted"):
            cleared = True
        else:
            cleared = screen_cleared(edge, posted_edge)
        tag = lane_tag(cleared)
        want = unit if cleared else unit * PAPER_OBSERVATION_STAKE_FRAC
        stake = min(want, cap)
        if stake < 0.002 * config.bankroll:
            break
        screen_txt = screen_plain(edge, posted_edge)
        positions.append(
            StrategyPosition(
                position_id=new_id("paper"),
                player_id=row.player_id,
                player_name=row.name,
                bet_type=BetType.WIN,
                stake=round(stake, 2),
                decimal_odds=odds,
                entry_edge=edge,
                entry_model_p=hp.central,
                entry_market_p=row.market_implied_by_bet.get("win"),
                notes=f"paper lock {tag}; {screen_txt}",
                user_recorded=True,
                proposed=False,
            )
        )
        open_exp += stake
        notes.append(
            f"{tag} {row.name} win stake={stake:.2f} @ {odds:.2f} EdgeW={edge:+.3f} "
            f"posted_edge={posted_edge:+.3f} ({screen_txt})"
        )
    if not positions:
        notes.append("No clean names to lock under this path's ticket screen.")
    book = PortfolioState(
        bankroll=config.bankroll,
        positions=positions,
        session_label=f"paper-{config.bankroll:.0f}",
    )
    record = PaperBookFile(
        tournament_id=str(event_id),
        tournament_name=event_name,
        bankroll=config.bankroll,
        locked_from_run_id=run_id,
        odds_book=odds_book,
        risk=config.risk.value,
        mode=config.mode.value,
        notes=notes,
        book=book,
        path_id=path_id or "lived",
        independent_bankroll=bool(independent_bankroll),
        method_law_hash=method_law_hash,
    )
    tickets = ticket_rows(record)
    by_name = {p.player_name: p for p in positions}
    record.movements = [
        lock_movement_for_ticket(
            t,
            position_id=by_name[t.player_name].position_id,
            player_id=by_name[t.player_name].player_id,
            config=config,
            run_id=run_id,
        )
        for t in tickets
        if t.player_name in by_name
    ]
    save_paper_book(record)
    if not independent_bankroll:
        ensure_opening_deposit(
            config.bankroll,
            event_id=str(event_id),
            event_name=event_name,
            note=f"opening paper bankroll for {event_name or event_id}",
        )
    if write_exports:
        from golf_offshoot.strategy.paper_export import write_paper_book_files

        write_paper_book_files(record, directory=package_data_dir() / "exports")
        from golf_offshoot.strategy.paper_pack import write_paper_pack

        write_paper_pack(record, extra_files=extra_export_files)
    return record


def format_paper_book(record: PaperBookFile) -> str:
    frac = (record.book.open_exposure / record.bankroll) if record.bankroll else 0.0
    cash = record.bankroll - record.book.open_exposure
    lines = [
        f"PAPER BOOK {record.tournament_name or record.tournament_id} "
        f"path={getattr(record, 'path_id', None) or 'lived'} "
        f"${record.bankroll:.0f} mock  never_auto_bet=true",
        f"locked_at={record.locked_at.isoformat()} run={record.locked_from_run_id} "
        f"odds_book={record.odds_book or 'n/a'}",
        f"open ${record.book.open_exposure:.2f} / ${record.bankroll:.2f} "
        f"({frac:.0%}) cash ${cash:.2f} n={len(record.book.positions)}",
        "Observation only:",
        observation_plain(),
        observation_technical(),
    ]
    for t in ticket_rows(record):
        lines.append(
            f"  {t.lane} {t.player_name} {t.market} ${t.stake:.2f} @ {t.posted:.2f} "
            f"model={t.model_win:.3f} EdgeW={t.edge_w:+.3f} vs_posted={t.posted_edge:+.3f} "
            f"if_wins=${t.if_wins:.2f}"
        )
        lines.append(f"    {t.screen}")
    if record.export_pdf:
        lines.append(f"paper book PDF: {record.export_pdf}")
    if record.latest_pack:
        lines.append(f"paper pack: {record.latest_pack}")
    lines.append("Observation only. Come back mid-round to mark / sell / reallocate. Never auto-bet.")
    return "\n".join(lines)
