# Material Admission Check — sparse horses pulse

**Date:** 2026-08-17  
**Parent application:** `2026-08_oil-futures-predictive-model`  
**Targeted gap:** **F-SKILL** (H-SPARSE-CAL + H-SPARSE-VOL vs no-change RMSE)  
**Linked:** `Lock_Horses_Sparse.md` · `PULSE_Horses_Sparse.md`  
**Intake:** `E_Package_Evidence_Intake_Sparse.md`  
**Rubric:** `E_Quantitative_Evidence_Rubric_Sparse.md`

**Quote freeze:** Rank 4 F-SKILL = next-session CL log-return RMSE vs last settlement (**F-CC**); L-SESS adds F-ON / F-DAY. Promote = F-CC beat on last 500 **and** not-lose on 250/750. This pulse = stipulated Yahoo stand-in + two named sparse horses.

---

## Candidate Material Summary

**In plain language:** Two recipes that usually predict no-change were scored. The calendar one had a **tiny** whole-trip improvement on last 500 and **lost** on last 750. The big-move one **lost** on the whole trip. Neither buys official CME. This is not a pass.

**Source(s):** Yahoo `CL=F`; pre-registered EIA/FOMC calendar; operator **B** 2026-08-17.

**Key content / finding:**

| Result | Status |
|--------|--------|
| Horses named (H-SPARSE-CAL, H-SPARSE-VOL) | **Admitted as named recipes** |
| CAL F-CC last 500 | 0.02868990 vs 0 0.02869369 — tiny dip; **not** F-CC-met |
| CAL F-CC last 750 | 0.025690 vs 0.025689 — **loss** |
| VOL F-CC last 500 | 0.02885 vs 0.02869 — **loss** |
| Promote gate | **Neither fires** |
| F-SKILL established | **No** |

---

## Admission Criteria

### 1. Relevance to Targeted Gap
- [x] Yes — named horses and scored vs the locked baseline  
- [ ] No  
- [x] Partially — stamps not live CME  

**Explanation:** The leftover was “name a horse and score it.” These two rows ran. They did not meet P-NonNegligible skill.

### 2. Consistency (Cons)
- [x] Yes  
- [ ] No  

**Any conflicts:** Conflict if the 0.000004 last-500 dip were called F-SKILL-met or a promote. Avoided.

---

## Admission Decision

- [x] **ADMIT** **H-SPARSE-CAL** / **H-SPARSE-VOL** (named) and **L-PULSE-SPARSE-1** (evaluation)  
- [ ] **ADMIT** F-SKILL / F-ON / F-DAY / F-CC **established** — **rejected**  
- [x] **REJECT** treating the CAL last-500 tiny dip as met or as a promote  
- [x] **REJECT** expanding this pair into a zoo this turn  

**Amb effect:** Unchanged. V-SRC **1**. **Amb = 1.0**. **Amb ≠ clearance.**

---

## Establishment-stop drill (mandatory)

**Would honest `04` declare established?** **No.**

Stop was **not** hit. Promote did **not** fire. Continue recording not-established. Do **not** auto-declare skill. Do **not** auto-open DataMine.

---

## Post-Incorporation Action

- [x] Record sparse lock + numeric pulse  
- [x] Combo still parked; V-VALUE still unnamed; zoo still capped at these two rows  
- [x] No Phase 2; no oil offshoot; not a trade  

---

*Standing rule: Material Admission Check. Conservative calibration. Print-match ≠ clearance.*
