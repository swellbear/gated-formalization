"""One honer tick: subscribe to quote_bus, fill/skip search+exam, settle. No HTTP."""

from __future__ import annotations

import json
from typing import Any

from golf_offshoot.data_feeds.kalshi_15m import is_paper_autobet_candidate
from golf_offshoot.honer_15m.books import apply_settle, has_ticket, record_action
from golf_offshoot.honer_15m.decide import decide_ticket, market_spread, posted_mark
from golf_offshoot.honer_15m.freeze import (
    complete_exam,
    exam_is_open,
    fire_freeze,
    increment_exam_n,
    load_exam_state,
    park_exam,
)
from golf_offshoot.honer_15m.paths import (
    assert_honer_path,
    last_tick_path,
    safe_artifact_stem,
    settlements_dir,
    watch_status_path,
)
from golf_offshoot.honer_15m.picker import apply_search_starvation, maybe_advance
from golf_offshoot.honer_15m.policy import FAMILY_RICH, load_policy
from golf_offshoot.honer_15m.score import (
    classify_completed_exam,
    exam_sums,
    futility_impossible,
    should_check_futility,
    write_exam_scorecard,
)
from golf_offshoot.honer_15m.theta import load_theta
from golf_offshoot.localtime import now

TRADING_ARMED = False


def _merge_watch(fields: dict[str, Any]) -> None:
    path = watch_status_path()
    payload: dict[str, Any] = {"running": False, "cycles": 0, "lane": "honer_15m"}
    if path.is_file():
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(existing, dict):
                payload.update(existing)
        except (OSError, ValueError):
            pass
    payload.update(fields)
    payload["lane"] = "honer_15m"
    payload["at"] = now().isoformat()
    assert_honer_path(path)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def fetch_markets(*, retries: int = 4) -> list[dict[str, Any]]:
    """Read the factory quote bus only. Missing or stale → skip. Never HTTP."""
    del retries
    if TRADING_ARMED:
        raise RuntimeError("trading NOT ARMED")
    from golf_offshoot.quote_bus import is_fresh, load_latest
    from golf_offshoot.quote_bus.bus import _parse_when

    payload = load_latest()
    if payload and is_fresh(payload):
        parsed = _parse_when(str(payload.get("fetched_at") or ""))
        age = int(max(0, (now() - parsed).total_seconds())) if parsed is not None else None
        _merge_watch(
            {
                "quote_bus_stale": False,
                "quote_bus_age_s": age,
                "quote_bus_fetch_id": payload.get("fetch_id"),
            }
        )
        return list(payload.get("markets") or [])
    _merge_watch({"quote_bus_stale": True, "quote_bus_age_s": None, "quote_bus_fetch_id": None})
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


