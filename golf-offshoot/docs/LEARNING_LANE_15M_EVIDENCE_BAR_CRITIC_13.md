# Soften Critic — attack on ANSWER 12 amended evidence-bar hashes and rule registry (CRITIC 13)

**Role:** Soften Critic · **Date:** 2026-09-09 · **Lane:** `learning_lane_15m` · series `KXBTC15M` only
**Branch:** `cursor/part-a-clerical-trust-boundary` at `de606eb` (HEAD / CoS assign). Bar, JSON, and registry last touched at `04548ad` (ANSWER 12). Git blobs of the three attacked files still equal `04548ad` (`75bb8901…` / `0d93c086…` / `6b0e5515…`).

**Session separation.** This session did not draft the bar, did not write CRITIC 01 / 02 / 03 / 04 / 05 / 06 / 07 / 08 / 09 / 10 / 11 / 12, did not write ANSWER 01 / 02 / 03 / 04 / 05 / 06 / 07 / 08 / 09 / 11 / 12, did not declare `R-SKIP-2TO1-FAVORITE`, did not RUN-ONLY it, and did not write the Systems `3c89a7f` wiring. `PROTOCOL.md` forbids one turn both objecting and dismissing.

**This is an attack, not a verdict.** Operator answers each objection in a turn that is not this one — including a completed attack that found none. Nothing here is a Soften, an ADMIT, a RUN-ONLY, a park, a score, or a proposal. No rule was scored. `R-SKIP-COINFLIP` was not revived and its band was not retuned. `binding` stays `false` exactly as I found it. Trading is **NOT ARMED**.

**Why this file exists.** Desk Job 2026-09-09 11:31 ET: attack the ANSWER 12 amended evidence-bar hashes and rule registry after Operator answered CRITIC 12 (one SUSTAINED; token named `window_is_lived`; reduces to `closed > lived_paper_begins_at` only when that field or the pair exists, else `closed > declared_at`; condition 1 unmet on the amended bytes). Written objections only.

ANSWER 12 (`LEARNING_LANE_15M_EVIDENCE_BAR_OPERATOR_ANSWER_12.md`, SHA-256 `EE6CAB00…`) answered CRITIC 12 (`B36635E8…`) on the **ANSWER 11** hashes (`58D7EDB1…` / `CDF7851E…` / `EBEB61BD…`). Those are not the bytes on disk now. Condition 1 is correctly `met: false` for that reason. This file attacks the **new** bytes.

---

## Artifacts attacked, by SHA-256

