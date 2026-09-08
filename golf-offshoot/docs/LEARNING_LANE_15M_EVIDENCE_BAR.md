# 15m evidence bar (DRAFT — not binding)

**Lane:** `learning_lane_15m` · series `KXBTC15M` only
**Drafted:** 2026-09-08 08:30 EDT · Operator
**Amended:** 2026-09-08 · Operator, admit pass on Soften Critic CRITIC 01
**Binding?** **N.** A system that sets its own threshold does not have one.
**Admit?** N · **Edge established?** N · `lab_admits` false · Trading **NOT ARMED**

This draft becomes binding only after all three:

1. the Soften Critic attacks it in writing, in a session that did not draft it, and Operator **sustains or explicitly overrules every objection, each with a stated reason**, in a turn separate from the objections. "Answered" is not "noted." The attack and the answers are both linked from this file so a read-once covers both.
2. `critic-invariants` passes on the bytes proposed to bind, **or** every failing check is named on this bar's face with Operator's reason for binding anyway. A findings artifact that says `passed: false` cannot sit under a bar that says `binding: true`.
3. Founder reads it once and acknowledges.

Condition 1 is met by [`LEARNING_LANE_15M_EVIDENCE_BAR_OPERATOR_ANSWER_01.md`](LEARNING_LANE_15M_EVIDENCE_BAR_OPERATOR_ANSWER_01.md), answering [`LEARNING_LANE_15M_EVIDENCE_BAR_CRITIC_01.md`](LEARNING_LANE_15M_EVIDENCE_BAR_CRITIC_01.md). **Conditions 2 and 3 are not met.** This is still a proposed bar. Writing it is not an ADMIT. Amending it is not an ADMIT. Scoring against it is not owed. `records[]` stays empty.

Amending this bar re-owes the Critic on the new text (`critic.py` keys findings by content hash). That is correct and intended: CRITIC 02 attacks *this* version.

Machine copy: [`LEARNING_LANE_15M_EVIDENCE_BAR.json`](LEARNING_LANE_15M_EVIDENCE_BAR.json).
Burned classes: [`LEARNING_LANE_15M_BURNED_CLASSES.json`](LEARNING_LANE_15M_BURNED_CLASSES.json).
Fee source: [`LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md`](LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md) (RUN-ONLY note only — those numbers do not go on the hub, in the digest, in `manifest.json`, or in `records[]`).

---

## What the mechanical Critic says about this bar

Disclosed on the face because a bar that fails its own lane's checks and does not say so reads as complete. Run `critic-invariants` against the exact bytes of this file before treating any of this as current.

At the last read, on the pre-amendment text, four method checks failed: `matched_exposure_control`, `delta_above_detection_floor`, `holdout_is_forward_only`, `fee_schedule_hash_recorded`. This amendment addresses the first three in substance. **`fee_schedule_hash_recorded` still fails and is a standing blocker on binding condition 2**: `k = 0.07` is used with no pinned sha256 for `https://kalshi.com/docs/kalshi-fee-schedule.pdf`, so a schedule change would be invisible. Pinning that hash is owed before this bar can bind.

Two of those checks are keyword-satisfiable and must not be read as clearance on their own:

- `holdout_is_forward_only` passes the moment `forward_only` appears in the JSON. The key is set below **because** the substantive control was added (commit-ordering, §No peeking), not instead of it.
- `matched_exposure_control` passes on the presence of a `matched_exposure` key. It is set because clause (5) exists, not to silence the check.

`honesty_stamp_is_fresh` is a property of `DESK.md`, not of this bar, and is not this file's to clear.

**A recorded hash in the findings artifact is not the byte hash of this file.** `critic.py` reads with `read_text()` and re-encodes, so on a CRLF checkout it records the newline-normalised digest. Binding condition 2 means the *normalised* bytes the checker actually read. Whoever verifies it must check which digest they are comparing.

---

## Two verdicts, not one

The method already says a gate pass is not a claim: Amb ≠ clearance, print-match ≠ clearance, no soft clearances, establishment-stop drill (`workflow.md`, `templates/02_Gate_Scoring_Sheet.md`). This lane inherits that split.

