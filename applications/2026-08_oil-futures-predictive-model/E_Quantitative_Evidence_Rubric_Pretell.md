# Quantitative Evidence Rubric — pretell hunt pulse

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Bar under test:** F-ON / F-DAY / F-CC RMSE vs no-change; F-SKILL = real shot of **beating** that baseline; promote gate as locked; hunt pick-one on discovery F-CC  
**Source / artifact:** `PULSE_Hunt_Pretell.md` · `data/pretell_hunt_scores.json`

---

| # | Check | Result |
|---|-------|--------|
| 1 | **Sample definition** | **Yes** — discovery last 500 of prefix ≤ 2023-08-21 (2021-08-25 … 2023-08-21); confirm last 250/500/750 **unseen** (and unused: no survivor) |
| 2 | **Costs / taxes / frictions** | **N/A** (RMSE skill). V-VALUE unused; V2 named but no book |
| 3 | **Significance vs point estimate** | **Point only** — RMSE comparison; no Diebold–Mariano. All eight discovery F-CC RMSEs **worse** than 0 |
| 4 | **Matched comparison** | **Partial** — eight horses vs 0 on matching discovery window; stamps not official CME |
| 5 | **Sensitivity to sample window** | **Not run on confirm** — protocol forbids confirm without a survivor. Discovery F-DAY tiny beats exist; they are **not** F-CC |
| 6 | **Print-match ≠ clearance** | **Yes** — a discovery F-DAY dip is not F-CC, not last-500 confirm, not live CME, not P-NonNegligible |

---

## Already-included legs

| Leg | In base bar test? | Notes |
|-----|-------------------|-------|
| No-change = 0 | Y | Competitor |
| F-CC parent F-SKILL | Y | **All eight lost** on discovery |
| Promote 500+250+750 | Y | **Does not fire** (no survivor) |
| Official CME open/settle | N | Stand-in |
| After-cost P/L | N | V-VALUE unused |

**If asked “what about TNX beating F-DAY on discovery?”:** Already included. Selection is **F-CC**. Tiny F-DAY ≠ survivor. Not a promote.

---

**Conflicted-source?** Conflicted vendor generic — stand-in only.

**Bar decision:** **Not establish.** **Not refute.**

**Establishment-stop:** Would honest `04` declare established? **No.**

---

*Standing rule: Quantitative Evidence Rubric.*
