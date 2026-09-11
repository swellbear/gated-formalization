"""15m operator-shell chrome. Display copy only.

Does not start, stop, or replace PaperWatch. Does not invent pnl, merge
lineages, or restyle golf WC1 / Ill. Trading stays NOT ARMED.
"""

from __future__ import annotations

import html
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from golf_offshoot.learning_lane_15m.paths import LANE_15M, LANE_GOLF, PRIMARY_SERIES
from golf_offshoot.operator_surface.lanes import CANONICAL_LANES, SELECTOR_FIELD
from golf_offshoot.operator_surface.modes import AI_NO_CASH, PAPER_ONLY
from golf_offshoot.operator_surface.runner import RunRecord, format_run_record

HEADER_TITLE = "KXBTC15M paper watch"
HEADER_KICKER = "15-min Kalshi learning lane"
TRUST_LINE = "Paper · not armed"
MARKET_LOCK_NOTE = "market lock"

#: Home tabs. Thin on purpose — the glance + board stay the trading-terminal home.
TABS = (
    ("home", "Home"),
    ("scoreboard", "Scoreboard"),
    ("lab", "Lab"),
    ("ops", "Ops"),
    ("bot-hub", "Bot-hub"),
)

#: POST values stay ingest/live/shadow/loop/refresh. Labels match what the 15m lane does.
ACTION_BUTTONS_15M = (
    (
        "ingest",
        "Fetch KXBTC15M",
        "Public KXBTC15M fetch. Observation only. PaperWatch already does this on the loop.",
    ),
    (
        "live",
        "Paper cycle",
        "One extra fetch → paper autobet → settle join. PaperWatch already loops this.",
    ),
    (
        "shadow",
        "Re-read journal",
        "Re-read the 15m journal from disk. Nothing is placed.",
    ),
    (
        "loop",
        "Extra cycle",
        "One extra cycle now. PaperWatch remains the loop; this button is an extra.",
    ),
    (
        "refresh",
        "Reload files",
        "Re-read saved files from disk. No run is started.",
    ),
)

CHART_15M_TITLE = "KXBTC15M paper windows — 15-minute board"
CHART_15M_PLAIN = (
    "The PNG already draws paper PnL where a window's own book records it, and it draws "
    "lineage A (local paper book) apart from lineage B (published Pages). Those books are "
    "never summed. A window with no book has no pnl — not 0. A window with no Kalshi "
    "result on disk stays SETTLE_PENDING. A missing paper join is not a pending window."
)
CHART_15M_SUB = (
    "Read-only PNG from settlements/*.json, latest/journal.json, paper/*.json and the "
    "published manifest. Lineage A P/L is that book's recorded numbers. Missing join ≠ "
    "pending. No golf WC1 / Ill board."
)
CHART_15M_MISSING = (
    "15m chart not yet available. The Illustrator regenerates it from the join files; nothing is "
    "drawn in its place. No golf WC1 / Ill here."
)
CHART_15M_NAMED = 6

_JOIN_LIMIT = 4
_LAB_NOTE = "LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md"
_GOLF_STAMP = (
    Path(__file__).resolve().parents[3] / "docs" / "phase1_dryrun" / "OPERATOR_STATUS_STAMP.md"
)


def chart_15m_path():
    """The Illustrator's 15m PNG, when it is actually on disk."""
    try:
        from golf_offshoot.learning_lane_15m.illustrate import chart_png_path

        path = chart_png_path()
    except Exception:
        return None
    return path if path.is_file() else None


def window_rows_15m() -> list:
    """Window rows as the Illustrator reads them. Display copy only, never written."""
    try:
        from golf_offshoot.learning_lane_15m.illustrate import collect_rows

        paper_rows, tape_rows = collect_rows()
    except Exception:
        return []
    return list(paper_rows) + list(tape_rows)


def window_summary_15m(rows: list, *, limit: int = CHART_15M_NAMED) -> tuple[str, str]:
    """(counts line, named-windows line) for the caption.

    Every figure here is copied from a file. ``yes``/``no`` are Kalshi results that
    already exist on disk. A missing paper join is counted apart from SETTLE_PENDING.
    """
    if not rows:
        return ("", "")
    yes = no = pending = missing = 0
    named: list[str] = []
    for row in rows:
        result = str(getattr(row, "kalshi_result", "") or "").strip().lower()
        status = str(getattr(row, "settle_status", "") or "").strip() or "unknown"
        ticker = str(getattr(row, "ticker", "") or "")
        missing_join = bool(getattr(row, "missing_join", False))
        if result == "yes":
            yes += 1
        elif result == "no":
            no += 1
        elif missing_join:
            missing += 1
        else:
            pending += 1
        if ticker and len(named) < max(0, int(limit)):
            if missing_join:
                named.append(f"{ticker} · missing paper join")
            elif result in ("yes", "no"):
                named.append(f"{ticker} · {status} · result={result}")
            elif status.upper() == "SETTLE_PENDING":
                named.append(f"{ticker} · SETTLE_PENDING")
            else:
                named.append(f"{ticker} · {status} · SETTLE_PENDING")
    joins = sum(
        1
        for row in rows
        if getattr(row, "paper_join", False) and not getattr(row, "missing_join", False)
    )
    counts = (
        f"{len(rows)} {PRIMARY_SERIES} window(s) on the board — {joins} paper-book join(s), "
        f"{len(rows) - joins} Kalshi-only journal row(s) · "
        f"settled result=yes {yes} · settled result=no {no} · SETTLE_PENDING {pending} · "
        f"missing paper join {missing}"
    )
    if not named:
        return (counts, "")
    rest = len(rows) - len(named)
    tail = f" · +{rest} more on the board" if rest > 0 else ""
    return (counts, "Windows: " + "; ".join(named) + tail)


def _esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def _watch_status(state: dict | None = None) -> dict[str, Any]:
    live: dict[str, Any] | None = None
    if state and state.get("paper_watch") is not None:
        try:
            live = state["paper_watch"].status()
        except Exception:
            live = None
    from golf_offshoot.learning_lane_15m.watch import load_watch_status

    file_st = load_watch_status()
    if live is not None:
        return live
    return file_st if isinstance(file_st, dict) else {}


def _load_wake() -> dict[str, Any] | None:
    try:
        from golf_offshoot.learning_lane_15m.learn import load_wake_state

        wake = load_wake_state()
    except Exception:
        return None
    return wake if isinstance(wake, dict) else None


def _fmt_when(value: object) -> str:
    if not value:
        return ""
    try:
        from golf_offshoot.localtime import format_eastern

        text = format_eastern(value)
    except Exception:
        text = str(value)
    return "" if text in {"", "n/a"} else text


def _ledger_a() -> tuple[str, str]:
    """Lineage A bankroll and betting_pnl as recorded on ledger.json. Never summed."""
    try:
        from golf_offshoot.learning_lane_15m.paper import load_ledger

        led = load_ledger()
    except Exception:
        return ("", "")
    try:
        pnl = f"{float(led.betting_pnl):+.2f}"
        bankroll = f"{float(led.bankroll):.2f}"
    except (TypeError, ValueError):
        return ("", "")
    return (pnl, bankroll)


def _close_epoch(*, ticker: str, window_id: str = "", close_time: str = "") -> float | None:
    raw = str(close_time or "").strip()
    if raw:
        text = raw[:-1] + "+00:00" if raw.endswith("Z") else raw
        try:
            parsed = datetime.fromisoformat(text)
        except ValueError:
            parsed = None
        if parsed is not None:
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            return parsed.timestamp()
    try:
        from golf_offshoot.learning_lane_15m.learn import _ticker_close_epoch, _window_close_epoch

        stamp = _window_close_epoch(window_id, ticker)
        if stamp is not None:
            return stamp
        return _ticker_close_epoch(ticker)
    except Exception:
        return None


