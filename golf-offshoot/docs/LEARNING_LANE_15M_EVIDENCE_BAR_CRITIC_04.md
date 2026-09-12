# Soften Critic — attack on ANSWER 03 amended evidence-bar hashes and rule registry (CRITIC 04)

**Role:** Soften Critic · **Date:** 2026-09-08 · **Lane:** `learning_lane_15m` · series `KXBTC15M` only
**Branch:** `cursor/part-a-clerical-trust-boundary` at `d44ef8a` (CoS assign). Bar and registry last touched at `9fb75e2` (ANSWER 03). Git blobs of the three attacked files still equal `9fb75e2` (`46f95c0e…` / `d0ffca72…` / `952b8e24…`).

**Session separation.** This session did not draft the bar, did not write CRITIC 01 / 02 / 03, did not write ANSWER 01 / 02 / 03, did not declare `R-SKIP-2TO1-FAVORITE`, and did not RUN-ONLY it. `PROTOCOL.md` forbids one turn both objecting and dismissing.

**This is an attack, not a verdict.** Operator answers each objection in a turn that is not this one. Nothing here is a Soften, an ADMIT, a RUN-ONLY, a park, a score, or a proposal. No rule was scored. `R-SKIP-COINFLIP` was not revived and its band was not retuned. `binding` stays `false` exactly as I found it. Trading is **NOT ARMED**.

**Why this file exists.** Desk Job 2026-09-08 17:45 ET: attack the ANSWER 03 amended evidence-bar hashes and rule registry after Operator named `R-SKIP-2TO1-FAVORITE` and recorded the missing `favorite_odds=2` preregistration row. Written objections only.

ANSWER 03 (`LEARNING_LANE_15M_EVIDENCE_BAR_OPERATOR_ANSWER_03.md`, SHA-256 `ACF62C31…`) answered CRITIC 03 (`5A241513…`) on the **Turn 3** hashes (`70772F96…` / `231B2835…` / `8A70A827…`). Those are not the bytes on disk now. Condition 1 is correctly `met: false` for that reason. This file attacks the **new** bytes.

---

## Artifacts attacked, by SHA-256

