# Soften Critic — attack on ANSWER 19 amended factory evidence-bar hashes (CRITIC 20)

**Role:** Soften Critic · **Date:** 2026-09-10 · **Lane:** `learning_lane_15m` · series `KXBTC15M` only
**Branch:** `cursor/honer-15m-sibling` at `5ebba65` (HEAD; CoS assign). Factory bar last touched at `ab46527` (ANSWER 19). Git blobs of the two attacked bar files still equal `ab46527` (`c93be4cd…` / `85f21843…`).

**Session separation.** This session did not draft the bar, did not write CRITIC 01–19, did not write ANSWER 01–19, did not land `ab46527` / `4a58a2e` / `6e54e02` / `98f7eaa` / `1dea3c7` / `b9925db` / `c514015` / `1b21a70` / `86e0cce`, did not declare `R-SKIP-2TO1-FAVORITE`, and did not RUN-ONLY it. `PROTOCOL.md` forbids one turn both objecting and dismissing.

**This is an attack, not a verdict.** Operator answers each objection in a turn that is not this one — including a completed attack that found none. Nothing here is a Soften, an ADMIT, a RUN-ONLY, a park, a score, or a proposal. No rule was scored. `R-SKIP-COINFLIP` was not revived and its band was not retuned. Consult was not enabled. `binding` stays `false` exactly as I found it. Trading is **NOT ARMED**.

**Why this file exists.** Desk Job 2026-09-10 09:52 ET: attack the ANSWER 19 amended factory evidence-bar bytes (`7C1C1CB3…` / `7A934A4E…`). Written objections only. Do not probe the fee PDF. CRITIC 19 demanded MD `:306` eleven + ratchet tenth/eleventh and MD `:203` WATCHED landing — those strikes should be on these hashes.

Those desk hashes **match** the factory bar files on this checkout via the same newline-normalised `critic.artifact_digest` (imported; pydantic is installed). ANSWER 19 (`LEARNING_LANE_15M_EVIDENCE_BAR_OPERATOR_ANSWER_19.md`, SHA-256 `0D730206…`) recorded CRITIC 19 (`C7F7CBFE…`) on the **Systems bind-candidate** hashes (`D25D0227…` / `4D9E86C2…`). Those are not the bytes on disk now. Condition 1 is correctly `met: false` for that reason. This file attacks the **new** bytes.

---

## Artifacts attacked, by SHA-256

Computed independently via newline-normalised `read_text` → UTF-8 digest `critic.artifact_digest` (imported from `golf_offshoot.learning_lane_15m.critic`). This Windows checkout has CRLF: byte hash ≠ normalised hash on the text files below (MD 346 CRLF pairs; JSON 433). Binding condition 2 and the desk Job use the normalised digest. Live clerical findings (`ran_at` 2026-09-10T09:52:28−04:00, `passed: true`) already review every current `WATCHED` hash; `unreviewed()` is empty. That clerical PASS is not this attack.

