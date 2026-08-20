# Gate Scoring Sheet — After EIA spot 21-day trend hunt pulse

**Date:** 2026-08-20  
**Application:** `2026-08_oil-futures-predictive-model`  
**Linked:** `04_Material_Admission_Spot_Trend.md` · `PULSE_Hunt_Spot_Trend.md`  
**Scope:** **Under Rank 4 (F-SKILL parked) + L-HUNT-SPOT-TREND + L-STANDIN-EIA-SPOT + L-SPOT-ARMS + L-SPOT-QUEUE + V-COST-V2**

---

## 1. Cons

**Score:** **High** — discovery/confirm vs continuation on the declared prefix does not clash with L₀. Clash avoided by not sending a discovery loser to confirm, not changing 21 after scores, and not scoring this pulse as F-CC.

**Compatible with L₀?** Yes.

---

## 2. Agree — secondary

**Score:** **Moderate** — careful readers of “both lose on discovery, no survivor, confirm skipped, this is not futures skill” converge; slogan readers may hear “we built a trend model so it works” or “oil has no trend.”

---

## 3. Prod — secondary

**Checkable consequences:** `python3 scripts/spot_trend_hunt.py --stage discovery` reproduces `data/spot_trend_hunt_scores.json` discovery block. Both `survivor.id` are null. Confirm is null.

---

## 4. Amb

| Free Parameter | Weight | Status |
|----------------|--------|--------|
| G1–G7 / G-SESS / F-SRC / G8 / live-vs-stand-in / V-COST | **0** | Locked |
| **V-SRC** | **1** | Leave unnamed |

**Weighted sum:** **1.0**

**Amb ≠ clearance:** Scoring two horses that **do not survive discovery** does **not** establish spot-trend skill, F-SKILL, or value.

---

## 5. Higher-Level Review

**Pass with caution** — leftover on this object is a **queued next class** (not a re-hunt of this confirm window, not a 21-day retune) or leave. Parent F-SKILL remains a **different** Yahoo horse or leave skill not shown. Live CME still gated.

---

## Final Verdict

- [x] **Provisional** (split: D-EXIST met; skill and value not; spot-trend drawer failed discovery)

**Reliability:** High for arithmetic on these CSVs; low as a live cash desk or futures tape.  
**Next:** `leave skill not shown` · `name horse …` on **queue** (**C-SPOT-INV** next; do **not** unburn FLIP-HOLD/REV; do **not** change 21) · `leave screen rule`. No Phase 2. Do **not** auto-open DataMine.

---

*Amb held 1.0. Amb ≠ clearance. No survivor ≠ least-bad. Failed discovery ≠ confirm. Spot ≠ futures.*
