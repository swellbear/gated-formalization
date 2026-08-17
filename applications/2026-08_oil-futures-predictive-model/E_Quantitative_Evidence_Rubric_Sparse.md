# Quantitative Evidence Rubric — sparse horses pulse

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Bar under test:** F-ON / F-DAY / F-CC RMSE vs no-change; F-SKILL = real shot of **beating** that baseline; promote gate as locked  
**Source / artifact:** `PULSE_Horses_Sparse.md` · `data/horse_scores.json`

---

| # | Check | Result |
|---|-------|--------|
| 1 | **Sample definition** | **Yes** — same last-500 Yahoo `CL=F` window as the baseline |
| 2 | **Costs / taxes / frictions** | **N/A** (RMSE skill). V-VALUE unused; V2 named but no book |
| 3 | **Significance vs point estimate** | **Point only** — RMSE comparison; no Diebold–Mariano. The CAL F-CC 500 edge is **0.000004** |
| 4 | **Matched comparison** | **Partial** — both horses vs 0 on matching windows; stamps not official CME |
| 5 | **Sensitivity to sample window** | **Tested** — 250 / 500 / 750. CAL F-CC **loses** on 750. VOL F-CC **loses** on all three |
| 6 | **Print-match ≠ clearance** | **Yes** — a last-500 tiny beat is not last-750, not live CME, not P-NonNegligible |

---

## Already-included legs

| Leg | In base bar test? | Notes |
|-----|-------------------|-------|
| No-change = 0 | Y | Competitor |
| F-CC parent F-SKILL | Y | CAL tiny 500 only; VOL **lost** |
| Promote 500+250+750 | Y | **Neither fires** |
| Official CME open/settle | N | Stand-in |
| After-cost P/L | N | V-VALUE unused |

**If asked “what about the calendar horse beating last 500?”:** Already included. It **fails** last 750. Stand-in. Tiny. Not F-CC-met. Not a promote.

---

**Conflicted-source?** Conflicted vendor generic — stand-in only.

**Bar decision:** **Not establish.** **Not refute.**

**Establishment-stop:** Would honest `04` declare established? **No.**

---

*Standing rule: Quantitative Evidence Rubric.*
