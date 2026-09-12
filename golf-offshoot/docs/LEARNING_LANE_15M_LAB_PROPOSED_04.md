# Lab — PROPOSED 04: skip the civil hour and half-hour walls

**State:** **PROPOSED.** **Not** Softened, **not** admitted, **not** a board, **not** a dashboard figure. `execution=false` this turn. Operator RUN-ONLY is the next seat. Lab never self-admits.
**Lane:** `learning_lane_15m` · series `KXBTC15M` only
**Role:** `lab` — `lab_admits=false`. Lab never admits its own candidate ([`.cursor/skills/gpf-lab/SKILL.md`](../../.cursor/skills/gpf-lab/SKILL.md)).
**Admit?** N · **Soften?** N · **Trading ARMED?** N · **Keys / orders / cash?** none
**Written:** 2026-09-12 07:45 EDT
**Registry id:** `R-SKIP-CIVIL-BOUNDARIES`
**Class:** `SKIP-CIVIL-BOUNDARIES`
**Catalog kind:** `CLOCK-CIVIL-BOUNDARIES`

**Gate this was written under.** Palshi M3SS / `F_continuation` after hour-close L1 PARK: one 15m PROPOSED under the invent contract (kill anatomy, unburned mechanism, pre-reg, live falsifier); handoff operator. Golf idle ON does not stop this Job. This is not golf WC3+ and is not golf idle-breach. Operator park of `R-SKIP-HOUR-CLOSE` is the precondition this catalog kind was waiting on. This turn does **not** set `execution=true`. Operator seats RUN-ONLY later.

**What this is not.** Not a revival of `R-SKIP-HOUR-CLOSE`. Not a retune of `skip_close_minute`. Not a copy of the parked rule with a new singleton clock (`RETUNE-CLOCK-MINUTE`). Not skip `:15` / `:30` / `:45` as `CLOCK-CLOSE-MINUTE`. Not a farm notebook. Not a revival of `R-SKIP-COINFLIP`. Not a retune of `favorite_odds`. Not a tape quantile of posted YES. Not PROPOSED 01 / FEE-AS-SIGNAL. Not PROPOSED 02 / `SKIP-2TO1-FAVORITE`. Not a skip-on-mark family. Not a golf board. It does not enter the Softened set, does not clear golf idle, does not touch golf θ / WC1 / WC2 / the Operator stamp / `phase1_dryrun/`, and does not expand past `KXBTC15M`. Golf idle stays **ON**.

---

## 1. Kill anatomy (last closed score/park)

Quoted from Operator L1 PARK of `R-SKIP-HOUR-CLOSE` ([`LEARNING_LANE_15M_OPERATOR_NOTE_SCORE_R-SKIP-HOUR-CLOSE_L1.md`](LEARNING_LANE_15M_OPERATOR_NOTE_SCORE_R-SKIP-HOUR-CLOSE_L1.md); scorecard [`LEARNING_LANE_15M_SCORECARD_R-SKIP-HOUR-CLOSE_L1.json`](LEARNING_LANE_15M_SCORECARD_R-SKIP-HOUR-CLOSE_L1.json)):

- `n=70`. `skip_count=1`. `skip_rate=0.014286`.
- Binding clauses **(1), (4), (5) FAIL**. `passes_every_binding_clause=false`.
- Clause (1): `mean_d=0.014857`, `t=-17.846154`, `p=1.0`, not `< α_k`.
- Clause (4): `mean_pnl_rule_fee_adj=-0.019143` (not `> 0`).
- Clause (5): observed mean does not exceed the matched-exposure quantile; `p_value=0.435756`.
- Operator: *indistinguishable from, and on (5) worse than, abstaining at the same rate with no skill.* Could not beat take-every-window.
- PARK instruction: do not retune `skip_close_minute`. Do not replace `0` with a tape-chosen slot.

That death is a **one-of-four civil-clock singleton**. Moving the same cut to another quartet minute is the burned class `RETUNE-CLOCK-MINUTE`. This PROPOSED does neither.

