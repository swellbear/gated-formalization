# Quantitative Evidence Rubric — gap horses pulse

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Bar under test:** F-DAY RMSE vs no-change for the named gap horses; parent F-SKILL remains **F-CC**; promote gate as locked  
**Source / artifact:** `PULSE_Horses_Gap.md` · `data/gap_horse_scores.json`

---

| # | Check | Result |
|---|-------|--------|
| 1 | **Sample definition** | **Yes** — discovery last 500 of prefix ≤ 2023-08-21; confirm last 250/500/750 unseen during selection |
| 2 | **Costs / taxes / frictions** | **N/A** (RMSE skill). V-VALUE unused; flattening book unnamed |
| 3 | **Significance vs point estimate** | **Point only** — no Diebold–Mariano. Discovery F-DAY edge **0.000003**; confirm last-500 F-DAY edge **0.000050** |
| 4 | **Matched comparison** | **Partial** — both horses vs 0 on matching F-DAY windows; stamps not official CME; F-CC not a skill test here (locked to 0) |
| 5 | **Sensitivity to sample window** | **Tested on confirm F-DAY** — 250 / 500 / 750 all small beats for FADE. F-CC tied with 0 on all three |
| 6 | **Print-match ≠ clearance** | **Yes** — a small F-DAY RMSE dip is not F-CC, not live CME, not P-NonNegligible |

---

## Already-included legs

| Leg | In base bar test? | Notes |
|-----|-------------------|-------|
| No-change = 0 | Y | Competitor |
| F-DAY exhibit | Y | FADE small confirm beats; **not** treated as met |
| F-CC parent F-SKILL | Y | Locked to 0; **does not beat** |
| Promote 500+250+750 | Y | **Does not fire** |
| Official CME open/settle | N | Stand-in |
| After-cost P/L / flatten book | N | V-VALUE / F-COMBO unused |

**If asked “what about fade beating the day on last 500?”:** Already included. Tiny. Stand-in. Not F-CC. Not a promote. Not F-DAY-met under P-NonNegligible as used in this app.

---

**Conflicted-source?** Conflicted vendor generic — stand-in only.

**Bar decision:** **Not establish.** **Not refute.**

**Establishment-stop:** Would honest `04` declare established? **No.**

---

*Standing rule: Quantitative Evidence Rubric.*
