# Operator Guide

How to run Golf Betting Offshoot week to week. Model `golf-offshoot-0.7.0`.

This is an operations manual, not a sales page. If a field is missing, treat it as missing. If strategy returns no action, that is often the correct output.

Related internals: [Architecture](ARCHITECTURE.md), [Data feeds](DATA_FEEDS.md), [Strategy layer](STRATEGY_LAYER.md), [Known limitations](KNOWN_LIMITATIONS.md), [Shadow journal](SHADOW_JOURNAL.md), [Calibration](CALIBRATION.md), [Compare method](COMPARE_METHOD.md).

---

## 1. Purpose

### What this is

An uncertainty-aware **golf analysis system**. It ingests a real PGA field, estimates player skill (`θ`), simulates Make Cut / Top 20 / Top 10 / Top 5 / Win, shows ranges and reliability, compares model probability to a real book when one exists, and can emit **advisory** strategy notes. Residual judgment stays with you.

It sits **beside** Gated Progressive Formalization. It does not import, score, lock, or mutate the core method, templates, or anything under `applications/`.

### What this is not

- Not a betting bot. It **never places bets**.
- Not a proven edge engine. Calibrated weights have not beaten expert initialization on hold-out (`calib-v1` through `calib-v3` all froze `keep_expert`).
- Not a complete market tape. Place / top-10 / opening lines exist only when a real coupon was captured. They are never invented from winner odds.
- Not a substitute for watching the event, injury news, or setup notes the feeds do not have.

### Current honest status

**Ready only for observation.** Use it to rank a field, see what is constrained vs unconstrained, compare model vs a real winner coupon, and keep a paper journal of advises. Do not treat ranked Win% or `EdgeW` as clearance to bet. Do not treat empty strategy output as a bug.

As of 0.7.0: production weights remain expert-initialized. St. Jude 2026 is settled (paper museum). **This week** is the BMW Championship (`401811963`, Bellerive, 50-player no-cut). Opening lines exist only if ingest captures prematch Winner before it flips to Winner Live. Place markets ticket only when a real coupon lists them.

---

## 2. Core principles

1. **No auto-betting.** There is no execute path. `never_auto_bet` is always true. Suggested stake is not a ticket.
2. **Uncertainty stays visible.** Every player row has a probability range, a reliability score (separate from the range), open questions, and flags. Do not collapse that to a single number.
3. **Advisory only.** Decision actions are `pass` / `consider` / `strong_consider`. Strategy actions are suggestions. You confirm or ignore.
4. **No mocks on the operating path.** `ingest`, `live`, `pressure-test`, `calibrate`, and shadow logging use real feeds. `demo` / `explain` / `strategy` (without ingest) print `OFFLINE DEMO — MOCK DATA` and must not be used for rankings you act on.
5. **You keep final judgment.** Thin samples, missing injury, missing agronomy, live juice, and unmatched names are your problem to refuse, not the model’s to paper over.

---

## 3. What the system can do right now

On a real event (`python -m golf_offshoot ingest` / `live` / `pressure-test`):

| Capability | What you actually get |
|------------|------------------------|
| Field analysis | ESPN field, course yards/par, cut rule from `cutRound` |
| Multi-horizon probabilities | Make Cut, T20, T10, T5, Win — each with central + low/high |
| Reliability | Separate score from data density, quality, and input stability |
| Free parameters | Board of factors; unconstrained until evidence quality allows a move |
| Market edge | When a real coupon matches a name: `EdgeW` = model − de-juiced implied |
| Live updates | Banks observed to-par; remaining holes simulated; `live_position` hole-dampened |
| Strategy suggestions | If enabled: `new_bet` / hold / reduce / exit / add / reallocate, or nothing |
| Shadow journal | Paper log of operating-path advises (`new_bet`, add, reduce, exit, reallocate) |
| Source inventory | Every important field labeled real live / real historical / derived / unavailable |
| Audit snapshots | JSON under `data/snapshots/` with model version, weight hash, data hash |

It can also run a labeled **offline demo** so you can learn the table format without hitting the network.

---

## 4. What it cannot do well yet

- **Proven paper-trading edge.** Hold-out proper scores have not justified freezing fitted weights.
- **Place / top-10 / top-20 / make-cut advice** when the book does not list those markets. St. Jude Winner Live had none. The system will not synthesize them from winner prices.
- **Opening-line movement** if no distinct prematch coupon was stored before the market flipped to Winner Live. Live is never relabeled as open.
- **Calibrated superiority over expert α.** `calib-v3` ran on a stronger 16-week SG panel and still recommended `keep_expert`.
- **Injury wire** beyond ESPN withdraw status.
- **Agronomy** (stimp, rough, firmness). Yards/par/name are real; setup is unconstrained.
- **Vendor last-8 SG** unless `DATA_GOLF_API_KEY` is set **and** the payload actually contains last-8 fields. Without that, recent SG is PGA EVENT_ONLY mean of up to 16 completed weeks the player actually appears in — not 16 guaranteed measurements.
- **OWGR.** ESPN rankings endpoint is empty; talent is finish-derived.
- **True exchange MTM / limits / steam.** Strategy mark-to-market uses live **posted** decimal on user-recorded positions (cash-out quote if you type one).

---

## 5. Installation / setup

Python **3.10+**. From the offshoot folder (not the parent repo root unless that is on `PYTHONPATH`):

