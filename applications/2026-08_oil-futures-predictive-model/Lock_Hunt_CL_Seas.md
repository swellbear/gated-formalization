# Lock Record — annual season overlay on Yahoo CL (F-SKILL screen)

**Date:** 2026-09-01  
**Application:** `2026-08_oil-futures-predictive-model`  
**Operator selection:** delegated — decide the best unused CL classes and chip without a further prompt (`C-CL-SEAS` first)  
**App-local lock IDs:** **L-HUNT-CL-SEAS** · **H-CL-SEAS-ANN** · **H-CL-SEAS-MON**  
**Status:** **IN FORCE as protocol + named drawer (cap = these two horses).** Written **before** last-500 confirm scores. Confirm is **one** survivor (or none). F-SKILL **not** auto-established. Unparks F-SKILL scoring on this object only (parent Rank 4 still split). Queue: `QUEUE_CL_Yahoo_Exploration.md`.

---

## 0. Plain-language framing

**What was decided:**  
Keep the futures skill leftover on the Yahoo stand-in tape. The next unused recipe is **calendar season** of the session date — not inventories, not EIA/FOMC *event* days, not a retune of burned lag/sparse/gap/pretell/DJT/COT/INV horses. One horse adds a smooth annual cycle (sine and cosine of day-of-year). The other adds calendar-month dummies. The computer may pick **one**, only if it already beat no-change on **older** whole sessions. Spot 21-day stays parked (Track B already lost confirm). The Yahoo month chain is **not** used (it is not historical CL1–CL18).

**What this settles:**  
The two season features, the two-horse cap, discovery/confirm under **L-SCREEN-Y-PROMOTE**, and that weekday overlay is the **only** pre-named next class (`C-CL-DOW`) if this drawer has no survivor.

**What this does *not* settle:**  
That oil “has a season.” That skill is shown. That anyone should trade. That a later weekday overlay may be rewritten after these scores.

---

## Named protocol (quote this)

**Scope:** **Under Rank 4 + L-SESS + F-SRC-CME-TAPE + L-STANDIN-Y-CLF + L-SCREEN-Y-PROMOTE + L-HUNT-CL-SEAS**.

This is a **capped named drawer**, not an unbounded calendar kitchen sink. Cap = **these two horses**. Do **not** expand after seeing scores. Do **not** hunt on last 500. Do **not** switch to lunar, heating-degree, or OPEC-meeting dummies after RMSE. Do **not** retune lag / sparse / gap / pretell / DJT / COT / INV. Do **not** remix Track B spot horses into this F-CC object. Do **not** treat `H-SPARSE-CAL` as this class.

### 1. Archive

**CL tape:** Yahoo `CL=F` Open/Close stand-in (`data/clf_yahoo_standin.csv`).

**Calendar:** Gregorian date of the **target session** *t* (ISO `date` on the tape). Known at t−1 settle.

**OUT of this pulse (frozen):** event-day EIA/FOMC flags; inventory; COT; pretell tickers; month-chain curve; spot 21-day hit-rate; heating/cooling degree days; lunar phase.

**Vehicle fail:** CL discovery pool too thin for last-500 F-CC → stop.

### 2. Features (two horses)

Let `doy` = day-of-year of session *t* (`1…366`). Frozen year length **365.25**.

- `sin_t` = sin(2π · doy / 365.25)  
- `cos_t` = cos(2π · doy / 365.25)  
- Month dummies: for calendar month `m = 2…12`, `1` if session *t* is month *m*, else `0`. **January is the baseline** (all dummies 0).

| ID | Extra OLS features (appended to the usual CL lags) |
|----|-----------------------------------------------------|
| **H-CL-SEAS-ANN** | `sin_t`, `cos_t` |
| **H-CL-SEAS-MON** | eleven month dummies `m2…m12` |

### 3. OLS

Expanding, intercept, min train **250**. Same CL lags as INV/COT/H-LAG:

| Window | Issued | Target | Base features |
|--------|--------|--------|----------------|
| **F-ON / F-CC** | t−1 settle | overnight / close-to-close | 1, r_ON,t−1, r_DAY,t−1 |
| **F-DAY** | t open | day log-return | 1, r_ON,t, r_DAY,t−1 |

Rank-deficient or n_train < 250 → **0**. Missing CL y/x → skip.

### 4. Discovery / confirm

| Slot | Rule |
|------|------|
| **Discovery cutoff** | CL sessions **≤ 2023-08-21** |
| **Discovery scoreboard** | F-CC RMSE vs 0 on last **500** of that prefix |
| **Selection** | Lowest F-CC RMSE **only if** it **strictly beats** 0. If neither → **no survivor** |
| **Ties** | Keep **H-CL-SEAS-ANN** (earlier in this lock) |
| **Confirm** | That **one** horse (or skip). Last **500 / 250 / 750** vs 0. No runner-up |
| **Promote** | **L-SCREEN-Y-PROMOTE**: last-500 F-CC **strictly beats** 0 **and** last-250 and last-750 F-CC **≤** 0. Yahoo win ≠ live ≠ F-SKILL-met |
| **Establishment-stop** | Honest `04` that would say **established** still **stops**. No DataMine auto-open |

Discovery **before** confirm. `--phase discovery` must not compute confirm windows.

### 5. After this drawer (frozen queue, not this pulse)

If **no survivor**, chip **C-CL-DOW** next (weekday overlay). Do **not** invent a third class after SEAS scores. If **C-CL-DOW** is later empty/scored and still no promote, **stop**.

---

## What this does *not* do

- Does **not** establish F-SKILL, F-ON, F-DAY, F-CC, or V-VALUE by existing.  
- Does **not** claim “oil is seasonal.”  
- Does **not** clear Track B spot skill.  
- Does **not** license a trade, Phase 2, or DataMine.

**Lock-time Amb warning:** Running this hunt does **not** drop V-SRC leftover-ambiguity. **Amb ≠ clearance.**

---

## Reopen

`leave skill not shown` · chip **C-CL-DOW** if this drawer has no survivor · `name horse …` only if the frozen `next` list is empty **and** the operator names a new class · `leave screen rule`. Live CME **only if** **L-SCREEN-Y-PROMOTE** fires. Honest **established** still **stops**.
