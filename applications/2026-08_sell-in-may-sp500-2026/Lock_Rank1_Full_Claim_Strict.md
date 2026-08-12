# Lock Record — Rank 1 Full-Claim-Strict

**Date:** 2026-08-12  
**Application:** `2026-08_sell-in-may-sp500-2026`  
**Operator selection:** **Rank 1 — Full-Claim-Strict** (message: “R1”)  
**Package codes:** **H2 + R1 + F3 + M1 + S3 + Y1**

---

## Plain-language lock

Under this lock we test the claim as an **investor-relevant standing policy**: after publication-era S&P total returns, switch **100% to T-bills** each May–October (with **taxes and trading costs**), judge “improves risk-adjusted” by **Sharpe vs buy-and-hold**, treat “should” as **default policy**, and apply that policy to **May–Oct 2026** as a yearly instance (not a 2026 weather forecast).

---

## Locked options

| Point | Locked choice | Meaning |
|-------|---------------|---------|
| D1 | **H2** | S&P 500 **total return**; May–Oct vs Nov–Apr; sample **post-1986 publication → latest available** |
| D2 | **R1** | 100% S&P in Nov–Apr window; 100% **T-bills** in May–Oct window |
| D3 | **F3** | **After-tax taxable account** (switches realize short-term gains as applicable) **+** trading costs |
| D4 | **M1** | **Sharpe** (excess vs T-bill) of strategy vs buy-and-hold over the locked sample |
| D5 | **S3** | Soft “should” = **P-BaseCase / default policy** for the standing May–Oct rule |
| D6 | **Y1** | **2026 follows automatically** if S3 standing policy is established — not a separate 2026 return forecast |

---

## OR-slots resolved at lock (explicit)

| OR-slot | Resolution |
|---------|------------|
| Trading calendar convention | **Month-end close:** exit S&P → T-bills at close of **last trading day of April**; re-enter S&P at close of **last trading day of October** |
| “Substantially lower” (G1 threshold) | On H2 sample, average May–Oct six-month total return is lower than average Nov–Apr six-month total return by **≥ 2.0 percentage points** (absolute gap in period returns) |

*(Operator may amend OR-slots; until amended, these are the freeze.)*

---

## Forced-deviation terms (carry forward)

FD1–FD5 from `R_Locking_Scaffolding_G1G2G4G5.md` remain on record. This lock **operationalizes** the claim; it does **not** erase FD findings about silent entailment from seasonality alone.

---

## Amb ≠ clearance (lock-time warning)

Selecting Rank 1 **drops Amb by fixing meanings**. That does **not** establish:
- that the H2 gap meets the ≥2.0 pp threshold,
- that after-tax Sharpe beats buy-and-hold,
- that S3 default policy is warranted,
- or that Y1 application to 2026 is thereby “cleared” beyond policy-application logic.

**Low Amb after lock ≠ claim cleared.**

---

## Scoped questions now well-posed (dependents reopened under lock)

1. **G1\*** — Does H2 S&P total-return seasonality meet the ≥2.0 pp threshold?  
2. **G4\*** — Does Rank-1 strategy Sharpe (F3) exceed buy-and-hold Sharpe on the locked sample?  
3. **G5\*** — Is S3 (default policy “should”) **established / not established / refuted** given G1\*/G4\* and L1a/L1e?  
4. **G6\*** — Under Y1, 2026 “should” **tracks G5\*** (policy application); it is **not** a separate return forecast (L1c still blocks average→2026 entailment).

---

## Next step

Phase 1 may continue under this lock (accuracy-first). **Phase 2** requires **new explicit operator authorization**.
