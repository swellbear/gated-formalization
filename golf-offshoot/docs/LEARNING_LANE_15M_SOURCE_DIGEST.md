# Digestor — 15m SOURCE honesty digest (living spine)

**Lane:** `learning_lane_15m` · series `KXBTC15M` only
**Role:** `digestor` — honesty owner. Never Soften / Harden / Kill / ADMIT.
**Admit?** N · **Soften?** N · **Trading ARMED?** N
**Evidence as-of:** 2026-09-08 05:48:54 EDT (`latest/journal.json` `generated_at`; wake `scanned_at` the same second)
**This is the overnight refresh.** The previous stamp was 2026-09-07 18:03:38 EDT and described none of the night. Prior Digestor docs on this lane were leftover-hook only until that first digest ([`LEARNING_LANE_15M.md`](LEARNING_LANE_15M.md) "Week-1 leftovers" item 1).

Sibling flag: [`LEARNING_LANE_15M_SOURCE_CONFLICT.md`](LEARNING_LANE_15M_SOURCE_CONFLICT.md) (the conflict flag; this file is its digest).
Operator park: [`LEARNING_LANE_15M_METHOD_PARK.md`](LEARNING_LANE_15M_METHOD_PARK.md).
Habit: [`docs/DIGESTOR_LIVING_SPINE_INDEX_HABIT.md`](../../docs/DIGESTOR_LIVING_SPINE_INDEX_HABIT.md).

---

## 0. Resume block (read this first if you are a later bot)

This digest is a **living spine**, not a dated record. Numbers below drift every ~15 minutes while the watch runs. To refresh instead of trusting the table:

```powershell
cd golf-offshoot
$env:PYTHONPATH = "src"
python -m golf_offshoot learn-15m          # human-readable tick
python -m golf_offshoot learn-15m --json   # same tick as JSON
```

The wake is a **reading aid, not truth**. It names which roles are owed and copies figures out of files; it never Softens, never ADMITs, and never invents a win, a lose or a pnl ([`LEARNING_LANE_15M.md`](LEARNING_LANE_15M.md) "Learning wake"; `src/golf_offshoot/learning_lane_15m/learn.py`).

Truth on disk, in the order this digest trusts it:

| Rank | File | What it is |
|------|------|-----------|
| 1 | `golf-offshoot/data/learning_lane_15m/settlements/*.json` | Official Kalshi join. `kalshi_result`, `settlement_ts`, `expiration_value`, `source_name`, `source_matched` |
| 2 | `golf-offshoot/data/learning_lane_15m/latest/journal.json` | Kalshi tape: per-window `status` + `result`. Wider than the settle files |
| 3 | `golf-offshoot/data/learning_lane_15m/paper/*.json` + `paper/ledger.json` | Local paper book — **lineage A** |
| 4 | `docs/observability-hub/data/manifest.json` | Published Pages export — **lineage B**. A separate book, not this tree's |
| aid | `golf-offshoot/data/learning_lane_15m/latest/learning_wake.json` | Wake fingerprint + `roles_owed`. Gitignored, derived, never authoritative |
| aid | `docs/observability-hub/data/charts/learning_lane_15m/paper_window_strip.png` | Illustrator's rendered board, drawn from ranks 1–4 |

**Path convention used in the tables below.** A window's stem is its `window_id` with `:` replaced by `-`
(`safe_artifact_stem`, `src/golf_offshoot/learning_lane_15m/paths.py`). Its settle file is
`golf-offshoot/data/learning_lane_15m/settlements/<stem>.json` and its paper book is
`golf-offshoot/data/learning_lane_15m/paper/<stem>.json`. Example stem:
`KXBTC15M-26SEP071545__2026-09-07T19-30-00Z__2026-09-07T19-45-00Z`.

---

## 1. SOURCE lock

Official settle for this lane is **Kalshi market `result`**, and only when the market is `finalized` / `determined`, matched to the event's documented `settlement_sources` — **CF Benchmarks**, CF index id pinned `BRTI`.

Cited to files:

