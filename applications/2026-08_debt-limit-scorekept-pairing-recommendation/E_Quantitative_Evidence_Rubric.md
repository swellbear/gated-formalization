# Quantitative Evidence Rubric

**Date:** 2026-08-12 (backfill for closeout hygiene)  
**Application:** `2026-08_debt-limit-scorekept-pairing-recommendation`  
**Bar under test (quote freeze):** Embedded Rank 1 — episode balanced iff C ≥ H  
**Source / artifact:** `E1_Evidence_Intake_FRA_2023.md` + `04h_…L2c…`

---

| # | Check | Result |
|---|-------|--------|
| 1 | **Sample definition** — series, window, return/quantity concept stated? | Yes — FRA 2023 episode; CBO C; CRS H |
| 2 | **Costs / taxes / frictions** — included, excluded, or N/A (state which)? | N/A — fiscal magnitudes (interest **excluded** from C by freeze) |
| 3 | **Significance vs point estimate** — test/interval, or point estimate only? | Point only — magnitude match; fail is arithmetic |
| 4 | **Matched comparison** — same locks / same instance on both sides of the bar? | Yes — same FRA episode for C and H |
| 5 | **Sensitivity to sample window** — noted, tested, or untested? | Noted — episode-scoped; other episodes open (R-EPISODE-2) |

---

## Already-included legs (mandatory for numerical / workbook bars)

| Leg | In base bar test? | Notes |
|-----|-------------------|-------|
| CBO non-interest C | Y | |
| CRS headroom H | Y | |
| Interest excluded from C | Y | |
| Same-episode match | Y | |
| Soft should / parent FDs | N | Separate |

---

**Conflicted-source?** See E1 intake  

**Bar decision supported by this artifact?** **Refute** (FRA fails C≥H for this episode only).  

**Comparability note:** Same rubric used for markets and fiscal numerical bars so fails remain comparable.

---

*Standing rule: Quantitative evidence quality bar + already-included legs.*
