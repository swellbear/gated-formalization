"""15m paper board rendered as readable text from the files on disk.

Every cell on this board is a value that already exists in a file. Nothing here derives a
win, a loss, or a bankroll figure:

* the official Kalshi status/result comes from ``settlements/*.json`` or ``latest/journal.json``
* a paper join, its mark and its paper pnl come from that window's own ``paper/*.json``
* the published Pages lineage comes from ``docs/observability-hub/data/manifest.json``

Two paper lineages exist over this series and they are drawn as separate blocks with separate
book lines. They are never summed into one bankroll. A window with no Kalshi result on disk
stays SETTLE_PENDING, and a window with no paper pnl on disk says so instead of showing 0.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from golf_offshoot.learning_lane_15m.paths import (
    latest_dir_15m,
    paper_dir_15m,
    settlements_dir_15m,
)
from golf_offshoot.operator_surface.observability import repo_root

SLOT_ID = "paper_window_strip"
REL_PNG = Path("docs") / "observability-hub" / "data" / "charts" / "learning_lane_15m" / "paper_window_strip.png"
REL_MANIFEST = Path("docs") / "observability-hub" / "data" / "manifest.json"

LANE = "learning_lane_15m"
SERIES = "KXBTC15M"

TITLE = f"{SERIES} · 15-minute learning lane — paper window board"
SUBTITLE = "PHASE 1 paper observation. Read off the join files. Not edge, not a track record, not cash."
BADGES = ("LEARNING LANE", "PHASE 1 OBSERVATION", "PAPER OBSERVATION ONLY", "AI: NO CASH IN/OUT", "TRADING NOT ARMED")

# Lineage keys. Order here is the order the blocks are drawn.
LINEAGE_LOCAL = "local_paper_book"
LINEAGE_PUBLISHED = "published_manifest"
LINEAGE_TAPE = "kalshi_tape"

LOCAL_TITLE = "PAPER LINEAGE A — local paper book on disk"
PUBLISHED_TITLE = "PAPER LINEAGE B — published Pages manifest"
TAPE_TITLE = "KALSHI TAPE — journal windows with no paper position"

SEPARATE_BOOKS_NOTE = (
    "Lineage A and lineage B are two different paper books over the same series. Their pnl and "
    "bankroll figures are shown apart and are never added together."
)

# paper_dir_15m() also holds the ledger and the notify watch file. Neither is a window book.
_NON_BOOK_FILES = frozenset({"ledger.json", "watch_learning_lane_15m.json", "watch.json"})

# Paper joins are the subject of this board so they are never dropped. The Kalshi-only tape keeps
# growing, so it is trimmed to the newest windows and the block header says it was trimmed.
MAX_TAPE_ROWS = 16

NO_PNL = "no pnl on disk"
NO_PAPER = "n/a"
PENDING_WORD = "SETTLE_PENDING"

BG = "#f5f2ec"
BAND = "#e8e2d5"
INK = "#171717"
MUTED = "#585c63"
FAINT = "#8a8d93"
RULE = "#b9b1a0"
CHIP = "#d3ccbd"
YES = "#1f6b46"
NO = "#8d2b2b"
PENDING = "#9a7a10"
PENDING_FILL = "#f0dfa4"
POS = "#1f6b46"
NEG = "#8d2b2b"

SANS = "DejaVu Sans"
MONO = "DejaVu Sans Mono"

# Geometry in inches. One row height across every block so the whole thing reads as one board.
FIG_W = 20.2
DPI = 100
ROW_IN = 0.40
HEADER_IN = 2.78
FOOTER_IN = 2.52
BLOCK_HEAD_IN = 1.10
BLOCK_GAP_IN = 0.34
MARGIN_IN = 0.30

#: (column key, x in inches, header label). Text is left-aligned on x.
COLUMNS: tuple[tuple[str, float, str], ...] = (
    ("ticker", 0.30, "TICKER (full)"),
    ("window", 2.62, "WINDOW (ET)"),
    ("join", 3.92, "PAPER JOIN"),
    ("kalshi_status", 5.35, "KALSHI STATUS"),
    ("kalshi_result", 6.70, "KALSHI RESULT"),
    ("expiry", 8.05, "EXPIRY VALUE"),
    ("mark", 9.20, "PAPER MARK"),
    ("paper_settle", 10.30, "PAPER SETTLE"),
    ("paper_pnl", 12.20, "PAPER PNL"),
    ("source", 16.45, "SOURCE FILE(S)"),
)
PNL_AX_X = 13.85
PNL_AX_W = 2.30


@dataclass(frozen=True)
class WindowRow:
    """One 15m window exactly as the files describe it."""

    ticker: str
    window_id: str
    settle_status: str
    kalshi_result: str
    settle_src: str
    paper_join: bool
    paper_side: str
    paper_mark: float | None
    open_at: datetime | None
    close_at: datetime | None
    lineage: str = LINEAGE_TAPE
    kalshi_status: str = ""
    expiry_value: str = ""
    paper_settle: str = ""
    paper_pnl: float | None = None
    paper_pnl_text: str = ""


@dataclass(frozen=True)
class Lineage:
    """A block of rows that share one paper book (or the no-paper-book tape)."""

    key: str
    title: str
    book_lines: tuple[str, ...]
    rows: list[WindowRow]
    total: int


@dataclass(frozen=True)
class _PaperJoin:
    window_id: str
    side: str
    mark: float | None
    winner: str
    settled_at: str
    pnl: float | None
    open_position: bool
    source: str


@dataclass(frozen=True)
class _SettleFacts:
    settle_status: str
    kalshi_result: str
    window_id: str
    kalshi_status: str
    expiry_value: str
    source_name: str


@dataclass(frozen=True)
class _PublishedLineage:
    rows: dict[str, dict[str, str]] = field(default_factory=dict)
    book_lines: tuple[str, ...] = ()


def chart_png_path() -> Path:
    return repo_root() / REL_PNG


def manifest_path() -> Path:
    return repo_root() / REL_MANIFEST


def _read_json(path: Path) -> dict[str, Any] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return payload if isinstance(payload, dict) else None


def _parse_stamp(raw: str) -> datetime | None:
    """Window ids keep ':' in JSON; artifact filenames use '-'. Accept both."""
    text = str(raw or "").strip()
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H-%M-%SZ"):
        try:
            return datetime.strptime(text, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def _window_bounds(window_id: str) -> tuple[datetime | None, datetime | None]:
    parts = str(window_id or "").split("__")
    if len(parts) < 3:
        return (None, None)
    return (_parse_stamp(parts[1]), _parse_stamp(parts[2]))


def _tagged_number(text: Any, key: str) -> float | None:
    """Pull a recorded ``key=<number>`` out of a note. Absent or unparsable → None."""
    prefix = f"{key}="
    for token in str(text or "").split():
        if token.startswith(prefix):
            try:
                return float(token[len(prefix) :].rstrip("."))
            except ValueError:
                return None
    return None


def _parse_signed(raw: Any) -> float | None:
    """``"+1.67"`` → 1.67. Anything that is not a plain signed number → None."""
    text = str(raw or "").strip().replace("$", "").replace(",", "")
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _side(player_name: Any) -> str:
    """Paper books name a position ``YES <ticker>``. Anything else is not a side."""
    head = str(player_name or "").strip().split(" ", 1)[0].upper()
    return head if head in ("YES", "NO") else ""


def _settlement_index() -> dict[str, _SettleFacts]:
    """ticker -> settle fields exactly as the settlement join wrote them."""
    index: dict[str, _SettleFacts] = {}
    root = settlements_dir_15m()
    if not root.is_dir():
        return index
    for path in sorted(root.glob("*.json")):
        payload = _read_json(path)
        if payload is None:
            continue
        for row in payload.get("rows") or []:
            if not isinstance(row, dict) or not row.get("ticker"):
                continue
            expiry = row.get("expiration_value")
            index[str(row["ticker"])] = _SettleFacts(
                settle_status=str(row.get("settle_status") or row.get("status") or ""),
                kalshi_result=str(row.get("kalshi_result") or ""),
                window_id=str(row.get("window_id") or payload.get("window_id") or ""),
                kalshi_status=str(row.get("status") or ""),
                expiry_value="" if expiry in (None, "") else str(expiry),
                source_name=str(row.get("source_name") or ""),
            )
    return index


def _journal() -> dict[str, Any]:
    return _read_json(latest_dir_15m() / "journal.json") or {}


def _journal_index(payload: dict[str, Any]) -> dict[str, dict[str, str]]:
    index: dict[str, dict[str, str]] = {}
    for window in payload.get("windows") or []:
        if not isinstance(window, dict) or not window.get("ticker"):
            continue
        index[str(window["ticker"])] = {
            "window_id": str(window.get("window_id") or ""),
            "status": str(window.get("status") or ""),
            "result": str(window.get("result") or ""),
        }
    return index


def _paper_joins() -> dict[str, _PaperJoin]:
    """ticker -> the paper position that joined that window, from that window's own book.

    A settled window keeps its ``movements`` but clears ``book.positions``, so the durable
    join record is the applied movement, not the live position. ``settlement_pnl`` is copied
    straight off the file; a book with no settle recorded keeps ``pnl=None``.
    """
    joins: dict[str, _PaperJoin] = {}
    root = paper_dir_15m()
    if not root.is_dir():
        return joins
    for path in sorted(root.glob("*.json")):
        if path.name in _NON_BOOK_FILES:
            continue
        payload = _read_json(path)
        book = payload.get("book") if payload else None
        if payload is None or not isinstance(book, dict):
            continue
        window_id = str(payload.get("tournament_id") or "")
        winner = str(payload.get("settlement_winner") or "")
        settled_at = str(payload.get("settled_at") or "")
        raw_pnl = payload.get("settlement_pnl")
        pnl = float(raw_pnl) if isinstance(raw_pnl, (int, float)) else None
        marks: dict[str, float | None] = {}
        sides: dict[str, str] = {}
        open_now: set[str] = set()
        for movement in payload.get("movements") or []:
            if not isinstance(movement, dict) or movement.get("kind") != "new_bet":
                continue
            ticker = str(movement.get("player_id") or "")
            if not ticker:
                continue
            marks[ticker] = _tagged_number(movement.get("reason_technical"), "paper_mark")
            sides[ticker] = _side(movement.get("player_name"))
        for position in book.get("positions") or []:
            if not isinstance(position, dict) or not position.get("player_id"):
                continue
            ticker = str(position["player_id"])
            mark = position.get("fill_price")
            if isinstance(mark, (int, float)):
                marks[ticker] = float(mark)
            marks.setdefault(ticker, None)
            sides[ticker] = _side(position.get("player_name")) or sides.get(ticker, "")
            open_now.add(ticker)
        for ticker, mark in marks.items():
            joins[ticker] = _PaperJoin(
                window_id=window_id,
                side=sides.get(ticker, ""),
                mark=mark,
                winner=winner,
                settled_at=settled_at,
                pnl=pnl,
                open_position=ticker in open_now,
                source=f"paper/{path.name}",
            )
    return joins


def _ledger_book_lines() -> tuple[str, ...]:
    """Lineage A book facts, copied out of paper/ledger.json. No figure is recomputed."""
    payload = _read_json(paper_dir_15m() / "ledger.json")
    if payload is None:
        return ("paper/ledger.json not on disk — no book line for this lineage",)
    bits: list[str] = []
    start = payload.get("starting_bankroll")
    now = payload.get("bankroll")
    pnl = payload.get("betting_pnl")
    if isinstance(start, (int, float)) and isinstance(now, (int, float)):
        bits.append(f"paper observation bankroll {start:.2f} → {now:.2f}")
    if isinstance(pnl, (int, float)):
        bits.append(f"betting_pnl {pnl:+.2f}")
    entries = payload.get("entries")
    if isinstance(entries, list):
        bits.append(f"{len(entries)} ledger entries")
    deposits = payload.get("deposits")
    withdrawals = payload.get("withdrawals")
    if isinstance(deposits, (int, float)) and isinstance(withdrawals, (int, float)):
        bits.append(f"deposits {deposits:.2f} · withdrawals {withdrawals:.2f}")
    head = "book: " + " · ".join(bits) if bits else "book: paper/ledger.json carries no bankroll fields"
    return (head, "source: golf-offshoot/data/learning_lane_15m/paper/*.json + paper/ledger.json")


def _published_lineage() -> _PublishedLineage:
    """The 15m paper rows the Pages manifest already publishes.

    This is a second, older paper book over the same series. It is read so a published
    paper_win is not silently dropped off the board; its figures stay in its own block.
    """
    payload = _read_json(manifest_path())
    if payload is None:
        return _PublishedLineage()
    lane = next(
        (
            candidate
            for candidate in payload.get("lanes") or []
            if isinstance(candidate, dict) and str(candidate.get("lane_id") or "") == LANE
        ),
        None,
    )
    if lane is None:
        return _PublishedLineage()
    last_run = lane.get("last_run") if isinstance(lane.get("last_run"), dict) else {}
    fields: dict[str, str] = {}
    for entry in (last_run or {}).get("fields") or []:
        if isinstance(entry, dict) and entry.get("label"):
            fields[str(entry["label"])] = str(entry.get("value") or "")

    rows: dict[str, dict[str, str]] = {}
    settled_ticker = fields.get("Settled paper fill", "").strip()
    if settled_ticker:
        rows[settled_ticker] = {
            "paper_settle": fields.get("Paper outcome", "").strip() or "settled",
            "pnl": fields.get("paper settle_win pnl", "").strip(),
            "kalshi_result": fields.get("Kalshi result", "").strip(),
            "kalshi_status": fields.get("Kalshi status", "").strip(),
            "expiry": fields.get("expiration_value", "").strip(),
        }
    live_ticker = fields.get("Live paper fill", "").strip()
    if live_ticker and live_ticker not in rows:
        rows[live_ticker] = {
            "paper_settle": fields.get("Live paper fill status", "").strip() or PENDING_WORD,
            "pnl": "",
            "kalshi_result": "",
            "kalshi_status": "",
            "expiry": "",
        }

    bits: list[str] = []
    after = fields.get("paper observation after settle", "").strip()
    win_pnl = fields.get("paper settle_win pnl", "").strip()
    if win_pnl:
        bits.append(f"published paper settle_win pnl {win_pnl}")
    if after:
        bits.append(f"paper observation after settle {after}")
    head = "book: " + " · ".join(bits) if bits else "book: manifest publishes no bankroll field for this lineage"
    return _PublishedLineage(
        rows=rows,
        book_lines=(head, f"source: {REL_MANIFEST.as_posix()} (lane {LANE}) — separate book from lineage A"),
    )


def _resolve_settle(
    settle: _SettleFacts | None,
    journal_row: dict[str, str] | None,
    published: dict[str, str] | None,
) -> tuple[str, str, str]:
    """(settle_status, kalshi_result, file the result was read from).

    The first file carrying a concrete Kalshi result wins. When no file carries one the row
    stays SETTLE_PENDING — a result is never inferred from a close time or an average.
    """
    candidates = (
        (settle.kalshi_result if settle else "", settle.settle_status if settle else "", "settlements/*.json"),
        ((journal_row or {}).get("result", ""), "settled", "latest/journal.json"),
        ((published or {}).get("kalshi_result", ""), "settled", REL_MANIFEST.name),
    )
    for raw, status, src in candidates:
        result = str(raw).strip().lower().removeprefix("kalshi:")
        if result in ("yes", "no"):
            return (status or "settled", result, src)
    if settle is not None:
        return (settle.settle_status or PENDING_WORD, "", "settlements/*.json")
    if journal_row is not None:
        return (PENDING_WORD, "", "latest/journal.json")
    return (PENDING_WORD, "", "no settle artifact")


def _paper_settle_cells(
    join: _PaperJoin | None,
    published: dict[str, str] | None,
) -> tuple[str, float | None, str]:
    """(paper settle wording, pnl for the bar, pnl text) using that book's own words."""
    if published is not None:
        wording = published.get("paper_settle", "") or PENDING_WORD
        pnl = _parse_signed(published.get("pnl", ""))
        text = published.get("pnl", "").strip() if pnl is not None else NO_PNL
        return (wording, pnl, text)
    if join is None:
        return (NO_PAPER, None, NO_PAPER)
    if join.pnl is not None:
        wording = "settled" if join.settled_at else "settle recorded"
        return (wording, join.pnl, f"{join.pnl:+.2f}")
    if join.open_position:
        return ("open position", None, NO_PNL)
    return (PENDING_WORD, None, NO_PNL)