- Every settle row on this tree carries `"source_name": "CF Benchmarks"` with `"source_matched": true`, plus `settlement_ts`, `settlement_value_dollars` and `expiration_value` — e.g. `settlements/KXBTC15M-26SEP071545__2026-09-07T19-30-00Z__2026-09-07T19-45-00Z.json`.
- The lock is written into [`LEARNING_LANE_15M.md`](LEARNING_LANE_15M.md) "Settle / field locks": `result` primary; `finalized`/`determined` + `result` → settle; `active`/`closed` without result → `SETTLE_PENDING`; `disputed`/`under-review` → `SETTLE_PENDING` banner.
- `latest/journal.json` carries `"cf_index_id": "BRTI"` and `"cfb_ws_average_role": "observe_only"`.

**Display prices are not settle evidence.** `yes_bid` / `yes_ask` / `last_price` / `volume` are display-only ([`LEARNING_LANE_15M.md`](LEARNING_LANE_15M.md), same section). They price a paper fill; they never decide a window.

**DIY CF Benchmarks average is observe-only.** Each settle row states the rule and then refuses to compute it as a settle: *"CRYPTO15M: official and final value is the simple average of 60 CF Benchmarks RTI prints in the last minute before expiration, rounded to 2 decimals. This adapter records the rule. It does not DIY that average as a settle."* A CFB websocket feed is observe/debug only and is a Hard NO as official settle without match-to-Kalshi-result.

---

## 2. What is locked

**Locked = an official Kalshi result in a settle file on this tree AND a paper book on this tree for the same `window_id`.** Fifty-six windows meet that bar as of this stamp. That count is **not** an unbroken run — see §3g.

Seed and book, from `golf-offshoot/data/learning_lane_15m/paper/ledger.json`:
`starting_bankroll` 100.00 → `bankroll` 93.86 · `betting_pnl` -6.14 · `deposits` 0.00 · `withdrawals` 0.00 · 114 entries (1 `observation_seed`, 57 `paper_fill`, 24 `settle_win`, 32 `settle_loss`) · 56 `events`.

57 paper books sit under `paper/KXBTC15M-*.json` (56 settled + the open `080600-00`). 57 settle files sit under `settlements/`. First locked ticker is still `KXBTC15M-26SEP071545-45`. Last locked ticker on this stamp is `KXBTC15M-26SEP080545-45` (`ledger.json` last `events[]` row: `settled_at` `2026-09-08T05:45:43.111529-04:00`, `kalshi_result=yes`, `pnl=+1.06`, `bankroll_after` 93.86).

The 56 recorded event pnls are the `ledger.json` `events[].tickets[].pnl` figures. They reconcile the `bankroll_before` → `bankroll_after` chain 100.00 → 93.86. Nothing here is recomputed or averaged. This digest does **not** reprint a 56-row scoreboard — that table would read as a track record, and §6 still forbids one.

Also locked: **the sequence has a hole.** `latest/journal.json` `windows[]` goes `KXBTC15M-26SEP072230-30` (`window_id` …`02:15:00Z`…`02:30:00Z`, `result` `no`) then `KXBTC15M-26SEP072300-00` (`window_id` …`02:45:00Z`…`03:00:00Z`, `result` `no`). There is no `072245` row. The same ticker is absent from `paper/` and `settlements/`. That is §3g, not a missing number.

---

## 3. What is residual

Four residual kinds. They are **different states with different reasons** and must not be collapsed into one "pending" bucket.

### 3a. Pending for want of a Kalshi result (a true pending window) — 1

`KXBTC15M-26SEP080600-00`, `window_id` `KXBTC15M-26SEP080600__2026-09-08T09:45:00Z__2026-09-08T10:00:00Z`.
`latest/journal.json` (first `windows[]` row): `status` `active`, `result` `""`. `digest_asof.json` names the same ticker under `pending`. A paper book exists at `paper/KXBTC15M-26SEP080600__2026-09-08T09-45-00Z__2026-09-08T10-00-00Z.json` and is not among the 56 `ledger.json` `events` (those are settled only).
**This one is honestly pending.** Kalshi has not spoken. The pending ticker rotates every ~15 minutes; do not freeze this name as if it were still open tomorrow.

