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
| `recommended` | either | Contextual when / size flags |

Prefer **KEEP** only. Pin copies under this directory so Lane B churn cannot
retune a running paper book. The watch loop never re-joins; it only reads
`POLICY.json` that a human / scheduled `--pin-from` wrote.
