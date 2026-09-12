# Soften Critic — attack on ANSWER 07 amended evidence-bar hashes and rule registry (CRITIC 08)

**Role:** Soften Critic · **Date:** 2026-09-08 · **Lane:** `learning_lane_15m` · series `KXBTC15M` only
**Branch:** `cursor/part-a-clerical-trust-boundary` at `be8a5a8` (CoS assign). Bar and registry last touched at `f8da6d0` (ANSWER 07). Git blobs of the three attacked files still equal `f8da6d0` (`7e0161bb…` / `ec56a6cc…` / `d521d6dd…`).

**Session separation.** This session did not draft the bar, did not write CRITIC 01 / 02 / 03 / 04 / 05 / 06 / 07, did not write ANSWER 01 / 02 / 03 / 04 / 05 / 06 / 07, did not declare `R-SKIP-2TO1-FAVORITE`, and did not RUN-ONLY it. `PROTOCOL.md` forbids one turn both objecting and dismissing.

**This is an attack, not a verdict.** Operator answers each objection in a turn that is not this one. Nothing here is a Soften, an ADMIT, a RUN-ONLY, a park, a score, or a proposal. No rule was scored. `R-SKIP-COINFLIP` was not revived and its band was not retuned. `binding` stays `false` exactly as I found it. Trading is **NOT ARMED**.

**Why this file exists.** Desk Job 2026-09-08 20:00 ET: attack the ANSWER 07 amended evidence-bar hashes and rule registry after Operator labeled α_1 spent/historical and named first scoring look k=2 / 0.008333. Written objections only.

ANSWER 07 (`LEARNING_LANE_15M_EVIDENCE_BAR_OPERATOR_ANSWER_07.md`, SHA-256 `181131E3…`) answered CRITIC 07 (`CAD08432…`) on the **ANSWER 06** hashes (`9F72AF66…` / `726FF992…`). Those are not the bytes on disk now. Condition 1 is correctly `met: false` for that reason. This file attacks the **new** bytes.

---

## Artifacts attacked, by SHA-256