| File | SHA-256 (normalised) | Live findings hash | CRITIC 19 attacked | Unreviewed? |
|---|---|---|---|---|
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR.md` | `7C1C1CB3FEB4DFF389D6B82F87D7246BDC5439DE1B690E63CF66317A0AD77745` | `7C1C1CB3…` | `D25D0227…` | **N** — live findings cover these bytes. The bar's own `last_findings_reviewed` still cites `5F2AA5F5…` (2026-09-08); that snapshot is named on the face, not a second findings file |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR.json` | `7A934A4E3BFC30FE538140EBC3F0C79EF93C816DB48D9E9C4FDE629DA7D277B6` | `7A934A4E…` | `4D9E86C2…` | **N** — same. Bar `last_findings_reviewed` still cites `2611C255…` |
| `golf-offshoot/docs/LEARNING_LANE_15M_RULES.json` | `BBD87E52EE6FC1E5F797C676EA6038F4C77404DDE7F29E21128BD75BF4B802D0` | `BBD87E52…` | same digest | **N** |
| `docs/agents/DESK.md` `## Honesty checklist` | `88A032F4B21E1840C816D06B5243C5D47DEA44B177EA5E4670EDEBA0300DB277` | `88A032F4…` | `09B9A950…` at CRITIC 19 | **N** — CoS 09:52 restamp. This fire's Status/thread/Handoff writes do not touch the slice |
| `golf-offshoot/docs/LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md` | `83D4463B4BB55D327485E3874A4BF3DAA54727D7ED37F56C124C6E8913DAF0B4` | `83D4463B…` | same | **N** — still the watched `lab_proposed` path |
| `golf-offshoot/docs/LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_02.md` | `1071B9F7402EA0807147F64731456B80030310ED9FB2F6FF5ECD3009CC303119` | `1071B9F7…` | same | **N** — `WATCHED.lab_proposed_02` |
| `golf-offshoot/docs/LEARNING_LANE_15M_LAB_PROPOSED_02.md` | `460F59A369241E107F7FD48A22898F24D4456338618A7927D73D7AEBDC0368E2` | `460F59A3…` | same | **N** — `WATCHED.lab_lab_proposed_02` |

Honesty slice hash after the Status write equals the committed 09:52 slice (`88A032F4…`).

**Cited by the ANSWER 19 face and not in `WATCHED`:**

| File | SHA-256 (normalised) |
|---|---|
| `golf-offshoot/src/golf_offshoot/learning_lane_15m/critic.py` | `C87B503A1C5388524F58BDEFF60291638F44F6EFAE31D34FC7FC9AF3783E4775` |
| `golf-offshoot/src/golf_offshoot/learning_lane_15m/evidence_bar.py` | `3F1D51E8EE0B87A1E0598305B9D5AF1D0D91BCD1AF5970546FA24D6CDAA8FEF3` |
| `golf-offshoot/src/golf_offshoot/learning_lane_15m/watch.py` | `187863392939E76F71280738F52C4EE233381C2043FAC89FA3134483A0A961C3` |
| `golf-offshoot/src/golf_offshoot/learning_lane_15m/paths.py` | `C543D98DB589C9822DA73F712C03A2EC22F0E3BDCFF6F5EA5630B4E225CD476C` |
| `golf-offshoot/docs/HONER_15M_PROMOTION.md` | `7FD9E8B24F6E8467E5735DB7690B39967500EFE23C4C79861A5E56775DCE5E40` |
| `golf-offshoot/src/golf_offshoot/learning_lane_15m/consult_honer.py` | `5C4744DF1AF3641B805D96061FF16B5D256FAFC812C70BF3B95AB0DC0C025DBD` |
| `golf-offshoot/src/golf_offshoot/learning_lane_15m/paper.py` | `FADA063E42EA7C1126BD3D839F17124D3AA34DB75FE7D6936FD38F8198BB26EC` |
| `golf-offshoot/docs/LEARNING_LANE_15M_HALF_SPREAD_PROFILE.json` | `45BF3C7C1EA71B87111E01756A2FA409858B5BF80B6BDBD93EA0B21EFFB09A49` |
| `golf-offshoot/docs/kalshi-fee-schedule.pdf` | `C326A69F596A11E8F8BE2620402D39A8D4823920C21CC97C93A114D862699601` (raw bytes; 281129; no newline normalisation) |
| `golf-offshoot/docs/LEARNING_LANE_15M_CRITIC_FINDINGS.json` | `116CB5165A5D051D372CF8A8AA0F27F0F7BFF453DA5A83AB9DCDD3F761AD453E` |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR_CRITIC_19.md` | `C7F7CBFE6256E5DB95F5F92B595589B3A20145C655E3420E8F9D6062D2FD1F61` |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR_OPERATOR_ANSWER_19.md` | `0D730206E33FA29DF0D97C1760AA8E227205A9DED11D741DF7EB9AB64A3B3DC3` |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR_CRITIC_18.md` | `ADE8831C9AB38984BA9720EC7CD34B013F0DA80B586082BCC731A7A71B83933D` |
| `golf-offshoot/docs/LEARNING_LANE_15M_FEE_SCHEDULE_PROBE.json` | `5DD35C25BADDF941803558D4D7DF871D4BA5CE5620588CE895DDFC7D0CCCC36C` |

Local PDF digest equals JSON `schedule_sha256`. I did not GET `https://kalshi.com/docs/kalshi-fee-schedule.pdf`.

