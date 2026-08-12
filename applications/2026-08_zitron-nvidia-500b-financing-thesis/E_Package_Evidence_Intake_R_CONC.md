# Package-Satisfying Evidence Intake — R-CONC-NOTES

**Date:** 2026-08-12  
**Application:** `2026-08_zitron-nvidia-500b-financing-thesis`  
**Locked package:** CONC-BAR (L5) — OpenAI + Anthropic jointly ≥70% of **AI-attributed** revenue at **Microsoft, Google, and Amazon**  
**Target dependent(s):** CONC-BAR met? (not SUSTAIN-BAR; LOCK-011)

---

## 1. Lock schema

| Slot | Required by lock | Value in this artifact |
|------|------------------|------------------------|
| Names | MSFT **and** GOOG **and** AMZN | Microsoft filing + Bloomberg MSFT analysis only. Google/Amazon **no matched primary notes** |
| Metric | **AI-attributed** revenue (not total company; not all cloud unless source says so) | MSFT: OpenAI related-party **dollars** disclosed; AI **total** not in 10-K. GOOG: UBS as cited is **Google Cloud %**. AMZN: Barclays as cited is Amazon **AI %** — primary PDF not found |
| Threshold | OpenAI + Anthropic jointly **≥70%** | Bloomberg ~70% is **OpenAI alone / estimated MSFT AI total**. Not three-name; not Anthropic-inclusive filing |
| Matching | Primary notes / equivalent — not Zitron paraphrase | **Partial:** Microsoft 10-K (issuer). Bloomberg via reprint. WF / Barclays / UBS / DB **PDFs not in hand** |
| OR-slots | n/a — three-name **AND** | One name cannot clear the bar |

**Schema match?** **Partial** — Microsoft OpenAI **dollar** disclosure matches a related-party slot, not CONC-BAR. Share-of-AI and Google/Amazon legs unmatched as primary.

---

## 2. Artifact summary

**Source / citation:**
- Microsoft Form 10-K FY ended June 30, 2026 ([SEC](https://www.sec.gov/Archives/edgar/data/789019/000119312526323660/msft-20260630.htm)): related-party disclosure — “For fiscal year 2026, we recorded revenue from commercial arrangements with OpenAI, inclusive of revenue-sharing payments, of **$24.1 billion**, and accounts receivable from OpenAI as of June 30, 2026 was **$6.0 billion**.” FY26 company revenue **$331.839B**.
- Bloomberg analysis as reprinted (BLOOMBERG byline) e.g. [Business Times 2026-08-06](https://www.businesstimes.com.sg/companies-markets/openai-accounted-likely-70-microsofts-ai-sales-disclosures-show): OpenAI “more than half, and likely about **70%**” of Microsoft FY26 AI sales, assuming March 123% AI run-rate growth continued → ~**$34B** FY AI total vs $24.1B OpenAI. Microsoft **did not** update a FY AI-sales total at FQ4. March run-rate “>$37B” is a different metric.
- UBS Stephen Ju (secondary, TipRanks 2026-06-04): models Google Cloud split Core / Vertex / AI-lab deals (Anthropic, OpenAI, Meta) and raises Cloud revenue estimates. **Does not print** 48% of Cloud or 70% of Google **AI**.
- Wells Fargo Michael Turrin / Barclays Ross Sandler / Deutsche Bank Brad Zelnick: **no public primary PDFs** located this pull. Figures remain Zitron paraphrase (*Don't Look Up* / *The AI Demand Bubble*). Zitron’s own editor note: UBS Ju on AWS has OpenAI+Anthropic at **59%** of AWS AI vs Barclays Sandler **73%** of Amazon AI — notes disagree.

**What it reports:** Microsoft discloses OpenAI-related **revenue dollars**, not an AI-revenue **share**. Bloomberg estimates that share for Microsoft only. Google/Amazon concentration remains advocacy citation of sell-side notes.

**Sample / setup limits:** No Bloomberg/FactSet terminal extract of WF/Barclays/UBS/DB workbooks. $24.1B mixes Azure consumption, model-build costs, and revenue-share (10-K does not split). $24.1 / $331.8 ≈ 7.3% of **total** Microsoft revenue — **not** CONC-BAR’s metric.

### Conflicted-source flag
- [x] **Non-conflicted** (in part): Microsoft 10-K related-party disclosure (issuer audited filing; dollars, not AI%).
- [x] **Conflicted / interest-aligned** (in part)
  - [x] Underwriter / bookrunner / paid placement research — **sell-side notes** (unmatched PDFs)
  - [x] Other: Bloomberg **estimate of denominator**; advocacy newsletter paraphrase

**If conflicted:** Sell-side / Bloomberg estimates may support **scenario presence** of a Microsoft-concentration debate. Must **not** solely clear three-name CONC-BAR. 10-K dollars may establish the OpenAI related-party amount.

### Quantitative bar?
Yes — see `E_Quantitative_Evidence_Rubric_R_CONC.md`.

---

## 3. Provisional gate intent
- [x] Aim **ADMIT** as constraining the dependent — **Microsoft OpenAI dollars + Bloomberg MSFT-AI-share estimate only**
- [ ] Aim **HOLD** the residual as a whole (partial admit is cleaner)
- [ ] Aim **REJECT**

**ADMIT bar for this freeze:** Matched primary notes (or equivalent issuer disclosure) showing OpenAI+Anthropic ≥70% of **AI-attributed** revenue at **each** of MSFT, GOOG, AMZN.  
**HOLD:** One-name estimate; Cloud% without AI%; secondary paraphrase of notes.  
**REJECT:** Treating UBS 48% of **Google Cloud** as 70% of Google **AI**; treating $24.1B / $331.8B as CONC-BAR; treating Microsoft-only as three-name clearance; treating CONC-BAR as SUSTAIN-BAR (LOCK-011).

---

## 4. Scoped-result honesty
Hold **under:** Microsoft 10-K related-party dollars; Bloomberg reprint-grade MSFT AI-share estimate as of ~2026-08-06.  
**Must not be promoted to:** CONC-BAR met; Google/Amazon 70% AI; Cloud% = AI%; demand bubble; C-VENDOR; GPU $1.6T.

---

## 5. Next
- [x] Proceed to `04i`
