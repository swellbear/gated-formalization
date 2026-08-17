# Lock Record — V-COST either (V1 or V2)

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Operator selection:** **C** → `lock V-COST either` (`V-EITHER`)  
**App-local lock ID:** V-EITHER / LOCK-012 (this application only; not a library process lock).  
**Status:** **SUPERSEDED 2026-08-17 as the singleton schedule** by `Lock_VCOST_V2.md` (operator named **V2**). Kept as audit trail of the OR-slot. Either-lock **lifted for the live schedule only**.

---

## Locked content

| ID | Rule |
|----|------|
| **V1** | Listed CL exchange/clearing/NFA-style fees; **no** slippage |
| **V2** | Those fees **plus** 1 CL tick slippage per side (**$10**/contract/side; **$20** round-turn slippage before fees) |
| **V-EITHER** | **Formally accept either** V1 or V2 |

**Scope:** **Under Rank 4 (D-EXIST ⊂ F-SKILL ⊂ V-VALUE) only**, **Under V-COST either**.

**Tick identity (market structure, not a fee quote):** CL = 1,000 barrels; tick = $0.01/barrel = **$10**/contract.

---

## What this does *not* do

- Does **not** establish V-VALUE, F-SKILL, or D-EXIST.  
- Does **not** name a recipe or paper book.  
- Does **not** license trading.  
- Does **not** pick V1 or V2 as the only rule.

**Lock-time Amb warning:** Fixing “either” drops leftover-ambiguity on an unset cost fork. **Amb drop ≠ clearance.**

---

## Dependents

V-VALUE may be **tested** under this either-lock. Honest test with **no specified recipe:** **not established** (not a refute of all books). Conflicted vendor backtests cannot solely affirm P-NonNegligible.
