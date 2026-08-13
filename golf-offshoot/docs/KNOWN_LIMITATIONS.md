# Known limitations

The system is honest about where it is weak. These are not “TODO cosmetics”; they are structural.

## Weak spots

- **New course setups / renovations** with little history: course-fit and course-history stay unconstrained; venue-cluster borrow is a shrink toward *similar* courses, not knowledge of a new cut of rough.
- **Sudden major swing / putting changes** that have not shown up in SG windows: short-term trend can only move as far as quality allows; narrative about a “new swing” is capped.
- **Lesser-known / opposite-tour players:** wider priors, more borrow, lower reliability. Do not read a tight Win interval as confidence.
- **Extreme weather outliers** (hurricane delay, 40 mph, altitude not in the player’s history): weather factor quality will be low unless a real split exists.
- **Health news** is usually sparse and late. Low quality by design; a rumor must not clear a favorite.
- **Live hole-by-hole** is approximated (to-par + holes completed), not a shot-by-shot remaining-strokes model.
- **Cut rule** is “place plus ties” after N rounds. Playoff, 36-hole cut exceptions, and projected-cut live lines are simplified.
- **Correlation in the book** uses θ proximity (decision screen) plus cut-risk / SG-style / weather slices (strategy layer), not a fitted copula of finishes.
- **Strategy MTM** is a decimal-odds ratio, not an exchange cash-out. Open positions exist only if the user records them.
- **Market** mocks do not include limit availability, steam, or exchange liquidity.
- **Weights** are expert-initialized. Calibration needs a season of logged results; do not treat α as fitted truth.
- **Independent rounds given θ** ignore hot-round autocorrelation except insofar as live updates re-condition.

## What it will not do

- Place bets (strategy suggestions are not tickets)
- Hide interval width
- Treat print-matching a sportsbook as clearance
- Replace the user’s residual judgment
- Modify Gated Progressive Formalization
