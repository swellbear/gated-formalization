# Agent desk

Live board. CoS owns the header. Workers only change `Status`, `Handoff`, and the thread.

Thread lines are **one sentence, newest first, max 10**. Long findings belong in the artifact, not here.

| Field | Value |
|-------|--------|
| Updated | 2026-09-11 12:01 ET |
| Active role | chief-of-staff |
| Job | Founder preview: keep 15m hub on 127.0.0.1:8765; add Desktop PREVIEW launcher on draft PR #179. Do not merge. Not armed. |
| Status | waiting-founder |
| Handoff | Preview hub is listening on this VM at 127.0.0.1:8765. Desktop launcher is golf-offshoot/Open-15m-Hub-PREVIEW.bat plus .url. A/B/C still on draft PR #179. |
| Waiting on Founder | **Y** |

## Ask Founder

Preview is up (Try Live desktop → http://127.0.0.1:8765). A/B/C are on draft PR #179 (not merged, not armed). Is a new Founder lock required, or does this draft sit until you say go-live?

## Publish gap (named so nobody assumes Pages is self-maintaining)

The runner exports locally. It does **not** commit or push. The public page is **not** self-maintaining. That is the same defect that left Pages stale for six hours tonight. A local export is not a publish. Systems still owns the manual tick step: material export → `--strict` → commit → push to `master`.

## Honesty checklist (CoS re-derived 2026-09-08 08:42 ET — not inherited)

| Box | State |
|-----|-------|
| Lineage story readable, dual lineage labeled not merged | **PASS** — lineage A is the live `paper/ledger.json` book; lineage B remains the published `071445-45` `+1.67`. Digest caveats and the export both forbid summing. |
| `KXBTC15M-26SEP071500-00` honestly joined or pending with a true reason | **PASS** — no paper book and no settle file on this tree. The rolling journal no longer holds its official row (forgotten, not resolved). Manifest still names it as a missing paper join, not `SETTLE_PENDING`. No pnl invented. |
| No invented charts or pnl | **PASS** — generated digest copies ledger figures only; a window with no book still has no pnl. Fee-accurate totals are not on the hub. |
| One hub process on `learning_lane_15m` | **PASS as one hub tree, not one OS process.** Live 08:42: supervisor PID 2940 (no `--no-browser`) parent of listener PID 9568 (`--no-browser`) on `127.0.0.1:8765`. The inherited 19:58 line ("both `--no-browser`") is **false**. Not two independent hubs. Do not kill the listener. |

**Gate is open on this live restamp.** The 19:58 stamp is retired. Golf idle stays **ON**. Evidence bar remains **not binding**.

## Thread

- 2026-09-11 12:01 ET  CoS → Founder: preview hub listening on 127.0.0.1:8765; copy Open-15m-Hub-PREVIEW.bat/.url. Still draft. next=Founder
- 2026-09-11 12:01 ET  hub-ui → chief-of-staff: added Founder-safe PREVIEW bat at golf-offshoot root; no git checkout of main. next=chief-of-staff
- 2026-09-11 11:50 ET  CoS → Founder: A/B/C landed on draft PR #179. Is a new lock required, or does this sit until go-live? next=Founder
- 2026-09-11 11:50 ET  hub-ui → chief-of-staff: C role strip collapsed unless owed; B golf tile is stamp status not a cockpit. next=chief-of-staff
- 2026-09-11 11:45 ET  hub-ui: 15m glance home + A this-lane doing/thinking/learning on the draft PR. PaperWatch stays. next=hub-ui (B then C)
- 2026-09-11 11:45 ET  CoS → hub-ui: Founder locked A then B then C after glance home; same draft PR; do not merge; not armed. next=hub-ui
- 2026-09-08 08:52 ET  CoS: honesty gate re-derived live. Hub box is one tree (2940/9568), not the 19:58 "both --no-browser" claim. next=systems
- 2026-09-08 08:51 ET  validator → systems: `--strict` OK; report sha256 matches the export bytes. next=systems
- 2026-09-08 08:49 ET  digestor → validator: SOURCE figures regenerated from live files (caveats concatenated, not rewritten). next=validator
- 2026-09-08 08:32 ET  CoS: Soften Critic hired (skill on tree). Evidence bar remains a draft until a separate-session attack and Founder acknowledgement. next=soften-critic (later session)