def collect_board() -> list[Lineage]:
    """The board as blocks of rows, newest window first, one block per paper lineage."""
    settles = _settlement_index()
    journal = _journal_index(_journal())
    joins = _paper_joins()
    published = _published_lineage()

    tickers = list(joins)
    tickers += [t for t in published.rows if t not in joins]
    tickers += [t for t in journal if t not in joins and t not in published.rows]
    tickers += [t for t in settles if t not in joins and t not in published.rows and t not in journal]

    buckets: dict[str, list[WindowRow]] = {LINEAGE_LOCAL: [], LINEAGE_PUBLISHED: [], LINEAGE_TAPE: []}
    for ticker in tickers:
        join = joins.get(ticker)
        pub = published.rows.get(ticker) if join is None else None
        settle = settles.get(ticker)
        journal_row = journal.get(ticker)
        status, result, src = _resolve_settle(settle, journal_row, pub)
        paper_settle, paper_pnl, paper_pnl_text = _paper_settle_cells(join, pub)

        window_id = next(
            (
                candidate
                for candidate in (
                    join.window_id if join else "",
                    (journal_row or {}).get("window_id", ""),
                    settle.window_id if settle else "",
                )
                if candidate
            ),
            "",
        )
        open_at, close_at = _window_bounds(window_id)

        sources = [src]
        if join is not None:
            sources.append("paper/*.json")
        if pub is not None:
            sources.append(REL_MANIFEST.name)
        expiry = settle.expiry_value if settle else ""
        if not expiry and pub is not None:
            expiry = pub.get("expiry", "")

        kalshi_status = (journal_row or {}).get("status", "") or (settle.kalshi_status if settle else "")
        if not kalshi_status and pub is not None:
            kalshi_status = pub.get("kalshi_status", "")

        if join is not None:
            lineage = LINEAGE_LOCAL
        elif pub is not None:
            lineage = LINEAGE_PUBLISHED
        else:
            lineage = LINEAGE_TAPE

        buckets[lineage].append(
            WindowRow(
                ticker=ticker,
                window_id=window_id,
                settle_status=status,
                kalshi_result=result,
                settle_src=" · ".join(dict.fromkeys(sources)),
                paper_join=lineage != LINEAGE_TAPE,
                # The manifest publishes no side for its rows, so a published join has none.
                paper_side=join.side if join else "",
                paper_mark=join.mark if join else None,
                open_at=open_at,
                close_at=close_at,
                lineage=lineage,
                kalshi_status=kalshi_status,
                expiry_value=expiry,
                paper_settle=paper_settle,
                paper_pnl=paper_pnl,
                paper_pnl_text=paper_pnl_text,
            )
        )

    floor = datetime.min.replace(tzinfo=timezone.utc)
    for rows in buckets.values():
        rows.sort(key=lambda r: (r.open_at or floor, r.ticker), reverse=True)

    tape_total = len(buckets[LINEAGE_TAPE])
    blocks = (
        Lineage(LINEAGE_LOCAL, LOCAL_TITLE, _ledger_book_lines(), buckets[LINEAGE_LOCAL], len(buckets[LINEAGE_LOCAL])),
        Lineage(
            LINEAGE_PUBLISHED,
            PUBLISHED_TITLE,
            published.book_lines,
            buckets[LINEAGE_PUBLISHED],
            len(buckets[LINEAGE_PUBLISHED]),
        ),
        Lineage(
            LINEAGE_TAPE,
            TAPE_TITLE,
            (
                "book: none — these windows have no paper position on any book, so every paper column reads n/a",
                "source: golf-offshoot/data/learning_lane_15m/latest/journal.json + settlements/*.json",
            ),
            buckets[LINEAGE_TAPE][:MAX_TAPE_ROWS],
            tape_total,
        ),
    )
    return [block for block in blocks if block.rows]


