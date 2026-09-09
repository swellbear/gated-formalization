# Soften Critic — attack on ANSWER 09 amended evidence-bar hashes and rule registry (CRITIC 10)

**Role:** Soften Critic · **Date:** 2026-09-08 · **Lane:** `learning_lane_15m` · series `KXBTC15M` only
**Branch:** `cursor/part-a-clerical-trust-boundary` at `5881980` (CoS assign). Bar and registry last touched at `818e268` (ANSWER 09). Git blobs of the three attacked files still equal `818e268` (`d05bd1f1…` / `7eee23c6…` / `d521d6dd…`).

**Session separation.** This session did not draft the bar, did not write CRITIC 01 / 02 / 03 / 04 / 05 / 06 / 07 / 08 / 09, did not write ANSWER 01 / 02 / 03 / 04 / 05 / 06 / 07 / 08 / 09, did not declare `R-SKIP-2TO1-FAVORITE`, and did not RUN-ONLY it. `PROTOCOL.md` forbids one turn both objecting and dismissing.

**This is an attack, not a verdict.** Operator answers each objection in a turn that is not this one — including a completed attack that found none. Nothing here is a Soften, an ADMIT, a RUN-ONLY, a park, a score, or a proposal. No rule was scored. `R-SKIP-COINFLIP` was not revived and its band was not retuned. `binding` stays `false` exactly as I found it. Trading is **NOT ARMED**.

**Why this file exists.** Desk Job 2026-09-08 21:01 ET: attack the ANSWER 09 amended evidence-bar hashes and rule registry after Operator recorded CRITIC 09 (zero UPHELD; condition 1 unmet on the link-amendment bytes). Written objections only.

ANSWER 09 (`LEARNING_LANE_15M_EVIDENCE_BAR_OPERATOR_ANSWER_09.md`, SHA-256 `A5206872…`) recorded CRITIC 09 (`CDEC94C5…`) on the **ANSWER 08** hashes (`6CACBB0F…` / `1C5D9FFF…`). Those are not the bytes on disk now. Condition 1 is correctly `met: false` for that reason. This file attacks the **new** bytes.

---

## Artifacts attacked, by SHA-256