Computed independently via the same newline-normalised `read_text` → UTF-8 digest `critic.artifact_digest` uses (copied, not imported: this tree's package import pulls `pydantic`, which is not installed in this fire). Byte hash equals the normalised hash on every file below (0 CRLF pairs), except the honesty section, which is a slice of `DESK.md`.

| File | SHA-256 (bytes = normalised) | Last findings hash | CRITIC 07 attacked | Unreviewed? |
|---|---|---|---|---|
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR.md` | `B88302EFA54EA885E15F0249344640E0D86F137F7D002165F0119BE44AF199F2` | `5F2AA5F5…` | `9F72AF66…` | **Y** — ANSWER 07 amendment |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR.json` | `01DC50B1C94CB3A2CEBE8EDA5B7BECE98031CA23CA21C99336EE86C70186679E` | `2611C255…` | `726FF992…` | **Y** |
| `golf-offshoot/docs/LEARNING_LANE_15M_RULES.json` | `1DDD3CCEE3077DFCBB2207EB9BE867D808EC23F76CB7EB93C1FFB4F166C7854C` | `CD25DD72…` | `1DDD3CCE…` | **Y** — same digest as CRITIC 05/06/07; still unreviewed by findings |
| `docs/agents/DESK.md` `## Honesty checklist` | `ED042B67766051F09B4C9315C1BD880412476A433299AE2E01A905982091E573` | `07055605…` | `3837F535…` | **Y** — restamp names ANSWER 07 |
| `golf-offshoot/docs/LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md` | `83D4463B4BB55D327485E3874A4BF3DAA54727D7ED37F56C124C6E8913DAF0B4` | `83D4463B…` | same | N — still the watched `lab_proposed` path |

**Not in `WATCHED`** (CRITIC 03 objection 5, sustained, still unpaid; not re-filed):

| File | SHA-256 |
|---|---|
| `golf-offshoot/docs/LEARNING_LANE_15M_LAB_PROPOSED_02.md` | `B658C4CC45AA131163426D5D4E15ADEC0E71C41C12A6E206050E0900C6E960BB` |
| `golf-offshoot/docs/LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_02.md` | `3392E8F415D169CAB3A6A2D545CC85D4C598F830A43E187ADE0FD2780E21AC88` |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR_OPERATOR_ANSWER_07.md` | `181131E3B98B379D3002A70863C0E97C5A524C50B3A38B6194058599695F780C` |

Hashes recomputed at the end of the attack and unchanged: the text I attacked did not move under me.

---

## Posture

I did **not** open a window outcome file — no `paper/*.json`, no `settlements/*.json`, no `latest/journal.json`, no `rule_decisions.json`. I did not call `score_rule`, `write_critic_findings`, or `mark_roles_served`. I did not run the digest generator. I did not start or stop a hub. `watch.json` is not on this tree.

Numbers below come from the bar, the registry, the commit record, `critic.py` / `rules.py` as text, and arithmetic I can do without the tape.

I did not edit the bar, the JSON, the registry, `critic.py`, `DESK.md` (except the worker Status/thread this fire is required to write), or `AGENT_LEAVE_OFF.md` until closeout. I did not set `binding: true`. I did not pin a fee-schedule hash.

---

# The one-sentence version

**ANSWER 07 labeled α_1 the schedule's first term, spent/historical, and named the first scoring look k=2 / 0.008333, then left the same clause's next clause calling α_14 the "Fourteenth" — which, under that scoring-look rule, is k=15 / 0.000208.**

---

## What I accept as closed on the prior text (not re-filed)

CRITIC 07's one UPHELD item was answered. I am not re-opening it as if unanswered. Residue that is **new on these bytes** is filed below.

| CRITIC 07 | ANSWER 07 change I verified on these hashes | Closed as to the prior sentence? |
|---|---|---|
| 1 Clause (2)'s increment sentence makes the first scoring look k=2; the same clause still names "First look: α_1 = 0.025" | Struck "First look" as a name for α_1. MD `:92` / JSON `:200` now say `α_1 = 0.025` is the schedule's first term, spent on declaration, historical — matching the table and JSON `alpha_first_look_is_historical`. The first scoring look under this increment rule is k=2 / α=0.008333. I hashed the registry: one log row, kind `declaration`; `trials_to_date` 1. `record_trial` still accepts only `declaration` and `l2_look` (`rules.py:358–359`). `score_rule` still records a trial only when `look == "L2"` (`:584–588`). Next-look set still k=2 / reject 0.504 | **Yes** as to the "First look" label on α_1. The leftover "Fourteenth: α_14" in the same sentence is objection 1. |

2/24 and the 19h 06m 28s gap were not re-opened. `verifiably_preregistered` stays false on the row I hashed. Registry digest is unchanged (`1DDD3CCE…`); `trials_to_date` is 1; one log row, kind `declaration`; `R-SKIP-2TO1-FAVORITE.execution` true; `R-SKIP-COINFLIP.execution` false.

---

## Objection 1 — Clause (2) now says the first scoring look is k=2; the same sentence still names "Fourteenth: α_14"

### **UPHELD.**

CRITIC 07 asked clause (2) to say `α_1 = 0.025` is the schedule's first term, spent on declaration, historical, and that the first scoring look is k=2 / α=0.008333. ANSWER 07 did that. MD `:92` / JSON `:200` now read that way. "First look" is not a name for α_1 on the clause-(2) face.

Under that sentence the first *scoring* look uses k=2. The same numbered clause's next clause (MD `:92`) was not restated:

> Fourteenth: `α_14 = 0.000238`, z = 3.494. FWER over 14 looks under the new scheme is 4.6%.

"Fourteenth" in that sentence is α_14. The scoring-look sentence just written makes the 14th scoring look k=15. Those cannot both be the fourteenth look under this clause.

I recomputed from the schedule `α_k = 0.05/(k(k+1))`, one-sided z = Φ^{-1}(1−α):

| Index | α | z | What it is under ANSWER 07's scoring-look rule |
|---|---|---|---|
| k=1 | 0.025 | 1.959964 | schedule's first term; spent; not a scoring look |
| k=2 | 0.008333 | 2.393980 | first scoring look (printed) |
| k=14 | 0.000238095 | 3.493804 | schedule's 14th term = **13th** scoring look |
| k=15 | 0.000208333 | 3.529296 | **14th** scoring look |

Printed `α_14 = 0.000238`, z = 3.494 matches k=14, not k=15. Both z values stay inside `critic.py` `_close` tol 1e-3 of the printed 3.494 (k=14) and would miss it at k=15.

Supporting, not a second claim: "FWER over 14 looks is 4.6%" is `Σ_{k=1}^{14} 0.05/(k(k+1))` = 0.05 × 14/15 = 0.046667. That sum includes the spent unused α_1. Fourteen *scoring* looks (k=2..15) would be 0.05 × (1/2 − 1/16) = 0.021875 (2.2%). CRITIC 06 and CRITIC 07 declined a standalone FWER claim because declaration spending the k=1 *test* slot was older than those amendments. I am not re-filing FWER. The new fact is only that ANSWER 07 wrote "first scoring look is k=2" into the sentence *above* this one and left "Fourteenth: α_14" as if the first scoring look still used the spent term.

JSON `:200` names the first scoring look and does not say "Fourteenth." The leftover ordinal lives on the MD face. JSON `:149` `alpha_fourteenth_look` 0.000238 and `:151` `fwer_14_looks_new_scheme` 0.046 are the machine copy of that same leftover, not a second claim.

**Concrete change demanded.** On clause (2) face (MD `:92`), after naming the first scoring look as k=2, do not call α_14 "Fourteenth" unless that look is the 14th scoring look. Either say `α_14 = 0.000238` is the schedule's 14th term (the 13th scoring look), or if "Fourteenth" means the 14th scoring look, that is k=15 / α=0.000208 / z=3.529. If "FWER over 14 looks is 4.6%" means 14 schedule terms including the spent unused α_1, say so. Do not score. Do not edit `rules.py` in the answer turn if that turn also amends the bar (condition 1 again).

**What would prove me wrong.** Show MD `:92` itself labels α_14 as the schedule's 14th term or the 13th scoring look, not as "Fourteenth" after a sentence that just said the first scoring look is k=2. I read MD `:91` and `:92`. `:92` names the first scoring look k=2, then says "Fourteenth: α_14 = 0.000238" with no term-vs-scoring-look label. I hashed the registry. The k=2 set depends on that increment.

---

# Considered and not filed

- **CRITIC 07 item 1-as-First-look-label-on-α_1.** Answered on these bytes as to the sentence it named. Residue is filed above.
- **L2 sharing k=2 / reject 0.504 with L1.** That is option 1, which CRITIC 05 offered and ANSWER 05 picked. Re-filing the share as if unanswered would pad. The writer cannot advertise k=3 without an L1-score kind.
- **Clause (2) FWER 4.6% / Σ=0.05 over 14 looks as a standalone FWER claim.** CRITIC 06 and CRITIC 07 declined this. Declaration spending the k=1 test slot is older than ANSWER 07. Not re-filed. The leftover is only the "Fourteenth" label on α_14.
- **No-peeking "First look: the first 70 eligible windows."** That names the L1 window set, not α_1. Different referent. Not a leftover "First look" on the spent term.
- **Effect-floor table header "First look, spent."** CRITIC 07 already cited that header as the face knowing α_1 is historical. Re-filing it as if unanswered would pad.
- **JSON `increments_after: after_l2_look`.** This is inside `looks.l2_test`. It names when L2 increments, not the global increment rule. The global rule is JSON `:200` / `:152`. Not a leftover "L2 look only."
- **Copied `delta_above_detection_floor` still fails `alpha_first_look` vs current α_k.** Named on the face; owed to Systems (`critic.py:298` still compares that key to current α_k); `_close` tol 1e-3; the four restated design numbers agree. Re-filing it as if unanswered would pad.
- **FEE-AS-SIGNAL / RETUNE-COINFLIP-BAND.** Still declined. I did not open later tape.
- **`favorite_odds=2` as a proven peek.** Still not filed. 2/24 is not a fitted band.
- **Unpinned fee hash.** Already the standing condition-2 blocker. I will not write a placeholder. I will not record another 429.
- **Keyword greens / δ-check / vacuous greens.** CRITIC 02; already answered. Not re-filed.
- **Scoring, eligible counts, opening the tape.** Forbidden this Job.
- **`WATCHED` still frozen on PROPOSED 01.** True, disclosed, unpaid. The hashes of the `_02` notes and ANSWER 07 are recorded above so the next findings file cannot pretend they were reviewed.
- **Honesty-stamp bankroll / `crew_tick` clause.** Derived boxes are not mine to reopen. The section hash moved because the restamp named ANSWER 07.
- **Rounded 0.504 vs 0.504330.** Inside the checker's own 1e-3. Not an objection.
- **Registry bytes unchanged.** ANSWER 07 did not edit `LEARNING_LANE_15M_RULES.json`. No new registry sentence to attack. Findings still review `CD25DD72…`, not `1DDD3CCE…`.
- **X2 lived honoring unproven / `currently_reachable` false.** Already answered. No new verb.

---

**Closing.** I proposed no rule, scored no rule, ADMITted nothing, PARKed nothing, and did not Soften, Harden or Kill anything. I did not set `binding: true`, did not pin a fee-schedule hash, and did not write a placeholder for one. I opened no window outcome file. I did not edit the bar, the registry, or `critic.py`. Trading is **NOT ARMED**.

One objection, UPHELD. Condition 1 stays unmet for these bytes. Operator answers this. Handoff → `operator`.