def collect_rows() -> tuple[list[WindowRow], list[WindowRow]]:
    """(paper-book joins, Kalshi-only journal rows), newest window first.

    Kept as a 2-tuple because the operator surface builds its caption from it.
    """
    blocks = {block.key: block.rows for block in collect_board()}
    paper_rows = list(blocks.get(LINEAGE_LOCAL, [])) + list(blocks.get(LINEAGE_PUBLISHED, []))
    return (paper_rows, list(blocks.get(LINEAGE_TAPE, [])))


def _result_chip(row: WindowRow) -> tuple[str, str, str]:
    """(label, text colour, fill colour). The word is always drawn, never colour alone."""
    result = row.kalshi_result.strip().lower()
    if result == "yes":
        return ("YES", "#ffffff", YES)
    if result == "no":
        return ("NO", "#ffffff", NO)
    return ("PENDING", PENDING, PENDING_FILL)


def _display_tz() -> tuple[Any, str, str]:
    """Ticker names are ET-stamped, so prefer ET. Fall back to the on-disk UTC."""
    try:
        from zoneinfo import ZoneInfo

        return (ZoneInfo("America/New_York"), "ET", "America/New_York")
    except Exception:
        return (timezone.utc, "UTC", "UTC")


def _window_text(row: WindowRow, tz: Any) -> str:
    if row.open_at and row.close_at:
        return f"{row.open_at.astimezone(tz):%H:%M}-{row.close_at.astimezone(tz):%H:%M}"
    return "no bounds"


