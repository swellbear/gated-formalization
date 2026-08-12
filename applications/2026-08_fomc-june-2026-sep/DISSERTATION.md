# Dissertation — Application Findings

**Date:** 2026-08-12  
**Application:** `2026-08_fomc-june-2026-sep`  
**Claim family / parent (if any):** — (standalone; no successor selected)  
**Closeout verdict:** Stable Provisional (split) — **hard stop sealed**  
**Amb at closeout:** ≈ **1** (Gap 8 realization still open; G8 not locked)

**Tags:** `markets` · `descriptive-census`, `forecast-extension` · `forced-deviation`

**Related applications (max 4):** Zitron Nvidia $500B (claimed-table vs elevation; Amb≠clearance); CoreWeave GPU-life (real-claim forecast locks); sell-in-May (markets elevation) — **no conclusion inheritance**

---

## 1. Plain-language summary

The June 17, 2026 Federal Reserve *Summary of Economic Projections* is a published set of what **18 FOMC participants** (17 for 2028) submitted as their **most likely** paths for growth, unemployment, and inflation, each under that person’s own idea of **appropriate** policy.

**What held up:** The document exists, the submitter counts are as printed, and the tables can be read under the document’s own definitions. The June **submitted** medians are GDP **2.2**, unemployment **4.3**, PCE **3.6**, core PCE **3.3**, funds-rate **3.8** for 2026, with 2027–28 and longer-run cells as printed. From March to June, 2026 PCE was revised **+0.9**, funds **+0.4**, GDP **−0.2**. Seventeen of eighteen said PCE uncertainty was higher than average and risks were to the upside. Historical 70% error fans are in the document **with** caveats that they may not match current judgments, use CPI not PCE for the inflation RMSE, and are not the same object as those tallies.

**What did not hold up as proven:** That those medians **are** the economy’s expected / central path — including after comparing them to the May 2026 Survey of Professional Forecasters (PCE/core printed the same Q4/Q4 numbers; GDP concepts differed; unemployment was 4.5 vs 4.3). That the median **is** the Committee’s forecast. That “appropriate policy” **is** a vote or the realized funds path. That longer-run PCE **2.0** means 2026 is on target. That the RMSE fans **are** current FOMC uncertainty. The July 29, 2026 FOMC statement was kept **out** of this package.

**Bottom line:** This is a solid census of an official brochure. It is not a cleared 2026 call. Low leftover ambiguity does not mean the path is established. This is not investment or policy advice.

---

## 2. Original claim and context

**Original claim (verbatim):**  
The June 17, 2026 SEP is a published package of FOMC participants’ projections of **most likely** GDP, unemployment, inflation, and **appropriate** federal-funds paths for 2026–2028 and the longer run. The document’s claims are the inventory in [`CLAIM_INVENTORY.md`](CLAIM_INVENTORY.md): process/definitions, printed actuals, June Table 1 medians/CT/ranges, March-to-June revisions, the dot plot and histograms, uncertainty/risk judgments, RMSE-based 70% fans, and the prose elevations (most likely; appropriate policy; longer-run convergence under no further shocks).

