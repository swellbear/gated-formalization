# Pressure test — 2026 FedEx St. Jude Championship

As of 2026-08-13T20:07:11.428159+00:00 UTC. **Never auto-bet.** Operating path only (no mocks). Model `golf-offshoot-0.7.0`

- Tournament: **FedEx St. Jude Championship** (`401811962`)
- Course: TPC Southwind · par 70 · 7288 yd
- Cut: no (playoff field) · start 2026-08-13
- Run: `20260813T200707Z-153c5f0c` mode=pre_tournament
- Weights: expert-initialized; calibrated artifact golf-offshoot-0.7.0-calib-v3 stored but not selected
- Weather: Partly sunny
- Odds quotes: 68 · overround: {'win': 1.372394083041732}
- SG coverage: 67/69
- Recent-SG feature players: 69
- recent_form board from as-of: 69
- recent_form dtheta players: 69
- Opening quotes: 0

## Source inventory

```
Field                        Kind                 Src                              Q  Coverage
----------------------------------------------------------------------------------------------------
player_identification_field  real_live            espn_field                    0.92  69/69
    notes: ESPN leaderboard competitors
    if missing: cannot rank without a field
long_term_talent             derived_from_real    espn_leaderboard_history      0.80  all players with prior starts
    notes: finish-skill from 82 completed ESPN events
    if missing: new players stay near 0 with wide SD
owgr                         unavailable          owgr                          0.00  0
    notes: ESPN rankings endpoint empty; OWGR not connected
    if missing: no official world rank; talent is finish-derived only
strokes_gained_categories    real_historical      pga_tour_sg                   0.88  67/69 (missing 2)
    notes: PGA Tour StatDetails year=2026 window=THROUGH_EVENT:R2026013 lastProcessed='Through the Wyndham Championship, Aug 9'; 164 players; categories OTT/APP/ARG/PUTT/Total; THROUGH_EVENT as-of Wyndham Championship start=2026-08-06 (before 2026-08-13); THROUGH_EVENT attached 66/69; prior-season fallback 1/69; unmatched: Alex Fitzpatrick, Jackson Koivun
    if missing: SG match/approach/ARG/putting unconstrained for unmatched players
strokes_gained_recent_window derived_from_real    pga_tour_sg_event_only        0.80  69/69
    notes: mean of 16/16 requested PGA EVENT_ONLY SG tables before 2026-08-13: Wyndham Championship (2026-08-06), Rocket Classic (2026-07-30), Corales Puntacana Championship (2026-07-16), ISCO Championship (2026-07-09), Genesis Scottish Open (2026-07-09), John Deere Classic (2026-07-02), Travelers Championship (2026-06-25), RBC Canadian Open (2026-06-11), the Memorial Tournament presented by Workday (2026-06-04), Charles Schwab Challenge (2026-05-28), THE CJ CUP Byron Nelson (2026-05-21), PGA Championship (2026-05-14), Truist Championship (2026-05-07), ONEflight Myrtle Beach Classic (2026-05-07), Cadillac Championship (2026-04-30), RBC Heritage (2026-04-16); 293 players with >=1 measured event; missing weeks skipped not zero-filled; not a season-to-date slice; events=Wyndham Championship (2026-08-06), Rocket Classic (2026-07-30), Corales Puntacana Championship (2026-07-16), ISCO Championship (2026-07-09), Genesis Scottish Open (2026-07-09), John Deere Classic (2026-07-02), Travelers Championship (2026-06-25), RBC Canadian Open (2026-06-11), the Memorial Tournament presented by Workday (2026-06-04), Charles Schwab Challenge (2026-05-28), THE CJ CUP Byron Nelson (2026-05-21), PGA Championship (2026-05-14), Truist Championship (2026-05-07), ONEflight Myrtle Beach Classic (2026-05-07), Cadillac Championship (2026-04-30), RBC Heritage (2026-04-16); median_events_per_player=7.0; p10=5.0 p90=9.0; window_requested=16; ott long=66 recent=69; app long=66 recent=69; arg long=66 recent=69; putt long=66 recent=69; total long=66 recent=69
    if missing: recent SG stays unconstrained; finish-residual form is not a last-N SG window
season_driving_putts         real_live            espn_athlete_season_ranking   0.68  69/69
    notes: yards/drive, accuracy %; putts/GIR only if SG:PUTT missing
    if missing: length/accuracy/putting proxies weaker
recent_form_trend            derived_from_real    espn_leaderboard_history      0.70  players with ≥1 prior start
    notes: pre-event residuals from prior events only
    if missing: form unconstrained
course_history               derived_from_real    espn_same_course_history      0.55  thin if course not in 2025–26 sample
    notes: same ESPN course id across loaded seasons
    if missing: course history unconstrained; reliability down
course_identity              real_live            espn_event_courses            0.85  1
    notes: yards/par/name from ESPN; course_type parkland is default inland parkland heuristic; firmness/rough/green_speed/tightness unavailable (defaults not used as evidence)
    if missing: yards/par real; agronomy unavailable
course_setup_agronomy        unavailable          course_setup_agronomy         0.00  0
    notes: firmness/rough/green speed not published on ESPN; left unconstrained
    if missing: tightness/rough/stimp not evidence
weather                      real_live            espn_accuweather              0.72  event
    notes: current conditions attached to ESPN course object (AccuWeather)
    if missing: weather suitability unconstrained
market_odds                  real_live            bovada                        0.78  68/69
    notes: Bovada FedEx St. Jude Championship lastModified=2026-08-13T19:37:22.320000+00:00; winner matched 68/69; unmatched names 1; markets=['Winner Live']; top10=unavailable on this coupon; top5=unavailable; top20=unavailable; make_cut=unavailable; opening=unavailable (no distinct prematch coupon); urls=['bovada_slug_fedex-st-jude-championship', 'bovada_golf_prematch', 'bovada_golf_live', 'bovada_pga_coupon', 'bovada_golf_coupon']; fetched_at=2026-08-13T19:57:13.585012+00:00; cached=True; age_s=594; ttl_s=600; odds_ttl_policy=pre_600s; feed=bovada; unmatched players have no invented price; de-juice is proportional (implied_fair = implied_raw / Σimplied_raw); decision layer requires model_p > 1/decimal (beat the posted number); place/top-10 never synthesized from winner odds
    if missing: no edges; strategy cannot size into a book; unmatched names are unavailable not invented
market_odds_place_top10      unavailable          bovada                        0.00  0/69
    notes: top10=0/69 top5=0/69 top20=0/69 make_cut=0/69; unavailable=top_5, top_10, top_20, make_cut; never synthesized from winner odds
    if missing: place/top-10 edges stay unavailable unless a real coupon exists
market_odds_opening          unavailable          bovada                        0.00  0
    notes: distinct prematch coupons tagged line_role=opening n=0; current in-play Winner Live is not treated as an opening line; archived prematch is used only if captured before the market flipped live
    if missing: no open-to-current movement; live prices are not claimed as opens
health_injury                unavailable          injury_wire                   0.00  WD only
    notes: no injury wire; WD status only
    if missing: injury rumours cannot move θ
cut_rule                     real_live            espn_tournament_cutRound      0.90  event
    notes: has_cut from ESPN cutRound
    if missing: has_cut=False
```

