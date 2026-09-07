# Calibration weather — golf-offshoot (Illustrator chart #2)

**Date:** 2026-09-07
**Lane:** golf-offshoot dry-run viz · **Phase 1 observation only**
**Source (real, already in repo):** [`golf-offshoot/data/calibration/weights_calib-v3.json`](../../../golf-offshoot/data/calibration/weights_calib-v3.json)
**Artifact:** `golf-offshoot-0.7.0-calib-v3`, frozen `2026-08-13`
**Deliverables:** [`calibration_weather.png`](calibration_weather.png) · [`render_calibration_weather.py`](render_calibration_weather.py)

![Calibration weather](calibration_weather.png)

---

## Honesty caption (read this before the chart)

**Observation, not edge.** The chart compares two sets of factor weights on the same golf events: the
hand-set **expert** weights that production actually uses, and a **calibrated** vector produced by
Bayesian search. On the three held-out events the calibrated vector wins some market buckets by a
hair and loses others by a hair. That is noise, not a demonstrated edge.

The artifact's own frozen recommendation is **`keep_expert`**. The chart surfaces that verdict as-is.
It does **not** argue for the calibrated vector, and it does **not** claim any edge is established.

Quoted from the artifact's `notes`:

> Hold-out did not clearly beat expert α; default recommendation is to keep expert weights in
> production and store the fitted vector for comparison.

Badges carried on the chart: `PHASE 1 OBSERVATION` · `AI: NO CASH IN / NO CASH OUT` ·
`SOURCE: weights_calib-v3.json` · `NOT Softened` · `NOT LIVE bets`.

---

## What the four panels show

| Panel | What it shows | How to read it |
|---|---|---|
| Held-out Brier by market bucket | Expert vs calibrated Brier on the 3 held-out events (n = 438 player-starts) | Lower is better. The two dots overlap in every bucket — that overlap **is** the finding. |
| Train Brier by market bucket | Same comparison on the 12 train events (n = 1,626 player-starts) | Same story where the search *was* allowed to fit. |
| Held-out log loss by market bucket | A second proper scoring rule on the same held-out events | Agrees with Brier; the result is not an artifact of one metric. |
| The whole gap, zoomed in | Calibrated **minus** expert on held-out, in ten-thousandths of a point | Left of zero = calibrated a hair better; right = a hair worse. Signs are **mixed**, which is what "no edge" looks like. |

Market buckets, in the artifact's own keys: `make_cut`, `top_20`, `top_10`, `top_5`, `win`.

The first three panels use a **log** x-axis because `win` Brier (≈0.0069) and `make_cut` Brier
(≈0.234) differ by ~34×. They are drawn as **dots, not bars**: a bar length on a log axis would
encode nothing honest. The zoom panel is linear, because that is where the actual differences live.

### Held-out numbers, straight from the JSON

| Market bucket | Expert Brier | Calibrated Brier | Difference (×10⁻⁴) |
|---|---|---|---|
| Make the cut | 0.234183 | 0.234194 | +0.10 (calibrated worse) |
| Top 20 | 0.124427 | 0.124032 | −3.95 (calibrated better) |
| Top 10 | 0.073490 | 0.073426 | −0.64 (calibrated better) |
| Top 5 | 0.040151 | 0.040301 | +1.50 (calibrated worse) |
| Win | 0.006933 | 0.006912 | −0.21 (calibrated better) |

Three buckets a hair better, two a hair worse, all differences under 0.0004 of a Brier point. That
mix is why the recommendation froze at `keep_expert`.

---

## Events behind the numbers

Names are taken verbatim from `extra.train_names` and `extra.holdout_names` in the artifact.

**Train (12 — the search was allowed to see these):** PGA Championship · THE CJ CUP Byron Nelson ·
Charles Schwab Challenge · the Memorial Tournament pres. by Workday · RBC Canadian Open ·
U.S. Open · Travelers Championship · John Deere Classic · Genesis Scottish Open · ISCO Championship ·
The Open · Corales Puntacana Championship

**Held out (3 — never used to accept a candidate fit):** 3M Open · Rocket Classic · Wyndham Championship

Artifact context also carried on the chart: `no_future_leakage: true`, `search_ran: true`,
30 search evaluations, recent as-of SG coverage 78.6%, median 6 measured events per player-start.

---

## What this is **not**

- **Not** a claim that any edge is established. The hold-out did not clear the bar; nothing here
  upgrades an observation into a demonstrated advantage.
- **Not** a bet, a price, a pick, a stake, or any buy/sell advice. `AI: NO CASH IN / NO CASH OUT`.
- **Not** a Soften verdict and **not** a Softened board. No Soften lane is opened, moved, or
  rewritten by this chart.
- **Not** a recommendation to switch production to the calibrated vector. Production stays on expert
  weights, exactly as the artifact says.
- **Not** shadow-settle evidence. See the blocked strip below.
- **Not** a new calibration run. Nothing was refit; this only reads a frozen artifact.
- **Not** a freeze of α as a physical constant. One and a half seasons, 15 events, one panel.

## Shadow honesty strip — BLOCKED

The shadow honesty strip is **deliberately absent** from the chart and from this page.

There is no LIVE `advises.jsonl` in this repository, so there are no real shadow advises and no real
shadow settles to plot. No stand-in, sample, replayed, or reconstructed shadow data was used, and
none may be. The strip stays blocked until a LIVE `advises.jsonl` exists and the operator advises
that it is usable.

`render_calibration_weather.py` enforces this: it checks for the canonical shadow-journal path
`golf-offshoot/data/shadow/advises.jsonl` (gitignored; currently absent — the directory holds only a
`.gitkeep`) and **refuses to render** if that file appears, so the chart cannot silently ship a stale
"no shadow data" claim once shadow data exists.

---

## Reproducing the PNG

```bash
pip install matplotlib
python docs/viz/golf_offshoot_dryrun_2026-09-07/render_calibration_weather.py
```

Output: `docs/viz/golf_offshoot_dryrun_2026-09-07/calibration_weather.png` (2640 × 1980 px, dark
`#0b0f14`).

The script reads the real artifact by relative path and **fails loudly if it is missing**. There is
no demo mode, no mock fixture, and no synthetic fallback: every number on the chart is read from
`weights_calib-v3.json` at render time.

---

*Docs only. Phase 1 observation. Source: `weights_calib-v3.json` (real, in repo). Recommendation
surfaced as frozen: `keep_expert` — no edge established. No cash in, no cash out. Not Softened, not a
Soften verdict, not LIVE bets. Shadow honesty strip BLOCKED pending a LIVE `advises.jsonl`; no shadow
settles were invented.*
