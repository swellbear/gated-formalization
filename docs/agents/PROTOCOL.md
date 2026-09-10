# Agent communication protocol

Chat is not memory. Roles talk through **[DESK.md](DESK.md)** and **[AGENT_LEAVE_OFF.md](../AGENT_LEAVE_OFF.md)**.

**Chief of Staff keeps the track moving.** Founder is only for a rare review or a real change of direction. Do not ping Founder to approve work that is already on leave-off “Next” or that stays inside the Hard NOs.

## CoS is a body, not a courtesy

CoS starts when `crew_tick.needed` is true, including via a Cursor Automation on a **15–30 minute** timer. Founder opening a chat is a backup, not the trigger. Do not schedule CoS at 90 seconds.

`crew_tick` is derived on each `learn-15m` tick and written into `learning_wake.json`. It is not a second SoT. The wake already names `roles_owed`; `crew_tick` only says whether a CoS session should start. Enumerated in `golf-offshoot/src/golf_offshoot/learning_lane_15m/crew_tick.py` and here. If unsure, `needed` stays true and the reason says why.

`needed` is **true** when at least one of these holds:

- **A.** A worker just finished and the desk says `next=chief-of-staff` (or `Status=done` and Active role is a worker, or `Status=idle` and a judicial owe exists that no job is covering).
- **B.** A *new* judicial owe appeared since the last CoS closeout (Operator exception, soften-critic on new artifact hashes, human digestor exception).
- **C.** A `CLERICAL_WHITELIST` role owed longer than two ticks (already an invariant).
- **D.** Watch or hub liveness failed (cycles not advancing, or the honesty hub box would fail). Hub fail is an ops doorbell (`D_hub`), not a veto on Lab.
- **E.** Desk `Status=idle` while leave-off Next / an unassigned factory precondition is still open.
- **F.** `F_continuation`: desk idle (or CoS with Job `—`), no assigned worker, no un-operated Lab PROPOSED, and no live 15m trial (executing selection still unscored). Favorite L1 PARK is dead. `R-SKIP-COINFLIP` `execution: false` is not live. Stamp F handled **only after** desk `Status=assigned` / `lab`.
- **H.** `H_honer_freeze`: honer exam is open (or freeze log has an unproposed snapshot), no Lab PROPOSED already names that freeze, `consult_enabled` is not true, and the desk is not an assigned worker. CoS assigns Lab to name **that** freeze even if a factory trial is live. If both H and F, H wins. Stamp H handled **only after** desk `Status=assigned` / `lab`.

`needed` is **false** when the watch is healthy AND no new judicial owe AND no clerical arrears AND the desk already has an assigned worker who is not stale AND F is not owed AND H is not owed, **or** when the last CoS closeout stamped the same `reason_ids` (a 90s heartbeat, not a doorbell). F and H are not silenced by that stamp unless Lab is assigned.

A CoS turn: session start, **one** assign or one closeout via `decide_cos_action` (`golf-offshoot/src/golf_offshoot/learning_lane_15m/cos_tick.py`), desk + leave-off to committed truth, stamp `last_cos_*` via `stamp_cos_closeout`. Then stop. It does not ping Founder for the Next list. It does ping Founder for arm / cash / keys, golf C2/C4/WC3+, and retune golf θ. Bind is not on that list. Forbidden assigns: score `R-SKIP-COINFLIP`, re-score PARK'd `R-SKIP-2TO1-FAVORITE`, arm, bind, git push to `master`. **Lab is legal:** F_continuation assigns one 15m PROPOSED. H_honer_freeze assigns Lab to name that freeze (even if a factory trial is live). CoS does not author the PROPOSED. Operator `lab_proposed` or Critic on a **new** hash first. Zero-objection closeout does not skip a sitting PROPOSED, a starved gym, or an open honer freeze (assign Operator or Lab).

