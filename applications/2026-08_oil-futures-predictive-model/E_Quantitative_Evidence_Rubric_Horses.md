# Quantitative Evidence Rubric — named horses pulse

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Bar under test:** F-ON / F-DAY / F-CC RMSE vs no-change; F-SKILL = real shot of **beating** that baseline  
**Source / artifact:** `PULSE_Horses_Standin.md` · `data/horse_scores.json`

---

| # | Check | Result |
|---|-------|--------|
| 1 | **Sample definition** | **Yes** for H-LAG — same last-500 Yahoo `CL=F` window as the baseline. **No** for H-KS (54 true-front dates) |
| 2 | **Costs / taxes / frictions** | **N/A** (RMSE skill). V-VALUE unused; V2 named but no book |
| 3 | **Significance vs point estimate** | **Point only** — RMSE comparison; no Diebold–Mariano / MCS |
| 4 | **Matched comparison** | **Partial** — H-LAG vs 0 on matching windows; stamps not official CME; KS unmatched |
| 5 | **Sensitivity to sample window** | **Tested** for H-LAG — 250 / 500 / 750; F-CC horse **worse** than 0 on all three |
| 6 | **Print-match ≠ clearance** | **Yes** — Kearney–Shang 2009–15 MAE unused; overnight dip not promoted |

---

## Already-included legs

| Leg | In base bar test? | Notes |
|-----|-------------------|-------|
| No-change = 0 | Y | Competitor for H-LAG |
| F-CC parent F-SKILL | Y | H-LAG **lost** |
| Official CME open/settle | N | Stand-in |
| Kearney–Shang FTS | N | Tape fail; not run |
| After-cost P/L | N | V-VALUE unused |

**If asked “what about the overnight win?”:** Already included as a reported window. It does **not** replace F-CC. Stand-in. Tiny. Not F-ON-met.

---

**Conflicted-source?** Conflicted vendor generic — stand-in only.

**Bar decision:** **Not establish.** **Not refute.**

**Establishment-stop:** Would honest `04` declare established? **No.**

---

*Standing rule: Quantitative Evidence Rubric.*
