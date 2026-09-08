# Digestor — 15m SOURCE honesty digest (living spine)

**Lane:** `learning_lane_15m` · series `KXBTC15M` only
**Role:** `digestor` — honesty owner. Never Soften / Harden / Kill / ADMIT.
**Admit?** N · **Soften?** N · **Trading ARMED?** N
**Evidence as-of:** 2026-09-07 18:03:38 EDT (wake scan `scanned_at`, `data/learning_lane_15m/latest/learning_wake.json`)
**First real digest for this lane.** Prior Digestor docs on this lane were leftover-hook only ([`LEARNING_LANE_15M.md`](LEARNING_LANE_15M.md) "Week-1 leftovers" item 1, and the `digestor_source_hook` string carried in every `settlements/*.json`).

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

**Locked = an official Kalshi result in a settle file on this tree AND a paper book on this tree for the same `window_id`.** Ten windows meet that bar.

Seed and book, from `golf-offshoot/data/learning_lane_15m/paper/ledger.json`:
`starting_bankroll` 100.00 → `bankroll` 96.59 · `betting_pnl` -3.41 · `deposits` 0.00 · `withdrawals` 0.00 · 22 entries (1 `observation_seed`, 11 `paper_fill`, 10 settle) · 10 `events`.

| Window ticker | Kalshi `result` | `expiration_value` | Paper mark on fill | Paper pnl on file | Settle file stem (see §0 convention) |
|---|---|---|---|---|---|
| `KXBTC15M-26SEP071545-45` | yes | 79339.56 | 0.9835 | +0.02 | `KXBTC15M-26SEP071545__2026-09-07T19-30-00Z__2026-09-07T19-45-00Z` |
| `KXBTC15M-26SEP071600-00` | yes | 79342.28 | 0.705 | +0.42 | `KXBTC15M-26SEP071600__2026-09-07T19-45-00Z__2026-09-07T20-00-00Z` |
| `KXBTC15M-26SEP071615-15` | no | 79226.35 | 0.635 | -1.00 | `KXBTC15M-26SEP071615__2026-09-07T20-00-00Z__2026-09-07T20-15-00Z` |
| `KXBTC15M-26SEP071630-30` | no | 79200.82 | 0.465 | -1.00 | `KXBTC15M-26SEP071630__2026-09-07T20-15-00Z__2026-09-07T20-30-00Z` |
| `KXBTC15M-26SEP071645-45` | no | 79183.47 | 0.605 | -1.00 | `KXBTC15M-26SEP071645__2026-09-07T20-30-00Z__2026-09-07T20-45-00Z` |
| `KXBTC15M-26SEP071700-00` | yes | 79218.12 | 0.385 | +1.60 | `KXBTC15M-26SEP071700__2026-09-07T20-45-00Z__2026-09-07T21-00-00Z` |
| `KXBTC15M-26SEP071715-15` | yes | 79239.28 | 0.645 | +0.55 | `KXBTC15M-26SEP071715__2026-09-07T21-00-00Z__2026-09-07T21-15-00Z` |
| `KXBTC15M-26SEP071730-30` | no | 79217.61 | 0.335 | -1.00 | `KXBTC15M-26SEP071730__2026-09-07T21-15-00Z__2026-09-07T21-30-00Z` |
| `KXBTC15M-26SEP071745-45` | no | 79180.33 | 0.515 | -1.00 | `KXBTC15M-26SEP071745__2026-09-07T21-30-00Z__2026-09-07T21-45-00Z` |
| `KXBTC15M-26SEP071800-00` | no | 79169.70 | 0.495 | -1.00 | `KXBTC15M-26SEP071800__2026-09-07T21-45-00Z__2026-09-07T22-00-00Z` |

