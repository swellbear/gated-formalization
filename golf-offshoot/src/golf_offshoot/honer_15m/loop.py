"""One honer tick: fetch public KXBTC15M, fill/skip search+exam, settle. Own cache."""

from __future__ import annotations

import json
import time
from typing import Any

from golf_offshoot.data_feeds.http import HttpCache
from golf_offshoot.data_feeds.kalshi_15m import Kalshi15mFeed, is_paper_autobet_candidate
from golf_offshoot.honer_15m.books import apply_settle, has_ticket, record_action
from golf_offshoot.honer_15m.decide import decide_yes_or_skip, posted_mark
from golf_offshoot.honer_15m.freeze import (
    complete_exam,
    exam_is_open,
    fire_freeze,
    increment_exam_n,
    load_exam_state,
    park_exam,
)
from golf_offshoot.honer_15m.paths import cache_dir, safe_artifact_stem, settlements_dir
from golf_offshoot.honer_15m.policy import load_policy
from golf_offshoot.honer_15m.score import exam_sums, futility_impossible, should_check_futility
from golf_offshoot.honer_15m.theta import load_theta
from golf_offshoot.localtime import now

TRADING_ARMED = False


def _feed() -> Kalshi15mFeed:
    return Kalshi15mFeed(cache=HttpCache(cache_dir()), refresh=True)


def fetch_markets(*, retries: int = 4) -> list[dict[str, Any]]:
    if TRADING_ARMED:
        raise RuntimeError("trading NOT ARMED")
    delay = 2.0
    last_err: Exception | None = None
    for _ in range(max(1, retries)):
        try:
            payload, _quality = _feed().fetch(refresh=True)
            return list(payload.get("markets") or [])
        except Exception as exc:  # noqa: BLE001 — backoff includes 429
            last_err = exc
            text = str(exc)
            if "429" in text or "rate" in text.lower():
                time.sleep(delay)
                delay = min(delay * 2.0, 30.0)
                continue
            raise
    if last_err:
        raise last_err
    return []


def _write_settle_row(market: dict[str, Any], result: str) -> None:
    ticker = str(market.get("ticker") or "")
    dest = settlements_dir() / f"{safe_artifact_stem(ticker)}.json"
    dest.write_text(
        json.dumps(
            {
                "lane": "honer_15m",
                "ticker": ticker,
                "window_id": str(market.get("window_id") or ""),
                "kalshi_result": result,
                "status": str(market.get("status") or ""),
                "as_of": now().isoformat(),
                "source": "public Kalshi result — honer copy, not learning_lane_15m/settlements",
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def _maybe_act(book: str, market: dict[str, Any], theta: float) -> None:
    ticker = str(market.get("ticker") or "")
    if not ticker or has_ticket(book, ticker):
        return
    if not is_paper_autobet_candidate(market):
        return
    mark = posted_mark(market)
    if mark is None:
        return
    action, reason = decide_yes_or_skip(mark, theta)
    record_action(
        book,
        ticker=ticker,
        window_id=str(market.get("window_id") or ""),
        action=action,
        reason=reason,
        posted_yes=mark,
        theta=theta,
        close_at=str(market.get("close_time") or ""),
    )


def run_tick(markets: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    if TRADING_ARMED:
        raise RuntimeError("trading NOT ARMED")
    rows = markets if markets is not None else fetch_markets()
    search_theta = float(load_theta()["theta"])
    exam = load_exam_state()
    frozen = exam.get("frozen_theta") if exam_is_open() else None

    for market in rows:
        if is_paper_autobet_candidate(market):
            _maybe_act("search", market, search_theta)
            if frozen is not None:
                _maybe_act("exam", market, float(frozen))

        result = str(market.get("result") or "").strip().lower()
        ticker = str(market.get("ticker") or "")
        if result not in {"yes", "no"} or not ticker:
            continue
        _write_settle_row(market, result)
        apply_settle("search", ticker, kalshi_result=result, step_theta=True)
        if exam_is_open():
            exam_row, newly = apply_settle("exam", ticker, kalshi_result=result, step_theta=False)
            if newly and exam_row is not None:
                state = increment_exam_n()
                n = int(state.get("n") or 0)
                pol = load_policy()
                if should_check_futility(n):
                    sums = exam_sums()
                    if futility_impossible(
                        int(sums["n"]),
                        sums["d_sum"],
                        sums["exam_pnl_sum"],
                        exam_n=int(pol["exam_n"]),
                    ):
                        park_exam(f"futility at n={n}: remaining skips cannot pass")
                elif n >= int(pol["exam_n"]):
                    complete_exam()

    fired = fire_freeze()
    return {
        "lane": "honer_15m",
        "search_theta": float(load_theta()["theta"]),
        "exam": load_exam_state(),
        "froze": bool(fired),
        "markets": len(rows),
        "trading_armed": False,
        "fee_omitted": True,
    }