**Zero-objection stop.** If the newest Soften Critic finding is zero UPHELD and Operator did **not** amend the bar (a record-only ANSWER, or no ANSWER owed), CoS **closes out**: `Status=idle`, do not assign Operator to write another ANSWER, do not assign Soften Critic on those same hashes. Two consecutive zero-UPHELD attacks is the treadmill; close it. A new judicial owe is a *new* bar/registry hash from a real amendment, not a new CRITIC file that found nothing. If `stamp_cos_closeout` cannot persist (cloud VM missing wake or import failure), the committed desk `last_cos_*` table is the stamp. `crew_tick` / `stamp_cos_closeout` must import without pydantic. Do not invent `A_worker_done` from an empty VM. Do not ask Founder to pip-install pydantic on the CoS VM.

Quiet tick: `needed` false ⇒ the automation no-ops. No desk spam.

The runner may write `crew_tick`. It may not open a chat, ADMIT, invent, or push. CoS, Operator, Lab, and soften-critic stay off `CLERICAL_WHITELIST`.

## Worker tick is a body, not a courtesy

When the desk `Status=assigned`, a **separate** 15-minute Cursor Automation (`15m worker tick`, cron `7,22,37,52`) becomes that Active role, does the Job, sets `Status=done`, and hands to CoS. It does not assign the next worker. CoS assigns; this timer runs. SoT: [`golf-offshoot/docs/WORKER_AUTOMATION.md`](../../golf-offshoot/docs/WORKER_AUTOMATION.md).

## The learning card is clerical, not a verdict

The 15m hub panel **What is on trial** is generated from files (`learning-card` on `CLERICAL_WHITELIST`). It may quote a Lab note or an Operator ruling. It is not itself a verdict. Operator notes remain the verdict SoT. Empty state is honest: if no selection PROPOSED exists, the card says so and names the executing baseline. SoT: [`golf-offshoot/docs/LEARNING_LANE_15M_LEARNING_CARD.md`](../../golf-offshoot/docs/LEARNING_LANE_15M_LEARNING_CARD.md).

## Session start (every turn)

1. Read `docs/AGENT_LEAVE_OFF.md`.
2. Read `docs/agents/DESK.md`.
3. Be **Chief of Staff** unless the desk `Active role` is already a named worker **and** this turn is finishing that job.
4. Read `.cursor/skills/gpf-chief-of-staff/SKILL.md`.
5. If CoS assigns a worker, read that worker’s skill, then do **only** that job.

## One worker at a time

Habit A. Do not run Lab + Systems + Illustrator in parallel. Validator may run **after** a worker finishes, in the same turn.

## How roles talk

Post on the desk, newest first, max 10 thread lines:

```
YYYY-MM-DD HH:MM TZ  FROM → TO: one sentence. next=ROLE or Founder.
```

| Event | Who writes | What |
|-------|------------|------|
| Assign | CoS | Set `Active role`, `Job`, `Status=assigned` |
| Start | Worker | `Status=working` + thread line |
| Done | Worker | `Status=done`, `Handoff`, thread line |
| Need you | Any | `Status=waiting-founder`, **one** question, then **stop** |
| Close | CoS | Update leave-off; `Active role=chief-of-staff` or next assign |

Do not leave a decision only in chat.

## When to ask Founder (stop)

Only if something **important must change or be reviewed**. One question, then wait.

Ask:

- C2 / C4 / TABLE / reopen WC3+
- Retune golf θ
- Arm trading, cash, Kalshi keys
- Change a Hard NO, or put golf WC1 / Ill on the 15m lane
- A new dated-record ADMIT / REJECT that would rewrite the Operator stamp
- A Validator fail that is not a simple writer fix (honesty / method conflict)

Do **not** ask (CoS just does it):

- Leave-off “Next” items
- Start or continue the 15m paper watch
- Assign Lab when `F_continuation` is owed (one 15m PROPOSED; CoS does not write it)
- Assign Lab when `H_honer_freeze` is owed (name that freeze snapshot; do not enable consult)
- Enable honer consult when exam + score + later Critic exist: assign Systems to flip **that** snapshot
- Scaffold a **new lane** when [`LEARNING_LANE_EXPANSION.md`](../../golf-offshoot/docs/LEARNING_LANE_EXPANSION.md) checklist is true **and** this gym already has a live try (not a second ticker on this ledger)
- `lane-15m` → `systems` → `validator` when a Kalshi `result` exists
- Stay `SETTLE_PENDING` when it does not (never invent win/lose)
- Desk / leave-off bookkeeping
- Chrome-only Hub UI inside existing Hard NOs
- Gym `PUBLISH_ARMED` material hub-allowlist push (this gym PC only). Cloud CoS/worker must **not** `git push` to `master`. Factory merge of #178 is a PR merge, not that script
- Do not ping Founder to stamp bind. Bind is Critic+Operator and critic-invariants; CoS assigns those roles. CoS does not set `binding: true`. Do not add a Founder stamp to bind.
- Ask Founder to click ingest / live / loop