```bash
cd golf-offshoot
pip install -e ".[dev]"
pytest
```

`pytest` should pass before you trust a weekly run. Operating ingest needs network access to ESPN, PGA Tour GraphQL, Bovada or The Odds API (Hard Rock Bet), and Open-Meteo.

### Environment variables (optional)

None are required for a basic operating run. Bovada public coupons and PGA public StatDetails work without keys.

| Variable | Effect if set | If unset |
|----------|----------------|----------|
| `THE_ODDS_API_KEY` | Tried first for golf outrights (`--book auto`); required for `--book hardrockbet` | Bovada fallback on `auto`; Hard Rock stays unavailable |
| `GOLF_ODDS_BOOK` | `hardrockbet` pins Hard Rock Bet (no Bovada substitute); `bovada` skips Odds API | Same as `--book auto` |
| `DATA_GOLF_API_KEY` or `DATAGOLF_API_KEY` | Used **only** if the payload has true recent-window fields (`sg_total_l8`, etc.) | PGA EVENT_ONLY last-16; Data Golf marked unavailable |

Do not set a key and assume coverage. If the payload has no golf outright or no last-8 fields, the field stays **unavailable**. Skill ratings are not a last-8 window.

No secrets belong in the repo. Do not commit `.env` files. Do not paste keys into chat.

**Add The Odds API key (Windows):** copy `golf-offshoot/.env.example` to `golf-offshoot/.env` and set `THE_ODDS_API_KEY=...`. Operating commands load that file. A non-empty shell variable still wins. Session-only alternative in PowerShell: `$env:THE_ODDS_API_KEY = "..."`. User-level Windows env vars need a new terminal / Cursor restart.

### Demo vs operating (do not mix them up)

| Command | Data | Use for |
|---------|------|---------|
| `demo`, `explain`, `strategy`, `board` | Mock toy field | Learning the UI / schemas |
| `ingest`, `live`, `pressure-test`, `calibrate`, `shadow` | Real feeds | Weekly operation |

If you see `OFFLINE DEMO — MOCK DATA`, you are not on the operating path.

### Finding an ESPN event id

Default (omit `--event`) is the current PGA leaderboard. To pin an event, use the ESPN golf event id. **This week:** BMW Championship 2026 = `401811963`. Last week (settled museum): St. Jude = `401811962`. It appears in ESPN URLs and in ingest output as `id=...`.

---

## 6. Weekly workflow

Run everything from `golf-offshoot/`. Prefer `--event <espn_id>` once you know it so live reruns hit the same tournament.

### Sunday–Wednesday: capture the open if it exists

If Bovada still shows prematch **Winner** (not Winner Live), run ingest **before** the market flips:

```bash
python -m golf_offshoot ingest --event 401811963 --book bovada
```

The first distinct prematch coupon is archived under `data/openings/`. After the card becomes Winner Live, later runs can merge that archive as `line_role=opening`. If you first show up Thursday with only Winner Live, opening stays unavailable for the week. Do not pretend live is the open.

If a Finishes / Top 5 / Top 10 card exists **for this event**, it will ingest. If it does not, those markets stay unavailable.

### Pre-tournament analysis

```bash
python -m golf_offshoot ingest --event <espn_id>
# fuller dump + two strategy modes + a live pass:
python -m golf_offshoot pressure-test --event <espn_id> --bankroll 2000
```

`ingest` is analysis-only (strategy off). `pressure-test` writes `docs/PRESSURE_TEST_{espn_id}.md` so a later event does not overwrite the St. Jude 2026 artifact. `--mode` and `--risk` apply to the operating live/pre strategy config; the report still prints all three strategy modes for comparison.

**Read the source inventory first**, then the table, then the leftover callout (used vs unconstrained vs held-ticket residual). Inventory tells you what is real vs missing this week. Leftover is display only; do not stuff it into theta.

### How to interpret the ranked table (short)

Every ranked table (terminal, PDF, txt) ends with a **column index** for the columns that are actually on that table. Inventory tables have their own index.

Live tables add **dWin / Pre# / dRnk** when a pre-tournament `ingest` snapshot exists for that ESPN id. Those keys are defined on the table itself. This is model movement vs the last pre snapshot, not opening-line movement.

1. Rank is Win **central**, not “best bet.”
2. Read the **range** and **Rel** before EdgeW.
3. EdgeW is model − **de-juiced** implied, not a ticket. Decision/strategy also require beating **1 / posted decimal**.
4. Flags such as `thin_sample_overconfidence` or `sparse_data` are hard reasons to pass. `course_history_missing` is not — Rel haircut only (the venue is not in the loaded ESPN years).
5. On no-cut playoff fields, Cut ≈ 1.00 except WD. That is the rule, not a forecast of making the weekend.

### Optional strategy construction

Operating `live` and `pressure-test` enable strategy. Default mode is **stay_selective** and risk **conservative** unless you pass `--mode` / `--risk`. `--bankroll` is the sample allocation unless a paper ledger exists.

Compare modes without placing anything:

```bash
python -m golf_offshoot pressure-test --event <espn_id> --bankroll 2000 --mode stay_selective
```

`pressure-test` already runs protect / press / selective on the same snapshot. Empty books and `no_action` are normal when screens fail (posted-price edge, range width, reliability, missing place coupon, live overround).

