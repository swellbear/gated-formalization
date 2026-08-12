# Evidence Intake — FRA 2023 Episode (G2/G5)

**Date:** 2026-08-11  
**Application:** `2026-08_debt-limit-scorekept-pairing-recommendation`  
**Locked package / scope label:** **Under Rank 1 claim freeze** (embedded P-Score-Strict+R2-content criterion)  
**Target dependent(s):** G2 (operational H), G5 (instance C≥H)  
**Episode selected:** **Fiscal Responsibility Act of 2023 (P.L. 118-5)** — not the 2025 $5T increase  

**Why this episode (not 2025 $5T):** FRA pairs a debt-limit **suspension** with a published **CBO score** of spending/deficit effects. The July 2025 $5T increase (P.L. 119-21) is a face-value raise bundled with reconciliation that CBO scored as **increasing** deficits — no candidate non-interest cut package C to test against H. FRA is the only recent episode with both CRS suspension/headroom tables and a CBO cut score.

**Authorization:** Operator-authorized short targeted evidence pass (this batch only).

---

## 1. Lock schema (must match freeze)

| Slot | Required by claim freeze | Value in this artifact |
|------|--------------------------|------------------------|
| Scorekeeper | Official CBO-style | CBO letter on H.R. 3746 (May 30, 2023) |
| Cuts counted | Non-interest disc + mandatory outlay reductions | Disc outlays −$1.3T (2024–2033); mandatory net −$10B; **interest excluded** (−$188B interest is **not** in C) |
| Baseline | Current-law / CBO May 2023 baseline | CBO May 2023 baseline (as in letter) |
| Window | Budget window | CBO 2023–2033 / discretionary table 2024–2033 |
| Anti-gimmick | Ban timing shifts / interest games | Interest excluded; FRA caps are statutory (sequester-enforced for 2024–25). Residual caveat: later appropriations “side deals” can erode realized savings vs scored path |
| Match target R2 | ≥ estimated borrowing headroom from suspension | H ≈ post-suspension reset limit − prior statutory limit |

**Schema match?** **Partial → usable for fail/pass test** — official C and a transparent H proxy exist; H is **ex post reset-based**, not a CBO prospective headroom score published inside the FRA text. Anti-gimmick is only partially auditable (no claim that all later appropriations adhered to scored path).

---

## 2. Artifact summary

### Artifact A — CRS debt-limit suspensions (H proxy)

**Source:** CRS Insight IN11829, *Debt Limit Suspensions* (updated Sep 11, 2025), https://www.everycrsreport.com/reports/IN11829.html  

**Reports:** FRA (P.L. 118-5) enacted June 3, 2023; suspended debt limit through January 1, 2025; limit reinstated January 2, 2025 at **$36.1 trillion** ($36,104 billion in Table 2). Prior statutory limit after Dec 2021 increase was just under **$31.4 trillion** (same CRS note; CBO Feb 2023 statutory-limit piece).  

**H (operational, this episode):**  
\[
H_{\mathrm{FRA}} \approx \$36.1\mathrm{T} - \$31.4\mathrm{T} = \$4.7\mathrm{T}
\]  
(Effective borrowing headroom created by the suspension/reset — same figure cited by CRFB as “effectively raised … by $4.7 trillion.”)

### Artifact B — CRS extraordinary-measures tables (context only; not H)

**Source:** CRS Insight IN10837, *Debt Limit Policy Questions: What Are Extraordinary Measures?* (Table 1, 2021–2025), https://www.everycrsreport.com/reports/IN10837.html  

**Reports:** Jan–June **2023** extraordinary-measures headroom components (e.g. G Fund ~$294B, ESF ~$17B, DISP one-time/monthly figures, etc.).  

**Use:** Documents pre-FRA binding-limit mechanics. **Must not** be used as H for the FRA suspension itself (those measures delay the X-date; they are not the suspension’s decade borrowing headroom).

### Artifact C — CBO score for FRA / H.R. 3746 (C)

**Source:** CBO letter to Speaker McCarthy, May 30, 2023, *CBO’s Estimate of the Budgetary Effects of H.R. 3746, the Fiscal Responsibility Act of 2023*, https://www.cbo.gov/system/files/2023-05/hr3746_Letter_McCarthy.pdf  

**Reports (vs May 2023 baseline):**  
- Total deficit reduction ≈ **$1.5T** (2023–2033), **including** interest  
- Discretionary outlay reductions ≈ **$1.3T** (2024–2033)  
- Mandatory spending, on net, **−$10B**  
- Revenues, on net, **−$2B**  
- Interest on public debt **−$188B** (exclude from C under freeze)  
- Division D: temporarily suspend debt limit through Jan 1, 2025  

**C (operational, this episode, non-interest outlay reductions):**  
\[
C_{\mathrm{FRA}} \approx \$1.3\mathrm{T} + \$0.01\mathrm{T} = \$1.31\mathrm{T}
\]  
(Discretionary outlay cuts + mandatory net outlay cut. Revenue effects and interest **excluded** per claim freeze.)

---

## 3. Provisional gate intent

- [x] Aim **ADMIT** G2 operational H for FRA episode (reset-based)  
- [x] Aim **ADMIT** G5 instance result: FRA **fails** C≥H under freeze  
- [ ] Aim HOLD only if numbers too ambiguous — they are not, for a fail test

**ADMIT bar:** Transparent official C + transparent H proxy; clear inequality.  
**HOLD bar:** If C or H only qualitative.  
**REJECT triggers:** Wrong episode; using interest as C; using extraordinary-measures stack as H; promoting fail instance into “should” verdict or parent FD language.

---

## 4. Scoped-result honesty

Findings hold **under Rank 1 claim freeze, FRA 2023 episode only.**  

**Partial / claim-adjacent?** Instance test of the **descriptive balance criterion** — not a resolution of soft “should” (G1).  

**Must not be promoted to:** Soft “should” true/false; parent FD1–FD5; claim that FRA “was fiscally irresponsible” in unrestricted sense; claim that extraordinary-measures dollars equal H; claim that later appropriations preserved the full scored C path.

---

## 5. Next

- [x] Proceed to formal `04` admissions (L2a H, L2b C, L2c C≱H)
