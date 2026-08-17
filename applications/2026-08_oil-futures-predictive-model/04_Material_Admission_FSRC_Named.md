# Material Admission Check — named CME tape pulse

**Date:** 2026-08-17  
**Parent application:** `2026-08_oil-futures-predictive-model`  
**Targeted gap:** **F-SRC** / F-SKILL (F-ON, F-DAY, F-CC)  
**Linked:** `Lock_FSRC_Named_CME_Tape.md` · `Lock_Session_Split.md` · `PULSE_Baseline_Session_RMSE.md`  
**Intake:** `E_Package_Evidence_Intake_FSRC_Named.md`  
**Rubric:** `E_Quantitative_Evidence_Rubric_FSRC_Named.md`

**Quote freeze:** F-SKILL / F-CC = next-session CL settlement log-return RMSE vs last settlement; L-SESS adds F-ON and F-DAY. Named class = CME official open/settle, roll R1.

---

## Candidate Material Summary

**In plain language:** You named the official CL tape and asked to measure night vs day vs the whole trip against “no change,” then optionally re-score Kearney–Shang. We named that class and tried to fetch the tape. We could not. We did not fake it with Yahoo.

**Source(s):** Operator-named class; CME DataMine as live home of official settlements; fetch failure this environment.

**Key content / finding:**

| Result | Status |
|--------|--------|
| F-SRC named (CME open/settle + R1) | **Admitted as vehicle** |
| G8 named (baseline RMSE; optional FTS) | **Admitted as meanings** |
| F-ON / F-DAY / F-CC RMSE | **Not computed** — live tape absent |
| Kearney–Shang RMSE re-score | **Not run** |
| F-SKILL established | **No** |
| Yahoo as live | **Rejected** this turn |

---

## Admission Criteria

### 1. Relevance to Targeted Gap
- [x] Yes  
- [ ] No  
- [x] Partially — class matches; sample missing  

**Explanation:** The named class is the right object. The pulse cannot score RMSE without stamps.

### 2. Consistency (Cons)
- [x] Yes  
- [ ] No  

**Any conflicts:** Conflict if Yahoo numbers were scored as live, or if “class named” were treated as skill-met. Avoided.

---

## Admission Decision

- [x] **ADMIT** **F-SRC-CME-TAPE** (named vehicle) and **L-PULSE-TAPE-0** (executed, not met)  
- [ ] **ADMIT** F-SKILL / F-ON / F-DAY / F-CC **established** — **rejected**  
- [x] **REJECT** unstipulated stand-in as live  
- [x] **HOLD** optional Kearney–Shang horse (no curve tape)

**Amb effect:** F-SRC 2 → **0**; G8 1 → **0**. Live vs stand-in remains **1** (now the live leftover). V-SRC **1**; V-COST **0.5**. **Amb = 2.5**. **Amb ≠ clearance.**

---

## Establishment-stop drill (mandatory)

**Would honest `04` declare established?** **No.**

Stop was **not** hit. Continue recording not-established. Do **not** auto-declare skill.

---

## Post-Incorporation Action

- [x] Record named lock + pulse (no numbers)  
- [x] Stop for operator on **live vs stand-in** (CME tape vs stipulated stand-in)  
- [x] Combo still parked  
- [x] No Phase 2; no invented class; not a trade  

---

*Standing rule: Material Admission Check. Conservative calibration. Print-match ≠ clearance.*
