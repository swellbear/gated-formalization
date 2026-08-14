# Historical calibration (first pass)

## What is fitted

Factor weights `α` in `Δθ = α × quality × constrainingability × evidence × stacking_discount`, plus ARD scales.

SG-category weights are moved **only** when as-of THROUGH_EVENT coverage on the panel is real (≥ 40%). Otherwise they stay at expert values.

Calibrated keys: `recent_form`, `short_term_trend`, `course_history`, `course_fit`, `weather_suitability`, `field_interaction`, `comparable_player_borrow`.

## Dataset (no future leakage)

1. ESPN completed PGA leaderboards for 2025–2026 (cached).
2. Open-Meteo **archive** wind/rain at the event city for those weeks.
3. For event **T**, every feature uses only events with `start_date < T.start_date`.
4. Current-season ESPN athlete rankings are **not** used as calibration features (they are season-to-date and would leak).
5. Burn-in: first completed events are history-only (not scored).
6. Hold-out: last 3 completed events. Never used to accept a candidate `α`.

Target outcomes: make cut, top 20, top 10, top 5, win. Scoring: **Brier** and **log loss** on all five, with a slight extra Win Brier term.

## Optimizer

Independent-Gaussian **Bayesian search** around expert `α`:

- Prior mean = expert-initialized `DEFAULT_ALPHA`.
- Per-coordinate length-scales `ell_k` (ARD): coordinates that do not change train loss shrink.
- Random samples from `N(μ, ell²)`, clipped to `[0, 1.2]`.
- Coordinate refinement around the best train score.
- ARD diagnostics: leave-one-weight-out Δloss on train; `ard_scale = relevance / (relevance + τ)`.

Production MC is still the ranking engine; calibration uses the same `update_theta` + a smaller MC (`n_sims≈180`) so the search is tractable.

## Artifacts

Frozen JSON: `data/calibration/weights_calib-v1.json`

Fields: calibrated vs expert `α`, ARD relevance, bounds hit, train/holdout Brier+logloss, event ids, `no_future_leakage: true`, `recommendation` = `use_calibrated` or `keep_expert`.

Default production behavior: use calibrated weights **only if** hold-out proper score beats expert by a small margin; otherwise keep expert `α` and still store the fit.

```bash
python -m golf_offshoot calibrate
# or
python scripts/calibrate.py
```

## First-pass results (2026-08-13)

- History: **82** completed ESPN PGA events (2025–2026).
- Train (8): RBC Canadian Open → Corales Puntacana. Hold-out (3): 3M Open, Rocket Classic, Wyndham.
- n = 1119 train player-starts, 438 hold-out.
- Hold-out Win Brier: expert **0.00684** vs fitted **0.00685** (no material gain).
- Recommendation frozen: **`keep_expert`**. Fitted vector stored for comparison. Bounds hit at 0: `recent_form`, `short_term_trend`, `comparable_player_borrow`.
- ARD: leave-one-out deltas are tiny; finish-derived form barely moves proper score beyond the talent prior. SG weights were not fitted (inputs unavailable).


This is a **first** pass: one-and-a-half seasons of finish-derived features, no as-of SG, no historical odds. Do not treat `α` as a settled physical constant.

## 0.4.0 — no second freeze

Odds and SG now flow on the **current** event, but:

- PGA SG StatDetails is a season-to-date table. Using the August 2026 table as a feature for June events would leak later-season rounds.
- Bovada coupons are live snapshots, not an opening-line archive.

Recalibrating on finish-only features again is forbidden by the product prompt. Production remains **`keep_expert`**. A new frozen vector requires an as-of SG (and preferably odds) panel plus a material hold-out win over expert.

## 0.6.0 — as-of SG panel

Long-term SG for event T is `THROUGH_EVENT` of the last completed PGA pill with `start < T.start`. Recent SG is the mean of up to 8 `EVENT_ONLY` tables for such pills. Season-to-date is not a last-8 proxy.

Calibration now attaches those as-of features to the leakage-safe historical panel. SG-category keys (`sg_match`, `approach_sg`, `around_green`, `putting`) enter the search only if long-term coverage ≥ 40%. Bayesian search runs only if recent-SG coverage ≥ 30%. Otherwise the run is skipped (not a finish-only refit).

Hold-out must still beat expert `scalar_loss` by 0.001 to freeze. Artifact: `data/calibration/weights_calib-v2.json`. `calib-v1` is retained for comparison.

Default production behavior is unchanged unless that artifact’s `recommendation` is `use_calibrated`.

## 0.6.0 results (2026-08-13)

- Panel: 8 train (RBC Canadian Open → Corales) + 3 hold-out (3M, Rocket, Wyndham). Pre-event features only.
- As-of coverage on 1557 player-starts: recent EVENT_ONLY **74.2%**, THROUGH_EVENT long-term **60.4%**. Search ran. Fitted keys included `recent_form` plus SG categories.
- Hold-out Win Brier: expert **0.00689** vs fitted **0.00690** (no material gain; fitted slightly worse on Win and make-cut).
- Bounds hit at 0: `short_term_trend`. ARD: `recent_form` / `sg_match` near-zero leave-one-out relevance on this small panel; `course_fit` carried most of the ARD mass.
- Recommendation frozen: **`keep_expert`**. Fitted vector stored in `weights_calib-v2.json` for comparison. Production stays expert-initialized.

True as-of SG is now an operating feature. It did not yet buy a better hold-out proper score than expert α on 11 events. Do not treat the fitted vector as a freeze.

## 0.7.0 — deeper EVENT_ONLY window

Recent SG now requests the last **16** completed PGA `EVENT_ONLY` pills (still skip-missing, never zero-filled, never a season-to-date slice). Pills are loaded for three StatDetails seasons. Per-player quality scales with measured weeks.

Recalibration runs **only if** the leakage-safe panel is materially stronger than calib-v2: median measured events ≥ 5 (was 3 on the 8-week St. Jude field) or recent coverage ≥ 85% (was 74.2%). Otherwise BO is not rerun just to show activity. Hold-out must still beat expert `scalar_loss` by 0.001 to freeze. Artifact: `data/calibration/weights_calib-v3.json`.

Default production behavior is unchanged unless that artifact’s `recommendation` is `use_calibrated`.

## 0.7.0 results (2026-08-13)

- Decision: **run search**. St. Jude 16-week field: median **7** measured EVENT_ONLY events/player (p10=5, p90=9, mean 6.8), coverage **69/69**. Historical panel (12 train + 3 hold-out, 2064 player-starts): recent coverage **78.6%**, median **6** measured events, long-term THROUGH_EVENT **64.0%**. That clears the material-strength bar vs calib-v2 (median 3, coverage 74.2%).
- Train: PGA Championship → Corales. Hold-out: 3M Open, Rocket Classic, Wyndham. Pre-event features only. Calibration history includes 2024–2026 ESPN events (130 completed) so 2024 pills can be dated; the operating path still uses 2025–2026 for talent/form.
- Search ran (BO + ARD). Fitted keys included `recent_form` plus SG categories. Fitted `recent_form` hit the 0 bound; leave-one-out ARD relevance on this panel is near-zero for almost every moved key (`approach_sg` carried the ARD mass).
- Hold-out Win Brier: expert **0.00693** vs fitted **0.00691** (tiny, not a 0.001 scalar-loss win). Make-cut Brier essentially tied.
- Recommendation frozen: **`keep_expert`**. Fitted vector stored in `weights_calib-v3.json`. Production stays expert-initialized.

A deeper true as-of window improved coverage and measured-event depth. It still did not buy a freeze-worthy hold-out proper score. Do not treat the fitted vector as a freeze.
