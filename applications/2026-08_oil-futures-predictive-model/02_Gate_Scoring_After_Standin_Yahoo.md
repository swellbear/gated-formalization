# Gate Scoring Sheet — After Yahoo CL=F stand-in pulse

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Linked:** `04_Material_Admission_Standin_Yahoo.md` · `Lock_Standin_Yahoo_CLF.md`  
**Scope:** **Under Rank 4 + L-SESS + F-SRC-CME-TAPE + L-STANDIN-Y-CLF**

---

## 1. Cons

**Score:** **High** — Yahoo is badged stand-in; baseline RMSE is not called a pass; R1 non-application is stated.

**Compatible with L₀?** Yes.

---

## 2. Agree — secondary

**Score:** **Moderate** — careful readers of “stand-in baseline, skill not shown” converge; slogan readers may hear “we have oil numbers, so it works.”

---

## 3. Prod — secondary

**Checkable consequences:** `data/clf_yahoo_standin.csv` + `scripts/cl_session_rmse.py --holdout 500` reproduces the table.

---

## 4. Amb

| Free Parameter | Weight | Status |
|----------------|--------|--------|
| G1–G7 / G-SESS | **0** | Locked |
| **D-SRC** | **0** | D-EXIST-MET-FT |
| **V-COST** | **0.5** | Either |
| **F-SRC** | **0** | Named F-SRC-CME-TAPE |
| **G8** | **0** | Named (baseline scored; optional FTS not run) |
| **Live vs stand-in** | **0** | **Stand-in stipulated** (Yahoo `CL=F`) |
| **V-SRC** | **1** | Leave unnamed |

**Weighted sum:** **1.5**

**Amb ≠ clearance:** A stand-in baseline does **not** establish skill.

---

## 5. Higher-Level Review

**Pass with caution** — next blocker is a **horse vs this baseline** (or a live-tape re-score), not an unnamed tape fork.

---

## Final Verdict

- [x] **Provisional** (split: D-EXIST met; session skill bars and value not)

**Reliability:** High for stand-in fetch and RMSE arithmetic. Low as a substitute for official settlement.  
**Next:** leave skill not shown, or `live CME only` to re-score, or name a horse that is scored against these RMSEs. No Phase 2.

---

*Amb 2.5 → 1.5. Amb ≠ clearance. Stand-in ≠ live. Baseline ≠ pass.*
