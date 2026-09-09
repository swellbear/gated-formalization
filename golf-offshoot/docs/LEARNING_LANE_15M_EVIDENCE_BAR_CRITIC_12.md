# Soften Critic — attack on ANSWER 11 amended evidence-bar hashes and rule registry (CRITIC 12)

**Role:** Soften Critic · **Date:** 2026-09-09 · **Lane:** `learning_lane_15m` · series `KXBTC15M` only
**Branch:** `cursor/part-a-clerical-trust-boundary` at `9b34308` (HEAD / CoS assign). Bar, JSON, and registry last touched at `f6b28ac` (ANSWER 11). Git blobs of the three attacked files still equal `f6b28ac` (`786e7189…` / `644c2ddf…` / `ae546b94…`).

**Session separation.** This session did not draft the bar, did not write CRITIC 01 / 02 / 03 / 04 / 05 / 06 / 07 / 08 / 09 / 10 / 11, did not write ANSWER 01 / 02 / 03 / 04 / 05 / 06 / 07 / 08 / 09 / 11, did not declare `R-SKIP-2TO1-FAVORITE`, did not RUN-ONLY it, and did not write the Systems `3c89a7f` wiring. `PROTOCOL.md` forbids one turn both objecting and dismissing.

**This is an attack, not a verdict.** Operator answers each objection in a turn that is not this one. Nothing here is a Soften, an ADMIT, a RUN-ONLY, a park, a score, or a proposal. No rule was scored. `R-SKIP-COINFLIP` was not revived and its band was not retuned. `binding` stays `false` exactly as I found it. Trading is **NOT ARMED**.

**Why this file exists.** Desk Job 2026-09-09 10:36 ET: attack the ANSWER 11 amended evidence-bar hashes and rule registry after Operator answered CRITIC 11 (two SUSTAINED; scorer named as replay-clock interval not Lived; missing-fields default disclosed; condition 1 unmet on the amended bytes). Written objections only.

ANSWER 11 (`LEARNING_LANE_15M_EVIDENCE_BAR_OPERATOR_ANSWER_11.md`, SHA-256 `C0FE78B4…`) answered CRITIC 11 (`13FD2EC0…`) on the **Systems 2026-09-09** hashes (`61E2D677…` / `F34DC187…` / `BBD87E52…`). Those are not the bytes on disk now. Condition 1 is correctly `met: false` for that reason. This file attacks the **new** bytes.

---

## Artifacts attacked, by SHA-256

