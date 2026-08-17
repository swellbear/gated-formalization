# Gate Scoring Sheet — After V-COST V2

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Linked:** `04_Material_Admission_VCOST_V2.md` · `Lock_VCOST_V2.md`  
**Scope:** **Under Rank 4 + L-SESS + F-SRC-CME-TAPE + L-STANDIN-Y-CLF + V-COST-V2**

---

## 1. Cons

**Score:** **High** — V2 matches the operator’s “more realistic mock.” Clash avoided by not calling V-VALUE met and not inventing a broker commission.

**Compatible with L₀?** Yes.

---

## 2. Agree — secondary

**Score:** **Moderate** — careful readers of “stricter paper costs, still no book” converge; slogan readers may hear “we modeled real trading.”

---

## 3. Prod — secondary

**Checkable consequences:** A later paper book must subtract listed fees **and** $10/contract/side; day/combo books count actual round-turns.

---

## 4. Amb

| Free Parameter | Weight | Status |
|----------------|--------|--------|
| G1–G7 / G-SESS | **0** | Locked |
| **D-SRC** | **0** | D-EXIST-MET-FT |
| **V-COST** | **0** | **Named V2** |
| **F-SRC** | **0** | Named F-SRC-CME-TAPE |
| **G8** | **0** | Named (baseline scored; optional FTS not run) |
| **Live vs stand-in** | **0** | Stand-in stipulated (Yahoo `CL=F`) |
| **V-SRC** | **1** | Leave unnamed |

**Weighted sum:** **1.0**

**Amb ≠ clearance:** Naming V2 does **not** establish after-cost value or skill.

---

## 5. Higher-Level Review

**Pass with caution** — leftover is still a **named paper book**, not a live trade.

---

## Final Verdict

- [x] **Provisional** (split: D-EXIST met; skill and value not)

**Reliability:** High for the cost pick.  
**Next:** skill leftover still live; V-VALUE still parked until a matching book is named under **V2**. No Phase 2.

---

*Amb 1.5 → 1.0. Amb ≠ clearance. V2 ≠ value-met.*
