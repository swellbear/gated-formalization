"""15-min paper journal. Reuses golf PaperBookFile / PaperLedger schemas.

Writes only under the 15-min artifact root. Golf paper_dir is never used.
Paper autobet is a mechanical observation probe — no claimed edge.
Trading is never armed. AI never deposit / withdraw / transfer.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from golf_offshoot.data_feeds.kalshi_15m import is_paper_autobet_candidate
from golf_offshoot.learning_lane_15m.paths import (
    LANE_15M,
    PRIMARY_SERIES,
    assert_not_golf_path,
    paper_dir_15m,
    safe_artifact_stem,
    shadow_dir_15m,
)
from golf_offshoot.learning_lane_15m.consult_honer import compose_and_skip, market_spread
from golf_offshoot.learning_lane_15m.rules import active_execution_rule, decide
from golf_offshoot.localtime import now
from golf_offshoot.models.enums import BetType
from golf_offshoot.models.strategy import PortfolioState, StrategyPosition, new_id
from golf_offshoot.strategy.paper_book import PaperBookFile, PaperMovement
from golf_offshoot.strategy.paper_ledger import LedgerEntry, PaperLedger

PAPER_OBSERVATION_SEED = 100.0
PAPER_UNIT = 1.0
PATH_ID = "learning_lane_15m"
TRADING_ARMED = False

#: One row per window, written whether the registry said fill or skip. A skip
#: leaves no position and no ledger entry, so without this the loop would have
#: no record that it consulted anything — and "the registry is honoured" would
#: be a claim rather than an artifact.
DECISIONS_NAME = "rule_decisions.json"

# Not a user deposit. Seed so the paper loop can run without a cash UI.
_SEED_KIND = "observation_seed"


def ledger_path() -> Path:
    path = paper_dir_15m() / "ledger.json"
    assert_not_golf_path(path)
    return path


def book_path(event_ticker: str) -> Path:
    path = paper_dir_15m() / f"{safe_artifact_stem(event_ticker)}.json"
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


def decisions_path() -> Path:
    path = paper_dir_15m() / DECISIONS_NAME
    assert_not_golf_path(path)
    return path


_SESSION_COUNTS: tuple[tuple[int, int], dict[str, Any]] | None = None


def paper_session_counts() -> dict[str, Any]:
    """Open/closed/bankroll for the hub strip. Not a pydantic walk of every book."""
    global _SESSION_COUNTS
    root = paper_dir_15m()
    led_path = ledger_path()
    try:
        dir_m = int(root.stat().st_mtime_ns)
    except OSError:
        dir_m = 0
    try:
        led_m = int(led_path.stat().st_mtime_ns)
    except OSError:
        led_m = 0
    key = (dir_m, led_m)
    if _SESSION_COUNTS is not None and _SESSION_COUNTS[0] == key:
        return dict(_SESSION_COUNTS[1])
    led = load_ledger()
    bank = float(getattr(led, "bankroll", 0) or 0)
    pnl = float(getattr(led, "betting_pnl", 0) or 0)
    open_n = 0
    closed_n = 0
    if root.is_dir():
        skip = {"ledger.json", DECISIONS_NAME.lower()}
        for path in root.glob("*.json"):
            if path.name.lower() in skip:
                continue
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            if not isinstance(payload, dict):
                continue
            if payload.get("settled_at"):
                closed_n += 1
            else:
                open_n += 1
    out = {"open": open_n, "closed": closed_n, "bankroll": bank, "pnl": pnl}
    _SESSION_COUNTS = (key, out)
    return dict(out)


def load_decisions() -> dict[str, dict]:
    path = decisions_path()
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    rows = payload.get("decisions") if isinstance(payload, dict) else None
    return rows if isinstance(rows, dict) else {}


def record_decision(ticker: str, row: dict) -> dict:
    """One decision per ticker, first one wins. The loop re-reads every ~90s."""
    rows = load_decisions()
    if ticker in rows:
        return rows[ticker]
    rows[ticker] = row
    path = decisions_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "lane": LANE_15M,
                "series": PRIMARY_SERIES,
                "framing": (
                    "What rules.decide() said for each window. A skip has no book, "
                    "no position and no pnl; this is the only place it is recorded."
                ),
                "trading_armed": TRADING_ARMED,
                "decisions": rows,
            },
            indent=2,
            default=str,
        )
        + "\n",
        encoding="utf-8",
    )
    return row


def iter_books() -> list[PaperBookFile]:
    out: list[PaperBookFile] = []
    root = paper_dir_15m()
    if not root.is_dir():
        return out
    for path in sorted(root.glob("*.json")):
        if path.name.lower() in {"ledger.json", DECISIONS_NAME.lower()}:
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


def consult_registry(
    rule: dict | None,
    *,
    posted_yes: float,
    close_at: str,
    spread: float | None = None,
    consult_root: Path | None = None,
) -> dict:
    """What the executing rule says about this window. Never a fill by default.

    The loop used to fill every candidate window and never open the registry,
    which is why ``Established`` was unreachable: no rule selected anything, so
    no lived L2 could exist. A registry with no executing rule fills nothing —
    an unnamed default is how "always fill" got in here in the first place.

    After ``rules.decide()``, ``compose_and_skip`` may add a honer skip from a
    dated frozen snapshot. That compositor is dark unless ``consult_enabled``
    is true. Live honer θ never consults.
    """
    if rule is None:
        verdict = {
            "rule_id": "",
            "action": "no_rule",
            "reason": "no rule in the registry carries execution=true; nothing fills",
            "eligible": False,
            "execution": False,
        }
    else:
        try:
            verdict = decide(rule, posted_yes=posted_yes, close_at=close_at)
        except ValueError as exc:
            verdict = {
                "rule_id": rule.get("id"),
                "action": "undecidable",
                "reason": f"cannot establish OOS for this window ({exc}); not filling",
                "eligible": False,
                "execution": bool(rule.get("execution")),
            }
    return compose_and_skip(
        verdict,
        posted_yes=posted_yes,
        spread=spread,
        root=consult_root,
    )


def paper_autobet_open_markets(
    markets: list[dict],
    *,
    unit: float = PAPER_UNIT,
    rule: dict | None = None,
) -> list[PaperMovement]:
    """Mechanical paper YES at the public Kalshi mid/last mark.

    Observation probe of the ops loop. Does not invent an edge. Skips
    already-booked tickers and missing/untradable marks. ``paper_mark`` is
    ``public_mid_or_last`` (the mid when both sides are quoted); ``yes_ask``
    is fallback only.

    Every candidate now goes through ``rules.decide()`` on the rule the
    registry marks ``execution: true``. A skip writes no position, no ledger
    entry and no pnl — only a decision row saying which rule skipped it and
    why.
    """
    if TRADING_ARMED:
        raise RuntimeError("trading NOT ARMED")
    ledger = ensure_observation_seed()
    active = rule if rule is not None else active_execution_rule()
    applied: list[PaperMovement] = []
    for market in markets:
        ticker = str(market.get("ticker") or "")
        event_ticker = str(market.get("event_ticker") or ticker)
        book_id = str(market.get("window_id") or event_ticker)
        if not ticker:
            continue
        if not is_paper_autobet_candidate(market):
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
        verdict = consult_registry(
            active,
            posted_yes=yes_f,
            close_at=str(market.get("close_time") or ""),
            spread=market_spread(market),
        )
        if verdict["action"] != "fill":
            if ticker not in load_decisions():
                record_decision(
                    ticker,
                    {
                        "ticker": ticker,
                        "window_id": book_id,
                        "rule_id": verdict.get("rule_id") or "",
                        "action": verdict["action"],
                        "reason": verdict["reason"],
                        "posted_yes": yes_f,
                        "close_at": str(market.get("close_time") or ""),
                        "at": now().isoformat(),
                        "pnl": None,
                        "note": "no fill, no position, no pnl; a skip is not a loss",
                    },
                )
                append_shadow_advise(
                    {
                        "action_kind": verdict["action"],
                        "event_ticker": event_ticker,
                        "ticker": ticker,
                        "posted_yes": yes_f,
                        "suggested_stake": 0.0,
                        "rule_id": verdict.get("rule_id") or "",
                        "reason": verdict["reason"],
                    }
                )
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
                "PAPER OBSERVATION ONLY. Mechanical YES at the public Kalshi "
                "mid/last mark. No claimed edge. Trading NOT ARMED. Not a Kalshi order."
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
                f"paper_mark={yes_f} yes_bid={market.get('yes_bid')} "
                f"yes_ask={market.get('yes_ask')} fee_type=quadratic x1 "
                f"price_level_structure=tapered_deci_cent paper_autobet observation "
                f"rule_id={verdict.get('rule_id') or ''} "
                f"rules.decide={verdict['action']} ({verdict['reason']})"
            ),
            amount_plain=f"Paper stake ${stake:.2f} at mark {yes_f:.3f} (decimal {dec_f:.2f}).",
        )
        rec.movements = list(rec.movements) + [mv]
        rec.latest_advice = [mv]
        save_book(rec)
        ledger.entries.append(
            LedgerEntry(
                entry_id=new_id("led"),
                kind="paper_fill",
                amount=0.0,
                bankroll_after=ledger.bankroll,
                event_id=event_ticker,
                event_name=str(market.get("title") or event_ticker),
                player_name=ticker,
                note=(
                    f"PAPER OBSERVATION fill position_id={pos.position_id} "
                    f"ticker={ticker} window_id={book_id} mark={yes_f}. "
                    "never_auto_bet. Not a deposit. Trading NOT ARMED."
                ),
                never_auto_bet=True,
            )
        )
        save_ledger(ledger)
        record_decision(
            ticker,
            {
                "ticker": ticker,
                "window_id": book_id,
                "rule_id": verdict.get("rule_id") or "",
                "action": verdict["action"],
                "reason": verdict["reason"],
                "posted_yes": yes_f,
                "close_at": str(market.get("close_time") or ""),
                "at": now().isoformat(),
                "position_id": pos.position_id,
                "stake": stake,
            },
        )
        append_shadow_advise(
            {
                "action_kind": "new_bet",
                "event_ticker": event_ticker,
                "ticker": ticker,
                "posted_yes": yes_f,
                "suggested_stake": stake,
                "rule_id": verdict.get("rule_id") or "",
                "reason": mv.reason_plain,
            }
        )
        applied.append(mv)
    return applied


def format_15m_observation_board() -> str:
    """Desktop journal: paper fills and official joins already on disk. No invented result."""
    from golf_offshoot.learning_lane_15m.paths import latest_dir_15m, settlements_dir_15m

    lines = [format_15m_ledger(), "", "Paper books"]
    books = list(iter_books())
    if not books:
        lines.append("  none yet")
    for rec in books:
        status = "settled" if rec.settled_at is not None else "open / SETTLE_PENDING"
        tickers = [pos.player_id for pos in rec.book.positions]
        label = tickers[0] if tickers else event_ticker_from_book(rec)
        extra = (
            f" pnl={float(rec.settlement_pnl or 0):+.2f}" if rec.settled_at is not None else ""
        )
        lines.append(f"  {label} {status}{extra}")
    journal = latest_dir_15m() / "journal.json"
    if journal.is_file():
        try:
            payload = json.loads(journal.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            payload = {}
        rows = [w for w in (payload.get("windows") or []) if isinstance(w, dict)]
        interesting = [
            w
            for w in rows
            if w.get("ticker")
            and (w.get("result") or w.get("status") in {"active", "finalized", "settled", "open"})
        ]
        if interesting:
            lines.extend(["", "Kalshi windows in latest journal (display, not extra settles)"])
            for window in interesting[:12]:
                lines.append(
                    f"  {window.get('ticker')} status={window.get('status') or ''} "
                    f"result={window.get('result') or 'n/a'}"
                )
    settles = sorted(settlements_dir_15m().glob("*.json"))
    if settles:
        lines.extend(["", "Official settle joins"])
        for path in settles[-8:]:
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            for row in payload.get("rows") or []:
                if not isinstance(row, dict):
                    continue
                lines.append(
                    f"  {row.get('ticker') or path.stem} "
                    f"{row.get('settle_status') or ''} "
                    f"kalshi_result={row.get('kalshi_result') or 'n/a'}"
                )
    return "\n".join(lines)


def event_ticker_from_book(rec) -> str:
    from golf_offshoot.learning_lane_15m.settle import event_ticker_from_book_id

    return event_ticker_from_book_id(str(rec.tournament_id or ""))


def format_15m_ledger(ledger: PaperLedger | None = None) -> str:
    led = ledger if ledger is not None else load_ledger()
    lines = [
        "PAPER LEDGER  journal=15m",
        f"bankroll=${led.bankroll:.2f}  P/L ${led.betting_pnl:+.2f}  start ${led.starting_bankroll:.2f}",
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
