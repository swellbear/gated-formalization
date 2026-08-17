# Map — overnight vs daytime oil (evaluation only)

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Layer ID:** **L-MAP-SESS** (evaluation — not F-ON/F-DAY/F-CC-met; not a named class)  
**Freeze quoted:** **L-SESS** + parent **F-CC** (Rank 4 F-SKILL).  
**Scope:** Under Rank 4 + L-SESS. Do **not** fill F-SRC.

**Glossary:** [`docs/READER_GLOSSARY.md`](../../docs/READER_GLOSSARY.md)

---

## 0. Plain-language framing

**What we’re doing:** After locking night vs day as **separate tests**, check whether published work has already run **those** tests (RMSE vs no-change on CL official open/settlement).

**Short answer:** People have studied **intraday momentum** and **overnight vs daytime** oil **returns**, often on **USO** (an ETF) or on **half-hour** slices, often as a **trading-rule** story. That is **not** F-ON or F-DAY as locked. Closest kinship still does **not** clear the bars.

---

## 1. Families

| ID | Family | Object | Vs F-ON / F-DAY / F-CC | Hold / shrink |
|----|--------|--------|-------------------------|---------------|
| **S-USO-IM** | Zhang et al. (2021), *Economic Modelling* 95; SSRN 3553682 | **USO ETF** high-frequency, 2006–2018. First half-hour return predicts last half-hour; overnight **component of** the first half-hour carries more of that signal | **Schema fail** (ETF ≠ NYMEX CL open/settlement log-return RMSE vs 0) | Authors: in-sample/OOS **half-hour** predictability + a market-timing **profit** claim. Inventory volume pattern **does not** predict last half-hour. **Must not** be promoted |
| **S-EIA-IM** | Zhang et al. (2023), *Energy Journal* 44(5) | Intraday momentum **around EIA** 10:30 ET (third half-hour predicts last half-hour on announcement days; else first half-hour / overnight component) | Nearby **F-DAY** kinship (day-session news). **Not** open-to-settlement RMSE vs 0 | Announcement-day pattern **differs** from other days. Trading-rule “gains” are **V-VALUE-adjacent**, not the RMSE bar, not V1/V2 |
| **S-TAIL** | Wang, Bouri, Xu & Zhang (2023), *Energy Economics* 127 | Intraday vs overnight **tail risk** / extreme-return predictability in crude oil | Wrong **object** (tails, not mean RMSE vs no-change) | Kinship that night and day are **different**. Not freeze-met |
| **S-CC** | L-MAP-FT daily CL papers | Settlement-ish **daily** curve / CL generics | **F-CC** kinship already scored; **not** a night/day split | Unchanged: closest daily CL MAE ≠ locked RMSE |

**Event-study inventory jumps (Ye–Karali; Geman–Li):** already on L-MAP-DRV. They explain a **print**, not F-DAY RMSE vs 0 for the whole open-to-settle window.

---

## 2. What remains untested on L-SESS

1. **F-ON:** NYMEX CL front-month, official settlement → next official open, walk-forward RMSE vs overnight no-change, standing public series.  
2. **F-DAY:** same contract, official open → same-day settlement, walk-forward RMSE vs day no-change.  
3. **F-CC:** still untested as originally locked (L-HUNT-PROVEN / L-MAP-FT).  
4. **F-COMBO:** named switching rule written in advance, after 1–2 are scored, walk-forward; then V1 or V2 if after-cost.

**Not untested:** That overnight and daytime oil returns can be **talked about separately**. That first-half-hour / overnight **components** show up in **USO** half-hour regressions. That EIA days look different **intraday**.

---

## 3. Establishment-stop drill

**Would honest `04` declare F-ON, F-DAY, F-CC, or F-COMBO established?** **No.**

USO ≠ CL. Half-hour momentum ≠ open-to-settle RMSE vs no-change. “Substantial profits” ≠ V1/V2. Print-match ≠ clearance.

**F-SRC:** stays unnamed. Do **not** silently pick Zhang et al. as the class.

---

*Evaluation census. Not trading advice. Not blended-slogan clearance.*