### 3b. Missing paper join (official result present, no book on this tree) — 1

`KXBTC15M-26SEP071500-00`. This is the CoS checklist box-2 case. Full treatment in **§4**.

### 3c. Published-only, lineage B (kept as published history, never re-derived) — 1

`KXBTC15M-26SEP071445-45`. `docs/observability-hub/data/manifest.json` publishes it as `paper_win`, `paper settle_win pnl` `+1.67`, `paper observation after settle` `101.67`, official `result=yes`, `settlement_ts` `2026-09-07T18:45:05Z`, `expiration_value` `79148.63`.
On **this** tree there is no `settlements/KXBTC15M-26SEP071445__*.json` and no `paper/KXBTC15M-26SEP071445__*.json`. `latest/journal.json` independently carries `status` `finalized`, `result` `yes` for that ticker — the official result is corroborated by the tape here; the **+1.67 paper figure is not**, because the book that produced it is not here.
Kept, cited to lineage B, never added to lineage A. See §5.

### 3d. Unmeasured tape (official result, no settle file and no paper position anywhere on this tree)

The 18:03 digest named eight pre-seed windows (`071315-15` … `071530-30`). `latest/journal.json` is a **rolling tape**, not an archive — those tickers have since fallen off the front. The class remains: a window can be `finalized` on a tape we no longer hold, with no `settlements/*.json` and no `paper/*.json` on this tree, because the local book seeded at 15:42:37 EDT (`ledger.json` `led-3a16b2ba0e`).
**Unmeasured is not lost and not losses.** Do not backfill them from a result. Do not count them in a denominator. This is a different state from §3g: those windows existed on a tape; `072245` never existed on this tree.

### 3e. Stale public page (real files, unpublished export) — residual for `systems`

The public viewer still reads the last *published* snapshot: `generated_at` `2026-09-07T21:28:39-04:00` on `be04ebe`. That is eight hours behind this stamp. The runner exports locally and does not commit or push. A local `manifest.json` rewrite is not a publish. Digestor does not publish.

### 3f. Explicitly unmeasured, by construction

No calibration, no method, no selection quality is measured on this lane at all. Every fill is taken at the posted mark with zero recorded edge (see §4b and §6). There is no model to score yet, so there is nothing to be right or wrong about beyond the arithmetic in §2.

### 3g. Outage gap — window `KXBTC15M-26SEP072245` does not exist

**This is a defect to record, not to explain away.**

`KXBTC15M-26SEP072245` (the 22:30–22:45 EDT window, `window_id` would have been `KXBTC15M-26SEP072245__2026-09-08T02:30:00Z__2026-09-08T02:45:00Z`) is absent from every file this digest trusts:

- no `paper/KXBTC15M-26SEP072245__*.json`
- no `settlements/KXBTC15M-26SEP072245__*.json`
- no `ledger.json` entry or event
- no `latest/journal.json` `windows[]` row

Cause, already named by Founder and visible in the adjacent files: the 22:25–22:50 EDT outage from the `--once` argparse collision. The sequence is otherwise continuous: `072230-30` exists (journal `result` `no`, paper book and settle file present) and `072300-00` exists (journal `result` `no`, paper book and settle file present). The 15-minute hole between those `window_id`s is the missing window.

**Do not backfill it. Do not infer what it would have been.** No Kalshi `result`, no paper fill, no pnl. 56 locked books is not an unbroken run. Anyone who treats 56 as a continuous overnight sample is reading the hole as data.

---

## 4. The distinction Operator must fold and Systems must re-word

Two residual states look alike on a dashboard and are not alike.

| | **Pending for want of a Kalshi result** | **Missing paper join** |
|---|---|---|
| Kalshi has spoken? | No | **Yes** |
| Evidence | `settle_status` `SETTLE_PENDING`, `kalshi_result` `""`, `status` `active` in `settlements/<stem>.json` | `status` `finalized` + `result` in `latest/journal.json` |
| Paper book | On this tree, open | **Not on this tree** |
| Paper pnl | Not yet — the window has not resolved | **Never on this tree** — no book here to produce one |
| Honest banner | `SETTLE_PENDING` | **Not** `SETTLE_PENDING` |
| What clears it | Waiting for Kalshi | Nothing on this tree. Only the original book's tree could join it |
| Current instance | `KXBTC15M-26SEP080600-00` (§3a) | `KXBTC15M-26SEP071500-00` (§4a) |