## Keep-looping (15m)

While the desktop hub is on `learning_lane_15m`, **PaperWatch** repeats the researcher/export half. Founder observes. Founder does not operate.

PaperWatch alone is **not learning.** Learning has not begun until settled outcomes are digested on a schedule and change what the crew does next.

### Learning tick (new official settle, new paper fill, or a pending cleared)

1. `lane-15m` — confirm watch healthy; do not double-start hubs; stay `SETTLE_PENDING` with no Kalshi `result`
2. `digest-figures` — generated figures half of the SOURCE digest from real files only (`python -m golf_offshoot digest-15m`). Does not write, rewrite, reorder, or drop the caveats file
3. `digestor` — human caveats turn only. Owed when `LEARNING_LANE_15M_SOURCE_DIGEST_CAVEATS.md` needs a new caveat, not on every settle. A figures-only SOURCE refresh leaves this owed
4. `operator` — Soften/park only what the spine supports; leave-off + desk to committed truth
5. `systems` — `manifest.json` merge; never drop published `paper_win`, never invent pending
6. `validator` — `python docs/observability-hub/validate_hub.py --strict --write-report` on the exact bytes about to publish; the hash-stamped report is its proof artifact
7. **publish** (gym PC only) — after the PaperWatch runner pass, `PUBLISH_ARMED` may push the hub allowlist (`manifest.json`, `paper_window_strip.png`, `validator_report.json`) to `origin/master` from a **master worktree** when `material_publish_reasons` is non-empty, `validate_hub.py --strict` is clean, `watch_is_collecting` PASS, and lineage A `ledger.json` is present. Never copy scorecards / `records[]` / fee-accurate Operator totals. Never `git push origin HEAD:master` from `cursor/honer-15m-sibling`. Cloud CoS/worker timers still do not publish. Skip a 90-second heartbeat. Never restamp an export to look fresher. Never invent. Factory merge of #178 is still a PR merge
8. `hub-ui` — only if display is wrong or stale. No number invention
9. `illustrator` — **owed by the wake** when the PNG lags live journal/settlements by more than one window (or there is no PNG and two or more windows of evidence exist). Claude Opus 5; real files only. One window of trail is allowed (the open window). Do not leave this optional. Re-render before a material publish so the board is not an hour behind the tables
10. `lab` — when `F_continuation` is owed (no live trial, no un-operated PROPOSED) **or** when `H_honer_freeze` is owed (open freeze, unproposed, consult off). One **PROPOSED** cheap test under the invent contract (mechanism catalog, density floor `10/n`, prefer HONER-FROZEN if H/Job says so, do not retune clock minute), paper-only, then `operator`. Never self-admit. Golf idle does not stop a 15m Lab assign. Honesty / hub fail is `D_hub`, not a Lab veto. H wins if both H and F. This fold does not enable consult.
11. CoS schedules the next tick. Do not ping Founder.

Nothing new on a tick: CoS posts **one** desk heartbeat line (no new settle; watch still running) and stays quiet.

### Python may not claim a role ran

The wake path detects evidence and names which roles are owed. It never writes a Digestor / Operator / Lab thread line, never Softens, and never ADMITs. The desk shows a role only when that role actually ran.

### Clerical runner (armed by `latest/RUNNER_ARMED`)

`python -m golf_offshoot learn-15m-runner` may serve **only** the named whitelist: Illustrator re-render, Systems local export, generated digest figures, and the hash-stamped Validator report. Everything else stays owed for a human. Judicial work (ADMIT, RUN-ONLY, closing a park, lifting the HOLD, Soften Critic attack, human Digestor caveats) is never on the list.

