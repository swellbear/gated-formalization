# Material Admission Check — pretell hunt pulse

**Date:** 2026-08-17  
**Parent application:** `2026-08_oil-futures-predictive-model`  
**Targeted gap:** **F-SKILL** (eight named tell horses vs no-change RMSE; discovery/confirm)  
**Linked:** `Lock_Hunt_Pretell.md` · `PULSE_Hunt_Pretell.md`  
**Intake:** `E_Package_Evidence_Intake_Pretell.md`  
**Rubric:** `E_Quantitative_Evidence_Rubric_Pretell.md`

**Quote freeze:** Rank 4 F-SKILL = next-session CL log-return RMSE vs last settlement (**F-CC**); L-SESS adds F-ON / F-DAY. Hunt = pick **one** horse only if it strictly beats 0 on discovery F-CC last 500 of prefix ≤ 2023-08-21. Promote = F-CC beat on last 500 **and** not-lose on 250/750. This pulse = stipulated Yahoo stand-in + locked tell drawer.

---

## Candidate Material Summary

**In plain language:** Eight named “other series then oil” recipes were scored on older sessions. **None** beat last settlement on the whole trip there. No winner went to the recent exam. This is not a pass.

**Source(s):** Yahoo `CL=F`; Yahoo DXY / RBOB / HO / SPX / HG / TNX; operator **C** 2026-08-17.

**Key content / finding:**

| Result | Status |
|--------|--------|
| Drawer named (eight horses) | **Admitted as named recipes / protocol** |
| Discovery F-CC vs 0 | **All eight lose** (0 = 0.026705; closest H-TELL-SPX 0.026765) |
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

**Explanation:** The leftover was “hunt among a named drawer without peeking at last 500.” The drawer ran. It did not meet P-NonNegligible skill.

### 2. Consistency (Cons)
- [x] Yes  
- [ ] No  

**Any conflicts:** Conflict if a discovery F-CC loser were sent to confirm, or a tiny F-DAY dip were called a survivor. Avoided.

---

## Admission Decision

- [x] **ADMIT** **L-HUNT-PRETELL** / **L-STANDIN-Y-TELLS** (protocol + drawer) and **L-PULSE-PRETELL-1** (evaluation)  
- [ ] **ADMIT** F-SKILL / F-ON / F-DAY / F-CC **established** — **rejected**  
- [x] **REJECT** picking the least-bad discovery F-CC loss, or treating a tiny F-DAY dip as a survivor  
- [x] **REJECT** expanding this drawer or re-hunting the same confirm window this turn  

**Amb effect:** Unchanged. V-SRC **1**. **Amb = 1.0**. **Amb ≠ clearance.**

---

## Establishment-stop drill (mandatory)

**Would honest `04` declare established?** **No.**

Stop was **not** hit. Promote did **not** fire. Continue recording not-established. Do **not** auto-declare skill. Do **not** auto-open DataMine.

---

## Post-Incorporation Action

- [x] Record hunt lock + numeric pulse  
- [x] Combo still parked; V-VALUE still unnamed; zoo still capped at these eight rows  
- [x] No Phase 2; no oil offshoot; not a trade  

---

*Standing rule: Material Admission Check. Conservative calibration. Print-match ≠ clearance.*