### 4a. `KXBTC15M-26SEP071500-00` — the honest statement

The published manifest wording — *"SETTLE_PENDING until Kalshi result on this window"* (`docs/observability-hub/data/manifest.json`, `$.lanes[1].settle.residual[0].note`) — **is stale.** Kalshi has since spoken on that window.

Evidence, on this tree:

- `golf-offshoot/data/learning_lane_15m/latest/journal.json`, window `KXBTC15M-26SEP071500-00` (`window_id` `KXBTC15M-26SEP071500__2026-09-07T18:45:00Z__2026-09-07T19:00:00Z`): `"status": "finalized"`, `"result": "yes"`.
- No `golf-offshoot/data/learning_lane_15m/settlements/KXBTC15M-26SEP071500__*.json` exists.
- No `golf-offshoot/data/learning_lane_15m/paper/KXBTC15M-26SEP071500__*.json` exists, and `paper/ledger.json` has no entry or event for that `window_id`.
- `docs/observability-hub/data/manifest.json` `$.lanes[1].last_run.fields[15]` names it as that lineage's "Live paper fill" — so the book being referred to is lineage B's, not this tree's.

The honest statement:

> Kalshi settled that window `yes`. The paper book the published lineage names is **not on this Windows tree**, so there is no paper pnl here and none is invented. That is a **missing paper join**, not a pending window.

What follows from it, and what does not:

- `SETTLE_PENDING` is the wrong banner for this window. It says "Kalshi has not spoken," and Kalshi has.
- The right words are *official result present; paper book not on this tree; no paper pnl on this tree; none is invented.*
- `result=yes` does **not** license a paper win, a `+pnl`, a `0`, or a loss on this tree. There is no fill here to settle. A window with no book has no pnl — that is a true statement, not a missing number.
- This is not an ADMIT and not a Soften. Digestor states it and cites it; `operator` folds it to the leave-off and desk; `systems` re-words `manifest.json`. Digestor edits neither.

### 4b. Why this is the honesty gate and not bookkeeping

CoS box 2 fails precisely because the published surface tells a reader "we are still waiting" when the truth is "we already know the result and we never had a position." The first invites a later bot to fill in a pnl the moment the result appears. The second forecloses it. The wake reports the same distinction independently in `latest/learning_wake.json` `scan.paper_join_missing[0]` (`state`: *"official result present; paper book not on this tree"*) and holds Lab off with `lab_gate.why`: *"honesty gate has not passed -- not passed: `KXBTC15M-26SEP071500-00` honestly joined or pending with a true reason"*. Python may report that gate; it may not stamp it.

---

## 5. SOURCE CONFLICT — two paper lineages (flagged, not Softened, not merged)

Two paper books describe the same series over overlapping windows. They are **separate books**, not two views of one book.

| | **Lineage A — local paper book on this tree** | **Lineage B — published Pages export** |
|---|---|---|
| Source of truth | `golf-offshoot/data/learning_lane_15m/paper/*.json` + `paper/ledger.json` | `docs/observability-hub/data/manifest.json` `$.lanes[1]` |
| Seed | `starting_bankroll` 100.00, `observation_seed` at 2026-09-07T15:42:37-04:00 | implied 100.00 → published `paper observation after settle` 101.67 |
| Current book | `bankroll` 93.86 · `betting_pnl` -6.14 · 114 entries · 56 settled events | published snapshot still `generated_at` `2026-09-07T21:28:39-04:00`: `paper_win` 1 · `+1.67` |
| Windows | `071545` … `080545` locked, plus open `080600`; **hole at `072245` (§3g)** | `071445-45` settled `paper_win` +1.67; `071500-00` missing paper join |
| Overlap | none — the two window sets are disjoint | none |

