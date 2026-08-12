# Locking Scaffolding — Sell in May / S&P / 2026

**Date:** 2026-08-12  
**Application:** `2026-08_sell-in-may-sp500-2026`  
**Dominant blocker ID(s):** G2, G3, G4, G5 (and G1 ops; G6 depends on G5)  
**Dependents blocked:** G6 (dated should), G7 (eval standard once metrics exist), any Phase 2 clearance of “improves” or “should”

**Explicit dependency statement:**  
G4 (“improves risk-adjusted vs buy-and-hold”) and G5/G6 (“should”) are blocked primarily because G2 (rule mechanics), G3 (frictions), and G1 (historical ops) remain unset. G6 is further blocked by L1c (averages do not entail 2026) unless a locked **standing rule** under G5 is applied as policy every year.

**Original claim (verbatim, for deviation comparison):**  
“Because the S&P 500 has historically delivered substantially lower average returns from May through October than from November through April, an investor should be out of the S&P 500 (or in cash/T-bills) for the May–October window; following this rule improves risk-adjusted outcomes relative to buy-and-hold over the long run and should be followed for the current May–October 2026 period.”

---

## 0. Plain-language framing (required)

**What decision is being made right now:**  
Choose how strictly to lock (1) what “Sell in May” means as a tradable rule, (2) how to score it vs buy-and-hold, (3) how strong “should” is — including whether 2026 is automatic.

**Why this decision is required before further work:**  
Without locks, “improves risk-adjusted” and both “should”s can mean almost anything; Amb stays high and Phase 2 would be unfalsifiable.

**What becomes testable once the decision is made:**  
Under the chosen package: historical seasonality magnitude for S&P (G1), strategy vs B&H stats (G4), and whether the locked “should” bar is established / not established / refuted.

**What still cannot be settled by this decision alone:**  
Locking meanings does **not** clear the claim. Especially: Amb drop ≠ clearance; a favorable long-run backtest ≠ 2026 weather; soft “should” may remain normative even if descriptive legs pass.

---

## 1. Decision points

| Point ID | Question (plain language) |
|----------|---------------------------|
| D1 | Which S&P return series and sample for the historical “substantially lower” premise? |
| D2 | Exact switch rule (when out / when back in; 100% cash or T-bills)? |
| D3 | Include transaction costs and taxes? |
| D4 | Which risk-adjusted metric vs buy-and-hold? |
| D5 | Soft “should” bar for the standing May–Oct rule? |
| D6 | Soft “should” for May–Oct 2026? |

## 2. Options per decision point

### D1 — Historical premise ops
| Option ID | What it means in ordinary terms | Provenance |
|-----------|---------------------------------|------------|
| H1 | S&P 500 **total return**, calendar May–Oct vs Nov–Apr averages, sample **1950→latest** (Almanac-style long sample) | Common popular sample |
| H2 | S&P 500 total return, same windows, sample **post-1986 publication** only (reduce data-snooping concern) | Loviscek & Broder framing |
| H3 | S&P 500 total return, Bouman–Jacobsen-style long international-comparable window; report S&P specifically | Academic Halloween line |

### D2 — Strategy mechanics
| Option ID | What it means | Provenance |
|-----------|---------------|------------|
| R1 | 100% S&P Nov 1–Apr 30; 100% **T-bills** May 1–Oct 31 (month-end / first-trading-day convention stated at lock) | Classic switching |
| R2 | Same calendar, but **cash** (0% yield) instead of T-bills | Stricter / more punitive to strategy |
| R3 | Partial de-risk (e.g. 50% equities May–Oct) | Softer than claim’s “out” |

### D3 — Frictions
| Option ID | What it means | Provenance |
|-----------|---------------|------------|
| F1 | Pre-tax; ignore trading costs | Optimistic |
| F2 | Pre-tax with modest round-trip costs | Common backtest |
| F3 | After-tax taxable account (short-term gains on switches) + costs | Loviscek & Broder emphasis |

