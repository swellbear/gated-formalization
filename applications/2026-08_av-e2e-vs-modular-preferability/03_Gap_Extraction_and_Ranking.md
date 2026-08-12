# Gap Extraction & Ranking Sheet

**Date:** 2026-08-11  
**Parent application / claim:** `2026-08_av-e2e-vs-modular-preferability`  
**Linked Gate Scoring Sheet:** `02_Gate_Scoring_Sheet.md`

---

## Identified Gaps (Free Parameters)

### Gap 1 — Architecture labels
**Description:** What counts as end-to-end vs modular vs hybrid.  

**Claim-freeze (one sentence — lock what this free parameter *is*):**  
Whether the claim’s exclusive E2E-vs-modular contrast is well-defined once hybrids and learned modules inside modular stacks are acknowledged.

**Impact (0–2):** 2  
**Anchor connection (0–2):** 2 (L₀.1, L₀.4, L₀.6)  
**Measurability (0–2):** 2  
**Sum:** 6  

### Gap 2 — Cascading / interface errors
**Description:** Scope of “cascading errors from hand-engineered interfaces” and whether E2E avoids cascading failure modes rather than relocating them.  

**Claim-freeze (one sentence):**  
Whether avoiding hand-engineered interfaces uniquely eliminates cascading error propagation, or only removes one engineering locus of composition error.

**Impact (0–2):** 2  
**Anchor connection (0–2):** 2 (L₀.2)  
**Measurability (0–2):** 1  
**Sum:** 5  

### Gap 3 — “Alone” uniqueness
**Description:** Exclusive claim that only E2E avoids the cited failure mode.  

**Claim-freeze (one sentence):**  
Whether E2E is the *unique* architecture class that avoids the relevant cascading-interface problem (as opposed to one approach among several, including better interfaces / hybrids).

**Impact (0–2):** 2  
**Anchor connection (0–2):** 1  
**Measurability (0–2):** 1  
**Sum:** 4  

### Gap 4 — Modular “structurally cannot” scale with data
**Description:** Claim that modular stacks structurally cannot continue to improve with data and scale the way E2E can.  

**Claim-freeze (one sentence):**  
Whether modular (including modular-with-learning) architectures are *structurally incapable* of continued system-level improvement from data/scale, in the sense asserted by the claim.

**Impact (0–2):** 2  
**Anchor connection (0–2):** 2 (L₀.3, L₀.4)  
**Measurability (0–2):** 2  
**Sum:** 6  

### Gap 5 — Preferability criteria
**Description:** On which evaluative dimensions “preferable” is asserted.  

**Claim-freeze (one sentence):**  
Which criteria (safety evidence, long-tail performance, debuggability, regulatory fit, etc.) are in force when calling E2E preferable to modular.

**Impact (0–2):** 2  
**Anchor connection (0–2):** 2 (L₀.5)  
**Measurability (0–2):** 2  
**Sum:** 6  

### Gap 6 — Scope / comparison class
**Description:** ODD, metrics, and which systems are being compared.  

**Claim-freeze (one sentence):**  
For which operational design domains, metrics, and comparison class the preferability/uniqueness claims are supposed to hold.

**Impact (0–2):** 1  
**Anchor connection (0–2):** 1  
**Measurability (0–2):** 2  
**Sum:** 4  

---

## Claim-freeze register (required at Phase 1 endpoint; quote before Phase 2 / Experimental Generation)

| Gap ID | One-sentence freeze lock |
|--------|--------------------------|
| G1 | Whether the claim’s exclusive E2E-vs-modular contrast is well-defined once hybrids and learned modules inside modular stacks are acknowledged. |
| G2 | Whether avoiding hand-engineered interfaces uniquely eliminates cascading error propagation, or only removes one engineering locus of composition error. |
| G3 | Whether E2E is the *unique* architecture class that avoids the relevant cascading-interface problem. |
| G4 | Whether modular (including modular-with-learning) architectures are *structurally incapable* of continued system-level improvement from data/scale. |
| G5 / R3 | Which criteria are in force when calling E2E preferable to modular. |
| G6 / R4 | For which ODD, metrics, and comparison class the claims are supposed to hold. |
| **R1 (R4-dependent)** | Whether, for a specified spectrum pair and ODD/metrics, E2E shows a *relative* closed-loop scaling / joint-optimization advantage vs modular-with-learning. |
| **R2 (R4-dependent)** | Relative magnitude of hand-engineered interface cascades vs E2E compounding/distribution-shift errors under matched conditions. |

**Dependency (first-class):** R1 and R2 are currently blocked primarily by the unset status of R4. Their general forms remain under-determined largely because R4 is free.  
**Rectification:** lock a concrete R4 (architecture pair + ODD + metrics + matching conditions), then re-open R1 and R2 as scoped technical questions under that freeze.  
**Reopen:** only after that R4 lock.

*Later candidates must quote the freeze line for any parameter they claim to close. Changing the freeze line is a claim change, not progress.*

---

## Priority Order (highest sum first)

1. G1 Architecture labels  
2. G4 Modular “structurally cannot”  
3. G5 Preferability criteria  
4. G2 Cascading errors  
5. G3 “Alone” uniqueness  
6. G6 Scope / comparison class  

---

## Search Plan for Top-Priority Gap(s)

**Targeted gap:** G1, G4, G5 first (definition + structural impossibility + preferability lock)  
**Source classes to check:** AV architecture surveys; industry practice on hybrids; known modular learning components; multi-criterion AV evaluation  
**Diminishing-returns / time-box rule:** Admit only definitional/structural locks that reduce Amb without smuggling preferability; stop a cycle when next candidates only restate advocacy.  
**Notes:** Technical domain — Phase 2 may later be applicable to residual structural gaps; preferability may remain Mixed/not Phase-2-applicable without criterion carve-out.

---

## Ready for Material Search & Admission Checks?

- [x] Yes  
- [ ] Need to refine gap definitions first
