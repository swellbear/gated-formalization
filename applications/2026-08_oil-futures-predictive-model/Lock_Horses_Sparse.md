# Lock Record — sparse horses (calendar + vol-state)

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Operator selection:** **B** `name horse H-SPARSE-CAL + H-SPARSE-VOL`  
**App-local lock ID:** **H-SPARSE-CAL** · **H-SPARSE-VOL**  
**Status:** **IN FORCE as named skill horses (cap = these two rows).** Pulse **L-PULSE-SPARSE-1** scored. Neither promotes. F-SKILL **not established**.

---

## 0. Plain-language framing

**What was decided:**  
Two — and only two — new recipes. Both usually predict **“no change.”** They only make a non-zero forecast when a condition that was **known at issue time** says so. One condition is “tomorrow is a scheduled EIA or FOMC day.” The other is “yesterday’s whole-trip move was in the top fifth of history so far.”

**What this settles:**  
Which two horses are on the card. Naming is **not** a pass.

**What this does *not* settle:**  
That skill is shown. That anyone should trade. That we will now try a zoo of other inputs.

---

## Named horses (quote this)

Shared machinery with **H-LAG-WF** (`Lock_Horses_Lag_KS.md`): Yahoo `CL=F` stand-in; OOS last **500** sessions (same holdout as the baseline); expanding OLS; min train **250** on **all** valid past observations of that window (not only triggered days); intercept included; same features; no redundant `r_CC` lag; rank-deficient or n_train < 250 → **0**.

**Emit rule (the sparsity):** on a session, if the window’s trigger is **false**, the forecast is **0**. If **true**, the forecast is the H-LAG OLS forecast. OLS is **fit on all expanding days**; it is **issued only on trigger days**. That is gated H-LAG, not a separate event-day regression.

| Window | Issued | Target | Features (when triggered) |
|--------|--------|--------|---------------------------|
| **F-ON** | t−1 settle | overnight log-return | 1, r_ON,t−1, r_DAY,t−1 |
| **F-DAY** | t open | day log-return | 1, r_ON,t, r_DAY,t−1 |
| **F-CC** | t−1 settle | close-to-close log-return | 1, r_ON,t−1, r_DAY,t−1 |

**H-SPARSE-CAL — calendar trigger.**  
Session date *t* is a trigger day if it is an **EIA WPSR release date** or a **regularly scheduled FOMC announcement date** (second day of the two-day meeting). Calendar known at t−1 settle. **Not** the inventory surprise or the rate decision itself.

- **FOMC list:** `data/sparse_calendar.json` (`fomc_announcement_dates`), from [Fed FOMC calendars](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm) retrieved 2026-08-17. Coverage **2021–2026**. Notation votes **OUT**. Unscheduled meetings **OUT**. Pre-2021 sessions: EIA-only for this horse.
- **EIA default:** Wednesday on the Yahoo tape; if that Wednesday is missing, next tape session with date ≤ Wednesday+6.
- **EIA holiday overrides:** same JSON (`eia_holiday_overrides`), from [EIA WPSR schedule](https://www.eia.gov/petroleum/supply/weekly/schedule.php) retrieved 2026-08-17. Those alternates **replace** that week’s Wednesday. Pre-table years may still tag Wednesday when EIA printed Thursday — named limitation, not a silent scrape.

**H-SPARSE-VOL — volatility-state trigger.**  
Trigger if **yesterday’s |r_CC|** is at or above the **80th percentile** of expanding history of |r_CC| through yesterday (inclusive). Require **≥ 250** past |r_CC| observations before any trigger; else **false**. Same trigger for F-ON, F-DAY, and F-CC (do **not** sneak in this morning’s overnight as a VOL trigger).

**Cap:** these two rows. No third architecture. No USD kitchen sink. No curve. No combo.

**Sensitivity:** also print last **250** and last **750** F-CC vs 0 (promote gate).

---

## What this does *not* do

- Does **not** establish F-SKILL, F-ON, F-DAY, F-CC, or V-VALUE.  
- Does **not** promote on F-ON/F-DAY alone or a tiny overnight dip.  
- Does **not** license trading or start an oil offshoot.  
- Does **not** enter Phase 2.  
- Does **not** open DataMine unless **L-SCREEN-Y-PROMOTE** fires.

**Lock-time Amb warning:** Naming two horses does **not** drop leftover-ambiguity on V-SRC. **Amb ≠ clearance.**

---

## Reopen

`leave skill not shown` · `name horse …` (a **different** front-only recipe; do **not** expand this pair into a zoo) · `leave screen rule`. Live CME **only if** **L-SCREEN-Y-PROMOTE** fires. Honest **established** still **stops**.
