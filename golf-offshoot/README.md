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
python -m golf_offshoot strategy --bankroll 2000 --mode stay_selective
python -m golf_offshoot ingest                 # real ESPN field (no mocks)
python -m golf_offshoot calibrate              # historical BO+ARD, pre-event features only
python -m golf_offshoot pressure-test
python -m golf_offshoot live
python -m golf_offshoot shadow              # review paper-observation advises
```

The `demo` / `explain` / `strategy` commands print an **OFFLINE DEMO — MOCK DATA** banner. They are not the operating path.

**Weekly use:** [Operator Guide](docs/OPERATOR_GUIDE.md) — how to run ingest/live, read ranges vs edge, and stay observation-only until the system actually earns more.

## Folder structure

```
golf-offshoot/
  README.md
  pyproject.toml
  docs/                  architecture, engines, known limitations
  data/mocks/            reserved for frozen vendor dumps
  data/snapshots/        audit JSON per run
  data/exports/          full-field ranked tables (PDF + HTML + txt) from ingest/live
  src/golf_offshoot/
    models/              Player, Tournament, probabilities, audit schemas
    free_parameters/     catalog, course-type importance, boards
    data_feeds/          real ESPN / Open-Meteo / Bovada / Hard Rock Bet (Odds API) / PGA SG / opening archive + mocks (demo/tests only)
    calibration/         leakage-safe dataset + BO/ARD weight fit
    operating.py         real-path ingest / pressure-test helpers
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

## Non-negotiables

- Uncertainty is always visible (ranges + decomposition + scenarios).
- Weak/low-quality evidence cannot move θ as much as strong evidence.
- Free parameters start broad and are constrained only when data quality allows.
- Model probability ≠ betting decision.
- Full audit: model version, weight hash, data snapshot hash, overrides, user-recorded bets.

## Documentation map

- **[Operator Guide](docs/OPERATOR_GUIDE.md)** — start here for weekly use
- [Architecture](docs/ARCHITECTURE.md)
- [Free parameters](docs/FREE_PARAMETERS.md)
- [Bayesian engine](docs/BAYESIAN_ENGINE.md)
- [Data feeds](docs/DATA_FEEDS.md)
- [Calibration](docs/CALIBRATION.md)
- [Pressure test (St. Jude 2026)](docs/PRESSURE_TEST_2026_ST_JUDE.md)
- [Probability, ranking, market, explainability](docs/PROBABILITY_RANKING_MARKET.md)
- [Decision, live, learning, audit](docs/DECISION_LIVE_LEARNING.md)
- [Strategy layer](docs/STRATEGY_LAYER.md)
- [Known limitations](docs/KNOWN_LIMITATIONS.md)
- [Leftover callout](docs/PARKED_LEFTOVER_CALLOUT.md) — after operating `live` / `ingest` strategy (display only)
- [Shadow journal](docs/SHADOW_JOURNAL.md)
