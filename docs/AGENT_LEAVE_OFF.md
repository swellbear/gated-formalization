# Agent leave-off (read this first)

**This file is the SoT for “where did we stop?”**  
Chat transcripts are not. A later Grok / Cursor cloud agent will not see a prior chat unless the work and this stamp are on GitHub.

| Field | Value |
|-------|--------|
| Updated | 2026-09-07 21:42 EDT (Gate 1 landed; Phase 2 RUN-ONLY + park classes; Phase 3 runner dry-run) |
| Interim operator | Cursor chat (Grok bot usage exhausted until **2026-09-13**) |
| Repo SoT | **`origin/master` @ `be04ebe`** (PR #165 merged). Pages reads that commit. Public snapshot `generated_at` `2026-09-07T21:28:39-04:00` |
| Local Windows tree for this interim | `C:\Users\bearh\gated-formalization-master-hub` |
| Do **not** treat as SoT | `C:\Users\bearh\gated-formalization` on `cursor/eia-window-job2` (stale + dirty) |
| Active track | `learning_lane_15m` (KXBTC15M paper loop) + Phase 1 desktop hub |
| Crew | `docs/agents/` — CoS routes; desk is live board |
| Trading | **NOT ARMED** |

## Required closeout (every session)

Before stopping, the agent that just worked **must**:

1. Update this file **and** `docs/agents/DESK.md` so they match **committed** truth.
2. Commit this file with the work (or a docs-only follow-up if the work already landed).
3. Push the branch / open or update the PR so `master` (or the open PR) is what the next bot clones.

If it is not in git on GitHub, the next bot does not have it.

## What is on `origin/master` versus what is only on this branch

**`origin/master` is the public SoT.** GitHub Pages serves that commit only. A local export, a desktop hub, or an unmerged PR is **not** published.

`origin/master` is `be04ebe` (PR #165 merged 2026-09-07). That commit **does** have `learn-15m`, the SOURCE digest, the pending/settled export guard, snapshot age on the viewer, and the corrected `071500-00` missing-paper-join wording. GitHub Pages build for `be04ebe` is `built`. Live `generated_at` is `2026-09-07T21:28:39-04:00`.

**On `master` now:** learning wake, digest, park file (as of #165 — still the old two-verdict park), Lab PROPOSED 01, export guard.

**Not yet on `master` (this session's Phase 2+3, until the next PR lands):** RUN-ONLY verdict, four trigger classes, CLOSED unreachable rows, Operator note with the fee hurdle, clerical runner in dry-run.

Do not write branch state as if it were landed. If Pages `generated_at` is more than one 15-minute window behind now, the public page should say so itself.

## What is already on master (PR #163 and earlier)

Desktop hub (control surface):

- Launch: `golf-offshoot/scripts/windows/Open-Phase1-Hub.bat` → `python -m golf_offshoot shell` → `http://127.0.0.1:8765`
- Code: `golf-offshoot/src/golf_offshoot/operator_surface/app.py`
- Two lanes, exact selector `lane=golf|learning_lane_15m` (bare `15m` is unknown → golf)
- Buttons: ingest / live / shadow / loop / refresh. Cash / arm / Kalshi-auth actions are refused.
- Golf live/loop auto-applies **paper** advises only. 15m live/loop = public fetch → paper autobet → settle join.
- ntfy: one ping on operator-triggered ingest/live/loop finish if `NTFY_TOPIC` is set.
- Auto-reload: artifacts soft-refresh; git/code change re-execs the hub.

15-minute Kalshi learning lane:

- Docs: `golf-offshoot/docs/LEARNING_LANE_15M.md`
- Code: `golf-offshoot/src/golf_offshoot/learning_lane_15m/`
- CLI: `python -m golf_offshoot lane-15m`
- Public read only. Official settle = Kalshi `result` matched to CF Benchmarks `BRTI`.
- Landed: PRs #151, #153, #156–#159, #161, #162.

Windows path fix (this branch): settlement filenames sanitize `:` (`safe_artifact_stem`). `window_id` inside JSON still keeps colons. Export keeps a published 15m settle history when the local journal would drop `Settled windows` / `paper_win`.

Golf Phase 1 (do not reopen unless asked):

- Stamp: `golf-offshoot/docs/phase1_dryrun/OPERATOR_STATUS_STAMP.md`
- WC1 admitted FAIL / park unproven. WC2 parked/rejected. Edge **not** established. Idle on WC3+ until a new settled week.
- **Golf idle is ON** and nothing on the 15m lane clears it, retunes golf θ, rewrites that stamp, or reopens WC1 / WC2 / WC3+.

## Learning is now **on** (this is the change since the last leave-off)

> **Public hub = `origin/master`.** A local `observability-export` does not update Pages. After PR #165 merges, `master` carries the learning wake (`learn-15m`), the SOURCE digest, the method park, Lab PROPOSED 01 (PARKED, not admitted), the export-time pending/settled guard, and the corrected `071500-00` missing-paper-join wording. Clone `master` after that merge. If you still see "Live 1500 stays SETTLE_PENDING" on GitHub Pages, the deploy has not finished — that wording is a known stale falsehood and must not be treated as current.

PaperWatch alone was never learning. Two halves now run together:

1. **PaperWatch** — the researcher/export half, one cycle roughly every **90 seconds** (`DEFAULT_INTERVAL_S = 90.0`, `golf-offshoot/src/golf_offshoot/learning_lane_15m/watch.py`). Public fetch → paper autobet → settle join → export. It starts itself with the 15m hub.
2. **The learning wake** — the crew half. It scans settlements / paper / journal / manifest, raises `new_settle` / `new_fill` / `pending_cleared` events, and **names which roles are owed a turn.**

Run the tick:

```powershell
cd golf-offshoot
$env:PYTHONPATH = "src"
python -m golf_offshoot learn-15m          # human-readable
python -m golf_offshoot learn-15m --json   # same tick as JSON
```

Wake state file: `golf-offshoot/data/learning_lane_15m/latest/learning_wake.json` (gitignored, derived, **never authoritative** — the files on disk are).

**Python names owed roles. It never marks one served, never writes a desk thread line, never Softens, never ADMITs, and never invents a win, a lose or a pnl.** A role clears its own line only after it really ran:

```powershell
python -c "from golf_offshoot.learning_lane_15m.learn import mark_roles_served; mark_roles_served(['operator'], by='operator', note='what you actually did')"
```

Read these two before touching the lane:

- **SOURCE honesty digest (living spine, every claim cited to a file):** `golf-offshoot/docs/LEARNING_LANE_15M_SOURCE_DIGEST.md`
- **Operator method park (residuals + explicit reopen triggers):** `golf-offshoot/docs/LEARNING_LANE_15M_METHOD_PARK.md`
- Standing conflict flag: `golf-offshoot/docs/LEARNING_LANE_15M_SOURCE_CONFLICT.md`

## Published hub snapshot — corrected against the digest and live files

**These numbers move.** The loop is live, so a window settles and the book changes roughly every 15 minutes. Figures below are as of **2026-09-07 18:19 EDT**. Do not trust them as current — re-read them with `learn-15m` and from `golf-offshoot/data/learning_lane_15m/`.

**Two paper lineages exist. They are two separate books, not two views of one book. Never sum them.**

*Lineage A — the local paper book on this tree* (`golf-offshoot/data/learning_lane_15m/paper/` + `paper/ledger.json`):

- Seed `starting_bankroll` 100.00 → `bankroll` **95.59** · `betting_pnl` **-4.41** · `deposits` 0.00 · `withdrawals` 0.00 · 24 entries · 11 settled events
- 12 settle files and 12 paper books on disk: **11 joined and settled, 1 open**
- Windows joined run `KXBTC15M-26SEP071545-45` onward. Each row's pnl comes off its own `paper/<stem>.json` `settlement_pnl` — e.g. `071600-00` is `+0.42` (the previous leave-off's `$+0.44` was wrong), `071615-15` is `-1.00`
- The recorded pnl figures reconcile the `bankroll_before` → `bankroll_after` chain in `ledger.json`. Nothing is recomputed or averaged

*Lineage B — the published Pages export* (`docs/observability-hub/data/manifest.json` `$.lanes[1]`):

- `KXBTC15M-26SEP071445-45` — official `result=yes`, **paper_win**, paper pnl `+1.67`. **Kept as published history.** The book that produced it is not on this tree, so `+1.67` is never re-derived here and never added into lineage A
- Why they are split, cited to code: `learning_lane_15m/paths.py` `artifact_root_15m()` prefers `/workspace/kalshi_15m_exports` and falls back to the repo root when `/workspace` is absent, as it is on this Windows tree. Same code, different machine, different book

**The two residual states that look alike on a dashboard and are not alike:**

- **Pending for want of a Kalshi result** — a true pending window. Kalshi has not spoken; the paper book here is open. There is normally exactly one, and it **rotates every ~15 minutes** — it was `071815-15` at 18:03 EDT, `071830-30` at 18:20 and `071845-45` at 18:32. **Read the current one off `learn-15m`, never off this file.** A ticker that has left this state did not fail; it settled, and its pnl is on its own book
- **`KXBTC15M-26SEP071500-00` is a missing paper join, NOT a pending window.** Kalshi settled it **`yes`** (`latest/journal.json`, `status` `finalized`). The paper book the published lineage names is **not on this tree**, so there is **no paper pnl here and none is invented.** `SETTLE_PENDING` is the wrong banner — it says "Kalshi has not spoken," and Kalshi has. `result=yes` does not license a win, a `+pnl`, a `0`, or a loss here. A window with no book has no pnl; that is a true statement, not a missing number

**Still stale on the published surface (owned by `systems`, not by whoever reads this):** `manifest.json` still carries *"SETTLE_PENDING until Kalshi result"* for `071500-00` at `$.lanes[1].settle.headline`, `$.lanes[1].settle.residual[0].note`, `$.lanes[1].last_run.headline` and `$.lanes[1].last_run.notes[2]` — while the **same file** already states the honest version at `$.lanes[1].settle.counts[5].note`. That re-word is Systems' job.

**Unmeasured tape:** a handful of windows are `finalized` with an official result in `latest/journal.json` but have no settle file and no paper book anywhere on this tree — they closed before the local book seeded at 15:42:37 EDT. The digest named 8 of them at 18:03 EDT; `071315-15` has already rolled off, leaving `071330-30`, `071345-45`, `071400-00`, `071415-15`, `071430-30`, `071515-15`, `071530-30` at 18:28 EDT. **`latest/journal.json` is a rolling 21-window tape, not an archive** — the oldest window falls off as a new one opens, so this list shrinks from the front. A shrinking list means windows are being *forgotten*, not resolved. **Unmeasured is not lost and not losses.** Do not backfill them from their results and do not count them in a denominator.

**15m charts now exist:** `docs/observability-hub/data/charts/learning_lane_15m/paper_window_strip.png` is a real, labeled board rendered from real files, drawing lineage A apart from lineage B with a *never summed* note. It is **behind**, not invented — its header stamps `journal generated_at=2026-09-07T17:10:08`, and its `071500-00` cell still prints `SETTLE_PENDING`. The old "charts not yet available" leftover is stale.

**No edge, no track record.** Every fill is taken at the posted mark with `entry_edge=0.0`; the model is the market. Paper fills are not admits (`lab_admits=false`). This lane has no dated record — `manifest.json` `$.lanes[1].records` is `[]`.

Golf WC1 FAIL does **not** transfer into this lane, and nothing on this lane retunes golf θ.

## Next (safe, in order)

**Start every turn by running the tick.** `python -m golf_offshoot learn-15m` tells you which roles are owed and why. Serve them in the Protocol learning-tick order below; do not ping Founder to approve any of it.

1. **The learning tick order is `lane-15m` → `digestor` → `operator` → `systems` → `validator`.** `hub-ui` runs only if the display is wrong or stale. **`illustrator` is owed by the wake** when the PNG lags live journal/settlements by more than one window (one window of trail is the open window and is allowed). **`lab` runs only after the honesty gate passes** — see item 5. A tick fires on a new official settle, a new paper fill, a pending window clearing, or a stale board.
   - `lane-15m` — confirm the watch is healthy, do not double-start hubs, stay `SETTLE_PENDING` where there is no Kalshi `result`
   - `digestor` — refresh the SOURCE honesty digest from real files only
   - `operator` — park/Soften only what the spine supports; put leave-off + desk on committed truth
   - `systems` — `manifest.json` merge; never drop the published `paper_win`, never invent a pending, never sum the lineages
   - `validator` — `python docs/observability-hub/validate_hub.py --strict` on the bytes about to publish
   - **publish** — if that export differs materially from `origin/master`, commit the manifest + current real PNG and push/merge so Pages updates. Do not publish a 90s heartbeat. Do not leave a corrected falsehood unpublished
2. **Owed right now:** read it off `python -m golf_offshoot learn-15m` — do not trust this line, the loop keeps moving. The `KXBTC15M-26SEP071500-00` re-word is **done**: the published manifest reads `missing paper join — official result present`, and the fix lives in the export writer so the next export cannot undo it. Validator passed `--strict` at 19:53 after an export race was closed — pending is now re-derived from live settle files at export time, and the export refuses to write a manifest that calls a settled window pending.
3. **Never collapse the two residual states.** A window pending for want of a Kalshi `result` is not the same as `KXBTC15M-26SEP071500-00`, which has an official `result=yes` and no book on this tree. Do not invent pnl for either. Do not merge lineage A and lineage B.
4. **Illustrator:** the wake owes a re-render when the PNG lags more than one window. Re-render from current files before a material publish. Never invent a chart. Do not put golf WC1 / Ill on this lane.
5. **`lab` PROPOSED 01 is RUN-ONLY**, not parked. Hurdle lives only in `golf-offshoot/docs/LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md`. Not an ADMIT. Not a dashboard figure. Lab does not bring a second PROPOSED. Lab never self-admits. Founder has not armed the clerical runner.
6. **Founder HOLD 2026-09-07 stands: no series other than `KXBTC15M` until this loop is honest.** Only Founder lifts it — not Operator, not CoS, not a later bot reading a tidy tick. Everything else parked (weekly honesty rollup, expanding the series, CFB websocket observe-only) is in `golf-offshoot/docs/LEARNING_LANE_15M_METHOD_PARK.md` with the explicit trigger that would reopen it.
7. **Golf idle stays ON** (WC3+ only on a new settled week, on a fresh Founder GO that names the next invent). Nothing on the 15m lane clears it, retunes golf θ, or rewrites `golf-offshoot/docs/phase1_dryrun/OPERATOR_STATUS_STAMP.md`.

## Hard NOs

- No Kalshi API keys, cash scopes, orders, or private endpoints
- AI never deposit / withdraw / transfer
- Do not retune golf θ from 15-min
- Do not invent win/lose or use DIY CFB averages as official settle. Display prices (`yes_bid` / `yes_ask` / `last_price`) are not settle evidence
- Do not put golf WC1 / Ill under `learning_lane_15m`
- Charts render from real files only. A chart no real file can drive stays `not yet available` — never invented, never back-filled
- Do not merge, sum, net or average the two paper lineages, and do not drop lineage B's published `paper_win` `+1.67` to make one clean story
- Do not Soften the SOURCE CONFLICT away. Either one readable lineage story or an explicitly labeled dual lineage — a silent merge fails the honesty gate
- Paper fills are not ADMITs (`lab_admits=false`). No edge established / banked edge / skill-met / productize on this lane
- Do not expand past `KXBTC15M` while the Founder HOLD stands, and do not lift it on the crew's own authority
- Soften Critic is **not hired** — do not invent the role
- Do not merge leftover oil-hunt / `cursor/eia-window-job2` dirt into this track

## Resume commands

```powershell
cd golf-offshoot
$env:PYTHONPATH = "src"
python -m golf_offshoot learn-15m                        # learning tick — what is owed and why (start here)
python -m golf_offshoot shell --lane learning_lane_15m   # PaperWatch starts itself (~90s cycle)
# Windows: golf-offshoot/scripts/windows/Open-15m-Learning-Hub.bat
python -m golf_offshoot lane-15m --watch                 # CLI-only repeat, same cadence
python docs/observability-hub/validate_hub.py --strict   # from repo root
```

One hub process only. A hub may already be live on `127.0.0.1:8765` — check before starting another, and never kill a running one to start your own.

Public viewer: `docs/observability-hub/` (read-only; no controls).
