# Quantitative Evidence Rubric — EIA spot expanding-window logistic pulse

**Date:** 2026-08-24  
**Application:** `2026-08_oil-futures-predictive-model`  
**Bar under test:** walk-forward hit-rate vs continuation on next 21-day spot sign; expanding past-only logistic; pick-one on discovery last 500 of prefix ≤ 2023-08-21; confirm last 500/250/750  
**Source / artifact:** `PULSE_Hunt_Spot_Logit.md` · `data/spot_logit_hunt_scores.json`

---

| # | Check | Result |
|---|-------|--------|
| 1 | **Sample definition** | **Yes** — same discovery 500 as prior Track B pulses; confirm last 500/250/750 of full eligible file |
| 2 | **Costs / taxes / frictions** | **N/A** (direction hit-rate) |
| 3 | **Significance vs point estimate** | **Point only**. Discovery **beat**; confirm **worse** than continuation every window both boards |
| 4 | **Matched comparison** | **Partial** — horse vs continuation on matching dates; FRED reprints; walk-forward refit |
| 5 | **Sensitivity to sample window** | Confirm ran; all three windows lose both boards |
| 6 | **Print-match ≠ clearance** | **Yes** — discovery beat is not confirm clearance and not F-SKILL-met |

---

## Already-included legs

| Leg | In base bar test? | Notes |
|-----|-------------------|-------|
| Continuation baseline | Y | Competitor |
| 21-step log-return | Y | Frozen |
| Expanding past-only logistic | Y | Min train 50 |
| Two horses FULL / SIGN | Y | Tie → FULL |
| Confirm 500+250+750 | Y | **Lost** both boards |
| Peer / inventory / W2B remix | N | **OUT** |
| Burned prior horses | N | **Not scored** |

**If asked “what about adding the Brent CROSS survivor into the fit?”:** Already included as **frozen OUT** (do not retune W2B).

---

**Conflicted-source?** FRED EIA reprints — stand-in.

**Bar decision:** **Not establish.** **Not refute.**

**Establishment-stop:** Would honest `04` declare established? **No.**

---

*Standing rule: Quantitative Evidence Rubric.*
