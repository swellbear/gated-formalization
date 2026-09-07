"""Ghost Strip prototype — after-charge displayed range vs the published window.

EXAMPLE DATA ONLY. Every number below is invented by hand for layout review.
Nothing here was scraped from Teslascope, read off a window sticker, or taken
from any real vehicle. The chart sorts readings into three buckets and stops
there: it is not a verdict, not a Soften/admit board, and not buy/sell advice.

Run:  python3 render_ghost_strip.py
Out:  ghost_strip.png  (2560 x 1440)
"""

from __future__ import annotations

import os

import viz_style as vs

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ghost_strip.png")

# ------------------------------------------------------------ EXAMPLE data ---
# Invented profile. A 2020 Model S Long Range Plus stands in as the *shape* of
# the question. The bounds below are NOT that car's real EPA or window-sticker
# figures; they are round placeholders chosen to make the three bands legible.
VEHICLE = "Stand-in profile: 2020 Model S Long Range Plus \u00b7 all bounds and readings below are invented"

WINDOW_LOW = 370.0      # EXAMPLE bottom of the stand-in sticker / EPA window
WINDOW_HIGH = 400.0     # EXAMPLE top of the same stand-in window
MARKETING_HIGH = 415.0  # EXAMPLE "up to" headline number, above the window

# 28 invented after-charge readings (displayed rated miles at a charge to full),
# in log order. Hand-written, not sampled, not real.
READINGS = [
    404, 392, 409, 388, 395, 376, 383, 374, 379, 371,
    352, 357, 348, 355, 344, 350, 341, 353, 347, 336,
    351, 343, 349, 338, 345, 342, 339, 346,
]

BUCKETS = [
    ("IN-WINDOW", vs.IN_WINDOW, "inside the\nexample window"),
    ("MARKETING-\nONLY", vs.MARKETING, "only inside the\nexample \u201cup to\u201d"),
    ("NOWHERE", vs.NOWHERE, "under every\nexample number"),
]

X_MAX = 41.0
PLOT_END = 28.9 / X_MAX  # bands stop before the right-hand label gutter


def bucket_of(miles: float) -> int:
    """0 = in-window, 1 = marketing-only, 2 = nowhere. There is no fourth bucket."""
    if WINDOW_LOW <= miles <= WINDOW_HIGH:
        return 0
    if WINDOW_HIGH < miles <= MARKETING_HIGH:
        return 1
    return 2


