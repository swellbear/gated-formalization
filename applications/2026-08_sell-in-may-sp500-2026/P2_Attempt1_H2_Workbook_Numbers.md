# P2 Attempt 1 — H2 Workbook Numbers

**Generated:** 2026-08-12 11:59 UTC
**Series:** ^SP500TR
**Price start/end:** 1988-01-04 → 2026-08-11
**N winter/summer windows:** 37

## G1* Seasonality (H2)

| Metric | Value |
|--------|-------|
| Mean Nov–Apr (winter) | 7.7718% |
| Mean May–Oct (summer) | 4.2541% |
| Gap (winter − summer) | 3.5176% |
| Threshold | ≥ 2.00 pp |
| **G1* threshold met?** | **YES** |

| Median gap | 3.5273% |
| % years winter > summer | 70.3% |

## G4* Strategy vs buy-and-hold

### Pre-tax (costs 5 bps/side on switch days only in after-tax block)

| Metric | Strategy (R1) | Buy & hold |
|--------|---------------|------------|
| CAGR | 8.8211% | 11.5385% |
| Ann. vol | 12.6693% | 17.8499% |
| Sharpe (ex T-bill) | 0.503 | 0.539 |

### F3 proxy (τ_ST=32% on April exit gains; 5 bps/side costs; B&H terminal τ_LT=20% on cumulative gain for CAGR only)

| Metric | Strategy after-tax proxy | B&H |
|--------|--------------------------|-----|
| CAGR | 6.0157% | pre-tax 11.5385% / terminal-LT nan% |
| Sharpe (ex T-bill) | 0.291 | 0.539 (B&H stream pre-tax daily) |

**G4* (strategy Sharpe > B&H Sharpe under F3 spirit)?** Strategy AT Sharpe 0.291 vs B&H Sharpe 0.539 → **NO** on this proxy.

## Method notes / limitations

- T-bill daily return from ^IRX discount yield transformed to effective daily — approximate.
- F3 tax model is a **proxy**, not a full Form-8949 simulation (lots, wash sales, state tax, Medicare surtax omitted).
- B&H Sharpe uses pre-tax daily equity returns (deferred realization); favors honesty that switcher pays interim tax.
- If ^SP500TR unavailable historically, SPY adj-close proxy noted in Series line.

By-year seasonality CSV: `P2_Attempt1_seasonality_by_year.csv`