def _clock_label(epoch: float | None) -> str:
    """Live window clock from a close epoch already on file. Not settle evidence."""
    if epoch is None:
        return "window close not on file"
    remaining = epoch - datetime.now(timezone.utc).timestamp()
    if remaining <= 0:
        return "window close passed — wait for Kalshi result"
    mins = int(remaining // 60)
    secs = int(remaining % 60)
    return f"{mins}:{secs:02d}"


def _next_window_chip(ticker: str, window_id: str = "", close_time: str = "") -> str:
    return _clock_label(
        _close_epoch(ticker=ticker, window_id=window_id, close_time=close_time)
    )


def _open_position_model() -> dict[str, Any]:
    """Open paper fill copied from this tree's book. None invented."""
    from golf_offshoot.learning_lane_15m.paper import event_ticker_from_book, iter_books

    for rec in iter_books():
        if rec.settled_at is not None:
            continue
        if not rec.book.positions:
            continue
        pos = rec.book.positions[0]
        name = str(pos.player_name or "")
        side = "YES" if name.upper().startswith("YES") else (name or "paper")
        mark = pos.fill_price if pos.fill_price is not None else pos.entry_market_p
        return {
            "ticker": str(pos.player_id or event_ticker_from_book(rec)),
            "window_id": str(rec.tournament_id or ""),
            "stake": pos.stake,
            "mark": mark,
            "side": side,
            "intent": str(pos.intent or "hold"),
        }
    return {}


def _last_settled_join_line() -> str:
    from golf_offshoot.learning_lane_15m.paper import event_ticker_from_book, iter_books

    settled = [rec for rec in iter_books() if rec.settled_at is not None]
    if not settled:
        return ""

    def _when(rec: Any) -> datetime:
        at = rec.settled_at
        if at.tzinfo is None:
            return at.replace(tzinfo=timezone.utc)
        return at

    rec = max(settled, key=_when)
    tickers = _book_tickers(rec)
    ticker = str(tickers[0] if tickers else event_ticker_from_book(rec))
    if rec.settlement_pnl is None:
        pnl = "no pnl on disk"
    else:
        pnl = f"pnl={float(rec.settlement_pnl):+.2f}"
    when = _fmt_when(rec.settled_at)
    extra = f" {when}" if when else ""
    return f"last joined {ticker} {pnl}{extra} — this book's recorded number"


def _current_window(scan: dict[str, Any], journal: list[dict[str, Any]]) -> dict[str, str]:
    """Current KXBTC15M window copied from an open book, else pending, else journal."""
    from golf_offshoot.learning_lane_15m.paper import event_ticker_from_book, iter_books

    for rec in iter_books():
        if rec.settled_at is not None:
            continue
        tickers = [pos.player_id for pos in rec.book.positions if pos.player_id]
        ticker = str(tickers[0] if tickers else event_ticker_from_book(rec))
        if ticker:
            return {
                "ticker": ticker,
                "window_id": str(rec.tournament_id or ""),
                "close_time": "",
                "kind": "open_book",
            }
    pending = [row for row in (scan.get("pending") or []) if isinstance(row, dict)]
    if pending:
        row = pending[0]
        return {
            "ticker": str(row.get("ticker") or ""),
            "window_id": str(row.get("window_id") or ""),
            "close_time": "",
            "kind": "pending",
        }
    for window in reversed(journal):
        status = str(window.get("status") or "").strip().lower()
        result = str(window.get("result") or "").strip().lower()
        ticker = str(window.get("ticker") or "").strip()
        if not ticker:
            continue
        if status in {"active", "open", "initialized"} or (not result and status not in {"finalized", "settled"}):
            return {
                "ticker": ticker,
                "window_id": str(window.get("window_id") or ""),
                "close_time": str(window.get("close_time") or ""),
                "kind": "journal",
            }
    if journal:
        window = journal[-1]
        return {
            "ticker": str(window.get("ticker") or ""),
            "window_id": str(window.get("window_id") or ""),
            "close_time": str(window.get("close_time") or ""),
            "kind": "journal_last",
        }
    return {"ticker": "", "window_id": "", "close_time": "", "kind": "none"}


def _scan_and_journal() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    scan: dict[str, Any] = {}
    journal: list[dict[str, Any]] = []
    try:
        from golf_offshoot.learning_lane_15m.learn import load_wake_state

        wake = load_wake_state() or {}
        scan = wake.get("scan") if isinstance(wake.get("scan"), dict) else {}
    except Exception:
        scan = {}
    try:
        from golf_offshoot.learning_lane_15m.learn import _journal_rows

        journal = list(_journal_rows())
    except Exception:
        journal = []
    if not scan:
        try:
            from golf_offshoot.learning_lane_15m.learn import scan_learning_evidence

            scan = scan_learning_evidence()
        except Exception:
            scan = {}
    return scan, journal


def glance_model(state: dict | None = None) -> dict[str, Any]:
    """Glance figures copied from files already on this tree. No invented pnl."""
    watch = _watch_status(state)
    running = bool(watch.get("running"))
    last_ok = watch.get("last_ok", True)
    if running and last_ok is False:
        watch_kind = "fail"
        watch_label = "Watch on — last cycle failed"
    elif running:
        watch_kind = "on"
        watch_label = "Watch on"
    else:
        watch_kind = "off"
        watch_label = "Watch off"
    scan, journal = _scan_and_journal()
    current = _current_window(scan, journal)
    pending = [row for row in (scan.get("pending") or []) if isinstance(row, dict)]
    missing = [row for row in (scan.get("paper_join_missing") or []) if isinstance(row, dict)]
    pnl, bankroll = _ledger_a()
    close_epoch = (
        _close_epoch(
            ticker=current.get("ticker") or "",
            window_id=current.get("window_id") or "",
            close_time=current.get("close_time") or "",
        )
        if current.get("ticker")
        else None
    )
    next_chip = (
        _clock_label(close_epoch)
        if current.get("ticker")
        else "no current window on file"
    )
    return {
        "watch_kind": watch_kind,
        "watch_label": watch_label,
        "watch_summary": str(watch.get("last_summary") or ""),
        "ticker": current.get("ticker") or PRIMARY_SERIES,
        "current_kind": current.get("kind") or "none",
        "pending": pending,
        "missing": missing,
        "lineage_a_pnl": pnl,
        "lineage_a_bankroll": bankroll,
        "next_chip": next_chip,
        "close_epoch": close_epoch,
        "series": PRIMARY_SERIES,
    }


def glance_chips_html(state: dict | None = None, *, model: dict[str, Any] | None = None) -> str:
    data = model if model is not None else glance_model(state)
    watch_kind = data["watch_kind"]
    pending = data["pending"]
    missing = data["missing"]
    pending_chip = (
        f'<span class="chip pending" data-kind="pending">'
        f"SETTLE_PENDING · {_esc(pending[0].get('ticker') or pending[0].get('window_id') or 'window')}</span>"
        if pending
        else '<span class="chip quiet" data-kind="pending-none">no pending window</span>'
    )
    missing_chip = (
        f'<span class="chip missing" data-kind="missing-join">'
        f"missing paper join · {_esc(missing[0].get('ticker') or 'window')}</span>"
        if missing
        else '<span class="chip quiet" data-kind="missing-none">no missing join</span>'
    )
    if data["lineage_a_pnl"]:
        pnl_chip = (
            f'<span class="chip pnl" data-kind="lineage-a">'
            f"lineage A P/L ${_esc(data['lineage_a_pnl'])} · bankroll ${_esc(data['lineage_a_bankroll'])}"
            "</span>"
        )
    else:
        pnl_chip = (
            '<span class="chip pnl" data-kind="lineage-a">lineage A P/L not on file — none invented</span>'
        )
    summary = data.get("watch_summary") or ""
    summary_html = f'<span class="watch-summary">{_esc(summary)}</span>' if summary else ""
    epoch = data.get("close_epoch")
    if epoch is not None:
        next_chip = (
            f'<span class="chip next" data-kind="next">next '
            f'<span data-close-epoch="{float(epoch):.3f}">{_esc(data["next_chip"])}</span></span>'
        )
    else:
        next_chip = (
            f'<span class="chip next" data-kind="next">{_esc(data["next_chip"])}</span>'
        )
    return (
        f'<span class="chip watch-{_esc(watch_kind)}" data-watch="{_esc(watch_kind)}">'
        f"{_esc(data['watch_label'])}</span>"
        f'<span class="chip market" data-kind="window">{_esc(data["ticker"])}</span>'
        f"{pending_chip}{missing_chip}{pnl_chip}"
        f"{next_chip}"
        f"{summary_html}"
    )


def session_inner_html(state: dict | None = None, *, model: dict[str, Any] | None = None) -> str:
    """One trading-terminal row: window clock + open paper fill from this tree."""
    data = model if model is not None else glance_model(state)
    pos = _open_position_model()
    epoch = data.get("close_epoch")
    ticker = data.get("ticker") or PRIMARY_SERIES
    clock = data.get("next_chip") or "window close not on file"
    if epoch is not None:
        clock_html = (
            f'<span class="sess-clock" data-close-epoch="{float(epoch):.3f}">'
            f"{_esc(clock)}</span>"
        )
    else:
        clock_html = f'<span class="sess-clock">{_esc(clock)}</span>'
    if pos:
        mark = pos.get("mark")
        mark_txt = f"{float(mark):.3f}" if mark is not None else "not on file"
        stake_txt = f"{float(pos['stake']):.2f}"
        pos_html = (
            f'<span class="sess-pos">open paper {_esc(pos["side"])} '
            f"${_esc(stake_txt)} @ {_esc(mark_txt)} · not an order</span>"
            '<span class="sess-note">copied from this tree\'s open book · '
            "display only, not settle</span>"
        )
    else:
        pos_html = (
            '<span class="sess-pos">no open paper book on this tree</span>'
            '<span class="sess-note">no fill invented</span>'
        )
    return (
        '<span class="sess-k">Window</span>'
        f'<span class="sess-ticker">{_esc(ticker)}</span>'
        f"{clock_html}{pos_html}"
    )


def session_strip_html(state: dict | None = None) -> str:
    return f'<div class="session" id="session-strip">{session_inner_html(state)}</div>'


def glance_strip_html(state: dict | None = None) -> str:
    return f'<div class="glance" id="glance-strip">{glance_chips_html(state)}</div>'


def _now_block(
    label: str,
    primary: str,
    *,
    glance_sub: str = "",
    extra: list[str] | None = None,
) -> str:
    bits = [
        '<div class="now-row"><span class="now-k">' + _esc(label) + "</span> "
        f'<span class="now-v">{_esc(primary)}</span></div>'
    ]
    if glance_sub:
        bits.append(f'<div class="now-sub">{_esc(glance_sub)}</div>')
    if extra:
        bits.append('<div class="now-more cockpit-only">')
        bits.extend(f'<div class="now-sub">{_esc(line)}</div>' for line in extra if line)
        bits.append("</div>")
    return "".join(bits)


def _short_why(text: str, *, limit: int = 88) -> str:
    why = str(text or "").strip()
    if not why:
        return ""
    first = why.split(".")[0].strip()
    if len(first) <= limit:
        return first
    return first[: max(0, limit - 1)] + "…"


def _window_tail(ticker: str) -> str:
    """Short window id for glance. Full ticker stays on Cockpit / Bot-hub."""
    text = str(ticker or "").strip()
    if not text:
        return ""
    parts = text.split("-")
    if len(parts) >= 3:
        return "-".join(parts[-2:])
    return text


def _human_pending_why(row: dict[str, Any] | None) -> str:
    """Founder-facing why. Raw wake text stays on Cockpit / Bot-hub."""
    row = row if isinstance(row, dict) else {}
    kind = str(row.get("kind") or "").strip().lower()
    if kind == "awaiting_kalshi_result":
        return "waiting on Kalshi result"
    raw = str(row.get("reason") or "").strip()
    low = raw.lower()
    if "can_close_early" in low or "wait for the kalshi" in low or "wait for kalshi" in low:
        return "waiting on Kalshi result"
    if "disputed" in low or "under review" in low:
        return "Kalshi disputed / under review"
    if "no kalshi market payload" in low:
        return "no Kalshi market payload on disk"
    cleaned = raw
    for prefix in ("SETTLE_PENDING:", "SETTLE_PENDING —", "SETTLE_PENDING -", "SETTLE_PENDING"):
        if cleaned.upper().startswith(prefix.upper()):
            cleaned = cleaned[len(prefix) :].lstrip(" :—-")
            break
    return _short_why(cleaned) or "waiting on Kalshi result"


def this_lane_now_inner_html(state: dict | None = None) -> str:
    """This-lane doing / thinking / learning. Glance is a teaser; Bot-hub has the rest."""
    from golf_offshoot.learning_lane_15m.learn import _event_label

    watch = _watch_status(state)
    wake = _load_wake()
    running = "on" if watch.get("running") else "off"
    cycles = watch.get("cycles")
    summary = str(watch.get("last_summary") or "").strip()
    failed = watch.get("last_ok") is False
    doing_primary = (
        f"Watch {running} · last cycle failed"
        if failed
        else f"Watch {running} · PaperWatch is the loop"
    )
    last_at = _fmt_when(watch.get("last_at"))
    interval = watch.get("interval_s")
    doing_extra: list[str] = []
    doing_glance = ""
    pos = _open_position_model()
    if failed and watch.get("last_error"):
        doing_glance = f"last cycle failed — {watch.get('last_error')}"
    elif pos:
        mark = pos.get("mark")
        mark_txt = f"{float(mark):.3f}" if mark is not None else "not on file"
        doing_glance = (
            f"open paper {pos['side']} ${float(pos['stake']):.2f} @ {mark_txt} "
            "— observation fill, not an order"
        )
    elif last_at:
        doing_glance = f"last cycle {last_at}"
    if cycles not in (None, ""):
        doing_extra.append(f"cycle {cycles}")
    if summary:
        doing_extra.append(summary)
    if last_at and (not doing_glance or "last cycle" not in doing_glance):
        doing_extra.append(f"last cycle {last_at}")
    if interval not in (None, ""):
        doing_extra.append(f"cadence ~{interval}s · extras are buttons, not the loop")
    if pos and doing_glance and "open paper" not in doing_glance:
        mark = pos.get("mark")
        mark_txt = f"{float(mark):.3f}" if mark is not None else "not on file"
        doing_extra.append(
            f"open paper {pos['side']} ${float(pos['stake']):.2f} @ {mark_txt} "
            "— observation fill, not an order"
        )

    scan = (wake or {}).get("scan") if isinstance((wake or {}).get("scan"), dict) else {}
    pending = [row for row in (scan.get("pending") or []) if isinstance(row, dict)]
    missing = [row for row in (scan.get("paper_join_missing") or []) if isinstance(row, dict)]
    kept = [row for row in (scan.get("published_only") or []) if isinstance(row, dict)]
    thinking_extra: list[str] = []
    if pending:
        row = pending[0]
        why = str(row.get("reason") or "wait for Kalshi result")
        ticker = str(row.get("ticker") or row.get("window_id") or "window")
        thinking_primary = _human_pending_why(row)
        thinking_extra.append(f"SETTLE_PENDING {ticker} — {why}")
        if len(pending) > 1:
            thinking_extra.append(f"+{len(pending) - 1} more pending window(s) on this tree")
    else:
        thinking_primary = "no pending window on this tree"
    thinking_glance = ""
    if missing:
        row = missing[0]
        why = str(row.get("reason") or row.get("state") or "missing paper join, not pending")
        thinking_glance = (
            f"missing paper join {len(missing)} — not pending · Scoreboard"
        )
        thinking_extra.append(
            f"missing paper join {row.get('ticker') or 'window'} — {why}"
        )
        if len(missing) > 1:
            thinking_extra.append(f"+{len(missing) - 1} more missing join(s) — no pnl invented")
    elif not pending:
        thinking_primary = "no pending window · no missing join on this tree"
    if pos:
        thinking_extra.append(
            "open-book mark is the paper fill on this tree — not a live bid/ask, not settle"
        )
    if kept:
        row = kept[0]
        thinking_extra.append(
            f"lineage B kept {row.get('ticker') or 'published'} "
            f"{str(row.get('paper_outcome') or '').strip()} "
            f"{str(row.get('published_paper_pnl') or '').strip()} "
            "— never summed into lineage A"
        )
    board = (wake or {}).get("board") if isinstance((wake or {}).get("board"), dict) else {}
    if board.get("note"):
        thinking_extra.append(str(board.get("note")))

    events = [
        ev
        for ev in ((wake or {}).get("new_events") or (wake or {}).get("events") or [])
        if isinstance(ev, dict)
    ]
    heartbeat = (wake or {}).get("heartbeat") or {}
    learning_extra: list[str] = []
    if events:
        ev = events[0]
        tail = _window_tail(str(ev.get("ticker") or ev.get("window_id") or ""))
        kind = str(ev.get("kind") or "learn")
        learning_primary = f"{kind} {tail}".strip() if tail else kind
        learning_extra.append(f"{_event_label(ev)} — {ev.get('detail') or 'see wake'}")
        when = _fmt_when(ev.get("at"))
        if when:
            learning_extra.append(f"last learn {when}")
        for extra_ev in events[1:3]:
            learning_extra.append(f"{_event_label(extra_ev)} — {extra_ev.get('detail') or 'see wake'}")
    elif heartbeat:
        learning_primary = str(heartbeat.get("note") or "no new settle; watch still running")
    elif not wake:
        learning_primary = "learning wake not recorded yet on this tree"
    else:
        learning_primary = "no new settle; watch still running"
    owed = [
        entry
        for entry in ((wake or {}).get("roles_owed") or [])
        if isinstance(entry, dict) and entry.get("role")
    ]
    learning_glance = ""
    if owed:
        first = owed[0]
        reasons = "; ".join(str(r) for r in (first.get("reasons") or [])[:2] if r)
        line = f"owed {first.get('role')} {first.get('age_text') or ''}".strip()
        learning_glance = f"{line} · Bot-hub"
        if reasons:
            learning_extra.append(f"{line} — {reasons}")
        else:
            learning_extra.append(line)
        if first.get("stale"):
            learning_extra.append(f"{first.get('role')} is STALE — still a request, not a completion")
    last_join = _last_settled_join_line()
    if last_join:
        learning_extra.append(last_join)
    tick = _fmt_when((wake or {}).get("updated_at"))
    if tick and tick not in learning_primary and not any(tick in line for line in learning_extra):
        learning_extra.append(f"wake tick {tick}")
    jump = (
        '<p class="now-jump">how it\'s thinking / learning → '
        '<a href="#bot-hub" data-tab="bot-hub">Bot-hub</a>'
        " · books → "
        '<a href="#scoreboard" data-tab="scoreboard">Scoreboard</a></p>'
    )
    return (
        _now_block("Doing", doing_primary, glance_sub=doing_glance, extra=doing_extra)
        + _now_block(
            "Thinking", thinking_primary, glance_sub=thinking_glance, extra=thinking_extra
        )
        + _now_block("Learning", learning_primary, glance_sub=learning_glance, extra=learning_extra)
        + jump
    )


def this_lane_now_html(state: dict | None = None) -> str:
    return (
        '<div class="lane-now home-only" id="lane-now">'
        f"{this_lane_now_inner_html(state)}"
        "</div>"
    )


def _stamp_field(text: str, label: str) -> str:
    """Copy one markdown-table cell. Empty if the stamp does not have that row."""
    needle = f"| {label}"
    for line in text.splitlines():
        if needle not in line:
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and cells[0].startswith(label):
            return cells[-1].replace("**", "")
    return ""


def golf_status_tile_model(stamp_text: str | None = None) -> dict[str, str]:
    """Golf as a compact status tile. Copied from the Operator stamp. Not a cockpit."""
    if stamp_text is None:
        try:
            stamp_text = _GOLF_STAMP.read_text(encoding="utf-8")
        except OSError:
            stamp_text = ""
    if not stamp_text.strip():
        return {
            "lane": LANE_GOLF,
            "status": "stamp not on this tree",
            "note": "no golf cockpit here",
        }
    idle_cell = _stamp_field(text=stamp_text, label="Operator idle until Founder GO?")
    if idle_cell.startswith("Y"):
        status = "idle ON"
    elif idle_cell.startswith("N"):
        status = "idle OFF"
    else:
        status = "idle not on stamp"
    wc1 = _stamp_field(text=stamp_text, label="Lab WC1")
    if "FAIL / park unproven" in wc1:
        note = "WC1 FAIL / park unproven"
    elif wc1:
        note = f"WC1 {wc1}"
    else:
        note = "WC1 not on stamp"
    plain = stamp_text.replace("**", "")
    if "edge not established" in plain.lower():
        note += " · edge not established"
    return {"lane": LANE_GOLF, "status": status, "note": note}


def other_lane_tiles_inner_html() -> str:
    """Status tiles for every canonical lane except this 15m page. Not cockpits."""
    tiles: list[str] = []
    for lane in CANONICAL_LANES:
        if lane == LANE_15M:
            continue
        if lane != LANE_GOLF:
            continue
        data = golf_status_tile_model()
        tiles.append(
            '<article class="lane-tile" data-lane="golf">'
            '<span class="tile-name">golf</span>'
            f'<span class="tile-status">{_esc(data["status"])}</span>'
            f'<span class="tile-note">{_esc(data["note"])}</span>'
            "</article>"
        )
    return "".join(tiles)


def other_lane_tiles_html() -> str:
    inner = other_lane_tiles_inner_html()
    if not inner:
        return ""
    return f'<div class="lane-tiles home-only" id="lane-tiles">{inner}</div>'


def _role_strip_model(state: dict | None = None) -> dict[str, Any]:
    """Owed / idle / served + last tick from the wake. Not a crew roster."""
    from golf_offshoot.learning_lane_15m.learn import (
        ILLUSTRATOR_ROLE,
        LAB_ROLE,
        ROLE_ORDER,
        load_wake_state,
    )
    from golf_offshoot.localtime import format_eastern

    wake = None
    try:
        wake = load_wake_state()
    except Exception:
        wake = None
    owed_entries = [
        entry
        for entry in ((wake or {}).get("roles_owed") or [])
        if isinstance(entry, dict) and entry.get("role")
    ]
    owed_names = [str(entry.get("role")) for entry in owed_entries]
    owed_set = {name.lower() for name in owed_names}
    known = list(ROLE_ORDER) + [ILLUSTRATOR_ROLE, LAB_ROLE]
    idle = [role for role in known if role.lower() not in owed_set]
    served = [
        entry
        for entry in ((wake or {}).get("served") or [])
        if isinstance(entry, dict) and entry.get("role")
    ]
    last_served = served[0] if served else None
    last_tick = "not recorded"
    if wake and wake.get("updated_at"):
        last_tick = format_eastern(wake.get("updated_at"))
    owed_bits = []
    for entry in owed_entries:
        age = str(entry.get("age_text") or "").strip()
        name = str(entry.get("role"))
        owed_bits.append(f"{name} {age}".strip() if age else name)
    served_line = "none on this wake"
    if last_served is not None:
        when = format_eastern(last_served.get("served_at")) if last_served.get("served_at") else ""
        served_line = f"{last_served.get('role')}" + (f" {when}" if when and when != "n/a" else "")
    return {
        "owed": owed_bits,
        "idle": idle,
        "served": served_line,
        "last_tick": last_tick,
        "open": bool(owed_bits),
    }


def role_strip_inner_html(state: dict | None = None) -> str:
    data = _role_strip_model(state)
    owed_line = ", ".join(data["owed"]) if data["owed"] else "none"
    idle_line = ", ".join(data["idle"]) if data["idle"] else "none"
    if data["owed"]:
        summary = f"owed {owed_line} · last tick {data['last_tick']}"
    else:
        summary = f"idle · last tick {data['last_tick']}"
    detail = (
        f"owed: {owed_line} · idle: {idle_line} · last served: {data['served']} · "
        f"last tick {data['last_tick']}"
    )
    open_attr = " open" if data["open"] else ""
    return (
        f'<details class="role-strip-details"{open_attr}>'
        f"<summary>{_esc(summary)}</summary>"
        f'<p class="role-line">{_esc(detail)}</p>'
        '<p class="role-jumps">'
        '<a href="#lane-now">this lane</a>'
        ' · <a href="#lab" data-tab="lab">Lab</a>'
        ' · <a href="#bot-hub" data-tab="bot-hub">Bot-hub</a>'
        ' · <a href="#home" data-density="cockpit">Cockpit</a>'
        "</p>"
        "</details>"
    )


def role_strip_html(state: dict | None = None) -> str:
    return f'<div class="role-strip home-only" id="role-strip">{role_strip_inner_html(state)}</div>'


def _book_tickers(rec: Any) -> list[str]:
    """Market tickers still on the book after settle (positions may be empty)."""
    keys: list[str] = []
    for pos in rec.book.positions:
        pid = str(pos.player_id or "")
        if pid and pid not in keys:
            keys.append(pid)
    for mv in rec.movements:
        pid = str(mv.player_id or "")
        if pid and pid not in keys:
            keys.append(pid)
    return keys


def _open_book_lines() -> list[str]:
    from golf_offshoot.learning_lane_15m.paper import event_ticker_from_book, iter_books

    lines: list[str] = []
    for rec in iter_books():
        if rec.settled_at is not None:
            continue
        tickers = [pos.player_id for pos in rec.book.positions if pos.player_id]
        label = str(tickers[0] if tickers else event_ticker_from_book(rec))
        lines.append(f"{label}  open / SETTLE_PENDING  (no pnl until this book settles)")
    return lines


def _recent_join_lines(limit: int = _JOIN_LIMIT) -> list[str]:
    from golf_offshoot.learning_lane_15m.paper import iter_books
    from golf_offshoot.learning_lane_15m.paths import settlements_dir_15m
    from golf_offshoot.learning_lane_15m.settle import event_ticker_from_book_id

    books = list(iter_books())
    by_ticker: dict[str, Any] = {}
    for rec in books:
        for key in _book_tickers(rec):
            by_ticker[key] = rec
        by_ticker[event_ticker_from_book_id(str(rec.tournament_id or ""))] = rec
        by_ticker[str(rec.tournament_id or "")] = rec

    rows: list[dict[str, Any]] = []
    root = settlements_dir_15m()
    if root.is_dir():
        for path in reversed(sorted(root.glob("*.json"))):
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            for row in reversed(payload.get("rows") or []):
                if not isinstance(row, dict):
                    continue
                rows.append(row)
                if len(rows) >= limit:
                    break
            if len(rows) >= limit:
                break
    rows.reverse()
    lines: list[str] = []
    for row in rows:
        ticker = str(row.get("ticker") or "")
        status = str(row.get("settle_status") or "")
        result = str(row.get("kalshi_result") or "n/a")
        rec = by_ticker.get(ticker) or by_ticker.get(str(row.get("window_id") or ""))
        if rec is not None and rec.settled_at is not None and rec.settlement_pnl is not None:
            pnl = f"pnl={float(rec.settlement_pnl):+.2f}"
        elif rec is None:
            pnl = "no pnl on disk"
        else:
            pnl = "no pnl on disk"
        lines.append(f"{ticker}  {status}  kalshi_result={result}  {pnl}")
    return lines


def exceptions_inner_html(last_run: RunRecord | None = None, *, state: dict | None = None) -> str:
    from golf_offshoot.learning_lane_15m.learn import format_wake_line, load_wake_state
    from golf_offshoot.learning_lane_15m.paper import format_15m_observation_board

    watch = _watch_status(state)
    opens = _open_book_lines()
    joins = _recent_join_lines()
    wake = None
    try:
        wake = load_wake_state()
    except Exception:
        wake = None
    owed = [str(row.get("role")) for row in (wake or {}).get("roles_owed") or [] if row.get("role")]
    last_cycle = str(watch.get("last_summary") or "")
    if last_run is not None and last_run.command and last_run.command != "watch":
        last_cycle_line = f"last extra button: {format_run_record(last_run).splitlines()[0]}"
    else:
        last_cycle_line = last_cycle or "no watch cycle recorded yet"

    open_html = (
        "<ul class='exceptions'>" + "".join(f"<li>{_esc(line)}</li>" for line in opens) + "</ul>"
        if opens
        else "<p class='help'>No open paper book on this tree.</p>"
    )
    join_html = (
        "<ul class='exceptions'>" + "".join(f"<li>{_esc(line)}</li>" for line in joins) + "</ul>"
        if joins
        else "<p class='help'>No official settle joins on file yet.</p>"
    )
    owed_html = (
        "<p class='owed'>roles owed: " + _esc(", ".join(owed)) + "</p>"
        if owed
        else "<p class='help'>roles owed: none</p>"
    )
    tape = ""
    try:
        tape = format_15m_observation_board()
    except Exception:
        tape = ""
    wake_line = format_wake_line(wake)
    return (
        "<h3>Open book</h3>"
        f"{open_html}"
        "<h3>Last official joins</h3>"
        f"{join_html}"
        "<h3>Wake</h3>"
        f"{owed_html}"
        f"<p class='help'>{_esc(wake_line.splitlines()[0] if wake_line else '')}</p>"
        "<h3>Last cycle</h3>"
        f"<p class='help'>{_esc(last_cycle_line)}</p>"
        "<details class='tape'><summary>Full tape (not the glance)</summary>"
        f"<pre>{_esc(tape)}</pre></details>"
    )


def exceptions_html(last_run: RunRecord | None = None, *, state: dict | None = None) -> str:
    return (
        '<section class="panel" id="journal-exceptions-panel">'
        '<details class="exceptions-fold" id="exceptions-fold">'
        "<summary>Exceptions — open book / last joins</summary>"
        '<p class="help">Open book, recent joins, owed roles. Not the full dump. '
        "Folded on glance so Home stays a terminal, not a wall.</p>"
        f'<div id="journal-exceptions">{exceptions_inner_html(last_run, state=state)}</div>'
        "</details>"
        "</section>"
    )


_LINEAGE_LABEL = {
    "local_paper_book": "A this tree",
    "published_manifest": "B published",
    "kalshi_tape": "tape",
}
_SCOREBOARD_ROWS = 16
_LAB_NOTE_PATH = Path(__file__).resolve().parents[3] / "docs" / _LAB_NOTE


def _scoreboard_status(row: Any) -> str:
    if bool(getattr(row, "missing_join", False)):
        return "missing paper join"
    result = str(getattr(row, "kalshi_result", "") or "").strip().lower()
    if result in ("yes", "no"):
        return f"settled {result}"
    status = str(getattr(row, "settle_status", "") or "").strip()
    if status.upper() == "SETTLE_PENDING" or not result:
        return "SETTLE_PENDING"
    return status or "unknown"


def _scoreboard_pnl(row: Any) -> str:
    if bool(getattr(row, "missing_join", False)):
        return "none invented"
    text = str(getattr(row, "paper_pnl_text", "") or "").strip()
    if text and text.lower() not in {"n/a", "none", "not recorded"}:
        return text
    pnl = getattr(row, "paper_pnl", None)
    if pnl is None:
        return "no pnl on disk"
    try:
        return f"{float(pnl):+.2f}"
    except (TypeError, ValueError):
        return "no pnl on disk"


def _lab_note_excerpt() -> str:
    """First ruling lines only. Never copy fee-accurate figures onto the hub."""
    try:
        text = _LAB_NOTE_PATH.read_text(encoding="utf-8")
    except OSError:
        return ""
    lines: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("|") or line == "---":
            continue
        if "fee-accurate" in line.lower() and "0.07" in line:
            continue
        if line.startswith("**k**") or line.startswith("`k`"):
            continue
        lines.append(line)
        if len(lines) >= 5:
            break
    return " ".join(lines)


def scoreboard_inner_html() -> str:
    rows = window_rows_15m()
    counts, _named = window_summary_15m(rows, limit=8)
    pnl, bankroll = _ledger_a()
    wake = _load_wake()
    scan = (wake or {}).get("scan") if isinstance((wake or {}).get("scan"), dict) else {}
    pending = [row for row in (scan.get("pending") or []) if isinstance(row, dict)]
    missing = [row for row in (scan.get("paper_join_missing") or []) if isinstance(row, dict)]
    kept = [row for row in (scan.get("published_only") or []) if isinstance(row, dict)]
    bits = [
        "<p class='view-lead'>This view is the books. Glance is the teaser. "
        f"Series <code>{PRIMARY_SERIES}</code> only. Lineage A and lineage B "
        "stay two books. Their pnl figures are never added together.</p>"
    ]
    if pnl:
        bits.append(
            f"<p class='counts'>Lineage A (this tree) P/L ${_esc(pnl)} · bankroll ${_esc(bankroll)}</p>"
        )
    else:
        bits.append("<p class='help'>Lineage A P/L not on file — none invented.</p>")
    bits.append(
        "<p class='counts'>SETTLE_PENDING "
        f"{len(pending)} · missing paper join {len(missing)} "
        "(missing join is not pending)</p>"
    )
    if kept:
        row = kept[0]
        bits.append(
            "<p class='help'>Lineage B (published Pages) kept "
            f"{_esc(row.get('ticker') or 'window')} "
            f"{_esc(row.get('paper_outcome') or '')} "
            f"{_esc(row.get('published_paper_pnl') or '')} "
            "— not summed into lineage A.</p>"
        )
    if counts:
        bits.append(f"<p class='counts'>{_esc(counts)}</p>")
    shown = [row for row in rows if not bool(getattr(row, "missing_join", False))][:_SCOREBOARD_ROWS]
    if shown:
        bits.append("<table class='board-table'><thead><tr>")
        bits.append(
            "<th>ticker</th><th>lineage</th><th>status</th><th>paper pnl</th></tr></thead><tbody>"
        )
        for row in shown:
            lineage = _LINEAGE_LABEL.get(str(getattr(row, "lineage", "")), "tape")
            bits.append(
                "<tr>"
                f"<td>{_esc(getattr(row, 'ticker', ''))}</td>"
                f"<td>{_esc(lineage)}</td>"
                f"<td>{_esc(_scoreboard_status(row))}</td>"
                f"<td>{_esc(_scoreboard_pnl(row))}</td>"
                "</tr>"
            )
        bits.append("</tbody></table>")
        rest = max(0, len(rows) - len(shown) - len(missing))
        if rest:
            bits.append(f"<p class='help'>+{rest} more windows stay on the PNG, not this table.</p>")
    if missing:
        first = missing[0].get("ticker") or "window"
        bits.append(
            f"<p class='help'>missing paper join {len(missing)} named on this tree, "
            f"e.g. {_esc(first)} — no pnl invented, not a pending window.</p>"
        )
    joins = _recent_join_lines()
    if joins:
        bits.append("<h3>Last official joins</h3>")
        bits.append(
            "<ul class='exceptions'>" + "".join(f"<li>{_esc(line)}</li>" for line in joins) + "</ul>"
        )
    bits.append(
        "<p class='help'>PnL only where a book exists. A window with no book has no pnl — not 0.</p>"
    )
    return "".join(bits)


def lab_inner_html() -> str:
    wake = _load_wake()
    gate = (wake or {}).get("lab_gate") or {}
    lab_owed = "owed" if gate.get("lab_owed") else "NOT owed"
    lab_line = str(gate.get("why") or "Lab is not owed from this glance.")
    boxes = []
    for box in gate.get("boxes") or []:
        if not isinstance(box, dict):
            continue
        boxes.append(f"<li>{_esc(box.get('box') or '')} · {_esc(box.get('state') or 'unstamped')}</li>")
    box_block = (
        "<h3>Honesty stamp (copied from the desk, not restamped here)</h3>"
        "<ul class='exceptions'>" + "".join(boxes) + "</ul>"
        if boxes
        else "<p class='help'>No honesty checklist copied onto this wake yet.</p>"
    )
    excerpt = _lab_note_excerpt()
    excerpt_html = f"<p class='help'>{_esc(excerpt)}</p>" if excerpt else ""
    return (
        "<p class='view-lead'>This view is Lab. Crew owed lives on Bot-hub. "
        "Nothing here is an ADMIT. No fee-accurate figure is displayed on this dashboard.</p>"
        f"<p class='owed'>Lab is { _esc(lab_owed) } — {_esc(lab_line)}</p>"
        f"<p class='help'>{_esc(_LAB_NOTE)} is RUN-ONLY, not a dashboard figure, not a dated record.</p>"
        f"{excerpt_html}"
        f"{box_block}"
        f"<p class='help'>{_esc(gate.get('note') or 'Lab never self-admits.')}</p>"
        '<p class="help">how it\'s thinking / learning → '
        '<a href="#bot-hub" data-tab="bot-hub">Bot-hub</a></p>'
    )


def bot_inner_html() -> str:
    from golf_offshoot.learning_lane_15m.learn import _event_label

    wake = _load_wake()
    if not wake:
        return (
            "<p class='view-lead'>This view is how the lane is thinking and learning. "
            "PaperWatch is the loop. The learning wake has not been recorded "
            "on this tree yet. No roles are owed and none are claimed.</p>"
        )
    tick = _fmt_when(wake.get("updated_at")) or "not recorded"
    owed = [e for e in (wake.get("roles_owed") or []) if isinstance(e, dict) and e.get("role")]
    served = [e for e in (wake.get("served") or []) if isinstance(e, dict) and e.get("role")]
    events = [e for e in (wake.get("new_events") or wake.get("events") or []) if isinstance(e, dict)]
    scan = wake.get("scan") if isinstance(wake.get("scan"), dict) else {}
    pending = [row for row in (scan.get("pending") or []) if isinstance(row, dict)]
    missing = [row for row in (scan.get("paper_join_missing") or []) if isinstance(row, dict)]
    think_bits: list[str] = []
    think_raw = ""
    if pending:
        row = pending[0]
        ticker = str(row.get("ticker") or row.get("window_id") or "window")
        think_bits.append(
            "<li>"
            f"{_esc(_human_pending_why(row))} · {_esc(ticker)} · SETTLE_PENDING</li>"
        )
        think_raw = str(row.get("reason") or "").strip()
        if len(pending) > 1:
            think_bits.append(f"<li>+{len(pending) - 1} more pending window(s)</li>")
    if missing:
        row = missing[0]
        think_bits.append(
            "<li>missing paper join "
            f"{_esc(row.get('ticker') or 'window')} "
            f"(+{max(0, len(missing) - 1)} more; not pending; no pnl invented)</li>"
        )
    think_html = (
        "<ul class='exceptions'>" + "".join(think_bits) + "</ul>"
        if think_bits
        else "<p class='help'>no pending window · no missing join on this tree</p>"
    )
    if think_raw:
        think_html += f"<p class='help'>wake: {_esc(think_raw)}</p>"
    owed_html = (
        "<ul class='exceptions'>"
        + "".join(
            "<li>"
            + _esc(
                f"{entry.get('role')} · owed {entry.get('age_text') or ''}"
                + (" STALE" if entry.get("stale") else "")
                + (
                    " — " + "; ".join(str(r) for r in (entry.get("reasons") or []) if r)
                    if entry.get("reasons")
                    else ""
                )
            )
            + "</li>"
            for entry in owed
        )
        + "</ul>"
        if owed
        else "<p class='help'>roles owed: none — a request for a turn, not a completion.</p>"
    )
    event_html = (
        "<ul class='exceptions'>"
        + "".join(
            "<li>"
            + _esc(_event_label(ev))
            + " — "
            + _esc(ev.get("detail") or "see wake")
            + (f" · {_esc(_fmt_when(ev.get('at')))}" if _fmt_when(ev.get("at")) else "")
            + "</li>"
            for ev in events[:8]
        )
        + "</ul>"
        if events
        else "<p class='help'>No new wake events this tick.</p>"
    )
    served_html = (
        "<ul class='exceptions'>"
        + "".join(
            "<li>"
            + _esc(
                f"{entry.get('role')} {_fmt_when(entry.get('served_at'))} "
                f"{entry.get('served_kind') or ''}".strip()
            )
            + "</li>"
            for entry in served[:6]
        )
        + "</ul>"
        if served
        else "<p class='help'>last served: none on this wake</p>"
    )
    heartbeat = wake.get("heartbeat") if isinstance(wake.get("heartbeat"), dict) else {}
    heart = str(heartbeat.get("note") or "")
    heart_html = f"<p class='help'>{_esc(heart)}</p>" if heart else ""
    return (
        "<p class='view-lead'>This view is how the lane is thinking and learning. "
        "PaperWatch is the loop. Bot-hub names owed roles from the wake. "
        "It serves none of them and invents no pnl.</p>"
        f"<p class='counts'>last tick { _esc(tick) } · series <code>{PRIMARY_SERIES}</code> · "
        "trading_armed=false</p>"
        f"<h3>How it's thinking</h3>{think_html}"
        f"<h3>How it's learning</h3>{event_html}{heart_html}"
        f"<h3>Owed (a request, not a completion)</h3>{owed_html}"
        f"<h3>Last served</h3>{served_html}"
    )


def _next_cycle_line(watch: dict[str, Any]) -> str:
    raw = watch.get("last_at")
    interval = watch.get("interval_s")
    if not raw or interval in (None, ""):
        return ""
    try:
        text = str(raw)
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        parsed = datetime.fromisoformat(text)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        due = parsed.timestamp() + float(interval)
    except (TypeError, ValueError):
        return ""
    remaining = due - datetime.now(timezone.utc).timestamp()
    if remaining <= 0:
        return "next cycle due"
    return f"next cycle ~{int(remaining)}s"


def ops_watch_inner_html(state: dict | None = None) -> str:
    watch = _watch_status(state)
    running = "on" if watch.get("running") else "off"
    last_at = _fmt_when(watch.get("last_at")) or "not recorded"
    interval = watch.get("interval_s")
    ok = "ok" if watch.get("last_ok", True) else "failed"
    nxt = _next_cycle_line(watch)
    err = str(watch.get("last_error") or "").strip()
    rows = [
        ("watch", running),
        ("cadence", f"~{interval}s" if interval not in (None, "") else "not on file"),
        ("last cycle", ok),
        ("cycle", str(watch.get("cycles") or "n/a")),
        ("last at", last_at),
    ]
    if nxt:
        rows.append(("next", nxt))
    if err and watch.get("last_ok") is False:
        rows.append(("error", err))
    dl = "".join(f"<div><dt>{_esc(k)}</dt><dd>{_esc(v)}</dd></div>" for k, v in rows)
    summary = str(watch.get("last_summary") or "PaperWatch is the loop. Buttons below are extras.")
    return (
        f"<dl class='ops-grid'>{dl}</dl>"
        f"<p class='help'>{_esc(summary)}</p>"
    )


def ops_html(last_run: RunRecord | None = None) -> str:
    buttons = []
    help_rows = []
    for value, label, blurb in ACTION_BUTTONS_15M:
        css = ' class="soft"' if value == "refresh" else ""
        buttons.append(f'<button{css} name="action" value="{value}">{_esc(label)}</button>')
        help_rows.append(f"<li><b>{_esc(label)}</b> — {_esc(blurb)}</li>")
    last_html = (
        f"<pre>{_esc(format_run_record(last_run))}</pre>"
        if last_run is not None
        else "<p class='help'>No extra button cycle in this shell session. The watch is the loop.</p>"
    )
    return (
        f'<div id="tab-ops-watch">{ops_watch_inner_html()}</div>'
        "<p class='view-lead'>This view is Ops. PaperWatch remains the loop. "
        "These buttons are extras. paper autobet is observation only. Trading is not armed. Series "
        f"<code>{PRIMARY_SERIES}</code> only.</p>"
        '<form class="row" method="post" action="/run">'
        f'<input type="hidden" name="{SELECTOR_FIELD}" value="{LANE_15M}"/>'
        f"{''.join(buttons)}"
        "</form>"
        f'<ul class="help">{"".join(help_rows)}</ul>'
        "<h3>Last extra cycle</h3>"
        f"{last_html}"
        '<form class="row lane-form" method="get" action="/">'
        "<fieldset><legend>Other chrome</legend>"
        "<p class='help'>Golf Phase 1 chrome is a different view. Opening it does "
        "<strong>not</strong> stop PaperWatch on this hub.</p>"
        f'<button type="submit" name="{SELECTOR_FIELD}" value="{LANE_GOLF}">Golf Phase 1 chrome</button>'
        f'<button type="submit" name="{SELECTOR_FIELD}" value="{LANE_15M}" class="active">'
        "Stay on 15-min Kalshi</button>"
        "</fieldset></form>"
    )


def tabs_nav_html() -> str:
    bits = []
    for tab_id, label in TABS:
        css = ' class="active"' if tab_id == "home" else ""
        bits.append(
            f'<a href="#{_esc(tab_id)}" data-tab="{_esc(tab_id)}"{css}>{_esc(label)}</a>'
        )
    bits.append(
        '<span class="density-toggle home-only" aria-label="density">'
        '<a href="#glance" data-density="glance" class="active">Glance</a>'
        '<a href="#cockpit" data-density="cockpit">Cockpit</a>'
        "</span>"
    )
    return f'<nav class="thin-tabs" aria-label="15m views">{"".join(bits)}</nav>'


def cockpit_rail_html() -> str:
    """Denser home extras: how it's thinking / learning. Hidden on glance."""
    from golf_offshoot.learning_lane_15m.learn import _event_label

    wake = _load_wake()
    scan = (wake or {}).get("scan") if isinstance((wake or {}).get("scan"), dict) else {}
    pending = [row for row in (scan.get("pending") or []) if isinstance(row, dict)]
    missing = [row for row in (scan.get("paper_join_missing") or []) if isinstance(row, dict)]
    if pending:
        row = pending[0]
        ticker = str(row.get("ticker") or row.get("window_id") or "window")
        think_html = (
            f"<p>{_esc(_human_pending_why(row))}</p>"
            f"<p>{_esc(ticker)} · SETTLE_PENDING</p>"
        )
        raw = str(row.get("reason") or "").strip()
        if raw:
            think_html += f"<p class='help'>{_esc(raw)}</p>"
    else:
        think_html = "<p>no pending window on this tree</p>"
    if missing:
        think_html += (
            f"<p>missing paper join {len(missing)} — not pending · "
            '<a href="#scoreboard" data-tab="scoreboard">Scoreboard</a></p>'
        )
    events = [
        ev
        for ev in ((wake or {}).get("new_events") or (wake or {}).get("events") or [])
        if isinstance(ev, dict)
    ]
    owed = [
        str(entry.get("role"))
        for entry in ((wake or {}).get("roles_owed") or [])
        if isinstance(entry, dict) and entry.get("role")
    ]
    tick = _fmt_when((wake or {}).get("updated_at")) or "not recorded"
    if events:
        ev = events[0]
        learn_html = (
            f"<p>{_esc(_event_label(ev))} — {_esc(ev.get('detail') or 'see wake')}</p>"
        )
        when = _fmt_when(ev.get("at"))
        if when:
            learn_html += f"<p>last learn { _esc(when) }</p>"
    else:
        heartbeat = (wake or {}).get("heartbeat") if isinstance((wake or {}).get("heartbeat"), dict) else {}
        learn_html = (
            f"<p>{_esc(heartbeat.get('note') or 'no new settle; watch still running')}</p>"
        )
    owed_line = ", ".join(owed) if owed else "none"
    learn_html += (
        f"<p>owed {_esc(owed_line)} · last tick {_esc(tick)} · "
        '<a href="#bot-hub" data-tab="bot-hub">Bot-hub</a></p>'
    )
    tape = _recent_join_lines(limit=3)
    if tape:
        tape_html = (
            "<ul class='exceptions'>"
            + "".join(f"<li>{_esc(line)}</li>" for line in tape)
            + "</ul>"
        )
    else:
        tape_html = "<p>No official settle joins on file yet.</p>"
    return (
        '<div class="cockpit-rail cockpit-only" id="cockpit-rail">'
        "<article>"
        '<h3><a href="#bot-hub" data-tab="bot-hub">How it\'s thinking</a></h3>'
        f"{think_html}"
        "</article>"
        "<article>"
        '<h3><a href="#bot-hub" data-tab="bot-hub">How it\'s learning</a></h3>'
        f"{learn_html}"
        "</article>"
        '<article class="tape-card">'
        '<h3><a href="#scoreboard" data-tab="scoreboard">Tape</a></h3>'
        f"{tape_html}"
        "</article>"
        "</div>"
    )


def header_15m_html(*, lane_line: str, wall_lines: str) -> str:
    return (
        '<header class="ops">'
        f'<p class="kicker">{_esc(HEADER_KICKER)}</p>'
        f"<h1>{_esc(HEADER_TITLE)}</h1>"
        '<div class="market-lock">'
        f'<span class="lock-ticker">{_esc(PRIMARY_SERIES)}</span>'
        f'<span class="lock-note">{_esc(MARKET_LOCK_NOTE)}</span>'
        "</div>"
        f'<div class="trust">{_esc(TRUST_LINE)}</div>'
        f'<div class="lane-line">{_esc(lane_line)}</div>'
        f"{wall_lines}"
        "</header>"
    )


def chart_caption_inner_html(rows: list | None = None) -> str:
    counts, windows = window_summary_15m(rows if rows is not None else window_rows_15m())
    bits = []
    if counts:
        bits.append(f'<span class="counts">{_esc(counts)}</span>')
    if windows:
        bits.append(f'<span class="windows cockpit-only">{_esc(windows)}</span>')
    bits.append(
        '<span class="src">Source: learning_lane_15m join files · lineages never summed · '
        "click the board to enlarge</span>"
    )
    return "".join(bits)


def viz_wall_15m_html() -> str:
    """The 15m board as a labelled figure. Missing stays 'not yet available'."""
    path = chart_15m_path()
    if path is None:
        return f'<p class="missing">{_esc(CHART_15M_MISSING)}</p>'
    try:
        cache = int(path.stat().st_mtime)
    except OSError:
        cache = 0
    src = f"/viz15/paper_window_strip.png?t={cache}"
    title = CHART_15M_TITLE
    badges = "".join(
        f'<span class="badge">{_esc(text)}</span>' for text in ("LEARNING LANE", PAPER_ONLY, AI_NO_CASH)
    )
    return (
        '<div class="viz-wall" id="viz-wall">'
        '<section class="viz wide" id="viz-slot-paper-window-strip">'
        f"<h3>{_esc(title)}</h3>"
        f'<div class="badge-row">{badges}</div>'
        f'<p class="plain cockpit-only">{_esc(CHART_15M_PLAIN)}</p>'
        f'<p class="sub cockpit-only">{_esc(CHART_15M_SUB)}</p>'
        "<figure>"
        f'<a class="zoom" href="{src}" data-viz-zoom="1" data-viz-title="{_esc(title)}" '
        f'aria-label="Enlarge {_esc(title)}">'
        f'<img src="{src}" alt="{_esc(title)} — read-only board" width="1700"/>'
        '<span class="zoom-hint">Click to enlarge</span>'
        "</a>"
        f'<figcaption id="chart-15m-caption">{chart_caption_inner_html()}</figcaption>'
        "</figure>"
        "</section>"
        "</div>"
    )


def live_payload(state: dict | None = None, *, last_run: RunRecord | None = None) -> dict[str, Any]:
    """JSON fragments for a soft refresh. Watch heartbeats must not full-page reload."""
    path = chart_15m_path()
    src = ""
    if path is not None:
        try:
            cache = int(path.stat().st_mtime)
        except OSError:
            cache = 0
        src = f"/viz15/paper_window_strip.png?t={cache}"
    rec = last_run
    if rec is None and state and isinstance(state.get("surface"), dict):
        rec = state["surface"].get("last_run")
    model = glance_model(state)
    return {
        "glance_html": glance_chips_html(state, model=model),
        "session_html": session_inner_html(state, model=model),
        "now_html": this_lane_now_inner_html(state),
        "tiles_html": other_lane_tiles_inner_html(),
        "roles_html": role_strip_inner_html(state),
        "exceptions_html": exceptions_inner_html(rec, state=state),
        "caption_html": chart_caption_inner_html(),
        "scoreboard_html": scoreboard_inner_html(),
        "lab_html": lab_inner_html(),
        "bot_html": bot_inner_html(),
        "ops_watch_html": ops_watch_inner_html(state),
        "cockpit_html": cockpit_rail_html(),
        "chart_src": src,
        "watch_kind": model["watch_kind"],
        "ticker": model["ticker"],
        "trading_armed": False,
        "lane": LANE_15M,
        "series": PRIMARY_SERIES,
    }


def main_15m_html(*, last_run: RunRecord | None = None, state: dict | None = None) -> str:
    rec = last_run
    if rec is None and state and isinstance(state.get("surface"), dict):
        rec = state["surface"].get("last_run")
    chart = viz_wall_15m_html()
    return (
        '<div id="tab-home" class="tab-panel active" data-tab-panel="home">'
        f"{cockpit_rail_html()}"
        '<section class="panel chart-panel">'
        "<h2>KXBTC15M board</h2>"
        '<p class="help">KXBTC15M windows from the join files. No golf WC1 / Ill here.</p>'
        f"{chart}"
        "</section>"
        f"{exceptions_html(rec, state=state)}"
        "</div>"
        '<div id="tab-scoreboard" class="tab-panel" data-tab-panel="scoreboard">'
        '<section class="panel"><h2>Scoreboard</h2>'
        f'<div id="tab-scoreboard-body">{scoreboard_inner_html()}</div>'
        "</section></div>"
        '<div id="tab-lab" class="tab-panel" data-tab-panel="lab">'
        '<section class="panel"><h2>Lab</h2>'
        f'<div id="tab-lab-body">{lab_inner_html()}</div>'
        "</section></div>"
        '<div id="tab-ops" class="tab-panel" data-tab-panel="ops">'
        '<section class="panel"><h2>Ops</h2>'
        f"{ops_html(rec)}"
        "</section></div>"
        '<div id="tab-bot-hub" class="tab-panel" data-tab-panel="bot-hub">'
        '<section class="panel"><h2>Bot-hub</h2>'
        f'<div id="tab-bot-body">{bot_inner_html()}</div>'
        "</section></div>"
    )


LANE_15M_CSS = """
 body.lane-15m header.ops .kicker { margin: 0; font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; opacity: 0.8; }
 body.lane-15m header.ops .market-lock { margin-top: 8px; }
 body.lane-15m header.ops .lock-ticker { font-size: 20px; font-weight: 700; letter-spacing: 1px; }
 body.lane-15m header.ops .lock-note { margin-left: 8px; font-size: 12px; opacity: 0.85; }
 body.lane-15m header.ops .trust { margin-top: 6px; font-size: 12px; font-weight: 400; opacity: 0.75; }
 .glance { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; padding: 12px 20px; background: #eef3f6; border-bottom: 1px solid #c9c2b2; }
 .glance .chip { display: inline-block; padding: 4px 10px; border-radius: 4px; font-size: 13px; background: #fff; border: 1px solid #c9c2b2; }
 .glance .chip.watch-on { background: #1f5c3a; color: #fff; border-color: #1f5c3a; }
 .glance .chip.watch-off { background: #55606b; color: #fff; border-color: #55606b; }
 .glance .chip.watch-fail { background: #7a0c0c; color: #fff; border-color: #7a0c0c; }
 .glance .chip.market { background: #0e1f29; color: #f2e27a; font-weight: 700; }
 .glance .chip.pending { background: #9a7a10; color: #fff; border-color: #9a7a10; }
 .glance .chip.missing { background: #d3ccbd; color: #171717; }
 .glance .chip.quiet { color: #4a4a4a; }
 .glance .chip.pnl { font-variant-numeric: tabular-nums; }
 .glance .watch-summary { font-size: 12px; color: #4a4a4a; }
 .session { display: flex; flex-wrap: wrap; gap: 8px 12px; align-items: baseline; padding: 6px 20px 8px; background: #0e1f29; color: #f4f1ea; border-bottom: 1px solid #c9c2b2; font-size: 13px; font-variant-numeric: tabular-nums; }
 .session .sess-k { font-size: 11px; letter-spacing: 0.08em; text-transform: uppercase; opacity: 0.75; }
 .session .sess-ticker { font-weight: 700; letter-spacing: 0.04em; color: #f2e27a; }
 .session .sess-clock { font-weight: 700; font-family: Consolas, "Courier New", monospace; }
 .session .sess-pos { color: #e8f0e8; }
 .session .sess-note { font-size: 12px; opacity: 0.75; }
 .lane-now { padding: 8px 20px 10px; background: #e7edf1; border-bottom: 1px solid #c9c2b2; font-size: 13px; }
 .lane-now .now-row { margin: 2px 0; }
 .lane-now .now-k { display: inline-block; min-width: 5.5rem; font-weight: 700; color: #1f3b4d; }
 .lane-now .now-v { color: #1b1b1b; }
 .lane-now .now-sub { margin: 0 0 2px 5.5rem; font-size: 12px; color: #4a4a4a; }
 .lane-now .now-jump { margin: 6px 0 0; font-size: 12px; }
 .cockpit-only { display: none; }
 body.density-cockpit .now-more.cockpit-only { display: block; }
 body.density-cockpit .cockpit-rail.cockpit-only { display: grid; }
 body.density-cockpit .windows.cockpit-only { display: inline; }
 body.density-cockpit p.plain.cockpit-only,
 body.density-cockpit p.sub.cockpit-only { display: block; }
 body.lane-15m:not([data-view="home"]) .home-only { display: none; }
 .lane-tiles { display: flex; flex-wrap: wrap; gap: 8px; padding: 6px 20px 8px; background: #eef3f6; border-bottom: 1px solid #c9c2b2; }
 .lane-tile { display: flex; flex-direction: column; gap: 2px; padding: 6px 10px; background: #fff; border: 1px solid #c9c2b2; font-size: 12px; min-width: 11rem; max-width: 16rem; }
 .lane-tile .tile-name { font-weight: 700; font-size: 11px; letter-spacing: 0.06em; text-transform: uppercase; }
 .lane-tile .tile-status { font-size: 13px; }
 .lane-tile .tile-note { color: #4a4a4a; }
 .role-strip { padding: 4px 20px 8px; background: #eef3f6; border-bottom: 1px solid #c9c2b2; font-size: 12px; }
 .role-strip summary { cursor: pointer; color: #4a4a4a; }
 .role-strip .role-line { margin: 4px 0 0; color: #1b1b1b; }
 .role-strip .role-jumps { margin: 4px 0 0; font-size: 12px; }
 .role-strip .role-jumps a { color: #1f3b4d; }
 .cockpit-rail { grid-template-columns: 1fr 1fr; gap: 8px; margin: 8px 0 0; }
 .cockpit-rail article { background: #fff; border: 1px solid #c9c2b2; padding: 8px 10px; font-size: 12px; }
 .cockpit-rail .tape-card { grid-column: 1 / -1; }
 .cockpit-rail h3 { margin: 0 0 4px; font-size: 13px; }
 .cockpit-rail p { margin: 2px 0; }
 .cockpit-rail .help { font-size: 12px; color: #4a4a4a; }
 .exceptions-fold summary { cursor: pointer; font-weight: 700; font-size: 16px; }
 .thin-tabs { display: flex; flex-wrap: wrap; gap: 2px; margin: 0; padding: 6px 20px 0; border-bottom: 1px solid #c9c2b2; position: sticky; top: 0; z-index: 4; background: #f4f1ea; }
 .thin-tabs a { padding: 6px 12px; font-size: 13px; color: #4a4a4a; text-decoration: none; }
 .thin-tabs a.active { color: #1b1b1b; font-weight: 700; border-bottom: 2px solid #1f3b4d; }
 .thin-tabs .density-toggle { margin-left: auto; display: flex; gap: 2px; }
 .thin-tabs .density-toggle a { font-size: 12px; }
 .tab-panel { display: none; }
 .tab-panel.active { display: block; }
 .view-lead { margin: 0 0 10px; }
 table.board-table { width: 100%; border-collapse: collapse; font-size: 13px; font-variant-numeric: tabular-nums; margin: 8px 0 12px; }
 table.board-table th, table.board-table td { text-align: left; padding: 4px 8px; border-bottom: 1px solid #d3ccbd; }
 dl.ops-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(10rem, 1fr)); gap: 8px; margin: 0 0 12px; }
 dl.ops-grid div { background: #fff; border: 1px solid #c9c2b2; padding: 8px 10px; }
 dl.ops-grid dt { font-size: 11px; letter-spacing: 0.06em; text-transform: uppercase; color: #4a4a4a; }
 dl.ops-grid dd { margin: 2px 0 0; font-size: 14px; }
 ul.exceptions { margin: 6px 0 10px; padding-left: 18px; font-size: 13px; font-family: Consolas, "Courier New", monospace; }
 details.tape { margin-top: 12px; font-size: 13px; }
 p.owed { font-weight: 700; }
"""


LANE_15M_JS = """
(function(){
  var nav = document.querySelector('.thin-tabs');
  if (!nav) return;
  var allowed = {home:1, scoreboard:1, lab:1, ops:1, 'bot-hub':1};
  function paintClocks(){
    var now = Date.now() / 1000;
    document.querySelectorAll('[data-close-epoch]').forEach(function(el){
      var epoch = parseFloat(el.getAttribute('data-close-epoch') || '');
      if (!isFinite(epoch)) return;
      var rem = epoch - now;
      if (rem <= 0) {
        el.textContent = 'window close passed — wait for Kalshi result';
        return;
      }
      var m = Math.floor(rem / 60);
      var s = Math.floor(rem % 60);
      el.textContent = m + ':' + (s < 10 ? '0' : '') + s;
    });
  }
  function foldExceptions(open){
    var fold = document.getElementById('exceptions-fold');
    if (fold) fold.open = !!open;
  }
  function show(id){
    if (!allowed[id]) id = 'home';
    document.querySelectorAll('.tab-panel').forEach(function(p){
      p.classList.toggle('active', p.getAttribute('data-tab-panel') === id);
    });
    nav.querySelectorAll('[data-tab]').forEach(function(a){
      a.classList.toggle('active', a.getAttribute('data-tab') === id);
    });
    try { localStorage.setItem('gpf-15m-tab', id); } catch (e) {}
    document.body.setAttribute('data-view', id);
  }
  function setDensity(mode){
    var cockpit = mode === 'cockpit';
    document.body.classList.toggle('density-cockpit', cockpit);
    document.body.classList.toggle('density-glance', !cockpit);
    try { localStorage.setItem('gpf-15m-density', cockpit ? 'cockpit' : 'glance'); } catch (e) {}
    document.querySelectorAll('[data-density]').forEach(function(a){
      a.classList.toggle('active', a.getAttribute('data-density') === (cockpit ? 'cockpit' : 'glance'));
    });
    foldExceptions(cockpit);
  }
  document.addEventListener('click', function(ev){
    var dens = ev.target.closest ? ev.target.closest('[data-density]') : null;
    if (dens) {
      ev.preventDefault();
      setDensity(dens.getAttribute('data-density') || 'glance');
      return;
    }
    var a = ev.target.closest ? ev.target.closest('[data-tab]') : null;
    if (!a) return;
    ev.preventDefault();
    var id = a.getAttribute('data-tab') || 'home';
    show(id);
    if (history.replaceState) history.replaceState(null, '', '#' + id);
  });
  document.addEventListener('keydown', function(ev){
    if (ev.altKey || ev.metaKey || ev.ctrlKey) return;
    var t = ev.target;
    if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable)) return;
    var keys = {'1':'home','2':'scoreboard','3':'lab','4':'ops','5':'bot-hub'};
    if (!keys[ev.key]) return;
    ev.preventDefault();
    show(keys[ev.key]);
    if (history.replaceState) history.replaceState(null, '', '#' + keys[ev.key]);
  });
  var hash = (location.hash || '').replace('#','');
  if (hash === 'cockpit') { setDensity('cockpit'); show('home'); }
  else if (hash === 'glance') { setDensity('glance'); show('home'); }
  else if (allowed[hash]) { show(hash); }
  else {
    var savedTab = '';
    try { savedTab = localStorage.getItem('gpf-15m-tab') || ''; } catch (e) {}
    show(allowed[savedTab] ? savedTab : 'home');
  }
  try {
    var saved = localStorage.getItem('gpf-15m-density');
    if (hash !== 'cockpit' && hash !== 'glance' && saved) setDensity(saved);
    else if (hash !== 'cockpit' && hash !== 'glance') setDensity('glance');
  } catch (e) {}
  setInterval(paintClocks, 1000);
  paintClocks();
})();
"""