**Why they are split, cited to code.** `src/golf_offshoot/learning_lane_15m/paths.py` resolves the lane's artifact root in `artifact_root_15m()`: it prefers `EXTERNAL_15M_ROOT = /workspace/kalshi_15m_exports` when that parent directory exists, and otherwise falls back to `REPO_15M_FALLBACK = golf-offshoot/data/learning_lane_15m`. On this Windows tree `/workspace` does not exist, so the root resolves to the repo fallback. Lineage B was written where the external root resolved. Same code, different machine, different book. This is a mundane, verifiable cause — not a mystery and not a defect to be papered over by addition.

**Hard NOs on this conflict:**

- Do **not** sum, net, average or reconcile the two bankrolls. 93.86 and 101.67 are two books. There is no combined figure, and `-6.14 + 1.67` is not a number that means anything.
- Do **not** drop lineage B's published `paper_win` `+1.67` to make one clean story. It is real published history on a real official result.
- Do **not** re-derive lineage B's `+1.67` from anything on this tree. The book is not here.
- Do **not** move `071445-45` or `071500-00` into `paper/ledger.json`, and do not backfill settle files for them.
- Either keep **one** readable lineage story or keep an **explicitly labeled dual** lineage. A silent merge fails the honesty gate ([`docs/agents/PROTOCOL.md`](../../docs/agents/PROTOCOL.md), "Honesty gate before Lab invents").

Currently the dual lineage is labeled in three places and summed in none: `manifest.json` keeps lineage-B figures in `$.lanes[1].paper_ledger` while `$.lanes[1].learning_status.rows` counts lineage A ("Paper books on this tree: 10"); the rendered board draws "PAPER LINEAGE A" and "PAPER LINEAGE B" as separate blocks with a *"never added together"* footnote; and this digest is the written spine. A later bot reading `$.lanes[1].paper_ledger` should not "fix" it against `ledger.json` — those blocks describe different books.

---

## 6. What must not be claimed

- **No edge.** Not established, not banked, not measured, not implied. There is no edge claim available from fifty-six mechanical fills, and the 24/32 `settle_win`/`settle_loss` split in `ledger.json` is **not** a hit rate.
- **No track record.** Fifty-six joined windows on one series overnight is still not a record, and it is not an unbroken sample — §3g sits in the middle. That split measures nothing about a method.
- **Paper fills are not admits.** `lab_admits=false`. A fill is an observation, not a claim, and never a Softened admit ([`docs/OPERATOR_SOFTEN_FOLD_HABIT.md`](../../docs/OPERATOR_SOFTEN_FOLD_HABIT.md); [`templates/SOFTEN_PR_HONESTY_CHECKLIST.md`](../../templates/SOFTEN_PR_HONESTY_CHECKLIST.md)).
- **`entry_edge=0` means the fill is mechanical, not smart.** `src/golf_offshoot/learning_lane_15m/paper.py` hardcodes `entry_edge=0.0` on the position and `edge_w=0.0` / `posted_edge=0.0` on the movement, and takes the fill at `paper_mark` (public mid, else `yes_ask`). Every book on disk shows it — e.g. `paper/KXBTC15M-26SEP071745__2026-09-07T21-30-00Z__2026-09-07T21-45-00Z.json` `movements[0]`: `edge_w` 0.0, `posted_edge` 0.0, `model_win` 0.515, `decimal_odds` 1.9417, `reason_plain` *"Paper observation fill at the public Kalshi mid/last mark."* The book buys YES at the posted mark on every candidate window. `model_win` equals the mark; the model is the market. Nothing is being selected, so the win/lose split measures the market's own noise, not a method.
- **No pnl anywhere a file does not record one.** A window with no book says so. It does not say `0`.
- **No golf transfer.** Golf WC1 FAIL / Ill / calibration and golf θ belong to the golf lane and say nothing here; nothing here retunes golf θ ([`LEARNING_LANE_15M.md`](LEARNING_LANE_15M.md) "Locked posture"; `manifest.json` `$.lanes[1].lane_scope_note`).
- **No expansion.** `KXBTC15M` only. Founder HOLD 2026-09-07 until this loop is honest.
- **Not live trading.** Trading NOT ARMED, no Kalshi keys, no cash scopes, no order placement, `never_auto_bet: true` and `paper_observation_only: true` on every artifact.
- **No dated record.** This lane has none: `manifest.json` `$.lanes[1].records` is `[]` with `records_note` *"No weekly operating record exists for this lane."* This digest does not create one.

