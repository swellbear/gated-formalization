# Material Admission Check — EIA spot WTI↔Brent cross-bench overlay pulse

**Date:** 2026-08-24  
**Parent application:** `2026-08_oil-futures-predictive-model`  
**Targeted gap:** **R-SPOT-TREND** (queued C-SPOT-CROSS overlay vs continuation). F-SKILL **parked**.  
**Linked:** `Lock_Hunt_Spot_Cross.md` · `PULSE_Hunt_Spot_Cross.md`  
**Intake:** `E_Package_Evidence_Intake_Spot_Cross.md`  
**Rubric:** `E_Quantitative_Evidence_Rubric_Spot_Cross.md`

**Quote freeze:** Pick the board’s horse only if it strictly beats continuation on discovery last 500 of prefix ≤ 2023-08-21. Do not unburn FLIP-HOLD/REV/INV. Do not change 21. Confirm never trains. Tiny ≠ met. WTI-met ≠ Brent-met.

---

## Candidate Material Summary

**In plain language:** Two named cross-bench rules were scored. Using Brent’s 21-day label to call WTI **lost** on older days (confirm skipped). Using WTI’s 21-day label to call Brent **beat** older days and also beat continuation on the three recent windows; the shortest recent window was a **one-hit** margin. This is not a futures skill test and not a dollar-spread test.

**Source(s):** existing EIA spot CSVs; operator **B** (C-SPOT-CROSS).

**Key content / finding:**

| Result | Status |
|--------|--------|
| Drawer named (two board-specific horses) | **Admitted as named recipes / protocol** |
| Peer Up/Down on discovery 500 | **500 / 500** both boards (vehicle **not** fail) |
| WTI discovery | **B2W loses** 0.494 vs 0.508; **no survivor** |
| Brent discovery | **W2B beats** 0.528 vs 0.506; survivor **H-SPOT-CROSS-W2B** |
| Brent confirm 500 / 250 / 750 | Strictly greater; **250 is +1 hit (tiny)** |
| Spot-trend / F-SKILL established | **No** |

---

## Admission Criteria

### 1. Relevance to Targeted Gap
- [x] Yes — named queued class scored vs continuation  
- [ ] No  
- [x] Partially — same-day peer sign ≠ lead–lag; FRED reprints not live EIA v2  

**Explanation:** The leftover was “next queued class without peeking at last 500.” The overlay ran. Brent is a protocol survivor with confirm point-beats. That does **not** meet P-NonNegligible skill on this object (WTI fail; tiny 250).

### 2. Consistency (Cons)
- [x] Yes  
- [ ] No  

**Any conflicts:** Conflict if B2W were sent to confirm, 21 changed, burned rows unburned, W2B retuned after confirm, or a spread substituted after scores. Avoided.

---

## Admission Decision

- [x] **ADMIT** **L-HUNT-SPOT-CROSS** (protocol) and **L-PULSE-SPOT-CROSS-1** (evaluation)  
- [ ] **ADMIT** spot-trend skill or F-SKILL **established** — **rejected**  
- [x] **REJECT** picking the WTI discovery loser, unburning, changing 21, confirm-as-train, or treating tiny 250 as met  

**Amb effect:** Unchanged. V-SRC **1**. **Amb = 1.0**. **Amb ≠ clearance.**

---

## Establishment-stop drill (mandatory)

**Would honest `04` declare established?** **No.**

Stop was **not** hit. Continue recording not-established. Do **not** auto-open DataMine.

---

## Post-Incorporation Action

- [x] Record hunt lock + numeric pulse  
- [x] Burned register updated (B2W on WTI; prior rows stay burned)  
- [x] Next queue **C-SPOT-LOGIT**; F-SKILL still parked; no Phase 2; not a trade  

---

*Standing rule: Material Admission Check. Conservative calibration. Tiny ≠ met. Print-match ≠ clearance.*
