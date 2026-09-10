# Soften Critic — attack on Systems bind-candidate factory evidence-bar hashes (CRITIC 19)

**Role:** Soften Critic · **Date:** 2026-09-10 · **Lane:** `learning_lane_15m` · series `KXBTC15M` only
**Branch:** `cursor/honer-15m-sibling` at `472f321` (HEAD; CoS `last_cos` stamp). Factory bar last touched at `4a58a2e` (Systems bind-candidate). Git blobs of the two attacked bar files still equal `4a58a2e` (`fc0ad9b9…` / `a51f8078…`).

**Session separation.** This session did not draft the bar, did not write CRITIC 01–18, did not write ANSWER 01–17, did not land `4a58a2e` / `6e54e02` / `98f7eaa` / `1dea3c7` / `b9925db` / `c514015` / `1b21a70` / `86e0cce`, did not declare `R-SKIP-2TO1-FAVORITE`, and did not RUN-ONLY it. `PROTOCOL.md` forbids one turn both objecting and dismissing.

**This is an attack, not a verdict.** Operator answers each objection in a turn that is not this one. Nothing here is a Soften, an ADMIT, a RUN-ONLY, a park, a score, or a proposal. No rule was scored. `R-SKIP-COINFLIP` was not revived and its band was not retuned. Consult was not enabled. `binding` stays `false` exactly as I found it. Trading is **NOT ARMED**.

**Why this file exists.** Desk Job 2026-09-10 09:10 ET: attack the Systems bind-candidate factory evidence-bar bytes (`D25D0227…` / `4D9E86C2…`). Written objections only. Do not probe the fee PDF. CRITIC 18 closed ANSWER 17 hashes (`D9FDA991…` / `F7E8F681…`); those are not these bytes.

Those desk hashes **match** the factory bar files on this checkout via the same newline-normalised `critic.artifact_digest` (imported; pydantic is installed). Condition 1 is correctly `met: false` until Operator records this attack. This file attacks **these** bytes.

---

## Artifacts attacked, by SHA-256

Computed independently via newline-normalised `read_text` → UTF-8 digest `critic.artifact_digest` (imported from `golf_offshoot.learning_lane_15m.critic`). This Windows checkout has CRLF: byte hash ≠ normalised hash on the text files below. Binding condition 2 and the desk Job use the normalised digest. Live clerical findings (`ran_at` 2026-09-10T09:15:25−04:00, `passed: true`) already review every current `WATCHED` hash; `unreviewed()` is empty. That clerical PASS is not this attack.

| File | SHA-256 (normalised) | Live findings hash | CRITIC 18 attacked | Unreviewed? |
|---|---|---|---|---|
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR.md` | `D25D0227136206EC08846147470E3DA4AEA58CFE0B25B5A0B51BB9B7284FEEB2` | `D25D0227…` | `D9FDA991…` | **N** — live findings cover these bytes. The bar's own `last_findings_reviewed` still cites `5F2AA5F5…` (2026-09-08); that snapshot is named on the face, not a second findings file |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR.json` | `4D9E86C2C45362B8AF5FBF040F2DA5C5BA39F2EFA879C0F82D04CFDB946B74D6` | `4D9E86C2…` | `F7E8F681…` | **N** — same. Bar `last_findings_reviewed` still cites `2611C255…` |
| `golf-offshoot/docs/LEARNING_LANE_15M_RULES.json` | `BBD87E52EE6FC1E5F797C676EA6038F4C77404DDE7F29E21128BD75BF4B802D0` | `BBD87E52…` | same digest | **N** |
| `docs/agents/DESK.md` `## Honesty checklist` | `09B9A950051F5A907DD58723A5F7312457E15BA4C829A1EB1F2A4DAE73DED41B` | `09B9A950…` | `1EB03BCC…` at CRITIC 18 | **N** — CoS 09:10 restamp. This fire's Status/thread/Handoff writes do not touch the slice |
| `golf-offshoot/docs/LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md` | `83D4463B4BB55D327485E3874A4BF3DAA54727D7ED37F56C124C6E8913DAF0B4` | `83D4463B…` | same | **N** — still the watched `lab_proposed` path |
| `golf-offshoot/docs/LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_02.md` | `1071B9F7402EA0807147F64731456B80030310ED9FB2F6FF5ECD3009CC303119` | `1071B9F7…` | cited, not `WATCHED` at CRITIC 18 | **N** — now `WATCHED.lab_proposed_02` |
| `golf-offshoot/docs/LEARNING_LANE_15M_LAB_PROPOSED_02.md` | `460F59A369241E107F7FD48A22898F24D4456338618A7927D73D7AEBDC0368E2` | `460F59A3…` | cited, not `WATCHED` at CRITIC 18 | **N** — now `WATCHED.lab_lab_proposed_02` |

