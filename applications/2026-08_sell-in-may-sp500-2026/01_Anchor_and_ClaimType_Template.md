# Anchor & Claim-Type Template

**Date:** 2026-08-12  
**Domain / Source material:** Equity seasonality / “Sell in May” (Halloween indicator); S&P 500; investor strategy claim for May–Oct 2026  
**Application ID / short name:** `2026-08_sell-in-may-sp500-2026`

---

## L₀ — Objective Anchors

List only anchors that are hard to dispute (empirical results, logical constraints, or strong intersubjective facts). Number them.

1. The S&P 500 is a capitalization-weighted equity index of large U.S. stocks; calendar returns can be partitioned into May–October vs November–April six-month windows.
2. Holding equities vs holding cash / T-bills are distinct portfolio states with different expected return and risk profiles over any given window.
3. A historical average seasonal differential (if present) is a sample statistic about past returns; it does not logically entail that any specific future window will underperform, nor that a trading rule is obligatory.
4. “Risk-adjusted outcomes” vs buy-and-hold is a comparative performance claim that requires explicit metrics, costs, taxes, and a sample design before it is well-posed.
5. Soft “should” prescriptions are normative/strategic; they are not forced by descriptive seasonality alone.
6. Public finance literature documents a long-discussed Halloween / “Sell in May” seasonality pattern (e.g. Bouman & Jacobsen 2002 and follow-ons); existence of a literature ≠ unrestricted endorsement of the packaged investor rule or of a named forward window.

---

## Candidate Claim or Layer Element

**Full statement of the claim / layer being evaluated:**

“Because the S&P 500 has historically delivered substantially lower average returns from May through October than from November through April, an investor should be out of the S&P 500 (or in cash/T-bills) for the May–October window; following this rule improves risk-adjusted outcomes relative to buy-and-hold over the long run and should be followed for the current May–October 2026 period.”

---

## Pre-Classification (required)

Select one (or split mixed claims):

- [ ] **Descriptive** (factual, causal, or structural)
- [ ] **Normative / Strategic** (value, advocacy, prescription, or framing recommendation)
- [x] **Mixed** — split as follows:
  - Descriptive part: Historical S&P 500 average returns May–Oct substantially lower than Nov–Apr; (contested) that following the seasonal rule improves risk-adjusted outcomes vs buy-and-hold over the long run.
  - Normative/Strategic part: An investor **should** be out (cash/T-bills) in May–Oct generally; and **should** follow the rule for **May–October 2026**.

**Notes on classification:**  
The “because” clause packages a descriptive premise as warrant for two prescriptions. “Improves risk-adjusted outcomes” is framed as descriptive/strategic performance but is under-determined without metric locks. Forward “should … 2026” is a dated prescription that cannot be settled by long-run averages alone.

### Soft-modal fork (when claim uses potential / could / may / should / etc.)

If soft modals carry claim strength, flag early (do not wait for endpoint):

| Term in claim | Candidate bar (circle one when locking) |
|---------------|----------------------------------------|
| “should be out … for the May–October window” (general rule) | P-Logical / P-NonNegligible / **P-BaseCase** / other: **strategic prescription (S-Should)** — lock required |
| “should be followed for … May–October 2026” (dated) | same fork; may need separate **S-Should-2026** lock |
| “improves risk-adjusted outcomes” | not a modal; needs **metric/package lock** (Sharpe / Sortino / etc.) |

**Near-vacuity warning:** Unbounded P-Logical (“might sometimes be better to be out”) + open horizon would be near-vacuous relative to this claim’s assertive packaging — state if operator picks P-Logical.

---

## Ready for Gate Scoring?

- [x] Yes — proceed to Gate Scoring Sheet
- [ ] No — revise anchors or claim statement first