**This is a move across the trust boundary, not an append.** `validator` left `JUDICIAL_NEVER` and joined `CLERICAL_WHITELIST`. Human `digestor` left the whitelist and joined `JUDICIAL_NEVER`. Do not add `operator`, `lab`, or `soften-critic` to the whitelist. Do not put the figures generator in the `digestor` slot — that would write SOURCE every tick and clear `digestor` automatically, undoing PR #171 one layer up.

`digest-figures` proves its own work against `LEARNING_LANE_15M_SOURCE_DIGEST.md`. Human `digestor` is keyed on `LEARNING_LANE_15M_SOURCE_DIGEST_CAVEATS.md` only. A figures-only SOURCE refresh leaves `digestor` owed. A new caveat is the only write that clears it. `validator` proves against `docs/observability-hub/data/validator_report.json` (SHA-256 of the exact bytes validated).

**Invoker:** PaperWatch. Each ~90s `_cycle` runs one clerical pass after the paper tick (`watch.py` `_runner_tick` → `run_once()`). The 15m hub starts PaperWatch; a hub or PaperWatch restart starts the runner again. The standalone CLI default is the same loop until the kill file — not a finite `--passes` that quietly runs out. `--once` / `--passes` are tests/debug only. Do not run the CLI loop and the hub at the same time.

The kill switch is the file `golf-offshoot/data/learning_lane_15m/latest/RUNNER_KILL` (or `--kill-runner`). The runner **re-reads that file at the start of every pass**. Touch it to stop the runner mid-flight without touching PaperWatch. An env var is not the switch.

It goes live when `latest/RUNNER_ARMED` is present (gitignored). Serve-on-proof is real: `serve_role` runs the clerical job and calls `mark_roles_served(..., served_kind='auto')` only after the artifact **hash** changed. If the file did not move, the role stays owed and the failure is logged. A systems heartbeat (`generated_at` only) is not proof. Exit code 0 is not proof.

A role also leaves `roles_owed` when the artifact it owns changes on disk, whoever changed it. That path records `served_kind='human'`. Auto and human stay distinguishable forever. Operator clears when the method park changes. Systems clears on a material manifest fingerprint, not a heartbeat rewrite. `digest-figures` clears when SOURCE changes. Human `digestor` clears when the caveats file changes, not when SOURCE or `digest_asof.json` is rewritten. Validator clears when the hash-stamped report changes. Lab owns no artifact and stays owed until a human marks it.

`execute=True` is a scratch-tree harness only. It requires `root=` pointing off the real repo and can never serve the live tree unarmed.

**Pages publish is gym-only, material, allowlisted.** The runner still does not `git commit` or `git push`. After each PaperWatch runner pass, `PUBLISH_ARMED` (gitignored, this gym tree) may push the hub allowlist to `origin/master` from a **master worktree** when `material_publish_reasons` is non-empty. Never sibling-HEAD-to-master. Cloud CoS/worker timers do not publish. Factory merge of #178 is still a PR merge.

### Who a tick owes (severity split)

A routine settle names **only** the three clerical roles: `digest-figures`, `systems`, `validator`. The runner clears them on the next pass, so naming them costs nothing. Ninety-six windows a day across three judicial roles is roughly 288 owed turns nobody reads, and a normally-settled window owes Operator nothing.

Judicial roles are named only by their **enumerated** exception kinds, in `learning_lane_15m/triggers.py`:

| Event kind | Owes | Meaning |
|---|---|---|
| `paper_join_missing_grew` | digestor + operator | a new window has an official result and no book on this tree |
| `book_open_no_join` | digestor | a paper book is open with no settle join written |
| `window_sequence_gap` | digestor + operator | a hole in the 15-minute sequence — the `072245` shape. Never backfill |
| `settle_contradicts_book` | digestor + operator | recorded winner, pnl sign, or pnl magnitude disagree with the book's own numbers |
| `unrecorded_cost` | digestor | an Operator note measured a cost the caveats do not acknowledge |
| `park_aged` | operator | a **crew** park past its ~1 day re-rule window |
| `falsifier_fired` | operator | a falsifier fired and has not been ruled |
| `rule_reached_n` | operator | a declared rule has accumulated the n its falsifier named |
| `lab_proposed` | operator | a Lab PROPOSED arrived |
| `artifact_unreviewed` | critic-invariants + soften-critic | a watched method artifact changed and no Critic finding covers that hash |