def _cells(row: WindowRow, tz: Any) -> dict[str, str]:
    join = "paper join" if row.paper_join else "journal only"
    if row.paper_join and row.paper_side:
        join = f"paper join · {row.paper_side}"
    return {
        "ticker": row.ticker,
        "window": _window_text(row, tz),
        "join": join,
        "kalshi_status": row.kalshi_status or "not recorded",
        "kalshi_result": "",  # drawn as a labelled chip
        "expiry": row.expiry_value or ("n/a" if not row.kalshi_result else "not recorded"),
        "mark": f"{row.paper_mark:.4g}" if row.paper_mark is not None else (NO_PAPER if not row.paper_join else "not recorded"),
        "paper_settle": row.paper_settle or NO_PAPER,
        "paper_pnl": row.paper_pnl_text or NO_PNL,
        "source": row.settle_src,
    }


def render_paper_window_strip() -> Path | None:
    """Regenerate the board PNG from disk. No rows or no matplotlib → no file written."""
    blocks = collect_board()
    if not blocks:
        return None
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.lines import Line2D
        from matplotlib.patches import Patch, Rectangle
    except ImportError:
        return None

    tz, tz_short, tz_long = _display_tz()

    body_in = sum(BLOCK_HEAD_IN + ROW_IN * len(block.rows) for block in blocks)
    body_in += BLOCK_GAP_IN * (len(blocks) - 1)
    fig_h = HEADER_IN + body_in + FOOTER_IN

    fig = plt.figure(figsize=(FIG_W, fig_h), dpi=DPI)
    fig.patch.set_facecolor(BG)

    def fx(x_in: float) -> float:
        return x_in / FIG_W

    def fy(y_in: float) -> float:
        return y_in / fig_h

    pnl_values = [row.paper_pnl for block in blocks for row in block.rows if row.paper_pnl is not None]
    pnl_span = max((abs(v) for v in pnl_values), default=0.0) * 1.35 or 1.0

    # A lineage whose files record no pnl gets no bar axis at all, rather than an empty grid.
    has_bars = [any(row.paper_pnl is not None for row in block.rows) for block in blocks]
    last_bar_block = max((i for i, flag in enumerate(has_bars) if flag), default=-1)

    cursor_in = fig_h - HEADER_IN
    for index, block in enumerate(blocks):
        rows = block.rows
        panel_h = ROW_IN * len(rows)
        bottom_in = cursor_in - BLOCK_HEAD_IN - panel_h
        top_in = bottom_in + panel_h

        count = f"({len(rows)} window{'s' if len(rows) != 1 else ''})"
        if block.total != len(rows):
            count = f"(newest {len(rows)} of {block.total} windows)"
        fig.text(
            fx(MARGIN_IN),
            fy(top_in + 0.80),
            f"{block.title}  {count}",
            fontsize=12.5,
            color=INK,
            fontweight="bold",
            family=SANS,
            va="bottom",
        )
        for line_index, line in enumerate(block.book_lines[:2]):
            fig.text(
                fx(MARGIN_IN),
                fy(top_in + 0.555 - line_index * 0.19),
                line,
                fontsize=8.6,
                color=MUTED,
                family=MONO,
                va="bottom",
            )
        for key, x_in, label in COLUMNS:
            if key == "ticker":
                continue
            fig.text(fx(x_in), fy(top_in + 0.10), label, fontsize=8.4, color=MUTED, fontweight="bold", family=SANS, va="bottom")
        if has_bars[index]:
            fig.text(
                fx(PNL_AX_X),
                fy(top_in + 0.10),
                "PAPER PNL BAR (this lineage only)",
                fontsize=8.4,
                color=MUTED,
                fontweight="bold",
                family=SANS,
                va="bottom",
            )
        fig.add_artist(
            Line2D(
                [fx(MARGIN_IN), fx(FIG_W - MARGIN_IN)],
                [fy(top_in + 0.04), fy(top_in + 0.04)],
                transform=fig.transFigure,
                color=RULE,
                linewidth=1.1,
            )
        )

        for row_index, row in enumerate(rows):
            row_top = top_in - row_index * ROW_IN
            centre = fy(row_top - ROW_IN / 2)
            if row_index % 2 == 0:
                fig.add_artist(
                    Rectangle(
                        (fx(MARGIN_IN - 0.12), fy(row_top - ROW_IN)),
                        fx(FIG_W - 2 * MARGIN_IN + 0.24),
                        fy(ROW_IN),
                        transform=fig.transFigure,
                        facecolor=BAND,
                        edgecolor="none",
                        zorder=0,
                    )
                )
            cells = _cells(row, tz)
            fig.text(fx(COLUMNS[0][1]), centre, row.ticker, fontsize=10, color=INK, fontweight="bold", family=MONO, va="center")
            for key, x_in, _ in COLUMNS[1:]:
                if key == "kalshi_result":
                    label, text_color, fill = _result_chip(row)
                    fig.text(
                        fx(x_in),
                        centre,
                        label,
                        fontsize=9,
                        color=text_color,
                        fontweight="bold",
                        family=SANS,
                        va="center",
                        bbox={"boxstyle": "round,pad=0.28", "facecolor": fill, "edgecolor": INK, "linewidth": 0.7},
                    )
                    continue
                if key == "paper_pnl":
                    is_number = row.paper_pnl is not None
                    fig.text(
                        fx(x_in),
                        centre,
                        cells[key],
                        fontsize=10 if is_number else 8.8,
                        color=(POS if (row.paper_pnl or 0) >= 0 else NEG) if is_number else FAINT,
                        fontweight="bold" if is_number else "normal",
                        family=MONO,
                        va="center",
                    )
                    continue
                fig.text(
                    fx(x_in),
                    centre,
                    cells[key],
                    fontsize=8.6 if key == "source" else 9.2,
                    color=FAINT if cells[key] in (NO_PAPER, NO_PNL, "not recorded") else (MUTED if key == "source" else INK),
                    family=MONO if key in ("window", "expiry", "mark", "source") else SANS,
                    va="center",
                )

        if has_bars[index]:
            ax = fig.add_axes((fx(PNL_AX_X), fy(bottom_in), fx(PNL_AX_W), fy(panel_h)))
            _draw_pnl_axis(ax, rows, span=pnl_span, show_x=index == last_bar_block)
        else:
            fig.text(
                fx(PNL_AX_X),
                fy(bottom_in + panel_h / 2),
                "no pnl bar on this block —\nno paper position on any book",
                fontsize=8.2,
                color=FAINT,
                family=SANS,
                va="center",
                linespacing=1.5,
            )

        cursor_in = bottom_in - BLOCK_GAP_IN

    _draw_header(fig, fx, fy, blocks, tz_short, Patch, Rectangle)
    _draw_footer(fig, fx, fy, tz_long)

    dest = chart_png_path()
    dest.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(dest, format="png", facecolor=BG)
    plt.close(fig)
    return dest


