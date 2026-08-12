# Material Admission Check — L4 D-DEF (SEP measurement / table-reading definitions)

**Date:** 2026-08-12  
**Parent application:** `2026-08_fomc-june-2026-sep`  
**Targeted gap:** Census substrate — how the SEP says to read its tables (inventory B)  
**Linked Gap Ranking Sheet:** `03_Gap_Extraction_and_Ranking.md`  
**Status:** **ADMITTED (operator 2026-08-12)** — recommended next step after L3; operator `admit.` after being offered `admit L4 D-DEF` (recommended) and `lock C-APPROP individual-mandate`  
**Prior layers:** L1 OBJECT-FORECAST · L2 F-ML P-BaseCase (bar not met) · L3 D-DOC  
**Evidence intake:** [`E_Package_Evidence_Intake_D_DEF.md`](E_Package_Evidence_Intake_D_DEF.md)  
**Frame:** June 17, 2026 SEP live. July 29 OUT.

---

## Candidate Material Summary

**Source(s):**
- [SEP PDF](https://www.federalreserve.gov/monetarypolicy/files/fomcprojtabl20260617.pdf)
- [Accessible HTML](https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260617.htm)
- Inventory B ([`CLAIM_INVENTORY.md`](CLAIM_INVENTORY.md))

**Key content / finding (concise):**  
The June 17, 2026 SEP defines its table conventions as follows. GDP and both inflation measures are **Q4/Q4** percent changes. PCE is the PCE price index; core PCE excludes food and energy. Unemployment is the **average civilian unemployment rate in Q4**. The funds-rate figure is the **midpoint of the projected appropriate target range** or the projected **appropriate target level**, at **year-end** (or longer run); Figure 2 dots are rounded to the nearest **1/8** percentage point. For each period, the **median** is the middle projection (average of the two middle when even). **Central tendency** excludes the three highest and three lowest projections. **Range** is lowest to highest. Longer-run projections for **core PCE are not collected**. Table 2 consumer-price RMSE uses **CPI** (not PCE), Q4/Q4; error ranges are ±RMSE of summer projections for **2006–2025**; under stated assumptions those ranges correspond to about a **70 percent** probability. The funds-rate fan-chart CIs are **not strictly consistent** with SEP funds-rate projections, because those projections are **not** forecasts of the likeliest funds-rate outcomes but assessments of **appropriate policy**. Cross-participant dispersion (Figure 1) is **much smaller** than average forecast errors over the past 20 years. Historical RMSE fans **may not** match participants’ current uncertainty judgments.

This is **definitional census** of how the SEP says to read its tables. It does not establish that any printed median **is** the P-BaseCase outcome.

---

## Admission Criteria

### 1. Relevance to Targeted Gap
- [x] Yes  
- [ ] No  
- [ ] Partially  

**Explanation:** Constrains D-DEF (inventory B). Does not constrain F-ML-BAR met, C-APPROP, F-LR, D-SEP cell values as forecast facts, or realization. Does not freeze Gap 4 (which statistic is load-bearing).

### 2. Consistency (Cons)
- [x] Yes  
- [ ] No  

**Any conflicts:** None with L₀ or L1–L3. Median / CT / range appear here only as **how the document defines those statistics**, already split by L1–L2 from bar-met. B15 restates the L2 split: funds-rate dots stay off F-ML-BAR. RMSE/CPI footnotes restate Gap 7’s draft split (historical fans ≠ current uncertainty) without freezing Gap 7.

---

## Admission Decision

- [x] **ADMIT** for incorporation *(operator `admit.` 2026-08-12 after recommended D-DEF; C-APPROP offered and not selected)*  
- [ ] **REJECT**  
- [ ] **HOLD**

**Locked as:** **L4 D-DEF** (measurement / table-reading definitions only).

**Amb effect:** D-DEF was L₀-already-hard. Package Amb stays ≈ **7** (no fake drop).  
**Prod effect:** Q4/Q4, median/CT/range, funds-rate midpoint, core-PCE-no-LR, and RMSE/CPI footnotes are checkable on the .gov URLs as *reading conventions*.

**Does not:**
- Meet F-ML-BAR (P-BaseCase still unmet).  
- Establish C-APPROP or F-LR.  
- Admit D-SEP Table 1 cells as forecast facts (next substrate: submitted figures, still not bar-met).  
- Treat a median as the Committee’s forecast.  
- Treat RMSE fans as current FOMC uncertainty.  
- Treat CPI RMSE as PCE RMSE.  
- Admit realization of 2026–28 outcomes.  
- Import July 29.

---

## Post-Incorporation Action

- [x] Re-score (`02e`)  
- [x] Update `admitted_layers.md`  
- [x] Keep split: D-DOC ≠ D-DEF ≠ D-SEP ≠ F-ML met  

---

## Residual Judgment Notes

Operator replied `admit.` after being offered recommended `admit L4 D-DEF` and `lock C-APPROP individual-mandate`. D-DEF only. C-APPROP remains the highest-W open slot; D-SEP (printed Table 1 as *submitted*, not bar-met) is the remaining census vehicle before that freeze. Definitions of median ≠ load-bearing-statistic freeze (Gap 4 still open).
