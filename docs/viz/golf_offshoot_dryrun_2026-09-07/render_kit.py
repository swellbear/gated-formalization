"""Shared illustrator render kit for the golf-offshoot dry-run boards (Ill 1 + Ill 2).

Dark, cold-readable style: large fonts, high contrast, no decorative chrome.
Both boards carry the same honesty badge strip, so it lives here once.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

BG = "#0b0f14"
PANEL = "#121a24"
PANEL_EDGE = "#1f2c3a"
GRID = "#1b2735"
TEXT = "#e8eff6"
MUTED = "#93a5ba"
DIM = "#6b7f96"

ACCENT = "#4cc9f0"
ACCENT_2 = "#f4a259"
ACCENT_3 = "#a78bfa"
GOOD = "#4ade80"
WALL = "#22d3ee"
PENDING = "#fbbf24"
WARN = "#f87171"

BADGES = [
    "PHASE 1 OBSERVATION",
    "AI: NO CASH IN/OUT",
    "SOURCE: real operating exports (not demo)",
    "paper observation only",
]


def apply_style() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": BG,
            "savefig.facecolor": BG,
            "axes.facecolor": PANEL,
            "axes.edgecolor": PANEL_EDGE,
            "axes.labelcolor": TEXT,
            "axes.titlecolor": TEXT,
            "axes.linewidth": 1.4,
            "text.color": TEXT,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "grid.color": GRID,
            "grid.linewidth": 1.0,
            "font.family": "DejaVu Sans",
            "font.size": 17,
            "axes.titlesize": 24,
            "axes.labelsize": 18,
            "xtick.labelsize": 16,
            "ytick.labelsize": 16,
            "legend.fontsize": 17,
            "legend.frameon": False,
            "figure.dpi": 110,
        }
    )


def panel(ax, title: str, subtitle: str | None = None) -> None:
    """Give an axes the standard panel look plus a title / subtitle pair."""
    ax.set_facecolor(PANEL)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color(PANEL_EDGE)
    ax.tick_params(length=0)
    ax.set_title(title, loc="left", pad=38 if subtitle else 14, fontweight="bold")
    if subtitle:
        ax.annotate(
            subtitle,
            xy=(0, 1.0),
            xycoords="axes fraction",
            xytext=(0, 9),
            textcoords="offset points",
            ha="left",
            va="bottom",
            fontsize=15,
            color=MUTED,
        )


def text_panel(ax, title: str, subtitle: str | None = None) -> None:
    """A panel used purely to hold typeset lines rather than plotted data."""
    panel(ax, title, subtitle)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.add_patch(
        FancyBboxPatch(
            (0.004, 0.01),
            0.992,
            0.98,
            boxstyle="round,pad=0.012,rounding_size=0.02",
            transform=ax.transAxes,
            facecolor=PANEL,
            edgecolor=PANEL_EDGE,
            linewidth=1.4,
            zorder=0,
        )
    )


def chip(ax, x, y, label, color, *, fontsize=15, pad=0.34):
    """Small pill label, used for badges and wall/pending markers."""
    return ax.text(
        x,
        y,
        label,
        transform=ax.transAxes,
        ha="left",
        va="center",
        fontsize=fontsize,
        color=color,
        fontweight="bold",
        bbox=dict(
            boxstyle=f"round,pad={pad}",
            facecolor=BG,
            edgecolor=color,
            linewidth=1.6,
        ),
    )


# Chrome is positioned in inches from the figure edge, not in figure fractions,
# so boards of different heights get identical headers and badge strips.
HEADER_BLOCK_IN = 2.60
FOOTER_BLOCK_IN = 1.41


def _from_top(fig, inches: float) -> float:
    return 1.0 - inches / fig.get_figheight()


def _from_bottom(fig, inches: float) -> float:
    return inches / fig.get_figheight()


def header(fig, kicker: str, title: str, standfirst: str) -> None:
    fig.text(0.012, _from_top(fig, 0.30), kicker, fontsize=17, color=ACCENT, fontweight="bold", va="top")
    fig.text(0.012, _from_top(fig, 0.58), title, fontsize=41, color=TEXT, fontweight="bold", va="top")
    fig.text(0.012, _from_top(fig, 1.30), standfirst, fontsize=19, color=MUTED, va="top", linespacing=1.45)


def banner(
    fig,
    y_in: float,
    height_in: float,
    headline: str,
    body: str,
    color: str = WALL,
    facecolor: str = "#10202b",
) -> None:
    """Full-width callout box measured in inches down from the top of the figure."""
    x0, x1 = 0.012, 0.988
    fig.patches.append(
        FancyBboxPatch(
            (x0, _from_top(fig, y_in + height_in)),
            x1 - x0,
            height_in / fig.get_figheight(),
            boxstyle="round,pad=0,rounding_size=0.006",
            transform=fig.transFigure,
            facecolor=facecolor,
            edgecolor=color,
            linewidth=2.4,
            zorder=1,
        )
    )
    fig.text(
        x0 + 0.012,
        _from_top(fig, y_in + 0.34),
        headline,
        fontsize=24,
        color=color,
        fontweight="bold",
        va="center",
        zorder=2,
    )
    fig.text(
        x0 + 0.012,
        _from_top(fig, y_in + 0.72),
        body,
        fontsize=17,
        color=TEXT,
        va="top",
        linespacing=1.5,
        zorder=2,
    )


def _badge_row(fig, y_in: float, labels: list[tuple[str, str]], fontsize: int) -> None:
    x = 0.012
    y = _from_bottom(fig, y_in)
    for label, color in labels:
        t = fig.text(
            x,
            y,
            label,
            fontsize=fontsize,
            color=color,
            fontweight="bold",
            va="center",
            ha="left",
            bbox=dict(
                boxstyle="round,pad=0.42",
                facecolor="#10202b",
                edgecolor=color,
                linewidth=1.6,
            ),
        )
        fig.canvas.draw()
        bbox = t.get_window_extent(renderer=fig.canvas.get_renderer())
        x += bbox.width / fig.bbox.width + 0.014


def badge_strip(fig, y_in: float = 1.10, extra: list[tuple[str, str]] | None = None) -> None:
    """The shared honesty badges. Identical on every board in this set.

    ``extra`` adds a second, board-specific row above the shared one. A board that
    passes nothing gets a byte-identical strip to every other board here.
    """
    _badge_row(fig, y_in, [(label, WALL) for label in BADGES], 16)
    if extra:
        _badge_row(fig, y_in + 0.62, extra, 16)


def footer(fig, lines: list[str], y_in: float = 0.72) -> None:
    fig.text(
        0.012,
        _from_bottom(fig, y_in),
        "\n".join(lines),
        fontsize=15,
        color=DIM,
        va="top",
        linespacing=1.5,
    )


def save(fig, path, min_px: int = 2400) -> tuple[int, int]:
    """Save at a dpi that guarantees the long edge clears ``min_px``."""
    w_in, h_in = fig.get_size_inches()
    dpi = max(110, int(min_px / max(w_in, h_in)) + 1)
    fig.savefig(path, dpi=dpi, facecolor=BG)
    plt.close(fig)
    return int(round(w_in * dpi)), int(round(h_in * dpi))