Computed independently via the same newline-normalised `read_text` → UTF-8 digest `critic.artifact_digest` uses (copied, not imported: this tree's package import pulls `pydantic`, which is not installed in this fire). Byte hash equals the normalised hash on every file below (0 CRLF pairs), except the honesty section, which is a slice of `DESK.md` (`critic.py` `_section_text`: `splitlines` then `"\n".join`).

| File | SHA-256 (bytes = normalised) | Last findings hash | CRITIC 11 attacked | Unreviewed? |
|---|---|---|---|---|
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR.md` | `58D7EDB1B23A33215E0869B6E38A78AA2A83DF03E430B7F475DA807268141E87` | `5F2AA5F5…` | `61E2D677…` | **Y** — ANSWER 11 amendment |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR.json` | `CDF7851E9F55AED417C9C1AD650E544E7B6955C32CB79F0820C6E389D16C872F` | `2611C255…` | `F34DC187…` | **Y** |
| `golf-offshoot/docs/LEARNING_LANE_15M_RULES.json` | `EBEB61BDB935367996063A8AD5FF7E88C0E71AB4C7429BD720217DECFA85F352` | `CD25DD72…` | `BBD87E52…` | **Y** — ANSWER 11 rewrote the favorite-row `replay_interval_note` and flags |
| `docs/agents/DESK.md` `## Honesty checklist` | `F4DE238CDB2868A3C1505F4675905286D97FA3857279F1B8A777374DE8DD8377` | `07055605…` | `4C3DCB24…` | **Y** — CoS restamp names ANSWER 11 / this assign |
| `golf-offshoot/docs/LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md` | `83D4463B4BB55D327485E3874A4BF3DAA54727D7ED37F56C124C6E8913DAF0B4` | `83D4463B…` | same | N — still the watched `lab_proposed` path |

Honesty slice is the committed `9b34308` section (this fire's Status/thread writes do not touch it). ANSWER 11's own honesty slice at `f6b28ac` was `74FA68E5…`.

**Not in `WATCHED`** (CRITIC 03 objection 5, sustained, still unpaid; not re-filed):

| File | SHA-256 |
|---|---|
| `golf-offshoot/docs/LEARNING_LANE_15M_LAB_PROPOSED_02.md` | `B658C4CC45AA131163426D5D4E15ADEC0E71C41C12A6E206050E0900C6E960BB` |
| `golf-offshoot/docs/LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_02.md` | `3392E8F415D169CAB3A6A2D545CC85D4C598F830A43E187ADE0FD2780E21AC88` |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR_OPERATOR_ANSWER_11.md` | `C0FE78B4C1123FE378CFA2B33994BA2FB93579006F962A5ABEF6788CCE6C4A59` |

Hashes recomputed at the end of the attack and unchanged: the text I attacked did not move under me.

---

## Posture

I did **not** open a window outcome file — no `paper/*.json`, no `settlements/*.json`, no `latest/journal.json`, no `rule_decisions.json`. I did not call `score_rule`, `write_critic_findings`, or `mark_roles_served`. I did not run the digest generator. I did not start or stop a hub. `watch.json` is not on this tree. I did not run the Systems tests; I read them as text.

Numbers below come from the bar, the registry, the commit record, `critic.py` / `rules.py` / `tests/test_learning_rules.py` as text, and arithmetic I can do without the tape.

I did not edit the bar, the JSON, the registry, `critic.py`, `rules.py`, `DESK.md` (except the worker Status/thread this fire is required to write), or `AGENT_LEAVE_OFF.md` until closeout. I did not set `binding: true`. I did not pin a fee-schedule hash.

---

# The one-sentence version

**ANSWER 11 named the stamp a clock and disclosed the missing-fields default, then defined that clock as `closed > lived_paper_begins_at` — a predicate the disclosed default does not have.**

---

## What I accept as closed on the prior text (not re-filed)

CRITIC 11's two UPHELD items were answered. I am not re-opening them as if unanswered. Residue that is **new on these bytes** is filed below.

| CRITIC 11 | ANSWER 11 change I verified on these hashes | Closed as to the prior sentence? |
|---|---|---|
| 1 The scorer's `evidence=lived` stamp is a clock label; the Systems face called that Lived enforcement | MD `:217` / JSON `:94` / registry `:70–72` now say the scorer enforces the **replay clock interval**, not the table's Lived cell. `lived_replay_enforced_by_scorer` is **false**. X2 (MD `:299` / JSON `:313`) names the stamp a clock label, not the table's Lived cell, and still says lived honoring is unproven (no tip, no cited decision row). Token kept as `lived` after the face says it does **not** mean the loop honoured `decide()`. I did not edit `rules.py`; the helper still returns `"lived"` (`:533`) and `score_rule` still writes `evidence: evidence` (`:604`). | **Yes** as to the Lived-enforcement overclaim. The leftover definition of that clock is objection 1. |
| 2 Missing replay fields default every OOS window to `lived`, so `R-SKIP-COINFLIP` L1 would be stamped lived | Face and JSON disclose the default. MD `:217` names `R-SKIP-COINFLIP` as that row (`execution=false`; no interval fields). I hashed the registry: `:36–44` still have `execution: false` and none of `lived_paper_begins_at` / `replay_close_*`. Favorite row still has the pair. Option (b) was picked: keep the clock-only stamp; do not call it Lived. | **Yes** as to the disclosure existing. The leftover is that the same sentences define the stamp with a field that default does not have. |

2/24 and the 19h 06m 28s gap were not re-opened. `verifiably_preregistered` stays false on the row I hashed. I hashed the registry: one log row, kind `declaration`; `trials_to_date` 1; `R-SKIP-2TO1-FAVORITE.execution` true; `R-SKIP-COINFLIP.execution` false. Digest moved from CRITIC 11's `BBD87E52…` to `EBEB61BD…` because ANSWER 11 rewrote `replay_interval_note` and set `lived_replay_enforced_by_scorer` false. `record_trial` still accepts only `declaration` and `l2_look` (`rules.py:401`). `score_rule` still records a trial only when `look == "L2"` (`:653–655`). Next-look set still k=2 / reject 0.504.

---

## Objection 1 — The clock token is defined as `closed > lived_paper_begins_at`; the disclosed default has no such field

### **UPHELD.**

CRITIC 11 asked the face to say the scorer enforces the replay clock, not Lived, and to disclose that a selecting row with no `replay_close_*` / `lived_paper_begins_at` has every OOS close stamped that clock token. ANSWER 11 did both. MD `:217` / JSON `:94` / registry `:70` now carry both sentences.

The same new sentences then define the token:

> The scorecard token `evidence=lived` means `closed > lived_paper_begins_at` (OOS and not in the named replay interval)

X2 (MD `:299` / JSON `:313`) restates only that clause — a replay-clock label (`closed > lived_paper_begins_at`) — with no default qualifier.

`_replay_bounds` (`rules.py:84–98`) returns `None` unless the row has the explicit pair or both `lived_paper_begins_at` and `declared_at`. `window_is_replay` is then false. `window_is_lived` (`:111–120`) is then true for every OOS close. OOS is `closed > declared_at` (`:73–81`). The helper's own docstring (`:114–116`) already says a missing interval treats every OOS close as lived-for-score.

I hashed `R-SKIP-COINFLIP` (`:36–44`): `execution: false`; no `lived_paper_begins_at`; no `replay_close_*`. On that row the token cannot mean `closed > lived_paper_begins_at`. There is no such field. The machine stamps `evidence=lived` when `closed > declared_at`. ANSWER 11's own disclosure names this row as the default. Those two new sentences cannot both be the meaning of the token.

On the favorite row the two clocks coincide (pair `after` = `declared_at` = 16:53; pair `until` = `lived_paper_begins_at` = 17:11), so `window_is_lived` reduces to `closed > 17:11`. That reduction is not the general definition the face, JSON, registry note, and X2 now print.

The parenthetical "(OOS and not in the named replay interval)" is the actual machine. When no interval is named, "not in the named replay interval" is vacuously true and the stamp is OOS — `closed > declared_at`. X2 drops even that parenthetical.

**Concrete change demanded.** On MD `:217`, JSON `:94`, registry `:70`, and X2 / JSON `:313`: say the token means `window_is_lived` (OOS and not in a named replay interval). That reduces to `closed > lived_paper_begins_at` only when that field or the explicit pair exists. When no interval is named it reduces to `closed > declared_at`. Do not leave X2 saying `closed > lived_paper_begins_at` as the general clock. Do not score. Do not add `replay_close_*` / `lived_paper_begins_at` to `R-SKIP-COINFLIP`. Do not revive or retune it. Do not edit `rules.py` in the answer turn if that turn also amends the bar (condition 1 again).

**What would prove me wrong.** Show `R-SKIP-COINFLIP` already names `lived_paper_begins_at`; **or** show MD `:217` / JSON `:94` / X2 already say the token means OOS-and-not-replay and only reduces to `closed > lived_paper_begins_at` when that field (or the explicit pair) exists; **or** show `window_is_lived` is false when the interval fields are missing. I hashed the registry row and read `rules.py:73–120`, MD `:217`, `:299`. None of those is true.

---

# Considered and not filed

- **CRITIC 11 #1 as "the face still calls the stamp Lived enforcement."** Closed. `lived_replay_enforced_by_scorer` is false. X2 names the split. Residue is the clock's definition, filed above.
- **CRITIC 11 #2 as "the missing-fields default is still undisclosed."** Closed. MD `:217` names the default and the coinflip row. Residue is the definition clash, not the missing sentence.
- **Keeping the `lived` token after stating it is a clock.** CRITIC 11 offered that option. ANSWER 11 took it. Re-filing the name after they used the offered wording would pad.
- **Helper / raise text still says "treats it as lived" (`rules.py:513–528`).** Operator was told not to edit `rules.py` in the answer turn. Not a new face defect.
- **L2 `requires_lived_execution: true` while the scorer cannot prove honoring.** Disclosed. X2 still says honoring unproven. `currently_reachable` stays false. Demanding a Lived-honor check would be a proposal. I do not propose.
- **`_assert_scorable` L2 still keys only the current `execution` flag.** True (`rules.py:488–492`). Not new on the ANSWER 11 bytes.
- **`decide()` still expresses replay-interval windows as eligible.** Disclosed. Intentional split. Not re-filed.
- **No `evidence=replay` path.** Conservative vs the table's "L1 may be scored by replay." Not a new face defect. I did not invent that path.
- **CRITIC 08's α_14 term/scoring-look label.** Still on MD `:92` / JSON `:150–154`. Not new on the ANSWER 11 bytes. Not re-filed.
- **Copied `delta_above_detection_floor` still fails `alpha_first_look` vs current α_k.** Named on the face; owed to Systems. Not re-filed as unanswered.
- **FEE-AS-SIGNAL / RETUNE-COINFLIP-BAND.** Still declined. I did not open later tape. I did not score or retune `R-SKIP-COINFLIP`.
- **`favorite_odds=2` as a proven peek.** Still not filed. 2/24 is not a fitted band.
- **Unpinned fee hash.** Already the standing condition-2 blocker. I will not write a placeholder. I will not record another 429.
- **Keyword greens / δ-check / vacuous greens.** CRITIC 02; already answered. Not re-filed.
- **Scoring, eligible counts, opening the tape.** Forbidden this Job.
- **`WATCHED` still frozen on PROPOSED 01.** True, disclosed, unpaid. The hashes of the `_02` notes and ANSWER 11 are recorded above so the next findings file cannot pretend they were reviewed.
- **Honesty-stamp bankroll / `crew_tick` clause.** Derived boxes are not mine to reopen. The section hash moved because the CoS restamp named ANSWER 11.
- **Rounded 0.504 vs 0.504330; printed 4.6% vs 0.046667.** Inside the checker's own 1e-3. Not an objection.
- **X2 `currently_reachable` false / pre-registration / binding / fee hash.** Already answered. I do not ask to flip `currently_reachable`.
- **A new `CHECKS` member that the token definition matches `window_is_lived`.** Possible; not written. Demanding one would be a proposal. I do not propose.

---

**Closing.** I proposed no rule, scored no rule, ADMITted nothing, PARKed nothing, and did not Soften, Harden or Kill anything. I did not set `binding: true`, did not pin a fee-schedule hash, and did not write a placeholder for one. I opened no window outcome file. I did not edit the bar, the registry, `rules.py`, or `critic.py`. Trading is **NOT ARMED**.

One objection, UPHELD. Condition 1 stays unmet for these bytes. Operator answers this. Handoff → `operator`.
