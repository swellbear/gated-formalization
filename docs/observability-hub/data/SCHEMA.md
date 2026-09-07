# `manifest.json` — the hub's only data contract

The viewer at [`../index.html`](../index.html) reads exactly one file: `manifest.json`
in this directory. It reads nothing else, polls nothing, and calls no API. Whatever is
absent from the manifest renders as **`not yet available`**.

Systems owns this file. The viewer's job is to display it honestly and to refuse it when
it stops being read-only.

- `schema_version` is `1`.
- All values are strings unless noted. Numbers are passed as **strings** so the hub never
  reformats, rounds, or arithmetics an operating figure.
- Every string reaches the page through `textContent`. Markup in a value is displayed as
  literal text, never parsed.

---

## Top level

| Key | Required | Meaning |
| --- | --- | --- |
| `schema_version` | yes | `1` |
| `hub` | yes | page-level provenance (below) |
| `global` | yes | standing posture, for cross-checking against the static wall |
| `lanes` | yes | array of lane objects, one per lane |

### `hub`

| Key | Meaning |
| --- | --- |
| `title`, `subtitle` | page copy |
| `generated_at` | ISO 8601 UTC stamp of when this manifest was written |
| `source_kind` | `fixture` or `export`. `fixture` makes the page say so, loudly. |
| `source_note` | one sentence on provenance — where the numbers came from |
| `control_surface_note` | restates that the control surface is the operator's local shell |

### `global`

| Key | Meaning |
| --- | --- |
| `badges` | must be exactly `READ ONLY`, `TRADING NOT ARMED`, `PAPER OBSERVATION ONLY`, `AI: NO CASH IN/OUT` |
| `wall_lines` | the standing no-controls statement |
| `hard_nos` | the enforced Hard NO list |

`global` is **documentation and a cross-check, not a source**. The standing wall is
hard-coded in `index.html` precisely so that no export can suppress it. The validator
checks that `global.badges` still matches the wall; a mismatch is an error in the
manifest, not a reason to change the wall.

---

## Lane object

`lane_id` must be one of the canonical ids. A lane with any other id is skipped by the
viewer and rejected by the validator. `15m` is not a lane id.

| `lane_id` | Lane |
| --- | --- |
| `golf` | Golf offshoot, Phase 1 observation |
| `learning_lane_15m` | 15-minute Kalshi learning lane (`KXBTC15M`) |

| Key | Required | Meaning |
| --- | --- | --- |
| `lane_id` | yes | canonical id above |
| `label` | yes | lane heading |
| `tab_label` | yes | short label for the lane tab |
| `lane_badge` | yes | the lane's loudest badge — `PHASE 1 OBSERVATION` for golf, `LEARNING LANE` for `learning_lane_15m` |
| `badges` | yes | lane badge strip |
| `summary_line` | yes | one sentence on what this lane is |
| `source_kind` | yes | provenance of this lane's figures |
| `lane_scope_note` | yes | what this lane's records do **not** cover — this is the anti-blur line |
| `last_run` | yes | last-run honesty block |
| `settle` | yes | settle banner block |
| `paper_ledger` | yes | paper ledger summary block |
| `records` | yes | array of dated weekly operating records (may be empty) |
| `records_note` | when `records` is empty | why there is no record, stated in place |
| `charts` | yes | array of chart slots (may be empty) |
| `charts_note` | when `charts` is empty | why there are no charts |
| `docs` | no | further reading links |

Lane blocks never cross lanes. A record under `golf` is a golf record; the viewer renders
it inside the golf tab only, alongside its own `lane_scope_note`. There is no shared or
global record slot, by design.

### `last_run`

```json
{
  "status": "published export",
  "headline": "one sentence a reader can act on",
  "fields": [{ "label": "Run id", "value": "…", "note": "optional" }],
  "notes": ["what this figure is not"]
}
```

Set `status` to `not yet available` and `fields` to `[]` when no run has been published.
The hub then says so instead of showing a stale run.

### `settle`

```json
{
  "banner": "SETTLE_PENDING",
  "banner_state": "pending",
  "headline": "…",
  "counts": [{ "label": "…", "value": "…", "note": "optional" }],
  "sources": [{ "label": "espn_official_final", "value": "89 rows" }],
  "residual": [{ "label": "named row", "value": "rec-…", "note": "why it is pending" }],
  "observation": {
    "label": "Paper hit rate",
    "value": "34/122 ≈ 0.279",
    "chips": ["OBSERVATION", "NOT EDGE ESTABLISHED", "NOT BANKED"],
    "note": "…"
  },
  "notes": ["…"]
}
```

`banner_state` is one of:

| value | rendered as |
| --- | --- |
| `pending` | the `banner` string, pending styling |
| `off` | `settle banner off` |
| `not_available` | `not yet available` |

If `observation` is present it **must** carry `chips`. A hit-rate number is never
publishable on its own — the qualifiers are drawn attached to the figure so it cannot be
screenshotted away from them.

