# Soften Critic — attack on the 15m evidence bar (CRITIC 01)

**Role:** Soften Critic · **Date:** 2026-09-08 · **Session:** separate from the session that drafted the bar (`11e4e3c`, 2026-09-08 08:34:40 −0400) and separate from the session that will answer.

**This is an attack, not a verdict.** Operator answers each objection separately, in the admit pass. Nothing here is a Soften, an ADMIT, a park, a score, or a proposal. Trading is **NOT ARMED** and nothing in this file arms it.

**Artifacts attacked, by SHA-256 of the exact bytes on disk:**

| File | SHA-256 |
|---|---|
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR.md` | `4C078654E709D9AFC2AD080D693D1BD4BD23317BD0DFB2D23FF3A9F849727A93` |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR.json` | `104F2C9663E52682947FA766CB4B4DAEFF1706C26DA3FB873D0C2565EC0B3417` |
| `golf-offshoot/docs/LEARNING_LANE_15M_RULES.json` | `8702C4B9F5804AB3285C5A6337614437C56DB5F58D6C63C4996F31736AADE081` |
| `golf-offshoot/src/golf_offshoot/learning_lane_15m/evidence_bar.py` | `CE2C1CE09391810D59EC220D98CD634B9866A6B23ABDAE234B6A1875E9C985BC` |

Hashes recomputed at the end of the attack and unchanged. Citations below are `file:line` against those bytes.

---

## Posture of this attack

**I did not open a single window outcome file** — not post-declaration, not pre-declaration. No `paper/*.json`, no `settlements/*.json`, no `latest/journal.json`. Every number below is derived from one of four places: the drafted text, the code, the already-committed RUN-ONLY note that the bar names as its own fee source (`LEARNING_LANE_15M_EVIDENCE_BAR.md:17`), or the lane's own mechanical checker run read-only.

I ran `run_critic_invariants()` in a throwaway process to check my own arithmetic. **I did not call `write_critic_findings()`**, and I did not serve or clear `critic-invariants`. `LEARNING_LANE_15M_CRITIC_FINDINGS.json` did appear on the tree at **2026-09-08T11:11:57−04:00** while I was writing — the clerical runner wrote it (`runner.py:370-373`, `runner.py:442`) once the import fault described at the end of this file was corrected. Its failing list is identical to the one I had already computed by hand. See **X7**, which is about what that artifact now does to the owed list.

This file is not one of `critic.py`'s `WATCHED` artifacts (`critic.py:63-69`), so writing it does not disturb the hash-keyed owed logic.

I did not edit the bar, `DESK.md`, or `AGENT_LEAVE_OFF.md`. I did not commit or push. I did not run the digest generator.

---

## The lane's own mechanical Critic already fails this bar

Before my objections: `critic.py` is the mechanical half of this role, and it is on the clerical whitelist (`runner.py:78`). Run against the exact bytes above, it reports **four failing method checks**. I computed these by hand first; the runner then wrote the same verdicts to `LEARNING_LANE_15M_CRITIC_FINDINGS.json` at 11:11:57 EDT, so this table is now an artifact on disk and not only my reading:

| Check | State | What it says |
|---|---|---|
| `matched_exposure_control` | **FAIL** | contrast is `d_i = pnl_rule_fee_adj_i - pnl_baseline_fee_adj_i` with `skip_contributes=0`; "the comparison rewards not playing rather than selecting" |
| `delta_above_detection_floor` | **FAIL** | δ 0.28 vs MDE 0.2807 at n=40, **ratio 0.997** — "the bar can only see its own detection floor" |
| `holdout_is_forward_only` | **FAIL** | held-out set is an index slice, and no `forward_only` key is declared |
| `fee_adjusted_book_is_binding` | PASS | the scored contrast is fee-adjusted |
| `declared_at_precedes_scored_windows` | PASS | (vacuous — no rule carries `scored_windows`) |
| `trials_counter_is_consistent` | PASS | (vacuous — `trials_to_date=0` covers 0 rules looked at) |
| `fee_schedule_hash_recorded` | **FAIL** | no sha256 pinned for the Kalshi schedule; `k=0.07` "is being used on habit" |
| `honesty_stamp_is_fresh` | FAIL | desk stamp stale; not a property of the bar, so I do not file on it |

This is not my opinion. It is the tree's own ratchet, failing on the text that is being proposed to bind. **The bar does not disclose this anywhere** — `LEARNING_LANE_15M_EVIDENCE_BAR.md:1-17` names two binding conditions and neither of them is "passes `critic-invariants`." See finding **X5**.

