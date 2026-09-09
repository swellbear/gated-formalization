"""Honer standing and window stories from honer files only.

Template sentences plus file fields. No free-written why. Never reads
learning_lane_15m paper, ledger, or journal.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from golf_offshoot.honer_15m.books import load_decisions, load_ledger
from golf_offshoot.honer_15m.freeze import freeze_ready, load_exam_state, load_trials
from golf_offshoot.honer_15m.paths import (
    freeze_log_path,
    latest_dir,
    paper_dir,
    settlements_dir,
)
from golf_offshoot.honer_15m.library import load_library
from golf_offshoot.honer_15m.policy import FAMILY_RICH, FAMILY_SPREAD, load_policy
from golf_offshoot.honer_15m.theta import load_theta
from golf_offshoot.honer_15m.watch import load_watch_status
from golf_offshoot.localtime import format_eastern, now, to_eastern

WAITING = "still waiting on Kalshi"
DO_NOT_ADD = "Do not add these two."
MAX_HTML_SEARCH = 48
MAX_PNG_ROWS = 24
MAX_HAPPENED = 8
MAX_THETA_TRAIL = 12


@dataclass(frozen=True)
class HonerRow:
    ticker: str
    window_id: str
    window_et: str
    action: str
    action_label: str
    posted_yes: float | None
    theta: float | None
    why: str
    why_short: str
    kalshi_result: str
    pnl: float | None
    pnl_text: str
    source: str
    book: str
    exam_k: int | None = None
    fill_all_pnl: float | None = None
    d: float | None = None
    fill_all_text: str = ""
    d_text: str = ""
    pending: bool = True
    close_at: str = ""
    at: str = ""
    near_line: bool | None = None
    near_line_text: str = "n/a"
    spread: float | None = None
    delta: float | None = None
    spread_text: str = "n/a"
    delta_text: str = "n/a"


@dataclass
class HonerStanding:
    what_it_is: str
    where_it_stands: str
    last_happened: str
    two_books: str
    glossary: str
    not_a_keep: str
    happened: list[str] = field(default_factory=list)
    theta_trail: str = ""
    phase: str = "searching"
    search_rows: list[HonerRow] = field(default_factory=list)
    exam_rows: list[HonerRow] = field(default_factory=list)
    png_search_rows: list[HonerRow] = field(default_factory=list)
    png_exam_rows: list[HonerRow] = field(default_factory=list)
    search_trimmed: int = 0
    exam_trimmed: int = 0
    subtitle_lines: tuple[str, ...] = ()
    current_search: HonerRow | None = None
    current_exam: HonerRow | None = None
    library_line: str = ""
    freeze_meter: str = ""


def cents(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{round(float(value) * 100):.0f}¢"


def dollars(value: float | None, *, signed: bool = False) -> str:
    if value is None:
        return WAITING
    num = float(value)
    if signed:
        return f"${num:+.2f}"
    return f"${num:.2f}"


def window_et_label(*, ticker: str = "", close_at: str = "", window_id: str = "") -> str:
    if close_at:
        stamp = format_eastern(close_at)
        if stamp and stamp != "n/a" and stamp != close_at:
            # "2026-09-09 14:00 EDT" → "14:00 ET"
            parts = stamp.split()
            if len(parts) >= 2 and ":" in parts[1]:
                return f"{parts[1]} ET"
            return stamp
    parts = str(window_id or "").split("__")
    if len(parts) >= 3:
        stamp = format_eastern(parts[-1].replace("-", ":", 2) if "T" in parts[-1] else parts[-1])
        if stamp and stamp != "n/a":
            bits = stamp.split()
            if len(bits) >= 2 and ":" in bits[1]:
                return f"{bits[1]} ET"
    token = str(ticker or "").rsplit("-", 2)
    if len(token) >= 2 and token[-2][-4:].isdigit():
        hhmm = token[-2][-4:]
        return f"{hhmm[:2]}:{hhmm[2:]} ET"
    return "window ET unknown"


def family_label(family: str) -> str:
    if str(family) == FAMILY_SPREAD:
        return "skip-wide-spread"
    return "skip-rich-YES"


def freeze_meter(
    theta_state: dict[str, Any] | None = None,
    *,
    policy: dict[str, Any] | None = None,
) -> str:
    """One-line freeze progress from honer files. Not a keep."""
    pol = policy or load_policy()
    st = theta_state if theta_state is not None else load_theta()
    need_n = int(pol["freeze_min_search_settled"])
    need_delta = float(pol["freeze_abs_delta"])
    stable_need = int(pol["freeze_stable_windows"])
    theta_now = float(st.get("theta") or pol["start_theta"])
    last_declared = float(st.get("last_declared_theta") or pol["start_theta"])
    settled = int(st.get("in_band_settled") or 0)
    far = int(st.get("far_settled_since_freeze") or 0)
    stable = int(st.get("in_band_stable") or 0)
    family = family_label(str(st.get("active_family") or FAMILY_RICH))
    if freeze_ready(st):
        return "Honer freeze: ready — next tick can open exam. Not a keep."
    moved = abs(theta_now - last_declared)
    return (
        f"Honer freeze: {settled}/{need_n} in-band · {far} far ignored · "
        f"moved {cents(moved)} of {cents(need_delta)} · "
        f"stable {stable}/{stable_need} · line {cents(theta_now)} · {family}"
    )


def library_english(
    lib: dict[str, Any] | None = None,
    *,
    family: str,
    clip_streak: int,
    clip_need: int,
    quote_ok: bool | None = None,
) -> str:
    payload = lib if lib is not None else load_library()
    rows = list(payload.get("rows") or [])
    last = ""
    if rows and isinstance(rows[-1], dict):
        last = str(rows[-1].get("outcome") or "")
    if last == "parked":
        exam_bit = "Last exam stopped early (futility). That cutoff is retired."
    elif last == "completed_dead":
        exam_bit = (
            "Last exam finished 70; mean was not above zero. That cutoff is retired. Not a score."
        )
    elif last == "completed_unscored":
        exam_bit = "Last exam finished 70; means were above zero. Still not a keep."
    else:
        exam_bit = "No exam yet."
    retired_n = len(list(payload.get("retired") or []))
    next_bit = "θ still walking"
    if payload.get("catalog_exhausted"):
        next_bit = "catalog exhausted — no new family"
    elif family == FAMILY_SPREAD:
        next_bit = "spread family walking; no further family after clip"
    elif int(clip_streak) >= int(clip_need):
        waiting = quote_ok is False
        if quote_ok is None:
            try:
                from golf_offshoot.honer_15m.quality import quote_quality_ok

                waiting = not quote_quality_ok()
            except Exception:
                waiting = False
        if waiting:
            next_bit = "θ on clip; spread family waiting on quotes"
        else:
            next_bit = "next family is skip-wide-spread"
    return (
        f"{exam_bit} {retired_n} retired snapshot(s). Next: {next_bit}. "
        "Not a keep; fee omitted."
    )


def action_label(action: str) -> str:
    if action == "fill":
        return "Filled YES"
    if action == "skip":
        return "Skipped"
    return str(action or "no decision")


def _in_band(posted: Any, theta: Any, band: float) -> bool:
    if posted is None or theta is None:
        return False
    try:
        return abs(float(posted) - float(theta)) <= float(band)
    except (TypeError, ValueError):
        return False


def theta_step_clause(
    action: str,
    result: str,
    *,
    step: float,
    posted_yes: Any = None,
    theta: Any = None,
    band: float = 0.10,
) -> str:
    result = str(result or "").strip().lower()
    if result not in {"yes", "no"}:
        return ""
    near = _in_band(posted_yes, theta, band)
    if action == "fill" and result == "no" and near:
        return f"Cutoff fell {cents(step)} (loss near the line; skip more)."
    if action == "skip" and result == "yes" and near:
        return f"Cutoff rose {cents(step)} (missed a YES near the line; skip less)."
    if (action == "fill" and result == "no") or (action == "skip" and result == "yes"):
        return "Cutoff unchanged (ticket was not near the line)."
    return "Cutoff unchanged (fill won, or skip+NO)."


def why_sentence(row: dict[str, Any], *, book: str, step: float, band: float = 0.10) -> tuple[str, str]:
    action = str(row.get("action") or "")
    posted = row.get("posted_yes")
    theta = row.get("theta")
    posted_s = cents(float(posted) if posted is not None else None)
    cutoff_s = cents(float(theta) if theta is not None else None)
    reason = str(row.get("reason") or "")
    if action == "skip" and reason.startswith("spread"):
        spread_s = cents(float(row["spread"]) if row.get("spread") is not None else None)
        delta_s = cents(float(row["delta"]) if row.get("delta") is not None else None)
        core = (
            f"Skipped: bid/ask spread {spread_s} was at or above the {delta_s} wide-book line."
        )
        short = f"skipped wide spread {spread_s} vs {delta_s}"
    elif action == "skip":
        core = f"Skipped: market YES {posted_s} was at or above the {cutoff_s} cutoff (too rich)."
        short = f"skipped at {posted_s} vs cutoff {cutoff_s}"
    elif action == "fill":
        core = f"Filled YES: market YES {posted_s} was below the {cutoff_s} cutoff."
        short = f"filled YES at {posted_s} vs cutoff {cutoff_s}"
    else:
        core = f"No honer decision on file for this window."
        short = "no decision"
    if book == "exam":
        core = f"{core} Exam used frozen cutoff {cutoff_s}; search cutoff may have been different."
    result = str(row.get("kalshi_result") or "").strip().lower()
    if book == "search":
        extra = theta_step_clause(
            action,
            result,
            step=step,
            posted_yes=posted,
            theta=theta,
            band=band,
        )
        if extra:
            core = f"{core} {extra}"
            short = f"{short}; {extra.rstrip('.')}"
    if book == "exam" and row.get("settled_at") and row.get("d") is not None and row.get("fill_all_pnl") is not None:
        fill_all = dollars(float(row["fill_all_pnl"]), signed=True)
        d_s = dollars(float(row["d"]), signed=True)
        if action == "skip":
            core = (
                f"{core} Skip vs always-buy: always-buy would have been {fill_all}, "
                f"so this skip's score is {d_s}."
            )
        else:
            core = f"{core} Fill matches always-buy on this window, so d is $0.00."
    return core, short


def _parse_when(raw: str) -> datetime | None:
    text = str(raw or "").strip()
    if not text:
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        return to_eastern(datetime.fromisoformat(text))
    except ValueError:
        return None


def _freeze_log() -> list[dict[str, Any]]:
    path = freeze_log_path()
    if not path.is_file():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    return payload if isinstance(payload, list) else []


def _exam_k_for(row: dict[str, Any]) -> int | None:
    if row.get("exam_k") not in (None, ""):
        try:
            return int(row["exam_k"])
        except (TypeError, ValueError):
            return None
    at = _parse_when(str(row.get("at") or ""))
    if at is None:
        return None
    chosen = None
    for entry in _freeze_log():
        declared = _parse_when(str(entry.get("declared_at") or ""))
        if declared is None or at < declared:
            continue
        try:
            chosen = int(entry.get("k_after") or 0) or None
        except (TypeError, ValueError):
            continue
    return chosen


def _kalshi_from_honer_settle(ticker: str, row: dict[str, Any]) -> str:
    result = str(row.get("kalshi_result") or "").strip().lower()
    if result in {"yes", "no"}:
        return result
    from golf_offshoot.honer_15m.paths import safe_artifact_stem

    dest = settlements_dir() / f"{safe_artifact_stem(ticker)}.json"
    if not dest.is_file():
        return ""
    try:
        payload = json.loads(dest.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return ""
    got = str(payload.get("kalshi_result") or "").strip().lower()
    return got if got in {"yes", "no"} else ""


def _row_from_decision(book: str, row: dict[str, Any], *, step: float) -> HonerRow:
    ticker = str(row.get("ticker") or "")
    result = _kalshi_from_honer_settle(ticker, row)
    pending = not bool(row.get("settled_at")) or result not in {"yes", "no"}
    pnl = row.get("pnl")
    pnl_f = float(pnl) if isinstance(pnl, (int, float)) else None
    if pending:
        pnl_f = None
        pnl_text = WAITING
    elif row.get("action") == "skip":
        pnl_text = "$0.00 (no ticket)"
        pnl_f = 0.0
    else:
        pnl_text = dollars(pnl_f, signed=True)
    why, why_short = why_sentence(
        {**row, "kalshi_result": result},
        book=book,
        step=step,
        band=float(load_policy()["step_band"]),
    )
    fill_all = row.get("fill_all_pnl")
    fill_all_f = float(fill_all) if isinstance(fill_all, (int, float)) and not pending else None
    d = row.get("d")
    d_f = float(d) if isinstance(d, (int, float)) and not pending else None
    source = f"honer_15m/{book}/paper/{ticker}.json"
    if not (paper_dir(book) / f"{ticker}.json").is_file():
        from golf_offshoot.honer_15m.paths import safe_artifact_stem

        source = f"honer_15m/{book}/decisions.json"
        stem = safe_artifact_stem(ticker)
        if (paper_dir(book) / f"{stem}.json").is_file():
            source = f"honer_15m/{book}/paper/{stem}.json"
    posted_f = float(row["posted_yes"]) if row.get("posted_yes") is not None else None
    theta_f = float(row["theta"]) if row.get("theta") is not None else None
    band = float(load_policy()["step_band"])
    near = _in_band(posted_f, theta_f, band) if posted_f is not None and theta_f is not None else None
    spread_f = float(row["spread"]) if row.get("spread") is not None else None
    delta_f = float(row["delta"]) if row.get("delta") is not None else None
    return HonerRow(
        ticker=ticker,
        window_id=str(row.get("window_id") or ""),
        window_et=window_et_label(
            ticker=ticker,
            close_at=str(row.get("close_at") or ""),
            window_id=str(row.get("window_id") or ""),
        ),
        action=str(row.get("action") or ""),
        action_label=action_label(str(row.get("action") or "")),
        posted_yes=posted_f,
        theta=theta_f,
        why=why,
        why_short=why_short,
        kalshi_result=result,
        pnl=pnl_f,
        pnl_text=pnl_text,
        source=source,
        book=book,
        exam_k=_exam_k_for(row) if book == "exam" else None,
        fill_all_pnl=fill_all_f,
        d=d_f,
        fill_all_text=(
            f"always-buy would have been {dollars(fill_all_f, signed=True)}"
            if fill_all_f is not None
            else ""
        ),
        d_text=dollars(d_f, signed=True) if d_f is not None else "",
        pending=pending,
        close_at=str(row.get("close_at") or ""),
        at=str(row.get("at") or ""),
        near_line=near,
        near_line_text="yes" if near is True else ("no" if near is False else "n/a"),
        spread=spread_f,
        delta=delta_f,
        spread_text=cents(spread_f) if spread_f is not None else "n/a",
        delta_text=cents(delta_f) if delta_f is not None else "n/a",
    )


def _sort_rows(rows: list[HonerRow]) -> list[HonerRow]:
    return sorted(rows, key=lambda r: r.ticker, reverse=True)


def collect_rows(book: str) -> list[HonerRow]:
    pol = load_policy()
    step = float(pol["step"])
    rows = []
    for raw in load_decisions(book).values():
        if isinstance(raw, dict) and raw.get("ticker"):
            rows.append(_row_from_decision(book, raw, step=step))
    return _sort_rows(rows)


def _window_story(row: HonerRow, *, book: str, step: float) -> str:
    if row.pending:
        return (
            f"{row.window_et} — {row.action_label.lower()} at {cents(row.posted_yes)}; "
            f"{WAITING}."
        )
    kalshi = row.kalshi_result.upper() if row.kalshi_result else "n/a"
    money = "no ticket" if row.action == "skip" else row.pnl_text
    return f"{row.window_et} — {row.why_short}; Kalshi {kalshi}; {money}."


def _last_happened(search_rows: list[HonerRow], *, step: float) -> str:
    if not search_rows:
        return (
            "Honer has not taken a window yet. Standing is the start cutoff "
            f"{cents(load_policy()['start_theta'])}, exam idle, both books at $100."
        )
    pending = next((r for r in search_rows if r.pending), None)
    settled = next((r for r in search_rows if not r.pending), None)
    if pending and not settled:
        return (
            f"This window is still open. Honer already decided **{pending.action_label.lower()} "
            f"at {cents(pending.posted_yes)}** (cutoff {cents(pending.theta)}). "
            f"Kalshi has not posted an official result. Paper pnl is not known yet — not zero."
        )
    if pending:
        open_line = (
            f"This window is still open. Honer already decided **{pending.action_label.lower()} "
            f"at {cents(pending.posted_yes)}** (cutoff {cents(pending.theta)}). "
            f"Kalshi has not posted an official result. Paper pnl is not known yet — not zero."
        )
    else:
        open_line = ""
    if settled is None:
        return open_line
    result = settled.kalshi_result.upper()
    if settled.action == "skip":
        body = (
            f"Last settled window **{settled.window_et}**: the market's YES was **{cents(settled.posted_yes)}**. "
            f"Cutoff was **{cents(settled.theta)}**, so honer **skipped** — the ticket looked too expensive. "
            f"Kalshi later said **{result}**. Search had no ticket, so paper pnl is **$0**. "
            f"{theta_step_clause(settled.action, settled.kalshi_result, step=step, posted_yes=settled.posted_yes, theta=settled.theta, band=float(load_policy()['step_band']))}"
        ).strip()
    else:
        body = (
            f"Last settled window **{settled.window_et}**: the market's YES was **{cents(settled.posted_yes)}**. "
            f"Cutoff was **{cents(settled.theta)}**, so honer **filled YES**. "
            f"Kalshi later said **{result}**. Search paper pnl is **{settled.pnl_text}**. "
            f"{theta_step_clause(settled.action, settled.kalshi_result, step=step, posted_yes=settled.posted_yes, theta=settled.theta, band=float(load_policy()['step_band']))}"
        ).strip()
    if open_line:
        return f"{open_line} {body}"
    return body


def _phase_paragraph(
    *,
    theta_now: float,
    last_declared: float,
    settled_since: int,
    need_n: int,
    need_delta: float,
    exam: dict[str, Any],
    trials: dict[str, Any],
) -> tuple[str, str]:
    moved = abs(theta_now - last_declared)
    if exam.get("parked"):
        reason = str(exam.get("park_reason") or "futility")
        k = int(exam.get("k_after") or trials.get("trials_to_date") or 0)
        n = int(exam.get("n") or 0)
        return (
            "exam_parked",
            f"Exam k={k} parked at n={n}: {reason} This is still not a keep. Search continues.",
        )
    if exam.get("open"):
        k = int(exam.get("k_after") or trials.get("trials_to_date") or 0)
        n = int(exam.get("n") or 0)
        frozen = float(exam.get("frozen_theta") or 0)
        return (
            "exam_open",
            f"Exam k={k} is running. For these 70 windows the cutoff is frozen at {cents(frozen)}. "
            f"Search may still move its own cutoff; that does not change this exam. "
            f"Scored **{n} of 70**. Futility check is at n=20 and n=40.",
        )
    if exam.get("completed"):
        k = int(exam.get("k_after") or trials.get("trials_to_date") or 0)
        n = int(exam.get("n") or 0)
        return (
            "exam_complete",
            f"Exam k={k} finished {n} windows. This is still not a keep. Search continues.",
        )
    if freeze_ready():
        nxt = int(trials.get("trials_to_date") or 0) + 1
        return (
            "freeze_ready",
            f"Novelty and stability are both met. Next honer tick can start exam k={nxt} "
            f"at frozen θ={cents(theta_now)}. This is not a keep.",
        )
    stable_need = int(load_policy()["freeze_stable_windows"])
    live = load_theta()
    stable_have = int(live.get("in_band_stable") or 0)
    far = int(live.get("far_settled_since_freeze") or 0)
    return (
        "searching",
        f"Right now it is **searching**. The exam book is empty on purpose. "
        f"Exam starts only after freeze: {need_n} **in-band** settled search windows, "
        f"θ moved by at least {cents(need_delta)} from the last declared cutoff, **and** "
        f"{stable_need} in-band windows with no cutoff move. Far tickets do not count. "
        f"In-band so far: **{settled_since} of {need_n}**. Far ignored: **{far}**. "
        f"θ has moved **{cents(moved)}** from {cents(last_declared)}. "
        f"In-band stable: **{stable_have} of {stable_need}**. Freeze is not ready.",
    )


def collect_standing() -> HonerStanding:
    pol = load_policy()
    step = float(pol["step"])
    start = float(pol["start_theta"])
    need_n = int(pol["freeze_min_search_settled"])
    need_delta = float(pol["freeze_abs_delta"])
    th = load_theta()
    theta_now = float(th.get("theta") or start)
    last_declared = float(th.get("last_declared_theta") or start)
    settled_since = int(th.get("in_band_settled") or 0)
    exam = load_exam_state()
    trials = load_trials()
    search_rows = collect_rows("search")
    exam_rows = collect_rows("exam")
    search_led = load_ledger("search")
    exam_led = load_ledger("exam")
    phase, where = _phase_paragraph(
        theta_now=theta_now,
        last_declared=last_declared,
        settled_since=settled_since,
        need_n=need_n,
        need_delta=need_delta,
        exam=exam,
        trials=trials,
    )
    family = str(th.get("active_family") or "H-SKIP-RICH-YES")
    family_bit = (
        "Family is skip-a-wide-bid/ask (θ locked as a seed)."
        if family == FAMILY_SPREAD
        else "Family is skip-rich-YES."
    )
    what = (
        "Honer is not predicting up or down. Each 15-minute window it either takes a paper YES "
        "ticket at the market's posted price, or it skips. It never buys NO. "
        f"{family_bit} Only tickets within 10¢ of the line move the cutoff; "
        "a loss near the line tightens it, a missed YES loosens it. "
        "Freeze counts only those in-band tickets. "
        f"Cutoff now is **{cents(theta_now)}**. Search started at {cents(start)}. Not a keep."
    )
    lib = load_library()
    library_line = library_english(
        lib,
        family=family,
        clip_streak=int(th.get("clip_streak") or 0),
        clip_need=int(pol["clip_exhaust_windows"]),
    )
    meter = freeze_meter(th, policy=pol)
    exam_line = "Exam (frozen cutoff, own $100): not started."
    if exam.get("open") or exam.get("completed") or exam.get("parked") or exam_rows:
        exam_line = (
            f"Exam (frozen cutoff, own $100): bankroll {dollars(float(exam_led.get('bankroll') or 0))} "
            f"paper pnl {dollars(float(exam_led.get('betting_pnl') or 0), signed=True)} "
            f"{int(exam_led.get('fills') or 0)} fill, {int(exam_led.get('skips') or 0)} skips."
        )
    two = (
        f"Search (discovery, cutoff may move): bankroll {dollars(float(search_led.get('bankroll') or 0))}, "
        f"paper pnl {dollars(float(search_led.get('betting_pnl') or 0), signed=True)}, "
        f"{int(search_led.get('fills') or 0)} fill, {int(search_led.get('skips') or 0)} skips. "
        f"{exam_line} {DO_NOT_ADD}"
    )
    glossary = (
        "Fill = paper YES ticket at the posted price. Skip = no ticket this window. "
        "Cutoff θ = richness line, in cents. Only tickets within 10¢ of the line move it. "
        "Exam = a later frozen test, not a keep. Library labels are not scores."
    )
    not_keep = "Not a keep; fee omitted. can_keep is false on this bar."
    exam_pnl = float(exam_led.get("betting_pnl") or 0)
    if (exam.get("open") or exam.get("completed")) and exam_pnl > 0:
        not_keep = (
            "A green exam book is not a keep. Freeze was for search novelty. "
            "Scoring is later and separate. Fee omitted."
        )
    chronological = list(reversed(search_rows))
    trail_vals = [cents(r.theta) for r in chronological[-MAX_THETA_TRAIL:] if r.theta is not None]
    trail = " → ".join(trail_vals) if trail_vals else cents(theta_now)
    happened = [_window_story(r, book="search", step=step) for r in search_rows[:MAX_HAPPENED]]
    png_search = search_rows[:MAX_PNG_ROWS]
    png_exam = exam_rows[:MAX_PNG_ROWS]
    bus_line = "Quote bus: n/a"
    try:
        from golf_offshoot.quote_bus import clock_line

        bus_line = clock_line()
    except Exception:
        pass
    subtitle = (
        meter,
        f"lane=honer_15m · {family_label(family)} · local_regret_v2 · freeze in_band_v1 · not a keep",
        f"Trading NOT ARMED · fee omitted · books do not merge · rendered {format_eastern(now())}",
        bus_line,
    )
    current_search = search_rows[0] if search_rows else None
    current_exam = next((r for r in exam_rows if current_search and r.ticker == current_search.ticker), None)
    if current_exam is None and exam_rows and exam.get("open"):
        current_exam = exam_rows[0]
    return HonerStanding(
        what_it_is=what,
        where_it_stands=where,
        last_happened=_last_happened(search_rows, step=step),
        two_books=two,
        glossary=glossary,
        not_a_keep=not_keep,
        happened=happened,
        theta_trail=trail,
        phase=phase,
        search_rows=search_rows[:MAX_HTML_SEARCH],
        exam_rows=exam_rows,
        png_search_rows=png_search,
        png_exam_rows=png_exam,
        search_trimmed=max(0, len(search_rows) - MAX_PNG_ROWS),
        exam_trimmed=max(0, len(exam_rows) - MAX_PNG_ROWS),
        subtitle_lines=subtitle,
        current_search=current_search,
        current_exam=current_exam,
        library_line=library_line,
        freeze_meter=meter,
    )


def current_search_action() -> dict[str, Any]:
    standing = collect_standing()
    row = standing.current_search
    if row is None:
        return {
            "ticker": "",
            "window_et": "",
            "phrase": "no decision yet",
            "kalshi": "n/a",
        }
    kalshi = WAITING if row.pending else (row.kalshi_result.upper() if row.kalshi_result else "n/a")
    posted = cents(row.posted_yes)
    cutoff = cents(row.theta)
    if row.near_line is False:
        phrase = f"{row.action_label.lower()} at {posted}, not near the {cutoff} line"
    elif row.action == "skip":
        phrase = f"skipped ({posted} at or above the {cutoff} cutoff)"
    elif row.near_line is True:
        phrase = f"filled YES at {posted}, near the {cutoff} line"
    else:
        phrase = f"{row.action_label.lower()} at {posted} vs {cutoff}"
    return {
        "ticker": row.ticker,
        "window_et": row.window_et,
        "phrase": phrase,
        "kalshi": kalshi,
        "action": row.action,
        "near_line": row.near_line,
    }


def current_exam_action() -> dict[str, Any]:
    exam = load_exam_state()
    if not exam.get("open") and not exam.get("completed"):
        return {"ticker": "", "phrase": "not started", "action": ""}
    standing = collect_standing()
    row = standing.current_exam
    if row is None:
        return {"ticker": "", "phrase": "no exam decision this window", "action": ""}
    return {
        "ticker": row.ticker,
        "phrase": (
            f"{row.action_label.lower()} ({cents(row.posted_yes)} vs frozen {cents(row.theta)})"
        ),
        "action": row.action,
    }


def watch_clock() -> dict[str, Any]:
    watch = load_watch_status()
    at = str(watch.get("at") or "")
    stale = False
    parsed = _parse_when(at)
    if not watch.get("running"):
        stale = True
    elif parsed is not None:
        stale = (now() - parsed).total_seconds() > 180
    return {
        "running": bool(watch.get("running")),
        "cycles": int(watch.get("cycles") or 0),
        "last": str(watch.get("last_summary") or ""),
        "at": format_eastern(at) if at else "n/a",
        "stale": stale,
        "png_mtime": _png_mtime(),
        "pid": watch.get("pid"),
        "sidecar": bool(watch.get("sidecar")),
        "quote_bus_stale": bool(watch.get("quote_bus_stale")),
    }


def _png_mtime() -> str:
    path = latest_dir() / "honer_window_strip.png"
    if not path.is_file():
        return "not yet available"
    try:
        return format_eastern(datetime.fromtimestamp(path.stat().st_mtime).astimezone())
    except OSError:
        return "not yet available"
