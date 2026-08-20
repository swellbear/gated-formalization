# Lock Record — EIA spot WTI / Brent 21-day trend hunt (Track B)

**Date:** 2026-08-20  
**Application:** `2026-08_oil-futures-predictive-model`  
**Operator selection:** build Track B (spot WTI + spot Brent trend call, flip trigger, next-window skill); three arms (train / select / confirm); exploration queue after this two-horse pulse  
**App-local lock IDs:** **L-HUNT-SPOT-TREND** · **L-STANDIN-EIA-SPOT** · **L-SPOT-ARMS** · **L-SPOT-QUEUE** · **H-SPOT-FLIP-HOLD** · **H-SPOT-REV**  
**Status:** **IN FORCE as protocol + named drawer (cap = these two horses) + three-arm split + queued next classes (not scored this pulse).** Written **before** last-500 confirm scores. Confirm is **one** survivor per scoreboard (or none). This pulse does **not** establish F-SKILL or V-VALUE. Parent F-SKILL stays **leave skill not shown**.

---

## 0. Plain-language framing

**What was decided:**  
Use the public **cash** (spot) price of WTI at Cushing and of Brent in the North Sea, not the futures pit. Each day, say whether the last **21** printed days went up or down, and whether that label **flipped** versus the day before. Then ask whether a frozen rule can call the **next** 21 days’ direction better than “whatever just happened will happen again.” The computer may pick **one** rule per oil, only if it already beat that “it continues” guess on **older** days. The recent exam is not for training. A miss does not retune the rule.

**What this settles:**  
The two spot series, the 21-day label, the flip trigger, the skill target, the continuation baseline, the two horses, the three arms, the discovery cutoff, and the next-class queue (not run this pulse).

**What this does *not* settle:**  
That anyone can trade it. That NYMEX CL or ICE Brent futures skill is shown. That a green test is a strategy. That the rule should rewrite itself after a miss.

---

## Named protocol (quote this)

**Scope:** **Under Rank 4 (F-SKILL parked this pulse: leave skill not shown) + L-HUNT-SPOT-TREND + L-STANDIN-EIA-SPOT + L-SPOT-ARMS + L-SPOT-QUEUE**.

This is a **capped named drawer** on a **new object** (spot 21-day sign), **not** an F-CC horse and **not** an unbounded trend kitchen sink. Cap = **these two horses**. Do **not** expand after seeing scores. Do **not** hunt on last 500 / 250 / 750. Do **not** change 21 to 5 / 63 / 252 after hit-rate. Do **not** mix DJT / COT / gap / pretell into this pulse. Do **not** use confirm as training.

**WTI-met ≠ Brent-met.** Two scoreboards. A survivor on one is not a survivor on the other.

### 1. Object / archive (L-STANDIN-EIA-SPOT)

| Scoreboard | Series | Named limitation |
|------------|--------|------------------|
| **WTI** | EIA daily Cushing OK WTI spot FOB (**PET.RWTC.D**) | Cash Cushing print, not NYMEX CL |
| **Brent** | EIA daily Europe Brent spot FOB (**PET.RBRTE.D**) | Cash Brent print, not ICE Brent futures |

**Primary fetch:** EIA public daily spot file / Open Data for those series.  
**Named fallback (only if EIA file fail):** FRED **DCOILWTICO** / **DCOILBRENTEU** (EIA-sourced daily reprints). Record which vehicle was used. Do **not** switch to futures, Bloomberg, or a different cash hub after scores.

Clock: last **completed** daily print in the file. No same-day revision games. Weekends/holidays are absent rows, not zeros.

**OUT of this pulse:** NYMEX CL, ICE Brent futures, Yahoo `CL=F`, real-price deflators, monthly averages, EIA STEO.

**Vehicle fail:** fetch fails, or either series has **< 250** discovery-eligible issue dates → stop; do not invent a spot tape.

### 2. Trend label (descriptive; not the skill bar)

On price-day *t* (index *t* in the sorted EIA prints):

**21-day log-return** = `ln(P_t / P_{t-21})` (21 steps between prints).

| Label | When |
|-------|------|
| **Up** | return **> 0** |
| **Down** | return **< 0** |
| **Flat** | return **= 0** only |

Year / 6-month / 5-day extra windows **OUT** of this pulse (do not add after scores).

This label is what “calling the trend” **means** on the descriptive dashboard. It is **not** by itself a pass.

### 3. Flip trigger (descriptive)

A **flip** at *t* holds iff the 21-day labels at *t* and *t−1* are **{Up, Down}** in either order.

Flat → Up, Flat → Down, Up → Flat, Down → Flat, and Flat → Flat are **not** flips.

Logged every eligible day. A flip is a **trigger to report**, not a license to retune.

### 4. Skill target, baseline, metric

**Target:** sign of the **next** 21-step log-return `ln(P_{t+21} / P_t)`.

**Baseline (not a horse):** **continuation** = call the 21-day sign as of *t*. Continuation is the thing to beat, not a named recipe.

**Skip (frozen):** drop the issue date if any of these fail: not enough history for *t−1*’s 21-day return (*t* index **< 22**); next 21 prints not yet in the file; sign at *t* is Flat; sign at *t−1* is Flat; realized next-21 sign is Flat.