Human `digestor` is owed when the **generated figures cannot express what changed** — not zero, and not every settle. The every-settle trigger is deliberately not restored.

Pre-split leftover `new_settle` / `new_fill` / `pending_cleared` reasons on `digestor` and `operator` are dropped by `rekey_leftover_owed` on the next tick. Those roles stay owed only on the exception list above. `critic_findings_failing` pages Operator only on a *new* failing set, or on a failing check the bar does not already name with a reason.

**Do not silently drop an exception class to shorten the owed list.** If it is unclear whether something belongs to Operator, it stays owing Operator and the reason is written down.

**Operator no longer clears on any park write.** `operator_write_addresses_owed` is shaped like `material_publish_reasons`: a park change clears Operator only when the new text names what Operator was owed for. If the owed line names no reason, or the park file cannot be read, Operator **stays owed**. #174 edited the park to reconcile the Soften Critic Hard NO lists and cleared an Operator line raised by settles on 080745 through 080830 that nothing had ruled on. That cannot happen again.

### The Critic has a body

Split the same way Digestor was split.

- **`critic-invariants`** — deterministic checker over the method artifacts, in `learning_lane_15m/critic.py`. **On `CLERICAL_WHITELIST`.** Proof artifact is `golf-offshoot/docs/LEARNING_LANE_15M_CRITIC_FINDINGS.json`, hashed like any other. Serve-on-proof clears it only when that file moves.
- **`soften-critic`** — the adversarial analysis turn. Stays in `JUDICIAL_NEVER`. A written attack is not hash-provable and is never auto-served. It must run in a session separate from whichever session authored the thing it attacks, and Operator's answers must be a separate turn from the objections. One turn may not both object and dismiss.

The trigger is the **repo-side event class**: a watched artifact's hash changed and no Critic finding exists for that hash. Watched: the evidence bar (both files), the rule registry, the Lab PROPOSED note, and the honesty-gate stamp section of DESK.md. The findings file is keyed by content hash, so editing a bar re-owes the Critic on the new text and cannot be cleared by editing something else.

**Critic objections meet the same bar as a Lab PROPOSED: specific and falsifiable.** "Let us be careful" is not an objection. A padded finding teaches Operator to route around the Critic.

Two guards exist because the Critic's first attack found them missing in the Critic's own body:

- **A failing report does not clear what it found.** `critic-invariants` clears on serve-on-proof like any clerical role, so a report reading *the bar fails four checks* cleared exactly as a clean one would, and the desk read that as clearance. A findings artifact with `passed: false` now raises `critic_findings_failing`, which owes **Operator** — the failing checks are properties of the bar, and the bar is Operator's. A failing method check cannot be retired by the machine that found it.
- **A heartbeat is not proof, for this role either.** The findings payload stamps `ran_at` on every pass, so the raw file hash moved every tick whether or not a verdict moved. `_critic_token` fingerprints the `checks` block and `passed`, not the clock — the same guard `material_publish_reasons` already gave Systems.

A detector that fails to read its evidence raises `detector_blind` to Operator. **A suite that cannot run is a failure, never a silent pass** — including the Critic's own repo scan, which previously swallowed its exception and reported no events, leaving the Critic quietly un-owed.

### Invariants (the ratchet)

`golf-offshoot/src/golf_offshoot/learning_lane_15m/invariants.py`. Every flaw found by analysis becomes a permanent check here, so it cannot recur silently. A finding that does not produce a check is a finding that will be rediscovered by hand.

The suite runs on every watch cycle **after** the clerical runner has had its pass, writes `golf-offshoot/data/learning_lane_15m/latest/invariants.json`, and prints its verdicts on `learn-15m`. A failing check names itself on the tick. **A failing invariant is never satisfied by prose** — it passes because a file says so, or it does not pass. A suite that cannot run is itself a failure, never a silent pass.