Per-row provenance: `result` / `expiration_value` / `settlement_ts` from the named `settlements/<stem>.json`; paper mark from the matching `paper/<stem>.json` `movements[].amount_plain` and its `ledger.json` `paper_fill` note; paper pnl from `paper/<stem>.json` `settlement_pnl` and the matching `ledger.json` `settle_win` / `settle_loss` entry. The ten recorded pnl figures sum to `betting_pnl` -3.41 and reconcile the `bankroll_before` → `bankroll_after` chain 100.00 → 96.59 across `ledger.json` `events`. Nothing here is recomputed or averaged.

Also locked: **the tape is wider than the joins.** `latest/journal.json` holds 21 windows (`KXBTC15M-26SEP071315-15` … `KXBTC15M-26SEP071815-15`), 20 of which carry an official `result`. Only 11 of those 21 have a settle file on this tree, and only 10 have a paper book. The gap is §3, not a hole to be filled by inference.

---

## 3. What is residual

Four residual kinds. They are **different states with different reasons** and must not be collapsed into one "pending" bucket.

### 3a. Pending for want of a Kalshi result (a true pending window) — 1

`KXBTC15M-26SEP071815-15`, `window_id` `KXBTC15M-26SEP071815__2026-09-07T22:00:00Z__2026-09-07T22:15:00Z`.
File: `settlements/KXBTC15M-26SEP071815__2026-09-07T22-00-00Z__2026-09-07T22-15-00Z.json` — `settle_status` `SETTLE_PENDING`, `kalshi_result` `""`, `status` `active`, `banner` `SETTLE_PENDING`, `won` null, `pnl` null. Reason on file: *"SETTLE_PENDING: can_close_early is set. Wait for the Kalshi result. Do not invent from close_time or a DIY CFB average."*
Its paper book `paper/KXBTC15M-26SEP071815__2026-09-07T22-00-00Z__2026-09-07T22-15-00Z.json` is open (`settled_at` absent, `settlement_pnl` null), fill mark 0.415 (`shadow/advises.jsonl` last row, `posted_yes` 0.415). `latest/journal.json` agrees: `status` `active`, `result` `""`.
**This one is honestly pending.** Kalshi has not spoken. Nothing is owed but waiting.

### 3b. Missing paper join (official result present, no book on this tree) — 1

`KXBTC15M-26SEP071500-00`. This is the CoS checklist box-2 case. Full treatment in **§4**.

### 3c. Published-only, lineage B (kept as published history, never re-derived) — 1

`KXBTC15M-26SEP071445-45`. `docs/observability-hub/data/manifest.json` publishes it as `paper_win`, `paper settle_win pnl` `+1.67`, `paper observation after settle` `101.67`, official `result=yes`, `settlement_ts` `2026-09-07T18:45:05Z`, `expiration_value` `79148.63`.
On **this** tree there is no `settlements/KXBTC15M-26SEP071445__*.json` and no `paper/KXBTC15M-26SEP071445__*.json`. `latest/journal.json` independently carries `status` `finalized`, `result` `yes` for that ticker — the official result is corroborated by the tape here; the **+1.67 paper figure is not**, because the book that produced it is not here.
Kept, cited to lineage B, never added to lineage A. See §5.

### 3d. Unmeasured tape (official result, no settle file and no paper position anywhere on this tree) — 8

`KXBTC15M-26SEP071315-15`, `071330-30`, `071345-45`, `071400-00`, `071415-15`, `071430-30`, `071515-15`, `071530-30`.
Each is `finalized` with a `result` in `latest/journal.json`. None has a `settlements/*.json` file, none has a `paper/*.json` book, none appears in `paper/ledger.json`. The watch started at 15:42:37 EDT (`ledger.json` `observation_seed` entry `led-3a16b2ba0e`), so these windows closed before the local book existed.
**They are unmeasured, not lost and not losses.** They carry no paper pnl and none may be inferred from their result.

### 3e. Stale display wording (real files, stale words) — residual for `systems` and `illustrator`

Not a data problem; a wording problem. Named here so the honest state is written down once and the right role fixes its own surface.

