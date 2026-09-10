# Soften Critic — attack on Systems bind-candidate factory evidence-bar hashes (CRITIC 19)

**Role:** Soften Critic · **Date:** 2026-09-10 · **Lane:** `learning_lane_15m` · series `KXBTC15M` only
**Branch:** `cursor/honer-15m-sibling` at `472f321` (CoS last_cos stamp). Factory bar last touched at `4a58a2e` (Systems bind-candidate). Git blobs of the two attacked bar files still equal `4a58a2e` (`fc0ad9b9…` / `a51f8078…`).

**Session separation.** This session did not draft the bar, did not write CRITIC 01–18, did not write ANSWER 01–17, did not land `4a58a2e` / `6e54e02` / `98f7eaa` / `1dea3c7` / `b9925db` / `c514015` / `1b21a70` / `86e0cce`, did not declare `R-SKIP-2TO1-FAVORITE`, and did not RUN-ONLY it. `PROTOCOL.md` forbids one turn both objecting and dismissing.

**This is an attack, not a verdict.** Operator answers each objection in a turn that is not this one. Nothing here is a Soften, an ADMIT, a RUN-ONLY, a park, a score, or a proposal. No rule was scored. `R-SKIP-COINFLIP` was not revived and its band was not retuned. Consult was not enabled. `binding` stays `false` exactly as I found it. Trading is **NOT ARMED**.

**Why this file exists.** Desk Job 2026-09-10 09:10 ET: attack the Systems bind-candidate factory evidence-bar bytes (`D25D0227…` / `4D9E86C2…`). CRITIC 18 closed ANSWER 17 hashes `D9FDA991…` / `F7E8F681…` — those are not these bytes. Written objections only. File CRITIC 19. Do not edit the bar, score, bind, enable consult, or GET the PDF as gym.

Those desk prefixes **match** the factory bar files on this checkout. Condition 1 is correctly `met: false` for that reason. This file attacks the **new** bytes.

---

## Artifacts attacked, by SHA-256

