# Free-parameter system

## Design

1. **Start broad.** Every catalog factor is on the board as unconstrained or parked (live-only).
2. **Rank importance** as `impact(course_type) × constrainingability`.
3. **Constrain** only when quality and sample size justify it (`CONSTRAINED` / `PARTIALLY_CONSTRAINED` / `UNCONSTRAINED` / `PARKED`).
4. **Course type** rescales impact (links wind, major bogey-avoidance, mountain distance, etc.).

## Required families (always present)

| ID | Role |
|----|------|
| `talent_prior` | Long-term talent |
| `course_fit` | Layout match |
| `recent_form` | Recent SG / finishes |
| `short_term_trend` | Direction of form, not level |
| `sg_match` | SG mix vs what the course pays |
| `weather_suitability` | Wind/rain/altitude splits |
| `health_setup` | Injury / equipment notes (often low quality) |
| `narrative_momentum` | Storylines — **hard-capped** so they cannot dominate |

Plus structural factors: course history, driving distance/accuracy, approach, ARG, putting, scrambling, bogey avoidance, par-5s, wind history, rest/travel, comparable borrow, venue-cluster borrow, field interaction, live position, live tee/pairing.

## Importance

See `free_parameters/ranking.py`. Example: `weather_suitability` importance rises on `links`; `bogey_avoidance` rises on `major_setup`.

## Open questions

Unconstrained high-importance factors are listed on every player row. They are not silently zeroed.