---

## Finding 1 — Rigged comparison

> *"When fill-all has negative EV, betting less automatically beats it. Skipping gets rewarded for not playing rather than for selecting."*

### **AMENDED** — the stated null is upheld; the magnitude claim is rejected.

**Upheld half.** Clause 1 is `H0: mean(d) ≤ 0` (`LEARNING_LANE_15M_EVIDENCE_BAR.md:72`, `LEARNING_LANE_15M_EVIDENCE_BAR.json:56`). Under the bar's own cost model that null is **known false before any data are collected**:

- The book fills at the posted mark and pays `1/mark`: `decimal = (1.0 / mark)` at `kalshi_15m.py:298`, consumed at `paper.py:204`, paid at `settle.py:345` as `payout = round(pos.stake * pos.decimal_odds, 2)`. A fill is therefore EV-zero *pre-fee* at a calibrated mark.
- The fee is strictly positive on every fill. The RUN-ONLY note's own falsifier F2 (`LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md:89`) records "No fill rounded to $0.00; minimum ceil-cent fee is $0.01."
- Therefore `E[d] > 0` for **any** nonzero skip rate, with no selection skill present at all. A one-sided test against `mean(d) ≤ 0` is a test whose null is arithmetically false.

**Rejected half.** "Betting less *automatically beats it*" does not survive contact with δ. The mechanical fee-avoidance component is computable from the bar's own numbers. Every mark strictly inside (0.45, 0.55) yields `0.07 × 1 × (1 − P) ∈ (0.0315, 0.0385)`, which ceils to **$0.04** without exception (`LEARNING_LANE_15M_EVIDENCE_BAR.md:64`). At the bar's own stated pre-declaration skip rate of 22/56 = 0.393 (`:137`), abstention alone earns

`0.393 × $0.04 ≈ $0.016 per window`

against a floor of **δ = $0.28** (`:74`). Free abstention buys **5.6% of the bar**. It cannot clear it. The rigging is real in the null statement and inert in the decision.

**Concrete change demanded.** Restate clause 1 as `H0: mean(d) ≤ δ` — a one-sided paired t-test *against the floor*, not against zero — so the p-value the score note prints is decision-relevant rather than a test of arithmetic everyone already knows the answer to. Then clause 3 stops being a second, separately-checked hurdle and becomes the null itself. Additionally, require the score note to print `skip_rate × mean(fee | skip)` beside `mean(d)`, so a reader can see how much of the contrast is mechanical.

Separately: the "Positive side" clause at `:80` is conditional prose — it binds only "a result that wants to be read as positive expectancy." It is not one of the numbered clauses, it is not referenced by the kill/park test at `:78`, and it is not required for the **Admissible** verdict at `:27`. Promote it to numbered clause **(4)**, binding for Established.

**What would prove me wrong.** Evidence that the paper mark sits systematically *below* the true settlement probability — i.e. that the fill-all baseline is EV-positive gross of fees. Then `H0: mean(d) ≤ 0` is not known-false and this objection dies.

---

## Finding 2 — No matched-exposure control

> *"Comparison must be per-bet or matched-exposure, or the result measures volume, not skill."*

### **UPHELD.**

The contrast is matched on *windows* and unmatched on *exposure*. A skip "contributes **0** pnl and **0** fee" (`LEARNING_LANE_15M_EVIDENCE_BAR.md:57`, `LEARNING_LANE_15M_EVIDENCE_BAR.json:54`), so the two arms deploy different capital: the rule arm risks `(1 − skip_rate) × n × $1` against the baseline's `n × $1`. Nothing in `:50-80` or `LEARNING_LANE_15M_EVIDENCE_BAR.json:52-61` normalizes for that, and no `matched_exposure` or per-bet key exists.

The bar states the question it means to ask — "The contrast lives in the skips" (`:58`) — and then does not build the control that answers it. `critic.py:208-236` already fails the bar on exactly this and words it the same way.

**Concrete change demanded.** Add a required control arm: a **permutation null that holds the number of skips fixed and reassigns which windows are skipped** — ≥10,000 draws, seed pre-registered in this document — and require the observed `mean(d)` to exceed the `1 − α` quantile of that null in addition to clauses (1)–(3). That converts the question from *"did abstaining help?"* to *"did **this** abstention rule beat abstaining at the same rate?"*, which is the question the bar says it is asking. It is deterministic given the seed, adds no code to the running loop, and needs no new data — it clears the CoS RUN-ONLY routing test at `PROTOCOL.md:155-160` on all four counts.

