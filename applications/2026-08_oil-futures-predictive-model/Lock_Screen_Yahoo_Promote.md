# Lock Record — Yahoo screen, promote to live CME only on F-CC beat

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Operator selection:** `yes lets do that` after recommended screen-then-confirm  
**App-local lock ID:** **L-SCREEN-Y-PROMOTE**  
**Status:** **IN FORCE as protocol.** Does **not** establish F-SKILL. **H-LAG-WF** already **fails** this gate (F-CC loss). **L-HUNT-CL-DOW** scored (**no survivor**; does not promote). **L-HUNT-CL-SEAS** scored (**no survivor**; does not promote). **L-HUNT-CL-INV** scored (**no survivor**; does not promote). **L-HUNT-SPOT-TREND** does **not** fire this gate (wrong object). Nothing promotes now.

---

## 0. Plain-language framing

**What was decided:**  
Keep building and testing front-only recipes on the Yahoo tape we already have. Spend on official CME only if a named recipe **beats “assume no change” on the whole trip**. A tiny overnight blip does **not** count.

**What this settles:**  
The order of work, and what “looks interesting” means before live stamps.

**What this does *not* settle:**  
That any model works. That a Yahoo win is a live win. That anyone should trade.

---

## Locked content

**Scope:** **Under Rank 4 + L-SESS + F-SRC-CME-TAPE + L-STANDIN-Y-CLF + L-SCREEN-Y-PROMOTE**.

| ID | Rule |
|----|------|
| **Screen tape** | Yahoo `CL=F` Open/Close stand-in (`Lock_Standin_Yahoo_CLF.md`). Front-only horses. |
| **Promotion gate (all required)** | A **named** horse, walk-forward, same declared OOS as the baseline: **F-CC RMSE < RMSE of 0** on last **500**, **and** F-CC horse RMSE **≤** RMSE of 0 on last **250** and last **750**. |
| **Does not promote** | F-ON or F-DAY alone; a tiny overnight dip; in-sample fit; Kearney–Shang MAE print-match |
| **Live confirmation** | Official CME open/settle + roll **R1**. Re-score the **same named horse** vs 0. Not a new fishing trip on live stamps. |
| **Yahoo win** | Still **stand-in**. Not live clearance. Not F-SKILL-met. Honest **established** still **stops**. |
| **H-SPARSE-CAL** | Scored: tiny F-CC last-500 dip; **loss** on last 750. **Does not promote.** |
| **H-SPARSE-VOL** | Scored: F-CC **loss**. **Does not promote.** |
| **H-LAG-WF** | Already scored: F-CC **loss**. **Does not promote.** |
| **H-KS-FTS** | **Out of this screen.** Needs a freeze-matching CL1–CL18 tape; Yahoo front `CL=F` is not that tape. |
| **L-HUNT-PRETELL** | Eight named tell horses. Discovery F-CC: **all lose**. **No survivor.** Confirm skipped. **Does not promote.** |
| **H-GAP-FADE** | Day-gap fade. Small F-DAY confirm beats; F-CC locked to 0. **Does not promote.** |
| **H-GAP-CONT** | Day-gap continuation. Discovery F-DAY **loss**. Not confirmed. **Does not promote.** |
| **L-HUNT-DJT** | Two Truth Social oil-sentiment horses. Discovery F-CC: **both tie 0**. **No survivor.** Confirm skipped. **Does not promote.** |
| **L-HUNT-COT** | Two CFTC managed-money horses. Discovery F-CC: **both lose**. **No survivor.** Confirm skipped. **Does not promote.** |
| **L-HUNT-CL-INV** | Two EIA weekly inventory overlay horses on Yahoo CL (**H-CL-INV-SURP** / **H-CL-INV-WOW**). Discovery F-CC last 500 of prefix ≤ 2023-08-21: RMSE 0 = **0.026705**; SURP **0.026836** (beats_0 false); WOW **0.026803** (beats_0 false, closest). **No survivor.** Do **not** pick least-bad. Confirm skipped. **Does not promote.** |
| **L-HUNT-CL-SEAS** | Two annual-season overlay horses on Yahoo CL (**H-CL-SEAS-ANN** / **H-CL-SEAS-MON**). Discovery F-CC last 500 of prefix ≤ 2023-08-21: RMSE 0 = **0.026705**; ANN **0.026799** (beats_0 false, closest); MON **0.026816** (beats_0 false). **No survivor.** Do **not** pick least-bad. Confirm skipped. **Does not promote.** |
| **L-HUNT-CL-DOW** | Two weekday overlay horses on Yahoo CL (**H-CL-DOW-WD** / **H-CL-DOW-FRI**). Discovery F-CC last 500 of prefix ≤ 2023-08-21: RMSE 0 = **0.026705**; WD **0.026812** (beats_0 false); FRI **0.026775** (beats_0 false, closest). **No survivor.** Do **not** pick least-bad. Confirm skipped. **Does not promote.** Named Yahoo CL queue **empty**. |
| **V-VALUE** | Unchanged. After-cost P/L under **V2** is a later named book, not this gate. |

**“Not lose” on 250/750** means horse RMSE **≤** no-change RMSE (ties allowed). Last **500** must **strictly beat**.

---

## What this does *not* do

- Does **not** establish F-SKILL, F-ON, F-DAY, F-CC, or V-VALUE.  
- Does **not** auto-fetch DataMine.  
- Does **not** license trading or start an oil offshoot.  
- Does **not** enter Phase 2.

**Lock-time Amb warning:** Fixing the screen rule does **not** drop leftover-ambiguity. **Amb ≠ clearance.**

---

## Reopen

A later operator may change the promotion numbers or skip straight to live CME. That is a freeze change, not a silent softening.
