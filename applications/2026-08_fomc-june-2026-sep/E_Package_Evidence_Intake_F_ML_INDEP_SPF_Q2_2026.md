# Package-Satisfying Evidence Intake — R-FML-INDEP (SPF Q2 2026)

**Date:** 2026-08-12  
**Application:** `2026-08_fomc-june-2026-sep`  
**Locked package / scope label:** L1–L16; L2 F-ML-BAR (P-BaseCase); L4 matching defs  
**Target dependent:** R-FML-INDEP — does a **non-SEP** matched expected-path show that June 2026 medians **are** the economy’s P-BaseCase?  
**Named-class pulse?** **Yes**  
**Rubric:** [`E_Quantitative_Evidence_Rubric_F_ML_INDEP_SPF_Q2_2026.md`](E_Quantitative_Evidence_Rubric_F_ML_INDEP_SPF_Q2_2026.md)

---

## 0. Named-class pulse (complete when this intake is an auto-continue pulse)

Quote freeze; name the public class; confirm this is not the brochure that posed the bar and not a substituted question. **Stop** if the honest `04` result would be **established**. Continue if not-established or refute. Effort ≠ clearance. Print-match ≠ clearance.

| Check | Value |
|-------|--------|
| Freeze line (quoted) | L2: “For GDP growth, unemployment, PCE inflation, and core PCE, a June 17 SEP figure is a ‘most likely outcome’ claim only if it is the **expected / central path** for that variable and window — not a mere live possibility (P-NonNegligible), not unbounded logical possibility, and not merely that the PDF contains the words ‘most likely.’” Funds-rate off this bar. |
| Named source class (specific series + matching locks) | Philadelphia Fed **Survey of Professional Forecasters, Q2 2026** — published **median** point forecasts (33 forecasters; received on or before May 12, 2026; released May 15, 2026), compared to June 17 SEP 2026 medians under L4 defs (Q4/Q4 GDP and PCE; Q4-average unemployment; core PCE). |
| Named enough? (on residual card **or** standing-rule example; published central statistic; rival series ≠ unnamed) | **Yes** — standing-rule example + this card. Published statistic is **median**, not mean (honest fetch, not a class swap). Tealbook / nowcast are **different classes**, not a reason to treat SPF as unnamed. |
| Non-circular? (not same brochure / not problem substitution) | **Yes** — SPF is a survey of outside professional forecasters, not the June 17 SEP Table 1 / “most likely” brochure. Not Tealbook (Fed staff). Not a nowcast (different object). Not July 29. |
| Schema match | **Partial** — PCE/core Q4/Q4 match; GDP concept fails; U near-concept, print ≠. Score **every** locked slot; do **not** collapse the bar to inflation. |
| Conflicted-source flag completed (§2)? | **Yes** |
| **Establishment-stop drill:** Would honest `04` declare **established**? | **No** — pulse continues. (If Yes, would have stopped.) |

If **Named source class** is unnamed or is a vehicle fork (which series?): **stop** — `name source class …`. Do not invent a class to make the leftover tractable. Do not treat a named series as unnamed because a rival class exists.

**Not used (would be a class swap):** Tealbook / Fed staff forecast (conflicted); Atlanta Fed GDPNow or similar nowcast (not Q4/Q4 annual); Q3 2026 SPF (not released as of 2026-08-12).

---

## 1. Lock schema (must match freeze)
| Slot | Required by lock | Value in this artifact |
|------|------------------|------------------------|
| Object | forecast | Test whether June 2026 SEP medians **are** the expected/central path, using a non-SEP series |
| F-ML bar | P-BaseCase | Under test, not assumed met |
| Window | 2026 only | Same as L13; not 2027–28, not longer run |
| Variables | GDP, U, PCE, core PCE | Funds-rate **excluded** (L2). SPF T-bill path noted only as off-bar kinship, not scored. |
| Statistic | SEP side = median of 18 (L14); SPF side = published median of 33 | Two different panels; not the same 18 people |
| Matching conditions | L4: Q4/Q4 GDP and PCE; Q4-average unemployment; core PCE | **Partial** — see §2. SPF publishes Q4/Q4 for PCE/core PCE. SPF GDP 2.2 is **annual-average**, not Q4/Q4. SPF unemployment 2026Q4 level **4.5** vs SEP Q4-average **4.3**. Vintage: SPF ≤ May 12 vs SEP June 17. |

**Schema match?** **Partial** — named class is the right *kind* of object (independent professional central path). L4 match holds for PCE and core PCE Q4/Q4. GDP concept does not match. Unemployment level differs by 0.2 pp. Vintage is earlier than June 17. Partial match is not a silent OR-slot; it is recorded.

---

