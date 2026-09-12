# Operator answer — admit pass on Soften Critic CRITIC 01

**Role:** Operator · **Date:** 2026-09-08 · **Lane:** `learning_lane_15m` · series `KXBTC15M` only

**Critic file answered:** [`LEARNING_LANE_15M_EVIDENCE_BAR_CRITIC_01.md`](LEARNING_LANE_15M_EVIDENCE_BAR_CRITIC_01.md)
**SHA-256 of the exact bytes answered:** `F23A5A513AB9E63746468128442D1D94DBA1BEC4E16552CEBC9B9BF27C9CA85C`
(newline-normalised digest, for comparison with `critic.py`'s reviewed list: `06A250CAB4F3425143AB48AC692F664544C3E6167C6AB79E4B88577BF79C987F`)

**This is a separate turn from the one that raised the objections.** `PROTOCOL.md` forbids one turn both objecting and dismissing: "Operator's answers must be a separate turn from the objections. One turn may not both object and dismiss." The Critic did not write this file and this turn did not write the attack.

**Nothing here is an ADMIT.** No rule was scored. `R-SKIP-COINFLIP` was not scored. No post-declaration window outcome file was opened — not `paper/*.json`, not `settlements/*.json`, not `latest/journal.json`. The bar stays `binding: false`, `admit: false`, `edge_established: false`, `lab_admits: false`, `trading_armed: false`. The series HOLD stands. Trading is **NOT ARMED**. Nothing was committed or pushed. `DESK.md` and `AGENT_LEAVE_OFF.md` were not touched — Chief of Staff owns those. No file under `golf-offshoot/src/` was edited; a separate Systems turn owns the code defects.

**Verdict count:** 14 objections. **7 SUSTAINED, 7 SUSTAINED IN PART, 0 dismissed without a reason.** Every objection carries a stated reason. Where a Critic claim did not survive my own check it is overruled and said so — three did not.

---

## What I verified myself before sustaining

The Critic's arithmetic was recomputed independently. Every number in this table was reproduced from the files, the code, or the commit record — not taken on the Critic's word.

| Claim | Critic | My recomputation | Verdict |
|---|---|---|---|
| SE at n = 40, sd 0.66 | ≈ 0.104 | 0.104355 | confirmed |
| δ / MDE at n = 40 | **0.997** | 0.28 / 0.280716 = **0.99745** | confirmed |
| Power at δ under H0 ≤ 0 | ≈ 50% | 49.73% | confirmed |
| 80% power effect at n = 40 | $0.369 | $0.36854 | confirmed |
| n for 80% power at δ | ≈ 70 | 69.3 | confirmed |
| z for α = 0.05/14 | 2.690 | 2.69012 | confirmed |
| FWER over 14 looks at α_k = 0.05/k | **≈ 15.2%** | 1 − Π(1 − 0.05/k) = **0.151767** | confirmed |
| Σ 0.05/k diverges | yes | harmonic; Σ over 14 = 0.16258 | confirmed |
| Two α's one line apart | $0.17 vs $0.28 | 1.645 × SE = $0.1716; 2.690 × SE = $0.2807 | confirmed |
| `fee = 0.07 × stake × (1 − P)` strictly decreasing in P | yes | ∂fee/∂P = −0.07 × stake < 0. Note's own table: raw fee at mark 0.9835 = 0.001155 = 0.07 × 0.0165 exactly | confirmed |
| Fee at P = 0.35 / 0.50 / 0.80 | $0.0455 / $0.035 / $0.014 | identical | confirmed |
| Free abstention buys 5.6% of δ | ≈ $0.016 | (22/56) × $0.04 = $0.01571 = 5.61% of δ | confirmed |
| Gap `2fea8d8` → `0786279` | 8h 7m | `git show -s --format=%at`: **8h 7m 14s** | confirmed |
| Band first named 51s after `declared_at` | yes | commit 05:56:51 −0400 vs `declared_at` 05:56:00 −0400 | confirmed |
| 8 in-band marks in the published 24-row table | 8 | 0.4650, 0.5150, 0.4950, 0.5150, 0.4850, 0.4550, 0.4750, 0.4550 — all pay $0.04 | confirmed |
| Those 8 rows sum | +$2.51 raw, +$2.19 fee-adj | +2.51 and +2.19; −$0.091/window over 24 | confirmed |
| Every $0.05 fee sits at a mark 0.3350–0.4250 | yes | all 7 such rows | confirmed |
| No production caller of `rules.decide()` | yes | only `tests/test_learning_rules.py` | confirmed |
| `settle.py` pays with no fee term | yes | `payout = round(pos.stake * pos.decimal_odds, 2) if won else 0.0`; no fee anywhere in `_apply_official_settle` | confirmed |
| `paper_mark` is the mid | yes | `public_mid_or_last` returns `(yes_bid + yes_ask)/2` whenever both are quoted | confirmed |
| Half-spread cost `s/(p+s)` at p = 0.50 / 0.90 | $0.010 / $0.006 | 0.00990 / 0.00552 on a one-cent book | confirmed |
| **Spread cost is worst at the coinflip** | asserted | **false** — see X1 | **not confirmed** |
| Alternative weighting Σ = 1 | asserted | 0.05/(k(k+1)): Σ→0.05, FWER₁₄ = 0.0459. 0.05·2⁻ᵏ: Σ = 0.05, FWER₁₄ = 0.0492 | confirmed |

One citation correction, immaterial to any finding: `kalshi_15m.py` is at `golf-offshoot/src/golf_offshoot/data_feeds/kalshi_15m.py`, not under `learning_lane_15m/`. All line references check out at that path.

---

## Finding 1 — Rigged comparison

### **SUSTAINED IN PART.**

**Overruled:** the original form, "when fill-all has negative EV, betting less automatically beats it." The Critic rejected this itself and I concur on the arithmetic. Every mark strictly inside (0.45, 0.55) yields a ceil-cent fee of exactly $0.04, so at the pre-declaration skip rate of 22/56 free abstention earns $0.0157 per window against δ = $0.28 — **5.6% of the bar**. Mechanical fee avoidance cannot clear the floor. The rigging is real in the null statement and inert in the decision.

**Sustained:** `H0: mean(d) ≤ 0` is known false before any data are collected. I verified the chain in code, not prose: `paper.py` reads `decimal_odds` or falls back to `1.0/mark`; `settle.py:345` pays `stake × decimal_odds`. So at a calibrated mark the expected pnl is `P(1/P − 1)·stake − (1−P)·stake = 0` exactly — the fill is EV-zero *pre-fee*. The fee is strictly positive on every fill (F2 in the RUN-ONLY note: minimum ceil-cent fee $0.01, none rounded to $0.00). Since a skip contributes 0 pnl and 0 fee while the baseline pays the fee, `E[d] = skip_rate × E[fee] > 0` for any nonzero skip rate with no selection skill present at all. A one-sided test against zero is a test of arithmetic.

**Changed in the bar.** Clause (1) restated as **H0: mean(d) ≤ δ**. Clause (3) is absorbed into the null rather than checked as a second hurdle, which is what the Critic asked for and is also cleaner — there is now one hurdle, not two. The score note must print `skip_rate × mean(fee | skip)` beside `mean(d)`. The "Positive side" clause, previously conditional prose outside the numbered clauses and not referenced by the kill/park test, is promoted to **binding clause (4)**.

---

## Finding 2 — No matched-exposure control

### **SUSTAINED.**

The contrast is matched on windows and unmatched on exposure. `skip_contributes: 0`, no `matched_exposure` key existed, and nothing normalised for the rule arm risking `(1 − skip_rate) × n × $1` against the baseline's `n × $1`. The bar named the question — "The contrast lives in the skips" — and did not build the control that answers it. `critic.py` `check_matched_exposure` fails on exactly this and words it the same way.

The demanded control also clears the CoS RUN-ONLY routing test on all four counts: deterministic given a seed, no loop code, quarantined output, and it carries its own falsifier.

**Changed in the bar.** New binding **clause (5)**: a permutation null holding the number of skips fixed and reassigning which windows are skipped, ≥ 10,000 draws, seed **`20260908`** pre-registered on the bar's face. Observed `mean(d)` must exceed the `1 − α_k` quantile. `mean(d)` per dollar at risk must be reported beside `mean(d)` per window.

Worth recording: this control and the Finding 1 fix attack the same defect from two directions, and clause (5) is the stronger of the two. The permutation null is automatically centred on "abstaining at the observed rate with no skill," which is the correct null — it prices the mechanical fee-avoidance term instead of assuming it away.

---

## Finding 3 — Power

### **SUSTAINED IN PART.**

**Overruled:** the original form, "thirteen eligible windows is nothing." That phrase appears nowhere in the draft. The bar said n = 40 in four places and explicitly forbade looking earlier. The Critic rejected its own premise and I concur — whoever reconstructed that finding was not reading the bar.

**Sustained:** all three sharper claims, each recomputed. δ/MDE = **0.99745** — clause 3 was clause 1's critical value relabeled, carrying no information about whether an effect that size is worth acting on. Power at δ was **49.7%**; a bar that misses half the effects it declares material is a coin. 80% power at n = 40 arrived only at **$0.3685/window**, 37% of a $1 stake every window.

**Overruled within the sustained part:** demand (c), "set n = 70" to obtain 80% power at δ, does not do what the Critic says once Finding 1 is also sustained. Under `H0: mean(d) ≤ δ`, power *at* δ equals α by construction — that is what testing against a floor means. There is no n at which the amended bar has 80% power at δ. The Critic's two remedies are incompatible and the filing did not notice. I take the number and discard the rationale: **n = 70** stands, because at n = 70 δ is 1.52× the detection floor instead of 0.997×, which is the defect that actually needed fixing.

**Changed in the bar.** n = 40 → **70**, with the reason stated. δ's rationale rewritten: it is explicitly **not** derived from the critical value, and the old coincidence is labelled as a coincidence rather than presented as a rationale. The power curve is printed on the face — 50% power at $0.464, 80% at $0.543 under the amended design, with the drafted design's 50%-at-δ recorded beside it for comparison. The bar now states plainly that with per-window sd near 0.66–0.78 and an n reachable in under two days, this lane can only detect very large effects, and that this is a property of the tape rather than a defect the bar can amend away. δ = $0.28 is carried **provisionally**, with re-derivation from decision relevance recorded as owed before binding.

---

## Finding 4 — Holdout is ineffective

### **SUSTAINED IN PART.**

**Overruled:** the factual premise. L2 is not carved from the same period — it is windows after `declared_at`, strictly forward of L1, which is strictly forward of declaration, and `rules.py` `window_is_oos` enforces `closed > declared` strictly in code. It was also pre-registered, written into the draft before any score existed. The Critic rejected its own premise and I concur.

**Sustained, residual (i):** one regime and less than a day of it. By the bar's own ~96 windows/day arithmetic, L1 + L2 spanned ≈20 hours and the δ calibration set spanned the ~14 hours immediately before — one contiguous ~34-hour stretch of tape covering calibration, first look and confirmation.

**Sustained, residual (ii):** the holdout was prose. "The session that scores L1 must not read L2" is an honour-system reading restriction on files in the same directory that are likely already settled on disk by L1-scoring time. The bar mechanically enforces its burned-class list and left its holdout to a sentence. `PROTOCOL.md`: "A failing invariant is never satisfied by prose."

**Changed in the bar.** The L1 score note must be **committed before the 71st eligible window closes**, recording that commit SHA and timestamp — hash-provable, and the only version of the rule that is not self-certification. L1 + L2 must span at least **3 distinct UTC days**, and the bar states on its face that an Established verdict is scoped to the regimes observed and does not generalise past them. The invariant is recorded as owed to Systems.

**Disclosed, because the Critic warned about exactly this:** setting `forward_only: true` flips `critic.py`'s `check_holdout_is_forward_only` from FAIL to PASS on a keyword. I set the key, and I record here and on the bar's face that **the keyword is not what makes the holdout real** — the commit-ordering clause is. That PASS must not be read as clearance. I am not willing to leave the key unset and pretend the substance is missing, nor to set it and pretend the check now means something.

---

## Finding 5 — Delta is an in-sample free parameter

### **SUSTAINED IN PART.**

**Overruled as applied to δ.** δ was a deterministic function of (sd, n, α), not of the observed mean, and the bar disclosed its calibration set in full: which 56 books, which two fields, which windows were not opened, and a volunteered statement that the in-sample mean contrast was inspected only to confirm δ was not fit so history would pass. The Critic rejected this itself and I concur — that is more disclosure than the finding assumed.

**Sustained as applied to the band, which is the parameter that actually selects windows.** I verified the commit record directly rather than accepting the Critic's table. `2fea8d8` landed 2026-09-07 21:49:37 −0400 with the RUN-ONLY note's 24-row table of mark and recorded pnl. `0786279` landed 2026-09-08 05:56:51 −0400 with the first appearance of (0.45, 0.55), 51 seconds after its own `declared_at`. `git show -s --format=%at` gives the gap as **8h 7m 14s**. A history search for the band across all refs finds no earlier artifact naming it. Eight of the 24 published rows fall strictly inside the band. The registry's own `note` — "Band chosen before looking at overnight marks" — is a self-certification the bar accepted without asking for anything, and the information was demonstrably published on this tree before the band was dated. Intent may well have been blind; the bar does not adjudicate intent.

**Sustained, (c):** δ is linear in sd and sd = 0.66 is one number from 56 windows in one 14-hour stretch. The χ² one-sided 95% upper confidence bound at 55 df is 38.958, giving sd_UCB = 0.66 × √(55/38.958) = **0.784**.

**Changed in the bar.** A new **Pre-registration of rule parameters** section: parameters count as pre-registered only with the commit SHA and timestamp of the registry entry that first names them, plus a statement that the timestamp predates the earliest window whose mark informed the parameter — including marks published anywhere on this tree, not only marks the author remembers reading. A `note` field's own claim is explicitly not proof. The bar records on its face that `R-SKIP-COINFLIP`'s band is **not verifiably pre-registered**, with the commit table, and that its L1 therefore **cannot support Established even if it passes every clause**; L1 may still be scored and may still support an Admissible dated record. δ now uses sd_UCB = 0.784, not the point estimate, wherever it is compared to a detection floor.

That last paragraph is a statement about the provenance of a parameter. It is not a score of the rule, and no post-declaration window outcome was read to write it.

---

## Finding 6 — Multiple testing uncorrected

### **SUSTAINED IN PART.**

**Overruled:** "uncorrected" is false. Clause 2 existed, and the draft said in terms that a bar with no multiplicity term is incomplete. The Critic rejected its own premise and I concur.

**Sustained, all three sharper forms, each recomputed.** (1) On the only trial this bar governs the correction is numerically inert: `trials_to_date: 0` gives α = 0.05/1 = 0.05, identical to the naive level the bar said it was replacing. (2) The scheme controls nothing — Σ 0.05/k is harmonic and diverges; over the bar's own 14-look week `1 − Π(1 − 0.05/k) = 0.151767`, i.e. **15.2%**, not 5%. (3) The bar stated two different α's one line apart: clause 2 gave α = 0.05 → threshold $0.1716, while δ was derived at α = 0.05/14 → threshold $0.2807. Both were presented as the bar and they are not the same bar.

**Also sustained:** nothing increments the counter. `evidence_bar.py` never reads `trials_to_date`; `rules.py` only loads the registry; the only references on the tree are docs and tests. `critic.py`'s `check_trials_counter_is_consistent` keys on `scored_windows` / `last_look_at`, fields no code writes, so it passes vacuously. The bar's own text says prose is not enforceable and its multiplicity counter was prose.

**Changed in the bar.** α_k = **0.05 / (k(k+1))**, k = `trials_to_date` + 1. I verified this sums to 0.05 over unbounded looks and gives FWER₁₄ = 0.0459 ≤ 0.05. First look α₁ = 0.025, z = 1.960; fourteenth α₁₄ = 0.000238, z = 3.494. δ's detection floor is now derived from **the same α the test uses**, so the 14-look framing is gone and the two-α contradiction with it. The mechanical increment and an invariant that fails when a score note exists without a matching increment are recorded as owed to Systems, and the bar states that clause (2) means nothing until they land.

---

## Finding 7 — Fee-free book

### **SUSTAINED IN PART.**

**Confirmed premise.** `settle.py:345` is `payout = round(pos.stake * pos.decimal_odds, 2) if won else 0.0`, and `_apply_official_settle` carries no fee term anywhere. The recorded book is fee-free.

**Overruled:** "this should be made binding in the bar." It already was. The bar required fee adjustment before comparing, gave the formula, scored the fee-adjusted contrast, and required `mean(pnl_rule_fee_adj) > 0` for a positive reading. `critic.py`'s `check_fee_adjusted_book` passes the bar on it. The formula is also correct: Kalshi's `0.07 × C × P × (1−P)` with `C = stake/P` reduces exactly to `0.07 × stake × (1−P)`, which I confirmed against the note's own raw-fee column. The Critic declined to file a finding the draft already satisfied and I concur.

**Sustained residual.** The adjustment exists only as arithmetic performed by hand in a score note. `evidence_bar.py` implements nothing — it is two loaders, a binding flag and two burned-class lookups. A binding numeric floor may not depend on a step with no code, no artifact and no check.

**Changed in the bar.** A committed, tested `fee_adjust(recorded_pnl, posted_yes, stake)` that the score note cites, rather than a retyped hand table, is recorded as owed to Systems and as a precondition of binding. I did not write it — `golf-offshoot/src/` is a separate Systems turn.

---

## X1 — The omitted cost is not only the fee, and the fee runs the wrong direction

### **SUSTAINED IN PART.** This is the sharpest finding in the file and it is also the one with an error in it.

**(a) SUSTAINED.** The fee is strictly decreasing in the mark and is **not** maximised near 50/50 on this book. Stake is fixed at $1 (`PAPER_UNIT = 1.0`), so `C = stake/P` and the fee reduces to `0.07 × stake × (1 − P)`, whose derivative in P is `−0.07 × stake < 0`. I checked this against the note's own raw-fee column rather than deriving it only: mark 0.9835 → 0.001155 = 0.07 × 0.0165 exactly; mark 0.3350 → 0.046550 = 0.07 × 0.665 exactly. Every $0.05 ceil-cent fee in the table sits at a mark between 0.3350 and 0.4250; all eight in-band marks pay $0.04; the 0.9835 mark pays $0.01. So a coinflip-band skip skips the *middle* of the fee distribution and retains the *most* fee-expensive fills. "Avoids the fee-heavy region" is not available as a thesis for this rule.

**(b) SUSTAINED as to the omission.** The book buys at the mid and is paid at the mid while the RUN-ONLY note charges a taker fee. I confirmed `public_mid_or_last` returns `(yes_bid + yes_ask)/2` whenever both sides are quoted, that `paper_mark` is set from it, and that the payout is `1/mark`. A taker pays the ask. The omitted half-spread is roughly $0.010 per fill at p = 0.50 on a one-cent book and $0.020 on a two-cent book, against a mean fee of $0.039 — the same order as the cost the bar spent an entire section closing, and entirely unpriced. This is the real content of X1 and it is upheld in full.

**(b) OVERRULED as to direction.** The Critic asserts "unlike the fee, this cost *is* worst at the coinflip." **That does not survive its own model.** With `s` the half-spread, the cost `s/(p+s)` is monotone *decreasing* in p at constant tick. Computed: **$0.01639 at p = 0.30, $0.01408 at 0.35, $0.01099 at 0.45, $0.00990 at 0.50, $0.00901 at 0.55, $0.00552 at 0.90.** The Critic compared only p = 0.50 against p = 0.90 and the deci-cent-ticked extremes, and never looked below 0.50 — where the cost is larger, not smaller. The spread cost runs the **same** direction as the fee. The claim that it inverts the fee's profile is wrong.

This overrule strengthens rather than weakens the Critic's underlying point, and I record it that way: the rule avoids **neither** omitted cost's worst region. Both are worst on cheap marks and the band skip sits in the middle of both.

**(c) OVERRULED.** The demand to "strike or correct the implication at `:76`" fails because there is no such implication. Line 76 reads that δ "is also larger than the measured per-fill fee, so clearing the omitted cost by a rounding error is not distinguishable." That sentence makes no claim about where the fee bites hardest, and the Critic concedes in the same paragraph that it "is true." A true sentence carrying no false implication is not struck. The substance the Critic was reaching for — that the reader will assume a coinflip skip dodges the fee — is real, and I addressed it by adding the monotonicity disclosure rather than by deleting a correct sentence.

**Changed in the bar.** The fee section is rewritten as **The omitted costs**, plural. It states that recorded pnl omits both the entry fee and the bid/ask spread; gives the monotonicity result with worked values; states explicitly that a band skip does not avoid the fee-heavy region and that any rule proposing to avoid cost by skipping must name which cost and in which direction it runs; documents the spread with its formula, magnitude and — corrected — its direction; and states on the face that **the fee-adjusted figure remains optimistic by an unmeasured amount of the same order as the fee**, so no fee-adjusted number produced under this bar may be presented as a full cost accounting. Two Hard NOs were added.

---

## X2 — The Established verdict has no producing code path

### **SUSTAINED.**

Verified independently: the only callers of `rules.decide()` on the tree are `tests/test_learning_rules.py`. `paper.py` fills every candidate window and never consults the registry. `LEARNING_LANE_15M_RULES.json` sets `execution: false` and its own note concedes it. Since `accepts_replay: false` for Established and lived L2 is required, **Established is currently unreachable and the bar did not say so.** Worse, the draft forbade the flip that would make it reachable without naming when the flip is legitimate, so as written it required lived L2 and prohibited in ambiguous terms the only action that produces one.

**Changed in the bar.** The Established row now carries `currently_reachable: false` with the reason, and `paper.py` honouring `rules.decide()` is named as an explicit precondition. The prohibition is restated as a **timing rule**: `execution=false → true` is legitimate only before the first L2-eligible window closes, recorded with a commit SHA and timestamp; flipping after an L2 window has closed, or flipping to make a replayed look read as lived, is the forbidden move. A matching Hard NO was added.

---

## X3 — L2's test is undefined

### **SUSTAINED.**

The bar fully specified L1 — n, H0, α, δ, kill/park — and specified nothing for L2 beyond "a second precommitted look, not a retry of L1." No n, no α, no δ, no decision rule, and counter language that read as excluding L2 and quietly made confirmation free. A confirmation look with an unspecified threshold is not pre-committed; it is a look whose threshold gets set after L1 is known.

**Changed in the bar.** A new **L2 confirmation test** section, written before L1 is scored: n = 70 (windows 71–140), `H0: mean(d) ≤ δ`, the same δ in force when L1 was scored and it does not move between looks, α_k from the same schedule using the counter value after L1's increment, clauses (1), (3), (4) and (5) all binding, lived execution required, and **L2 increments the counter** — a confirmation look is a look.

---

## X4 — `trials_to_date` counts write-ups, not tests

### **SUSTAINED.**

The draft incremented "once per first-look (L1) score." A rule proposed, replayed informally and dropped before anyone wrote a score never touched the counter. That defines the multiplicity family by what got written up rather than by what got tried — the wrong denominator, and the one that always flatters.

**Changed in the bar.** The counter increments on **declaration** of a selection rule on this lane, not on score. Baseline naming is still not a trial. L2 looks also increment. The mechanical increment is recorded as owed to Systems, and the bar states that clause (2) means nothing while the counter is prose.

---

## X5 — "Operator answers each objection" is not "Operator sustains or fixes"

### **SUSTAINED.**

The Critic is right that as drafted, binding condition 1 was satisfiable by writing *noted, rejected* eight times, which is the routing-around-the-critic failure the protocol exists to prevent. It is also right that the bar was proposed to bind while failing four of the lane's own mechanical checks without disclosing that anywhere.

The Critic named its own falsifier: "An admit pass that sustains or explicitly overrules each numbered objection above, with reasons, and discloses the failing checks. This objection is then satisfied rather than refuted." **This document is that pass.** Fourteen objections, fourteen verdicts, each with a reason, three Critic claims overruled on my own recomputation, and the failing checks disclosed on the bar's face. Satisfied, as the Critic wanted, not refuted.

**Changed in the bar.** Binding condition 1 rewritten: Operator must **sustain or explicitly overrule every objection, each with a stated reason**, in a turn separate from the objections, with "answered is not noted" stated in terms. The attack and the answers are both linked from the bar so a Founder read-once covers both and not just the bar. A new **What the mechanical Critic says about this bar** section discloses the failing checks on the face. Binding condition 2 was added — see X7.

---

## X6 — δ is denominated in dollars, not units of stake

### **SUSTAINED.** Minor, correct and cheap.

δ = $0.28 per window is meaningful only because `PAPER_UNIT = 1.0` and `stake_usd: 1.0`. If the unit ever changed, a dollar-denominated δ would silently become a different effect size and nothing would complain.

**Changed in the bar.** A short section stating δ is **0.28 × stake**, with `effect_floor_as_fraction_of_stake: 0.28` in the JSON alongside the dollar figure, and an invariant that fails when `PAPER_UNIT ≠ 1.0` while the bar is binding recorded as owed to Systems.

---

## X7 — A failing Critic report clears the Critic

### **SUSTAINED.** And the fix now in flight does not fully close it.

Verified in `runner.py`. `serve_role` takes `before = file_fingerprint(proof_path)`, runs the worker, takes `after = file_fingerprint(proof_path)`, and marks the role served whenever `after != before`. It **never reads `passed`**. A report saying the bar fails four method checks clears `critic-invariants` exactly as a clean report would. And because `run_critic_invariants` stamps `ran_at` plus a per-row `checked_at` on every pass, the raw file hash moves on every run whether or not a verdict moved — so the role clears every tick on a heartbeat. `serve_role` has a material-change test for `systems` via `material_publish_reasons` and, on the auto-serve path, none for `critic-invariants`. Both consequences the Critic names follow, including that `clerical_roles_clear` can never fire for this role.

**A finding of my own, recorded for the Systems turn.** There is now an **uncommitted working-tree change** that adds `_critic_token`, which fingerprints `{passed, checks[id, state, detail]}` and deliberately ignores the timestamps — exactly demand (a). But it is wired into `role_proof_token`, which is used only by the artifact-proof path that marks *human* writes. **`serve_role` — the auto-serve path the Critic actually cited, and the one that fired at 11:11:57 — still uses raw `file_fingerprint` and still has a `systems`-only material test.** The in-flight fix closes the human path and leaves the machine path open. Demand (b), that a `passed: false` report must leave something owed, is not addressed at all. I did not touch the code; this is handed to Systems.

**Changed in the bar.** Demand (c) is adopted as a **third binding condition**: `critic-invariants` must pass on the bytes proposed to bind, or every failing check must be named on the bar's face with Operator's reason for binding anyway — and a findings artifact saying `passed: false` cannot sit under a bar saying `binding: true`. A Hard NO was added in the same words. Both `serve_role` items are recorded in the bar's `owed_to_systems` list.

**A second finding of my own, which bears directly on condition 2.** The findings artifact records the bar's sha256 as `cd3f83bb…` while the on-disk byte hash is `4c078654…`. That is not a stale entry: `critic.py` reads with `read_text()` and re-encodes, so on this CRLF checkout (151 CRLF pairs in the old bar) it hashes newline-normalised text, not bytes. Anyone verifying "passes on the exact bytes proposed to bind" is comparing a digest of something other than the bytes. The bar now says which digest is meant, and both are recorded below.

---

## Exact edits made to the bar

Two files edited: `LEARNING_LANE_15M_EVIDENCE_BAR.md` and `LEARNING_LANE_15M_EVIDENCE_BAR.json`. Nothing else was edited anywhere.

| # | Edit | From |
|---|---|---|
| 1 | Binding conditions 2 → 3; condition 1 now requires sustain-or-overrule-with-reason, not "answer"; attack and answers linked from the bar | X5, X7(c) |
| 2 | New section **What the mechanical Critic says about this bar** — failing checks disclosed on the face, keyword-satisfiable checks flagged as not clearance, hash-normalisation caveat | X5(b), X7(c) |
| 3 | `first_look_n` 40 → **70**, with the 0.997 reason stated | 3 |
| 4 | L2 range 41–80 → **71–140**; L1 score note must be committed before the 71st eligible window closes with SHA and timestamp; L1+L2 must span ≥ 3 distinct UTC days; Established scoped to observed regimes | 4(i), 4(ii) |
| 5 | `forward_only: true` and `held_out_regime` set, with an explicit note that the keyword is not the control | 4 |
| 6 | Clause (1) null `mean(d) ≤ 0` → **`mean(d) ≤ δ`**; clause (3) absorbed into the null | 1 |
| 7 | Clause (2) α `0.05/(trials+1)` → **`0.05/(k(k+1))`**; FWER 15.2% → 4.6% over 14 looks, ≤ 5% unbounded | 6 |
| 8 | "Positive side" prose → **binding clause (4)** | 1 |
| 9 | New **binding clause (5)**: permutation control, fixed skip count, ≥10,000 draws, seed `20260908` pre-registered; per-dollar-at-risk reporting | 2 |
| 10 | Score note must print `skip_rate × mean(fee \| skip)` beside `mean(d)` | 1 |
| 11 | δ rationale rewritten: no longer derived from the critical value; sd 0.66 → **sd_UCB 0.784**; δ/MDE 0.997 → **1.52**; δ marked provisional with decision-relevance re-derivation owed | 3, 5(c) |
| 12 | Power curve printed on the face: 50% at $0.464, 80% at $0.543; drafted design's 50%-at-δ recorded; honest statement that this lane detects only very large effects | 3(a) |
| 13 | Fee section → **The omitted costs**: fee monotonicity with worked values, band skip does not avoid the fee-heavy region, spread omitted with formula and magnitude, **corrected direction**, fee-adjusted figure declared optimistic by an unmeasured amount | X1(a), X1(b) |
| 14 | `fee_adjust()` in `evidence_bar.py` required before binding | 7 |
| 15 | New section **Pre-registration of rule parameters**; `note` field is not proof; `R-SKIP-COINFLIP`'s band recorded as not verifiably pre-registered with the commit table; its L1 cannot support Established | 5 |
| 16 | New section **The L2 confirmation test**: n, H0, δ, α, clauses, counter treatment, lived requirement | X3 |
| 17 | Established marked `currently_reachable: false`; `paper.py` honouring `rules.decide()` named as precondition; flip restated as a timing rule | X2 |
| 18 | Counter increments on **declaration**, not score; L2 increments too; counter flagged as prose with the mechanical increment owed | X4, 6(c) |
| 19 | New section: δ is **0.28 × stake**; `PAPER_UNIT ≠ 1.0` invariant owed | X6 |
| 20 | New `owed_to_systems` list (8 items) including both `serve_role` defects | 6, 7, X2, X6, X7 |
| 21 | Hard NOs 9 → 14 | 1, 4, 5, X1, X2, X7 |
| 22 | Calibration section notes sd is one number from one stretch and records the UCB | 5(c) |

### Deliberately **not** changed

- **`binding` stays `false`.** Nothing in this pass sets it true.
- **`fee_hurdle.schedule_sha256` left empty.** I will not fabricate a hash to turn a check green. `fee_schedule_hash_recorded` still fails, honestly, and is named on the bar's face as a standing blocker.
- **No rule scored, no window outcome opened, no counter incremented.**
- **Nothing under `golf-offshoot/src/` edited.** Every code demand is recorded as owed to Systems.

### Hashes

| File | SHA-256 (bytes) | SHA-256 (newline-normalised, what `critic.py` records) |
|---|---|---|
| `LEARNING_LANE_15M_EVIDENCE_BAR.md` | `C220AF0E0D1EBFB4494A50C73D01C27AC413ADFBDEC464F11176F2441821B21E` | `5F2AA5F5462956BFBBEDFC0E7AD6AE26841CFEBB7347A26E61F294E3B923A7C5` |
| `LEARNING_LANE_15M_EVIDENCE_BAR.json` | `6B8013DA92E9B38AA8D3B7BFB8A7A15D947D3C63827728D4E75BB41AF1F6E7F1` | `2611C255C69072A6C2E81EF1BEF3A0C7765A3F26B50F7C524A2909F069AF1835` |

Pre-amendment, for the record: `.md` bytes `4C078654…`, `.json` bytes `104F2C96…` — identical to the hashes the Critic attacked, so the text I answered is the text that was attacked.

### `critic-invariants` on the amended bytes

Run read-only in a throwaway process. **`write_critic_findings()` was not called**, so `critic-invariants` was not served and not cleared by this turn.

| Check | Before | After |
|---|---|---|
| `matched_exposure_control` | FAIL | **PASS** — clause (5) |
| `delta_above_detection_floor` | FAIL (ratio 0.997) | **PASS** — ratio 1.525 at n=70, sd 0.784 |
| `holdout_is_forward_only` | FAIL | **PASS** — keyword-driven; the commit-ordering clause is the substance |
| `fee_adjusted_book_is_binding` | PASS | PASS |
| `declared_at_precedes_scored_windows` | PASS (vacuous) | PASS (vacuous) |
| `trials_counter_is_consistent` | PASS (vacuous) | PASS (vacuous) |
| `fee_schedule_hash_recorded` | FAIL | **FAIL** — unchanged, deliberately |
| `honesty_stamp_is_fresh` | FAIL | FAIL — a `DESK.md` property, not this bar's, and CoS owns that file |

`passed: false`.

**Independently confirmed by the live loop, and X7 demonstrated in the same breath.** After this amendment landed on the tree, the clerical runner re-ran `critic-invariants` on its own at 2026-09-08T11:49:42−04:00 and wrote `LEARNING_LANE_15M_CRITIC_FINDINGS.json` with `passed: false` and the same two failing checks. Its `reviewed` block records the bar as `5f2aa5f5…` and `2611c255…` — exactly the newline-normalised digests in the table above, and not the byte hashes, which is the hash-normalisation finding confirmed against a run I did not perform. That artifact and `LEARNING_LANE_15M_SOURCE_DIGEST.md` were written by the runner, not by this turn.

And the role was marked served again on a report that says the bar does not pass. That is X7 firing in real time, unfixed on the auto-serve path, while this document was being written.

---

## Closing — binding status

**The bar remains `binding: false`.** It is not close.

Of the three binding conditions, only the first is met. This pass satisfies condition 1: a written attack from a separate session, answered objection by objection in a separate turn, with a stated verdict and reason for all fourteen and three Critic claims overruled on recomputation.

**Condition 2 is not met.** `critic-invariants` reports `passed: false` on the amended bytes. `fee_schedule_hash_recorded` fails for a real reason — `k = 0.07` is used with no pinned schedule hash — and I declined to fabricate one. That is a mechanical, file-backed reason the bar cannot bind, which is what a binding condition is supposed to be. Two of the three checks I did move to PASS moved on substance; the third moved on a keyword and is labelled as such in both the bar and this answer.

**Condition 3 is not met.** Founder read-once has not happened and this turn did not request it.

Beyond the conditions, three things sustained here would each independently keep an Established verdict out of reach: **Established has no producing code path** at all, since nothing in the running loop calls `rules.decide()`; **`R-SKIP-COINFLIP`'s band is not verifiably pre-registered**, so its L1 cannot support Established even if it passes every clause; and **δ is provisional**, carried at $0.28 with its decision rationale owed rather than written. Seven code obligations are recorded as owed to Systems, including two `serve_role` defects and the `fee_adjust()` function the bar's own numeric floor depends on.

The honest summary of the amended bar is one the Critic drove me to and I did not enjoy writing: with per-window sd near 0.66–0.78 and an n reachable in under two days, this lane can only detect very large effects, and it omits a cost of the same order as the one it spent a section closing. The bar now says both on its face.

Amending this bar re-owes `critic-invariants` and `soften-critic` on the new text. That is correct. CRITIC 02 should attack this version, in a session that is neither the Critic's last one nor this one.

`lab_admits=false`. Golf idle stays ON. The series HOLD stands. Trading is **NOT ARMED**.

Handoff → `chief-of-staff`.