Honesty slice hash after the Status write equals the committed 09:10 slice (`09B9A950…`).

**Cited by the bind-candidate face and not in `WATCHED`:**

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
| `golf-offshoot/docs/LEARNING_LANE_15M_CRITIC_FINDINGS.json` | `503FD6CCCD33046A3DD751B067262F06B8B2C76EDF7C7F45349AFDD11F824D50` |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR_CRITIC_18.md` | `ADE8831C9AB38984BA9720EC7CD34B013F0DA80B586082BCC731A7A71B83933D` |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR_OPERATOR_ANSWER_17.md` | `A69CFF96C05129F584CD7679F337F379E0071580761DB68709435297B4D6D5A1` |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR_CRITIC_17.md` | `C90C16EC1357CFF4EC46E7DB37785A3308423CA4EA9B3A71A541B99949F57E9E` |
| `golf-offshoot/docs/LEARNING_LANE_15M_FEE_SCHEDULE_PROBE.json` | `5DD35C25BADDF941803558D4D7DF871D4BA5CE5620588CE895DDFC7D0CCCC36C` |

Local PDF digest equals JSON `schedule_sha256`. I did not GET `https://kalshi.com/docs/kalshi-fee-schedule.pdf`.

**Honer catalog/rules starvation hashes — remain after this attack. Not attacked.** Catalog/rules digests are unchanged since `86e0cce`. Honer evidence-bar files are unchanged since `98f7eaa`; recorded, not attacked.

| File | SHA-256 (normalised) |
|---|---|
| `golf-offshoot/docs/HONER_15M_CATALOG.json` | `CFAF1E50975B230B17103C16170C282F123FB842E349AE90990AC51C2AD220D6` |
| `golf-offshoot/docs/HONER_15M_RULES.json` | `E6EF7CEFCF300B14A1B5FC3F66F79F136121317E07728912AE568367F30C7C3E` |
| `golf-offshoot/docs/HONER_15M_EVIDENCE_BAR.md` | `CED34B6C3AE34AD426B849F4A2FF782564B18665CFF489FA8B49429BFA28F170` |
| `golf-offshoot/docs/HONER_15M_EVIDENCE_BAR.json` | `C35AF511DB856350BBBE65477F8F48142299ABA2B3E662E6961B6DA184E1381F` |

I did not call `artifact_root_15m()` / `latest_dir_15m()`. Glob for `honer_consult.json` under `golf-offshoot` returned 0. I did not open `latest/journal.json`. Live clerical `series_fee_regime_matches` evidence has `snapshot_absent: false`; I did not open that snapshot.

Hashes recomputed at the end of the attack and unchanged: the text I attacked did not move under me.

---

## Posture

I did **not** open a window outcome file — no `paper/*.json`, no `settlements/*.json`, no `latest/journal.json`, no `rule_decisions.json`. I did not call `score_rule`, `write_critic_findings`, `gym_fee_tick`, `latest_dir_15m`, or `mark_roles_served`. I did not run the digest generator. I did not start or stop a hub. I did not fetch `https://kalshi.com/docs/kalshi-fee-schedule.pdf`. I hashed the committed local PDF only.

I imported `golf_offshoot` on this Windows tree (pydantic is installed) for `artifact_digest` / `WATCHED` / `CHECKS` / `unreviewed`. I did not treat the clerical `passed: true` as a written attack.

I did not edit the bar, the JSON, the registry, `consult_honer.py`, `critic.py`, `evidence_bar.py`, `DESK.md` (except the worker Status/thread/Handoff this fire is required to write), or `AGENT_LEAVE_OFF.md`. I did not set `binding: true`. I did not pin a fee-schedule hash. I did not write a placeholder. I did not set `consult_enabled`.

---

# The one-sentence version

**`4a58a2e` landed eleven method checks and `WATCHED` PROPOSED 02 — MD `:47`, JSON `ratchet_guards`, and `critic.py` `CHECKS` / `WATCHED` all show that landing — and left MD `:306` still saying the suite has nine and MD `:203` still saying PROPOSED 02 notes are outside `WATCHED`.**

