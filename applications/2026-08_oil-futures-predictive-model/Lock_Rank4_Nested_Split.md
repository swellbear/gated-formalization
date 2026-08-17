# Lock Record — Package Rank 4 (nested split A+B+C)

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Operator selection:** **A** → **Rank 4 — Nested split A+B+C** (`lock Rank 4`)  
**Status:** **IN FORCE for meanings.** V-COST **either accepted**. V-SRC **leave unnamed** (operator **B**, 2026-08-17 — `Lock_VSRC_Leave_Unnamed.md`). D-SRC **unnamed for now** (not a sealed `leave unnamed`). V-VALUE-TEST-0 **not established**.

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
| **V-VALUE** | Real shot (P-NonNegligible) of after-cost paper economic value vs the curve on the same CL next-session book | `O3+M2+S4+C1+T1+H1+E1` — **V-COST either** (each test names V1 or V2) |

**Claim-freeze (under Rank 4):**  
“Can a predictive model for oil futures be built?” is graded as **three separate legs**. A result on one is not a result on the others. D-EXIST is the wording-faithful core. F-SKILL operationalizes “predictive.” V-VALUE is an added performance elevation, not a “should trade.”

**Deviation (per leg):** D-EXIST Minimal · F-SKILL Moderate · V-VALUE Substantial / elevation.

---

## Scope label (mandatory on subsequent findings)

**Under Rank 4 (D-EXIST ⊂ F-SKILL ⊂ V-VALUE) only.**

---

## OR-slot (V-VALUE) — formally accepted as either

Cost schedule is **not** a singleton. Operator **C** formally accepted **either** V1 or V2 (`Lock_VCOST_Either.md`).

- **V1:** listed CL exchange/clearing/NFA-style fees; **no** slippage.  
- **V2:** those fees **plus** 1 CL tick/side (**$10**/contract/side; **$20** round-turn slippage before fees).  
- A later value-leg test **must still name V1 or V2** (or report both). Accepting either is **not** “we already used the stricter cost.”  
- **Do not** invent a live broker schedule.

D-EXIST and F-SKILL do not wait on this slot.

---

## Dependents now eligible to re-open (scoped)

- **D-EXIST** — D-SRC **unnamed for now** (live ask). Proven-only hunt submitted no class. No-change **OUT** as the model exhibit. Reopen: `name source class …` / `leave unnamed` / `endpoint only`.  
- **F-SKILL** — **not established** on the hunt.  
- **G8** — still free under F-SKILL.  
- **V-VALUE** — **not established** (V-VALUE-TEST-0). V-SRC **sealed leave unnamed**. Reopen only with `name source class …` matching V-VALUE; test must still name V1 or V2.

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
6. V-COST either is **not** “we used V2.” Each test must name V1 or V2.  
7. Last-settlement no-change is the F-SKILL **baseline**, not the D-EXIST **model** (operator B).
