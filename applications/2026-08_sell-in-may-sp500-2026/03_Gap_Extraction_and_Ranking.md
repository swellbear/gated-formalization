# Gap Extraction & Ranking Sheet

**Date:** 2026-08-12  
**Parent application / claim:** `2026-08_sell-in-may-sp500-2026`  
**Linked Gate Scoring Sheet:** `02_Gate_Scoring_Sheet.md` (Cycle 0)

---

## Identified Gaps (Free Parameters)

### Gap G1
**Description:** Historical sample period, index series, and return definition for “substantially lower average returns” May–Oct vs Nov–Apr (price vs total return; arithmetic vs geometric; what “substantially” means).  

**Claim-freeze (one sentence — lock what this free parameter *is*):**  
G1 is the operational definition of the historical seasonality premise for the S&P 500 (sample, return concept, and substantiality threshold).  

**Impact (0–2):** 2  
**Anchor connection (0–2):** 2  
**Measurability (0–2):** 2  
**Sum:** 6  

### Gap G2
**Description:** Strategy mechanics — calendar switch dates, cash/T-bill proxy, 100% exit vs partial, re-entry rules.  

**Claim-freeze (one sentence):**  
G2 is the trading-rule definition of “out of the S&P 500 (or in cash/T-bills) for the May–October window.”  

**Impact (0–2):** 2  
**Anchor connection (0–2):** 2  
**Measurability (0–2):** 2  
**Sum:** 6  

### Gap G3
**Description:** Transaction costs, taxes, dividend treatment, and frictions in the strategy vs buy-and-hold comparison.  

**Claim-freeze (one sentence):**  
G3 is the friction and cash-flow treatment applied when comparing the seasonal rule to buy-and-hold.  

**Impact (0–2):** 2  
**Anchor connection (0–2):** 1  
**Measurability (0–2):** 2  
**Sum:** 5  

### Gap G4
**Description:** Risk-adjusted performance metric(s) and what counts as “improves … relative to buy-and-hold over the long run.”  

**Claim-freeze (one sentence):**  
G4 is the metric package and evaluation design that would make “improves risk-adjusted outcomes vs buy-and-hold” a well-posed test.  

**Impact (0–2):** 2  
**Anchor connection (0–2):** 2  
**Measurability (0–2):** 2  
**Sum:** 6  

### Gap G5
**Description:** Soft-modal strength of the general “should be out … May–October” prescription.  

**Claim-freeze (one sentence):**  
G5 is the locked bar for the standing seasonal “should” (e.g. strategic recommendation strength — not mere logical possibility).  

**Impact (0–2):** 2  
**Anchor connection (0–2):** 1  
**Measurability (0–2):** 1  
**Sum:** 4  

### Gap G6
**Description:** Soft-modal / warrant for applying the rule specifically to May–October 2026.  

**Claim-freeze (one sentence):**  
G6 is what would make “should be followed for May–October 2026” true or false under the locked general rule (if any) — a dated application, not a restatement of long-run averages.  

**Impact (0–2):** 2  
**Anchor connection (0–2):** 1  
**Measurability (0–2):** 1  
**Sum:** 4  

### Gap G7
**Description:** Long-run sample length / statistical significance standard for strategy evaluation.  

**Claim-freeze (one sentence):**  
G7 is the evaluation horizon and inferential standard used for the long-run comparison.  

**Impact (0–2):** 1  
**Anchor connection (0–2):** 1  
**Measurability (0–2):** 2  
**Sum:** 4  

### Gap G8
**Description:** Warrant bridge — whether historical average seasonality licenses the packaged prescriptions.  

**Claim-freeze (one sentence):**  
G8 is the inference rule from descriptive seasonality (and any strategy backtest) to investor “should” (general and/or 2026).  

**Impact (0–2):** 2  
**Anchor connection (0–2):** 2  
**Measurability (0–2):** 1  
**Sum:** 5  

---

## Claim-freeze register (working; finalize at Phase 1 endpoint)

| Gap ID | One-sentence freeze lock |
|--------|--------------------------|
| G1 | Operational definition of historical May–Oct vs Nov–Apr S&P 500 seasonality premise |
| G2 | Trading-rule definition of being “out” / in cash-T-bills for May–Oct |
| G3 | Friction and cash-flow treatment in strategy vs B&H |
| G4 | Risk-adjusted metric package vs B&H over the long run |
| G5 | Soft “should” bar for the standing May–Oct rule |
| G6 | Dated “should” for May–Oct 2026 under the locked rule |
| G7 | Long-run evaluation horizon / significance standard |
| G8 | Warrant from history/backtest to prescription |

*Later candidates must quote the freeze line for any parameter they claim to close. Changing the freeze line is a claim change, not progress.*

---

## Priority Order (highest sum first)

1. G1, G2, G4 (tied 6) — definitional locks for descriptive/strategic tests  
2. G3, G8 (5) — frictions + warrant bridge  
3. G5, G6, G7 (4) — soft shoulds + significance  

**Soft-modal note:** Offer locking-scaffolding for G5/G6 early; do not wait until all descriptive gaps close.

---

## Search Plan for Top-Priority Gap(s)

**Targeted gap:** Structural constraints first (seasonality ≠ obligation; dated window ≠ long-run average; risk-adjusted needs metric lock), then literature-shaped descriptive constraints without silently clearing G5/G6.  

**Source classes to check:** Seasonality literature (Bouman & Jacobsen; follow-ons); investor-facing backtests (costs/taxes); logical L₀ applications.  

**Diminishing-returns / time-box rule:** Prefer ADMIT of structural layers that shrink Amb without pretending the packaged claim is cleared.  

**Notes:** Accuracy posture — literature disagreement on B&H superiority is itself material for G4/G8.
