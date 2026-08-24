# Gate Scoring Sheet — After EIA spot expanding-window logistic pulse

**Date:** 2026-08-24  
**Application:** `2026-08_oil-futures-predictive-model`  
**Linked:** `04_Material_Admission_Spot_Logit.md` · `PULSE_Hunt_Spot_Logit.md`  
**Scope:** **Under Rank 4 (F-SKILL parked) + L-HUNT-SPOT-TREND + L-HUNT-SPOT-LOGIT + L-SPOT-QUEUE + V-COST-V2**

---

## 1. Cons

**Score:** **High** — discovery before confirm; confirm losses not used to retune; burned rows not scored; 21 not changed.

**Compatible with L₀?** Yes.

---

## 2. Agree — secondary

**Score:** **Moderate** — careful readers of “discovery beat, confirm lose, not F-SKILL” converge; slogan readers may hear “we fitted a model so skill is shown.”

---

## 3. Prod — secondary

**Checkable consequences:** `python3 scripts/spot_logit_hunt.py --stage discovery` then `--stage confirm` reproduces `data/spot_logit_hunt_scores.json`. Both boards’ confirm `beats_continuation` are false.

---

## 4. Amb

| Free Parameter | Weight | Status |
|----------------|--------|--------|
| G1–G7 / G-SESS / F-SRC / G8 / live-vs-stand-in / V-COST | **0** | Locked |
| **V-SRC** | **1** | Leave unnamed |

**Weighted sum:** **1.0**

**Amb ≠ clearance:** Discovery survivors that lose confirm do **not** establish spot-trend skill, F-SKILL, or value.

---

## 5. Higher-Level Review

**Pass with caution** — Track B named queue is **empty**. Next is leave skill not shown, or name a **different** CL horse on Yahoo, or explicitly name a new spot class. Do **not** invent a spot class after scores. Do **not** retune FULL after confirm.

---

## Final Verdict

- [x] **Provisional** (split: D-EXIST met; skill and value not; LOGIT discovery beat / confirm lose)

**Reliability:** High for arithmetic on these CSVs; low as a live desk.  
**Next:** `leave skill not shown` · `name horse …` on Yahoo (different **CL** recipe) · optional `name source class …` for a new spot class. No Phase 2.

---

*Amb held 1.0. Amb ≠ clearance. Discovery ≠ confirm clearance. Confirm is not a training arm.*
