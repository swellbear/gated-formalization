# Material Admission Check — EIA spot expanding-window logistic pulse

**Date:** 2026-08-24  
**Parent application:** `2026-08_oil-futures-predictive-model`  
**Targeted gap:** **R-SPOT-TREND** (queued C-SPOT-LOGIT vs continuation). F-SKILL **parked**.  
**Linked:** `Lock_Hunt_Spot_Logit.md` · `PULSE_Hunt_Spot_Logit.md`  
**Intake:** `E_Package_Evidence_Intake_Spot_Logit.md`  
**Rubric:** `E_Quantitative_Evidence_Rubric_Spot_Logit.md`

**Quote freeze:** Pick one per board only if it strictly beats continuation on discovery last 500 of prefix ≤ 2023-08-21. Confirm never trains. Tiny ≠ met. Do not unburn prior rows. Do not change 21. Do not retune W2B.

---

## Candidate Material Summary

**In plain language:** Two named expanding-window logistic rules were fit on past-only days and scored. Both beat continuation on the older exam for WTI and Brent (tied with each other; FULL kept). On the recent exam the fuller rule **lost** to continuation on every locked window for both oils. This is not a futures skill test.

**Source(s):** existing EIA spot CSVs; operator **B** (C-SPOT-LOGIT).

**Key content / finding:**

| Result | Status |
|--------|--------|
| Drawer named (train arm used) | **Admitted as named recipes / protocol** |
| Successful fits on discovery 500 | **500 / 500** both boards |
| WTI discovery | FULL = SIGN **0.532** vs cont **0.508**; survivor **FULL** |
| Brent discovery | FULL = SIGN **0.550** vs cont **0.506**; survivor **FULL** |
| Confirm FULL both boards | **Lose** all of 500 / 250 / 750 |
| Spot-trend / F-SKILL established | **No** |

---

## Admission Criteria

### 1. Relevance to Targeted Gap
- [x] Yes — named queued class scored vs continuation  
- [ ] No  
- [x] Partially — FRED reprints; discovery≠confirm  

**Explanation:** The leftover was “next queued class without peeking at last 500.” The train-arm drawer ran. Discovery survivors failed confirm. Spot-trend skill remains not established.

### 2. Consistency (Cons)
- [x] Yes  
- [ ] No  

**Any conflicts:** Conflict if confirm were used to retune features, SIGN swapped after FULL confirm loss, 21 changed, or burned rows unburned. Avoided.

---

## Admission Decision

- [x] **ADMIT** **L-HUNT-SPOT-LOGIT** (protocol) and **L-PULSE-SPOT-LOGIT-1** (evaluation)  
- [ ] **ADMIT** spot-trend skill or F-SKILL **established** — **rejected**  
- [x] **REJECT** confirm-as-train, unburning, changing 21, or treating discovery alone as met  

**Amb effect:** Unchanged. V-SRC **1**. **Amb = 1.0**. **Amb ≠ clearance.**

---

## Establishment-stop drill (mandatory)

**Would honest `04` declare established?** **No.**

Stop was **not** hit. Continue recording not-established. Do **not** auto-open DataMine.

---

## Post-Incorporation Action

- [x] Record hunt lock + numeric pulse  
- [x] Queue empty after this class; F-SKILL still parked; no Phase 2; not a trade  

---

*Standing rule: Material Admission Check. Conservative calibration. Discovery ≠ confirm clearance.*
