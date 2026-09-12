# Kalshi golf ingest island (golf-1)

Public-GET catalog for golf-tagged Kalshi series. Own artifact root. **Not** a merge of `cursor/golf-kalshi-gym`, and **not** a Pages lane.

Harvested catalog / matcher / path isolation from gym tip `fdcb556` via `git show`. Paper, `--watch`, Kelly, mix/brain, hub tab, Farm/Honer, and a Pages `lane_id` stay later slices.

Trading is **NOT ARMED**.

## Destination

```
golf-offshoot/data/golf_kalshi/
  latest/catalog.json
  latest/unmatched.json
  cache/                    # HTTP cache for public series/markets
```

Test override: `set_golf_kalshi_root_override(path)`. Never writes `learning_lane_15m`, `/workspace/kalshi_15m_exports`, or Phase 1 `data/paper/`.

## CLI

```bash
cd golf-offshoot
PYTHONPATH=src python -m golf_offshoot golf-kalshi          # one-shot ingest
PYTHONPATH=src python -m golf_offshoot golf-kalshi --json
PYTHONPATH=src python -m golf_offshoot golf-kalshi --refresh
```

`--watch` is refused here (golf-3). This command does not start or kill 15m PaperWatch.

Selector stays exact `golf` | `learning_lane_15m`. `lane_header_name("golf")` is still **Golf Phase 1**. Bare `15m` still → golf.

## Catalog

Public Kalshi only. Series from `/series?tags=Golf` (Sports fallback), then `/markets?series_ticker=…&status=open|settled`. The global `/markets?status=open` dump is refused. A row needs a golf `series_ticker`. Fail-open last-good is golf-only.

This package does **not** change `kalshi_15m.ALLOWED_SERIES` (`KXBTC15M` only).

## Unmatched

Names that do not match a supplied candidate map stay unmatched. Ingest does not invent a `player_id` and does not write a paper fill. No field → catalog + unmatched file only.

## Hard NOs

- Do not mix golf and 15m ledgers, bankrolls, n-counts, or lessons.
- Do not widen `kalshi_15m.py` `ALLOWED_SERIES`.
- Do not invent unmatched players, missing fields, or Kalshi results.
- Private / cash / order URLs are refused. `TRADING_ARMED = False`.
- Polymarket is not a venue here.
- Do not retune Phase 1 golf θ.
- Hub selector and Pages schema are unchanged in this slice.

## Later (not this slice)

golf-2 paper ledger, golf-3 `--watch`, golf-4 wallet recipe, golf-5 shell tab. Those must not land by “finishing” this ingest.
