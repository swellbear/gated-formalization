# Dissertation — Application Findings

**Date:** 2026-08-13  
**Application:** `2026-08_india-heat-mortality-mitigation-show`  
**Claim family / parent:** none  
**Closeout verdict:** Stable Provisional (split)  
**Amb at closeout:** ≈ 2.5  

**Tags:** Domain `other` (climate–health) · Claim-shape `descriptive-census`, `forecast-extension` · Pattern `forced-deviation`

**Related applications (max 4, process only):** `2026-08_heatwave-next-summer-should-prepare` (forward heat + elevation); `2026-08_fomc-june-2026-sep` (printed path ≠ finding met); `2026-08_sell-in-may-sp500-2026` (core vs elevation). **Not inherited.**

---

## 1. Plain-language summary

A public climate-health preprint reports a model in which India’s heat-related deaths, trained on national counts, rise faster under a high-emission temperature path than under an intermediate path, and look more spread-out across states in that high path. The **abstract** says those findings **demonstrate** that **climate mitigation can substantially reduce** both the **size** and the **unevenness** of future **urban** heat-health burdens.

This run treated that last sentence as the claim. What the page **prints about its own setup** can be listed. That the setup **shows mitigation works on urban heat-health** is **not established**. The authors’ own methods use two climate **scenarios**, not a real mitigation law, and **national** deaths plus city **temperatures**, not city death counts. Their discussion already uses a softer “could.” Completing the paper did not finish the slogan.

---

## 2. Original claim and context

**Original claim (verbatim):** These findings demonstrate that climate mitigation can substantially reduce both the magnitude and inequality of future urban heat-health burdens.

**Source / domain context:** Munshi, Kailasam, Shukla, Bakar, Chakraborti, arXiv:2603.24244 (HTML 2026-08-13). Intended *Urban Climate*. Not the Genesis software-agent preprint.

**Claim type:** Mixed (D-DOC / E-DEM)

**Parent or successor:** none

---

## 3. How it was examined

**Method path:** Lean Default Path. Anchors and mixed split; import LOCK-003/007 (+ analog of 011); Cycle 0 Amb ≈ 10; Rank 1 `O1+D1+M1+L1`; admit D-DOC as document census; E-DEM tested against methods + §4 limitations + §5 “could.” No Phase 2. No independent climate rerun.

**Governing lock:** `Lock_Rank1_DocDemonstrate.md`

**Key artifacts:** `01`–`05`, `E_Package_Evidence_Intake.md`, this file, share pack, residual + optional menus.

---

## 4. What was established

| Finding | Scope |
|---------|--------|
| The document describes 67 ~1° locations, six CMIP6 models, SMT March–September, ARIMAX, national 1970–2023 heat-death compilation, two SSPs | Under O1; live for **print**, stand-in for the world |
| It **reports** a steeper national path and more state spread under SSP5-8.5 than SSP2-4.5 in that model | Census of figures/text, not independent verification |
| Authors: relative scenario divergence robust; absolute levels uncertain; humidity/UHI/city deaths/linear form listed as limits | Census of §3–4 |

---

## 5. What was not established

| Item | Status |
|------|--------|
| E-DEM: mitigation **demonstrated** to substantially reduce magnitude **and** inequality of **urban** heat-health burdens | **not established** |
| SSP contrast = evaluation of real mitigation or Heat Action Plans | **not established** |
| City-level mortality projections | **not established** (authors: national deaths + city climate) |
| Independent confirmation of ARIMAX/CMIP6 numbers | **untested** (OUT unless residual) |
| Heat is not a health risk | **not claimed**; not a refute |

---

## 6. Forced deviations and scope limits

**Forced-deviation terms:** “Urban burdens” as city deaths; “mitigation” as enacted policy.

**Scoped vs unrestricted:** D-DOC is scoped to this page. It is not unrestricted support for the abstract.

**What the freeze could not settle:** Whether a different model with humidity, UHI, and district deaths would still show the same relative SSP gap — and whether that gap **is** “mitigation demonstrated.”

---

## 7. Quantitative results (if any)

None generated here. The paper’s own printed paths and `r≈0.95` (SMT vs heatwave days, as reported) are **their** numbers. Implications ≠ proofs. No QI (no failed C≥H instance bar of our own).

---

## 8. Revisions, implications, and alternatives

UX **run** (2026-08-13 picker) — uses of the split only; see [`UX_Use_Exploration.md`](UX_Use_Exploration.md). CX / CR **declined.** QI **N/A.** Original wording kept. Verdict unchanged.

---

## 9. Final status of the original claim

**Verdict:** Stable Provisional (split)

**Amb ≠ clearance:** Amb ≈ 2.5 after Rank 1.

**Locked-bar status:** D1 **not established**.

**Continuation / hard-stop note:** Hard stop. Optional modes and residuals offered only.

---

## 10. What would still be needed

See [`RESIDUAL_BRANCH_MENU.md`](RESIDUAL_BRANCH_MENU.md): city-death series (unnamed); real-policy class (unnamed); independent rerun (park). CR would rewrite wrapping to match §4/§5 — does not meet E-DEM on the parent sentence.

---

## 11. Technical appendix

### Amb path

| Stage | Amb | Note |
|-------|-----|------|
| Cycle 0 | ≈ 10 | Slogan as written |
| After Rank 1 | ≈ 2.5 | Meanings frozen; E-DEM unmet |

### Admitted layers

| ID | One-line | Pointer |
|----|----------|---------|
| D-DOC | Census of arXiv HTML methods/results/limits | `04`, `E_Package_Evidence_Intake.md` |

### Key artifacts

- `Lock_Rank1_DocDemonstrate.md` · `SHARE_PACK.md` · `STATUS.md`

### Failure-mode / tracker pointers

- Wrapper cash vs methods; national deaths posing as urban burdens; SSP labels posing as mitigation.
