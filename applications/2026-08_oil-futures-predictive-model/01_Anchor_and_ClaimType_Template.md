# Anchor & Claim-Type Template

> **Plain language.** This sheet pins down starting facts and says what sentence is under test. It does not prove the claim.

**Date:** 2026-08-17  
**Domain / Source material:** Operator question (verbatim); crude oil futures as exchange-traded contracts  
**Application ID / short name:** `2026-08_oil-futures-predictive-model`

---

## L₀ — Objective Anchors

**In plain language:** List only starting points that are hard to dispute for this run.

1. Standardized **crude oil futures** are listed and traded on major exchanges (widely cited examples: NYMEX Light Sweet Crude Oil / WTI under ticker **CL**; ICE **Brent**). A futures price is a contracted price for a specified grade, location, and timing — not the same object as an unstandardized cash spot print, though the two are related.
2. A **model**, in ordinary use, is a specified mapping from inputs to outputs. Writing *some* mapping that emits a number labeled “forecast” is cheap. Whether that mapping **predicts**, and relative to **what baseline**, is a different question.
3. Listed oil-futures prices form **recorded time series** that can be used as inputs, targets, or both.
4. The listed **futures curve** is already a set of market prices for future delivery. Fitting past prints is not the same claim as **beating that curve**, or as making money after costs.
5. The claim text uses the soft modal **“can.”** It does **not** name a contract, tenor, horizon, success metric, sample protocol, or a “should trade / should build” prescription.
6. A historical fit, a published outlook, or the mere existence of forecasting software does **not** by itself license a forward live edge or a default-action elevation (process kinship with LOCK-011; re-validated here, not inherited as a verdict).

---

## Candidate Claim or Layer Element

**In plain language:** The full sentence under test — not a quieter rewrite.

**Full statement of the claim / layer being evaluated:**

Can a predictive model for oil futures be built?

---

## Pre-Classification (required)

**In plain language:** This is a fact-style feasibility question as written, not a “should trade” sentence. Stronger packages below would split in a later lock; they are not smuggled in as the as-written type.

Select one (or split mixed claims):

- [x] **Descriptive** (factual, causal, or structural)
- [ ] **Normative / Strategic** (value, advocacy, prescription, or framing recommendation)
- [ ] **Mixed** — split as follows:
  - Descriptive part:  
  - Normative/Strategic part:  

**Notes on classification:**  
As written, the sentence asks whether construction/feasibility of a forecasting procedure is possible. There is no “should.” Rank 2 in the lock table (after-cost economic value) would add a **performance / trading-edge** elevation and would then be treated as **Mixed**. Rank 3 (existence census) stays Descriptive. **Rank 4** (operator-asked A+B+C combination) would **split** D-EXIST / F-SKILL / V-VALUE rather than blending them; V-VALUE stays a marked elevation, not a “should trade.” Do not score an unstated “should we trade oil futures with a model” as this claim. Split sheet (draft only): `MULTI_ELEVATION_SPLIT.md`.

**Critically related apps (process only; no conclusion inheritance):**  
- `2026-08_spacex-600-dollar-stock` — soft-modal “can/potential” plus missing window/success criterion.  
- `2026-08_fomc-sep-2026-uffr-change` — object fork (census vs forecast vs odds) must lock before a well-posed test.

### Soft-modal fork (when claim uses potential / could / may / should / etc.)

**In plain language:** “Can” is doing the strength work. Choosing the height is not meeting it.

| Term in claim | Candidate bar (circle one when locking) |
|---------------|----------------------------------------|
| “can” | P-Logical / P-NonNegligible / P-BaseCase / other: **unset — lock package required** |

**Near-vacuity warning:** Unbounded **P-Logical** (“not a contradiction that some program emits a number”) plus unspecified contract/horizon/metric is **near-vacuous**. Low productivity. State this if Rank 3 is selected. Do **not** silently strengthen “can” into “expected to work” (P-BaseCase) or into a trading recommendation.

---

## Imported Active locks (before first full gate scoring)

| Lock | Why imported | Cons vs these L₀ |
|------|----------------|------------------|
| **LOCK-2026-08-003** | Amb drop / scope lock ≠ clearance | No clash |
| **LOCK-2026-08-009** | Soft-modal + window/success freeze on forecast-shaped language | No clash |
| **LOCK-2026-08-010** | Forecast well-posedness ≠ bar-met (specialize 003) | No clash |
| **LOCK-2026-08-011** | History / published track record ≠ forward material “can” / live edge | No clash |

**Not imported:** LOCK-006 (no “should” in the claim text). If a later package adds a prescription, import 006 then.

**Stamp:** `IMPORTED_PATTERN_STAMP.md`

---

## Ready for Gate Scoring?

**In plain language:** The starting facts are stable. The *sentence* is still mushy; Cycle 0 scores that under-specification rather than pretending a lock already exists.

- [x] Yes — proceed to Gate Scoring Sheet (Cycle 0 of unconstrained slogan)
- [ ] No — revise anchors or claim statement first
