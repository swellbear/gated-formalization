# Phase 1 viz-wall hook (read-only)

Illustrator owns regeneration. The operator surface **renders files that exist** and shows `not yet available` otherwise. It does **not** generate or fabricate charts. It does **not** import Illustrator internals.

## Display contract

| Slot | Title | Subline |
|------|-------|---------|
| `shadow_honesty_strip` | Shadow honesty strip | Live-book paper journal — not settled PnL · not Kalshi demo |
| `calibration_weather` | Calibration weather | All freezes keep_expert (v1→v3) — not edge established |

Permanent badges on both slots:

`PHASE 1 OBSERVATION` · `AI: NO CASH IN/OUT` · `PAPER OBSERVATION ONLY`

Hard NO: demo/mock edge language on this wall.

## Path precedence

Hardcoded `/workspace/...` is a local operator default only. It will not exist everywhere.

1. `--viz-root` on `python -m golf_offshoot shell`
2. `GOLF_OFFSHOOT_VIZ_ROOT`
3. `/workspace/illustrator_ops/golf_offshoot/` when that shared SoT has Ill PNGs
4. Repo fallback `golf-offshoot/docs/viz/golf_offshoot_dryrun_2026-09-07/`
5. Repo-root fallback `docs/viz/golf_offshoot_dryrun_2026-09-07/` (Illustrator PR #140)
6. `golf-offshoot/data/viz/` (documented hook location; may be empty)

An empty shared `/workspace/illustrator_ops/golf_offshoot/` directory does not hide a fallback that actually has `shadow_honesty_strip.png` / `calibration_weather.png`. The hub renders those PNGs as images. Missing stays `not yet available`. Charts are never invented.

Expected filenames at the resolved root:

- `shadow_honesty_strip.png`
- `calibration_weather.png`
- optional `viz_wall_manifest.json`

## Optional manifest

```json
{
  "slots": {
    "shadow_honesty_strip": {"path": "shadow_honesty_strip.png"},
    "calibration_weather": {"path": "calibration_weather.png"}
  }
}
```

Rules:

- PNG only.
- Paths must stay inside the viz root (no `..`, no absolute escape).
- Refresh display from file mtime. Do not cache a missing file as a chart.
- Invalid or MOCK/DEMO manifests are errors, not silent demo fills.

See also [Operator Guide](OPERATOR_GUIDE.md#14-operator-shell-phase-1).
