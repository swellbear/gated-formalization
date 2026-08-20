# Pulse result — EIA weekly crude inventory surprise overlay (Track B queue)

**Date:** 2026-08-20  
**Application:** `2026-08_oil-futures-predictive-model`  
**Layer ID:** **L-PULSE-SPOT-INV-1**  
**Locks:** `Lock_Hunt_Spot_Inv.md` · `Lock_Hunt_Spot_Trend.md` · `QUEUE_Spot_Trend_Exploration.md`  
**Live vs stand-in:** EIA weekly HTML leaf (**PET.WCESTUS1.W**) + existing FRED EIA spot reprints. **Not** Bloomberg survey surprise. **Not** NYMEX CL. **No print scored to met.**

---

## 0. Plain-language framing

**What we did:** You asked to try the next idea on the same cash 21-day question: take the public weekly U.S. crude stockpile report, compare this week’s change to the average of the previous four weeks, and overlay that on the next-21-day call. One rule treats a tighter-than-recent print as a reason to call **up**; the other does the opposite. The computer could pick **one** per oil only if it already beat “the trend continues” on **older** days. Neither did. The two rules that already failed were **not** brought back. 21 days was **not** changed. The recent exam was **not** used to train.

**What this settles:** Numeric discovery hit-rates for this two-horse overlay. Hunt **failed at discovery**. Confirm **skipped**. Not a trade.

---

## 1. Vehicle (not a fail)

EIA weekly history grid parsed as HTML (FRED `WCESTUS1` 404). **2290** weeks, week-ending **1982-08-20 … 2026-08-14** (release Wednesdays **1982-08-25 … 2026-08-19**). Reports with release ≤ discovery cutoff: WTI-span **1963** / Brent-span **1892** (threshold 30 — **not** vehicle-fail).

Naive surprise = WoW change minus mean of prior **4** WoW changes. Clock: `release_date ≤ t−1`, then carry. Do **not** retune. Do **not** switch to Cushing-only or a Street poll after scores. Burned FLIP-HOLD / REV **not** scored.

---

## 2. Discovery (locked before last-500 confirm)

Cutoff: issue dates **≤ 2023-08-21**. Scoreboard: last **500** eligible of that prefix (same dates as Track B pulse 1). Train arm: **N/A**.

### WTI (2021-08-24 … 2023-08-21)

Continuation: **0.508** (254 / 500).

| Horse | Hits | Hit-rate | Beats continuation? |
|-------|------|----------|---------------------|
| **H-SPOT-INV-CONT** | 253 | 0.506 | **no** (closest loss) |
| **H-SPOT-INV-FADE** | 247 | 0.494 | **no** |

**Survivor:** **none.**

### Brent (2021-08-27 … 2023-08-21)

Continuation: **0.506** (253 / 500).

| Horse | Hits | Hit-rate | Beats continuation? |
|-------|------|----------|---------------------|
| **H-SPOT-INV-CONT** | 251 | 0.502 | **no** |
| **H-SPOT-INV-FADE** | 249 | 0.498 | **no** |

**Survivor:** **none.**

Do **not** pick the least-bad. WTI-met ≠ Brent-met; both failed.

---

## 3. Confirm

**Skipped** on both scoreboards. Last 250 / 500 / 750 were **not** used to pick a horse. Do **not** re-hunt confirm. Do **not** change 21. Do **not** unburn. Do **not** add Cushing-only or Bloomberg consensus after scores.

**L-SCREEN-Y-PROMOTE:** **does not apply**.

---

## 4. Establishment-stop drill

**Would honest `04` declare spot 21-day skill established?** **No.**

**Would honest `04` declare F-SKILL established?** **No.** This pulse did not score next-session CL RMSE.

**Would honest `04` declare those bars refuted?** **No.** A finite overlay miss is not “inventories don’t move oil,” and it is not a Street-poll test.

---

## 5. Exploration queue (after scores)

Burned (add): H-SPOT-INV-CONT and H-SPOT-INV-FADE on **both** boards. FLIP-HOLD / REV stay burned.

Next (not scored): **C-SPOT-CROSS** · **C-SPOT-LOGIT**.

---

## 6. Scripts / artifacts

- `scripts/fetch_eia_inventory.py` · `scripts/spot_inv_hunt.py`  
- `data/eia_weekly_crude_exspr.csv` · `data/eia_inv_fetch.json` · `data/spot_inv_hunt_scores.json` · `data/spot_trend_queue.json`  
- Reproduce: `python3 scripts/fetch_eia_inventory.py` then `python3 scripts/spot_inv_hunt.py --stage discovery`

---

*Not trading advice. Naive surprise ≠ Bloomberg. No survivor ≠ least-bad. Confirm is not a training arm.*