## Ranked field (top 12)

```
  # Player                        Win        T10        Cut    EdgeW   Rel Flags
----------------------------------------------------------------------------------------
  1 Scottie Scheffler      0.137[0.11-0.17]      0.581      1.000   +0.039  0.75 
  2 Tommy Fleetwood        0.055[0.03-0.08]      0.362      1.000   -0.026  0.74 
  3 Matt Fitzpatrick       0.046[0.03-0.06]      0.329      1.000   +0.012  0.75 
  4 Cameron Young          0.035[0.02-0.05]      0.279      1.000   +0.010  0.77 
  5 Si Woo Kim             0.035[0.02-0.05]      0.270      1.000   +0.026  0.79 
  6 Sam Burns              0.035[0.02-0.05]      0.252      1.000   -0.008  0.76 
  7 Jackson Koivun         0.033[0.02-0.05]      0.232      1.000   +0.029  0.61 thin_sample_overconfidence,sparse_data
  8 Ludvig Åberg           0.030[0.02-0.04]      0.225      1.000   +0.002  0.74 
  9 Russell Henley         0.028[0.01-0.04]      0.235      1.000   +0.023  0.74 
 10 Hideki Matsuyama       0.026[0.02-0.04]      0.209      1.000   -0.030  0.77 
 11 Collin Morikawa        0.025[0.01-0.04]      0.220      1.000   +0.004  0.73 
 12 Xander Schauffele      0.023[0.02-0.03]      0.234      1.000   -0.033  0.73 
```

## Real market edges (top 10 vs de-juiced win)

