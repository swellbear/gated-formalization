# Lock Record — named finite discovery/confirm pre-tell hunt

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Operator selection:** **C** `proceed with C` (named finite discovery/confirm pre-tell hunt)  
**App-local lock IDs:** **L-HUNT-PRETELL** · **L-STANDIN-Y-TELLS**  
**Status:** **IN FORCE as protocol + named drawer (cap = these eight horses).** Written **before** last-500 confirm scores. Confirm is **one** survivor (or none). F-SKILL **not** auto-established by running the hunt.

---

## 0. Plain-language framing

**What was decided:**  
The computer may hunt among **eight named recipes** that use a **short, pre-registered** list of other Yahoo series (dollar, gasoline, heating oil, equities, copper, 10-year yield). It may **only** look at older sessions while choosing. The last 250 / 500 / 750 sessions stay unseen until **one** winner is picked — and only if that winner already beat “no change” on the older window. If none beat “no change” there, the hunt **fails**; we do **not** take the least-bad and hope the recent window saves it.

**What this settles:**  
The drawer, the lag (so we do not peek at the same afternoon’s equity close), the cutoff, and the pick-one rule.

**What this does *not* settle:**  
That skill is shown. That a Yahoo win is live CME. That anyone should trade. That we will now search an unbounded kitchen sink.

---

## Named protocol (quote this)

**Scope:** **Under Rank 4 + L-SESS + F-SRC-CME-TAPE + L-STANDIN-Y-CLF + L-SCREEN-Y-PROMOTE + L-HUNT-PRETELL + L-STANDIN-Y-TELLS**.

This is a **capped named drawer**, not kinship family **D-KITCHEN** / Kearney–Shang Fund, and not an unbounded “A goes up, B goes up” search. Cap = **these eight horses**. Do **not** expand the drawer after seeing scores. Do **not** hunt on last 500. Do **not** use confirm to pick a runner-up.

### Discovery / confirm split

| Slot | Rule |
|------|------|
| **Discovery cutoff** | CL sessions with date **≤ 2023-08-21** (the day before last-750 first date **2023-08-22**). Last **250 / 500 / 750** are all unseen during selection. |
| **Discovery scoreboard** | F-CC RMSE vs 0 on the **last 500 sessions of that prefix**, walk-forward, min train **250**, using **only** data ≤ cutoff. |
| **Selection** | Among the eight, pick the **single** horse with **lowest** F-CC RMSE on discovery, **only if** it **strictly beats** 0 on that discovery 500. If **none** beat 0 → **no survivor**. Do **not** pick the least-bad. Report hunt failed at discovery. |
| **Ties** | If two discovery F-CC RMSEs are exactly equal and both beat 0, keep the **earlier** horse in the locked table below. Do not break ties with confirm. |
| **Confirm** | That **one** horse only (or skip if none). Score last **500 / 250 / 750** vs 0 on the full Yahoo `CL=F` tape. No going back to a runner-up on the same confirm window. |
| **Promote** | Still **L-SCREEN-Y-PROMOTE**. A Yahoo win is still **stand-in**, not live clearance, not F-SKILL-met. Tiny dips ≠ met. |
| **Establishment-stop** | Even a confirm beat is stand-in. Honest `04` that would say **established** still **stops**. Do **not** auto-open DataMine. |

### L-STANDIN-Y-TELLS (Yahoo vendor generics; not live CME)

| ID | Yahoo symbol | Role |
|----|--------------|------|
| DXY | `DX-Y.NYB` | dollar |
| RBOB | `RB=F` | gasoline |
| HO | `HO=F` | heating oil |
| SPX | `^GSPC` | equities |
| Copper | `HG=F` | industrial |
| TNX | `^TNX` | 10Y yield (log-change only if yield **> 0**) |

**OUT of this drawer (named, not silent):** Brent `BZ=F` (too same-object). USO (circular with oil). Unbounded extra tickers after seeing scores.

