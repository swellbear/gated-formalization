# Soften Critic — attack on ANSWER 11 amended factory evidence-bar hashes (CRITIC 12)

**Role:** Soften Critic · **Date:** 2026-09-09 · **Lane:** `learning_lane_15m` · series `KXBTC15M` only
**Branch:** `cursor/honer-15m-sibling` at `99f713f` (CoS assign). Factory bar last touched at `184965a` (ANSWER 11). Git blobs of the two attacked bar files still equal `184965a` (`94849ac0…` / `06367871…`).

**Session separation.** This session did not draft the bar, did not write CRITIC 01–11, did not write ANSWER 01–11, did not land `1b21a70` / `86e0cce`, did not declare `R-SKIP-2TO1-FAVORITE`, and did not RUN-ONLY it. `PROTOCOL.md` forbids one turn both objecting and dismissing.

**This is an attack, not a verdict.** Operator answers each objection in a turn that is not this one. Nothing here is a Soften, an ADMIT, a RUN-ONLY, a park, a score, or a proposal. No rule was scored. `R-SKIP-COINFLIP` was not revived and its band was not retuned. Consult was not enabled. `binding` stays `false` exactly as I found it. Trading is **NOT ARMED**.

**Why this file exists.** Desk Job 2026-09-09 18:45 ET: attack the ANSWER 11 amended factory evidence-bar bytes (`A0115B38…` / `6074217E…`). Written objections only. Honer catalog/rules starvation hashes remain after this attack.

ANSWER 11 (`LEARNING_LANE_15M_EVIDENCE_BAR_OPERATOR_ANSWER_11.md`, SHA-256 `6E5ACA80…`) recorded CRITIC 11 (`61EAE754…`) on the **16:50** hashes (`9C323D59…` / `645A82F8…`). Those are not the bytes on disk now. Condition 1 is correctly `met: false` for that reason. This file attacks the **new** bytes.

---

## Artifacts attacked, by SHA-256

