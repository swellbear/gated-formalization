# Kalshi golf gym

Paper gym on the same hub process as KXBTC15M. One golf bankroll. The advisor is in `decide_golf` from the first watch tick. Skip when the brain cannot see. Trading is **NOT ARMED** until `golf-offshoot/data/golf_kalshi/latest/TRADING_ARMED` exists **and** keys are present.

This is not a WC3 reopen. Golf idle / WC1 stays the museum of the old weekly claim.

## Destination

The same machine that papers Kalshi golf can later place live Kalshi golf orders. Paper is the gym. Live is a per-lane file + keys, not a chat stamp.

## Hard NOs

- Do not mix golf and 15m ledgers, bankrolls, n-counts, or lessons.
- Do not widen `kalshi_15m.py` `ALLOWED_SERIES` (`KXBTC15M` only).
- Do not invent unmatched players, missing fields, or Kalshi results.
- AI never deposit / withdraw / transfer. Hub never grows cash buttons.
- Polymarket is not a venue, odds source, or import for this loop.
- Do not retune golf player-weights from the 15m tape.
- Do not rank wallet recipes or player-brain updates by richest pnl.
- Unmatched names stay unmatched. No field → catalog only, no fill.
- Settle SoT is Kalshi `result`. ESPN finish is not enough.
- Per-series `fee_multiplier` is required on a fill. Do not assume ×1.

## Catalog

Public Kalshi only. Series come from `/series?tags=Golf` (Sports fallback), then markets from `/markets?series_ticker=…&status=open|settled` with pagination (settled capped at one page per series). The global `/markets?status=open` dump is refused. A row needs a golf `series_ticker`. Fail-open last-good is golf-only. Catalog refresh is its own TTL (`saved_at` inside the markets TTL). It is not on the brain clock.

The 8765 Catalog is a tour-family tree (PGA / LIV / LPGA / …): every series is listed as a count; **market rows load when you open a series** (`GET /golf-catalog/series?ticker=`). Unmatched is collapsed by default (count on the summary; rows via `GET /golf-catalog/unmatched`). That shelf is still inspectable. It is not a 9k-row first paint. Open markets are Kalshi contracts. Open tickets are paper fills from `decide_golf` on **open** markets only. This does not widen `kalshi_15m` `ALLOWED_SERIES`.

Open ≠ in-play. `in_play` is Kalshi `can_close_early`. ESPN live competitors also put a bound event on the live brain rotation.

## Field hunt

Per Kalshi **event** (`event_ticker` when present, else series). PGA-only is not the gym.

The tick is staged so the advisor can see:

1. **Settle** always.
2. **Identity hunt** every open event against a tick-level ESPN league snapshot (one leaderboard read per league, in-memory title bind). Cheap. History is not loaded here.
3. **Monte Carlo** only for the round-robin slice (`max_brain`, remaining clock). `keep_expert` in memory (`include_odds=False`). Never `run_operating`. Never write Phase 1 `data/paper/`. Re-run when the live scoreboard fingerprint moves. A clock miss is deferred, not stored as thin. Listed names stay in `field_candidates` through that defer. Unscored listed events with `n_names > 0` take the slice after held tickets so they cannot sit `field_deferred` behind a live book. That puts a pending listed hunt ahead of an unheld live in-play ESPN event.
4. **Decide** every open market from cached p. Skip is honest (`no_model_p`, unmatched, `thin`, `field_deferred`). Empty names is `no_field`. Clock miss is `field_deferred`. A hunt that produced no p is `thin`. Recovered-id count is telemetry, not a skip. Fill cap is count, not the clock.

Hunt order:

1. ESPN league for that family (`pga`, `lpga`, `eur` for DP World, `champ`, `liv` if ESPN serves it). Conservative title overlap. Wrong-tour bind is worse than a miss.
2. If ESPN has no board for that series: Kalshi open `yes_sub_title` names **are** the field. The listed player is that sub-title when a positive name-shape check says the string itself is a person. A present sub-title that fails is unmatched; the market title does not re-admit a golfer. Attach ESPN athlete ids from **history** when they match; provisional ids otherwise. Never Polymarket. Never Bovada `list_provisional_names`. A listed field with `n_names > 0` hunts from those names. `n_recovered=0` is not defer-forever.
3. History-id floor (`n_recovered` ≥ min(half the extracted names, 20), at least 1) is telemetry (`history_thin`), not a hunt park and not a fill skip. Below the floor the listed names still score when the `yes_sub_title` itself names a golfer. A country, date phrase, threshold ladder, or "X beats Y" match-up is not a golfer and does not get a `model_p`. A field where every sub-title fails reads `no_field` / `field_source=miss`, same as Kalshi serving no names. Catalog stays.
4. Season-long / missing MC horizon → `no_model_p`. A listed market gets a probability only when its `yes_sub_title` names a person (two or more letter tokens, no digits / `+` / connective predicates; closed-class team/country/tie tokens are not person names). If a sub-title is present and fails, `match_market_player` does not map the title onto a candidate. Exact-match tote strings (`the field`, `any other`) stay unmatched. Live Kalshi golf has no tote sub-titles.
5. Kalshi-listed fields take a tour haircut. `field_source` is stamped on tickets. Listed-name fills are observation, not promote fuel.

The last tick writes bound / brain / deferred on the Golf board so an empty cart is readable.

