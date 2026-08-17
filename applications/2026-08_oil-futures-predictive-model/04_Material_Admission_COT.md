# Material Admission Check — CFTC positioning hunt pulse

**Date:** 2026-08-17  
**Parent application:** `2026-08_oil-futures-predictive-model`  
**Targeted gap:** **F-SKILL** (two named CFTC managed-money horses vs no-change RMSE; discovery/confirm)  
**Linked:** `Lock_Hunt_COT.md` · `PULSE_Hunt_COT.md`  
**Intake:** `E_Package_Evidence_Intake_COT.md`  
**Rubric:** `E_Quantitative_Evidence_Rubric_COT.md`

**Quote freeze:** Rank 4 F-SKILL = next-session CL log-return RMSE vs last settlement (**F-CC**); L-SESS adds F-ON / F-DAY. Hunt = pick **one** horse only if it strictly beats 0 on discovery F-CC last 500 of prefix ≤ 2023-08-21. Promote = F-CC beat on last 500 **and** not-lose on 250/750. This pulse = stipulated Yahoo stand-in + locked CFTC drawer.

---

## Candidate Material Summary

**In plain language:** Two named weekly managed-money positioning recipes were scored on older sessions. **Neither** beat last settlement on the whole trip there. No winner went to the recent exam. This is not a pass.

**Source(s):** Yahoo `CL=F`; CFTC disagg futures-only 067651; operator 2026-08-17.

**Key content / finding:**

| Result | Status |
|--------|--------|
| Drawer named (two horses) | **Admitted as named recipes / protocol** |
| Discovery-span reports | **711** (≥30; vehicle **not** fail) |
| Discovery F-CC vs 0 | **Both lose** (0 = 0.026705; closest H-COT-NET 0.026796) |
| Survivor | **none** |
| Confirm | **skipped** |
| Promote gate | **does not fire** |
| F-SKILL established | **No** |

---

## Admission Criteria

### 1. Relevance to Targeted Gap
- [x] Yes — named finite hunt scored vs the locked baseline  
- [ ] No  
- [x] Partially — stamps not live CME  

**Explanation:** The leftover was “hunt among a named positioning drawer without peeking at last 500.” The drawer ran. It did not meet P-NonNegligible skill.

### 2. Consistency (Cons)
- [x] Yes  
- [ ] No  

**Any conflicts:** Conflict if a discovery F-CC loser were sent to confirm, or percent-of-OI were added after scores. Avoided.

---

## Admission Decision

- [x] **ADMIT** **L-HUNT-COT** / **L-STANDIN-CFTC-COT** (protocol + drawer) and **L-PULSE-COT-1** (evaluation)  
- [ ] **ADMIT** F-SKILL / F-ON / F-DAY / F-CC **established** — **rejected**  
- [x] **REJECT** picking a discovery F-CC loser, or adding percent-of-OI / other trader groups after scores  

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
