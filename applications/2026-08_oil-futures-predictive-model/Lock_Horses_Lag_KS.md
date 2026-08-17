# Lock Record — named horses (lagged-return + Kearney–Shang)

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Operator selection:** `ok proceed` after recommended Yahoo month-chain stand-in, then score **both** recipes  
**App-local lock ID:** **H-LAG-WF** · **H-KS-FTS**  
**Status:** **IN FORCE as named skill horses.** H-LAG-WF scored. H-KS-FTS **not run** (no freeze-matching CL1–CL18 tape). F-SKILL **not established**.

---

## 0. Plain-language framing

**What was decided:**  
Two recipes are on the card. The simple one uses only yesterday’s night and day moves on Yahoo `CL=F`. The published curve method needs CL1–CL18 history, which Yahoo’s live month list does not provide.

**What this settles:**  
Which models are being tested. Naming is **not** a pass.

**What this does *not* settle:**  
That skill is shown. That anyone should trade. That Kearney–Shang was re-run.

---

## Named horses (quote this)

**H-LAG-WF — lagged-return expanding OLS on the Yahoo `CL=F` stand-in.**  
OOS = last **500** sessions (2024-08-20 … 2026-08-14), same holdout as the baseline pulse. Min train **250**. Intercept included. On this continuous generic `r_CC = r_ON + r_DAY`, so a third lag of `r_CC` is **not** used (that design is rank-deficient and collapses to the 0 forecast).

| Window | Issued | Target | Features |
|--------|--------|--------|----------|
| **F-ON** | t−1 settle | overnight log-return | 1, r_ON,t−1, r_DAY,t−1 |
| **F-DAY** | t open | day log-return | 1, r_ON,t, r_DAY,t−1 |
| **F-CC** | t−1 settle | close-to-close log-return | 1, r_ON,t−1, r_DAY,t−1 |

Rank-deficient or n_train < 250 → forecast **0** that day.

**H-KS-FTS — Kearney & Shang (2020) FTS re-score.**  
FPCA on generic **CL1–CL9, CL12, CL18** (99% variance / two functional PCs in the paper), damped-trend exponential smoothing of scores, expanding window, RMSE on log-returns vs no-change on F-ON / F-DAY / F-CC. **Not run** this pulse: Yahoo month chain is not historical CL1–CL18 (`Lock_Standin_Yahoo_Curve.md`).

---

## What this does *not* do

- Does **not** establish F-SKILL, F-ON, F-DAY, F-CC, or V-VALUE.  
- Does **not** license trading or start an oil offshoot.  
- Does **not** treat a tiny overnight RMSE dip as F-ON-met.  
- Does **not** enter Phase 2.

**Lock-time Amb warning:** Naming horses does **not** drop leftover-ambiguity on V-SRC. **Amb drop ≠ clearance.**

---

## Reopen

`name horse …` for a different recipe, or `live CME only` / a freeze-matching curve tape for H-KS-FTS. Honest **established** still **stops**.
