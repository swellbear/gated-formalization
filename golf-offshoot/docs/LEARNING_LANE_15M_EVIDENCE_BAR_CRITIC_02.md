# Soften Critic — attack on the **amended** 15m evidence bar (CRITIC 02)

**Role:** Soften Critic · **Date:** 2026-09-08 · **Lane:** `learning_lane_15m` · series `KXBTC15M` only
**Branch:** `cursor/part-a-clerical-trust-boundary` at `2ad6fe1` ("Part 7 admit pass: Operator answers all 14 objections and amends the bar").

**Session separation.** This session did not draft the bar (#174), did not write CRITIC 01, and did not write the admit pass that amended it (`2ad6fe1`). Three separate sessions now.

**This is an attack, not a verdict.** Operator answers each objection in a turn that is not this one. Nothing here is a Soften, an ADMIT, a RUN-ONLY, a park, a score, or a proposal. No rule was scored. `binding` stays `false` exactly as I found it. Trading is **NOT ARMED** and nothing in this file arms it.

**Why this file exists.** CRITIC 01 attacked the *draft*. Operator then rewrote the test — a new null, a new α schedule, n 40 → 70, a permutation control, a pre-registration section, an L2 test, a rewritten cost section. Binding condition 1 is marked `met: true` for CRITIC 01 (`LEARNING_LANE_15M_EVIDENCE_BAR.json:14-18`). It is **not** met for the bar as it now stands, and the bar says so itself at `:17`: "CRITIC 02 attacks *this* version." That is the gap this file closes.

---

## Artifacts attacked, by SHA-256

Binding condition 2 is defined on "the bytes proposed to bind," and the bar itself warns at `LEARNING_LANE_15M_EVIDENCE_BAR.md:38` that `critic.py` records a newline-normalised digest rather than the byte hash. Both are recorded here. I computed the normalised column independently via `critic.artifact_digest()` rather than reading it out of the findings artifact; it agrees with what that artifact recorded at 12:02:45.

| File | SHA-256 (bytes) | SHA-256 (newline-normalised) |
|---|---|---|
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR.md` | `C220AF0E0D1EBFB4494A50C73D01C27AC413ADFBDEC464F11176F2441821B21E` | `5F2AA5F5462956BFBBEDFC0E7AD6AE26841CFEBB7347A26E61F294E3B923A7C5` |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR.json` | `6B8013DA92E9B38AA8D3B7BFB8A7A15D947D3C63827728D4E75BB41AF1F6E7F1` | `2611C255C69072A6C2E81EF1BEF3A0C7765A3F26B50F7C524A2909F069AF1835` |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR_CRITIC_01.md` | `F23A5A513AB9E63746468128442D1D94DBA1BEC4E16552CEBC9B9BF27C9CA85C` | — |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR_OPERATOR_ANSWER_01.md` | `176D09DC99524936ADC7241913CECE72528EE7DFF9DFDE3CCFC89B2B17205364` | — |
| `golf-offshoot/docs/LEARNING_LANE_15M_CRITIC_FINDINGS.json` | `AEE248D24727CF4DE0B74FAECBBC6153FD26AF9A7B6655AF023F81FFA9AB81D0` | — |
| `golf-offshoot/docs/LEARNING_LANE_15M_RULES.json` | `8702C4B9F5804AB3285C5A6337614437C56DB5F58D6C63C4996F31736AADE081` | `CD25DD72BE7E6182A9ACD6BFA1F7F0854A4A75FC98E4D55D71730BCA68309027` |
| `golf-offshoot/docs/LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md` | `71AAB4DA1C0AFFD86396C8D02864670FE8A373079770A7F6A11D5AFD0421A616` | `83D4463B4BB55D327485E3874A4BF3DAA54727D7ED37F56C124C6E8913DAF0B4` |
| `golf-offshoot/src/golf_offshoot/learning_lane_15m/critic.py` | `A2F7CE900746685E58F0C6F4372FE6CEABA8FF931B84A9312F2876D2DFD52424` | — |
| `golf-offshoot/src/golf_offshoot/learning_lane_15m/runner.py` | `E6C5276B028D2098816461A4F25BE21349BD7C8F7FA25E7F8BE855ADECDC8E02` | — |
| `golf-offshoot/src/golf_offshoot/learning_lane_15m/triggers.py` | `2B108CAD737132AA78F64BE404717A8050D5415762C4BBAE85496F3AA75364DE` | — |
| `golf-offshoot/src/golf_offshoot/learning_lane_15m/paper.py` | `C59CBBE79EB975292089AD02198409FF4DA199AD66E0B8B686E5CF4E28058D2D` | — |
| `golf-offshoot/src/golf_offshoot/learning_lane_15m/settle.py` | `339473EF1319D76C1E0BF055ADDCB0E2694BEA5EBB4D3B626A93DDC39982850D` | — |
| `golf-offshoot/src/golf_offshoot/learning_lane_15m/rules.py` | `321AE400FA16CF54049E6792DFC4F9A271D5BC6CEAAA01941A0887FFF7EBC6A8` | — |
| `golf-offshoot/src/golf_offshoot/learning_lane_15m/learn.py` | `0D832A04CAA9DF6A203E67BAC1B97913EBE2C6C5381D13BD7A8CF711206FAB61` | — |
| `golf-offshoot/src/golf_offshoot/learning_lane_15m/evidence_bar.py` | `CE2C1CE09391810D59EC220D98CD634B9866A6B23ABDAE234B6A1875E9C985BC` | — |

Hashes recomputed at the end of the attack and unchanged: the text I attacked did not move under me. The `.md` byte hash differs from the normalised one over 288 CRLF pairs; the `.json` over 245.

---

## Posture

**I did not open a single window outcome file** — no `paper/*.json`, no `settlements/*.json`, no `latest/journal.json`, pre- or post-declaration. Objection 4 invited me to compute the empirical half-spread profile from the tape. I declined, because the cheapest honest version of that computation reads the recorded books, and I would rather leave that owed to Systems than have a Critic be the first party to open the tape after declaration. Where a claim needs data I do not have, I say so and name who can get it.

Every number below comes from one of five places: the amended text, the code, the commit record, the derived wake state at `latest/learning_wake.json`, or my own arithmetic. **I re-derived every figure on the bar rather than taking the admit pass's word for it.** All of them reproduce (see §8).

I ran `run_critic_invariants()` read-only in a throwaway process. **I did not call `write_critic_findings()`**, did not serve or clear `critic-invariants`, and did not touch the findings artifact. To demonstrate objection 1 I built a scratch root in the OS temp directory, ran individual check functions against doctored copies with `root=`, and deleted it; nothing under this repo was written.

I did not edit the bar, the JSON, `critic.py`, `runner.py`, `DESK.md`, or `AGENT_LEAVE_OFF.md`. I did not commit, push, run the digest generator, or start or stop a hub.

---

# The one-sentence version

**The amendment rewrote the test and did not extend the ratchet, so nothing mechanical on this tree reads any of the new substance.** Not the new null, not the α schedule, not the power curve, not the pre-registration requirement, not the L2 test, not the calendar span, not the spread. `critic.py` reads no key named `h0`, `alpha`, `clauses`, `power`, `preregistration`, `calendar_days_min_l1_l2`, `sd_used`, `se_at_n`, `mde`, `delta_over_mde`, or `reject_if_mean_d_exceeds` — verified by search over the whole module. Six of the eight checks now read PASS, and the bar's own §What the mechanical Critic says presents that as the amendment landing in substance. It is not the same claim.

---

## Objection 1 — Keyword greens

### **UPHELD**, and wider than briefed: **five** of the eight checks are satisfiable by typing, not two.

`LEARNING_LANE_15M_EVIDENCE_BAR.md:31` discloses "**Two** of those checks are keyword-satisfiable." That understates it by three. I demonstrated each of the five on a scratch root, editing only the bar and never the code:

| Check | What I wrote | Result |
|---|---|---|
| `matched_exposure_control` | replaced the whole control object with the string `"NOT DONE - no control exists"` | **PASS** |
| `fee_adjusted_book_is_binding` | contrast set to `"pnl_rule_i - pnl_baseline_i (GROSS, no fee)"`, plus `fee_hurdle.binding: true` | **PASS** |
| `holdout_is_forward_only` | held-out set back to the bare index slice `"windows 71 through 140"`, `held_out_regime` and `forward_only_enforced_by` deleted, `forward_only: true` kept | **PASS** |
| `delta_above_detection_floor` | every declared number left alone; only the prose `effect_floor_rationale` changed to `"sd ~0.10 so 1.960 * SE_70 is small"` | **PASS**, ratio **11.952** |
| `fee_schedule_hash_recorded` | `schedule_sha256: "not-a-hash"` | **PASS** |

The mechanisms, in the code:

- `critic.py:221` — `ok = bool(declared) or per_bet`, where `declared = dist.get("matched_exposure")`. Any truthy value passes. A dict admitting no control exists is truthy.
- `critic.py:254` — `binding = bool(fee.get("binding")) or "fee_adj" in contrast`. Substring match on a free-text field, **or** a `binding: true` typed into `fee_hurdle`. Note what that second route means: the bar's own Hard NO at `:275` is "Do not set `binding: true` while `critic-invariants` reports `passed: false`" — and there is a *different* `binding` key, inside `fee_hurdle`, that turns a method check green with no fee adjustment anywhere.
- `critic.py:285-286` — `regime = bool(looks.get("held_out_regime") or looks.get("forward_only"))`, then `ok = regime or not by_index`. The keyword defeats the index-slice test outright.
- `critic.py:176-190` — `sd` and the critical value are scraped by regex out of the prose `effect_floor_rationale` string, then `mde = crit * sd / sqrt(n)` and `ok = ratio > 1.10`. The four structured fields that state the same quantities — `sd_used`, `se_at_n`, `mde`, `delta_over_mde` at `LEARNING_LANE_15M_EVIDENCE_BAR.json:120-123` — are **never read**. The bar can therefore declare one sd and be checked against another, and the check will report the one in the sentence.
- `critic.py:359` — `ok = bool(recorded)`. Non-emptiness, not a hash. The standing blocker on binding is one keystroke from green, and nothing compares the recorded digest to the fetched document. I record this precisely because Operator and CoS both declined to write a placeholder: their restraint is the only thing holding this check, and restraint is not a mechanism.

**The fee premise in the objection is right, and the reason is worse than stated.** `settle.py:345` is still `payout = round(pos.stake * pos.decimal_odds, 2) if won else 0.0` with no fee term. Yet the findings artifact records `"recorded_book_has_fee_term": true` (`LEARNING_LANE_15M_CRITIC_FINDINGS.json:66`). The cause is `critic.py:253`, `book_has_fee = "fee" in body.lower()` — and the only occurrence of `fee` in the whole of `settle.py` is at `settle.py:27`, inside the module path `golf_offshoot.data_**fee**ds.kalshi_15m`. My scratch settle.py, which had the payout line and no `data_feeds` import, produced `recorded_book_has_fee_term: False`. So a method check's evidence block asserts the exact opposite of the bar's own §The omitted costs, and it does so on a substring of a package name.

**Operator already conceded the shape of this for two checks and set the keys anyway, with the concession written down** (`:33-35`, and Finding 4 of the admit pass). I am not attacking that choice — leaving a key unset to fake a failure would be worse. I am attacking the arithmetic of what it buys: the desk now reads "**6 of 8**" (`DESK.md:47`) and the bar reads "This amendment addresses the first three in substance" (`:29`). Three of those six passes are prose, and a fourth reports a fee term that does not exist.

**Concrete change demanded.** For each of the five, either (a) replace the keyword test with one that recomputes or requires code to exist — `matched_exposure_control` should fail unless a committed permutation function with the pre-registered seed exists and is cited; `fee_adjusted_book_is_binding` should fail unless a committed `fee_adjust()` exists (already owed at `:225`) and should read the fee term from the payout expression rather than from any substring of the file; `delta_above_detection_floor` should read `sd_used` / `se_at_n` and fail when they disagree with the rationale; `fee_schedule_hash_recorded` should require a 64-hex-character value and a non-empty `schedule_checked_at`; `holdout_is_forward_only` should key on the commit-ordering clause, not the adjective — or (b) state on the bar's face, in the count, that **five** of the eight are keyword-satisfiable, and stop describing three prose passes as the amendment landing "in substance." One of those two. Not neither.

**What would prove me wrong.** Show that any one of the five checks fails on a doctored bar whose *substance* was removed and whose *keyword* was kept. I ran exactly that experiment on all five and all five passed; a corrected run showing a FAIL kills that row.

---

## Objection 2 — The δ check answers a retired question

### **UPHELD.**

`check_delta_above_detection_floor` computes `mde = crit * sd / sqrt(n)` (`critic.py:188`) and passes when `delta / mde > 1.10` (`:190`). That ratio is the distance from δ to the rejection threshold of a test **against a zero null**. The bar's null is no longer zero. It is `H0: mean(d) <= δ` (`LEARNING_LANE_15M_EVIDENCE_BAR.md:92`, `LEARNING_LANE_15M_EVIDENCE_BAR.json:100`). `critic.py` contains no reference to `h0` at all.

Re-derived from the bar's own numbers, sd 0.784 and n 70:

- SE = 0.784 / √70 = **0.093706** (bar: 0.0937 ✓)
- `z * SE` at α₁ = 0.025 = **0.183660** (bar: 0.1837 ✓)
- δ / that = 0.28 / 0.183660 = **1.524554** → the check prints 1.525, the JSON prints 1.52 ✓
- The **operative** rejection threshold under the bar's actual null is δ + z·SE = **0.463660** (bar: 0.464 ✓)

So the number the check blesses, 1.525, is δ measured against a threshold the bar does not use. Measured against the threshold it *does* use, δ is 0.28 / 0.4637 = **0.604** of it. And the bar states the consequence itself at `:121`: "power *at* δ is α by construction." That is 2.5% power at the effect the bar declares material. **The check reads "delta is more than 10% above the floor" on a design with 2.5% power at δ, and that ratio can stay green at any n, forever, because both numerator and the scraped-SE denominator move with the design while the null sits on top of δ.**

This is not a small mislabeling. `delta_above_detection_floor` is the check the ratchet is proudest of — it caught 0.997 on the draft, the desk records it as the loop closing (`DESK.md:47`, `AGENT_LEAVE_OFF.md:5`), and it is now green. It went green because n moved, which was the right fix for the defect it *found*; it is no longer measuring that defect or any other.

**Concrete change demanded.** Add a check that reads `distinguishable.h0` and evaluates the design the bar actually specifies. The honest quantity under a floor null is power against a **stated alternative** — e.g. fail unless the bar names an effect size at which it has ≥ 80% power *and* that effect is inside a range the crew has said is worth acting on. Then keep `delta_above_detection_floor` for the zero-null case and make it assert which null it is evaluating, so a future amendment that moves the null cannot leave it silently answering the old question. This is the ratchet's own rule at `PROTOCOL.md:152`: a check that no longer reads the artifact it guards is a finding waiting to be rediscovered by hand.

**What would prove me wrong.** Show that `critic.py` reads `h0`, or show a reading of `delta/(z·SE) > 1.10` that constrains a test whose null is δ. If Operator names a decision-relevant δ (already owed at `:128`) and the bar's power at that δ is stated and adequate, the objection is satisfied rather than refuted.

---

## Objection 3 — Vacuous greens

### **UPHELD.**

Both checks pass on absence, and on this tree they are structurally incapable of failing.

- `check_declared_at_precedes_scored_windows` iterates `rule.get("scored_windows")` for each registry rule (`critic.py:308-312`). Neither rule in `LEARNING_LANE_15M_RULES.json` has that field. `violations: []` → PASS (`LEARNING_LANE_15M_CRITIC_FINDINGS.json:77`).
- `check_trials_counter_is_consistent` builds `looked` from rules carrying `scored_windows` or `last_look_at` (`critic.py:332`) and passes when `trials >= len(looked)` (`:333`). `trials_to_date: 0` ≥ 0 → PASS, and the artifact prints its own vacuity: `"trials_to_date=0 covers 0 rule(s) that have been looked at"` (`:84`).

The bar concedes the underlying prose problem twice — `:97` ("Nothing on the tree currently reads or writes `trials_to_date` — it is prose") and `:225` (the mechanical increment owed to Systems). What it does not say is that the two checks over that prose will report PASS for as long as the prose persists, because the fields they key on are fields the bar itself says no code writes. **A check whose failure condition requires a field no writer exists for is not a check; it is a green light with a docstring.**

There is a second-order defect here worth Operator's attention: `critic.py:342`'s failure message names `alpha 0.05/(trials+1)` — the **drafted** α scheme, retired by amendment 7 of the admit pass and replaced by `0.05/(k(k+1))` (`:96`). Should this check ever fail, it will explain the failure in terms of a formula the bar no longer uses.

**Concrete change demanded.** Make both checks fail closed while the counter is prose: `trials_counter_is_consistent` should FAIL, not PASS, when nothing on the tree writes `trials_to_date` — the condition is already known and written on the bar's face, so this costs no new information. And update `critic.py:342` to the α scheme in force. If a green is not available honestly, the suite should not print one.

**What would prove me wrong.** A committed writer for `scored_windows` / `last_look_at` / `trials_to_date`, at which point both checks become capable of failing and the objection dies. Until then, name the observation that could ever turn either red.

---

## Objection 4 — The spread overrule is model-conditional

### **AMENDED.** The demand as briefed is already half-met on the bar's face. The sharper defect is that the bar's constant-tick premise is contradicted by the tick model its own cited module declares.

**Rejected as stated: "Demand the overrule carry that condition explicitly."** It already does, in both files. `LEARNING_LANE_15M_EVIDENCE_BAR.md:150` opens "**At a constant tick**, `s/(p+s)` is *decreasing* in p," and `LEARNING_LANE_15M_EVIDENCE_BAR.json:178` opens "at a constant tick, s/(p+s) DECREASES in p." I will not file a demand the amended text satisfies, any more than CRITIC 01 would.

**And Operator's arithmetic is correct.** I recomputed it independently at a one-cent book, s = 0.005: 0.01639 at p = 0.30, 0.01408 at 0.35, 0.01099 at 0.45, 0.00990 at 0.50, 0.00901 at 0.55, 0.00552 at 0.90. Monotone decreasing throughout. CRITIC 01's claim that the spread inverts the fee's profile is wrong at constant tick, and the overrule stands.

**Upheld in a sharper form.** The premise is not merely unverified — it is contradicted by the code the bar reasons from. `kalshi_15m.py:56` declares `PRICE_LEVEL_STRUCTURE = "tapered_deci_cent"`, and that string is written onto every market row (`kalshi_15m.py:343-344`, `:395`) and into every paper movement (`paper.py:147`, `:265`). A *tapered* tick is by construction not a constant tick: it is finer at the extremes and coarser in the middle. That is the one tick geometry under which `s` rises toward 0.50 — and `s/(p+s)` is increasing in `s`. So the module the bar cites for `paper_mark` names precisely the structure that can restore CRITIC 01's direction, and the bar reasons as though the tick were flat. CRITIC 01 flagged the taper as an inference from mark endings; it is not an inference, it is a declared constant.

Compounding it, the conditional survives only one sentence. `:150` continues, unconditionally: "It runs the **same** direction as the fee, not the opposite. Both omitted costs are worst on cheap marks. A band skip avoids neither's worst region." The JSON does the same after its own conditional. The condition is stated once and then dropped, and it is the dropped form that a reader carries away, that the desk repeated at `DESK.md:53`, and that the leave-off repeated at `AGENT_LEAVE_OFF.md:178`.

**The data to settle it is already on the book and nobody has looked.** `yes_bid` and `yes_ask` are captured on every row (`kalshi_15m.py:289-290`, stored at `:314-315`) and classified `DISPLAY_ONLY_FIELDS` at `:57`. Nothing on this lane computes a spread from them: a search for `spread` across the whole package finds it only in `strategy/flip.py`, which is golf. The empirical half-spread against mark has never been plotted on `KXBTC15M`.

**Concrete change demanded.** (a) Carry "at a constant tick" into every sentence that states the conclusion, in both files, or state the conclusion as conditional once and never unconditionally. (b) Record on the bar's face that the constant-tick premise is contradicted by `PRICE_LEVEL_STRUCTURE = "tapered_deci_cent"` in the module the bar cites, and that the direction of the spread cost near 0.50 is therefore **unknown**, not settled. (c) Name the empirical half-spread profile — mean `(yes_ask − yes_bid)/2` bucketed by mark — as owed to Systems before the bar binds. It needs no new data collection, only fields already on disk. Until it exists, the bar should not assert that a band skip avoids neither cost's worst region; it should assert that it avoids neither the fee's worst region, which is proven, and that the spread's profile is unmeasured.

**What would prove me wrong.** An empirical profile from the recorded books showing half-spread flat or decreasing across the mark range, which would make the constant-tick model adequate and the overrule unconditional. I have deliberately not computed it (see §Posture); whoever does, wins this row either way.

---

## Objection 5 — `critic_findings_failing` re-owes Operator for a failure already on the bar's face

### **UPHELD.**

`triggers.py:344-369` raises the event whenever `payload.get("passed") is not False` fails to hold — i.e. on every tick that the findings artifact says `passed: false` — and it reads exactly two fields, `passed` and `failing` (`:356-358`). It has **no materiality test and no discharge path**. Live confirmation from the wake: `operator` is owed with reason `critic_findings_failing critic-invariants`, `owed_since 2026-09-08T08:45:43`, `age_text "3h 42m"`.

Compare the two guards this tree already built for the same shape:

- `systems` clears only on `material_publish_reasons`, not a heartbeat (`runner.py:504`).
- `operator` clears a park only when the new text **names what Operator was owed for** — `operator_write_addresses_owed`, `PROTOCOL.md:130`.

`critic_findings_failing` gets neither. It cannot be discharged by Operator writing anything, because the only thing that clears it is `passed` flipping true, and the single bar-side failure is `fee_schedule_hash_recorded`, which needs a document fetch that returned **HTTP 429** (`DESK.md:39`, `AGENT_LEAVE_OFF.md:154`). Under the bar's own park taxonomy (`PROTOCOL.md:226-231`) that is an **external** trigger — "needs an outside event," and external rows "age without pressure. They are not the crew's to fire." This one applies pressure every tick, with `ticks_unanswered` climbing.

And the bar's escape hatch has already been used. Binding condition 2 says "**or** every failing check is named on this bar's face with Operator's reason for binding anyway" (`:12`), and `:29` names `fee_schedule_hash_recorded` with the reason. The method's own designed discharge was exercised, and the machine cannot see it. That is the judicial-side twin of X7: X7 was a role *clearing* on a non-material change, this is a role *owing* on a non-material change. Same defect, opposite sign, same fix shape.

One aggravating detail. `fee_hurdle.schedule_checked_at` is `""` (`LEARNING_LANE_15M_EVIDENCE_BAR.json:170`). The 429 exists only as desk prose. So the machine record cannot distinguish *never attempted* from *attempted and externally blocked*, which is the distinction that decides whether Operator is silent or stonewalled.

**Concrete change demanded.** (a) Give `critic_findings_failing` a materiality test on the **failing set**: re-raise when the set changes, not on every tick that it is non-empty. (b) Give it a discharge path shaped like `operator_write_addresses_owed`: the line clears when the bar's face names exactly the current failing set with a stated reason, and stays owed — explicitly, with the reason written — when it does not or cannot be read. (c) Record the fetch attempt and its HTTP status in `fee_hurdle.schedule_checked_at` and a `schedule_fetch_status` field, and stamp the row **external**. **To be unambiguous: (c) does not turn the check green.** `critic.py:359` keys on `schedule_sha256` alone, so recording a failed fetch leaves `fee_schedule_hash_recorded` FAILING, which is correct. I am not asking anyone to pin a hash and I have not pinned one.

**What would prove me wrong.** Show a route by which Operator can discharge this line without the external fetch succeeding, or show that the event carries a materiality test I missed. Either kills it.

---

## Objection 6 — `honesty_stamp_is_fresh` is a 900-second desk timer living in the method suite

### **UPHELD**, and it is worse than a nuisance: **it defeats the X7 fix that Systems landed at 11:58.**

The check reads a date out of `## Honesty checklist` on `DESK.md` and fails past 900 seconds (`critic.py:374-416`). It is the eighth member of `CHECKS` (`critic.py:419-428`), so its state sets `passed`, and `passed: false` fires `critic_findings_failing` → owes **Operator** (objection 5). The bar already disowns it: "`honesty_stamp_is_fresh` is a property of `DESK.md`, not of this bar, and is not this file's to clear" (`:36`). Correct — and it is wired so that it pages Operator about the bar anyway.

**It has already flickered, twice, with the bar untouched.** The admit pass recorded it FAIL on the amended bytes (`OPERATOR_ANSWER_01.md:288`). The findings artifact written at 12:02:45 records it **PASS** — "stamped 2026-09-08 12:01, 105s old" (`LEARNING_LANE_15M_CRITIC_FINDINGS.json:104-112`) — with `failing: ["fee_schedule_hash_recorded"]`, a single entry. My read-only run reports it **FAIL** again, "1794s old," and `failing: ['fee_schedule_hash_recorded', 'honesty_stamp_is_fresh']`. Three states in about thirteen minutes; the bar's bytes were identical throughout. A desk that goes quiet for fifteen minutes turns the method suite red.

**The consequence nobody has noticed.** `serve_role` now guards `critic-invariants` with `critic_verdicts` instead of a raw fingerprint (`runner.py:509-517`) — the fix Operator found half-applied and Systems completed at 11:58. `critic_verdicts` is documented as "The verdicts and what they cover, **without the clock**" (`runner.py:298`), and it includes `detail` in the token: `{"id": ..., "state": ..., "detail": row.get("detail")}` (`runner.py:314`). Both `honesty_stamp_is_fresh` details embed a live clock reading — `f"stamped {stamped}, {int(age)}s old, ..."` at `critic.py:410` and `:412`, where `age = (now() - when).total_seconds()` at `:403`. Every other check's detail is static. So `age` changes on every ~90s pass, `detail` changes, the token changes, and `serve_role` marks `critic-invariants` served on a heartbeat exactly as before. **X7 has now been fixed twice and is still open, and the reason is the one check that does not belong in the suite.** `clerical_roles_clear` (`PROTOCOL.md:163`) still cannot fire for this role.

**Concrete change demanded.** Move `honesty_stamp_is_fresh` out of `CHECKS` and onto the desk/honesty surface where CoS owns it, reporting separately so it can never set the method suite's `passed`. If it must stay — and the ratchet's rule is that weakening a check is not Founder-free, which I respect — then (a) it must not contribute to `passed` or to `critic_findings_failing`, and (b) `critic_verdicts` must exclude any clock-bearing substring from the token, most simply by dropping `detail` and keeping `{id, state}` plus the reviewed hash set. Note that dropping `detail` does not weaken any check: `detail` is a rendering of `state` and `evidence`, and the reviewed-hash half of the token — the anti-deadlock guard at `runner.py:306-310` — is untouched.

**What would prove me wrong.** Show that `critic_verdicts` is stable across two consecutive passes with no artifact change. It cannot be while `detail` carries `int(age)`; a run showing two identical tokens 90 seconds apart kills this. Or show that `honesty_stamp_is_fresh` cannot set `passed` — contradicted by `critic.py:435`, which builds `failing` from every check in `CHECKS`.

---

## Objection 7 — Leftover owed lines make the board lie

### **UPHELD.** Read directly off `latest/learning_wake.json`.

`digestor`, owed since **09:01:48**, `age_text "3h 26m"`, eight reasons — every one of them `new_settle`, `new_fill` or `pending_cleared` on windows `081000` through `081045`. Part 2 replaced the every-settle trigger for human `digestor` with five enumerated exceptions (`triggers.py:74-261`; `PROTOCOL.md:113-121`), and the leave-off states at 7f that "the every-settle trigger is **not** restored." **Not one of the five appears in this role's reasons.** The line is owed entirely on a trigger class that no longer exists.

`operator`, owed since **08:45:43**, `age_text "3h 42m"`, eight reasons — six are `new_settle` / `new_fill` / `pending_cleared` on `081045` through `081115`, which Part 4 explicitly stopped naming Operator for ("A routine settle names **only** the three clerical roles," `PROTOCOL.md:106`). Only the last two, `artifact_unreviewed lab_proposed` and `critic_findings_failing critic-invariants`, are live enumerated exceptions.

So the two judicial roles the desk shows as hours-stale are stale mostly on reasons the amended trigger model does not raise. The board is not reporting who owes what; it is reporting who owed what before Parts 2 and 4 landed, plus whatever accrued since. `MAX_REASONS` truncation makes it worse rather than better: the live reasons are appended at the tail (`learn.py:970-973`), so the retired ones occupy the head of a capped list and the real obligation is the part most likely to scroll off.

This matters beyond tidiness for one specific reason. `AGENT_LEAVE_OFF.md:130` and `PROTOCOL.md:130` record that #174 cleared an Operator line raised by settles on `080745`–`080830` that nothing had ruled on, and that "that cannot happen again." The guard built for it, `operator_write_addresses_owed`, tests whether Operator's *write* names what Operator was owed for. It does nothing about an owed line whose *reason* is retired — and an Operator who reads these eight reasons cannot tell which two are real.

**Concrete change demanded.** Migrate `roles_owed` when the trigger model changes: on load, drop reasons whose event kind is no longer raised for that role, and record the drop with its cause in the wake payload so the board shows a shortening rather than a silent edit. Do not clear the roles — `operator` is legitimately owed on `artifact_unreviewed lab_proposed` and `critic_findings_failing`, and `digestor` should be re-derived against the five exceptions and stay owed if any holds. This is a reason-list correction, not an amnesty, and it must not be done by a role clearing itself.

**What would prove me wrong.** Show that `new_settle` / `new_fill` / `pending_cleared` still name human `digestor` or `operator` under `triggers.py` as it stands. I read the module and they do not; if they do, these lines are honest and the objection dies.

---

## Objection 8 — Re-verification of CRITIC 01 against the admit pass

### **The 7 / 7 accounting is CONFIRMED**, and every figure on the bar reproduces.

Fourteen objections, fourteen verdicts, none dismissed without a reason:

**SUSTAINED (7):** Finding 2, X2, X3, X4, X5, X6, X7.
**SUSTAINED IN PART (7):** Findings 1, 3, 4, 5, 6, 7, X1.

Each "in part" carries an explicit overrule with a stated reason, and three of those overrules are of Critic claims rather than of the briefed premises: the magnitude half of Finding 1, demand (c) of Finding 3 (n = 70 for 80% power at δ, which is incompatible with the floor null the same pass adopted), and the direction claim in X1(b). Operator's own §What I verified myself table is not decoration — I recomputed all 22 rows of it and every one holds.

**Numbers I re-derived from scratch, all confirming the bar:**

| Quantity | Bar | Mine |
|---|---|---|
| α₁ = 0.05/(1·2), z | 0.025, 1.960 | 0.025, 1.95996 |
| α₁₄ = 0.05/(14·15), z | 0.000238, 3.494 | 0.000238095, 3.49380 |
| FWER over 14 looks, `0.05/k` | 15.2% | 0.151767 |
| FWER over 14 looks, `0.05/(k(k+1))` | 4.6% | 0.045945 |
| Σ 0.05/(k(k+1)) | 0.05 | 0.050000 |
| SE at n=70, sd 0.784 | 0.0937 | 0.093706 |
| MDE, δ/MDE | 0.1837, 1.52 | 0.183660, 1.524554 |
| Reject if mean(d) > | 0.464 | 0.463660 |
| 80% power effect | 0.543 | 0.542525 |
| sd 95% UCB, 55 df | 0.784 | 0.78420 |
| Drafted δ/MDE at n=40 | 0.997 | 0.997411 |
| Drafted power at δ | ~50% | 0.497221 |
| Drafted 80% power effect | $0.37 | 0.368554 |
| n for 80% power at δ (zero null) | ~70 | 69.302 |
| Fee at P = 0.35 / 0.50 / 0.80 | .0455/.035/.014 | identical |
| Spread s/(p+s) at 0.30/0.50/0.90 | .0164/.0099/.0055 | .01639/.00990/.00552 |
| 56 calibration windows | 56 | 57 quarter-hours 15:45→05:45 less `072245` = 56 |
| `2fea8d8` → `0786279` | 8h 7m 14s | confirmed from the commit record |

The arithmetic of the amendment is sound. My objections are about what the amendment is *checked* by, not about its numbers.

*One record-keeping discrepancy, noted not filed:* `AGENT_LEAVE_OFF.md:176` says CRITIC 01 rejected three briefed premises and names Findings 3, 4 and multiplicity (6); `DESK.md:56` says "findings 3, 4 and half of 1." Both are defensible readings of a file that rejects part of 1, 5 and 7 as well, but the two boards disagree about which three. Board bookkeeping, not a bar defect.

---

# Findings the amended bar introduced that were not on the list

## Y1 — `amended_at` is midnight, and it precedes `drafted_at` by eight and a half hours

`LEARNING_LANE_15M_EVIDENCE_BAR.json:6` reads `"amended_at": "2026-09-08T00:00:00-04:00"`. `:5` reads `"drafted_at": "2026-09-08T08:30:00-04:00"`. **The machine copy of the bar says it was amended 8h 30m before it was drafted.** Midnight is also not when the amendment happened: CRITIC 01 was filed at 11:35 (`DESK.md:56`), the runner re-ran on the amended bytes at 11:49:42 (`OPERATOR_ANSWER_01.md:297`), and Operator posted done at 11:55 (`DESK.md:55`). The true value is between 11:35 and 11:49, so the field is wrong by roughly 11h 45m in the direction that makes the amendment look older than the draft it amends.

This is not a typo I would file on its own. I file it because of where it sits. The bar's §Pre-registration of rule parameters exists to stop exactly this: it refuses a `note` field's self-certification, demands "the **commit SHA and timestamp** of the registry entry that first names them" (`:165`), and records `R-SKIP-COINFLIP`'s band as not verifiably pre-registered on an 8h 07m 14s timestamp comparison. A bar that disqualifies a rule on timestamp order, in a machine artifact whose own timestamp order is inverted, has a credibility problem that no reader should have to discover. And nothing catches it: no check compares `amended_at` to `drafted_at`, and `check_declared_at_precedes_scored_windows` covers registry rules only.

**Demanded.** Correct `amended_at` to the real amendment time with the commit SHA beside it, and add a check that fails when any `*_at` on the bar precedes `drafted_at`, or when `amended_at` is midnight-exact — the signature of a hand-typed date. **Falsifier.** Evidence that the amendment work began at 2026-09-08T00:00:00−04:00. The desk thread and the runner's own 11:49:42 run contradict it.

## Y2 — Fourteen sustained objections, twenty-two edits, zero new checks

`PROTOCOL.md:151-152` and `:167`: "every flaw analysis finds becomes a permanent check here, so it cannot recur silently. A finding that does not produce a check is a finding that will be rediscovered by hand." The admit pass sustained fourteen objections and lists twenty-two edits to the bar. `CHECKS` still has exactly eight members (`critic.py:419-428`), the same eight enumerated at `PROTOCOL.md:167` and `AGENT_LEAVE_OFF.md:172`. **Not one new check.**

The eight code obligations went to `owed_to_systems` (`LEARNING_LANE_15M_EVIDENCE_BAR.json:219-228`) instead, which is a list on the artifact being checked — the same category the bar calls prose when a rule does it. Combined with objection 2, the effect is that the entire amended substance is unguarded: I searched `critic.py` for `h0`, `alpha`, `clauses`, `power`, `preregistration`, `verifiably`, `calendar_days`, `spread`, `sd_used`, `se_at_n`, `mde`, `delta_over_mde`, `reject_if` and found three hits, all of them incidental — a rounding call at `:204` and two mentions of the retired α formula in docstring and failure text at `:327` and `:342`.

**Demanded.** Before this bar binds, name for each of the fourteen sustained objections either the check that now guards it or the reason a check is impossible, on the bar's face. The ratchet's promise is the reason a reader is entitled to treat six-of-eight as meaningful; where the promise was not kept, the count should not be quoted. **Falsifier.** A check added for any sustained objection between `915195b` and `2ad6fe1`. The `CHECKS` tuple is unchanged.

## Y3 — "3 distinct UTC days" is a clock-alignment rule, not a span rule

`LEARNING_LANE_15M_EVIDENCE_BAR.md:67` requires L1 and L2 together to span "at least **3 distinct UTC days**," and gives the rationale: "without this the whole test lives inside one contiguous stretch of one regime." `LEARNING_LANE_15M_EVIDENCE_BAR.json:82` sets `calendar_days_min_l1_l2: 3`.

L1 + L2 is fixed at 140 windows, which the bar correctly computes as ~35 hours (140 × 15 min = 35.0 h exactly). I enumerated every quarter-hour start time in a UTC day: **a 35-hour block touches 3 distinct UTC dates for any start at or after 13:15 UTC, and 2 for any start before it.** So the constraint is satisfied or not purely by what time of day L1 begins, and it requires **zero** additional tape. The minimum elapsed time that can touch three UTC dates at all is 24h 15m, well under the 35 hours the design already has.

Since the crew chooses when a rule is declared, and L1 starts at the first eligible window after `declared_at`, this is fully under crew control and costs nothing. It answers CRITIC 01's residual (i) — "one regime, and less than a day of it" — with a rule that adds no regime diversity whatsoever and can be met by declaring a rule in the afternoon.

**Demanded.** Replace the calendar-date test with a tape-span test: state a minimum elapsed wall-clock span for L1 + L2 in hours, chosen for regime diversity rather than for midnight-crossing, and/or require a stated gap between the close of L1 and the open of L2. If 35 hours is all this lane can offer, say that on the face and scope the Established verdict to it — which the bar already does at `:68`, making the 3-day clause redundant as well as gameable. **Falsifier.** Show a 140-window block that fails the 3-UTC-date test while spanning more than 35 hours, or a start time at or after 13:15 UTC that fails it. Neither exists.

## Y4 — The registry was not amended with the bar, so the rule's own falsifier still says 40

`LEARNING_LANE_15M_EVIDENCE_BAR.md:103` calls its kill clause "the numeric form of `R-SKIP-COINFLIP`'s existing falsifier." That falsifier, unchanged at `LEARNING_LANE_15M_RULES.json:32`, reads: "**After 40 eligible windows**, if selected-fill settlement_pnl cannot be distinguished from R-BASELINE-FILL-ALL on those same windows, park this rule." The bar forbids computing at that n — "Do not compute the test at n = 1, 10, **40**, or 69" (`:64`) — and its Hard NO at `:277` forbids scoring "before 70 eligible windows." **The bar claims to be the numeric form of a falsifier it now contradicts.**

`PROTOCOL.md:123` defines `rule_reached_n` as firing when "a declared rule has accumulated the n **its falsifier named**," and `triggers.py:304` repeats it. The code does something else: `target = (bar.get("looks") or {}).get("first_look_n")` (`triggers.py:308`), so it fires at 70. That happens to be the safe direction, and I record it as such — but it means the documented contract, the code, and the rule's own falsifier now name three different sources for one number, and only the code is right.

The same file carries a second stale self-certification: `LEARNING_LANE_15M_RULES.json:33` still asserts "Band chosen before looking at overnight marks," which the bar has just recorded as not verifiably pre-registered and which the bar's `:161` says is "**self-certification and is not accepted as proof**." `rule_registry` is a WATCHED artifact (`critic.py:65`), so this text is inside the Critic's remit and no check reads it.

**Demanded.** Amend `R-SKIP-COINFLIP`'s falsifier to n = 70 with a pointer to the bar as the governing source, or restate it as "the n named by the evidence bar in force" so the two cannot drift again. Annotate the registry `note` so it no longer asserts blind choice as fact, referencing the bar's pre-registration finding. Align `triggers.py:304` and `PROTOCOL.md:123` with what the code reads. **Falsifier.** A reading under which "after 40 eligible windows" and "do not compute the test at n = 40" are consistent instructions about the same rule.

## Y5 — The recorded paper book carries two contradictory accounts of its own fill price, and the bar's spread argument depends on which one is true

The bar's §The omitted costs rests on one factual claim: "`paper_mark` is `public_mid_or_last(...)` — the **mid** whenever both sides are quoted — and the payout is `1/mark`" (`:148`). I verified it in code and it is right: `public_mid_or_last` returns `(yes_bid + yes_ask)/2` when both sides exist (`kalshi_15m.py:220-223`), that becomes `paper_mark` (`:292`, `:318`), and `paper.py:198` prefers it.

But the book that gets written to disk says otherwise, in two places:

- `paper.py:181`, the function's own docstring: "Mechanical paper YES at **posted ask** for each open KXBTC15M window."
- `paper.py:232`, the `notes` string stamped onto **every recorded position**: "PAPER OBSERVATION ONLY. Mechanical YES at **posted Kalshi ask**."

against, on the same fill:

- `paper.py:258`, the movement's `reason_plain`: "Paper observation fill at the public Kalshi **mid/last** mark."

The `yes_ask` path exists only as a fallback when `paper_mark` is absent (`paper.py:199-200`), so on the live path the mid wins and the two "ask" strings are the false ones. This is exactly CRITIC 01's stated falsifier for X1(b) — "show that `paper_mark` resolves to `yes_ask` rather than the mid in practice. Either kills (b)" — and an auditor who takes the book's own position note at face value will conclude the omitted half-spread does not exist and that X1(b) is dead. The bar spends a section on a cost whose existence the recorded artifact denies.

Adjacent, same fill: `reason_technical` stamps `fee_type=quadratic x1` (`paper.py:264`) and `paper.py:147` writes the same into the seed note, on a book where no fee is ever charged (`settle.py:345`). A book that labels a fee type it does not apply is the write-side twin of the `data_feeds` substring in objection 1.

**Demanded.** Correct `paper.py:181` and `paper.py:232` to say the fill is struck at the public mid/last mark, matching `:258` and the code, so the recorded book cannot be read as contradicting the bar's cost section. Record on the bar's face that the position note said "ask" for every book written to date, so the calibration set's own provenance strings are known to be wrong rather than silently corrected. State that `fee_type=quadratic x1` is a label of the schedule that *would* apply, not a fee that was charged. **Falsifier.** Show that `paper_mark` is routinely absent so the `yes_ask` fallback is the live path — in which case the notes are right, the bar's spread section is wrong instead, and this finding inverts rather than dies. Settling it needs one read of `entry_market_p` against `yes_bid`/`yes_ask` on the recorded books; I did not open them, and it is owed to Systems, not to a Critic.

## Y6 — The judicial-silence counter reports the same number for lines 2h 26m apart

Part 8's one landed item is the silence counter: "Every owed line carries `ticks_unanswered` and the tick prints `silent N ticks`. Silence is now a number" (`AGENT_LEAVE_OFF.md:183`), implemented at `learn.py:985` as `entry["ticks_unanswered"] = int(entry.get("ticks_unanswered") or 0) + 1`, docstring "how many ticks this role has been named and has not answered" (`:983-984`).

The live wake reports `ticks_unanswered: 44` for **all three** owed roles, whose `owed_since` values are 08:45:43 (`operator`), 09:01:48 (`digestor`) and 11:11:51 (`soften-critic`) — spanning 2h 26m, roughly 98 cycles at the 90-second interval. Three lines that began 98 ticks apart cannot all have gone unanswered for 44 ticks. The counter increments once per recompute for every row present, from whatever was carried in, so it measures recomputes since the list was last reset — the same value for every row, by construction, regardless of when the row was named.

The number is therefore not a per-line silence measure, and it is the one number Part 8 shipped to make silence legible. It currently understates `operator` by more than a factor of two and overstates nothing, which is the flattering direction.

Same function, adjacent: `learn.py:981` sets `entry["served_at"] = None` unconditionally on every recompute, so a served timestamp on a role that is later re-owed is erased rather than retained.

**Demanded.** Derive `ticks_unanswered` from `owed_since` and the cycle interval, or seed it to 0 at the tick the role is named and increment only that row thereafter — and either way assert in a test that two rows with different `owed_since` cannot carry the same count. **Falsifier.** Show that all three roles were first named in the same tick, which the `owed_since` values on the artifact itself contradict.

## Y7 — Binding condition 2's `detail` is a point-in-time claim with no freshness requirement, and it is already wrong

`LEARNING_LANE_15M_EVIDENCE_BAR.json:22` states, as the standing detail of binding condition 2: "`fee_schedule_hash_recorded` **still FAILS**: no sha256 pinned … Standing blocker on binding." Singular. My read-only run reports `failing: ['fee_schedule_hash_recorded', 'honesty_stamp_is_fresh']` — two. The on-disk findings artifact (12:02:45) reports one, because `honesty_stamp_is_fresh` happened to be 105 seconds old at that moment.

So the bar's machine copy names a failing set that is correct only when the desk was stamped inside the last fifteen minutes, and the "or" branch of condition 2 requires "**every** failing check named on this bar's face with Operator's reason." Whether that branch is satisfied depends on how long ago CoS typed a date. Objection 6 removes the cause; this is the separate defect that the bar records a suite verdict as a static sentence with no timestamp and no requirement to be re-read, while `:26` correctly instructs the reader to "Run `critic-invariants` against the exact bytes of this file before treating any of this as current."

**Demanded.** Stamp the failing set on the bar with the `ran_at` of the run it came from, and require condition 2 to be evaluated against a findings artifact whose `reviewed` block contains the normalised digest of the bytes proposed to bind. Both digests are recorded at the top of this file for exactly that comparison. **Falsifier.** Show `honesty_stamp_is_fresh` cannot fail while the bar's bytes are unchanged — contradicted three times in thirteen minutes today.

---

# Considered and not filed

Recorded so Operator can see what I examined and declined to raise. A padded finding teaches Operator to route around the Critic.

- **Operator's overrule of X1(b)'s direction.** Recomputed independently and correct at constant tick. I filed the conditionality (objection 4), not the arithmetic, and I record that CRITIC 01 was wrong on this point and Operator right.
- **`delta_over_mde: 1.52` in the JSON versus `ratio 1.525` in the check.** Both are roundings of 1.524554. Immaterial; not filed.
- **The α schedule, the sd upper bound, the power curve, the 56-window count, the 8h 07m 14s gap, the fee monotonicity.** All reproduced exactly (§8). Honest arithmetic throughout; nothing found.
- **The `execution=false → true` timing rule** (`:213`). Sound as amended, and it fixes a real ambiguity in the draft. Nothing found.
- **`fee_adjust()` and the six other `owed_to_systems` code obligations.** Real and correctly recorded as preconditions of binding. CRITIC 01 raised them and Operator sustained; I do not re-file another session's upheld findings.
- **`check_honesty_stamp_is_fresh` attaches `now().tzinfo` to a naive desk stamp** (`critic.py:394`). It would misread a desk stamped in a different zone. On a single-machine Eastern tree it is harmless, and objection 6 asks for the check to leave the suite anyway. Not filed.
- **`_section_text` hashes `## Honesty checklist` to the next `## `** (`critic.py:76-88`), so a CoS edit below that heading does not re-owe the Critic. Deliberate and correct — the section scope is what stops unrelated desk edits from re-owing. Nothing found.
- **Whether `R-SKIP-COINFLIP` has reached any n.** Not computed, not looked at. Reporting an eligible count is permitted and I did not need one; nothing in this file requires it.

---

**Closing.** I proposed no rule, scored no rule, ADMITted nothing, PARKed nothing, and did not Soften, Harden or Kill anything. I did not set `binding: true`, did not pin a fee-schedule hash, and did not write a placeholder for one. I opened no window outcome file, pre- or post-declaration. I did not edit the bar, the JSON, `critic.py`, `runner.py`, `DESK.md` or `AGENT_LEAVE_OFF.md`, did not write the findings artifact, did not run the digest generator, did not start or stop a hub, and did not commit or push. Trading is **NOT ARMED**.

Eight objections ruled: six UPHELD, one AMENDED, none rejected outright — objection 4's briefed demand was rejected as already met and upheld in a sharper form. Seven findings added. `binding` stays `false`, and on objections 1, 2 and 3 together, the number that most needs to stop being quoted is "6 of 8."

Operator answers these. Handoff → `operator`.
