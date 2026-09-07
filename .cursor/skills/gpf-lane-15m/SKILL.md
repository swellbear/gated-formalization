---
name: gpf-lane-15m
description: Runs the KXBTC15M paper loop (ingest, live, paper autobet, settle join). Never self-admits. Use when CoS assigns lane-15m, or when refreshing the 15-minute Kalshi learning lane.
disable-model-invocation: true
---

# 15-min researcher

Paper observation only. `lab_admits=false`. Trading NOT ARMED.

## Start

Read [PROTOCOL.md](../../../docs/agents/PROTOCOL.md) and [golf-offshoot/docs/LEARNING_LANE_15M.md](../../../golf-offshoot/docs/LEARNING_LANE_15M.md). Post START.

## Do

From `golf-offshoot/`:

```bash
python -m golf_offshoot lane-15m
```

Official settle = Kalshi `result` matched to CF Benchmarks `BRTI`. If no `result`, leave `SETTLE_PENDING`.

## You may

- Public Kalshi read
- 15m paper ledger / snapshots under the 15m root
- Ask Founder if you would have to invent a result

## You must not

- Keys, orders, cash UI
- DIY CFB average as official settle
- Self-admit
- Retune golf θ
- Widen past `KXBTC15M` without Founder GO

## Done

Handoff → `systems` (so the Pages manifest can match the journal).
