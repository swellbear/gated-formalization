# Material Admission Check — EIA spot 21-day trend hunt pulse

**Date:** 2026-08-20  
**Parent application:** `2026-08_oil-futures-predictive-model`  
**Targeted gap:** **R-SPOT-TREND** (two named spot 21-day horses vs continuation hit-rate; discovery/confirm). F-SKILL **parked** this pulse.  
**Linked:** `Lock_Hunt_Spot_Trend.md` · `PULSE_Hunt_Spot_Trend.md`  
**Intake:** `E_Package_Evidence_Intake_Spot_Trend.md`  
**Rubric:** `E_Quantitative_Evidence_Rubric_Spot_Trend.md`

**Quote freeze:** Pick **one** horse per scoreboard only if it strictly beats continuation on discovery hit-rate last 500 of prefix ≤ 2023-08-21. Confirm one survivor (or none). Confirm never trains. This pulse = stipulated EIA/FRED cash spots + locked two-horse drawer.

---

## Candidate Material Summary

**In plain language:** Two named 21-day spot rules were scored on older cash WTI and Brent days. **Neither** beat “the trend continues” there, on either oil. No winner went to the recent exam. This is not a pass, and it is not a futures skill test.

**Source(s):** FRED DCOILWTICO / DCOILBRENTEU (EIA-sourced); operator 2026-08-20.

**Key content / finding:**

| Result | Status |
|--------|--------|
| Drawer named (two horses, two boards, three arms, queue) | **Admitted as named recipes / protocol** |
| Discovery-eligible pool | WTI **9408** / Brent **9119** (≥250; vehicle **not** fail) |
| Discovery vs continuation | **Both horses lose on both boards** (WTI cont. 0.508; Brent 0.506) |
| Survivor | **none** (both boards) |
| Confirm | **skipped** |
| F-SKILL / Yahoo promote | **does not apply / does not fire** |
| Spot-trend skill established | **No** |

---

## Admission Criteria

### 1. Relevance to Targeted Gap
- [x] Yes — named finite hunt scored vs the locked continuation baseline  
- [ ] No  
- [x] Partially — FRED reprint; not a live cash desk; not F-SKILL  

**Explanation:** The leftover was “hunt among a named spot-trend drawer without peeking at last 500.” The drawer ran. It did not meet P-NonNegligible skill on this object.

### 2. Consistency (Cons)
- [x] Yes  
- [ ] No  

**Any conflicts:** Conflict if a discovery loser were sent to confirm, 21 were changed after scores, confirm were used as train, or this pulse were scored as F-CC. Avoided.

---

## Admission Decision

- [x] **ADMIT** **L-HUNT-SPOT-TREND** / **L-STANDIN-EIA-SPOT** / **L-SPOT-ARMS** / **L-SPOT-QUEUE** (protocol) and **L-PULSE-SPOT-1** (evaluation)  
- [ ] **ADMIT** spot-trend skill or F-SKILL **established** — **rejected**  
- [x] **REJECT** picking a discovery loser, changing 21 after scores, or using confirm as train  

**Amb effect:** Unchanged. V-SRC **1**. **Amb = 1.0**. **Amb ≠ clearance.**

---

## Establishment-stop drill (mandatory)

**Would honest `04` declare established?** **No.**

Stop was **not** hit. Confirm did **not** run. Continue recording not-established. Do **not** auto-declare skill. Do **not** auto-open DataMine.

---

## Post-Incorporation Action

- [x] Record hunt lock + numeric pulse  
- [x] Burned register updated; queued classes still not scored  
- [x] F-SKILL still **leave skill not shown**; V-VALUE still unnamed; no Phase 2; not a trade  

---

*Standing rule: Material Admission Check. Conservative calibration. Print-match ≠ clearance.*