Header fields only were used for this quote (`n`, `skip_count`, clause results, PARK instruction). Window-level marks and close stamps in that scorecard were **not** used to choose a parameter.

---

## 2. Burned classes loaded

Loaded [`LEARNING_LANE_15M_BURNED_CLASSES.json`](LEARNING_LANE_15M_BURNED_CLASSES.json) and [`LEARNING_LANE_15M_MECHANISM_CATALOG.json`](LEARNING_LANE_15M_MECHANISM_CATALOG.json) before naming the class. `class_is_burned` is **false** for `SKIP-CIVIL-BOUNDARIES` and for `R-SKIP-CIVIL-BOUNDARIES`. It is **true** for `SKIP-HOUR-CLOSE`, `RETUNE-CLOCK-MINUTE`, `SKIP-2TO1-FAVORITE`, `RETUNE-COINFLIP-BAND`, `FEE-AS-SIGNAL`, and the other seeded oil / lane burns.

| Refused | Why |
|---|---|
| Revive `R-SKIP-HOUR-CLOSE` / retune `skip_close_minute` | Burned class `SKIP-HOUR-CLOSE` / `RETUNE-CLOCK-MINUTE` |
| Copy the parked rule with a new singleton clock (`:15` / `:30` / `:45`) | Same shape as moving `skip_close_minute`; remaining `CLOCK-CLOSE-MINUTE` slots are farm notebooks, not this live chair |
| Promote a farm keeper this fire | This Job is `F_continuation` invent, not `J_farm_promote` |
| Revive `R-SKIP-COINFLIP` | Already declared; L1 cannot Establish it |
| Retune `(0.45, 0.55)` | Burned class `RETUNE-COINFLIP-BAND` |
| Retune `favorite_odds` or replace `2/3` with a tape quantile | Burned class `SKIP-2TO1-FAVORITE` |
| Skip cheap YES because the fee is larger there | Burned class `FEE-AS-SIGNAL` |
| Any posted_yes cut, fitted or conventional | Skip-on-mark family |
| Oil `SEAS-DIR` / `MOY-DIR` | Month-of-year *direction* on Track B. This is a 15m *fill-or-skip* on named civil walls |
| Oil `SPREAD` or honer `H-SKIP-WIDE-SPREAD` | Spread cuts; half-spread profile n=624 is already an informing measurement on this tree |
| `HONER-FROZEN-CONSULT` / retype freeze θ | Not a Lab invent |
| `HONER-FAMILY-AMEND` / `HONER-FROZEN-REPLACE` | Honer exams still running; consult has not lived |

**Unburned mechanism.** Skip on the **two named civil-clock walls** (`:00` and `:30`), not on posted YES and not on a moved singleton minute. The 15-minute product is defined on quarter-hour walls. Hour and half-hour are the two civil boundaries on that quartet. Catalog `CLOCK-CIVIL-BOUNDARIES` names `expected_skip_rate=0.5` from that product structure. That kind was illegal while hour-close held the chair; Operator L1 PARK is the `legal_after` flip. Parameters are `{0, 30}`, not the two worst minutes on this book.

---

## 3. The one rule

**Skip the paper fill when the window's `close_at` clock minute is 0 or 30 (civil hour and half-hour). Otherwise fill at the posted mark with `entry_edge=0.0`.**

The free parameter is the integer pair **`skip_close_minutes = [0, 30]`**. It is a civil-clock pair, not a posted_yes cutoff. `decide()` already reads `params.skip_close_minutes` and compares `_as_dt(close_at).minute`. Posted YES is not an input to the expression. No new loop code.

No posted_yes, no paper book, no RUN-ONLY fee table, no digest, no manifest, and no scorecard window row informed `{0, 30}`. `{0, 30}` is the catalog's named civil walls. It is not a mark, not a quantile, and not a widening of `skip_close_minute=0` chosen from this tape.

