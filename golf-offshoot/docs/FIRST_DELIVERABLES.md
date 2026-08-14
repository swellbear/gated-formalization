# First deliverables (A–G)

Written against the live tree under `golf-offshoot/` after the initial implementation pass. Core Gated Formalization files were not modified.

## A. Final folder structure

See [README.md](../README.md). Top-level `golf-offshoot/` (not `applications/`) so the method, templates, locks, and existing apps stay untouched.

## B. README

[README.md](../README.md) — purpose, relationship to the core method, quick start, non-negotiables.

## C. Core data models / schemas

Pydantic v2 in `src/golf_offshoot/models/`:

- Identity: `Player`, `Course`, `Tournament`, `FieldSnapshot`
- Evidence: `DataQuality`, `EvidenceItem`, `StrokesGainedProfile`, `PlayerInputs`
- Free parameters: `FreeParameterDef`, `FreeParameterState`
- Outputs: `HorizonProbability`, `ProbabilityBundle`, `PlayerOutput`, `ReliabilityScore`, `ExplainabilityReport`
- Market: `MarketQuote`, `MarketSnapshot`
- Decision / journal: `DecisionAdvice`, `HumanOverride`, `BetRecord`, `AuditRecord`, `ModelVersionRecord`, `TournamentRunResult`

## D. Free-parameter system

Catalog in `free_parameters/catalog.py` (required eight families plus structural/live factors). Importance = course-adjusted impact × constrainingability. Boards start unconstrained and move to partial/constrained only with quality and n. Narrative is capped. Course type rescales (links weather, major bogey-avoidance, etc.).

## E. Bayesian engine (ranges and evidence strength)

`θ` prior from long-term talent. Updates: `α × quality × constrainingability × evidence × correlation-discount`. Weak quality cannot match strong quality (tested). Variance stays wide when data are thin. Same θ drives MC Make Cut / T20 / T10 / T5 / Win with percentile-style ranges, leave-one-factor decomposition, and optimistic/pessimistic scenarios on open majors. `α` starts expert-initialized; `calibration/` fits a first-pass BO+ARD vector on pre-event ESPN history and freezes it under `data/calibration/`.

## F. Ranking + market edge + explainability

`rank_field` always attaches Win range, reliability, edge (model − fair implied), open questions, flags, and `explain_player` (prior → posterior, contribution list). Market removes overround before edge. Decision advice is a separate pass/consider layer and cannot execute.

## G. Assumptions and open questions

**Assumptions**

- Round scores independent given θ (except live re-conditioning).
- Demo field is 20 players with a scaled cut; production tournaments set `cut_place` on `Tournament`.
- Vendor feeds are mocked; quality/fallback contracts are real.
- Weights are not yet season-calibrated.
- Positive edge means the model is hotter than the de-juiced book, not “this is a bet.”

**Open implementation questions (do not block v0.1)**

1. Which live SG/odds vendor is canonical (Data Golf, official ShotLink, exchange vs book)?
2. Exact major vs PGA cut/playoff variants to freeze per tour.
3. Whether to replace θ-proximity portfolio correlation with a fitted finish copula once enough audits exist.
4. Shot-level remaining-strokes live model vs current holes-completed blend.
5. When to run the first real BO+ARD pass (needs a logged season, not the demo).

---

## Strategy layer (v0.2)

See [`STRATEGY_LAYER.md`](STRATEGY_LAYER.md) for A–G on the Decision Layer + Dynamic Strategy System. Default off. Never auto-bets.
