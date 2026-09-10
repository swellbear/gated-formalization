# Operator note — RUN-ONLY of Lab PROPOSED 03 (skip the hour-ending 15m close)

**Verdict:** **RUN-ONLY** · Operator · 2026-09-10 13:36 EDT
**Not an ADMIT.** Not Softened. Not a dated record. Not a dashboard figure.
**Lane:** `learning_lane_15m` · series `KXBTC15M` only · `lab_admits=false` · Trading **NOT ARMED**
**Candidate:** [`LEARNING_LANE_15M_LAB_PROPOSED_03.md`](LEARNING_LANE_15M_LAB_PROPOSED_03.md)
**Registry id:** `R-SKIP-HOUR-CLOSE` in [`LEARNING_LANE_15M_RULES.json`](LEARNING_LANE_15M_RULES.json)

This note is the only place this ruling lives. It does not go in `manifest.json`, the digest, the hub, `records[]`, or any dated record. Selecting is **not** an edge, not a hit rate, not evidence of method quality, and not evidence toward lifting the Founder HOLD.

---

## Ruling (this is the decision)

1. **The test runs.** It is deterministic, adds no loop code (`_express_selection` already dispatches `params.skip_close_minute` / `close_minute_eq`; `paper.py` already consults `decide()`), quarantines output here, and carries one live falsifier (n named by the bar in force, currently `looks.first_look_n = 70`; indistinguishable from `R-BASELINE-FILL-ALL` → park; do not retune `skip_close_minute`). All four Protocol RUN-ONLY gates hold.
2. **No specific objection.** "Be careful" is not one. Burned-class and pre-registration checks are below. None fire.
3. **`execution=true` on this row only** (paper implementation). Dead `R-SKIP-2TO1-FAVORITE` is dropped off the selecting seat (`execution` true → false; the L1 PARK stands). `R-SKIP-COINFLIP` stays `execution=false`. `binding` is not touched. `trading_armed` stays false. The HOLD stands. This turn **does not score**.

---

## Four gates

| Gate | Holds? | Why |
|---|---|---|
| Deterministic | **Yes** | Skip when `close_at.minute == 0`, else fill at the posted mark with `entry_edge=0.0`. No new collection. No wait-to-start. |
| No new loop code | **Yes** | Expression already in `rules._express_selection`. The paper path already calls `consult_registry` → `decide()`. This turn flips a registry flag. |
| Output quarantined | **Yes** | This note. Not the hub, digest, manifest, `records[]`, or a dated record. |
| Live falsifier | **Yes** | After the n the bar names (70), if selected-fill `settlement_pnl` cannot be distinguished from `R-BASELINE-FILL-ALL` on those same windows, park this rule. Do not retune `skip_close_minute`. Do not replace 0 with a tape-chosen slot. |

---

## Objections considered (none sustained)

