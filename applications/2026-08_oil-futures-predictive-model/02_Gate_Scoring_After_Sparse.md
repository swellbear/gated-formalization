# Gate Scoring Sheet — After sparse horses pulse

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Linked:** `04_Material_Admission_Sparse.md` · `PULSE_Horses_Sparse.md`  
**Scope:** **Under Rank 4 + L-SESS + L-STANDIN-Y-CLF + L-SCREEN-Y-PROMOTE + H-SPARSE-CAL + H-SPARSE-VOL + V-COST-V2**

---

## 1. Cons

**Score:** **High** — gated OLS vs 0 on the declared window does not clash with L₀. Clash avoided by not calling the 0.000004 last-500 dip a pass and not promoting after a 750 loss.

**Compatible with L₀?** Yes.

---

## 2. Agree — secondary

**Score:** **Moderate** — careful readers of “tiny 500 beat, lost on 750, does not promote” converge; slogan readers may hear “the calendar model works.”

---

## 3. Prod — secondary

**Checkable consequences:** `python3 scripts/cl_horses.py` reproduces `data/horse_scores.json`. Promote `fires` is false for both rows.

---

## 4. Amb

| Free Parameter | Weight | Status |
|----------------|--------|--------|
| G1–G7 / G-SESS / F-SRC / G8 / live-vs-stand-in / V-COST | **0** | Locked |
| **V-SRC** | **1** | Leave unnamed |

**Weighted sum:** **1.0**

**Amb ≠ clearance:** Scoring two horses that **do not promote** does **not** establish skill or value.

---

## 5. Higher-Level Review

**Pass with caution** — leftover is still a **different named horse** (not an expansion of this pair) or leave skill not shown. Live CME still gated.

---

## Final Verdict

- [x] **Provisional** (split: D-EXIST met; skill and value not)

**Reliability:** High for arithmetic on this CSV; low as live CME.  
**Next:** `leave skill not shown` · `name horse …` (a **different** recipe; do **not** grow this zoo) · `leave screen rule`. No Phase 2. Do **not** auto-open DataMine.

---

*Amb held 1.0. Amb ≠ clearance. Tiny ≠ met. Failed 750 ≠ promote.*