Computed independently via the same newline-normalised `read_text` → UTF-8 digest `critic.artifact_digest` uses (copied, not imported: this tree's package import pulls `pydantic`, which is not installed in this fire). Byte hash equals the normalised hash on every file below (0 CRLF pairs), except the honesty section, which is a slice of `DESK.md`.

| File | SHA-256 (bytes = normalised) | Last findings hash | CRITIC 09 attacked | Unreviewed? |
|---|---|---|---|---|
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR.md` | `DC46EFA6033F31F13E58C7A403B71E5E0C9F176B2CFFCFCFDE71EDF80535E9B4` | `5F2AA5F5…` | `6CACBB0F…` | **Y** — ANSWER 09 link-amendment |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR.json` | `B6DDDB6BCC2825B345CAF63245C664B2F128BCB8005EBBF6AFEF2E403BE81EB2` | `2611C255…` | `1C5D9FFF…` | **Y** |
| `golf-offshoot/docs/LEARNING_LANE_15M_RULES.json` | `1DDD3CCEE3077DFCBB2207EB9BE867D808EC23F76CB7EB93C1FFB4F166C7854C` | `CD25DD72…` | `1DDD3CCE…` | **Y** — same digest as CRITIC 05/06/07/08/09; still unreviewed by findings |
| `docs/agents/DESK.md` `## Honesty checklist` | `CF0FEAB2D5F47235C6C248DA7AFE3DC2D18CFAB25DEC7218D2DEF0D530D013B3` | `07055605…` | `88AB20F8…` | **Y** — restamp names ANSWER 09 / this assign |
| `golf-offshoot/docs/LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md` | `83D4463B4BB55D327485E3874A4BF3DAA54727D7ED37F56C124C6E8913DAF0B4` | `83D4463B…` | same | N — still the watched `lab_proposed` path |

Honesty slice is the committed `5881980` section (this fire's Status/thread writes do not touch it). ANSWER 09's own honesty slice at `818e268` was `604DDE81…`.

**Not in `WATCHED`** (CRITIC 03 objection 5, sustained, still unpaid; not re-filed):

| File | SHA-256 |
|---|---|
| `golf-offshoot/docs/LEARNING_LANE_15M_LAB_PROPOSED_02.md` | `B658C4CC45AA131163426D5D4E15ADEC0E71C41C12A6E206050E0900C6E960BB` |
| `golf-offshoot/docs/LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_02.md` | `3392E8F415D169CAB3A6A2D545CC85D4C598F830A43E187ADE0FD2780E21AC88` |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR_OPERATOR_ANSWER_09.md` | `A520687276F0294618C32E74DCEF72C5F70A165A1F13E283422FF06E57D869B6` |

Hashes recomputed at the end of the attack and unchanged: the text I attacked did not move under me.

---

## Posture

I did **not** open a window outcome file — no `paper/*.json`, no `settlements/*.json`, no `latest/journal.json`, no `rule_decisions.json`. I did not call `score_rule`, `write_critic_findings`, or `mark_roles_served`. I did not run the digest generator. I did not start or stop a hub. `watch.json` is not on this tree.

Numbers below come from the bar, the registry, the commit record, `critic.py` / `rules.py` as text, and arithmetic I can do without the tape.

I did not edit the bar, the JSON, the registry, `critic.py`, `DESK.md` (except the worker Status/thread this fire is required to write), or `AGENT_LEAVE_OFF.md` until closeout. I did not set `binding: true`. I did not pin a fee-schedule hash.

---

# The one-sentence version

**ANSWER 09 recorded CRITIC 09 (zero UPHELD) on the ANSWER 08 hashes by linking the pair — no clause-(2) face change; CRITIC 08's demanded α_14 term/scoring-look label remains on these hashes; no new leftover ordinal.**

---

## What I accept as closed on the prior text (not re-filed)

CRITIC 09's completed attack (zero UPHELD) was recorded. I am not re-opening it as if unanswered. I hunted residue that would be **new on these bytes**. I did not find one that meets the specific-and-falsifiable bar without padding.

| CRITIC 09 | ANSWER 09 change I verified on these hashes | Closed as to the prior sentence? |
|---|---|---|
| Zero UPHELD. CRITIC 08's demanded α_14 term-vs-scoring-look label is on the ANSWER 08 hashes | Link-amendment only. `amended_at` → 21:00; condition 1 names this pair and the ANSWER 08 hashes (`6CACBB0F…` / `1C5D9FFF…`); JSON `upheld` 0; `prior_amendment` = ANSWER 08 at `78db2cc`. No clause-(2) edit. MD `:92` / JSON `:203` still say `α_14 = 0.000238` is the schedule's 14th term (the 13th scoring look). MD `:92` does not say "Fourteenth." JSON `:150` `alpha_fourteenth_look_is_schedule_term` true; `:151` `alpha_fourteenth_look_scoring_look_index` 13; `:154` `fwer_14_looks_includes_spent_alpha_1` true. I hashed the registry: one log row, kind `declaration`; `trials_to_date` 1; digest still `1DDD3CCE…`. `record_trial` still accepts only `declaration` and `l2_look` (`rules.py:358–359`). `score_rule` still records a trial only when `look == "L2"` (`:584–588`). Next-look set still k=2 / reject 0.504. Printed `α_14 = 0.000238`, z = 3.494 matches k=14 (α=0.000238095 / z=3.493804), not k=15 (α=0.000208333 / z=3.529296). Both stay inside `critic.py` `_close` tol 1e-3 of their own printed figures; k=15's z misses the printed 3.494. Cited CRITIC 09 bytes `CDEC94C5…` and ANSWER 08 file `339724BE…` recompute. Git blobs of the three attacked files equal `818e268`. | **Yes.** The demanded term-vs-scoring-look label is still on the clause-(2) face. The only new sentences are the record of the pair. |

2/24 and the 19h 06m 28s gap were not re-opened. `verifiably_preregistered` stays false on the row I hashed. Registry digest is unchanged (`1DDD3CCE…`); `trials_to_date` is 1; one log row, kind `declaration`; `R-SKIP-2TO1-FAVORITE.execution` true; `R-SKIP-COINFLIP.execution` false.

---

## Objections

**None. Zero UPHELD.**

This is a completed attack, not a skip. CRITIC 09's "what would prove me wrong" remains true of MD `:92` on these hashes: that sentence labels α_14 as the schedule's 14th term and the 13th scoring look, not as "Fourteenth" after naming the first scoring look k=2. ANSWER 09 did not touch that sentence. Filing a tenth leftover ordinal on a neighboring "looks" that prior critics already declined, or treating the disclosed link-amendment ratchet as a new face defect, would pad. Operator still records this.

I do not close condition 1. An attack with no objections is still an attack Operator must record in a separate turn. Binding stays `false` as I found it. Conditions 2 and 3 are not met on these bytes.

---

# Considered and not filed

- **CRITIC 08 item 1-as-Fourteenth-label-on-α_14.** Still answered on the clause-(2) face ANSWER 09 inherited. No new leftover ordinal of that class.
- **Condition 1 unmet solely because linking a zero-UPHELD pair amends the face.** Disclosed and intended on these bytes (`Amending this bar re-owes the Critic on the new text`). The hash-equality rider predates ANSWER 09. Demanding a sidecar, a bind, or a rewrite of the rider would be a proposal. I do not propose.
- **JSON keys `alpha_fourteenth_look` / `fwer_14_looks_new_scheme` still say "look."** Declined after the flags landed. Asking for a rename would pad.
- **Unbounded-sum sentence still says "looks" / "FWER ≤ 0.05 forever."** Predates ANSWER 08. CRITIC 06, 07, 08, and 09 declined. Not re-filed.
- **"14-look week" 15.2% on the drafted `0.05/k` scheme.** Already on the ANSWER 07 bytes. Critic declined. Not new residue.
- **L2 sharing k=2 / reject 0.504 with L1.** Option 1 from CRITIC 05 / ANSWER 05. Critic declined. I do not file it.
- **Clause (2) FWER 4.6% / Σ=0.05 over 14 looks as a standalone FWER claim.** Declined four times and now labeled. I do not file it.
- **No-peeking "First look: the first 70 eligible windows."** Names the L1 window set, not α_1. Different referent.
- **Effect-floor table header "First look, spent."** Already cited as the face knowing α_1 is historical.
- **JSON `increments_after: after_l2_look`.** Inside `looks.l2_test`. Names when L2 increments, not the global increment rule.
- **JSON `upheld: 0` without a `verdicts` array.** A count of CRITIC 09's UPHELD, which I verified. X5 already says a hash check cannot read an admit-pass verdict. Not a new face defect.
- **Copied `delta_above_detection_floor` still fails `alpha_first_look` vs current α_k.** Named on the face; owed to Systems (`critic.py:298` still compares that key to current α_k); `_close` tol 1e-3; the four restated design numbers agree. Re-filing it as if unanswered would pad.
- **FEE-AS-SIGNAL / RETUNE-COINFLIP-BAND.** Still declined. I did not open later tape.
- **`favorite_odds=2` as a proven peek.** Still not filed. 2/24 is not a fitted band.
- **Unpinned fee hash.** Already the standing condition-2 blocker. I will not write a placeholder. I will not record another 429.
- **Keyword greens / δ-check / vacuous greens.** CRITIC 02; already answered. Not re-filed.
- **Scoring, eligible counts, opening the tape.** Forbidden this Job.
- **`WATCHED` still frozen on PROPOSED 01.** True, disclosed, unpaid. The hashes of the `_02` notes and ANSWER 09 are recorded above so the next findings file cannot pretend they were reviewed.
- **Honesty-stamp bankroll / `crew_tick` clause.** Derived boxes are not mine to reopen. The section hash moved because the CoS restamp named ANSWER 09.
- **Rounded 0.504 vs 0.504330; printed 4.6% vs 0.046667.** Inside the checker's own 1e-3. Not an objection.
- **Registry bytes unchanged.** ANSWER 09 did not edit `LEARNING_LANE_15M_RULES.json`. No new registry sentence to attack. Findings still review `CD25DD72…`, not `1DDD3CCE…`.
- **X2 lived honoring unproven / `currently_reachable` false.** Already answered. No new verb.

---

**Closing.** I proposed no rule, scored no rule, ADMITted nothing, PARKed nothing, and did not Soften, Harden or Kill anything. I did not set `binding: true`, did not pin a fee-schedule hash, and did not write a placeholder for one. I opened no window outcome file. I did not edit the bar, the registry, or `critic.py`. Trading is **NOT ARMED**.

Zero objections, UPHELD none. Condition 1 stays unmet for these bytes until Operator records this attack. Operator answers this. Handoff → `operator`.
