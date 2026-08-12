# Package-Satisfying Evidence Intake — remaining D-* census (submitted / printed, not outcomes)

**Date:** 2026-08-12  
**Application:** `2026-08_fomc-june-2026-sep`  
**Locked package / scope label:** L1 OBJECT-FORECAST + L2 F-ML P-BaseCase (bar not met) + L3 D-DOC + L4 D-DEF  
**Target dependents:** D-ACTUAL (C) · D-SEP (D–E) · D-REV (F) · D-DOTS / D-HIST (G–H) · D-UNCERT (I) · D-RMSE (J)  
**Operator:** `admit all remaining layers in question` (2026-08-12)

**Claim form (all sections):** “The June 17, 2026 SEP prints X.” Not: “X will occur.” Not: “X is the Committee’s forecast.” Not: F-ML-BAR met.

**Source:** [SEP PDF](https://www.federalreserve.gov/monetarypolicy/files/fomcprojtabl20260617.pdf) · [accessible HTML](https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260617.htm) · [`CLAIM_INVENTORY.md`](CLAIM_INVENTORY.md)  
**OUT:** July 29, 2026 FOMC statement.

---

## 1. Lock schema (must match freeze)
| Slot | Required by lock | Value in this artifact |
|------|------------------|------------------------|
| Object | forecast | Census of *what the SEP prints*, under the forecast object, not F-ML met |
| F-ML bar | P-BaseCase | Not tested; printing ≠ meeting the bar |
| ODD / domain | June 17 2026 SEP | Same PDF/HTML |
| Metrics | printed cells / tallies / fans | Inventory C–J |
| Matching conditions | live primary | Official .gov release |
| OR-slots | n/a | |

**Schema match?** Yes — remaining descriptive-census vehicle. Does not clear P-BaseCase, C-APPROP-as-vote, F-LR-as-dated-unconditional, or 2026–28 realization.

### Conflicted-source flag (mandatory)
- [x] **Non-conflicted** for *what the official SEP prints*
- [ ] **Conflicted / interest-aligned** for *F-ML-BAR met* if used as sole proof that medians are the economy’s base case — **not so used here**

---

## 2. D-ACTUAL — inventory C (2021–2025 printed as “Actual”)

*These are claims the document prints as “Actual.” They are not independently re-verified here. They are not 2026–28 realization.*

| Series | 2021 | 2022 | 2023 | 2024 | 2025 |
|--------|------|------|------|------|------|
| Real GDP Q4/Q4 | 5.8 | 1.3 | 3.4 | 2.4 | 2.0 |
| Unemployment (Q4 avg) | 4.2 | 3.6 | 3.8 | 4.1 | 4.5 |
| PCE inflation | 5.8 | 6.0 | 2.9 | 2.6 | 2.8 |
| Core PCE | 4.8 | 5.2 | 3.3 | 3.0 | 2.9 |
| Funds rate (year-end midpoint) | 0.1 | 4.4 | 5.4 | 4.4 | 3.6 |

---

## 3. D-SEP — inventory D–E (June Table 1 as submitted)

*Claim form: “The median / CT / range of submitted June projections is X.” G4 default used in quoting: medians are the load-bearing census quotes; CT/range remain distributional. G4 freeze remains open unless separately locked.*

### D — medians

| Variable | 2026 | 2027 | 2028 | Longer run |
|----------|------|------|------|------------|
| Change in real GDP | 2.2 | 2.3 | 2.2 | 2.0 |
| Unemployment rate | 4.3 | 4.3 | 4.2 | 4.2 |
| PCE inflation | 3.6 | 2.3 | 2.0 | 2.0 |
| Core PCE inflation | 3.3 | 2.5 | 2.1 | *(not collected)* |
| Federal funds rate (appropriate path) | 3.8 | 3.6 | 3.4 | 3.1 |

Funds-rate row is a census of **appropriate-path midpoints** (L4 B4/B15). It is **not** under F-ML-BAR.

### E — central tendency and range

| Variable | 2026 CT | 2027 CT | 2028 CT | LR CT | 2026 range | 2027 range | 2028 range | LR range |
|----------|---------|---------|---------|-------|------------|------------|------------|----------|
| Real GDP | 2.0–2.3 | 2.0–2.4 | 2.0–2.3 | 1.8–2.0 | 1.8–2.6 | 1.9–2.9 | 1.8–2.6 | 1.7–2.5 |
| Unemployment | 4.3–4.4 | 4.2–4.5 | 4.1–4.3 | 4.0–4.3 | 4.3–4.6 | 4.0–4.6 | 4.0–4.4 | 3.8–4.5 |
| PCE inflation | 3.5–3.7 | 2.2–2.5 | 2.0–2.1 | 2.0 | 2.7–4.1 | 1.9–2.8 | 2.0–2.3 | 2.0 |
| Core PCE | 3.2–3.5 | 2.3–2.6 | 2.0–2.2 | — | 2.6–3.5 | 2.0–3.0 | 2.0–2.4 | — |
| Fed funds | 3.6–4.1 | 3.1–3.9 | 3.1–3.6 | 3.0–3.5 | 3.4–4.4 | 2.9–4.4 | 2.9–3.9 | 2.9–3.9 |

PCE longer-run CT and range are both **2.0** (all 18 in that cell). That is a census of submissions, not F-LR-BAR met and not 2026 PCE 3.6 “on the way to target.”

---

## 4. D-REV — inventory F (March vs June printed medians)

*Claim form: “The document prints March median Y; June median is X.” Revision is a derived census claim, not a causal claim about why.*

| Variable | Mar 2026 | Jun 2026 | Mar 2027 | Jun 2027 | Mar 2028 | Jun 2028 | Mar LR | Jun LR |
|----------|----------|----------|----------|----------|----------|----------|--------|--------|
| Real GDP | 2.4 | 2.2 | 2.3 | 2.3 | 2.1 | 2.2 | 2.0 | 2.0 |
| Unemployment | 4.4 | 4.3 | 4.3 | 4.3 | 4.2 | 4.2 | 4.2 | 4.2 |
| PCE | 2.7 | 3.6 | 2.2 | 2.3 | 2.0 | 2.0 | 2.0 | 2.0 |
| Core PCE | 2.7 | 3.3 | 2.2 | 2.5 | 2.0 | 2.1 | — | — |
| Fed funds | 3.4 | 3.8 | 3.1 | 3.6 | 3.1 | 3.4 | 3.1 | 3.1 |

**Salient derived census:** 2026 PCE median **+0.9 pp**; 2026 core PCE **+0.6 pp**; 2026 funds-rate median **+0.4 pp**; 2026 GDP median **−0.2 pp**.

---

## 5. D-DOTS / D-HIST — inventory G–H

### G — Figure 2 June dots (appropriate funds-rate midpoints)

Counts of participants. 2028 column sums to 17 (one non-submitter).

| Midpoint (%) | 2026 | 2027 | 2028 | Longer run |
|--------------|------|------|------|------------|
| 4.375 | 1 | 1 | | |
| 4.125 | 5 | 2 | | |
| 3.875 | 3 | 5 | 3 | 1 |
| 3.750 | | | | 1 |
| 3.625 | 8 | 2 | 5 | 1 |
| 3.500 | | | | 1 |
| 3.375 | 1 | 3 | 2 | 2 |
| 3.250 | | | | 1 |
| 3.125 | | 4 | 6 | 2 |
| 3.000 | | | | 7 |
| 2.875 | | 1 | 1 | 2 |
| **Sum** | **18** | **18** | **17** | **18** |

**Derived census:** 2026 modal bin is **3.625** (8 of 18). Nine of 18 2026 dots are at **3.875 or above**. Longer-run modal bin is **3.000** (7 of 18).

These are C-APPROP-conditioned midpoints, not F-ML rate forecasts (B15 / L2 / L4).

### H — Figure 3 histograms (selected load-bearing bins)

**Real GDP 2026:** 1 in 1.8–1.9; 6 in 2.0–2.1; **9 in 2.2–2.3**; 1 in 2.4–2.5; 1 in 2.6–2.7.  
**Unemployment 2026:** **13 in 4.2–4.3**; 4 in 4.4–4.5; 1 in 4.6–4.7.  
**PCE 2026:** 1 in 2.7–2.8; **9 in 3.5–3.6**; 5 in 3.7–3.8; 2 in 3.9–4.0; 1 in 4.1–4.2.  
**PCE longer run:** **18 in 1.9–2.0**.  
**Core PCE 2026:** 1 in 2.5–2.6; 3 in 3.1–3.2; **10 in 3.3–3.4**; 4 in 3.5–3.6.  
**Core PCE 2028:** 8 in 1.9–2.0; 8 in 2.1–2.2; 1 in 2.3–2.4.

---

## 6. D-UNCERT — inventory I (June vs March uncertainty/risk tallies)

| Object | June Lower / Similar / Higher | March | June Downside / Balanced / Upside | March |
|--------|-------------------------------|-------|-------------------------------------|-------|
| GDP growth uncertainty | 0 / 9 / 9 | 0 / 4 / 15 | | |
| GDP growth risks | | | 5 / 10 / 3 | 14 / 5 / 0 |
| Unemployment uncertainty | 0 / 8 / 10 | 0 / 3 / 16 | | |
| Unemployment risks | | | 1 / 10 / 7 | 0 / 3 / 16 |
| PCE uncertainty | 0 / 1 / **17** | 0 / 3 / 16 | | |
| PCE risks | | | 0 / 1 / **17** | 0 / 2 / 17 |
| Core PCE uncertainty | 0 / 1 / **17** | 0 / 4 / 15 | | |
| Core PCE risks | | | 0 / 1 / **17** | 0 / 3 / 16 |

**June 2026 diffusion index (risks):** GDP **−0.11**; unemployment **+0.33**; PCE **+0.94**; core PCE **+0.94**.  
(Index = (Upside − Downside) / N.)

This is a census of **participant judgments**. It is not the RMSE 70% fan (inventory J / L4 B14–B16). G7 remains an open freeze slot; both objects are admitted as distinct printed claims.

---

## 7. D-RMSE — inventory J (historical 70% fans, document-caveated)

| Variable | 2026 median | 70% CI (printed) | 2027 | 2028 |
|----------|-------------|------------------|------|------|
| Real GDP | 2.2 | 0.5 to 3.9 | 0.5 to 4.1 (med 2.3) | 0.0 to 4.4 (med 2.2) |
| Unemployment | 4.3 | 3.4 to 5.2 | 2.9 to 5.7 (med 4.3) | 2.3 to 6.1 (med 4.2) |
| PCE inflation | 3.6 | 2.6 to 4.6 | 0.7 to 3.9 (med 2.3) | 0.6 to 3.4 (med 2.0) |
| Fed funds | 3.8 | 3.1 to 4.5 | 1.8 to 5.4 (med 3.6) | 1.1 to 5.7 (med 3.4) |

**Table 2 ±RMSE:** GDP ±1.7 / ±1.8 / ±2.2; unemployment ±0.9 / ±1.4 / ±1.9; total consumer prices (**CPI**) ±1.0 / ±1.6 / ±1.4; short-term rates ±0.7 / ±1.8 / ±2.3 (for 2026 / 2027 / 2028).

**Document caveats (already in L4 D-DEF, restated as binding on this census):** CIs assumed symmetric; may not match participants’ current uncertainty/risk judgments; funds-rate CI not strictly consistent with SEP dots (B15); unemployment cannot be negative; Table 2 price RMSE is CPI, not PCE.

---

## 8. Provisional gate intent
- [x] Aim **ADMIT** each remaining D-* as submitted/printed census  
- [ ] Aim **HOLD**  
- [ ] Aim **REJECT**

**REJECT triggers:** Using any table to clear F-ML-BAR; median → Committee forecast; SEP → will happen; RMSE fan → current FOMC uncertainty; CPI RMSE → PCE; appropriate dots → vote; LR 2% → 2026 on-target; importing July 29.

## 9. Scoped-result honesty
Findings hold **under:** this PDF/HTML as of the June 17, 2026 release, as *what the document prints*.  
**Must not be promoted to:** F-ML-BAR met; C-APPROP as Committee vote; F-LR as dated unconditional forecast; 2026–28 realization; July 29 “will deliver.”
