# Gap Extraction & Ranking Sheet

**Date:** 2026-08-12  
**Parent application / claim:** `2026-08_fl-property-tax-abolish-10y` — question as intake  
**Linked Gate Scoring Sheet:** `02_Gate_Scoring_Sheet.md` (Cycle 0)

---

## Identified Gaps (Free Parameters)

### Gap 1 — Speech act
**Description:** Keep the intake as a question, or freeze candidate **answers** as claims under a lock. Scoring the interrogative as established is disallowed.

**Claim-freeze (LOCKED Rank 1 Q1):**  
The intake remains a question; the testable unit is the Rank 1 candidate answer-claim, not the interrogative itself.

**Impact (0–2):** 2  
**Anchor connection (0–2):** 2  
**Measurability (0–2):** 2  
**Sum:** 6  

### Gap 2 — “Abolished”
**Description:** Repeal of ad valorem as a class vs large cuts vs homestead/exemption so typical owners pay ~0 vs replacement by another tax.

**Claim-freeze (LOCKED Rank 1 A1):**  
“Abolished” = legal end of general ad valorem millage on real property as a class (not a cut, not homestead-to-zero, not a swap that keeps the levy).

**Impact (0–2):** 2  
**Anchor connection (0–2):** 2  
**Measurability (0–2):** 2  
**Sum:** 6  

### Gap 3 — “Likely” bar
**Description:** P-Logical (not impossible) vs P-NonNegligible (live shot) vs P-BaseCase (expected/central path). Silent P-BaseCase is disallowed.

**Claim-freeze (LOCKED Rank 1 L3):**  
“Likely” = P-BaseCase: abolition is the expected/central path inside the locked window (not merely possible, not merely a live long-shot). **Bar locked ≠ bar met.**

**Impact (0–2):** 2  
**Anchor connection (0–2):** 1  
**Measurability (0–2):** 1  
**Sum:** 4  

### Gap 4 — Scope (which levies / geography)
**Description:** Statewide all general millage (county + school + municipal + special district) vs some locals vs school-only vs a “state property tax” that Florida does not levy as a class.

**Claim-freeze (LOCKED Rank 1 S1):**  
Scope = statewide: counties, school districts, municipalities, and special districts cannot levy general ad valorem on real property.

**Impact (0–2):** 2  
**Anchor connection (0–2):** 2  
**Measurability (0–2):** 2  
**Sum:** 6  

### Gap 5 — Window
**Description:** Rolling 10 years from the ask date vs calendar years 2027–2036 vs “this decade.”

**Claim-freeze (LOCKED Rank 1 W1):**  
Window = **2026-08-12 through 2036-08-12** (rolling 10 years from the question date).

**Impact (0–2):** 1  
**Anchor connection (0–2):** 2  
**Measurability (0–2):** 2  
**Sum:** 5  

### Gap 6 — Replacement (dependent)
**Description:** Whether “abolished” allows a successor tax that keeps a property-based levy. Blocked until Gap 2.

**Claim-freeze (LOCKED Rank 1 with A1):**  
A renamed or successor ad valorem levy still counts as **not abolished**.

**Impact (0–2):** 1  
**Anchor connection (0–2):** 1  
**Measurability (0–2):** 1  
**Sum:** 3  

---

## Claim-freeze register (required at Phase 1 endpoint; quote before Phase 2 / Experimental Generation)

| Gap ID | One-sentence freeze lock |
|--------|--------------------------|
| G1 | **LOCKED Rank 1 Q1:** Intake remains a question; testable unit = Rank 1 candidate answer-claim. |
| G2 | **LOCKED Rank 1 A1:** Abolished = legal end of general ad valorem millage as a class. |
| G3 | **LOCKED Rank 1 L3:** Likely = P-BaseCase inside W1. Bar locked ≠ bar met. |
| G4 | **LOCKED Rank 1 S1:** Statewide all general millage classes. |
| G5 | **LOCKED Rank 1 W1:** 2026-08-12 through 2036-08-12. |
| G6 | **LOCKED Rank 1 with A1:** Successor ad valorem still = not abolished. |

*Later candidates must quote the freeze line for any parameter they claim to close. Changing the freeze line is a claim change, not progress.*

---

## Priority Order (highest sum first)

1. Gap 1 — Speech act (dominant; autonomy split)  
2. Gap 2 — Abolished (dominant; blocks D-LAW object and forecast object)  
3. Gap 4 — Scope (tied with G2 for object)  
4. Gap 5 — Window  
5. Gap 3 — Likely bar (dominant for F-FORWARD; lower sum because measurability of “expected path” is harder)  
6. Gap 6 — Replacement (dependent on G2)

**Rectification (done for G1–G6):** operator selected Rank 1 on 2026-08-12 (`Lock_Rank1_Q1A1L3S1W1.md`). Live vs stand-in **locked**. D-LAW **admitted**. F-FORWARD: operator **`leave unnamed`** (Phase 1 endpoint). Untested ≠ unlikely.

---

## Search Plan for Top-Priority Gap(s)

**Targeted gap:** G1–G6 locked. D-LAW **admitted**. F-FORWARD **leave unnamed** (Phase 1 endpoint).  
**Source classes to check:** C1–C4 **REJECT** as Rank 1 vehicles. C5 not filled. No further search until `name source class C5: …`.  
**Diminishing-returns / time-box rule:** Phase 1 search on this leftover stopped by operator `leave unnamed`.  
**Notes:** Untested ≠ unlikely. Problem substitution (Amendment 3) → CR optional, not this leftover.

---

## Ready for Material Search & Admission Checks?

- [x] D-LAW — done (`04_Material_Admission_D_LAW.md`)  
- [x] F-FORWARD — **stopped** (`leave unnamed`); park-until-trigger
