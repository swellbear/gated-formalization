# Quantitative Evidence Rubric — EIA inventory-surprise overlay pulse

**Date:** 2026-08-20  
**Application:** `2026-08_oil-futures-predictive-model`  
**Bar under test:** walk-forward hit-rate vs continuation on next 21-day spot sign; inventory overlay; pick-one on discovery last 500 of prefix ≤ 2023-08-21  
**Source / artifact:** `PULSE_Hunt_Spot_Inv.md` · `data/spot_inv_hunt_scores.json`

---

| # | Check | Result |
|---|-------|--------|
| 1 | **Sample definition** | **Yes** — same discovery 500 as Track B pulse 1; weekly WCESTUS1 1982-08-20 … 2026-08-14; confirm unused (no survivor) |
| 2 | **Costs / taxes / frictions** | **N/A** (direction hit-rate) |
| 3 | **Significance vs point estimate** | **Point only**. Both horses **worse** than continuation on both boards |
| 4 | **Matched comparison** | **Partial** — overlay vs continuation on matching dates; EIA HTML not v2 API; not Street surprise |
| 5 | **Sensitivity to sample window** | **Not run on confirm** — protocol forbids confirm without a survivor |
| 6 | **Print-match ≠ clearance** | **Yes** — a 0.506 vs 0.508 loss is not a beat; not Bloomberg; not F-SKILL-met |

---

## Already-included legs

| Leg | In base bar test? | Notes |
|-----|-------------------|-------|
| Continuation baseline | Y | Competitor |
| 21-step log-return | Y | Frozen; not retuned |
| Naive surprise (prior-4 WoW) | Y | Not Street consensus |
| Two scoreboards | Y | Both no survivor |
| Confirm 500+250+750 | Y | **Skipped** |
| Cushing-only / products / API / Bloomberg | N | **OUT** |
| Burned FLIP-HOLD / REV | N | **Not scored** |

**If asked “what about Cushing stocks or the survey number?”:** Already included as **frozen OUT**.

---

**Conflicted-source?** EIA HTML leaf — stand-in.

**Bar decision:** **Not establish.** **Not refute.**

**Establishment-stop:** Would honest `04` declare established? **No.**

---

*Standing rule: Quantitative Evidence Rubric.*
