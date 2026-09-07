#!/usr/bin/env python3
"""Ill 2 — Calibration weather.

Renders ``calibration_weather.png`` from the real operating exports
``source/calibration/weights_calib-v{1,2,3}.json``.

The story the files actually tell: three successive calibration freezes all
landed on the same decision, ``keep_expert``. The fitted weight vector is
stored for comparison only. Train and hold-out scores for expert vs fitted are
close enough, and mixed enough in sign, that the hold-out did not clearly beat
the expert alpha. The board says exactly that and no more.

Usage:
    python render_calibration_weather.py
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import render_kit as kit

HERE = Path(__file__).resolve().parent
CALIB_DIR = HERE / "source" / "calibration"
OUT = HERE / "calibration_weather.png"

VERSIONS = ["v1", "v2", "v3"]
MARKETS = ["make_cut", "top_20", "top_10", "top_5", "win"]

SERIES = [
    ("train_expert", "train · expert α", kit.ACCENT),
    ("train_fitted", "train · fitted α", "#2b6f8f"),
    ("holdout_expert", "hold-out · expert α", kit.ACCENT_2),
    ("holdout_fitted", "hold-out · fitted α", "#9c6127"),
]


def load() -> dict[str, dict]:
    return {v: json.loads((CALIB_DIR / f"weights_calib-{v}.json").read_text()) for v in VERSIONS}


def draw_freeze_card(ax, tag: str, data: dict, *, latest: bool) -> None:
    arrow = "" if latest else "   →"
    title = f"FREEZE {tag}{arrow}" + ("   (latest)" if latest else "")
    kit.text_panel(ax, title, data["version_id"])

    created = data["created_at"][:16].replace("T", "  ")
    facts = [
        ("frozen", f"{created} UTC"),
        ("train events", f"{len(data['train_event_ids'])}  ({data['metrics']['train_expert']['n']} player-rows)"),
        ("hold-out events", f"{len(data['holdout_event_ids'])}  ({data['metrics']['holdout_expert']['n']} player-rows)"),
        ("search evals", str(data["n_evals"])),
        ("no_future_leakage", str(data["no_future_leakage"]).lower()),
    ]
    for i, (label, value) in enumerate(facts):
        y = 0.78 - i * 0.135
        ax.text(0.045, y, label, transform=ax.transAxes, va="center", fontsize=16, color=kit.MUTED)
        ax.text(
            0.44,
            y,
            value,
            transform=ax.transAxes,
            va="center",
            fontsize=16,
            color=kit.TEXT,
            fontweight="bold",
        )

    kit.chip(
        ax,
        0.045,
        0.075,
        f"DECISION: {data['recommendation'].upper()}",
        kit.GOOD,
        fontsize=19,
        pad=0.4,
    )


def draw_brier(ax, v3: dict) -> None:
    kit.panel(
        ax,
        "Brier score by market — expert α vs fitted α, train vs hold-out (calib-v3)",
        "lower is better; bars are close enough that no pair separates by eye",
    )
    x = np.arange(len(MARKETS))
    width = 0.2
    for i, (key, label, color) in enumerate(SERIES):
        vals = [v3["metrics"][key]["brier"][m] for m in MARKETS]
        offset = (i - 1.5) * width
        bars = ax.bar(x + offset, vals, width * 0.92, label=label, color=color, zorder=3)
        for b, val in zip(bars, vals):
            ax.annotate(
                f"{val:.4f}",
                xy=(b.get_x() + b.get_width() / 2, val),
                xytext=(0, 6),
                textcoords="offset points",
                ha="center",
                fontsize=12,
                color=kit.MUTED,
                rotation=90,
            )
    ax.set_xticks(x)
    ax.set_xticklabels(MARKETS)
    ax.set_ylabel("Brier score")
    ax.set_ylim(0, 0.29)
    ax.grid(True, axis="y", alpha=0.5, zorder=1)
    ax.legend(loc="upper right", ncol=2, labelcolor=kit.TEXT, fontsize=16)
    ax.annotate(
        "Hold-out events were never used to accept a candidate weight vector. "
        "The fitted vector is stored for comparison only; production keeps expert α.",
        xy=(0, 0),
        xycoords="axes fraction",
        xytext=(0, -58),
        textcoords="offset points",
        fontsize=14,
        color=kit.DIM,
    )


def draw_delta(ax, v3: dict, metric: str, title: str) -> None:
    kit.panel(ax, title, "fitted minus expert, % of expert score · left of zero = fitted better")
    y = np.arange(len(MARKETS))[::-1]
    width = 0.36
    for i, split in enumerate(("train", "holdout")):
        rel = []
        for m in MARKETS:
            e = v3["metrics"][f"{split}_expert"][metric][m]
            f = v3["metrics"][f"{split}_fitted"][metric][m]
            rel.append(100.0 * (f - e) / e)
        color = kit.ACCENT if split == "train" else kit.ACCENT_2
        offset = width / 2 if split == "train" else -width / 2
        ax.barh(
            y + offset,
            rel,
            width * 0.9,
            color=color,
            label="train" if split == "train" else "hold-out",
            zorder=3,
        )
        for yi, val in zip(y + offset, rel):
            ax.annotate(
                f"{val:+.2f}%" if abs(val) >= 0.01 else "\u22480%",
                xy=(val, yi),
                xytext=(7 if val >= 0 else -7, 0),
                textcoords="offset points",
                ha="left" if val >= 0 else "right",
                va="center",
                fontsize=13,
                color=kit.TEXT,
            )
    ax.axvline(0, color=kit.TEXT, lw=2.0, zorder=4)
    ax.set_yticks(y)
    ax.set_yticklabels(MARKETS)
    lim = 6.6 if metric == "logloss" else 0.85
    ax.set_xlim(-lim, lim)
    ax.set_xlabel(f"relative change in {metric} (%)")
    ax.grid(True, axis="x", alpha=0.5, zorder=1)
    ax.legend(loc="lower right", labelcolor=kit.TEXT, fontsize=15)
    ax.annotate(
        "signs disagree across markets — not a consistent gain",
        xy=(0, 0),
        xycoords="axes fraction",
        xytext=(0, -74),
        textcoords="offset points",
        fontsize=14,
        color=kit.DIM,
    )


def draw_footprint(ax, v3: dict) -> None:
    keys = v3["extra"]["fitted_keys"]
    expert = v3["expert_alpha"]
    fitted = v3["calibrated_alpha"]
    keys = sorted(keys, key=lambda k: abs(fitted[k] - expert[k]), reverse=True)

    kit.panel(
        ax,
        "Where the fit wanted to move",
        "the 11 searched weights · shelved, NOT in production",
    )
    y = np.arange(len(keys))[::-1]
    for yi, k in zip(y, keys):
        e, f = expert[k], fitted[k]
        ax.plot([e, f], [yi, yi], color=kit.PANEL_EDGE, lw=3.0, zorder=2)
    ax.scatter([expert[k] for k in keys], y, s=150, color=kit.ACCENT, label="expert α", zorder=3)
    ax.scatter(
        [fitted[k] for k in keys],
        y,
        s=150,
        color=kit.ACCENT_3,
        label="fitted α (shelved)",
        zorder=3,
    )
    ax.set_yticks(y)
    ax.set_yticklabels([k.replace("comparable_player_borrow", "cmp_player_borrow") for k in keys], fontsize=13)
    ax.set_xlim(-0.03, 0.56)
    ax.set_xlabel("weight")
    ax.grid(True, axis="x", alpha=0.5, zorder=1)
    ax.legend(loc="lower right", labelcolor=kit.TEXT, fontsize=15)
    ax.annotate(
        "movement is a search artefact, not a discovered truth",
        xy=(0, 0),
        xycoords="axes fraction",
        xytext=(0, -74),
        textcoords="offset points",
        fontsize=14,
        color=kit.DIM,
    )


def draw_verdict(ax, calib: dict) -> None:
    v3 = calib["v3"]
    quote = v3["notes"][-1]
    assert quote.startswith("Hold-out did not clearly beat expert"), "v3 note text changed"

    kit.text_panel(ax, "The honest read", "quoted from the export's own notes")
    kit.chip(ax, 0.045, 0.90, "3 of 3 freezes: KEEP_EXPERT", kit.GOOD, fontsize=18, pad=0.4)

    # One uniform ladder of lines so the quote can never collide with the read.
    lines = [
        ("\u201cHold-out did not clearly beat expert α;", kit.TEXT, "italic"),
        ("default recommendation is to keep expert", kit.TEXT, "italic"),
        ("weights in production and store the fitted", kit.TEXT, "italic"),
        ("vector for comparison.\u201d", kit.TEXT, "italic"),
        ("", kit.TEXT, "normal"),
        ("No version was promoted to fitted weights.", kit.GOOD, "normal"),
        ("", kit.TEXT, "normal"),
        ("Every hold-out Brier gap below is under", kit.PENDING, "normal"),
        ("half a percent, and flips sign by market.", kit.PENDING, "normal"),
        ("", kit.TEXT, "normal"),
        ("That is not evidence of an edge. It is", kit.WARN, "normal"),
        ("evidence the search found nothing worth", kit.WARN, "normal"),
        ("shipping. Expert α stays in production.", kit.WARN, "normal"),
    ]
    for i, (line, color, style) in enumerate(lines):
        ax.text(
            0.045,
            0.755 - i * 0.058,
            line,
            transform=ax.transAxes,
            va="center",
            fontsize=15,
            color=color,
            style=style,
            fontweight="normal" if style == "italic" else "bold",
        )


def main() -> None:
    kit.apply_style()
    calib = load()
    v3 = calib["v3"]

    recs = {v: calib[v]["recommendation"] for v in VERSIONS}
    assert set(recs.values()) == {"keep_expert"}, f"unexpected recommendations: {recs}"

    height = 20.0
    fig = plt.figure(figsize=(24, height))
    gs = fig.add_gridspec(
        3,
        3,
        left=0.068,
        right=0.985,
        top=1.0 - kit.HEADER_BLOCK_IN / height,
        # row 3 hangs a note ~1.25in below its axes, so the footer block needs clearance
        bottom=(kit.FOOTER_BLOCK_IN + 1.25) / height,
        hspace=0.62,
        wspace=0.34,
        height_ratios=[1.02, 1.30, 1.06],
    )

    kit.header(
        fig,
        "GOLF-OFFSHOOT DRY RUN · ILL 2 OF 2 · 2026-09-07",
        "Calibration weather",
        "Three real calibration freezes, one unchanged decision. Leakage-safe train/hold-out split; "
        "hold-out never used to accept a candidate.",
    )

    for i, v in enumerate(VERSIONS):
        draw_freeze_card(fig.add_subplot(gs[0, i]), f"calib-{v}", calib[v], latest=(v == "v3"))

    draw_brier(fig.add_subplot(gs[1, 0:2]), v3)
    draw_verdict(fig.add_subplot(gs[1, 2]), calib)

    draw_delta(fig.add_subplot(gs[2, 0]), v3, "brier", "Brier: how much did fitting help?")
    draw_delta(fig.add_subplot(gs[2, 1]), v3, "logloss", "Log loss: same question")
    draw_footprint(fig.add_subplot(gs[2, 2]), v3)

    kit.badge_strip(fig)
    kit.footer(
        fig,
        [
            "Source: docs/viz/golf_offshoot_dryrun_2026-09-07/source/calibration/weights_calib-v{1,2,3}.json "
            "(all three: recommendation=keep_expert, no_future_leakage=true).",
            "Rendered by render_calibration_weather.py. Scores are read straight from each export's "
            "metrics block; no edge, profitability, or forward-performance claim is made.",
        ],
    )

    w, h = kit.save(fig, OUT)
    print(f"wrote {OUT} ({w}x{h}px) · freezes {recs}")


if __name__ == "__main__":
    main()
