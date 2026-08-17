# Known limitations

The system is honest about where it is weak. These are not “TODO cosmetics”; they are structural.

## Weak spots

- **New course setups / renovations** with little history: course-fit and course-history stay unconstrained; venue-cluster borrow is a shrink toward *similar* courses, not knowledge of a new cut of rough.
- **Sudden major swing / putting changes** that have not shown up in SG windows: short-term trend can only move as far as quality allows; narrative about a “new swing” is capped.
- **Lesser-known / opposite-tour players:** wider priors, more borrow, lower reliability. Do not read a tight Win interval as confidence.
- **Extreme weather outliers** (hurricane delay, 40 mph, altitude not in the player’s history): weather factor quality will be low unless a real split exists.
- **Health news** is usually sparse and late. Low quality by design; a rumor must not clear a favorite.
- **Live hole-by-hole** banks observed to-par and simulates only remaining holes (`σ √remaining_rounds`). `live_position` evidence is hole-dampened: Round-1 incomplete boards use `(h/H)×(h/18)` so a 6-hole lead cannot dominate θ.
- **Cut rule** is “place plus ties” after N rounds. Playoff, 36-hole cut exceptions, and projected-cut live lines are simplified.
- **Correlation in the book** uses θ proximity (decision screen) plus cut-risk / SG-style / weather slices (strategy layer), not a fitted copula of finishes.
- **Strategy MTM** uses live **posted** decimal when present (`stake × lock_odds / live_posted`). De-juiced implied is the fallback only if posted is missing. A typed `--cash-out` quote overrides MTM. Applied paper reduce/exit without a typed quote books an **estimated** cash-out: odds-ratio MTM on the sold slice, then 20% of the MTM gap is haircut (labeled estimated; not scraped Open Bets). Missing live posted stays at cost. Open positions exist only if the user records them. Bovada is not scraped for Open Bets.
- **Market** mocks do not include limit availability, steam, or exchange liquidity.
- **Weights** may be expert-initialized or a frozen calibration (`docs/CALIBRATION.md`). `calib-v1` is finish-derived only. `calib-v2` used an 8-week as-of panel and did not beat expert. `calib-v3` is considered only when the as-of recent-SG panel is materially stronger than calib-v2 and hold-out beats expert. Finish-only refits are not allowed.
- **Strokes gained** uses PGA Tour GraphQL as-of windows: `THROUGH_EVENT` for long-term, `EVENT_ONLY` mean of the last **16** completed events for recent form. Unmatched players stay unavailable. Missing weeks are skipped, not zero-filled; requesting 16 weeks does not fabricate 16 measured events. Season-to-date is a long-term fallback only, never a fake last-N. Data Golf remains preferred for recent windows when a key and true last-8 fields exist.
- **Market odds** use The Odds API when a key and golf outright exist; otherwise Bovada public Winner / Winner Live, plus Finishes cards when listed on the matching event. Live passes refetch with a 45s TTL. Failed refresh uses a labeled stale snapshot only if younger than 15 minutes; older prices are suppressed. Edges are vs proportional de-juice; tickets still have to beat the posted decimal. Unmatched names are unavailable, not invented. Top-5/10/20/make-cut are ingested only when the coupon lists them — never synthesized from winner odds. Opening lines are stored only when a distinct prematch coupon exists (live coupon and/or `data/openings/` archive). Current in-play prices are never claimed as opens. Champions Tour finishes are not attached to PGA events.
- **Cut rule** uses ESPN `cutRound`. Playoff events with `cutRound=0` are treated as no-cut (make-cut ≈ 1 except WD).
- **Independent rounds given θ** ignore hot-round autocorrelation except insofar as live updates re-condition.
- **Operator leftover callout** (used vs unconstrained vs held-ticket residual) prints after `ingest` / `live` / pressure-test. Display only. It does not fill agronomy, tee pairing, narrative, or injury rumor. Spec: [PARKED_LEFTOVER_CALLOUT.md](PARKED_LEFTOVER_CALLOUT.md).
- **A/B compare method** is paper/mock only. Lived `{event}.json` is a museum: lock frozen (`--lock-paper` off), live apply still mutates until official settle. After settle, leftover Winner quotes are not a new market (voided at cost). Compare ledgers started at $250 and must not write `ledger.json`. St. Jude (`401811962`) stays Winner-only. Later events ticket Top 5/10/20 when a real coupon exists (never from Winner odds) and score Winner vs place posted P/L as two lines. See [COMPARE_METHOD.md](COMPARE_METHOD.md).

## What it will not do

- Place bets (strategy suggestions are not tickets)
- Hide interval width
- Treat print-matching a sportsbook as clearance
- Replace the user’s residual judgment
- Modify Gated Progressive Formalization
