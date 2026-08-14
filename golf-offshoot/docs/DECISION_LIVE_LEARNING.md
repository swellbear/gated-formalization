# Decision, live updates, learning, audit

## Decision layer

Separate from probability. Screens:

- edge vs threshold
- range width
- reliability
- correlation with an existing book (θ proximity proxy)
- hard pass on `thin_sample_overconfidence`

Actions: `pass` / `consider` / `strong_consider`. There is **no execute**. Kelly fraction is a **cap suggestion** only. `never_auto_bet` and `requires_user_confirmation` are always true.

Bets enter the journal only via `BetRecord` the user records.

## Strategy layer (optional)

See [`STRATEGY_LAYER.md`](STRATEGY_LAYER.md). Default **off**. When enabled, pre-tournament construction and live hold/reduce/exit/add/reallocate suggestions are written to `AuditRecord.strategy`. User accept/reject is `user_strategy_decisions`. Still never auto-bets.

## Live / in-tournament

`pipeline.rerun_live` sets `RunMode.LIVE`, unparks `live_position` (hole-dampened evidence + quality), and the simulator banks current to-par while drawing remaining holes with `σ √remaining_rounds`. `diff_runs` writes what changed vs the previous audit.

## Learning

After results:

- Brier and log-loss on Win
- reliability bins (calibration)
- override counterfactual (did Δθ overrides help Brier?)
- `suggest_alpha_update` — simplified residual × contribution step
- `ard_scales_from_alpha` — tiny weights get a small ARD scale

This is the hook for later BO + ARD, not a claim that weights are optimal.

## Versioning and journal

Each run freezes `MODEL_VERSION`, weight hash, config hash, data snapshot hash, full outputs, overrides, user bets. JSON on disk under `data/snapshots/`.
