# Agent leave-off (read this first)

**This file is the SoT for “where did we stop?”**  
Chat transcripts are not. A later Grok / Cursor cloud agent will not see a prior chat unless the work and this stamp are on GitHub.

| Field | Value |
|-------|--------|
| Updated | 2026-09-07 |
| Interim operator | Cursor chat (Grok bot usage exhausted until **2026-09-13**) |
| Repo SoT | `origin/master` @ `352b967` (PR #163) |
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

## What is already on master

Desktop hub (control surface):

- Launch: `golf-offshoot/scripts/windows/Open-Phase1-Hub.bat` → `python -m golf_offshoot shell` → `http://127.0.0.1:8765`
- Code: `golf-offshoot/src/golf_offshoot/operator_surface/app.py`
- Two lanes, exact selector `lane=golf|learning_lane_15m` (bare `15m` is unknown → golf)
- Buttons: ingest / live / shadow / loop / refresh. Cash / arm / Kalshi-auth actions are refused.
- Golf live/loop auto-applies **paper** advises only. 15m live/loop = public fetch → paper autobet → settle join.
- ntfy: one ping on operator-triggered ingest/live/loop finish if `NTFY_TOPIC` is set.
- Auto-reload: artifacts soft-refresh; git/code change re-execs the hub.

15-minute Kalshi learning lane:

- Docs: `golf-offshoot/docs/LEARNING_LANE_15M.md`
- Code: `golf-offshoot/src/golf_offshoot/learning_lane_15m/`
- CLI: `python -m golf_offshoot lane-15m`
- Public read only. Official settle = Kalshi `result` matched to CF Benchmarks `BRTI`.
- Landed: PRs #151, #153, #156–#159, #161, #162.

Published hub snapshot (`docs/observability-hub/data/manifest.json`, generated 2026-09-07T18:56:00Z):

- Settled: `KXBTC15M-26SEP071445-45` — `result=yes`, finalized, CF Benchmarks matched, **paper_win**, paper pnl `+1.67`
- Pending: `KXBTC15M-26SEP071500-00` — live paper fill, **SETTLE_PENDING** (do not invent win/lose)
- 15m charts: **not yet available**
- Golf WC1 FAIL does **not** transfer into this lane

Golf Phase 1 (do not reopen unless asked):

- Stamp: `golf-offshoot/docs/phase1_dryrun/OPERATOR_STATUS_STAMP.md`
- WC1 admitted FAIL / park unproven. WC2 parked/rejected. Edge **not** established. Idle on WC3+ until a new settled week.

## Next (safe, in order)

1. Founder GO on the desk: run `lane-15m` → `systems` → `validator` **only if** Kalshi posted `result` on `KXBTC15M-26SEP071500-00`. Else stay `SETTLE_PENDING`.
2. Only if asked: leftovers in `LEARNING_LANE_15M.md` (Digestor digest, 15m viz wall, weekly honesty, expand past `KXBTC15M`, CFB websocket observe-only).

## Hard NOs

- No Kalshi API keys, cash scopes, orders, or private endpoints
- AI never deposit / withdraw / transfer
- Do not retune golf θ from 15-min
- Do not invent win/lose or use DIY CFB averages as official settle
- Do not put golf WC1 / Ill under `learning_lane_15m`
- Missing charts stay `not yet available`
- Do not merge leftover oil-hunt / `cursor/eia-window-job2` dirt into this track

## Resume commands

```bash
cd golf-offshoot
python -m golf_offshoot hub --lane learning_lane_15m
python -m golf_offshoot lane-15m
python -m golf_offshoot observability-export
python3 docs/observability-hub/validate_hub.py --strict   # from repo root
```

Public viewer: `docs/observability-hub/` (read-only; no controls).
