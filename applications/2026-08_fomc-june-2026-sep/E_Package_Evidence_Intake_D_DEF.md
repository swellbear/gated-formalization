# Package-Satisfying Evidence Intake — D-DEF (SEP measurement / table-reading definitions)

**Date:** 2026-08-12  
**Application:** `2026-08_fomc-june-2026-sep`  
**Locked package / scope label:** L1 OBJECT-FORECAST + L2 F-ML P-BaseCase (bar not met) + L3 D-DOC  
**Target dependent(s):** D-DEF (definitional census of how the SEP says to read its tables)

---

## 1. Lock schema (must match freeze)
| Slot | Required by lock | Value in this artifact |
|------|------------------|------------------------|
| Object | forecast | Census of *how the SEP defines its table conventions*, not F-ML met |
| F-ML bar | P-BaseCase | Not tested by this artifact |
| ODD / domain | June 17 2026 SEP | Same PDF/HTML |
| Metrics | definitional conventions | Q4/Q4; median / CT / range; funds-rate midpoint; core-PCE-no-LR; RMSE/CPI footnotes |
| Matching conditions | live primary | Official .gov release |
| OR-slots | n/a | |

**Schema match?** Yes — measurement definitions under the forecast object, without claiming P-BaseCase clearance or admitting Table 1 cells as outcomes.

---

