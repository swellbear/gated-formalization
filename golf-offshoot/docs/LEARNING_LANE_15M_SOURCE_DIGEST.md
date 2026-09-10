# Digestor — 15m SOURCE honesty digest (living spine)

**Lane:** `learning_lane_15m` · series `KXBTC15M` only
**Role:** `digestor` — honesty owner. Never Soften / Harden / Kill / ADMIT.
**Admit?** N · **Soften?** N · **Trading ARMED?** N
**Evidence as-of:** 2026-09-10 07:42 EDT (`latest/journal.json` `generated_at`)
**Figures:** generated from files. **Caveats:** concatenated verbatim from [`LEARNING_LANE_15M_SOURCE_DIGEST_CAVEATS.md`](LEARNING_LANE_15M_SOURCE_DIGEST_CAVEATS.md). The generator may not write that file.

Truth on disk, in the order this digest trusts it:

| Rank | File | What it is |
|------|------|-----------|
| 1 | `golf-offshoot/data/learning_lane_15m/settlements/*.json` | Official Kalshi join |
| 2 | `golf-offshoot/data/learning_lane_15m/latest/journal.json` | Kalshi tape |
| 3 | `golf-offshoot/data/learning_lane_15m/paper/*.json` + `paper/ledger.json` | Lineage A |
| 4 | `docs/observability-hub/data/manifest.json` | Lineage B published export |
| aid | `latest/learning_wake.json` | Derived, never authoritative |
| aid | `docs/observability-hub/data/charts/learning_lane_15m/paper_window_strip.png` | Illustrator board |

---

## Generated figures

Cited to the file that recorded them. No default, no zero-fill, no pnl a file does not have.

### Lineage A — `paper/ledger.json`

- `starting_bankroll` 100.0 → `bankroll` 87.33 · `betting_pnl` -12.67 · `deposits` 0.0 · `withdrawals` 0.0
- entries 458 (1 `observation_seed`, 229 `paper_fill`, 121 `settle_loss`, 107 `settle_win`)
- events 228
- paper books on this tree: 229 (228 with `settled_at`, 1 open: `KXBTC15M-26SEP100745`)
- settle files on this tree: 229
- first event `event_name`: `BTC price up in next 15 mins?`
- last event `event_name`: `BTC price up in next 15 mins?` · `settled_at` `2026-09-10T07:15:58.172221-04:00` · last-row ticket `pnl` +1.30 · `bankroll_after` 87.33

Recorded book. The standing caveats say these figures omit the known fee.

### Pending on the current journal tape

`KXBTC15M-26SEP100745-45` · journal `status` `active` · `result` "" · `window_id` `KXBTC15M-26SEP100745__2026-09-10T11:30:00Z__2026-09-10T11:45:00Z`

### Absences (recorded as absence, not as zero)

- `KXBTC15M-26SEP072245` paper+settle files present? `False` — expected absent; see caveats.
- overnight hole `100315`–`100500` (8 windows) paper+settle files present? `False` — expected all absent; see caveats.
- `KXBTC15M-26SEP071500-00` paper+settle files present? `False` — expected absent; missing paper join.

### Lineage B — `docs/observability-hub/data/manifest.json`

- hub `generated_at` `2026-09-10T07:42:16.378625-04:00` (local export; a local rewrite is not a publish)
- `$.lanes[1].records` length: 0
- published history kept: `KXBTC15M-26SEP071445-45` `paper_win` `+1.67` — cited to the manifest, never re-derived here, never added to lineage A

<!-- BEGIN STANDING CAVEATS — generator must concatenate this file verbatim and may never write, rewrite, reorder, or drop it -->

# Standing caveats (hand-authored)

The figures generator concatenates this file after the generated figures section. It may **never** write, rewrite, reorder, or drop this file. A new caveat is a human Digestor turn.

**Lane:** `learning_lane_15m` · series `KXBTC15M` only
**Role:** `digestor` — honesty owner. Never Soften / Harden / Kill / ADMIT.
**Admit?** N · **Soften?** N · **Trading ARMED?** N

Sibling flag: [`LEARNING_LANE_15M_SOURCE_CONFLICT.md`](LEARNING_LANE_15M_SOURCE_CONFLICT.md).
Operator park: [`LEARNING_LANE_15M_METHOD_PARK.md`](LEARNING_LANE_15M_METHOD_PARK.md).
Habit: [`docs/DIGESTOR_LIVING_SPINE_INDEX_HABIT.md`](../../docs/DIGESTOR_LIVING_SPINE_INDEX_HABIT.md).

