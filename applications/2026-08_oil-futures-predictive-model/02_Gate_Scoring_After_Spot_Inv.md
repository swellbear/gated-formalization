# Gate Scoring Sheet — After EIA inventory-surprise overlay pulse

**Date:** 2026-08-20  
**Application:** `2026-08_oil-futures-predictive-model`  
**Linked:** `04_Material_Admission_Spot_Inv.md` · `PULSE_Hunt_Spot_Inv.md`  
**Scope:** **Under Rank 4 (F-SKILL parked) + L-HUNT-SPOT-TREND + L-HUNT-SPOT-INV + L-STANDIN-EIA-INV + L-SPOT-QUEUE + V-COST-V2**

---

## 1. Cons

**Score:** **High** — discovery vs continuation on the declared prefix does not clash with L₀. Clash avoided by not sending a discovery loser to confirm, not unburning FLIP-HOLD/REV, and not changing 21.

**Compatible with L₀?** Yes.

---

## 2. Agree — secondary

**Score:** **Moderate** — careful readers of “both lose, no survivor, confirm skipped, not a Street poll” converge; slogan readers may hear “we used inventories so a model works.”

---

## 3. Prod — secondary

**Checkable consequences:** `python3 scripts/spot_inv_hunt.py --stage discovery` reproduces `data/spot_inv_hunt_scores.json` discovery block. Both `survivor.id` are null. Confirm is null.

---

## 4. Amb

| Free Parameter | Weight | Status |
|----------------|--------|--------|
| G1–G7 / G-SESS / F-SRC / G8 / live-vs-stand-in / V-COST | **0** | Locked |
| **V-SRC** | **1** | Leave unnamed |

**Weighted sum:** **1.0**

**Amb ≠ clearance:** Overlay horses that **do not survive discovery** do **not** establish spot-trend skill, F-SKILL, or value.

---

## 5. Higher-Level Review

**Pass with caution** — next on this object is queued **C-SPOT-CROSS**, or leave. Do **not** pick CONT as least-bad. Parent F-SKILL remains a different Yahoo horse or leave skill not shown.

---

## Final Verdict

- [x] **Provisional** (split: D-EXIST met; skill and value not; INV overlay failed discovery)

**Reliability:** High for arithmetic on these CSVs; low as a live desk or survey surprise.  
**Next:** `leave skill not shown` · queued **C-SPOT-CROSS** · `name horse …` on Yahoo (different **CL** recipe). No Phase 2.

---

*Amb held 1.0. Amb ≠ clearance. No survivor ≠ least-bad. Naive surprise ≠ Bloomberg.*
