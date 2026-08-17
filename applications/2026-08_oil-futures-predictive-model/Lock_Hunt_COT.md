# Lock Record — CFTC managed-money WTI positioning hunt

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Operator selection:** implement named CFTC positioning hunt (keep going, different class)  
**App-local lock IDs:** **L-HUNT-COT** · **L-STANDIN-CFTC-COT** · **H-COT-NET** · **H-COT-CHG**  
**Status:** **IN FORCE as protocol + named drawer (cap = these two horses).** Written **before** last-500 confirm scores. Confirm is **one** survivor (or none). F-SKILL **not** auto-established.

---

## 0. Plain-language framing

**What was decided:**  
Take the public weekly count of how many crude-oil futures “managed money” traders are long minus short. Use the latest report the computer was allowed to know, or the change from the week before. See whether either number beats “assume no change” on the next whole oil session. The computer may pick **one** of those two, only if it already beat no-change on **older** sessions. Percent-of-open-interest and other trader groups are **not** in this test.

**What this settles:**  
The CFTC file, the two features, the clock, the scale, and the two-horse cap.

**What this does *not* settle:**  
That specs drive crude. That skill is shown. That anyone should trade. That a Friday report should beat Monday’s settlement.

---

## Named protocol (quote this)

**Scope:** **Under Rank 4 + L-SESS + F-SRC-CME-TAPE + L-STANDIN-Y-CLF + L-SCREEN-Y-PROMOTE + L-HUNT-COT + L-STANDIN-CFTC-COT**.

This is a **capped named drawer**, not an unbounded positioning kitchen sink. Cap = **these two horses**. Do **not** expand after seeing scores. Do **not** hunt on last 500. Do **not** switch to percent-of-OI, producer/merchant, swap dealers, or options-combined after RMSE. Do **not** retune DJT / gap / pretell this pulse.

### 1. Archive (L-STANDIN-CFTC-COT)

CFTC **Disaggregated Futures-Only** Commitments of Traders. Contract **Crude Oil, Light Sweet – NEW YORK MERCANTILE EXCHANGE**, CFTC code **067651**.

Fields: report date; **Managed Money** long and short (all). Net = long − short.

Primary: CFTC public weekly / historical compressed `fut_disagg_txt_YYYY.zip` (and the current-week `f_disagg.txt` if needed to extend the last year). No Bloomberg. No “all traders” / legacy non-commercial mix. Options-combined **OUT** unless futures-only is missing (named fallback only; then **stop** if still empty).

**Named limitation:** third-party CFTC website files, not a live desk feed. Disaggregated history starts **2006-06-13**.

### 2. Feature (two horses)

| ID | Signal |
|----|--------|
| **H-COT-NET** | Latest known managed-money **net** (contracts), carried until the next report |
| **H-COT-CHG** | Week-over-week **change** in that net (0 until two reports exist) |

Carry-forward is required for a Friday report (unlike DJT silent-day = 0).

OLS scale: divide net (and the change) by **100000** (`1e5`). Frozen. Percent-of-OI **OUT**. Producer/merchant, swap dealers, other reportables **OUT**.

### 3. Clock

“Known as of” date *d* = latest report whose **release calendar date** is **≤ d**.

Release date = **Friday of the report week** (weekday Friday on or after the Tuesday-style report date; if the report date is already Friday, use that day). Named limitation: the file usually has no release timestamp; typical publication is Friday ~15:30 ET.

| Window | Issued | COT known as of |
|--------|--------|-----------------|
| **F-ON / F-CC** | t−1 settle | CL date **t−2** |
| **F-DAY** | t open | CL date **t−1** |

A Friday afternoon release therefore **never** enters that Friday’s F-CC (t−2 is Wednesday).

### 4. OLS

Expanding, intercept, min train **250**. F-ON/F-CC: `[1, r_ON,t−1, r_DAY,t−1, s]`. F-DAY: `[1, r_ON,t, r_DAY,t−1, s]`. `s` is the scaled H-COT-NET or H-COT-CHG value known as of the lagged date. Rank-deficient or n_train < 250 → **0**. Missing CL y/x → skip (same as H-LAG). Before the first known report, `s` = **0**.

### 5. Discovery / confirm

| Slot | Rule |
|------|------|
| **Discovery cutoff** | CL sessions **≤ 2023-08-21** |
| **Discovery scoreboard** | F-CC RMSE vs 0 on last **500** of that prefix |
| **Selection** | Lowest F-CC RMSE **only if** it **strictly beats** 0. If neither → **no survivor** |
| **Ties** | Keep **H-COT-NET** (earlier in this lock) |
| **Confirm** | That **one** horse (or skip). Last **500 / 250 / 750** vs 0. No runner-up |
| **Promote** | Still **L-SCREEN-Y-PROMOTE**. Yahoo win ≠ live ≠ F-SKILL-met |
| **Vehicle fail** | Fetch fails or discovery-span reports **< 30** → stop; do not invent a positioning series |
| **Establishment-stop** | Honest `04` that would say **established** still **stops**. No DataMine auto-open |

---

## What this does *not* do

- Does **not** establish F-SKILL, F-ON, F-DAY, F-CC, or V-VALUE.  
- Does **not** say specs drive crude.  
- Does **not** include EIA surprise, percent-of-OI, or other trader groups.  
- Does **not** license trading, start an oil offshoot, or enter Phase 2.

**Lock-time Amb warning:** Running this hunt does **not** drop leftover-ambiguity on V-SRC. **Amb ≠ clearance.**

---

## Reopen

`leave skill not shown` · `name horse …` (a **different** recipe; do **not** add percent-of-OI or other trader groups after scores) · `leave screen rule`. Live CME **only if** **L-SCREEN-Y-PROMOTE** fires. Honest **established** still **stops**.