Proportional de-juice: `implied_fair = implied_raw / Σ implied_raw`. Decision/strategy still require beating the **posted** decimal (`model_p > 1/odds`). Unmatched players have no invented price.

```
  1 Scottie Scheffler      model=0.137 fair=0.097 posted=7.50 edge_fair=+0.039
  7 Jackson Koivun         model=0.033 fair=0.004 posted=176.00 edge_fair=+0.029
  5 Si Woo Kim             model=0.035 fair=0.009 posted=81.00 edge_fair=+0.026
  9 Russell Henley         model=0.028 fair=0.005 posted=151.00 edge_fair=+0.023
 13 Patrick Cantlay        model=0.023 fair=0.005 posted=151.00 edge_fair=+0.018
 19 Robert MacIntyre       model=0.015 fair=0.000 posted=2501.00 edge_fair=+0.015
 14 Tom Kim                model=0.022 fair=0.009 posted=81.00 edge_fair=+0.013
 22 Jordan Smith           model=0.014 fair=0.001 posted=501.00 edge_fair=+0.013
 20 Rory McIlroy           model=0.015 fair=0.003 posted=251.00 edge_fair=+0.012
  3 Matt Fitzpatrick       model=0.046 fair=0.035 posted=21.00 edge_fair=+0.012
```

## Place / finish market coverage

Winner and place markets stay separated. Place prices are never synthesized from winner odds. Opening lines are counted only when a distinct prematch coupon exists beside the current price.

```json
{
  "field_size": 69,
  "synthesized": false,
  "by_market": {
    "win": {
      "n": 68,
      "available": true,
      "coverage": "68/69",
      "books": [
        "bovada_live"
      ],
      "as_of": "2026-08-13T19:37:22.320000+00:00"
    },
    "top_5": {
      "n": 0,
      "available": false,
      "coverage": "0/69",
      "books": [],
      "as_of": null
    },
    "top_10": {
      "n": 0,
      "available": false,
      "coverage": "0/69",
      "books": [],
      "as_of": null
    },
    "top_20": {
      "n": 0,
      "available": false,
      "coverage": "0/69",
      "books": [],
      "as_of": null
    },
    "make_cut": {
      "n": 0,
      "available": false,
      "coverage": "0/69",
      "books": [],
      "as_of": null
    }
  },
  "available_markets": [
    "win"
  ],
  "unavailable_markets": [
    "top_5",
    "top_10",
    "top_20",
    "make_cut"
  ],
  "opening_quotes": 0,
  "opening_available": false,
  "notes": "Place/top-10 ingested only when the source coupon lists them. Winner odds are never converted into place prices. Opening lines counted only when a distinct prematch coupon exists alongside the current (usually live) price."
}
```

### Top 5

```
top_5 coupon unavailable (not synthesized from winner odds)
```

### Top 10

```
top_10 coupon unavailable (not synthesized from winner odds)
```

### Top 20

```
top_20 coupon unavailable (not synthesized from winner odds)
```

### Make cut

```
make_cut coupon unavailable (not synthesized from winner odds)
```

## Coherence / edges / reliability

- All displayed centrals satisfy Win ≤ T5 ≤ T10 ≤ T20 ≤ Make Cut
- 68 players have win edges; max +0.039 min -0.037
- Reliability median 0.75 min 0.61

## Explainability (top 5)

### 1. Scottie Scheffler

- Win 0.137 [0.106, 0.167]
- T10 0.581 Make cut 1.000
- Reliability 0.75 (many free parameters still open)
- Posted win odds: 7.5
- Posted top-5 odds: unavailable
- Posted top-10 odds: unavailable
- Posted top-20 odds: unavailable
- Posted make-cut odds: unavailable
- Fair implied win: 0.09715382409534835
- Edge vs fair win: 0.039346175904651656
- Edge vs fair top-5: unavailable
- Edge vs fair top-10: unavailable
- Edge vs fair top-20: unavailable
- Edge vs fair make-cut: unavailable
- SG factors: approach_sg dtheta=+0.053 q=0.88; sg_match dtheta=+0.143 q=0.88; recent_form dtheta=+0.140 q=0.57; around_green dtheta=+0.011 q=0.88; putting dtheta=+0.012 q=0.88
- Open: Wind / firm-and-fast splits unconstrained at start; Comparable-player borrowed strength unconstrained at start; Driving accuracy not fully pinned; Par-5 scoring unconstrained at start
- Flags: none
- Scottie Scheffler: prior θ=1.68 → posterior 2.28 ± 0.28. Strokes-gained match +0.143θ (q=0.88); Recent form +0.140θ (q=0.57); Course fit +0.069θ (q=0.50); This-course / this-event history +0.062θ (q=0.54); Approach (SG:APP) +0.053θ (q=0.88); Field-composition relative value +0.047θ (q=0.70); Driving distance +0.030θ (q=0.68).