Expression (paper only; **`execution=false` this turn** — Operator flips if it survives):

- `close_at.minute in {0, 30}` → **skip**
- `close_at.minute not in {0, 30}` → **fill** at the posted mark, `entry_edge=0.0`
- window `close_time` ≤ `declared_at` → **ineligible** (history, not OOS)
- missing `close_at` → **unknown** (cannot express a clock rule)

`R-SKIP-COINFLIP`, `R-SKIP-2TO1-FAVORITE`, and `R-SKIP-HOUR-CLOSE` id-dispatch and parameters are untouched. Hour-close `execution` is not flipped here.

---

## 4. Prediction and falsifier

**Prediction.** Selecting away from civil hour and half-hour closes changes the paper book relative to `R-BASELINE-FILL-ALL` by more than noise-plus-δ, under the bar in force, on the first look the bar names.

**Falsifier.** After the n named by the evidence bar in force (currently `looks.first_look_n = 70`), if selected-fill `settlement_pnl` cannot be distinguished from `R-BASELINE-FILL-ALL` on those same windows, **park this rule**. Do not retune `skip_close_minutes`. Do not replace `{0, 30}` with a tape-chosen pair. The bar is the governing source.

This turn **does not score**. n is not counted here. No post-declaration outcome file was opened to write this.

---

## 5. Pre-registration statement

The bar's pre-registration test needs (1) the commit SHA and timestamp of the registry row that first names the parameter, and (2) that this timestamp predates the earliest window whose **mark** informed the parameter.

**No window mark informed `skip_close_minutes=[0, 30]`.** The parameter is the catalog's named civil-clock pair, not a posted_yes cutoff, and it was not read from `paper/`, the RUN-ONLY fee table, the digest, the manifest, the half-spread profile, or scorecard window rows. I did not open those mark tables to choose it. The first naming is this declaration; the commit that lands `LEARNING_LANE_15M_RULES.json` with this id is the SHA the bar asked for.

`expected_skip_rate` is `2/4 = 0.5` from the 15m quartet `{0, 15, 30, 45}`. That is above `10 / looks.first_look_n` (~14% at n=70) and at the catalog preference of ≥ 25%.

This is the statement the bar requires. It is not itself the proof — the commit record is.

`R-SKIP-COINFLIP` remains not verifiably pre-registered. `favorite_odds=2` remains not verifiably pre-registered. This row does not repair either.

`declare_rule` still refuses a *posted-yes* selecting rule on a tree that already has KXBTC15M paper marks. A `close_minute_in` row is a new class, not another skip-band, and not a moved `skip_close_minute`.

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
| Loop code | **None.** Expression already in `rules._express_selection` for `params.skip_close_minutes`. `paper.py` already consults `decide()`. This turn does not flip `execution` |
| Score | **Forbidden this turn** |
| Output quarantine | Operator note after RUN-ONLY. Never hub, digest, `manifest.json`, `records[]`, or a dated record |

---

## 8. Hard NOs honored

- Burned classes loaded; `R-SKIP-HOUR-CLOSE` not revived; `skip_close_minute` not retuned; singleton clock not copied; `R-SKIP-COINFLIP` not revived; `(0.45, 0.55)` not retuned; `favorite_odds` not retuned
- No Soften, no Harden, no Kill, no ADMIT, no self-admit
- No score, no scorecard, no post-declaration outcome file opened for results
- `execution` left false; `binding` not touched; `trading_armed` not touched; HOLD not lifted
- No golf θ, no WC3+, no second series, no second hub, no placeholder fee hash
- No Founder impersonation of arm or HOLD. Do not add `founder_read_once` as a bind condition
- Operator park child's desk / leave-off / park / burned-class writes were not overwritten

---

## 9. Handoff

→ **`operator`.** Operator sustains or overrules, and may set `execution=true` on this pre-registered row if it survives (only one selecting seat; a falsifier PARK drops the dead row's execution). Lab does not.