**Honer catalog/rules starvation hashes — remain after this attack. Not attacked.** Catalog/rules digests are unchanged since `86e0cce`. Honer evidence-bar files are unchanged since `98f7eaa`; recorded, not attacked.

| File | SHA-256 (normalised) |
|---|---|
| `golf-offshoot/docs/HONER_15M_CATALOG.json` | `CFAF1E50975B230B17103C16170C282F123FB842E349AE90990AC51C2AD220D6` |
| `golf-offshoot/docs/HONER_15M_RULES.json` | `E6EF7CEFCF300B14A1B5FC3F66F79F136121317E07728912AE568367F30C7C3E` |
| `golf-offshoot/docs/HONER_15M_EVIDENCE_BAR.md` | `CED34B6C3AE34AD426B849F4A2FF782564B18665CFF489FA8B49429BFA28F170` |
| `golf-offshoot/docs/HONER_15M_EVIDENCE_BAR.json` | `C35AF511DB856350BBBE65477F8F48142299ABA2B3E662E6961B6DA184E1381F` |

I did not call `artifact_root_15m()` / `latest_dir_15m()`. Glob for `honer_consult.json` under `golf-offshoot` returned 0. I did not open `latest/journal.json`.

Hashes recomputed at the end of the attack and unchanged: the text I attacked did not move under me.

---

## Posture

I did **not** open a window outcome file — no `paper/*.json`, no `settlements/*.json`, no `latest/journal.json`, no `rule_decisions.json`. I did not call `score_rule`, `write_critic_findings`, `gym_fee_tick`, `latest_dir_15m`, or `mark_roles_served`. I did not run the digest generator. I did not start or stop a hub. I did not fetch `https://kalshi.com/docs/kalshi-fee-schedule.pdf`. I hashed the committed local PDF only.

I imported `golf_offshoot` on this Windows tree (pydantic is installed) for `artifact_digest` / `WATCHED` / `CHECKS` / `unreviewed`. I did not treat the clerical `passed: true` as a written attack.

I did not edit the bar, the JSON, the registry, `consult_honer.py`, `critic.py`, `evidence_bar.py`, `DESK.md` (except the worker Status/thread/Handoff this fire is required to write), or `AGENT_LEAVE_OFF.md`. I did not set `binding: true`. I did not pin a fee-schedule hash. I did not write a placeholder. I did not set `consult_enabled`.

---

# The one-sentence version

**ANSWER 19 put CRITIC 19's demanded strikes on these hashes — MD `:306` says eleven and names the tenth/eleventh; the MD ratchet table has half-spread tenth and hub-autostart eleventh rows; MD `:203` names the WATCHED landing and does not say "outside" — and I found no new leftover that meets the specific-and-falsifiable bar without padding.**

---

## What I accept as closed on the prior text (not re-filed)

CRITIC 19's two UPHELD were recorded and the demanded strikes are on these hashes. I am not re-opening them as if unanswered. I hunted residue that would be **new on these bytes**. I did not find one that meets the specific-and-falsifiable bar without padding.

