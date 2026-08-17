# Gate Scoring Sheet — After gap horses pulse

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Linked:** `04_Material_Admission_Gap.md` · `PULSE_Horses_Gap.md`  
**Scope:** **Under Rank 4 + L-SESS + L-STANDIN-Y-CLF + L-SCREEN-Y-PROMOTE + L-HUNT-GAP + V-COST-V2**

---

## 1. Cons

**Score:** **High** — F-DAY gap vs 0 on the declared windows does not clash with L₀. Clash avoided by not calling the small F-DAY dip a pass and not promoting after F-CC tied with 0.

**Compatible with L₀?** Yes.

---

## 2. Agree — secondary

**Score:** **Moderate** — careful readers of “small day fade, whole trip unchanged, does not promote” converge; slogan readers may hear “the fade model works.”

---

## 3. Prod — secondary

**Checkable consequences:** `python3 scripts/cl_gap_horses.py` reproduces `data/gap_horse_scores.json`. Promote `fires` is false. Survivor is H-GAP-FADE.

---

## 4. Amb

| Free Parameter | Weight | Status |
|----------------|--------|--------|
| G1–G7 / G-SESS / F-SRC / G8 / live-vs-stand-in / V-COST | **0** | Locked |
| **V-SRC** | **1** | Leave unnamed |

**Weighted sum:** **1.0**

**Amb ≠ clearance:** Scoring two day horses that **do not promote** does **not** establish skill or value.

---

## 5. Higher-Level Review

**Pass with caution** — leftover is still a **different named horse** (not a remix of this pair, not a pretell variation) or leave skill not shown. Live CME still gated on F-CC. Combo still unnamed.

---

## Final Verdict

- [x] **Provisional** (split: D-EXIST met; skill and value not)

**Reliability:** High for arithmetic on this CSV; low as live CME.  
**Next:** `leave skill not shown` · `name horse …` (a **different** recipe; do **not** remix this pair; do **not** re-hunt confirm) · `leave screen rule`. No Phase 2. Do **not** auto-open DataMine.

---

*Amb held 1.0. Amb ≠ clearance. Tiny ≠ met. Day win ≠ promote.*
