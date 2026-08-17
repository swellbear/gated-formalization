# Material Admission Check — named horses pulse

**Date:** 2026-08-17  
**Parent application:** `2026-08_oil-futures-predictive-model`  
**Targeted gap:** **F-SKILL** (H-LAG-WF + H-KS-FTS vs no-change RMSE)  
**Linked:** `Lock_Horses_Lag_KS.md` · `Lock_Standin_Yahoo_Curve.md` · `PULSE_Horses_Standin.md`  
**Intake:** `E_Package_Evidence_Intake_Horses.md`  
**Rubric:** `E_Quantitative_Evidence_Rubric_Horses.md`

**Quote freeze:** Rank 4 F-SKILL = next-session CL log-return RMSE vs last settlement (**F-CC**); L-SESS adds F-ON / F-DAY. Live class = CME official. This pulse = stipulated Yahoo stand-in + named horses.

---

## Candidate Material Summary

**In plain language:** We scored a simple lagged-return model against “assume no change.” It did **not** beat the whole-trip baseline. A tiny overnight improvement is not a pass. The published curve method could not run: Yahoo does not keep expired months.

**Source(s):** Yahoo `CL=F` and month-chain chart API; operator `ok proceed` 2026-08-17.

**Key content / finding:**

| Result | Status |
|--------|--------|
| Horses named (H-LAG-WF, H-KS-FTS) | **Admitted as named recipes** |
| H-LAG F-ON last 500 | 0.01283 vs 0 0.01291 — tiny dip; **not** F-ON-met |
| H-LAG F-DAY last 500 | 0.02670 vs 0 0.02663 — **loss** |
| H-LAG F-CC last 500 | 0.02888 vs 0 0.02869 — **loss** (parent bar) |
| H-KS-FTS | **Not run** (54 true-front dates; need 750) |
| F-SKILL established | **No** |
| Yahoo month chain as historical CL1–CL18 | **Rejected** |

---

## Admission Criteria

### 1. Relevance to Targeted Gap
- [x] Yes — named horses and scored H-LAG vs the locked baseline  
- [ ] No  
- [x] Partially — H-KS tape fail; stamps not live CME  

**Explanation:** The leftover was “name a horse and score it.” That ran for H-LAG. It did not meet P-NonNegligible skill.

### 2. Consistency (Cons)
- [x] Yes  
- [ ] No  

**Any conflicts:** Conflict if the overnight dip were called F-SKILL-met, or leftover far months were called CL1. Avoided.

---

## Admission Decision

- [x] **ADMIT** **H-LAG-WF** / **H-KS-FTS** (named) and **L-PULSE-HORSES-1** (evaluation)  
- [x] **ADMIT** **L-STANDIN-Y-CHAIN** as attempted curve stand-in (**tape fail** for historical CL1–CL18)  
- [ ] **ADMIT** F-SKILL / F-ON / F-DAY / F-CC **established** — **rejected**  
- [x] **REJECT** Yahoo month leftovers as freeze-matching CL1–CL18  
- [x] **HOLD** H-KS-FTS score (no tape)

**Amb effect:** Unchanged. V-SRC **1**. **Amb = 1.0**. **Amb ≠ clearance.**

---

## Establishment-stop drill (mandatory)

**Would honest `04` declare established?** **No.**

Stop was **not** hit. Parent F-CC horse lost. Continue recording not-established. Do **not** auto-declare skill.

---

## Post-Incorporation Action

- [x] Record horse lock + numeric pulse  
- [x] Combo still parked; V-VALUE still unnamed  
- [x] No Phase 2; no oil offshoot; not a trade  

---

*Standing rule: Material Admission Check. Conservative calibration. Print-match ≠ clearance.*
