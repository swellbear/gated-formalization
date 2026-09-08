---
name: gpf-systems
description: Writes the observability export (manifest.json) against SCHEMA. Use when CoS assigns systems, after lane-15m has a new journal, or when publishing hub data (not chrome).
disable-model-invocation: true
---

# Systems

Data export. Hub UI owns chrome. You write the one file the public viewer reads.

## Start

Read [PROTOCOL.md](../../../docs/agents/PROTOCOL.md), [docs/observability-hub/data/SCHEMA.md](../../../docs/observability-hub/data/SCHEMA.md), and [golf-offshoot/docs/SHAREABLE_OBSERVABILITY_EXPORT.md](../../../golf-offshoot/docs/SHAREABLE_OBSERVABILITY_EXPORT.md). Post START.

## You may

- `docs/observability-hub/data/manifest.json`
- `python -m golf_offshoot observability-export` from `golf-offshoot/`
- Numbers as **strings**. No `bankroll` / `autobet` keys.

## You must not

- Invent Kalshi `result` / win/lose
- Change hub HTML/CSS/JS (that is `hub-ui`)
- Merge golf WC1 into the 15m lane
- Add controls or cash fields

## After validator

If `--strict` is clean **and** `material_publish_reasons(what_master_serves, this_export)` is non-empty, commit the manifest + current real PNG and push so Pages updates. Do not publish a heartbeat. Do not leave a corrected falsehood on `master`.

## Done

Handoff → `validator`. Always. After a material publish, note the commit and `hub.generated_at` on the desk.
