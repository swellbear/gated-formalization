# Agent leave-off (read this first)

**This file is the SoT for “where did we stop?”**  
Chat transcripts are not. A later Grok / Cursor cloud agent will not see a prior chat unless the work and this stamp are on GitHub.

| Field | Value |
|-------|--------|
| Updated | 2026-09-08 15:35 EDT (15m learning card generated from files; empty until a selection PROPOSED exists. Lab still assigned from 14:58. last_cos 7e15c76. Bar not binding.) |
| Interim operator | Cursor chat (Grok bot usage exhausted until **2026-09-13**) |
| Repo SoT | **PR [#176](https://github.com/swellbear/gated-formalization/pull/176) is OPEN, not merged.** `origin/master` is still `b063f56` (#175). Part A + Parts 0/1 live only on `cursor/part-a-clerical-trust-boundary`. |
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

`origin/master` before this fold is `b063f56` (PR #175 — live digest refresh + hash-stamped validator report, validator still judicial). `#174` hired Soften Critic and drafted the bar. `#173` put autostart scripts on the tree, not registered. GitHub Pages is **not** self-maintaining. A local export is not a publish.

**On `master` now:** learning wake, digest, park file with RUN-ONLY / classes, Lab PROPOSED 01 (RUN-ONLY, not admitted), export guard, serve-on-proof runner, kill file, continuous PaperWatch invoke, human artifact-proof.

**Armed locally:** `golf-offshoot/data/learning_lane_15m/latest/RUNNER_ARMED` (gitignored). The runner still does not commit or push. The public page is **not** self-maintaining. Restart the 15m hub if the running PaperWatch predates `c6354cc`.

Do not write branch state as if it were landed. If Pages `generated_at` is more than one 15-minute window behind now, the public page should say so itself.

## What is already on master (PR #163 and earlier)

Desktop hub (control surface):

- Launch: `golf-offshoot/scripts/windows/Open-Phase1-Hub.bat` → `python -m golf_offshoot shell` → `http://127.0.0.1:8765`
- Code: `golf-offshoot/src/golf_offshoot/operator_surface/app.py`
- Two lanes, exact selector `lane=golf|learning_lane_15m` (bare `15m` is unknown → golf)
- Buttons: ingest / live / shadow / loop / refresh. Cash / arm / Kalshi-auth actions are refused.
- Golf live/loop auto-applies **paper** advises only. 15m live/loop = public fetch → paper autobet → settle join.
- ntfy: one ping on operator-triggered ingest/live/loop finish if `NTFY_TOPIC` is set.
- Auto-reload: artifacts soft-refresh; git/code change re-execs the hub. Watched code is `operator_surface/*.py`, `learning_lane_15m/*.py`, `__main__.py`, `audit/shadow_settle.py`. `git_tip` resolves branch SHAs through the worktree `commondir` — without that a linked worktree never sees a commit on its own branch.

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

1. **The learning tick order is `lane-15m` → `digest-figures` → `digestor` (caveats only) → `operator` → `systems` → `validator`.** `hub-ui` runs only if the display is wrong or stale. **`illustrator` is owed by the wake** when the PNG lags live journal/settlements by more than one window (one window of trail is the open window and is allowed). **`lab` is still assigned 2026-09-08 14:58 ET** — one PROPOSED selection rule; do not revive `R-SKIP-COINFLIP`. **Do not run Lab in a CoS authoring turn.** Founder saved **15m worker tick** (`golf-offshoot/docs/WORKER_AUTOMATION.md`, cron `7,22,37,52`). First fire becomes that Lab job. The 15m hub tab has a **learning card** (`golf-offshoot/docs/LEARNING_LANE_15M_LEARNING_CARD.md`), generated from files; empty-state until a selection PROPOSED exists. **CoS last_cos** handled `A_idle_uncovered_judicial, B_new_judicial, E_idle_unassigned` at `7e15c76` (desk block + this line; wake is gitignored). A tick fires on a new official settle, a new paper fill, a pending window clearing, or a stale board. CoS starts when `crew_tick.needed` is true. Do not schedule CoS at 90s.
   - `lane-15m` — confirm the watch is healthy, do not double-start hubs, stay `SETTLE_PENDING` where there is no Kalshi `result`
   - `digest-figures` — generate the SOURCE figures half (`python -m golf_offshoot digest-15m`). Never write the caveats file
   - `digestor` — human caveats turn only, and **owed only on its five exceptions** (7f). A figures-only SOURCE refresh leaves this owed. A new caveat is the only write that clears it
   - `operator` — park/Soften only what the spine supports; put leave-off + desk on committed truth
   - `systems` — `manifest.json` merge; never drop the published `paper_win`, never invent a pending, never sum the lineages
   - `validator` — `python docs/observability-hub/validate_hub.py --strict --write-report` on the bytes about to publish; the hash-stamped report is its proof
   - `critic-invariants` — clerical, self-serving. Runs the eight method checks and writes `LEARNING_LANE_15M_CRITIC_FINDINGS.json`. It objects to nothing
   - `soften-critic` — the written attack. **Never auto-served**, and never in the same session as whoever authored the thing it attacks
   - **publish** — if that export differs materially from `origin/master`, commit the manifest + current real PNG and push/merge so Pages updates. Do not publish a 90s heartbeat. Do not leave a corrected falsehood unpublished
2. **Owed right now:** read it off `python -m golf_offshoot learn-15m` — do not trust this line, the loop keeps moving. The `KXBTC15M-26SEP071500-00` re-word is **done**: the published manifest reads `missing paper join — official result present`, and the fix lives in the export writer so the next export cannot undo it. Validator passed `--strict` at 19:53 after an export race was closed — pending is now re-derived from live settle files at export time, and the export refuses to write a manifest that calls a settled window pending.
3. **Never collapse the two residual states.** A window pending for want of a Kalshi `result` is not the same as `KXBTC15M-26SEP071500-00`, which has an official `result=yes` and no book on this tree. Do not invent pnl for either. Do not merge lineage A and lineage B.
4. **Illustrator:** the wake owes a re-render when the PNG lags more than one window. Re-render from current files before a material publish. Never invent a chart. Do not put golf WC1 / Ill on this lane.
5. **`lab` PROPOSED 01 is RUN-ONLY**, not parked. Hurdle lives only in `golf-offshoot/docs/LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md`. Not an ADMIT. Not a dashboard figure. Lab does not bring a second PROPOSED. Lab never self-admits. The clerical runner is armed by local `latest/RUNNER_ARMED` (gitignored). **Whitelist (trust-boundary move, not an append):** `illustrator`, `systems`, `digest-figures`, `validator`, `critic-invariants`. Human `digestor` is now in `JUDICIAL_NEVER`. Do not add `operator`, `lab`, or `soften-critic`. Do not put the figures generator in the `digestor` slot. Publish stays **manual**.
6. **`KXBTC15M-26SEP072245` does not exist.** 22:25–22:50 EDT `--once` argparse outage. Do not backfill. 56 locked lineage-A events is not an unbroken run. Digest §3g.
7. **Evidence bar has been attacked twice, amended twice, and is still NOT binding.** Read CRITIC 02 then `LEARNING_LANE_15M_EVIDENCE_BAR_OPERATOR_ANSWER_02.md` (`5dc4f24`) before touching the bar. CRITIC 01 answers remain in `OPERATOR_ANSWER_01.md`. Factory: Turn 1 `4090983` (CRITIC 02) → Turn 2 `0a480d4` (`decide()` live) → Turn 3 `5dc4f24` (admit pass). Operator on CRITIC 02: 3 OVERRULED (keyword greens on live checkers, δ reads H0, leftover owed / honesty-in-suite), 1 CONFIRMED, rest SUSTAINED or IN PART. Bar now names `control_function`, `adjustment_function`, `commit_order_control`. Method suite: 6 of 7 PASS; standing FAIL is `fee_schedule_hash_recorded`. Full suite **565 passed** against `5dc4f24` at 14:22 ET.
   - **Do not score `R-SKIP-COINFLIP`.** n is 70. `execution` stays false. Report the eligible count only; do not open a post-declaration outcome file.
   - **The band is not verifiably pre-registered.** Same 8h 07m finding as CRITIC 01. L1 still cannot Establish that rule.
   - **Why it is still not binding:** condition 2 fails on the unpinned fee hash (HTTP 429 at 13:42; `schedule_sha256` empty; no placeholder). Condition 3 (`founder_read_once`) is unmet and is **not requested**. Amending the bar re-owes `soften-critic` on the new bytes.
   - **`decide()` is live in the running hub** (`paper.py` → `consult_registry` → `rules.decide()`). Baseline fills (e.g. `KXBTC15M-26SEP081400-00` / `R-BASELINE-FILL-ALL`). `currently_reachable` stays **false** because `R-SKIP-COINFLIP` cannot Establish. Do not flip it after an L2 window has closed.
7b. **Part A landed and is now actually running.** `digest-figures` proves SOURCE. Human `digestor` is keyed on `LEARNING_LANE_15M_SOURCE_DIGEST_CAVEATS.md` only. `validator` is on the clerical whitelist with `validator_report.json` as proof. Proven in production, runner pass **10:46:45**: `served=[illustrator, systems, digest-figures, validator]`, `failed=[]`, with `operator` and `digestor` held for human. Auto-publish is **not** armed.

7c. **Part 0 — why Part A sat inert for ninety minutes.** Two independent defects, both needed for silence:
   - `read_git_tip` resolved refs only inside the **worktree** git dir. A linked worktree keeps branch refs in the common dir named by `commondir`, so every branch SHA read as empty and `git_tip` changed **only when the branch name changed**. A commit on the current branch looked like no change.
   - `hub_code_files` watched `operator_surface/*.py` only. The entire `learning_lane_15m` package — which PaperWatch and the clerical runner execute **inside** the hub — was unwatched.
   Both fixed in `operator_surface/reload.py`. The supervisor re-exec'd its own child; nothing was killed and no second hub was started. `process_matches_disk` is the standing check if this regresses.

7d. **Part 1 — the invariant suite.** `learning_lane_15m/invariants.py`, artifact `latest/invariants.json`, printed on every `learn-15m`. Four checks: `digest_matches_ledger`, `process_matches_disk`, `watch_is_collecting`, `clerical_roles_clear`. It runs **after** the runner pass, so a digest the runner just regenerated is not reported stale. Adding a check is Founder-free; **removing or weakening one is not.**

7e. **Also fixed:** `tests/test_learning_digest.py` called `write_digest()` with no root, so every full test run silently rewrote the **published** SOURCE digest. That is how the digest appeared to refresh at 10:40 before `digest-figures` had ever served. The generator now only touches the real spine through the runner.

7f. **Part 2 — human `digestor` has triggers again.** Five enumerated exceptions in `learning_lane_15m/triggers.py`, the cases where generated figures cannot express what changed: `paper_join_missing_grew`, `book_open_no_join`, `window_sequence_gap` (the `072245` shape), `settle_contradicts_book`, `unrecorded_cost`. The every-settle trigger is **not** restored. A detector that cannot read its evidence raises to Operator rather than staying silent — a detector that cannot see is not a detector that saw nothing.

7g. **Part 3 — three honesty boxes are derived, one needs evidence.** `learning_lane_15m/honesty.py`. Lineage, missing-join and hub-tree come off files, and the **derived verdict wins**: prose can shut a box, never open one, and deleting a row from the desk does not open the gate either. The hub box counts hub **trees** off the process table — the criterion is preserved exactly as written, a supervisor plus its child is one hub. `No invented charts or pnl` stays judgment and now needs a PID, a file hash or a timestamp; `**PASS**` alone no longer opens it. The parser was **narrowed, not widened**.

7h. **Part 4 — Operator no longer over-fires or false-clears.** A routine settle names `digest-figures`, `systems`, `validator` and nobody judicial. Operator is named by six enumerated exceptions (`park_aged`, `settle_contradicts_book`, `paper_join_missing_grew`, `window_sequence_gap`, `falsifier_fired`, `rule_reached_n`, `lab_proposed`). `operator_write_addresses_owed` is shaped like `material_publish_reasons`: a park write clears Operator only when the new text names what Operator was owed for, and **if it is unclear Operator stays owed**. No exception class was dropped to shorten the list and no Operator verdict is automated.

7i. **Part 5 — the Critic has a body.** Split like Digestor. `critic-invariants` is a deterministic checker, **on `CLERICAL_WHITELIST`**, proof artifact `golf-offshoot/docs/LEARNING_LANE_15M_CRITIC_FINDINGS.json`. `soften-critic` stays in `JUDICIAL_NEVER` — a written attack is not hash-provable. The missing trigger is now a **repo-side event class**, `artifact_unreviewed`: a watched artifact's hash changed and no Critic finding exists for that hash. Watched: the evidence bar (both files), the rule registry, the Lab PROPOSED, and the honesty-gate stamp section of the desk. Findings are keyed by content hash, so editing a bar re-owes the Critic on the new text and cannot be cleared by editing something else. Proven live 11:11:57: `served=[critic-invariants]` while `soften-critic` stayed owed.

7j. **Part 6 — the ratchet.** Eight method checks in `critic.py`, printed on every tick beside the four lane invariants: `matched_exposure_control`, `delta_above_detection_floor`, `holdout_is_forward_only`, `fee_adjusted_book_is_binding`, `declared_at_precedes_scored_windows`, `trials_counter_is_consistent`, `fee_schedule_hash_recorded`, `honesty_stamp_is_fresh`. A checker cannot find an unknown failure mode — that is why every flaw analysis finds becomes a permanent check. **Adding one is Founder-free; removing or weakening one is not.**

8. **Soften Critic is hired and has now run.** Skill `.cursor/skills/gpf-soften-critic/SKILL.md`. Not on the clerical whitelist and never auto-served. Part 7 attack: `LEARNING_LANE_15M_EVIDENCE_BAR_CRITIC_01.md`, written in a session separate from the one that drafted the bar (#174). Operator's answers are a **separate turn** from the objections — one turn may not both object and dismiss. Both turns did real adversarial work in both directions:
   - The Critic **rejected three of the seven briefed premises as factually wrong about the drafted text** — "thirteen eligible windows" is nowhere in a bar that says n=40 four times; L2 *is* forward-only and enforced in `rules.py`; and multiplicity was not uncorrected. It upheld sharper versions of each instead.
   - Operator **overruled the Critic's sharpest new claim.** The Critic argued the omitted bid/ask spread is worst at 50/50 *unlike* the fee. Operator recomputed: `s/(p+s)` is monotone decreasing in p, the same direction as the fee. The rule avoids neither cost's worst region — which is a worse result for the rule than the Critic's version, and it is the correct one.
   - **The ratchet closed on its own author.** The Critic found three defects in code committed an hour earlier, and Operator then found that the fix for one of them was only half applied: `_critic_token` reached the human artifact-proof path but `serve_role` still compared raw fingerprints, so the runner kept clearing the Critic on a heartbeat. Fixed at the same place `systems` gets its material test, with a guard against the opposite failure — a run that reviews a newly-changed artifact *has* done work, and treating it as a heartbeat would deadlock the role once `artifact_unreviewed` stopped firing.
8b. **Hub autostart scripts are on `master` (`b8b4d12`) and still not registered.** Task `GatedFormalization-15mLearningHub` does not exist. Founder, elevated local PowerShell, `Register-15m-Learning-Hub-Task.ps1`. An agent cannot elevate. Same exposure that cost `072245`.
8c. **Part 8 — one of five landed, and the other four have reasons, not excuses.**
   - **Landed: the judicial-silence counter.** Every owed line carries `ticks_unanswered` and the tick prints `silent N ticks`. Silence is now a number.
   - **Not landed: auto-publish on material change.** The mechanism (`material_publish_reasons`) already exists, but arming it means the clerical runner commits and pushes to the public surface on its own. That is an authority expansion across the same trust boundary the whitelist exists to guard, and it is the one item on the Next list that changes what an unattended process can do to `master`. **Publish stays manual.** Founder arms this, or it stays a one-command Systems step.
   - **Partly landed: `score_rule` exists and `decide()` is in the paper path.** `score_rule` was **not run**. `R-SKIP-COINFLIP` remains unscored, `execution` false. Do not score in a proposing, attacking, or amending turn.
   - **Partly landed: a runtime for Operator.** Part 4 gave Operator six enumerated triggers and a materiality test on its clear, which is most of a runtime. What it still lacks is a place to exercise ADMIT authority on this lane, and that is blocked behind a binding bar.
   - **Not landed: promoting `learning_lane_15m` into the gated method.** Blocked as written — the bar is not binding, and the Critic just gave four mechanical reasons why it should not become binding as drafted.
9. **Founder HOLD 2026-09-07 stands: no series other than `KXBTC15M` until this loop is honest.** Only Founder lifts it — not Operator, not CoS, not a later bot reading a tidy tick. Lifting it opens a **new lane**; it does not add a ticker here. Procedure: `golf-offshoot/docs/LEARNING_LANE_EXPANSION.md`. Everything else parked (weekly honesty rollup, expanding the series, CFB websocket observe-only) is in `golf-offshoot/docs/LEARNING_LANE_15M_METHOD_PARK.md` with the explicit trigger that would reopen it.
10. **Golf idle stays ON** (WC3+ only on a new settled week, on a fresh Founder GO that names the next invent). Nothing on the 15m lane clears it, retunes golf θ, or rewrites `golf-offshoot/docs/phase1_dryrun/OPERATOR_STATUS_STAMP.md`.

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
- Do not expand past `KXBTC15M` while the Founder HOLD stands, and do not lift it on the crew's own authority. Do not add a second series to this lane’s ledger, bar, or globs. Expansion procedure: `golf-offshoot/docs/LEARNING_LANE_EXPANSION.md`
- Soften Critic **is hired** — do not skip it, do not let it share the authoring session, do not put it on the clerical whitelist
- Do not merge leftover oil-hunt / `cursor/eia-window-job2` dirt into this track

## Resume commands

```powershell
cd golf-offshoot
$env:PYTHONPATH = "src"
python -m golf_offshoot learn-15m                        # learning tick — what is owed and why (start here)
python -m golf_offshoot shell --lane learning_lane_15m   # PaperWatch starts itself (~90s cycle) and runs one clerical pass each tick
# Windows: golf-offshoot/scripts/windows/Open-15m-Learning-Hub.bat
python -m golf_offshoot lane-15m --watch                 # CLI-only repeat, same cadence (do not also run learn-15m-runner)
python -m golf_offshoot learn-15m-runner --kill-runner   # write latest/RUNNER_KILL; does not touch PaperWatch
python docs/observability-hub/validate_hub.py --strict   # from repo root
```

One hub process only. A hub may already be live on `127.0.0.1:8765` — check before starting another, and never kill a running one to start your own.

Public viewer: `docs/observability-hub/` (read-only; no controls).