### 2. Tommy Fleetwood

- Win 0.055 [0.026, 0.084]
- T10 0.362 Make cut 1.000
- Reliability 0.74 (many free parameters still open)
- Posted win odds: 9.0
- Posted top-5 odds: unavailable
- Posted top-10 odds: unavailable
- Posted top-20 odds: unavailable
- Posted make-cut odds: unavailable
- Fair implied win: 0.08096152007945695
- Edge vs fair win: -0.02596152007945695
- Edge vs fair top-5: unavailable
- Edge vs fair top-10: unavailable
- Edge vs fair top-20: unavailable
- Edge vs fair make-cut: unavailable
- SG factors: approach_sg dtheta=+0.030 q=0.88; sg_match dtheta=+0.090 q=0.88; recent_form dtheta=+0.086 q=0.60; around_green dtheta=+0.013 q=0.88; putting dtheta=+0.003 q=0.88
- Open: Wind / firm-and-fast splits unconstrained at start; Comparable-player borrowed strength unconstrained at start; Driving accuracy not fully pinned; Par-5 scoring unconstrained at start
- Flags: none
- Tommy Fleetwood: prior θ=1.11 → posterior 1.55 ± 0.28. Strokes-gained match +0.090θ (q=0.88); Recent form +0.086θ (q=0.60); Course fit +0.066θ (q=0.50); This-course / this-event history +0.062θ (q=0.54); Field-composition relative value +0.038θ (q=0.70); Approach (SG:APP) +0.030θ (q=0.88); Driving accuracy +0.028θ (q=0.68).

### 3. Matt Fitzpatrick

- Win 0.046 [0.031, 0.062]
- T10 0.329 Make cut 1.000
- Reliability 0.75 (many free parameters still open)
- Posted win odds: 21.0
- Posted top-5 odds: unavailable
- Posted top-10 odds: unavailable
- Posted top-20 odds: unavailable
- Posted make-cut odds: unavailable
- Fair implied win: 0.034697794319767265
- Edge vs fair win: 0.011802205680232734
- Edge vs fair top-5: unavailable
- Edge vs fair top-10: unavailable
- Edge vs fair top-20: unavailable
- Edge vs fair make-cut: unavailable
- SG factors: approach_sg dtheta=+0.077 q=0.88; sg_match dtheta=+0.104 q=0.88; recent_form dtheta=+0.099 q=0.60; around_green dtheta=+0.013 q=0.88; putting dtheta=+0.000 q=0.88
- Open: Wind / firm-and-fast splits unconstrained at start; Comparable-player borrowed strength unconstrained at start; Driving accuracy not fully pinned; Par-5 scoring unconstrained at start
- Flags: none
- Matt Fitzpatrick: prior θ=1.04 → posterior 1.41 ± 0.28. Strokes-gained match +0.104θ (q=0.88); Recent form +0.099θ (q=0.60); Approach (SG:APP) +0.077θ (q=0.88); Field-composition relative value +0.042θ (q=0.70); Driving accuracy +0.025θ (q=0.68).

### 4. Cameron Young

- Win 0.035 [0.017, 0.053]
- T10 0.279 Make cut 1.000
- Reliability 0.77 (many free parameters still open)
- Posted win odds: 29.0
- Posted top-5 odds: unavailable
- Posted top-10 odds: unavailable
- Posted top-20 odds: unavailable
- Posted make-cut odds: unavailable
- Fair implied win: 0.025125988990176297
- Edge vs fair win: 0.0103740110098237
- Edge vs fair top-5: unavailable
- Edge vs fair top-10: unavailable
- Edge vs fair top-20: unavailable
- Edge vs fair make-cut: unavailable
- SG factors: approach_sg dtheta=+0.047 q=0.88; sg_match dtheta=+0.074 q=0.88; recent_form dtheta=+0.057 q=0.64; around_green dtheta=+0.005 q=0.88; putting dtheta=-0.003 q=0.88
- Open: Wind / firm-and-fast splits unconstrained at start; Comparable-player borrowed strength unconstrained at start; Driving accuracy not fully pinned; Par-5 scoring unconstrained at start
- Flags: none
- Cameron Young: prior θ=0.98 → posterior 1.35 ± 0.27. Strokes-gained match +0.074θ (q=0.88); Course fit +0.060θ (q=0.50); Recent form +0.057θ (q=0.64); This-course / this-event history +0.052θ (q=0.54); Approach (SG:APP) +0.047θ (q=0.88); Driving distance +0.040θ (q=0.68); Field-composition relative value +0.036θ (q=0.70).

