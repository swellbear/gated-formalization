# ARM hub (paper-live sim)

Separate Kalshi ARM-candidate hub. **Not** the learning-lane / leftover-hunt paper hub.

Trading is **NOT ARMED**. Paper bankroll starts at **$500** and **accumulates** (fees + settles, no daily reset). The same executor codepath later flips to live by adding `latest/ARM.flag` plus production keys — not by writing a second bot.

## Start once → leaves running

No Grok / Founder / Micro / Lab / chat in the hot path. The loop is a deterministic Python process that only reads files from disk.

```text
python -m golf_offshoot arm-hub            # one paper tick
python -m golf_offshoot arm-hub --watch    # always-on, own PID, until --kill
python -m golf_offshoot arm-hub --kill     # write data/arm_hub/latest/KILL
python -m golf_offshoot arm-hub --status   # bankroll / policy / NOT ARMED banner
```

Equivalent: `python -m golf_offshoot.arm_hub …`

`--watch` re-reads `strategies/POLICY.json` and `latest/state.json` every tick. It does **not** call the strategy loader, does **not** ask a bot, and does **not** regenerate POLICY. Bots (if any) are optional **offline** tools for inventing or editing policy files. A human GO or a scheduled script copies those files onto disk. The running process just notices the new bytes.

Never bind port **8765** (learning-lane hub). A later UI may use **8766** — not in this scaffold.

Windows (detached paper watch): `golf-offshoot/scripts/windows/Start-Arm-Hub-Paper.bat`

## Paper → live (one codepath)

| | Paper (default) | Live (later) |
|---|---|---|
| Trigger | `latest/ARM.flag` **absent** | flag **present** AND secrets present |
| Ledger / balance | `paper/ledger.json` ($500 accumulate) | Kalshi account (same order/settle functions) |
| Host | public read / replay tape | `https://external-api.kalshi.com/trade-api/v2` |
| Keys | not required | `KALSHI_ARM_API_KEY_ID` + `KALSHI_ARM_PRIVATE_KEY_PATH` (RSA `.key` file) |
| POLICY / sizing / guardrails | identical | identical (promote-bar allowlist enforced) |

Ladder: **paper (now) → optional demo shadow → live ARM**. Demo host is `https://demo-api.kalshi.com/trade-api/v2` (documented; not auto-armed).

This scaffold ships paper-first. Live HTTP submit is the same `submit_order` function and is **refused** unless the flag and keys both resolve. Keys are never invented and never committed.

## Keepers (pin copies)

Operator machine source (not on this git tree):

`C:\Users\bearh\leftover_hunt_exam\shortlist_grow_freeze\`

- `shortlist_v1.json` (active 30)
- `SHORTLIST_SHELF.json` (KEEP / DEAD)
- latest lean under `out/`

Join shape: `shortlist_v1` ⨝ `SHORTLIST_SHELF.per_id` — see `data/arm_hub/strategies/STRATEGY_BRIDGE_EXPORT_SHAPE.md`.

Pin into `data/arm_hub/strategies/` so Lane B churn cannot retune mid-run:

```text
python -m golf_offshoot arm-hub --pin-from "C:\Users\bearh\leftover_hunt_exam\shortlist_grow_freeze"
```

Prefer **KEEP**-labeled rows only. **Invent packs** are a Hard NO for live intake. Repo CI uses the checked-in sample pins under `data/arm_hub/strategies/`.

Contextual rules (time / secs-to-expiry / price band + size % / DD brake / daily kill + claim/DSL) live in `strategies/POLICY.json`. The watch loop never auto-rewrites that file. Rebuild is an explicit offline `--rebuild-policy` / `--pin-from`.

## Artifact tree

```text
golf-offshoot/data/arm_hub/
  config.yaml
  paper/ledger.json          # $500 seed, accumulates
  paper/fills/
  paper/settlements/
  latest/state.json
  latest/ARM.flag            # absent = PAPER
  latest/KILL
  strategies/                # pinned keepers + POLICY.json
  audit/
  fixtures/replay_tape.json  # CI / no live quotes
```

## Hard NOs

- Do not touch `golf-offshoot/data/learning_lane_15m/**`, learning-lane collectors, or Lane B grow-freeze watcher membership.
- Do not import `golf_offshoot.learning_lane_15m` from this package.
- Trading stays **NOT ARMED** until a human writes `latest/ARM.flag` **and** supplies env keys.
- Never invent API keys. Never put secrets in chat or git.
- No bot / chat / Lab / Founder in the runtime loop.
- Do not always-fire a keeper id — rules are contextual.
- Invent packs are refused for live intake.
- Do not bind port 8765.
- Do not reset the paper book each day.
- AI never deposit / withdraw / transfer.
- Do not self-merge this track onto the learning-lane hub.

## Tests

From `golf-offshoot/`:

```text
python -m pytest tests/test_arm_hub.py -q
```
