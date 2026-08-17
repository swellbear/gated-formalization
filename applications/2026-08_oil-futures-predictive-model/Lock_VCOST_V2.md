# Lock Record — V-COST named V2

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Operator selection:** `go with V2 then` (more realistic mock; learn how a model would perform)  
**App-local lock ID:** **V-COST-V2**  
**Status:** **IN FORCE as the named paper-cost schedule.** Prior **V-EITHER** remains the historical OR-slot; the singleton for later tests is **V2**. V-VALUE **not established** (no named book).

---

## 0. Plain-language framing

**What was decided:**  
Paper P/L, when a book is later named, must survive listed CL fees **and** 1 tick of slippage each way: **$10/contract in and $10 out** ($20 round-turn slippage before fees).

**What this settles:**  
Which cost mock this app uses. V1 (fees only, fill at the stamp) is **not** the live schedule.

**What this does *not* settle:**  
That a model makes money. That skill is shown. That anyone should trade. A fee **table** in dollars is still not invented here; the extra friction that is named is the tick.

---

## Locked content

**Scope:** **Under Rank 4 + V-EITHER (historical) + V-COST-V2**.

| ID | Rule |
|----|------|
| **V2** | Listed CL exchange/clearing/NFA-style fees **plus** 1 CL tick / side = **$10**/contract/side (**$20** round-turn slippage before fees) |
| **V1** | **Not** the schedule for later tests on this app |
| **Day / combo books** | Count **actual** round-turns. Daily in-and-out is not free |

**Tick identity (market structure, not a broker quote):** CL = 1,000 barrels; tick = $0.01/barrel = **$10**/contract.

---

## What this does *not* do

- Does **not** establish V-VALUE, F-SKILL, or D-EXIST.  
- Does **not** name a recipe or paper book.  
- Does **not** license trading or start an oil offshoot.  
- Does **not** invent a live broker commission in dollars.

**Lock-time Amb warning:** Naming V2 drops leftover-ambiguity on V-COST (0.5 → 0). **Amb drop ≠ clearance.**

---

## Reopen

A later operator may switch the schedule (e.g. back to V1 or a named broker table). That is a freeze change, not a silent softening.