**Tell series construction:** daily Close. Align to each CL date as the **last tell close on or before** that CL date. `r_tell` on CL date *d* = log(as-of close on *d* / as-of close on the previous CL session). Missing as-of → `r_tell` is missing.

### Look-ahead (mandatory; uniform for all six)

SPX cash close is **4pm ET**. CL settle is ~**2:30pm ET**. Same-calendar-day equity close is **not** known at t−1 CL settle. To avoid a silent same-day peek, **all six** tells use this conservative lag:

| Window | Issued | Tell lag |
|--------|--------|----------|
| **F-ON / F-CC** | t−1 settle | `r_tell` **ending on CL date t−2** (tell closes on t−2 and t−3). Do **not** use t−1 tell close. |
| **F-DAY** | t open | `r_tell` **ending on CL date t−1** is OK (prior cash close known by next morning). |

### OLS / missing days

Shared machinery with **H-LAG-WF**: expanding OLS; intercept; min train **250**; rank-deficient or n_train < 250 → forecast **0**. Fit on all expanding days with **complete** features (including tells).  

If CL target or CL lags are missing (same as H-LAG) → **skip** that day (do not put it in RMSE).  
If CL y/x are present but a required tell is **missing** → forecast **0** that day and **keep the day** so n matches the CL baseline window as far as y/x allow.

### Eight horses (cap)

Univariate always-on (1–6). When the tell is present:

| Window | Features |
|--------|----------|
| **F-ON / F-CC** | `[1, r_ON,t−1, r_DAY,t−1, r_tell]` with tell lag **t−2** |
| **F-DAY** | `[1, r_ON,t, r_DAY,t−1, r_tell]` with tell lag **t−1** |

| # | Horse ID | Recipe |
|---|----------|--------|
| 1 | **H-TELL-DXY** | Univariate always-on; tell = DXY |
| 2 | **H-TELL-RBOB** | Univariate always-on; tell = RBOB |
| 3 | **H-TELL-HO** | Univariate always-on; tell = HO |
| 4 | **H-TELL-SPX** | Univariate always-on; tell = SPX |
| 5 | **H-TELL-HG** | Univariate always-on; tell = Copper |
| 6 | **H-TELL-TNX** | Univariate always-on; tell = TNX |
| 7 | **H-TELL-AND-DXY-RBOB** | Sparse: forecast **0** unless **both** DXY and RBOB `r_tell` (same lag as the window) are **nonzero and the same sign**. When on: OLS with **both** tells + CL lags. |
| 8 | **H-TELL-AND-RBOB-HO** | Sparse: forecast **0** unless **both** RBOB and HO `r_tell` (same lag as the window) are **nonzero and the same sign**. When on: OLS with **both** tells + CL lags. |

Sparse horses **fit** OLS on all expanding days with complete features; they **issue** the OLS forecast only on trigger days (same emit rule as H-SPARSE-CAL).

---

## What this does *not* do

- Does **not** establish F-SKILL, F-ON, F-DAY, F-CC, or V-VALUE.  
- Does **not** promote on F-ON/F-DAY alone or a tiny RMSE dip.  
- Does **not** license trading or start an oil offshoot.  
- Does **not** enter Phase 2.  
- Does **not** open DataMine unless **L-SCREEN-Y-PROMOTE** fires.  
- Does **not** convert the hunt into “we will find a model then it works.”  
- Does **not** use same-day SPX close for F-ON/F-CC.  
- Does **not** relabel leftover Yahoo months as historical CL1.

**Lock-time Amb warning:** Running a finite hunt does **not** drop leftover-ambiguity on V-SRC. **Amb ≠ clearance.**

---

## Reopen

`leave skill not shown` · `name horse …` (a **different** recipe; do **not** re-hunt this confirm window; do **not** expand this drawer after scores) · `leave screen rule`. Live CME **only if** **L-SCREEN-Y-PROMOTE** fires. Honest **established** still **stops**.
