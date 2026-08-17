# Material Admission Check — DJT Truth Social hunt pulse

**Date:** 2026-08-17  
**Parent application:** `2026-08_oil-futures-predictive-model`  
**Targeted gap:** **F-SKILL** (two named Truth Social oil-sentiment horses vs no-change RMSE; discovery/confirm)  
**Linked:** `Lock_Hunt_DJT.md` · `PULSE_Hunt_DJT.md`  
**Intake:** `E_Package_Evidence_Intake_DJT.md`  
**Rubric:** `E_Quantitative_Evidence_Rubric_DJT.md`

**Quote freeze:** Rank 4 F-SKILL = next-session CL log-return RMSE vs last settlement (**F-CC**); L-SESS adds F-ON / F-DAY. Hunt = pick **one** horse only if it strictly beats 0 on discovery F-CC last 500 of prefix ≤ 2023-08-21. Promote = F-CC beat on last 500 **and** not-lose on 250/750. This pulse = stipulated Yahoo stand-in + locked Truth Social drawer.

---

## Candidate Material Summary

**In plain language:** Two named week/month averages of Trump oil-adjacent Truth posts were scored on older sessions. Both **tied** last settlement on the whole trip there (the daily score was always zero on those oil-session dates). No winner went to the recent exam. This is not a pass.

**Source(s):** Yahoo `CL=F`; CNN Truth Social dump; frozen `data/djt_oil_lexicon.json`; operator 2026-08-17.

**Key content / finding:**

| Result | Status |
|--------|--------|
| Drawer named (two horses) | **Admitted as named recipes / protocol** |
| Discovery-window oil-adjacent | **53** (≥30; vehicle **not** fail) |
| Discovery CL days with nonzero score | **0** |
| Discovery F-CC vs 0 | **Both tie** (0 = 0.026705) |
| Survivor | **none** |
| Confirm | **skipped** |
| Promote gate | **does not fire** |
| F-SKILL established | **No** |

---

## Admission Criteria

### 1. Relevance to Targeted Gap
- [x] Yes — named finite hunt scored vs the locked baseline  
- [ ] No  
- [x] Partially — stamps not live CME; UTC date; Truth Social only  

**Explanation:** The leftover was “hunt among a named dated-text drawer without peeking at last 500.” The drawer ran. It did not meet P-NonNegligible skill.

### 2. Consistency (Cons)
- [x] Yes  
- [ ] No  

**Any conflicts:** Conflict if a discovery F-CC tie were sent to confirm, or the lexicon were retuned after seeing zeros. Avoided.

---

## Admission Decision

- [x] **ADMIT** **L-HUNT-DJT** / **L-STANDIN-DJT-TRUTH** (protocol + drawer) and **L-PULSE-DJT-1** (evaluation)  
- [ ] **ADMIT** F-SKILL / F-ON / F-DAY / F-CC **established** — **rejected**  
- [x] **REJECT** picking a discovery F-CC tie, retuning the lexicon, mapping weekend posts, mixing speeches, or adding year/6-month/day windows after scores  

**Amb effect:** Unchanged. V-SRC **1**. **Amb = 1.0**. **Amb ≠ clearance.**

---

## Establishment-stop drill (mandatory)

**Would honest `04` declare established?** **No.**

Stop was **not** hit. Promote did **not** fire. Continue recording not-established. Do **not** auto-declare skill. Do **not** auto-open DataMine.

---

## Post-Incorporation Action

- [x] Record hunt lock + numeric pulse  
- [x] Combo still parked; V-VALUE still unnamed; zoo still capped at these two rows  
- [x] No Phase 2; no oil offshoot; not a trade  

---

*Standing rule: Material Admission Check. Conservative calibration. Print-match ≠ clearance.*