**What would prove me wrong.** A skip rate of zero (the arms are then identical), or an amendment normalizing the contrast per dollar at risk so the arms are exposure-equal by construction. Either kills this objection.

---

## Finding 3 — Power

> *"The n required is far larger than the bar states. Thirteen eligible windows is nothing."*

### **AMENDED** — the premise as written is false; a sharper power objection is upheld in its place.

**Rejected as stated.** "Thirteen eligible windows" appears nowhere in the draft. The bar says **n = 40** in four places: `LEARNING_LANE_15M_EVIDENCE_BAR.md:38`, `:40`, `:70`, and `LEARNING_LANE_15M_EVIDENCE_BAR.json:44`. It also forbids looking earlier — "Do not compute the test at n = 1, 10, 20, or 39" (`:41`). Whoever reconstructed this finding was not reading the bar. I reject it in that form.

**Upheld in this form**, from the bar's own numbers at `:76` (sd ≈ 0.66, SE₄₀ ≈ 0.104):

1. **δ is the rejection threshold wearing an effect floor's clothes.** `2.69 × SE₄₀ = $0.2807`. δ = $0.28. The ratio is **0.997**. Clause 3 is not an independent floor; it is clause 1's critical value relabeled, and it therefore carries no information about whether an effect of that size is worth acting on. `critic.py:163-206` computes the identical ratio and fails the bar on it.
2. **The bar is coin-flip powered at its own floor.** When the true effect equals δ, the test rejects with probability ≈ **50%**. A bar that misses half of the effects it declares material is not a bar, it is a coin.
3. **80% power at n = 40 arrives only at $0.37 per window** — `(2.690 + 0.842) × 0.104 = $0.369`, i.e. **37% of a $1 stake, every window**. To get 80% power *at δ* the bar needs **n ≈ 70**, not 40.

**Concrete change demanded.** (a) Print the power curve on the bar's face: "at n = 40 this bar has ~50% power at δ and ~80% power only at $0.37/window." A bar that hides its own power is a bar that will be read as stronger than it is. (b) Derive δ from what size of edge is worth acting on, and if that number coincides with the critical value, say so explicitly instead of presenting the coincidence as a rationale. (c) If δ is to remain the decision-relevant floor, set n = 70.

**What would prove me wrong.** A power calculation in the bar showing ≥80% power at δ = 0.28 with sd = 0.66 at n = 40. It cannot exist: `0.28 / 0.104 = 2.68 < 2.690 + 0.842`. If sd is revised downward on more data, recompute and this objection weakens accordingly.

---

## Finding 4 — Holdout is ineffective

> *"A holdout carved from the same period and regime is not out-of-sample. OOS must be forward-only and pre-registered."*

### **AMENDED** — the factual premise is wrong; two real residuals survive.

**Rejected as stated.** L2 is **not** carved from the same period. It is "eligible windows 41 through 80 **after `declared_at`**" (`LEARNING_LANE_15M_EVIDENCE_BAR.md:42`, `LEARNING_LANE_15M_EVIDENCE_BAR.json:47`), strictly forward of L1, which is itself strictly forward of declaration. `rules.py:40-45` enforces this in code — `window_is_oos` returns `closed > declared`, strict. And it is pre-registered: it is written into this draft before any score exists. The "index slice" framing in `critic.py:275-298` is a *keyword* check that passes the moment someone adds `"forward_only": true` to the JSON; it does not test the substance. Do not let that check clear this finding either.

**Residual (i) — one regime, and less than a day of it.** By the bar's own arithmetic at `:73` (~96 windows/day, a 40-window look resolving in ~10 hours), L1 + L2 span **≈20 hours**. The δ calibration set spans the ~14 hours immediately before (`:131`, `071545` → `080545`). All three sets — calibration, first look, confirmation — sit inside one contiguous ~34-hour stretch of BTC tape. An **Established** verdict would rest on less than a day and would have seen exactly one regime.

**Residual (ii) — the holdout is prose.** "The session that scores L1 must not read L2 marks, fills, or pnl" (`:42`) is an honor-system reading restriction on files sitting in the same directory, which by L1-scoring time are likely already settled on disk. The bar mechanically enforces its burned-class list — `evidence_bar.py:46-61` loads JSON and matches aliases — and leaves its holdout to a sentence. `PROTOCOL.md:112`: "A failing invariant is never satisfied by prose — it passes because a file says so, or it does not pass." The bar's own `:107` says the same thing about `failure_mode_log.md`.