---

## 7. Spine index — where each claim lives

| Claim | File |
|---|---|
| SOURCE lock (`result` + CF Benchmarks `BRTI`) | `settlements/*.json` rows; [`LEARNING_LANE_15M.md`](LEARNING_LANE_15M.md) "Settle / field locks" |
| Official result per window | `settlements/<stem>.json`; corroborated by `latest/journal.json` |
| Paper fill mark and zero edge | `paper/<stem>.json` `movements[]`; `src/golf_offshoot/learning_lane_15m/paper.py` |
| Paper pnl and the 100.00 → 93.86 chain | `paper/ledger.json` `entries` + `events`; `paper/<stem>.json` `settlement_pnl` |
| True pending window | `latest/journal.json` first row `080600-00`; rotates |
| Missing paper join (§4) | absence of `settlements/`/`paper/` `071500` files; official `result` last seen on an earlier tape |
| Outage gap `072245` (§3g) | absence of that ticker in `paper/`, `settlements/`, `ledger.json`, and `latest/journal.json` `windows[]` |
| Lineage B figures | `docs/observability-hub/data/manifest.json` `$.lanes[1]` |
| Why the lineages are split | `src/golf_offshoot/learning_lane_15m/paths.py` `artifact_root_15m()` |
| Roles owed / honesty gate state | `data/learning_lane_15m/latest/learning_wake.json` (`roles_owed`, `lab_gate`) — derived, not truth |
| Rendered board | `docs/observability-hub/data/charts/learning_lane_15m/paper_window_strip.png` |
| Conflict flag | [`LEARNING_LANE_15M_SOURCE_CONFLICT.md`](LEARNING_LANE_15M_SOURCE_CONFLICT.md) |
| Method leftovers park | [`LEARNING_LANE_15M_METHOD_PARK.md`](LEARNING_LANE_15M_METHOD_PARK.md) |

---

## 8. Handoff — what each role owes next

Digestor's part is done for this tick. Digestor does not do any of the following.

- **`operator`** — fold §3g into the leave-off and desk as committed truth: `KXBTC15M-26SEP072245` does not exist; cause is the 22:25–22:50 `--once` argparse outage; do not backfill; 56 locked books is not an unbroken run. Keep §4a (`071500-00` missing paper join). Keep the two lineages separate. Do not read §2 as edge. Any ADMIT is Operator's alone.
- **`systems`** — publish. The public page is still `generated_at` `2026-09-07T21:28:39-04:00`. Local export is not a publish. Keep the published `paper_win` `+1.67`. Never invent a pending. Never sum the lineages. Never invent `072245`.
- **`validator`** — `python docs/observability-hub/validate_hub.py --strict` on the exact bytes about to publish.
- **`lab`** — stays idle on new PROPOSED work. PROPOSED 01 is already RUN-ONLY. This digest is not an ADMIT and not a second residual.

---

## 9. Change log

| When | Who | What |
|---|---|---|
| 2026-09-08 05:50 EDT | `digestor` | Overnight refresh. Lineage A is 100.00 → 93.86 (`betting_pnl` -6.14, 56 settled events, 57 paper books). Named §3g: `KXBTC15M-26SEP072245` does not exist (22:25–22:50 `--once` argparse outage). No backfill, no inferred result or pnl. 56 is not an unbroken run. Public page still 21:28:39. No Soften, no ADMIT, no merge. |
| 2026-09-07 18:03 EDT | `digestor` | First real SOURCE honesty digest for `learning_lane_15m`. Locked 10 official-settle + paper joins with settle files named; separated four residual kinds; wrote the pending-vs-missing-paper-join distinction for `KXBTC15M-26SEP071500-00` (CoS box 2); flagged lineage A vs lineage B and cited `paths.py` for why they are split. No Soften, no ADMIT, no merge, no invented pnl. |