---

## Resume (later bot)

This digest is a **living spine**, not a dated record. Numbers in the generated figures section drift every ~15 minutes while the watch runs. Refresh them with the generator; do not invent replacements.

```powershell
cd golf-offshoot
$env:PYTHONPATH = "src"
python -m golf_offshoot digest-15m
python -m golf_offshoot learn-15m
```

The wake is a **reading aid, not truth**. It names which roles are owed and copies figures out of files; it never Softens, never ADMITs, and never invents a win, a lose or a pnl.

**Path convention.** A window's stem is its `window_id` with `:` replaced by `-` (`safe_artifact_stem`). Settle file: `golf-offshoot/data/learning_lane_15m/settlements/<stem>.json`. Paper book: `golf-offshoot/data/learning_lane_15m/paper/<stem>.json`.

---

## SOURCE lock

Official settle for this lane is **Kalshi market `result`**, and only when the market is `finalized` / `determined`, matched to the event's documented `settlement_sources` — **CF Benchmarks**, CF index id pinned `BRTI`.

Display prices (`yes_bid` / `yes_ask` / `last_price` / `volume`) are not settle evidence. They price a paper fill; they never decide a window.

A DIY CF Benchmarks average is observe-only. A CFB websocket feed is observe/debug only and is a Hard NO as official settle without match-to-Kalshi-result.

---

## Fee omission

**These recorded figures omit a known, measured cost.** `settle.py` pays `stake × decimal_odds` with no fee term. The Operator note ([`LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md`](LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md), RUN-ONLY) measured the missing entry-side Kalshi taker fee on this lane. That cost is not in the ledger, not in `betting_pnl`, and not in the recorded bankroll chain. The recorded book is therefore incomplete, not merely rounded.

This paragraph does **not** replace those figures with a fee-accurate total — minting that number is a claim, and fee-accurate pnl still does not go on the hub, in `manifest.json`, or in `records[]`. The digest may name the omission. It may not print a corrected total.

---

## Locked count is not an unbroken run

**Locked** = an official Kalshi result in a settle file on this tree AND a paper book on this tree for the same `window_id`. The generated locked count is **not** an unbroken run — see the outage gaps below (`072245` and the overnight `100315`–`100500` hole).

This digest does **not** reprint a window-by-window scoreboard. That table would read as a track record.

---

## Outage gap — `KXBTC15M-26SEP072245` does not exist

**This is a defect to record, not to explain away.**

`KXBTC15M-26SEP072245` (the 22:30–22:45 EDT window) is absent from every file this digest trusts: no `paper/` file, no `settlements/` file, no `ledger.json` entry or event, no `latest/journal.json` `windows[]` row.

Cause: the 22:25–22:50 EDT outage from the `--once` argparse collision. Adjacent windows `072230-30` and `072300-00` exist. The 15-minute hole between those `window_id`s is the missing window.

**Do not backfill it. Do not infer what it would have been.** No Kalshi `result`, no paper fill, no pnl. Anyone who treats the locked count as a continuous overnight sample is reading the hole as data.

---

## Overnight hole — eight windows `100315` through `100500` do not exist

**This is a defect to record, not to explain away.** Detector name on the owed line: `window_sequence_gap KXBTC15M-26SEP100515-15` (the first window *after* the hole).

Eight consecutive 15-minute windows are absent from every file this digest trusts: no `paper/` file, no `settlements/` file, no `ledger.json` entry or event, no `latest/journal.json` `windows[]` row.

| Stem | UTC window | EDT |
|---|---|---|
| `KXBTC15M-26SEP100315` | 07:00–07:15Z | 03:00–03:15 |
| `KXBTC15M-26SEP100330` | 07:15–07:30Z | 03:15–03:30 |
| `KXBTC15M-26SEP100345` | 07:30–07:45Z | 03:30–03:45 |
| `KXBTC15M-26SEP100400` | 07:45–08:00Z | 03:45–04:00 |
| `KXBTC15M-26SEP100415` | 08:00–08:15Z | 04:00–04:15 |
| `KXBTC15M-26SEP100430` | 08:15–08:30Z | 04:15–04:30 |
| `KXBTC15M-26SEP100445` | 08:30–08:45Z | 04:30–04:45 |
| `KXBTC15M-26SEP100500` | 08:45–09:00Z | 04:45–05:00 |