**Concrete change demanded.** (a) Require the L1 score note to be **committed before the 41st eligible window closes**, and record that commit SHA and timestamp in the note. That is hash-provable, it is the only version of this rule that is not self-certification, and it belongs in `invariants.py` as a check. (b) Require L1 and L2 together to span at least a stated number of distinct UTC days, **or** state on the bar's face that any Established verdict is scoped to a sub-day regime and does not generalize past it.

**What would prove me wrong.** An invariant that checks the L1-note-before-L2-close ordering, plus a stated calendar separation between L1 and L2. With both, this objection dies.

---

## Finding 5 — Delta is an in-sample free parameter

> *"The coinflip band was chosen after seeing the data, which inflates significance. Pre-commit it or penalize it."*

### **AMENDED** — wrong about δ, right about the band, and the band is the parameter that matters.

**Rejected as applied to δ.** δ is a deterministic function of (sd, n, α) and not of the observed mean: `:76` derives it as `2.69 × SE₄₀`. The bar discloses its calibration set in full (`:129-137`), names the two fields it read (`:133`), states which windows it did not open (`:135`), and volunteers that the in-sample mean contrast was inspected only to confirm δ was **not** fit so history would pass (`:137`). That is more disclosure than the finding assumes, and I will not pretend otherwise.

**Upheld as applied to the band (0.45, 0.55)** — `rules.py:63` — which is the free parameter that actually selects windows.

`LEARNING_LANE_15M_RULES.json:33` asserts: *"Band chosen before looking at overnight marks."* That is a self-certification with nothing behind it, and the commit record contradicts the spirit of it:

| Commit | Time (EDT) | What landed |
|---|---|---|
| `2fea8d8` | 2026-09-07 **21:49:37** | the RUN-ONLY fee note — including a full table of **mark and recorded pnl for 24 lineage-A windows** (`LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md:43-67`) |
| `0786279` | 2026-09-08 **05:56:51** | the rule registry — first appearance of the (0.45, 0.55) band, 51 seconds after its own `declared_at` |

**Eight hours and seven minutes** separate them. Eight of the 24 rows in that committed table fall strictly inside (0.45, 0.55): marks 0.4650, 0.5150, 0.4950, 0.5150, 0.4850, 0.4550, 0.4750, 0.4550. The band was therefore written down by a crew that had already published, on this tree, the exact marks the band selects on and what each of them paid. "Chosen before looking" may be true of the author's intent; it is not true of the information available, and the bar accepts the claim without asking for anything.

For completeness, and clearly labeled: those eight rows sum to +$2.51 recorded pnl and +$2.19 after their (uniformly $0.04) fees, so skipping them would have subtracted $2.19 across the 24 published windows — a contrast of **−$0.091 per window** against a floor of +$0.28. That is pre-declaration history, explicitly not OOS under `rules.py:40-45`, and n = 8 in-band is far too small to say anything about whether the rule works. **I am not scoring, and this is not evidence for or against `R-SKIP-COINFLIP`.** I cite it for one purpose: to show the data was there, published, and quantitatively informative about this band before the band was dated.

**Concrete change demanded.** (a) The bar must require a **verifiable pre-registration** for any selection rule's parameters — the commit SHA and timestamp of the registry entry, plus a statement that the timestamp predates the earliest window whose mark informed the parameter — and must stop accepting a `note` field's own claim as proof. (b) Because that condition demonstrably fails for this band, the bar must either treat `R-SKIP-COINFLIP`'s L1 as calibration rather than a clean first look, **or** state on its face that this rule's band is not verifiably pre-registered and that L1 therefore cannot support **Established** even if it passes. (c) Set δ from an upper confidence bound on sd, not the point estimate — δ is linear in sd, and sd = 0.66 is one number from 56 windows in one 14-hour stretch.

**What would prove me wrong.** Produce a commit, desk line, or dated artifact predating 2026-09-07 21:49:37 EDT that names the (0.45, 0.55) band. This objection then dies in full, and I would want it recorded that it died.

---

## Finding 6 — Multiple testing uncorrected

> *"Many rules and bands tested against one book."*

### **AMENDED** — "uncorrected" is false; the correction that exists does not control anything.

