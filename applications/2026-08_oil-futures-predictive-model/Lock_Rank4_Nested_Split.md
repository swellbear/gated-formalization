# Lock Record — Package Rank 4 (nested split A+B+C)

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Operator selection:** **A** → **Rank 4 — Nested split A+B+C** (`lock Rank 4`)  
**Status:** **IN FORCE for meanings.** **D-EXIST established (futures-target only).** V-COST **V2 named** (`Lock_VCOST_V2.md`; V-EITHER superseded as singleton). V-SRC **leave unnamed**. **F-SRC-CME-TAPE** named. F-SKILL and V-VALUE **not established**.

---

## Locked package

**Claim-under-test (original slogan):** **D-EXIST**  
**Marked elevations (not the slogan):** **F-SKILL**, **V-VALUE**  
**Nesting:** `D-EXIST ⊂ F-SKILL ⊂ V-VALUE`  
**Do not collapse legs.**

| Leg | Job | Mechanics |
|-----|-----|-----------|
| **D-EXIST** | Specified forecasting mapping for some liquid crude futures can be written or already exists | `O1+M1+S1+C3+T2+H3+E3` — P-Logical construction; any specified mapping; WTI **or** Brent as class (either accepted); census protocol |
| **F-SKILL** | Real shot (P-NonNegligible) a specified recipe beats last-settlement RMSE, walk-forward | `O2+M2+S2+C1+T1+H1+E1` — NYMEX **CL front-month**, next-session **log-return**, walk-forward vs **no-change / last settlement** |
| **V-VALUE** | Real shot (P-NonNegligible) of after-cost paper economic value vs the curve on the same CL next-session book | `O3+M2+S4+C1+T1+H1+E1` — **V-COST-V2** (historical OR-slot was V-EITHER) |

**Claim-freeze (under Rank 4):**  
“Can a predictive model for oil futures be built?” is graded as **three separate legs**. A result on one is not a result on the others. D-EXIST is the wording-faithful core. F-SKILL operationalizes “predictive.” V-VALUE is an added performance elevation, not a “should trade.”

**Deviation (per leg):** D-EXIST Minimal · F-SKILL Moderate · V-VALUE Substantial / elevation.

---

## Scope label (mandatory on subsequent findings)

**Under Rank 4 (D-EXIST ⊂ F-SKILL ⊂ V-VALUE) only.**

---

## OR-slot (V-VALUE) — later named V2

Cost schedule was first formally **either** (`Lock_VCOST_Either.md`). **Later (same day):** operator named **V2** as the live singleton (`Lock_VCOST_V2.md`).

- **V2 (live):** listed CL exchange/clearing/NFA-style fees **plus** 1 CL tick/side (**$10**/contract/side; **$20** round-turn slippage before fees).  
- **V1:** **not** the schedule for later tests on this app.  
- Naming V2 is **not** “the model already made money.”  
- **Do not** invent a live broker schedule.

D-EXIST and F-SKILL do not wait on this slot.

---

## Dependents now eligible to re-open (scoped)

- **D-EXIST** — **established** (futures-target only). Spot/real-price **OUT**. Menu is not a singleton pick.  
- **F-SKILL** — **not established**. **F-SRC-CME-TAPE** named; stand-in baseline scored; leftover live.  
- **G8** — meanings admitted (baseline; optional FTS not run).  
- **V-VALUE** — **not established** (V-VALUE-TEST-0). V-SRC **sealed leave unnamed**. Costs **V2**.

---

## Lock-time Amb warning

Selecting Rank 4 **drops leftover-ambiguity by fixing meanings** (three jobs, “can” heights, contract/metric/horizon per leg). **That drop does not establish** D-EXIST, F-SKILL, or V-VALUE. **Low Amb after lock ≠ clearance.**

---

## Honesty lines

1. Establishing D-EXIST does **not** establish F-SKILL or V-VALUE.  
2. Establishing F-SKILL does **not** establish V-VALUE.  
3. Refuting V-VALUE does **not** refute D-EXIST.  
4. Print-match of a spot-oil paper or in-sample R² is **not** F-SKILL-met.  
5. Conflicted vendor backtests cannot solely affirm V-VALUE.  
6. V-COST either was **not** “we used V2.” **Later:** V2 **was** named as the singleton (`Lock_VCOST_V2.md`). V2 ≠ value-met.  
7. Last-settlement no-change is the F-SKILL **baseline**, not the D-EXIST **model** (operator B).  
8. D-EXIST-met is **not** a pick of one paper from the menu, **not** spot-inside-C3, and **not** F-SKILL or V-VALUE.  
9. F-SRC leave unnamed is **not** a refute of skill, **not** an undo of D-EXIST-MET-FT, and **not** a license to invent a class.  
10–14. Session-split honesty: see `Lock_Session_Split.md` (F-DAY ≠ F-CC; combo is a third test; not a trade).