## 2. Artifact summary
**Source / citation:**  
- Release page: https://www.philadelphiafed.org/surveys-and-data/real-time-data-research/spf-q2-2026  
- PDF: https://www.philadelphiafed.org/-/media/FRBP/Assets/Surveys-And-Data/survey-of-professional-forecasters/2026/spfQ226.pdf  
- “The figures on each line are medians of 33 forecasters.” Forecasts received on or before May 12, 2026. Released May 15, 2026.

**What it reports (concise):**

| SPF Q2 2026 (published median) | Figure | L4 match to June SEP 2026 median? |
|--------------------------------|--------|-----------------------------------|
| Real GDP 2026 **annual-average** | **2.2** | **No** — SEP is **Q4/Q4 2.2**. Same print, different concept. SPF does not publish a Q4/Q4 GDP analogue in the inflation-style Q4/Q4 table. Quarterly SAAR: 2026Q2 2.1 / Q3 2.2 / Q4 **1.6**. |
| Unemployment 2026Q4 | **4.5** (annual-average 2026 **4.4**) | **Near-concept, different print** — SEP Q4-average **4.3**. Gap **+0.2** (Q4) / **+0.1** (annual avg). |
| Headline PCE Q4/Q4 2026 | **3.6** | **Yes — print match** vs SEP **3.6** |
| Core PCE Q4/Q4 2026 | **3.3** | **Yes — print match** vs SEP **3.3** |

**Sample / setup limits:** 33 outside forecasters; information set as of mid-May 2026 (before June 17 SEP and before whatever moved March SEP 2026 PCE 2.7 → June 3.6). Q3 2026 SPF not released as of this intake.

### Conflicted-source flag (mandatory)
- [x] **Non-conflicted** (independent research, audited filings, disinterested benchmarks, etc.)
- [ ] **Conflicted / interest-aligned** — check all that apply:
  - [ ] Underwriter / bookrunner / paid placement research
  - [ ] Issuer / company marketing or pitch
  - [ ] Vendor white paper
  - [ ] Advocacy / campaign material
  - [ ] Self-reported unaudited metrics as sole proof
  - [ ] Other: ________

**Note:** Publisher is a Reserve Bank; panelists are outside professionals, not FOMC participants and not the June 17 SEP brochure. Institutional Fed-System publisher ≠ Tealbook and ≠ Table 1 circularity. Usable as independent of the candidate brochure. Must **not** be treated as “the” unique expected path of the economy.

**If conflicted:** N/A for this artifact’s independence from SEP Table 1.

### Quantitative bar?
Yes — [`E_Quantitative_Evidence_Rubric_F_ML_INDEP_SPF_Q2_2026.md`](E_Quantitative_Evidence_Rubric_F_ML_INDEP_SPF_Q2_2026.md).

---

## 3. Provisional gate intent (before full `04`)
- [x] Aim **ADMIT** as constraining the dependent under this package — admit SPF Q2 2026 medians as a **non-SEP comparison series** and admit the **test result**: F-ML-BAR still **not established**
- [ ] Aim **HOLD** (borderline, incomplete match, or magnitude unclear)  
- [ ] Aim **REJECT** (fails relevance, Cons, or Amb-net)

**ADMIT bar for this freeze:** SPF is the named class; freeze quoted; non-circular; numbers taken from the public release; result is not-established or refute.  
**HOLD bar:** Would apply if the class were still a vehicle fork (SPF vs Tealbook vs nowcast). It is not.  
**REJECT triggers:** Using SPF to declare F-ML **met** because PCE/core print-match; swapping in Tealbook/nowcast; treating annual-average GDP 2.2 as Q4/Q4; importing July 29.

---

## 4. Scoped-result honesty
Findings, if admitted, hold **under:** L2 F-ML-BAR + L4 defs + SPF Q2 2026 median vintage (≤ May 12, 2026) vs June 17 SEP 2026 medians.  
**Partial / claim-adjacent?** **Yes** — PCE/core Q4/Q4 print-match is kinship, not identification of the SEP median as *the* expected path. GDP fails matching conditions. Unemployment disagrees. Policy-mix (L11) still applies on the SEP side. One survey median ≠ unique central path.  
**Must not be promoted to:** F-ML-BAR **met**; “the economy’s” unique expected path; Committee forecast; 2026-on-target; funds-rate on this bar; a refute of 2026 medians as live possibilities.

---

## 5. Next
- [x] Proceed to formal `04` ([`04q_Material_Admission_F_ML_INDEP_SPF_Q2_2026.md`](04q_Material_Admission_F_ML_INDEP_SPF_Q2_2026.md))  
- [ ] Stop — evidence insufficient even for HOLD  

---

*Standing-rule package-satisfying evidence intake. Named-class pulse. Domain-general.*
