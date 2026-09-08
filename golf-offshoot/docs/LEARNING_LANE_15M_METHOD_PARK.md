# Operator — 15m method leftovers PARK (not Softened)

**Track:** `learning_lane_15m` · series `KXBTC15M` only
**Updated:** 2026-09-07 21:13 EDT (Operator PARK of Lab PROPOSED 01 — not an ADMIT)
**State:** **PARK.** No dated ADMIT on this lane. No Soften. No edge claim. `lab_admits=false` · Trading **NOT ARMED**
**Golf idle:** stays **ON** (WC3+ only on a new settled week). This file does not clear it, does not touch golf θ, and does not rewrite `phase1_dryrun/OPERATOR_STATUS_STAMP.md`.

Digest this park folds: [`LEARNING_LANE_15M_SOURCE_DIGEST.md`](LEARNING_LANE_15M_SOURCE_DIGEST.md) (living spine, every claim cited to a file).
Conflict flag: [`LEARNING_LANE_15M_SOURCE_CONFLICT.md`](LEARNING_LANE_15M_SOURCE_CONFLICT.md) — **not** Softened away, **not** merged.

## How to read this file

Every row below is **parked**, not admitted and not rejected. Each carries an explicit **trigger**: the thing that would have to become true for the row to reopen. Until that trigger fires the row stays parked and no one fills it in by inference.

A park is not a promise that the trigger will fire. Three of these triggers cannot fire on this tree at all, and one is Founder's alone.

Numbers on this lane move while the watch runs. This park names **states and triggers**, not figures; live figures live in the digest and on disk (`data/learning_lane_15m/`).

---

## Parked residuals

### 1. True pending window — pending for want of a Kalshi `result`

| | |
|---|---|
| **Instance** | **Do not read a ticker off this row.** It rotates faster than this file can be edited: the digest named `071815-15` at 18:03 EDT, it was `071830-30` at 18:20, and `071845-45` at 18:32. There is normally exactly **one** open window at a time |
| **Parked state** | Genuinely `SETTLE_PENDING`. Kalshi has not spoken. The open window's paper book on this tree exists with `settlement_pnl` null |
| **Evidence** | `data/learning_lane_15m/settlements/<open stem>.json` — `settle_status` `SETTLE_PENDING`, `kalshi_result` `""`, `status` `active`, `won` null, `pnl` null, note *"can_close_early is set. Wait for the Kalshi result. Do not invent from close_time or a DIY CFB average."* |
| **Trigger to reopen** | Kalshi publishes a `result` on that window with `status` `finalized` / `determined`, matched to CF Benchmarks `BRTI`. Then `lane-15m` joins it and the row closes on its own |
| **Not a trigger** | `close_time` passing · a DIY CFB 60s average · a display price (`yes_bid` / `yes_ask` / `last_price`) |

This row parks a **state**, not a ticker. A later bot reads the current pending window off `python -m golf_offshoot learn-15m`, never off this file. A ticker that has left this row did not fail — it settled, and its pnl is on its own book.

### 2. `KXBTC15M-26SEP071500-00` — missing paper join, **not** a pending window

| | |
|---|---|
| **Parked state** | Kalshi settled this window `yes`. The paper book the published lineage names is **not on this tree**, so there is no paper pnl here and none is invented. That is a *missing paper join* |
| **Evidence** | `data/learning_lane_15m/latest/journal.json` — `status` `finalized`, `result` `yes`. No `settlements/KXBTC15M-26SEP071500__*.json` and no `paper/KXBTC15M-26SEP071500__*.json` exist; `paper/ledger.json` has no entry or event for that `window_id`. Full statement: digest §4a |
| **Trigger to reopen** | The **original book** — the tree where `artifact_root_15m()` resolved to `/workspace/kalshi_15m_exports` — is recovered onto this tree, producing a real `paper/KXBTC15M-26SEP071500__*.json` |
| **Not a trigger** | The official `result` already being known. It is known, and it still licenses nothing here |

