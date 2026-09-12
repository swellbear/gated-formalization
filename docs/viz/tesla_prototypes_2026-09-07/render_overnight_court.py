"""Overnight Court prototype — an overnight rated-miles drop next to the wording
that is supposed to cover it.

EXAMPLE DATA ONLY. The night, the states, and the "paraphrased wording" are all
invented for layout review. The paraphrase blocks are written in plain English
by hand as stand-ins for the kind of standby / parked-loss guidance a maker
publishes; they are not quotes, and nothing here is scraped from Teslascope or
read off a real vehicle.

The chart names one mismatch hole: a stretch where the example log and the
example wording do not line up. Naming a hole is not a verdict, not a claim
that a car is bad, and not buy/sell/sue/repair advice.

Run:  python3 render_overnight_court.py
Out:  overnight_court.png  (2560 x 1440)
"""

from __future__ import annotations

import os

import viz_style as vs

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "overnight_court.png")

# ------------------------------------------------------------ EXAMPLE data ---
VEHICLE = ("Stand-in profile: 2020 Model S Long Range Plus \u00b7 every number, "
           "state, and paraphrase below is invented")

# Hours are decimal and run past 24 so one night is a single increasing axis:
# 22.0 = 10 pm, 26.0 = 2 am, 31.0 = 7 am.
T_START, T_END = 22.0, 31.0
SAMPLE_H = 0.05  # one invented sample every three minutes

ASLEEP = "asleep"
AWAKE_FEATURE = "awake_feature"
AWAKE_BARE = "awake_bare"

STATE_COLOR = {
    ASLEEP: vs.IN_WINDOW,
    AWAKE_FEATURE: vs.MARKETING,
    AWAKE_BARE: vs.NOWHERE,
}

# (state, start hour, end hour, rated miles at start, rated miles at end)
SEGMENTS = [
    (AWAKE_FEATURE, 22.0, 23.5, 268.0, 264.0),
    (ASLEEP, 23.5, 26.0, 264.0, 263.0),
    (AWAKE_BARE, 26.0, 28.5, 263.0, 252.0),
    (ASLEEP, 28.5, 31.0, 252.0, 249.0),
]

HOLE_ID = "G-EX-AWAKE-DRAIN-01"

# Hand-written plain-English stand-ins for published standby / parked-loss
# guidance. Paraphrase, not quotation. EXAMPLE wording only.
PARAPHRASE = [
    (ASLEEP, "Parked and asleep",
     ["Losing some range while parked is",
      "normal and expected."]),
    (AWAKE_FEATURE, "Awake for a feature",
     ["Leaving things like security camera",
      "mode or climate on uses more."]),
    (AWAKE_BARE, "Awake for no logged reason",
     ["Not addressed by the two lines",
      "above. That gap is the hole."]),
]

LEGEND = [
    (ASLEEP, "asleep"),
    (AWAKE_FEATURE, "awake + feature"),
    (AWAKE_BARE, "awake, no feature"),
]


def series(state_filter=None):
    """Rounded example series. Displayed rated miles are whole numbers, so the
    log is drawn as steps rather than a smooth curve."""
    xs, ys = [], []
    for state, t0, t1, m0, m1 in SEGMENTS:
        if state_filter is not None and state != state_filter:
            continue
        steps = int(round((t1 - t0) / SAMPLE_H))
        for k in range(steps + 1):
            t = t0 + k * SAMPLE_H
            frac = k / steps
            xs.append(t)
            ys.append(round(m0 + (m1 - m0) * frac))
    return xs, ys


def segment_drop(index: int) -> int:
    """Miles lost across one segment, read off the rounded example series."""
    state, t0, t1, m0, m1 = SEGMENTS[index]
    return int(round(m0) - round(m1))


