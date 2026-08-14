# Golf Betting Offshoot

Uncertainty-aware golf analysis that sits **beside** Gated Progressive Formalization, not inside it.

This folder is a separate Python system. It does **not** import, score, lock, or mutate the core method, templates, locks, or anything under `applications/`. Residual judgment stays with the user. The system **never auto-bets**.

## Relationship to the core method

| Core method (`applications/`, templates, Amb, gates) | This offshoot |
|------------------------------------------------------|----------------|
| Examines whether a **claim** is established | Estimates **player/field probabilities** with visible uncertainty |
| Must not be modified by this work | New code lives only under `golf-offshoot/` |
| Residual judgment is explicit | Same: decision layer recommends; humans record bets |

Shared *spirit* only: surface free parameters, constrain them with quality-weighted evidence, keep ranges honest, audit what you believed.

## Quick start

```bash
cd golf-offshoot
pip install -e ".[dev]"
pytest
python -m golf_offshoot demo --sims 1500
python -m golf_offshoot explain --player p01
python -m golf_offshoot paper
python -m golf_offshoot paper --paper-file path/to/book.json
python -m golf_offshoot paper --live --json
python -m golf_offshoot strategy --bankroll 2000 --mode stay_selective
python -m golf_offshoot strategy --live --mode protect_profits
```

## Folder structure

```
golf-offshoot/
  README.md
  pyproject.toml
  docs/                  architecture, engines, known limitations
  data/mocks/            reserved for frozen vendor dumps
  data/snapshots/        audit JSON per run
  src/golf_offshoot/
    models/              Player, Tournament, probabilities, audit schemas
    free_parameters/     catalog, course-type importance, boards
    data_feeds/          primary/fallback interfaces + mocks
    bayesian_engine/     prior → evidence updates → MC horizons
    clustering/          comparable players, venue clusters
    field_effects/       this-week field composition
    probability/         coherence helpers
    market/              implied odds, overround, edge, movement
    ranking/             table, reliability, explainability
    decision/            consider/pass — never execute
    flags/               recency, narrative, thin-sample, favorite-longshot
    learning/            calibration, override eval, weight-update hook
    audit/               version + data hash + journal
    strategy/            optional Decision Layer + Dynamic Strategy System
    pipeline.py          pre-tournament and live reruns
    demo.py              deterministic 20-player toy tournament
  scripts/               calibration research entry
  tests/
```

## What a ranked row always shows

For every player: **probability range** (central + low/high), **reliability** (separate from the range), **market edge** when odds exist, **open questions**, **bias flags**, and a one-call **explainability** narrative.

`python -m golf_offshoot paper` prints that **full card for each player currently in the paper book** (user-recorded positions), including stake, entry vs live edge, mark-to-market, and the advisory strategy action. Default is the demo book; pass `--paper-file` for your recorded `PortfolioState` JSON. `--json` dumps the same payload. The engine still **never auto-bets**.

## Non-negotiables

- Uncertainty is always visible (ranges + decomposition + scenarios).
- Weak/low-quality evidence cannot move θ as much as strong evidence.
- Free parameters start broad and are constrained only when data quality allows.
- Model probability ≠ betting decision.
- Full audit: model version, weight hash, data snapshot hash, overrides, user-recorded bets.

## Documentation map

- [Architecture](docs/ARCHITECTURE.md)
- [Free parameters](docs/FREE_PARAMETERS.md)
- [Bayesian engine](docs/BAYESIAN_ENGINE.md)
- [Data feeds](docs/DATA_FEEDS.md)
- [Probability, ranking, market, explainability](docs/PROBABILITY_RANKING_MARKET.md)
- [Decision, live, learning, audit](docs/DECISION_LIVE_LEARNING.md)
- [Strategy layer](docs/STRATEGY_LAYER.md)
- [Known limitations](docs/KNOWN_LIMITATIONS.md)
