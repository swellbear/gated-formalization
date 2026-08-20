# Pulse result — EIA spot WTI / Brent 21-day trend hunt (Track B)

**Date:** 2026-08-20  
**Application:** `2026-08_oil-futures-predictive-model`  
**Layer ID:** **L-PULSE-SPOT-1**  
**Locks:** `Lock_Hunt_Spot_Trend.md` · `QUEUE_Spot_Trend_Exploration.md`  
**Live vs stand-in:** **Stand-in cash tape** (FRED EIA-sourced reprints **DCOILWTICO** / **DCOILBRENTEU**). **Not** NYMEX CL / ICE Brent. **No print scored to met.**

---

## 0. Plain-language framing

**What we did:** You asked the computer to read the public **cash** price of WTI and of Brent, label the last **21** printed days as up or down, note whether that label flipped, and pick at most one frozen rule that calls the **next** 21 days — only if it already beat “whatever just happened will happen again” on **older** days. One rule waits a day after a flip. The other always calls the opposite. Neither beat “it continues” on that older exam, for WTI or for Brent. So **no winner was sent** to the recent exam. We did **not** change 21 days after seeing that. We did **not** train on the recent exam.

**What this settles:** Numeric discovery hit-rates for the locked two-horse drawer on both spot scoreboards. Hunt **failed at discovery**. Confirm **skipped**. This is **not** F-SKILL on futures. Not a trade.

**Descriptive as of last completed print (2026-08-18):** both WTI and Brent 21-day labels are **Up**; **no flip** that day. That dashboard is **not** a pass.

---

## 1. Vehicle (not a fail)

Named fallback **fred_eia_reprint** (EIA Open Data key absent; EIA `.xls` present but not parsed without xlrd). Lock allows this vehicle.

| Series | Prints | Span | Discovery-eligible pool |
|--------|--------|------|-------------------------|
| **WTI** | **10225** | 1986-01-02 … 2026-08-18 | **9408** (threshold 250 — **not** vehicle-fail) |
| **Brent** | **9958** | 1987-05-20 … 2026-08-18 | **9119** |

Horizon = **21** price steps. Unified skip: need *t−1* 21-day sign, realized next 21, no Flats. Do **not** retune 21. Queued classes **C-SPOT-INV** / **C-SPOT-CROSS** / **C-SPOT-LOGIT** were **not** scored.

---

## 2. Discovery (locked before last-500 confirm)

Cutoff: issue dates **≤ 2023-08-21**. Scoreboard: last **500** eligible of that prefix. Train arm: **N/A** (no fitted coefficients). Select arm only.

### WTI (2021-08-24 … 2023-08-21)

Continuation hit-rate: **0.508** (254 / 500).

| Horse | Hits | Hit-rate | Beats continuation? |
|-------|------|----------|---------------------|
| **H-SPOT-FLIP-HOLD** | 247 | 0.494 | **no** |
| **H-SPOT-REV** | 246 | 0.492 | **no** |

**Survivor:** **none.**

### Brent (2021-08-27 … 2023-08-21)

Continuation hit-rate: **0.506** (253 / 500).

| Horse | Hits | Hit-rate | Beats continuation? |
|-------|------|----------|---------------------|
| **H-SPOT-FLIP-HOLD** | 248 | 0.496 | **no** |
| **H-SPOT-REV** | 247 | 0.494 | **no** |

**Survivor:** **none.**

Do **not** pick the least-bad. WTI-met ≠ Brent-met; both failed.

---

## 3. Confirm

**Skipped** on both scoreboards. Last 250 / 500 / 750 were **not** used to pick a horse and were **not** computed as a training arm. Do **not** re-hunt this confirm window. Do **not** change 21. Do **not** unburn these rows.

**L-SCREEN-Y-PROMOTE:** **does not apply** (wrong object). **Does not fire.**

---

## 4. Establishment-stop drill

**Would honest `04` declare spot 21-day skill (hit-rate vs continuation) established?** **No.**

Two named rules that **both lose** to continuation on the discovery 500 are not P-NonNegligible skill on this object. Failed discovery ≠ a confirm pass.

**Would honest `04` declare F-SKILL / F-CC established?** **No.** This pulse did not score next-session CL RMSE. Parent leftover stays **leave skill not shown**.

**Would honest `04` declare those bars refuted?** **No.** A finite drawer miss does not refute every trend rule. It also does **not** say “oil has no trend.” Continuation itself was only ~51% on this window.

---

## 5. Exploration queue (after scores)

Burned (do **not** retune): H-SPOT-FLIP-HOLD and H-SPOT-REV on **both** WTI and Brent.

Next (not scored): **C-SPOT-INV** · **C-SPOT-CROSS** · **C-SPOT-LOGIT**. See `QUEUE_Spot_Trend_Exploration.md`.

---

## 6. Scripts / artifacts

- `scripts/fetch_eia_spot.py` · `scripts/spot_trend_hunt.py`  
- `data/eia_spot_wti.csv` · `data/eia_spot_brent.csv` · `data/eia_spot_fetch.json` · `data/spot_trend_hunt_scores.json` · `data/spot_trend_queue.json`  
- Reproduce: `python3 scripts/fetch_eia_spot.py` then `python3 scripts/spot_trend_hunt.py --stage discovery` from this application folder. Confirm stays skipped unless a later lock names a discovery survivor.

---

*Not trading advice. Spot ≠ futures. No survivor ≠ pick the least-bad. Confirm is not a training arm. Cap remains these two rows.*
