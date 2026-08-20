# Material Admission Check — EIA inventory-surprise overlay pulse

**Date:** 2026-08-20  
**Parent application:** `2026-08_oil-futures-predictive-model`  
**Targeted gap:** **R-SPOT-TREND** (queued C-SPOT-INV overlay vs continuation). F-SKILL **parked**.  
**Linked:** `Lock_Hunt_Spot_Inv.md` · `PULSE_Hunt_Spot_Inv.md`  
**Intake:** `E_Package_Evidence_Intake_Spot_Inv.md`  
**Rubric:** `E_Quantitative_Evidence_Rubric_Spot_Inv.md`

**Quote freeze:** Pick **one** horse per scoreboard only if it strictly beats continuation on discovery last 500 of prefix ≤ 2023-08-21. Do not unburn FLIP-HOLD/REV. Do not change 21. Confirm never trains.

---

## Candidate Material Summary

**In plain language:** Two named weekly-inventory overlay rules were scored on older cash WTI and Brent days. **Neither** beat “the trend continues.” No winner went to the recent exam. This is not a Street-poll test and not a futures skill test.

**Source(s):** EIA PET.WCESTUS1.W HTML leaf; existing spot CSVs; operator **B** 2026-08-20.

**Key content / finding:**

| Result | Status |
|--------|--------|
| Drawer named (two overlay horses) | **Admitted as named recipes / protocol** |
| Weekly reports ≤ discovery cutoff | **1963** / **1892** (≥30; vehicle **not** fail) |
| Discovery vs continuation | **Both horses lose on both boards** (closest WTI CONT 0.506 vs 0.508) |
| Survivor | **none** |
| Confirm | **skipped** |
| Spot-trend / F-SKILL established | **No** |

---

## Admission Criteria

### 1. Relevance to Targeted Gap
- [x] Yes — named queued class scored vs continuation  
- [ ] No  
- [x] Partially — naive surprise ≠ survey; HTML leaf not v2 API  

**Explanation:** The leftover was “next queued class without peeking at last 500.” The overlay ran. It did not meet P-NonNegligible skill on this object.

### 2. Consistency (Cons)
- [x] Yes  
- [ ] No  

**Any conflicts:** Conflict if a discovery loser were sent to confirm, 21 changed, FLIP-HOLD/REV unburned, or Bloomberg substituted after scores. Avoided.

---

## Admission Decision

- [x] **ADMIT** **L-HUNT-SPOT-INV** / **L-STANDIN-EIA-INV** (protocol) and **L-PULSE-SPOT-INV-1** (evaluation)  
- [ ] **ADMIT** spot-trend skill or F-SKILL **established** — **rejected**  
- [x] **REJECT** picking a discovery loser, unburning, changing 21, or confirm-as-train  

**Amb effect:** Unchanged. V-SRC **1**. **Amb = 1.0**. **Amb ≠ clearance.**

---

## Establishment-stop drill (mandatory)

**Would honest `04` declare established?** **No.**

Stop was **not** hit. Continue recording not-established. Do **not** auto-open DataMine.

---

## Post-Incorporation Action

- [x] Record hunt lock + numeric pulse  
- [x] Burned register updated (INV rows + prior FLIP-HOLD/REV)  
- [x] Next queue **C-SPOT-CROSS**; F-SKILL still parked; no Phase 2; not a trade  

---

*Standing rule: Material Admission Check. Conservative calibration. Print-match ≠ clearance.*