`result=yes` does **not** license a paper win, a `+pnl`, a `0`, or a loss on this tree. There is no fill here to settle. A window with no book has no pnl — a true statement, not a missing number.

`SETTLE_PENDING` is the **wrong banner** for this window; it says "Kalshi has not spoken," and Kalshi has. The honest words are *official result present; paper book not on this tree; no paper pnl on this tree; none is invented.* Re-wording the published surface is row 5 (`systems`), not this file.

### 3. `KXBTC15M-26SEP071445-45` — published-only lineage B, kept, never merged

| | |
|---|---|
| **Parked state** | Published Pages history: `paper_win`, paper pnl `+1.67`, official `result=yes`. **Kept.** Cited to lineage B (`docs/observability-hub/data/manifest.json` `$.lanes[1]`). Never added to lineage A |
| **Evidence** | The official result is independently corroborated on this tree by `latest/journal.json` (`status` `finalized`, `result` `yes`). The **`+1.67` is not** — the book that produced it is not here. No `settlements/` or `paper/` `071445` file exists |
| **Trigger to reopen** | The lineage-B book is recovered onto this tree, so `+1.67` can be read off a file **here** instead of being carried as published history |
| **Even then** | It joins under **lineage B**. It is never summed into lineage A's bankroll. Recovery would end the *split*, not authorize a *merge* |

**Never:** re-derive `+1.67` from anything on this tree · drop it to make one clean story · move `071445-45` or `071500-00` into `paper/ledger.json` · backfill settle files for either.

**Never sum the two books.** Lineage A (local, seed 100.00) and lineage B (published) are two books, not two views of one book. There is no combined bankroll, and adding their pnl figures produces a number that means nothing. Cause is mundane and cited to code: `src/golf_offshoot/learning_lane_15m/paths.py` `artifact_root_15m()` prefers `/workspace/kalshi_15m_exports` and falls back to the repo root when `/workspace` is absent, as it is on this Windows tree. Same code, different machine, different book.

### 4. Unmeasured tape — official result, no book anywhere on this tree

| | |
|---|---|
| **Windows** | The digest named 8 at 18:03 EDT: `071315-15`, `071330-30`, `071345-45`, `071400-00`, `071415-15`, `071430-30`, `071515-15`, `071530-30`. **`071315-15` has since rolled off the tape** — see the note below — leaving 7 still visible in `latest/journal.json` as of 18:28 EDT |
| **Parked state** | **Unmeasured.** Each is `finalized` with a `result` in `latest/journal.json`. None has a settle file, none has a paper book, none appears in `paper/ledger.json`. They carry no paper pnl and none may be inferred from their result |
| **Why** | The local watch seeded at 15:42:37 EDT (`ledger.json` `observation_seed`). These windows closed before the local book existed |
| **Trigger to reopen** | **None available on this tree.** Only a recovered book from the machine that was running at the time could join them. Absent that, they stay unmeasured permanently |
| **Not a trigger** | Having the official result. An official result is not a position |

**`latest/journal.json` is a rolling tape, not an archive.** It holds 21 windows; as new ones open, the oldest fall off. `KXBTC15M-26SEP071315-15` was on it when the digest was written and is not on it now. So this set **shrinks from the front over time**, and a window that rolls off leaves no trace on this tree at all. That makes the row's trigger harder to fire, never easier — a later bot must not read a shrinking list as windows being resolved.

Unmeasured is **not** lost and **not** losses. Do not backfill these from their results, and do not count them in any denominator.

### 5. Stale display wording — real files, stale words

Not a data problem. Named once here so the honest state is written down and each surface is fixed by its own owner. **Operator does not edit either surface.**

