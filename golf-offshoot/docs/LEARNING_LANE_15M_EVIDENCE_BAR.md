# 15m evidence bar (binding for scoring; Established still unreachable)

**Lane:** `learning_lane_15m` · series `KXBTC15M` only
**Drafted:** 2026-09-08 08:30 EDT · Operator
**Amended:** 2026-09-10 10:15 EDT · Operator, record of Soften Critic CRITIC 20 (zero UPHELD; 0 SUSTAINED / 0 OVERRULED) and Founder-plan bind. Prior: 2026-09-10 09:50 EDT · Operator ANSWER 19 (CRITIC 19 two SUSTAINED leftover-citation strikes; CRITIC 18 recorded as closed-on-prior-hashes). Binding for Admissible scoring. Established still unreachable. Not a score. Consult not enabled.
**Binding?** **Y.** Binding is for Admissible scoring. Established remains unreachable. A system that sets its own *edge* threshold still does not have one.
**Admit?** N · **Edge established?** N · `lab_admits` false · Trading **NOT ARMED**

This bar is **binding for Admissible scoring** after both:

1. the Soften Critic attacks it in writing, in a session that did not draft it, and Operator **sustains or explicitly overrules every objection, each with a stated reason**, in a turn separate from the objections. "Answered" is not "noted." The attack and the answers are both linked from this file. Zero UPHELD is a completed attack: 0 to sustain, 0 to overrule.
2. `critic-invariants` passes on the bytes proposed to bind, **or** every failing check is named on this bar's face with Operator's reason for binding anyway. A findings artifact that says `passed: false` cannot sit under a bar that says `binding: true`.

Founder read-once is **not** a bind condition. Founder 2026-09-09 dropped it: the crew had written it into the 08:30 draft; it was not a Founder GO. Founder remains for **arm** and **HOLD lift** only. Putting it back is a Hard NO; `bind_has_no_founder_read_once` fails the method suite if it returns.

Condition 1 is **met**. This Operator answer (ANSWER 20) records CRITIC 20 (`LEARNING_LANE_15M_EVIDENCE_BAR_CRITIC_20.md`) on the ANSWER 19 hashes (`7C1C1CB3…` / `7A934A4E…`): zero UPHELD, 0 SUSTAINED, 0 OVERRULED. Completed attack, not a skip. CRITIC 19's demanded strikes (MD `:306` eleven with tenth/eleventh named; MD ratchet table half-spread tenth / hub-autostart eleventh; MD `:203` WATCHED landing, not "outside") are on those hashes. CRITIC 18 (`LEARNING_LANE_15M_EVIDENCE_BAR_CRITIC_18.md`) was already recorded in ANSWER 19 as a prior-hash close: a completed zero-UPHELD attack on the ANSWER 17 hashes (`D9FDA991…` / `F7E8F681…`). Those ANSWER 17 bytes were **not** proposed to bind. ANSWER 18 was not written. This bind-face is the Founder-plan recording of CRITIC 20, not a leftover-strike amend that reopens condition 1. **Condition 2** is met as Operator's statement that `run_critic_invariants()` returned `passed: true` on the tree (`fee_schedule_hash_recorded` PASS; pin `founder_browser_bytes`) and that `write_critic_findings()` ran after this face was frozen. The face does **not** copy the findings artifact hash back onto the JSON (that would move the bytes). `last_findings_cover_these_bytes` stays **false**: do not pre-claim; the clerical artifact [`LEARNING_LANE_15M_CRITIC_FINDINGS.json`](LEARNING_LANE_15M_CRITIC_FINDINGS.json) is the machine SoT and is a separate file. The 2026-09-08 `last_findings_reviewed` list remains a lagged snapshot of other bytes. The fee pin is Founder browser bytes (`founder_browser_bytes`), not a gym HTTP 200. Gym 12h 429 is drift detection, not the pin clock. `check_delta_above_detection_floor` now compares `alpha_first_look` to the schedule's first term and `next_look_alpha` to current α_k. δ stays provisional and is not the sole bind reason. Founder read-once is not a bind condition. Binding is not an ADMIT. Scoring against it is not owed this turn. `records[]` stays empty. `currently_reachable` stays **false**.

Amending this bar re-owes the Critic on the new text (`critic.py` keys findings by content hash). That is correct and intended.

Machine copy: [`LEARNING_LANE_15M_EVIDENCE_BAR.json`](LEARNING_LANE_15M_EVIDENCE_BAR.json).
Burned classes: [`LEARNING_LANE_15M_BURNED_CLASSES.json`](LEARNING_LANE_15M_BURNED_CLASSES.json).
Fee source: [`LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md`](LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md) (RUN-ONLY note only — those numbers do not go on the hub, in the digest, in `manifest.json`, or in `records[]`).