## 2. Artifact summary
**Source / citation:**  
[fomcprojtabl20260617.pdf](https://www.federalreserve.gov/monetarypolicy/files/fomcprojtabl20260617.pdf) · [accessible HTML](https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260617.htm) (Last Update: June 17, 2026) · inventory B in [`CLAIM_INVENTORY.md`](CLAIM_INVENTORY.md)

**What it reports (concise):**  
The June 17, 2026 SEP states how to read its tables: GDP and both inflation measures are Q4/Q4 percent changes; unemployment is the Q4 average civilian rate; the funds-rate figure is the year-end (or longer-run) midpoint of the projected appropriate target range or the projected appropriate target level; median / central tendency / range are defined as census statistics of submissions; longer-run core PCE is not collected; Table 2 consumer-price RMSE uses CPI, not PCE; historical error ranges are ±RMSE of summer projections for 2006–2025 and, under stated assumptions, about a 70 percent probability band; the funds-rate fan is not strictly consistent with SEP funds-rate projections because those are appropriate-policy assessments, not likeliest-rate forecasts.

This is a **census of definitions**. It is not an admission that any printed median is the P-BaseCase outcome.

**Sample / setup limits:** Official publication’s own footnotes and notes. Not an independent audit of 2026–28 outcomes. Not a freeze of which statistic is load-bearing (Gap 4 remains open).

### Conflicted-source flag (mandatory)
- [x] **Non-conflicted** for *table-reading definitions* (official primary of the claim package)
- [ ] **Conflicted / interest-aligned** for *F-ML-BAR met* if used as sole proof that medians are the economy’s base case — **not so used here**

**If used to clear F-ML-BAR:** would be the forecast’s own brochure. This intake is **not** that use.

### Quantitative bar?
No — definitional census only. No `E_Quantitative_Evidence_Rubric` for D-DEF. Table 2 RMSE numbers are quoted as *the document’s error-convention definitions*, not as current FOMC uncertainty and not as 2026–28 outcome bands.

---

## 3. Quoted definitional language (live HTML, June 17 2026)

Pointers: Table 1 general note and footnotes 1–4; Figure 1 note; Figure 2 note; Figure 4.A–4.C notes; Figure 5 note; Table 2 note and footnotes 1–3; “Forecast Uncertainty” box. Same release as the PDF.

### B1 — Q4/Q4 for GDP and inflation
> Projections of change in real gross domestic product (GDP) and projections for both measures of inflation are percent changes from the fourth quarter of the previous year to the fourth quarter of the year indicated.

### B2 — PCE vs core PCE
> PCE inflation and core PCE inflation are the percentage rates of change in, respectively, the price index for personal consumption expenditures (PCE) and the price index for PCE excluding food and energy.

### B3 — Unemployment as Q4 average
> Projections for the unemployment rate are for the average civilian unemployment rate in the fourth quarter of the year indicated.

### B4 — Funds-rate midpoint / year-end (or longer run)
> The projections for the federal funds rate are the value of the midpoint of the projected appropriate target range for the federal funds rate or the projected appropriate target level for the federal funds rate at the end of the specified calendar year or over the longer run.

Figure 2 note (rounding convention, not a cell-as-outcome admit):
> Each shaded circle indicates the value (rounded to the nearest 1/8 percentage point) of an individual participant's judgment of the midpoint of the appropriate target range for the federal funds rate or the appropriate target level for the federal funds rate at the end of the specified calendar year or over the longer run.

### B5 — Median
> For each period, the median is the middle projection when the projections are arranged from lowest to highest. When the number of projections is even, the median is the average of the two middle projections.

### B6 — Central tendency
> The central tendency excludes the three highest and three lowest projections for each variable in each year.

### B7 — Range
> The range for a variable in a given year includes all participants' projections, from lowest to highest, for that variable in that year.

### B8 — Core PCE has no longer-run projection
> Longer-run projections for core PCE inflation are not collected.

Figure 1 core-PCE panel has no Longer-run column; Table 1 core PCE longer-run cells are blank. That is the same convention, not a finding about 2028 core PCE.

### B9 — Figure 1 actuals are annual
> The data for the actual values of the variables are annual.

### B11–B14 — Table 2 RMSE / CPI / 70 percent convention
Table 2 note:
> Error ranges shown are measured as plus or minus the root mean squared error of projections for 2006 through 2025 that were released in the summer by various private and government forecasters. As described in the box "Forecast Uncertainty," under certain assumptions, there is about a 70 percent probability that actual outcomes for real GDP, unemployment, consumer prices, and the federal funds rate will be in ranges implied by the average size of projection errors made in the past.

Table 2 footnote 2 (CPI, not PCE):
> Measure is the overall consumer price index, the price measure that has been most widely used in government and private economic forecasts. Projections are percent changes on a fourth quarter to fourth quarter basis.

Table 2 footnote 3 (short-rate errors):
> For Federal Reserve staff forecasts, measure is the federal funds rate. For other forecasts, measure is the rate on 3-month Treasury bills. Projection errors are calculated using average levels, in percent, in the fourth quarter.

Figure 4.A–4.C shared caveat (historical RMSE ≠ current FOMC uncertainty):
> Because current conditions may differ from those that prevailed, on average, over the previous 20 years, the width and shape of the confidence interval estimated on the basis of the historical forecast errors may not reflect FOMC participants' current assessments of the uncertainty and risks around their projections; these current assessments are summarized in the lower panels.

### B15 — Funds-rate fan not strictly consistent with SEP dots
Figure 5 note:
> The confidence interval is not strictly consistent with the projections for the federal funds rate, primarily because these projections are not forecasts of the likeliest outcomes for the federal funds rate, but rather projections of participants' individual assessments of appropriate monetary policy.

Forecast Uncertainty box (same split; end-of-year basis):
> It should be noted, however, that these confidence intervals are not strictly consistent with the projections for the federal funds rate, as these projections are not forecasts of the most likely quarterly outcomes but rather are projections of participants' individual assessments of appropriate monetary policy and are on an end-of-year basis.

Figure 5 also states the zero-truncation convention is a charting convention, not a negative-rate decision.

### B16 — Cross-participant dispersion vs 20-year RMSE
Forecast Uncertainty box:
> A comparison of figure 1 with figures 4.A through 4.C shows that the dispersion of the projections across participants is much smaller than the average forecast errors over the past 20 years.

---

## 4. Provisional gate intent (before full `04`)
- [x] Aim **ADMIT** as constraining D-DEF  
- [ ] Aim **HOLD**  
- [ ] Aim **REJECT**

**ADMIT bar for this freeze:** Official SEP states the measurement/table-reading conventions in inventory B.  
**HOLD bar:** n/a  
**REJECT triggers:** Using this to clear F-ML-BAR; treating definitions as Table 1 cell-as-outcome admits; treating RMSE fans as current FOMC uncertainty; treating CPI RMSE as PCE RMSE; importing July 29.

---

## 5. Scoped-result honesty
Findings, if admitted, hold **under:** this PDF/HTML as of the June 17, 2026 release, as *how the document says to read its tables*.  
**Partial / claim-adjacent?** No for D-DEF; yes if smuggled into F-ML, C-APPROP, F-LR, or D-SEP cell-as-outcome.  
**Must not be promoted to:** F-ML-BAR met; C-APPROP met; F-LR met; D-SEP Table 1 cells as forecast facts; Committee forecast; 2026–28 realization; RMSE fan as current uncertainty; CPI RMSE as PCE; July 29 “will deliver.”

---

## 6. Next
- [x] Proceed to formal `04d`  
- [ ] Stop