Adjacent windows **do** exist: `KXBTC15M-26SEP100300` (02:45–03:00 EDT; settle file `as_of` 2026-09-10T05:02:12-04:00, `settlement_ts` 2026-09-10T09:00:03Z) and `KXBTC15M-26SEP100515` (05:00–05:15 EDT; `as_of` 2026-09-10T05:16:39-04:00). Honer has none of the eight stems either. This is **not** the `072245` `--once` argparse collision.

**Do not backfill them. Do not infer what they would have been.** No Kalshi `result`, no paper fill, no pnl for those eight. Anyone who treats the locked count as a continuous overnight sample is reading the hole as data.

---

## Four residual kinds (do not collapse)

They are different states with different reasons and must not be collapsed into one "pending" bucket.

1. **Pending for want of a Kalshi `result`** — a true pending window. Kalshi has not spoken. The open paper book exists. The ticker rotates; read it off the generated figures, never freeze a name here.
2. **Missing paper join** — official result present (or once present on a tape that has since rolled off), no book on this tree. **`KXBTC15M-26SEP071500-00`.** There is no paper pnl here and none is invented. `SETTLE_PENDING` is the wrong banner.
3. **Published-only lineage B** — `KXBTC15M-26SEP071445-45`, `paper_win` `+1.67`. Kept as published history. Never re-derived here. Never added to lineage A.
4. **Unmeasured tape** — official result, no settle file and no paper position anywhere on this tree, because the local book seeded later (`ledger.json` `observation_seed` 15:42:37 EDT). `latest/journal.json` is a **rolling tape**, not an archive. A shrinking list means windows are being *forgotten*, not resolved. **Unmeasured is not lost and not losses.** Do not backfill them from a result. Do not count them in a denominator. This is a different state from the `072245` and `100315`–`100500` gaps: unmeasured windows existed on a tape; the gap stems never existed on this tree.

A window with no book has no pnl. That is a true statement, not a missing number. Do not write `0`.

---

## Pending vs missing paper join

| | **Pending for want of a Kalshi result** | **Missing paper join** |
|---|---|---|
| Kalshi has spoken? | No | **Yes** (or had, on a tape that may have rolled off) |
| Paper book | On this tree, open | **Not on this tree** |
| Paper pnl | Not yet | **Never on this tree** |
| Honest banner | `SETTLE_PENDING` | **Not** `SETTLE_PENDING` |
| Current standing instance | Read the generated pending ticker | `KXBTC15M-26SEP071500-00` |

`result=yes` does **not** license a paper win, a `+pnl`, a `0`, or a loss on this tree when there is no fill here to settle.

---

## Two paper lineages — flagged, not Softened, not merged

They are **separate books**, not two views of one book.

**Why they are split, cited to code.** `src/golf_offshoot/learning_lane_15m/paths.py` `artifact_root_15m()` prefers `/workspace/kalshi_15m_exports` when that parent exists, otherwise `golf-offshoot/data/learning_lane_15m`. On this Windows tree `/workspace` does not exist. Lineage B was written where the external root resolved. Same code, different machine, different book.

**Hard NOs:**

- Do **not** sum, net, average or reconcile the two bankrolls. There is no combined figure.
- Do **not** drop lineage B's published `paper_win` `+1.67` to make one clean story.
- Do **not** re-derive lineage B's `+1.67` from anything on this tree.
- Do **not** move `071445-45` or `071500-00` into `paper/ledger.json`, and do not backfill settle files for them.
- Either keep **one** readable lineage story or keep an **explicitly labeled dual** lineage. A silent merge fails the honesty gate.

---

## What must not be claimed

- **No edge.** Not established, not banked, not measured, not implied. A `settle_win` / `settle_loss` split is **not** a hit rate.
- **No track record.** Joined windows on one series are not a record, and they are not an unbroken sample.
- **Paper fills are not admits.** `lab_admits=false`.
- **`entry_edge=0` means the fill is mechanical, not smart.** `paper.py` hardcodes `entry_edge=0.0`. The model is the market.
- **No pnl anywhere a file does not record one.**
- **No fee-accurate pnl on the hub or in the generated figures.** Name the omission. Do not print a corrected total.
- **No golf transfer.** Nothing here retunes golf θ.
- **No expansion.** `KXBTC15M` only. Founder HOLD 2026-09-07.
- **Not live trading.** Trading NOT ARMED, no keys, no cash, no orders.
- **No dated record.** `records[]` is `[]`. This digest does not create one.

---

## A local export is not a publish

The runner exports locally. It does not commit or push. The public page reads `origin/master` only. Digestor does not publish.
