# Soften Critic — attack on Systems 2026-09-09 lived/replay scorer wiring (CRITIC 11)

**Role:** Soften Critic · **Date:** 2026-09-09 · **Lane:** `learning_lane_15m` · series `KXBTC15M` only
**Branch:** `cursor/part-a-clerical-trust-boundary` at `6743c68` (HEAD). Bar, registry, and `rules.py` last touched at `3c89a7f` (Systems wiring). Git blobs of the three attacked files still equal `3c89a7f` (`65b15e38…` / `70e45e9e…` / `4a1b4842…`).

**Session separation.** This session did not draft the bar, did not write CRITIC 01 / 02 / 03 / 04 / 05 / 06 / 07 / 08 / 09 / 10, did not write ANSWER 01 / 02 / 03 / 04 / 05 / 06 / 07 / 08 / 09, did not declare `R-SKIP-2TO1-FAVORITE`, did not RUN-ONLY it, and did not write the Systems `3c89a7f` wiring. `PROTOCOL.md` forbids one turn both objecting and dismissing.

**This is an attack, not a verdict.** Operator answers each objection in a turn that is not this one. Nothing here is a Soften, an ADMIT, a RUN-ONLY, a park, a score, or a proposal. No rule was scored. `R-SKIP-COINFLIP` was not revived and its band was not retuned. `binding` stays `false` exactly as I found it. Trading is **NOT ARMED**.

**Why this file exists.** Desk Job 2026-09-09 09:05 ET: attack the Systems 2026-09-09 lived/replay scorer wiring on the new bar hashes + registry. Written objections only.

Systems (`3c89a7f`) wired `score_rule` / `_assert_window_lived_or_raise` to reject `(replay_close_after, replay_close_at_or_before]` as lived, flipped `lived_replay_fields_are_prose_only` to false, and set `lived_replay_enforced_by_scorer` true. Condition 1 is correctly `met: false` for that reason. This file attacks the **new** bytes.

---

## Artifacts attacked, by SHA-256

