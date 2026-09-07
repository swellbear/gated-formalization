# Agent communication protocol

Chat is not memory. Roles talk through **[DESK.md](DESK.md)** and **[AGENT_LEAVE_OFF.md](../AGENT_LEAVE_OFF.md)**. Founder (the user) is the only GO.

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

Ask **one** question, then wait. Do not guess.

- Hire Soften Critic
- C2 / C4 / TABLE / reopen WC3+
- Expand past `KXBTC15M`
- Arm trading, cash, Kalshi keys
- Put golf WC1 / Ill on the 15m lane
- Invent win/lose or treat DIY CFB as official settle
- Anything **not** on leave-off “Next”

## Routing

| Job | Role | Then |
|-----|------|------|
| Route / ask Founder / update leave-off | `chief-of-staff` | — |
| 15m ingest / paper / settle | `lane-15m` | `systems` |
| Write `manifest.json` / export | `systems` | `validator` |
| Hub chrome, tabs, enlarge, copy | `hub-ui` | `validator` |
| `validate_hub.py` + Hard-NO language | `validator` | CoS |
| Soften / dated-record ADMIT / stamp | `operator` | Digestor or Illustrator if needed |
| Invent / cheap-test (never admit) | `lab` | `operator` |
| SOURCE honesty / living spine | `digestor` | `operator` |
| Charts from real files only | `illustrator` | `hub-ui` or `validator` |

## Soften Critic

**Not hired.** Do not invent that role.
