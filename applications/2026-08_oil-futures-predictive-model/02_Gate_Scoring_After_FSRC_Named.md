# Gate Scoring Sheet — After named CME tape pulse

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Linked:** `04_Material_Admission_FSRC_Named.md` · `Lock_FSRC_Named_CME_Tape.md`  
**Scope:** **Under Rank 4 + L-SESS + F-SRC-CME-TAPE**

---

## 1. Cons

**Score:** **High** — naming official CME stamps matches L-SESS. Clash avoided by not scoring Yahoo as live and not calling a missing tape a pass.

**Compatible with L₀?** Yes.

---

## 2. Agree — secondary

**Score:** **Moderate** — careful readers of “class named, tape missing, skill not shown” converge; slogan readers may hear “we picked CME, so it works.”

---

## 3. Prod — secondary

**Checkable consequences:** RMSE formulas are stated; a CSV with `date,open,settle,front_id` can run `scripts/cl_session_rmse.py`. Live vs stand-in is now a concrete fork.

---

## 4. Amb

| Free Parameter | Weight | Status |
|----------------|--------|--------|
| G1–G7 / G-SESS | **0** | Locked |
| **D-SRC** | **0** | D-EXIST-MET-FT |
| **V-COST** | **0.5** | Either |
| **F-SRC** | **0** | **Named** F-SRC-CME-TAPE |
| **G8** | **0** | **Named** (baseline RMSE; optional FTS) |
| **Live vs stand-in** | **1** | **Open** — live CME not in hand; stand-in not stipulated |
| **V-SRC** | **1** | Leave unnamed |

**Weighted sum:** **2.5**

**Amb ≠ clearance:** Naming the tape and dropping Amb does **not** establish skill.

---

## 5. Higher-Level Review

**Pass with caution** — next blocker is the **tape**, not an unnamed class.

---

## Final Verdict

- [x] **Provisional** (split: D-EXIST met; session skill bars and value not)

**Reliability:** High for vehicle naming and fetch-failure recording.  
**Next:** `stipulate stand-in …` **or** provide live CME official open/settle. Not `none — hard stop`. No Phase 2.

---

*Amb 5.5 → 2.5. Amb ≠ clearance. Pulse ≠ pass.*
