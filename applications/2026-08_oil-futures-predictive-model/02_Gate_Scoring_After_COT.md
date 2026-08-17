# Gate Scoring Sheet — After CFTC positioning hunt pulse

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Linked:** `04_Material_Admission_COT.md` · `PULSE_Hunt_COT.md`  
**Scope:** **Under Rank 4 + L-SESS + L-STANDIN-Y-CLF + L-SCREEN-Y-PROMOTE + L-HUNT-COT + L-STANDIN-CFTC-COT + V-COST-V2**

---

## 1. Cons

**Score:** **High** — discovery/confirm vs 0 on the declared prefix does not clash with L₀. Clash avoided by not sending a discovery F-CC loser to confirm and not adding percent-of-OI after scores.

**Compatible with L₀?** Yes.

---

## 2. Agree — secondary

**Score:** **Moderate** — careful readers of “both lose on discovery F-CC, no survivor, confirm skipped” converge; slogan readers may hear “we scored specs so a model exists” or “specs don’t move oil.”

---

## 3. Prod — secondary

**Checkable consequences:** `python3 scripts/cl_cot_hunt.py` reproduces `data/cot_hunt_scores.json`. `survivor.id` is null. Promote `fires` is false.

---

## 4. Amb

| Free Parameter | Weight | Status |
|----------------|--------|--------|
| G1–G7 / G-SESS / F-SRC / G8 / live-vs-stand-in / V-COST | **0** | Locked |
| **V-SRC** | **1** | Leave unnamed |

**Weighted sum:** **1.0**

**Amb ≠ clearance:** Scoring two horses that **do not survive discovery** does **not** establish skill or value.

---

## 5. Higher-Level Review

**Pass with caution** — leftover is still a **different named horse** (not a re-hunt of this confirm window, not percent-of-OI / other trader groups after scores) or leave skill not shown. Live CME still gated.

---

## Final Verdict

- [x] **Provisional** (split: D-EXIST met; skill and value not)

**Reliability:** High for arithmetic on these CSVs; low as live CME.  
**Next:** `leave skill not shown` · `name horse …` (a **different** recipe; do **not** add percent-of-OI or other trader groups after scores) · `leave screen rule`. No Phase 2. Do **not** auto-open DataMine.

---

*Amb held 1.0. Amb ≠ clearance. No survivor ≠ least-bad. Failed discovery ≠ promote.*
