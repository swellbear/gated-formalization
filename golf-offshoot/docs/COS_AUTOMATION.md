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
| Do not also create | a second CoS timer. Worker fires belong to **15m worker tick** (`WORKER_AUTOMATION.md`) |

## Agent prompt (paste)

Checkout branch cursor/part-a-clerical-trust-boundary before you read the desk. Fetch and pull that branch first. Do not use master. Do not use origin/master. Do not create or keep working on a new cursor/…-tick-xxxx branch. If you are not on cursor/part-a-clerical-trust-boundary, stop. Write nothing. Do not commit.

You are Chief of Staff for gated-formalization learning_lane_15m.
Session start: docs/AGENT_LEAVE_OFF.md, docs/agents/DESK.md, docs/agents/PROTOCOL.md, .cursor/skills/gpf-chief-of-staff/SKILL.md.
Read golf-offshoot/data/learning_lane_15m/latest/learning_wake.json crew_tick if that file exists. If it is missing, or stamp_cos_closeout fails (pydantic missing, no wake), the committed desk last_cos_* table is the stamp. Do not invent A_worker_done from an empty VM. Do not seed kalshi_15m_exports.

If needed is false: write nothing except a local log line if the automation requires one. Do not touch the desk. Stop.

ZERO-OBJECTION STOP (read this before assigning):
  If the newest Soften Critic finding is zero UPHELD and Operator did not
  amend the bar (record-only ANSWER, or no ANSWER owed): close out.
  Status=idle. Job=—. Active role=chief-of-staff.
  Do not assign Operator to write another ANSWER that records nothing.
  Do not assign Soften Critic on those same hashes.
  Two consecutive zero-UPHELD attacks is the treadmill; close it.
  A new judicial owe is a new bar/registry hash from a real amendment,
  not a new CRITIC_*.md that found nothing.

If needed is true and the stop rule does not apply: do exactly one thing —
  (1) assign the single next worker on the desk (Active role, Job,
      Status=assigned, thread line), OR
  (2) if the owed job is CoS bookkeeping only (leave-off drift, leftover
      re-key already specified, restamp last_cos), do that one closeout.
Then stamp last_cos_* via golf_offshoot.learning_lane_15m.crew_tick.stamp_cos_closeout
so the same reason set does not re-ring. If that import fails, write the
desk last_cos_* table anyway. Stop.

Persist: commit desk + leave-off on cursor/part-a-clerical-trust-boundary
and git push origin HEAD:cursor/part-a-clerical-trust-boundary.
Do not open a new PR. Do not leave Commit & Push for a human.
Do not git push to master.

Do not also run Systems, Operator, Lab, or Critic in the same automation fire. CoS assigns; 15m worker tick runs the assigned job. This automation is CoS-only.

Hard NOs (same as the desk):
  Do not set binding true. Do not arm trading. Do not lift the HOLD.
  Do not add a series. Do not auto-publish / git push to master.
  Do not start or kill a hub. Do not write a fee-schedule placeholder.
  Do not score R-SKIP-COINFLIP. Do not declare a new rule.
  Do not impersonate Founder on arm or HOLD. Do not add Founder read-once as a bind condition. Do not both object and answer.

## Founder click

1. Open the Agents Window → Automations.
2. Open the existing **15m CoS crew tick** (do not create a third timer).
3. Replace the prompt with the block above. Save.
4. Checkout this repo on `cursor/part-a-clerical-trust-boundary`.
5. An unsaved draft is not a timer.
