# Shareable observability export

Binds to Hub UI PR [#151](https://github.com/swellbear/gated-formalization/pull/151).

The viewer reads **only** `docs/observability-hub/data/manifest.json`. Schema SoT: [`docs/observability-hub/data/SCHEMA.md`](https://github.com/swellbear/gated-formalization/blob/master/docs/observability-hub/data/SCHEMA.md).

Local operator shell (ingest / live / paper autobet / settle / trigger) is **not** exposed.

## Publish paths

| Path | What |
|------|------|
| `docs/observability-hub/data/manifest.json` | **Primary.** Hub UI contract. `lanes` is an array. Numbers are strings. |
| `docs/observability-hub/data/SCHEMA.md` | Schema SoT (PR #151) |
| `/workspace/kalshi_15m_exports/latest/journal.json` | Live 15m journal only — not the Pages contract |
| `golf-offshoot/docs/observability/` | Pointer notes only. Not the Pages contract. |

Journals stay isolated. Golf paper/shadow never write into the 15m root. Live `golf-offshoot/data/exports/observability/` is gitignored.

## Contract locks

- Canonical lane ids: `golf` | `learning_lane_15m` (Hub UI SoT). No bare `15m` alias.
- `lanes` is an **array**.
- Operating figures are **strings**.
- Forbidden control / cash / secret **keys** are refused (including `bankroll` and `autobet` as keys). Paper counts go under `paper_ledger.rows` labels/values.
- Never put golf WC1 under `learning_lane_15m`.
- Missing charts stay `not yet available` — never invented.

```bash
python -m golf_offshoot observability-export
```