### 5. Si Woo Kim

- Win 0.035 [0.022, 0.048]
- T10 0.270 Make cut 1.000
- Reliability 0.79 (many free parameters still open)
- Posted win odds: 81.0
- Posted top-5 odds: unavailable
- Posted top-10 odds: unavailable
- Posted top-20 odds: unavailable
- Posted make-cut odds: unavailable
- Fair implied win: 0.008995724453272996
- Edge vs fair win: 0.025504275546727007
- Edge vs fair top-5: unavailable
- Edge vs fair top-10: unavailable
- Edge vs fair top-20: unavailable
- Edge vs fair make-cut: unavailable
- SG factors: approach_sg dtheta=+0.067 q=0.88; sg_match dtheta=+0.082 q=0.88; recent_form dtheta=+0.091 q=0.67; around_green dtheta=+0.005 q=0.88; putting dtheta=-0.003 q=0.88
- Open: Wind / firm-and-fast splits unconstrained at start; Comparable-player borrowed strength unconstrained at start; Driving accuracy not fully pinned; Par-5 scoring unconstrained at start
- Flags: none
- Si Woo Kim: prior θ=0.86 → posterior 1.25 ± 0.27. Recent form +0.091θ (q=0.67); Strokes-gained match +0.082θ (q=0.88); Approach (SG:APP) +0.067θ (q=0.88); Field-composition relative value +0.036θ (q=0.70); Course fit +0.032θ (q=0.50); This-course / this-event history +0.029θ (q=0.54); Driving accuracy +0.029θ (q=0.68).


## Strategy layer (advisory, sample bankroll $2000)

### protect_profits

```
strategy rec-a24331fd64 enabled=True never_auto_bet=True
Open exposure 0.00 (0% of bankroll) | unrealized +0.00 | weighted live edge +0.000 | concentration none 0% | posture Protect
```

### press_edges

```
strategy rec-8dea40f25d enabled=True never_auto_bet=True
Open exposure 0.00 (0% of bankroll) | unrealized +0.00 | weighted live edge +0.000 | concentration none 0% | posture Press
```

### stay_selective

```
strategy rec-f903d4c44a enabled=True never_auto_bet=True
Open exposure 0.00 (0% of bankroll) | unrealized +0.00 | weighted live edge +0.000 | concentration none 0% | posture Selective
```

## Live update (round in progress, hole-dampened)

Formula: until 18 holes, `dampen = (h/H) × (h/18)`; after 18 holes `dampen = h/H` with `H = 72`. `live_position` evidence = `(-score/3) × dampen`, quality = `0.30 + 0.65 × (h/H)`. Remaining score = current to-par + `(-θ × rem_rounds)` + `N(0, σ √rem_rounds)`. Prior un-dampened live run put Kitayama near 26% win from a Round-1 board; this run must not repeat that.

