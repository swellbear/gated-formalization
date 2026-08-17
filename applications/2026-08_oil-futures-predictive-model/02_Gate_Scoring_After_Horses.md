# Gate Scoring Sheet — After named horses pulse

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Linked:** `04_Material_Admission_Horses.md` · `PULSE_Horses_Standin.md`  
**Scope:** **Under Rank 4 + L-SESS + F-SRC-CME-TAPE + L-STANDIN-Y-CLF + L-STANDIN-Y-CHAIN + H-LAG-WF + V-COST-V2**

---

## 1. Cons

**Score:** **High** — lagged OLS vs 0 on the declared window does not clash with L₀. Clash avoided by not calling the overnight dip a pass and not treating leftover far months as CL1.

**Compatible with L₀?** Yes.

---

## 2. Agree — secondary

**Score:** **Moderate** — careful readers of “simple lags lost on the whole trip” converge; slogan readers may hear “we built a model so it works.”

---

## 3. Prod — secondary

**Checkable consequences:** `python3 scripts/cl_horses.py` reproduces `data/horse_scores.json`. F-CC horse RMSE > RMSE of 0 on 250/500/750.

---

## 4. Amb

| Free Parameter | Weight | Status |
|----------------|--------|--------|
| G1–G7 / G-SESS | **0** | Locked |
| **D-SRC** | **0** | D-EXIST-MET-FT |
| **V-COST** | **0** | Named V2 |
| **F-SRC** | **0** | Named F-SRC-CME-TAPE |
| **G8** | **0** | Named horses; H-LAG scored; H-KS not run |
| **Live vs stand-in** | **0** | Stand-in stipulated |
| **V-SRC** | **1** | Leave unnamed |

**Weighted sum:** **1.0**

**Amb ≠ clearance:** Scoring a horse that **loses** on F-CC does **not** establish skill or value.

---

## 5. Higher-Level Review

**Pass with caution** — leftover is still a **better-matching tape or a different horse**, plus the unnamed paper book.

---

## Final Verdict

- [x] **Provisional** (split: D-EXIST met; skill and value not)

**Reliability:** High for H-LAG arithmetic on this CSV; low as live CME; H-KS **not scored**.  
**Next:** skill leftover still live. No Phase 2.

---

*Amb unchanged 1.0. Amb ≠ clearance. Overnight dip ≠ F-SKILL-met.*
