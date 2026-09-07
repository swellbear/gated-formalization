# Observability hub — shareable, read only

A static, link-shareable window onto what the system has already published: charts, the
paper ledger summary, the settle banner, the WC1 dated FAIL record, lane badges, and
last-run honesty. One page, two lanes, no controls.

**Intended live URL** (once Pages is on):
`https://swellbear.github.io/gated-formalization/observability-hub/`

Deep links per lane: append `#golf` or `#learning_lane_15m` only. `#15m` is not a lane id and falls back to `golf`.

| | |
| --- | --- |
| This hub | **view only.** Shareable. Cannot start a run or move a cent. |
| The operator shell at `127.0.0.1:8765` | **the control surface.** Local, unchanged by this hub, not linked from it. |

This PR does not touch `operator_surface` behaviour. The local golf operator UX is a
separate concern on its own PR.

---

## Hard NOs — enforced, not just documented

The page carries none of the following, and the viewer refuses a data feed that tries to
introduce them:

- No ingest / live / shadow / loop / refresh control
- No paper deposit, withdraw, or transfer
- No trade arming, one-tap bet, or Kalshi trade keys
- No cash movement UI of any kind
- No API keys, secrets, or `.env` values on the page or in the committed client JS
- No live Kalshi (or any) API call from the browser
- Missing charts stay **`not yet available`** — never invented, never substituted
- Never claim edge, banked edge, or "edge established"
- **Never blur the golf WC1 FAIL into the 15-minute lane**, in either direction

Where each one is enforced:

| Hard NO | Enforced by |
| --- | --- |
| No controls in the markup | `validate_hub.py` fails on `<form>`, `<input>`, `<select>`, `<textarea>`, `method="post"` anywhere in `index.html` |
| No control/cash/secret data | `assets/hub.js` refuses to render a manifest carrying a forbidden key or a credential-shaped value, and prints the offending JSON paths; `validate_hub.py` fails the same input before it can be committed |
| No write requests | `validate_hub.py` fails if `hub.js` issues anything but the one GET of `data/manifest.json` |
| No markup injection from data | every manifest value reaches the DOM as a text node; `validate_hub.py` fails if `hub.js` starts assigning markup |
| No invented charts | a chart is drawn only after its PNG actually loads in the reader's browser; a 404, a non-PNG, or an off-site path degrades to `not yet available` |
| Standing wall cannot be suppressed | the badge wall is hard-coded in `index.html`, not read from the manifest; `validate_hub.py` fails if those strings go missing |
| Lanes stay separate | `validate_hub.py` fails if a golf-only marker (`0.279`, `34/122`, `WC1`, `Mitchell`, an ESPN id) appears in a non-golf lane's displayed figures |
| No edge claims | `validate_hub.py` fails on "edge established", "banked edge", "validated edge" and friends, unless the sentence is denying one |

Run it:

```bash
python3 docs/observability-hub/validate_hub.py --strict
```

Standard library only. Exit 0 means publishable.

---

## Lanes

Canonical ids. The tabs are the loudest thing on the page after the wall.

| `lane_id` | Lane | Loud badge | State today |
| --- | --- | --- | --- |
| `golf` | Golf offshoot, Phase 1 observation | `PHASE 1 OBSERVATION` | Real committed exports. Settle banner up, WC1 dated **FAIL**, two charts published. |
| `learning_lane_15m` | 15-minute Kalshi learning lane (`KXBTC15M`) | `LEARNING LANE` | **Nothing published yet.** Every panel reads `not yet available`. |

The 15-minute lane is deliberately empty rather than pre-filled. There are no KXBTC15M
artifacts in this repository yet, so there is nothing honest to show — and a placeholder
number would be worse than a blank. It renders as an explicit "no export published",
with a note stating that the golf WC1 FAIL is a golf record and does not transfer here.

Adding a future lane means adding its id to `CANONICAL_LANES` in both `assets/hub.js` and
`validate_hub.py`, and adding a tab to `index.html`. An unrecognised `lane_id` is skipped
by the viewer and rejected by the validator, so a lane cannot appear by accident.

---

## How Systems drops an export

The viewer reads exactly one file. Everything else follows from it.

1. **Write `data/manifest.json`.** Full contract in [`data/SCHEMA.md`](data/SCHEMA.md).
   Set `hub.source_kind` to `export` (`fixture` makes the page announce that it is
   showing checked-in sample data).