---

## What I accept as closed on the prior text (not re-filed)

CRITIC 18 was a completed zero-UPHELD attack on the ANSWER 17 hashes. Those are not these bytes. I am not re-opening CRITIC 17's condition-3 leftover as if unanswered. I hunted residue that would be **new on these bind-candidate bytes**.

| Bind-candidate change | What I verified on these hashes | Closed as to the prior sentence? |
|---|---|---|
| Founder browser fee pin `founder_browser_bytes` | JSON `schedule_sha256` = `c326a69f596a11e8f8be2620402d39a8d4823920c21cc97c93a114d862699601` = local PDF bytes (281129). `schedule_pin_source=founder_browser_bytes`. `standing_named_fail` is `[]`. `standing_named_fail_struck` names the pin. MD `:16` / `:50` / `:159` / `:238` say not a gym HTTP 200. `schedule_fetch_status` remains 429 as drift. Grep of both bar files for `unpinned` is empty. | **Yes, as to the pin and the not-gym-200 label.** Not a placeholder. I did not fetch. |
| α-key | `4a58a2e` changed `check_delta_above_detection_floor` from `("alpha_first_look", alpha, …)` to `alpha_first_term` plus `("next_look_alpha", alpha, …)`. Live findings `disagreements: []`. MD `:16` and JSON `:72` / `:407` name that split. | **Yes, as to the comparison.** The prior leftover (first-look key vs current α_k) is not on this machine. |
| Half-spread profile | Named artifact n=624 mean 0.00385. MD `:169–171` / Hard NO `:337` / JSON `:297–304` say it is **not** a fee adjustment; `fee_adjust` still omits it. Tenth check exists in `CHECKS`. | **Yes, as to "not a fee adjustment" and the named n.** Residue of the ratchet *count* is objection 1. |
| Eleven method checks | MD `:47` says **eleven**; tenth `half_spread_profile_recorded`; eleventh `hub_autostart_registered`. JSON `:72` names tenth and eleventh. `critic.py` `CHECKS` has **11** members. JSON `ratchet_guards` has `half_spread_tenth` and `hub_autostart_eleventh`. | **Yes, as to `:47` / JSON / `CHECKS`.** Residue of MD `:306` still counting nine is objection 1. |
| `WATCHED` PROPOSED 02 | `4a58a2e` added `Watched("lab_proposed_02", …)` and `Watched("lab_lab_proposed_02", …)`. `WATCHED` length **7**. JSON `:8` amendment names it. JSON `:405` `owed_to_systems` says `WATCHED.lab_proposed_02 LANDED`. Live findings review both notes. | **Yes, as to the landing in `critic.py` / JSON owed.** Residue of MD `:203` still saying they are outside is objection 2. |
| CRITIC 17 MD `:238` "condition 3 is unmet" | Grep of the markdown for `condition 3 is unmet` is **0**. Grep for `condition 3` is **0**. JSON `binding_conditions` has **two** rows. JSON `:48` `binding_rule` has no `(3)`. JSON `:124` `unreachable_because` has no `condition 3`. | **Yes.** CRITIC 17's "what would prove me wrong" remains true of these hashes. Not re-filed. |
| ANSWER 15 leftover half-pass citation | Still named on MD `:324` / JSON `:281–288` / `:390` as a citation of the machine, not of ANSWER 14 hashes. CRITIC 16 closed that as to those hashes. | **Yes.** Not re-filed. |

Registry digest is unchanged (`BBD87E52…`); `trials_to_date` is 1; one log row, kind `declaration`; `R-SKIP-2TO1-FAVORITE.execution` true; `R-SKIP-COINFLIP.execution` false; `verifiably_preregistered` false on both selection rows. `binding` false. `consult_enabled` false. I did not enable it.

---

## Objections

## Objection 1 — MD `:306` still says the suite has nine method checks after these hashes added the tenth and eleventh

### **UPHELD.**

`4a58a2e` added `check_half_spread_profile` and `check_hub_autostart_registered` to `CHECKS`. These hashes have **eleven** method checks. MD `:47`:

> The method suite has **eleven** checks (`honesty_stamp_is_fresh` is a desk check in `DESK_CHECKS` and does not set `passed`). The tenth is `half_spread_profile_recorded` … The eleventh is `hub_autostart_registered` …

