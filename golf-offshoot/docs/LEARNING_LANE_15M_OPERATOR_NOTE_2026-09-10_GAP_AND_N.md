# Operator note — overnight hole and `rule_reached_n` (not a score)

**Verdicts:** **CLOSED / recorded defect** on the overnight hole · **counts only** on `rule_reached_n` · Operator · 2026-09-10 07:35 EDT
**Not an ADMIT.** Not Softened. Not a score. Not a bind. Not a dashboard figure.
**Lane:** `learning_lane_15m` · series `KXBTC15M` only · `lab_admits=false` · Trading **NOT ARMED**

This note is the only place these two rulings live together. It does not go in `manifest.json`, the hub, `records[]`, or any dated record.

Owed subjects this write names (so the park can clear Operator): `KXBTC15M-26SEP100515-15`, `R-SKIP-COINFLIP`, `R-SKIP-2TO1-FAVORITE`.

---

## 1. Overnight hole — do not backfill

Detector: `window_sequence_gap KXBTC15M-26SEP100515-15` (the first window after the hole).

Eight consecutive windows **do not exist** on this tree: `KXBTC15M-26SEP100315` through `KXBTC15M-26SEP100500` (03:00–05:00 EDT). No paper book, no settle file, no ledger row, no journal `windows[]` row. Adjacent `100300` and `100515` exist. Honer has none of the eight stems. This is **not** the `072245` `--once` argparse collision.

**Ruling:** CLOSED / recorded defect. Same class as row 11. Do not invent a fill, a Kalshi `result`, a `0`, or a pnl. Do not put those eight in any denominator. The locked count is not an unbroken overnight sample.

Caveat: [`LEARNING_LANE_15M_SOURCE_DIGEST_CAVEATS.md`](LEARNING_LANE_15M_SOURCE_DIGEST_CAVEATS.md). Park row 14.

---

## 2. `rule_reached_n` — report the count, do not score

`looks.first_look_n` on the bar is **70**. Counted this turn from settle files' `settlement_ts` (228 settled files on this tree).

| Rule | `declared_at` | Eligible settled after `declared_at` | Lived after execution flip | `execution` | Scored this turn? |
|---|---|---:|---:|---|---|
| `R-SKIP-COINFLIP` | 2026-09-08T05:56:00-04:00 | **172** | n/a (`execution` false; no lived paper) | **false** | **No** |
| `R-SKIP-2TO1-FAVORITE` | 2026-09-08T16:53:00-04:00 | **128** | **127** (after `lived_paper_begins_at` 17:11) | true (paper) | **No** |

The falsifier is now *rulable* on n. That is not a park on the falsifier and not an Establish.

**`R-SKIP-COINFLIP`:** do not open a post-declaration outcome file. The band is not verifiably pre-registered. L1 cannot Establish. `execution` stays false.

**`R-SKIP-2TO1-FAVORITE`:** still RUN-ONLY. `favorite_odds=2` is not verifiably pre-registered. L1 cannot Establish. Do not retune `favorite_odds`. This turn does not run `score_rule`.

The eight missing overnight windows are **not** invented into either count.

---

## What this turn did not do

- Bind the evidence bar
- Enable honer consult
- Arm trading
- Score either rule
- Backfill `100315`–`100500` or `072245`
- Probe the fee PDF / write a placeholder hash
