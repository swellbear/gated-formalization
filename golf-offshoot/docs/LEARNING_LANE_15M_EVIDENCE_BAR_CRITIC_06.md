# Soften Critic — attack on ANSWER 05 amended evidence-bar hashes and rule registry (CRITIC 06)

**Role:** Soften Critic · **Date:** 2026-09-08 · **Lane:** `learning_lane_15m` · series `KXBTC15M` only
**Branch:** `cursor/part-a-clerical-trust-boundary` at `c8226b8` (CoS assign). Bar and registry last touched at `0b2f5e9` (ANSWER 05). Git blobs of the three attacked files still equal `0b2f5e9` (`fa4c6570…` / `a801df21…` / `d521d6dd…`).

**Session separation.** This session did not draft the bar, did not write CRITIC 01 / 02 / 03 / 04 / 05, did not write ANSWER 01 / 02 / 03 / 04 / 05, did not declare `R-SKIP-2TO1-FAVORITE`, and did not RUN-ONLY it. `PROTOCOL.md` forbids one turn both objecting and dismissing.

**This is an attack, not a verdict.** Operator answers each objection in a turn that is not this one. Nothing here is a Soften, an ADMIT, a RUN-ONLY, a park, a score, or a proposal. No rule was scored. `R-SKIP-COINFLIP` was not revived and its band was not retuned. `binding` stays `false` exactly as I found it. Trading is **NOT ARMED**.

**Why this file exists.** Desk Job 2026-09-08 18:45 ET: attack the ANSWER 05 amended evidence-bar hashes and rule registry after Operator struck L2 after-L1-increment (L2 shares next-look 0.504), set X2 registry flag true, and labeled lived honoring unproven this turn. Written objections only.

ANSWER 05 (`LEARNING_LANE_15M_EVIDENCE_BAR_OPERATOR_ANSWER_05.md`, SHA-256 `15189CFC…`) answered CRITIC 05 (`03157E7D…`) on the **ANSWER 04** hashes (`D9B484FD…` / `48EAE5D1…`). Those are not the bytes on disk now. Condition 1 is correctly `met: false` for that reason. This file attacks the **new** bytes.

---

## Artifacts attacked, by SHA-256

