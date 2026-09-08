# Operator note — RUN-ONLY of Lab PROPOSED 02 (skip a posted 2-to-1 YES favorite)

**Verdict:** **RUN-ONLY** · Operator · 2026-09-08 17:11 EDT
**Not an ADMIT.** Not Softened. Not a dated record. Not a dashboard figure.
**Lane:** `learning_lane_15m` · series `KXBTC15M` only · `lab_admits=false` · Trading **NOT ARMED**
**Candidate:** [`LEARNING_LANE_15M_LAB_PROPOSED_02.md`](LEARNING_LANE_15M_LAB_PROPOSED_02.md)
**Registry id:** `R-SKIP-2TO1-FAVORITE` in [`LEARNING_LANE_15M_RULES.json`](LEARNING_LANE_15M_RULES.json)

This note is the only place this ruling lives. It does not go in `manifest.json`, the digest, the hub, `records[]`, or any dated record. Selecting is **not** an edge, not a hit rate, not evidence of method quality, and not evidence toward lifting the Founder HOLD.

---

## Ruling (this is the decision)

1. **The test runs.** It is deterministic, adds no loop code (`_express_selection` already dispatches `params.favorite_odds`; `paper.py` already consults `decide()`), quarantines output here, and carries one live falsifier (n named by the bar in force, currently `looks.first_look_n = 70`; indistinguishable from `R-BASELINE-FILL-ALL` → park; do not retune `favorite_odds`). All four Protocol RUN-ONLY gates hold.
2. **No specific objection.** "Be careful" is not one. Burned-class and pre-registration checks are below. None fire.
3. **`execution=true` on this row only** (paper implementation). `R-SKIP-COINFLIP` stays `execution=false`. `binding` stays false. `trading_armed` stays false. The HOLD stands. This turn **does not score**.

---

## Four gates

| Gate | Holds? | Why |
|---|---|---|
| Deterministic | **Yes** | Skip when posted YES ≥ 2/3, else fill at the posted mark with `entry_edge=0.0`. No new collection. No wait-to-start. |
| No new loop code | **Yes** | Expression already in `rules._express_selection`. The paper path already calls `consult_registry` → `decide()`. This turn flips a registry flag. |
| Output quarantined | **Yes** | This note. Not the hub, digest, manifest, `records[]`, or a dated record. |
| Live falsifier | **Yes** | After the n the bar names (70), if selected-fill `settlement_pnl` cannot be distinguished from `R-BASELINE-FILL-ALL` on those same windows, park this rule. Do not retune `favorite_odds`. Do not replace 2/3 with a tape quantile. |

---

## Objections considered (none sustained)

| Candidate objection | Verdict | Why |
|---|---|---|
| FEE-AS-SIGNAL (burned) | **Does not fire** | Taker fee `k · stake · (1 − P)` is smallest where this rule **skips** (posted YES ≥ 2/3) and largest where it still **fills**. The rule does not read `k`. Opposite region from fee-avoidance. |
| RETUNE-COINFLIP-BAND (burned) | **Does not fire** | Different class, different parameter (`favorite_odds=2`), different skip region (high YES, not `(0.45, 0.55)`). `R-SKIP-COINFLIP` is not revived and its band is not touched. |
| THRESH / other oil burns | **Does not fire** | `class_is_burned("SKIP-2TO1-FAVORITE")` is false. This is not a rename of a burned oil class. |
| `favorite_odds=2` already an informing mark | **Does not fire** | First naming is the Lab declaration commit **`e9fab5a`** at `declared_at` `2026-09-08T16:53:00-04:00`. Tree search for `favorite_odds` / this 2-to-1 cutoff finds only that declaration and its follow-on docs. This turn did **not** open `paper/`, the RUN-ONLY fee table, the digest, or the manifest to choose or check the cut. |
| Golf idle / park row 8 "second PROPOSED not owed" | **Does not fire** | Golf idle is the WC latch, not a 15m invent freeze. Park row 9's trigger was *a later PROPOSED that actually selects*. CoS assigned that Lab job after `decide()` went live. This is that residual, not a new named horse. |
| Bar not binding / fee hash unpinned | **Not an objection to RUN-ONLY** | Those block ADMIT / bind / score. They do not block paper execution. "Cannot admit" is not "cannot compute." |

---

## Execution flip (paper only)

| | |
|---|---|
| Rule | `R-SKIP-2TO1-FAVORITE` |
| `declared_at` | `2026-09-08T16:53:00-04:00` |
| First-naming commit | `e9fab5a` |
| `execution` | **false → true** this turn |
| Flipped at | `2026-09-08T17:11:00-04:00` |
| Flip commit | the commit that lands this note |
| Timing | Before this rule's first L2-eligible window closes (L2 is eligible windows 71–140 after `declared_at`). No L2 window of this rule has closed. |
| Not flipped | `R-SKIP-COINFLIP` (`execution` stays false) |
| Not set | `binding`, `trading_armed`, `founder_read_once` |

`active_execution_rule()` will honour this row over the baseline. Two selecting rules with `execution=true` would raise; only this selecting row is live.

Replay of windows that closed after `declared_at` and before this flip is still replay, not lived. Lived paper skips/fills begin at the flip. This turn does not treat replay as lived and does not score either set.

---

## What this does not do

- **Not an edge.** Not established, not banked, not measured, not implied.
- **Not an admit.** `lab_admits=false`. Promotion still requires the normal ADMIT gate, a binding bar, and a Soften Critic attack from a separate session.
- **Not a score.** `score_rule` was not called. No scorecard was opened. No post-declaration outcome file was opened to write this.
- **Not a bind, not an arm.** `binding` stays false. `trading_armed` stays false. The HOLD stands.
- **Not a bar amend.** The bar still says "No selection rule declared after the flip exists" and `currently_reachable` stays **false**. That sentence is now stale as to existence of a post-`0a480d4` selecting row; updating it would re-owe Soften Critic. This fire does not edit the bar. Established remains unreachable until L2 is lived under a binding bar.
- **Not a revival of `R-SKIP-COINFLIP`.** Do not score that rule. Do not retune `(0.45, 0.55)`.
- **Not a lineage merge.** Lineage B's published `+1.67` is neither re-derived nor summed.
- **Not a second series.** `KXBTC15M` only. Golf idle stays **ON**.

---

## Park consequence

Park row 9 (zero-edge fills — the observation gap) **closes**: its trigger was *a later PROPOSED that actually selects*, and this is that PROPOSED, now RUN-ONLY with `execution=true`. Fills that still happen remain `entry_edge=0.0`; that honesty lives here, not as an open park. A third Lab PROPOSED is not owed (row 8 restated).

---

## Falsifier (live, not evaluated)

After the n named by the evidence bar in force (currently `looks.first_look_n = 70`), if selected-fill `settlement_pnl` cannot be distinguished from `R-BASELINE-FILL-ALL` on those same windows, **park this rule**. Do not retune `favorite_odds`. Do not replace `2/3` with a tape quantile. The bar is the governing source.

This turn does not evaluate the falsifier. n is not counted here.

Golf idle stays ON. HOLD stands. Trading is **NOT ARMED**.