**Metric:** walk-forward **hit-rate** = share of remaining issue dates where the call equals the realized next-21 sign.

**Beats continuation:** horse hit-rate **strictly greater** than continuation hit-rate on the **same** eligible dates. Tiny ≠ met. Tie ≠ pick.

### 5. Three arms (L-SPOT-ARMS)

Testing is **not** a training arm. Freeze:

| Arm | Job | May it change the frozen recipe? |
|-----|-----|----------------------------------|
| **Train** | Fit or update using **only prints dated < *t*** (past-only at issue date *t*) | Yes, **inside** a recipe written before discovery. These two horses have **no fitted coefficients** (train = N/A / identity). |
| **Select (discovery)** | Pick at most **one** horse per scoreboard vs continuation | Only pick / **no survivor**. No retune. No least-bad. |
| **Confirm** | Honest test on unseen last **500 / 250 / 750** issue dates | **No.** Confirm never trains, never selects, never retunes. |

Do **not** use last 500 / 250 / 750 to fit, pick, or tweak. Do **not** treat “we tested many ideas on the same tape” as training.

**Walk-forward note:** a later queued horse may update coefficients with yesterday’s outcome in **tomorrow’s** train set **only if** that update rule is written before discovery. Seeing confirm misses and inventing a new filter is a **different object**.

### 6. Horses (cap 2)

Unified eligible set as in §4 (so both horses and continuation always issue a call).

| ID | Skill call at *t* |
|----|-------------------|
| **H-SPOT-FLIP-HOLD** | **One-print hold:** call the 21-day sign as of **t−1**. Today’s completed print (and today’s descriptive flip) is **not** in that day’s skill call. The new sign enters the call on the **next** print. |
| **H-SPOT-REV** | Call the **opposite** of the 21-day sign as of *t*. |

Do **not** add a third horse after scores. Do **not** replace 21. Descriptive dashboard (latest *t*): report s_t, flip_t, continuation call, both horse calls — that is **not** a third scoreboard.

### 7. Discovery / confirm

| Slot | Rule |
|------|------|
| **Discovery cutoff** | Issue dates **≤ 2023-08-21** |
| **Discovery scoreboard** | Hit-rate vs continuation on last **500** eligible issue dates of that prefix |
| **Selection** | Highest hit-rate **only if** it **strictly beats** continuation. If neither → **no survivor** for that scoreboard |
| **Ties** (both beat, equal hit-rate) | Keep **H-SPOT-FLIP-HOLD** (earlier in this lock) |
| **Confirm** | That **one** horse (or skip). Last **500 / 250 / 750** eligible issue dates of the **full** file vs continuation. No runner-up. No re-hunt of confirm |
| **F-SKILL / promote** | **Does not apply.** This object is spot 21-day sign, not next-session CL RMSE. **L-SCREEN-Y-PROMOTE** is unchanged and **not** fired by a spot hit-rate |
| **Establishment-stop** | Honest `04` that would say **established** still **stops**. No DataMine auto-open. Not a trade |

Discovery **before** confirm. Scripts must be runnable as `--stage discovery` without computing confirm windows.

### 8. Exploration queue (L-SPOT-QUEUE)

Chip-away is **one named class per later pulse**, not an online learner.

Register: `QUEUE_Spot_Trend_Exploration.md` + `data/spot_trend_queue.json`.

**This pulse:** only **H-SPOT-FLIP-HOLD** and **H-SPOT-REV**. Queued classes below are **named enough to wait**, **not scored**.

**After scores:** if a horse fails discovery on a scoreboard, that **horse+scoreboard** row is **burned** for this object (same 21-day target, same tape family). Do **not** retune it. Do **not** remix with DJT / COT / gap.

**Queued (not this pulse):**

| Queue ID | Next class (freeze later in its own lock) |
|----------|-------------------------------------------|
| **C-SPOT-INV** | EIA weekly petroleum inventory **surprise** overlay on the same 21-day sign target |
| **C-SPOT-CROSS** | WTI 21-day sign as the call for Brent’s next 21 (and the reverse) — still two scoreboards |
| **C-SPOT-LOGIT** | Expanding-window logistic: features = last 21-day sign + absolute 21-day return, fit **past-only** (train arm used) |

Intuition belongs in **proposing the next frozen class**, not in editing this pulse after hit-rate. Bad calls teach the **project** (burn / next class), not the **horse**.

---

## What this does *not* do

- Does **not** establish F-SKILL, F-ON, F-DAY, F-CC, or V-VALUE.  
- Does **not** bring spot inside D-EXIST C3 (D-EXIST remains futures-target).  
- Does **not** say a green hit-rate is a trading system.  
- Does **not** let confirm or backtest rewrite the rule.  
- Does **not** license Phase 2, an oil offshoot, or DataMine.

**Lock-time Amb warning:** Running this hunt does **not** drop leftover-ambiguity on V-SRC. **Amb ≠ clearance.** Spot skill-met (if ever) ≠ CL skill-met.

---

## Reopen

`leave skill not shown` (F-SKILL parked) · `name horse …` on **this** object only via the **queue** (do **not** retune 21; do **not** unburn a failed row; do **not** use confirm as train) · `leave screen rule` (unchanged; not this object). Honest **established** still **stops**.
