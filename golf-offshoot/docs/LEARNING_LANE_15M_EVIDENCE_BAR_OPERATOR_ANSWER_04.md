# Operator answer — admit pass on Soften Critic CRITIC 04

**Role:** Operator · **Date:** 2026-09-08 · **Lane:** `learning_lane_15m` · series `KXBTC15M` only

**Critic file answered:** [`LEARNING_LANE_15M_EVIDENCE_BAR_CRITIC_04.md`](LEARNING_LANE_15M_EVIDENCE_BAR_CRITIC_04.md)
**SHA-256 of the exact bytes answered:** `E7DD9DE5BCE5E0387AE0524A14023288324A9A2040D0D3A594BB69AF18402566`
(newline-normalised digest is the same; 0 CRLF pairs)

**This is a separate turn from the one that raised the objections** (`5e0216a`, 17:57 ET) **and from ANSWER 03** (`9fb75e2`) **and from the RUN-ONLY flip** (`0daae90`). `PROTOCOL.md` forbids one turn both objecting and dismissing. The Critic did not write this file and this turn did not write the attack, the bar draft, PROPOSED 02, ANSWER 03, or the execution flip.

**Nothing here is an ADMIT.** No rule was scored. `R-SKIP-COINFLIP` was not scored, not revived, and not retuned. Its `execution` stays **false**. No post-declaration window outcome file was opened — not `paper/*.json`, not `settlements/*.json`, not `latest/journal.json`. `score_rule` was not called. The bar stays `binding: false`, `admit: false`, `edge_established: false`, `lab_admits: false`, `trading_armed: false`. `founder_read_once` stays false. The series HOLD stands. Trading is **NOT ARMED**. `write_critic_findings()` was not called. The hub was not started or killed. The digest generator was not hand-run. No fee-schedule hash was written. `critic.py` was not edited. `rules.py` was not edited.

**Verdict count:** 5 numbered objections. **5 SUSTAINED.** Every item carries a stated reason. Where a concrete change was demanded of the bar or registry, this turn made it. Where the demand was a `critic.py` / `rules.py` change, it is owed to Systems — this fire does not become Systems.

---

## What I verified myself before sustaining

Hashes recomputed with the same newline-normalised `read_text` → UTF-8 digest `critic.artifact_digest` uses. Byte hash equals the normalised hash on every file below (0 CRLF pairs). I did not import the package (`pydantic` is not installed in this fire; `golf_offshoot` does not import).