Seeded with the four that were live and invisible on 2026-09-08:

| Check | Fails when |
|---|---|
| `digest_matches_ledger` | the SOURCE digest headline `bankroll` / `betting_pnl` differ from the live ledger. Regenerate through `digest-figures`; never hand-edit the figures to clear it |
| `process_matches_disk` | the running loop's `ROLE_ORDER` / `CLERICAL_WHITELIST` / `JUDICIAL_NEVER` differ from the code on disk, or the watch has stamped no runtime config at all. A stale process is an honesty defect, not a freshness one: roles silently stop self-serving while the desk looks normal |
| `watch_is_collecting` | the watch claims `running` but its last cycle is older than three intervals. A re-exec that never comes back resets the counter and stops collection with no other symptom |
| `clerical_roles_clear` | a **whitelisted** role has been owed longer than two ticks. A clerical role that cannot clear itself is either broken or misfiled as clerical. Judicial roles sitting owed are not arrears — that is what they are for |

Adding a check is Founder-free. **Removing or weakening one is not.**

A second suite runs over the **method** artifacts and is owned by `critic-invariants` (`learning_lane_15m/critic.py`). Its artifact is `LEARNING_LANE_15M_CRITIC_FINDINGS.json` and it also prints on the tick: `matched_exposure_control`, `delta_above_detection_floor`, `holdout_is_forward_only`, `fee_adjusted_book_is_binding`, `declared_at_precedes_scored_windows`, `trials_counter_is_consistent`, `fee_schedule_hash_recorded`, `series_fee_regime_matches`, `bind_has_no_founder_read_once`, `honesty_stamp_is_fresh`. A checker cannot find an unknown failure mode, which is exactly why the ratchet exists: **every flaw analysis finds becomes a permanent check.** A finding that does not produce a check is a finding that will be rediscovered by hand.

### Honesty gate: derived, not typed

Three of the four boxes are computed from files in `learning_lane_15m/honesty.py`, and the **derived verdict wins** — desk prose can shut a derived box, never open one. A derived box deleted from the desk is still evaluated, so removing a row cannot open the gate.

| Box | Source |
|---|---|
| lineage readable, dual lineage labeled not merged | **derived** from the scan: lineage A ledger present, lineage B kept as `published_only` rows, no combined figure |
| `KXBTC15M-26SEP071500-00` honestly joined or pending with a true reason | **derived** from the scan: not on the pending list, and no missing-join row carries a pnl |
| one hub process | **derived** from the process table: exactly one hub **tree**. The criterion is preserved as written — a supervisor plus its child is one hub, not two |
| no invented charts or pnl | **judgment** — must carry evidence |

A judgment box now needs `**PASS**` **and** evidence: a PID, a file hash, or a timestamp. **A stamp with no evidence attached does not open the gate.** The parser was not widened to accept more phrasings — it was narrowed.

### Auto-reload is load-bearing

The hub re-execs its child when `git_tip` or a watched module's mtime moves (`operator_surface/reload.py`). Watched code is `operator_surface/*.py`, `learning_lane_15m/*.py`, `__main__.py`, `audit/shadow_settle.py`. The lane package is on that list because PaperWatch and the clerical runner run **inside** the hub process: a merge that only touches the lane must still re-exec.

`git_tip` resolves branch SHAs through the worktree `commondir`. Without that, a linked worktree reads every branch SHA as empty, so a commit on the current branch looks like no change and nothing re-execs. `process_matches_disk` is the check that catches it if this regresses.

### Honesty gate is not a Lab veto

Three of the four boxes are derived (`learning_lane_15m/honesty.py`). A failing hub tree is `D_hub`: CoS assigns Digestor/Operator for honesty, but **does not** hold Lab when `F_continuation` or `H_honer_freeze` is owed. Hub fail is an ops doorbell, not a Founder-shaped invent stop.

### Operator verdicts (claims vs arithmetic)

Operator has **three** verdicts on a Lab PROPOSED. Lab, CoS, and the wake issue none of them.