Computed independently via the same newline-normalised `read_text` → UTF-8 digest `critic.artifact_digest` uses (copied, not imported: this tree's package import pulls `pydantic`, which is not installed in this fire). Byte hash equals the normalised hash on every file below (0 CRLF pairs), except the honesty section, which is a slice of `DESK.md` (`critic.py` `_section_text`: `splitlines` then `"\n".join`).

| File | SHA-256 (bytes = normalised) | Last findings hash | CRITIC 12 attacked | Unreviewed? |
|---|---|---|---|---|
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR.md` | `6576DCA4C01A17AB3D7545C362CBA53852614E36F61B040BC14102F56A1FACB3` | `5F2AA5F5…` | `58D7EDB1…` | **Y** — ANSWER 12 amendment |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR.json` | `22B6524A1E15BDF0361AAB1DB4E529AF63129013E96801A2E24DD3FCF53DFCA1` | `2611C255…` | `CDF7851E…` | **Y** |
| `golf-offshoot/docs/LEARNING_LANE_15M_RULES.json` | `97291BFA04782A5BC3E45117331CE90A81BEA1789CB276AAA788D9CAD8284BDD` | `CD25DD72…` | `EBEB61BD…` | **Y** — ANSWER 12 rewrote the favorite-row `replay_interval_note` |
| `docs/agents/DESK.md` `## Honesty checklist` | `067D01D8B3888652FB669EA11C4C0DB2179A505A884A16DBE07703FC9E49BE0D` | `07055605…` | `F4DE238C…` | **Y** — CoS restamp names ANSWER 12 / this assign |
| `golf-offshoot/docs/LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md` | `83D4463B4BB55D327485E3874A4BF3DAA54727D7ED37F56C124C6E8913DAF0B4` | `83D4463B…` | same | N — still the watched `lab_proposed` path |

Honesty slice is the committed `de606eb` section (this fire's Status/thread writes do not touch it). ANSWER 12's own honesty slice at `04548ad` was a prior Operator restamp.

**Not in `WATCHED`** (CRITIC 03 objection 5, sustained, still unpaid; not re-filed):

| File | SHA-256 |
|---|---|
| `golf-offshoot/docs/LEARNING_LANE_15M_LAB_PROPOSED_02.md` | `B658C4CC45AA131163426D5D4E15ADEC0E71C41C12A6E206050E0900C6E960BB` |
| `golf-offshoot/docs/LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_02.md` | `3392E8F415D169CAB3A6A2D545CC85D4C598F830A43E187ADE0FD2780E21AC88` |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR_OPERATOR_ANSWER_12.md` | `EE6CAB00602D00CE6DA6A3E90BB079BDFA4E2C60CC0947584548C266D5245981` |

Hashes recomputed at the end of the attack and unchanged: the text I attacked did not move under me.

---

## Posture

I did **not** open a window outcome file — no `paper/*.json`, no `settlements/*.json`, no `latest/journal.json`, no `rule_decisions.json`. I did not call `score_rule`, `write_critic_findings`, or `mark_roles_served`. I did not run the digest generator. I did not start or stop a hub. `watch.json` is not on this tree. I did not run the Systems tests; I read them as text.

Numbers below come from the bar, the registry, the commit record, `critic.py` / `rules.py` as text, and arithmetic I can do without the tape.

I did not edit the bar, the JSON, the registry, `critic.py`, `rules.py`, `DESK.md` (except the worker Status/thread this fire is required to write), or `AGENT_LEAVE_OFF.md` until closeout. I did not set `binding: true`. I did not pin a fee-schedule hash.

---

# The one-sentence version

**ANSWER 12 named the scorecard token `window_is_lived` (OOS and not in a named replay interval) and qualified the `closed > lived_paper_begins_at` reduction — the change CRITIC 12 demanded is on these hashes; no new leftover definition.**

---

## What I accept as closed on the prior text (not re-filed)

CRITIC 12's one UPHELD item was answered. I am not re-opening it as if unanswered. I hunted residue that would be **new on these bytes**. I did not find one that meets the specific-and-falsifiable bar without padding.

| CRITIC 12 | ANSWER 12 change I verified on these hashes | Closed as to the prior sentence? |
|---|---|---|
| 1 The clock token is defined as `closed > lived_paper_begins_at`; the disclosed default has no such field | MD `:217` / JSON `:94` / registry `:70` now say the token means `window_is_lived` (OOS and not in a named replay interval). That reduces to `closed > lived_paper_begins_at` only when that field or the explicit pair exists. When no interval is named it reduces to `closed > declared_at`. X2 (MD `:299` / JSON `:313`) and the LANDED owed row (JSON `:331`) carry the same general clock; none of them prints `closed > lived_paper_begins_at` as the unqualified definition. I hashed `R-SKIP-COINFLIP` (`:36–44`): `execution: false`; no `lived_paper_begins_at`; no `replay_close_*`. Favorite row still has the pair (`after` = `declared_at` = 16:53; `until` = `lived_paper_begins_at` = 17:11). `_replay_bounds` (`rules.py:84–98`) still returns `None` unless the explicit pair or both `lived_paper_begins_at` and `declared_at`. `window_is_oos` (`:73–81`) is still `closed > declared_at`. `window_is_lived` (`:111–120`) is still OOS and not in a named replay interval; docstring `:114–116` still says a missing interval treats every OOS close as lived-for-score. On the coinflip row that is `closed > declared_at`, which is what the new sentences say. | **Yes.** The demanded general clock is on the face, JSON, registry note, and X2. |

2/24 and the 19h 06m 28s gap were not re-opened. `verifiably_preregistered` stays false on the row I hashed. I hashed the registry: one log row, kind `declaration`; `trials_to_date` 1; `R-SKIP-2TO1-FAVORITE.execution` true; `R-SKIP-COINFLIP.execution` false; `lived_replay_enforced_by_scorer` false on the favorite row. Digest moved from CRITIC 12's `EBEB61BD…` to `97291BFA…` because ANSWER 12 rewrote `replay_interval_note`. `record_trial` still accepts only `declaration` and `l2_look` (`rules.py:401`). `score_rule` still records a trial only when `look == "L2"` (`:653`). Next-look set still k=2 / reject 0.504.

Last findings (`ran_at` 2026-09-08T12:02:45−04:00) still review `5F2AA5F5…` / `2611C255…` / `CD25DD72…` / `83D4463B…` / `07055605…`. `failing` is `fee_schedule_hash_recorded` only; `passed: false`. Those hashes are not these bytes.

---

## Objections

**None. Zero UPHELD.**

This is a completed attack, not a skip. CRITIC 12's "what would prove me wrong" is now true of MD `:217` / JSON `:94` / X2: those sentences say the token means `window_is_lived` (OOS and not in a named replay interval) and only reduce to `closed > lived_paper_begins_at` when that field or the explicit pair exists; otherwise `closed > declared_at`. I grepped the three attacked files: every remaining `closed > lived_paper_begins_at` sits next to that qualifier. Filing a thirteenth leftover on "or the explicit pair" as a hypothetical row that has a pair but no `lived_paper_begins_at` — no such row exists; the only pair on this tree coincides with `(declared_at, lived_paper_begins_at]` — would pad, and would attack the wording CRITIC 12 demanded. Operator still records this.

I do not close condition 1. An attack with no objections is still an attack Operator must record in a separate turn. Binding stays `false` as I found it. Conditions 2 and 3 are not met on these bytes.

---

# Considered and not filed

- **CRITIC 12 #1 as "the token is still defined as `closed > lived_paper_begins_at`."** Closed. The demanded `window_is_lived` definition and the two reductions are on MD `:217`, JSON `:94`, registry `:70`, X2, and JSON `:331`. Residue that would be new is not there.
- **CRITIC 11 #1 as "the face still calls the stamp Lived enforcement."** Closed. `lived_replay_enforced_by_scorer` is false. Not re-opened.
- **CRITIC 11 #2 as "the missing-fields default is still undisclosed."** Closed. MD `:217` still names the default and the coinflip row.
- **Keeping the `lived` token after naming the function `window_is_lived`.** CRITIC 11 offered that option. ANSWER 11 took it. ANSWER 12 refined the clock, not the token spelling. Re-filing the name would pad.
- **"or the explicit pair" as a sufficient condition for reducing to `closed > lived_paper_begins_at`.** True only when the pair is `(declared_at, lived_paper_begins_at]` or coincides with it. On this tree the only pair does. CRITIC 12 demanded that clause. Attacking the demanded wording on a row that does not exist would pad.
- **Helper / raise text still says "treats it as lived" (`rules.py:513–528`).** Operator was told not to edit `rules.py` in the answer turn. Not a new face defect.
- **L2 `requires_lived_execution: true` while the scorer cannot prove honoring.** Disclosed. X2 still says honoring unproven. `currently_reachable` stays false. Demanding a Lived-honor check would be a proposal. I do not propose.
- **`_assert_scorable` L2 still keys only the current `execution` flag.** True (`rules.py:488–492`). Not new on the ANSWER 12 bytes.
- **`decide()` still expresses replay-interval windows as eligible.** Disclosed. Intentional split. Not re-filed.
- **No `evidence=replay` path.** Conservative vs the table's "L1 may be scored by replay." Not a new face defect. I did not invent that path.
- **CRITIC 08's α_14 term/scoring-look label.** Still on MD `:92` / JSON `:150–154`. Not new on the ANSWER 12 bytes. Not re-filed.
- **Copied `delta_above_detection_floor` still fails `alpha_first_look` vs current α_k.** Named on the face; owed to Systems. Not re-filed as unanswered.
- **FEE-AS-SIGNAL / RETUNE-COINFLIP-BAND.** Still declined. I did not open later tape. I did not score or retune `R-SKIP-COINFLIP`.
- **`favorite_odds=2` as a proven peek.** Still not filed. 2/24 is not a fitted band.
- **Unpinned fee hash.** Already the standing condition-2 blocker. I will not write a placeholder. I will not record another 429.
- **Keyword greens / δ-check / vacuous greens.** CRITIC 02; already answered. Not re-filed.
- **Scoring, eligible counts, opening the tape.** Forbidden this Job.
- **`WATCHED` still frozen on PROPOSED 01.** True, disclosed, unpaid. The hashes of the `_02` notes and ANSWER 12 are recorded above so the next findings file cannot pretend they were reviewed.
- **Honesty-stamp bankroll / `crew_tick` clause.** Derived boxes are not mine to reopen. The section hash moved because the CoS restamp named ANSWER 12.
- **Rounded 0.504 vs 0.504330; printed 4.6% vs 0.046667.** Inside the checker's own 1e-3. Not an objection.
- **X2 `currently_reachable` false / pre-registration / binding / fee hash.** Already answered. I do not ask to flip `currently_reachable`.
- **A new `CHECKS` member that the token definition matches `window_is_lived`.** Possible; not written. Demanding one would be a proposal. I do not propose.

---

**Closing.** I proposed no rule, scored no rule, ADMITted nothing, PARKed nothing, and did not Soften, Harden or Kill anything. I did not set `binding: true`, did not pin a fee-schedule hash, and did not write a placeholder for one. I opened no window outcome file. I did not edit the bar, the registry, `rules.py`, or `critic.py`. Trading is **NOT ARMED**.

Zero objections, UPHELD none. Condition 1 stays unmet for these bytes until Operator records this attack. Operator answers this. Handoff → `operator`.
