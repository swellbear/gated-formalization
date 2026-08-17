# Quantitative Evidence Rubric — DJT Truth Social hunt pulse

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Bar under test:** F-ON / F-DAY / F-CC RMSE vs no-change; F-SKILL = real shot of **beating** that baseline; promote gate as locked; hunt pick-one on discovery F-CC  
**Source / artifact:** `PULSE_Hunt_DJT.md` · `data/djt_hunt_scores.json`

---

| # | Check | Result |
|---|-------|--------|
| 1 | **Sample definition** | **Yes** — discovery last 500 of prefix ≤ 2023-08-21 (2021-08-25 … 2023-08-21); confirm last 250/500/750 **unseen** (and unused: no survivor) |
| 2 | **Costs / taxes / frictions** | **N/A** (RMSE skill). V-VALUE unused; V2 named but no book |
| 3 | **Significance vs point estimate** | **Point only** — RMSE comparison; no Diebold–Mariano. Both discovery F-CC RMSEs **equal** 0 (not a strict beat) |
| 4 | **Matched comparison** | **Partial** — two horses vs 0 on matching discovery window; stamps not official CME; UTC post date ≠ ET |
| 5 | **Sensitivity to sample window** | **Not run on confirm** — protocol forbids confirm without a survivor. Coverage: 0 nonzero discovery CL days |
| 6 | **Print-match ≠ clearance** | **Yes** — equal-to-0 is not a beat; not last-500 confirm; not live CME; not P-NonNegligible. All-zero session series is not a license to retune the lexicon |

---

## Already-included legs

| Leg | In base bar test? | Notes |
|-----|-------------------|-------|
| No-change = 0 | Y | Competitor |
| F-CC parent F-SKILL | Y | **Both tied** on discovery |
| Promote 500+250+750 | Y | **Does not fire** (no survivor) |
| Official CME open/settle | N | Stand-in |
| After-cost P/L | N | V-VALUE unused |
| Speeches / White House remarks | N | **OUT** of this pulse (named) |

**If asked “what about mapping weekend posts / adding a year average / loosening the lexicon?”:** Already included as **frozen OUT**. Seeing an all-zero series does **not** reopen those knobs this pulse.

---

**Conflicted-source?** Conflicted vendor generic + third-party scrape — stand-in only.

**Bar decision:** **Not establish.** **Not refute.**

**Establishment-stop:** Would honest `04` declare established? **No.**

---

*Standing rule: Quantitative Evidence Rubric.*