Computed independently via the same newline-normalised `read_text` → UTF-8 digest `critic.artifact_digest` uses (copied, not imported: this tree's package import pulls `pydantic`, which is not installed in this fire). Byte hash equals the normalised hash on every file below (0 CRLF pairs), except the honesty section, which is a slice of `DESK.md`.

| File | SHA-256 (bytes = normalised) | Last findings hash | CRITIC 10 attacked | Unreviewed? |
|---|---|---|---|---|
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR.md` | `61E2D677BFCE22F6FB0BCEC35D75DC85128EE9E86BCA8D24DC3579A234D1AB1E` | `5F2AA5F5…` | `DC46EFA6…` | **Y** — Systems wiring amendment |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR.json` | `F34DC187228AAACBCD30EB45C7AFF19E8730DA93FF504B772D2DEBDD53BAAA79` | `2611C255…` | `B6DDDB6B…` | **Y** |
| `golf-offshoot/docs/LEARNING_LANE_15M_RULES.json` | `BBD87E52EE6FC1E5F797C676EA6038F4C77404DDE7F29E21128BD75BF4B802D0` | `CD25DD72…` | `1DDD3CCE…` | **Y** — Systems flipped the lived/replay flags on the favorite row |
| `docs/agents/DESK.md` `## Honesty checklist` | `4C3DCB24155F44B28EE1F346326301A7D2F9563C057B72A28F1DD8FB72AA27EC` | `07055605…` | `CF0FEAB2…` | **Y** — restamp names Systems wiring / this assign |
| `golf-offshoot/docs/LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md` | `83D4463B4BB55D327485E3874A4BF3DAA54727D7ED37F56C124C6E8913DAF0B4` | `83D4463B…` | same | N — still the watched `lab_proposed` path |

Honesty slice is the committed `6743c68` / `3c89a7f` section (this fire's Status/thread writes do not touch it).

**Not in `WATCHED`** (CRITIC 03 objection 5, sustained, still unpaid; not re-filed):

| File | SHA-256 |
|---|---|
| `golf-offshoot/docs/LEARNING_LANE_15M_LAB_PROPOSED_02.md` | `B658C4CC45AA131163426D5D4E15ADEC0E71C41C12A6E206050E0900C6E960BB` |
| `golf-offshoot/docs/LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_02.md` | `3392E8F415D169CAB3A6A2D545CC85D4C598F830A43E187ADE0FD2780E21AC88` |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR_OPERATOR_ANSWER_09.md` | `A520687276F0294618C32E74DCEF72C5F70A165A1F13E283422FF06E57D869B6` |

Hashes recomputed at the end of the attack and unchanged: the text I attacked did not move under me.

---

## Posture

I did **not** open a window outcome file — no `paper/*.json`, no `settlements/*.json`, no `latest/journal.json`, no `rule_decisions.json`. I did not call `score_rule`, `write_critic_findings`, or `mark_roles_served`. I did not run the digest generator. I did not start or stop a hub. `watch.json` is not on this tree. I did not run the new Systems tests; I read them as text.

Numbers below come from the bar, the registry, the commit record, `critic.py` / `rules.py` / `tests/test_learning_rules.py` as text, and arithmetic I can do without the tape.

I did not edit the bar, the JSON, the registry, `critic.py`, `rules.py`, `DESK.md` (except the worker Status/thread this fire is required to write), or `AGENT_LEAVE_OFF.md` until closeout. I did not set `binding: true`. I did not pin a fee-schedule hash.

---

# The one-sentence version

**Systems closed the (16:53, 17:11] clock hole CRITIC 04 named, then stamped every remaining OOS window `evidence=lived` and flipped the fields from prose-only to "enforced" — a clock gate is not the bar's Lived definition.**

---

## What I accept as closed on the prior text (not re-filed)

CRITIC 04 objection 5 demanded the interval be readable by the scorer, or labeled prose-only. ANSWER 04 labeled it prose-only and owed the wiring to Systems. Systems landed the clock read. I am not re-opening "the scorer cannot fail a lived-mislabel of (16:53, 17:11]" as if unanswered. Residue that is **new on these bytes** is filed below.

| Prior sentence | Systems change I verified on these hashes | Closed as to that sentence? |
|---|---|---|
| CRITIC 04 #5: `score_rule` / `_assert_scorable` / `window_is_oos` do not read `lived_paper_begins_at` / `replay_close_*` | `_assert_window_lived_or_raise` (`rules.py:513–528`) raises `RuleNotScorable` when `window_is_replay` is true. `window_is_replay` (`:101–108`) is `after < closed <= until` on the explicit pair, else `(declared_at, lived_paper_begins_at]`. `score_rule` (`:577–579`) calls that helper on every window before `decide()`. The committed test `test_score_rule_rejects_replay_window_as_lived` (`tests/test_learning_rules.py:199–211`) asserts a `2026-09-08T17:00:00-04:00` close raises with `replay interval`. `window_is_oos` (`:73–81`) still keys only `closed > declared_at`, as the face now says. | **Yes** as to the interval gate. A window in `(16:53, 17:11]` cannot sit in a scorecard. The leftover is what the writer stamps on every *other* OOS window (objection 1) and what it does when the fields are absent (objection 2). |
| ANSWER 04 / CRITIC 10: `lived_replay_fields_are_prose_only: true`; wiring owed | MD `:217` / JSON `:93–94` / registry `:71–72` now say `lived_replay_fields_are_prose_only: false` and `lived_replay_enforced_by_scorer: true`. JSON `:329` marks the owed row LANDED. | **Yes** as to the flip happening. The overclaim in that flip is objection 1. |

2/24 and the 19h 06m 28s gap were not re-opened. `verifiably_preregistered` stays false on the row I hashed. I hashed the registry: one log row, kind `declaration`; `trials_to_date` 1; `R-SKIP-2TO1-FAVORITE.execution` true; `R-SKIP-COINFLIP.execution` false. Digest moved from CRITIC 10's `1DDD3CCE…` to `BBD87E52…` because Systems wrote the two flags and the new `replay_interval_note` onto the favorite row. `record_trial` still accepts only `declaration` and `l2_look`. Next-look set still k=2 / reject 0.504.

---

## Objection 1 — The scorer's `evidence=lived` stamp is a clock label; the face now calls that Lived enforcement

### **UPHELD.**

Lived, on this bar, is not a close-time. MD `:210`:

> **Lived** = "`execution=true`; the loop honoured `rules.decide()`."

The same face (MD `:217`) and JSON (`:93–94`) and the favorite registry row (`:71–72`) now say those fields are **enforced by the scorer**, not prose-only. What the machine actually does after the interval raise:

| Step | What it checks | What it does not check |
|---|---|---|
| `_assert_window_lived_or_raise` (`rules.py:513–533`) | OOS, then not in the named replay interval, then `window_is_lived` (the same two clocks) | `rule.execution`; a tip; a decision row; that the loop honoured `decide()` at that close |
| return value (`:533`) | — | always `"lived"` |
| `score_rule` row (`:604`) | — | writes `evidence: "lived"` |
| `_assert_scorable` L2 (`:488–492`) | current `rule.execution` is truthy | whether each window closed after the flip (the loop now does that **if** the fields exist) |

`window_is_lived` (`:111–120`) is "OOS and not replay." Its own docstring (`:114–116`) says a missing interval treats every OOS close as lived-for-score, and that `execution=false` is "the L2 execution guard, not this clock."

The committed test `test_score_rule_accepts_post_flip_windows_and_labels_lived` (`tests/test_learning_rules.py:181–196`, `:214–219`) builds 70 synthetic windows dated `2026-09-09T00:00` onward — no book, no hub, no `decide()` honor — and asserts `all(row["evidence"] == "lived")`. I did not run it. The assertion is the writer's intended meaning of the stamp.

X2 on these same bytes (MD `:299` / JSON `:311`) still says lived honoring is **unproven on this tree this turn** (no tip, no cited decision row). `watch.json` is still absent. I did not start a hub. I did not open `rule_decisions.json`. The face that just made the scorer emit the Lived verb still denies the process fact that verb names.

CRITIC 04 asked for a machine that can fail a lived-mislabel of the interval, or a prose-only label. Systems delivered the interval fail **and** renamed the clock remainder Lived. A later scorecard that prints `evidence=lived` on every post-17:11 window will read as the table's Lived cell, which this writer does not check.

**Concrete change demanded.** On MD `:217`, JSON `:93–94`, registry `:71–72`, and the scorecard `evidence` field: say the scorer enforces the **replay clock interval**, not Lived. Stamp `not_in_replay_interval` / `oos_after_flip` (or keep `lived` only after stating on the face that this token means `closed > lived_paper_begins_at` and does **not** mean the loop honoured `decide()`). Set `lived_replay_enforced_by_scorer` to name the clock, or set it false. Do not leave X2 saying honoring is unproven while the writer stamps Lived. Do not score. Do not start a hub to manufacture a tip. Do not edit `rules.py` in the answer turn if that turn also amends the bar (condition 1 again).

**What would prove me wrong.** Show `_assert_window_lived_or_raise` returns `"lived"` only when `execution` is true **and** a cited tip or decision-row hash shows the loop honoured `decide()` at that close; **or** show MD `:217` / JSON `:93–94` still call the fields prose-only / a clock gate and the scorecard stamp is not the Lived verb; **or** show X2 no longer says honoring is unproven on a face whose scorer stamps `lived`. I read `rules.py:513–533`, `:604`, MD `:210`, `:217`, `:299`. None of those is true.

---

## Objection 2 — Missing replay fields default every OOS window to `lived`, so `R-SKIP-COINFLIP` L1 would be stamped lived

### **UPHELD.**

`_replay_bounds` (`rules.py:84–98`) returns `None` unless the row has the explicit pair **or** both `lived_paper_begins_at` and `declared_at`. `window_is_replay` is then false. `window_is_lived` is then true for every OOS close.

I hashed `LEARNING_LANE_15M_RULES.json`. `R-SKIP-COINFLIP` (`:36–44`) has `execution: false` and **none** of `lived_paper_begins_at`, `replay_close_after`, `replay_close_at_or_before`. The favorite row has the pair. The default is therefore live on the other selecting rule.

MD `:210` says replay (`execution=false`; books collected without the rule acting) may score L1 and **cannot** Established. An L1 of `R-SKIP-COINFLIP` under this writer would still pass `_assert_window_lived_or_raise` (OOS, not in an interval that does not exist) and would write `evidence: "lived"` on every window. That is treating a replayed book as lived — the Hard NO the same bar prints at MD `:319` / JSON `:344` — as a machine, on the first rule the lane declared.

This is not a request to score `R-SKIP-COINFLIP`, flip its `execution`, retune `(0.45, 0.55)`, or invent a replay interval for it. It is a request to stop claiming Lived is enforced while the default stamps Lived on the rule whose entire post-declaration tape is replay.

The face (MD `:217`) and the LANDED owed row (JSON `:329`) describe only the favorite interval. They do not disclose the missing-fields default the helper's docstring already admits (`rules.py:114–116`).

**Concrete change demanded.** On the face and in JSON: disclose that a selecting row with no `replay_close_*` / `lived_paper_begins_at` has every OOS close stamped `lived`. Then either (a) make `_assert_window_lived_or_raise` return `replay` (or raise) when `execution` is false, or (b) keep the clock-only stamp and do not call it Lived (objection 1). Do not score `R-SKIP-COINFLIP`. Do not add fields to that row in a turn that also answers this. Do not revive or retune it.

**What would prove me wrong.** Show `window_is_lived` is false when `execution` is false; **or** show `R-SKIP-COINFLIP` already names a replay interval that covers its OOS tape; **or** show MD `:217` / JSON `:92–94` already disclose the missing-fields ⇒ all-OOS-stamped-lived default. I hashed the registry row and read `rules.py:84–120`. None of those is true.

---

# Considered and not filed

- **CRITIC 04 #5 as "the interval is still unread."** Closed. The 17:00-close class now raises. Residue is the Lived stamp and the default, filed above.
- **`_assert_scorable` L2 still keys only the current `execution` flag.** True (`rules.py:488–492`). The window loop now reads the fields when they exist, so re-filing CRITIC 04's exact table would pad. The leftover is the default in objection 2, not the favorite interval.
- **`decide()` still expresses replay-interval windows as eligible.** Disclosed (MD `:217`; test `:175–178`). Intentional split. The scorer is the gate. Not re-filed.
- **No `evidence=replay` path, so L1 cannot include (16:53, 17:11] even as Admissible replay.** Conservative vs the table's "L1 may be scored by replay." The face only forbade treating that interval as lived. Not a new face defect.
- **Re-expressing `decide()` onto caller-supplied `recorded_pnl` rather than reading a book action.** Predates this wiring. The new defect is labeling that remainder Lived (objection 1).
- **CRITIC 08's α_14 term/scoring-look label.** Still on MD `:92` / JSON `:150–154`. Not new on the Systems bytes. Not re-filed.
- **Copied `delta_above_detection_floor` still fails `alpha_first_look` vs current α_k.** Named on the face; owed to Systems (`critic.py:298`). Not new.
- **FEE-AS-SIGNAL / RETUNE-COINFLIP-BAND.** Still declined. I did not open later tape. I did not score or retune `R-SKIP-COINFLIP`.
- **`favorite_odds=2` as a proven peek.** Still not filed. 2/24 is not a fitted band.
- **Unpinned fee hash.** Already the standing condition-2 blocker. I will not write a placeholder. I will not record another 429.
- **Keyword greens / δ-check / vacuous greens.** CRITIC 02; already answered. Not re-filed.
- **Scoring, eligible counts, opening the tape.** Forbidden this Job.
- **`WATCHED` still frozen on PROPOSED 01.** True, disclosed, unpaid. The hashes of the `_02` notes and ANSWER 09 are recorded above so the next findings file cannot pretend they were reviewed.
- **Honesty-stamp bankroll / `crew_tick` clause.** Derived boxes are not mine to reopen. The section hash moved because the CoS restamp named the Systems wiring.
- **Rounded 0.504 vs 0.504330; printed 4.6% vs 0.046667.** Inside the checker's own 1e-3. Not an objection.
- **X2 `currently_reachable` false / pre-registration / binding / fee hash.** Already answered. I do not ask to flip `currently_reachable`.
- **A new `CHECKS` member that the scorer reads `replay_close_*`.** Possible; not written. Demanding one would be a proposal. I do not propose.

---

**Closing.** I proposed no rule, scored no rule, ADMITted nothing, PARKed nothing, and did not Soften, Harden or Kill anything. I did not set `binding: true`, did not pin a fee-schedule hash, and did not write a placeholder for one. I opened no window outcome file. I did not edit the bar, the registry, `rules.py`, or `critic.py`. Trading is **NOT ARMED**.

Two objections, both UPHELD. Condition 1 stays unmet for these bytes. Operator answers these. Handoff → `operator`.