## Golf Farm / Honer

Idle shells on the golf tab: `data/golf_kalshi/latest/farm.json` and `data/golf_kalshi/honer/`. They read the live golf `paper/ledger.json` and last tick on every watch tick. Empty notebooks until dated. No golf `crew_tick`. They do not consult 15m `decide()`. They do not write "no golf tape yet" when tickets exist. The 15m Lab chair is untouched. Lab 2026-09-12 looked at the live paper tickets and **refused** to date a family ([`GOLF_KALSHI_LAB_NAMER.md`](GOLF_KALSHI_LAB_NAMER.md)). Empty notebooks after that look are honest. Farm/Honer do not auto-name.

## Unattended

When `GatedFormalization-15mLearningHub` is up, 15m PaperWatch, Honer, and golf watch start with no click. `WATCH_KILL` under `data/golf_kalshi/latest/` stops golf only.

Skip is the default when field, name, quote, fee, or edge is missing. That is the brain working. A spent MC clock is deferred, not a skip-all `budget` stamp.

## Wallet recipe v1.2

Dated `2026-09-11`. Seed paper **$1000**. `recipe_v1()` is the live loader. Tickets keep the recipe id they were filled under. The ledger stamp moves forward. Seed is not reset. v1.1 halt was next UTC day; v1.2 paper pause is 120s then continue.

- **Fast** — 25% of the 20% cap (`$50`). Round-leader / 3-ball / same-day. Fail-clock 18/36/54 holes or +20% bid pop.
- **Week** — 50% (`$100`). This event winner / make-cut / top-N.
- **Slow** — 25% (`$50`). Season-long / captain / Ryder / Presidents Cup / 2027.
- One `event_ticker` may hold open stake up to the 5% name cap. Ticket count is not a live gate. Do not re-trim tickets already open. 5% per name.
- Size is 0.25 Kelly (`fractional_kelly` on listed-haircut p vs `1/ask`) inside remaining sleeve / name / event-dollar / displayed room. Not a richest-pnl ranker of the catalog.
- Screen is the complete gate (name, p, Kalshi ask, fee, after-fee edge). Gross bar 3pp then `edge_after_fee > 0`. Stake lives in `allocate`.
- Skip reasons include `mix_sleeve_full`, `mix_event_cap`, `mix_not_picked`, `mix_rebuy_blocked`. Same-ticker rebuy is blocked until live `edge_after_fee` ≥ `min_edge`.
- Overweight week: no net-new and no ADD in week until under share. Reallocate (swap quality) still allowed. Empty fast/slow may catch up to their shares even if total is already at 20%. Catch-up stops when week is no longer overweight.
- Daily loss 5%. Drawdown halt 8%. **Paper** pauses **120s**, records the halt, then continues (peak ratchets so the same hole does not re-trip). Paper bankroll may go negative and still size from the seed. **Live** (`TRADING_ARMED`) keeps next-UTC-day resume and does not size a spent book. Halt skips new fills / ADD / reallocate; collapse, fail-clock, and Kalshi settle still run.
- Path: collapse vs live ask after golf has started; sell at `yes_bid`. Missing bid, missing multiplier, or `displayed_size` too small → HOLD. Pre-tee quote drift is HOLD. Pre-tee reallocate is allowed. ADD if live edge improved 1.5pp, golf started, and the sleeve is under share. Official settle is Kalshi `result`. `paper_exit` is a path record, not a Brier label.
- One-time trim on the v1 → v1.1 bump: per `event_ticker` with more than 3 open tickets, paper-exit the worst live `edge_after_fee` (missing mark = worst) until 3 remain. Reason `recipe_event_cap`. Does not run every tick. Bankroll is not reset. The dollar event cap does not re-open that trim.
- In-play watch stays **45s**. Monte Carlo budget is 8s / `max_brain=2`. Held events are scored first; a cache hit does not consume a brain slot.
- Hub mix line: `worthy N · picked F/W/S · exits E · realloc R · adds A` plus last-tick skip counts. Sleeve bars vs live `sizing_bank` targets (seed card is still `$50/$100/$50`). Open tickets on Home. Closed tickets (result + after-fee P/L) on Scoreboard. Halt log on Scoreboard. `?lane=golf_kalshi` is Golf. Golf Farm / Honer point at that tape; they do not say there is no tape. No cash / arm / mode slider.

Fee pin: Founder browser bytes of `golf-offshoot/docs/kalshi-fee-schedule.pdf` (`founder_browser_bytes`, sha256 `c326a69f596a11e8f8be2620402d39a8d4823920c21cc97c93a114d862699601`, 281129 bytes). Adjustment function is `golf_offshoot.learning_lane_15m.evidence_bar.fee_adjust`.

## Learning clocks

1. Wallet recipe — exam on new settles; next mix by `declared_at`, not pnl. `paper_exit` is counted as a path, not a Brier row.
2. Player brain — ESPN-field Kalshi `yes`/`no` feeds Brier. Listed-name stays observation. `suggest_alpha_update` is a candidate. Production stays `keep_expert` until a hold-out beats expert. `promote` stays false until that happens.

## Live

`TRADING_ARMED` + keys. `live_scale` starts at 0.1 until 10 lived fills settle. Unarmed executor never calls `/orders`. Hub has no Place / Arm / cash buttons.