**Rejected as stated.** Clause 2 exists: `α = 0.05 / (trials_to_date + 1)` (`LEARNING_LANE_15M_EVIDENCE_BAR.md:73`, `LEARNING_LANE_15M_EVIDENCE_BAR.json:57`). The draft explicitly says "A bar with no multiplicity term is incomplete."

**Upheld in three sharper forms.**

1. **On the only trial this bar currently governs, the correction is numerically inert.** `LEARNING_LANE_15M_RULES.json:9` sets `trials_to_date: 0`. The first look therefore gets `α = 0.05/1 = 0.05` — identical to the naive level the bar says it is replacing ("Scarcity is being removed; this is the replacement", `:73`). `R-SKIP-COINFLIP` is the first look.
2. **The scheme does not control family-wise error.** `Σ 0.05/k` diverges. Over the bar's own 14-look week, `1 − Π_{k=1..14}(1 − 0.05/k) ≈ **15.2%**`, not 5%. The bar names the hazard correctly and then does not fix it.
3. **The bar states two different α's one line apart.** Clause 2 yields α = 0.05 at `trials_to_date = 0` — threshold `1.645 × 0.104 = $0.17`. δ at `:76` is derived at α = 0.05/14 — threshold `2.690 × 0.104 = $0.28`. Both are presented as the bar. They are not the same bar.

Also: nothing increments the counter. `evidence_bar.py:28-70` loads the bar and the burned classes and never reads `trials_to_date`; `rules.py:21-26` only loads the registry. The only references on the tree are docs and tests. `critic.py:326-345` checks the counter against rules carrying `scored_windows` or `last_look_at` — fields no code writes — so it passes vacuously (`trials_to_date=0 covers 0 rule(s)`). The bar's `:107` says prose is not enforceable; its multiplicity counter is prose.

**Concrete change demanded.** (a) Use a weight scheme whose weights sum to 1 — `α_k = 0.05 / (k(k+1))` or `α_k = 0.05 × 2^(−k)` — so FWER ≤ 0.05 over an unbounded number of looks. (b) Derive δ from the *same* α the test uses, or drop the 14-look framing from `:76`. (c) Put the increment in code and add an invariant that fails when a score note exists without a matching increment.

**What would prove me wrong.** Show that `1 − Π_{k=1..14}(1 − 0.05/k) ≤ 0.05`, or name the standard FWER procedure that `α_k = 0.05/k` implements. Neither exists.

---

## Finding 7 — Fee-free book

> *"`settle.py` pays `stake × decimal_odds` with no fee term… A rule that only wins gross of fees is not admissible. This should be made binding in the bar."*

### **AMENDED** — the premise about the code is correct; the demand is already met; the cost model is nonetheless wrong in a way the finding did not reach (see **X1**).

**Confirmed.** `settle.py:345` is `payout = round(pos.stake * pos.decimal_odds, 2) if won else 0.0`, and `_apply_official_settle` (`settle.py:333-401`) carries no fee term anywhere. The recorded book is fee-free, exactly as the RUN-ONLY note says at `LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md:80`.

**Rejected: "this should be made binding in the bar."** It already is. The bar requires fee adjustment before comparing (`:60`), gives the formula (`:64-66`), scores the *fee-adjusted* contrast (`LEARNING_LANE_15M_EVIDENCE_BAR.json:53`), and requires `mean(pnl_rule_fee_adj) > 0` for a positive reading (`:80`, `LEARNING_LANE_15M_EVIDENCE_BAR.json:72`). `critic.py:239-272` passes the bar on this check. The formula is also correct: Kalshi's `0.07 × C × P × (1−P)` with `C = stake/P` reduces exactly to `0.07 × stake × (1−P)`. I will not file a finding the draft already satisfies.

**Residual that is upheld.** The adjustment exists only as arithmetic performed by hand in a score note. `evidence_bar.py` implements nothing (`:28-70` is two loaders, a binding flag, and two burned-class lookups). The bar's binding numeric floor depends on a step with no code, no artifact, and no check.

**Concrete change demanded.** Implement `fee_adjust(recorded_pnl, posted_yes, stake)` in `evidence_bar.py` and require the score note to cite its output rather than a hand table, so the adjustment is reproducible from the bar rather than retyped. Then read **X1**, which is the part of this finding that actually bites.

**What would prove me wrong.** A committed, tested fee-adjustment function that the score note calls. That closes the residual.

---

# Findings the draft contains that were not on the list

