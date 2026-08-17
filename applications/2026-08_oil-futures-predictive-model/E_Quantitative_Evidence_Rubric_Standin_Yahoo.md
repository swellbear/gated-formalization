# Quantitative Evidence Rubric — Yahoo CL=F stand-in pulse

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Bar under test:** F-ON / F-DAY / F-CC RMSE vs no-change (0); F-SKILL = real shot of **beating** that baseline  
**Source / artifact:** `PULSE_Standin_Yahoo_CLF_RMSE.md` · `data/clf_yahoo_standin.csv`

---

| # | Check | Result |
|---|-------|--------|
| 1 | **Sample definition** | **Yes** — Yahoo `CL=F` daily Open/Close; 2000-08-23 … 2026-08-14; n=6520 rows; OOS last 500 |
| 2 | **Costs / taxes / frictions** | **N/A** (RMSE skill). V-VALUE unused |
| 3 | **Significance vs point estimate** | **Point only** — RMSE of 0-forecast; no test that a rival model beats it |
| 4 | **Matched comparison** | **Partial** — windows match L-SESS; stamps **not** official CME; R1 **not** applied |
| 5 | **Sensitivity to sample window** | **Tested** — 250 / 500 / 750 / full; ranking F-DAY > F-ON stable on this tape |
| 6 | **Print-match ≠ clearance** | **Yes** — these RMSEs are the baseline, not a pass; Kearney–Shang MAE unused |

---

## Already-included legs

| Leg | In base bar test? | Notes |
|-----|-------------------|-------|
| No-change = 0 | Y | RMSE of 0 **is** window RMS |
| F-CC parent F-SKILL | Y | Baseline only; horse **not** scored |
| Official CME open/settle | N | Stand-in |
| Roll rule R1 | N | Constant `front_id` |
| Kearney–Shang FTS | N | Not run |
| After-cost P/L | N | V-VALUE unused |

**If asked “what about just using Yahoo as live?”:** Already excluded. Badge **stand-in**.

---

**Conflicted-source?** Conflicted vendor generic — stand-in only.

**Bar decision:** **Not establish.** **Not refute.** Baseline measured; skill horse absent.

**Establishment-stop:** Would honest `04` declare established? **No.**

---

*Standing rule: Quantitative evidence quality bar + already-included legs.*
