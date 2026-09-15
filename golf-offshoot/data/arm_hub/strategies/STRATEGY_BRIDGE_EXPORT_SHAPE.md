# STRATEGY_BRIDGE_EXPORT_SHAPE (ARM hub pin)

Locked intake for `strategy_loader.py`. Mirror of the Kalshi Micro / leftover-hunt
`shortlist_grow_freeze` export. This tree does **not** contain the operator
exam dir; CI uses the sample JSON beside this file.

Operator source:

`C:\Users\bearh\leftover_hunt_exam\shortlist_grow_freeze\`

## Join

`shortlist_v1` ⨝ `SHORTLIST_SHELF.per_id` on `id`.

| Field | Where | Notes |
|---|---|---|
| `id` | both | Keeper / Path Rank / promote-bar style id |
| `claim` | shortlist | Claim text |
| `dsl` | shortlist | DSL / rule expression |
| `mode` | shortlist | e.g. promote-bar |
| `pack` | shortlist | Invent packs Hard NO for live intake |
| `idea` | shortlist | Short idea line |
| `why_short` | shortlist | Why it is on the +96 shortlist |
| `shelf_label` | shelf | `KEEP` or `DEAD` (living) |
| `living` | shelf | `false` or `DEAD` drops the row |
| `recommended` | either | Contextual when / size flags + optional url, digestor_label, fill_to_30, stamp_binding, size_hint, guardrails |

Pull filter:

1. `shelf_label == KEEP` (`KEEP_WATCH` maps to KEEP). Drop `DEAD` / `LIKELY_DEAD` / `STRUCTURAL_DEAD`.
2. `dsl` must be present.
3. Invent packs are not a strategy source (live or paper pin).
4. Emit `strategies/strategy_bridge_keepers.jsonl` (one row per keeper) plus the JSON pins.

Pinned records also stamp `lab_admits=false`, `trading_armed=false`, `hub_untouched=true`.

Prefer **KEEP** only. Pin copies under this directory so Lane B churn cannot
retune a running paper book. The watch loop never re-joins; it only reads
`POLICY.json` that a human / scheduled `--pin-from` wrote.
