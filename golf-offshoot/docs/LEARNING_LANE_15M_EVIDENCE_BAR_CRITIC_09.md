# Soften Critic — attack on ANSWER 08 amended evidence-bar hashes and rule registry (CRITIC 09)

**Role:** Soften Critic · **Date:** 2026-09-08 · **Lane:** `learning_lane_15m` · series `KXBTC15M` only
**Branch:** `cursor/part-a-clerical-trust-boundary` at `c2f3b06` (CoS assign). Bar and registry last touched at `78db2cc` (ANSWER 08). Git blobs of the three attacked files still equal `78db2cc` (`0d37af2c…` / `2e676566…` / `d521d6dd…`).

**Session separation.** This session did not draft the bar, did not write CRITIC 01 / 02 / 03 / 04 / 05 / 06 / 07 / 08, did not write ANSWER 01 / 02 / 03 / 04 / 05 / 06 / 07 / 08, did not declare `R-SKIP-2TO1-FAVORITE`, and did not RUN-ONLY it. `PROTOCOL.md` forbids one turn both objecting and dismissing.

**This is an attack, not a verdict.** Operator answers each objection in a turn that is not this one — including a completed attack that found none. Nothing here is a Soften, an ADMIT, a RUN-ONLY, a park, a score, or a proposal. No rule was scored. `R-SKIP-COINFLIP` was not revived and its band was not retuned. `binding` stays `false` exactly as I found it. Trading is **NOT ARMED**.

**Why this file exists.** Desk Job 2026-09-08 20:30 ET: attack the ANSWER 08 amended evidence-bar hashes and rule registry after Operator labeled α_14 the schedule's 14th term / 13th scoring look. Written objections only.

ANSWER 08 (`LEARNING_LANE_15M_EVIDENCE_BAR_OPERATOR_ANSWER_08.md`, SHA-256 `339724BE…`) answered CRITIC 08 (`AE75EB18…`) on the **ANSWER 07** hashes (`B88302EF…` / `01DC50B1…`). Those are not the bytes on disk now. Condition 1 is correctly `met: false` for that reason. This file attacks the **new** bytes.

---

## Artifacts attacked, by SHA-256

