# Agent communication protocol

Chat is not memory. Roles talk through **[DESK.md](DESK.md)** and **[AGENT_LEAVE_OFF.md](../AGENT_LEAVE_OFF.md)**.

**Chief of Staff keeps the track moving.** Founder is only for a rare review or a real change of direction. Do not ping Founder to approve work that is already on leave-off “Next” or that stays inside the Hard NOs.

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

- Hire Soften Critic
- C2 / C4 / TABLE / reopen WC3+
- Expand past `KXBTC15M` or retune golf θ
- Arm trading, cash, Kalshi keys
- Change a Hard NO, or put golf WC1 / Ill on the 15m lane
- A new dated-record ADMIT / REJECT that would rewrite the Operator stamp
- A Validator fail that is not a simple writer fix (honesty / method conflict)

Do **not** ask (CoS just does it):

- Leave-off “Next” items
- Start or continue the 15m paper watch
- `lane-15m` → `systems` → `validator` when a Kalshi `result` exists
- Stay `SETTLE_PENDING` when it does not (never invent win/lose)
- Desk / leave-off bookkeeping
- Chrome-only Hub UI inside existing Hard NOs
- Commit / push of a valid observability export so Pages can update
- Ask Founder to click ingest / live / loop / publish

## Keep-looping (15m)

While the desktop hub is on `learning_lane_15m`, **PaperWatch** repeats the researcher/export half. Founder observes. Founder does not operate.

PaperWatch alone is **not learning.** Learning has not begun until settled outcomes are digested on a schedule and change what the crew does next.

### Learning tick (new official settle, new paper fill, or a pending cleared)

1. `lane-15m` — confirm watch healthy; do not double-start hubs; stay `SETTLE_PENDING` with no Kalshi `result`
2. `digestor` — SOURCE honesty digest for this lane from real files only (settled vs pending, lineage A vs published Pages if still split)
3. `operator` — Soften/park only what the spine supports; leave-off + desk to committed truth
4. `systems` — `manifest.json` merge; never drop published `paper_win`, never invent pending
5. `validator` — `python docs/observability-hub/validate_hub.py --strict` on the exact bytes about to publish
6. **publish** (standing tick step, not a project) — Systems owns `observability-export` → re-render the current real PNG → `validate_hub.py --strict` on those bytes → commit → push to `master` so Pages updates. Publishing is part of the tick, not a later event. Skip only a 90-second PaperWatch heartbeat that did not fire this learning tick. Never restamp an export to look fresher. Never invent. Use `material_publish_reasons` when deciding a heartbeat is empty. Do **not** leave a corrected falsehood unpublished. The public page reads `master` only
7. `hub-ui` — only if display is wrong or stale. No number invention
8. `illustrator` — **owed by the wake** when the PNG lags live journal/settlements by more than one window (or there is no PNG and two or more windows of evidence exist). Claude Opus 5; real files only. One window of trail is allowed (the open window). Do not leave this optional. Re-render before a material publish so the board is not an hour behind the tables
9. `lab` — only after Operator posts a clear residual **and** the honesty checklist passes. One **PROPOSED** cheap test, paper-only, then `operator`. Never self-admit
10. CoS schedules the next tick. Do not ping Founder.

Nothing new on a tick: CoS posts **one** desk heartbeat line (no new settle; watch still running) and stays quiet.

### Python may not claim a role ran

The wake path detects evidence and names which roles are owed. It never writes a Digestor / Operator / Lab thread line, never Softens, and never ADMITs. The desk shows a role only when that role actually ran.

### Clerical runner (armed by `latest/RUNNER_ARMED`)

`python -m golf_offshoot learn-15m-runner` may serve **only** the named whitelist: Illustrator re-render, Systems local export, Digestor digest. Everything else stays owed for a human. Judicial work (ADMIT, RUN-ONLY, closing a park, lifting the HOLD) is never on the list.

**Invoker:** PaperWatch. Each ~90s `_cycle` runs one clerical pass after the paper tick (`watch.py` `_runner_tick` → `run_once()`). The 15m hub starts PaperWatch; a hub or PaperWatch restart starts the runner again. The standalone CLI default is the same loop until the kill file — not a finite `--passes` that quietly runs out. `--once` / `--passes` are tests/debug only. Do not run the CLI loop and the hub at the same time.

The kill switch is the file `golf-offshoot/data/learning_lane_15m/latest/RUNNER_KILL` (or `--kill-runner`). The runner **re-reads that file at the start of every pass**. Touch it to stop the runner mid-flight without touching PaperWatch. An env var is not the switch.

It goes live when `latest/RUNNER_ARMED` is present (gitignored). Serve-on-proof is real: `serve_role` runs the clerical job and calls `mark_roles_served(..., served_kind='auto')` only after the artifact **hash** changed. If the file did not move, the role stays owed and the failure is logged. A systems heartbeat (`generated_at` only) is not proof. Exit code 0 is not proof.

A role also leaves `roles_owed` when the artifact it owns changes on disk, whoever changed it. That path records `served_kind='human'`. Auto and human stay distinguishable forever. Operator clears when the method park changes. Systems clears on a material manifest fingerprint, not a heartbeat rewrite. Validator and Lab own no artifact and stay owed until a human marks them.

`execute=True` is a scratch-tree harness only. It requires `root=` pointing off the real repo and can never serve the live tree unarmed.

**Publish is still manual.** The runner exports locally. It does not `git commit` or `git push`. The public page is **not** self-maintaining. That is the same defect that left Pages stale for six hours. A local export is not a publish. Systems still owns the standing tick step: material export → `--strict` → commit → push to `master`. Do not assume the public page moved because the runner ran.

### Honesty gate before Lab invents

CoS stamps these on the desk first. Any box failing ⇒ `digestor` + `operator` fix honesty and Lab stays idle.

- One readable lineage story, or an explicitly labeled dual lineage — never a silent merge
- `KXBTC15M-26SEP071500-00` honestly joined, or pending with its true reason (original book not on this tree / no invent)
- No invented charts or pnl
- One hub process for `learning_lane_15m`

### Operator verdicts (claims vs arithmetic)

Operator has **three** verdicts on a Lab PROPOSED. Lab, CoS, and the wake issue none of them.

| Verdict | Authorizes | Forbids | Where the output lives |
|---|---|---|---|
| **ADMIT** | A dated claim | Nothing about the claim once dated | Dated record. Still requires a real dated result. `lab_admits=false` |
| **RUN-ONLY** | Execution | Claiming. Never becomes an ADMIT by accumulation | An Operator note only. Never `manifest.json`, never the digest, never the hub, never `records[]`, never a dated record |
| **PARK** | Waiting | Execution and claiming | Method park, with a trigger class |

Promotion from RUN-ONLY to a claim uses the normal ADMIT gate, exactly as strict as today. A falsifier firing is a **complete, successful outcome**: record it as a park closed on that falsifier. Do not delete it silently. Do not score a dead test as a failed turn.

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
| Soften / dated-record ADMIT / RUN-ONLY / park class / stamp | `operator` | Digestor or Illustrator if needed |
| Invent / cheap-test (never admit) | `lab` | `operator` |
| SOURCE honesty / living spine | `digestor` | `operator` |
| Charts from real files only | `illustrator` (**Claude Opus 5**) | `hub-ui` or `validator` |

## Soften Critic

**Not hired.** Do not invent that role.
