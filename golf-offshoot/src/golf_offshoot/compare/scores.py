"""Winner vs place posted P/L for compare books. Never auto-bets. Never real money."""

from __future__ import annotations

from golf_offshoot.compare.paths import COMPARE_LEDGERS, compare_allows_place, ledger_id
from golf_offshoot.models.enums import BetType
from golf_offshoot.strategy.paper_book import PaperBookFile, load_paper_file
from golf_offshoot.strategy.paper_ledger import TicketResult, ticket_hit

_PLACE = {"top_5", "top_10", "top_20", "make_cut"}


def is_place_bet(bet_type: str | BetType) -> bool:
    return str(getattr(bet_type, "value", bet_type) or "win").lower() in _PLACE


def split_pnl(tickets: list[TicketResult] | None = None, *, record: PaperBookFile | None = None) -> tuple[float, float, float]:
    """(win_pnl, place_pnl, total). Open books report 0 until settled."""
    if record is not None and record.settlement_pnl_win is not None:
        win = float(record.settlement_pnl_win)
        place = float(record.settlement_pnl_place or 0.0)
        total = float(record.settlement_pnl if record.settlement_pnl is not None else win + place)
        return round(win, 2), round(place, 2), round(total, 2)
    win = 0.0
    place = 0.0
    for t in tickets or []:
        if is_place_bet(t.bet_type):
            place = round(place + t.pnl, 2)
        else:
            win = round(win + t.pnl, 2)
    return win, place, round(win + place, 2)


def split_open_exposure(record: PaperBookFile) -> tuple[float, float]:
    win = 0.0
    place = 0.0
    for pos in record.book.positions:
        if is_place_bet(pos.bet_type):
            place += pos.stake
        else:
            win += pos.stake
    return round(win, 2), round(place, 2)


def tickets_from_positions(
    record: PaperBookFile,
    *,
    finishes: dict[str, tuple[int | None, str]],
    winner_ids: set[str],
) -> list[TicketResult]:
    tickets: list[TicketResult] = []
    for pos in list(record.book.positions):
        place, _nm = finishes.get(pos.player_id, (None, pos.player_name))
        won = ticket_hit(pos.bet_type.value, place, winner_ids, pos.player_id)
        payout = round(pos.stake * pos.decimal_odds, 2) if won else 0.0
        pnl = round(payout - pos.stake, 2)
        tickets.append(
            TicketResult(
                player_id=pos.player_id,
                player_name=pos.player_name,
                bet_type=pos.bet_type.value,
                stake=pos.stake,
                decimal_odds=pos.decimal_odds,
                finish=place,
                won=won,
                payout=payout,
                pnl=pnl,
                note=(
                    f"{'HIT' if won else 'MISS'} finish={place if place is not None else 'n/a'} "
                    f"stake={pos.stake:.2f} @ {pos.decimal_odds:.2f} payout={payout:.2f} pnl={pnl:+.2f}"
                ),
            )
        )
    return tickets


def path_score_row(record: PaperBookFile | None, path_id: str) -> dict:
    if record is None:
        return {
            "path_id": path_id,
            "n": 0,
            "open_win": 0.0,
            "open_place": 0.0,
            "posted_price_pnl_win": None,
            "posted_price_pnl_place": None,
            "posted_price_pnl": None,
            "settled": False,
        }
    open_win, open_place = split_open_exposure(record)
    win_pnl, place_pnl, total = split_pnl(record=record)
    settled = bool(record.settled_at)
    return {
        "path_id": path_id,
        "n": len(record.book.positions),
        "open_win": open_win,
        "open_place": open_place,
        "posted_price_pnl_win": win_pnl if settled else None,
        "posted_price_pnl_place": place_pnl if settled else None,
        "posted_price_pnl": total if settled else None,
        "settled": settled,
        "bankroll": record.bankroll,
    }


def event_scoreboard(event_id: str) -> dict:
    rows = []
    for path in COMPARE_LEDGERS:
        pid = ledger_id(path)
        rec = load_paper_file(event_id, path_id=pid)
        rows.append(path_score_row(rec, pid))
    return {
        "event_id": event_id,
        "place_allowed": compare_allows_place(event_id),
        "never_auto_bet": True,
        "paths": rows,
        "note": (
            "Winner and place posted P/L are separate lines. "
            "Do not blend them. Place tickets require a real coupon."
        ),
    }


def scoreboard_lines(event_id: str) -> list[str]:
    board = event_scoreboard(event_id)
    place = "on (real coupon only)" if board["place_allowed"] else "off (St. Jude Winner-only freeze)"
    lines = [
        f"compare scores event={event_id} place={place}",
        "  path        open_win open_place  pnl_win pnl_place   pnl  settled",
    ]
    for row in board["paths"]:
        pw = "n/a" if row["posted_price_pnl_win"] is None else f"{row['posted_price_pnl_win']:+.2f}"
        pp = "n/a" if row["posted_price_pnl_place"] is None else f"{row['posted_price_pnl_place']:+.2f}"
        pt = "n/a" if row["posted_price_pnl"] is None else f"{row['posted_price_pnl']:+.2f}"
        lines.append(
            f"  {row['path_id']:10} ${row['open_win']:7.2f} ${row['open_place']:8.2f}  "
            f"{pw:>7} {pp:>9} {pt:>6}  {str(row['settled']).lower()}"
        )
    lines.append("  Winner P/L and place P/L stay separate. Never invent place from Winner odds.")
    return lines