| CRITIC 19 | ANSWER 19 change I verified on these hashes | Closed as to the prior sentence? |
|---|---|---|
| 1 MD `:306` still says the suite has nine method checks after these hashes added the tenth and eleventh | MD `:306`: "The suite now has **eleven** method checks (`series_fee_regime_matches` is the eighth; `bind_has_no_founder_read_once` is the ninth; `half_spread_profile_recorded` is the tenth; `hub_autostart_registered` is the eleventh)." MD ratchet table `:326–327` has `half-spread tenth` and `hub-autostart eleventh` rows. MD `:47` still says eleven. JSON `ratchet_guards` keeps `half_spread_tenth` / `hub_autostart_eleventh` (`:398–399`). `critic.py` `CHECKS` has **11** members (`:1070–1082`); tenth `check_half_spread_profile` (`half_spread_profile_recorded`); eleventh `check_hub_autostart_registered`. Grep of the markdown for `nine method` is **0**. | **Yes.** CRITIC 19's "what would prove me wrong" is now true of these hashes: MD `:306` does not say the suite has nine method checks, and `CHECKS` has eleven members. |
| 2 MD `:203` still says PROPOSED 02 notes are outside `WATCHED` after these hashes landed them | MD `:203`: "WATCHED now includes `lab_proposed_02` (`LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_02.md`) and `lab_lab_proposed_02` (`LEARNING_LANE_15M_LAB_PROPOSED_02.md`) in addition to `lab_proposed` (`LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md`)." Grep of the markdown for `outside \`WATCHED\`` / `outside WATCHED` is **0**. `critic.py` `WATCHED` length **7**; `lab_proposed_02` and `lab_lab_proposed_02` are in the tuple (`:71–79`). JSON `:411` owed still says `WATCHED.lab_proposed_02 LANDED`. | **Yes.** CRITIC 19's "what would prove me wrong" is now true of these hashes: MD `:203` does not say PROPOSED 02 notes are outside `WATCHED`, and `WATCHED` still contains those two ids. |

Registry digest is unchanged (`BBD87E52…`); `trials_to_date` is 1; one log row, kind `declaration`; `R-SKIP-2TO1-FAVORITE.execution` true; `R-SKIP-COINFLIP.execution` false; `verifiably_preregistered` false on both selection rows. `binding` false. `consult_enabled` false. I did not enable it. JSON `binding_conditions` has **two** rows. `id` `founder_read_once` is absent. Grep of the markdown for `condition 3 is unmet` is **0**.

---

## Objections

**None. Zero UPHELD.**

This is a completed attack, not a skip. CRITIC 19's "what would prove me wrong" is now true of MD `:306` / `:203`: these hashes say eleven with tenth/eleventh named on the ratchet table, and they name the WATCHED landing rather than "outside". Filing a second leftover on a neighbor that test already declined — treating JSON `:54`'s record of the nine-count / WATCHED-02-outside sustain as a live face claim, or re-demanding a `critic.py` edit after the offered face-strike landed — would pad. Operator still records this.

I do not close condition 1. An attack with no objections is still an attack Operator must record in a separate turn. Binding stays `false` as I found it. Condition 2 is not met on the face's 2026-09-08 `last_findings_reviewed` list (`last_findings_cover_these_bytes: false`). Condition 3 is not a bind condition on these bytes.

---

# Considered and not filed

