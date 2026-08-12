# Anchor & Claim-Type Template

**Date:** 2026-08-11  
**Domain / Source material:** Autonomous driving architecture debate (end-to-end neural vs modular perception–planning–control)  
**Application ID / short name:** `2026-08_av-e2e-vs-modular-preferability`

---

## L₀ — Objective Anchors

List only anchors that are hard to dispute (empirical results, logical constraints, or strong intersubjective facts). Number them.

1. Production and research AV systems exist that emphasize learned end-to-end (or heavily neural) mappings from sensors to controls/waypoints, and systems that emphasize modular pipelines with separately engineered perception, prediction/planning, and control modules connected by explicit interfaces.
2. In a modular pipeline, errors or mis-calibrations at an upstream interface can affect downstream modules (composition / interface-error propagation is a real engineering phenomenon).
3. Modern deep learning systems in many domains improve predictive performance with more data and larger models under suitable training regimes (broad empirical regularity; not AV-specific proof of safety improvement).
4. Modular AV stacks can and do incorporate learned components (detectors, predictors, learned planners) trained on data; “modular” does not mean “non-learning.”
5. Architecture choice for AV is evaluated under multiple criteria in practice (safety/validation, interpretability/debuggability, data efficiency, latency, liability/regulatory fit, operational design domain) — not a single scalar “preferability” by default.
6. Hybrid architectures (learned modules inside modular skeletons; E2E with intermediate supervision / discrete interfaces) are common; the E2E↔modular boundary is not a sharp exclusive partition in deployed practice.

---

## Candidate Claim or Layer Element

**Full statement of the claim / layer being evaluated:**

“End-to-end neural networks are preferable to modular (perception–planning–control) architectures for autonomous driving because they alone avoid cascading errors from hand-engineered interfaces and can continue to improve with data and scale in a way that modular stacks structurally cannot.”

---

## Pre-Classification (required)

Select one (or split mixed claims):

- [ ] **Descriptive** (factual, causal, or structural)
- [ ] **Normative / Strategic** (value, advocacy, prescription, or framing recommendation)
- [x] **Mixed** — split as follows:
  - Descriptive part: (D1) E2E uniquely avoids cascading errors from hand-engineered interfaces; (D2) E2E can continue to improve with data/scale; (D3) modular stacks *structurally cannot* improve that way; (D4) “alone” uniqueness of E2E on these grounds.
  - Normative/Strategic part: (P) Therefore E2E is *preferable* to modular architectures for autonomous driving.

**Notes on classification:**  
(D1)–(D4) are structural/causal comparative claims. (P) is preferability and inherits whatever criteria are left unspecified. Treat (P) as blocked until descriptive premises are constrained; do not admit preferability by rhetoric.

---

## Ready for Gate Scoring?

- [x] Yes — proceed to Gate Scoring Sheet  
- [ ] No — revise anchors or claim statement first
