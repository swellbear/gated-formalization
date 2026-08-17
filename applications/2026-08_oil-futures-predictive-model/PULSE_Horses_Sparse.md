# Pulse result — sparse horses vs no-change RMSE (Yahoo stand-in)

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Layer ID:** **L-PULSE-SPARSE-1**  
**Locks:** `Lock_Horses_Sparse.md` · `Lock_Screen_Yahoo_Promote.md` · `Lock_Standin_Yahoo_CLF.md`  
**Live vs stand-in:** **Stand-in.** **No print scored to met.**

---

## 0. Plain-language framing

**What we did:** You named two recipes that usually predict “no change,” and only speak up on a calendar day or after a big prior move. We scored both on Yahoo `CL=F` against last settlement.

**What this settles:** Numeric RMSE for **H-SPARSE-CAL** and **H-SPARSE-VOL**. Neither promotes to live CME. Skill is still **not shown**. Not a trade.

---

## 1. H-SPARSE-CAL (last 500 sessions, 2024-08-20 … 2026-08-14)

Triggered on **105 / 500** sessions (EIA WPSR or scheduled FOMC announcement). Else forecast 0.

| Window | RMSE horse | RMSE 0 | n | Beats 0? |
|--------|------------|--------|---|----------|
| **F-ON** | **0.01288** | 0.01291 | 500 | tiny yes |
| **F-DAY** | **0.02663** | 0.02663 | 500 | tiny yes |
| **F-CC** | **0.02869** | 0.02869 | 500 | tiny yes |

Exact F-CC: horse **0.02868990** vs 0 **0.02869369**. Difference ≈ **0.000004**. That is **not** F-CC-met.

Sensitivity F-CC:

| Window | RMSE horse | RMSE 0 | Beats 0? |
|--------|------------|--------|----------|
| last 250 | 0.03434 | 0.03436 | yes (tiny) |
| last 500 | 0.02868990 | 0.02869369 | yes (tiny) |
| last 750 | **0.025690** | **0.025689** | **no** |

**L-SCREEN-Y-PROMOTE:** **does not fire** (last 750 F-CC **loss**).

---

## 2. H-SPARSE-VOL (same last 500)

Triggered on **120 / 500** sessions (|r_CC,t−1| ≥ expanding 80th percentile). Else forecast 0.

| Window | RMSE horse | RMSE 0 | n | Beats 0? |
|--------|------------|--------|---|----------|
| **F-ON** | **0.01284** | 0.01291 | 500 | tiny yes |
| **F-DAY** | **0.02668** | 0.02663 | 500 | **no** |
| **F-CC** | **0.02885** | 0.02869 | 500 | **no** |

F-CC also **worse** than 0 on last 250 (0.03460 vs 0.03436) and last 750 (0.02580 vs 0.02569).

**L-SCREEN-Y-PROMOTE:** **does not fire**.

---

## 3. Establishment-stop drill

**Would honest `04` declare F-SKILL / F-CC / F-ON / F-DAY established?** **No.**

A 0.000004 RMSE dip on a stand-in, which **fails** last 750, is not P-NonNegligible skill. VOL lost the parent bar. Two named rows is not a zoo win. Tiny ≠ met. Promote did **not** fire.

**Would honest `04` declare those bars refuted?** **No.** Two sparse gates on Yahoo do not refute every recipe.

---

## 4. Scripts / artifacts

- `scripts/cl_horses.py` · `data/sparse_calendar.json` · `data/horse_scores.json`  
- Reproduce: `python3 scripts/cl_horses.py` from this application folder.

---

*Not trading advice. Stand-in ≠ live. Tiny F-CC dip ≠ skill-met. Failed 750 ≠ promote. Cap remains these two rows.*
