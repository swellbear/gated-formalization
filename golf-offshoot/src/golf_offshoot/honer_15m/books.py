"""Search and exam paper books. Skips are rows. Two ledgers, never summed."""

from __future__ import annotations

import json
from typing import Any

from golf_offshoot.honer_15m.paths import (
    assert_honer_path,
    decisions_path,
    ledger_path,
    paper_dir,
    safe_artifact_stem,
)
from golf_offshoot.honer_15m.policy import SEED_BANKROLL, STAKE
from golf_offshoot.localtime import now

BOOKS = ("search", "exam")


def _empty_ledger() -> dict[str, Any]:
    return {
        "starting_bankroll": SEED_BANKROLL,
        "bankroll": SEED_BANKROLL,
        "betting_pnl": 0.0,
        "entries": 0,
        "fills": 0,
        "skips": 0,
        "settled": 0,
        "lane": "honer_15m",
        "fee_omitted": True,
    }


def load_ledger(book: str) -> dict[str, Any]:
    path = ledger_path(book)
    if not path.is_file():
        led = _empty_ledger()
        save_ledger(book, led)
        return led
    return json.loads(path.read_text(encoding="utf-8"))


def save_ledger(book: str, ledger: dict[str, Any]) -> None:
    path = ledger_path(book)
    assert_honer_path(path)
    path.write_text(json.dumps(ledger, indent=2), encoding="utf-8")


def load_decisions(book: str) -> dict[str, Any]:
    path = decisions_path(book)
    if not path.is_file():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def save_decisions(book: str, rows: dict[str, Any]) -> None:
    path = decisions_path(book)
    assert_honer_path(path)
    path.write_text(json.dumps(rows, indent=2), encoding="utf-8")


def paper_path(book: str, ticker: str) -> Any:
    return paper_dir(book) / f"{safe_artifact_stem(ticker)}.json"


def has_ticket(book: str, ticker: str) -> bool:
    return ticker in load_decisions(book) or paper_path(book, ticker).is_file()


def record_action(
    book: str,
    *,
    ticker: str,
    window_id: str,
    action: str,
    reason: str,
    posted_yes: float,
    theta: float,
    close_at: str,
) -> dict[str, Any]:
    if has_ticket(book, ticker):
        return load_decisions(book)[ticker]
    row = {
        "ticker": ticker,
        "window_id": window_id,
        "action": action,
        "reason": reason,
        "posted_yes": posted_yes,
        "theta": theta,
        "stake": STAKE if action == "fill" else 0.0,
        "close_at": close_at,
        "kalshi_result": "",
        "pnl": None,
        "fill_all_pnl": None,
        "d": None,
        "settled_at": None,
        "at": now().isoformat(),
        "book": book,
        "lane": "honer_15m",
        "entry_edge": 0.0,
        "fee_omitted": True,
    }
    dest = paper_path(book, ticker)
    assert_honer_path(dest)
    dest.write_text(json.dumps(row, indent=2), encoding="utf-8")
    decisions = load_decisions(book)
    decisions[ticker] = row
    save_decisions(book, decisions)
    led = load_ledger(book)
    led["entries"] = int(led.get("entries") or 0) + 1
    if action == "fill":
        led["fills"] = int(led.get("fills") or 0) + 1
    else:
        led["skips"] = int(led.get("skips") or 0) + 1
    save_ledger(book, led)
    return row


def fill_all_pnl(posted_yes: float, kalshi_result: str, *, stake: float = STAKE) -> float:
    """Counterfactual always-YES at the same mark. Zero fee."""
    result = str(kalshi_result).strip().lower()
    if result == "yes":
        return round(stake / float(posted_yes) - stake, 2)
    if result == "no":
        return round(-stake, 2)
    raise ValueError("fill_all_pnl needs yes/no")


def apply_settle(
    book: str,
    ticker: str,
    *,
    kalshi_result: str,
    step_theta: bool,
) -> tuple[dict[str, Any] | None, bool]:
    decisions = load_decisions(book)
    row = decisions.get(ticker)
    if row is None:
        return None, False
    if row.get("settled_at"):
        return row, False
    result = str(kalshi_result).strip().lower()
    if result not in {"yes", "no"}:
        return row
    posted = float(row["posted_yes"])
    baseline = fill_all_pnl(posted, result)
    if row["action"] == "fill":
        pnl = baseline
        d = 0.0
    else:
        pnl = 0.0
        d = round(0.0 - baseline, 2)
    row["kalshi_result"] = result
    row["pnl"] = pnl
    row["fill_all_pnl"] = baseline
    row["d"] = d
    row["settled_at"] = now().isoformat()
    decisions[ticker] = row
    save_decisions(book, decisions)
    dest = paper_path(book, ticker)
    dest.write_text(json.dumps(row, indent=2), encoding="utf-8")
    led = load_ledger(book)
    if row["action"] == "fill":
        led["bankroll"] = round(float(led["bankroll"]) + pnl, 2)
        led["betting_pnl"] = round(float(led["betting_pnl"]) + pnl, 2)
    led["settled"] = int(led.get("settled") or 0) + 1
    save_ledger(book, led)
    if step_theta:
        from golf_offshoot.honer_15m.theta import step_search_theta

        step_search_theta(action=str(row["action"]), kalshi_result=result)
    return row, True


def iter_settled(book: str) -> list[dict[str, Any]]:
    rows = []
    for row in load_decisions(book).values():
        if isinstance(row, dict) and row.get("settled_at") and row.get("kalshi_result") in {"yes", "no"}:
            rows.append(row)
    return rows
