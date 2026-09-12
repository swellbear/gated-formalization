"""Honer paper board PNG. Honer files only. Never Lineage A."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from golf_offshoot.honer_15m.board import HonerRow, HonerStanding, collect_standing
from golf_offshoot.honer_15m.books import load_ledger
from golf_offshoot.honer_15m.paths import assert_honer_path, board_png_path, decisions_path

TITLE = "KXBTC15M · honer_15m — search and exam paper board"
BADGES = (
    "HONER SIBLING",
    "PHASE 1 OBSERVATION",
    "PAPER OBSERVATION ONLY",
    "AI: NO CASH IN/OUT",
    "TRADING NOT ARMED",
)

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

FIG_W = 24.8
DPI = 100
ROW_IN = 0.40
HEADER_IN = 3.20
FOOTER_IN = 1.80
BLOCK_HEAD_IN = 1.10
BLOCK_GAP_IN = 0.34
MARGIN_IN = 0.30

COLUMNS: tuple[tuple[str, float, str], ...] = (
    ("ticker", 0.30, "TICKER (full)"),
    ("window", 2.50, "WINDOW (ET)"),
    ("action", 3.72, "ACTION"),
    ("posted", 4.88, "POSTED YES"),
    ("cutoff", 5.98, "CUTOFF"),
    ("near", 7.08, "NEAR LINE"),
    ("spread", 8.28, "SPREAD"),
    ("wide", 9.38, "WIDE-BOOK"),
    ("kalshi", 10.62, "KALSHI RESULT"),
    ("pnl", 12.28, "PAPER PNL"),
    ("why", 14.10, "WHY"),
    ("source", 20.55, "SOURCE FILE(S)"),
)
PNL_AX_X = 17.95
PNL_AX_W = 2.20


def chart_png_path() -> Path:
    path = board_png_path()
    assert_honer_path(path)
    return path


def _book_lines(book: str) -> tuple[str, ...]:
    led = load_ledger(book)
    return (
        f"book: bankroll {float(led.get('bankroll') or 0):.2f} · "
        f"betting_pnl {float(led.get('betting_pnl') or 0):+.2f} · "
        f"fills {int(led.get('fills') or 0)} · skips {int(led.get('skips') or 0)} · this book only",
        f"source: golf-offshoot/data/honer_15m/{book}/ · never added to the other book or Lineage A",
    )


def _chip(row: HonerRow) -> tuple[str, str, str]:
    if row.pending or row.kalshi_result not in {"yes", "no"}:
        return ("PENDING", INK, PENDING_FILL)
    if row.kalshi_result == "yes":
        return ("YES", "#fff", YES)
    return ("NO", "#fff", NO)


def maybe_render(*, force: bool = False) -> Path | None:
    dest = chart_png_path()
    if not force and dest.is_file():
        try:
            from golf_offshoot.honer_15m.paths import family_amend_path, library_path, theta_path
            from golf_offshoot.quote_bus.paths import snapshot_path

            png_m = dest.stat().st_mtime
            newest = png_m
            watched = [theta_path(), library_path(), family_amend_path(), snapshot_path()]
            for book in ("search", "exam"):
                watched.append(decisions_path(book))
            for path in watched:
                if path.is_file():
                    newest = max(newest, path.stat().st_mtime)
            if png_m >= newest:
                return dest
        except OSError:
            pass
    return render_honer_window_strip()


def render_honer_window_strip() -> Path | None:
    standing = collect_standing()
    search_rows = standing.png_search_rows
    exam_rows = standing.png_exam_rows
    if not search_rows and not exam_rows:
        # Still draw the empty exam block so idle is visible when search exists.
        if not search_rows:
            return None
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.lines import Line2D
        from matplotlib.patches import Patch, Rectangle
    except ImportError:
        return None

    blocks: list[tuple[str, tuple[str, ...], list[HonerRow], int]] = [
        (
            "HONER SEARCH BOOK — discovery, cutoff may move, never a keep",
            _book_lines("search"),
            search_rows,
            len(standing.search_rows) + standing.search_trimmed,
        ),
        (
            "HONER EXAM BOOK — frozen cutoff, own $100, not a keep",
            _book_lines("exam")
            if exam_rows
            else (
                f"exam idle — {standing.freeze_meter}",
                "source: golf-offshoot/data/honer_15m/exam/ — empty on purpose",
            ),
            exam_rows,
            len(exam_rows) + standing.exam_trimmed,
        ),
    ]

    body_in = 0.0
    for _title, _lines, rows, _total in blocks:
        count = max(1, len(rows))
        body_in += BLOCK_HEAD_IN + ROW_IN * count
    body_in += BLOCK_GAP_IN
    fig_h = HEADER_IN + body_in + FOOTER_IN

    fig = plt.figure(figsize=(FIG_W, fig_h), dpi=DPI)
    fig.patch.set_facecolor(BG)

    def fx(x_in: float) -> float:
        return x_in / FIG_W

    def fy(y_in: float) -> float:
        return y_in / fig_h

    pnl_values = [row.pnl for _t, _l, rows, _n in blocks for row in rows if row.pnl is not None]
    pnl_span = max((abs(v) for v in pnl_values), default=0.0) * 1.35 or 1.0

    cursor_in = fig_h - HEADER_IN
    for index, (title, book_lines, rows, total) in enumerate(blocks):
        draw_rows = rows or []
        panel_h = ROW_IN * max(1, len(draw_rows))
        bottom_in = cursor_in - BLOCK_HEAD_IN - panel_h
        top_in = bottom_in + panel_h
        count = f"({len(draw_rows)} window{'s' if len(draw_rows) != 1 else ''})"
        if total > len(draw_rows) and draw_rows:
            count = f"(newest {len(draw_rows)} of {total} windows)"
        fig.text(
            fx(MARGIN_IN),
            fy(top_in + 0.80),
            f"{title}  {count}",
            fontsize=12.5,
            color=INK,
            fontweight="bold",
            family=SANS,
            va="bottom",
        )
        for line_index, line in enumerate(book_lines[:2]):
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
            fig.text(
                fx(x_in),
                fy(top_in + 0.10),
                label,
                fontsize=8.4,
                color=MUTED,
                fontweight="bold",
                family=SANS,
                va="bottom",
            )
        if any(row.pnl is not None for row in draw_rows):
            fig.text(
                fx(PNL_AX_X),
                fy(top_in + 0.10),
                "PAPER PNL BAR (this book only)",
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
        if not draw_rows:
            fig.text(
                fx(MARGIN_IN),
                fy(top_in - ROW_IN / 2),
                f"Exam idle. {standing.freeze_meter}",
                fontsize=10,
                color=MUTED,
                family=SANS,
                va="center",
            )
        for row_index, row in enumerate(draw_rows):
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
            fig.text(
                fx(COLUMNS[0][1]),
                centre,
                row.ticker,
                fontsize=10,
                color=INK,
                fontweight="bold",
                family=MONO,
                va="center",
            )
            label, text_color, fill = _chip(row)
            why = row.why_short[:64] + ("…" if len(row.why_short) > 64 else "")
            cells = {
                "window": row.window_et,
                "action": row.action_label,
                "posted": f"{round(row.posted_yes * 100):.0f}¢" if row.posted_yes is not None else "n/a",
                "cutoff": f"{round(row.theta * 100):.0f}¢" if row.theta is not None else "n/a",
                "near": row.near_line_text,
                "spread": row.spread_text,
                "wide": row.delta_text,
                "pnl": row.pnl_text,
                "why": why,
                "source": row.source,
            }
            for key, x_in, _label in COLUMNS[1:]:
                if key == "kalshi":
                    fig.text(
                        fx(x_in),
                        centre,
                        label,
                        fontsize=9,
                        color=text_color,
                        fontweight="bold",
                        family=SANS,
                        va="center",
                        bbox={
                            "boxstyle": "round,pad=0.28",
                            "facecolor": fill,
                            "edgecolor": INK,
                            "linewidth": 0.7,
                        },
                    )
                    continue
                is_pnl = key == "pnl" and row.pnl is not None
                fig.text(
                    fx(x_in),
                    centre,
                    cells[key],
                    fontsize=8.6 if key in {"why", "source"} else 9.2,
                    color=(POS if (row.pnl or 0) >= 0 else NEG) if is_pnl else (FAINT if key == "source" else INK),
                    fontweight="bold" if is_pnl or key == "action" else "normal",
                    family=MONO if key in {"window", "posted", "cutoff", "pnl", "source"} else SANS,
                    va="center",
                )
        if any(row.pnl is not None for row in draw_rows):
            ax = fig.add_axes((fx(PNL_AX_X), fy(bottom_in), fx(PNL_AX_W), fy(panel_h)))
            _draw_pnl_axis(ax, draw_rows, span=pnl_span, show_x=index == 1)
        cursor_in = bottom_in - BLOCK_GAP_IN

    _draw_header(fig, fx, fy, standing, Patch)
    fig.text(
        fx(MARGIN_IN),
        fy(1.20),
        "Trading NOT ARMED. Two honer books. Do not add these bankrolls to each other or to Lineage A.",
        fontsize=12,
        color=INK,
        fontweight="bold",
        family=SANS,
        va="top",
    )
    fig.text(
        fx(MARGIN_IN),
        fy(0.86),
        "ACTION is fill YES or skip. A skip is a row. Pending Kalshi result is never drawn as $0.00. "
        "Only in-band tickets move the line or count toward freeze. PAPER PNL BAR is this block only. "
        "Fee omitted. Not a keep.",
        fontsize=8.8,
        color=MUTED,
        family=SANS,
        va="top",
    )

    dest = chart_png_path()
    dest.parent.mkdir(parents=True, exist_ok=True)
    assert_honer_path(dest)
    fig.savefig(dest, format="png", facecolor=BG)
    plt.close(fig)
    return dest


def _draw_pnl_axis(ax: Any, rows: list[HonerRow], *, span: float, show_x: bool) -> None:
    count = max(1, len(rows))
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
        if row.pnl is None:
            continue
        ax.barh(
            y,
            row.pnl,
            height=0.46,
            color=POS if row.pnl >= 0 else NEG,
            edgecolor=INK,
            linewidth=0.7,
            zorder=3,
        )
    if show_x:
        ax.tick_params(axis="x", labelsize=8, colors=MUTED, length=3)
        ax.set_xlabel(
            "paper pnl in $ as recorded on that window's own file · this book only",
            fontsize=8.2,
            color=MUTED,
            labelpad=5,
        )
    else:
        ax.tick_params(axis="x", labelbottom=False, length=0)


def _draw_header(fig: Any, fx: Any, fy: Any, standing: HonerStanding, patch_cls: Any) -> None:
    def from_top(y_in: float) -> float:
        return 1.0 - fy(y_in)

    fig.text(fx(0.30), from_top(0.40), TITLE, fontsize=20, color=INK, fontweight="bold", family=SANS, va="top")
    for offset, line in enumerate(standing.subtitle_lines[:4]):
        fig.text(
            fx(0.30),
            from_top(0.82 + offset * 0.26),
            line,
            fontsize=10.2 if offset == 0 else 9.0,
            color=INK if offset == 0 else MUTED,
            family=SANS,
            va="top",
        )
    x_in = 0.30
    for badge in BADGES:
        text = fig.text(
            fx(x_in),
            from_top(2.55),
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
            patch_cls(facecolor=YES, edgecolor=INK, label='chip "YES" — honer settlement says yes'),
            patch_cls(facecolor=NO, edgecolor=INK, label='chip "NO" — honer settlement says no'),
            patch_cls(facecolor=PENDING_FILL, edgecolor=INK, label='chip "PENDING" — still waiting on Kalshi'),
        ],
        title="KALSHI RESULT (honer copy only)",
        loc="upper left",
        bbox_to_anchor=(fx(14.20), from_top(0.34)),
        frameon=False,
        fontsize=9,
        title_fontsize=9.2,
        alignment="left",
    )
