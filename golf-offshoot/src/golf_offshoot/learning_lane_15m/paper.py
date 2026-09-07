"""15-min paper journal. Reuses golf PaperBookFile / PaperLedger schemas.

Writes only under the 15-min artifact root. Golf paper_dir is never used.
Paper autobet is a mechanical observation probe — no claimed edge.
Trading is never armed. AI never deposit / withdraw / transfer.
"""

from __future__ import annotations

import json

from golf_offshoot.learning_lane_15m.paths import (
    LANE_15M,
    PRIMARY_SERIES,
    assert_not_golf_path,
    paper_dir_15m,
    shadow_dir_15m,
)
from golf_offshoot.localtime import now
from golf_offshoot.models.enums import BetType
from golf_offshoot.models.strategy import PortfolioState, StrategyPosition, new_id
from golf_offshoot.strategy.paper_book import PaperBookFile, PaperMovement
from golf_offshoot.strategy.paper_ledger import LedgerEntry, PaperLedger

PAPER_OBSERVATION_SEED = 100.0
PAPER_UNIT = 1.0
PATH_ID = "learning_lane_15m"
TRADING_ARMED = False

# Not a user deposit. Seed so the paper loop can run without a cash UI.
_SEED_KIND = "observation_seed"


def ledger_path() -> Path:
    path = paper_dir_15m() / "ledger.json"
    assert_not_golf_path(path)
    return path


def book_path(event_ticker: str) -> Path:
    safe = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in str(event_ticker))
    path = paper_dir_15m() / f"{safe or 'event'}.json"
    assert_not_golf_path(path)
    return path


def shadow_path() -> Path:
    path = shadow_dir_15m() / "advises.jsonl"
    assert_not_golf_path(path)
    return path


def load_ledger() -> PaperLedger:
    path = ledger_path()
    if not path.is_file():
        return PaperLedger()
    return PaperLedger.model_validate_json(path.read_text(encoding="utf-8"))


def save_ledger(ledger: PaperLedger) -> Path:
    path = ledger_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    assert_not_golf_path(path)
    path.write_text(ledger.model_dump_json(indent=2), encoding="utf-8")
    return path


def load_book(event_ticker: str) -> PaperBookFile | None:
    path = book_path(event_ticker)
    if not path.is_file():
        return None
    return PaperBookFile.model_validate_json(path.read_text(encoding="utf-8"))


def save_book(record: PaperBookFile) -> Path:
    path = book_path(record.tournament_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    assert_not_golf_path(path)
    path.write_text(record.model_dump_json(indent=2), encoding="utf-8")
    return path


def iter_books() -> list[PaperBookFile]:
    out: list[PaperBookFile] = []
    root = paper_dir_15m()
    if not root.is_dir():
        return out
    for path in sorted(root.glob("*.json")):
        if path.name.lower() == "ledger.json":
            continue
        try:
            rec = PaperBookFile.model_validate_json(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        out.append(rec)
    return out


def ensure_observation_seed(ledger: PaperLedger | None = None) -> PaperLedger:
    """Start the 15m paper bankroll without a deposit UI or cash transfer."""
    led = ledger if ledger is not None else load_ledger()
    if led.entries:
        return led
    amt = round(PAPER_OBSERVATION_SEED, 2)
    led.starting_bankroll = amt
    led.bankroll = amt
    led.entries.append(
        LedgerEntry(
            entry_id=new_id("led"),
            kind=_SEED_KIND,
            amount=amt,
            bankroll_after=amt,
            note=(
                "PAPER OBSERVATION ONLY seed. Not a deposit. "
                "AI never deposit/withdraw/transfer. Trading NOT ARMED."
            ),
        )
    )
    save_ledger(led)
    return led


def refuse_cash_transfer(kind: str) -> None:
    """Hard NO: 15-min lane has no deposit / withdraw / transfer."""
    raise RuntimeError(
        f"AI never deposit/withdraw/transfer (refused {kind}). "
        "15-min lane has no cash UI. Trading NOT ARMED."
    )


def _open_book(event_ticker: str, title: str, ledger: PaperLedger) -> PaperBookFile:
    existing = load_book(event_ticker)
    if existing is not None:
        return existing
    rec = PaperBookFile(
        tournament_id=event_ticker,
        tournament_name=title or event_ticker,
        bankroll=ledger.bankroll,
        odds_book="kalshi_15m",
        paper_observation_only=True,
        never_auto_bet=True,
        notes=[
            "learning_lane_15m paper observation. No claimed edge.",
            "Trading NOT ARMED. PAPER OBSERVATION ONLY.",
            "fee_type=quadratic x1; price_level_structure=tapered_deci_cent; paper marks=public mid/last.",
        ],
        book=PortfolioState(bankroll=ledger.bankroll, session_label=PATH_ID),
        path_id=PATH_ID,
        independent_bankroll=True,
        starting_bankroll=ledger.starting_bankroll or PAPER_OBSERVATION_SEED,
    )
    save_book(rec)
    return rec


def append_shadow_advise(row: dict[str, object]) -> None:
    dest = shadow_path()
    dest.parent.mkdir(parents=True, exist_ok=True)
    assert_not_golf_path(dest)
    payload = {
        "timestamp": now().isoformat(),
        "lane": LANE_15M,
        "series": PRIMARY_SERIES,
        "never_auto_bet": True,
        "paper_observation_only": True,
        "trading_armed": TRADING_ARMED,
        "no_claimed_edge": True,
        **row,
    }
    with dest.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, default=str) + "\n")