| Verdict | Authorizes | Forbids | Where the output lives |
|---|---|---|---|
| **ADMIT** | A dated claim | Nothing about the claim once dated | Dated record. Still requires a real dated result. `lab_admits=false` |
| **RUN-ONLY** | Execution | Claiming. Never becomes an ADMIT by accumulation | An Operator note only. Never `manifest.json`, never the digest, never the hub, never `records[]`, never a dated record |
| **PARK** | Waiting | Execution and claiming | Method park, with a trigger class |

Promotion from RUN-ONLY to a claim uses the normal ADMIT gate, exactly as strict as today. A falsifier firing is a **complete, successful outcome**: record it as a park closed on that falsifier. Do not delete it silently. Do not score a dead test as a failed turn. If that rule still has `execution: true`, Operator drops `execution` in the score turn so a dead skip does not own the next trial. Only one selecting rule may execute.

The method gates **claims**, not arithmetic. "Cannot admit" is not "cannot compute."

### CoS routing for a PROPOSED

Route a PROPOSED to **RUN-ONLY** rather than park when all four hold, unless Operator names a **specific** objection:

1. Deterministic — no new data collection, no waiting to accumulate n
2. Adds no code to the running loop
3. Output is quarantined to an Operator note
4. It carries at least one live falsifier

"Let us be careful" is not an objection. "That document read is outside public-read-only posture" is. A well-falsified cheap test is easier to authorize than a vague one. A test pre-committed to dying is the safest thing available to authorize.

### Park trigger classes

Every park row is stamped with exactly one class:

| Class | Meaning |
|---|---|
| **crew** | The crew can make the trigger fire on this tree |
| **external** | Needs an outside event or a recovery outside crew control |
| **founder** | Founder alone |
| **unreachable** | Cannot fire, ever. These are renamed **CLOSED** with the reason and are not listed as open parks |

A park whose trigger can never fire is a rejection wearing a deferral's clothes. That is an honesty defect.

### Park aging (re-rule, never a forced conclusion)

Any **crew** park that has not been re-ruled within roughly one day of active loop returns to Operator for **one line**: restate the trigger, reclassify it, or close it. Restating is legitimate. Silence is what is ruled against, not deferral. Never pressure a role toward a verdict.

**external** and **founder** rows age without pressure. They are not the crew's to fire.

### Park ledger

Systems owns the counts. The ledger is an honesty instrument, not a productivity metric: total open parks, count in each class, how many triggers fired since the last stamp, how many closed on a falsifier. If nothing has fired in a long stretch, that stays visible. Validator checks the framing does not read as progress theater.

## Routing

| Job | Role | Then |
|-----|------|------|
| Route / ask Founder / update leave-off | `chief-of-staff` | — |
| 15m ingest / paper / settle | `lane-15m` | `systems` |
| Write `manifest.json` / export | `systems` | `validator` |
| Hub chrome, tabs, enlarge, copy | `hub-ui` (Claude Opus 5 when the job is a chart/board) | `validator` |
| `validate_hub.py` + Hard-NO language | `validator` | CoS |
| Soften / dated-record ADMIT / RUN-ONLY / park class / stamp | `operator` | Digestor or Illustrator if needed. A proposed ADMIT or a bar that wants to bind goes through `soften-critic` first, in a **separate session**. |
| Attack a proposed ADMIT or the 15m evidence bar | `soften-critic` | `operator` — Operator records each objection and answers it in the admit pass |
| Invent / cheap-test (never admit) | `lab` | `operator` |
| SOURCE honesty / living spine | `digestor` | `operator` |
| Charts from real files only | `illustrator` (**Claude Opus 5**) | `hub-ui` or `validator` |

## Soften Critic

**Hired 2026-09-08.** Skill: `.cursor/skills/gpf-soften-critic/SKILL.md`.

Its job is to attack a proposed ADMIT — and the 15m evidence bar — in writing, before Operator stamps. No authorship stake: it may not propose rules, may not score, may not ADMIT, may not park. It objects, with reasons.

It must run as a session separate from whichever session proposed or scored the thing it is attacking. Operator must record each objection and answer it in the admit pass, not route around it.

Do not add this role to `CLERICAL_WHITELIST`. A written attack is not hash-provable. `JUDICIAL_NEVER` stays. `lab_admits=false` already runs with two bots. This is the third.