- `docs/observability-hub/data/manifest.json` still carries the stale pending wording for the §4 case at `$.lanes[1].settle.headline`, `$.lanes[1].settle.residual[0].note`, `$.lanes[1].last_run.headline` and `$.lanes[1].last_run.notes[2]`. The same file **already** states the honest distinction at `$.lanes[1].settle.counts[5].note`, `$.lanes[1].settle.notes[3]` and `$.lanes[1].learning_status.rows[4].note`. Both wordings are in one file; the stale one is the one Founder reads first. `manifest.json` is Systems' file — Digestor does not edit it.
- `docs/observability-hub/data/charts/learning_lane_15m/paper_window_strip.png` is a real render from real files and labels lineage A and lineage B apart with a never-summed note. Two staleness facts: its own header stamps `journal generated_at=2026-09-07T17:10:08`, so it shows lineage A at 7 windows and 100.00 → 99.04 rather than the current 10 windows and 100.00 → 96.59; and its lineage-B row for `KXBTC15M-26SEP071500-00` prints `PAPER SETTLE = SETTLE_PENDING` (with `PAPER PNL = no pnl on disk` and `KALSHI RESULT = YES`), carrying the same stale word. The board invents nothing. It is behind.
- `docs/agents/DESK.md` thread line 2026-09-07 17:12 ET says the local book is "100.00 → 99.04". True when written, stale now (`paper/ledger.json` `bankroll` 96.59). Desk history is not rewritten; the current figure lives here.

### 3f. Explicitly unmeasured, by construction

No calibration, no method, no selection quality is measured on this lane at all. Every fill is taken at the posted mark with zero recorded edge (see §4b and §6). There is no model to score yet, so there is nothing to be right or wrong about beyond the arithmetic in §2.

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
| Current instance | `KXBTC15M-26SEP071815-15` (§3a) | `KXBTC15M-26SEP071500-00` (§4a) |

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
| Current book | `bankroll` 96.59 · `betting_pnl` -3.41 · 22 entries · 10 settled events | `Ledger entries` 4 · `Open books` 1 · `Settled books` 1 · `paper_win` 1 |
| Windows | `071545` … `071815` (11 books, 10 settled + 1 open) | `071445-45` settled `paper_win` +1.67; `071500-00` named as its live fill |
| Overlap | none — the two window sets are disjoint | none |

**Why they are split, cited to code.** `src/golf_offshoot/learning_lane_15m/paths.py` resolves the lane's artifact root in `artifact_root_15m()`: it prefers `EXTERNAL_15M_ROOT = /workspace/kalshi_15m_exports` when that parent directory exists, and otherwise falls back to `REPO_15M_FALLBACK = golf-offshoot/data/learning_lane_15m`. On this Windows tree `/workspace` does not exist, so the root resolves to the repo fallback. Lineage B was written where the external root resolved. Same code, different machine, different book. This is a mundane, verifiable cause — not a mystery and not a defect to be papered over by addition.

**Hard NOs on this conflict:**

- Do **not** sum, net, average or reconcile the two bankrolls. 96.59 and 101.67 are two books. There is no combined figure, and `-3.41 + 1.67` is not a number that means anything.
- Do **not** drop lineage B's published `paper_win` `+1.67` to make one clean story. It is real published history on a real official result.
- Do **not** re-derive lineage B's `+1.67` from anything on this tree. The book is not here.
- Do **not** move `071445-45` or `071500-00` into `paper/ledger.json`, and do not backfill settle files for them.
- Either keep **one** readable lineage story or keep an **explicitly labeled dual** lineage. A silent merge fails the honesty gate ([`docs/agents/PROTOCOL.md`](../../docs/agents/PROTOCOL.md), "Honesty gate before Lab invents").