## X1 — The omitted cost is not only the fee, and the fee runs the wrong direction for this rule

This is the most serious thing I found, and it inverts the bar's fee section.

**(a) The fee is not maximized near 50/50 on this book.** Stake is fixed at $1 (`paper.py:29`, `paper.py:218`), so contracts `C = stake/P` and the fee reduces to `0.07 × stake × (1 − P)` — **strictly decreasing in P**. Concretely: $0.035 at P = 0.50, $0.0455 at P = 0.35, $0.014 at P = 0.80. The RUN-ONLY note's own table confirms it — every $0.05 ceil-cent fee sits at a mark between 0.3350 and 0.4250, every in-band mark pays $0.04, and the 0.9835 mark pays $0.01 (`LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md:43-67`). `R-SKIP-COINFLIP` therefore skips the *middle* of the fee distribution and keeps the *most* fee-expensive fills. Whatever this rule does, "avoids the fee-heavy region" is not it. The bar's sentence at `:76` — "δ is also larger than the measured per-fill fee, so clearing the omitted cost by a rounding error is not distinguishable" — is true and describes the wrong hazard.

**(b) The book omits the bid/ask spread entirely, and the spread *is* largest near 50/50.** `paper_mark` is `public_mid_or_last(...)` (`kalshi_15m.py:213-228`, `:292`, `:318`) — the **mid** whenever both sides are quoted — and the payout is `1/mark` (`kalshi_15m.py:298`). The book buys at the mid and is paid at the mid. The RUN-ONLY note then charges a **taker** fee on that fill: "Taker formula, not maker" (`LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md:32`). A taker does not get the mid. A taker pays the ask.

The omitted half-spread costs `s / (p + s)` per $1 of stake. At p = 0.50 that is **$0.010 per fill** on a one-cent book and **$0.020** on a two-cent book, against a mean fee of $0.039 (`:68`) — the same order as the cost the bar spent an entire section closing. And unlike the fee, this cost *is* worst at the coinflip: at p = 0.50 it is $0.010, at p = 0.90 it is $0.006, and near the deci-cent-ticked extremes it is negligible.

**The bar priced the cost that does not support the rule's thesis and omitted the one that does.**

Supporting inference on the spread's width, flagged as inference: every mark in the note's 24-row table terminates in a half-cent (0.4650, 0.5150, 0.6350, 0.7050, 0.3850 …) except 0.9835, which is what the mid of a one-cent-wide book looks like, with a finer tick near the boundary consistent with `PRICE_LEVEL_STRUCTURE = "tapered_deci_cent"` (`kalshi_15m.py:56`).

**Concrete change demanded.** (a) Amend `:60` to read that recorded pnl omits **both** the entry fee and the bid/ask spread, since fills are struck at the public mid and paid at `1/mid`. (b) Either add a half-spread term to the adjustment at `:64-66`, or state plainly on the bar's face that the fee-adjusted figure remains optimistic by an unmeasured amount of the same order as the fee. A bar that closes one omitted cost and stays silent about a comparable one is more dangerous than a bar that closes neither, because it reads as complete. (c) Strike or correct the implication at `:76` that the fee hurdle bites hardest near 50/50 on this book.

**What would prove me wrong.** Show `yes_bid == yes_ask` on these windows (zero spread), or show that `paper_mark` resolves to `yes_ask` rather than the mid in practice. Either kills (b). Note that (a) needs no market data at all — it follows from `fee = 0.07 × stake × (1 − P)` being monotone in P.

## X2 — The Established verdict has no producing code path

`:91` requires `execution=true`, "the loop honored `rules.decide()`", for L2 confirmation and for any establishment verdict, and `LEARNING_LANE_15M_EVIDENCE_BAR.json:37-39` sets `accepts_replay: false`, `accepts_lived: true`, `requires_held_out_confirmation: true`.

Nothing in the running loop calls `rules.decide()`. The only callers on the tree are `tests/test_learning_rules.py:1,34,38,40`. `paper.py:176-301` fills every candidate window and never consults the registry. `LEARNING_LANE_15M_RULES.json:30` sets `"execution": false`, and its own note concedes: "execution=false until paper.py honors `rules.decide()`."

So **Established is currently unreachable**, and the bar does not say so. Worse, `:93` forbids the flip that would make it reachable — "Do not flip `R-SKIP-COINFLIP` to `execution=true` in order to make a replayed look look lived" — without ever naming when the flip *is* legitimate. As drafted, the bar requires lived L2 and prohibits, in ambiguous terms, the only action that produces one.

