# Quantitative Evidence Rubric

**Date:** 2026-08-12 (backfill for closeout hygiene)  
**Application:** `2026-08_sell-in-may-sp500-2026`  
**Bar under test (quote freeze):** Rank 1 Full-Claim-Strict — G1* seasonality gap; G4* strategy Sharpe vs B&H under F3 spirit  
**Source / artifact:** `P2_Attempt1_H2_Workbook_Numbers.md`

---

| # | Check | Result |
|---|-------|--------|
| 1 | **Sample definition** — series, window, return/quantity concept stated? | Yes — ^SP500TR; 1988-01-04→2026-08-11; H2 Nov–Apr / May–Oct; N=37 |
| 2 | **Costs / taxes / frictions** — included, excluded, or N/A (state which)? | Included — 5 bps/side; F3 tax **proxy** (not full Form-8949) |
| 3 | **Significance vs point estimate** — test/interval, or point estimate only? | Point only — gap/Sharpe point estimates; no formal significance test admitted |
| 4 | **Matched comparison** — same locks / same instance on both sides of the bar? | Yes — same series/window; strategy vs B&H under Rank 1 |
| 5 | **Sensitivity to sample window** — noted, tested, or untested? | Noted — series start/end fixed; no alternate-window suite admitted |

---

## Already-included legs (mandatory for numerical / workbook bars)

| Leg | In base bar test? | Notes |
|-----|-------------------|-------|
| G1* winter−summer gap | Y | See workbook |
| R1 switch calendar | Y | |
| T-bill / ^IRX cash yield | Y | Approximate |
| 5 bps costs on switches | Y | |
| F3 tax proxy | Y | Proxy only |
| Matched series/window | Y | |
| Lots / wash / state / NIIT | N | Out of scope |

**If asked “what about X?”:** Point here if X is listed Y.

---

**Conflicted-source?** Non-conflicted (market series workbook)  

**Bar decision supported by this artifact?** G1* **Establish** (gap ~3.52 pp ≥ 2 pp). G4* **Not establish** (AT Sharpe 0.291 ≱ B&H 0.539).  

**Comparability note:** Same rubric used for markets and fiscal numerical bars so fails remain comparable.

---

*Standing rule: Quantitative evidence quality bar + already-included legs.*
