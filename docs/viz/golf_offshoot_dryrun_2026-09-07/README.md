# Golf-offshoot dry run — Ill 1 + Ill 2 (2026-09-07)

Two illustrator boards rendered from **real operating exports** of the golf-offshoot
system. Not demo data, not mock feeds, not a Kalshi sandbox. The exports themselves
are checked in under [`source/`](source/) so every number on the boards can be
recomputed from this directory alone.

**Shared badges on both boards:**
`PHASE 1 OBSERVATION` · `AI: NO CASH IN/OUT` · `SOURCE: real operating exports (not demo)` · `paper observation only`

---

## Ill 1 — Shadow honesty strip

![Shadow honesty strip](shadow_honesty_strip.png)

`shadow_honesty_strip.png` (2640 × 2090 px) · rendered by
[`render_shadow_honesty.py`](render_shadow_honesty.py) from
[`source/shadow/advises.jsonl`](source/shadow/advises.jsonl).

**Honesty caption.** 162 paper-observation rows written against a **live** sportsbook
across three FedExCup playoff events (FedEx St. Jude → BMW → TOUR Championship,
2026-08-13 → 2026-08-30). Every row carries `run_mode=live`,
`paper_observation_only=true`, and `never_auto_bet=true`. "Live" describes the book
the prices came from, not money at risk: nothing was staked, so there is nothing to
settle. The advisory posture was `stay_selective` on 158 of 162 rows.

**Settlement columns are PENDING / join later.** `advises.jsonl` has no settle,
outcome, or PnL field of any kind — no `settled_at`, `outcome`, `won/lost`, `payout`,
`realized_pnl`, `closing_line`, `clv`, or `roi`. The board draws each of those as an
explicit `PENDING / join later` badge rather than leaving a blank a reader could
mistake for zero. Any hit rate, ROI, CLV, or profit figure for this window would have
to be invented, so none is shown.

**On the model-vs-market panel.** The scatter and the signed-gap histogram show where
the model's stated probability sat relative to the probability implied by the posted
decimal odds. That is a **disagreement between two stated numbers**, nothing more. It
is not a measured edge, not a validated edge, and not a reason to act. 12 exit rows
carry no posted price and are excluded from those two panels; they are still counted
everywhere else.

## Ill 2 — Calibration weather

![Calibration weather](calibration_weather.png)

`calibration_weather.png` (2640 × 2200 px) · rendered by
[`render_calibration_weather.py`](render_calibration_weather.py) from
[`source/calibration/weights_calib-v1.json`](source/calibration/weights_calib-v1.json),
[`v2`](source/calibration/weights_calib-v2.json), and
[`v3`](source/calibration/weights_calib-v3.json).

**Honesty caption.** Three successive calibration freezes — `calib-v1` (8 train
events), `calib-v2` (8), `calib-v3` (12, latest) — and all three landed on the same
recommendation: **`keep_expert`**. All three record `no_future_leakage=true`, and the
hold-out events were never used to accept a candidate weight vector.

**The hold-out did not clearly beat expert α.** That sentence is quoted from the
exports' own notes, and the score panels show why. Expert and fitted Brier scores sit
on top of each other in every market. On hold-out Brier, the fitted vector moves the
score by less than half a percent in either direction and **flips sign by market**
(`top_20` −0.32%, `top_5` +0.37%, `win` −0.30%, `top_10` −0.09%, `make_cut` ≈0%). Log
loss behaves the same way. Mixed signs at that magnitude are not a consistent gain, so
the fitted vector is stored for comparison only and expert α stays in production.

The "where the fit wanted to move" panel shows the 11 searched weights, expert value
vs fitted value. It is included to make the shelved candidate inspectable, not to
suggest those movements are discoveries. Per v3's own ARD notes, most of those keys had
near-zero leave-one-out relevance.

---

## What this is *not*

- **Not settled bets.** No position was ever placed, so nothing won, lost, or paid.
- **Not a track record.** No hit rate, ROI, CLV, PnL, or profitability claim is made or
  derivable from these files.
- **Not an edge claim.** Neither board asserts an edge exists, is established, or has
  been validated. The model/market spread on Ill 1 is a disagreement between two stated
  probabilities; the calibration deltas on Ill 2 are a search result that did not beat
  the expert prior.
- **Not advice.** Nothing here is a buy, sell, back, lay, or stake recommendation.
- **Not demo or mock data.** These are the real operating exports. The offshoot's
  `demo` / `explain` / `strategy` commands print an `OFFLINE DEMO — MOCK DATA` banner
  and are *not* the source here.
- **Not a forward-performance statement.** Historical calibration scores say nothing
  about future events.
- **Not part of the core method.** The golf offshoot sits beside Gated Progressive
  Formalization; it does not score, lock, or mutate anything under `applications/`.

## Re-rendering

```bash
cd docs/viz/golf_offshoot_dryrun_2026-09-07
pip install matplotlib          # only dependency beyond the stdlib
python render_shadow_honesty.py
python render_calibration_weather.py
```

Both scripts read only from `source/`, print the pixel dimensions they wrote, and
assert the honesty invariants they depend on (all three calibration freezes must still
read `keep_expert`; the v3 hold-out note must still begin "Hold-out did not clearly
beat expert"). If an export is ever replaced with one that contradicts a caption, the
render fails instead of quietly redrawing a false claim.

Shared style and the badge strip live in [`render_kit.py`](render_kit.py), so both
boards carry byte-identical badges.
