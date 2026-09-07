#!/usr/bin/env python3
"""Ill 1 — Shadow honesty strip (settle-joined refresh).

Renders ``shadow_honesty_strip.png`` from the real operating exports
``source/shadow/advises.jsonl`` (162 paper-observation rows, FedEx St. Jude ->
BMW -> TOUR Championship) and ``source/shadow/settle_join_summary.json``.

The earlier cut of this board drew every settlement column as PENDING because the
export genuinely had none. A real settle join has since landed, so the board now
reads the settle fields that actually exist: ``settle_status``, ``settle_source``,
``settled_at``. Nothing else. There is still no payout, stake-settled, closing-line,
CLV, or ROI column anywhere in the export, so no money or edge figure is drawn.

Denominator convention (founder Option A, Digestor digest is source of truth):

* 122 **settleable** advises -> 88 ``paper_lose`` / 34 ``paper_win``, nothing pending
  inside the denominator. There is no board-level SETTLE_PENDING badge.
* 2 BMW place advises are **excluded** as ``absent_from_official_field``: the player is
  not on the official STATUS_FINAL finisher list, so no finish exists to settle them
  against. Non-settleable, dropped from the pending denominator — not board
  SETTLE_PENDING, not wins, not losses, never defaulted.
* 38 round-leader in-play advises are ``never_settled`` by design. Honest nulls, not losses.

The paper hit rate is only ever drawn with an OBSERVATION / NOT EDGE ESTABLISHED /
NOT BANKED chip row attached to the figure itself.

Usage:
    python render_shadow_honesty.py
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np

import render_kit as kit

HERE = Path(__file__).resolve().parent
ADVISES = HERE / "source" / "shadow" / "advises.jsonl"
SUMMARY = HERE / "source" / "shadow" / "settle_join_summary.json"
OUT = HERE / "shadow_honesty_strip.png"

TOURNAMENT_ORDER = [
    "FedEx St. Jude Championship",
    "BMW Championship",
    "TOUR Championship",
]

MARKET_ORDER = ["win", "win_after_r1", "win_after_r2", "win_after_r3", "top_5", "top_10", "top_20"]

ACTION_ORDER = ["new_bet", "exit", "add", "reallocate", "reduce"]

# Markets whose result comes off the official final leaderboard. The round-leader
# markets are deliberately absent: they resolve intra-tournament and the operating
# system never settles them.
SETTLEABLE_MARKETS = {"win", "top_5", "top_10", "top_20"}
ROUND_LEADER_MARKETS = {"win_after_r1", "win_after_r2", "win_after_r3"}

# The only two values the export ever carries, and the only two it is allowed to.
ALLOWED_STATUS = {"paper_win", "paper_lose"}
ALLOWED_SOURCES = {"paper_ledger_ticket", "espn_official_final"}

# The 2 place advises excluded as absent_from_official_field: Keith Mitchell did not
# appear in the BMW Championship official final field, so there is no finish to settle
# against. Founder Option A adjudicates them never_settled / absent-from-field —
# non-settleable, dropped from the pending denominator, and never defaulted to a loss to
# make the board look finished. The staged export leaves their settle fields unset.
ABSENT_FIELD_TOKEN = "absent_from_official_field"
ABSENT_FIELD_KEYS = {
    ("401811963", "8906", "top_10"),
    ("401811963", "8906", "top_20"),
}

MARKET_COLOR = {
    "win": kit.ACCENT,
    "win_after_r1": "#8fd3f4",
    "win_after_r2": "#6aa9d8",
    "win_after_r3": "#4a7fb5",
    "top_5": kit.ACCENT_2,
    "top_10": "#f7c07a",
    "top_20": "#f9dcae",
}

# Categories, not profit and loss. Cyan/orange deliberately instead of green/red so a
# glance at the settle panel cannot be read as money made or money lost.
STATUS_COLOR = {"paper_win": kit.ACCENT, "paper_lose": kit.ACCENT_2}

# Columns a money or edge claim would need. None of them exist in the export, and none
# of them are being derived from the ones that do.
ABSENT_COLUMNS = [
    "payout",
    "realized_pnl",
    "closing_line",
    "clv",
    "roi",
    "stake_settled",
]

MONEY_FIELD_HINTS = ("payout", "pnl", "profit", "clv", "roi", "closing_line", "stake_settled", "bankroll")


def row_key(row: dict) -> tuple[str, str, str]:
    return (row["tournament_id"], row["player_id"], row["market"])


def load_rows() -> tuple[list[dict], dict]:
    with ADVISES.open() as fh:
        rows = [json.loads(line) for line in fh if line.strip()]
    summary = json.loads(SUMMARY.read_text())

    # ---- Honesty invariants. Each one guards a caption drawn on the board. ----

    # 1. Only the three real settle fields, and only the two allowed vocabularies.
    statuses = {r.get("settle_status") for r in rows} - {None}
    sources = {r.get("settle_source") for r in rows} - {None}
    assert statuses <= ALLOWED_STATUS, f"unexpected settle_status values: {sorted(statuses)}"
    assert sources <= ALLOWED_SOURCES, f"unexpected settle_source values: {sorted(sources)}"

    # 2. No money- or edge-shaped column has appeared. The board claims none exists.
    present = {k for r in rows for k in r}
    leaked = sorted(k for k in present if any(h in k.lower() for h in MONEY_FIELD_HINTS))
    assert not leaked, f"money/edge-shaped fields appeared in the export: {leaked}"

    # 3. No status without a source, and no source without a status: nothing invented.
    orphans = [r for r in rows if (r.get("settle_status") is None) != (r.get("settle_source") is None)]
    assert not orphans, f"{len(orphans)} rows carry a settle status/source without the other"

    # 4. Round-leader markets stay never_settled. Their nulls are by design, not losses.
    leader_settled = [r for r in rows if r["market"] in ROUND_LEADER_MARKETS and r.get("settle_status")]
    assert not leader_settled, f"{len(leader_settled)} round-leader rows got settled; they never should be"

    # 5. The settleable denominator is fully settled and the only rows outside it are
    #    the two adjudicated non-settleable place advises.
    unsettled = {row_key(r) for r in rows if r["market"] in SETTLEABLE_MARKETS and not r.get("settle_status")}
    assert unsettled == ABSENT_FIELD_KEYS, f"unexpected unsettled settleable rows: {sorted(unsettled)}"

    # 6. The staged join summary and the raw rows have to agree, or one of them is stale.
    counted = Counter(r.get("settle_status") for r in rows)
    assert summary["n"] == len(rows), f"summary n={summary['n']} but export has {len(rows)} rows"
    for key, expected in summary["settle_status_all"].items():
        got = counted[None if key == "null" else key]
        assert got == expected, f"summary settle_status_all[{key}]={expected} but export has {got}"

    return rows, summary


def buckets(rows: list[dict]) -> dict:
    """Split the 162 rows into the three mutually exclusive settle buckets."""
    excluded = [r for r in rows if row_key(r) in ABSENT_FIELD_KEYS]
    settled = [r for r in rows if r.get("settle_status")]
    never_settled = [r for r in rows if r["market"] in ROUND_LEADER_MARKETS]
    out = {
        "settled": settled,
        "excluded_absent_field": excluded,
        "never_settled": never_settled,
    }
    assert len(settled) + len(excluded) + len(never_settled) == len(rows), "buckets do not partition the export"
    return out


def hbar(ax, labels, values, colors, *, total, note=None, note_color=None, labelsize=None):
    y = np.arange(len(labels))[::-1]
    ax.barh(y, values, color=colors, height=0.62, zorder=3)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    if labelsize:
        ax.tick_params(axis="y", labelsize=labelsize)
    ax.set_xlim(0, max(values) * 1.30)
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
        # va="top" so a multi-line note always hangs below the panel; matplotlib
        # otherwise anchors the block at its bottom line and pushes the rest inside.
        ax.annotate(
            note,
            xy=(0, 0),
            xycoords="axes fraction",
            xytext=(0, -22),
            textcoords="offset points",
            va="top",
            fontsize=14,
            color=note_color or kit.DIM,
            linespacing=1.5,
        )


def chip_row(ax, x, y, items, *, fontsize=12, gap=0.016):
    """Lay chips left-to-right inside an axes, measuring each one as it is placed."""
    fig = ax.get_figure()
    for label, color in items:
        t = kit.chip(ax, x, y, label, color, fontsize=fontsize, pad=0.28)
        fig.canvas.draw()
        width = t.get_window_extent(renderer=fig.canvas.get_renderer()).width
        x += width / ax.get_window_extent().width + gap


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
        note="win / top_5 / top_10 / top_20 settle off the official final;\nwin_after_rN never settles",
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


def parse_ts(value: str) -> datetime:
    """Rows mix trailing Z with explicit offsets; normalise everything to UTC."""
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def draw_cadence(ax, rows):
    kit.panel(
        ax,
        "When the observations were written",
        "one dot per row, placed on its own timestamp · lanes are the three events",
    )
    lanes = {t: i for i, t in enumerate(reversed(TOURNAMENT_ORDER))}
    rng = np.random.default_rng(7)
    for market in MARKET_ORDER:
        pts = [r for r in rows if r["market"] == market]
        if not pts:
            continue
        ax.scatter(
            [parse_ts(r["timestamp"]) for r in pts],
            [lanes[r["tournament"]] + rng.uniform(-0.17, 0.17) for r in pts],
            s=110,
            alpha=0.8,
            color=MARKET_COLOR[market],
            edgecolors=kit.BG,
            linewidths=0.9,
            zorder=3,
        )
    ax.set_yticks(list(lanes.values()))
    ax.set_yticklabels(["TOUR Champ.", "BMW", "FedEx St. Jude"])
    ax.set_ylim(-0.6, len(lanes) - 0.4)
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    ax.grid(True, axis="x", alpha=0.5, zorder=1)
    ax.set_xlabel("observation timestamp (UTC)")
    ax.annotate(
        f"{len({r['run_id'] for r in rows})} runs over 17 days · clusters are tournament weeks, "
        "not a fixed schedule · gaps are weeks with nothing worth writing down",
        xy=(0, 0),
        xycoords="axes fraction",
        xytext=(0, -52),
        textcoords="offset points",
        va="top",
        fontsize=14,
        color=kit.DIM,
    )


def draw_actions(ax, rows):
    counts = Counter(r["action_kind"] for r in rows)
    order = [a for a in ACTION_ORDER if counts[a]]
    values = [counts[a] for a in order]
    kit.panel(ax, "Action kind mix", "what each row was advising")
    hbar(
        ax,
        order,
        values,
        [kit.ACCENT if a == "new_bet" else kit.PENDING if a == "exit" else kit.ACCENT_3 for a in order],
        total=len(rows),
        note="an 'exit' is an advised exit from a paper position that was\n"
        "never placed — settling it on paper realised nothing",
    )


def draw_settle_mix(ax, rows):
    settled = [r for r in rows if r.get("settle_status")]
    counts = Counter(r["settle_status"] for r in settled)
    order = ["paper_lose", "paper_win"]
    n = len(settled)
    hit = counts["paper_win"] / n
    kit.panel(
        ax,
        f"Settle mix — the settleable {n}",
        "real settle_status only · paper outcomes of tickets that were never placed",
    )
    hbar(
        ax,
        order,
        [counts[s] for s in order],
        [STATUS_COLOR[s] for s in order],
        total=n,
        note=f"{n}/{n} settleable advises carry a real settle_status · 0 pending inside\n"
        "the denominator · colours are categories, not profit and loss",
        note_color=kit.MUTED,
    )
    # Room under the bars for the hit rate, so the figure never appears without the
    # chips that qualify it.
    ax.set_ylim(-2.05, 1.5)
    ax.text(
        0.022,
        0.235,
        f"paper hit rate  {counts['paper_win']}/{n} ≈ {hit:.3f}",
        transform=ax.transAxes,
        va="center",
        fontsize=19,
        color=kit.TEXT,
        fontweight="bold",
    )
    chip_row(
        ax,
        0.022,
        0.10,
        [
            ("OBSERVATION", kit.WALL),
            ("NOT EDGE ESTABLISHED", kit.WARN),
            ("NOT BANKED", kit.WARN),
        ],
        fontsize=11,
        gap=0.014,
    )


def draw_settle_sources(ax, rows):
    counts = Counter(r.get("settle_source") for r in rows)
    order = ["espn_official_final", "paper_ledger_ticket"]
    values = [counts[s] for s in order]
    dated = sum(1 for r in rows if r.get("settled_at"))
    kit.panel(
        ax,
        "Where the settle came from",
        "two sources, both real records · nothing inferred, nothing modelled",
    )
    hbar(
        ax,
        ["espn_official\n_final", "paper_ledger\n_ticket"],
        values,
        [kit.WALL, kit.ACCENT_3],
        total=sum(values),
        note=f"{sum(values)} settled rows · {dated} carry an explicit settled_at\n"
        "(the paper-ledger tickets); the ESPN-final rows carry\nthe source, not a stamp",
        labelsize=14,
    )


def draw_out_of_denominator(ax, rows):
    leader = Counter(r["market"] for r in rows if r["market"] in ROUND_LEADER_MARKETS)
    labels = ["win_after_r1", "win_after_r2", "win_after_r3", "absent_from\n_official_field"]
    values = [leader["win_after_r1"], leader["win_after_r2"], leader["win_after_r3"], len(ABSENT_FIELD_KEYS)]
    kit.panel(
        ax,
        "Outside the settle denominator",
        "rows with no settle_status, and the honest reason each one has none",
    )
    hbar(
        ax,
        labels,
        values,
        [MARKET_COLOR["win_after_r1"], MARKET_COLOR["win_after_r2"], MARKET_COLOR["win_after_r3"], kit.PENDING],
        total=sum(values),
        note=f"{sum(values) - len(ABSENT_FIELD_KEYS)} round-leader rows are never_settled by design;\n"
        f"the {len(ABSENT_FIELD_KEYS)} excluded rows are the BMW top_10 + top_20 place\n"
        "advises, absent from the official final field ·\n"
        "none of these is a loss and none is counted",
        labelsize=14,
    )


def draw_residual(ax):
    kit.text_panel(
        ax,
        f"Residual: 2 advises excluded as {ABSENT_FIELD_TOKEN}, outside the denominator",
        "non-settleable — not board SETTLE_PENDING, not a win, not a loss, not invented",
    )
    ax.text(
        0.030,
        0.855,
        "Keith Mitchell · BMW Championship (401811963) · 2026-08-17 · both action_kind=new_bet",
        transform=ax.transAxes,
        va="center",
        fontsize=19,
        color=kit.TEXT,
        fontweight="bold",
    )
    entries = [
        ("top_10", "rec-2853b9e721", "posted 10.0 · model p 0.149"),
        ("top_20", "rec-9643405947", "posted 10.0 · model p 0.301"),
    ]
    for i, (market, rec, detail) in enumerate(entries):
        y = 0.700 - i * 0.145
        kit.chip(ax, 0.030, y, "EXCLUDED", kit.PENDING, fontsize=15, pad=0.32)
        ax.text(
            0.160,
            y,
            f"{market:<7}  {rec}",
            transform=ax.transAxes,
            va="center",
            fontsize=18,
            color=kit.TEXT,
            family="DejaVu Sans Mono",
        )
        ax.text(
            0.470,
            y,
            f"{ABSENT_FIELD_TOKEN} · {detail}",
            transform=ax.transAxes,
            va="center",
            fontsize=17,
            color=kit.MUTED,
        )
    ax.text(
        0.030,
        0.435,
        "Keith Mitchell is not on the BMW official final field, so no place finish exists to settle these two\n"
        "against. Founder Option A adjudicates them never_settled / absent_from_official_field — non-settleable,\n"
        "so they are dropped from the pending denominator and held outside the settleable 122. They are not\n"
        "board SETTLE_PENDING, and never defaulted to a loss: the staged export leaves them unset.",
        transform=ax.transAxes,
        va="top",
        fontsize=17,
        color=kit.PENDING,
        linespacing=1.55,
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
        f"{missing} exit rows carry no posted price and are excluded from this panel · spread is a disagreement in\n"
        "stated probability, NOT an established edge · the settle join does not turn it into one",
        xy=(0, 0),
        xycoords="axes fraction",
        xytext=(0, -52),
        textcoords="offset points",
        va="top",
        fontsize=14,
        color=kit.DIM,
    )


def draw_gap(ax, rows):
    settled = sum(1 for r in rows if r.get("settle_status"))
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
        f"bars are not split by settle_status — {settled} paper outcomes\nare too few to calibrate this, and it is not attempted",
        xy=(0, 0),
        xycoords="axes fraction",
        xytext=(0, -56),
        textcoords="offset points",
        va="top",
        fontsize=14,
        color=kit.DIM,
        linespacing=1.5,
    )


def draw_walls(ax, rows):
    n = len(rows)
    settled = [r for r in rows if r.get("settle_status")]
    kit.text_panel(
        ax,
        "Honesty walls held on every row",
        "field-by-field check against the export, not a claim about intent",
    )
    walls = [
        ("paper_observation_only = true", sum(1 for r in rows if r["paper_observation_only"] is True), n),
        ("never_auto_bet = true", sum(1 for r in rows if r["never_auto_bet"] is True), n),
        ("run_mode = live (real book, paper record)", sum(1 for r in rows if r["run_mode"] == "live"), n),
        ("uncertainty interval present (model_p_low/high)", sum(1 for r in rows if r.get("model_p_low") is not None), n),
        (
            "settle_status ∈ {paper_win, paper_lose} only",
            sum(1 for r in settled if r["settle_status"] in ALLOWED_STATUS),
            len(settled),
        ),
        (
            "settle_source ∈ {paper_ledger_ticket, espn_official_final}",
            sum(1 for r in settled if r["settle_source"] in ALLOWED_SOURCES),
            len(settled),
        ),
        (
            "excluded absent-from-field rows left unset, never defaulted to a loss",
            sum(1 for r in rows if row_key(r) in ABSENT_FIELD_KEYS and r.get("settle_status") is None),
            len(ABSENT_FIELD_KEYS),
        ),
        ("no payout / pnl / clv / roi / stake_settled column exists", n, n),
    ]
    for i, (label, count, denom) in enumerate(walls):
        y = 0.915 - i * 0.116
        held = count == denom
        kit.chip(ax, 0.028, y, f"{count}/{denom}", kit.WALL if held else kit.WARN, fontsize=16)
        ax.text(
            0.185,
            y,
            label,
            transform=ax.transAxes,
            va="center",
            fontsize=18,
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


def draw_columns(ax, rows):
    settled = sum(1 for r in rows if r.get("settle_status"))
    dated = sum(1 for r in rows if r.get("settled_at"))
    kit.text_panel(
        ax,
        "What the join delivered — and what is still not in the export",
        "the settle fields are read as-is; the money and edge columns remain absent, not zero",
    )
    state_color = {"JOINED": kit.WALL, "PARTIAL": kit.PENDING, "EXCLUDED": kit.PENDING}
    joined = [
        (f"settle_status ({settled}/{len(rows)})", "JOINED"),
        (f"settle_source ({settled}/{len(rows)})", "JOINED"),
        (f"settled_at ({dated}/{len(rows)})", "PARTIAL"),
        (f"unset ({len(ABSENT_FIELD_KEYS)}/{len(rows)})", "EXCLUDED"),
    ]
    for i, (name, state) in enumerate(joined):
        y = 0.900 - i * 0.165
        kit.chip(ax, 0.028, y, state, state_color[state], fontsize=14, pad=0.3)
        ax.text(
            0.150,
            y,
            name,
            transform=ax.transAxes,
            va="center",
            fontsize=16,
            color=kit.TEXT,
            family="DejaVu Sans Mono",
        )
    for i, name in enumerate(ABSENT_COLUMNS):
        col = 0.455 if i < 3 else 0.725
        y = 0.900 - (i % 3) * 0.165
        kit.chip(ax, col, y, "ABSENT", kit.WARN, fontsize=14, pad=0.3)
        ax.text(
            col + 0.095,
            y,
            name,
            transform=ax.transAxes,
            va="center",
            fontsize=16,
            color=kit.TEXT,
            family="DejaVu Sans Mono",
        )
    ax.text(
        0.028,
        0.285,
        "So: a paper win/lose count exists and is shown, and 2 absent-from-field rows stay unset and excluded.\n"
        "Payout, PnL, ROI, CLV, and closing line do not exist and are not derived from it.",
        transform=ax.transAxes,
        va="top",
        fontsize=16,
        color=kit.PENDING,
        fontweight="bold",
        linespacing=1.5,
    )


def draw_plain_english(ax, rows):
    settled = [r for r in rows if r.get("settle_status")]
    wins = sum(1 for r in settled if r["settle_status"] == "paper_win")
    kit.text_panel(ax, "In plain English", None)
    lines = [
        ("These are observations of a live sportsbook,", kit.TEXT),
        ("written down on paper. No money moved.", kit.TEXT),
        ("", kit.TEXT),
        ("The paper outcomes are now joined:", kit.TEXT),
        (f"{wins} paper wins, {len(settled) - wins} paper losses, of {len(settled)}.", kit.TEXT),
        ("Two are excluded: not on the final field.", kit.TEXT),
        ("", kit.TEXT),
        ("That is a record of what would have", kit.PENDING),
        ("happened to tickets nobody bought.", kit.PENDING),
        ("Not banked money. Not a track record.", kit.PENDING),
        ("Not a Kalshi demo or mock feed —", kit.PENDING),
        ("this is the real operating export.", kit.PENDING),
        ("", kit.TEXT),
        ("Nothing here says an edge exists.", kit.WARN),
        ("Nothing here is buy or sell advice.", kit.WARN),
    ]
    for i, (line, color) in enumerate(lines):
        ax.text(
            0.045,
            0.945 - i * 0.0655,
            line,
            transform=ax.transAxes,
            va="center",
            fontsize=18,
            color=color,
            fontweight="bold" if color != kit.TEXT else "normal",
        )


def main() -> None:
    kit.apply_style()
    rows, summary = load_rows()
    parts = buckets(rows)
    settled = parts["settled"]
    wins = sum(1 for r in settled if r["settle_status"] == "paper_win")

    height = 37.5
    fig = plt.figure(figsize=(24, height))
    banner_top = kit.HEADER_BLOCK_IN
    banner_h = 2.02
    gs = fig.add_gridspec(
        7,
        3,
        left=0.082,
        right=0.985,
        top=1.0 - (banner_top + banner_h + 1.05) / height,
        bottom=3.72 / height,
        hspace=1.10,
        wspace=0.38,
        height_ratios=[1.0, 1.05, 1.30, 1.05, 1.20, 1.05, 1.15],
    )

    kit.header(
        fig,
        "GOLF-OFFSHOOT DRY RUN · ILL 1 OF 2 · 2026-09-07 · SETTLE-JOINED REFRESH",
        "Shadow honesty strip",
        f"{len(rows)} paper-observation rows from the real operating shadow export, now with a real settle join. "
        "Live book, paper record, no cash in or out.",
    )
    kit.banner(
        fig,
        banner_top,
        banner_h,
        f"SETTLE JOIN COMPLETE ON THE SETTLEABLE {len(settled)} — {wins} paper_win · {len(settled) - wins} paper_lose · "
        "0 pending inside the denominator",
        f"Denominator is {len(settled)} settleable advises. {len(parts['excluded_absent_field'])} BMW place advises are excluded as "
        f"{ABSENT_FIELD_TOKEN} (Keith Mitchell is not on the official final field),\n"
        f"and {len(parts['never_settled'])} round-leader in-play advises are never_settled by design. All "
        f"{len(parts['excluded_absent_field']) + len(parts['never_settled'])} are held outside the denominator, never defaulted to a loss.\n"
        f"Paper hit rate {wins}/{len(settled)} ≈ {wins / len(settled):.3f} is an OBSERVATION of unplaced paper tickets: "
        "NOT an edge, NOT ROI, NOT banked money.",
    )

    draw_coverage(fig.add_subplot(gs[0, 0]), rows)
    draw_markets(fig.add_subplot(gs[0, 1]), rows)
    draw_modes(fig.add_subplot(gs[0, 2]), rows)

    draw_cadence(fig.add_subplot(gs[1, 0:2]), rows)
    draw_actions(fig.add_subplot(gs[1, 2]), rows)

    draw_spread(fig.add_subplot(gs[2, 0:2]), rows)
    draw_gap(fig.add_subplot(gs[2, 2]), rows)

    draw_settle_mix(fig.add_subplot(gs[3, 0]), rows)
    draw_settle_sources(fig.add_subplot(gs[3, 1]), rows)
    draw_out_of_denominator(fig.add_subplot(gs[3, 2]), rows)

    draw_residual(fig.add_subplot(gs[4, 0:2]))
    draw_plain_english(fig.add_subplot(gs[4:7, 2]), rows)

    draw_walls(fig.add_subplot(gs[5, 0:2]), rows)
    draw_columns(fig.add_subplot(gs[6, 0:2]), rows)

    kit.badge_strip(
        fig,
        y_in=2.74,
        extra=[
            ("NOT EDGE ESTABLISHED", kit.WARN),
            ("NOT BANKED MONEY", kit.WARN),
            ("SETTLE SOURCES: paper_ledger_ticket + espn_official_final", kit.ACCENT_3),
        ],
    )
    kit.footer(
        fig,
        [
            "Source: docs/viz/golf_offshoot_dryrun_2026-09-07/source/shadow/advises.jsonl "
            f"({len(rows)} rows, run_mode=live, paper_observation_only=true, never_auto_bet=true)",
            "+ source/shadow/settle_join_summary.json. Both staged exports are unmodified. Settle fields are read "
            "as-is: settle_status ∈ {paper_win, paper_lose},",
            "settle_source ∈ {paper_ledger_ticket, espn_official_final}. The summary's overall null count of "
            f"{summary['settle_status_all']['null']} is {len(parts['never_settled'])} never_settled round-leader rows",
            f"plus the {len(parts['excluded_absent_field'])} absent-from-field place advises. The staged summary predates founder "
            "Option A: it records SETTLE_PENDING_cleared=false against its own",
            f"{summary['relevant_n']}-row relevant denominator, which still counts those "
            f"{len(parts['excluded_absent_field'])} rows. Option A excludes {ABSENT_FIELD_TOKEN} rows from that denominator, leaving",
            f"the {len(settled)}-row settleable denominator, which is fully joined — so no board-level SETTLE_PENDING is claimed "
            "and neither row is defaulted to a loss.",
            "Rendered by render_shadow_honesty.py. No payout, PnL, ROI, CLV, closing-line, edge-established, or "
            "buy/sell figure is derived or implied from the paper win/lose counts.",
        ],
        y_in=2.35,
    )

    w, h = kit.save(fig, OUT)
    print(
        f"wrote {OUT} ({w}x{h}px) from {len(rows)} rows · "
        f"settleable {len(settled)} ({wins} paper_win / {len(settled) - wins} paper_lose, 0 pending inside) · "
        f"held outside: {len(parts['excluded_absent_field'])} excluded {ABSENT_FIELD_TOKEN} "
        f"+ {len(parts['never_settled'])} never_settled"
    )


if __name__ == "__main__":
    main()
