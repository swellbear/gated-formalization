# Quantitative Evidence Rubric — EIA spot WTI↔Brent cross-bench overlay pulse

**Date:** 2026-08-24  
**Application:** `2026-08_oil-futures-predictive-model`  
**Bar under test:** walk-forward hit-rate vs continuation on next 21-day spot sign; peer-sign overlay; pick-one on discovery last 500 of prefix ≤ 2023-08-21; confirm last 500/250/750 if survivor  
**Source / artifact:** `PULSE_Hunt_Spot_Cross.md` · `data/spot_cross_hunt_scores.json`

---

| # | Check | Result |
|---|-------|--------|
| 1 | **Sample definition** | **Yes** — same discovery 500 as prior Track B pulses; confirm Brent last 500/250/750 of full eligible file (last 750 overlaps discovery prefix by inherited rule) |
| 2 | **Costs / taxes / frictions** | **N/A** (direction hit-rate) |
| 3 | **Significance vs point estimate** | **Point only**. WTI horse **worse**. Brent horse strictly greater on discovery and three confirm windows; confirm **250 is +1 hit** |
| 4 | **Matched comparison** | **Partial** — overlay vs continuation on matching home-board dates; FRED reprints; same-day peer print allowed |
| 5 | **Sensitivity to sample window** | Confirm ran on Brent only. 500 and 750 beat by +11 / +15; 250 is **tiny** |
| 6 | **Print-match ≠ clearance** | **Yes** — a Brent point-beat is not F-SKILL-met, not both-board skill-met, and not a lead–lag theorem. Tiny ≠ met |

---

## Already-included legs

| Leg | In base bar test? | Notes |
|-----|-------------------|-------|
| Continuation baseline | Y | Competitor |
| 21-step log-return | Y | Frozen; not retuned |
| Peer sign (date ≤ t, carry) | Y | Flat/missing → continuation |
| Two scoreboards | Y | WTI no survivor; Brent survivor |
| Confirm 500+250+750 | Y | Brent only; WTI **skipped** |
| Dollar spread / crack / fade-of-peer / futures | N | **OUT** |
| Burned FLIP-HOLD / REV / INV | N | **Not scored** |

**If asked “what about the WTI–Brent dollar spread?”:** Already included as **frozen OUT**.

---

**Conflicted-source?** FRED EIA reprints — stand-in.

**Bar decision:** **Not establish.** **Not refute.**

**Establishment-stop:** Would honest `04` declare established? **No.**

---

*Standing rule: Quantitative Evidence Rubric.*
