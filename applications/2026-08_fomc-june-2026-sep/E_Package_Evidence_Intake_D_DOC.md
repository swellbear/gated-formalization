# Package-Satisfying Evidence Intake — D-DOC (SEP process/identity)

**Date:** 2026-08-12  
**Application:** `2026-08_fomc-june-2026-sep`  
**Locked package / scope label:** L1 OBJECT-FORECAST + L2 F-ML P-BaseCase (bar not met)  
**Target dependent(s):** D-DOC (process/identity census)

---

## 1. Lock schema (must match freeze)
| Slot | Required by lock | Value in this artifact |
|------|------------------|------------------------|
| Object | forecast | Census of *what the SEP is/says about itself*, not F-ML met |
| F-ML bar | P-BaseCase | Not tested by this artifact |
| ODD / domain | June 17 2026 SEP | Same PDF/HTML |
| Metrics | process facts | Release time, meeting, submitter counts, vintage |
| Matching conditions | live primary | Official .gov release |
| OR-slots | n/a | |

**Schema match?** Yes — document identity under the forecast object, without claiming P-BaseCase clearance.

---

## 2. Artifact summary
**Source / citation:**  
[fomcprojtabl20260617.pdf](https://www.federalreserve.gov/monetarypolicy/files/fomcprojtabl20260617.pdf) · [accessible HTML](https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260617.htm) · inventory A in [`CLAIM_INVENTORY.md`](CLAIM_INVENTORY.md)

**What it reports (concise):**  
SEP for the June 16–17, 2026 FOMC meeting, released 2:00 p.m. EDT June 17, 2026. Eighteen participants submitted; one of those 18 skipped 2028. Nineteen had submitted in March (meeting March 17–18, 2026). Prose: most-likely outcomes under each participant’s appropriate policy; longer-run = convergence under appropriate policy and no further shocks; considerable uncertainty; models imperfect.

**Sample / setup limits:** Official publication of the projections themselves. Not an independent audit of 2026–28 outcomes.

### Conflicted-source flag (mandatory)
- [x] **Non-conflicted** for *document identity* (official primary of the claim package)
- [ ] **Conflicted / interest-aligned** for *F-ML-BAR met* if used as sole proof that medians are the economy’s base case — **not so used here**

**If used to clear F-ML-BAR:** would be the forecast’s own brochure. This intake is **not** that use.

### Quantitative bar?
No — process/identity only. No `E_Quantitative_Evidence_Rubric` for D-DOC.

---

## 3. Provisional gate intent (before full `04`)
- [x] Aim **ADMIT** as constraining D-DOC  
- [ ] Aim **HOLD**  
- [ ] Aim **REJECT**

**ADMIT bar for this freeze:** Official SEP states the process facts in inventory A.  
**HOLD bar:** n/a  
**REJECT triggers:** Using this to clear F-ML-BAR or July 29 commitment.

---

## 4. Scoped-result honesty
Findings, if admitted, hold **under:** this PDF/HTML as of the June 17, 2026 release.  
**Partial / claim-adjacent?** No for D-DOC; yes if smuggled into F-ML.  
**Must not be promoted to:** F-ML-BAR met; C-APPROP met; F-LR met; Committee forecast; 2026–28 realization; July 29 “will deliver.”

---

## 5. Next
- [x] Proceed to formal `04c`  
- [ ] Stop