### `paper_ledger`

```json
{
  "status": "counts only — no cash figures published",
  "headline": "…",
  "rows": [{ "label": "Settleable paper tickets", "value": "122" }],
  "absent_fields": ["payout", "realized_pnl", "roi"],
  "notes": ["…"]
}
```

Counts only. `absent_fields` names the money-shaped columns that do not exist in the
export; the hub draws each one as `ABSENT` rather than blank, and derives none of them.

A **cash figure is not publishable here at all** — see the forbidden keys below. There is
no bankroll, balance, or transfer row, and there is no control to move any.

### `records`

```json
{
  "record_id": "WC1",
  "title": "…",
  "verdict": "FAIL",
  "lean": "park unproven",
  "lane_scope_note": "This is a golf-lane record. It does not transfer.",
  "rows": [{ "label": "SETTLE_PENDING_cleared", "value": "false" }],
  "hard_nos": ["Never claim edge / banked edge / \"edge established\""],
  "links": [{ "label": "…", "href": "https://github.com/swellbear/gated-formalization/…" }]
}
```

A dated FAIL stays a FAIL. Do not re-publish a record with a softened `verdict`; publish
a new dated record instead.

### `charts`

```json
{
  "slot_id": "shadow_honesty_strip",
  "title": "Shadow honesty strip",
  "subline": "Live-book paper journal — not settled PnL · not Kalshi demo",
  "badges": ["PHASE 1 OBSERVATION", "AI: NO CASH IN/OUT", "PAPER OBSERVATION ONLY"],
  "status": "available",
  "path": "../viz/golf_offshoot_dryrun_2026-09-07/shadow_honesty_strip.png",
  "pixel_size": "2640 × 4125",
  "note": "read-only PNG",
  "doc_href": "https://github.com/swellbear/gated-formalization/…"
}
```

`status` is `available` or `not yet available`. Omit `path` when unavailable.

`path` rules, enforced in the browser and by the validator:

- relative, never absolute, never a URL, never a scheme
- `.png` only
- must resolve **inside the published tree** (`docs/`) — either beside this manifest under
  `charts/<lane_id>/`, or a reuse of an existing published board such as
  `../viz/golf_offshoot_dryrun_2026-09-07/`

A chart is drawn only once its PNG has actually loaded in the reader's browser. Declaring
`available` for a file that is not in the published tree does not produce a chart: the
slot degrades to `not yet available` and says the file is missing. **Only a chart whose
PNG loaded is clickable to enlarge.** An unavailable slot has no enlarge button, no
pointer cursor, and cannot open the overlay.

---

## Forbidden content — the manifest is refused, not sanitised

If any of the following appears anywhere in the manifest, the viewer renders **no lane
content at all** and prints the offending JSON paths. A bad export blanks the panel rather
than quietly growing an affordance. Run [`../validate_hub.py`](../validate_hub.py) before
publishing and you will never see this.

**Forbidden keys** (case-insensitive, any depth). Prose is free to use these words; a
*key* with one of these names is refused.

- *control-shaped*: `action`, `actions`, `control`, `controls`, `button`, `buttons`,
  `form`, `forms`, `submit`, `endpoint`, `endpoints`, `api`, `api_base`, `api_url`,
  `api_endpoint`, `post`, `post_url`, `run_url`, `ingest`, `live_run`, `shadow_run`,
  `loop`, `refresh`, `reload`, `poll`, `poll_url`, `ws`, `ws_url`, `websocket`,
  `stream_url`, `arm`, `arming`, `armed`, `trade`, `trades`, `trade_url`, `order`,
  `orders`, `place`, `place_bet`, `cancel`, `bet`, `bets`, `one_tap`, `onetap`,
  `autobet`, `auto_bet`
- *cash-shaped*: `deposit`, `withdraw`, `withdrawal`, `transfer`, `cash`, `cash_in`,
  `cash_out`, `cashout`, `cashin`, `bankroll`, `balance`, `funds`, `wallet`, `stake_now`,
  `money`, `payout_url`
- *secret-shaped*: `secret`, `secrets`, `api_key`, `apikey`, `api_secret`, `token`,
  `access_token`, `refresh_token`, `bearer`, `password`, `passwd`, `credential`,
  `credentials`, `private_key`, `privatekey`, `key`, `keys`, `env`, `dotenv`, `ssh_key`,
  `session`, `cookie`, `auth`, `authorization`, `kalshi_key`, `kalshi_api_key`

**Forbidden values** — anything shaped like a credential (private key blocks, `sk-…`,
`AKIA…`, `ghp_…`, `xox…`, JWTs, or `api_key: …` style assignments). These are **refused,
not redacted**: a redacted page would still leave the secret sitting in a committed public
file. Remove it from the export and rotate it.

**Link hrefs** must be `https://github.com/swellbear/gated-formalization/…` or a relative
path inside the published tree. Anything else is dropped silently by the viewer and flagged
as an error by the validator.