---

## Discovery organ (honer_15m)

This lane is the **gym**. `honer_15m` is the **discovery organ** (search → in-band freeze → exam). Isolation of books is a staging wall so evidence stays clean, not a claim that honer stays a toy.

A surviving honer exam may earn a dated **AND-skip consult** inside factory `consult_registry`: one executing factory rule still expresses fill-or-skip; the compositor in [`consult_honer.py`](../src/golf_offshoot/learning_lane_15m/consult_honer.py) may add a skip from a **frozen snapshot**. The compositor reads `latest_dir_15m() / honer_consult.json`: `/workspace/kalshi_15m_exports/latest/honer_consult.json` when `/workspace` exists, else `golf-offshoot/data/learning_lane_15m/latest/honer_consult.json`. The labeled `learning_lane_15m/latest/honer_consult.json` is the fallback shape, not a single path. Enable is `consult_enabled` exactly true. It may never force a fill the factory rule would skip. Live wandering search θ (`honer_15m/latest/theta.json`) never consults.

The compositor already expresses two families: `H-SKIP-RICH-YES` and `H-SKIP-WIDE-SPREAD`. `H-SKIP-WIDE-SPREAD` is OR(spread ≥ (δ or 0), posted_yes ≥ θ), not spread-only. A missing or null δ is `0.0`, so `spread ≥ δ` then holds for every non-negative quoted spread under that family. A rich YES on a tight book still skips under that family.

A honer skip under this compositor keeps the factory `rule_id` and overwrites `reason`. `consult: honer_and_skip` is on the in-memory verdict only; `record_decision` and `append_shadow_advise` do not copy it. A later reader grouping on `consult` will not see honer skips. A `rule_id` group is therefore not a factory-only skip set.

**Currently off** on this tree this turn means the resolved `honer_consult.json` is missing or `consult_enabled` is not exactly true. That is a file flag, not a machine Founder gate. There is no committed lock, no Founder field, and `WATCHED` does not include the snapshot. An enabled snapshot without numeric theta returns the factory verdict (fail-closed). Writing `consult_enabled: true` still leaves the dark path until the family's skip expression also fires. Founder-named implement after exam + later-session Critic is **policy**, not `consult_is_enabled`.

The protocol's exam contrast (step 6) is `d_i = pnl_exam − pnl_fill_all` (gross, in-band exam windows). That is **not** this bar's fee-adjusted five-clause test (`d_i = pnl_rule_fee_adj_i − pnl_baseline_fee_adj_i`, H0 `mean(d) ≤ δ`, clauses (1)–(5), L1 n=70 after `declared_at` then lived L2). Surviving the exam is therefore not surviving this bar.

This paragraph is not a seat, not an ADMIT, not Established, not a keep. Consult stays **off**. `currently_reachable` stays **false**. Binding is **true** for Admissible scoring. Established still unreachable. Trading **NOT ARMED**. HOLD stands.

---

## What the mechanical Critic says about this bar

Disclosed on the face because a bar that fails its own lane's checks and does not say so reads as complete. Run `critic-invariants` against the exact bytes of this file before treating any of this as current.

The method suite has **eleven** checks (`honesty_stamp_is_fresh` is a desk check in `DESK_CHECKS` and does not set `passed`). The tenth is `half_spread_profile_recorded`: [`LEARNING_LANE_15M_HALF_SPREAD_PROFILE.json`](LEARNING_LANE_15M_HALF_SPREAD_PROFILE.json) must exist with n≥1 and be named here. The eleventh is `hub_autostart_registered`: Windows gym queries schtasks `GatedFormalization-15mLearningHub`. The eighth is `series_fee_regime_matches`: ingested `KXBTC15M` `fee_type` / `fee_multiplier` must match `expected_fee_type=quadratic` / `expected_fee_multiplier=1`. `snapshot_absent` returns `state: PASS` (`ok=True` in `_check`). It is inside `CHECKS`, so it does **not** appear in `failing` and does **not** block `passed: true`. `fee_schedule_hash_recorded` is already pinned (`founder_browser_bytes`). That is a named suite green on absence, not a pin of k. The ninth is `bind_has_no_founder_read_once`: the bar must not put Founder acknowledgement on bind. `fee_adjust` still reads `fee_hurdle.k`; live M does not retune k.

