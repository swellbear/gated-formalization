# Quantitative Evidence Rubric — EIA spot 21-day trend hunt pulse

**Date:** 2026-08-20  
**Application:** `2026-08_oil-futures-predictive-model`  
**Bar under test:** walk-forward hit-rate vs continuation on next 21-day spot sign; pick-one on discovery last 500 of prefix ≤ 2023-08-21; confirm never trains  
**Source / artifact:** `PULSE_Hunt_Spot_Trend.md` · `data/spot_trend_hunt_scores.json`

---

| # | Check | Result |
|---|-------|--------|
| 1 | **Sample definition** | **Yes** — discovery last 500 eligible issue dates of prefix ≤ 2023-08-21 (WTI 2021-08-24 … 2023-08-21; Brent 2021-08-27 … 2023-08-21); confirm last 250/500/750 **unseen** (and unused: no survivor) |
| 2 | **Costs / taxes / frictions** | **N/A** (direction hit-rate, not a book). V-VALUE unused |
| 3 | **Significance vs point estimate** | **Point only** — hit-rate comparison; no binomial test. Both horses **worse** than continuation on both boards |
| 4 | **Matched comparison** | **Partial** — two horses vs continuation on matching discovery windows; FRED reprint not EIA v2; not futures |
| 5 | **Sensitivity to sample window** | **Not run on confirm** — protocol forbids confirm without a survivor |
| 6 | **Print-match ≠ clearance** | **Yes** — a discovery loss is not a beat; not last-500 confirm; not F-SKILL-met; not a trade. Losing is not a license to change 21 |

---

## Already-included legs

| Leg | In base bar test? | Notes |
|-----|-------------------|-------|
| Continuation baseline | Y | Competitor; not a horse |
| 21-step log-return | Y | Frozen |
| Two scoreboards | Y | WTI-met ≠ Brent-met; **both** no survivor |
| Confirm 500+250+750 | Y | **Skipped** (no survivor) |
| Train arm (fitted) | N | N/A this pulse |
| NYMEX CL / ICE Brent | N | **OUT** |
| Year / 6-month / 5-day windows | N | **OUT** of this pulse |
| Queued C-SPOT-* classes | N | **OUT** of this pulse |

**If asked “what about a 63-day window or blending the two horses?”:** Already included as **frozen OUT**. Seeing two discovery losses does **not** reopen those knobs this pulse.

---

**Conflicted-source?** Conflicted FRED reprint of EIA spots — stand-in only.

**Bar decision:** **Not establish.** **Not refute.**

**Establishment-stop:** Would honest `04` declare established? **No.**

---

*Standing rule: Quantitative Evidence Rubric.*
