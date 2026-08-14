"""Paper (mock) bankroll for one event. Never auto-bets. Never real money."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel, Field

from golf_offshoot.config import MIN_EDGE_TO_CONSIDER
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


def juice_plain() -> str:
    return observation_plain()


def posted_price_edge(model_p: float, decimal_odds: float) -> float:
    if decimal_odds <= 1.0:
        return model_p
    return float(model_p) - 1.0 / float(decimal_odds)


def screen_cleared(edge_w: float, posted_edge: float) -> bool:
    return edge_w >= MIN_EDGE_TO_CONSIDER and posted_edge >= MIN_EDGE_TO_CONSIDER


def screen_plain(edge_w: float, posted_edge: float) -> str:
    if screen_cleared(edge_w, posted_edge):
        return "Cleared — model still beats the posted price by at least 3 percentage points"
    if posted_edge > 0:
        return (
            f"Short of 3pp vs the posted price ({posted_edge * 100:+.1f}pp). "
            "Live juice makes the number you would actually buy harder to beat than the fair EdgeW."
        )
    return "Does not beat the posted price. The book is already shorter than the model."


def ticket_rows(record: PaperBookFile) -> list[PaperTicketRow]:
    rows: list[PaperTicketRow] = []
    for p in record.book.positions:
        posted_edge = posted_price_edge(p.entry_model_p, p.decimal_odds)
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
            )
        )
    return rows


def sizing_plain(config: StrategyConfig) -> str:
    unit = config.bankroll * scaled_single_cap(config)
    total = config.bankroll * scaled_exposure_cap(config)
    return (
        f"Each name is capped at {scaled_single_cap(config):.1%} of the "
        f"${config.bankroll:.0f} paper bankroll (${unit:.2f}). That is a 5% single-name "
        "ceiling times a 70% conservative haircut. It is a concentration rule, not a "
        "fitted Kelly size. Kelly after the uncertainty haircut is usually much smaller; "
        "this paper lock uses the cap as the stake so the tickets are visible to track. "
        "Two names can get the same dollar amount because both hit that per-name ceiling, "
        "not because they have the same edge. Cash left is unused room under the "
        f"{scaled_exposure_cap(config):.0%} total cap (${total:.2f}) plus everything above it."
    )


def sizing_technical(config: StrategyConfig) -> str:
    return (
        "scaled_single_cap = max_single_position_frac (0.05) * conservative risk 0.70 = 0.035. "
        "scaled_exposure_cap = 0.20 * 0.70 = 0.14. Paper lock unit = bankroll * scaled_single_cap. "
        "Advisory size is fractional Kelly (0.25) * range haircut * reliability * risk 0.40 * "
        "stay_selective 0.70, then min(unit, remaining total cap). The paper lock does not use "
        "that Kelly figure as the stake; it uses the unit cap."
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
    why_name_plain = (
        f"{ticket.player_name} is in the book because the winner quote was real and still "
        f"beat the posted number (model {ticket.model_win * 100:.1f}% vs 1/odds "
        f"{(1.0 / ticket.posted) * 100:.1f}%, EdgeW {ticket.edge_w * 100:+.1f}pp, "
        f"vs posted {ticket.posted_edge * 100:+.1f}pp). {ticket.screen}"
    )
    why_name_tech = (
        f"kind=lock status=applied bet=win posted={ticket.posted:.2f} "
        f"model_p={ticket.model_win:.3f} EdgeW={ticket.edge_w:+.3f} "
        f"posted_edge={ticket.posted_edge:+.3f} screen_cleared={ticket.cleared}"
    )
    hit_cap = abs(ticket.stake - unit) < 0.02
    amount_plain = (
        f"${ticket.stake:.2f} is the conservative single-name cap "
        f"({scaled_single_cap(config):.1%} of ${config.bankroll:.0f})."
        if hit_cap
        else f"${ticket.stake:.2f} is what remained under the total exposure cap."
    )
    amount_plain += (
        " Same dollars as another name means both hit the cap, not that the edges matched. "
        "Kelly after the uncertainty haircut would usually be smaller."
    )
    amount_tech = (
        f"stake={ticket.stake:.2f} unit_cap={unit:.2f} "
        f"total_cap={config.bankroll * scaled_exposure_cap(config):.2f} "
        f"mode={config.mode.value} risk={config.risk.value}"
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
        "Sell the whole paper ticket. The original edge has collapsed versus the live market."
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
        amount_plain = _advice_amount_plain(kind, before, delta, after)
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
                decimal_odds=pos.decimal_odds if pos else None,
                run_id=run_id,
                reason_plain=plain,
                reason_technical=f"kind={kind} reason={act.reason}{warn} details={details}",
                amount_plain=amount_plain,
                amount_technical=(
                    f"delta={delta:+.2f} unit={act.suggested_unit:.2f} "
                    f"before={before:.2f} after={after if after is not None else 'n/a'}"
                ),
            )
        )
    return out


def _advice_amount_plain(kind: str, before: float, delta: float, after: float | None) -> str:
    if kind == "hold":
        return f"Stake stays ${before:.2f}. Hold is a size of zero change, not a new bet."
    if kind == "exit":
        return f"Sell ${before:.2f} back to cash (paper). After = $0.00."
    if kind == "reduce":
        after_s = f"${after:.2f}" if after is not None else "n/a"
        return (
            f"Sell ${abs(delta):.2f} of the ${before:.2f} ticket "
            f"(after {after_s} if applied). Fraction of current stake, not a Kelly resize."
        )
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


def apply_advice(record: PaperBookFile, advice: list[PaperMovement]) -> PaperBookFile:
    """Apply advised sells/adds/reallocates to the mock book. Still never real money."""
    positions = list(record.book.positions)
    by_id = {p.position_id: i for i, p in enumerate(positions)}
    applied: list[PaperMovement] = []
    for mv in advice:
        if mv.kind == "hold":
            continue
        if mv.kind == "exit" and mv.position_id in by_id:
            i = by_id[mv.position_id]
            pos = positions[i]
            applied.append(mv.model_copy(update={"status": "applied", "stake_after": 0.0, "stake_delta": -pos.stake}))
            positions.pop(i)
            by_id = {p.position_id: j for j, p in enumerate(positions)}
            continue
        if mv.kind == "reduce" and mv.position_id in by_id:
            i = by_id[mv.position_id]
            pos = positions[i]
            after = round(max(0.0, pos.stake + mv.stake_delta), 2)
            if after < 0.002 * record.bankroll:
                applied.append(mv.model_copy(update={"status": "applied", "stake_after": 0.0, "stake_delta": -pos.stake}))
                positions.pop(i)
            else:
                positions[i] = pos.model_copy(update={"stake": after, "notes": f"{pos.notes}; paper reduce"})
                applied.append(mv.model_copy(update={"status": "applied", "stake_after": after}))
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
            positions.append(
                StrategyPosition(
                    position_id=new_id("paper"),
                    player_id=mv.player_id,
                    player_name=mv.player_name,
                    bet_type=BetType(mv.bet_type) if mv.bet_type in {b.value for b in BetType} else BetType.WIN,
                    stake=round(mv.stake_delta, 2),
                    decimal_odds=mv.decimal_odds or 0.0,
                    entry_edge=mv.edge_w or 0.0,
                    entry_model_p=mv.model_win or 0.0,
                    notes="paper new_bet applied from advice",
                    user_recorded=True,
                    proposed=False,
                )
            )
            applied.append(mv.model_copy(update={"status": "applied", "stake_after": round(mv.stake_delta, 2)}))
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
    record.book = record.book.model_copy(update={"positions": positions})
    record.movements = list(record.movements) + applied
    return record


def paper_dir() -> Path:
    d = package_data_dir() / "paper"
    d.mkdir(parents=True, exist_ok=True)
    return d


def paper_book_path(event_id: str) -> Path:
    safe = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in str(event_id))
    return paper_dir() / f"{safe or 'event'}.json"


def load_paper_book(event_id: str) -> PortfolioState | None:
    path = paper_book_path(event_id)
    if not path.is_file():
        return None
    payload = PaperBookFile.model_validate_json(path.read_text(encoding="utf-8"))
    return payload.book


def load_paper_file(event_id: str) -> PaperBookFile | None:
    path = paper_book_path(event_id)
    if not path.is_file():
        return None
    return PaperBookFile.model_validate_json(path.read_text(encoding="utf-8"))


def save_paper_book(record: PaperBookFile) -> Path:
    path = paper_book_path(record.tournament_id)
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
            out.append(PaperBookFile.model_validate_json(path.read_text(encoding="utf-8")))
        except (OSError, ValueError):
            continue
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


def paper_candidates(rows: list[PlayerOutput], bet: BetType = BetType.WIN) -> list[PlayerOutput]:
    """Clean names with a real quote that still beats the posted number."""
    scored: list[tuple[float, PlayerOutput]] = []
    for row in rows:
        if _hard_pass(row):
            continue
        odds = _posted(row, bet)
        if not odds:
            continue
        edge = row.edge_by_bet.get(bet.value)
        if edge is None or edge <= 0:
            continue
        hp = row.probabilities.p(_BET_HORIZON[bet])
        posted_edge = hp.central - 1.0 / odds
        if posted_edge <= 0:
            continue
        scored.append((edge, row))
    scored.sort(key=lambda t: t[0], reverse=True)
    preferred = [r for e, r in scored if e >= MIN_EDGE_TO_CONSIDER]
    if preferred:
        return preferred
    return [r for _, r in scored]


def lock_paper_positions(
    rows: list[PlayerOutput],
    config: StrategyConfig,
    *,
    event_id: str,
    event_name: str = "",
    run_id: str = "",
    odds_book: str = "",
    extra_export_files: list[Path] | None = None,
) -> PaperBookFile:
    """Accept a mock book at conservative caps. Does not place a real bet."""
    from golf_offshoot.strategy.paper_ledger import (
        ensure_opening_deposit,
        load_ledger,
        working_bankroll,
    )

    existing = load_ledger()
    if existing.entries:
        config = config.model_copy(
            update={"bankroll": working_bankroll(except_event_id=str(event_id))}
        )
    unit = config.bankroll * scaled_single_cap(config)
    positions: list[StrategyPosition] = []
    open_exp = 0.0
    notes = [
        "PAPER / MOCK bankroll. Not real money. The system never places bets.",
        "Locked so a later live run can suggest hold, sell, add, or reallocate.",
        observation_plain(),
        observation_technical(),
    ]
    for row in paper_candidates(rows):
        cap = remaining_exposure_capacity(open_exp, config.bankroll, config)
        stake = min(unit, cap)
        if stake < 0.002 * config.bankroll:
            break
        odds = _posted(row) or 0.0
        hp = row.probabilities.p(Horizon.WIN)
        posted_edge = posted_price_edge(hp.central, odds)
        edge = row.edge_by_bet.get("win") or 0.0
        screen = screen_plain(edge, posted_edge)
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
                notes=f"paper lock; {screen}",
                user_recorded=True,
                proposed=False,
            )
        )
        open_exp += stake
        notes.append(
            f"{row.name} win stake={stake:.2f} @ {odds:.2f} EdgeW={edge:+.3f} "
            f"posted_edge={posted_edge:+.3f} ({screen})"
        )
    if not positions:
        notes.append("No clean positive posted-edge names to lock.")
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
    ensure_opening_deposit(
        config.bankroll,
        event_id=str(event_id),
        event_name=event_name,
        note=f"opening paper bankroll for {event_name or event_id}",
    )
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
            f"  {t.player_name} {t.market} ${t.stake:.2f} @ {t.posted:.2f} "
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
