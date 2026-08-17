# Material Admission Check — mover-list census

**Date:** 2026-08-17  
**Parent application:** `2026-08_oil-futures-predictive-model`  
**Targeted gap:** **F-SKILL** / live [R-F-SKILL](RESIDUAL_BRANCH_MENU.md#r-f-skill) — whether a comprehensive exhaustive list exists of what can move next-session CL (or Brent) futures  
**Linked:** `03_Gap_Extraction_and_Ranking.md` · `Lock_Rank4_Nested_Split.md` · `Lock_FSRC_Leave_Unnamed.md` · `MAP_Futures_Target_Forecasting_Methods.md`  
**Intake:** `E_Package_Evidence_Intake_FT_Driver_Map.md`  
**Rubric:** `E_Quantitative_Evidence_Rubric_FT_Driver_Map.md`  
**Map:** `MAP_What_Can_Move_CL.md`

**Quote freeze:** F-SKILL = next-session CL front-month log-return, walk-forward RMSE vs last-settlement. F-SRC **leave unnamed** unless the operator names a class.

---

## Candidate Material Summary

**In plain language:** Checking whether anyone has listed **everything** that can move the thing we are scoring (tomorrow’s CL change versus today’s official close). They have not. They have buckets, calendars, and studies of a few scheduled prints.

**Source(s):** EIA seven-factor guide; Kilian (2009) / Kilian–Murphy (2014); Baumeister & Kilian (2016); Ye & Karali (2016); Geman & Li (2018); Demirer & Kutan (2010); CME/broker calendars; L-MAP-FT macro horse.

**Key content / finding (concise):**

| Result | Status |
|--------|--------|
| Exhaustive list of next-session CL movers | **Not found** (not a well-posed finite object) |
| Bucket taxonomies of oil **prices** | Exist (EIA 7; Kilian 3/4 shocks) — **different object** |
| Scheduled-news calendars | Exist — **not exhaustive**; “world events” unbounded |
| Inventory **surprises** move WTI **futures** at the print | **Shown** in event studies — **contemporaneous**, not F-SKILL |
| After the print, surprise often **does not** forecast remaining nearby return | Authors’ own efficiency-style finding — still not our RMSE bar |
| Oil still surprises despite better driver *kinds* | Baumeister–Kilian 2016 — **against** treating lists as complete |

---

## Admission Criteria

### 1. Relevance to Targeted Gap
- [x] Yes — the question is aimed at what could feed an F-SKILL information set  
- [ ] No  
- [x] Partially — taxonomies and event studies constrain **nearby** objects (monthly oil; announcement-day jumps), not every locked slot  

**Explanation:** Relevant as a **negative census** (no exhaustive list) plus kinship (inventories *do* move CL when they print). Not relevant as silent F-SKILL clearance or as filling F-SRC.

### 2. Consistency (Cons)
- [x] Yes  
- [ ] No  

**Any conflicts:** **Conflict if admitted as F-SKILL-met or as a named F-SRC class.** No conflict if admitted as **L-MAP-DRV: census executed, exhaustive list absent, bar not met, class still unnamed.**

---

## Admission Decision

- [x] **ADMIT** the map as evaluation: **L-MAP-DRV**  
- [ ] **ADMIT** F-SKILL **established** — **rejected**  
- [x] **REJECT** naming EIA seven factors / Kilian shocks / Ye–Karali inventory surprises as the **submitted** F-SRC class on this turn  
- [ ] **HOLD** the map (not run)

**Locked as:** **L-MAP-DRV** — census executed; exhaustive mover list **does not exist**; F-SRC remains **unnamed**; F-SKILL **not established** (not a refute).

**Amb effect:** Unchanged at **5.5**. A map is not a named vehicle. **Amb ≠ clearance.**

**Prod effect:** Live residual still the skill test. Knowing *kinds* of movers ≠ a named series.

---

## Establishment-stop drill (mandatory)

**Would honest `04` declare established?** **No** (F-SKILL).

Do **not** auto-declare skill because inventories move CL on Wednesday mornings. Print-match ≠ clearance. Partial match: every locked slot scored; bar **not** shrunk to announcement-day returns.

---

## Post-Incorporation Action

- [x] Record map + intake + rubric  
- [x] F-SRC still unnamed  
- [x] Stop for operator — do not invent a class; do not enter Phase 2  

**Would-be-met?** No. Continue recording; do not declare skill.

---

*Standing rule: Material Admission Check. Conservative calibration. Print-match ≠ clearance.*
