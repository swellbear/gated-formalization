# Quantitative Evidence Rubric — named CME tape pulse

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Bars:** F-ON / F-DAY / F-CC RMSE vs no-change (0). Optional FTS not in the base bar.  
**Source / artifact:** `PULSE_Baseline_Session_RMSE.md` · `Lock_FSRC_Named_CME_Tape.md`

---

| # | Check | Result |
|---|-------|--------|
| 1 | **Sample definition** | **Stated** (CL official open/settle, R1). **Not in hand.** n = 0 computed |
| 2 | **Costs / taxes / frictions** | **N/A** (RMSE skill). V-VALUE unused |
| 3 | **Significance vs point estimate** | **Neither** — no RMSE computed |
| 4 | **Matched comparison** | **Not scored.** Do not collapse Kearney–Shang MAE or USO half-hours into this bar |
| 5 | **Sensitivity to sample window** | **Declared** (500 / 250 / 750 holdout) — **untested** (no tape) |
| 6 | **Print-match ≠ clearance** | **Yes** — published FTS MAE is kinship, unused as a pass |

---

## Already-included legs

| Leg | In base bar test? | Notes |
|-----|-------------------|-------|
| No-change = 0 | Y | Baseline; RMSE of 0 **is** window RMS |
| F-CC parent F-SKILL | Y | Not computed |
| Kearney–Shang FTS MAE 2009–15 | N | Optional horse, different loss; **not run** |
| Yahoo / `CL=F` | N | Stand-in, **not stipulated** |

**If asked “what about just using Yahoo?”:** Already in this rubric as **excluded stand-in**. Stipulating it is an operator act.

---

**Bar decision:** **Not establish.** **Not refute.** Tape missing.

**Establishment-stop:** Would honest `04` declare established? **No.**

---

*Standing rule: Quantitative evidence quality bar + already-included legs.*
