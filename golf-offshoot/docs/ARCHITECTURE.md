# Architecture

The offshoot is a pipeline, not a claim-examination worksheet.

```
data feeds (quality-scored, primary→fallback)
        ↓
free-parameter board (start broad → constrain)
        ↓
comparable-player + venue-cluster borrow (thin samples)
        ↓
field-interaction adjustments (this week's composition)
        ↓
Bayesian θ update (evidence × quality × constrainingability; correlation discount)
        ↓
Monte Carlo field (same latent → Make Cut / T20 / T10 / T5 / Win)
        ↓
market edge + reliability + flags + explainability
        ↓
decision advice (never auto-bet)
        ↓
optional strategy layer (pre-tournament book / live hold-reduce-exit-add; off by default)
        ↓
audit snapshot (version, weights, data hash, overrides, user bets, strategy suggestions)
        ↓
post-event learning (calibration, override eval, α update hook)
```

## Spec coverage

| Spec item | Module |
|-----------|--------|
| 1 Free-parameter system | `free_parameters/` |
| 2 Automated data feeds | `data_feeds/` |
| 3 Bayesian update engine | `bayesian_engine/` |
| 4 Comparables & venue clusters | `clustering/` |
| 5 Field interaction | `field_effects/` |
| 6 Multi-horizon probabilities | `bayesian_engine/simulate.py`, `probability/` |
| 7 Market-relative layer | `market/` |
| 8 Ranking + explainability | `ranking/` (`report.py` = full player cards; `paper` CLI scopes them to the book) |
| 9 Reliability score | `ranking/reliability.py` |
| 10 Decision layer | `decision/` |
| 10b Strategy layer (optional) | `strategy/` |
| 11 Live updates | `pipeline.rerun_live`, live factors |
| 12 Learning loop | `learning/` |
| 13 Bias flags | `flags/` |
| 14 Versioning | `audit/`, `config.MODEL_VERSION` |
| 15 Decision journal | `audit/journal.py` |
| 16 Known limitations | `docs/KNOWN_LIMITATIONS.md` |

## Modes

- **Pre-tournament:** live-only factors are parked.
- **Live:** `live_position` / tee-pairing enter the board (hole-dampened); MC banks observed to-par and simulates remaining holes only.

## What is mocked today

**Operating path (`ingest`, `calibrate`, `pressure-test`, `live`): no mocks.** Missing vendors are labeled `unavailable`.

Mocks exist only for `python -m golf_offshoot demo` (explicit banner) and unit tests.