| Verdict | What it answers | What it licenses | What it does not |
|---|---|---|---|
| **Admissible** | Is this rule well-posed and honestly testable under the gate sheet and this bar? | A dated-record ADMIT that the *test completed* and the rule may stay live as a candidate. Operator note / park row. | Edge. `records[]` as a track record. Skill-met. Productize. Arming. Lifting the HOLD. |
| **Established** | Did the rule clear the locked numerical bar as *edge*, after confirmation? | A method establishment verdict on this lane only, and only after the track has been promoted into the gated method. | Money, keys, series expansion, golf θ, usefulness Soften. **Edge Softened/established?** on an ops-beside stamp stays **N** until promotion has fired. |

An ops ADMIT on this lane, while the lane is still ops-beside-method, is a dated record. Per [`docs/operator_ops/OPS_BESIDE_METHOD.md`](../../docs/operator_ops/OPS_BESIDE_METHOD.md): it does **not** establish edge. **Edge Softened/established?** stays **N**. Observation ≠ edge.

Promotion into the gated method is a separate Founder-named conditional. This bar does not fire it. This bar being written does not fire it. This bar is not binding yet, so the promotion condition that requires a binding bar cannot hold yet.

---

## No peeking

Score a selection rule at **n = 70** eligible settled windows, not every tick. Continuous scoring against a threshold manufactures significance.

n was 40 in the drafted version. It is 70 because at n = 40 the effect floor δ sat at 0.997 × the minimum detectable effect — the floor *was* the critical value, relabeled. See §Effect floor.

- First look: the first 70 eligible windows after `declared_at` (`close` strictly after declaration). Call this set **L1**.
- Do not compute the test at n = 1, 10, 40, or 69. Do not peek and then wait for a prettier n.
- **L2** (eligible windows 71–140 after `declared_at`) is held out. L2 is strictly forward of L1, which is strictly forward of declaration; `rules.py` `window_is_oos` enforces `closed > declared`, strict.
- **The holdout is not an honour-system reading restriction.** The L1 score note must be **committed before the 71st eligible window closes**, and must record that commit SHA and its timestamp. A note that cannot show it predates the first L2 window is not an L1 score; it is a look at both sets. This is the only form of the rule that is not self-certification, and it belongs in `invariants.py` as a check (owed to Systems).
- L1 and L2 together must span at least **3 distinct UTC days**. At ~96 windows/day, 140 windows is ~35 hours; without this the whole test lives inside one contiguous stretch of one regime.
- Even with that span: an **Established** verdict on this lane is scoped to the regimes actually observed and does not generalise past them. Say so in the verdict.
- A later confirmation look on L2 is a second precommitted look, not a retry of L1. Its test is specified in §The L2 confirmation test, before L1 is scored.
- `072245` does not exist. Do not invent it. Do not put it in any denominator.

`R-SKIP-COINFLIP` was declared at `2026-09-08T05:56:00-04:00`. It is **not scored in the session that wrote this bar, nor in the session that amended it.** Eligible-window *counts* may be reported. Outcomes of windows that closed after declaration must not be read to choose or illustrate this bar.

---

## What "distinguishable" means

Contrast, on the **same** n eligible windows:

`d_i = pnl_rule_fee_adj_i − pnl_baseline_fee_adj_i`

- Baseline is `R-BASELINE-FILL-ALL` on window i (the recorded fill, then fee-adjusted).
- The rule side uses that rule's fill-or-skip. A skip contributes **0** pnl and **0** fee.
- On a window both sides fill, `d_i = 0` after the same fee. The contrast lives in the skips (or in any later rule that fills a different contract).
- Lineage A only. Do not sum, net, or average lineage B's published `+1.67` into this arithmetic.
- Recorded `settlement_pnl` on disk has **no fee term**. Fee-adjust before comparing. The fee-adjusted figures live in the score note only.

**The arms are not exposure-matched and the contrast is not normalised for that.** The rule arm risks `(1 − skip_rate) × n × $1`; the baseline risks `n × $1`. Clause (5) is the control that makes the comparison answer *"did this rule beat abstaining at the same rate?"* rather than *"did abstaining help?"*. Report `mean(d)` per dollar at risk beside `mean(d)` per window so a reader can see both.

**Test at n = 70 (L1), one look. All five clauses bind.**