- Live run `20260813T200711Z-809ce53b`
- Kitayama pre Win 0.016
- Kitayama live Win 0.082 rank 3
- Live odds freshness: Bovada FedEx St. Jude Championship lastModified=2026-08-13T19:55:14.576000+00:00; winner matched 68/69; unmatched names 1; markets=['Winner Live']; top10=unavailable on this coupon; top5=unavailable; top20=unavailable; make_cut=unavailable; opening=unavailable (no distinct prematch coupon); urls=['bovada_slug_fedex-st-jude-championship', 'bovada_golf_prematch', 'bovada_golf_live', 'bovada_pga_coupon', 'bovada_golf_coupon']; fetched_at=2026-08-13T20:07:10.645983+00:00; cached=False; age_s=0; ttl_s=45; odds_ttl_policy=live_45s; feed=bovada; unmatched players have no invented price; de-juice is proportional (implied_fair = implied_raw / Σimplied_raw); decision layer requires model_p > 1/decimal (beat the posted number); place/top-10 never synthesized from winner odds
- Pre odds freshness: Bovada FedEx St. Jude Championship lastModified=2026-08-13T19:37:22.320000+00:00; winner matched 68/69; unmatched names 1; markets=['Winner Live']; top10=unavailable on this coupon; top5=unavailable; top20=unavailable; make_cut=unavailable; opening=unavailable (no distinct prematch coupon); urls=['bovada_slug_fedex-st-jude-championship', 'bovada_golf_prematch', 'bovada_golf_live', 'bovada_pga_coupon', 'bovada_golf_coupon']; fetched_at=2026-08-13T19:57:13.585012+00:00; cached=True; age_s=594; ttl_s=600; odds_ttl_policy=pre_600s; feed=bovada; unmatched players have no invented price; de-juice is proportional (implied_fair = implied_raw / Σimplied_raw); decision layer requires model_p > 1/decimal (beat the posted number); place/top-10 never synthesized from winner odds
```
  # Player                        Win        T10        Cut    EdgeW   Rel Flags
----------------------------------------------------------------------------------------
  1 Tommy Fleetwood        0.111[0.08-0.15]      0.608      1.000   +0.028  0.74 
  2 Scottie Scheffler      0.104[0.08-0.13]      0.559      1.000   +0.004  0.75 
  3 Kurt Kitayama          0.082[0.05-0.11]      0.536      1.000   +0.038  0.76 
  4 Michael Thorbjornsen   0.074[0.06-0.09]      0.433      1.000   +0.017  0.72 thin_sample_overconfidence,sparse_data
  5 Hideki Matsuyama       0.070[0.04-0.10]      0.483      1.000   +0.008  0.77 
  6 Matt Fitzpatrick       0.052[0.03-0.07]      0.390      1.000   +0.017  0.73 
  7 Xander Schauffele      0.043[0.02-0.07]      0.320      1.000   -0.002  0.71 
  8 Jordan Spieth          0.041[0.03-0.05]      0.349      1.000   +0.001  0.76 
```

### Pre vs live posted win (stale vs refreshed)

```
player                         pre_posted  live_posted  pre_model  live_model
Scottie Scheffler                   7.5          7.5     0.137      0.104 same_number
Matt Fitzpatrick                   21.0         21.0     0.046      0.052 same_number
Kurt Kitayama                      19.0         17.0     0.016      0.082 REFRESHED
Tommy Fleetwood                     9.0          9.0     0.055      0.111 same_number
Live pass uses a 45s odds TTL so a Winner coupon cached from pre (10 min TTL) is refetched when it can be. If this live ingest ran within 45s of pre, a cache hit is expected and is not the old 10-min reuse bug. If refresh fails, prices older than 15 min are suppressed rather than treated as live.
```

```
strategy rec-67489fc4f5 enabled=True never_auto_bet=True
Open exposure 0.00 (0% of bankroll) | unrealized +0.00 | weighted live edge +0.000 | concentration none 0% | posture Selective
```

### Live strategy modes (empty book, advisory)

#### protect_profits

```
strategy rec-cf7b81454b enabled=True never_auto_bet=True
Open exposure 0.00 (0% of bankroll) | unrealized +0.00 | weighted live edge +0.000 | concentration none 0% | posture Protect
```

#### press_edges

```
strategy rec-c9ed63f4bb enabled=True never_auto_bet=True
Open exposure 0.00 (0% of bankroll) | unrealized +0.00 | weighted live edge +0.000 | concentration none 0% | posture Press
```

#### stay_selective

```
strategy rec-d03c01dc7e enabled=True never_auto_bet=True
Open exposure 0.00 (0% of bankroll) | unrealized +0.00 | weighted live edge +0.000 | concentration none 0% | posture Selective
```

## Shadow journal (paper observation only)

Logged `new_bet` / `add` / `reduce` / `exit` / `reallocate` advises. Never auto-bet. Review later with `python -m golf_offshoot shadow`.

