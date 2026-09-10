# Lab — PROPOSED 03: skip the hour-ending 15m close

**State:** **PROPOSED.** **Not** Softened, **not** admitted, **not** RUN-ONLY, **not** a board, **not** a dashboard figure. `execution=false` (Operator may flip). Not scored.
**Lane:** `learning_lane_15m` · series `KXBTC15M` only
**Role:** `lab` — `lab_admits=false`. Lab never admits its own candidate ([`.cursor/skills/gpf-lab/SKILL.md`](../../.cursor/skills/gpf-lab/SKILL.md)).
**Admit?** N · **Soften?** N · **Trading ARMED?** N · **Keys / orders / cash?** none
**Written:** 2026-09-10 13:25 EDT
**Registry id:** `R-SKIP-HOUR-CLOSE`
**Class:** `SKIP-HOUR-CLOSE`

**Gate this was written under.** Desk Job 2026-09-10 13:05 ET: one 15m PROPOSED under the invent contract (kill anatomy, unburned mechanism, pre-reg, live falsifier); handoff operator. `F_continuation`. Golf idle ON does not stop this Job. This is not golf WC3+ and is not golf idle-breach.

**What this is not.** Not a revival of `R-SKIP-COINFLIP`. Not a retune of `(0.45, 0.55)`. Not a retune of `favorite_odds`. Not a tape quantile of posted YES. Not PROPOSED 01 / FEE-AS-SIGNAL. Not PROPOSED 02 / `SKIP-2TO1-FAVORITE`. Not a skip-on-mark family. Not a golf board. It does not enter the Softened set, does not clear golf idle, does not touch golf θ / WC1 / WC2 / the Operator stamp / `phase1_dryrun/`, and does not expand past `KXBTC15M`. Golf idle stays **ON**.

---

## 1. Kill anatomy (last closed score/park)

Quoted from Operator L1 PARK of `R-SKIP-2TO1-FAVORITE` ([`LEARNING_LANE_15M_OPERATOR_NOTE_SCORE_R-SKIP-2TO1-FAVORITE_L1.md`](LEARNING_LANE_15M_OPERATOR_NOTE_SCORE_R-SKIP-2TO1-FAVORITE_L1.md); scorecard [`LEARNING_LANE_15M_SCORECARD_R-SKIP-2TO1-FAVORITE_L1.json`](LEARNING_LANE_15M_SCORECARD_R-SKIP-2TO1-FAVORITE_L1.json)):

- `n=70`. `skip_count=1`. `skip_rate=0.014286`.
- Binding clauses **(1), (4), (5) FAIL**. `passes_every_binding_clause=false`.
- Clause (1): `mean_d=-0.004857`, `p=1.0`, not `< α_k`.
- Clause (4): `mean_pnl_rule_fee_adj=-0.078714` (not `> 0`).
- Clause (5): observed mean does not exceed the matched-exposure quantile; `p_value=0.548845`.
- The one skip was a winning favorite on the recorded book. Skipping it produced `d_i < 0` on that window and zeros on the other 69. Operator: *indistinguishable from, and on (1) and (5) worse than, abstaining at the same rate with no skill.*
- PARK instruction: do not retune `favorite_odds`. Do not replace `2/3` with a tape quantile.

That death is a **rare posted-YES cut**. Moving the same cut, or replacing it with a tape quantile, is the burned class `SKIP-2TO1-FAVORITE` / `RETUNE-FAVORITE-ODDS`. This PROPOSED does neither.

Header fields only were used for this quote (`n`, `skip_count`, clause results, PARK instruction). Window-level marks and close stamps in that scorecard were **not** used to choose a parameter.

---

## 2. Burned classes loaded

Loaded [`LEARNING_LANE_15M_BURNED_CLASSES.json`](LEARNING_LANE_15M_BURNED_CLASSES.json) before naming the class. `class_is_burned` is **false** for `SKIP-HOUR-CLOSE` and for `R-SKIP-HOUR-CLOSE`. It is **true** for `SKIP-2TO1-FAVORITE`, `RETUNE-COINFLIP-BAND`, `FEE-AS-SIGNAL`, `SEAS-DIR`, `SPREAD`, `THRESH`, `PERSIST`, and the other seeded oil / lane burns.

| Refused | Why |
|---|---|
| Revive `R-SKIP-COINFLIP` | Already declared; L1 cannot Establish it |
| Retune `(0.45, 0.55)` | Burned class `RETUNE-COINFLIP-BAND` |
| Retune `favorite_odds` or replace `2/3` with a tape quantile | Burned class `SKIP-2TO1-FAVORITE` |
| Skip cheap YES because the fee is larger there | Burned class `FEE-AS-SIGNAL` |
| Any posted_yes cut, fitted or conventional | Skip-on-mark family; the last closed test died as a rare mark skip |
| Oil `SEAS-DIR` / `MOY-DIR` | Month-of-year *direction* on Track B. This is a 15m *fill-or-skip* on a civil-clock minute, not a direction class |
| Oil `SPREAD` or honer `H-SKIP-WIDE-SPREAD` | Spread cuts; half-spread profile n=624 is already an informing measurement on this tree |

