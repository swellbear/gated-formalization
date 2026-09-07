"""Shared dark-card style for the Teslascope x gated-formalization prototype charts.

EXAMPLE-DATA PROTOTYPES ONLY. Nothing here renders live vehicle telemetry and
nothing here renders a Soften / admit / verdict board.

Layout notes for anyone editing these scripts:

* Figures are 12.8 x 7.2 inches at dpi 200, i.e. 2560 x 1440 px. Point sizes
  below are tuned to that inch size, so the type stays large relative to the
  canvas and survives being scaled down to a phone screen.
* Cards are drawn in figure coordinates at a negative z-order, because
  figure-level patches otherwise paint on top of the axes.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# ---------------------------------------------------------------- palette ----

BG = "#0b0f14"
CARD = "#131a23"
CARD_EDGE = "#22303e"
CARD_DEEP = "#0f151d"

INK = "#e9f0f7"
INK_SOFT = "#aebccb"
INK_FAINT = "#7c8b9a"

# The only three data colors either chart is allowed to use.
IN_WINDOW = "#3ddc97"
MARKETING = "#f5b93f"
NOWHERE = "#e8687f"

BADGE_BG = "#3a2418"
BADGE_EDGE = "#f5b93f"

GRID = "#1b2531"

# ------------------------------------------------------------- type scale ----

FIG_W_IN = 12.8
FIG_H_IN = 7.2
DPI = 200

TITLE = 27
SUBTITLE = 17
KICKER = 15
BADGE = 15
CARD_HEAD = 20
CARD_SUB = 14
BODY = 15
SMALL = 13
TICK = 13
BIG_NUMBER = 34


def line_step(size: float, tight: float = 1.35) -> float:
    """Figure-fraction step between text baselines for a given point size."""
    return size * tight / (FIG_H_IN * 72.0)


def new_figure():
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["DejaVu Sans"],
            "figure.facecolor": BG,
            "savefig.facecolor": BG,
            "axes.facecolor": CARD,
            "text.color": INK,
            "axes.edgecolor": CARD_EDGE,
            "axes.labelcolor": INK_SOFT,
            "xtick.color": INK_SOFT,
            "ytick.color": INK_SOFT,
        }
    )
    fig = plt.figure(figsize=(FIG_W_IN, FIG_H_IN), dpi=DPI)
    fig.patch.set_facecolor(BG)
    return fig


def card(fig, x, y, w, h, facecolor=CARD, edgecolor=CARD_EDGE, radius=0.012,
         lw=1.6, alpha=1.0, zorder=-5):
    """Soft rounded card in figure coordinates, painted behind the axes."""
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        transform=fig.transFigure,
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=lw,
        alpha=alpha,
        zorder=zorder,
        mutation_aspect=FIG_W_IN / FIG_H_IN,
    )
    fig.patches.append(patch)
    return patch


def example_badge(fig, x=0.965, y=0.962,
                  text="EXAMPLE DATA \u2014 NOT LIVE CAR DATA"):
    """Loud EXAMPLE stamp. Both charts carry one above the title."""
    fig.text(
        x,
        y,
        text,
        ha="right",
        va="center",
        fontsize=BADGE,
        fontweight="bold",
        color=MARKETING,
        bbox=dict(
            boxstyle="round,pad=0.5",
            facecolor=BADGE_BG,
            edgecolor=BADGE_EDGE,
            linewidth=1.8,
        ),
        zorder=8,
    )


def title_block(fig, title, subtitle, kicker=None, x=0.035):
    fig.text(x, 0.905, title, ha="left", va="center", fontsize=TITLE,
             fontweight="bold", color=INK)
    fig.text(x, 0.856, subtitle, ha="left", va="center", fontsize=SUBTITLE,
             color=INK_SOFT)
    if kicker:
        fig.text(x, 0.820, kicker, ha="left", va="center", fontsize=KICKER,
                 color=INK_FAINT)


def card_heading(fig, x, y, heading, sub=None):
    fig.text(x, y, heading, ha="left", va="center", fontsize=CARD_HEAD,
             fontweight="bold", color=INK, zorder=6)
    if sub:
        fig.text(x, y - 0.036, sub, ha="left", va="center", fontsize=CARD_SUB,
                 color=INK_FAINT, zorder=6)


def caption_card(fig, x, y, w, h, heading, lines, heading_color=MARKETING,
                 size=14, head_size=CARD_HEAD):
    """Plain-English honesty caption card.

    `lines` are pre-wrapped on purpose: the wording is reviewed as written and
    should not be re-flowed at render time.
    """
    card(fig, x, y, w, h, facecolor=CARD_DEEP)
    fig.text(x + 0.016, y + h - 0.046, heading, ha="left", va="center",
             fontsize=head_size, fontweight="bold", color=heading_color,
             zorder=6)
    step = line_step(size, 1.42)
    for i, text in enumerate(lines):
        fig.text(x + 0.016, y + h - 0.098 - i * step, text, ha="left",
                 va="center", fontsize=size, color=INK_SOFT, zorder=6)


def example_line(fig, text, y=0.305, x=0.035, size=SMALL):
    fig.text(x, y, text, ha="left", va="center", fontsize=size,
             fontweight="bold", color=MARKETING, zorder=6)


def footer(fig, left_text, right_text, y=0.022, size=11):
    fig.text(0.035, y, left_text, ha="left", va="center", fontsize=size,
             color=INK_FAINT)
    fig.text(0.965, y, right_text, ha="right", va="center", fontsize=size,
             color=INK_FAINT)


def strip_axes_spines(ax, keep=()):
    for side in ("top", "right", "bottom", "left"):
        ax.spines[side].set_visible(side in keep)
        if side in keep:
            ax.spines[side].set_color(CARD_EDGE)
