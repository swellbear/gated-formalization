# Material Admission Check — gap horses pulse

**Date:** 2026-08-17  
**Parent application:** `2026-08_oil-futures-predictive-model`  
**Targeted gap:** **F-DAY** exhibit under L-SESS; parent **F-SKILL** remains **F-CC**  
**Linked:** `Lock_Horses_Gap.md` · `PULSE_Horses_Gap.md`  
**Intake:** `E_Package_Evidence_Intake_Gap.md`  
**Rubric:** `E_Quantitative_Evidence_Rubric_Gap.md`

**Quote freeze:** Rank 4 F-SKILL = F-CC RMSE vs last settlement. L-SESS adds F-ON / F-DAY as **separate** scoreboards. This pulse = two named gap horses on F-DAY; F-ON/F-CC locked to 0; promote = F-CC beat on last 500 **and** not-lose on 250/750.

---

## Candidate Material Summary

**In plain language:** After a large overnight gap, “fade the day” barely beat no-change on an older day exam and still beat, by a small amount, on the recent day exam. The whole trip was left as no-change. That is **not** a pass on skill, and it does **not** buy official CME.

**Source(s):** Yahoo `CL=F`; operator 2026-08-17 `ok proceed with your suggested route`.

**Key content / finding:**

| Result | Status |
|--------|--------|
| Horses named (H-GAP-FADE, H-GAP-CONT) | **Admitted as named recipes** |
| Discovery F-DAY FADE | 0.02584386 vs 0 0.02584659 — tiny beat; **survivor** |
| Discovery F-DAY CONT | **loss** |
| Confirm F-DAY last 500 | 0.026584 vs 0 0.026634 — small beat; **not** F-DAY-met |
| F-CC last 500 | **tie** with 0 (forecast locked to 0) |
| Promote gate | **does not fire** |
| F-SKILL / F-DAY established | **No** |

---

## Admission Criteria

### 1. Relevance to Targeted Gap
- [x] Yes — named day horses scored vs the locked F-DAY baseline  
- [ ] No  
- [x] Partially — stamps not live CME; parent bar is F-CC  

**Explanation:** The leftover authorized was “name the gap fade/continuation day test.” It ran. It did not meet P-NonNegligible skill.

### 2. Consistency (Cons)
- [x] Yes  
- [ ] No  

**Any conflicts:** Conflict if the small F-DAY confirm dip were called F-SKILL-met or a promote. Avoided.

---

## Admission Decision

- [x] **ADMIT** **H-GAP-FADE** / **H-GAP-CONT** (named) and **L-HUNT-GAP** / **L-PULSE-GAP-1** (evaluation)  
- [ ] **ADMIT** F-SKILL / F-ON / F-DAY / F-CC **established** — **rejected**  
- [x] **REJECT** treating the small F-DAY dip as met or as a promote  
- [x] **REJECT** expanding this pair or sending CONT to confirm this turn  

**Amb effect:** Unchanged. V-SRC **1**. **Amb = 1.0**. **Amb ≠ clearance.**

---

## Establishment-stop drill (mandatory)

**Would honest `04` declare established?** **No.**

Stop was **not** hit. Promote did **not** fire. Continue recording not-established. Do **not** auto-declare skill. Do **not** auto-open DataMine.

---

## Post-Incorporation Action

- [x] Record gap lock + numeric pulse  
- [x] Combo still parked; V-VALUE still unnamed; zoo still capped at these two rows  
- [x] No Phase 2; no oil offshoot; not a trade  

---

*Standing rule: Material Admission Check. Conservative calibration. Print-match ≠ clearance.*
