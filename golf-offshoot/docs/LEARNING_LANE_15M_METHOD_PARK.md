# Operator — 15m method leftovers (park / CLOSED / RUN-ONLY)

**Track:** `learning_lane_15m` · series `KXBTC15M` only
**Updated:** 2026-09-08 17:11 EDT (PROPOSED 02 RUN-ONLY; row 9 closed on its trigger; bar still not binding)
**State:** No dated ADMIT on this lane. No Soften. No edge claim. `lab_admits=false` · Trading **NOT ARMED**
**Golf idle:** stays **ON**. This file does not clear it, does not touch golf θ, and does not rewrite `phase1_dryrun/OPERATOR_STATUS_STAMP.md`.

Digest this park folds: [`LEARNING_LANE_15M_SOURCE_DIGEST.md`](LEARNING_LANE_15M_SOURCE_DIGEST.md).
Conflict flag: [`LEARNING_LANE_15M_SOURCE_CONFLICT.md`](LEARNING_LANE_15M_SOURCE_CONFLICT.md) — **not** Softened away, **not** merged.
Ledger (honesty instrument, not progress): [`LEARNING_LANE_15M_PARK_LEDGER.json`](LEARNING_LANE_15M_PARK_LEDGER.json).

## How to read this file

Every **open** row is parked, not admitted. Each carries a **trigger** and a **class**:

| Class | Meaning |
|---|---|
| `crew` | The crew can make the trigger fire on this tree. Re-rule or restate within ~one day of active loop |
| `external` | Outside event or recovery. Ages without pressure |
| `founder` | Founder alone. Ages without pressure |
| `unreachable` | Cannot fire. These rows are **CLOSED**, not open parks |

A park whose trigger can never fire is a rejection wearing a deferral's clothes.

Numbers move while the watch runs. This file names **states and triggers**, not live figures.

---

## Park ledger (2026-09-08 17:11 EDT)

| | Count |
|---|---:|
| Open parks | **4** |
| Open · crew | 0 |
| Open · external | 1 |
| Open · founder | 3 |
| Open · unreachable | 0 |
| CLOSED · unreachable | **3** |
| CLOSED · trigger fired since last stamp | 3 |
| CLOSED · recorded defect (no backfill) | 1 |
| CLOSED · on a falsifier | 0 |
| RUN-ONLY executed (not an ADMIT) | 2 |
| Dated ADMITs | 0 |

No open crew park remains. The aging clock has nothing crew-owned to work on. Three open parks are founder; one is the rotating pending window (external). Do not mistake a clean crew column for progress.

---

## Open parks

### 1. True pending window — pending for want of a Kalshi `result`

| | |
|---|---|
| **Class** | `external` |
| **Last re-ruled** | 2026-09-07 21:40 EDT |
| **Instance** | **Do not read a ticker off this row.** It rotates. Read `python -m golf_offshoot learn-15m` |
| **Parked state** | Genuinely `SETTLE_PENDING`. Kalshi has not spoken. The open window's paper book on this tree exists with `settlement_pnl` null |
| **Trigger** | Kalshi publishes a `result` with `status` `finalized` / `determined`, matched to CF Benchmarks `BRTI`. Then `lane-15m` joins it |
| **Not a trigger** | `close_time` passing · a DIY CFB 60s average · a display price |

### 6. 15m weekly honesty rollup

| | |
|---|---|
| **Class** | `founder` |
| **Last re-ruled** | 2026-09-07 21:40 EDT |
| **Parked state** | **PROPOSED / PARK.** No dated ADMIT. `manifest.json` `$.lanes[1].records` is `[]` |
| **Trigger** | All three: (a) CoS honesty checklist all-PASS; (b) a full settled week on **one** readable lineage; (c) a fresh Founder **GO that names this rollup** |
| **Not a trigger** | Enough windows accumulating · restating park facts · a tidy tick |

### 7. Expand past `KXBTC15M` — Founder **HOLD**

| | |
|---|---|
| **Class** | `founder` |
| **Last re-ruled** | 2026-09-07 21:40 EDT |
| **Parked state** | **HOLD**, set by Founder 2026-09-07: no series other than `KXBTC15M` until this loop is honest |
| **Trigger** | **Founder lifts it.** Only trigger. The lift checklist is [`LEARNING_LANE_EXPANSION.md`](LEARNING_LANE_EXPANSION.md) — a new lane, not a ticker on this one. |
| **Who may lift it** | Founder. Not Operator, not CoS, not Lab, not a later bot |