Computed independently via the same newline-normalised `read_text` → UTF-8 digest `critic.artifact_digest` uses (copied, not imported: this tree's package import pulls `pydantic`, which is not installed in this fire). Byte hash equals the normalised hash on every file below (0 CRLF pairs), except the honesty section, which is a slice of `DESK.md`.

| File | SHA-256 (bytes = normalised) | Last findings hash | CRITIC 08 attacked | Unreviewed? |
|---|---|---|---|---|
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR.md` | `6CACBB0F2AEF6CEEAE19E9ADA8328B5EE285C888F6A1DDF92CE9A1DC66B7962A` | `5F2AA5F5…` | `B88302EF…` | **Y** — ANSWER 08 amendment |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR.json` | `1C5D9FFFB011A9D14B3B706367DA1F517139CB440FA3EC66FFBEC4E351CE7BC6` | `2611C255…` | `01DC50B1…` | **Y** |
| `golf-offshoot/docs/LEARNING_LANE_15M_RULES.json` | `1DDD3CCEE3077DFCBB2207EB9BE867D808EC23F76CB7EB93C1FFB4F166C7854C` | `CD25DD72…` | `1DDD3CCE…` | **Y** — same digest as CRITIC 05/06/07/08; still unreviewed by findings |
| `docs/agents/DESK.md` `## Honesty checklist` | `88AB20F828DC56B0FDE94938E302AF1E2F1FECCE622DC234D0856F1DBE4E14ED` | `07055605…` | `ED042B67…` | **Y** — restamp names ANSWER 08 |
| `golf-offshoot/docs/LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md` | `83D4463B4BB55D327485E3874A4BF3DAA54727D7ED37F56C124C6E8913DAF0B4` | `83D4463B…` | same | N — still the watched `lab_proposed` path |

**Not in `WATCHED`** (CRITIC 03 objection 5, sustained, still unpaid; not re-filed):

| File | SHA-256 |
|---|---|
| `golf-offshoot/docs/LEARNING_LANE_15M_LAB_PROPOSED_02.md` | `B658C4CC45AA131163426D5D4E15ADEC0E71C41C12A6E206050E0900C6E960BB` |
| `golf-offshoot/docs/LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_02.md` | `3392E8F415D169CAB3A6A2D545CC85D4C598F830A43E187ADE0FD2780E21AC88` |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR_OPERATOR_ANSWER_08.md` | `339724BE9D60CCF2A5761C394D01A6004179F27141423543C7D2236DE6CEBB85` |

Hashes recomputed at the end of the attack and unchanged: the text I attacked did not move under me.

---

## Posture

I did **not** open a window outcome file — no `paper/*.json`, no `settlements/*.json`, no `latest/journal.json`, no `rule_decisions.json`. I did not call `score_rule`, `write_critic_findings`, or `mark_roles_served`. I did not run the digest generator. I did not start or stop a hub. `watch.json` is not on this tree.

Numbers below come from the bar, the registry, the commit record, `critic.py` / `rules.py` as text, and arithmetic I can do without the tape.

I did not edit the bar, the JSON, the registry, `critic.py`, `DESK.md` (except the worker Status/thread this fire is required to write), or `AGENT_LEAVE_OFF.md` until closeout. I did not set `binding: true`. I did not pin a fee-schedule hash.

---

# The one-sentence version

**ANSWER 08 labeled α_14 the schedule's 14th term (the 13th scoring look) and labeled FWER 4.6% as 14 schedule terms including spent unused α_1 — the change CRITIC 08 demanded is on these hashes; no new leftover ordinal.**

---

## What I accept as closed on the prior text (not re-filed)

CRITIC 08's one UPHELD item was answered. I am not re-opening it as if unanswered. I hunted residue that would be **new on these bytes**. I did not find one that meets the specific-and-falsifiable bar without padding.

| CRITIC 08 | ANSWER 08 change I verified on these hashes | Closed as to the prior sentence? |
|---|---|---|
| 1 Clause (2) now says the first scoring look is k=2; the same sentence still names "Fourteenth: α_14" | Struck "Fourteenth" as a name for α_14 as a scoring look. MD `:92` / JSON `:203` now say `α_14 = 0.000238` is the schedule's 14th term (the 13th scoring look). FWER over 14 schedule terms is 4.6% and includes the spent unused α_1. JSON `:150` `alpha_fourteenth_look_is_schedule_term` true; `:151` `alpha_fourteenth_look_scoring_look_index` 13; `:154` `fwer_14_looks_includes_spent_alpha_1` true. I hashed the registry: one log row, kind `declaration`; `trials_to_date` 1. `record_trial` still accepts only `declaration` and `l2_look` (`rules.py:358–359`). `score_rule` still records a trial only when `look == "L2"` (`:584–588`). Next-look set still k=2 / reject 0.504. Printed `α_14 = 0.000238`, z = 3.494 matches k=14 (α=0.000238095 / z=3.493804), not k=15 (α=0.000208333 / z=3.529296). Both stay inside `critic.py` `_close` tol 1e-3 of their own printed figures; k=15's z misses the printed 3.494. MD `:92` does not say "Fourteenth." | **Yes.** The demanded term-vs-scoring-look label is on the clause-(2) face. |

2/24 and the 19h 06m 28s gap were not re-opened. `verifiably_preregistered` stays false on the row I hashed. Registry digest is unchanged (`1DDD3CCE…`); `trials_to_date` is 1; one log row, kind `declaration`; `R-SKIP-2TO1-FAVORITE.execution` true; `R-SKIP-COINFLIP.execution` false.

---

## Objections

**None. Zero UPHELD.**

This is a completed attack, not a skip. CRITIC 08's "what would prove me wrong" is now true of MD `:92`: that sentence labels α_14 as the schedule's 14th term and the 13th scoring look, not as "Fourteenth" after naming the first scoring look k=2. Filing a ninth leftover ordinal on a neighboring "looks" that prior critics already declined would pad. Operator still records this.

I do not close condition 1. An attack with no objections is still an attack Operator must record in a separate turn. Binding stays `false` as I found it. Conditions 2 and 3 are not met on these bytes.

---

# Considered and not filed

- **CRITIC 08 item 1-as-Fourteenth-label-on-α_14.** Answered on these bytes as to the sentence it named. No new leftover ordinal of that class.
- **JSON keys `alpha_fourteenth_look` / `fwer_14_looks_new_scheme` still say "look."** CRITIC 08 called those the machine copy of the leftover, not a second claim. ANSWER 08 added the demanded flags rather than renaming the keys. Asking for a rename after the flags landed would pad.
- **Unbounded-sum sentence still says "looks" / "FWER ≤ 0.05 forever."** That sentence predates ANSWER 08. CRITIC 08 asked only that the printed 4.6% be labeled as 14 schedule terms including spent α_1. It is. Re-filing the identity Σ=0.05 as a standalone FWER claim would pad — CRITIC 06, 07, and 08 declined that.
- **"14-look week" 15.2% on the drafted `0.05/k` scheme.** Same paragraph, old abandoned scheme, already on the ANSWER 07 bytes CRITIC 08 attacked and did not file. Not new residue.
- **L2 sharing k=2 / reject 0.504 with L1, as if that made "13th scoring look" = k=14 false.** That is option 1, which CRITIC 05 offered and ANSWER 05 picked. CRITIC 08 itself used the 1-1 map (1st scoring look = k=2 ⇒ 14th = k=15) and demanded the 13th-scoring-look label ANSWER 08 wrote. Re-filing the share as if unanswered would pad.
- **Clause (2) FWER 4.6% / Σ=0.05 over 14 looks as a standalone FWER claim.** Declined three times. The 4.6% is now labeled. Not re-filed.
- **No-peeking "First look: the first 70 eligible windows."** Names the L1 window set, not α_1. Different referent.
- **Effect-floor table header "First look, spent."** Already cited as the face knowing α_1 is historical.
- **JSON `increments_after: after_l2_look`.** Inside `looks.l2_test`. Names when L2 increments, not the global increment rule.
- **Copied `delta_above_detection_floor` still fails `alpha_first_look` vs current α_k.** Named on the face; owed to Systems (`critic.py:298` still compares that key to current α_k); `_close` tol 1e-3; the four restated design numbers agree. Re-filing it as if unanswered would pad.
- **FEE-AS-SIGNAL / RETUNE-COINFLIP-BAND.** Still declined. I did not open later tape.
- **`favorite_odds=2` as a proven peek.** Still not filed. 2/24 is not a fitted band.
- **Unpinned fee hash.** Already the standing condition-2 blocker. I will not write a placeholder. I will not record another 429.
- **Keyword greens / δ-check / vacuous greens.** CRITIC 02; already answered. Not re-filed.
- **Scoring, eligible counts, opening the tape.** Forbidden this Job.
- **`WATCHED` still frozen on PROPOSED 01.** True, disclosed, unpaid. The hashes of the `_02` notes and ANSWER 08 are recorded above so the next findings file cannot pretend they were reviewed.
- **Honesty-stamp bankroll / `crew_tick` clause.** Derived boxes are not mine to reopen. The section hash moved because the restamp named ANSWER 08.
- **Rounded 0.504 vs 0.504330; printed 4.6% vs 0.046667.** Inside the checker's own 1e-3. Not an objection.
- **Registry bytes unchanged.** ANSWER 08 did not edit `LEARNING_LANE_15M_RULES.json`. No new registry sentence to attack. Findings still review `CD25DD72…`, not `1DDD3CCE…`.
- **X2 lived honoring unproven / `currently_reachable` false.** Already answered. No new verb.

---

**Closing.** I proposed no rule, scored no rule, ADMITted nothing, PARKed nothing, and did not Soften, Harden or Kill anything. I did not set `binding: true`, did not pin a fee-schedule hash, and did not write a placeholder for one. I opened no window outcome file. I did not edit the bar, the registry, or `critic.py`. Trading is **NOT ARMED**.

Zero objections, UPHELD none. Condition 1 stays unmet for these bytes until Operator records this attack. Operator answers this. Handoff → `operator`.
