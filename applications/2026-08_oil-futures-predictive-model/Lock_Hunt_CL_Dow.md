# Lock Record — weekday overlay on Yahoo CL (F-SKILL screen)

**Date:** 2026-09-01  
**Application:** `2026-08_oil-futures-predictive-model`  
**Operator selection:** delegated chip of frozen `next` after **C-CL-SEAS** (no survivor)  
**App-local lock IDs:** **L-HUNT-CL-DOW** · **H-CL-DOW-WD** · **H-CL-DOW-FRI**  
**Status:** **IN FORCE as protocol + named drawer (cap = these two horses).** Written **before** last-500 confirm scores. Confirm is **one** survivor (or none). F-SKILL **not** auto-established. Queue: `QUEUE_CL_Yahoo_Exploration.md` (`C-CL-DOW`).

---

## 0. Plain-language framing

**What was decided:**  
The annual-season drawer lost discovery. The only remaining frozen class is the **weekday** of the session date — not a retune of Fourier/month dummies, not EIA/FOMC event days. One horse adds Tuesday–Friday dummies (Monday baseline). The other adds only a Friday dummy. The computer may pick **one**, only if it already beat no-change on **older** whole sessions. Burned SEAS/INV/COT/DJT/gap/pretell/lag/sparse horses stay burned. After this drawer, `next` is **empty** — stop unless the operator names a new class.

**What this settles:**  
The two weekday features, the two-horse cap, discovery/confirm under **L-SCREEN-Y-PROMOTE**, and that this is the last pre-named Yahoo CL class.

**What this does *not* settle:**  
That oil has a day-of-week effect. That skill is shown. That anyone should trade.

---

## Named protocol (quote this)

**Scope:** **Under Rank 4 + L-SESS + F-SRC-CME-TAPE + L-STANDIN-Y-CLF + L-SCREEN-Y-PROMOTE + L-HUNT-CL-DOW**.

Cap = **these two horses**. Do **not** expand after seeing scores. Do **not** retune SEAS/INV/sparse-cal. Do **not** add weekend/holiday zoos after RMSE. Do **not** invent a third class after these scores.

### 1. Archive

**CL tape:** Yahoo `CL=F` Open/Close stand-in (`data/clf_yahoo_standin.csv`).

**Calendar:** weekday of the **target session** *t* (ISO `date` on the tape). Python `date.weekday()`: Monday = 0 … Sunday = 6. Known at t−1 settle.

**OUT of this pulse (frozen):** annual sin/cos; month dummies; EIA/FOMC event flags; inventory; pretell; month-chain curve; spot 21-day.

**Vehicle fail:** CL discovery pool too thin for last-500 F-CC → stop.

### 2. Features (two horses)

| ID | Extra OLS features (appended to the usual CL lags) |
|----|-----------------------------------------------------|
| **H-CL-DOW-WD** | four dummies: Tuesday, Wednesday, Thursday, Friday (Monday = all 0). Weekend sessions, if any, also all 0. |
| **H-CL-DOW-FRI** | one dummy: Friday = 1, else 0 |

### 3. OLS

Same as **L-HUNT-CL-SEAS**: expanding, intercept, min train **250**. F-ON/F-CC: `[1, r_ON,t−1, r_DAY,t−1, …]`. F-DAY: `[1, r_ON,t, r_DAY,t−1, …]`. Rank-deficient or n_train < 250 → **0**.

### 4. Discovery / confirm

Same screen as SEAS/INV: cutoff CL sessions **≤ 2023-08-21**; last **500** F-CC vs 0; pick lowest RMSE **only if** it **strictly beats** 0; ties keep **H-CL-DOW-WD**; confirm last **500 / 250 / 750**; promote **L-SCREEN-Y-PROMOTE**. `--phase discovery` must not compute confirm.

If **no survivor**, `next` is empty — **stop**. Do **not** pick least-bad. Do **not** append a class after RMSE.

---

## What this does *not* do

- Does **not** establish F-SKILL or V-VALUE.  
- Does **not** retune SEAS.  
- Does **not** license a trade, Phase 2, or DataMine.

**Lock-time Amb warning:** **Amb ≠ clearance.**

---

## Reopen

`leave skill not shown` · `name horse …` only if this drawer has no survivor **and** the operator names a new class (frozen `next` will be empty) · `leave screen rule`. Honest **established** still **stops**.