**Source / domain context:**  
- Primary: [fomcprojtabl20260617.pdf](https://www.federalreserve.gov/monetarypolicy/files/fomcprojtabl20260617.pdf)  
- Accessible twin: [fomcprojtabl20260617.htm](https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260617.htm)  
- Release: 2:00 p.m. EDT, June 17, 2026; meeting June 16–17, 2026  
- **OUT:** July 29, 2026 FOMC statement; news/blog gloss; named-official non-submission stories not in this PDF

**Claim type:** **Mixed** — `descriptive-census` of a published SEP + `forecast-extension` (“most likely outcomes”) + soft evaluative (“appropriate monetary policy”).

**Parent or successor relationship (if any):** None. Claim-Revision (`run CR` / [R-REV](RESIDUAL_BRANCH_MENU.md#r-rev)) **offered, not run**. Default at closeout: **keep original wording**.

---

## 3. How it was examined

**Method path:** Cycle 0 operator-confirmed (Amb ≈ 11) → object lock **forecast** (L1) → F-ML bar freeze **P-BaseCase** (L2, bar not met) → remaining census vehicle (L3–L10) → C-APPROP and F-LR meaning freezes (L11–L12) → authorized 2026 F-ML-BAR test (L13, not established) → structural G4/G5/G7 locks (L14–L16) → residual and optional-mode menus offered → operator `closeout` → **named-class pulse** R-FML-INDEP (L17 SPF Q2 2026, not established). No Phase 2. No Experimental Generation. July 29 never entered the package.

**Governing lock / freeze (if any):** Imported LOCK-003, 009–011 (re-validated; [`IMPORTED_PATTERN_STAMP.md`](IMPORTED_PATTERN_STAMP.md)). App freezes: OBJECT-FORECAST; F-ML-BAR = P-BaseCase (funds-rate off bar); C-APPROP = individual mandate; F-LR = convergence + no further shocks; G4 median-of-18; G5 year-slots; G7 tallies ≠ RMSE.

**Phase 2 classification:** **Not entered.** Named-class pulse ran **without** Phase 2. Per leftover: R-FML-INDEP was empirically resolvable and named (SPF) — pulse, not theory generation. Remaining: R-REALIZE later empirical; R-G8 definition freeze (operator); R-FML-2027-28 park-90d; R-REV CR (operator). Mixed case: census done; unmet bars need evidence, not Experimental Generation.

**Key artifacts:** `01`–`03`, `02`–`02j`, `04a`–`04p`, [`CLAIM_INVENTORY.md`](CLAIM_INVENTORY.md), [`admitted_layers.md`](admitted_layers.md), [`E_Quantitative_Evidence_Rubric_F_ML_2026.md`](E_Quantitative_Evidence_Rubric_F_ML_2026.md), [`RESIDUAL_BRANCH_MENU.md`](RESIDUAL_BRANCH_MENU.md), [`OPTIONAL_MODES_MENU.md`](OPTIONAL_MODES_MENU.md), [`SHARE_PACK.md`](SHARE_PACK.md), [`STATUS.md`](STATUS.md).

---

## 4. What was established

| Finding | Scope |
|---------|--------|
| **L1 OBJECT-FORECAST** — object is a forecast of most-likely outcomes; census is the vehicle; commitment is not the object | Under package |
| **L2 F-ML-BAR meaning** — P-BaseCase for GDP / U / PCE / core PCE; funds-rate dots off this bar | Evaluation freeze only |
| **L3 D-DOC** — June 17 2026 SEP; 18 submitters (17 for 2028); March vintage 19 | Document identity / process prose |
| **L4 D-DEF** — Q4/Q4; median/CT/range; funds midpoint; core-PCE-no-LR; RMSE/CPI footnotes | Reading conventions |
| **L5 D-SEP** — Table 1 medians/CT/range as *submitted* | Census; not F-ML met; not Committee forecast |
| **L6 D-ACTUAL** — 2021–2025 printed actuals | Exhibit census; not 2026–28 realization |
| **L7 D-REV** — March→June printed medians (2026 PCE +0.9, funds +0.4, GDP −0.2) | Derived census; not causal |
| **L8 D-DOTS / D-HIST** — Figure 2–3 distributions; dots = appropriate-path midpoints | Distributional census |
| **L9 D-UNCERT** — 17/18 PCE uncertainty higher and risks upside | Judgment tallies; ≠ RMSE |
| **L10 D-RMSE** — Table 2 / 70% fans with document caveats; CPI not PCE | Historical convention |
| **L11 C-APPROP meaning** — individual mandate reading | Meaning freeze; vote not met |
| **L12 F-LR meaning** — convergence under appropriate policy and no further shocks | Meaning freeze; dated/2026-on-target not met |
| **L13 test executed** — 2026 medians scored against F-ML-BAR | Evaluation record; result is not-established |
| **L14 G4** — load-bearing census statistic = median of 18 (17 for 2028) | Census; not Committee forecast |
| **L15 G5** — 2026 / 2027 / 2028 / longer run are separate slots | Structural; LR 2.0 ≠ 2026 on-target |
| **L16 G7** — D-UNCERT ≠ D-RMSE; 17/18 ≠ 70% interval; CPI ≠ PCE | Structural |
| **L17 SPF Q2 2026 comparison executed** — non-SEP professional medians on the record | Evaluation; bar still not established; not a refute |

---

## 5. What was not established

| Item | Status |
|------|--------|
| **F-ML-BAR met** — 2026 GDP 2.2 / U 4.3 / PCE 3.6 / core 3.3 **are** the expected / central path | **Not established** — L13 brochure test + L17 SPF Q2 2026; **not a refute**. SPF PCE/core Q4/Q4 print-match ≠ clearance. |
| F-ML-BAR on 2027 and 2028 medians | **Untested** — [R-FML-2027-28](RESIDUAL_BRANCH_MENU.md#r-fml-2027-28) park-90d |
| Median = Committee forecast | **Blocked** (L14) |
| C-APPROP as vote or realized funds path | **Not met** (L11); July 29 OUT |
| F-LR as dated unconditional forecast or 2026-on-target | **Not met** (L12 + L15) |
| RMSE fans = current FOMC uncertainty; 17/18 = 70% interval; CPI RMSE = PCE | **Blocked** (L16) |
| 2026–28 realization matching L5 medians | **Open / later** — Gap 8; [R-REALIZE](RESIDUAL_BRANCH_MENU.md#r-realize) |
| July 29 statement content | **OUT of package** — [R-JULY29](RESIDUAL_BRANCH_MENU.md#r-july29) drop |
| Policy advice (“should the FOMC have been more hawkish”) | Not claimed / not branchable |

---

## 6. Forced deviations and scope limits

**Forced-deviation terms (if any):**  
- SEP cell or the words “most likely” → P-BaseCase **met** (LOCK-010; L2 + L13 + L17).  
- SPF PCE/core Q4/Q4 print-match → F-ML **met**; SPF annual-average GDP 2.2 → SEP Q4/Q4.  
- F-ML-BAR **freeze** → bar **met**.  
- Median of 18 → Committee forecast.  
- Appropriate-policy dots → vote or realized funds path.  
- Longer-run PCE 2.0 → 2026 on-target.  
- RMSE 70% fans → current FOMC uncertainty; 17/18 → 70% interval; CPI RMSE → PCE.  
- Amb drop after locks → clearance.  
- July 29 appearing on a residual menu → in-package.

**Scoped vs unrestricted:** Established pieces are **scoped** to a census of the June 17 document plus meaning freezes. Unrestricted slogan (“these medians **are** the expected path / the Committee forecast / on target”) was **not** reached.

**What the lock/package could not settle relative to the original wording:** Whether the submitted medians **are** the economy’s central path; whether “appropriate” paths were a Committee decision; whether 2026 is on the way to 2%; whether 2026–28 actuals will match. Those terms could not be tested as unrestricted clearance from the SEP’s own tables — a property of the claim text vs the brochure, not a temporary lack of Table 1 cells.

---

## 7. Quantitative results (if any)

**Census of submitted June 2026 medians (L5; not F-ML met):**

| Variable | 2026 | 2027 | 2028 | Longer run |
|----------|------|------|------|------------|
| Real GDP (Q4/Q4) | 2.2 | 2.3 | 2.2 | 2.0 |
| Unemployment (Q4 avg) | 4.3 | 4.3 | 4.2 | 4.2 |
| PCE inflation | 3.6 | 2.3 | 2.0 | 2.0 |
| Core PCE | 3.3 | 2.5 | 2.1 | *(not collected)* |
| Fed funds (appropriate-path midpoint) | 3.8 | 3.6 | 3.4 | 3.1 |

**March→June 2026 median revisions (L7; not causal):** PCE **+0.9**; core PCE **+0.6**; funds **+0.4**; GDP **−0.2**.

**L13 F-ML-BAR test (2026 only; funds-rate off bar):**

| Variable | 2026 median | F-ML-BAR (P-BaseCase) |
|----------|-------------|------------------------|
| Real GDP | 2.2 | **Not established** |
| Unemployment | 4.3 | **Not established** (tightest cluster; still brochure + policy-mix) |
| PCE | 3.6 | **Not established** (weakest: +0.9 vintage jump; 17/18 upside) |
| Core PCE | 3.3 | **Not established** |
| Funds rate | 3.8 | **Not under this bar** |

**Why “met” fails:** (1) Brochure circularity — the SEP posing figures as most-likely submissions is exactly what L2 said does not clear P-BaseCase. (2) Policy-mix — medians mix 18 different appropriate-policy conditionings (L11). (3) PCE/core extra — 17/18 upside risk vs “expected” if expected means mean; vintage jump.

**L17 named-class pulse (SPF Q2 2026; funds-rate off bar):** Philadelphia Fed Survey of Professional Forecasters, released May 15, 2026; published **medians** of 33; received on or before May 12, 2026.

| Variable | June SEP 2026 | SPF Q2 2026 | F-ML-BAR |
|----------|---------------|-------------|----------|
| Real GDP | Q4/Q4 **2.2** | Annual-average **2.2**; Q4 SAAR **1.6** | **Not established** (concept mismatch) |
| Unemployment | Q4-avg **4.3** | 2026Q4 **4.5** | **Not established** |
| PCE | Q4/Q4 **3.6** | Q4/Q4 **3.6** | **Not established** (print-match ≠ identification) |
| Core PCE | Q4/Q4 **3.3** | Q4/Q4 **3.3** | **Not established** (print-match ≠ identification) |

**Not a refute:** no demonstration that 2026 medians are *not* a live central path. Independent series now **is** admitted (SPF); it still does not establish P-BaseCase.

**RMSE 70% fans (L10; historical convention, not current uncertainty):** 2026 PCE printed fan 2.6 to 4.6 around median 3.6; GDP 0.5 to 3.9 around 2.2. Table 2 inflation RMSE is **CPI**, not PCE.

Implications ≠ proofs. Census numbers are not bar clearance.

---

## 8. Revisions, implications, and alternatives

Optional modes — [`OPTIONAL_MODES_MENU.md`](OPTIONAL_MODES_MENU.md):

- **UX** — **offered, not run**.  
- **CX** — **offered, not run**.  
- **CR / R-REV** — **offered, not run**. Closeout default: **keep original wording**. Rewording would not meet F-ML-BAR.  
- **QI** — **N/A** (unmet P-BaseCase is a modal bar, not a failed C≥H / Sharpe instance).

Original wording remains on record. No successor application started. No exhibits invented.

---

## 9. Final status of the original claim

**Verdict:** **Stable Provisional (split)** — hard stop sealed.

**Amb ≠ clearance:** Closeout Amb ≈ **1** because Gap 8 (realization in-scope-now) was left open and G8 was **not** locked. That leftover slot, plus unmet bars, is not a finding that 2026 PCE 3.6 is the expected outcome. Low Amb after census and meaning freezes does **not** clear F-ML-BAR, vote, or 2026-on-target.

**Locked-bar status summary:** F-ML-BAR **frozen, not met** (2026 tested L13 + L17). C-APPROP as vote **not met**. F-LR as dated/2026-on-target **not met**. Census vehicle **established**. SPF comparison **on the record**.

**Continuation / hard-stop note:** Examination of this package is done. Original wording kept by default. Reopen only via an authorized residual or optional mode. Do not import July 29 to “finish.”

---

## 10. What would still be needed

Concrete reopen paths — [`RESIDUAL_BRANCH_MENU.md`](RESIDUAL_BRANCH_MENU.md):

- [R-FML-2026](RESIDUAL_BRANCH_MENU.md#r-fml-2026) — **executed**; not established.  
- [R-FML-INDEP](RESIDUAL_BRANCH_MENU.md#r-fml-indep) — **executed L17** (SPF Q2 2026); not established; later SPF vintage not auto-run.  
- [R-G8-SCOPE](RESIDUAL_BRANCH_MENU.md#r-g8-scope) — freeze realization as out of scope *now* (Amb 1→0; ≠ clearance). **Not locked** at this closeout.  
- [R-REALIZE](RESIDUAL_BRANCH_MENU.md#r-realize) — park-until-trigger: 2026 Q4 actuals under L4 definitions vs L5 medians. Hit ≠ F-ML met.  
- [R-FML-2027-28](RESIDUAL_BRANCH_MENU.md#r-fml-2027-28) — park-90d; diminishing returns after L13/L17; G5 forbids copy.  
- [R-REV](RESIDUAL_BRANCH_MENU.md#r-rev) — park-90d / `run CR`; rewording ≠ bar clearance.  
- [R-JULY29](RESIDUAL_BRANCH_MENU.md#r-july29) — **drop** unless explicit L₀ elevation.

---

## 11. Technical appendix

### Amb path

| Stage | Amb | Note |
|-------|-----|------|
| Cycle 0 (operator-confirmed) | ≈ 11 | Object unset |
| After L1 OBJECT-FORECAST | ≈ 9 | Forecast object; not census-only; not commitment |
| After L2 F-ML P-BaseCase | ≈ 7 | Bar frozen, not met |
| After L3 D-DOC | ≈ 7 | Process/identity; no fake Amb drop |
| After L4 D-DEF | ≈ 7 | Definitional census; no fake Amb drop |
| After L5–L10 remaining D-* | ≈ 7 | Submitted/printed census; no fake Amb drop |
| After L11 C-APPROP | ≈ 5 | Individual-mandate freeze; vote not met |
| After L12 F-LR | ≈ 4 | Convergence + no further shocks; dated/2026-on-target not met |
| After L13 F-ML-BAR 2026 test | ≈ 4 | 2026 medians not established; no fake Amb drop |
| After L14 G4 median-load-bearing | ≈ 3 | Median of 18 (17 for 2028) |
| After L15 G5 year-slots | ≈ 2 | Years separate; LR 2% ≠ 2026 on-target |
| After L16 G7 tallies ≠ RMSE | ≈ 1 | D-UNCERT ≠ D-RMSE; Gap 8 open |
| Closeout (hard stop) | ≈ **1** | G8 not locked; menus offered not run |
| After L17 SPF Q2 2026 pulse | ≈ **1** | R-FML-INDEP executed; print-match ≠ clearance; no fake Amb drop |

### Admitted layers (index)

| ID | One-line | Pointer |
|----|----------|---------|
| L1 | OBJECT-FORECAST | [04a](04a_Material_Admission_OBJECT_FORECAST.md) |
| L2 | F-ML-BAR P-BaseCase (not met) | [04b](04b_Material_Admission_F_ML_P_BaseCase.md) |
| L3 | D-DOC | [04c](04c_Material_Admission_D_DOC.md) |
| L4 | D-DEF | [04d](04d_Material_Admission_D_DEF.md) |
| L5 | D-SEP submitted | [04e](04e_Material_Admission_D_SEP.md) |
| L6 | D-ACTUAL 2021–25 | [04f](04f_Material_Admission_D_ACTUAL.md) |
| L7 | D-REV March→June | [04g](04g_Material_Admission_D_REV.md) |
| L8 | D-DOTS / D-HIST | [04h](04h_Material_Admission_D_DOTS_HIST.md) |
| L9 | D-UNCERT | [04i](04i_Material_Admission_D_UNCERT.md) |
| L10 | D-RMSE | [04j](04j_Material_Admission_D_RMSE.md) |
| L11 | C-APPROP individual-mandate | [04k](04k_Material_Admission_C_APPROP.md) |
| L12 | F-LR meaning | [04l](04l_Material_Admission_F_LR.md) |
| L13 | F-ML-BAR 2026 test (not established) | [04m](04m_Material_Admission_F_ML_BAR_2026_Test.md) |
| L14 | G4 median-load-bearing | [04n](04n_Material_Admission_G4_Median_Load_Bearing.md) |
| L15 | G5 year-slots | [04o](04o_Material_Admission_G5_Year_Slots.md) |
| L16 | G7 tallies ≠ RMSE | [04p](04p_Material_Admission_G7_Tallies_Neq_RMSE.md) |
| L17 | F-ML-INDEP SPF Q2 2026 (not established) | [04q](04q_Material_Admission_F_ML_INDEP_SPF_Q2_2026.md) |

### Key artifacts

- [`STATUS.md`](STATUS.md) · [`SHARE_PACK.md`](SHARE_PACK.md) · [`EXECUTIVE_BRIEF.md`](EXECUTIVE_BRIEF.md) · [`final_verdict.md`](final_verdict.md)  
- [`05_Original_Claim_Assessment_Closeout.md`](05_Original_Claim_Assessment_Closeout.md)  
- [`CLAIM_INVENTORY.md`](CLAIM_INVENTORY.md) · [`admitted_layers.md`](admitted_layers.md)  
- Rubric: [`E_Quantitative_Evidence_Rubric_F_ML_2026.md`](E_Quantitative_Evidence_Rubric_F_ML_2026.md) · [`E_Quantitative_Evidence_Rubric_F_ML_INDEP_SPF_Q2_2026.md`](E_Quantitative_Evidence_Rubric_F_ML_INDEP_SPF_Q2_2026.md)  
- Menus: [`RESIDUAL_BRANCH_MENU.md`](RESIDUAL_BRANCH_MENU.md) · [`OPTIONAL_MODES_MENU.md`](OPTIONAL_MODES_MENU.md)

### Failure-mode / tracker pointers (if any)

- FD: pose/freeze/median → clearance; SPF print-match → met; annual-avg GDP → Q4/Q4; RMSE → current uncertainty; July 29 smuggle.  
- Portfolio / residual queue / claim-graph / pattern map / calibration updated this pulse.

---

*Generated under standing rule: Application Dissertation Deliverable. Stubs ≠ hard stop.*
