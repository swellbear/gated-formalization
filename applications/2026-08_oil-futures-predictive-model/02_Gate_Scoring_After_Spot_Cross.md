# Gate Scoring Sheet — After EIA spot WTI↔Brent cross-bench overlay pulse

**Date:** 2026-08-24  
**Application:** `2026-08_oil-futures-predictive-model`  
**Linked:** `04_Material_Admission_Spot_Cross.md` · `PULSE_Hunt_Spot_Cross.md`  
**Scope:** **Under Rank 4 (F-SKILL parked) + L-HUNT-SPOT-TREND + L-HUNT-SPOT-CROSS + L-SPOT-QUEUE + V-COST-V2**

---

## 1. Cons

**Score:** **High** — WTI discovery loss was not sent to confirm; Brent confirm never trained; burned prior rows not scored; 21 not changed.

**Compatible with L₀?** Yes.

---

## 2. Agree — secondary

**Score:** **Moderate** — careful readers of “WTI lost; Brent survivor; confirm 250 is +1; not F-SKILL” converge; slogan readers may hear “WTI leads Brent so a model works.”

---

## 3. Prod — secondary

**Checkable consequences:** `python3 scripts/spot_cross_hunt.py --stage discovery` then `--stage confirm` reproduces `data/spot_cross_hunt_scores.json`. WTI `survivor.id` is null. Brent confirm 500/250/750 `beats_continuation` is true.

---

## 4. Amb

| Free Parameter | Weight | Status |
|----------------|--------|--------|
| G1–G7 / G-SESS / F-SRC / G8 / live-vs-stand-in / V-COST | **0** | Locked |
| **V-SRC** | **1** | Leave unnamed |

**Weighted sum:** **1.0**

**Amb ≠ clearance:** A Brent protocol survivor with a tiny confirm-250 margin does **not** establish spot-trend skill, F-SKILL, or value.

---

## 5. Higher-Level Review

**Pass with caution** — next on this object is queued **C-SPOT-LOGIT**, or leave. Do **not** pick B2W as least-bad. Do **not** retune W2B after confirm. Parent F-SKILL remains a different Yahoo horse or leave skill not shown.

---

## Final Verdict

- [x] **Provisional** (split: D-EXIST met; skill and value not; CROSS WTI failed discovery; Brent confirm point-beats, tiny 250)

**Reliability:** High for arithmetic on these CSVs; low as a live desk or lead–lag theorem.  
**Next:** `leave skill not shown` · queued **C-SPOT-LOGIT** · `name horse …` on Yahoo (different **CL** recipe). No Phase 2.

---

*Amb held 1.0. Amb ≠ clearance. Tiny 250 ≠ met. WTI-met ≠ Brent-met. Confirm is not a training arm.*
