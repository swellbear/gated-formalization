# Options Offshoot

Uncertainty-aware **paper** options tape that sits **beside** Gated Progressive Formalization, not inside it. It does **not** import golf-offshoot, Amb, gates, templates, or anything under `applications/`. Residual judgment stays with the user. The system **never auto-trades**.

## Relationship to the core method

| Core method (`applications/`, templates, Amb, gates) | This offshoot |
|------------------------------------------------------|----------------|
| Examines whether a **claim** is established | Estimates **contract** fair vs the ask, with visible uncertainty |
| Must not be modified by this work | New code lives only under `options-offshoot/` |
| Residual judgment is explicit | Same: advice is not a ticket |

Shared *spirit* only: surface free parameters, constrain them with quality-weighted evidence, keep ranges honest, audit what you believed. B-guts is GPF-*like*, not GPF.

## What this is not

- Not a golf Win% table. Rows are contracts. Sort is **vs-ask**, not P(ITM).
- Not “every option in the universe.” You pick a **predeclared field**.
- Not a hunter. The `fields` index is a **map**. Do not pour $20k into the fattest table.
- Not GPF-integrated. Running the tape as “these prices are established” still fails Amb.

## Quick start

```bash
cd options-offshoot
pip install -e ".[dev]"
pytest
python -m options_offshoot demo
python -m options_offshoot fields
python -m options_offshoot ingest --field earnings_us_week
python -m options_offshoot live --field spx_this_friday
```

`demo` prints an **OFFLINE DEMO — MOCK DATA** banner. It is not the operating path.

Operating ingest/live need `POLYGON_API_KEY` in `options-offshoot/.env` (see `.env.example`). Do not commit `.env`.

**Paper bankroll:** $20,000 **per field per path**. Independent. Never auto-trade. Settle at expiry.

## Folder structure

```
options-offshoot/
  README.md
  docs/                  operator, compare method, feeds, leftover, limitations
  data/fields/           frozen ticker universes
  src/options_offshoot/
```
