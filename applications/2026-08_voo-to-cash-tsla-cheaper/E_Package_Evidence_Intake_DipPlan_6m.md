# Package Evidence Intake — Dip Plan-6m E1/E2

**Date:** 2026-08-12  
**Application:** `2026-08_voo-to-cash-tsla-cheaper`  
**Locked package:** Dip Plan-6m (R2 + H-6m + M3)  
**Target:** E1 (P(T0)+threshold), E2 (M3 path)

---

## 1. Lock schema

| Slot | Required | Value in artifact |
|------|----------|-------------------|
| R | ≤ 0.90×P(T0) | Threshold below |
| H | 6 months to 2027-02-12 | Unchanged |
| M | M3 non-negligible path | Assessed below |
| T0 | 2026-08-12 | Same |

**Schema match?** Yes  

---

## 2. Artifact summary

### E1 — Price / threshold

**Sources:** Exa market library TSLA (Aug 12, 2026 print); StockAnalysis / CNBC prior close Aug 11, 2026.  

| Item | Value |
|------|--------|
| **P(T0) used** | **$327.47** (Aug 12, 2026 session print) |
| **0.90 × P(T0)** | **$294.72** |
| Prior close (Aug 11) | $332.81 (context only; not used as P(T0)) |
| 52-week low (cited) | ~$297.38 (2026-07-29) — about **9.2%** below P(T0); near but above threshold |
| 52-week high (cited) | ~$498.83 (2025-12-22) |

**Close caveat:** Same-day print may differ slightly from final official close. If final close differs by more than ~1%, recompute threshold; M3 qualitative conclusion unlikely to flip for a ~10% bar on this name.

### Conflicted-source flag
- [x] **Non-conflicted** for price prints / historical vol-drawdown stats (market data / analytics)  
- [ ] Sell-side targets — **not used** to affirm M3  

### E2 — M3 path evidence (ordinary public)

| Fact | Bearing on M3 |
|------|----------------|
| TSLA 1y ann. vol cited ~46%; multi-year ~55–60% | 10% move in 6 months is well inside ordinary volatility scale |
| Historical drawdown stats: many events; average depth ~10%; average duration ~tens of days | A ≥10% decline within 6 months is a **recurring** path class for this name — not vanishingly thin |
| Large peak-to-trough history (30%+ and deeper drawdowns repeatedly) | Supports path thickness for a milder −10% bar |
| Already near 52w low zone vs P(T0) | Shows proximity to threshold; does **not** by itself prove a further print ≤ $294.72 |

**M3 reading:** A **non-negligible path** to ≤ $294.72 within 6 months is **established**.  
**Not claimed:** That the print **will** occur; that it is **likely** (M4); that one **should** buy.

---

## 3. Provisional gate intent
- [x] ADMIT E1 numbers (with close caveat)  
- [x] ADMIT M3 **established** under Dip Plan-6m  
- [x] HOLD / reject any “should buy TSLA” or “will bottom” elevation  
- [x] Affirm G5: VOO gain / 50% cash does **not** warrant M3 (M3 stands on TSLA path evidence alone)

---

## 4. Scoped-result honesty

Holds **under Dip Plan-6m only**.  
Partial: M3 path ≠ timing success ≠ advice.  
Must not promote to: investment recommendation; VOO sale wisdom; “more cash is correct.”
