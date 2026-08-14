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

## Live remaining holes

When `RunMode.LIVE`:

**Score card (MC):**

```
total = current_to_par + (−θ × remaining_rounds) + N(0, σ √remaining_rounds)
remaining_rounds = (H − h) / 18
H = n_rounds × 18
```

Completed holes are not resimulated.

**Skill nudge (`live_position`):**

```
raw = −score_to_par / 3
dampen = (h/H)×(h/18)   if h < 18
dampen = h/H            if h ≥ 18
evidence = raw × dampen
quality = 0.30 + 0.65 × (h/H)   (capped at 0.95)
```

A −6 through 6 holes (`H=72`) has `dampen ≈ 0.028`, not the old undampened evidence of 2.0 that produced ~26% Win for an early leader.

## Field MC note

Cut place is the tournament's ESPN cut (or `cut_place` on the object). Events with `has_cut=False` / `cut_after=0` skip the 36-hole cut. The demo sets `cut_place=10` for a 20-player field; the engine no longer silently halves the field.
