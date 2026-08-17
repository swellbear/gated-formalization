# Plain-language card

**Application:** `2026-08_oil-futures-predictive-model`  
**Date / checkpoint:** 2026-08-17 · V-COST named **V2** (after Yahoo `CL=F` stand-in pulse)

---

## What we’re doing

You picked the **stricter paper-cost mock**: listed fees **plus** $10 per contract in and $10 out. Later paper books will be graded that way. That is how we keep the mock closer to a real fill. It does **not** mean a book already made money. Skill vs last settlement is still **not shown**. This is not a trade.

## What we need from you

Nothing required on costs. Optional on skill: wait for official CME stamps and re-score, or name a recipe to test **against** the Yahoo baselines.

**Preferred reply:** click A / B / C. Typed: `leave skill not shown` · `live CME only` · `name horse …`

## What a “yes” / this update means

Paper costs are **V2**. Fees-only (V1) is **not** the live schedule. Naming a cost rule is not a pass of after-cost value.

## What this does *not* mean

That a model beats last settlement. That a paper book made money after costs. That anyone should trade. That an oil offshoot is cleared. That a live broker commission table was invented.

---

## Details (technical record — secondary)

| Item | Value |
|------|--------|
| Claim-freeze / claim under test | Rank 4 F-CC + L-SESS F-ON/F-DAY; F-SRC-CME-TAPE; L-STANDIN-Y-CLF; **V-COST-V2** |
| Amb | **1.0** (**≠ clearance**) — leftover is V-SRC only |
| Locks / package IDs | Rank 4; D-EXIST-MET-FT; L-SESS; F-SRC-CME-TAPE; L-STANDIN-Y-CLF; L-PULSE-STANDIN-1; **V-COST-V2** |
| Method verdict label (if any) | Stable Provisional (split) — hard stop (residuals live) |
| Live vs stand-in | **Stand-in stipulated** (Yahoo `CL=F` Open/Close) |
| Last-500 RMSE vs 0 | F-ON 0.01291 · F-DAY 0.02663 · F-CC 0.02869 (n=500) |
| Paper costs | **V2** = listed fees + 1 CL tick/side ($10/contract/side; $20 RT slippage before fees) |
| Artifact pointers | `Lock_VCOST_V2.md` · `04_Material_Admission_VCOST_V2.md` · `Lock_Standin_Yahoo_CLF.md` |

---

*Standing rule: Dual-audience communication. Glossary: `docs/READER_GLOSSARY.md`.*
