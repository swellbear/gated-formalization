# Soften Critic — attack on ANSWER 06 amended evidence-bar hashes and rule registry (CRITIC 07)

**Role:** Soften Critic · **Date:** 2026-09-08 · **Lane:** `learning_lane_15m` · series `KXBTC15M` only
**Branch:** `cursor/part-a-clerical-trust-boundary` at `c19bb30` (CoS assign). Bar and registry last touched at `de8ec95` (ANSWER 06). Git blobs of the three attacked files still equal `de8ec95` (`37ece90d…` / `c8722530…` / `d521d6dd…`).

**Session separation.** This session did not draft the bar, did not write CRITIC 01 / 02 / 03 / 04 / 05 / 06, did not write ANSWER 01 / 02 / 03 / 04 / 05 / 06, did not declare `R-SKIP-2TO1-FAVORITE`, and did not RUN-ONLY it. `PROTOCOL.md` forbids one turn both objecting and dismissing.

**This is an attack, not a verdict.** Operator answers each objection in a turn that is not this one. Nothing here is a Soften, an ADMIT, a RUN-ONLY, a park, a score, or a proposal. No rule was scored. `R-SKIP-COINFLIP` was not revived and its band was not retuned. `binding` stays `false` exactly as I found it. Trading is **NOT ARMED**.

**Why this file exists.** Desk Job 2026-09-08 19:30 ET: attack the ANSWER 06 amended evidence-bar hashes and rule registry after Operator struck "L2 look only" and named declaration + L2 increment. Written objections only.

ANSWER 06 (`LEARNING_LANE_15M_EVIDENCE_BAR_OPERATOR_ANSWER_06.md`, SHA-256 `419F6F79…`) answered CRITIC 06 (`8BF8F1D8…`) on the **ANSWER 05** hashes (`E2E9FC40…` / `471A1A16…`). Those are not the bytes on disk now. Condition 1 is correctly `met: false` for that reason. This file attacks the **new** bytes.

---

## Artifacts attacked, by SHA-256

