# Multi-elevation split — proposed (not in force until a Rank 4 lock)

**Application:** `2026-08_oil-futures-predictive-model`  
**Date:** 2026-08-17  
**Status:** **In force for meanings** (operator `lock Rank 4`, 2026-08-17). V-COST **either accepted** (operator **C**). D-EXIST **not** auto-established (establishment-stop). V-VALUE-TEST-0 **not established**.

**Rule:** Do **not** collapse legs. A yes on one is not a yes on the others. Amb drop ≠ clearance.

Imported pattern from `training/2026-08_stage8_us-50-states-only-coherent-curriculum` (split-not-blend), re-validated here. That app’s uniqueness/should verdicts are **not** inherited.

---

## Why a split exists

A, B, and C from the Cycle 0 picker are **rival jobs**, not interchangeable options on one decision point:

| Picker | Everyday job | Cannot be the same freeze as |
|--------|----------------|------------------------------|
| **C / Rank 3** | Existence — can a forecasting recipe be written / exist? | Skill or after-cost P/L |
| **A / Rank 1** | Skill — real shot it beats last-price out of sample on named CL protocol | Existence-only or trading-value |
| **B / Rank 2** | Value — real shot of after-cost paper P/L vs the curve | Construction census |

Locking “A and B and C” as **one object** (O1+O2+O3) is an **incoherent combo**. “Formally accept either {existence, skill, value}” would leave the job unset.

The coherent combination is **named nested legs**.

---

## Legs (fixed if Rank 4)

| ID | Leg | Expectation if this package is locked |
|----|-----|----------------------------------------|
| **D-EXIST** | Specified forecasting mapping for some liquid crude futures can be written or already exists (P-Logical construction) | May establish cheaply; near-vacuous vs “predictive” as success |
| **F-SKILL** | Real shot (P-NonNegligible) a specified recipe beats last-settlement RMSE, walk-forward, NYMEX CL front-month, next-session log-return | Separate bar; D-EXIST does not meet it |
| **V-VALUE** | Real shot (P-NonNegligible) of after-cost paper economic value on the same CL next-session book vs the curve | **Marked elevation**; not the original sentence. Out of package under Rank 4-AC |

## Legs (fixed if Rank 4-AC)

D-EXIST and F-SKILL only. V-VALUE **out**.

---

## Already-included nesting

```
D-EXIST  ⊂  F-SKILL  ⊂  V-VALUE   (Rank 4)
D-EXIST  ⊂  F-SKILL               (Rank 4-AC)
```

- A skill test already includes “there is a specified mapping.”
- A value test already includes “there is a forecast rule.”
- “What about existence?” after a skill miss does **not** mean the census was omitted.

---

## Honesty lines (mandatory on every later `04`)

1. Establishing D-EXIST does **not** establish F-SKILL or V-VALUE.
2. Establishing F-SKILL does **not** establish V-VALUE.
3. Refuting V-VALUE does **not** refute D-EXIST (or, by itself, F-SKILL).
4. Print-match of a spot-oil paper or in-sample R² is **not** F-SKILL-met.
5. Conflicted vendor backtests cannot solely affirm V-VALUE.

---

## OR-slots

| Leg | OR-slot | Status until operator acts |
|-----|---------|----------------------------|
| D-EXIST | C3 class = WTI **or** Brent (either accepted inside Rank 3 mechanics) | Complete if Rank 4 / 4-AC selected |
| F-SKILL | none | Complete if selected |
| V-VALUE | Cost schedule (round-turn + slippage) must be **singled** or formally “either” | **Either accepted** (V1 or V2; each test names which) |

---

## Claim-type if activated

- Rank 4: **Mixed** — D-EXIST + F-SKILL descriptive; V-VALUE performance elevation (still not a “should trade” unless LOCK-006 is later imported).
- Rank 4-AC: **Descriptive** split of census vs skill; no value elevation.

---

*Rank 4 locked 2026-08-17. **D-EXIST established (futures-target only).** **L-SESS** in force (F-CC parent; F-ON/F-DAY separate; F-COMBO third test). **F-SRC-CME-TAPE** named 2026-08-17; pulse not computed (live tape absent). Spot/real-price OUT. Menu ≠ “the” recipe. V-SRC leave unnamed. F-SKILL and V-VALUE not established. Closeout: **hard stop (residuals live)**. Optional modes **declined**. Live residual: tape ([R-LIVE-STANDIN](RESIDUAL_BRANCH_MENU.md#r-live-standin)) plus skill ([R-F-SKILL](RESIDUAL_BRANCH_MENU.md#r-f-skill)). Not a trade. Next: `live CME only` / `stipulate stand-in …` / `leave tape pending`.*