def draw() -> str:
    fig = vs.new_figure()

    vs.example_badge(fig)
    vs.title_block(
        fig,
        "Overnight Court \u2014 the drop, and what covers it",
        "An example overnight rated-miles drop, with the state the example log says the car was in.",
        VEHICLE,
    )

    total_drop = int(round(SEGMENTS[0][3]) - round(SEGMENTS[-1][4]))
    hole_drop = segment_drop(2)

    # -------------------------------------------------------- night panel ----
    vs.card(fig, 0.035, 0.350, 0.63, 0.440)
    vs.card_heading(fig, 0.058, 0.752, "The night",
                    "example displayed rated miles, 10 pm to 7 am")

    ax = fig.add_axes([0.085, 0.505, 0.545, 0.185])
    ax.set_xlim(T_START, T_END)
    ax.set_ylim(245, 273)

    ax.axvspan(SEGMENTS[2][1], SEGMENTS[2][2], facecolor=vs.NOWHERE,
               alpha=0.10, zorder=0)
    for edge in (SEGMENTS[2][1], SEGMENTS[2][2]):
        ax.axvline(edge, color=vs.NOWHERE, lw=1.3, alpha=0.55,
                   linestyle=(0, (5, 4)), zorder=1)

    xs, ys = series()
    for i, (state, t0, t1, _m0, _m1) in enumerate(SEGMENTS):
        seg = [(x, y) for x, y in zip(xs, ys) if t0 <= x <= t1]
        ax.plot([p[0] for p in seg], [p[1] for p in seg], drawstyle="steps-post",
                color=STATE_COLOR[state], lw=3.2, zorder=4)
        drop = segment_drop(i)
        label = f"\u2212{drop} mi \u2014 the hole" if state == AWAKE_BARE else f"\u2212{drop} mi"
        ax.text((t0 + t1) / 2.0, 271.2, label, ha="center", va="center",
                fontsize=12, fontweight="bold", color=STATE_COLOR[state],
                zorder=5)

    ax.set_xticks([22, 24, 26, 28, 30, 31])
    ax.set_xticklabels([])
    ax.set_yticks([250, 255, 260, 265, 270])
    ax.tick_params(labelsize=vs.TICK)
    ax.set_ylabel("displayed rated miles", fontsize=13, labelpad=8)
    ax.grid(axis="y", color=vs.GRID, lw=0.9)
    ax.set_axisbelow(True)
    vs.strip_axes_spines(ax, keep=("left",))

    # state strip, sharing the same x range
    sx = fig.add_axes([0.085, 0.445, 0.545, 0.042])
    sx.set_xlim(T_START, T_END)
    sx.set_ylim(0, 1)
    for state, t0, t1, _m0, _m1 in SEGMENTS:
        sx.broken_barh([(t0, t1 - t0)], (0.08, 0.84),
                       facecolors=STATE_COLOR[state], alpha=0.9,
                       edgecolors=vs.CARD, linewidth=1.5, zorder=2)
    sx.set_xticks([22, 24, 26, 28, 30, 31])
    sx.set_xticklabels(["10 pm", "12 am", "2 am", "4 am", "6 am", "7 am"])
    sx.set_yticks([])
    sx.tick_params(axis="x", labelsize=vs.TICK, length=0, pad=6)
    vs.strip_axes_spines(sx)

    lx = fig.add_axes([0.085, 0.372, 0.545, 0.022])
    lx.set_xlim(0, 1)
    lx.set_ylim(0, 1)
    lx.set_axis_off()
    lx.text(0.0, 0.5, "the example log says:", ha="left", va="center",
            fontsize=11, color=vs.INK_FAINT, zorder=3)
    for i, (state, label) in enumerate(LEGEND):
        x0 = 0.30 + i * 0.24
        lx.scatter([x0], [0.5], s=110, marker="s", color=STATE_COLOR[state],
                   zorder=3)
        lx.text(x0 + 0.022, 0.5, label, ha="left", va="center", fontsize=11,
                color=vs.INK_SOFT, zorder=3)

    # ------------------------------------------------------ wording panel ----
    vs.card(fig, 0.680, 0.350, 0.285, 0.440)
    fig.text(0.700, 0.752, "The wording, paraphrased", ha="left", va="center",
             fontsize=15, fontweight="bold", color=vs.INK, zorder=6)
    fig.text(0.700, 0.716, "EXAMPLE paraphrase \u2014 not a quote", ha="left",
             va="center", fontsize=11, color=vs.MARKETING, zorder=6)

    for i, (state, heading, lines) in enumerate(PARAPHRASE):
        top = 0.665 - i * 0.110
        fig.text(0.700, top, "\u25cf", ha="left", va="center", fontsize=13,
                 color=STATE_COLOR[state], zorder=6)
        fig.text(0.716, top, heading, ha="left", va="center", fontsize=12,
                 fontweight="bold", color=STATE_COLOR[state], zorder=6)
        for j, line in enumerate(lines):
            fig.text(0.716, top - 0.034 - j * 0.030, line, ha="left",
                     va="center", fontsize=11, color=vs.INK_SOFT, zorder=6)

    # ---------------------------------------------------------- captions ----
    vs.caption_card(
        fig,
        0.035,
        0.050,
        0.60,
        0.280,
        f"Named mismatch hole (EXAMPLE): {HOLE_ID}",
        [
            f"In this example night, {hole_drop} of the {total_drop} lost miles land while the log",
            "says the car was awake with no feature named. The paraphrased",
            "wording covers sleep loss and feature-on loss \u2014 not this stretch.",
            "What would close it: a log field naming a feature that was on.",
            "What would harden it: the same shape on repeat example nights.",
        ],
        heading_color=vs.NOWHERE,
        head_size=16,
    )

    vs.caption_card(
        fig,
        0.655,
        0.050,
        0.310,
        0.280,
        "Read this first",
        [
            "A hole is a place where the log and",
            "the wording do not line up. That is",
            "all it is. It is not a verdict, not a",
            "method call, and it does not say the",
            "car is bad or that anyone lied. It is",
            "not buy, sell, sue, or repair advice.",
        ],
        size=12,
        head_size=16,
    )

    vs.footer(
        fig,
        "docs/viz/tesla_prototypes_2026-09-07/overnight_court.png  \u00b7  regenerate: python3 render_overnight_court.py",
        "EXAMPLE data \u00b7 not live car data",
    )

    fig.savefig(OUT, facecolor=vs.BG)
    return OUT


if __name__ == "__main__":
    print(draw())