This fold does **not** lift the HOLD and is not evidence toward lifting it. A RUN-ONLY fee hurdle is not evidence toward lifting it. Citing the expansion file is not evidence toward lifting it.

### 8. Lab — new named horse on this lane

| | |
|---|---|
| **Class** | `founder` |
| **Last re-ruled** | 2026-09-08 17:11 EDT |
| **Parked state** | **Named horse not opened.** The residual-triggered selection PROPOSED (row 9 / row 13 RUN-ONLY) used the second cheap-test slot. A third PROPOSED is not owed |
| **Trigger** | A fresh Founder GO that names a new invent. Under golf idle, a WC3+ / new board without that GO is an idle-breach REJECT |

### 9. Zero-edge fills — the observation gap (residual, not a board) — **CLOSED / trigger fired**

| | |
|---|---|
| **Closed** | 2026-09-08 17:11 EDT |
| **What fired** | Lab PROPOSED 02 `R-SKIP-2TO1-FAVORITE` selects. Operator **RUN-ONLY**; `execution=true` (paper only). Trigger named here: *a later PROPOSED that actually selects* |
| **Honest state (still true)** | Fills that still happen remain `entry_edge=0.0`. Selecting is not an edge and not an ADMIT. That honesty lives in [`LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_02.md`](LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_02.md), not as an open park |
| **Not a claim** | Closing this row is not Established, not a bind, and not evidence toward lifting the HOLD |

---

## CLOSED — unreachable (cannot fire on this tree)

These required a machine we do not have, or a book that never existed here. They are not open parks.

### 2. `KXBTC15M-26SEP071500-00` — missing paper join — **CLOSED / unreachable**

| | |
|---|---|
| **Closed** | 2026-09-07 21:40 EDT |
| **Reason** | The original book lives on a tree where `artifact_root_15m()` resolved to `/workspace/kalshi_15m_exports`. That machine is not this tree. The crew cannot produce the book |
| **Honest state (still true)** | Kalshi settled `yes`. There is no paper pnl here and none is invented. The published surface now says *missing paper join*, not `SETTLE_PENDING` |
| **Not reopened by** | Knowing the official result · inventing a pnl · summing lineage A and B |

### 3. `KXBTC15M-26SEP071445-45` — published-only lineage B book — **CLOSED / unreachable**

| | |
|---|---|
| **Closed** | 2026-09-07 21:40 EDT |
| **Reason** | The book that produced published `+1.67` is not on this tree and requires the same missing machine |
| **Honest state (still true)** | Lineage B `paper_win` `+1.67` is **kept** as published history. Never added to lineage A. Never re-derived here |

### 4. Unmeasured tape — **CLOSED / unreachable**

| | |
|---|---|
| **Closed** | 2026-09-07 21:40 EDT |
| **Reason** | These windows closed before the local book existed (`ledger.json` `observation_seed` 15:42:37 EDT). No book existed here. None can be recovered on this tree. The rolling journal will drop them from the front; that is forgetting, not resolving |
| **Honest state (still true)** | Unmeasured is not lost and not losses. Do not backfill from official results. Do not count them in any denominator |

---

## CLOSED — recorded defect (do not backfill)

### 11. `KXBTC15M-26SEP072245` — outage gap — **CLOSED / recorded defect**

| | |
|---|---|
| **Closed** | 2026-09-08 05:55 EDT |
| **What happened** | The 22:25–22:50 EDT `--once` argparse collision. Window `KXBTC15M-26SEP072245` (22:30–22:45 EDT) does not exist on this tree |
| **Evidence** | No `paper/` file, no `settlements/` file, no `ledger.json` row, no `latest/journal.json` `windows[]` row. Adjacent windows `072230-30` and `072300-00` exist |
| **Honest state** | 56 locked lineage-A events is **not** an unbroken run. Digest §3g |
| **Forbidden** | Backfill · infer a Kalshi `result` · invent a fill or pnl · treat 56 as a continuous overnight sample |
| **Not reopened by** | Knowing the outage cause · wishing the console had stayed up |

---

## CLOSED — trigger fired

### 5. Stale display wording — **CLOSED / trigger fired**