JSON `:72` names tenth and eleventh. JSON `ratchet_guards` has `half_spread_tenth` and `hub_autostart_eleventh` (`:392–393`). `critic.py:1070–1082` `CHECKS` has eleven members.

The same hashes, `:306` — the ratchet paragraph that exists because Y2 was "zero new `CHECKS` members":

> The suite now has **nine** method checks (`series_fee_regime_matches` is the eighth; `bind_has_no_founder_read_once` is the ninth).

The MD ratchet table (`:308–325`) still ends at "gym-pin eighth" and "Founder 2026-09-09". It has no tenth or eleventh row. X1 names the landed profile and says it is not a fee adjustment; that row does not count the suite.

This is the same leftover class CRITIC 14 filed when the gym-pin face added the eighth check and left the ratchet paragraph on seven. ANSWER 14 put eight on that paragraph. Later hashes put nine there, which was then true. These hashes added two checks and left the paragraph on nine.

I am not asking for a new mechanical check. I am asking the face that just added the tenth and eleventh not to also say there are nine. JSON already names the new rows; that does not strike the MD count.

**Concrete change demanded.** Make MD `:306` say eleven (tenth `half_spread_profile_recorded`, eleventh `hub_autostart_registered`), and add MD ratchet rows that match JSON `half_spread_tenth` / `hub_autostart_eleventh` — **or** state that `:306` still says nine after these hashes added those checks. Do not score. Do not bind. Do not treat clerical PASS as the strike.

**What would prove me wrong.** Show MD `:306` does not say the suite has nine method checks, or show `critic.py` `CHECKS` has nine members. JSON already naming tenth and eleventh does not prove the MD count leftover wrong. The hashes I attacked say nine at `:306` and eleven at `:47` / in `CHECKS`.

---

## Objection 2 — MD `:203` still says PROPOSED 02 notes are outside `WATCHED` after these hashes landed them

### **UPHELD.**

`4a58a2e` added two `WATCHED` rows. `critic.py:71–79` is seven items; `lab_proposed_02` and `lab_lab_proposed_02` are in the tuple. JSON `:8` amendment lists "WATCHED PROPOSED 02". JSON `:405`:

> `WATCHED.lab_proposed_02 LANDED 2026-09-10: OPERATOR_NOTE_PROPOSED_02.md and LAB_PROPOSED_02.md`

Live findings review both note hashes. `unreviewed()` is empty.

The same hashes, MD `:203`:

> `WATCHED.lab_proposed` in `critic.py` is still pinned to `LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md`. PROPOSED 02 notes are **outside** `WATCHED`. Watching them is owed to Systems. This turn did not edit `critic.py`.

The first sentence is still true of id `lab_proposed` (it still points at `_01`). The next three are false of these bytes: PROPOSED 02 notes are inside `WATCHED`; watching them is not still owed; `4a58a2e` edited `critic.py` (+127 / −1, including those two `Watched` lines).

CRITIC 03 / later critics disclosed the unpaid gap while it was unpaid. I am not re-filing "still frozen on `_01`" as if the landing never happened. I am filing the leftover unpaid sentence after the landing, the same way CRITIC 17 filed MD `:238` after JSON dropped condition 3.

**Concrete change demanded.** State that MD `:203` still says PROPOSED 02 notes are outside `WATCHED` after these hashes landed `lab_proposed_02` / `lab_lab_proposed_02` — `WATCHED` length 7, JSON owed says LANDED, amendment header names the watch — **or** strike those three leftover clauses. Do not unwatch the notes. Do not bind. Do not edit `critic.py` in this answer if the strike is a face-statement.

**What would prove me wrong.** Show MD `:203` does not say PROPOSED 02 notes are outside `WATCHED`, or show `critic.py` `WATCHED` lacks `lab_proposed_02` / `lab_lab_proposed_02`. JSON owed landing does not prove the MD leftover wrong. The hashes I attacked have the leftover on the markdown.

---

# Considered and not filed