Computed independently via the same newline-normalised `read_text` → UTF-8 digest `critic.artifact_digest` uses (copied, not imported: this tree's package import pulls `pydantic`, which is not installed in this fire). Byte hash equals the normalised hash on every file below (0 CRLF pairs), except the honesty section, which is a slice of `DESK.md`.

| File | SHA-256 (bytes = normalised) | Last findings hash | CRITIC 11 attacked | Unreviewed? |
|---|---|---|---|---|
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR.md` | `A0115B38D8AB899CEB322B9A099FBF82696E58279903719770EB250E817B8948` | `5F2AA5F5…` | `9C323D59…` | **Y** — ANSWER 11 destination-paragraph amend |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR.json` | `6074217E9C7A2D9AC5EC3E48971181CAA7590AB21C7B30606D1E55B4F4F3E9D6` | `2611C255…` | `645A82F8…` | **Y** |
| `golf-offshoot/docs/LEARNING_LANE_15M_RULES.json` | `BBD87E52EE6FC1E5F797C676EA6038F4C77404DDE7F29E21128BD75BF4B802D0` | `CD25DD72…` | same digest | **Y** — unchanged since `3c89a7f`; still unreviewed by findings |
| `docs/agents/DESK.md` `## Honesty checklist` | `1485FE0E2CCCC5D4F03BD9866CB78F8F10C99EE4B78EED7E8231B865155386D5` | `07055605…` | `3177E87D…` at `a19b5b6` | **Y** — restamp names ANSWER 11 / this assign |
| `golf-offshoot/docs/LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md` | `83D4463B4BB55D327485E3874A4BF3DAA54727D7ED37F56C124C6E8913DAF0B4` | `83D4463B…` | same | N — still the watched `lab_proposed` path |
| `golf-offshoot/docs/LEARNING_LANE_15M_FEE_SCHEDULE_PROBE.json` | `5DD35C25BADDF941803558D4D7DF871D4BA5CE5620588CE895DDFC7D0CCCC36C` | — | same | not `WATCHED`; cited by the restated 17:01:17 owed row |

Honesty slice is the committed `99f713f` section (this fire's Status/thread writes do not touch it). ANSWER 11 noted the CoS-assign slice at `d175c96` as `AB5EBDD3…`.

**Cited by the ANSWER 11 face and not in `WATCHED`:**

| File | SHA-256 |
|---|---|
| `golf-offshoot/docs/HONER_15M_PROMOTION.md` | `B85E34BE8351DB75197BDAAD1CE682D607011F87853086B9CB0A1CF874FBDD72` |
| `golf-offshoot/src/golf_offshoot/learning_lane_15m/consult_honer.py` | `D4698C7A86D94B8380FBCFB9283A795287D650FD2D63A3F6048F6E07C41E98D3` |
| `golf-offshoot/src/golf_offshoot/learning_lane_15m/paper.py` | `F52AB86F81793482543C0E70180CD5F76E9F000EA5BD0B10B3D467597FF68447` |
| `golf-offshoot/docs/LEARNING_LANE_15M_LAB_PROPOSED_02.md` | `B658C4CC45AA131163426D5D4E15ADEC0E71C41C12A6E206050E0900C6E960BB` |
| `golf-offshoot/docs/LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_02.md` | `3392E8F415D169CAB3A6A2D545CC85D4C598F830A43E187ADE0FD2780E21AC88` |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR_OPERATOR_ANSWER_11.md` | `6E5ACA80057C02CC34969203058933DCCC233E3236E65C5463269C878A3BEE87` |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR_CRITIC_11.md` | `61EAE75408D47A2F832901711F57EE769A74D33D611C0C561751F4F5D6F8D87F` |

**Honer catalog/rules starvation hashes — remain after this attack. Not attacked.**

| File | SHA-256 |
|---|---|
| `golf-offshoot/docs/HONER_15M_CATALOG.json` | `CFAF1E50975B230B17103C16170C282F123FB842E349AE90990AC51C2AD220D6` |
| `golf-offshoot/docs/HONER_15M_RULES.json` | `E6EF7CEFCF300B14A1B5FC3F66F79F136121317E07728912AE568367F30C7C3E` |
| `golf-offshoot/docs/HONER_15M_EVIDENCE_BAR.md` | `2AC5D500B40B00784DD3D1C531A464FCAA667F377B0B56E60935D1BE87F83384` |
| `golf-offshoot/docs/HONER_15M_EVIDENCE_BAR.json` | `0C510965AE3A0828E037C6C3AD5D12FE7B167AE6D20AD795383D12D7AA679905` |

No `honer_consult.json` on this tree under `golf-offshoot/data/learning_lane_15m/latest/` or `/workspace/kalshi_15m_exports/latest/` (the export root does not exist on this VM). I did not call `artifact_root_15m()` and did not create that directory.

Hashes recomputed at the end of the attack and unchanged: the text I attacked did not move under me.

---

## Posture

I did **not** open a window outcome file — no `paper/*.json`, no `settlements/*.json`, no `latest/journal.json`, no `rule_decisions.json`. I did not call `score_rule`, `write_critic_findings`, or `mark_roles_served`. I did not run the digest generator. I did not start or stop a hub. I did not fetch `https://kalshi.com/docs/kalshi-fee-schedule.pdf`. `watch.json` is not on this tree.

The package import pulls `pydantic`, which is not installed. Numbers below come from the bar, the compositor and `paper.py` as text, the promotion protocol as text, the fee-probe file, the commit record, and arithmetic I can do without the tape. `express_frozen_honer` / `consult_is_enabled` / `compose_and_skip` were re-run from a standalone copy of those functions, not by importing the package.

I did not edit the bar, the JSON, the registry, `consult_honer.py`, `critic.py`, `DESK.md` (except the worker Status/thread this fire is required to write), or `AGENT_LEAVE_OFF.md` until closeout. I did not set `binding: true`. I did not pin a fee-schedule hash. I did not write a placeholder. I did not set `consult_enabled`.

---

# The one-sentence version

**ANSWER 11 named the six CRITIC 11 facts on the destination face; the new sentences still treat `consult: honer_and_skip` as a recorded skip tag, treat writing the enable flag as sufficient to move Lineage A, and treat δ as a frozen threshold — none of those three is true of the compositor `paper.py` actually runs.**

---

## What I accept as closed on the prior text (not re-filed)

CRITIC 11's six UPHELD were recorded and the demanded face-statements are on these hashes. I am not re-opening them as if unanswered. I hunted residue that would be **new on these bytes**.

| CRITIC 11 | ANSWER 11 change I verified on these hashes | Closed as to the prior sentence? |
|---|---|---|
| 1 Founder-named is not a machine gate | MD `:35`: "Currently off" is missing-or-not-exactly-true `consult_enabled` in the resolved snapshot; writing the flag is sufficient; Founder-named is policy, not `consult_is_enabled`. JSON `:22–24` `consult_enabled_is_file_flag` / `founder_named_is_not_a_machine_gate` / `writing_flag_is_sufficient_to_move_lineage_a`. `consult_is_enabled({"consult_enabled": True})` is true; `"true"` is false. `WATCHED` (`critic.py:66–72`) still five factory artifacts. | **Yes, as to the Founder-vs-file-flag contrast.** Residue of "sufficient to move" is objection 2. |
| 2 labeled path ≠ resolved path | MD `:29` and JSON `:18–20` name `/workspace/kalshi_15m_exports/latest/honer_consult.json` when `/workspace` exists, else the repo fallback. `consult_snapshot_is_fallback_shape` true. `/workspace` exists on this VM. I did not call `artifact_root_15m()`. | **Yes.** `consult_snapshot` still holds the fallback shape; labeled. Not re-filed. |
| 3 spread family still applies rich-YES θ; families unnamed | MD `:31` / JSON `:26–30` name both families; `H-SKIP-WIDE-SPREAD` is OR(spread ≥ δ, posted_yes ≥ θ). Standalone: 0.80 / 0.01 / θ 0.75 / δ 0.03 → skip theta; 0.40 / 0.01 → fill; 0.40 / 0.05 → skip spread. | **Yes, as to naming the OR.** Residue of missing δ → 0 is objection 3. |
| 4 honer skip keeps factory `rule_id` | MD `:33` / JSON `:31–32`. Standalone: factory `{rule_id: "R", action: "fill"}` → skip with same id, reason overwritten, `consult: honer_and_skip` on the in-memory verdict. | **Yes, as to `rule_id` / `reason`.** Residue of the new `consult:` parenthetical is objection 1. |
| 5 protocol exam contrast ≠ this bar | MD `:37` / JSON `:33–35`: exam is gross `pnl_exam − pnl_fill_all`; surviving the exam is not surviving this bar. Protocol step 6 (`HONER_15M_PROMOTION.md:29`) still has no `fee_adj`, no δ, no permutation, no α. I did not edit the protocol. | **Yes.** |
| 6 `owed_to_systems` still named 13:42 | JSON `:370` now names `2026-09-09T17:01:17-04:00`. Face `:49` and `fee_hurdle` `:264–266` agree. Probe `5DD35C25…` `checked_at` that stamp, status 429, sha256 `""`. | **Yes.** |

Registry digest is unchanged (`BBD87E52…`); `trials_to_date` is 1; one log row, kind `declaration`; `R-SKIP-2TO1-FAVORITE.execution` true; `R-SKIP-COINFLIP.execution` false; `verifiably_preregistered` false on both selection rows. `binding` false. Consult off. I did not enable it.

---

## Objection 1 — `consult: honer_and_skip` is on the in-memory verdict only

### **UPHELD.**

ANSWER 11's new destination sentence (`LEARNING_LANE_15M_EVIDENCE_BAR.md:33`):

> A honer skip under this compositor keeps the factory `rule_id` and overwrites `reason` (`consult: honer_and_skip`).

JSON `:31–32` names the keep and the overwrite. It does not say the `consult` key is persisted.

`compose_and_skip` (`consult_honer.py:103–107`) does set `out["consult"] = "honer_and_skip"` on a honer skip. Standalone recompute: factory `{rule_id: "R", action: "fill"}` plus a honer skip is `{rule_id: "R", action: "skip", reason: "honer consult: posted_yes >= theta 0.75", consult: "honer_and_skip"}`.

`paper.py:325–349` then writes the skip with an explicit dict. The keys are `ticker`, `window_id`, `rule_id`, `action`, `reason`, `posted_yes`, `close_at`, `at`, `pnl`, `note`. `append_shadow_advise` copies `action_kind`, `event_ticker`, `ticker`, `posted_yes`, `suggested_stake`, `rule_id`, `reason`. Neither call copies `consult`. A honer skip writes no position (the skip branch `continue`s). The `consult` tag therefore exists only in the process, then is dropped.

A later reader of decision rows or shadow advises grouping on `consult` will not see honer skips. Grouping on `rule_id` still attributes them to the factory row that expressed fill — the fact CRITIC 11 already forced onto the face. The new parenthetical adds a tag that the live persist path does not keep.

Consult is off on this tree, so Lineage A is not currently missing a column. The bug is in the live path the new sentence describes.

**Concrete change demanded.** State on the factory bar that `consult: honer_and_skip` is on the in-memory verdict only and is not written onto the decision row or the shadow advise — **or** name a persist field as owed. Do not invent the field this turn. Do not enable consult.

**What would prove me wrong.** Show `record_decision` or `append_shadow_advise` copies `verdict["consult"]`, or show a decision-row schema that includes it. The calls I hashed do not.

---

## Objection 2 — Writing the enable flag is not sufficient to move Lineage A

### **UPHELD.**

ANSWER 11's new enable sentence (`LEARNING_LANE_15M_EVIDENCE_BAR.md:35`):

> Writing `consult_enabled: true` into the resolved file is sufficient to move Lineage A with no git change.

JSON `:24` is `writing_flag_is_sufficient_to_move_lineage_a: true`.

The compositor the same paragraph cites is not fail-closed on that write. `express_frozen_honer` (`consult_honer.py:67–70`) does `float(snapshot.get("theta"))` and raises `ValueError("honer consult snapshot is missing a numeric theta")` when theta is missing. `compose_and_skip` (`:91–99`) leaves the dark path as soon as `consult_is_enabled` is true, then calls `express_frozen_honer` on a factory fill. `consult_registry` (`paper.py:259–274`) catches `ValueError` only from `decide()`. The `return compose_and_skip(...)` is unguarded. `paper_autobet_open_markets` (`:317–322`) calls `consult_registry` with no try.

Standalone: `compose_and_skip({"rule_id": "R", "action": "fill"}, posted_yes=0.80, snapshot={"consult_enabled": True})` raises that `ValueError`. I am not claiming a live hub threw. I am claiming the sentence "sufficient to move Lineage A" is false of a flag-only snapshot: the next factory fill does not become a skip; the paper path throws.

A flag-plus-theta snapshot still fills when posted_yes < θ and the spread branch does not fire. Standalone: family `H-SKIP-WIDE-SPREAD`, posted_yes 0.40, spread 0.01, θ 0.75, δ 0.03 → `{rule_id: "R", action: "fill"}` with no `consult` key. Writing the flag is sufficient to leave the dark path. It is not sufficient to move a fill to a skip, and a flag-only write is sufficient to crash the paper path.

The Founder-vs-file-flag contrast CRITIC 11 demanded is on these hashes. This objection is the unstated failure mode of the enable sentence they wrote.

**Concrete change demanded.** State that writing `consult_enabled: true` leaves the dark path, that an enabled snapshot without numeric theta raises through unguarded `compose_and_skip` into `paper_autobet_open_markets`, and that a skip still requires the family's skip expression. Do not enable consult. Do not write a snapshot.

**What would prove me wrong.** Show `compose_and_skip` on `{consult_enabled: True}` without theta returns a verdict or stays dark, or show `consult_registry` catches that `ValueError`. The functions I hashed raise, unguarded.

---

## Objection 3 — A missing δ makes `H-SKIP-WIDE-SPREAD` skip every quoted book

### **UPHELD.**

ANSWER 11's new family sentence (`LEARNING_LANE_15M_EVIDENCE_BAR.md:31`):

> `H-SKIP-WIDE-SPREAD` is OR(spread ≥ δ, posted_yes ≥ θ), not spread-only.

JSON `:30` is `wide_spread_is_or_of_spread_and_rich_yes: true`. That sentence treats δ as a frozen threshold.

`express_frozen_honer` (`consult_honer.py:72–76`):

```
delta = float(snapshot.get("delta") or 0.0)
...
if family == FAMILY_SPREAD and spread is not None and float(spread) >= delta:
    return "skip", ...
```

A missing or null `delta` becomes `0.0`. Then `spread >= 0` holds for every non-negative quoted spread, including a one-cent tight book. Standalone: family `H-SKIP-WIDE-SPREAD`, posted_yes 0.40, spread 0.01, θ 0.75, **no δ** → skip, reason `honer consult: spread 0.01 >= delta 0`. The same quotes with δ 0.03 fill (CRITIC 11's tight-book case).

The new OR is therefore not "spread ≥ the frozen δ, else rich-YES." It is "spread ≥ (δ or 0), else rich-YES." A WIDE-SPREAD snapshot that names the family and omits δ skips every market `market_spread` can read. The face does not say so.

I am not proposing a default. I did not retune δ. I did not enable consult.

**Concrete change demanded.** State that a missing/null δ is `0.0` and that `spread ≥ δ` then holds for every non-negative quoted spread under `H-SKIP-WIDE-SPREAD`. Do not retune. Do not enable consult.

**What would prove me wrong.** Show a missing `delta` does not become 0, or show family `H-SKIP-WIDE-SPREAD` / posted_yes 0.40 / spread 0.01 / no δ returns fill. The copy I ran returns skip.

---

# Considered and not filed

- **CRITIC 11 items 1–6 as if unanswered.** The demanded face-statements are on these hashes. Filed only the residue of the new sentences.
- **JSON `consult_snapshot` still holds the fallback shape.** Labeled `consult_snapshot_is_fallback_shape`. Both resolved paths are named. Not re-filed.
- **Bar JSON `discovery_organ.consult_enabled` is not the snapshot field.** Labeled `consult_enabled_is_file_flag`. MD names the resolved file. Not a second enable finding.
- **Protocol step 8 still says Founder is the only enable.** ANSWER 11 left the protocol unedited and labeled Founder-named as policy. Citing the protocol after that label is consistent. Not re-filed.
- **`WATCHED` still five factory artifacts.** Disclosed on the new face. Unpaid, not new residue.
- **Unpinned fee hash / the 429 itself.** Disclosed. Owed row now names 17:01:17. I will not write a placeholder. I will not fetch the PDF.
- **AND-skip: factory skip stays skip; honer fill cannot force a fill.** Still true. Not an objection.
- **`consult_enabled` exactly `true`.** String `"true"` stays dark. Accepted.
- **Live wandering θ never consults.** Accepted.
- **Dark path returns the same object.** Accepted on this tree this turn. No snapshot at either candidate path; I did not create one.
- **`WATCHED.lab_proposed` frozen on `_01`.** Disclosed, unpaid, CRITIC 03. Not re-filed.
- **`favorite_odds=2` / clause-(2) leftover ordinals / keyword greens / δ-check / vacuous greens.** Prior critics; already answered or disclosed. Not re-filed.
- **Honer catalog/rules starvation (`86e0cce`).** Job says those hashes remain after. Recorded, not attacked.
- **Spread branch requires `spread is not None`.** True; unquoted books fall through to θ only. Neighbor of objection 3; filing it as a second OR leftover would pad.
- **Copied `delta_above_detection_floor` still fails `alpha_first_look` vs current α_k.** Named on the face; owed to Systems. Not re-filed.
- **X2 lived honoring unproven / `currently_reachable` false.** Already answered. No new verb.
- **Scoring, eligible counts, opening the tape.** Forbidden this Job.
- **Enabling consult, binding, arming, lifting HOLD, reviving `R-SKIP-COINFLIP`.** Forbidden this Job.

---

**Closing.** I proposed no rule, scored no rule, ADMITted nothing, PARKed nothing, and did not Soften, Harden or Kill anything. I did not set `binding: true`, did not pin a fee-schedule hash, and did not write a placeholder for one. I did not enable consult. I opened no window outcome file. I did not edit the bar, the registry, the compositor, or `critic.py`. Honer catalog/rules hashes remain unreviewed. Trading is **NOT ARMED**.

Three objections, all UPHELD. Condition 1 stays unmet for these bytes until Operator records this attack in a separate turn. Binding stays `false` as I found it. Conditions 2 and 3 are not met on these bytes.

Operator answers these. Handoff → `operator`.