1. **Null.** One-sided paired t-test, **H0: mean(d) ≤ δ**. Reject only if p < α_k.
   The drafted null was `mean(d) ≤ 0`. That null is **known false before any data are collected**: the book fills at the posted mark and pays `1/mark`, so a fill is EV-zero *pre-fee* at a calibrated mark, and the fee is strictly positive on every fill (minimum ceil-cent fee $0.01). Therefore `E[d] > 0` for any nonzero skip rate with no selection skill present. Testing against zero is testing arithmetic. The floor is now the null, so clause (3) is absorbed here rather than checked separately.
2. **Multiplicity.** `α_k = 0.05 / (k · (k+1))`, where `k = trials_to_date + 1`, using the registry counter *before* incrementing. Then increment.
   The drafted scheme was `0.05 / k`. Its weights are the harmonic series, which diverges, so it controls nothing: over the bar's own 14-look week `1 − Π(1 − 0.05/k) = 15.2%`, not 5%. The replacement sums to 0.05 over an unbounded number of looks (`Σ 0.05/(k(k+1)) = 0.05`), giving FWER ≤ 0.05 forever. First look: `α_1 = 0.025`, z = 1.960. Fourteenth: `α_14 = 0.000238`, z = 3.494. FWER over 14 looks under the new scheme is 4.6%.
   The increment must be **mechanical**. Nothing on the tree currently reads or writes `trials_to_date` — it is prose, and `:Burned classes` already says prose is not enforceable. An invariant that fails when a score note exists without a matching increment is owed to Systems.
3. **Effect floor:** `δ = $0.28` per window, **= 0.28 × stake**. Absorbed into clause (1) as the null. See §Effect floor for what δ is and is not.
4. **Positive side.** `mean(pnl_rule_fee_adj) > 0` on those same n windows. Promoted from conditional prose to a binding numbered clause. Beating a losing baseline by skipping, and still booking ~0 after fees, is distinguishable-or-not; it is not a positive result that cleared the cost. Skip-all yields 0 and fails this clause.
5. **Matched-exposure permutation control.** `mean(d)` must exceed the `1 − α_k` quantile of a permutation null that **holds the number of skips fixed and reassigns which windows are skipped**: ≥ 10,000 draws, seed **`20260908`**, pre-registered here. This null is centred on abstaining at the observed rate with no skill, which is the correct comparison; clause (1) alone would still credit mechanical fee avoidance. Deterministic given the seed, no new data, no loop code.

**Also print, beside `mean(d)`:** `skip_rate × mean(fee | skip)` — the mechanical fee-avoidance component of the contrast — so a reader can see how much of the result is arithmetic rather than selection.

