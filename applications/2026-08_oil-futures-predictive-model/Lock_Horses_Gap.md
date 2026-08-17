# Lock Record — overnight-gap day horses (fade vs continuation)

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Operator selection:** `ok proceed with your suggested route` after recommended **H-GAP-FADE + H-GAP-CONT**  
**App-local lock IDs:** **H-GAP-FADE** · **H-GAP-CONT** · **L-HUNT-GAP**  
**Status:** **IN FORCE as named day-book horses (cap = these two rows).** Written **before** last-500 confirm scores. Pulse **L-PULSE-GAP-1** scored. Survivor **H-GAP-FADE** (tiny discovery F-DAY beat; small confirm F-DAY beats). Promote does **not** fire (F-CC locked to 0). F-DAY / F-SKILL **not established**.

---

## 0. Plain-language framing

**What was decided:**  
Two — and only two — new recipes. Both usually predict **“no change” for the day session.** They only speak when **last night’s move was large** (top fifth of overnight history so far). One predicts the day **gives some of it back**. The other predicts the day **keeps going**. The computer may pick **one**, only if that one already beat “no change” on the **day** exam in the **older** window.

**What this settles:**  
Which two day-session horses are on the card, the trigger, the scale, the discovery/confirm split, and that a day win is **not** a whole-trip win.

**What this does *not* settle:**  
That skill is shown. That anyone should trade. That flattening before the close is already a pass. That we will now remix these two until one works.

---

## Named horses (quote this)

**Scope:** **Under Rank 4 + L-SESS + F-SRC-CME-TAPE + L-STANDIN-Y-CLF + L-SCREEN-Y-PROMOTE + L-HUNT-GAP**.

This is **not** a remix of **L-HUNT-PRETELL** (other-series OLS). The new information is **this morning’s overnight gap**, which is known at the **open** and is **not** known at yesterday’s settle. Cap = **these two rows**. Do **not** expand after seeing scores. Do **not** hunt on last 500. Do **not** use confirm to pick a runner-up.

### Information set

| Window | Issued | This horse’s forecast |
|--------|--------|------------------------|
| **F-DAY** | t open | Gap recipe below (r_ON,t is known) |
| **F-ON** | t−1 settle | **Always 0** (this morning’s gap is not known yet) |
| **F-CC** | t−1 settle | **Always 0** (same reason) |

F-DAY-met ≠ F-CC-met. F-DAY-met ≠ promote. Combo / “flatten before the close” stays **unnamed** ([R-F-COMBO](RESIDUAL_BRANCH_MENU.md#r-f-combo)).

### Trigger (shared)

Session *t* is a trigger day for **F-DAY** if **|r_ON,t|** is at or above the **80th percentile** of expanding history of **|r_ON|** through **yesterday** (t−1), not including today. Require **≥ 250** past |r_ON| observations; else **false**. If r_ON,t is missing → not a trigger (and skip the day if y is missing, same as H-LAG F-DAY).

### Scale (shared, expanding, through t−1)

k_t = slope from expanding **no-intercept** OLS: **r_DAY = k · r_ON**, fit on all past complete F-DAY days through t−1. Min train **250**. Rank-deficient or n_train < 250 → k unused; forecast **0** even on a trigger.

### Emit

If trigger is false → forecast **0**.  
If trigger is true:

| Horse | Forecast |
|-------|----------|
| **H-GAP-FADE** | **−|k_t| · r_ON,t** (day gives some of the overnight back) |
| **H-GAP-CONT** | **+|k_t| · r_ON,t** (day continues the overnight) |

They are opposite by construction. Unconstrained OLS is **not** used as the emit (that would collapse the two horses).

### Discovery / confirm

| Slot | Rule |
|------|------|
| **Discovery cutoff** | CL sessions with date **≤ 2023-08-21** (day before last-750 first date **2023-08-22**). Last **250 / 500 / 750** unseen during selection. |
| **Discovery scoreboard** | **F-DAY** RMSE vs 0 on the **last 500 sessions of that prefix**, walk-forward, using **only** data ≤ cutoff. |
| **Selection** | Pick the **single** horse with **lowest** F-DAY RMSE on discovery, **only if** it **strictly beats** 0. If **neither** beats 0 → **no survivor**. Do **not** pick the least-bad. |
| **Ties** | If both beat 0 with equal F-DAY RMSE, keep **H-GAP-FADE** (earlier in this lock). Do not break ties with confirm. |
| **Confirm** | That **one** horse only (or skip). Score last **500 / 250 / 750** vs 0 on F-DAY **and** print F-ON / F-CC (locked to 0). No runner-up on the same confirm window. |
| **Promote** | Still **L-SCREEN-Y-PROMOTE** (**F-CC**). A day-only win **does not promote**. F-CC is locked to 0, so last-500 F-CC cannot **strictly** beat 0. |
| **Establishment-stop** | Even a confirm F-DAY beat is stand-in, not F-CC-met, not F-SKILL-met. Honest `04` that would say **established** still **stops**. Do **not** auto-open DataMine. |

---

## What this does *not* do

- Does **not** establish F-SKILL, F-ON, F-DAY, F-CC, F-COMBO, or V-VALUE.  
- Does **not** promote on F-DAY alone.  
- Does **not** name the flattening / switching rule (still [R-F-COMBO](RESIDUAL_BRANCH_MENU.md#r-f-combo)).  
- Does **not** remix L-HUNT-PRETELL or grow this pair into a zoo.  
- Does **not** license trading, start an oil offshoot, or enter Phase 2.

**Lock-time Amb warning:** Naming two day horses does **not** drop leftover-ambiguity on V-SRC. **Amb ≠ clearance.**

---

## Reopen

`leave skill not shown` · `name horse …` (a **different** recipe; do **not** remix this pair; do **not** re-hunt confirm) · `leave screen rule`. Live CME **only if** **L-SCREEN-Y-PROMOTE** fires. Honest **established** still **stops**.