| Claim | Critic | My recomputation | Verdict |
|---|---|---|---|
| Bar `.md` bytes attacked | `2732552E…` | `2732552E66EBC97C273FDA46B662B12C1A348BDEDB6C4C7E40BB38C69413277D` | confirmed |
| Bar `.json` bytes attacked | `1269395C…` | `1269395C12B789444176E580A8915EF4F2BC4FD383B809398BD5C585CB0FCAC6` | confirmed |
| Registry bytes attacked | `5C6A61F7…` | `5C6A61F7BDDE4D79B83920F290B6C20340E97747EE0F651F9DD1B9223ECC63CB` | confirmed |
| ANSWER 03 bytes | `ACF62C31…` | `ACF62C3166F367C73FAF965162ECA2E774E1D3E0225FD7155737C0AC7E9E308A` | confirmed |
| CRITIC 04 bytes | (this file's target) | `E7DD9DE5BCE5E0387AE0524A14023288324A9A2040D0D3A594BB69AF18402566` | confirmed |
| Last findings `ran_at` | `2026-09-08T12:02:45−04:00` | same; reviews `5F2AA5F5…` / `2611C255…` / `CD25DD72…` / `83D4463B…` / `07055605…` | confirmed |
| Findings `failing` | `fee_schedule_hash_recorded` only | same; `passed: false` | confirmed |
| `trials_to_date` | 1 | 1 | confirmed |
| Next-look α | `0.05/(2·3) = 0.008333` | `alpha_k(1)` = `0.05/6` = 0.008333… | confirmed |
| SE at n=70, sd 0.784 | 0.093706 | 0.09370592 | confirmed |
| Next-look z / MDE / reject / 80% | 2.394 / 0.2243 / 0.504 / 0.583 | z=2.393994; MDE=0.224331; reject=0.504331; 80%=0.583196 | confirmed |
| First-look z / MDE / reject / 80% | 1.960 / 0.1837 / 0.464 / 0.543 | z=1.959964; MDE=0.183660; reject=0.463660; 80%=0.542525 | confirmed |
| Face `reject_if_mean_d_exceeds` on attacked bytes | 0.464 | 0.464 | confirmed |
| `score_rule` α source | `alpha_k(trials_to_date)` at `:504–505` | same; does not read `alpha_first_look` | confirmed |
| `check_delta_above_detection_floor` α source | registry `trials_to_date+1` at `:272–305` | same; compares `mde` / `reject_if_mean_d_exceeds` / `alpha_first_look` / both power effects | confirmed |
| Two-part preregistration test | (a)+(b) only at JSON `:227` | same; no conventional-prior clause | confirmed |
| `dies_if` extra clause | conventional-prior exception at JSON `:259` | present on attacked bytes | confirmed |
| Face cites hub tip `0a480d4` | MD `:216` / JSON `:81` | present on attacked bytes | confirmed |
| `0a480d4` `decide()` | no `favorite_odds` dispatch | confirmed: after OOS it only special-cases `R-SKIP-COINFLIP`; else `unknown` | confirmed |
| HEAD `_express_selection` | (not claimed live) | dispatches `params.favorite_odds` at `:90–95` | confirmed |
| `watch.json` | absent | absent; I did not start a hub | confirmed |
| Lived/replay keys read by scorer | not read | `window_is_oos` keys `closed > declared_at` only; `_assert_scorable` L2 keys current `execution`; `score_rule` loop has no lived/replay label | confirmed |
| Published marks ≥ 2/3 | 2/24 | not re-opened; already confirmed in ANSWER 03 from the RUN-ONLY table | accepted |

I did **not** open a window outcome file. Numbers above come from the bar, the registry, the commit record, `critic.py` / `rules.py` as text, and arithmetic.

---

## Objection 1 — The next look's α is 0.008333; the rejection threshold on the face is still the spent first-look slot

### **SUSTAINED.**

The face and JSON already name `next_look_k = 2` and `next_look_alpha = 0.008333`, and they label `alpha_first_look: 0.025` historical. The numbers a later score will be compared against on this page were still the spent slot: `mde` 0.1837, `reject_if_mean_d_exceeds` 0.464, 50% power 0.464, 80% power 0.543. `score_rule` reads `trials_to_date` and calls `alpha_k(k_before)`. With `trials_to_date = 1` the next look is α = 0.008333, z = 2.394, MDE = 0.2243, reject if mean(d) > 0.504, 80% power against 0.583. Those are different tests. Labeling 0.025 "historical" does not move the threshold.

I do not score to produce the numbers. I restated them from the bar's own `sd_used = 0.784`, n = 70, SE = 0.093706.

**Changed in the bar.** First-look MDE / reject / 50% / 80% stay on the face, labeled the spent slot. Next-look MDE 0.2243, reject 0.504, 50% 0.504, 80% 0.583 are printed beside them and are the numbers a later score under k = 2 will be compared against. `reject_if_mean_d_exceeds` is no longer 0.464 as the only rejection threshold.

---

## Objection 2 — Binding condition 2's disclosed failing set is not the failing set these bytes would produce

### **SUSTAINED.**

`failing_set_at_last_operator_read: ["fee_schedule_hash_recorded"]` was stamped `2026-09-08T14:04:31-04:00` — before Turn 3, before the declaration increment, before ANSWER 03. The last findings file (`ran_at` 12:02:45) still reviews `5F2AA5F5…` / `2611C255…` / `CD25DD72…`. Those are not `2732552E…` / `1269395C…` / `5C6A61F7…`. Condition 2's own rule: the findings artifact must cover **these** bytes, **or** every failing check is named on the face with a reason. The 14:04 set described other bytes.

I did not import the package. I copied `check_delta_above_detection_floor` (`critic.py:272–305`). On the ANSWER 03 hashes that function recomputes α from `trials_to_date + 1` = 2 and would name at least:

- `mde` 0.1837 vs 0.2243
- `reject_if_mean_d_exceeds` 0.464 vs 0.504
- `alpha_first_look` 0.025 vs 0.008333
- `power.effect_at_50pct_power` 0.464 vs 0.504
- `power.effect_at_80pct_power` 0.543 vs 0.583

After this amendment restates the four design numbers at next-look α, the same copied function would still compare `alpha_first_look` (0.025, correctly the spent first term) to current α_k (0.008333). That key/checker mismatch is owed to Systems. I did not edit `critic.py`. I did not call `write_critic_findings()`. I did not treat "fee hash still empty" as the only fail on the attacked bytes.

**Changed in the bar.** Struck `failing_set_at_last_operator_read` as a description of these bytes. The face now says the last findings do not cover the ANSWER 03 hashes or the bytes this amendment produces, names the copied `delta_above_detection_floor` disagreements on the attacked hashes, and keeps `fee_schedule_hash_recorded` as the standing named fail (empty sha256 after HTTP 429). No placeholder hash.

---

## Objection 3 — The new preregistration row writes a path around the test it just applied

### **SUSTAINED.**

The two-part test has (a) first-naming SHA and timestamp and (b) that timestamp predates informing marks published anywhere on this tree. No third clause. ANSWER 03 applied (b), recorded `verifiably_preregistered: false`, and I agree with that arithmetic. The same row's `dies_if` then named "a later attack+answer accepts the conventional-prior exception as sufficient." That exception is not in the test. Requirement (b) is information, not intent. A conventional prior is a reason the parameter *could* have been chosen without the tape; it does not make the published marks stop existing.

**`verifiably_preregistered` stays false.** I am not adding the exception to the test. I am not flipping the flag.

**Changed in the bar.** Removed the conventional-prior exception from `dies_if` and from the MD paragraph. `dies_if` now names only a predating commit / desk line / dated artifact. The conventional-prior sentence stays as recorded-not-proof. The flag stays **false**.

---

## Objection 4 — The face still cites running-hub tip `0a480d4`, which cannot express the executing rule

### **SUSTAINED.**

The attacked face said the running hub is on `0a480d4` **and** that `R-SKIP-2TO1-FAVORITE` exists and is executing. `0a480d4` is 13:46 EDT. The rule's expression landed at `e9fab5a` (16:56). At `0a480d4`, `decide()` has no `favorite_odds` dispatch: after the OOS check it only special-cases `R-SKIP-COINFLIP`; every other selecting id gets `action = "unknown"`. HEAD `_express_selection` does dispatch `params.favorite_odds`. Those are different binaries.

`watch.json` is absent on this tree. I did not start or kill a hub. I am not asserting a live PID. The face claim was internally inconsistent: either the tip was stale leftover from Turn 3, or the process it named could not express the rule the same sentence said was executing.

**Changed in the bar.** Dropped the claim that the running hub is on `0a480d4`. The face now says no live tip was readable this turn, that `0a480d4` is a historical Turn 2 SHA whose `decide()` cannot express this rule, and that HEAD text can. `currently_reachable` stays **false**.

---

## Objection 5 — The new lived/replay fields are not read by the scorer that would enforce them

### **SUSTAINED.**

ANSWER 03 put `lived_paper_begins_at` / `lived_paper_begins_commit` / `replay_close_after` / `replay_close_at_or_before` on the registry row and on `verdicts.established`. The bar says a later L1/L2 score that treats a window from (16:53, 17:11] as lived **fails this bar**. The machine that scores does not read those keys. I read HEAD `rules.py`. `window_is_oos` keys `closed > declared_at`. `_assert_scorable` L2 keys current `execution`. `score_rule` skips iff `action == "skip"`. No per-window lived/replay label. Labeling the interval without wiring it leaves the hole on the governing artifacts' *reader*.

I did **not** edit `rules.py`. Wiring a scorer read is Systems. This fire is Operator. I did not score.

**Changed.** Face and JSON now say these fields are **prose-only today**. Wiring `window_is_oos` / `_assert_scorable` to read them is owed to Systems, the same way ANSWER 03 named `WATCHED.lab_proposed`. A later score that treats a window from that interval as lived still fails this bar as prose. The scorer cannot fail it as a machine.

---

# Considered and not filed as new objections

- **CRITIC 03 items already answered.** Not re-opened.
- **FEE-AS-SIGNAL / RETUNE-COINFLIP-BAND.** Critic declined both. I do not invert them. I did not open later tape.
- **`favorite_odds=2` as a proven peek.** Critic declined. I do not file it. Objection 3 is the escape hatch, not a peek claim.
- **Scoring, eligible counts, opening the tape.** Forbidden this Job.
- **Unpinned fee hash.** Already the standing condition-2 blocker. I will not write a placeholder.
- **`WATCHED` still frozen on PROPOSED 01.** True, disclosed, unpaid. Not re-filed as if unanswered.
- **Keyword greens / δ-check / vacuous greens.** CRITIC 02; already answered. Not re-filed.

---

## Exact edits made

| # | Edit | From |
|---|---|---|
| 1 | `amended_at` → this turn; `prior_amendment` = ANSWER 03 at `9fb75e2` / 17:42 | standing |
| 2 | Binding condition 1 `met: false`; names CRITIC 04 + this file and the ANSWER 03 hashes answered | 2 (condition 1 again) |
| 3 | First-look MDE/reject/power labeled spent; next-look MDE 0.2243, reject 0.504, 50/80% 0.504/0.583 printed as the k=2 set | 1 |
| 4 | Struck `failing_set_at_last_operator_read` as a description of these bytes; last findings do not cover them; copied `delta_above_detection_floor` disagreements named; `fee_schedule_hash_recorded` remains the standing named fail | 2 |
| 5 | Removed conventional-prior exception from `dies_if` and the MD paragraph; `verifiably_preregistered` stays false | 3 |
| 6 | Dropped the live-hub `0a480d4` claim; no tip readable this turn | 4 |
| 7 | Lived/replay fields labeled prose-only; wiring owed to Systems | 5 |
| 8 | Registry row: lived/replay note says the scorer does not read these keys | 5 |

### Deliberately **not** changed

- **`binding` stays `false`.** Condition 1 is unmet on these new bytes. Condition 2 is not met (findings do not cover these bytes; fee hash unpinned; copied `delta_above_detection_floor` would still disagree on `alpha_first_look` vs current α_k). Condition 3 is not met (Founder has not read).
- **`founder_read_once` stays false.** This turn did not request it and did not impersonate it.
- **`schedule_sha256` left empty.** I will not fabricate a hash.
- **No rule scored. `score_rule` was not called. No window outcome opened. `trials_to_date` not incremented.**
- **`R-SKIP-COINFLIP.execution` stays false.** Do not score it. Do not retune `(0.45, 0.55)`.
- **`currently_reachable` stays false.** Do not flip it after answering a face-tip inconsistency.
- **`R-SKIP-2TO1-FAVORITE.execution` stays true.** RUN-ONLY stands. This turn does not overrule the flip.
- **`verifiably_preregistered` stays false.** Conventional-prior is not a third test clause.
- **No file under `golf-offshoot/src/` edited.** Wiring lived/replay into the scorer, and stopping `check_delta_above_detection_floor` from comparing `alpha_first_look` to current α_k, are owed to Systems.
- **`write_critic_findings()` was not called.**
- **Hub not started or killed. Digest generator not hand-run.**

### Hashes at the start of this turn (the bytes CRITIC 04 attacked)

| File | SHA-256 (bytes = newline-normalised) |
|---|---|
| `LEARNING_LANE_15M_EVIDENCE_BAR.md` | `2732552E66EBC97C273FDA46B662B12C1A348BDEDB6C4C7E40BB38C69413277D` |
| `LEARNING_LANE_15M_EVIDENCE_BAR.json` | `1269395C12B789444176E580A8915EF4F2BC4FD383B809398BD5C585CB0FCAC6` |
| `LEARNING_LANE_15M_RULES.json` | `5C6A61F7BDDE4D79B83920F290B6C20340E97747EE0F651F9DD1B9223ECC63CB` |

Amending moves those digests. Condition 1 is therefore unmet for the resulting bytes.

---

## Closing — binding status

**The bar remains `binding: false`.** It is not close.

Of the three binding conditions, **none is met** on the bytes this amendment produces. Condition 1 is met only for a named attack+answer pair whose hashes equal the bytes proposed to bind. This pair answers the ANSWER 03 hashes. These bytes are not those hashes.

**Condition 2 is not met.** The last findings file does not review these hashes. `fee_schedule_hash_recorded` still fails for a real reason. I declined to fabricate a hash. I declined to call `write_critic_findings()` in the same turn that amends the bar.

**Condition 3 is not met.** Founder read-once has not happened and this turn did not request it.

`currently_reachable` stays false. `R-SKIP-2TO1-FAVORITE` exists and is executing on paper; it is not verifiably pre-registered, the bar is not binding, and L2 has not been lived under a binding bar. `R-SKIP-COINFLIP` still cannot Establish.

`lab_admits=false`. Golf idle stays ON. The series HOLD stands. Trading is **NOT ARMED**. I did not score.

Handoff → `chief-of-staff`.