Computed independently via the same newline-normalised `read_text` → UTF-8 digest `critic.artifact_digest` uses (copied, not imported: this tree's package import pulls `pydantic`, which is not installed in this fire). Byte hash equals the normalised hash on every file below (0 CRLF pairs), except the honesty section, which is a slice of `DESK.md`, and the PDF, which is raw bytes (`schedule_digest_kind` says no newline normalisation).

| File | SHA-256 (bytes = normalised) | Last findings hash | CRITIC 18 attacked | Unreviewed? |
|---|---|---|---|---|
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR.md` | `D25D0227136206EC08846147470E3DA4AEA58CFE0B25B5A0B51BB9B7284FEEB2` | `D25D0227…` (findings `503FD6CC…`, `ran_at` 2026-09-10T09:15:25−04:00, same commit as the bar) | `D9FDA991…` | clerical Y-covered / written **Y** — Systems bind-candidate. Clerical findings are not this attack |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR.json` | `4D9E86C2C45362B8AF5FBF040F2DA5C5BA39F2EFA879C0F82D04CFDB946B74D6` | `4D9E86C2…` | `F7E8F681…` | same |
| `golf-offshoot/docs/LEARNING_LANE_15M_RULES.json` | `BBD87E52EE6FC1E5F797C676EA6038F4C77404DDE7F29E21128BD75BF4B802D0` | `BBD87E52…` | same digest | clerical covered; unchanged since `3c89a7f` |
| `docs/agents/DESK.md` `## Honesty checklist` | `09B9A950051F5A907DD58723A5F7312457E15BA4C829A1EB1F2A4DAE73DED41B` | `09B9A950…` | `1EB03BCC…` | clerical covered — CoS 09:10 restamp names this assign |
| `golf-offshoot/docs/LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md` | `83D4463B4BB55D327485E3874A4BF3DAA54727D7ED37F56C124C6E8913DAF0B4` | `83D4463B…` | same | N — still the watched `lab_proposed` path |
| `golf-offshoot/docs/LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_02.md` | `1071B9F7402EA0807147F64731456B80030310ED9FB2F6FF5ECD3009CC303119` | `1071B9F7…` | not watched at CRITIC 18 | clerical covered — `WATCHED` now includes this path |
| `golf-offshoot/docs/LEARNING_LANE_15M_LAB_PROPOSED_02.md` | `460F59A369241E107F7FD48A22898F24D4456338618A7927D73D7AEBDC0368E2` | `460F59A3…` | not watched at CRITIC 18 | clerical covered |
| `golf-offshoot/docs/kalshi-fee-schedule.pdf` | `C326A69F596A11E8F8BE2620402D39A8D4823920C21CC97C93A114D862699601` | — | absent | not `WATCHED`; 281129 bytes; raw SHA-256 equals the face pin. I hashed the committed file. I did not GET the URL |
| `golf-offshoot/docs/LEARNING_LANE_15M_HALF_SPREAD_PROFILE.json` | `45BF3C7C1EA71B87111E01756A2FA409858B5BF80B6BDBD93EA0B21EFFB09A49` | — | absent | not `WATCHED`; n=624 mean 0.00385 matches the face |
| `golf-offshoot/docs/LEARNING_LANE_15M_FEE_SCHEDULE_PROBE.json` | `5DD35C25BADDF941803558D4D7DF871D4BA5CE5620588CE895DDFC7D0CCCC36C` | — | same | not `WATCHED`; cited by the restated 17:01:17 gym-GET row |

Honesty slice is the committed `472f321` section (this fire's Status/thread writes do not touch it). Hash of that slice after the Status write equals the committed slice and the findings `honesty_stamp` row.

**Cited by the bind-candidate face and not in `WATCHED`:**

| File | SHA-256 |
|---|---|
| `golf-offshoot/src/golf_offshoot/learning_lane_15m/critic.py` | `C87B503A1C5388524F58BDEFF60291638F44F6EFAE31D34FC7FC9AF3783E4775` |
| `golf-offshoot/src/golf_offshoot/learning_lane_15m/evidence_bar.py` | `3F1D51E8EE0B87A1E0598305B9D5AF1D0D91BCD1AF5970546FA24D6CDAA8FEF3` |
| `golf-offshoot/src/golf_offshoot/learning_lane_15m/rules.py` | `9090F499D4AB3E701766BD13CF4F7CBF1C14F6C18C580FCF9C2552470B11FCB7` |
| `golf-offshoot/src/golf_offshoot/learning_lane_15m/spread_profile.py` | `E281866EF2B9D9EF897D228792A33BC1A99B768C04098728C138DA755D2BF6BD` |
| `golf-offshoot/src/golf_offshoot/learning_lane_15m/consult_honer.py` | `5C4744DF1AF3641B805D96061FF16B5D256FAFC812C70BF3B95AB0DC0C025DBD` |
| `golf-offshoot/src/golf_offshoot/learning_lane_15m/paper.py` | `FADA063E42EA7C1126BD3D839F17124D3AA34DB75FE7D6936FD38F8198BB26EC` |
| `golf-offshoot/src/golf_offshoot/learning_lane_15m/watch.py` | `187863392939E76F71280738F52C4EE233381C2043FAC89FA3134483A0A961C3` |
| `golf-offshoot/src/golf_offshoot/learning_lane_15m/notify.py` | `1015F00798ADE8FC89B97F56A84C670C290A4DFBCE60C38CA980619C46EC0D3A` |
| `golf-offshoot/src/golf_offshoot/learning_lane_15m/paths.py` | `C543D98DB589C9822DA73F712C03A2EC22F0E3BDCFF6F5EA5630B4E225CD476C` |
| `golf-offshoot/docs/HONER_15M_PROMOTION.md` | `7FD9E8B24F6E8467E5735DB7690B39967500EFE23C4C79861A5E56775DCE5E40` |
| `golf-offshoot/docs/LEARNING_LANE_15M_CRITIC_FINDINGS.json` | `503FD6CCCD33046A3DD751B067262F06B8B2C76EDF7C7F45349AFDD11F824D50` |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR_CRITIC_18.md` | `ADE8831C9AB38984BA9720EC7CD34B013F0DA80B586082BCC731A7A71B83933D` |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR_OPERATOR_ANSWER_17.md` | `A69CFF96C05129F584CD7679F337F379E0071580761DB68709435297B4D6D5A1` |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR_CRITIC_17.md` | `C90C16EC1357CFF4EC46E7DB37785A3308423CA4EA9B3A71A541B99949F57E9E` |

**Honer catalog/rules starvation hashes — remain after this attack. Not attacked.** Catalog/rules digests are unchanged since `86e0cce`. Honer evidence-bar files are unchanged since `98f7eaa`; recorded, not attacked.

| File | SHA-256 |
|---|---|
| `golf-offshoot/docs/HONER_15M_CATALOG.json` | `CFAF1E50975B230B17103C16170C282F123FB842E349AE90990AC51C2AD220D6` |
| `golf-offshoot/docs/HONER_15M_RULES.json` | `E6EF7CEFCF300B14A1B5FC3F66F79F136121317E07728912AE568367F30C7C3E` |
| `golf-offshoot/docs/HONER_15M_EVIDENCE_BAR.md` | `CED34B6C3AE34AD426B849F4A2FF782564B18665CFF489FA8B49429BFA28F170` |
| `golf-offshoot/docs/HONER_15M_EVIDENCE_BAR.json` | `C35AF511DB856350BBBE65477F8F48142299ABA2B3E662E6961B6DA184E1381F` |

I did not call `artifact_root_15m()` / `latest_dir_15m()` and did not create that directory.

Hashes recomputed at the end of the attack and unchanged: the text I attacked did not move under me.

---

## Posture

I did **not** open a window outcome file — no `paper/*.json`, no `settlements/*.json`, no `latest/journal.json`, no `rule_decisions.json`. I did not call `score_rule`, `write_critic_findings`, `gym_fee_tick`, `latest_dir_15m`, or `mark_roles_served`. I did not run the digest generator. I did not start or stop a hub. I did not fetch `https://kalshi.com/docs/kalshi-fee-schedule.pdf`. `watch.json` is not on this tree.

The package import pulls `pydantic`, which is not installed. Numbers below come from the bar, `critic.py` as text, the committed PDF and half-spread profile, the findings file as text, and the commit record.

I did not edit the bar, the JSON, the registry, `consult_honer.py`, `critic.py`, `evidence_bar.py`, `DESK.md` (except the worker Status/thread this fire is required to write), or `AGENT_LEAVE_OFF.md` until closeout. I did not set `binding: true`. I did not pin a fee-schedule hash. I did not write a placeholder. I did not set `consult_enabled`.

---

# The one-sentence version

**`4a58a2e` landed eleven method checks and WATCHED PROPOSED 02 — MD `:47`, JSON `ratchet_guards` tenth/eleventh, `critic.py` `CHECKS` (11) and `WATCHED` (`lab_proposed_02` / `lab_lab_proposed_02`) — and left MD `:306` still saying the suite has nine method checks and MD `:203` still saying PROPOSED 02 notes are outside WATCHED and this turn did not edit `critic.py`.**

---

## What I accept as closed on the prior text (not re-filed)

CRITIC 18's zero UPHELD closed ANSWER 17 hashes. Those are not these bytes. I am not re-opening CRITIC 17's demanded MD `:238` strike as if unanswered. I hunted residue that would be **new on these Systems bytes**.

| Systems bind-candidate change | What I verified on these hashes | Closed as to the prior sentence? |
|---|---|---|
| Fee pin `founder_browser_bytes` | JSON `:266` `schedule_sha256` = `c326a69f596a11e8f8be2620402d39a8d4823920c21cc97c93a114d862699601`. Committed `kalshi-fee-schedule.pdf` is 281129 bytes and raw SHA-256 equals that digest. Grep of both bar files for `unpinned` is **0**. `standing_named_fail` is `[]`. `schedule_pin_source` is `founder_browser_bytes`. Gym last GET remains 429 at 17:01:17. I did not GET the URL. | **Yes, as to the pin existing and matching the committed file.** The 429 is drift, named. Not a second 429 finding. |
| Half-spread profile n=624 mean 0.00385 | Named artifact exists. `n` 624; bucket ns sum to 624; `mean_half_spread` 0.00385; middle buckets 0.005; `0.00-0.10` ~0.0005. `half_spread_profile_recorded` is `CHECKS[9]`. `fee_adjust` still omits it, named. | **Yes, as to the named numbers matching the file.** Not a fee adjustment. |
| `check_delta_above_detection_floor` α-key | `critic.py:306–307` compares `alpha_first_look` to `0.05/(1*2)` and `next_look_alpha` to current `alpha_k`. JSON `alpha_first_look` 0.025 / `next_look_alpha` 0.008333. | **Yes, as to the comparison existing.** |
| Bind stays two conditions; no condition 3 | Grep of both files for `condition 3 is unmet` is **0**. Grep for `condition 3` is **0**. `binding_conditions` has two rows. `binding_rule` has no `(3)`. | **Yes.** CRITIC 17/18 closed. |
| Ninth check `bind_has_no_founder_read_once` | Still present. Needles unchanged. `founder_read_once` is not a bind id. | **Yes.** Not re-filed. |
| ANSWER 15 leftover half-pass citation | Still on MD `:324` / JSON `:281` / `:286–288` / ratchet `:390`. Closed as to those hashes. Still true of these hashes. | **Yes.** Not re-filed. |

Registry digest is unchanged (`BBD87E52…`); `trials_to_date` is 1; one log row, kind `declaration`; `R-SKIP-2TO1-FAVORITE.execution` true; `R-SKIP-COINFLIP.execution` false; `verifiably_preregistered` false on both selection rows. `binding` false. Consult off. I did not enable it.

---

## Objection 1 — MD `:306` still says the suite has nine method checks after these hashes added the tenth and eleventh

### **UPHELD.**

`4a58a2e` added `half_spread_profile_recorded` and `hub_autostart_registered`. These hashes have eleven `CHECKS` members. MD `:47` says so:

> The method suite has **eleven** checks (`honesty_stamp_is_fresh` is a desk check in `DESK_CHECKS` and does not set `passed`). The tenth is `half_spread_profile_recorded` … The eleventh is `hub_autostart_registered` …

`critic.py` `CHECKS` (`:1070–1082`) has **eleven** callables. The tenth is `check_half_spread_profile`. The eleventh is `check_hub_autostart_registered`. JSON `ratchet_guards` has `half_spread_tenth` and `hub_autostart_eleventh`. Same-commit findings list eleven method rows.

MD `:306` — the ratchet paragraph that claims to name how many checks guard the findings — still says:

> The suite now has **nine** method checks (`series_fee_regime_matches` is the eighth; `bind_has_no_founder_read_once` is the ninth).

Grep of the markdown for `nine method` is **1** (that line). Grep of the JSON for `nine method` is **0**. There is no nine-member suite on these hashes for that sentence to be true *of*.

This is the same leftover shape as CRITIC 17 item 1: one face updated (here `:47` / JSON tenth+eleventh / `CHECKS`) and the ratchet face still cites the deleted count. I am not asking to drop the tenth or eleventh. I am not asking to set `binding: true`. I am not asking to edit `critic.py`.

**Concrete change demanded.** State that MD `:306` still says "nine method checks" after these hashes added the tenth and eleventh — MD `:47` says eleven, `CHECKS` has eleven members, JSON `ratchet_guards` names `half_spread_tenth` and `hub_autostart_eleventh` — **or** strike that count so the ratchet face agrees. Do not bind. Do not fetch the PDF.

**What would prove me wrong.** Show MD `:306` does not contain `nine method checks`, or show `CHECKS` still has nine members, or show MD `:47` also says nine so the faces agree. The hashes I attacked have the leftover on the ratchet paragraph only.

---

## Objection 2 — MD `:203` still says PROPOSED 02 notes are outside `WATCHED` after these hashes landed them

### **UPHELD.**

`4a58a2e` added `WATCHED` rows for the PROPOSED 02 notes. The amendment header (MD `:5`) and JSON `:8` name "WATCHED PROPOSED 02". JSON `:405` `owed_to_systems` says `WATCHED.lab_proposed_02 LANDED 2026-09-10: OPERATOR_NOTE_PROPOSED_02.md and LAB_PROPOSED_02.md`. `critic.py:71–78` is seven watched artifacts; the new ids are `lab_proposed_02` (`PROPOSED_02_REL`) and `lab_lab_proposed_02` (`LAB_PROPOSED_02_REL`). Same-commit findings `reviewed` includes both paths (`1071B9F7…` / `460F59A3…`). The Systems commit touches `critic.py` (128 insertions in the `4a58a2e` stat).

MD `:203` — the pre-registration leftover that was true of the ANSWER 17 hashes — still says:

> `WATCHED.lab_proposed` in `critic.py` is still pinned to `LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md`. PROPOSED 02 notes are **outside** `WATCHED`. Watching them is owed to Systems. This turn did not edit `critic.py`.

Grep of the markdown for `outside` `WATCHED` is that line. The first sentence remains true as far as it goes: `lab_proposed` is still the `_01` path. The next two sentences are false of these hashes. `WATCHED` has three Lab rows, not one. This turn *is* the Systems turn that edited `critic.py`.

I am not asking to unwatch PROPOSED 02. I am not asking to set `binding: true`. I am not asking for a fourth watched path.

**Concrete change demanded.** State that MD `:203` still says PROPOSED 02 notes are outside `WATCHED` and that this turn did not edit `critic.py` after these hashes landed `lab_proposed_02` / `lab_lab_proposed_02` — JSON `:405` already says LANDED, `WATCHED` has those two ids — **or** strike those two sentences. Do not bind. Do not fetch the PDF.

**What would prove me wrong.** Show MD `:203` does not say PROPOSED 02 notes are outside `WATCHED` and does not say this turn did not edit `critic.py`, or show `critic.py` `WATCHED` has no `lab_proposed_02` / `lab_lab_proposed_02`, or show JSON `:405` does not say LANDED so the faces agree. The hashes I attacked have the leftover on the markdown only.

---

# Considered and not filed

- **CRITIC 17 item 1 / CRITIC 18 zero UPHELD as if unanswered.** The demanded MD `:238` strike is on these hashes. Not re-filed.
- **Fee pin as if still unpinned.** `schedule_sha256` is 64-hex and equals the committed PDF. Grep `unpinned` is 0. Not re-filed.
- **I hashed the committed PDF.** That is not a gym GET. The Job forbids GET-as-gym. The pin claim is true of the file on this tree.
- **`schedule_fetch_status: 429` sitting next to `schedule_checked_at` 09:01:32 (the pin time).** Disclosed: gym last GET is the separate `schedule_gym_last_*` 17:01:17 row; `schedule_fetch_note` names Founder browser bytes. Neighbor of a named 429 already declined.
- **`check_fee_schedule_hash_recorded` greens on any 64-hex plus a timestamp and does not open the PDF.** The named file matches. Demanding a Systems needle after the pin landed would pad.
- **Half-spread n=624 / mean 0.00385.** Matches the named file. `fee_adjust` still omits it, named. Not a fee adjustment.
- **`collect_from_paper_books` globs every `KXBTC15M-*.json` while calibration `:296` says post-declaration files were not opened for marks or pnl.** The profile names no window ids. I did not open paper files. n=624 can come from snapshots / quote_log. Not filed.
- **Same-commit findings (`503FD6CC…`, `ran_at` 09:15:25) review these exact bar hashes and say `passed: true`, while JSON `:74` `last_findings_cover_these_bytes` is false and `:75` still cites 2026-09-08.** The face also says it does not pre-claim a clerical findings file. Authoring-session clerical pass is not condition 2. The eleventh row in that file is `scratch-tree critic run`. Filing "update last_findings to the file you just wrote" would push a scratch-tree green toward bind. Not filed.
- **`hub_autostart_registered` PASSes when `root is not None` or `os.name != "nt"`.** Disclosed as scratch-tree / not-Windows skip. Neighbor of `snapshot_absent` already named. Not a second path finding.
- **CRITIC 16 / ANSWER 15 leftover half-pass.** Still named on the face. Closed as to those hashes. Not re-filed.
- **The machine detail still says `latest/series_fee.json`.** Disclosed on `:47` / JSON `:275–277`. ANSWER 14 named both resolved paths. Not a second path finding.
- **`load_series_fee_snapshot` on invalid JSON is `{}`.** Disclosed. Closed as to CRITIC 14 item 1.
- **`expected_fee_type` / `expected_fee_multiplier` default to quadratic / 1 when omitted** (`critic.py:790–795`). Live bytes have both keys. Neighbor of a fail-open already declined. Not filed.
- **AND-skip / in-memory consult tag / flag-write / missing δ.** ANSWER 12 face remains. Not re-filed.
- **`favorite_odds=2` / clause-(2) leftover ordinals / keyword greens / δ-check / vacuous greens.** Prior critics; already answered or disclosed. Not re-filed.
- **Honer catalog/rules starvation (`86e0cce`).** Recorded, not attacked.
- **X2 lived honoring unproven / `currently_reachable` false.** Already answered. No new verb.
- **JSON `binding_conditions[0]` still points at CRITIC 17 / ANSWER 17 / drop-read-once hashes.** The detail names those as not the bind-candidate and says condition 1 is unmet on these bytes. Bookkeeping of the last answered pair, not a face lie. Not filed.
- **Scoring, eligible counts, opening the tape.** Forbidden this Job.
- **Enabling consult, binding, arming, lifting HOLD, reviving `R-SKIP-COINFLIP`, probing the fee PDF.** Forbidden this Job.

---

**Closing.** I proposed no rule, scored no rule, ADMITted nothing, PARKed nothing, and did not Soften, Harden or Kill anything. I did not set `binding: true`, did not pin a fee-schedule hash, and did not write a placeholder for one. I did not enable consult. I opened no window outcome file. I did not fetch the PDF. I did not edit the bar, the registry, the compositor, or `critic.py`. Honer catalog/rules hashes remain unreviewed as a written attack. Trading is **NOT ARMED**.

Two objections, both UPHELD. Condition 1 stays unmet for these bytes until Operator records this attack in a separate turn. Binding stays `false` as I found it. Condition 2 is not met on these bytes as a bind claim. Condition 3 is not a bind condition on these bytes.

Operator answers this. Handoff → `operator`.