**Unburned mechanism.** Skip on the **civil-clock close minute**, not on posted YES. The 15-minute product is defined on quarter-hour walls. The hour (`minute == 0`) is the only named civil-clock boundary that is not a 15-minute fraction. That is series structure, not a mark.

---

## 3. The one rule

**Skip the paper fill when the window's `close_at` clock minute equals 0 (the hour-ending slot). Otherwise fill at the posted mark with `entry_edge=0.0`.**

The free parameter is the integer prior **`skip_close_minute = 0`**. It is a clock minute, not a posted_yes cutoff. `decide()` reads it from `params.skip_close_minute` and compares `_as_dt(close_at).minute`. Posted YES is not an input to the expression.

No posted_yes, no paper book, no RUN-ONLY fee table, no digest, no manifest, and no scorecard window row informed `0`. `0` is the hour. It is not a mark, not a quantile, and not a widening of `(0.45, 0.55)` or `2/3`.

Expression (paper only; **`execution=false` this turn** — Operator flips if it survives):

- `close_at.minute == 0` → **skip**
- `close_at.minute != 0` → **fill** at the posted mark, `entry_edge=0.0`
- window `close_time` ≤ `declared_at` → **ineligible** (history, not OOS)
- missing `close_at` → **unknown** (cannot express a clock rule)

`R-SKIP-COINFLIP` and `R-SKIP-2TO1-FAVORITE` id-dispatch and parameters are untouched. Favorite `execution` is not flipped here.

---

## 4. Prediction and falsifier

**Prediction.** Selecting away from hour-ending closes changes the paper book relative to `R-BASELINE-FILL-ALL` by more than noise-plus-δ, under the bar in force, on the first look the bar names.

**Falsifier.** After the n named by the evidence bar in force (currently `looks.first_look_n = 70`), if selected-fill `settlement_pnl` cannot be distinguished from `R-BASELINE-FILL-ALL` on those same windows, **park this rule**. Do not retune `skip_close_minute`. Do not replace `0` with a tape-chosen slot. The bar is the governing source.

This turn **does not score**. n is not counted here. No post-declaration outcome file was opened to write this.

---

## 5. Pre-registration statement

The bar's pre-registration test needs (1) the commit SHA and timestamp of the registry row that first names the parameter, and (2) that this timestamp predates the earliest window whose **mark** informed the parameter.

**No window mark informed `skip_close_minute=0`.** The parameter is a civil-clock minute, not a posted_yes cutoff, and it was not read from `paper/`, the RUN-ONLY fee table, the digest, the manifest, the half-spread profile, or scorecard window rows. I did not open those mark tables to choose it. The first naming is this declaration; the commit that lands `LEARNING_LANE_15M_RULES.json` with this id is the SHA the bar asked for.

This is the statement the bar requires. It is not itself the proof — the commit record is.

`R-SKIP-COINFLIP` remains not verifiably pre-registered. `favorite_odds=2` remains not verifiably pre-registered. This row does not repair either.

`declare_rule` still refuses a *posted-yes* selecting rule on a tree that already has KXBTC15M paper marks. A `close_minute_eq` row is a new class, not another skip-band, and the gate now says so.

---

## 6. What this does not claim

- **Not an edge.** Not established, not banked, not measured, not implied.
- **Not an admit.** `lab_admits=false`. Operator decides RUN-ONLY / PARK / (later) ADMIT.
- **Not lived.** `execution=false`. Replay of later windows is still replay. Lived paper begins if and when Operator flips.
- **Not a score.** `score_rule` is not called. No scorecard is opened.
- **Not a bind, not an arm.** `binding` is not touched. `trading_armed` stays false. The HOLD stands.
- **Not a lineage merge.** Lineage A only, if and when anyone scores. Lineage B's published `+1.67` is neither re-derived nor summed.
- **Not a second series.** `KXBTC15M` only.

---

## 7. Cost

| Need | Status |
|---|---|
| New data collection | **None** |
| New series | **None** |
| Kalshi keys / orders / cash | **None.** Trading NOT ARMED |
| Loop code | Expression only, in `rules._express_selection`, dispatched from declared `params.skip_close_minute`. `paper.py` already consults `decide()`. This turn does not flip `execution` |
| Score | **Forbidden this turn** |

---

## 8. Hard NOs honored

- Burned classes loaded; `R-SKIP-COINFLIP` not revived; `(0.45, 0.55)` not retuned; `favorite_odds` not retuned
- No Soften, no Harden, no Kill, no ADMIT, no self-admit
- No score, no scorecard, no post-declaration outcome file opened for results
- `execution` left false; `binding` not touched; `trading_armed` not touched; HOLD not lifted
- No golf θ, no WC3+, no second series, no second hub, no placeholder fee hash
- No Founder impersonation of arm or HOLD. Do not add `founder_read_once` as a bind condition

---

## 9. Handoff

→ **`operator`.** Operator sustains or overrules, and may set `execution=true` on this pre-registered row if it survives (only one selecting seat; a falsifier PARK drops the dead row's execution). Lab does not.