def draw() -> str:
    fig = vs.new_figure()

    vs.example_badge(fig)
    vs.title_block(
        fig,
        "Ghost Strip \u2014 where the after-charge number lands",
        "Displayed rated miles after each charge, against a published range window.",
        VEHICLE,
    )

    counts = [0, 0, 0]
    for miles in READINGS:
        counts[bucket_of(miles)] += 1

    # ------------------------------------------------------- strip panel ----
    vs.card(fig, 0.035, 0.335, 0.565, 0.455)
    vs.card_heading(fig, 0.058, 0.748, "The strip",
                    "one dot per example charge-to-full, oldest at the left")

    ax = fig.add_axes([0.078, 0.412, 0.495, 0.275])
    ax.set_xlim(0, X_MAX)
    ax.set_ylim(325, 428)

    bands = [
        (WINDOW_LOW, WINDOW_HIGH, vs.IN_WINDOW, "IN-WINDOW",
         f"{WINDOW_LOW:.0f}\u2013{WINDOW_HIGH:.0f} mi"),
        (WINDOW_HIGH, MARKETING_HIGH, vs.MARKETING, "MARKETING-ONLY",
         f"{WINDOW_HIGH:.0f}\u2013{MARKETING_HIGH:.0f} mi"),
        (325, WINDOW_LOW, vs.NOWHERE, "NOWHERE",
         f"under {WINDOW_LOW:.0f} mi"),
    ]
    for low, high, color, name, note in bands:
        ax.axhspan(low, high, xmax=PLOT_END, facecolor=color, alpha=0.09,
                   zorder=0)
        mid = (low + high) / 2.0
        ax.text(30.0, mid + 5.0, name, ha="left", va="center", fontsize=13,
                fontweight="bold", color=color, zorder=4)
        ax.text(30.0, mid - 5.5, note, ha="left", va="center", fontsize=10.5,
                color=vs.INK_FAINT, zorder=4)

    for edge in (WINDOW_LOW, WINDOW_HIGH, MARKETING_HIGH):
        ax.axhline(edge, xmax=PLOT_END, color=vs.CARD_EDGE, lw=1.3,
                   linestyle=(0, (6, 5)), zorder=1)

    for i, miles in enumerate(READINGS, start=1):
        color = BUCKETS[bucket_of(miles)][1]
        ax.plot([i, i], [325, miles], color=color, lw=1.6, alpha=0.28, zorder=2)
        ax.scatter([i], [miles], s=88, color=color, edgecolors=vs.BG,
                   linewidths=1.5, zorder=3)

    ax.set_xticks([1, 7, 14, 21, 28])
    ax.set_xticklabels(["1st", "7th", "14th", "21st", "28th"])
    ax.set_yticks([340, 360, 380, 400, 420])
    ax.tick_params(labelsize=vs.TICK)
    ax.set_xlabel("example charge session, in invented log order", fontsize=13,
                  labelpad=8)
    ax.set_ylabel("displayed rated miles", fontsize=13, labelpad=8)
    ax.grid(axis="y", color=vs.GRID, lw=0.9)
    ax.set_axisbelow(True)
    vs.strip_axes_spines(ax, keep=("bottom", "left"))

    # ------------------------------------------------------ column panel ----
    vs.card(fig, 0.615, 0.335, 0.35, 0.455)
    vs.card_heading(fig, 0.638, 0.748, "The count",
                    f"all {len(READINGS)} example readings, bucketed")

    bx = fig.add_axes([0.638, 0.478, 0.305, 0.155])
    bx.set_xlim(-0.62, 2.62)
    bx.set_ylim(0, max(counts) * 1.45)
    for i, (_name, color, _sub) in enumerate(BUCKETS):
        bx.bar(i, counts[i], width=0.6, color=color, alpha=0.9,
               edgecolor=color, linewidth=1.5, zorder=2)
        bx.text(i, counts[i] + max(counts) * 0.06, str(counts[i]), ha="center",
                va="bottom", fontsize=vs.BIG_NUMBER, fontweight="bold",
                color=color)
    bx.set_xticks([])
    bx.set_yticks([])
    vs.strip_axes_spines(bx)

    for i, (name, color, sub) in enumerate(BUCKETS):
        cx = 0.638 + 0.305 * ((i + 0.5) / 3.0)
        fig.text(cx, 0.462, name, ha="center", va="top", fontsize=12,
                 fontweight="bold", color=color, linespacing=1.4, zorder=6)
        fig.text(cx, 0.398, sub, ha="center", va="top", fontsize=10.5,
                 color=vs.INK_FAINT, linespacing=1.45, zorder=6)

    # ---------------------------------------------------------- captions ----
    vs.example_line(
        fig,
        "EXAMPLE NUMBERS: invented for layout review \u2014 not Teslascope data, not a window sticker, not any real car.",
        y=0.310,
    )

    vs.caption_card(
        fig,
        0.035,
        0.050,
        0.455,
        0.235,
        "What this chart does",
        [
            "It counts where example after-charge numbers",
            "land: inside the published window, only inside a",
            "marketing \u201cup to\u201d number, or under every",
            "published number. Sorting is the whole job.",
        ],
        heading_color=vs.IN_WINDOW,
    )

    vs.caption_card(
        fig,
        0.510,
        0.050,
        0.455,
        0.235,
        "What it does not do",
        [
            "It is not a verdict and not a method call of any",
            "kind. It does not say a car is bad or that anyone",
            "lied. It is not buy, sell, sue, or repair advice.",
            "A dot in one bucket is a reading, not a fault.",
        ],
        heading_color=vs.NOWHERE,
    )

    vs.footer(
        fig,
        "docs/viz/tesla_prototypes_2026-09-07/ghost_strip.png  \u00b7  regenerate: python3 render_ghost_strip.py",
        "EXAMPLE data \u00b7 not live car data",
    )

    fig.savefig(OUT, facecolor=vs.BG)
    return OUT


if __name__ == "__main__":
    print(draw())
