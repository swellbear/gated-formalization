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


def _next_window_chip(ticker: str, window_id: str = "", close_time: str = "") -> str:
    epoch = _close_epoch(ticker=ticker, window_id=window_id, close_time=close_time)
    if epoch is None:
        return "window close not on file"
    remaining = epoch - datetime.now(timezone.utc).timestamp()
    if remaining <= 0:
        return "window close passed — wait for Kalshi result"
    mins = int(remaining // 60)
    return f"next window ~{mins}m"


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
    next_chip = (
        _next_window_chip(
            current.get("ticker") or "",
            window_id=current.get("window_id") or "",
            close_time=current.get("close_time") or "",
        )
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
    return (
        f'<span class="chip watch-{_esc(watch_kind)}" data-watch="{_esc(watch_kind)}">'
        f"{_esc(data['watch_label'])}</span>"
        f'<span class="chip market" data-kind="window">{_esc(data["ticker"])}</span>'
        f"{pending_chip}{missing_chip}{pnl_chip}"
        f'<span class="chip next" data-kind="next">{_esc(data["next_chip"])}</span>'
        f"{summary_html}"
    )


def glance_strip_html(state: dict | None = None) -> str:
    return f'<div class="glance" id="glance-strip">{glance_chips_html(state)}</div>'


def this_lane_now_inner_html(state: dict | None = None) -> str:
    """This-lane doing / thinking / learning. Copied from the watch + wake. No golf tiles."""
    from golf_offshoot.learning_lane_15m.learn import _event_label, load_wake_state

    watch = _watch_status(state)
    running = "on" if watch.get("running") else "off"
    cycles = watch.get("cycles")
    summary = str(watch.get("last_summary") or "").strip()
    doing = f"Watch {running}"
    if cycles not in (None, ""):
        doing += f" · cycle {cycles}"
    doing += " · PaperWatch is the loop"
    if summary:
        doing += f" · {summary}"

    wake = None
    try:
        wake = load_wake_state()
    except Exception:
        wake = None
    scan = (wake or {}).get("scan") if isinstance((wake or {}).get("scan"), dict) else {}
    pending = [row for row in (scan.get("pending") or []) if isinstance(row, dict)]
    missing = [row for row in (scan.get("paper_join_missing") or []) if isinstance(row, dict)]
    if pending:
        row = pending[0]
        why = str(row.get("reason") or "wait for Kalshi result")
        thinking = (
            f"SETTLE_PENDING {row.get('ticker') or row.get('window_id') or 'window'} — {why}"
        )
    elif missing:
        row = missing[0]
        why = str(row.get("reason") or row.get("state") or "missing paper join, not pending")
        thinking = f"missing paper join {row.get('ticker') or 'window'} — {why}"
    else:
        thinking = "no pending window · no missing join on this tree"

    events = (wake or {}).get("new_events") or (wake or {}).get("events") or []
    heartbeat = (wake or {}).get("heartbeat") or {}
    if events and isinstance(events[0], dict):
        ev = events[0]
        learning = f"{_event_label(ev)} — {ev.get('detail') or 'see wake'}"
    elif heartbeat:
        learning = str(heartbeat.get("note") or "no new settle; watch still running")
    elif not wake:
        learning = "learning wake not recorded yet on this tree"
    else:
        learning = "no new settle; watch still running"
    return (
        '<div class="now-row"><span class="now-k">Doing</span> '
        f'<span class="now-v">{_esc(doing)}</span></div>'
        '<div class="now-row"><span class="now-k">Thinking</span> '
        f'<span class="now-v">{_esc(thinking)}</span></div>'
        '<div class="now-row"><span class="now-k">Learning</span> '
        f'<span class="now-v">{_esc(learning)}</span></div>'
    )


def this_lane_now_html(state: dict | None = None) -> str:
    return (
        '<div class="lane-now" id="lane-now">'
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
    return f'<div class="lane-tiles" id="lane-tiles">{inner}</div>'


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
        tickers = [pos.player_id for pos in rec.book.positions if pos.player_id]
        if tickers:
            by_ticker[str(tickers[0])] = rec
        by_ticker[event_ticker_from_book_id(str(rec.tournament_id or ""))] = rec

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
        rec = by_ticker.get(ticker)
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
        "<h2>Exceptions</h2>"
        '<p class="help">Open book, recent joins, owed roles. Not the full dump.</p>'
        f'<div id="journal-exceptions">{exceptions_inner_html(last_run, state=state)}</div>'
        "</section>"
    )


def scoreboard_inner_html() -> str:
    counts, windows = window_summary_15m(window_rows_15m(), limit=24)
    bits = []
    if counts:
        bits.append(f"<p class='counts'>{_esc(counts)}</p>")
    if windows:
        bits.append(f"<p class='windows'>{_esc(windows)}</p>")
    bits.append(
        "<p class='help'>Lineage A and lineage B stay two books. Their pnl figures are never added "
        "together. Missing paper join is not SETTLE_PENDING. PnL only where a book exists.</p>"
    )
    return "".join(bits) or "<p class='help'>No window rows on file yet.</p>"


def lab_inner_html() -> str:
    from golf_offshoot.learning_lane_15m.learn import load_wake_state

    wake = None
    try:
        wake = load_wake_state()
    except Exception:
        wake = None
    owed = (wake or {}).get("roles_owed") or []
    gate = (wake or {}).get("lab_gate") or {}
    rows = []
    for entry in owed:
        role = str(entry.get("role") or "")
        age = str(entry.get("age_text") or "")
        reasons = "; ".join(str(r) for r in (entry.get("reasons") or []) if r)
        rows.append(f"<li>{_esc(role)} · owed {_esc(age)}" + (f" — {_esc(reasons)}" if reasons else "") + "</li>")
    owed_block = (
        "<ul class='exceptions'>" + "".join(rows) + "</ul>" if rows else "<p class='help'>No roles owed.</p>"
    )
    lab_line = str(gate.get("why") or "Lab is not owed from this glance.")
    return (
        "<p class='help'>Lab output stays in Operator notes. Nothing here is an ADMIT. "
        f"{_esc(_LAB_NOTE)} is RUN-ONLY, not a dashboard figure.</p>"
        f"<h3>Roles owed</h3>{owed_block}"
        f"<p class='help'>{_esc(lab_line)}</p>"
    )


def bot_inner_html() -> str:
    from golf_offshoot.learning_lane_15m.learn import format_wake_line, load_wake_state

    wake = None
    try:
        wake = load_wake_state()
    except Exception:
        wake = None
    return (
        "<p class='help'>PaperWatch is the loop. This tab is the wake — names owed roles, "
        "serves none of them, invents no pnl.</p>"
        f"<pre>{_esc(format_wake_line(wake))}</pre>"
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
        '<p class="help">PaperWatch remains the loop. These buttons are extras. '
        "paper autobet is observation only. Trading is not armed. Series "
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
    return f'<nav class="thin-tabs" aria-label="15m views">{"".join(bits)}</nav>'


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
        bits.append(f'<span class="windows">{_esc(windows)}</span>')
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
        f'<p class="plain">{_esc(CHART_15M_PLAIN)}</p>'
        f'<p class="sub">{_esc(CHART_15M_SUB)}</p>'
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
        "now_html": this_lane_now_inner_html(state),
        "tiles_html": other_lane_tiles_inner_html(),
        "exceptions_html": exceptions_inner_html(rec, state=state),
        "caption_html": chart_caption_inner_html(),
        "scoreboard_html": scoreboard_inner_html(),
        "lab_html": lab_inner_html(),
        "bot_html": bot_inner_html(),
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
        '<section class="panel chart-panel">'
        "<h2>KXBTC15M board</h2>"
        '<p class="help">KXBTC15M windows from the join files. No golf WC1 / Ill here.</p>'
        f"{chart}"
        "</section>"
        f"{tabs_nav_html()}"
        '<div id="tab-home" class="tab-panel active" data-tab-panel="home">'
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
 .lane-now { padding: 8px 20px 10px; background: #e7edf1; border-bottom: 1px solid #c9c2b2; font-size: 13px; }
 .lane-now .now-row { margin: 2px 0; }
 .lane-now .now-k { display: inline-block; min-width: 5.5rem; font-weight: 700; color: #1f3b4d; }
 .lane-now .now-v { color: #1b1b1b; }
 .lane-tiles { display: flex; flex-wrap: wrap; gap: 8px; padding: 6px 20px 8px; background: #eef3f6; border-bottom: 1px solid #c9c2b2; }
 .lane-tile { display: flex; flex-direction: column; gap: 2px; padding: 6px 10px; background: #fff; border: 1px solid #c9c2b2; font-size: 12px; min-width: 11rem; max-width: 16rem; }
 .lane-tile .tile-name { font-weight: 700; font-size: 11px; letter-spacing: 0.06em; text-transform: uppercase; }
 .lane-tile .tile-status { font-size: 13px; }
 .lane-tile .tile-note { color: #4a4a4a; }
 .thin-tabs { display: flex; flex-wrap: wrap; gap: 2px; margin: 8px 0 0; border-bottom: 1px solid #c9c2b2; }
 .thin-tabs a { padding: 6px 12px; font-size: 13px; color: #4a4a4a; text-decoration: none; }
 .thin-tabs a.active { color: #1b1b1b; font-weight: 700; border-bottom: 2px solid #1f3b4d; }
 .tab-panel { display: none; }
 .tab-panel.active { display: block; }
 ul.exceptions { margin: 6px 0 10px; padding-left: 18px; font-size: 13px; font-family: Consolas, "Courier New", monospace; }
 details.tape { margin-top: 12px; font-size: 13px; }
 p.owed { font-weight: 700; }
"""


LANE_15M_JS = """
(function(){
  var nav = document.querySelector('.thin-tabs');
  if (!nav) return;
  var allowed = {home:1, scoreboard:1, lab:1, ops:1, 'bot-hub':1};
  function show(id){
    if (!allowed[id]) id = 'home';
    document.querySelectorAll('.tab-panel').forEach(function(p){
      p.classList.toggle('active', p.getAttribute('data-tab-panel') === id);
    });
    nav.querySelectorAll('[data-tab]').forEach(function(a){
      a.classList.toggle('active', a.getAttribute('data-tab') === id);
    });
  }
  nav.addEventListener('click', function(ev){
    var a = ev.target.closest('[data-tab]');
    if (!a) return;
    ev.preventDefault();
    var id = a.getAttribute('data-tab') || 'home';
    show(id);
    if (history.replaceState) history.replaceState(null, '', '#' + id);
  });
  show((location.hash || '#home').replace('#',''));
})();
"""
