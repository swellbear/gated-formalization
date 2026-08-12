# Package-Satisfying Evidence Intake — F-ML-BAR test on 2026 medians

**Date:** 2026-08-12  
**Application:** `2026-08_fomc-june-2026-sep`  
**Locked package / scope label:** L1–L12  
**Target dependent:** Does any **2026** GDP / unemployment / PCE / core-PCE **median** meet F-ML-BAR (P-BaseCase)?  
**Operator:** `test F-ML-BAR on 2026 medians` (2026-08-12)  
**Rubric:** [`E_Quantitative_Evidence_Rubric_F_ML_2026.md`](E_Quantitative_Evidence_Rubric_F_ML_2026.md)

**Quote freeze (L2):** A June 17 SEP figure is a “most likely outcome” claim only if it is the **expected / central path** for that variable and window. Printing Table 1 does not clear P-BaseCase. Funds-rate dots are not under this bar.

**G4 note:** This test uses the G4 *default* (median of 18) because the operator named **2026 medians**. G4 is **not** locked by this test. A later different load-bearing statistic would require a re-test.

---

## 1. Lock schema (must match freeze)
| Slot | Required by lock | Value in this artifact |
|------|------------------|------------------------|
| Object | forecast | Test whether submitted 2026 medians **are** the expected/central path |
| F-ML bar | P-BaseCase | Under test, not assumed met |
| Window | 2026 only | Not 2027–28, not longer run |
| Variables | GDP, U, PCE, core PCE | Funds-rate **excluded** |
| Statistic | median (G4 default) | 18 submitters |
| Matching conditions | live primary + already-admitted layers | No new source; July 29 OUT |

**Schema match?** Yes — this is the L2 residual (“whether any median meets P-BaseCase”), scoped to 2026 as authorized.

---

## 2. Candidates (already admitted as D-SEP, not as outcomes)

| Variable | 2026 median (L5) | 2026 CT / range (L5) | 2026 histogram peak (L8) | Other admitted context |
|----------|------------------|----------------------|--------------------------|------------------------|
| Real GDP Q4/Q4 | **2.2** | CT 2.0–2.3; range 1.8–2.6 | 9 of 18 in 2.2–2.3 | L7: March 2.4 → June 2.2 |
| Unemployment Q4 avg | **4.3** | CT 4.3–4.4; range 4.3–4.6 | 13 of 18 in 4.2–4.3 | L7: March 4.4 → June 4.3 |
| PCE Q4/Q4 | **3.6** | CT 3.5–3.7; range 2.7–4.1 | 9 of 18 in 3.5–3.6 | L7: March 2.7 → June 3.6 (**+0.9**); L9: **17/18** uncertainty higher **and** risks upside; L10: printed 70% band 2.6–4.6 (historical RMSE; CPI not PCE) |
| Core PCE Q4/Q4 | **3.3** | CT 3.2–3.5; range 2.6–3.5 | 10 of 18 in 3.3–3.4 | L7: March 2.7 → June 3.3 (**+0.6**); L9: **17/18** uncertainty higher **and** risks upside |

**Not a candidate:** 2026 funds-rate median **3.8** (L2 / B15 / L11).

---

## 3. What would meet the bar

The median must be shown to be the **expected / central path of the variable** (the 2026 outcome path), not merely:

- that the PDF says “most likely outcomes” (K1 / L3 — already admitted as document text);
- that 18 people submitted numbers and the middle one is X (L5 — already admitted as census);
- that submissions cluster near X (L8 — already admitted as distributional census);
- that X is a live possibility (P-NonNegligible — not the locked bar).

Independent establishment would need a matched expected-path object under the same locks (same window, same variable definitions, not just the SEP brochure). None is admitted.

---

## 4. Blocking facts already on the record (not new search)

1. **Brochure / conflicted for clearance.** The only source that 2.2 / 4.3 / 3.6 / 3.3 *are* the economy’s expected path is the SEP’s own “most likely” label plus the median of those labels. L4/L5 intakes already flagged that use as conflicted for F-ML-BAR met. LOCK-010: posed ≠ clearance. LOCK-011: printed SEP ≠ realized path.

2. **Policy-mix incoherence (L11).** Each GDP, unemployment, and inflation submission is conditioned on **that participant’s** appropriate-policy path. The 2026 GDP median is not generated under the same funds-rate path as the 2026 PCE median. A joint “expected path for the economy” is not identified.

3. **Expected vs most-likely (L9, PCE/core).** P-BaseCase was locked as **expected / central** path. **17 of 18** participants judge 2026 PCE (and core PCE) risks **to the upside** and uncertainty **higher** than average. If the risk distribution is skewed up, the mean expected inflation can sit above the mode/median of “most likely” point submissions. L2 said high uncertainty can coexist with a well-posed base-case *claim*; it did not say upside-skewed risk tallies *establish* that the median equals the expected path.

4. **Vintage fragility (L7).** The candidate 2026 PCE “central path” moved **0.9 pp** between March and June (2.7 → 3.6). A quantity that jumps by that much across adjacent SEPs is a poor identification of *the* expected 2026 path as of a stable object — and this test has no non-SEP anchor to choose June over March except that June is the claim package.

5. **Historical-error width ≠ identification (L10).** Printed 2026 PCE 70% band **2.6 to 4.6** around 3.6 is a 2006–2025 RMSE convention, CPI not PCE, and the document says it may not match current judgments. Width does not refute a point base case by itself; it also does not identify 3.6 as the expected path.

6. **Document’s own humility (L3).** “Considerable uncertainty attends these projections”; models are “necessarily imperfect.” Compatible with a posed base case; not establishment.

---

## 5. What clustering does *not* do

L8 shows tight-ish 2026 piles (especially unemployment, 13/18 in 4.2–4.3). That supports L5: the median is a representative census statistic of *submissions*. L2 already separated that census from P-BaseCase clearance. Clustering of brochure points is not an independent expected-path.

---

## 6. Provisional gate intent
- [x] Aim **ADMIT** the **test result**: F-ML-BAR **not established** for 2026 GDP, U, PCE, and core PCE medians  
- [ ] Aim **ADMIT** F-ML-BAR **met** for any of those four  
- [ ] Aim **REFUTE** (that would require an admitted rival expected path showing the medians are not central)  
- [ ] Aim **HOLD**

**REJECT triggers for “met”:** brochure-only clearance; median → Committee forecast; SEP → will happen; treating L8 clustering as P-BaseCase; putting funds-rate 3.8 on this bar; importing July 29; silently locking G4.

## 7. Scoped-result honesty
The test holds **under:** L1–L12, 2026 window, G4-default medians, no new source.  
**Must not be promoted to:** F-ML-BAR met; refutation of 2026 medians as a live possibility; 2027–28/LR clearance or failure; realization; July 29.