```
SHADOW JOURNAL (paper observation only — never auto-bet)
n=8 showing last 8

2026-08-13T18:53:32.293309+00:00 stay_selective new_bet Matt Fitzpatrick win posted=12.00 model_p=0.120 [0.089,0.151] stake=4.00 odds_as_of=2026-08-13T18:32:16.248000+00:00
    FedEx St. Jude Championship run=20260813T185332Z-d1cd18cb — Kelly is tiny after uncertainty haircut; sized to minimum advisory unit
2026-08-13T18:53:32.377107+00:00 protect_profits new_bet Matt Fitzpatrick win posted=12.00 model_p=0.120 [0.089,0.151] stake=4.00 odds_as_of=2026-08-13T18:32:16.248000+00:00
    FedEx St. Jude Championship run=20260813T185332Z-d1cd18cb — Kelly is tiny after uncertainty haircut; sized to minimum advisory unit
2026-08-13T18:53:32.384110+00:00 press_edges new_bet Matt Fitzpatrick win posted=12.00 model_p=0.120 [0.089,0.151] stake=4.00 odds_as_of=2026-08-13T18:32:16.248000+00:00
    FedEx St. Jude Championship run=20260813T185332Z-d1cd18cb — Kelly is tiny after uncertainty haircut; sized to minimum advisory unit
2026-08-13T18:53:32.390110+00:00 stay_selective new_bet Matt Fitzpatrick win posted=12.00 model_p=0.120 [0.089,0.151] stake=4.00 odds_as_of=2026-08-13T18:32:16.248000+00:00
    FedEx St. Jude Championship run=20260813T185332Z-d1cd18cb — Kelly is tiny after uncertainty haircut; sized to minimum advisory unit
2026-08-13T19:27:55.909030+00:00 stay_selective new_bet Matt Fitzpatrick win posted=13.00 model_p=0.108 [0.078,0.139] stake=4.00 odds_as_of=2026-08-13T18:52:23.715000+00:00
    FedEx St. Jude Championship run=20260813T192755Z-2b4c97a9 — Kelly is tiny after uncertainty haircut; sized to minimum advisory unit
2026-08-13T19:27:56.004816+00:00 protect_profits new_bet Matt Fitzpatrick win posted=13.00 model_p=0.108 [0.078,0.139] stake=4.00 odds_as_of=2026-08-13T18:52:23.715000+00:00
    FedEx St. Jude Championship run=20260813T192755Z-2b4c97a9 — Kelly is tiny after uncertainty haircut; sized to minimum advisory unit
2026-08-13T19:27:56.012816+00:00 press_edges new_bet Matt Fitzpatrick win posted=13.00 model_p=0.108 [0.078,0.139] stake=4.00 odds_as_of=2026-08-13T18:52:23.715000+00:00
    FedEx St. Jude Championship run=20260813T192755Z-2b4c97a9 — Kelly is tiny after uncertainty haircut; sized to minimum advisory unit
2026-08-13T19:27:56.019816+00:00 stay_selective new_bet Matt Fitzpatrick win posted=13.00 model_p=0.108 [0.078,0.139] stake=4.00 odds_as_of=2026-08-13T18:52:23.715000+00:00
    FedEx St. Jude Championship run=20260813T192755Z-2b4c97a9 — Kelly is tiny after uncertainty haircut; sized to minimum advisory unit

Review later: compare posted_decimal at odds_as_of to the settlement result for that player/market. This file is not a betting bot ledger.
```

## Recalibration decision

0.7.0 may run Bayesian search + ARD only when the leakage-safe as-of recent SG panel is materially stronger than calib-v2 (median measured EVENT_ONLY events >= 5 or coverage >= 85%) and coverage still clears 30%. A weak 16-week request is not a reason to rerun BO. Finish-only refits are still forbidden. `calib-v1`/`calib-v2` remain stored. Production uses calibrated weights only if the new artifact says `use_calibrated`.

## As-of SG coverage (this event)