This amendment **names** the functions the stricter checks require: `control_function` = `golf_offshoot.learning_lane_15m.rules.matched_exposure_permutation`, `adjustment_function` = `golf_offshoot.learning_lane_15m.evidence_bar.fee_adjust`, `commit_order_control.invariant` = `l1_committed_before_l2`. **`fee_schedule_hash_recorded` is pinned from Founder browser bytes**, not a gym HTTP 200: `schedule_pin_source=founder_browser_bytes`, file [`kalshi-fee-schedule.pdf`](kalshi-fee-schedule.pdf). Last gym GET remains HTTP 429 (drift detection only, 12h cooldown). Do not GET the PDF every 90s. Do not spoof a browser. A 429 does not clear a Founder pin.

`honesty_stamp_is_fresh` is a property of `DESK.md`, not of this bar, and is not this file's to clear. It does not set `passed`.

**A recorded hash in the findings artifact is not the byte hash of this file.** `critic.py` reads with `read_text()` and re-encodes, so on a CRLF checkout it records the newline-normalised digest. Binding condition 2 means the *normalised* bytes the checker actually read. Whoever verifies it must check which digest they are comparing.

---

## Two verdicts, not one

The method already says a gate pass is not a claim: Amb ≠ clearance, print-match ≠ clearance, no soft clearances, establishment-stop drill (`workflow.md`, `templates/02_Gate_Scoring_Sheet.md`). This lane inherits that split.

| Verdict | What it answers | What it licenses | What it does not |
|---|---|---|---|
| **Admissible** | Is this rule well-posed and honestly testable under the gate sheet and this bar? | A dated-record ADMIT that the *test completed* and the rule may stay live as a candidate. Operator note / park row. | Edge. `records[]` as a track record. Skill-met. Productize. Arming. Lifting the HOLD. |
| **Established** | Did the rule clear the locked numerical bar as *edge*, after confirmation? | A method establishment verdict on this lane only, and only after the track has been promoted into the gated method. | Money, keys, series expansion, golf θ, usefulness Soften. **Edge Softened/established?** on an ops-beside stamp stays **N** until promotion has fired. |

An ops ADMIT on this lane, while the lane is still ops-beside-method, is a dated record. Per [`docs/operator_ops/OPS_BESIDE_METHOD.md`](../../docs/operator_ops/OPS_BESIDE_METHOD.md): it does **not** establish edge. **Edge Softened/established?** stays **N**. Observation ≠ edge.

Promotion into the gated method is a separate Founder-named conditional. This bar does not fire it. This bar being written or bound does not fire it. This bar is binding for Admissible scoring. Established remains unreachable (`favorite_odds=2` is not verifiably pre-registered), so a promotion condition that requires Established cannot hold.

---

## No peeking

Score a selection rule at **n = 70** eligible settled windows, not every tick. Continuous scoring against a threshold manufactures significance.

n was 40 in the drafted version. It is 70 because at n = 40 the effect floor δ sat at 0.997 × the minimum detectable effect — the floor *was* the critical value, relabeled. See §Effect floor.

- First look: the first 70 eligible windows after `declared_at` (`close` strictly after declaration). Call this set **L1**.
- Do not compute the test at n = 1, 10, 40, or 69. Do not peek and then wait for a prettier n.
- **L2** (eligible windows 71–140 after `declared_at`) is held out. L2 is strictly forward of L1, which is strictly forward of declaration; `rules.py` `window_is_oos` enforces `closed > declared`, strict.
- **The holdout is not an honour-system reading restriction.** The L1 score note must be **committed before the 71st eligible window closes**, and must record that commit SHA and its timestamp. A note that cannot show it predates the first L2 window is not an L1 score; it is a look at both sets. Enforced by invariant `l1_committed_before_l2` (landed at `0a480d4`). `forward_only: true` is not the control.
- L1 and L2 together are **140 windows = 35.0 hours** elapsed. That is the tape span this lane can offer. The drafted "3 distinct UTC days" clause is **retired**: a 35-hour block touches 3 UTC dates iff L1 starts at or after 13:15 UTC, and 2 if it starts earlier — a clock-alignment rule, not a regime-diversity rule. Recomputed 2026-09-08; no 140-window block that spans more than 35 hours can fail a 3-date test it already games by start time.
- An **Established** verdict on this lane is scoped to the regimes actually observed and does not generalise past them. Say so in the verdict. The retired calendar-date clause does not add a second scope.
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
2. **Multiplicity.** `α_k = 0.05 / (k · (k+1))`, where `k = trials_to_date + 1`, using the registry counter *before* the look. The counter increments on **declaration** and after an **L2** look. An L1 score does not increment.
   The drafted scheme was `0.05 / k`. Its weights are the harmonic series, which diverges, so it controls nothing: over the bar's own 14-look week `1 − Π(1 − 0.05/k) = 15.2%`, not 5%. The replacement sums to 0.05 over an unbounded number of looks (`Σ 0.05/(k(k+1)) = 0.05`), giving FWER ≤ 0.05 forever. `α_1 = 0.025`, z = 1.960, is the schedule's first term, spent on declaration, historical — matching the table and JSON `alpha_first_look_is_historical`. The first scoring look under this increment rule is k=2 / α=0.008333. `α_14 = 0.000238`, z = 3.494, is the schedule's 14th term (the 13th scoring look). FWER over 14 schedule terms under the new scheme is 4.6% — that sum includes the spent unused α_1.
   The increment is **mechanical**: `rules.record_trial` writes `trials_log` and `trials_to_date` on `declaration` and `l2_look` only. Baseline naming is not a trial. An L1 score is not a trial kind. `R-SKIP-COINFLIP`'s pre-mechanism declaration is not backfilled; the counter stays 0. Clause (2) uses that counter as it stands.