def _write_last_tick(*, markets: int, quote_bus_stale: bool) -> None:
    path = last_tick_path()
    assert_honer_path(path)
    path.write_text(
        json.dumps(
            {
                "lane": "honer_15m",
                "http_fetches": 0,
                "markets": markets,
                "quote_bus_stale": quote_bus_stale,
                "wrote_learning_lane_15m": False,
                "at": now().isoformat(),
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def _exam_knobs(exam: dict[str, Any]) -> dict[str, Any]:
    pol = load_policy()
    return {
        "family": str(exam.get("frozen_family") or FAMILY_RICH),
        "theta": float(exam.get("frozen_theta") or pol["start_theta"]),
        "delta": float(exam.get("frozen_delta") or pol["start_delta"]),
    }


def _close_exam_to_library(exam: dict[str, Any], *, outcome: str) -> None:
    from golf_offshoot.honer_15m.picker import on_exam_close

    on_exam_close(
        outcome=outcome,
        family=str(exam.get("frozen_family") or FAMILY_RICH),
        knobs=_exam_knobs(exam),
        k=int(exam.get("k_after") or 0),
    )
    maybe_advance()


def _maybe_act(book: str, market: dict[str, Any], theta: float, *, family: str, delta: float) -> None:
    ticker = str(market.get("ticker") or "")
    if not ticker or has_ticket(book, ticker):
        return
    if not is_paper_autobet_candidate(market):
        return
    mark = posted_mark(market)
    if mark is None:
        return
    spread = market_spread(market)
    action, reason = decide_ticket(mark, theta, family=family, delta=delta, spread=spread)
    exam_k = None
    if book == "exam":
        exam_k = int(load_exam_state().get("k_after") or 0) or None
    record_action(
        book,
        ticker=ticker,
        window_id=str(market.get("window_id") or ""),
        action=action,
        reason=reason,
        posted_yes=mark,
        theta=theta,
        close_at=str(market.get("close_time") or ""),
        exam_k=exam_k,
        family=family,
        delta=delta,
        spread=spread,
    )


def run_tick(markets: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    if TRADING_ARMED:
        raise RuntimeError("trading NOT ARMED")
    used_bus = markets is None
    rows = markets if markets is not None else fetch_markets()
    stale = False
    if used_bus:
        try:
            payload = json.loads(watch_status_path().read_text(encoding="utf-8"))
            stale = bool(payload.get("quote_bus_stale"))
        except (OSError, ValueError):
            stale = not rows
    search = load_theta()
    search_theta = float(search["theta"])
    search_family = str(search.get("active_family") or FAMILY_RICH)
    search_delta = float(search.get("delta") or load_policy()["start_delta"])
    exam = load_exam_state()
    frozen = exam.get("frozen_theta") if exam_is_open() else None
    exam_family = str(exam.get("frozen_family") or search_family)
    exam_delta = float(exam.get("frozen_delta") or search_delta)

    for market in rows:
        if is_paper_autobet_candidate(market):
            _maybe_act("search", market, search_theta, family=search_family, delta=search_delta)
            if frozen is not None:
                _maybe_act("exam", market, float(frozen), family=exam_family, delta=exam_delta)

        result = str(market.get("result") or "").strip().lower()
        ticker = str(market.get("ticker") or "")
        if result not in {"yes", "no"} or not ticker:
            continue
        _write_settle_row(market, result)
        _search_row, newly_search = apply_settle("search", ticker, kalshi_result=result, step_theta=True)
        if newly_search:
            apply_search_starvation()
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
                        parked = park_exam(f"futility at n={n}: remaining skips cannot pass")
                        from golf_offshoot.honer_15m.fee import apply_factory_fee

                        apply_factory_fee()
                        write_exam_scorecard(parked, outcome="parked")
                        _close_exam_to_library(parked, outcome="parked")
                        apply_search_starvation()
                elif n >= int(pol["exam_n"]):
                    completed = complete_exam()
                    from golf_offshoot.honer_15m.fee import apply_factory_fee

                    apply_factory_fee()
                    outcome = classify_completed_exam()
                    write_exam_scorecard(completed, outcome=outcome)
                    _close_exam_to_library(completed, outcome=outcome)
                    apply_search_starvation()

    maybe_advance()
    fired = fire_freeze()
    from golf_offshoot.honer_15m.quality import save_quote_quality

    save_quote_quality()
    _write_last_tick(markets=len(rows), quote_bus_stale=stale)
    try:
        from golf_offshoot.honer_15m.invariants import run_invariants

        run_invariants()
    except Exception:
        pass
    try:
        from golf_offshoot.honer_15m.illustrate import maybe_render

        maybe_render()
    except Exception:
        pass
    live = load_theta()
    from golf_offshoot.honer_15m.keep import load_bar

    bar = load_bar()
    return {
        "lane": "honer_15m",
        "search_theta": float(live["theta"]),
        "active_family": str(live.get("active_family") or FAMILY_RICH),
        "exam": load_exam_state(),
        "froze": bool(fired),
        "markets": len(rows),
        "trading_armed": False,
        "fee_omitted": bool(bar.get("fee_omitted", True)),
        "http_fetches": 0,
        "quote_bus_stale": stale,
    }