Currently the dual lineage is labeled in three places and summed in none: `manifest.json` keeps lineage-B figures in `$.lanes[1].paper_ledger` while `$.lanes[1].learning_status.rows` counts lineage A ("Paper books on this tree: 10"); the rendered board draws "PAPER LINEAGE A" and "PAPER LINEAGE B" as separate blocks with a *"never added together"* footnote; and this digest is the written spine. A later bot reading `$.lanes[1].paper_ledger` should not "fix" it against `ledger.json` — those blocks describe different books.

---

## 6. What must not be claimed

- **No edge.** Not established, not banked, not measured, not implied. There is no edge claim available from ten mechanical fills.
- **No track record.** Ten joined windows over roughly two hours on one series is not a record. Four of the ten recorded a positive paper pnl and six recorded a negative one (§2), and that split is **not** a hit rate to elevate — see the next bullet for why it measures nothing.
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
| Paper pnl and the 100.00 → 96.59 chain | `paper/ledger.json` `entries` + `events`; `paper/<stem>.json` `settlement_pnl` |
| True pending window | `settlements/KXBTC15M-26SEP071815__*.json`; `latest/journal.json` |
| Missing paper join (§4) | `latest/journal.json` (result) + absence of `settlements/`/`paper/` `071500` files |
| Lineage B figures | `docs/observability-hub/data/manifest.json` `$.lanes[1]` |
| Why the lineages are split | `src/golf_offshoot/learning_lane_15m/paths.py` `artifact_root_15m()` |
| Roles owed / honesty gate state | `data/learning_lane_15m/latest/learning_wake.json` (`roles_owed`, `lab_gate`) — derived, not truth |
| Rendered board | `docs/observability-hub/data/charts/learning_lane_15m/paper_window_strip.png` |
| Conflict flag | [`LEARNING_LANE_15M_SOURCE_CONFLICT.md`](LEARNING_LANE_15M_SOURCE_CONFLICT.md) |
| Method leftovers park | [`LEARNING_LANE_15M_METHOD_PARK.md`](LEARNING_LANE_15M_METHOD_PARK.md) |

---

## 8. Handoff — what each role owes next

Digestor's part is done for this tick. Digestor does not do any of the following.

- **`operator`** — fold §4a into the leave-off and desk as committed truth: `071500-00` is a missing paper join, not a pending window. Soften/park only what §2–§3 support. Keep the two lineages separate. Do not read §2 as edge. Any ADMIT is Operator's alone.
- **`systems`** — re-word `manifest.json` at `$.lanes[1].settle.headline`, `$.lanes[1].settle.residual[0].note`, `$.lanes[1].last_run.headline`, `$.lanes[1].last_run.notes[2]` off "SETTLE_PENDING until Kalshi result" and onto the §4a wording, which the same file already uses at `$.lanes[1].settle.counts[5].note`. Keep the published `paper_win` `+1.67`. Never invent a pending. Never sum the lineages. `071815-15` remains a genuine `SETTLE_PENDING`.
- **`validator`** — `python docs/observability-hub/validate_hub.py --strict` after Systems.
- **`illustrator`** — a later tick may re-render `paper_window_strip.png` from current files (§3e: lineage A now 10 windows and 100.00 → 96.59; the `071500-00` PAPER SETTLE cell should carry the §4a wording, not `SETTLE_PENDING`). Real files only, or leave the prior real board.
- **`lab`** — stays idle. `lab_gate.honesty_gate_passed` is false until CoS re-stamps box 2 all-PASS **and** Operator posts a residual explicitly. This digest is not that stamp and not that residual.

---

## 9. Change log

| When | Who | What |
|---|---|---|
| 2026-09-07 18:03 EDT | `digestor` | First real SOURCE honesty digest for `learning_lane_15m`. Locked 10 official-settle + paper joins with settle files named; separated four residual kinds; wrote the pending-vs-missing-paper-join distinction for `KXBTC15M-26SEP071500-00` (CoS box 2); flagged lineage A vs lineage B and cited `paths.py` for why they are split. No Soften, no ADMIT, no merge, no invented pnl. |
