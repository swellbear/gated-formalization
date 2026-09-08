# Digestor — 15m SOURCE conflict (not Softened)

**Lane:** `learning_lane_15m` · series `KXBTC15M` only  
**Updated:** 2026-09-07  
**Admit?** N · **Soften?** N

> **Digest:** the full SOURCE honesty digest for this lane is [`LEARNING_LANE_15M_SOURCE_DIGEST.md`](LEARNING_LANE_15M_SOURCE_DIGEST.md) — living spine, every claim cited to a file. This file stays as the standing conflict flag.

## SOURCE (official settle)

Kalshi market `result` when `finalized` / `determined`, matched to event `settlement_sources` CF Benchmarks `BRTI`. Display prices are not settle evidence. DIY CFB average is observe-only.

## CONFLICT (do not Soften away)

Two paper-journal lineages exist:

1. **Lineage B** — Pages / first export (`docs/observability-hub/data/manifest.json`): `KXBTC15M-26SEP071445-45` paper_win `+1.67`. The book that produced it is not on this Windows tree.
2. **Lineage A** — this Windows tree (`golf-offshoot/data/learning_lane_15m/paper/`): later windows (`071545`, `071600`, `071615`, …) with their own seed 100.00.

Cause, cited to code: `src/golf_offshoot/learning_lane_15m/paths.py` `artifact_root_15m()` prefers `/workspace/kalshi_15m_exports` and falls back to the repo root when `/workspace` is absent, as it is here. Same code, different machine, different book.

Do not merge those into one bankroll. Do not invent 15:00 pnl. Golf WC1 does not transfer.

`KXBTC15M-26SEP071500-00` is **not** a pending window. `latest/journal.json` carries Kalshi `result=yes`, `status=finalized`; the paper book the published lineage names is not on this tree, so there is no paper pnl here and none is invented. That is a **missing paper join**. Full statement: [`LEARNING_LANE_15M_SOURCE_DIGEST.md`](LEARNING_LANE_15M_SOURCE_DIGEST.md) §4.

## Living-spine hook

Digestor docs for this lane were leftover-hook only until 2026-09-07 18:03 EDT, when the first real digest landed at [`LEARNING_LANE_15M_SOURCE_DIGEST.md`](LEARNING_LANE_15M_SOURCE_DIGEST.md). This file flags the conflict. It is not an ADMIT and not a weekly honesty Soften.
