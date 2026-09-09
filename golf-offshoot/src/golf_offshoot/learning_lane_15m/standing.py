"""Factory English standing from live 15m files only.

Does not edit the learning card, the Lineage A PNG, the registry, or the bar.
Does not read honer_15m.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from golf_offshoot.learning_lane_15m.paper import load_book, load_decisions, load_ledger
from golf_offshoot.learning_lane_15m.paths import latest_dir_15m, settlements_dir_15m
from golf_offshoot.learning_lane_15m.rules import (
    active_execution_rule,
    favorite_threshold,
    load_rules,
)
from golf_offshoot.localtime import format_eastern, now, to_eastern

WAITING = "still waiting on Kalshi"
TWO_TO_ONE = 2.0 / 3.0
PLANNED_N = 70


@dataclass(frozen=True)
class FactoryStanding:
    what_it_is: str
    where_it_stands: str
    last_happened: str
    this_book: str
    not_a_keep: str
    current_ticker: str
    current_window_et: str
    current_phrase: str
    current_kalshi: str
    current_action: str


def _cents(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{round(float(value) * 100):.0f}¢"


def _dollars(value: float | None, *, signed: bool = False) -> str:
    if value is None:
        return WAITING
    num = float(value)
    return f"${num:+.2f}" if signed else f"${num:.2f}"


def _window_et(ticker: str, close_at: str = "", window_id: str = "") -> str:
    if close_at:
        stamp = format_eastern(close_at)
        parts = stamp.split()
        if len(parts) >= 2 and ":" in parts[1] and stamp != close_at:
            return f"{parts[1]} ET"
    bits = str(window_id or "").split("__")
    if len(bits) >= 3:
        stamp = format_eastern(bits[-1])
        parts = stamp.split()
        if len(parts) >= 2 and ":" in parts[1]:
            return f"{parts[1]} ET"
    token = str(ticker or "").rsplit("-", 2)
    if len(token) >= 2 and token[-2][-4:].isdigit():
        hhmm = token[-2][-4:]
        return f"{hhmm[:2]}:{hhmm[2:]} ET"
    return "window ET unknown"


def _cutoff(rule: dict[str, Any] | None) -> float:
    if rule is None:
        return TWO_TO_ONE
    params = rule.get("params") or {}
    if params.get("favorite_odds") is not None:
        try:
            return favorite_threshold(float(params["favorite_odds"]))
        except ValueError:
            return TWO_TO_ONE
    return TWO_TO_ONE


def _journal_result(ticker: str) -> str:
    path = latest_dir_15m() / "journal.json"
    if not path.is_file():
        return ""
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return ""
    for window in payload.get("windows") or []:
        if isinstance(window, dict) and str(window.get("ticker") or "") == ticker:
            got = str(window.get("result") or "").strip().lower()
            if got in {"yes", "no"}:
                return got
    return ""


def _settle_result(ticker: str) -> str:
    from golf_offshoot.learning_lane_15m.paths import safe_artifact_stem

    dest = settlements_dir_15m() / f"{safe_artifact_stem(ticker)}.json"
    if not dest.is_file():
        return ""
    try:
        payload = json.loads(dest.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return ""
    for row in payload.get("rows") or []:
        if isinstance(row, dict) and str(row.get("ticker") or "") == ticker:
            got = str(row.get("kalshi_result") or "").strip().lower()
            if got in {"yes", "no"}:
                return got
    got = str(payload.get("kalshi_result") or "").strip().lower()
    return got if got in {"yes", "no"} else ""


def _paper_pnl(ticker: str) -> float | None:
    rec = load_book(ticker)
    if rec is None:
        return None
    raw = rec.settlement_pnl
    if raw is None:
        return None
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def _sorted_decisions() -> list[tuple[str, dict[str, Any]]]:
    rows = [(k, v) for k, v in load_decisions().items() if isinstance(v, dict)]
    return sorted(rows, key=lambda item: item[0], reverse=True)


def _lived_count(rule: dict[str, Any] | None) -> int:
    """Settled factory decisions on this tree. A count, not a score."""
    begins = ""
    if rule is not None:
        begins = str(rule.get("lived_paper_begins_at") or rule.get("execution_flipped_at") or "")
    begin_dt = None
    if begins:
        text = begins[:-1] + "+00:00" if begins.endswith("Z") else begins
        try:
            begin_dt = to_eastern(datetime.fromisoformat(text))
        except ValueError:
            begin_dt = None
    n = 0
    for ticker, row in load_decisions().items():
        if not isinstance(row, dict):
            continue
        at = str(row.get("at") or row.get("close_at") or "")
        if begin_dt is not None and at:
            try:
                stamped = to_eastern(
                    datetime.fromisoformat(at[:-1] + "+00:00" if at.endswith("Z") else at)
                )
                if stamped <= begin_dt:
                    continue
            except ValueError:
                pass
        result = _settle_result(ticker) or _journal_result(ticker)
        if row.get("action") == "skip":
            if result in {"yes", "no"}:
                n += 1
            continue
        if _paper_pnl(ticker) is not None or result in {"yes", "no"}:
            n += 1
    return n


def collect_factory_standing() -> FactoryStanding:
    try:
        rule = active_execution_rule()
    except ValueError:
        rule = None
    cutoff = _cutoff(rule)
    rule_id = str((rule or {}).get("id") or "no executing selection rule")
    selects = bool((rule or {}).get("selects"))
    what = (
        "Factory is not predicting up or down. Each window it either takes a paper YES at the "
        "posted price or skips because that price is too rich "
        f"(2-to-1 favorite: posted YES at or above {_cents(cutoff)}). It never buys NO. "
        "The model is the market (entry_edge=0)."
    )
    if not selects:
        what = (
            "Factory is not predicting up or down. The executing row is the named fill-all baseline: "
            "every candidate window gets a paper YES at the posted price. It never buys NO. "
            "The model is the market (entry_edge=0)."
        )
    n = _lived_count(rule)
    binding = False
    try:
        reg = load_rules()
        binding = bool((reg.get("evidence_bar") or {}).get("binding"))
    except (OSError, ValueError, FileNotFoundError):
        binding = False
    where = (
        f"RUN-ONLY, not scored, not bound. The book you are watching is {rule_id}. "
        "Baseline fill-all is the named comparison sitting in the registry; it is not a second live brain. "
        f"Settled windows counted on this tree since the selection rule started running: {n}. "
        f"The planned first look is {PLANNED_N}. That count is not a result. Not a keep."
    )
    if binding:
        where = where.replace("not bound", "bar file says binding — still do not treat this page as a keep")
    decisions = _sorted_decisions()
    last = (
        "Factory has not recorded a window decision on this tree yet."
    )
    current_ticker = ""
    current_et = ""
    current_phrase = "no decision yet"
    current_kalshi = "n/a"
    current_action = ""
    if decisions:
        ticker, row = decisions[0]
        current_ticker = ticker
        current_et = _window_et(
            ticker,
            close_at=str(row.get("close_at") or ""),
            window_id=str(row.get("window_id") or ""),
        )
        posted = row.get("posted_yes")
        posted_f = float(posted) if posted is not None else None
        action = str(row.get("action") or "")
        current_action = action
        result = _settle_result(ticker) or _journal_result(ticker)
        pnl = _paper_pnl(ticker)
        pending = result not in {"yes", "no"} and pnl is None
        current_kalshi = WAITING if pending else (result.upper() if result else "n/a")
        if action == "skip":
            current_phrase = (
                f"skipped ({_cents(posted_f)} at or above the {_cents(cutoff)} 2-to-1 line)"
            )
        elif action == "fill":
            current_phrase = (
                f"filled YES ({_cents(posted_f)} below the {_cents(cutoff)} 2-to-1 line)"
            )
        else:
            current_phrase = f"{action or 'no decision'} (posted {_cents(posted_f)})"
        if pending:
            last = (
                f"This window is still open. Factory already decided **{current_phrase}**. "
                f"Kalshi has not posted an official result. Paper pnl is not known yet — not zero."
            )
        elif action == "skip":
            last = (
                f"Last settled window **{current_et}**: the market's YES was **{_cents(posted_f)}**. "
                f"The 2-to-1 line is **{_cents(cutoff)}**, so factory **skipped**. "
                f"Kalshi later said **{result.upper()}**. No ticket, so paper pnl is **$0** "
                "(a skip is not a loss)."
            )
        else:
            money = _dollars(pnl, signed=True) if pnl is not None else WAITING
            last = (
                f"Last settled window **{current_et}**: the market's YES was **{_cents(posted_f)}**. "
                f"The 2-to-1 line is **{_cents(cutoff)}**, so factory **filled YES**. "
                f"Kalshi later said **{(result or 'n/a').upper()}**. This book's paper pnl is **{money}**."
            )
        # If newest is pending, also name last settled when one exists.
        if pending:
            for other_ticker, other in decisions[1:]:
                other_result = _settle_result(other_ticker) or _journal_result(other_ticker)
                other_pnl = _paper_pnl(other_ticker)
                if other_result not in {"yes", "no"} and other_pnl is None:
                    continue
                other_et = _window_et(
                    other_ticker,
                    close_at=str(other.get("close_at") or ""),
                    window_id=str(other.get("window_id") or ""),
                )
                other_posted = other.get("posted_yes")
                other_action = str(other.get("action") or "")
                if other_action == "skip":
                    last += (
                        f" Last settled window **{other_et}**: skipped at {_cents(float(other_posted) if other_posted is not None else None)} "
                        f"vs {_cents(cutoff)}; Kalshi {(other_result or 'n/a').upper()}; no ticket."
                    )
                else:
                    last += (
                        f" Last settled window **{other_et}**: filled YES at {_cents(float(other_posted) if other_posted is not None else None)}; "
                        f"Kalshi {(other_result or 'n/a').upper()}; "
                        f"paper pnl {_dollars(other_pnl, signed=True)}."
                    )
                break
    led = load_ledger()
    this_book = (
        f"Lineage A (this tree): bankroll {_dollars(float(led.bankroll))} "
        f"paper pnl {_dollars(float(led.betting_pnl), signed=True)}. "
        "Lineage B is the published Pages book, named apart, never added."
    )
    not_keep = ""
    if float(led.betting_pnl) > 0:
        not_keep = "A green factory ledger is not a track record. RUN-ONLY is not a keep."
    return FactoryStanding(
        what_it_is=what,
        where_it_stands=where,
        last_happened=last,
        this_book=this_book,
        not_a_keep=not_keep,
        current_ticker=current_ticker,
        current_window_et=current_et,
        current_phrase=current_phrase,
        current_kalshi=current_kalshi,
        current_action=current_action,
    )


def current_factory_action() -> dict[str, Any]:
    standing = collect_factory_standing()
    return {
        "ticker": standing.current_ticker,
        "window_et": standing.current_window_et,
        "phrase": standing.current_phrase,
        "kalshi": standing.current_kalshi,
        "action": standing.current_action,
    }


def factory_png_mtime() -> str:
    dest = (
        Path(__file__).resolve().parents[4]
        / "docs"
        / "observability-hub"
        / "data"
        / "charts"
        / "learning_lane_15m"
        / "paper_window_strip.png"
    )
    if not dest.is_file():
        return "not yet available"
    try:
        return format_eastern(datetime.fromtimestamp(dest.stat().st_mtime).astimezone())
    except OSError:
        return "not yet available"


def journal_generated_at() -> str:
    path = latest_dir_15m() / "journal.json"
    if not path.is_file():
        return "journal missing"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return "journal unreadable"
    stamp = str(payload.get("generated_at") or "")
    return format_eastern(stamp) if stamp else "journal generated_at not recorded"


def factory_watch_clock() -> dict[str, Any]:
    from golf_offshoot.learning_lane_15m.watch import load_watch_status

    watch = load_watch_status()
    at = str(watch.get("last_at") or watch.get("at") or "")
    stale = not bool(watch.get("running"))
    if at and not stale:
        text = at[:-1] + "+00:00" if at.endswith("Z") else at
        try:
            stamped = to_eastern(datetime.fromisoformat(text))
            stale = (now() - stamped).total_seconds() > 180
        except ValueError:
            stale = True
    return {
        "running": bool(watch.get("running")),
        "cycles": int(watch.get("cycles") or 0),
        "last": str(watch.get("last_summary") or ""),
        "at": format_eastern(at) if at else "n/a",
        "stale": stale,
        "png_mtime": factory_png_mtime(),
        "journal_at": journal_generated_at(),
    }