2. **Put the PNGs where the manifest points.** Either
   - beside the manifest, at `data/charts/<lane_id>/<slot_id>.png`, or
   - reuse an already-published board, e.g.
     `../viz/golf_offshoot_dryrun_2026-09-07/shadow_honesty_strip.png`.

   Paths must be relative, `.png`, and resolve inside `docs/`. Anything else is refused.
3. **Anything not ready gets `"status": "not yet available"` and no `path`.** Do not point
   a slot at a file you are about to add. A slot that claims a file it does not have
   renders as missing and says so.
4. **Validate**: `python3 docs/observability-hub/validate_hub.py --strict`
5. **Preview** (optional, and identical to what Pages will serve):

   ```bash
   python3 -m http.server 8080 --directory docs
   # then open http://127.0.0.1:8080/observability-hub/
   ```

   Serve it over http rather than opening the file from disk — `fetch` cannot read a
   manifest over `file://`, and the page will honestly tell you it could not load.
6. **Commit and push.** Pages republishes on push. Nothing on the page polls, so what a
   reader sees is whatever was last committed — which is why every lane carries its own
   last-run honesty block saying so.

For the 15-minute lane specifically: point it at whatever the
`/workspace/kalshi_15m_exports/`-style snapshots become once they are copied into this
published tree. Do not have the browser read them from anywhere else, and do not add a
live Kalshi call.

### What must not go in an export

Cash figures, credentials, and anything control-shaped. The paper ledger block is
**counts only** — tickets, wins, losses, pending. Money-shaped columns go in
`absent_fields`, where the hub draws each one as `ABSENT` rather than blank and derives
none of them from the counts. The operator's own ledger at `data/paper/ledger.json` is
gitignored and stays unpublished.

---

## Turning Pages on

Pages is **not** enabled on this repository yet, so the URL above 404s until Founder
switches it on. The site ships complete and needs no build step.

**Settings → Pages → Build and deployment**

- Source: **Deploy from a branch**
- Branch: **`master`**, folder: **`/docs`**
- Save.

That serves `docs/` as the site root, so the hub lands at
`https://swellbear.github.io/gated-formalization/observability-hub/` and the golf boards
under `docs/viz/…` resolve without being duplicated.

Notes:

- No GitHub Actions workflow is added. Branch-folder publishing needs none, and it keeps
  this PR thin.
- `docs/.nojekyll` is included so files are served verbatim rather than run through Jekyll.
- Everything under `docs/` becomes browsable. The repository is already public, so this
  exposes nothing new — but it is worth knowing that the method documents and PDFs in
  `docs/` will be reachable too.
- The page sets `robots: noindex`. It is meant to be shared by link, not found by search.
- Pages is public for a public repository. Do not treat this URL as private.

---

## Files

| Path | Role |
| --- | --- |
| `index.html` | page shell. Carries the standing badge wall and the lane tabs statically, so no data feed can suppress them. |
| `assets/hub.css` | styling. No framework, CSS custom properties, per-lane accent colour. |
| `assets/hub.js` | renderer, Hard-NO enforcement, and the enlarge overlay. ~600 lines, no dependencies. |
| `data/manifest.json` | the only data file the viewer reads. Currently a fixture. |
| `data/SCHEMA.md` | the contract Systems writes against. |
| `validate_hub.py` | pre-publish validator. Standard library only. |

No framework, no bundler, no `node_modules`, no build step. House style follows
`ui/choice-presenter`: one page, vanilla JS, CSS custom properties.

---

## Reading the charts

Available charts are **clickable to enlarge**. The boards are large — the shadow honesty
strip is 2640 × 4125 — and unreadable scaled into a column, so:

- Click the chart, or focus it and press Enter, to open a fullscreen overlay.
- **Esc**, the close button, or a click outside the image closes it.
- **Actual size** switches from fit-to-screen to 100% so you can scroll around the detail;
  **Fit to screen** goes back. In actual size, clicking the image pans rather than closes.

A `not yet available` slot is not clickable. It has no button, no pointer cursor, and
cannot open the overlay — there is nothing behind it, and the page does not pretend
otherwise. The overlay itself fetches nothing; it is a larger view of a PNG already on the
page.

---

## What this page is not

- Not settled bets, and not banked money. Nothing was ever staked.
- Not a track record. No ROI, CLV, PnL, or payout figure exists in the exports or is
  derivable from them.
- Not an edge claim. The golf paper hit rate is an observation over unplaced tickets and
  carries its qualifiers wherever it is drawn.
- Not live. The page polls nothing; it shows the last published export, and says so.
- Not the operator's console. That is local, and it is not this.
