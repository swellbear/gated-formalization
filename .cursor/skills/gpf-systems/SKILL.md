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

## Done

Handoff → `validator`. Always.
