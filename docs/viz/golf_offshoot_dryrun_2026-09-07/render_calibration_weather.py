#!/usr/bin/env python3
"""Render the golf-offshoot "calibration weather" chart.

Reads the frozen calibration artifact
``golf-offshoot/data/calibration/weights_calib-v3.json`` and draws one dark,
cold-readable PNG comparing expert vs calibrated weights on train and hold-out
events, per market bucket.

Every number on the chart comes from that JSON. There is no demo path, no mock
fallback, and no shadow-settle input: if the artifact is missing the script
fails instead of drawing anything.

    python docs/viz/golf_offshoot_dryrun_2026-09-07/render_calibration_weather.py
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch, Patch

REPO_ROOT = Path(__file__).resolve().parents[3]
SOURCE = REPO_ROOT / "golf-offshoot" / "data" / "calibration" / "weights_calib-v3.json"
OUT_PNG = Path(__file__).resolve().parent / "calibration_weather.png"

# Shadow honesty strip is deliberately absent. It stays absent until a LIVE
# advises.jsonl exists in the repo; nothing here may stand in for one.
SHADOW_LEDGER = REPO_ROOT / "golf-offshoot" / "data" / "shadow" / "advises.jsonl"

BUCKETS = ["make_cut", "top_20", "top_10", "top_5", "win"]
BUCKET_LABELS = {
    "make_cut": "Make the cut",
    "top_20": "Top 20",
    "top_10": "Top 10",
    "top_5": "Top 5",
    "win": "Win",
}

BG = "#0b0f14"
PANEL = "#111823"
GRID = "#1e2836"
INK = "#e8eef6"
MUTED = "#94a6bb"
FAINT = "#5f7086"
EXPERT = "#f0a23c"
CALIB = "#43c6c0"
WORSE = "#e2615f"
BETTER = "#57b98a"


def load_artifact() -> dict:
    if not SOURCE.exists():
        raise SystemExit(f"missing real calibration artifact: {SOURCE}")
    with SOURCE.open() as fh:
        return json.load(fh)


def style_axes(ax, *, title: str, subtitle: str) -> None:
    ax.set_facecolor(PANEL)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(colors=MUTED, labelsize=15, length=0)
    ax.set_title(title, color=INK, fontsize=21, fontweight="bold", loc="left", pad=26)
    ax.text(
        0.0,
        1.035,
        subtitle,
        transform=ax.transAxes,
        color=MUTED,
        fontsize=14.5,
        va="bottom",
        ha="left",
    )


def dot_panel(
    ax,
    expert: dict,
    fitted: dict,
    *,
    title: str,
    subtitle: str,
    xlabel: str,
    note: str | None = None,
) -> None:
    """Log-scale dot plot: two markers per bucket, joined by the gap between them.

    Dots, not bars: on a log axis a bar length would encode nothing honest.
    """
    style_axes(ax, title=title, subtitle=subtitle)
    ys = list(range(len(BUCKETS)))[::-1]

    for y, bucket in zip(ys, BUCKETS):
        e = expert[bucket]
        f = fitted[bucket]
        ax.plot([min(e, f), max(e, f)], [y, y], color=FAINT, lw=3, solid_capstyle="round", zorder=2)
        ax.scatter([e], [y], s=290, color=EXPERT, zorder=4, edgecolor=BG, linewidth=1.6)
        ax.scatter([f], [y], s=150, color=CALIB, zorder=5, edgecolor=BG, linewidth=1.4)
        ax.text(
            e * 1.16,
            y,
            f"{e:.5f}",
            color=INK,
            fontsize=14,
            va="center",
            ha="left",
            fontweight="bold",
        )

    ax.set_xscale("log")
    ax.set_yticks(ys)
    ax.set_yticklabels([BUCKET_LABELS[b] for b in BUCKETS], color=INK, fontsize=16)
    ax.set_ylim(-1.55, len(BUCKETS) - 0.25)
    ax.set_xlabel(xlabel, color=MUTED, fontsize=15, labelpad=12)
    ax.grid(axis="x", color=GRID, lw=1.1)
    ax.set_axisbelow(True)

    if note:
        ax.text(
            0.014,
            0.055,
            note,
            transform=ax.transAxes,
            color=MUTED,
            fontsize=14,
            va="bottom",
            ha="left",
            style="italic",
        )

    # Leave room on the right so the printed scores stay inside the panel.
    lo = min(min(expert.values()), min(fitted.values()))
    hi = max(max(expert.values()), max(fitted.values()))
    ax.set_xlim(lo * 0.62, hi * 2.6)


def delta_panel(ax, metrics: dict) -> None:
    """Zoom on hold-out (calibrated minus expert). Lower score is better."""
    style_axes(
        ax,
        title="The whole gap, zoomed in \u2014 held-out events",
        subtitle="Calibrated minus expert. Left of zero = calibrated a hair better.",
    )

    brier = [
        metrics["holdout_fitted"]["brier"][b] - metrics["holdout_expert"]["brier"][b]
        for b in BUCKETS
    ]
    logloss = [
        metrics["holdout_fitted"]["logloss"][b] - metrics["holdout_expert"]["logloss"][b]
        for b in BUCKETS
    ]

    ys = list(range(len(BUCKETS)))[::-1]
    h = 0.32
    for i, y in enumerate(ys):
        if i % 2 == 0:
            ax.axhspan(y - 0.46, y + 0.46, color="#182231", zorder=1)

    for y, db, dl in zip(ys, brier, logloss):
        for offset, value, hatch in ((h / 2 + 0.015, db, None), (-h / 2 - 0.015, dl, "///")):
            color = WORSE if value > 0 else BETTER
            ax.barh(
                y + offset,
                value * 1e4,
                height=h,
                color=color,
                alpha=0.92 if hatch is None else 0.5,
                hatch=hatch,
                edgecolor=color,
                linewidth=1.2,
                zorder=3,
            )
            side = 1 if value > 0 else -1
            ax.text(
                value * 1e4 + side * 0.45,
                y + offset,
                f"{value * 1e4:+.2f}",
                color=INK,
                fontsize=12.5,
                va="center",
                ha="left" if value > 0 else "right",
            )

    ax.axvline(0, color=INK, lw=1.6, zorder=4)
    ax.set_yticks(ys)
    ax.set_yticklabels([BUCKET_LABELS[b] for b in BUCKETS], color=INK, fontsize=16)
    # Extra headroom below the bars so the key sits in empty space, not on data.
    ax.set_ylim(-2.5, len(BUCKETS) - 0.25)
    span = max(abs(v) for v in brier + logloss) * 1e4
    ax.set_xlim(-span * 1.85, span * 1.85)
    ax.set_xlabel(
        "Difference \u00d7 10\u207b\u2074  (a full point of Brier is 10,000 of these)",
        color=MUTED,
        fontsize=15,
        labelpad=12,
    )
    ax.grid(axis="x", color=GRID, lw=1.1)
    ax.set_axisbelow(True)

    ax.legend(
        handles=[
            Patch(facecolor=BETTER, edgecolor=BETTER, label="calibrated slightly better"),
            Patch(facecolor=WORSE, edgecolor=WORSE, label="calibrated slightly worse"),
            Patch(facecolor=MUTED, edgecolor=MUTED, alpha=0.9, label="solid = Brier"),
            Patch(facecolor=MUTED, edgecolor=MUTED, alpha=0.5, hatch="///", label="hatched = log loss"),
        ],
        loc="lower center",
        ncol=4,
        frameon=False,
        fontsize=13.5,
        labelcolor=MUTED,
        handletextpad=0.5,
        columnspacing=1.8,
    )


def badge_row(fig, badges, *, y: float, x0: float = 0.035, fontsize: float = 14.5) -> None:
    renderer = fig.canvas.get_renderer()
    x = x0
    for text, fg, bg in badges:
        label = fig.text(
            x,
            y,
            f"  {text}  ",
            color=fg,
            fontsize=fontsize,
            fontweight="bold",
            va="center",
            ha="left",
            bbox=dict(boxstyle="round,pad=0.42", facecolor=bg, edgecolor=fg, linewidth=1.3),
        )
        width = label.get_window_extent(renderer=renderer).width / fig.bbox.width
        x += width + 0.013


def main() -> Path:
    data = load_artifact()
    metrics = data["metrics"]
    extra = data["extra"]
    train_names = extra["train_names"]
    holdout_names = extra["holdout_names"]

    fig = plt.figure(figsize=(24.0, 18.0), dpi=110)
    fig.patch.set_facecolor(BG)

    fig.text(
        0.035,
        0.972,
        "Calibration weather \u2014 golf-offshoot",
        color=INK,
        fontsize=41,
        fontweight="bold",
        va="center",
    )
    fig.text(
        0.035,
        0.943,
        f"Did the fitted weights beat the hand-set expert weights? On events the fit never saw: no. "
        f"Frozen recommendation: {data['recommendation']}.",
        color=MUTED,
        fontsize=19,
        va="center",
    )
    fig.text(
        0.035,
        0.921,
        f"{data['version_id']}   \u00b7   artifact frozen {data['created_at'][:10]}   \u00b7   "
        f"expert weight hash {data['weight_hash_expert']}   \u00b7   calibrated weight hash {data['weight_hash_calibrated']}",
        color=FAINT,
        fontsize=15,
        va="center",
    )

    badge_row(
        fig,
        [
            ("PHASE 1 OBSERVATION", "#7fd4ff", "#0e2233"),
            ("AI: NO CASH IN / NO CASH OUT", "#ffc98a", "#2a1d0e"),
            ("SOURCE: weights_calib-v3.json", "#9fe6c8", "#0e2620"),
            ("NOT Softened", "#c9b6ff", "#1b1630"),
            ("NOT LIVE bets", "#ff9a9a", "#2c1416"),
        ],
        y=0.892,
    )

    gs = fig.add_gridspec(
        2,
        2,
        left=0.075,
        right=0.975,
        top=0.800,
        bottom=0.408,
        hspace=0.62,
        wspace=0.24,
    )

    dot_panel(
        fig.add_subplot(gs[0, 0]),
        metrics["holdout_expert"]["brier"],
        metrics["holdout_fitted"]["brier"],
        title="Held-out Brier score by market bucket",
        subtitle=f"3 events never used to accept a fit \u00b7 n = {metrics['holdout_expert']['n']:,} player-starts \u00b7 lower is better \u00b7 log scale",
        xlabel="Brier score (log scale) \u2014 printed number is the expert score",
        note="In every bucket the two dots land on top of each other. That overlap is the finding.",
    )
    dot_panel(
        fig.add_subplot(gs[0, 1]),
        metrics["train_expert"]["brier"],
        metrics["train_fitted"]["brier"],
        title="Train Brier score by market bucket",
        subtitle=f"12 events the search could fit on \u00b7 n = {metrics['train_expert']['n']:,} player-starts \u00b7 lower is better \u00b7 log scale",
        xlabel="Brier score (log scale) \u2014 printed number is the expert score",
    )
    dot_panel(
        fig.add_subplot(gs[1, 0]),
        metrics["holdout_expert"]["logloss"],
        metrics["holdout_fitted"]["logloss"],
        title="Held-out log loss by market bucket",
        subtitle="Second scoring rule, same held-out events. It tells the same story as Brier.",
        xlabel="Log loss (log scale) \u2014 printed number is the expert score",
    )
    delta_panel(fig.add_subplot(gs[1, 1]), metrics)

    fig.legend(
        handles=[
            Line2D([], [], marker="o", ls="", markersize=17, color=EXPERT, label="Expert weights (what production actually uses)"),
            Line2D([], [], marker="o", ls="", markersize=13, color=CALIB, label="Calibrated weights (the fitted vector, stored for comparison only)"),
        ],
        loc="upper left",
        bbox_to_anchor=(0.035, 0.868),
        frameon=False,
        fontsize=16.5,
        labelcolor=INK,
        ncol=2,
        columnspacing=3.0,
        handletextpad=0.6,
    )

    # Footer card
    card = FancyBboxPatch(
        (0.035, 0.048),
        0.93,
        0.285,
        transform=fig.transFigure,
        boxstyle="round,pad=0.010",
        facecolor=PANEL,
        edgecolor=GRID,
        linewidth=1.5,
        zorder=0,
    )
    fig.patches.append(card)

    fig.text(
        0.052,
        0.312,
        "What this chart is saying, in plain English",
        color=INK,
        fontsize=20,
        fontweight="bold",
        va="center",
    )
    plain = (
        "Two sets of factor weights were scored on the same golf events: the hand-set \u201cexpert\u201d weights, and a vector fitted by Bayesian search.\n"
        "On the three held-out events the fitted vector wins some buckets by a hair and loses others by a hair. That is noise, not an edge.\n"
        f"So the artifact froze the recommendation as {data['recommendation']}: production keeps the expert weights, and the fitted vector is stored only for comparison.\n"
        "Artifact note, quoted: \u201cHold-out did not clearly beat expert \u03b1; default recommendation is to keep expert weights in production.\u201d"
    )
    fig.text(0.052, 0.292, plain, color=MUTED, fontsize=16.5, va="top", linespacing=1.9)

    fig.text(
        0.052,
        0.186,
        "Train events (12, the fit was allowed to see these)",
        color=INK,
        fontsize=15,
        fontweight="bold",
        va="center",
    )
    mid = (len(train_names) + 1) // 2
    fig.text(
        0.052,
        0.168,
        "\n".join(f"\u00b7 {n}" for n in train_names[:mid]),
        color=FAINT,
        fontsize=13.5,
        va="top",
        linespacing=1.7,
    )
    fig.text(
        0.255,
        0.168,
        "\n".join(f"\u00b7 {n}" for n in train_names[mid:]),
        color=FAINT,
        fontsize=13.5,
        va="top",
        linespacing=1.7,
    )
    fig.text(
        0.430,
        0.186,
        "Held-out events (3, never fitted on)",
        color=INK,
        fontsize=15,
        fontweight="bold",
        va="center",
    )
    fig.text(
        0.430,
        0.168,
        "\n".join(f"\u00b7 {n}" for n in holdout_names),
        color=FAINT,
        fontsize=13.5,
        va="top",
        linespacing=1.7,
    )

    fig.text(
        0.635,
        0.186,
        "What this is not",
        color=INK,
        fontsize=15,
        fontweight="bold",
        va="center",
    )
    fig.text(
        0.635,
        0.168,
        "\u00b7 Not a claim that any edge is established \u2014 the hold-out did not clear the bar.\n"
        "\u00b7 Not a bet, a price, a pick, or any buy/sell advice.\n"
        "\u00b7 Not a Soften verdict, and not a Softened board.\n"
        "\u00b7 Not shadow-settle evidence: no LIVE advises.jsonl exists, so the shadow\n"
        "   honesty strip is BLOCKED and deliberately left off this chart.",
        color=FAINT,
        fontsize=13.5,
        va="top",
        linespacing=1.9,
    )

    fig.text(
        0.035,
        0.024,
        f"Every number read from {SOURCE.relative_to(REPO_ROOT)} \u00b7 no_future_leakage: {str(data['no_future_leakage']).lower()} \u00b7 "
        f"search_ran: {str(data['search_ran']).lower()} \u00b7 {data['n_evals']} search evaluations \u00b7 "
        f"recent as-of SG coverage {extra['asof_coverage']['recent_coverage'] * 100:.1f}% \u00b7 median measured events {extra['asof_coverage']['median_events']:.0f}. "
        "Observation only. No mock or demo data path.",
        color=FAINT,
        fontsize=13,
        va="center",
    )

    if SHADOW_LEDGER.exists():
        raise SystemExit(
            "advises.jsonl now exists; the shadow honesty strip is no longer blocked. "
            "Update this script deliberately instead of letting it render a stale chart."
        )

    fig.savefig(OUT_PNG, facecolor=BG, dpi=110)
    plt.close(fig)
    return OUT_PNG


if __name__ == "__main__":
    path = main()
    print(f"wrote {path}")
