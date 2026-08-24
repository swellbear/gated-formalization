# Lock Record — EIA spot expanding-window logistic (Track B queue)

**Date:** 2026-08-24  
**Application:** `2026-08_oil-futures-predictive-model`  
**Operator selection:** **B** — chip the next queued spot class (**C-SPOT-LOGIT**)  
**App-local lock IDs:** **L-HUNT-SPOT-LOGIT** · **H-SPOT-LOGIT-FULL** · **H-SPOT-LOGIT-SIGN**  
**Status:** **IN FORCE as protocol + named drawer (cap = these two horses).** Written **before** last-500 confirm scores. Same 21-day spot object as `Lock_Hunt_Spot_Trend.md`. **First use of the train arm** with fitted coefficients. Do **not** unburn H-SPOT-FLIP-HOLD / H-SPOT-REV / H-SPOT-INV-CONT / H-SPOT-INV-FADE / H-SPOT-CROSS-B2W. Do **not** retune H-SPOT-CROSS-W2B. Do **not** change 21. Confirm is **one** survivor per scoreboard (or none). F-SKILL stays **leave skill not shown**.

---

## 0. Plain-language framing

**What was decided:**  
Keep the same cash WTI / Brent 21-day question. This pulse is the first time the computer may **fit** coefficients — but only on **older** days whose next-21 outcome is already known, and only inside a recipe written now. Features are today’s 21-day up/down label and how large that move was. One rule uses both; the other uses the label alone. The computer may pick **one** per oil only if that oil’s named fit already beat “the trend continues” on **older** days. Burned rules stay burned. 21 days stays 21. The recent exam still does **not** train.

**What this settles:**  
The feature set, the expanding past-only train clock, the two-horse cap, the min-train floor, and that 21 and burned rows stay frozen.

**What this does *not* settle:**  
That a logistic “model of oil” exists. That skill is shown. That anyone should trade. That W2B should be remixed into the fit.

---

## Named protocol (quote this)

**Scope:** **Under Rank 4 (F-SKILL parked) + L-HUNT-SPOT-TREND + L-STANDIN-EIA-SPOT + L-SPOT-ARMS + L-SPOT-QUEUE + L-HUNT-SPOT-LOGIT**.

Parent object, 21-day label, flip (descriptive), skill target, continuation baseline, skip mask, discovery cutoff, confirm windows, and three arms are **inherited** from `Lock_Hunt_Spot_Trend.md`. This pulse names a **new two-horse drawer** that **uses the train arm**. Reuse the existing EIA spot CSVs. No new fetch class.

**WTI-met ≠ Brent-met.** Same two scoreboards. Fits are **per board** (do not pool WTI and Brent rows into one coefficient vector).

### 1. Features (frozen)

On issue date *t* (eligible print):

| Feature | Definition |
|---------|------------|
| **sign_num** | **+1** if 21-day sign at *t* is Up; **−1** if Down |
| **abs_r21** | Absolute value of the 21-day log-return at *t*, `\|ln(P_t / P_{t−21})\|` |

**OUT of this pulse (frozen):** peer (cross-oil) features; inventory; lag-1 sign as a second feature beyond what SIGN already encodes; polynomials; rolling windows that drop early history; regularization strength as a free knob after scores; dollar returns instead of log. Do **not** add those after hit-rate.

### 2. Train clock (past-only; outcome must be known)

At call date *t*:

**Train set** = every earlier eligible issue date *u* on the **same** board such that the print date of *u+21* is **strictly before** the print date of *t* (so `truth_u` is known without using *t* or any later print).

**Expanding window:** all such *u*, oldest first — not a fixed-length roll.

**Label:** `y_u = 1` if truth at *u* is Up; `0` if Down.

**Min train:** need **≥ 50** train rows. If fewer, or if the fit fails (singular / non-finite / max iterations without a usable β), the horse calls **continuation** (sign at *t*).

**Refit:** coefficients are re-estimated at every call date from that date’s train set. Confirm windows **recompute** the same walk-forward rule; they do **not** freeze discovery β and paste it forward, and they do **not** peek at confirm misses to change features.

### 3. Horses (cap 2)

Same eligible issue dates as Track B. Continuation = sign_t (baseline, not a horse).

| ID | Design matrix at *t* / in train | Call |
|----|--------------------------------|------|
| **H-SPOT-LOGIT-FULL** | intercept + sign_num + abs_r21 | Up if `P(y=1) ≥ 0.5`, else Down |
| **H-SPOT-LOGIT-SIGN** | intercept + sign_num | Up if `P(y=1) ≥ 0.5`, else Down |

`P(y=1) = 1 / (1 + exp(−x′β))` with β from maximum-likelihood logistic (IRLS). Probability exactly 0.5 → **Up** (frozen; rare).

Do **not** score burned horses. Do **not** blend with DJT / COT / gap / CROSS-W2B. Do **not** change 21.

Ties (both beat, equal hit-rate): keep **H-SPOT-LOGIT-FULL** (earlier in this lock).

### 4. Discovery / confirm

Inherited. Discovery cutoff **2023-08-21**; last **500** eligible of that prefix; pick one only if it **strictly beats** continuation; else **no survivor**. Confirm that one horse (or skip) on last **500 / 250 / 750**. Confirm never trains (never changes features, min-train, or solver). Yahoo promote **does not apply**. Honest **established** still **stops**. Tiny ≠ met.

Discovery **before** confirm. `--stage discovery` must not compute confirm windows.

**Vehicle fail:** either board discovery pool **< 250**, or fewer than **250** of that board’s discovery last-500 have a successful fit (not continuation-fallback) → stop.

### 5. Queue

**C-SPOT-LOGIT** is this pulse (no longer queued). Queue is otherwise **empty** after this class. Burned rows stay burned. CROSS-W2B stays a Brent protocol survivor on the prior pulse — **not** remixed here.

---

## What this does *not* do

- Does **not** establish F-SKILL, V-VALUE, or spot-trend skill by existing.  
- Does **not** unburn prior horses or retune 21 / W2B.  
- Does **not** license a trade, Phase 2, or DataMine.

**Lock-time Amb warning:** Running this hunt does **not** drop V-SRC leftover-ambiguity. **Amb ≠ clearance.**

---

## Reopen

`leave skill not shown` · stop Track B chipping (queue empty after this pulse) · `name horse …` on Yahoo (different **CL** recipe) · `leave screen rule`. Honest **established** still **stops**. Do **not** invent a new spot class after scores without a new operator pick.