**Demanded.** Name the `paper.py` change as an explicit precondition of **Established**, and state the permitted flip point — before the first L2-eligible window closes, recorded with a commit SHA — so the prohibition at `:93` reads as a timing rule rather than a blanket ban.

**Falsifier.** Show a production call path to `rules.decide()` outside the test suite and this dies.

## X3 — L2's test is undefined

The bar fully specifies L1: n, H0, α, δ, and the kill/park consequence (`:70-80`). For L2 it specifies **nothing** beyond "a second precommitted look, not a retry of L1" (`:43`). No n beyond the range, no α, no δ, no decision rule, and no statement of whether an L2 look increments the counter — `:99` says the counter increments "once per first-look (L1) score," which reads as excluding L2 and quietly makes confirmation free.

A confirmation look with an unspecified threshold is not pre-committed. It is a look whose threshold gets set after L1 is known.

**Demanded.** State L2's α, δ, H0, and counter treatment in this document, before L1 is scored. **Falsifier.** They appear. Then this dies.

## X4 — `trials_to_date` counts write-ups, not tests

`:99`: "It increments once per first-look (L1) **score** of any *selection* rule." A rule that is proposed, replayed informally, and dropped before anyone writes a score never touches the counter. The multiplicity family is therefore defined by what got written up rather than by what got tried, which is the wrong denominator and the one that always flatters.

**Demanded.** Define the family as *declared* selection rules on this lane, increment on declaration rather than on score, and make it mechanical (see finding 6). **Falsifier.** A rule declared, replayed, and abandoned without incrementing the counter is the observation that confirms me; a bar that increments on declaration removes the objection.

## X5 — "Operator answers each objection" is not "Operator sustains or fixes"

`:8-11` makes the bar binding on two conditions: a Soften Critic attack that Operator answers in the admit pass, and a Founder read-once acknowledgement. Neither requires Operator to **sustain** anything. As written, "answers each objection" is satisfied by writing *noted, rejected* eight times. That is the routing-around-the-critic failure `PROTOCOL.md:208` exists to prevent.

And the bar is proposed to bind while failing four of the lane's own mechanical checks, without disclosing that anywhere in `:1-17`.

**Demanded.** (a) `:10` must require that every objection Operator does not sustain is answered with a stated reason, and that the objections **and** the answers are linked from the bar itself, so Founder's read-once covers both and not just the bar. (b) Add a third binding condition: `critic-invariants` passes on the exact bytes proposed to bind, or each failing check is named on the bar's face with Operator's reason for binding anyway.

**Falsifier.** An admit pass that sustains or explicitly overrules each numbered objection above, with reasons, and discloses the failing checks. This objection is then satisfied rather than refuted — which is the outcome I want.

## X6 — (minor) δ is denominated in dollars, not units of stake

δ = $0.28 per window (`:74`) is meaningful only because `PAPER_UNIT = 1.0` (`paper.py:29`) and `stake_usd: 1.0` (`LEARNING_LANE_15M_EVIDENCE_BAR.json:67`). If the unit ever changes, δ silently becomes a different effect size and nothing complains. One-line fix: express δ as a fraction of stake, or add an invariant that fails when `PAPER_UNIT ≠ 1.0` while this bar is binding.

## X7 — A failing Critic report clears the Critic

This one arrived under me during the attack and is the cleanest example of gate-pass-as-clearance on the tree.

At 11:11:57 EDT the clerical runner served `critic-invariants` and wrote `LEARNING_LANE_15M_CRITIC_FINDINGS.json` with `"passed": false` and five failing checks, four of them properties of this bar. The role was then **marked served and left the owed list**, because `serve_role` decides on one thing only: `if after == before: … role stays owed` (`runner.py:450-463`). It never reads `passed`. A report saying *the bar fails four method checks* clears the role exactly as a clean report would.

Two consequences, both bad:

1. **The desk will show `critic-invariants` served while the bar it reviewed is failing.** A later reader — Operator, Founder, or the next session — sees a whitelisted role cleared on proof and reads it as clearance. It is not clearance. It is a report that the bar does not pass.
2. **The role clears every tick regardless of content.** `run_critic_invariants` stamps `ran_at` and a per-row `checked_at` on every run (`critic.py:440`, `:450-452`), so the payload — and therefore the proof hash — changes on every pass whether or not a single verdict moved. `serve_role` has a material-change test for `systems` (`runner.py:464-469`, `material_publish_reasons`) and **no equivalent for `critic-invariants`**. This is the exact defect `PROTOCOL.md:97` names: "A systems heartbeat (`generated_at` only) is not proof." It is unpatched for this role, which also means `clerical_roles_clear` (`PROTOCOL.md:120`) can never fire for it.