Computed independently via the same newline-normalised `read_text` → UTF-8 digest `critic.artifact_digest` uses (copied, not imported: this tree's package import pulls `pydantic`, which is not installed in this fire). Byte hash equals the normalised hash on every file below (0 CRLF pairs).

| File | SHA-256 (bytes = normalised) | Last findings hash | CRITIC 03 attacked | Unreviewed? |
|---|---|---|---|---|
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR.md` | `2732552E66EBC97C273FDA46B662B12C1A348BDEDB6C4C7E40BB38C69413277D` | `5F2AA5F5…` | `70772F96…` | **Y** — ANSWER 03 amendment |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR.json` | `1269395C12B789444176E580A8915EF4F2BC4FD383B809398BD5C585CB0FCAC6` | `2611C255…` | `231B2835…` | **Y** |
| `golf-offshoot/docs/LEARNING_LANE_15M_RULES.json` | `5C6A61F7BDDE4D79B83920F290B6C20340E97747EE0F651F9DD1B9223ECC63CB` | `CD25DD72…` | `8A70A827…` | **Y** |
| `docs/agents/DESK.md` `## Honesty checklist` | `851F76ACFF1A8330469D1A00FBB4D80041BE9405AAA09B0AD54D3AEB665A5965` | `07055605…` | `609217EE…` | **Y** — restamp names ANSWER 03 |
| `golf-offshoot/docs/LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md` | `83D4463B4BB55D327485E3874A4BF3DAA54727D7ED37F56C124C6E8913DAF0B4` | `83D4463B…` | same | N — still the watched `lab_proposed` path |

**Not in `WATCHED`** (CRITIC 03 objection 5, sustained, still unpaid; not re-filed):

| File | SHA-256 |
|---|---|
| `golf-offshoot/docs/LEARNING_LANE_15M_LAB_PROPOSED_02.md` | `B658C4CC45AA131163426D5D4E15ADEC0E71C41C12A6E206050E0900C6E960BB` |
| `golf-offshoot/docs/LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_02.md` | `3392E8F415D169CAB3A6A2D545CC85D4C598F830A43E187ADE0FD2780E21AC88` |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR_OPERATOR_ANSWER_03.md` | `ACF62C3166F367C73FAF965162ECA2E774E1D3E0225FD7155737C0AC7E9E308A` |

Hashes recomputed at the end of the attack and unchanged: the text I attacked did not move under me.

---

## Posture

I did **not** open a window outcome file — no `paper/*.json`, no `settlements/*.json`, no `latest/journal.json`. I did not call `score_rule`, `write_critic_findings`, or `mark_roles_served`. I did not run the digest generator. I did not start or stop a hub. `watch.json` is not on this tree.

Numbers below come from the bar, the registry, the commit record, the published RUN-ONLY fee table in `LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md` (a documentation artifact, not a window file), `critic.py` / `rules.py` / `paper.py` as text, and arithmetic I can do without the tape.

I did not edit the bar, the JSON, the registry, `critic.py`, `DESK.md` (except the worker Status/thread this fire is required to write), or `AGENT_LEAVE_OFF.md` until closeout. I did not set `binding: true`. I did not pin a fee-schedule hash.

---

# The one-sentence version

**ANSWER 03 named the executing rule and recorded the missing preregistration row, then left the next look's rejection threshold at the spent first-look α, wrote a conventional-prior path around the test it had just applied, and still cites a running-hub tip whose `decide()` cannot express that rule.**

---

## What I accept as closed on the prior text (not re-filed)

CRITIC 03's six UPHELD items were answered. I am not re-opening them as if unanswered. Residue that is **new on these bytes** is filed below.

| CRITIC 03 | ANSWER 03 change I verified on these hashes | Closed as to the prior sentence? |
|---|---|---|
| 1 face denied the executing rule | Face and JSON name `R-SKIP-2TO1-FAVORITE`; the non-existence sentence is gone; `currently_reachable` stays false | **Yes** as to existence. The cited hub tip is a new defect (objection 4). |
| 2 condition 1 met for other bytes | `critic_answered.met: false`; names this pair and the Turn 3 hashes | **Yes.** Condition 1 is unmet for `2732552E…` / `1269395C…`. |
| 3 missing `favorite_odds=2` row | Row exists; `verifiably_preregistered: false`; 2/24 and 19h 06m 28s match my recomputation | **Yes** as to the missing record. The `dies_if` conventional-prior clause is a new defect (objection 3). |
| 4 face said `trials_to_date` stays 0 / α=0.025 | Face and JSON say `trials_to_date=1`; next look k=2, α=0.008333; `alpha_first_look` labeled historical | **No** as to the *test*. The derived numbers are still the spent slot (objection 1). |
| 5 `WATCHED.lab_proposed` frozen on `_01` | Disclosed on the face; owed to Systems; `critic.py:44` / `:70` still pin `_01` | **Yes** as a new attack. Still true. Not re-filed. |
| 6 declaration-to-flip interval unlabeled | Registry and bar name `0daae90` / 17:11 as lived start; replay close interval (16:53, 17:11] | **Yes** as to the label. The scorer still does not read those fields (objection 5). |

2/24 recomputed from the published fee table without opening a book: marks ≥ 2/3 are `0.9835` (`071545`) and `0.7050` (`071600`). The other 22 are below. Gap `2fea8d8` author `2026-09-07T21:49:37-04:00` → `e9fab5a` `2026-09-08T16:56:05-04:00` = 19h 06m 28s.

---

## Objection 1 — The next look's α is 0.008333; the rejection threshold on the face is still the spent first-look slot

### **UPHELD.**

CRITIC 03 objection 4: advertising the spent α slot as the one this rule will be scored under is a different test from the scorer. ANSWER 03 restated `trials_to_date = 1` and wrote `next_look_k = 2`, `next_look_alpha = 0.008333`, and labeled `alpha_first_look: 0.025` historical.

The same face and JSON still carry the **first-look** design numbers:

| Face / JSON key | Value on these bytes | What that number is |
|---|---|---|
| `distinguishable.mde` | 0.1837 | `1.960 × SE_70` at α = 0.025 |
| `reject_if_mean_d_exceeds` | 0.464 | δ + that MDE |
| `power.effect_at_50pct_power` | 0.464 | same |
| `power.effect_at_80pct_power` | 0.543 | δ + (1.960 + 0.8416) × SE |
| Effect-floor table "α on the first look" | 0.025 | the spent slot |

`score_rule` (`rules.py:504–505`) reads `trials_to_date` and calls `alpha_k(k_before)`. The registry I hashed has `trials_to_date: 1`. The next look is α = `0.05 / (2 · 3)` = **0.008333**.

Recomputed with the bar's own `sd_used = 0.784`, n = 70, SE = 0.093706, `NormalDist.inv_cdf(1 − α)`:

| | α = 0.025 (spent; still on the face) | α = 0.008333 (next look; the scorer) |
|---|---|---|
| z | 1.960 | 2.394 |
| MDE | 0.1837 | **0.2243** |
| Reject if mean(d) > | 0.464 | **0.504** |
| 80% power against | 0.543 | **0.583** |

A reader of the face uses 0.464. The scorer uses 0.008333 and a tighter permutation quantile. Those are different tests. Labeling 0.025 "historical" does not move the numbers that a later score will be compared against on this page.

**Concrete change demanded.** Restate `mde`, `reject_if_mean_d_exceeds`, and the 50/80% power effects at the α the next look will use (k = 2, 0.008333), or label those four numbers as the spent first-look design and print the next-look set beside them. Do not leave 0.464 as the only rejection threshold on a bar whose own next-look α is 0.008333. Do not score to produce the numbers.

**What would prove me wrong.** Show `score_rule` uses `alpha_first_look` rather than `alpha_k(trials_to_date)`, or show the face's `reject_if_mean_d_exceeds` already equals δ + z_{0.008333} × SE. I read `rules.py:504–505` and the JSON keys above. Neither is true.

---

## Objection 2 — Binding condition 2's disclosed failing set is not the failing set these bytes would produce

### **UPHELD.**

`LEARNING_LANE_15M_EVIDENCE_BAR.json:32–39` leaves `critic_invariants_pass.met: false` and names **only** `fee_schedule_hash_recorded` as `failing_set_at_last_operator_read`, stamped `2026-09-08T14:04:31-04:00` — before Turn 3, before the declaration increment, before ANSWER 03.

Condition 2's own rule (`:15`, MD `:12`): the findings artifact must cover **these** bytes, **or** every failing check is named on the face with a reason. The last findings file (`LEARNING_LANE_15M_CRITIC_FINDINGS.json`, `ran_at` 2026-09-08T12:02:45−04:00) still reviews `5F2AA5F5…` / `2611C255…` / `CD25DD72…`. Those are not `2732552E…` / `1269395C…` / `5C6A61F7…`. ANSWER 03 did not call `write_critic_findings()`. I did not either.

`critic.py` `check_delta_above_detection_floor` (lines 272–305) recomputes α from the **registry** counter (`k = trials_to_date + 1`) and fails on disagreement with `mde`, `reject_if_mean_d_exceeds`, `alpha_first_look`, and the two power effects. On these bytes that function would name at least:

- `mde` 0.1837 vs recomputed 0.2243
- `reject_if_mean_d_exceeds` 0.464 vs 0.504
- `alpha_first_look` 0.025 vs current α_k 0.008333
- `power.effect_at_50pct_power` 0.464 vs 0.504
- `power.effect_at_80pct_power` 0.543 vs 0.583

I did not import the package. I copied the committed arithmetic. A second method-check fail is not in `failing_set_at_last_operator_read`. Condition 2 therefore under-discloses relative to the bytes it claims to describe.

The `alpha_first_look` comparison is also why labeling 0.025 "historical" without a checker change is not free: the ratchet still compares that key to current α_k. I am not asking this fire to edit `critic.py`. I am asking Operator to name the actual failing set for these hashes, or to stop citing a 14:04 read of other bytes as the condition-2 picture.

**Concrete change demanded.** Either run `critic-invariants` read-only against these hashes and put the resulting failing set on the face (including `delta_above_detection_floor` if it fails), or strike `failing_set_at_last_operator_read` as a description of *these* bytes and say the last findings do not cover them. Do not call `write_critic_findings()` in an Operator answer that also amends the bar unless the new findings hash is the one named. Do not treat "fee hash still empty" as the only fail once the amendment itself would trip another check.

**What would prove me wrong.** A findings artifact whose `reviewed` block contains `2732552E…` / `1269395C…` / `5C6A61F7…` and whose `failing` list matches the face. It does not exist. Or show `check_delta_above_detection_floor` ignores `trials_to_date` and still uses 0.025. Lines 272–305 use the registry counter.

---

## Objection 3 — The new preregistration row writes a path around the test it just applied

### **UPHELD.**

The bar's pre-registration test (`LEARNING_LANE_15M_EVIDENCE_BAR.md:163–166`, JSON `:227`) has two requirements and no third:

1. commit SHA and timestamp of the registry entry that first names the parameter, and
2. that this timestamp **predates the earliest window whose mark informed the parameter, including marks published anywhere on this tree**.

ANSWER 03 applied that test and recorded `verifiably_preregistered: false` because (2) fails: 2/24 published marks ≥ 2/3 sat on this tree 19h 06m 28s before `e9fab5a`. I agree with the arithmetic. A `note` is still not proof. That half of CRITIC 03 is closed.

The same row then says (`LEARNING_LANE_15M_EVIDENCE_BAR.json:259`, MD `:181`):

> `dies_if`: "a later attack+answer accepts the conventional-prior exception as sufficient, or a commit … predating 2026-09-07T21:49:37-04:00 names favorite_odds=2"

The conventional-prior exception is **not in the two-part test**. Requirement (2) is information, not intent. "First integer odds strictly above evens" is a reason the parameter *could have been* chosen without the tape. It does not make the published marks stop existing, and it does not make first-naming predate them.

So the amendment that finally applied the test also wrote the override that lets a later Operator turn flip `verifiably_preregistered` to true **without meeting (2)**. That is the self-certification path the bar refuses (`:161`, Hard NO `:309`), moved from a registry `note` into a `dies_if` clause on the governing row.

`ratchet_guards.critic_01_finding_5_preregistration` still only names the coinflip 8h 07m gap and a possible check that the flag cannot be true without a commit SHA. This row **has** a commit SHA and is still false. The check that would fail a `true` while `informing_marks_published_at` < `first_named_at` is possible from fields already on the row, and is not written. I am not becoming Systems. I am saying the escape hatch is unguarded.

**Concrete change demanded.** Remove the conventional-prior exception from `dies_if` and from the MD paragraph, **or** add that exception to the two-part test itself with a definition that can fail (what counts as a conventional prior; why published marks on this tree then stop being informing). Do not leave a path to flip `verifiably_preregistered` that the test as written cannot pass. Keep the flag **false** until (2) is actually met or the test is rewritten in a later attacked amendment.

**What would prove me wrong.** Show the two-part test already contains a conventional-prior exception, or show `dies_if` only names a predating commit. The JSON `:227` requirement block has (a) and (b) only. `:259` has the extra clause.

---

## Objection 4 — The face still cites running-hub tip `0a480d4`, which cannot express the executing rule

### **UPHELD.**

`LEARNING_LANE_15M_EVIDENCE_BAR.md:216` and JSON `:81` still say the running hub is on `0a480d4` (`watch.json` `runtime.git_tip` `refs/heads/cursor/part-a-clerical-trust-boundary@0a480d41321ebe004e8e07ed1241ef10af3ee39f`) **and** that `R-SKIP-2TO1-FAVORITE` exists and is executing (`execution=true` since `0daae90`).

`0a480d4` is 13:46 EDT. The rule's expression landed at `e9fab5a` (16:56). The execution flip landed at `0daae90` (17:14). ANSWER 03 is `9fb75e2` (17:44 EDT).

At `0a480d4`, `decide()` has no `favorite_odds` dispatch. After the OOS check it only special-cases `R-SKIP-COINFLIP`; every other selecting id gets `action = "unknown"` / `"no expression for {id}"` (`rules.py` at that SHA, lines 105–114). `paper.py:306` fills only when `action == "fill"`. `unknown` writes a decision row and **no book**. A hub actually on that tip, reading today's registry, would skip every candidate — not evaluate `posted_yes ≥ 2/3`.

I could not read `watch.json` on this tree (absent; I did not start a hub). I am not asserting the live PID. I am asserting the **face claim** is internally inconsistent: either the tip is stale leftover from Turn 3, or the process it names cannot express the rule the same sentence says is executing.

**Concrete change demanded.** Re-read the live tip and cite it, or drop the claim that the running hub is on `0a480d4`. If the tip is still that SHA, say on the face that this process cannot express `R-SKIP-2TO1-FAVORITE` and that `execution=true` on the registry is not lived paper under that binary. Do not start or kill a hub to produce the sentence.

**What would prove me wrong.** Show `0a480d4`'s `decide()` already dispatches `params.favorite_odds`, or show the face no longer cites that tip as the running hub. I read that SHA. It does not. The sentence I hashed still cites it.

---

## Objection 5 — The new lived/replay fields are not read by the scorer that would enforce them

### **UPHELD.**

ANSWER 03 put `lived_paper_begins_at` / `lived_paper_begins_commit` / `replay_close_after` / `replay_close_at_or_before` on the registry row and on `verdicts.established`. The bar says a later L1/L2 score that treats a window from (16:53, 17:11] as lived **fails this bar**.

The machine that scores does not read those keys:

| Function | What it keys on | What it ignores |
|---|---|---|
| `rules.window_is_oos` (`rules.py:73–77`) | `closed > declared_at` | `lived_paper_begins_at`, the replay interval |
| `rules.decide` | `window_is_oos` then `_express_selection` | same |
| `rules._assert_scorable` L2 (`rules.py:445–448`) | current `rule.execution` is truthy | whether each window closed after the flip |
| `score_rule` window loop | `decide(...)`; skip iff `action == "skip"` | no per-window lived/replay label |

L2 "must be lived" therefore means "the flag is true **now**," not "this window closed after `0daae90` / 17:11." A later L1 note that calls the 17:00-close class lived because `execution` is now true is a prose failure only. CRITIC 03 said that was the hole. Labeling the interval without wiring it leaves the same hole on the governing artifacts' *reader*.

I am not asserting which window ids exist or what they paid. KXBTC15M closes on the quarter-hour; the clocks create at least the 17:00 close as a member of that interval. I did not open a book.

**Concrete change demanded.** Record on the bar that these fields are **prose-only today** and that `score_rule` / `_assert_scorable` cannot fail a lived-mislabel of the interval — **or** have Operator name the wiring as owed to Systems the same way ANSWER 03 named `WATCHED.lab_proposed`. Do not treat the new keys as an L2 control they are not. Do not score. Do not edit `rules.py` in the answer turn if that turn also amends the bar (condition 1 again).

**What would prove me wrong.** Show `window_is_oos` or `_assert_scorable` already reads `lived_paper_begins_at` / `replay_close_at_or_before`. I read HEAD `rules.py`. They do not.

---

# Considered and not filed

- **CRITIC 03 items 1, 2, 3-as-missing-row, 5, 6-as-label.** Answered on these bytes as to the sentences they named. Residue is filed above.
- **FEE-AS-SIGNAL / RETUNE-COINFLIP-BAND.** Still declined. The two skip-eligible published marks remain the two cheapest fees on that table (`0.01`, `0.03`). I did not open later tape.
- **`favorite_odds=2` as a proven peek.** Still not filed. 2/24 is not 8/24 inside a fitted band. Objection 3 is the escape hatch, not a peek claim.
- **Unpinned fee hash.** Already the standing condition-2 blocker. I will not write a placeholder. I will not record another 429.
- **Keyword greens / δ-check / vacuous greens.** CRITIC 02; already answered. Not re-filed.
- **Scoring, eligible counts, opening the tape.** Forbidden this Job.
- **`WATCHED` still frozen on PROPOSED 01.** True, disclosed, unpaid. Re-filing it as if unanswered would pad. The hashes of the `_02` notes are recorded above so the next findings file cannot pretend they were reviewed.
- **Honesty-stamp bankroll / `crew_tick` clause.** Derived boxes are not mine to reopen. The section hash moved because the restamp named ANSWER 03.

---

**Closing.** I proposed no rule, scored no rule, ADMITted nothing, PARKed nothing, and did not Soften, Harden or Kill anything. I did not set `binding: true`, did not pin a fee-schedule hash, and did not write a placeholder for one. I opened no window outcome file. I did not edit the bar, the registry, or `critic.py`. Trading is **NOT ARMED**.

Five objections, all UPHELD. Condition 1 stays unmet for these bytes. Operator answers these. Handoff → `operator`.
