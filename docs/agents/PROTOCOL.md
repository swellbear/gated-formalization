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
5. `validator` — `python docs/observability-hub/validate_hub.py --strict`
6. `hub-ui` — only if display is wrong or stale. No number invention
7. `illustrator` — only if real join/journal files can drive a PNG; else leave the prior real board
8. `lab` — only after Operator posts a clear residual **and** the honesty checklist passes. One **PROPOSED** cheap test, paper-only, then `operator`. Never self-admit
9. CoS schedules the next tick. Do not ping Founder.

Nothing new on a tick: CoS posts **one** desk heartbeat line (no new settle; watch still running) and stays quiet.

### Python may not claim a role ran

The wake path detects evidence and names which roles are owed. It never writes a Digestor / Operator / Lab thread line, never Softens, and never ADMITs. The desk shows a role only when that role actually ran.

### Honesty gate before Lab invents

CoS stamps these on the desk first. Any box failing ⇒ `digestor` + `operator` fix honesty and Lab stays idle.

- One readable lineage story, or an explicitly labeled dual lineage — never a silent merge
- `KXBTC15M-26SEP071500-00` honestly joined, or pending with its true reason (original book not on this tree / no invent)
- No invented charts or pnl
- One hub process for `learning_lane_15m`

## Routing

| Job | Role | Then |
|-----|------|------|
| Route / ask Founder / update leave-off | `chief-of-staff` | — |
| 15m ingest / paper / settle | `lane-15m` | `systems` |
| Write `manifest.json` / export | `systems` | `validator` |
| Hub chrome, tabs, enlarge, copy | `hub-ui` (Claude Opus 5 when the job is a chart/board) | `validator` |
| `validate_hub.py` + Hard-NO language | `validator` | CoS |
| Soften / dated-record ADMIT / stamp | `operator` | Digestor or Illustrator if needed |
| Invent / cheap-test (never admit) | `lab` | `operator` |
| SOURCE honesty / living spine | `digestor` | `operator` |
| Charts from real files only | `illustrator` (**Claude Opus 5**) | `hub-ui` or `validator` |

## Soften Critic

**Not hired.** Do not invent that role.
