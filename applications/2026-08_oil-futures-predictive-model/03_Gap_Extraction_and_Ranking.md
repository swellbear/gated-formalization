# Gap Extraction & Ranking Sheet — Cycle 0

> **Plain language.** Name leftover choices, freeze what each leftover *is*, rank which ones matter most. Lean Default Path: attack only the top one or two.

**Date:** 2026-08-17  
**Parent application / claim:** `2026-08_oil-futures-predictive-model` — Can a predictive model for oil futures be built?  
**Linked Gate Scoring Sheet:** `02_Gate_Scoring_Sheet.md` · `02_Gate_Scoring_After_Rank4.md` · `02_Gate_Scoring_After_VCOST.md`  

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
| G1 | **LOCKED Rank 4:** three jobs, not one object — D-EXIST (claim-under-test) ⊂ F-SKILL ⊂ V-VALUE (elevations). |
| G2 | **LOCKED per leg:** D-EXIST P-Logical; F-SKILL P-NonNegligible; V-VALUE P-NonNegligible. Height ≠ met. |
| G6 | **LOCKED per leg:** D-EXIST S1 any specified mapping **except** last-settlement no-change as the model exhibit (operator B); F-SKILL RMSE vs last-settlement; V-VALUE after-cost P/L vs curve. |
| D-SRC | D-EXIST exhibit — **established** (futures-target only, 2026-08-17). No-change **OUT**. Spot/real-price **OUT**. Menu ≠ singleton pick. |
| G3 | **LOCKED per leg:** D-EXIST C3 class (WTI or Brent, either); F-SKILL/V-VALUE C1 NYMEX CL front-month. |
| G4 | **LOCKED per leg:** D-EXIST T2 price-level census; F-SKILL/V-VALUE T1 next-session log-return. |
| G5 | **LOCKED per leg:** D-EXIST H3 open (census); F-SKILL/V-VALUE H1 next session as **F-CC** (settlement-to-settlement). **L-SESS:** F-ON = settlement→next official open; F-DAY = official open→same-day settlement. Combo is a **third** test, not a substitute. |
| G7 | **LOCKED per leg:** D-EXIST E3 census; F-SKILL/V-VALUE E1 walk-forward. Live vs stand-in for settlements still open. |
| G8 | Named model class under F-SKILL — **re-opened**; not a D-EXIST requirement. |
| V-COST | V-VALUE cost schedule — **either accepted** (V1 or V2; each test must name which). Incomplete as a singleton. |
| F-SRC | Named public class for F-SKILL — **leave unnamed** (operator B); F-SKILL **not established**; live residual; do not invent a class. Later pulse must **report F-ON and F-DAY** separately (`Lock_Session_Split.md`). |
| V-SRC | Named recipe/book for V-VALUE — **leave unnamed** (operator B); V-VALUE-TEST-0 **not established**; not a refute. |
| F-COMBO | Named switching rule — **park-until-trigger** (rule in advance + F-ON and F-DAY already scored separately). |

*Later candidates must quote the freeze line for any parameter they claim to close. Changing the freeze line is a claim change, not progress.*

---

## Priority Order (highest sum first)

1. **F-SRC** — sealed leave unnamed; **live residual** (skill test); reopen only with `name source class …`  
2. **G8** / live vs stand-in — F-SRC-dependent  
3. **V-SRC** — sealed leave unnamed; reopen only with `name source class …`  

Lean Default Path: do **not** invent a skill class. Existence stays separate. Next operator fork is reopen / endpoint / closeout. Do not auto-pulse. Do not enter Phase 2.

---

## Inter-parameter dependency (mandatory)

**D-EXIST** is **established** (futures-target only). **F-SKILL** is blocked primarily by **F-SRC leave unnamed** (live residual; do not invent a class). **V-VALUE** is blocked primarily by **V-SRC leave unnamed**.

**Rectification:** `name source class …` matching NYMEX CL official open/settlement stamps (report F-CC, F-ON, and F-DAY separately), or `endpoint only` / `closeout`. Do not auto-enter Phase 2. Do not treat the existence menu or a USO half-hour paper as F-SRC. Combo does not skip the queue.

**Reopen condition (prominent):** After a named-enough non-circular F-SKILL class, or `endpoint only` / `closeout`.

---

## Search Plan for Top-Priority Gap(s)

**Targeted gap:** F-SRC leave unnamed (live residual).  
**Source classes to check:** None. Do not invent. Do not relabel L-D-SUITE / EIA STEO / Alquist–Kilian as F-SKILL.  
**Diminishing-returns / time-box rule:** Leave-unnamed is the seal. Existence met ≠ skill met.  
**Notes:** `Lock_FSRC_Leave_Unnamed.md`.

---

## Ready for Material Search & Admission Checks?

- [x] Yes — F-SRC sealed leave unnamed; **stop** (live skill residual; no invented class)  
- [ ] Need operator lock pick first