def paper_autobet_open_markets(
    markets: list[dict],
    *,
    unit: float = PAPER_UNIT,
) -> list[PaperMovement]:
    """Mechanical paper YES at posted ask for each open KXBTC15M window.

    Observation probe of the ops loop. Does not invent an edge. Skips
    already-booked tickers and missing/untradable asks.
    """
    if TRADING_ARMED:
        raise RuntimeError("trading NOT ARMED")
    ledger = ensure_observation_seed()
    applied: list[PaperMovement] = []
    for market in markets:
        ticker = str(market.get("ticker") or "")
        event_ticker = str(market.get("event_ticker") or ticker)
        book_id = str(market.get("window_id") or event_ticker)
        if not ticker:
            continue
        if not market.get("is_open"):
            continue
        mark = market.get("paper_mark")
        if mark is None:
            mark = market.get("yes_ask")
        decimal = market.get("decimal_odds")
        try:
            yes_f = float(mark) if mark is not None else None
            dec_f = float(decimal) if decimal is not None else ((1.0 / yes_f) if yes_f else None)
        except (TypeError, ValueError):
            continue
        if yes_f is None or dec_f is None or yes_f <= 0.0 or yes_f >= 1.0 or dec_f <= 1.0:
            continue
        rec = _open_book(
            book_id,
            str(market.get("title") or event_ticker),
            ledger,
        )
        if rec.settled_at is not None:
            continue
        if any(p.player_id == ticker for p in rec.book.positions):
            continue
        stake = round(float(unit), 2)
        if stake <= 0 or stake > rec.bankroll + 1e-9:
            continue
        pos = StrategyPosition(
            position_id=new_id("paper"),
            player_id=ticker,
            player_name=f"YES {ticker}",
            bet_type=BetType.WIN,
            stake=stake,
            decimal_odds=dec_f,
            entry_edge=0.0,
            entry_model_p=yes_f,
            entry_market_p=yes_f,
            notes=(
                "PAPER OBSERVATION ONLY. Mechanical YES at posted Kalshi ask. "
                "No claimed edge. Trading NOT ARMED. Not a Kalshi order."
            ),
            user_recorded=True,
            proposed=False,
            fill_price=yes_f,
        )
        rec.book = rec.book.model_copy(
            update={"positions": list(rec.book.positions) + [pos]}
        )
        mv = PaperMovement(
            movement_id=new_id("move"),
            kind="new_bet",
            status="applied",
            player_id=ticker,
            player_name=pos.player_name,
            bet_type=BetType.WIN.value,
            position_id=pos.position_id,
            stake_before=0.0,
            stake_delta=stake,
            stake_after=stake,
            decimal_odds=dec_f,
            model_win=yes_f,
            edge_w=0.0,
            posted_edge=0.0,
            reason_plain=(
                "Paper observation fill at the public Kalshi mid/last mark. "
                "This is mock money for the shared ops loop. Not live trading. "
                "Not a golf WC1 edge."
            ),
            reason_technical=(
                f"lane={LANE_15M} series={PRIMARY_SERIES} ticker={ticker} "
                f"paper_mark={yes_f} fee_type=quadratic x1 "
                f"price_level_structure=tapered_deci_cent paper_autobet observation"
            ),
            amount_plain=f"Paper stake ${stake:.2f} at mark {yes_f:.3f} (decimal {dec_f:.2f}).",
        )
        rec.movements = list(rec.movements) + [mv]
        rec.latest_advice = [mv]
        save_book(rec)
        append_shadow_advise(
            {
                "action_kind": "new_bet",
                "event_ticker": event_ticker,
                "ticker": ticker,
                "posted_yes": yes_f,
                "suggested_stake": stake,
                "reason": mv.reason_plain,
            }
        )
        applied.append(mv)
    return applied


def format_15m_ledger(ledger: PaperLedger | None = None) -> str:
    led = ledger if ledger is not None else load_ledger()
    lines = [
        "PAPER LEDGER  journal=15m  lane=learning_lane_15m",
        f"bankroll=${led.bankroll:.2f}  never_auto_bet=true  PAPER OBSERVATION ONLY",
        "Trading NOT ARMED. AI: NO CASH IN/OUT. Not a golf total.",
        f"starting ${led.starting_bankroll:.2f}  betting P/L ${led.betting_pnl:+.2f}",
    ]
    if led.events:
        lines.append("Windows")
        for ev in led.events:
            lines.append(
                f"  {ev.event_name or ev.event_id}  P/L ${ev.betting_pnl:+.2f}  "
                f"bankroll ${ev.bankroll_after:.2f}"
            )
    return "\n".join(lines)


def latest_shadow_lines(n: int = 12) -> list[str]:
    dest = shadow_path()
    if not dest.is_file():
        return []
    rows = [ln for ln in dest.read_text(encoding="utf-8").splitlines() if ln.strip()]
    return rows[-n:]