| | |
|---|---|
| **Closed** | 2026-09-07 21:33 EDT |
| **What fired** | Systems re-worded the export; Illustrator re-rendered from current files; PR #165 merged; Pages build `be04ebe` served `generated_at` `2026-09-07T21:28:39-04:00` |
| **Public wording now** | `KXBTC15M-26SEP071500-00 is a missing paper join, not a pending window` |
| **Not a claim** | Publishing the correction is not an ADMIT and not evidence toward lifting the HOLD |

---

## RUN-ONLY executed (not a park, not an ADMIT)

### 10. Lab PROPOSED 01 — charge the documented fee

| | |
|---|---|
| **Verdict** | **RUN-ONLY** · Operator · 2026-09-07 21:40 EDT |
| **Note** | [`LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md`](LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md) |
| **Posture ruling** | Reading `https://kalshi.com/docs/kalshi-fee-schedule.pdf` is inside public-read-only. **F1 did not fire** |
| **Falsifiers** | F1–F4 all attached; **none fired** |
| **What it is** | A cost / hurdle in an Operator note. ~$0.04 per $1 fill, 3.92% of $24 stake, n=24 lineage-A books |
| **What it is not** | An ADMIT · an edge · a hit rate · a dashboard figure · evidence toward lifting the HOLD |
| **Promotion** | Would require the normal dated-record ADMIT gate. Accumulation of this note does not admit it |

The 21:05 "park it, do not schedule" instruction is **superseded**.

### 13. Lab PROPOSED 02 — skip a posted 2-to-1 YES favorite

| | |
|---|---|
| **Verdict** | **RUN-ONLY** · Operator · 2026-09-08 17:11 EDT |
| **Note** | [`LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_02.md`](LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_02.md) |
| **Registry** | `R-SKIP-2TO1-FAVORITE` · `favorite_odds=2` · first naming `e9fab5a` · `execution=true` (paper only) |
| **Owed for** | `lab_proposed` — CoS assigned RUN-ONLY unless a specific objection |
| **Falsifier** | After the n the bar names (currently 70), indistinguishable from `R-BASELINE-FILL-ALL` → park; do not retune `favorite_odds` |
| **What it is** | A paper selection rule authorized to execute. Skip posted YES ≥ 2/3; else fill at the posted mark with `entry_edge=0.0` |
| **What it is not** | An ADMIT · an edge · a score · a dashboard figure · a revival of `R-SKIP-COINFLIP` · evidence toward lifting the HOLD |
| **Promotion** | Would require the normal dated-record ADMIT gate, a binding bar, and a Soften Critic attack from a separate session. Accumulation of this note does not admit it |

---

## Hard NO (this park)

- Soften this file away · treat paper fills or RUN-ONLY output as an ADMIT · claim edge / banked edge / skill-met / productize
- Merge the two paper lineages, sum their bankrolls, or drop the published `paper_win` `+1.67`
- Invent win / lose / pnl anywhere a file does not record one · use a DIY CFB average as an official settle
- Retune golf θ · rewrite the golf Operator stamp · reopen WC3+ · clear golf idle
- Skip the Soften Critic on a proposed ADMIT or on binding the evidence bar
- Lift the Founder HOLD (row 7) · expand past `KXBTC15M` · arm trading, keys, orders or cash
- Put a fee-accurate figure on the hub or in `records[]` without a later ADMIT
- Relist CLOSED-unreachable rows as open parks

## CLOSED — founder trigger fired

### 12. Soften Critic hire — **CLOSED / founder trigger fired**

| | |
|---|---|
| **Closed** | 2026-09-08 08:30 EDT |
| **What fired** | Founder GO hired the Soften Critic. Skill: `.cursor/skills/gpf-soften-critic/SKILL.md` |
| **Honest state** | The role exists. It attacks proposed ADMITs and the evidence bar from a separate session. Operator records each objection. The hire is not an ADMIT and does not bind the bar |
| **Not a claim** | Hiring the critic does not establish edge and does not promote this lane into the gated method |

## Handoff

CoS: PROPOSED 02 is **RUN-ONLY** (`R-SKIP-2TO1-FAVORITE`, `execution=true`, not scored). Evidence bar is a **draft, not binding**. Soften Critic is hired. Promotion has not fired (bar is not binding). Golf idle stays **ON**. Founder HOLD stands. A third Lab PROPOSED is not owed.