**Demanded.** (a) `serve_role` must not mark `critic-invariants` served on a timestamp-only rewrite — give it a material-change test on the `checks` block, the way `systems` has one on the manifest. (b) A findings report with `passed: false` must leave something owed — either the role itself or a named Operator obligation — so a failing method check cannot be retired by the machine that found it. (c) The bar's binding conditions (`:8-11`) must not be satisfiable while its own findings artifact says `passed: false`; this is the same demand as **X5(b)**, reached from the other direction.

**What would prove me wrong.** Show that `serve_role` inspects `passed`, or that a timestamp-only rewrite leaves the proof hash unchanged. Neither is true today: `runner.py:445-463` runs the worker and compares fingerprints, and the payload carries `ran_at`.

---

# Considered and not filed

Recorded so Operator can see what I looked at and declined to raise. Padding a finding teaches Operator to route around me.

- **"An Admissible ADMIT could be issued on a test that failed the numeric bar."** `:121` already scopes an ADMIT to "a frozen exit (PASS / FAIL / park / residual) under the named bar for that date," which covers it. Not filed.
- **Burned-class completeness.** `:111` names five lane-local classes; all five are present in `LEARNING_LANE_15M_BURNED_CLASSES.json:149-183` with aliases, and `H-SPOT-MOY-CONT` is correctly in `fragile_not_null` rather than `classes` (`:6-14`), matching `:109`. `evidence_bar.py:46-70` enforces both. Nothing found.
- **The 56-window calibration count.** `:131` checks out: 2026-09-07 15:45 through 2026-09-08 05:45 inclusive is 57 windows at 15-minute spacing, minus the missing `072245` = 56. Honest arithmetic.
- **The fee formula and the note's totals.** `0.07 × stake × (1 − P)` is Kalshi's published taker formula specialized to fixed-$1 notional. The note's totals reconcile: $0.94 / $24.00 = 3.92%, mean $0.039 (`LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md:69-76`). Nothing found. The ceil-to-cent choice is conservative against the rule and is disclosed at `:31`.
- **`k = 0.07` is used without a pinned schedule hash.** Real, but `critic.py:348-371` already fails the bar on it and words it better than I would. Recorded above in the check table; not re-filed as mine.

---

# A note on tree movement during this attack

For the record, because it bears on whether the mechanical Critic was live when the bar was drafted, not as a finding against the bar: on first read, `critic.py` imported `repo_root` from `learning_lane_15m.paths`, which does not export it (`paths.py` has no such name), and the module raised `ImportError` on import. On re-read the import had been corrected to `operator_surface.observability` (`critic.py:35`), the suite ran, and at 11:11:57 EDT the clerical runner served `critic-invariants` and wrote its findings artifact for the first time. I did not make the code change and did not write the artifact. The bar's own hashes were identical before, during, and after, so the text I attacked did not move.

The window matters: while that import was broken, `critic-invariants` could not run and the `EVENT_ARTIFACT_UNREVIEWED` event class could not fire — so a bar landing on the tree raised nothing, which is the precise defect `critic.py:3-6` says the module was written to fix. The bar was drafted inside that window.

Two things follow that are worth Operator's attention. `learn.py:876` imports `unreviewed` **outside** the `try` at `:878-881`, so an import failure propagates out of `repo_events()` rather than being handled; and the `except Exception: return []` at `:880-881` means any *runtime* failure in the Critic's detector reports **no events**, silently leaving the Critic un-owed. Ten lines above, the sibling detector does the right thing — it emits an event saying "a detector that cannot see is not a detector that saw nothing" (`learn.py:858-864`). `PROTOCOL.md:112`: "A suite that cannot run is itself a failure, never a silent pass." The same file contains both patterns.

---

**Closing.** I did not propose a rule, score a rule, ADMIT, PARK, Soften, Harden, or Kill anything. I did not open a window outcome file, pre- or post-declaration. I did not edit the bar, the desk, or the leave-off, and I did not commit, push, or run the digest generator. I wrote objections. Operator answers them.

Handoff → `operator`.
