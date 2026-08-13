# Bayesian update engine

## Latent

Each player has skill θ (higher = better). The field is simulated from posterior θ, not from a single softmax slogan.

## Prior

`θ ~ (talent_prior, talent_prior_sd²)`. Lesser-known players get a wider prior.

## Evidence-weighted update

For each non-parked factor:

```
Δθ = α_f × ARD_f × quality × constrainingability × standardized_evidence × stacking_discount
```

- **quality ∈ [0,1]** — weak data cannot move θ like strong data (same evidence, 0.10 vs 0.95 quality, is tested).
- **constrainingability** — some factors (narrative, weather splits) cannot pin θ even when a number exists.
- **status** — unconstrained evidence is heavily shrunk; partial is half-weight.
- **stacking_discount** — correlated factors (form & trend, SG-match & approach) do not add at full strength.
- **narrative cap** — `|Δθ_narrative| ≤ 0.35`.

Variance shrinks only when quality × constrain is high. Missing data leaves the range wide.

## Weights and later calibration

`alpha` is expert-initialized (`bayesian_engine/weights.py`). The learning loop can take a simplified gradient step and expose ARD scales (`ard_scales_from_alpha`). Full Bayesian optimization + ARD is the intended next fit, not a claimed current optimum.

## Ranges

Monte Carlo:

- Draw θᵢ from its posterior.
- Four round scores `~ Normal(-θ, σ²)`.
- Cut after 36 holes (configurable place + ties).
- From the same draws: Make Cut, Top 20, Top 10, Top 5, Win.
- Displayed low/high = spread of block-level rates around the coherent central (not a fake ±).

Horizons are forced **coherent**: Win ≤ T5 ≤ T10 ≤ T20 ≤ Make Cut.

## Decomposition and scenarios

Leave-one-factor-out shares attribute Win-range width. Optimistic/pessimistic scenarios push major *unconstrained* factors and map Δθ through a field softmax so the user sees how open parameters could move Win.

## Field MC note

Cut place is min(tournament.cut_place, field-scaled default) so a 20-player demo is not using a PGA 65-cut against 20 names.
