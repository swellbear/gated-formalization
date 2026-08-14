# Probability, ranking, market, explainability

## Probability outputs

Same model, five horizons: Make Cut, Top 20, Top 10, Top 5, Win. Each has central + low/high, Win decomposition, optimistic/pessimistic Win scenarios.

Reliability is **not** the interval width. A tight interval with sparse data is flagged (`thin_sample_overconfidence`).

## Ranking display

`rank_field` sorts by Win central. Each `PlayerOutput` includes range, reliability, edges, open questions, flags, explainability, optional decision advice.

CLI table columns: rank, name, Win range, T10, Cut, Win edge, reliability, flags.

Full card: `format_player_report` / `python -m golf_offshoot explain --player p01`. Paper-scoped cards (only names in the current book): `python -m golf_offshoot paper`. See [Strategy layer](STRATEGY_LAYER.md#h-full-reports-on-the-current-paper).

## Market

- American → decimal → raw implied
- Proportional overround removal → `implied_fair`
- Edge = model_p − fair implied (positive: model hotter than the market)
- Movement vs a previous snapshot when provided

## Explainability

`explain_player` (also attached on every row): prior θ → posterior θ ± sd, largest Δθ contributions with quality, borrowed-strength notes, field-interaction note, open questions. One call, no second model.