def _draw_pnl_axis(ax: Any, rows: list[WindowRow], *, span: float, show_x: bool) -> None:
    """A zero-centred paper-pnl bar per row. A row with no pnl on file gets no bar."""
    count = len(rows)
    ax.set_facecolor("none")
    ax.set_xlim(-span, span)
    ax.set_ylim(0, count)
    ax.set_yticks([])
    ax.set_axisbelow(True)
    ax.grid(axis="x", color=RULE, linestyle=":", linewidth=0.6)
    for name, spine in ax.spines.items():
        spine.set_visible(name == "bottom" and show_x)
        spine.set_color(RULE)
    ax.axvline(0, color=MUTED, linewidth=1.0)

    for index, row in enumerate(rows):
        y = count - index - 0.5
        if row.paper_pnl is None:
            # No bar at all. The PAPER PNL text column already says why, and a 0-length bar
            # sitting on the zero line would read as a settled break-even.
            continue
        ax.barh(
            y,
            row.paper_pnl,
            height=0.46,
            color=POS if row.paper_pnl >= 0 else NEG,
            edgecolor=INK,
            linewidth=0.7,
            zorder=3,
        )

    if show_x:
        ax.tick_params(axis="x", labelsize=8, colors=MUTED, length=3)
        ax.set_xlabel(
            "paper pnl in $ as recorded on that window's own file · shared scale · never a lineage total",
            fontsize=8.2,
            color=MUTED,
            labelpad=5,
        )
    else:
        ax.tick_params(axis="x", labelbottom=False, length=0)