3. **Effect floor:** `δ = $0.28` per window, **= 0.28 × stake**. Absorbed into clause (1) as the null. See §Effect floor for what δ is and is not.
4. **Positive side.** `mean(pnl_rule_fee_adj) > 0` on those same n windows. Promoted from conditional prose to a binding numbered clause. Beating a losing baseline by skipping, and still booking ~0 after fees, is distinguishable-or-not; it is not a positive result that cleared the cost. Skip-all yields 0 and fails this clause.
5. **Matched-exposure permutation control.** `mean(d)` must exceed the `1 − α_k` quantile of a permutation null that **holds the number of skips fixed and reassigns which windows are skipped**: ≥ 10,000 draws, seed **`20260908`**, pre-registered here. This null is centred on abstaining at the observed rate with no skill, which is the correct comparison; clause (1) alone would still credit mechanical fee avoidance. Deterministic given the seed, no new data, no loop code.

**Also print, beside `mean(d)`:** `skip_rate × mean(fee | skip)` — the mechanical fee-avoidance component of the contrast — so a reader can see how much of the result is arithmetic rather than selection.

**Kill / park** (the numeric form of `R-SKIP-COINFLIP`'s falsifier): if at n = 70 the rule fails any of (1)–(5), **park it and do not retune the band.** A dead test is a complete outcome. Record the park on that falsifier. The registry falsifier now reads "the n named by the evidence bar in force" so the two cannot drift to 40 vs 70 again. `triggers.py` already fires `rule_reached_n` from `looks.first_look_n`, not from the registry sentence.

### Effect floor

**δ = $0.28 per window is provisional and is not yet derived from decision relevance.** Stated plainly because the drafted bar presented a coincidence as a rationale: δ was `2.69 × SE₄₀`, the critical value at family α = 0.05 over 14 looks, and δ/MDE was **0.997**. The floor was the rejection threshold wearing an effect floor's clothes, and it therefore carried no information about whether an effect of that size is worth acting on.

What has changed: δ is no longer derived from the critical value, and n has moved so the two numbers are not the same number.

| | Drafted (n = 40) | First look, spent (n = 70, α = 0.025) | Next look (k = 2, α = 0.008333; the scorer) |
|---|---|---|---|
| sd used | 0.66 (point estimate) | **0.784** — 95% upper confidence bound on 0.66 from 56 calibration windows. δ is linear in sd and 0.66 is one number from one 14-hour stretch | same 0.784 |
| SE | 0.1044 | 0.0937 | 0.0937 |
| α | 0.05 | 0.025 (spent slot; labeled historical) | **0.008333** |
| z | — | 1.960 | **2.394** |
| MDE | 0.2807 | 0.1837 | **0.2243** |
| **δ / MDE** | **0.997** | **1.52** | **1.25** |
| Reject if mean(d) > | 0.28 (H0 ≤ 0) | 0.464 (H0 ≤ δ; spent) | **0.504** (H0 ≤ δ; next look) |

**Power, on the bar's face.** Under the amended null, power *at* δ is α by construction — that is what testing against a floor means. So the honest statement is the curve, not a single number. The spent first-look curve is historical. A later score under `trials_to_date = 1` uses the next-look curve:

- Spent first look (α = 0.025): 50% power against **$0.464/window**; 80% against **$0.543/window**.
- Next look (k = 2, α = 0.008333): 50% power against **$0.504/window**; 80% against **$0.583/window**.
- Under the *drafted* design (H0 ≤ 0, n = 40) the bar had **~50% power at δ** and reached 80% power only at $0.37/window. A bar that misses half the effects it declares material is a coin.

**Read this honestly: with per-window sd near 0.66–0.78 and an n reachable in under two days, this lane can only detect very large effects.** That is a property of the tape and the $1 unit, not a defect the bar can amend away. It is disclosed rather than hidden.

**Owed before binding:** δ re-derived from what size of edge is worth acting on. The crew has no decision-relevance anchor today — the lane is paper-only, HOLD stands, no capital is at risk — so δ is carried at $0.28 provisionally with the coincidence labelled. A later Operator turn or Founder must name a decision-relevant δ. Until then this bar cannot bind on δ alone.

---

## The omitted costs

Recorded pnl omits **two** costs, not one: the entry fee **and** the bid/ask spread.

**Fee adjustment** (from the RUN-ONLY note, k = 0.07, $1 stake, ceil to the cent):

`fee_i = ceil_cent(0.07 × stake_i × (1 − posted_yes_i))`

`pnl_fee_adj_i = recorded_pnl_i − fee_i` on a fill; `0` on a skip.

Measured cost cited from that note, not restated here as a dashboard figure: mean **$0.039** per fill, **3.92%** of stake, on the first 24 lineage-A books. A later public schedule that names a different `k` or a `KXBTC15M` override makes this stale. **The schedule sha256 is pinned from Founder browser bytes** (`founder_browser_bytes`, [`kalshi-fee-schedule.pdf`](kalshi-fee-schedule.pdf)) — see §What the mechanical Critic says.

**The fee is strictly decreasing in the mark.** With stake fixed at $1, contracts `C = stake/P`, and Kalshi's `0.07 × C × P × (1−P)` reduces exactly to `0.07 × stake × (1 − P)`. So: $0.0455 at P = 0.35, $0.035 at P = 0.50, $0.014 at P = 0.80. The RUN-ONLY note's own table confirms it — every $0.05 ceil-cent fee sits at a mark between 0.3350 and 0.4250, every mark inside (0.45, 0.55) pays $0.04, and the 0.9835 mark pays $0.01.

**Consequence for band rules, stated because it inverts an easy assumption:** a rule that skips the middle of the mark distribution does **not** avoid the fee-heavy region. It skips the middle of the fee distribution and keeps the most fee-expensive fills. "Avoids the fee" is not available as a thesis for a coinflip-band skip on this book. Any rule proposing to avoid cost by skipping must state which cost, and in which direction it runs.

**The spread is omitted entirely and is not adjusted for.** `paper_mark` is `public_mid_or_last(...)` — the **mid** whenever both sides are quoted — and the payout is `1/mark`. The book buys at the mid and is paid at the mid, while the RUN-ONLY note charges a **taker** fee on that fill. A taker pays the ask, not the mid. The omitted half-spread costs `s / (p + s)` per $1 of stake: on a one-cent book that is about **$0.010 per fill** at p = 0.50 and about **$0.020** on a two-cent book — the same order as the $0.039 mean fee.

**Direction of the spread cost, at a constant tick only.** At a constant tick, `s/(p+s)` is *decreasing* in p — $0.0164 at p = 0.30, $0.0110 at 0.45, $0.0099 at 0.50, $0.0055 at 0.90. **At a constant tick** it runs the same direction as the fee, not the opposite. **At a constant tick** a band skip avoids neither cost's worst region.

That constant-tick premise is **contradicted** by the module this bar cites for `paper_mark`: `PRICE_LEVEL_STRUCTURE = "tapered_deci_cent"` in `kalshi_15m.py`. A tapered tick is finer at the extremes and coarser in the middle — the geometry that can restore an increasing half-spread toward 0.50. The empirical profile — mean `(yes_ask − yes_bid)/2` bucketed by mark — is [`LEARNING_LANE_15M_HALF_SPREAD_PROFILE.json`](LEARNING_LANE_15M_HALF_SPREAD_PROFILE.json). `half_spread_profile_recorded` fails if that artifact is missing or empty. The fee-adjusted figure remains optimistic by the measured half-spread; it is still not a full cost accounting.

**Therefore: the fee-adjusted figure remains optimistic by the measured half-spread** (mean **0.00385** on n=624 quotes in [`LEARNING_LANE_15M_HALF_SPREAD_PROFILE.json`](LEARNING_LANE_15M_HALF_SPREAD_PROFILE.json); middle buckets near 0.005). `fee_adjust` still does not subtract it. No fee-adjusted number produced under this bar may be presented as a full cost accounting.

**The adjustment is code.** `golf_offshoot.learning_lane_15m.evidence_bar.fee_adjust` landed at `0a480d4` and reproduces all 24 rows of the RUN-ONLY fee table. The score note must cite that function. The recorded book still has no fee term (`settle.py` pays `stake * decimal_odds`). `fee_type=quadratic x1` on a movement is a label of the schedule that *would* apply, not a fee that was charged.

**The recorded book's own notes contradicted the mid fill, and the live writer is corrected.** `paper.py` prefers `paper_mark` (the mid) and falls back to `yes_ask` only when the mark is absent. The live path is the mid. The docstring and position `notes` now say public mid/last mark. Historical books written to date still carry the old "posted Kalshi ask" string; those provenance strings are known wrong rather than silently rewritten.

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

**`R-SKIP-2TO1-FAVORITE`'s `favorite_odds=2` does not meet this either, and this bar records that on its face.** First naming is `e9fab5a` at 2026-09-08 16:56:05 EDT (`declared_at` 16:53:00; 3m 5s commit lag). The published RUN-ONLY fee table (`2fea8d8`, author 2026-09-07 21:49:37 EDT) already listed 24 marks; **2 of 24** are ≥ 2/3 (`0.9835` on `071545`, `0.7050` on `071600`). Gap: **19h 06m 28s**. A registry `note` asserting those marks did not inform the parameter is not proof. `favorite_odds=2` as "the first integer odds strictly above evens" is a conventional prior that does not require the tape — that is recorded, not treated as proof, and **is not a third clause of this test**. This is **not** a peek finding and not a score. **`verifiably_preregistered` is false.** L1 cannot support Established for this rule even if it later passes every clause. L1 may still be scored and may still support an Admissible dated record. `execution` stays true (RUN-ONLY, paper). This condition dies for this rule if a commit, desk line, or dated artifact predating 2026-09-07 21:49:37 EDT names `favorite_odds=2`. None was found. A later turn may not flip the flag by accepting a conventional-prior exception the two-part test does not contain.

WATCHED now includes `lab_proposed_02` (`LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_02.md`) and `lab_lab_proposed_02` (`LEARNING_LANE_15M_LAB_PROPOSED_02.md`) in addition to `lab_proposed` (`LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md`). This turn did not edit `critic.py`.

---

## The L2 confirmation test

Specified here, before L1 is scored, so the confirmation threshold cannot be set once L1 is known. A confirmation look with an unspecified threshold is not pre-committed.

| | L2 |
|---|---|
| n | 70 (eligible windows 71–140 after `declared_at`) |
| H0 | `mean(d) ≤ δ`, same form as L1 |
| δ | the same δ in force when L1 was scored. It does not move between looks |
| α | `α_k` from the same schedule, using the counter as it stands after the **declaration** increment. L1 scoring does not increment. With `trials_to_date = 1` today, L2 shares the next-look set (k=2, α=0.008333, reject 0.504, MDE 0.2243, 50% 0.504, 80% 0.583). The struck sentence said "after L1's increment." `record_trial` accepts only `declaration` and `l2_look`; there is no L1-score kind |
| Clauses | (1), (3), (4), (5) all bind, same as L1 |
| Counter | **L2 increments `trials_to_date` after its look.** A confirmation look is a look. Not counting it makes confirmation free. An L1 score does not increment |
| Execution | must be **lived** — see §Replay versus lived |

---

## Replay versus lived

The registry already says these are different evidence. This bar says which verdict accepts which.

| Evidence | Admissible | Established |
|---|---|---|
| **Replay** (`execution=false`; books collected without the rule acting) | Yes — L1 may be scored by replay. Declaration time makes the data clean. | **No.** A replayed survivor is not a lived one. |
| **Lived** (`execution=true`; the loop honoured `rules.decide()`) | Yes — also acceptable for L1 if the rule was live for those windows. | **Required** for L2 confirmation and for any establishment verdict. |

Replay assumes fills live execution might not get. Skipping a bet changes nothing about the market and does change the fill sequence. Both are legitimate. They are not interchangeable.

**Lived paper for `R-SKIP-2TO1-FAVORITE` begins at the execution flip, not at `declared_at`.** Flip recorded in the Operator note at **2026-09-08T17:11:00-04:00**, commit `0daae90` (17:14:46 EDT). Any window whose `close` is strictly after `declared_at` `2026-09-08T16:53:00-04:00` and at or before `2026-09-08T17:11:00-04:00` is **replay** for this rule. A later L1/L2 score that includes a window from that interval as lived fails this bar. I am not asserting which window ids exist or what they paid.

**These lived/replay fields are enforced by the scorer.** `window_is_oos` still keys only on `closed > declared_at` (the `decide()` expression gate). `score_rule` calls `_assert_window_lived_or_raise`, which reads `lived_paper_begins_at` / `replay_close_*` and raises `RuleNotScorable` on a window in `(replay_close_after, replay_close_at_or_before]`. A later score that treats a window from that interval as lived fails as a machine, not only as prose. This Systems turn did not score and did not open window outcome files.

**Established is currently unreachable, and this bar says so rather than implying otherwise.** `paper.py` consults `rules.decide()` via `consult_registry`, then a dark AND-skip compositor that does not move Lineage A while `consult_enabled` is off. **This face does not claim a live process tip.** `watch.json` may exist on the gym tree; it is not bind evidence. This turn did not start or kill a hub. The previous face cited running-hub tip `0a480d4`. That SHA is Turn 2 (13:46 EDT). At `0a480d4`, `decide()` has no `favorite_odds` dispatch: after the OOS check it only special-cases `R-SKIP-COINFLIP`; every other selecting id gets `unknown`. HEAD `_express_selection` does dispatch `params.favorite_odds`. `R-SKIP-2TO1-FAVORITE` **does exist**: declared at `e9fab5a` (`declared_at` 16:53:00), `execution=true` since 17:11 (`0daae90`). That is not enough. The bar is binding for Admissible scoring; `favorite_odds=2` is **not verifiably pre-registered**; skip-on-mark classes on this tree are likely burned for Established. The fee pin is `founder_browser_bytes`, not a gym HTTP 200. `R-SKIP-COINFLIP` still has `execution: false`, and its band is not verifiably pre-registered. `currently_reachable` stays **false**.

**Explicit precondition of Established:** a selection rule declared after the `decide()` flip, with verifiably pre-registered parameters, and `execution=true` before its first L2-eligible window closes, scored under a binding bar. `R-SKIP-COINFLIP` cannot satisfy this. `R-SKIP-2TO1-FAVORITE` fails the pre-registration half. This turn does not flip `R-SKIP-COINFLIP` and does not flip `currently_reachable`.

**The permitted flip point.** `execution=false → true` is legitimate **only before the first L2-eligible window closes**, and only recorded with a commit SHA and timestamp. Flipping it after any L2 window has closed, or flipping it to make a replayed look read as lived, is the prohibited move. The drafted ban read as absolute and forbade the only action that produces a lived confirmation; it is a timing rule.

---

## Trials accounting

`trials_to_date` lives on [`LEARNING_LANE_15M_RULES.json`](LEARNING_LANE_15M_RULES.json). It started at **0**. It is now **1**.

**It increments on the *declaration* of a selection rule on this lane, not on the score.** The drafted rule incremented "once per first-look (L1) score," which defines the multiplicity family by what got written up rather than by what got tried. A rule proposed, replayed informally and dropped before anyone wrote a score never touched the counter. That is the wrong denominator and it always flatters. Baseline naming is not a trial. L2 confirmation looks also increment (see §The L2 confirmation test).

The counter is mechanical as of `0a480d4`: `record_trial` writes `trials_log`. Baseline naming is not a trial. `R-SKIP-COINFLIP`'s pre-mechanism declaration is not backfilled. The `R-SKIP-2TO1-FAVORITE` declaration spent the first slot (`trials_log` row at 16:53:00; `trials_to_date_after` 1). This turn does not increment it again.

**Next look.** `score_rule` reads the registry counter and computes `alpha_k` with `k = trials_to_date + 1`. The next look is **k = 2**, α = `0.05 / (2 · 3)` = **0.008333**. `alpha_first_look: 0.025` is the schedule's first term, now historical. The rejection threshold / MDE / 50% / 80% power a later score will be compared against are the next-look set in §Effect floor (0.504 / 0.2243 / 0.504 / 0.583), not the spent first-look set (0.464 / 0.1837 / 0.464 / 0.543). L2 uses that same k: an L1 score does not increment, so a later L2 is also k=2 until L2 itself increments. Advertising "after L1's increment" as if an L1 score moved the counter is a different test from the scorer.

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

After promotion fires (conditional, not this bind): establishment is adjudicated under the standing gated-method rules against *this* bar. Operator issues that verdict without asking Founder. Promotion is not itself a verdict. Binding for Admissible scoring is not promotion and is not Established.

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

## Ratchet: which check guards which CRITIC 01 finding

Named on the face because fourteen sustained objections and zero new `CHECKS` members was the Y2 finding. The suite now has **eleven** method checks (`series_fee_regime_matches` is the eighth; `bind_has_no_founder_read_once` is the ninth; `half_spread_profile_recorded` is the tenth; `hub_autostart_registered` is the eleventh). Several of the first seven were **rewritten** at `0a480d4` rather than appended. JSON copy: `ratchet_guards`.

| CRITIC 01 | What now guards it, or why a check is impossible |
|---|---|
| F1 H0 floor | `delta_above_detection_floor` reads `h0` and reports 50/80% power |
| F2 matched exposure | `matched_exposure_control` requires `control_function` + `score_rule` call |
| F3 power | same check recomputes se / mde / threshold / power and fails on disagreement |
| F4 holdout | `holdout_is_forward_only` keys on `l1_committed_before_l2`, not `forward_only` |
| F5 pre-registration | no check searches git history; the coinflip 8h 07m 14s gap and the `favorite_odds=2` 19h 06m 28s gap stay on the face; conventional-prior is not a flip path |
| F6 multiplicity | `trials_counter_is_consistent` requires `record_trial`; α is `0.05/(k(k+1))` |
| F7 fee-free book | `fee_adjusted_book_is_binding` requires `fee_adjust` and reads the payout line |
| X1 spread | empirical profile landed n=624 mean 0.00385 (`LEARNING_LANE_15M_HALF_SPREAD_PROFILE.json`); `fee_adjust` still omits it; not a fee adjustment |
| X2 reachable | `currently_reachable` stays false; `R-SKIP-2TO1-FAVORITE` registry `execution` is true; lived honoring is unproven on this tree this turn (no tip, no cited decision row); pre-registration still blocks Established; bar is binding for Admissible scoring; fee pin is landed |
| X3 L2 test | `looks.l2_test` is on the face; L2 α is the declaration-counter k and shares the next-look set; a missing-field check is possible, not written |
| X4 trials on declaration | `record_trial`; baseline naming raises |
| X5 sustain-or-overrule | prose; a hash check cannot read an admit-pass verdict |
| X6 δ is a fraction | `effect_floor_as_fraction_of_stake`; `PAPER_UNIT` invariant still owed |
| X7 heartbeat clear | `critic_verdicts` drops `detail`; honesty is a desk check; failing-set materiality |
| gym-pin eighth | `series_fee_regime_matches` is in `CHECKS`; `snapshot_absent` (missing, unreadable, or non-dict) is `state: PASS` and does not block `passed: true`; fee hash is pinned (`founder_browser_bytes`); a well-formed present missing/drifted M FAILs; the eighth-check detail and docstring still say "half-pass" / "silent half-pass" "named on the bar", which the ANSWER 14 hashes did not contain |
| Founder 2026-09-09 | `bind_has_no_founder_read_once` fails if that id returns on `binding_conditions`, or if `binding_rule` still requires a numbered Founder-acknowledgement gate |
| half-spread tenth | `half_spread_profile_recorded` requires n≥1 named artifact LEARNING_LANE_15M_HALF_SPREAD_PROFILE.json |
| hub-autostart eleventh | `hub_autostart_registered` queries schtasks GatedFormalization-15mLearningHub on the live Windows gym; scratch-tree skips |

## Hard NOs (this bar)

- Do not treat binding for Admissible scoring as Established
- Do not add `founder_read_once` as a bind condition
- Do not set `binding: true` while `critic-invariants` reports `passed: false` on these bytes
- Do not score `R-SKIP-COINFLIP` before 70 eligible windows, and not in the drafting or amending session
- Do not peek L2 while scoring L1, and do not claim you did not without the commit order to show it
- Do not treat a `note` field's claim of blind parameter choice as pre-registration
- Do not present a fee-adjusted figure as a full cost accounting while the measured half-spread is omitted from `fee_adjust`
- Do not claim a band skip avoids the fee-heavy region on this book
- Do not treat the half-spread profile as a fee adjustment
- Do not put fee-accurate totals on the hub, digest, manifest, or `records[]`
- Do not revive a burned class under a new name
- Do not treat `H-SPOT-MOY-CONT` as a null
- Do not treat a replayed survivor as lived establishment
- Do not flip `execution` to `true` after an L2-eligible window has closed
- Do not merge lineage A and B
- Do not backfill `072245`
