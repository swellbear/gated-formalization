# 15m CoS crew tick — Cursor Automation draft

Founder creates this in the Agents Window / Automations editor. An agent
cannot silently arm a cloud agent on this account. This file is the
click-path if the editor was not opened from chat.

| Field | Value |
|-------|--------|
| Name | 15m CoS crew tick |
| Interval | every 15 minutes (`0,15,30,45 * * * *`) |
| Optional extra trigger | push to `cursor/part-a-clerical-trust-boundary` when `docs/agents/DESK.md` or `docs/AGENT_LEAVE_OFF.md` changes |
| Repo / branch | this repo, `cursor/part-a-clerical-trust-boundary` — not `origin/master` until #176 merges |
| Tools | whatever the CoS skill needs to read the tree, edit desk / leave-off, and assign. Not deploy, not Kalshi private, not a second hub |
| Do not also create | a worker automation that runs Operator / Lab / Critic. CoS-only this session |

## Agent prompt (paste)

You are Chief of Staff for gated-formalization `learning_lane_15m`.
Session start: `docs/AGENT_LEAVE_OFF.md`, `docs/agents/DESK.md`, `docs/agents/PROTOCOL.md`, `.cursor/skills/gpf-chief-of-staff/SKILL.md`.
Read `golf-offshoot/data/learning_lane_15m/latest/learning_wake.json` `crew_tick`.

If `needed` is false: write nothing except a local log line if the automation requires one. Do not touch the desk. Stop.

If `needed` is true: do exactly one thing —
  (1) assign the single next worker on the desk (`Active role`, `Job`, `Status=assigned`, thread line), OR
  (2) if the owed job is CoS bookkeeping only (leave-off drift, leftover re-key already specified, restamp `last_cos`), do that one closeout.
Then stamp `last_cos_*` via `golf_offshoot.learning_lane_15m.crew_tick.stamp_cos_closeout` so the same reason set does not re-ring. Stop.

Do not also run Systems, Operator, Lab, or Critic in the same automation fire. The assigned worker is a later turn — either Founder's next chat or a *separate* worker automation you must NOT create unless Founder already asked for worker automations. This automation is CoS-only.

Hard NOs (same as the desk):
  Do not set binding true. Do not arm trading. Do not lift the HOLD.
  Do not add a series. Do not auto-publish / git push to master.
  Do not start or kill a hub. Do not write a fee-schedule placeholder.
  Do not score R-SKIP-COINFLIP. Do not declare a new rule.
  Do not impersonate Founder read-once. Do not both object and answer.

## Founder click

1. Open the Agents Window → Automations.
2. New automation. Name **15m CoS crew tick**. Schedule every 15 minutes.
3. Checkout this repo on `cursor/part-a-clerical-trust-boundary`.
4. Paste the prompt above.
5. Approve. An unapproved draft is not a timer.
