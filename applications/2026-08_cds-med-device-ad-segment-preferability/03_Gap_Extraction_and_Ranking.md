# Gap Extraction & Ranking Sheet

**Date:** 2026-08-12  
**Parent application / claim:** Med device = best next CDS ad segment  
**Linked Gate Scoring Sheet:** `02_Gate_Scoring_Sheet.md`

---

## Identified Gaps (Free Parameters)

### Gap 1 — G1 Comparison class
**Description:** Which alternative advertiser segments are in the “next place to play” race?  

**Claim-freeze (one sentence — lock what this free parameter *is*):**  
C₀ = the finite set of expansion segments against which med device must win “best next” (must be named; membership changes = claim change).  

**Impact (0–2):** 2  
**Anchor connection (0–2):** 2 (A4, A5)  
**Measurability (0–2):** 2 (operator can name; competitive intel can refine)  
**Sum:** **6**

### Gap 2 — G2 Preferability criteria
**Description:** What makes a segment “best” (weights on revenue potential, sales-cycle speed, compliance risk, inventory fit, strategic option value, etc.)?  

**Claim-freeze:**  
“Best next” = argmax over C₀ of a locked criteria vector V with stated weights / lexicographic order for this decision.  

**Impact (0–2):** 2  
**Anchor connection (0–2):** 2 (A5)  
**Measurability (0–2):** 1 (operator preference + finance constraints)  
**Sum:** **5**

### Gap 3 — G3 Med-device scope
**Description:** Which device subsegments count (capital, implant, disposable, digital, imaging, etc.)?  

**Claim-freeze:**  
“Med device” for this claim = named subsegment set S (and exclusions).  

**Impact (0–2):** 2  
**Anchor connection (0–2):** 1  
**Measurability (0–2):** 2  
**Sum:** **5**

### Gap 4 — G4 Platform fit
**Description:** Does *this* CDS’s specialty mix, workflow moments, and inventory match device buyer needs vs alternatives?  

**Claim-freeze:**  
Fit evidence must be about this platform’s audience/workflow (or a stipulated proxy), not generic HCP media.  

**Impact (0–2):** 2  
**Anchor connection (0–2):** 1  
**Measurability (0–2):** 1 (needs internal data / sales)  
**Sum:** **4**

### Gap 5 — G5 Commercial evidence bar
**Description:** What evidence establishes win vs alternatives (pipeline, willingness-to-pay, case studies, category spend)?  

**Claim-freeze:**  
Establish/refute “dominates on V” only via evidence meeting a stated commercial bar B (e.g. matched comparison on V components).  

**Impact (0–2):** 1  
**Anchor connection (0–2):** 1  
**Measurability (0–2):** 1  
**Sum:** **3**

### Gap 6 — G6 Compliance / promo risk
**Description:** Relative promotional/compliance friction for device vs pharma vs other C₀ members on this platform.  

**Claim-freeze:**  
Risk differential enters V only if locked as a criterion; otherwise out of preferability test.  

**Impact (0–2):** 1  
**Anchor connection (0–2):** 2 (A6)  
**Measurability (0–2):** 1  
**Sum:** **4**

---

## Claim-freeze register

| Gap ID | One-sentence freeze lock |
|--------|--------------------------|
| G1 | C₀ = named finite set of rival expansion segments |
| G2 | “Best” = argmax on locked criteria vector V |
| G3 | “Med device” = named subsegment set S |
| G4 | Fit evidence is platform-specific (or stipulated proxy) |
| G5 | Dominance on V only via commercial bar B |
| G6 | Compliance risk in V only if locked as criterion |

---

## Priority Order (highest sum first)

1. **G1** Comparison class C₀  
2. **G2** Preferability criteria V  
3. **G3** Med-device scope S  
4. **G4** / **G6** Platform fit & compliance (tie → operator choice)  
5. **G5** Commercial evidence bar B  

---

## Search Plan for Top-Priority Gap(s)

**Targeted gap:** G1 + G2 (locking-scaffolding first — evidence without locks will not establish “best”)  
**Source classes to check:** Operator strategy docs; sales pipeline by category; HCP media category maps; compliance constraints  
**Diminishing-returns / time-box rule:** Do not run broad “med device TAM” search until C₀ and V are locked  
**Notes:** Pattern match to preferability apps — lock before Phase 2 comparative tests.

---

## Ready for Material Search & Admission Checks?

- [ ] Yes — after lock authorization  
- [x] Need to refine gap definitions first — **authorize locking-scaffolding** (or revise claim to descriptive viability)