- **CRITIC 17 item 1 as if unanswered.** The demanded MD `:238` strike remains on these hashes. Not re-filed.
- **CRITIC 14 item 3 as if unanswered on seven-vs-eight.** That demanded strike is not these bytes' leftover. The new leftover is nine-vs-eleven after *this* amend. Filed as objection 1, not as CRITIC 14 unanswered.
- **`WATCHED.lab_proposed` still pointing at `_01`.** True of that id. Not a defect. The leftover is the "outside `WATCHED`" sentences. Objection 2.
- **Last_findings fields on the bar still cite 2026-09-08 hashes (`5F2AA5F5…` / `2611C255…` / `CD25DD72…`) and `last_findings_cover_these_bytes: false`, while live findings at 09:15:25 already review these bar hashes.** Disclosed-and-named, not UPHELD. JSON `:72` says a later clerical findings file is a separate artifact and this face does not pre-claim those hashes. JSON `:73` says Operator bind restates `last_findings` after critic-invariants covers these bytes. `standing_named_fail_struck` already says the 2026-09-08 `last_findings_reviewed` list describes other bytes. Filing that snapshot as a pretence that findings do not exist would pad the restatement note. Clerical `passed: true` is not this attack. Condition 2 `met: false` stays Operator's restatement, not a face lie I answer.
- **MD `:16` / `:238` "condition 2 waits on covering these bytes."** Same restatement. Not a claim that the 09:15 findings file is missing. Not filed.
- **Condition 1 `met: false` / `binding: false`.** Correct until Operator records this attack. Not defects.
- **Fee pin labeled as gym HTTP 200 / placeholder hash / `unpinned` leftover.** Not on these hashes. Pin is `founder_browser_bytes`. Not filed.
- **α-key still comparing `alpha_first_look` to current α_k.** Struck in `4a58a2e`. Not re-filed.
- **Half-spread treated as a fee adjustment.** The face forbids it. Not filed.
- **`consult_enabled: true` / `binding: true`.** Both false as found. Not filed.
- **CRITIC 16 / ANSWER 15 leftover half-pass.** Still named on the face as a machine leftover. Closed as to those hashes. Not re-filed.
- **`snapshot_absent` is `state: PASS` and does not block `passed: true`.** Disclosed on `:47` / JSON `:281–284`. Closed as to CRITIC 14 item 1. Not re-filed.
- **Labeled `latest/` is the fallback shape.** Disclosed. ANSWER 14 named both resolved paths. Not a second path finding.
- **The historical 429 still sitting on `fee_hurdle`.** Disclosed (`schedule_fetch_status` 429; gym last check 2026-09-09T17:01:17). Drift, not the pin clock. Not a second 429 finding.
- **`schedule_park_class: external` while `schedule_fetch_is_external: false`.** Neighbor of the landed pin. The pin and the 429-as-drift are named. Not filed.
- **AND-skip / in-memory consult tag / flag-write / missing δ.** ANSWER 12 face remains. Not re-filed.
- **`favorite_odds=2` / clause-(2) leftover ordinals / keyword greens / δ-check / vacuous greens.** Prior critics; already answered or disclosed. Not re-filed.
- **Honer catalog/rules starvation (`86e0cce`).** Recorded, not attacked.
- **X2 lived honoring unproven / `currently_reachable` false.** Already answered. No new verb. I did not flip reachable.
- **Eleventh check `skipped: true` on the live findings scratch-tree path.** Named on JSON `:393`. Clerical, not this attack.
- **`WATCHED` still omitting the fee probe / `series_fee` / `honer_consult` snapshot.** Not claimed as landed on these hashes. Prior unpaid disclosure. Not new residue.
- **Scoring, eligible counts, opening the tape.** Forbidden this Job.
- **Enabling consult, binding, arming, lifting HOLD, reviving `R-SKIP-COINFLIP`, probing the fee PDF, editing the bar.** Forbidden this Job.

---

**Closing.** I proposed no rule, scored no rule, ADMITted nothing, PARKed nothing, and did not Soften, Harden or Kill anything. I did not set `binding: true`, did not pin a fee-schedule hash, and did not write a placeholder for one. I did not enable consult. I opened no window outcome file. I did not fetch the PDF. I did not edit the bar, the registry, the compositor, or `critic.py`. Honer catalog/rules hashes remain unreviewed as honer. Trading is **NOT ARMED**.

Two objections, both UPHELD. Condition 1 stays unmet for these bytes until Operator records this attack in a separate turn. Binding stays `false` as I found it. Condition 2 is Operator's restatement of last_findings; I did not treat clerical PASS as bind. Condition 3 is not a bind condition on these bytes.

Operator answers these. Handoff → `operator`.