**Kill / park** (the numeric form of `R-SKIP-COINFLIP`'s existing falsifier): if at n = 70 the rule fails any of (1)–(5), **park it and do not retune the band.** A dead test is a complete outcome. Record the park on that falsifier.

### Effect floor

**δ = $0.28 per window is provisional and is not yet derived from decision relevance.** Stated plainly because the drafted bar presented a coincidence as a rationale: δ was `2.69 × SE₄₀`, the critical value at family α = 0.05 over 14 looks, and δ/MDE was **0.997**. The floor was the rejection threshold wearing an effect floor's clothes, and it therefore carried no information about whether an effect of that size is worth acting on.

What has changed: δ is no longer derived from the critical value, and n has moved so the two numbers are not the same number.

| | Drafted (n = 40) | Amended (n = 70) |
|---|---|---|
| sd used | 0.66 (point estimate) | **0.784** — 95% upper confidence bound on 0.66 from 56 calibration windows. δ is linear in sd and 0.66 is one number from one 14-hour stretch |
| SE | 0.1044 | 0.0937 |
| α on the first look | 0.05 | 0.025 |
| MDE | 0.2807 | 0.1837 |
| **δ / MDE** | **0.997** | **1.52** |
| Reject if mean(d) > | 0.28 (H0 ≤ 0) | **0.464** (H0 ≤ δ) |

**Power, on the bar's face.** Under the amended null, power *at* δ is α by construction — that is what testing against a floor means. So the honest statement is the curve, not a single number:

- 50% power against a true effect of **$0.464/window** (46% of a $1 stake, every window).
- 80% power against a true effect of **$0.543/window** (54% of stake).
- Under the *drafted* design (H0 ≤ 0, n = 40) the bar had **~50% power at δ** and reached 80% power only at $0.37/window. A bar that misses half the effects it declares material is a coin.

**Read this honestly: with per-window sd near 0.66–0.78 and an n reachable in under two days, this lane can only detect very large effects.** That is a property of the tape and the $1 unit, not a defect the bar can amend away. It is disclosed rather than hidden.

**Owed before binding:** δ re-derived from what size of edge is worth acting on. The crew has no decision-relevance anchor today — the lane is paper-only, HOLD stands, no capital is at risk — so δ is carried at $0.28 provisionally with the coincidence labelled. A later Operator turn or Founder must name a decision-relevant δ. Until then this bar cannot bind on δ alone.

---

## The omitted costs

Recorded pnl omits **two** costs, not one: the entry fee **and** the bid/ask spread.

**Fee adjustment** (from the RUN-ONLY note, k = 0.07, $1 stake, ceil to the cent):

`fee_i = ceil_cent(0.07 × stake_i × (1 − posted_yes_i))`

`pnl_fee_adj_i = recorded_pnl_i − fee_i` on a fill; `0` on a skip.

Measured cost cited from that note, not restated here as a dashboard figure: mean **$0.039** per fill, **3.92%** of stake, on the first 24 lineage-A books. A later public schedule that names a different `k` or a `KXBTC15M` override makes this stale. **No sha256 is pinned for that schedule** — see §What the mechanical Critic says.

**The fee is strictly decreasing in the mark.** With stake fixed at $1, contracts `C = stake/P`, and Kalshi's `0.07 × C × P × (1−P)` reduces exactly to `0.07 × stake × (1 − P)`. So: $0.0455 at P = 0.35, $0.035 at P = 0.50, $0.014 at P = 0.80. The RUN-ONLY note's own table confirms it — every $0.05 ceil-cent fee sits at a mark between 0.3350 and 0.4250, every mark inside (0.45, 0.55) pays $0.04, and the 0.9835 mark pays $0.01.

**Consequence for band rules, stated because it inverts an easy assumption:** a rule that skips the middle of the mark distribution does **not** avoid the fee-heavy region. It skips the middle of the fee distribution and keeps the most fee-expensive fills. "Avoids the fee" is not available as a thesis for a coinflip-band skip on this book. Any rule proposing to avoid cost by skipping must state which cost, and in which direction it runs.

**The spread is omitted entirely and is not adjusted for.** `paper_mark` is `public_mid_or_last(...)` — the **mid** whenever both sides are quoted — and the payout is `1/mark`. The book buys at the mid and is paid at the mid, while the RUN-ONLY note charges a **taker** fee on that fill. A taker pays the ask, not the mid. The omitted half-spread costs `s / (p + s)` per $1 of stake: on a one-cent book that is about **$0.010 per fill** at p = 0.50 and about **$0.020** on a two-cent book — the same order as the $0.039 mean fee.

**Direction of the spread cost.** At a constant tick, `s/(p+s)` is *decreasing* in p — $0.0164 at p = 0.30, $0.0110 at 0.45, $0.0099 at 0.50, $0.0055 at 0.90. It runs the **same** direction as the fee, not the opposite. Both omitted costs are worst on cheap marks. A band skip avoids neither's worst region.

**Therefore: the fee-adjusted figure remains optimistic by an unmeasured amount of the same order as the fee.** No fee-adjusted number produced under this bar may be presented as a full cost accounting. A bar that closes one omitted cost and stays silent about a comparable one is more dangerous than a bar that closes neither, because it reads as complete.

**The adjustment must be code, not a hand table.** `evidence_bar.py` implements no arithmetic — it is two loaders, a binding flag and two burned-class lookups. A binding numeric floor may not depend on a step with no code, no artifact and no check. A committed, tested `fee_adjust(recorded_pnl, posted_yes, stake)` that the score note cites is owed to Systems before this bar binds.

---

## Pre-registration of rule parameters

A selection rule's parameters are the free parameters that actually pick windows. A `note` field asserting they were chosen blind is **self-certification and is not accepted as proof**.

To count as pre-registered, a rule's parameters need:

1. the **commit SHA and timestamp** of the registry entry that first names them, and
2. a statement that this timestamp **predates the earliest window whose mark informed the parameter** — including marks published anywhere on this tree, not only marks the author remembers reading.

**`R-SKIP-COINFLIP`'s (0.45, 0.55) band does not meet this, and this bar records that on its face.**

| Commit | Time (EDT) | What landed |
|---|---|---|
| `2fea8d8` | 2026-09-07 21:49:37 | the RUN-ONLY fee note, including a table of mark and recorded pnl for 24 lineage-A windows |
| `0786279` | 2026-09-08 05:56:51 | the rule registry — first appearance of (0.45, 0.55), 51 seconds after its own `declared_at` |

**8 hours 7 minutes 14 seconds** separate them, verified from the commit record. Eight of those 24 published rows fall strictly inside the band. The band was written down by a crew that had already published, on this tree, the exact marks it selects on and what each of them paid. Intent may well have been blind; the *information* was not, and the bar does not adjudicate intent.

**Consequence:** `R-SKIP-COINFLIP`'s band is **not verifiably pre-registered**. Its L1 therefore **cannot support an Established verdict even if it passes every clause.** L1 may still be scored, and may still support an Admissible dated record. This is a statement about the provenance of a parameter, not a score of the rule, and no window outcome after declaration was read to write it.

This condition dies for this rule if a commit, desk line, or dated artifact predating 2026-09-07 21:49:37 EDT names the (0.45, 0.55) band. None was found in the history.

---

## The L2 confirmation test

Specified here, before L1 is scored, so the confirmation threshold cannot be set once L1 is known. A confirmation look with an unspecified threshold is not pre-committed.

| | L2 |
|---|---|
| n | 70 (eligible windows 71–140 after `declared_at`) |
| H0 | `mean(d) ≤ δ`, same form as L1 |
| δ | the same δ in force when L1 was scored. It does not move between looks |
| α | `α_k` from the same schedule, using the counter value **after** L1's increment |
| Clauses | (1), (3), (4), (5) all bind, same as L1 |
| Counter | **L2 increments `trials_to_date` too.** A confirmation look is a look. Not counting it makes confirmation free |
| Execution | must be **lived** — see §Replay versus lived |

---

## Replay versus lived

The registry already says these are different evidence. This bar says which verdict accepts which.

| Evidence | Admissible | Established |
|---|---|---|
| **Replay** (`execution=false`; books collected without the rule acting) | Yes — L1 may be scored by replay. Declaration time makes the data clean. | **No.** A replayed survivor is not a lived one. |
| **Lived** (`execution=true`; the loop honoured `rules.decide()`) | Yes — also acceptable for L1 if the rule was live for those windows. | **Required** for L2 confirmation and for any establishment verdict. |

Replay assumes fills live execution might not get. Skipping a bet changes nothing about the market and does change the fill sequence. Both are legitimate. They are not interchangeable.

**Established is currently unreachable, and this bar says so rather than implying otherwise.** Nothing in the running loop calls `rules.decide()` — the only callers on the tree are the test suite. `paper.py` fills every candidate window and never consults the registry. So the lane cannot produce a lived L2 today.

**Explicit precondition of Established:** `paper.py` honours `rules.decide()`. That is a Systems change, and until it lands no rule on this lane can be Established by any route.

**The permitted flip point.** `execution=false → true` is legitimate **only before the first L2-eligible window closes**, and only recorded with a commit SHA and timestamp. Flipping it after any L2 window has closed, or flipping it to make a replayed look read as lived, is the prohibited move. The drafted ban read as absolute and forbade the only action that produces a lived confirmation; it is a timing rule.

---

## Trials accounting

`trials_to_date` lives on [`LEARNING_LANE_15M_RULES.json`](LEARNING_LANE_15M_RULES.json). It starts at **0**.

**It increments on the *declaration* of a selection rule on this lane, not on the score.** The drafted rule incremented "once per first-look (L1) score," which defines the multiplicity family by what got written up rather than by what got tried. A rule proposed, replayed informally and dropped before anyone wrote a score never touched the counter. That is the wrong denominator and it always flatters. Baseline naming is not a trial. L2 confirmation looks also increment (see §The L2 confirmation test).

The counter is currently prose: no code reads or writes it. Making it mechanical, plus an invariant that fails when a score note exists without a matching increment, is owed to Systems and is a precondition of clause (2) meaning anything.

The held-out L2 range is the other half of the protection: the scorer of L1 never sees it, and must prove that by commit order. Establishment cannot be claimed from L1 alone even if L1 passes.

---

## Burned classes

Prose in `logs/failure_mode_log.md` is not enforceable. Lab and any later proposer **must** load [`LEARNING_LANE_15M_BURNED_CLASSES.json`](LEARNING_LANE_15M_BURNED_CLASSES.json) before naming a class.

Oil Track B direction classes are seeded there so they cannot be re-proposed under new 15m names. **`H-SPOT-MOY-CONT` is FRAGILE, not a null.** Do not burn it to empty a queue. Do not promote it.

Lane-local burned classes start as: fee-as-signal, retune-coinflip-band-after-tape, sum-lineages, backfill-gap, baseline-as-edge.

A class lands on this list when it is parked on a falsifier or rejected as a burned revival. Aliases are first-class. Re-naming MAG as "magnitude-gate" is still MAG.

---

## What an ADMIT on this lane does and does not authorize

While the lane is ops-beside-method:

- An ADMIT is a **dated record** of a frozen exit (PASS / FAIL / park / residual) under the named bar for that date.
- **Edge Softened/established?** stays **N**. Write N even if a paper-hit count exists.
- It does not arm trading, lift the series HOLD, clear golf idle, rewrite the golf Operator stamp, or put a fee-accurate figure on the hub.

After promotion fires (conditional, not this draft): establishment is adjudicated under the standing gated-method rules against *this* bar once binding. Operator issues that verdict without asking Founder. Promotion is not itself a verdict.

---

## δ is a fraction of stake, not a dollar figure

δ = $0.28 per window is meaningful only because `PAPER_UNIT = 1.0` and `stake_usd = 1.0`. Read δ as **0.28 × stake**. If the unit ever changes, a dollar-denominated δ silently becomes a different effect size and nothing complains. An invariant that fails when `PAPER_UNIT ≠ 1.0` while this bar is binding is owed to Systems.

---

## Pre-declaration windows used to choose δ

**Used:** the 56 settled lineage-A paper books whose close is **at or before** `2026-09-08T05:56:00-04:00`: `KXBTC15M-26SEP071545-45` through `KXBTC15M-26SEP080545-45`, excluding the missing `KXBTC15M-26SEP072245`.

**Read from those books:** `movements[0].model_win` (posted YES) and recorded `settlement_pnl`, then the note's ceil-cent fee. Used only to estimate sd of the paired difference under a skip-inside-(0.45, 0.55) expression, so SE could be named before any OOS look.

**Not used:** any window that closed after `2026-09-08T05:56:00-04:00`. Those files were not opened for marks or pnl while drafting or amending this bar.

**Not a score:** the in-sample mean contrast on those 56 books was inspected only to confirm δ was **not** fit so that history would pass. That mean is not a method result and is not printed here as one. Pre-declaration skip rate on that expression was 22/56. That rate is history, not OOS.

**sd is one number from one stretch.** The point estimate 0.66 comes from 56 windows inside a single ~14-hour period. The bar now uses its 95% upper confidence bound, **0.784**, wherever δ is compared to a detection floor. Recompute both when more tape exists.

---

## Hard NOs (this bar)

- Do not treat this draft as binding
- Do not set `binding: true` while `critic-invariants` reports `passed: false` on these bytes
- Do not score `R-SKIP-COINFLIP` before 70 eligible windows, and not in the drafting or amending session
- Do not peek L2 while scoring L1, and do not claim you did not without the commit order to show it
- Do not treat a `note` field's claim of blind parameter choice as pre-registration
- Do not present a fee-adjusted figure as a full cost accounting while the spread is unmeasured
- Do not claim a band skip avoids the fee-heavy region on this book
- Do not put fee-accurate totals on the hub, digest, manifest, or `records[]`
- Do not revive a burned class under a new name
- Do not treat `H-SPOT-MOY-CONT` as a null
- Do not treat a replayed survivor as lived establishment
- Do not flip `execution` to `true` after an L2-eligible window has closed
- Do not merge lineage A and B
- Do not backfill `072245`