```json
{
  "field_size": 69,
  "long_term_available": true,
  "long_term_source": "pga_tour_sg",
  "long_term_kind": "real_historical",
  "long_term_coverage": "66/69",
  "long_term_anchor": "Wyndham Championship",
  "recent_available": true,
  "recent_source": "pga_tour_sg_event_only",
  "recent_kind": "derived_from_real",
  "recent_coverage": "69/69",
  "recent_window_requested": 16,
  "recent_events_used": [
    "Wyndham Championship (2026-08-06)",
    "Rocket Classic (2026-07-30)",
    "Corales Puntacana Championship (2026-07-16)",
    "ISCO Championship (2026-07-09)",
    "Genesis Scottish Open (2026-07-09)",
    "John Deere Classic (2026-07-02)",
    "Travelers Championship (2026-06-25)",
    "RBC Canadian Open (2026-06-11)",
    "the Memorial Tournament presented by Workday (2026-06-04)",
    "Charles Schwab Challenge (2026-05-28)",
    "THE CJ CUP Byron Nelson (2026-05-21)",
    "PGA Championship (2026-05-14)",
    "Truist Championship (2026-05-07)",
    "ONEflight Myrtle Beach Classic (2026-05-07)",
    "Cadillac Championship (2026-04-30)",
    "RBC Heritage (2026-04-16)"
  ],
  "recent_events_used_n": 16,
  "recent_median_events_per_player": 7.0,
  "recent_p10_events_per_player": 5.0,
  "recent_p50_events_per_player": 7.0,
  "recent_p90_events_per_player": 9.0,
  "recent_mean_events_per_player": 6.768115942028985,
  "recent_players_with_window": 69,
  "by_category": {
    "ott": {
      "long_term": 66,
      "recent": 69
    },
    "app": {
      "long_term": 66,
      "recent": 69
    },
    "arg": {
      "long_term": 66,
      "recent": 69
    },
    "putt": {
      "long_term": 66,
      "recent": 69
    },
    "total": {
      "long_term": 66,
      "recent": 69
    }
  },
  "notes": "Recent window is EVENT_ONLY mean of up to 16 completed pills; missing weeks skipped not zero-filled. Season-to-date is not a last-N proxy. Depth is measured events per player, not the requested window length.",
  "datagolf": {
    "available": false,
    "source_kind": "unavailable",
    "notes": "DATA_GOLF_API_KEY / DATAGOLF_API_KEY not set; true as-of recent SG windows unavailable. PGA season StatDetails are not used as a last-8 proxy."
  },
  "players_with_recent_sg": 69
}
```

```json
{
  "recommendation": "keep_expert",
  "search_ran": true,
  "n_evals": 30,
  "holdout": {
    "n": 438,
    "brier": {
      "make_cut": 0.23419370118417737,
      "top_20": 0.1240320315780633,
      "top_10": 0.07342577055513565,
      "top_5": 0.040301079197110935,
      "win": 0.006911976148484086
    },
    "logloss": {
      "make_cut": 0.6594342657352446,
      "top_20": 0.3995547789294663,
      "top_10": 0.2655898177092005,
      "top_5": 0.1729529582076923,
      "win": 0.05799775713157398
    }
  },
  "holdout_expert": {
    "n": 438,
    "brier": {
      "make_cut": 0.23418337112622825,
      "top_20": 0.12442661039724533,
      "top_10": 0.07348995968757874,
      "top_5": 0.04015116318132191,
      "win": 0.0069327202485932665
    },
    "logloss": {
      "make_cut": 0.6594541175111673,
      "top_20": 0.40093039872265424,
      "top_10": 0.2654886637291467,
      "top_5": 0.17350370848698862,
      "win": 0.05801020322948785
    }
  },
  "bounds_hit": [
    "recent_form",
    "short_term_trend",
    "around_green"
  ],
  "train_event_ids": [
    "401811947",
    "401811948",
    "401811949",
    "401811950",
    "401811951",
    "401811952",
    "401811953",
    "401811954",
    "401811955",
    "401811956",
    "401811957",
    "401811958"
  ],
  "holdout_event_ids": [
    "401811959",
    "401811960",
    "401811961"
  ],
  "notes": [
    "Search is Bayesian in the sense of sampling from an independent-Gaussian prior centered on expert \u03b1, then updating per-coordinate mean/variance (ARD).",
    "Hold-out events are never used to accept a candidate.",
    "Fitted keys: recent_form, short_term_trend, course_history, course_fit, weather_suitability, field_interaction, comparable_player_borrow, sg_match, approach_sg, around_green, putting.",
    "SG category weights are in the search because as-of THROUGH_EVENT coverage is real.",
    "Hold-out did not clearly beat expert \u03b1; default recommendation is to keep expert weights in production and store the fitted vector for comparison."
  ],
  "asof_coverage": {
    "n_player_starts": 2064.0,
    "recent_sg": 0.7858527131782945,
    "long_term_sg": 0.6395348837209303,
    "recent_coverage": 0.7858527131782945,
    "median_events": 6.0,
    "p10_events": 2.0,
    "p90_events": 9.0,
    "mean_events": 5.5998766954377315,
    "window_requested": 16.0
  },
  "fitted_keys": [
    "recent_form",
    "short_term_trend",
    "course_history",
    "course_fit",
    "weather_suitability",
    "field_interaction",
    "comparable_player_borrow",
    "sg_match",
    "approach_sg",
    "around_green",
    "putting"
  ]
}
```