| Owner | Surface | Parked state | Trigger to reopen |
|---|---|---|---|
| `systems` | `docs/observability-hub/data/manifest.json` at `$.lanes[1].settle.headline`, `$.lanes[1].settle.residual[0].note`, `$.lanes[1].last_run.headline`, `$.lanes[1].last_run.notes[2]` | Still carries *"SETTLE_PENDING until Kalshi result"* for the row-2 case. The **same file already** states the honest distinction at `$.lanes[1].settle.counts[5].note`, `$.lanes[1].settle.notes[3]` and `$.lanes[1].learning_status.rows[4].note`. Both wordings are in one file; the stale one is the one Founder reads first | `systems` re-words those four paths onto the row-2 wording, keeps the published `paper_win` `+1.67`, invents no pending, sums no lineages, and leaves the true pending window (row 1) as a genuine `SETTLE_PENDING`. Then `validator` runs `--strict` |
| `illustrator` | `docs/observability-hub/data/charts/learning_lane_15m/paper_window_strip.png` | A **real** render from real files that labels lineage A and lineage B apart with a *never summed* note. It invents nothing — it is **behind.** Its header stamps `journal generated_at=2026-09-07T17:10:08`, so lineage A shows fewer windows and an older bankroll than the live ledger; and its `071500-00` cell prints `PAPER SETTLE = SETTLE_PENDING`, carrying the same stale word | A later tick re-renders from **current** files only: lineage A at its live window count and bankroll, and the `071500-00` cell carrying the row-2 wording instead of `SETTLE_PENDING`. If real files cannot drive it, leave the prior real board standing |

Desk history is **not** rewritten. The 2026-09-07 17:12 ET thread line's "100.00 → 99.04" was true when written; the current figure lives in the digest and on disk.

### 6. 15m weekly honesty rollup

| | |
|---|---|
| **Parked state** | **PROPOSED / PARK.** No dated ADMIT. This lane has no weekly operating record — `manifest.json` `$.lanes[1].records` is `[]` with `records_note` *"No weekly operating record exists for this lane."* Nothing here creates one |
| **Trigger to reopen** | All three: (a) the CoS honesty checklist re-stamps **all-PASS**; (b) a full settled week exists on **one** readable lineage; (c) a fresh Founder **GO that names this rollup as the next invent** |
| **Not a trigger** | Enough windows accumulating · restating park facts · a tick that looks tidy |

Habit F (idle latch): idle clears only on a Founder GO that **names the next invent**. Restating park facts is not a GO.

### 7. Expand past `KXBTC15M` — Founder **HOLD**

| | |
|---|---|
| **Parked state** | **HOLD**, set by Founder 2026-09-07: no series other than `KXBTC15M` until this loop is honest |
| **Trigger to reopen** | **Founder lifts it.** That is the only trigger |
| **Who may lift it** | Founder. **Not** Operator, not CoS, not Lab, not a later bot reading a tidy tick |

This fold does **not** lift the HOLD and is not evidence toward lifting it.

### 8. Lab — new named horse on this lane

| | |
|---|---|
| **Parked state** | **Named horse not opened.** The one cheap paper-only PROPOSED slot opened after the honesty gate and is **PARKED** as row 10 — not a named horse, not a board, not an admit |
| **Trigger to reopen** | Both already fired (CoS all-PASS 19:58 ET **and** Operator residual on desk). Lab brought **one** cheap paper-only PROPOSED — it is **PARKED** as row 10, **not** admitted. A **second** PROPOSED is not owed |
| **Under golf idle** | A new **named-horse** invent (WC3+ / new board) arriving without a fresh Founder GO that names it is still an **idle-breach REJECT**, not a Soften. Row 10 is not that invent |

### 9. Zero-edge fills — the observation gap (residual, not a board)

| | |
|---|---|
| **Parked state** | `src/golf_offshoot/learning_lane_15m/paper.py` hardcodes `entry_edge=0.0` on the position and `edge_w=0.0` / `posted_edge=0.0` on the movement, and takes every fill at `paper_mark` (public mid, else `yes_ask`). `model_win` equals the mark — **the model is the market.** Nothing is being selected, so the win/lose split across settled windows measures the market's own noise, not a method |
| **Why it is parked** | It is the honest reason this lane cannot produce an edge claim no matter how many windows join. It is a **residual**, stated so a later bot does not read the settled table as a hit rate |
| **Trigger to reopen** | Row 8's gate opened; Lab brought one cheap paper-only test against this residual. That candidate is **PARKED** as row 10 — **not** admitted, **not** scheduled |
| **Not opened here** | This row stays the residual, not the test. The test design lives in [`LEARNING_LANE_15M_LAB_PROPOSED_01.md`](LEARNING_LANE_15M_LAB_PROPOSED_01.md) and the Operator decision is row 10 |

