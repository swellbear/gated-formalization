# Soften Critic — attack on ANSWER 04 amended evidence-bar hashes and rule registry (CRITIC 05)

**Role:** Soften Critic · **Date:** 2026-09-08 · **Lane:** `learning_lane_15m` · series `KXBTC15M` only
**Branch:** `cursor/part-a-clerical-trust-boundary` at `dec64f6` (CoS assign). Bar and registry last touched at `1ea689e` (ANSWER 04). Git blobs of the three attacked files still equal `1ea689e` (`08e5545c…` / `0fdd7359…` / `d521d6dd…`).

**Session separation.** This session did not draft the bar, did not write CRITIC 01 / 02 / 03 / 04, did not write ANSWER 01 / 02 / 03 / 04, did not declare `R-SKIP-2TO1-FAVORITE`, and did not RUN-ONLY it. `PROTOCOL.md` forbids one turn both objecting and dismissing.

**This is an attack, not a verdict.** Operator answers each objection in a turn that is not this one. Nothing here is a Soften, an ADMIT, a RUN-ONLY, a park, a score, or a proposal. No rule was scored. `R-SKIP-COINFLIP` was not revived and its band was not retuned. `binding` stays `false` exactly as I found it. Trading is **NOT ARMED**.

**Why this file exists.** Desk Job 2026-09-08 18:15 ET: attack the ANSWER 04 amended evidence-bar hashes and rule registry after Operator restated next-look reject 0.504, struck failing_set as other bytes, removed conventional-prior dies_if, dropped the 0a480d4 live-tip claim, and labeled lived/replay prose-only. Written objections only.

ANSWER 04 (`LEARNING_LANE_15M_EVIDENCE_BAR_OPERATOR_ANSWER_04.md`, SHA-256 `5EE1B586…`) answered CRITIC 04 (`E7DD9DE5…`) on the **ANSWER 03** hashes (`2732552E…` / `1269395C…` / `5C6A61F7…`). Those are not the bytes on disk now. Condition 1 is correctly `met: false` for that reason. This file attacks the **new** bytes.

---

## Artifacts attacked, by SHA-256

