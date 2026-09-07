#!/usr/bin/env python3
"""Ill 1 — Shadow honesty strip.

Renders ``shadow_honesty_strip.png`` from the real operating export
``source/shadow/advises.jsonl`` (162 paper-observation rows, FedEx St. Jude ->
BMW -> TOUR Championship).

What the board is allowed to say: what was observed, in which market, in which
advisory mode, and how the model's stated probability sat against the posted
price. What it must never say: that anything settled, won, lost, paid, or
established an edge. The export carries no settlement fields at all, so every
settle/result column is drawn as PENDING / join later.

Usage:
    python render_shadow_honesty.py
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import render_kit as kit

HERE = Path(__file__).resolve().parent
ADVISES = HERE / "source" / "shadow" / "advises.jsonl"
OUT = HERE / "shadow_honesty_strip.png"

TOURNAMENT_ORDER = [
    "FedEx St. Jude Championship",
    "BMW Championship",
    "TOUR Championship",
]

MARKET_ORDER = ["win", "win_after_r1", "win_after_r2", "win_after_r3", "top_5", "top_10", "top_20"]

MARKET_COLOR = {
    "win": kit.ACCENT,
    "win_after_r1": "#8fd3f4",
    "win_after_r2": "#6aa9d8",
    "win_after_r3": "#4a7fb5",
    "top_5": kit.ACCENT_2,
    "top_10": "#f7c07a",
    "top_20": "#f9dcae",
}

# Columns a settlement join would eventually supply. None of them exist in the
# export, and none of them are being guessed at here.
SETTLEMENT_COLUMNS = [
    "settled_at",
    "outcome / result",
    "won / lost",
    "payout",
    "realized_pnl",
    "closing_line",
    "clv",
    "roi",
]


SETTLEMENT_FIELD_HINTS = ("settle", "outcome", "result", "payout", "pnl", "profit", "clv", "roi", "won", "lost")


def load_rows() -> list[dict]:
    with ADVISES.open() as fh:
        rows = [json.loads(line) for line in fh if line.strip()]

    # The PENDING / join later panel is only honest while the export really has no
    # settlement data. If one ever lands, fail loudly rather than redraw a false claim.
    present = {k for r in rows for k in r}
    leaked = sorted(k for k in present if any(h in k.lower() for h in SETTLEMENT_FIELD_HINTS))
    assert not leaked, f"settlement-shaped fields appeared in the export: {leaked}"
    return rows


def hbar(ax, labels, values, colors, *, total, note=None):
    y = np.arange(len(labels))[::-1]
    ax.barh(y, values, color=colors, height=0.62, zorder=3)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlim(0, max(values) * 1.28)
    ax.set_xticks([])
    ax.xaxis.grid(False)
    for yi, v in zip(y, values):
        ax.annotate(
            f"{v}  ({v / total:.0%})",
            xy=(v, yi),
            xytext=(10, 0),
            textcoords="offset points",
            va="center",
            fontsize=16,
            color=kit.TEXT,
            fontweight="bold",
        )
    if note:
        ax.annotate(
            note,
            xy=(0, 0),
            xycoords="axes fraction",
            xytext=(0, -30),
            textcoords="offset points",
            fontsize=14,
            color=kit.DIM,
        )


def draw_coverage(ax, rows):
    counts = Counter(r["tournament"] for r in rows)
    labels = ["FedEx St. Jude", "BMW", "TOUR Champ."]
    values = [counts[t] for t in TOURNAMENT_ORDER]
    kit.panel(
        ax,
        "Tournament coverage",
        "three FedExCup playoff events, 2026-08-13 → 2026-08-30",
    )
    hbar(
        ax,
        labels,
        values,
        [kit.ACCENT, "#6aa9d8", kit.ACCENT_3],
        total=len(rows),
        note=f"{len(rows)} observation rows · {len({r['run_id'] for r in rows})} runs · "
        f"{len({r['player_id'] for r in rows})} players",
    )


def draw_markets(ax, rows):
    counts = Counter(r["market"] for r in rows)
    values = [counts[m] for m in MARKET_ORDER]
    kit.panel(ax, "Market mix", "outright win dominates; in-play win_after_rN next")
    hbar(
        ax,
        MARKET_ORDER,
        values,
        [MARKET_COLOR[m] for m in MARKET_ORDER],
        total=len(rows),
        note="top_5 / top_10 / top_20 are place markets, not settled placings",
    )


def draw_modes(ax, rows):
    counts = Counter(r["mode"] for r in rows)
    order = [m for m, _ in counts.most_common()]
    values = [counts[m] for m in order]
    kit.panel(ax, "Advisory mode mix", "stay_selective is overwhelmingly dominant")
    hbar(
        ax,
        order,
        values,
        [kit.GOOD if m == "stay_selective" else kit.ACCENT_2 for m in order],
        total=len(rows),
        note="mode = advisor posture, not an instruction anyone followed",
    )


def draw_spread(ax, rows):
    paired = [r for r in rows if r["posted_decimal"] and r["model_probability"] is not None]
    missing = len(rows) - len(paired)
    kit.panel(
        ax,
        "Model probability vs posted price",
        "each dot is one observation row; posted decimal odds converted to implied probability",
    )
    for market in MARKET_ORDER:
        pts = [r for r in paired if r["market"] == market]
        if not pts:
            continue
        ax.scatter(
            [1.0 / r["posted_decimal"] for r in pts],
            [r["model_probability"] for r in pts],
            s=120,
            alpha=0.82,
            color=MARKET_COLOR[market],
            edgecolors=kit.BG,
            linewidths=0.9,
            label=f"{market} ({len(pts)})",
            zorder=3,
        )
    ax.plot([0, 1], [0, 1], color=kit.MUTED, lw=1.8, ls="--", zorder=2)
    ax.annotate(
        "model = posted",
        xy=(0.74, 0.74),
        xytext=(6, -26),
        textcoords="offset points",
        fontsize=15,
        color=kit.MUTED,
        rotation=38,
    )
    ax.set_xlim(-0.03, 0.9)
    ax.set_ylim(-0.03, 1.03)
    ax.set_xlabel("implied probability from posted odds")
    ax.set_ylabel("model probability")
    ax.grid(True, alpha=0.55, zorder=1)
    ax.legend(
        loc="lower right",
        ncol=2,
        labelcolor=kit.TEXT,
        handletextpad=0.4,
        columnspacing=1.0,
        fontsize=15,
    )
    ax.annotate(
        f"{missing} exit rows carry no posted price and are excluded from this panel · "
        "spread is a disagreement in stated probability, NOT an established edge",
        xy=(0, 0),
        xycoords="axes fraction",
        xytext=(0, -66),
        textcoords="offset points",
        fontsize=14,
        color=kit.DIM,
    )


def draw_gap(ax, rows):
    paired = [r for r in rows if r["posted_decimal"] and r["model_probability"] is not None]
    gaps = np.array([r["model_probability"] - 1.0 / r["posted_decimal"] for r in paired])
    kit.panel(
        ax,
        "Disagreement, signed",
        "model probability minus implied probability",
    )
    bins = np.linspace(-0.25, 0.7, 39)
    ax.hist(gaps[gaps > 0], bins=bins, color=kit.ACCENT, alpha=0.9, zorder=3)
    ax.hist(gaps[gaps <= 0], bins=bins, color=kit.ACCENT_2, alpha=0.9, zorder=3)
    ax.axvline(0, color=kit.TEXT, lw=2.0, zorder=4)
    ax.set_xlabel("model p − implied p")
    ax.set_ylabel("rows")
    ax.grid(True, axis="y", alpha=0.5, zorder=1)
    ax.annotate(
        f"model above posted: {int((gaps > 0).sum())} rows\n"
        f"model below posted: {int((gaps <= 0).sum())} rows\n"
        f"median gap: {np.median(gaps):+.3f}",
        xy=(1, 1),
        xycoords="axes fraction",
        xytext=(-12, -12),
        textcoords="offset points",
        ha="right",
        va="top",
        fontsize=15,
        color=kit.TEXT,
        linespacing=1.6,
    )
    ax.annotate(
        "no outcome is attached to any bar",
        xy=(0, 0),
        xycoords="axes fraction",
        xytext=(0, -66),
        textcoords="offset points",
        fontsize=14,
        color=kit.DIM,
    )


def draw_walls(ax, rows):
    n = len(rows)
    kit.text_panel(
        ax,
        "Honesty walls held on every row",
        "field-by-field check against the export, not a claim about intent",
    )
    walls = [
        ("paper_observation_only = true", sum(1 for r in rows if r["paper_observation_only"] is True)),
        ("never_auto_bet = true", sum(1 for r in rows if r["never_auto_bet"] is True)),
        ("run_mode = live (real book, paper record)", sum(1 for r in rows if r["run_mode"] == "live")),
        ("uncertainty interval present (model_p_low/high)", sum(1 for r in rows if r.get("model_p_low") is not None)),
    ]
    for i, (label, count) in enumerate(walls):
        y = 0.86 - i * 0.235
        held = count == n
        kit.chip(ax, 0.035, y, f"{count}/{n}", kit.WALL if held else kit.WARN, fontsize=18)
        ax.text(
            0.20,
            y,
            label,
            transform=ax.transAxes,
            va="center",
            fontsize=19,
            color=kit.TEXT,
        )
        ax.text(
            0.885,
            y,
            "HELD" if held else "BROKEN",
            transform=ax.transAxes,
            va="center",
            ha="left",
            fontsize=17,
            fontweight="bold",
            color=kit.WALL if held else kit.WARN,
        )


def draw_pending(ax):
    kit.text_panel(
        ax,
        "Settlement columns: PENDING / join later",
        "advises.jsonl has no settle, outcome, or PnL field — these are deliberately blank, not zero",
    )
    columns = (SETTLEMENT_COLUMNS[:4], SETTLEMENT_COLUMNS[4:])
    for col, items in zip((0.035, 0.52), columns):
        for i, name in enumerate(items):
            y = 0.87 - i * 0.183
            kit.chip(ax, col, y, "PENDING / join later", kit.PENDING, fontsize=14, pad=0.3)
            ax.text(
                col + 0.215,
                y,
                name,
                transform=ax.transAxes,
                va="center",
                fontsize=18,
                color=kit.TEXT,
                family="DejaVu Sans Mono",
            )
    ax.text(
        0.035,
        0.085,
        "Any win/loss, hit rate, ROI, CLV, or profit number for this window would have to be invented. None is shown.",
        transform=ax.transAxes,
        va="center",
        fontsize=17,
        color=kit.PENDING,
        fontweight="bold",
    )


def draw_plain_english(ax):
    kit.text_panel(ax, "In plain English", None)
    lines = [
        ("These are observations of a live sportsbook,", kit.TEXT),
        ("written down on paper. No money moved.", kit.TEXT),
        ("", kit.TEXT),
        ("Not settled bets. Not a track record.", kit.PENDING),
        ("Not a Kalshi demo or mock feed —", kit.PENDING),
        ("this is the real operating export.", kit.PENDING),
        ("", kit.TEXT),
        ("Nothing here says an edge exists.", kit.WARN),
        ("Nothing here is buy or sell advice.", kit.WARN),
    ]
    for i, (line, color) in enumerate(lines):
        ax.text(
            0.045,
            0.90 - i * 0.098,
            line,
            transform=ax.transAxes,
            va="center",
            fontsize=18,
            color=color,
            fontweight="bold" if color != kit.TEXT else "normal",
        )


def main() -> None:
    kit.apply_style()
    rows = load_rows()

    fig = plt.figure(figsize=(24, 19))
    gs = fig.add_gridspec(
        4,
        3,
        left=0.082,
        right=0.985,
        top=0.855,
        bottom=0.115,
        hspace=0.90,
        wspace=0.32,
        height_ratios=[1.0, 1.35, 0.86, 0.90],
    )

    kit.header(
        fig,
        "GOLF-OFFSHOOT DRY RUN · ILL 1 OF 2 · 2026-09-07",
        "Shadow honesty strip",
        f"{len(rows)} paper-observation rows from the real operating shadow export. "
        "Live book, paper record, no settlement joined yet.",
    )

    draw_coverage(fig.add_subplot(gs[0, 0]), rows)
    draw_markets(fig.add_subplot(gs[0, 1]), rows)
    draw_modes(fig.add_subplot(gs[0, 2]), rows)

    draw_spread(fig.add_subplot(gs[1, 0:2]), rows)
    draw_gap(fig.add_subplot(gs[1, 2]), rows)

    draw_walls(fig.add_subplot(gs[2, 0:2]), rows)
    draw_plain_english(fig.add_subplot(gs[2:4, 2]))

    draw_pending(fig.add_subplot(gs[3, 0:2]))

    kit.badge_strip(fig)
    kit.footer(
        fig,
        [
            "Source: docs/viz/golf_offshoot_dryrun_2026-09-07/source/shadow/advises.jsonl "
            "(162 rows, run_mode=live, paper_observation_only=true, never_auto_bet=true).",
            "Rendered by render_shadow_honesty.py. Counts are read straight from the export; "
            "no win/loss, edge-established, or buy/sell language is derived or implied.",
        ],
    )

    w, h = kit.save(fig, OUT)
    print(f"wrote {OUT} ({w}x{h}px) from {len(rows)} rows")


if __name__ == "__main__":
    main()