There is no real-money ticket writer. `--lock-paper` on `live` writes a **mock / paper** book under `data/paper/{espn_id}.json` (gitignored), a paper-book PDF, **and a new batch pack** under `data/exports/packs/{espn_id}_{time}_{run}/`. That pack starts with **`00_trigger.pdf`** (this snapshot’s sell / reallocate / partial sell / add / new / hold list), then the ticket sheet, a bets-made explanation page, the ESPN live leaderboard from that run, the full-field ranking table from that run when it exists, `05_bankroll.pdf`, `04_movements.json`, **and `00_full_readout.pdf`**, which concatenates the numbered PDFs into one file with the trigger first. Individual PDFs stay in the folder. Each lock or later `live` with that paper book writes a **new** pack. Do not reuse an old folder as if it were current.

```bash
python -m golf_offshoot live --event 401811963 --book bovada --lock-paper
python -m golf_offshoot live --event 401811963 --book bovada
python -m golf_offshoot paper-export --event 401811963
```

`live` with an existing paper book records hold / reduce / exit / add / reallocate as **advice** in that snapshot's pack. When the **actionable** advice set changes (not a HOLD-only snapshot), it auto-applies that mock book. `--no-apply-paper` records advice without applying. `--apply-paper` force-applies even if the set did not change. After ESPN is official and the week is settled, live does **not** open new tickets on leftover Winner quotes; leftover post-settle opens are voided at cost (not a cash-out, not week P/L). Still mock money, still never a real bet. Open pack PDFs in Edge, Chrome, or Adobe — not as source in the editor. If a place ticket has no live posted coupon (`|n/a` on Screen), HOLD means ride to official settle — not “edge intact,” and not an invented cash-out.

`--lock-paper` refuses an empty field (`n=0`) instead of writing a blank book. If ESPN competitors are empty, ingest falls back to the **pinned book’s** Winner names joined to ESPN history ids (provisional field; not labeled as ESPN). Pinning a settled event prints ESPN’s current week (name + id) so you do not silently score last week’s museum. Ingest before Thursday warns if no distinct opening coupon was stored yet — capture Winner before it flips to Winner Live.

Parallel A/B paper machines (independent $250-start books; lived lock frozen, live apply still mutates): [Compare method](COMPARE_METHOD.md).

```bash
python -m golf_offshoot live --event 401811963 --book bovada --compare-method
python -m golf_offshoot compare-replay --event 401811963
```

`--compare-method` writes one folder under `data/exports/packs/{espn_id}_{time}_{run}_batch/` with **`00_full_readout.pdf`** in this order: **trigger pull** (lived this snapshot: sell, reallocate, partial sell, add, new, hold), how to read (five-book legend), fights, ESPN leaderboard, model field, lived / A-replay / B-guts / B-nerves / B-full tickets and why-bets, then lived bankroll. Each ticket page is titled with the book. A-control shares A-replay; there is not a second A book. Individual PDFs stay in the folder. Open the readout in Edge, Chrome, or Adobe — not as source in the editor. `--compare-method` will not `--lock-paper` lived. Live apply still mutates until official settle. St. Jude (`401811962`) A/B books stay Winner-only. BMW and later events ticket Top 5/10/20 when a real coupon exists and score Winner vs place P/L separately.