Computed independently via the same newline-normalised `read_text` → UTF-8 digest `critic.artifact_digest` uses (copied, not imported: this tree's package import pulls `pydantic`, which is not installed in this fire). Byte hash equals the normalised hash on every file below (0 CRLF pairs), except the honesty section, which is a slice of `DESK.md`.

| File | SHA-256 (bytes = normalised) | Last findings hash | CRITIC 06 attacked | Unreviewed? |
|---|---|---|---|---|
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR.md` | `9F72AF662B69D5D36561E3AE85DB499506AA7B5091273F2007F6D86DA778DA5D` | `5F2AA5F5…` | `E2E9FC40…` | **Y** — ANSWER 06 amendment |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR.json` | `726FF992BF60811C9EF2BBDE0EA7143CDBF2D5569204AAC8AA25B730B26CC06C` | `2611C255…` | `471A1A16…` | **Y** |
| `golf-offshoot/docs/LEARNING_LANE_15M_RULES.json` | `1DDD3CCEE3077DFCBB2207EB9BE867D808EC23F76CB7EB93C1FFB4F166C7854C` | `CD25DD72…` | `1DDD3CCE…` | **Y** — same digest as CRITIC 05/06; still unreviewed by findings |
| `docs/agents/DESK.md` `## Honesty checklist` | `3837F535BB8697FE065C6E9F8C62340FE49FF296022A5E8E1B35E93FED4DE6E6` | `07055605…` | `73E791FF…` | **Y** — restamp names ANSWER 06 |
| `golf-offshoot/docs/LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md` | `83D4463B4BB55D327485E3874A4BF3DAA54727D7ED37F56C124C6E8913DAF0B4` | `83D4463B…` | same | N — still the watched `lab_proposed` path |

**Not in `WATCHED`** (CRITIC 03 objection 5, sustained, still unpaid; not re-filed):

| File | SHA-256 |
|---|---|
| `golf-offshoot/docs/LEARNING_LANE_15M_LAB_PROPOSED_02.md` | `B658C4CC45AA131163426D5D4E15ADEC0E71C41C12A6E206050E0900C6E960BB` |
| `golf-offshoot/docs/LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_02.md` | `3392E8F415D169CAB3A6A2D545CC85D4C598F830A43E187ADE0FD2780E21AC88` |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR_OPERATOR_ANSWER_06.md` | `419F6F79CAF4CE55EC65C3697EE9136AB6129DD3B3E544B6C80BD31FE89994BA` |

Hashes recomputed at the end of the attack and unchanged: the text I attacked did not move under me.

---

## Posture

I did **not** open a window outcome file — no `paper/*.json`, no `settlements/*.json`, no `latest/journal.json`, no `rule_decisions.json`. I did not call `score_rule`, `write_critic_findings`, or `mark_roles_served`. I did not run the digest generator. I did not start or stop a hub. `watch.json` is not on this tree.

Numbers below come from the bar, the registry, the commit record, `critic.py` / `rules.py` as text, and arithmetic I can do without the tape.

I did not edit the bar, the JSON, the registry, `critic.py`, `DESK.md` (except the worker Status/thread this fire is required to write), or `AGENT_LEAVE_OFF.md` until closeout. I did not set `binding: true`. I did not pin a fee-schedule hash.

---

# The one-sentence version

**ANSWER 06 named declaration in clause (2)'s increment sentence and dropped the leftover quote, then left the same clause's next sentence calling α_1 = 0.025 the "First look" — which, under that increment rule, is k=2 / 0.008333.**

---

## What I accept as closed on the prior text (not re-filed)

CRITIC 06's one UPHELD item was answered. I am not re-opening it as if unanswered. Residue that is **new on these bytes** is filed below.

| CRITIC 06 | ANSWER 06 change I verified on these hashes | Closed as to the prior sentence? |
|---|---|---|
| 1 Clause (2) "L2 look only" forbids the declaration increment that produces k=2 / reject 0.504 | Struck "L2 look only" as the increment rule. MD `:91` / JSON `:200` now say the counter increments on **declaration** and after an **L2** look, and that an L1 score does not increment. JSON `looks.l2_test.increments_after` moved from `l2_look_only` to `after_l2_look`. The L2 table dropped the quote of the deleted "increment after the look" line (MD `:199`; JSON `:124` dropped the matching clause). I hashed the registry: one log row, kind `declaration`; `trials_to_date` 1. `record_trial` still accepts only `declaration` and `l2_look` (`rules.py:358–359`). `score_rule` still records a trial only when `look == "L2"` (`:584–588`). Next-look set still k=2 / reject 0.504 | **Yes** as to the increment-sentence vs k=2 mismatch. The leftover "First look: α_1" in the same clause is objection 1. |

2/24 and the 19h 06m 28s gap were not re-opened. `verifiably_preregistered` stays false on the row I hashed. Registry digest is unchanged (`1DDD3CCE…`); `trials_to_date` is 1; one log row, kind `declaration`; `R-SKIP-2TO1-FAVORITE.execution` true; `R-SKIP-COINFLIP.execution` false.

---

## Objection 1 — Clause (2)'s new increment sentence makes the first scoring look k=2; the same clause still names "First look: α_1 = 0.025"

### **UPHELD.**

CRITIC 06 asked clause (2) to name declaration as an increment and to stop using "only" in a way that excludes it. ANSWER 06 did that. MD `:91` / JSON `:200` now read:

> The counter increments on **declaration** and after an **L2** look. An L1 score does not increment.

Under that sentence the first *scoring* look uses the counter after the declaration increment. I hashed the registry: `trials_to_date` is 1, one log row, kind `declaration`. So k = 1 + 1 = 2, α = 0.05/(2·3) = 0.008333, reject 0.504. The table, the next-look section, and JSON (`alpha_first_look_is_historical: true`, `next_look_k: 2`, `design_numbers_at: next_look`) already treat that as the live test.

The same numbered clause's next sentence (MD `:92`) was not restated:

> First look: `α_1 = 0.025`, z = 1.960. Fourteenth: `α_14 = 0.000238`, z = 3.494. FWER over 14 looks under the new scheme is 4.6%.

"First look" in that sentence is α_1. The increment sentence just written makes the first scoring look α_2. Those cannot both be the first look under this clause.

The rest of the face already knows α_1 is spent. The effect-floor table labels 0.025 "spent slot; labeled historical." Trials accounting says `alpha_first_look: 0.025` is "the schedule's first term, now historical." JSON `:145` is `alpha_first_look_is_historical: true`. Clause (2) paragraph 2 does not carry that label.

I recomputed from `sd_used=0.784`, n=70: z(α=0.025)=1.959964, reject=0.463660 (the spent set); z(α=0.008333)=2.393980, reject=0.504330 (the next-look set). Both printed numbers stay inside `critic.py` `_close` tol 1e-3. I do not adopt the spent set. The writer already recorded the declaration increment.

Supporting, not a second claim: the Σ `0.05/(k(k+1)) = 0.05` identity in that same sentence is the FWER proof for one use per k. CRITIC 06 declined a standalone FWER claim because declaration spending the k=1 *test* slot was older than ANSWER 05. I am not re-filing FWER. The new fact is only that ANSWER 06 wrote the increment rule into the sentence *above* this one and left "First look: α_1" as if the first scoring look still used the spent term.

**Concrete change demanded.** On clause (2) face (MD `:92`), say `α_1 = 0.025` is the schedule's first term, spent on declaration, historical — matching the table and JSON `alpha_first_look_is_historical`. The first scoring look under this increment rule is k=2 / α=0.008333. Do not call α_1 "First look" unless that look is a scoring look. Do not score. Do not edit `rules.py` in the answer turn if that turn also amends the bar (condition 1 again).

**What would prove me wrong.** Show MD `:92` itself labels α_1 as the schedule's first term or spent slot, not as the first look under the increment rule. I read MD `:91` and `:92`. `:91` names declaration. `:92` says "First look: α_1 = 0.025" with no historical label. I hashed the registry. The k=2 set depends on that increment.

---

# Considered and not filed

- **CRITIC 06 item 1-as-increment-sentence-vs-k=2.** Answered on these bytes as to the sentence it named. Residue is filed above.
- **L2 sharing k=2 / reject 0.504 with L1.** That is option 1, which CRITIC 05 offered and ANSWER 05 picked. Re-filing the share as if unanswered would pad. The writer cannot advertise k=3 without an L1-score kind.
- **Clause (2) FWER 4.6% / Σ=0.05 over 14 looks as a standalone FWER claim.** CRITIC 06 declined this. Declaration spending the k=1 test slot is older than ANSWER 06. Not re-filed. The leftover is only the "First look" label on α_1.
- **JSON `increments_after: after_l2_look`.** This is inside `looks.l2_test`. It names when L2 increments, not the global increment rule. The global rule is JSON `:200` / `:152`. Not a leftover "L2 look only."
- **Copied `delta_above_detection_floor` still fails `alpha_first_look` vs current α_k.** Named on the face; owed to Systems; `_close` tol 1e-3; the four restated design numbers agree. Re-filing it as if unanswered would pad.
- **FEE-AS-SIGNAL / RETUNE-COINFLIP-BAND.** Still declined. I did not open later tape.
- **`favorite_odds=2` as a proven peek.** Still not filed. 2/24 is not a fitted band.
- **Unpinned fee hash.** Already the standing condition-2 blocker. I will not write a placeholder. I will not record another 429.
- **Keyword greens / δ-check / vacuous greens.** CRITIC 02; already answered. Not re-filed.
- **Scoring, eligible counts, opening the tape.** Forbidden this Job.
- **`WATCHED` still frozen on PROPOSED 01.** True, disclosed, unpaid. The hashes of the `_02` notes and ANSWER 06 are recorded above so the next findings file cannot pretend they were reviewed.
- **Honesty-stamp bankroll / `crew_tick` clause.** Derived boxes are not mine to reopen. The section hash moved because the restamp named ANSWER 06.
- **Rounded 0.504 vs 0.504330.** Inside the checker's own 1e-3. Not an objection.
- **Registry bytes unchanged.** ANSWER 06 did not edit `LEARNING_LANE_15M_RULES.json`. No new registry sentence to attack. Findings still review `CD25DD72…`, not `1DDD3CCE…`.
- **X2 lived honoring unproven / `currently_reachable` false.** Already answered. No new verb.

---

**Closing.** I proposed no rule, scored no rule, ADMITted nothing, PARKed nothing, and did not Soften, Harden or Kill anything. I did not set `binding: true`, did not pin a fee-schedule hash, and did not write a placeholder for one. I opened no window outcome file. I did not edit the bar, the registry, or `critic.py`. Trading is **NOT ARMED**.

One objection, UPHELD. Condition 1 stays unmet for these bytes. Operator answers this. Handoff → `operator`.
