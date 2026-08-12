# Phase 2 Attempt 1 Readout — Exact H2 Workbook

**Date:** 2026-08-12  
**Authorization:** Operator authorized Phase 2 (exact H2 workbook)  
**Lock:** Rank 1 Full-Claim-Strict  
**Artifacts:** `P2_Attempt1_H2_Workbook_Numbers.md`, `P2_Attempt1_seasonality_by_year.csv`, `_p2_h2_workbook.py`

---

## Amb ≠ clearance

Workbook **lowered residual on G1*** and **hardened G4* failure**. It does **not** clear the original packaged claim.

---

## Locked-bar status (after Attempt 1)

| Bar | Status | Evidence |
|-----|--------|----------|
| **G1*** substantial seasonality (≥2 pp) | **Established** | ^SP500TR gap **3.52 pp** (mean winter 7.77% vs summer 4.25%; n=37) |
| **G4*** Sharpe improves vs B&H (F3) | **Not established** | Pre-tax Sharpe 0.503 < 0.539; F3-proxy 0.291 < 0.539; CAGR lower |
| **G5*** S3 default “should” | **Not established** | No warrant once G4* fails; L1a |
| **G6*** should for May–Oct 2026 | **Not established** | Y1 tracks G5*; L1c |

---

## Already-included legs

| Leg | In base assessment? |
|-----|---------------------|
| Average winter > summer (G1*) | **Yes** — established, already counted |
| Lower strategy volatility | **Yes** — present; insufficient for Sharpe win |
| T-bill yield in May–Oct | **Yes** — in R1 construction |
| After-tax switch friction | **Yes** — F3 proxy |

“What about seasonality?” — already included; does not rescue G4*/G5*/G6*.

---

## Progress / still open

**Closed this attempt:** Exact H2 G1* measurement; Rank-1 Sharpe comparison (pre-tax + F3 proxy).  

**Still open / residual:** Full tax-lot simulation fidelity; T-bill from ^IRX is approximate; ^SP500TR starts 1988 (not Nov 1986). None of these residuals reverse the G4* direction on current numbers.

**Intractability:** Not declared — residuals are refinement, not blockers.

---

## Amb (informal re-score)

**≈ 2–3** (definitional locks + G1* established + G4*/G5*/G6* statused). Still **≠ clearance**.

---

## Recommended next action

1. **Closeout** Stable Provisional under Rank 1 (honest: seasonality yes; rule/should/2026 not established), optional Thesis Tracker  
2. **Phase 2 Attempt 2** only if authorizing a *different* F3 tax engine or alternate cash proxy — not expected to flip G4* given pre-tax Sharpe already fails  
3. Claim-Revision Scaffolding (e.g. descriptive-only seasonality claim)

**Stop for authorization** before further Phase 2.