- **CRITIC 19 item 1 as if unanswered.** The demanded MD `:306` eleven-count and ratchet tenth/eleventh rows are on these hashes. Not re-filed.
- **CRITIC 19 item 2 as if unanswered.** The demanded MD `:203` WATCHED-landing strike is on these hashes. Not re-filed.
- **JSON `:54` still contains the tokens `nine-count leftover` / `WATCHED-02-outside leftover`.** That field records what ANSWER 19 SUSTAINED on the prior hashes. Filing the successful naming as a live leftover on these bytes would pad.
- **JSON `amendment` still contains `WATCHED leftover struck`.** Same class: it records the strike. Not filed.
- **MD `:203` still says "This turn did not edit `critic.py`."** True of ANSWER 19. CRITIC 19's leftover was the "outside `WATCHED`" / still-owed clauses after Systems had already edited `critic.py`. Those clauses are gone. Re-filing a now-true Operator-turn sentence as the Systems falsehood would pad.
- **`WATCHED.lab_proposed` still pointing at `_01`.** True of that id. Not a defect. The leftover was the "outside `WATCHED`" sentences.
- **Last_findings fields on the bar still cite 2026-09-08 hashes (`5F2AA5F5…` / `2611C255…` / `CD25DD72…`) and `last_findings_cover_these_bytes: false`, while live findings at 09:52:28 already review these bar hashes.** Disclosed-and-named, not UPHELD. JSON `:79` says a later clerical findings file is a separate artifact and this face does not pre-claim the post-amend hashes. The face does not claim those 2026-09-08 hashes cover these bytes. Clerical `passed: true` is not this attack.
- **MD `:16` / `:238` "condition 2 waits on covering these bytes."** Same restatement. Not a claim that the 09:52 findings file is missing. Not filed.
- **Condition 1 `met: false` / `binding: false`.** Correct until Operator records this attack. Not defects.
- **CRITIC 17 MD `:238` "condition 3 is unmet".** Grep is 0. Bind stays two. Closed as to CRITIC 18. Not re-filed.
- **CRITIC 16 / ANSWER 15 leftover half-pass.** Still named on MD `:324` / JSON `:287` as a citation of the machine, not of ANSWER 14 hashes. Closed as to those hashes. Not re-filed.
- **`snapshot_absent` is `state: PASS` and does not block `passed: true`.** Disclosed on `:47` / JSON `:288–290`. Closed as to CRITIC 14 item 1. Not re-filed.
- **Fee pin labeled as gym HTTP 200 / placeholder hash / `unpinned` leftover.** Not on these hashes. Pin is `founder_browser_bytes`. Not filed.
- **α-key still comparing `alpha_first_look` to current α_k.** Struck in `4a58a2e`. Not re-filed.
- **Half-spread treated as a fee adjustment.** The face forbids it. Not filed.
- **`consult_enabled: true` / `binding: true`.** Both false as found. Not filed.
- **AND-skip / in-memory consult tag / flag-write / missing δ.** ANSWER 12 face remains. Not re-filed.
- **`favorite_odds=2` / clause-(2) leftover ordinals / keyword greens / δ-check / vacuous greens.** Prior critics; already answered or disclosed. Not re-filed.
- **Honer catalog/rules starvation (`86e0cce`).** Recorded, not attacked.
- **X2 lived honoring unproven / `currently_reachable` false.** Already answered. No new verb. I did not flip reachable.
- **MD `:36` `WATCHED` does not include the honer snapshot.** Different artifact from PROPOSED 02. CRITIC 19 considered the unpaid probe / `series_fee` / `honer_consult` gap and did not file it as new residue. ANSWER 19 did not claim to watch the snapshot. Not re-filed.
- **Eleventh check `skipped: true` on a scratch-tree path.** Named on JSON `:399`. Clerical, not this attack.
- **The historical 429 still sitting on `fee_hurdle`.** Disclosed (`schedule_fetch_status` 429; gym last check 2026-09-09T17:01:17). Drift, not the pin clock. Not a second 429 finding.
- **Scoring, eligible counts, opening the tape.** Forbidden this Job.
- **Enabling consult, binding, arming, lifting HOLD, reviving `R-SKIP-COINFLIP`, probing the fee PDF, editing the bar.** Forbidden this Job.

---

**Closing.** I proposed no rule, scored no rule, ADMITted nothing, PARKed nothing, and did not Soften, Harden or Kill anything. I did not set `binding: true`, did not pin a fee-schedule hash, and did not write a placeholder for one. I did not enable consult. I opened no window outcome file. I did not fetch the PDF. I did not edit the bar, the registry, the compositor, or `critic.py`. Honer catalog/rules hashes remain unreviewed as honer. Trading is **NOT ARMED**.

Zero objections, UPHELD none. Condition 1 stays unmet for these bytes until Operator records this attack in a separate turn. Binding stays `false` as I found it. Condition 2 is not met on the face's 2026-09-08 list. Condition 3 is not a bind condition on these bytes.

Handoff → `chief-of-staff`.