def _draw_header(
    fig: Any,
    fx: Any,
    fy: Any,
    blocks: list[Lineage],
    tz_short: str,
    patch_cls: Any,
    rect_cls: Any,
) -> None:
    journal = _journal()
    root = settlements_dir_15m()
    settle_files = len(list(root.glob("*.json"))) if root.is_dir() else 0
    joins = sum(len(b.rows) for b in blocks if b.key != LINEAGE_TAPE)
    tape = sum(b.total for b in blocks if b.key == LINEAGE_TAPE)
    drawn = [row for block in blocks for row in block.rows]
    yes = sum(1 for row in drawn if row.kalshi_result == "yes")
    no = sum(1 for row in drawn if row.kalshi_result == "no")
    pending = len(drawn) - yes - no

    def from_top(y_in: float) -> float:
        return 1.0 - fy(y_in)

    fig.text(fx(0.30), from_top(0.44), TITLE, fontsize=21, color=INK, fontweight="bold", family=SANS, va="top")
    fig.text(fx(0.30), from_top(0.86), SUBTITLE, fontsize=10.5, color=MUTED, family=SANS, va="top")

    lane = str(journal.get("lane") or LANE)
    series = str(journal.get("series") or SERIES)
    index_id = str(journal.get("cf_index_id") or "")
    lane_line = f"lane={lane} · series={series}"
    if index_id:
        lane_line += f" · cf_index_id={index_id}"
    stamp = str(journal.get("generated_at") or "")
    lines = (
        lane_line,
        f"{joins} paper-book join(s) · {tape} Kalshi-only journal row(s) · {settle_files} settlement file(s) · "
        f"result=yes {yes} · result=no {no} · {PENDING_WORD} {pending}",
        (f"journal generated_at={stamp}" if stamp else "journal generated_at not recorded")
        + f" · window clock in {tz_short} · rendered {datetime.now().astimezone():%Y-%m-%d %H:%M %Z}",
    )
    for offset, line in enumerate(lines):
        fig.text(fx(0.30), from_top(1.24 + offset * 0.235), line, fontsize=9, color=MUTED, family=MONO, va="top")

    x_in = 0.30
    for badge in BADGES:
        text = fig.text(
            fx(x_in),
            from_top(2.24),
            badge,
            fontsize=8.8,
            color=INK,
            fontweight="bold",
            family=SANS,
            va="center",
            bbox={"boxstyle": "round,pad=0.34", "facecolor": CHIP, "edgecolor": INK, "linewidth": 0.9},
        )
        fig.canvas.draw()
        width = text.get_window_extent(renderer=fig.canvas.get_renderer()).width
        x_in += width / fig.dpi + 0.16

    fig.legend(
        handles=[
            patch_cls(facecolor=YES, edgecolor=INK, label='chip "YES" — file records kalshi_result = yes'),
            patch_cls(facecolor=NO, edgecolor=INK, label='chip "NO" — file records kalshi_result = no'),
            patch_cls(facecolor=PENDING_FILL, edgecolor=INK, label=f'chip "PENDING" — {PENDING_WORD}, no result on disk'),
        ],
        title="KALSHI RESULT column (every chip carries its word)",
        loc="upper left",
        bbox_to_anchor=(fx(12.05), from_top(0.34)),
        frameon=False,
        fontsize=9,
        title_fontsize=9.2,
        alignment="left",
    )
    fig.legend(
        handles=[
            patch_cls(facecolor=POS, edgecolor=INK, label="bar right — pnl recorded on file is positive"),
            patch_cls(facecolor=NEG, edgecolor=INK, label="bar left — pnl recorded on file is negative"),
            patch_cls(facecolor=BG, edgecolor=FAINT, label=f'no bar — "{NO_PNL}" / "{NO_PAPER}", never 0'),
        ],
        title="PAPER PNL column (per window, per lineage)",
        loc="upper left",
        bbox_to_anchor=(fx(16.35), from_top(0.34)),
        frameon=False,
        fontsize=9,
        title_fontsize=9.2,
        alignment="left",
    )

    fig.add_artist(
        rect_cls(
            (fx(0.18), from_top(2.52)),
            fx(FIG_W - 0.36),
            0.0,
            transform=fig.transFigure,
            edgecolor=RULE,
            facecolor="none",
            linewidth=1.2,
        )
    )


