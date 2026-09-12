# 15m worker tick — file SoT

This file is SoT for **15m worker tick**
(`a78779fc-abb9-11f1-b532-320a589b8025`). CoS assigns. This timer runs the
assigned job. Cloud ticks checkout `cursor/honer-15m-sibling` (#178).
There is **no** Automations paste PATCH. **This file wins** over a stale
Automations-editor paste.

Do not ask M3SS to Save. Do not create a third automation, or role-specific
extra automations. Never `origin/master`. Never gym 8765. Never attach gym
CoS `91e26eab-eb97-4901-80f1-ae836a17325b`. Trading **NOT ARMED**.

The pair:

| Timer | Cron | Job |
|-------|------|-----|
| **15m CoS crew tick** | `0,15,30,45 * * * *` | if `crew_tick.needed`, assign or closeout, stop |
| **15m worker tick** | `7,22,37,52 * * * *` | if desk `Status=assigned`, become Active role, one job, stop |

Offset is load-bearing. Do not collapse the two timers.

| Field | Value |
|-------|--------|
| Name | 15m worker tick |
| UUID | `a78779fc-abb9-11f1-b532-320a589b8025` |
| Interval | every 15 minutes, **offset** from CoS (`7,22,37,52 * * * *`) |
| Repo / branch | this repo, `cursor/honer-15m-sibling` — never `origin/master` |

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

**CoS-seated F/I invent — no-op.** If Active role is `lab` and the Job is
one 15m PROPOSED because CoS seated `F_continuation` / `I_farm_open`
invent (needles: `one 15m PROPOSED under the invent contract`,
`continuation_assign_lab`, `starved gym`, `F_continuation`, `date every
currently legal unused catalog slot as farm notebooks`, `I_farm_open`,
`farm_open_assign_lab`, `invent the next kind`, `LEARNING_LANE_15M_FARM_MENU_EXHAUSTED.json so I stops`):
do **not** write a PROPOSED, do not date a family, do not press invent.
`Status=done`. Handoff: CoS-seated F/I invent is the gym leash / files
(#195, gym `1c72ad0`), not this cloud fire; Lab not pressed.
`next=chief-of-staff`. Persist that desk handoff on honer only. Do not
push master.

Still run Lab when the Job is a **method** fire already owed on the desk
(HONER-FROZEN-REPLACE photocopy after consult has lived; Lab refusal stands).
Dated PROPOSED hygiene is Operator, not Lab. Search park (#193) is not a
Lab job. `family_amend.json` owed is not a cloud-worker Lab seat.

Lab hard rules (when you actually run Lab): `lab_admits=false`. One
PROPOSED per fire. Invent contract in the note: kill anatomy, unburned
mechanism (load burned classes + LEARNING_LANE_15M_MECHANISM_CATALOG.json),
density floor 10/n from the 15m quartet, HONER-FAMILY-AMEND only after a
dead honer exam or catalog exhaust (no third family until the two dated
families finish exams), HONER-FROZEN-REPLACE only after consult has lived
and hour-close is not the live trial (photocopy freeze knobs; do not retype
θ), pre-reg, live falsifier. Do not retune skip_close_minute /
RETUNE-CLOCK-MINUTE. Do not revive `R-SKIP-COINFLIP` or retune its band. Do
not retune PARK'd `favorite_odds`. Golf idle does not stop a 15m KXBTC15M
paper **method** Job. Do not score. Do not self-admit. Do not set
`execution:true` (Operator does that). Consult enable is a file gate, not
this Lab job.

Operator hard rules: may set `execution:true` on a surviving pre-registered
rule (paper implementation). A falsifier PARK of an executing selection rule
drops `execution` in that score turn. The next RUN-ONLY takes the only
selecting seat. Must not set `binding` true or `trading_armed`. A
KXBTC15M paper PROPOSED is not golf idle-breach. When the Job is PARK or
CONTINUE from the L1 scorecard: read the pushed
`LEARNING_LANE_15M_SCORECARD_{id}_L1.json`. Never invent tape. No card → do not
park, do not score, do not invent windows (handoff no-card). PARK drops
execution; CONTINUE leaves it. Do not stop PaperWatch at 70. Look owner is
Operator, not Systems.

## Thin live paste (pointer)

Checkout branch cursor/honer-15m-sibling before you read the desk. Fetch and
pull that branch first. Do not use master. Do not use origin/master. Do not
use cursor/part-a-clerical-trust-boundary. If Cursor booted a new cursor/…
branch, check out honer-15m-sibling; if you are not on that branch, stop.
Write nothing. Do not commit.

Read golf-offshoot/docs/WORKER_AUTOMATION.md on that checkout. Follow it. This
file is SoT.

## Agent prompt (what to do)

You are the assigned worker for gated-formalization learning_lane_15m,
or you are a no-op.

SESSION START
Read:
  golf-offshoot/docs/WORKER_AUTOMATION.md
  docs/AGENT_LEAVE_OFF.md
  docs/agents/DESK.md
  docs/agents/PROTOCOL.md
  golf-offshoot/docs/LEARNING_LANE_15M_BURNED_CLASSES.json
  golf-offshoot/docs/LEARNING_LANE_15M_MECHANISM_CATALOG.json

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

COS-SEATED F/I INVENT (when you are lab): if the Job is one 15m PROPOSED
because CoS seated F_continuation / I_farm_open invent (needles in the
gate section above): no-op invent. Status=done. Handoff CoS. Do not
write a PROPOSED. Invent is the gym leash / files, not this cloud fire.

Set Status=working, one thread line FROM → CoS that you started, then
do the Job as written on the desk — no extra scope. Skip working if the
F/I invent no-op already closed the Job.

When the Job is done:
  Status=done
  Handoff = the artifact path and a one-line result
  next=chief-of-staff
  Waiting on Founder = N unless the ONLY leftover is trading_armed
  after a lived L2 Established (then Y, one sentence, stop)
  Do not assign the next worker. Do not stamp last_cos_*.
  Commit desk + the work on this branch if allowed. Do not push master.

LAB HARD RULES (when you are lab and the Job is a method fire, not F/I invent)
  One PROPOSED selection rule, paper only, KXBTC15M only.
  Golf idle ON does not stop a method Job. This is not golf WC3+.
  The PROPOSED note itself must contain:
    1. Kill anatomy — quote the last closed score/park (clauses, skip_count).
       Favorite L1: n=70, skip_count=1, clauses 1/4/5 fail. Not a favorite_odds
       retune and not a tape quantile (burned). Do not retune skip_close_minute
       (RETUNE-CLOCK-MINUTE is burned).
    2. Unburned mechanism — load LEARNING_LANE_15M_BURNED_CLASSES.json and
       LEARNING_LANE_15M_MECHANISM_CATALOG.json. Skip-on-mark families that only
       move the same cut are retunes. HONER-FROZEN-CONSULT is not a Lab invent
       (freeze bytes are the name; clerical copies the snapshot). HONER-FAMILY-AMEND
       dates a third honer family only after a dead exam or catalog exhaust; do
       not tape-sort; do not append until the two dated families finish exams.
       HONER-FROZEN-REPLACE photocopies freeze knobs as the executing row after
       consult has lived and hour-close is not live; Operator RUN-ONLY; not Founder;
       not arm. Do not retype freeze theta.
    3. Pre-registration — parameters must not be informing marks on this tree.
       declare_rule density: expected_skip_rate from the 15m quartet, floor 10/n.
    4. Live falsifier — n and a park instruction, no retune-if-dead.
  Do not revive R-SKIP-COINFLIP. Do not retune its band. Do not score.
  Do not self-admit. Do not set execution:true (Operator does that).
  Consult enable is a file gate, not this Lab job.
  Handoff → operator.

OPERATOR HARD RULES (when you are operator)
  Sustain or overrule with reasons. Separate from any Critic fire.
  May set execution:true on a pre-registered survivor (paper
  implementation). Only one selecting rule may have execution:true.
  A falsifier PARK drops that row's execution. The next RUN-ONLY takes
  the only seat (dead row off, new row on).
  A KXBTC15M paper PROPOSED is not golf idle-breach.
  When the Job is PARK or CONTINUE from an L1 card: read
  LEARNING_LANE_15M_SCORECARD_{id}_L1.json. Never invent tape. No card →
  no-card, do not park. PARK drops execution; CONTINUE leaves it. Do not
  stop PaperWatch at 70.
  Do not set binding true. Do not set trading_armed.
  Do not score in the same turn you amend a bar
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
  Do not score R-SKIP-COINFLIP. Do not re-score PARK'd R-SKIP-2TO1-FAVORITE.
  Naming rule_reached_n on the park without scoring is allowed bookkeeping.
  Do not declare a rule unless you are lab and that is a method Job.
  Do not impersonate Founder on arm or HOLD. Do not add Founder read-once as a bind condition. Do not both object and answer.
  Do not land #194. Do not merge #178 or #177 onto master.