### D4 — Risk-adjusted metric
| Option ID | What it means | Provenance |
|-----------|---------------|------------|
| M1 | Sharpe ratio (excess vs T-bill) of strategy vs B&H over locked sample | Standard |
| M2 | Max drawdown + CAGR pair (must improve both or pre-stated tradeoff rule) | Practitioner |
| M3 | After-tax terminal wealth vs B&H (taxable) | Investor-relevant; overlaps F3 |

### D5 — Soft “should” (general)
| Option ID | What it means | Provenance |
|-----------|---------------|------------|
| S1 | **P-Logical** — not ruled out that being out can help | Near-vacuous vs claim tone |
| S2 | **P-NonNegligible / soft recommendation** — live candidate rule if locked tests favor it | Modest vs claim |
| S3 | **P-BaseCase / default policy** — investor ought to follow as standing policy | Matches claim tone most closely |

### D6 — Soft “should” (2026)
| Option ID | What it means | Provenance |
|-----------|---------------|------------|
| Y1 | Automatic: if S3 standing policy locked, apply every year including 2026 (no 2026 forecast) | Policy application |
| Y2 | Separate: require 2026-specific evidence / forecast edge beyond standing rule | Stronger than Y1 |
| Y3 | Drop dated 2026 prescription from scope | Problem substitution vs claim |

---

## 3–5. Ranked packages (most → least powerful for dependents)

### Rank 1 — Package **Full-Claim-Strict** (R1+F3+M1+H2+S3+Y1)

**What this package concretely means:**  
Post-1986 S&P total-return seasonality; classic 100% T-bill May–Oct switch; after-tax + costs; Sharpe vs B&H; standing **should** as default policy; 2026 follows automatically as yearly application (not a weather call).

**If chosen, the next phase can check:**  
Whether seasonality remains “substantial” under H2; whether strategy Sharpe (after tax/costs) beats B&H; whether S3 remains warranted if tests fail.

**It still cannot settle (vs original claim):**  
Does not make failure of tests into success; Y1 still isn’t a 2026 return prediction.

**Relevance warning:** High overlap with claim wording; tax/cost strictness may make “improves” harder — accuracy-first, not a dodge.

**Objective claim-deviation assessment**  
1. **Strong-language preservation:** “should” kept as S3; “improves risk-adjusted” kept as M1 testable; “substantially lower” needs H2 threshold still to be stated numerically at lock confirmation.  
2. **Problem-identity check:** Same proposition, operationalized.  
3. **Scope / baseline / metric shift:** After-tax + post-1986 are stricter than bare claim (claim silent on tax/sample).  
4. **Deviation summary:** **Moderate deviation** (adds tax/sample ops claim omitted)

### Rank 2 — Package **Classic-PreTax** (R1+F2+M1+H1+S2+Y1)

**What this package concretely means:**  
Long Almanac-style sample; T-bill switch; light costs; Sharpe; soft recommendation (S2) not hard default; 2026 follows if S2 is treated as standing seasonal practice.

**If chosen, next phase can check:** Seasonality magnitude; Sharpe vs B&H pre-tax.

**It still cannot settle:** Hard “should” / obligation; after-tax investor reality; 2026 idiosyncratic risk.

**Relevance warning:** Pre-tax optimism can overstate investor-relevant “improves.”

**Objective claim-deviation assessment**  
1. **Strong-language preservation:** Softens “should” to S2; keeps performance claim as M1.  
2. **Problem-identity check:** Same family; weaker prescription.  
3. **Scope / baseline / metric shift:** H1 long sample; F2 light costs.  
4. **Deviation summary:** **Moderate deviation**

### Rank 3 — Package **Descriptive-Only** (H2+R1+F2+M1, **no** S3/Y1 — S1 only)

**What this package concretely means:**  
Measure seasonality and backtest Sharpe vs B&H, but treat “should” as mere possibility (S1); drop normative force and dated 2026 obligation from official scope.

**If chosen, next phase can check:** Descriptive legs only.

