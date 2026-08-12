# Anchor & Claim-Type Template

**Date:** 2026-08-12  
**Application ID:** `2026-08_fomc-june-2026-sep`  
**Domain:** markets / official U.S. monetary-policy projections  
**Frame:** Cycle 0 confirmed; **L1 OBJECT-FORECAST** locked (operator `forecast`). F-ML not established. July 29 OUT.

## L₀ — Objective Anchors

1. The Federal Reserve released *Summary of Economic Projections* materials for the June 16–17, 2026 FOMC meeting at 2:00 p.m. EDT, June 17, 2026: [PDF](https://www.federalreserve.gov/monetarypolicy/files/fomcprojtabl20260617.pdf) and [accessible HTML](https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260617.htm).  
2. The document states that participants submitted projections of **most likely outcomes** for GDP, unemployment, and inflation for 2026–2028 and the longer run, each under that participant’s assessment of **appropriate monetary policy**.  
3. Eighteen participants submitted in June; one of those 18 did not submit 2028 projections. Nineteen had submitted in March 2026.  
4. Full cell-level inventory (medians, central tendencies, ranges, dots, histograms, uncertainty/risk tallies, RMSE fans, definitions) is in [`CLAIM_INVENTORY.md`](CLAIM_INVENTORY.md).

**OUT of L₀ / claim package:** July 29, 2026 FOMC statement; news/blog gloss; named-official non-submission stories not in this PDF.

## Candidate claim (census of the document)

The June 17, 2026 SEP is a published package of FOMC participants’ projections of **most likely** GDP, unemployment, inflation, and **appropriate** federal-funds paths for 2026–2028 and the longer run. The document’s claims are the inventory in [`CLAIM_INVENTORY.md`](CLAIM_INVENTORY.md): process/definitions, printed actuals, June Table 1 medians/CT/ranges, March-to-June revisions, the dot plot and histograms, uncertainty/risk judgments, RMSE-based 70% fans, and the prose elevations (most likely; appropriate policy; longer-run convergence under no further shocks).

## Pre-Classification (required)

- [x] **Mixed** — split:
  - **D-DOC:** Release identity, meeting dates, 18/19 submitter counts, March vintage (inventory A).  
  - **D-DEF:** Q4/Q4, median/CT/range, funds-rate midpoint, core-PCE-no-LR, RMSE/CPI footnotes (inventory B).  
  - **D-ACTUAL:** 2021–2025 actuals as printed (inventory C).  
  - **D-SEP:** June Table 1 medians, CT, ranges (inventory D–E).  
  - **D-REV:** March vs June printed medians / implied revisions (inventory F).  
  - **D-DOTS / D-HIST:** Figure 2–3 distributions (inventory G–H).  
  - **D-UNCERT:** June uncertainty/risk tallies and diffusion indexes (inventory I).  
  - **D-RMSE:** Table 2 and printed 70% fans, with the document’s own caveats (inventory J).  
  - **F-ML:** Submitted figures are **most likely** outcomes (K1).  
  - **C-APPROP:** Paths are **appropriate** policy under each participant’s mandate reading (K2–K3).  
  - **F-LR:** Longer-run values (incl. PCE **2.0**) are expected convergence under appropriate policy and **no further shocks** (K4–K5).

### Soft-modal / classification fork

| Term | Candidate bar |
|------|----------------|
| most likely outcomes | **Locked L2: P-BaseCase** (expected / central path). Bar **not met**. Funds-rate dots not under this bar. |
| appropriate monetary policy | Individual mandate reading vs Committee decision vs realized path |
| longer run / no further shocks | Open horizon + ceteris paribus (near-vacuity risk if unbounded) |
| 70% confidence | Historical RMSE convention vs participants’ current uncertainty judgments |
| median | The Committee’s forecast vs a census statistic of 18 submissions |

## Imported locks

```
Imported pattern from forecast-extension + Amb≠clearance cluster, re-validated here.
- LOCK-2026-08-003 (Amb drop / freeze ≠ clearance)
- LOCK-2026-08-009 (soft-modal / window when forward)
- LOCK-2026-08-010 (posed ≠ clearance)
- LOCK-2026-08-011 (announcement/history ≠ full elevation)
- Re-validation: Official SEP is live primary; cells are a census; “most likely” / “appropriate” / longer-run 2% are elevations.
- Not inherited: Zitron / CoreWeave / sell-in-may / SpaceX verdicts; July 29 FOMC statement.
```

## Live vs stand-in

**Live:** June 17, 2026 SEP PDF + accessible HTML (same release).  
**OUT:** July 29 statement; secondary news gloss.

- [x] Ready for Cycle 0 gate scoring  
- [x] **Cycle 0 operator-confirmed 2026-08-12** (Cons / Agree / Prod / Amb ≈ 11; gap order 1→8 as drafted).  
- [x] **L1 OBJECT-FORECAST** (operator `forecast` 2026-08-12). Commitment not selected.  
- [x] **L2 F-ML P-BaseCase** (operator `basecase` 2026-08-12). Bar **not met**.  
- [x] **L3 D-DOC** (operator authorized recommended step 2026-08-12). Process/identity only.  
- [x] **L4 D-DEF** (operator `admit.` 2026-08-12 after recommended D-DEF; C-APPROP offered, not selected). Measurement / table-reading definitions only.  
- [x] **L5–L10 remaining D-*** (operator `admit all remaining layers in question` 2026-08-12). Submitted/printed census; not F-ML met.  
- [x] **L11 C-APPROP individual-mandate** (same authorization). Meaning freeze; vote/realized-path **not met**.  
- [x] **L12 F-LR** (same authorization). Convergence + no further shocks; dated/2026-on-target **not met**.  
- [x] **L13 F-ML-BAR 2026 test** (operator `test F-ML-BAR on 2026 medians` 2026-08-12). Bar **not established** for GDP 2.2 / U 4.3 / PCE 3.6 / core 3.3. Not a refute. Funds-rate off bar.  
- [x] **L14 G4 median-load-bearing** (operator `whatever you recommend next` 2026-08-12). Median of 18 (17 for 2028); CT/range/dots distributional. Not Committee forecast. Not F-ML met.  
- [x] **L15 G5 year-slots** (operator `proceed with recommended` 2026-08-12). 2026 / 2027 / 2028 / LR separate. LR 2.0 ≠ 2026 on-target. 2027–28 F-ML untested.  
- [x] **L16 G7 tallies ≠ RMSE** (operator `proceed with recommended` 2026-08-12). D-UNCERT ≠ D-RMSE. 17/18 ≠ 70% interval. RMSE ≠ current FOMC uncertainty.  
- [x] **Residual + optional-mode menus offered** (operator `residual menu` 2026-08-12). No branch/mode run. QI N/A. July 29 still OUT.  
- [x] **Hard stop sealed** (operator `closeout` 2026-08-12). Default keep original wording. G8 not locked. Amb ≈ 1.