Polymarket is a **separate** paper machine. It never fills from Bovada, never writes `ledger.json`, and never lands in the `_batch/` five-book pack. `live --book polymarket` writes `{espn_id}_{time}_{run}_polymarket/` with its own `00_full_readout.pdf`, including `05_bankroll.pdf` for that path (opening $250, this week's moves, cash-outs, weekend settle/rollover on Polymarket only). Paper file is `data/paper/{espn_id}_polymarket.json` (independent $250). Odds come from the **US app** golf futures list (Winner and end-of-round leader when listed), not the international website Top 5/10/20 cards. Strategy prices each US card with the matching model (Win vs lead-after-N). Winner still needs 3pp vs the posted Yes. End-of-round leader still has to beat the Yes ask, but the consider bar scales with posted Yes (floor 1.5/2.0/2.5pp, cap Winner 3pp) and size is 35/55/75% of the Winner unit. Same player does not stack Win with R2/R3 (R1 may sit beside Win). 2-ball / matchup questions stay skipped. No orders.

Auto-lock observation tickets are **not** fills. After you actually buy, record shares and the Yes price you got. `paper-fill` attaches to the **last ntfy ADD** on that name+market when the ping was ADD (ESPN id, existing intent, lock model) and **adds shares** onto the open ticket. If the ping was NEW, it still attaches to that NEW. R1 leader is not automatically a flip.

```bash
python -m golf_offshoot paper-fill --event 401811963 --player "Matt Fitzpatrick" --shares 50 --fill 0.034
python -m golf_offshoot paper-fill --event 401811963 --player "Matt Fitzpatrick" --shares 50 --fill 0.034 --cost 1.80
python -m golf_offshoot paper-fill --event 401811963 --player "Matt Fitzpatrick" --shares 50 --fill 0.034 --market win_after_r1
```

`--fill` is a Yes price in `(0, 1)`. `--cost` is optional USDC spent (defaults to shares × fill). Watch’s last ping is merged with the current paper advice, so an R1 ADD still on file does not hide a later R2 NEW. That replaces a matching observation stub on the Polymarket path only. The lock model and vs-posted edge stay on the ticket so it still says why the name was booked. Later `live --book polymarket` marks the fill with `shares × bestBid` vs hold EV and prints **bid now** and **min-sell** on the trigger, plus a **fill tape** (cost vs offer vs keep-to-win, pop or no pop). Offer vs cost is display only — Stay Selective still sells only if the bid beats keep-to-win. **Flip** tickets are a separate sleeve on **listed** Yes cards (Winner, R1/R2/R3, place/make-cut when quoted): leftover prints P(early contract % ≥ ask + spread); NEW only if that P is at least 0.20; one flip per player; at most 6 open flips (3 per market), counting fills already on the book — a later live does not refill with the next-best names; a fail/sell that frees a slot can still print whoever is hottest then; live sells at fill+20% if still green on a following live run (not keep-to-win). Fail clock is 18 holes for R1, 36 for Winner/R2/place, 54 for R3. Unlisted cards are not invented. Fitz/Cole-style hold-to-Sunday tickets stay `intent=hold`. `--cash-out "Name=12.40"` on that same command overrides the bid dollars. Until you `paper-fill`, open names stay **[observation]** tracking stubs, not fills.

Pack leftover is `04_leftover.pdf` (used vs unconstrained vs Round 1/2/3 vs-posted, fill tape, fat Top 10 / skinny Win, and flip heat P as display, not a ticket). After Thursday, rerun `live --book polymarket` when the ESPN board moves so Round 2/3 use live to-par. Tee/wave stays leftover, not theta. The pack is the journal; do not keep a separate notebook.

Polymarket cash is **not** `ledger.json`:

```bash
python -m golf_offshoot paper-ledger --book polymarket --event 401811963
python -m golf_offshoot paper-deposit --book polymarket --event 401811963 --amount 50 --note "add cash"
python -m golf_offshoot paper-withdraw --book polymarket --event 401811963 --amount 20 --note "take some off"
python -m golf_offshoot paper-export --book polymarket --event 401811963
```

```bash
python -m golf_offshoot live --event 401811963 --book polymarket
python -m golf_offshoot live --event 401811963 --book polymarket --cash-out "Matt Fitzpatrick=2.10"
python -m golf_offshoot watch --event 401811963 --book polymarket --once
python -m golf_offshoot watch --event 401811963 --book polymarket
```

`watch` pings [ntfy](https://ntfy.sh) when the trigger actually changes (TAKE THE POP, FLIP FAILED, SELL after golf starts, ADD, NEW, REALLOCATE). Leftover heat does not ping. It always refreshes, never applies paper, never writes a pack/PDF/snapshot, and never places a CLOB order. Set `NTFY_TOPIC` in `golf-offshoot/.env` and subscribe to that topic in the ntfy app. `--once` is the phone check. Leave the looping command running in a terminal; pre-tee waits 30 minutes between ticks, in-play 10 minutes. Ctrl+C stops it.

### Paper bankroll (rollover)

There is now a lifetime mock ledger at `data/paper/ledger.json` (gitignored). Wins add to the bankroll. Losses come out. Deposits and withdrawals you record are included. This is still not real money.

```bash
python -m golf_offshoot paper-ledger
python -m golf_offshoot paper-ledger --event 401811962
python -m golf_offshoot paper-deposit --amount 50 --note "add cash"
python -m golf_offshoot paper-withdraw --amount 20 --note "take some off"
python -m golf_offshoot paper-settle --event 401811962 --refresh
```

`live`, `paper-ledger`, and `paper-export` **auto-settle** any open paper book when ESPN marks that event **final** with exactly one official winner. They do not invent a winner or a playoff; those stay open. After settle, that event’s book stays empty: leftover posted odds are not a new market. After a finished week is booked, the next `--lock-paper` sizes off the **rolled** bankroll (and subtracts any tickets still open on a not-yet-final event). `paper-settle` is still the explicit command that errors if the field is not official. After a lock exists, `live --bankroll` is ignored in favor of the working bankroll; use `paper-deposit` to add cash.

Every batch pack includes `00_full_readout.pdf` (all numbered PDFs in one file), `03_leaderboard.pdf` on live snapshots (ESPN place / to-par / thru at that run, not model Win%), `04_leftover.pdf` (display leftover, including Round 1/2/3 vs-posted when quoted), and `05_bankroll.pdf`: this week’s moves, ticket wins/losses once settled, deposits/withdrawals, and lifetime event P/L. Bankroll is last in the combo.

`--book bovada` screens tickets against Bovada quotes only (Winner / Winner Live when listed). Use that for this week's BMW Championship: The Odds API has no weekly PGA outright and no Hard Rock golf coupon, so `--book hardrockbet` stays empty. Do not map Hard Rock, DraftKings, or major-winner futures onto this event. After St. Jude settle, the next `--lock-paper` sizes off the **rolled** ledger bankroll. `--bankroll` on live is ignored when a ledger exists. Empty strategy output is still the honest result when nobody clears.

**Screens vs live juice, in plain language:** the sportsbook takes a cut on live winner odds, so the number you would actually buy is worse than a fair market. `EdgeW` looks at the fair market after that cut is stripped and can look good. The ticket screen asks whether the model is still at least 3 percentage points more optimistic than `1 / posted odds` **on Winner**. End-of-round leader uses a smaller, posted-Yes-scaled bar (still must beat the ask). When live juice is heavy, that screen fails even if EdgeW is positive. That is expected. A paper lock still records clean names so you can track fake money: **cleared** tickets get the full single-name unit (R1/R2/R3 get 35/55/75% of that unit); **observation** tickets (positive vs-posted but short of that card's bar) get 25% of that card's unit. It is not clearance to bet. The St. Jude mock book was locked before the cleared/observation split and was not re-sized. BMW is a new lock off the rolled bankroll.

**Same point, technical:** `EdgeW = model_p − implied_fair`. Winner ticket screen = `model_p − 1/decimal` ≥ `MIN_EDGE_TO_CONSIDER` (0.03). Round-leader bar = `max(floor, min(0.03, scale × posted Yes))` with floors 0.015/0.020/0.025 and scales 0.25/0.30/0.35 for R1/R2/R3. Live winner overround on this event has been ~1.29–1.37.

### Live updates during the event

```bash
python -m golf_offshoot live --event <espn_id> --book bovada
python -m golf_offshoot live --event <espn_id> --book bovada --refresh   # force odds refetch
python -m golf_offshoot live --event 401811963 --book bovada
```

Live mode:

- Uses ESPN score-to-par and holes completed (`period` + `thru`, not “FINISHED = 72 holes”).
- Until anyone has a board mark (holes / place / to-par), live **HOLD**s open tickets. Pre-tee quote drift is not a collapse sell. Typed `--cash-out` that beats hold EV can still EXIT.
- Hole-dampens `live_position` so a 6-hole Round-1 lead cannot dominate θ.
- Refetches odds with a **45s** TTL. If refresh fails, quotes older than **15 minutes** are suppressed (`EDGES_SUPPRESSED_STALE`), not treated as live.
- Prints **dWin / Pre# / dRnk** against the latest pre-tournament snapshot for that event. Run `ingest` first this week or those columns stay off. Live is never treated as the opening line.
- Writes a **full-field PDF** plus HTML and txt under `data/exports/` on every `ingest` / `live` / `pressure-test` persist. Terminal may truncate; the files do not. Open the PDF in Edge, Chrome, or Adobe — not as source in the editor. The `.html` file is the same table in a browser.

Rerun when the board or the coupon actually moved. Do not spam `--refresh` to manufacture activity.

### Typed cash-out vs hold (optional)

Bovada’s public Winner Live board is not a cash-out quote. If you have a real Open Bets number (or want to practice with a hypothetical), pass it on that live snapshot:

```bash
python -m golf_offshoot live --event 401811962 --book bovada --cash-out "Kurt Kitayama=12.40,Tommy Fleetwood=7.10"
```

Last name or ESPN id also works (`Fleetwood=7.10`). Repeat `--cash-out` for one name at a time. The quote is **not stored** as a standing price; type it again next run if you still have it.

Live strategy then compares **take $X now** vs **hold for the winner payout**: remaining EV ≈ live Win% × stake × lock odds, with a Stay Selective buffer so a quote has to beat the interval, not just scrape past the central number. If the quote wins, advice is EXIT (still never auto-bet). If it loses, advice is HOLD — even if the odds-ratio MTM looks like a “runner.” Applying that EXIT with `--apply-paper` books paper P/L as quote minus stake.

Without `--cash-out`, an applied paper reduce or exit still books an **estimated** cash-out when that snapshot has a live posted decimal: odds-ratio MTM on the sold slice, then a 20% haircut on the MTM gap (benefit if the price shortened, penalty if it lengthened). The ledger note is labeled estimated. It is not a scraped Open Bets number. No live posted coupon → stay at cost (0 P/L). A typed `--cash-out` quote always overrides the estimate.

A cash-out sell does not automatically reallocate. Leftover cash stays cash unless another name clears live screens.

This works on the mock book too. You do not need a live account to pass the flag.

Open the latest PDF from `golf-offshoot/data/exports/` in Edge, Chrome, or Adobe (filename `{espn_id}_{mode}_{run_id}.pdf`). Cursor/VS Code will show `%PDF` binary if you open that file as text — that is not the report. The matching `.html` file is the same table and opens as a normal page.

### Shadow journaling

Operating runs with strategy enabled and `persist=True` append advises to `data/shadow/advises.jsonl` when the layer emits `new_bet` / add / reduce / exit / reallocate. `hold` and `no_action` are not logged.

```bash
python -m golf_offshoot shadow
```

### Post-event review

1. Replay `shadow` against the actual finish. An advise that “would have won” is not validation by itself — note posted price, range, reliability, and whether the market even existed.
2. Read the audit JSON in `data/snapshots/` for that `run_id`.
3. Do **not** run `calibrate` every week. Recalibration is a research action when the as-of panel is materially stronger (see [CALIBRATION.md](CALIBRATION.md)). Finish-only refits are forbidden. Production stays expert until an artifact says `use_calibrated`.
4. Read the leftover callout on `ingest` / `live` (used vs unconstrained vs held tickets). Do not stuff leftovers into theta; documented `HumanOverride` or they do not happen. Spec: [PARKED_LEFTOVER_CALLOUT.md](PARKED_LEFTOVER_CALLOUT.md).

---

## 7. How to read the outputs

### Central probability vs range

`0.137[0.11-0.17]` means: Monte Carlo Win **central** 13.7%, with a low/high band from the same simulation (and θ uncertainty). The band is the claim about uncertainty. A 14% favorite with `[0.04-0.28]` is not the same object as 14% `[0.12-0.16]`.

Horizons (Make Cut, T20, T10, T5, Win) come from **one** θ, not five separate models. They should be coherent (Win ≤ T5 ≤ T10 ≤ T20 ≤ Make Cut).

### Reliability score

`Rel` is **not** 1 − interval width. It blends data density, input quality, and stability. A tight Win interval on a thin sample is a warning (`thin_sample_overconfidence`), not confidence. Lesser-known / opposite-field names often rank with lower Rel even if Win central looks spicy.

### Leftover callout

`ingest`, `live`, and `pressure-test` print a leftover block after the table / strategy: already used, still unconstrained, on held tickets, do not stuff into theta. Live names the open paper book; ingest prints none held. A hot round is residual, not extra theta. See [PARKED_LEFTOVER_CALLOUT.md](PARKED_LEFTOVER_CALLOUT.md).

### Open uncertainties / free parameters

Explain output (and inventory notes) lists what moved θ and what did not. Unconstrained factors (injury, agronomy, missing SG) stay broad on purpose. Narrative momentum is capped. “Open:” on a row is unfinished business, not flavor text.

`python -m golf_offshoot board --course-type parkland` dumps the **demo** factor catalog (mock). For a real player, use operating ingest plus the explainability block in a pressure-test report, or `explain` only as a format demo.

### Market edge vs posted price

Two different comparisons:

| Quantity | Formula | Meaning |
|----------|---------|---------|
| Displayed `EdgeW` | `model_p − implied_fair` | Fair = raw implied / sum of raw implied (overround stripped) |
| Ticket screen | `model_p − 1/decimal` | Winner must clear ~3pp (`MIN_EDGE_TO_CONSIDER`). R1/R2/R3 leader uses a scaled bar (still must beat the Yes ask). |

Live Winner coupons often carry **large overround** (St. Jude ~1.29–1.37). De-juicing shrinks longshot fair probs and inflates `EdgeW` on names the book barely prices. That is why a +0.03 EdgeW on a 176.00 longshot is usually still `pass` on the posted-number screen.

Unmatched names have **no** price. The system does not invent one.

### Why a player may rank high but still not be actionable

Typical stack:

- Favorite by Win central, but EdgeW is **negative** (book already hotter).
- Positive EdgeW vs fair, but does not beat **1/odds**.
- Range wider than ~0.18 on the horizon.
- Rel below ~0.45.
- `thin_sample_overconfidence` / `sparse_data` / `narrative_overweight`. `course_history_missing` is not a hard pass.
- No coupon for the horizon you wanted (e.g. ranked on T10, book has Winner only).
- Playoff field: make-cut “edges” are meaningless when Cut is structurally ~1.

### Why strategy may return no-action

The construction layer only proposes `new_bet` after the **decision screen** passes, sizing survives Kelly × haircut × caps, and the market exists. Empty `protect_profits` / `press_edges` / `stay_selective` blocks on St. Jude 0.7.0 were honest: live juice made the posted-price screen fail for most of the field, place coupons were missing, and the user book was empty until `--lock-paper`. That is the system working.

---

## 8. Strategy layer usage

### Pure analysis vs strategy mode

| Path | Strategy |
|------|----------|
| `ingest` | Off. Rankings + inventory + leftover callout |
| `live`, `pressure-test` | On (advisory) |
| `demo --strategy` / `strategy` | On, **mock data** |

Default pipeline strategy is off. Operating helpers turn it on for live/pressure-test only.

### Modes

| Mode | Bias |
|------|------|
| **Protect Profits** (`protect_profits`) | Smaller size; reduce runners; do not add into a live move |
| **Press Edges** (`press_edges`) | Larger size; hold/add when live edge improved |
| **Stay Selective** (`stay_selective`) | Mid size; only strong remaining edges (default) |

Risk preference (`conservative` / `normal` / `aggressive`) scales caps separately. CLI `--risk` applies to the **demo** `strategy` command. Operating live/pressure-test currently uses **conservative**.

### Pre-tournament vs live actions

- **Pre:** construct a suggested book from ranked rows (`new_bet` only). Does not debit bankroll.
- **Live:** if open positions exist, mark entry vs live edge, then hold / reduce / exit / add / reallocate / new_bet. Out of the box weekly CLI, the book is **empty**, so you mostly see posture + maybe `new_bet`.

### What the action words mean

| Action | Meaning |
|--------|---------|
| `new_bet` | Suggested new position (not placed) |
| `add` | Increase an existing user-recorded position |
| `reduce` | Cut size (e.g. runner lock under Protect, or cooling-off) |
| `exit` | Get out; original edge collapsed or worse |
| `reallocate` | Move stake from a worse live edge to a better name at cap |
| `hold` | Keep as-is (not written to shadow) |
| `no_action` | Nothing to do (not written to shadow) |

Suggested stake is fractional Kelly on a **range-haircut** probability, times quality, risk, and mode, capped by single-position and total-exposure limits. Tiny numbers are a feature.

### All strategy output is advisory

`StrategyPosition` is proposed, not booked. The engine never writes a `BetRecord`. If you actually bet, that is outside this system. Do not paste a `$4` advise into a sportsbook and call it a model bet without reading range, Rel, posted decimal, and inventory.

---

## 9. Shadow journal

### What it logs

Operating-path strategy advises: `new_bet`, `add`, `reduce`, `exit`, `reallocate`. Each line includes tournament, player, market, posted decimal (current coupon, never opening), model p + range, suggested stake, mode, run mode, reason, odds as-of, and `never_auto_bet=true`.

Demo/mock runs do **not** write here.

### Where it lives

`golf-offshoot/data/shadow/advises.jsonl` (gitignored).

### How to review

```bash
python -m golf_offshoot shadow
```

### How to learn without fooling yourself

- An advise is a **timestamped opinion**, not a fill.
- Grade it against the **posted decimal at `odds_as_of`**, not closing or opening unless those were actually stored.
- If place markets were unavailable, do not backfill a fictional top-10 ticket.
- Repeat advises on the same name (same week, moving live price) are not independent trials.
- Empty weeks are data: the screens refused. Count those too.
- Do not tune α from the journal by hand. That is what `calibrate` is for, and it has not beaten expert yet.

---

## 10. Data reality / source honesty

Every inventory row has a **kind**. Use it.

| Kind | Meaning | Operator implication |
|------|---------|----------------------|
| `real_live` | This week’s scoreboard, forecast, or live coupon | Can be stale; check `as_of` / lag / TTL notes |
| `real_historical` | Completed leaderboards, PGA EVENT_ONLY / THROUGH_EVENT tables | Pre-event only; no future leakage by design |
| `derived_from_real` | Transform of real observations (finish-skill, EVENT_ONLY mean, wind fit) | Still not a vendor last-8 or OWGR |
| `unavailable` | No source | Unconstrained factor. **Not** “average,” not zero, not healthy |
| `mock` | Tests and labeled demo only | Illegal on operating ingest (run will raise) |

**Unavailable is not solved.** If opening is unavailable, you do not have movement vs open. If top-10 is unavailable, you do not have a top-10 edge. If health is unavailable, the player is not “cleared.” If recent SG notes say median 7 of 16 requested, you do not have 16 measured weeks.

Quality scores (0–1) scale how hard evidence may move θ. Low quality + a large standardized signal still should not dominate a high-quality SG category.

---

## 11. Current limitations

Consolidated, without softening:

- Production weights are **expert-initialized**. Three calibration artifacts exist; none is selected.
- Recent SG is PGA EVENT_ONLY up to 16 weeks, skip-missing. Data Golf last-8 is unused without a qualifying key+payload. Requesting 16 ≠ measuring 16.
- Long-term SG unmatched names stay unconstrained (example: two St. Jude names missed THROUGH_EVENT).
- Winner Live is in-play. Opening is missing unless a prematch coupon was archived or still listed.
- Place/top/make-cut only when the **matching event** lists them. Champions/LPGA cards are not attached to PGA.
- Live overround on winner markets is often severe; displayed EdgeW overstates ticket value.
- No injury wire, no OWGR, no stimp/rough/firmness.
- Cut rule is ESPN `cutRound` (0 ⇒ no cut). Playoff and 36-hole exceptions are simplified.
- Live model banks to-par and independent remaining rounds; hole-dampen prevents Round-1 board domination but is not shot-level.
- Correlation screens are θ proximity / SG-style / cut-risk slices, not a fitted finish copula.
- Strategy MTM uses live posted decimal (not de-juiced implied) unless you type `--cash-out` for that snapshot. Open positions are user-recorded; weekly CLI starts empty.
- HTTP cache under `data/cache/` is for reproducibility; `--refresh` when you need a new coupon, not to hide staleness.

The system will not: place bets, hide interval width, treat print-matching a book as clearance, or modify Gated Progressive Formalization.

---

## 12. Recommended use mode now

**Use it for:**

- Pre-event field ranking with ranges and reliability.
- Seeing which factors are actually constrained this week (inventory).
- Comparing model Win% to a **real** winner coupon, including the posted-number screen.
- Live board updates with hole-dampened position (sanity-check that a round-1 leader is not 25%+ without enough holes).
- Paper observation of advises in the shadow journal.
- Learning where the model and the book disagree — then deciding yourself.

**Do not use it for:**

- Automatic or “the model said so” betting.
- Place/top-10 tickets when those coupons are unavailable.
- Open-to-current steam trades when opening is unavailable.
- Treating `keep_expert` as a temporary UI state you can ignore.
- Demo-command rankings as if they were this week’s PGA field.

**Week to week:**

1. Ingest while prematch still exists if you can.
2. Read inventory → table → leftover callout → explain top names → strategy block (expect silence).
3. Live rerun after meaningful board/price change.
4. Shadow review on Monday against actual finishes and **logged** prices.
5. Keep a personal note of what the feeds missed (WD rumor, pin sheets, weather delay). That note is part of residual judgment, not something to stuff into θ by hand unless you use a documented override and accept the audit trail.
6. Leftover callout is already on `ingest` / `live`. Use it; do not fill agronomy / tee / injury / narrative into theta by hand.

Until opening lines, place markets, or a hold-out-beating freeze exist, the honest posture is **observation-only**.

---

## 13. Command cheatsheet

All commands: `python -m golf_offshoot <command> ...` from `golf-offshoot/`.

| Intent | Command |
|--------|---------|
| Real pre-tournament analysis | `python -m golf_offshoot ingest --event <id>` |
| Same, bypass HTTP TTL | `python -m golf_offshoot ingest --event <id> --refresh` |
| Skip ESPN season ranking fetches | `python -m golf_offshoot ingest --event <id> --no-season-stats` |
| Real live board + strategy (empty book) | `python -m golf_offshoot live --event <id>` |
| Downloadable full-field table | `data/exports/` PDF (open in Edge/Adobe, not the editor) plus HTML |
| Batch paper pack (combo + tickets + why-bets + field + bankroll) | `python -m golf_offshoot paper-export --event <id>` |
| Paper bankroll readout (week + lifetime) | `python -m golf_offshoot paper-ledger` |
| Add / remove mock cash | `paper-deposit --amount 50` / `paper-withdraw --amount 20` |
| Settle weekend tickets into the rollover | `live` / `paper-ledger` auto-settle when ESPN is final; or `paper-settle --event <id>` |
| Apply mock sells/reallocates to the paper book | default `live` when advice set changes; `--no-apply-paper` to skip; `--apply-paper` to force |
| A vs B method compare (2 MCs, fights + batch pack + `00_full_readout.pdf`) | `python -m golf_offshoot live --event <id> --book bovada --compare-method` |
| Retrofit A-replay + B-nerves from snapshots | `python -m golf_offshoot compare-replay --event 401811962` |
| Record a Polymarket fill (shares + Yes price; no CLOB) | `python -m golf_offshoot paper-fill --event <id> --player "Name" --shares 50 --fill 0.034` |
| Live with typed cash-out vs hold | `python -m golf_offshoot live --event <id> --book bovada --cash-out "Name=12.40"` |
| Pre + live + three strategy modes + markdown report | `python -m golf_offshoot pressure-test --event <id> --bankroll 2000` |
| More Monte Carlo draws | add `--sims 2500` (pressure-test floors pre at 2000) |
| Review paper advises | `python -m golf_offshoot shadow` |
| Recalibrate (research; do not expect a freeze) | `python -m golf_offshoot calibrate` |
| **Mock** ranked toy field | `python -m golf_offshoot demo --sims 1500` |
| **Mock** one-player explain | `python -m golf_offshoot explain --player p01` |
| **Mock** strategy demo | `python -m golf_offshoot strategy --bankroll 2000 --mode stay_selective` |
| **Mock** live strategy after demo book | `python -m golf_offshoot strategy --live --mode press_edges` |
| Factor catalog JSON (not a live field) | `python -m golf_offshoot board --course-type parkland` |
| Tests | `pytest` |

`--mode` values: `protect_profits` \| `press_edges` \| `stay_selective`.  
`--risk` (demo strategy): `conservative` \| `normal` \| `aggressive`.  
`--event` omitted ⇒ current ESPN PGA leaderboard.

---

## 14. Glossary

| Term | Plain meaning |
|------|----------------|
| **θ (theta)** | Latent skill in strokes per round (higher = better). Prior from long-term talent; evidence updates it. |
| **α (alpha)** | Factor weights on those updates. Production: expert-initialized unless a calibration artifact says `use_calibrated`. |
| **Horizon** | Outcome bucket: make cut, top 20, top 10, top 5, win. |
| **Central / range** | Simulation point estimate and low–high band. |
| **Reliability** | Trust in the inputs, not the inverse of range width. |
| **Free parameter** | A factor that starts unconstrained and only tightens with quality evidence. |
| **SG** | Strokes gained. Long-term: PGA `THROUGH_EVENT`. Recent: mean of `EVENT_ONLY` weeks actually measured. |
| **EVENT_ONLY / THROUGH_EVENT** | PGA StatDetails windows for one event vs cumulative through that event. |
| **De-juice / overround** | Book implied probabilities sum to >1. Fair = each raw implied divided by the total. |
| **EdgeW** | Model Win probability minus fair implied. Not a ticket. |
| **dWin / Pre# / dRnk** | Live vs latest pre-tournament snapshot: Win delta, pre rank, rank change (`+` = climbed). Not opening movement. |
| **Posted decimal** | The actual price (e.g. 7.50). Ticket screen uses `1/decimal`. |
| **Opening / prematch** | Distinct pre-live Winner coupon. Winner Live is in-play, not an open. |
| **line_role** | `current` vs `opening` on a quote. |
| **Consider / pass** | Decision-layer advice. Never execute. |
| **new_bet / hold / reduce / exit / add / reallocate** | Strategy suggestions. Advisory. |
| **Shadow journal** | JSONL paper log of some strategy advises. Not a bankroll. |
| **Operating path** | Real ingest/live/calibrate/pressure-test. No mocks. |
| **keep_expert** | Calibration recommendation: do not put fitted weights into production. |
| **Hole-dampen** | Live leaderboard evidence scaled by holes completed so early boards cannot dominate. |
| **No-cut field** | ESPN `cutRound=0` (e.g. some playoff events). Make-cut ≈ 1 except WD. |

---

## Quick refusal checklist

Before you treat any row as more than observation:

- [ ] Command was `ingest` / `live` / `pressure-test`, not `demo`
- [ ] Inventory read; unavailable fields named
- [ ] Range and Rel inspected, not only central Win
- [ ] Coupon exists for the market you care about
- [ ] Posted-price edge cleared, not only EdgeW
- [ ] Opening used only if `opening` coverage > 0
- [ ] No `thin_sample_overconfidence` you are ignoring
- [ ] You still have residual judgment for news the feeds lack
