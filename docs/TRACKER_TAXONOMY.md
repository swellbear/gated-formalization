# Tracker taxonomy (controlled vocabulary)

Canonical tags for Layers 1–3 and critically relevant application surfacing.  
Standing rule: `.cursor/rules/applications-gated-method.mdc`. Do not invent ad-hoc tags without updating this file.

---

## Domain tags (pick **one** primary per app)

| Tag | Use for |
|-----|---------|
| `foundations` | Physics / philosophy of science / interpretational foundations |
| `engineering` | Architecture, systems engineering, AV stacks, design preferability |
| `fiscal-legislative` | Budget, debt limit, statute-shaped fiscal rules |
| `markets` | Equities, valuation, investment rules, seasonality |
| `opinion-advocacy` | Opinion pieces, political framing, advocacy packages |
| `AI-systems` | LLMs, computational cognition sketches, AI architecture claims |
| `commercial-health` | HCP media, CDS/point-of-care commercial strategy, advertiser-segment expansion |
| `other` | Does not fit above |

---

## Claim-shape tags (one or more)

| Tag | Use for |
|-----|---------|
| `uniqueness-preferability` | “Alone / only / uniquely” + therefore preferable |
| `numerical-standard-plus-should` | Numerical bar (C≥H, Sharpe, gap threshold) packaged with soft “should” |
| `design-spectrum` | Architecture/design as spectrum vs exclusive binary |
| `descriptive-census` | Inventory / hallmark / census claims without strong ought |
| `forecast-extension` | Forward dated window or future-state elevation from history/locks |
| `procedural-rule` | Process/pairing/procedure recommendation |
| `other` | Does not fit above |

---

## Pattern tags (as **observed** in the record — do not force)

| Tag | Use for |
|-----|---------|
| `forced-deviation` | FD extraction / no Minimal-deviation package |
| `R-dependence` | Dependents blocked primarily by unset lock/parameter |
| `comparison-class-unset` | Preferability/uniqueness blocked by unset comparison class |
| `sharpe-after-cost-fail` | Risk-adjusted edge fails after costs/taxes |
| `C-lt-H-fail` | Named instance fails numerical C ≥ H (or analogue) |
| `QI-scale-factor` | QI scale-factor / counterfactual run |
| `contrastive-alternatives` | Contrastive Recommendation mode run |
| `parent-successor-family` | Claim-Revision parent/successor lineage |
| `incomplete-record` | Worksheets/closeout missing; verdict-only reconstruction |
| `stipulated-proxy` | Operator-authorized stand-in used to score locked bars without live data |

---

## Program / training tags (when applicable)

| Tag | Use for |
|-----|---------|
| `training` | Any Training Ladder application |
| `training-ladder` | Explicitly part of the staged ladder path |
| `training-smoke` | Stage 0 smoke / tautology |
| `training-stage-N` | Ladder stage number (`training-stage-0` … `training-stage-8`) |

See `templates/TRAINING_LADDER.md`. Training apps prefer `applications/training/`.

---

## Relatedness (max 4)

Link only with a clear basis in: shared claim-shape, shared pattern, parent/successor, or failure-mode kinship. One-line reason each. **No conclusion inheritance.**
