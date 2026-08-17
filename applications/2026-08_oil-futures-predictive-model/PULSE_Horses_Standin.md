# Pulse result — named horses vs no-change RMSE (Yahoo stand-in)

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Layer ID:** **L-PULSE-HORSES-1**  
**Locks:** `Lock_Horses_Lag_KS.md` · `Lock_Standin_Yahoo_Curve.md` · `Lock_Standin_Yahoo_CLF.md`  
**Live vs stand-in:** **Stand-in.** **No print scored to met.**

---

## 0. Plain-language framing

**What we did:** We named two recipes and tried to score both against “assume no change.” The simple lagged-return model ran on Yahoo `CL=F`. The published curve method did **not** run: Yahoo’s month list is not historical CL1–CL18.

**What this settles:** Numeric RMSE for **H-LAG-WF** on the same last-500 window as the baseline. Skill is still **not shown**. Not a trade.

---

## 1. H-LAG-WF (last 500 sessions, 2024-08-20 … 2026-08-14)

Expanding OLS; min train 250; features as locked (no redundant r_CC lag).

| Window | RMSE horse | RMSE 0 | n | Beats 0? |
|--------|------------|--------|---|----------|
| **F-ON** | **0.01283** | 0.01291 | 500 | tiny yes |
| **F-DAY** | **0.02670** | 0.02663 | 500 | **no** |
| **F-CC** | **0.02888** | 0.02869 | 500 | **no** |

Sensitivity: F-CC horse also **worse** than 0 on last 250 (0.03454 vs 0.03436) and last 750 (0.02582 vs 0.02569). Overnight tiny dip is **stable** on 250/750 and is **not** F-ON-met (stand-in; parent skill bar is F-CC; edge is small).

Do **not** promote the overnight dip to “night is predictable” or F-SKILL-met.

---

## 2. H-KS-FTS

**Not run.**

| Gate | Value |
|------|--------|
| Yahoo month symbols tried | 60 |
| Live / 404 | 38 / 22 (expired months 404) |
| Dates labeled CL1–CL18 among leftovers | 1944 — **wrong object** (far contracts ranked as CL1) |
| True-front dates with CL1–CL18 | **54** (2026-06-01 … 2026-08-17) |
| Need for 250+500 | **750** |

Nasdaq CHRIS `CME_CLn` in this environment: **HTTP 403** (feed deprecated). Not used as a silent substitute.

---

## 3. Establishment-stop drill

**Would honest `04` declare F-SKILL / F-CC / F-ON / F-DAY established?** **No.**

Parent F-CC horse **lost** to no-change on the declared OOS. A tiny overnight RMSE dip on a stand-in is not P-NonNegligible skill. Kearney–Shang was not scored.

**Would honest `04` declare those bars refuted?** **No.** One lagged OLS on Yahoo does not refute every recipe. Missing curve tape is not a refute of FTS.

---

## 4. Scripts / artifacts

- `scripts/cl_horses.py` · `scripts/fetch_yahoo_month_chain.py`  
- `data/horse_scores.json` · `data/clf_yahoo_month_chain.csv` · `data/clf_yahoo_month_chain_fetch.json`

---

*Not trading advice. Stand-in ≠ live. Tiny overnight dip ≠ skill-met. Missing curve ≠ FTS-met.*
