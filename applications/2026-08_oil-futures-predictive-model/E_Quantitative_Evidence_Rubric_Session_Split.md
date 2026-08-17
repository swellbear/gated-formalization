# Quantitative Evidence Rubric — session split

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Bars:** F-CC / F-ON / F-DAY RMSE vs matching no-change; F-COMBO not yet eligible.  
**Source / artifact:** `Lock_Session_Split.md` · `MAP_Session_Split.md`

---

| # | Check | Result |
|---|-------|--------|
| 1 | **Sample definition** | **No** freeze-matching CL official open/settle series submitted. USO 2006–2018 high-frequency is a **different** sample |
| 2 | **Costs / taxes / frictions** | **N/A** for RMSE bars. Timing-profit claims **excluded** from skill; V-VALUE uses **V2** and counts daily round-turns on a day/combo book |
| 3 | **Significance vs point estimate** | Zhang papers report **regression** significance on half-hours, not locked RMSE vs 0 |
| 4 | **Matched comparison** | **No** — do not collapse half-hour R² or USO timing profits into F-ON/F-DAY/F-CC |
| 5 | **Sensitivity to sample window** | Noted in those papers (EIA days vs other days). Untested on this freeze |
| 6 | **Print-match ≠ clearance** | **Yes** — “overnight component predicts last half-hour in USO” is kinship |

---

## Already-included legs

| Leg | In base bar test? | Notes |
|-----|-------------------|-------|
| F-CC next-session vs last settlement | Y | Parent F-SKILL; still not met |
| L-MAP-FT daily CL MAE/MCS | Y | Not a night/day split |
| L-MAP-DRV inventory **at the print** | Y | Not F-DAY RMSE vs 0 |
| USO first→last half-hour | N | Wrong object |
| F-COMBO | N | Parked until F-ON and F-DAY scored and rule named |

**If asked “what about Zhang overnight predicting the last half-hour?”:** Already in this rubric as **kinship** — not an omitted F-ON/F-DAY pass.

---

**Bar decision:** **Not establish** (all session skill bars). **Not refute.** **REJECT** as F-SRC.

**Establishment-stop:** Would honest `04` declare established? **No.**

---

*Standing rule: Quantitative evidence quality bar + already-included legs.*
