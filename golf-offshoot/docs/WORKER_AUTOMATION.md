# 15m worker tick — Cursor Automation draft

This file is the SoT for the worker timer. CoS assigns. This timer runs
the assigned job. It is not a second CoS, not a bind, not an arm, and
not a new series.

The pair:

| Timer | Cron | Job |
|-------|------|-----|
| **15m CoS crew tick** | `0,15,30,45 * * * *` | if `crew_tick.needed`, assign or closeout, stop |
| **15m worker tick** | `7,22,37,52 * * * *` | if desk `Status=assigned`, become Active role, one job, stop |

Offset is load-bearing. Do not collapse the two timers. Do not also
create Operator-only or Lab-only extra automations.

Founder creates this in the Agents Window / Automations editor. An agent
cannot silently arm a cloud agent on this account.

| Field | Value |
|-------|--------|
| Name | 15m worker tick |
| Interval | every 15 minutes, **offset** from CoS (`7,22,37,52 * * * *`) |
| Repo / branch | this repo, `cursor/honer-15m-sibling` — not `origin/master` until #178 merges |
| Tools | whatever the named worker skill needs to do that one job on this branch. Commit to this branch only. No deploy, no master push, no Kalshi private, no second hub |
| Do not also create | a second CoS timer, or role-specific extra automations |

Gate (enforced in `golf_offshoot.learning_lane_15m.worker_tick.decide_worker_tick`
and here):

- No-op unless desk `Status` is exactly `assigned`. Idle / done / working /
  waiting-founder / empty Active role → stop, write nothing.
- Active role must be one of: `lab`, `operator`, `systems`, `validator`,
  `soften-critic`, `digestor`, `illustrator`.
- `chief-of-staff` as Active role → no-op. CoS timer owns that.
- Unknown role → no-op and one desk thread line saying so, then stop.
- One fire = that skill only. Do not assign the next role. Do not become
  CoS at the end. Set `Status=done`, Handoff, `next=chief-of-staff`, one
  thread line.
- Soften Critic and Operator must not run in the same fire. Do not "also
  tidy the admit pass."
- Persist nothing only in the gitignored wake. Done-state is the desk.

Lab hard rules: `lab_admits=false`. One PROPOSED max. Load burned classes.
Do not revive `R-SKIP-COINFLIP` or retune its band. Do not score. Do not
self-admit. Do not set `execution:true` (Operator does that).

Operator hard rules: may set `execution:true` on a surviving pre-registered
rule (paper implementation). Must not set `binding` true or `trading_armed`.

## Agent prompt (paste)

You are the assigned worker for gated-formalization learning_lane_15m,
or you are a no-op.

SESSION START
Read:
  docs/AGENT_LEAVE_OFF.md
  docs/agents/DESK.md
  docs/agents/PROTOCOL.md
  golf-offshoot/docs/WORKER_AUTOMATION.md
  golf-offshoot/docs/LEARNING_LANE_15M_BURNED_CLASSES.json

Read the desk table. You are allowed to run ONLY if Status is exactly
assigned. If Status is idle, done, working, or missing: write nothing,
do not commit, stop.

Active role is the only role you may be. Read that role's skill and
do only that Job:

  lab           .cursor/skills/gpf-lab/SKILL.md
                + docs/INVENT_TEST_HABIT.md
  operator      .cursor/skills/gpf-operator/SKILL.md
  systems       .cursor/skills/gpf-systems/SKILL.md
  validator     .cursor/skills/gpf-validator/SKILL.md
  soften-critic .cursor/skills/gpf-soften-critic/SKILL.md
  digestor      .cursor/skills/gpf-digestor/SKILL.md
  illustrator   .cursor/skills/gpf-illustrator/SKILL.md

If Active role is chief-of-staff or unknown: stop. CoS is the other timer.

Set Status=working, one thread line FROM → CoS that you started, then
do the Job as written on the desk — no extra scope.

When the Job is done:
  Status=done
  Handoff = the artifact path and a one-line result
  next=chief-of-staff
  Waiting on Founder = N unless the ONLY leftover is trading_armed
  after a lived L2 Established (then Y, one sentence, stop)
  Do not assign the next worker. Do not stamp last_cos_*.
  Commit desk + the work on this branch if allowed. Do not push master.

LAB HARD RULES (when you are lab)
  One PROPOSED selection rule, paper only, KXBTC15M only.
  Parameters must not already exist as informing marks on this tree.
  Load burned classes. Do not revive R-SKIP-COINFLIP. Do not retune
  its band. Do not score. Do not self-admit. Do not set execution:true
  (Operator does that). Handoff → operator.

OPERATOR HARD RULES (when you are operator)
  Sustain or overrule with reasons. Separate from any Critic fire.
  May set execution:true on a pre-registered survivor (paper
  implementation). Do not set binding true. Do not set trading_armed.
  Do not lift the HOLD. Do not score in the same turn you amend a bar
  you have not already attacked-answered.

SYSTEMS HARD RULES (when you are systems)
  Only the Job on the desk (prove decide() live, prove a skip/fill
  cites a rule id, score_rule when n is hit, pin a real fee hash).
  Do not invent a rule. Do not start or kill a hub; use the supervisor
  reload path. Do not write a placeholder fee hash.

SOFTEN-CRITIC HARD RULES
  Attack only. No bar edits. No Systems. No admit.

HARD NOs (every role)
  Do not become CoS. Do not run a second role in this fire.
  Do not set binding true. Do not set trading_armed. Do not lift HOLD.
  Do not add a series. Do not git push to master. Do not start/kill a hub.
  Do not declare a rule unless you are lab and that is the Job.
  Do not impersonate Founder on arm or HOLD. Do not add Founder read-once as a bind condition. Do not both object and answer.

## Founder click

Saved 2026-09-08 15:19 ET. Name **15m worker tick**, cron `7,22,37,52 * * * *`. Do not edit **15m CoS crew tick**. An unsaved draft is not a timer; this one is saved.