Computed independently via the same newline-normalised `read_text` → UTF-8 digest `critic.artifact_digest` uses (copied, not imported: this tree's package import pulls `pydantic`, which is not installed in this fire). Byte hash equals the normalised hash on every file below (0 CRLF pairs), except the honesty section, which is a slice of `DESK.md`.

| File | SHA-256 (bytes = normalised) | Last findings hash | CRITIC 05 attacked | Unreviewed? |
|---|---|---|---|---|
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR.md` | `E2E9FC400DF4B6903BE323586408D8D84A5CBBD2BA631C0E8072B6554B4B3C3C` | `5F2AA5F5…` | `D9B484FD…` | **Y** — ANSWER 05 amendment |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR.json` | `471A1A1604DDBDDE424B3D0D0E3634D5B818D7CE4931595224C99CB3E3CEAD80` | `2611C255…` | `48EAE5D1…` | **Y** |
| `golf-offshoot/docs/LEARNING_LANE_15M_RULES.json` | `1DDD3CCEE3077DFCBB2207EB9BE867D808EC23F76CB7EB93C1FFB4F166C7854C` | `CD25DD72…` | `1DDD3CCE…` | **Y** — same digest as CRITIC 05; still unreviewed by findings |
| `docs/agents/DESK.md` `## Honesty checklist` | `73E791FF9A2E272C120047CA93D24216EDCBDE29D9255C827285DC8F0D70A64E` | `07055605…` | `D399D087…` | **Y** — restamp names ANSWER 05 |
| `golf-offshoot/docs/LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md` | `83D4463B4BB55D327485E3874A4BF3DAA54727D7ED37F56C124C6E8913DAF0B4` | `83D4463B…` | same | N — still the watched `lab_proposed` path |

**Not in `WATCHED`** (CRITIC 03 objection 5, sustained, still unpaid; not re-filed):

| File | SHA-256 |
|---|---|
| `golf-offshoot/docs/LEARNING_LANE_15M_LAB_PROPOSED_02.md` | `B658C4CC45AA131163426D5D4E15ADEC0E71C41C12A6E206050E0900C6E960BB` |
| `golf-offshoot/docs/LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_02.md` | `3392E8F415D169CAB3A6A2D545CC85D4C598F830A43E187ADE0FD2780E21AC88` |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR_OPERATOR_ANSWER_05.md` | `15189CFC38796F1D1F1679BC4C2326460855C8DC4BB9CC9CA95025DD4317C119` |

Hashes recomputed at the end of the attack and unchanged: the text I attacked did not move under me.

---

## Posture

I did **not** open a window outcome file — no `paper/*.json`, no `settlements/*.json`, no `latest/journal.json`, no `rule_decisions.json`. I did not call `score_rule`, `write_critic_findings`, or `mark_roles_served`. I did not run the digest generator. I did not start or stop a hub. `watch.json` is not on this tree.

Numbers below come from the bar, the registry, the commit record, `critic.py` / `rules.py` as text, and arithmetic I can do without the tape.

I did not edit the bar, the JSON, the registry, `critic.py`, `DESK.md` (except the worker Status/thread this fire is required to write), or `AGENT_LEAVE_OFF.md` until closeout. I did not set `binding: true`. I did not pin a fee-schedule hash.

---

# The one-sentence version

**ANSWER 05 aligned L2's α with the writer and dropped the Lived verb, then rewrote clause (2) to "increment after an L2 look only" — which, read as the increment rule, forbids the declaration increment that produces the k=2 / reject 0.504 set the same amendment just printed.**

---

## What I accept as closed on the prior text (not re-filed)

CRITIC 05's two UPHELD items were answered. I am not re-opening them as if unanswered. Residue that is **new on these bytes** is filed below.

| CRITIC 05 | ANSWER 05 change I verified on these hashes | Closed as to the prior sentence? |
|---|---|---|
| 1 L2 α after an L1-score increment the writer cannot perform | Struck "after L1's increment." MD `:197` / JSON `:124` use the declaration-increment counter; L1 scoring does not increment; L2 shares the next-look set (k=2, α=0.008333, reject 0.504, MDE 0.2243, 50% 0.504, 80% 0.583). I recomputed z=2.394, MDE=0.2243, reject=0.5043, 80%=0.5832 from `sd_used=0.784`, n=70. All four printed numbers are inside `critic.py` `_close` tol 1e-3. `record_trial` still accepts only `declaration` and `l2_look` (`rules.py:358–359`). `score_rule` still computes `alpha_k(k_before)` before any increment and records a trial only when `look == "L2"` (`:504–505`, `:584–588`) | **Yes** as to the advertised-vs-scorer mismatch. The increment sentence that replaced it is objection 1. |
| 2 X2 Lived verb "is executing" with no process | X2 / `critic_01_x2_reachable` say the registry `execution` flag is true and lived honoring is unproven this turn (no tip, no cited decision row). Face MD has **no** "is executing." `watch.json` still absent. I did not start a hub. I did not open a decision row | **Yes** as to the verb. |

2/24 and the 19h 06m 28s gap were not re-opened. `verifiably_preregistered` stays false on the row I hashed. Registry digest is unchanged (`1DDD3CCE…`); `trials_to_date` is 1; one log row, kind `declaration`; `R-SKIP-2TO1-FAVORITE.execution` true; `R-SKIP-COINFLIP.execution` false.

---

## Objection 1 — Clause (2)'s new increment sentence forbids the declaration increment that produces the k=2 set ANSWER 05 just printed

### **UPHELD.**

CRITIC 05 option 1 asked for three face edits: strike "after L1's increment," print that L2 shares the next-look set, and say clause (2)'s "increment after the look" does not apply to L1 scoring. ANSWER 05 did the first two. For the third it rewrote clause (2) itself.

ANSWER 04's clause (2) increment line was "using the registry counter *before* incrementing. Then increment." ANSWER 05 replaced it with (`LEARNING_LANE_15M_EVIDENCE_BAR.md:91`, JSON `:200`):

> Increment after an **L2** look only. An L1 score does not increment.

"Only" is the increment rule in that sentence. Declaration is not an L2 look. The same amendment's next-look set (k=2, reject 0.504) exists because a declaration increment already moved `trials_to_date` from 0 to 1. The registry I hashed still has that one log row, kind `declaration`.

Three other sentences on these bytes still say declaration increments:

| Where | What it says |
|---|---|
| MD `:93` | `record_trial` writes on `declaration` and `l2_look` only |
| MD `:231` / JSON `:152` | increments on **declaration** of a selection rule, **not on an L1 score**; L2 looks increment after the L2 look |
| MD `:197` / JSON `:124` | L2 uses the counter as it stands after the **declaration** increment; `record_trial` accepts only `declaration` and `l2_look` |

The machine implements the declaration+L2 pair (`rules.py:358–359`, `:402–403`, `:584–588`). Clause (2)'s new first sentence, read as written, is a different increment rule: L2 only. Under that reading `trials_to_date` would still be 0, the next look would be k=1, α=0.025, reject 0.464 — the spent first-look set ANSWER 04 labeled historical and this amendment kept historical.

This is the same shape CRITIC 05 filed against L2's α: one increment sentence vs the writer and vs the rest of the face. The L2 α sentence was struck. The leftover is now clause (2)'s increment sentence.

The L2 table still quotes the *deleted* ANSWER 04 wording (MD `:199`: "Clause (2)'s 'increment after the look' does not apply to L1 scoring"). Clause (2) no longer says that. Supporting, not a second claim.

**Concrete change demanded.** On clause (2) face and JSON `:200`, say the counter increments on **declaration** and after an **L2** look, and that an L1 score does not increment. Do not use "only" in a way that excludes declaration. The L2 table can drop the quote of the deleted "increment after the look" line. Do not score. Do not edit `rules.py` in the answer turn if that turn also amends the bar (condition 1 again).

**What would prove me wrong.** Show clause (2)'s increment sentence itself names declaration as an increment, or show "L2 look only" is scoped to scoring-looks in that sentence rather than to the counter. I read MD `:91` and JSON `:200`. Neither names declaration. I hashed the registry. The k=2 set depends on that increment.

---

# Considered and not filed

- **CRITIC 05 items 1-as-advertised-vs-scorer and 2-as-Lived-verb.** Answered on these bytes as to the sentences they named. Residue is filed above.
- **L2 sharing k=2 / reject 0.504 with L1.** That is option 1, which CRITIC 05 offered and ANSWER 05 picked. Re-filing the share as if unanswered would pad. The writer cannot advertise k=3 without an L1-score kind.
- **Clause (2) FWER 4.6% / Σ=0.05 over 14 looks.** That is the schedule if each k is used once. Declaration spending the k=1 *test* slot is older than this amendment. Not re-filed as a new FWER claim.
- **JSON key `executing_selection_rule`.** Names the `execution=true` rule. Not a sentence that uses the Lived verb. X2 no longer says "is executing."
- **Copied `delta_above_detection_floor` still fails `alpha_first_look` vs current α_k.** Named on the face; owed to Systems; `_close` tol 1e-3; the four restated design numbers agree. Re-filing it as if unanswered would pad.
- **FEE-AS-SIGNAL / RETUNE-COINFLIP-BAND.** Still declined. I did not open later tape.
- **`favorite_odds=2` as a proven peek.** Still not filed. 2/24 is not a fitted band.
- **Unpinned fee hash.** Already the standing condition-2 blocker. I will not write a placeholder. I will not record another 429.
- **Keyword greens / δ-check / vacuous greens.** CRITIC 02; already answered. Not re-filed.
- **Scoring, eligible counts, opening the tape.** Forbidden this Job.
- **`WATCHED` still frozen on PROPOSED 01.** True, disclosed, unpaid. The hashes of the `_02` notes and ANSWER 05 are recorded above so the next findings file cannot pretend they were reviewed.
- **Honesty-stamp bankroll / `crew_tick` clause.** Derived boxes are not mine to reopen. The section hash moved because the restamp named ANSWER 05.
- **Rounded 0.504 vs 0.504330.** Inside the checker's own 1e-3. Not an objection.
- **Registry bytes unchanged.** ANSWER 05 did not edit `LEARNING_LANE_15M_RULES.json`. No new registry sentence to attack. Findings still review `CD25DD72…`, not `1DDD3CCE…`.

---

**Closing.** I proposed no rule, scored no rule, ADMITted nothing, PARKed nothing, and did not Soften, Harden or Kill anything. I did not set `binding: true`, did not pin a fee-schedule hash, and did not write a placeholder for one. I opened no window outcome file. I did not edit the bar, the registry, or `critic.py`. Trading is **NOT ARMED**.

One objection, UPHELD. Condition 1 stays unmet for these bytes. Operator answers this. Handoff → `operator`.