**It still cannot settle:** The claim’s “should … should be followed for 2026” core.

**Relevance warning:** **Partial/weak overlap** with original claim’s prescriptions — do not present as full address.

**Objective claim-deviation assessment**  
1. **Strong-language preservation:** Drops both “should”s’ force.  
2. **Problem-identity check:** **Substitutes** measurement for prescription.  
3. **Scope / baseline / metric shift:** Normative legs out of scope.  
4. **Deviation summary:** **Problem substitution**

### Rank 4 — Package **Forecast-2026** (any mechanics + Y2)

**What this package concretely means:**  
Require separate evidence that May–Oct 2026 specifically should be skipped (macro forecast, etc.), beyond long-run seasonality.

**If chosen, next phase can check:** Whether any non-seasonal 2026 edge exists (likely thin).

**It still cannot settle:** May make G6 intractable quickly.

**Relevance warning:** Stronger than claim’s “because historically…” warrant; claim leans on standing seasonality, not a 2026 forecast model.

**Objective claim-deviation assessment**  
1. **Strong-language preservation:** Keeps 2026 “should” but changes warrant.  
2. **Problem-identity check:** Shifts toward forecasting.  
3. **Scope / baseline / metric shift:** Adds forecast requirement.  
4. **Deviation summary:** **Substantial deviation**

---

## Forced-deviation extraction

**No Minimal-deviation package exists** (all realistic packages ≥ Moderate deviation, or Problem substitution).

| ID | Term | Class | Notes |
|----|------|-------|-------|
| **FD1** | “Because [seasonality] → should be out” as automatic warrant | Over-strong inference | Blocked by L1a; packages must not restore silent entailment |
| **FD2** | Unrestricted “improves risk-adjusted … over the long run” without metric/friction locks | Under-specified | G4/G3 |
| **FD3** | “Should be followed for … May–October 2026” as if entailed by long-run averages | Over-strong / under-specified | L1c; Y1 is policy application, not entailment from averages |
| **FD4** | Bare “substantially lower” without ops | Under-specified | G1 |
| **FD5** | Dual soft “should” as obligation-grade without S-bar lock | Over-strong / under-specified | G5/G6 |

```
Imported pattern from `2026-08_debt-limit-scorekept-pairing-recommendation` (+ parent FD style), re-validated here.
- What was imported: numerical-bar + soft-should package shape; FD extraction when no Minimal-deviation package
- Re-validation under current claim: Rank 1 rebuilt as H2+R1+F3+M1+S3+Y1; G1*/G4* bars defined on market series — not fiscal C≥H; soft should remains open/not selected
- Not inherited: FRA fail, QI ~3.6×, Amb scores, admitted layers from debt apps
```

---

## 6. OR-slots

If selecting Rank 1 or 2, resolve or formally accept “either” for:
- Exact trading calendar convention (month-end close vs first trading day) — recommend **state explicitly at lock**
- Numerical “substantially” threshold (e.g. winter–summer average gap ≥ X pp) — recommend **state explicitly at lock**

---

## 7. Choice prompt

**Pick one:**
1. **Rank 1 — Full-Claim-Strict** (H2+R1+F3+M1+S3+Y1) — recommended if testing the claim as an investor-relevant obligation-style package  
2. **Rank 2 — Classic-PreTax** (H1+R1+F2+M1+S2+Y1) — common backtest style; softer “should”  
3. **Rank 3 — Descriptive-Only** — measurement only (problem substitution; say so)  
4. **Rank 4 — Forecast-2026** — separate 2026 forecast bar  
5. À-la-carte: list D1–D6 option IDs  

**Lock-time Amb warning (mandatory):** Selecting a package will **drop Amb by fixing meanings** (sample, switch rule, frictions, metric, should-bar). **That Amb drop does not establish** historical “substantially,” long-run “improves,” or either “should.” Low Amb after lock ≠ clearance.

**Await operator selection** before reopening G1/G4/G5/G6 as scoped tests under the lock.