| Candidate objection | Verdict | Why |
|---|---|---|
| SKIP-2TO1-FAVORITE / RETUNE-FAVORITE-ODDS (burned) | **Does not fire** | Different class. Free parameter is `skip_close_minute=0`, a civil-clock minute, not `favorite_odds` and not a posted-YES cut. `favorite_odds` is not retuned. |
| RETUNE-COINFLIP-BAND (burned) | **Does not fire** | Different class, different parameter, different skip region (hour-ending close, not `(0.45, 0.55)`). `R-SKIP-COINFLIP` is not revived and its band is not touched. |
| FEE-AS-SIGNAL (burned) | **Does not fire** | The rule does not read `k`, posted YES, or the fee table. Hour-ending is series structure, not a cheap-YES region. |
| SEAS-DIR / SPREAD / THRESH / other oil burns | **Does not fire** | `class_is_burned("SKIP-HOUR-CLOSE")` is false. A 15m fill-or-skip on a civil-clock minute is not oil month-of-year *direction* and not a spread or mark threshold. |
| `skip_close_minute=0` already an informing mark | **Does not fire** | First naming is the Lab declaration commit **`c917e56`** at `declared_at` `2026-09-10T13:25:00-04:00`. Tree search for `skip_close_minute` / this hour-ending cutoff finds only that declaration and its follow-on docs. `0` is the hour. This turn did **not** open `paper/`, the RUN-ONLY fee table, the digest, the manifest, or a scorecard window row to choose or check the minute. |
| Golf idle / park row 8 "third PROPOSED not owed" | **Does not fire** | A CoS-assigned `KXBTC15M` paper PROPOSED is not golf idle-breach. Park row 8's leftover "third not owed" was restated after PROPOSED 02. CoS assigned Lab under `F_continuation` after favorite L1 PARK (no live trial). This is that residual, now RUN-ONLY. |
| Favorite still `execution=true` after L1 PARK | **Not an objection to RUN-ONLY** | Only one selecting rule may execute. The score turn left the dead row on the seat; this RUN-ONLY takes the only seat (dead row off, new row on). Not a re-score and not a retune of `favorite_odds`. |
| Bar Established unreachable / `favorite_odds=2` not pre-registered | **Not an objection to RUN-ONLY** | Those block Established / ADMIT. They do not block paper execution. "Cannot admit" is not "cannot compute." Binding is not touched this turn. |

---

## Execution flip (paper only)

| | |
|---|---|
| Rule | `R-SKIP-HOUR-CLOSE` |
| `declared_at` | `2026-09-10T13:25:00-04:00` |
| First-naming commit | `c917e56` |
| `execution` | **false → true** this turn |
| Flipped at | `2026-09-10T13:36:00-04:00` |
| Flip commit | the commit that lands this note |
| Seat | `R-SKIP-2TO1-FAVORITE` `execution` **true → false** this turn (L1 PARK already closed on the falsifier; dead skip must not own the next trial) |
| Not flipped | `R-SKIP-COINFLIP` (`execution` stays false) |
| Not set | `binding`, `trading_armed` |

`active_execution_rule()` will honour this row over the baseline. Two selecting rules with `execution=true` would raise; only this selecting row is live.

Replay of windows that closed after `declared_at` and before this flip is still replay, not lived. Lived paper skips/fills begin at the flip. This turn does not treat replay as lived and does not score either set.

---

## What this does not do

- **Not an edge.** Not established, not banked, not measured, not implied.
- **Not an admit.** `lab_admits=false`. Promotion still requires the normal ADMIT gate, a binding bar, and a Soften Critic attack from a separate session.
- **Not a score.** `score_rule` was not called. No scorecard was opened. No post-declaration outcome file was opened to write this. `R-SKIP-COINFLIP` was not scored. PARK'd `R-SKIP-2TO1-FAVORITE` was not re-scored.
- **Not a bind, not an arm.** `binding` is not touched. `trading_armed` stays false. The HOLD stands.
- **Not a revival of `R-SKIP-COINFLIP`.** Do not score that rule. Do not retune `(0.45, 0.55)`.
- **Not a retune of `favorite_odds`.** The L1 PARK stands. Class `SKIP-2TO1-FAVORITE` stays burned.
- **Not a lineage merge.** Lineage B's published `+1.67` is neither re-derived nor summed.
- **Not a second series.** `KXBTC15M` only. Golf idle stays **ON**.

---

## Park consequence

Park row 8 is **restated**, not closed: `F_continuation` after favorite L1 PARK used the third cheap-test slot. A fourth named horse is not owed without a fresh Founder GO. Fills that still happen remain `entry_edge=0.0`; that honesty lives here, not as a new open park.

---

## Falsifier (live, not evaluated)

After the n named by the evidence bar in force (currently `looks.first_look_n = 70`), if selected-fill `settlement_pnl` cannot be distinguished from `R-BASELINE-FILL-ALL` on those same windows, **park this rule**. Do not retune `skip_close_minute`. Do not replace `0` with a tape-chosen slot. The bar is the governing source.

This turn does not evaluate the falsifier. n is not counted here.

Golf idle stays ON. HOLD stands. Trading is **NOT ARMED**.
