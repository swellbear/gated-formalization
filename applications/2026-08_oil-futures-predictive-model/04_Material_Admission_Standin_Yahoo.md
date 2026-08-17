# Material Admission Check — Yahoo CL=F stand-in pulse

**Date:** 2026-08-17  
**Parent application:** `2026-08_oil-futures-predictive-model`  
**Targeted gap:** Live vs stand-in; F-SKILL (F-ON, F-DAY, F-CC)  
**Linked:** `Lock_Standin_Yahoo_CLF.md` · `PULSE_Standin_Yahoo_CLF_RMSE.md`  
**Intake:** `E_Package_Evidence_Intake_Standin_Yahoo.md`  
**Rubric:** `E_Quantitative_Evidence_Rubric_Standin_Yahoo.md`

**Quote freeze:** F-SKILL / F-CC = next-session CL log-return RMSE vs last settlement; L-SESS adds F-ON and F-DAY. Live class = CME official open/settle. This pulse = stipulated Yahoo stand-in.

---

## Candidate Material Summary

**In plain language:** You allowed Yahoo `CL=F` as a weaker tape. We scored night / day / whole-trip against “assume no change.” Those are baseline sizes, not a model that beats last price.

**Source(s):** Yahoo `CL=F` chart API; operator stipulation.

**Key content / finding:**

| Result | Status |
|--------|--------|
| Stand-in stipulated (Yahoo Open/Close) | **Admitted as vehicle** |
| F-ON RMSE (last 500) | **0.01291** (n=500) — baseline, **not** skill-met |
| F-DAY RMSE (last 500) | **0.02663** (n=500) — baseline, **not** skill-met |
| F-CC RMSE (last 500) | **0.02869** (n=500) — baseline, **not** skill-met |
| Kearney–Shang RMSE re-score | **Not run** |
| F-SKILL established | **No** |
| Yahoo as live CME | **Rejected** |

---

## Admission Criteria

### 1. Relevance to Targeted Gap
- [x] Yes — closes the tape fork and computes the named RMSE  
- [ ] No  
- [x] Partially — official stamps and R1 still unmatched  

**Explanation:** The leftover was live vs stand-in. Stipulation + fetch constrain that fork. They do not meet P-NonNegligible skill.

### 2. Consistency (Cons)
- [x] Yes  
- [ ] No  

**Any conflicts:** Conflict if Yahoo were labeled live, or if baseline RMSE were called a pass. Avoided.

---

## Admission Decision

- [x] **ADMIT** **L-STANDIN-Y-CLF** and **L-PULSE-STANDIN-1** (stand-in baseline RMSE)  
- [ ] **ADMIT** F-SKILL / F-ON / F-DAY / F-CC **established** — **rejected**  
- [x] **REJECT** Yahoo as live CME  
- [x] **HOLD** optional Kearney–Shang horse (no curve tape)

**Amb effect:** Live vs stand-in 1 → **0**. V-SRC **1**; V-COST **0.5**. **Amb = 1.5**. **Amb ≠ clearance.**

---

## Establishment-stop drill (mandatory)

**Would honest `04` declare established?** **No.**

Stop was **not** hit. Continue recording not-established. Do **not** auto-declare skill.

---

## Post-Incorporation Action

- [x] Record stand-in lock + numeric pulse  
- [x] Combo still parked  
- [x] No Phase 2; no oil offshoot; not a trade  

---

*Standing rule: Material Admission Check. Conservative calibration. Print-match ≠ clearance.*