### 10. Lab PROPOSED 01 — charge the documented fee, read the hurdle (**PARK**, not ADMIT)

Candidate: [`LEARNING_LANE_15M_LAB_PROPOSED_01.md`](LEARNING_LANE_15M_LAB_PROPOSED_01.md) (Lab, 2026-09-07 20:05 EDT). Spine this folds against: digest §3f / §6 and park row 9.

| | |
|---|---|
| **Parked state** | Lab PROPOSED a cheap paper-only **arithmetic** test: charge the documented `fee_type=quadratic × fee_multiplier=1` against settled books already on disk and read the per-fill hurdle the current zero-fee pnl omits. **PARK.** Not an ADMIT. Not Softened. Not scheduled. Not a board. Not a named horse |
| **What Lab found (cite, not re-derived as an admit)** | The lane **records** the fee regime as metadata (`fee_type=quadratic`, `fee_multiplier=1` in `data_feeds/kalshi_15m.py:54`–`:55`, copied into books/movements) and settle pays `payout = stake × decimal_odds` / `pnl = payout − stake` with **no fee term** (`settle.py:345`–`:346`). Cited from the PROPOSED §1; Operator does not re-derive it as an admit and did **not** run the arithmetic this fold |
| **Falsifiers (stay attached)** | All four from the PROPOSED §3. **Especially F1:** if `k` is not on a **public** Kalshi document, the test dies — no coefficient invented, no fee-accurate number published, no key requested. F2: fee rounds to $0.00/fill at the $1 unit → cosmetic. F3: total fee < 1% of stake → immaterial. F4: fee-accurate pnl is not strictly ≤ recorded pnl on some window → model wrong, withdraw |
| **Trigger to reopen** | A **public URL + retrieval date** for `k`, **or** a Founder **GO that names this test** |
| **Not a trigger** | Inventing `k` · running the arithmetic with an unsourced coefficient · Lab self-admit · a tidy tick · restating park facts · enough windows accumulating |
| **Not run this fold** | `k` is unsourced in the PROPOSED on purpose. Operator does not source it, does not invent it, and does not compute a hurdle |

`lab_admits=false`. Paper fills are not admits; this PROPOSED is not an admit. Golf idle stays **ON**. Founder HOLD (row 7) stands. No θ. No WC3+. Golf Operator stamp untouched.

---

## Hard NO (this park)

- Soften this park away · treat paper fills as an ADMIT (`lab_admits=false`) · claim edge established / banked edge / skill-met / productize
- Merge the two paper lineages, sum their bankrolls, or drop the published `paper_win` `+1.67`
- Invent win / lose / pnl anywhere a file does not record one · use a DIY CFB average as an official settle · read display prices as settle evidence
- Retune golf θ from this lane · rewrite the golf Operator stamp · reopen WC3+ · clear golf idle
- Hire a Soften Critic (**not hired** — do not invent the role)
- Lift the Founder HOLD (row 7) · expand past `KXBTC15M` · arm trading, keys, orders or cash
- Invent `k` · run the fee arithmetic without a public URL + retrieval date · treat row 10 as scheduled or as an ADMIT

## Handoff

CoS: Lab PROPOSED 01 is **PARKED** as row 10 — not admitted, not scheduled. Reopen only on a public URL + retrieval date for `k`, or a Founder GO that names this test. Lab does not bring a second PROPOSED. `systems` / `illustrator` still own row 5 if those surfaces are stale. Golf idle stays **ON**. Founder HOLD (row 7) stands.
