# Gap Extraction & Ranking Sheet — Cycle 0

> **Plain language.** Name leftover choices, freeze what each leftover *is*, rank which ones matter most. Lean Default Path: attack only the top one or two.

**Date:** 2026-08-17  
**Parent application / claim:** `2026-08_oil-futures-predictive-model` — Can a predictive model for oil futures be built?  
**Linked Gate Scoring Sheet:** `02_Gate_Scoring_Sheet.md`  

---

## Identified Gaps (Free Parameters)

### Gap 1 — G1 Object

**Description:** Whether the sentence is a construction census (“some forecasting recipe can be written / already exists”), a skill test (“a recipe that beats a named baseline”), or an economic-value test (“a recipe that is worth money after costs”).

**Claim-freeze (one sentence — lock what this free parameter *is*):**  
G1 is the **job** the claim is doing: existence/construction of a forecasting mapping, locked out-of-sample skill vs a named baseline, or after-cost economic value — not which architecture is fashionable.

**Impact (0–2):** 2  
**Anchor connection (0–2):** 2  
**Measurability (0–2):** 2 (once locked; 0 while rival jobs remain)  
**Sum:** 6  

### Gap 2 — G2 “Can” modal bar

**Description:** How strong “can” is: not a contradiction; a real (not-tiny) feasibility shot; or the expected/central path that such a model works.

**Claim-freeze (one sentence):**  
G2 is the **height** of “can” (P-Logical / P-NonNegligible / P-BaseCase). Choosing the height is not meeting it.

**Impact (0–2):** 2  
**Anchor connection (0–2):** 2  
**Measurability (0–2):** 1 (definitional lock; empirical test follows only after G1/G6)  
**Sum:** 5  

### Gap 3 — G6 Success metric + baseline (dominant with G1)

**Description:** What would count as “predictive”: any mapping; statistical skill vs last-price/random-walk; skill vs the futures curve; or after-cost P/L.

**Claim-freeze (one sentence):**  
G6 is the **grading rule**: metric + baseline + that “predictive” is not silently swapped for a different target.

**Impact (0–2):** 2  
**Anchor connection (0–2):** 2  
**Measurability (0–2):** 2 (once named)  
**Sum:** 6  

### Gap 4 — G3 Contract identity

**Description:** Which listed oil-futures object (NYMEX WTI CL front-month vs ICE Brent vs “any liquid crude futures as a class”) and which tenor.

**Claim-freeze (one sentence):**  
G3 is the **named listed contract and tenor** the mapping is supposed to forecast — not spot crude unless the operator revises the claim.

**Impact (0–2):** 2  
**Anchor connection (0–2):** 2  
**Measurability (0–2):** 2  
**Sum:** 6  

### Gap 5 — G4 Target

**Description:** Settlement price, log-return, direction-only, or curve/spread.

**Claim-freeze (one sentence):**  
G4 is the **numeric target** of the mapping on the locked contract.

**Impact (0–2):** 1  
**Anchor connection (0–2):** 1  
**Measurability (0–2):** 2  
**Sum:** 4  

### Gap 6 — G5 Horizon

**Description:** Next session, next month, or open-ended.

**Claim-freeze (one sentence):**  
G5 is the **time from forecast issuance to the print that counts**.

**Impact (0–2):** 1  
**Anchor connection (0–2):** 1  
**Measurability (0–2):** 2  
**Sum:** 4  

### Gap 7 — G7 Evaluation protocol

**Description:** In-sample fit vs walk-forward; live official settlements vs a stand-in series.

**Claim-freeze (one sentence):**  
G7 is **how** skill/value is scored (walk-forward vs in-sample; live vs stand-in), including a Live vs stand-in badge if a proxy series is used.

**Impact (0–2):** 1  
**Anchor connection (0–2):** 1  
**Measurability (0–2):** 2  
**Sum:** 4  

### Gap 8 — G8 Model class (G1-dependent)

**Description:** Which architecture/features count as “a model” once the job and metric are locked.

**Claim-freeze (one sentence):**  
G8 is the **named model class and feature recipe** under a locked G1/G6 — blocked until those are set.

**Impact (0–2):** 1  
**Anchor connection (0–2):** 1  
**Measurability (0–2):** 1  
**Sum:** 3  

---

## Claim-freeze register (required at Phase 1 endpoint; quote before Phase 2 / Experimental Generation)

| Gap ID | One-sentence freeze lock |
|--------|--------------------------|
| G1 | The **job**: existence/construction vs locked out-of-sample skill vs after-cost economic value. |
| G2 | The **height** of “can” (P-Logical / P-NonNegligible / P-BaseCase); height ≠ met. |
| G6 | The **grading rule**: metric + baseline that “predictive” must satisfy. |
| G3 | The **named listed contract and tenor** (futures, not a silent spot swap). |
| G4 | The **numeric target** (price / return / direction / curve). |
| G5 | The **horizon** from forecast to the print that counts. |
| G7 | The **evaluation protocol** (walk-forward vs in-sample; live vs stand-in). |
| G8 | The **named model class** — **G1/G6-dependent**; do not pretend empirical closure first. |

*Later candidates must quote the freeze line for any parameter they claim to close. Changing the freeze line is a claim change, not progress.*

---

## Priority Order (highest sum first)

1. **G1 Object** (tied with G6/G3 on sum; dominant blocker — dependents hang on it)  
2. **G6 Success metric + baseline**  
3. **G3 Contract identity**  
4. **G2 “Can” modal bar**  
5. G4 Target · G5 Horizon · G7 Protocol  
6. **G8 Model class (dependent)** — do not attack first  

Lean Default Path: attack **G1+G2+G6** as one lock package (contract/horizon/target ride in the package). Do not open architecture bake-offs or trading-book design while the job is unset.

---

## Inter-parameter dependency (mandatory)

**G8** (and any architecture census) is currently blocked primarily by unset **G1** and **G6**. G4/G5/G7 are also G1-shaped: an existence object scopes them out or freezes them loosely; a skill/value object must lock them.

**Rectification:** operator selects a lock package in `R_Locking_Scaffolding.md`. Then re-open only the dependents that package marks in-scope.

**Reopen condition (prominent):** After `lock Rank N` (or à-la-carte with OR-slots resolved), re-score Amb and run only tests the package licenses. Do not auto-enter Phase 2. Named-class pulse only if the source class is already **named enough** and non-circular.

---

## Search Plan for Top-Priority Gap(s)

**Targeted gap:** G1/G2/G6 via locking-scaffolding — **not** material search until the operator picks a package.  
**Source classes to check:** none yet (unnamed). After a skill lock, a public series must be **named** (`name source class …`) before a pulse; “some oil-forecasting papers” is unnamed.  
**Diminishing-returns / time-box rule:** Do not hunt models to “answer yes” while three jobs remain live. One lock-pick turn, then hygiene.  
**Notes:** Existence of forecasting *software* or *spot* oil papers is not a silent admit for a locked futures skill bar (print-match ≠ clearance).

---

## Ready for Material Search & Admission Checks?

- [ ] Yes  
- [x] Need operator lock pick first (`R_Locking_Scaffolding.md`). Material search before that would pick a job by shopping sources.