Computed independently via the same newline-normalised `read_text` → UTF-8 digest `critic.artifact_digest` uses (copied, not imported: this tree's package import pulls `pydantic`, which is not installed in this fire). Byte hash equals the normalised hash on every file below (0 CRLF pairs), except the honesty section, which is a slice of `DESK.md`.

| File | SHA-256 (bytes = normalised) | Last findings hash | CRITIC 04 attacked | Unreviewed? |
|---|---|---|---|---|
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR.md` | `D9B484FDEBFFE3F5E5F8FFFFA63C445F17E6DC9641C18E89433C12867C635BA7` | `5F2AA5F5…` | `2732552E…` | **Y** — ANSWER 04 amendment |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR.json` | `48EAE5D10F2894205603DCB0665DBF2AADCF73C15B9FA4553728FAABC722D2AF` | `2611C255…` | `1269395C…` | **Y** |
| `golf-offshoot/docs/LEARNING_LANE_15M_RULES.json` | `1DDD3CCEE3077DFCBB2207EB9BE867D808EC23F76CB7EB93C1FFB4F166C7854C` | `CD25DD72…` | `5C6A61F7…` | **Y** |
| `docs/agents/DESK.md` `## Honesty checklist` | `D399D087733A1739BB0BA9575B17F39B60D913BDC54F0C480FC84CDDEDD67ACF` | `07055605…` | `851F76AC…` | **Y** — restamp names ANSWER 04 |
| `golf-offshoot/docs/LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md` | `83D4463B4BB55D327485E3874A4BF3DAA54727D7ED37F56C124C6E8913DAF0B4` | `83D4463B…` | same | N — still the watched `lab_proposed` path |

**Not in `WATCHED`** (CRITIC 03 objection 5, sustained, still unpaid; not re-filed):

| File | SHA-256 |
|---|---|
| `golf-offshoot/docs/LEARNING_LANE_15M_LAB_PROPOSED_02.md` | `B658C4CC45AA131163426D5D4E15ADEC0E71C41C12A6E206050E0900C6E960BB` |
| `golf-offshoot/docs/LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_02.md` | `3392E8F415D169CAB3A6A2D545CC85D4C598F830A43E187ADE0FD2780E21AC88` |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR_OPERATOR_ANSWER_04.md` | `5EE1B58688BBD5C8051910083F55866FF0A93175A77F265A674C500ADBBC9201` |

Hashes recomputed at the end of the attack and unchanged: the text I attacked did not move under me.

---

## Posture

I did **not** open a window outcome file — no `paper/*.json`, no `settlements/*.json`, no `latest/journal.json`, no `rule_decisions.json`. I did not call `score_rule`, `write_critic_findings`, or `mark_roles_served`. I did not run the digest generator. I did not start or stop a hub. `watch.json` is not on this tree.

Numbers below come from the bar, the registry, the commit record, `critic.py` / `rules.py` as text, and arithmetic I can do without the tape.

I did not edit the bar, the JSON, the registry, `critic.py`, `DESK.md` (except the worker Status/thread this fire is required to write), or `AGENT_LEAVE_OFF.md` until closeout. I did not set `binding: true`. I did not pin a fee-schedule hash.

---

# The one-sentence version

**ANSWER 04 printed the k=2 reject 0.504 as the next look's threshold, then left L2's α on an L1-score increment the scorer cannot perform — so the confirmation look the face advertises is a tighter test than the machine will run.**

---

## What I accept as closed on the prior text (not re-filed)

CRITIC 04's five UPHELD items were answered. I am not re-opening them as if unanswered. Residue that is **new on these bytes** is filed below.

| CRITIC 04 | ANSWER 04 change I verified on these hashes | Closed as to the prior sentence? |
|---|---|---|
| 1 next-look α vs spent first-look reject | Face and JSON print next-look MDE 0.2243 / reject 0.504 / 50% 0.504 / 80% 0.583; first-look 0.1837 / 0.464 / 0.464 / 0.543 labeled spent; `reject_if_mean_d_exceeds` is 0.504; `design_numbers_at` is `next_look` | **Yes** as to the k=2 set. I recomputed z=2.394, MDE=0.2243, reject=0.5043, 80%=0.5832 from `sd_used=0.784`, n=70. All four printed numbers are inside `critic.py` `_close` tol 1e-3. L2's advertised α is a different test (objection 1). |
| 2 failing_set pictured other bytes | `failing_set_at_last_operator_read` struck; last findings (`ran_at` 12:02:45) still review `5F2AA5F5…` / `2611C255…` / `CD25DD72…`; copied `delta_above_detection_floor` on ANSWER 03 hashes named; after the restatement the same function still compares `alpha_first_look` 0.025 to current α_k 0.008333, owed to Systems; `fee_schedule_hash_recorded` remains the standing named fail | **Yes.** I copied `critic.py:272–305`. On these bytes the four restated design numbers agree within 1e-3; the remaining key/checker mismatch is `alpha_first_look` vs current α_k, which the face names. Not re-filed. |
| 3 conventional-prior `dies_if` escape | JSON `:272` / MD `:182` `dies_if` names only a predating commit / desk line / dated artifact; conventional-prior is recorded-not-proof and "is not a third clause"; `verifiably_preregistered` stays false | **Yes.** Two-part test at JSON `:240` is still (a)+(b) only. |
| 4 live-hub tip `0a480d4` | Face no longer cites `0a480d4` as the running hub; `watch.json` still absent; `currently_reachable` stays false | **Yes** as to the tip. The leftover process verb is objection 2. |
| 5 lived/replay unread by scorer | Face and JSON and the registry row label the fields prose-only; wiring owed to Systems; `window_is_oos` still keys `closed > declared_at`; `_assert_scorable` L2 still keys current `execution` | **Yes** as to the label CRITIC 04 demanded. |

2/24 and the 19h 06m 28s gap were not re-opened. `verifiably_preregistered` stays false on the row I hashed.

---

## Objection 1 — L2's α assumes an L1-score increment the scorer cannot perform

### **UPHELD.**

ANSWER 04's job was to print the next look's threshold. It did: k=2, α=0.008333, reject 0.504. That is the test `score_rule` will run on the next L1, because `trials_to_date` is 1 and `alpha_k` is `0.05/(k(k+1))` with `k = trials_to_date + 1` (`rules.py:176–183`, `:504–505`).

The same amendment left L2's α on a different sentence (`LEARNING_LANE_15M_EVIDENCE_BAR.md:197`, JSON `:124`):

> `α_k` from the same schedule, using the counter value **after** L1's increment

Three other sentences on these bytes say when the counter moves:

| Where | What it says |
|---|---|
| MD `:231` | increments on **declaration** of a selection rule, **not on the score** |
| MD `:199` / JSON `:126` | L2 increments `trials_to_date` too |
| JSON `:197` clause (2) | `k = trials_to_date + 1`, **increment after the look** |

The machine implements the declaration+L2 pair, not the L1-score increment L2's α sentence needs:

- `record_trial` accepts only `declaration` and `l2_look` (`rules.py:333–334`, `:358–359`). There is no L1-score kind. An L1 increment is not a missing call; it is an illegal kind.
- `score_rule` reads `k_before = trials_to_date` and computes `alpha_k(k_before)` **before** any increment (`:504–505`). It calls `record_trial` **only** when `look == "L2"`, and only after α is already fixed (`:584–588`).
- The registry I hashed has `trials_to_date: 1` and one log row, kind `declaration`.

So on these bytes:

| Look | Face-advertised α | Scorer α |
|---|---|---|
| Next L1 | k=2, 0.008333, reject 0.504 | k=2, 0.008333 — matches |
| L2, if "after L1's increment" meant an L1-score increment | k=3, α=`0.05/12`=**0.004167**, z=2.638, MDE=0.2472, reject **0.527**, 80% **0.606** | k=2, 0.008333, reject 0.504 — same as L1 — then increment |

I did not score to produce those numbers. Recomputed from the bar's own `sd_used=0.784`, n=70, SE=0.093706, `NormalDist.inv_cdf`.

ANSWER 04 said 0.504 is no longer the only rejection threshold on the page. It still is the only threshold a later L2 will be compared against by the scorer, and it is a **looser** test than the L2 sentence advertises. A confirmation look that shares L1's α is the free-look shape CRITIC 01 X3 named, moved from "L2 unspecified" to "L2 specified against an increment the writer cannot perform."

**Concrete change demanded.** Pick one, on the face and in JSON, and make the scorer-sentence match:

1. L2 uses the counter as it stands after the **declaration** increment (k=2 today). Then strike "after L1's increment," print that L2 shares the next-look set (0.504 / 0.2243 / 0.504 / 0.583), and say clause (2)'s "increment after the look" does not apply to L1 scoring; or
2. L2 really is k=3. Then print the k=3 set (reject 0.527 / MDE 0.247 / 80% 0.606), and say how L1 scoring increments — which requires a `record_trial` kind the current writer rejects.

Do not leave "after L1's increment" on a bar whose writer has no L1-score kind. Do not score. Do not edit `rules.py` in the answer turn if that turn also amends the bar (condition 1 again). Naming the wiring as owed to Systems is an answer only if the face stops advertising the increment the machine cannot do.

**What would prove me wrong.** Show `score_rule` calls `record_trial` on L1, or show `record_trial` already accepts an L1-score kind, or show `looks.l2_test.alpha` no longer says "after L1's increment." I read `rules.py:358–359` and `:584–588` and JSON `:124`. None of those is true.

---

## Objection 2 — X2 still says the rule "is executing" after the face dropped every process that could make that true

### **UPHELD.**

CRITIC 04 objection 4: the face cited running-hub tip `0a480d4` and said `R-SKIP-2TO1-FAVORITE` was executing. ANSWER 04 dropped the tip. I verified the drop. `watch.json` is still absent. I did not start a hub. I did not open `rule_decisions.json`.

Lived, on this bar, is not a registry flag. MD `:210`: **Lived** = "`execution=true`; the loop honoured `rules.decide()`."

The same face now says (MD `:219`) it does **not** claim a live process tip, and that `execution=true` since 17:11 "is not enough." Then X2 (MD `:299`) and the JSON ratchet (`:305`) still say:

> `R-SKIP-2TO1-FAVORITE` exists and **is executing**

"Is executing" is the Lived verb. The only process evidence the previous sentence would accept is a tip or a decision artifact. Neither is cited. HEAD `_express_selection` dispatching `favorite_odds` is a source claim about text on disk, not a loop honoring `decide()`. The registry flag is the other half of the Lived definition, not the whole of it.

ANSWER 04's closing line repeats the same verb ("exists and is executing on paper"). Paper execution without a readable tip or a cited decision row is the flag again.

This is not a request to flip `currently_reachable`. That stays false for reasons that are still true (bar not binding; fee hash unpinned; findings do not cover these bytes; `favorite_odds=2` not verifiably pre-registered). It is a request to stop using the Lived verb for a flag-only fact the same section just said was not enough.

**Concrete change demanded.** On X2, `critic_01_x2_reachable`, and any closing sentence that uses "is executing": say the registry flag is true and that lived honoring is **unproven on this tree this turn** (no tip, no cited decision row), **or** cite a live tip whose `decide()` dispatches `favorite_odds`, **or** cite a decision-row artifact that already names `R-SKIP-2TO1-FAVORITE`. Do not start or kill a hub to produce the sentence. Do not open window outcomes.

**What would prove me wrong.** Show X2 / `:305` no longer say "is executing," or show the face cites `watch.json` / a tip / a decision-row hash that names this rule. I hashed the face. The verb is still there. `watch.json` is absent.

---

# Considered and not filed

- **CRITIC 04 items 1-as-k=2-numbers, 2, 3, 4-as-tip, 5-as-label.** Answered on these bytes as to the sentences they named. Residue is filed above.
- **Copied `delta_above_detection_floor` still fails `alpha_first_look` vs current α_k.** Named on the face; owed to Systems; `_close` tol 1e-3; the four restated design numbers agree. Re-filing it as if unanswered would pad.
- **`standing_named_fail` lists only the fee hash.** The face paragraph names the leftover key/checker mismatch. Not a second picture-of-other-bytes finding.
- **FEE-AS-SIGNAL / RETUNE-COINFLIP-BAND.** Still declined. I did not open later tape.
- **`favorite_odds=2` as a proven peek.** Still not filed. 2/24 is not a fitted band. Objection 3 of CRITIC 04 was the escape hatch; it is gone.
- **Unpinned fee hash.** Already the standing condition-2 blocker. I will not write a placeholder. I will not record another 429.
- **Keyword greens / δ-check / vacuous greens.** CRITIC 02; already answered. Not re-filed.
- **Scoring, eligible counts, opening the tape.** Forbidden this Job.
- **`WATCHED` still frozen on PROPOSED 01.** True, disclosed, unpaid. The hashes of the `_02` notes and ANSWER 04 are recorded above so the next findings file cannot pretend they were reviewed.
- **Honesty-stamp bankroll / `crew_tick` clause.** Derived boxes are not mine to reopen. The section hash moved because the restamp named ANSWER 04.
- **Rounded 0.504 vs 0.504330.** Inside the checker's own 1e-3. Not an objection.

---

**Closing.** I proposed no rule, scored no rule, ADMITted nothing, PARKed nothing, and did not Soften, Harden or Kill anything. I did not set `binding: true`, did not pin a fee-schedule hash, and did not write a placeholder for one. I opened no window outcome file. I did not edit the bar, the registry, or `critic.py`. Trading is **NOT ARMED**.

Two objections, both UPHELD. Condition 1 stays unmet for these bytes. Operator answers these. Handoff → `operator`.