def _draw_footer(fig: Any, fx: Any, fy: Any, tz_long: str) -> None:
    fig.text(
        fx(0.30),
        fy(1.86),
        "official settle = Kalshi result matched to CF Benchmarks BRTI. Trading NOT ARMED.",
        fontsize=12,
        color=INK,
        fontweight="bold",
        family=SANS,
        va="top",
    )
    notes = (
        SEPARATE_BOOKS_NOTE,
        "PAPER JOIN = this window has a paper position on that lineage's book. journal only = no paper position "
        "anywhere on disk, so PAPER MARK / PAPER SETTLE / PAPER PNL read n/a rather than 0.",
        "PAPER MARK = the public Kalshi mid/last recorded on the position at join. PAPER SETTLE and PAPER PNL use "
        "that book's own wording and its own recorded number. Nothing is recomputed, averaged or carried across lineages.",
        f"KALSHI STATUS / KALSHI RESULT / EXPIRY VALUE are copied from the settle join. A window with no Kalshi result "
        f"on disk stays {PENDING_WORD}; a result is never inferred from a close time or a DIY benchmark average.",
        f"sources on disk: golf-offshoot/data/learning_lane_15m/{{settlements/*.json, latest/journal.json, paper/*.json, "
        f"paper/ledger.json}} + {REL_MANIFEST.as_posix()} · window clock {tz_long}.",
        f"{LANE} / {SERIES} only. No golf WC1, Ill or calibration board on this lane. PHASE 1 paper observation — "
        "edge is not established and is not claimed. AI never deposits, withdraws or transfers.",
    )
    fig.text(fx(0.30), fy(1.56), "\n".join(notes), fontsize=8.8, color=MUTED, family=SANS, va="top", linespacing=1.6)
