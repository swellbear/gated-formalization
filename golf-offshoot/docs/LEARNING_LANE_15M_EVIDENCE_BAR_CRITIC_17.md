# Soften Critic — attack on Founder-GO drop-read-once factory evidence-bar hashes (CRITIC 17)

**Role:** Soften Critic · **Date:** 2026-09-09 · **Lane:** `learning_lane_15m` · series `KXBTC15M` only
**Branch:** `cursor/honer-15m-sibling` at `e0ff49c` (CoS assign). Factory bar last touched at `98f7eaa` (drop `founder_read_once`). Git blobs of the two attacked bar files still equal `98f7eaa` (`aa7dead4…` / `3ef92f2f…`).

**Session separation.** This session did not draft the bar, did not write CRITIC 01–16, did not write ANSWER 01–15, did not land `98f7eaa` / `1dea3c7` / `b9925db` / `c514015` / `1b21a70` / `86e0cce`, did not declare `R-SKIP-2TO1-FAVORITE`, and did not RUN-ONLY it. `PROTOCOL.md` forbids one turn both objecting and dismissing.

**This is an attack, not a verdict.** Operator answers each objection in a turn that is not this one. Nothing here is a Soften, an ADMIT, a RUN-ONLY, a park, a score, or a proposal. No rule was scored. `R-SKIP-COINFLIP` was not revived and its band was not retuned. Consult was not enabled. `binding` stays `false` exactly as I found it. Trading is **NOT ARMED**.

**Why this file exists.** Desk Job 2026-09-09 21:50 ET: attack the Founder-GO drop-read-once factory evidence-bar bytes (`2ACB998B…` / `B1044CCE…`). Written objections only. Do not probe the fee PDF. Honer catalog/rules starvation hashes remain after this attack.

Those desk prefixes do **not** match the factory bar files on this checkout. The drop-read-once factory bytes at `98f7eaa` digest to `1D29ABCD…` / `A5FCFAB7…` (newline-normalised = raw; 0 CRLF). I attacked those files. ANSWER 15 (`LEARNING_LANE_15M_EVIDENCE_BAR_OPERATOR_ANSWER_15.md`, SHA-256 `14747327…`) recorded CRITIC 15 on the **ANSWER 14** hashes. CRITIC 16 (`1F513FBD…`) was zero UPHELD on the **ANSWER 15** hashes (`3C8369B4…` / `1F183CE1…`). Those are not the bytes on disk now. Condition 1 is correctly `met: false` for that reason. This file attacks the **new** bytes.

---

## Artifacts attacked, by SHA-256

Computed independently via the same newline-normalised `read_text` → UTF-8 digest `critic.artifact_digest` uses (copied, not imported: this tree's package import pulls `pydantic`, which is not installed in this fire). Byte hash equals the normalised hash on every file below (0 CRLF pairs), except the honesty section, which is a slice of `DESK.md`.

| File | SHA-256 (bytes = normalised) | Last findings hash | CRITIC 16 attacked | Unreviewed? |
|---|---|---|---|---|
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR.md` | `1D29ABCDC13746F349374F584F265CDD226C53486862CFA467552EB898C8091E` | `5F2AA5F5…` | `3C8369B4…` | **Y** — drop-read-once amend |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR.json` | `A5FCFAB7004A71F8C25E608505941FC9619C9DC8415B218DEA0E32F7F4DC4770` | `2611C255…` | `1F183CE1…` | **Y** |
| `golf-offshoot/docs/LEARNING_LANE_15M_RULES.json` | `BBD87E52EE6FC1E5F797C676EA6038F4C77404DDE7F29E21128BD75BF4B802D0` | `CD25DD72…` | same digest | **Y** — unchanged since `3c89a7f`; still unreviewed by findings |
| `docs/agents/DESK.md` `## Honesty checklist` | `615410C04ED519B17E5E7920AD7C8CA46E680EA4AB0D804186473F91E5A33826` | `07055605…` | `7C5A9AE5…` at CRITIC 16 | **Y** — CoS 21:50 restamp names the drop / this assign |
| `golf-offshoot/docs/LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md` | `83D4463B4BB55D327485E3874A4BF3DAA54727D7ED37F56C124C6E8913DAF0B4` | `83D4463B…` | same | N — still the watched `lab_proposed` path |
| `golf-offshoot/docs/LEARNING_LANE_15M_FEE_SCHEDULE_PROBE.json` | `5DD35C25BADDF941803558D4D7DF871D4BA5CE5620588CE895DDFC7D0CCCC36C` | — | same | not `WATCHED`; cited by the restated 17:01:17 owed row |

Honesty slice is the committed `e0ff49c` section (this fire's Status/thread writes do not touch it). Hash of that slice after the Status write equals the committed slice.

**Cited by the drop-read-once face and not in `WATCHED`:**

| File | SHA-256 |
|---|---|
| `golf-offshoot/src/golf_offshoot/learning_lane_15m/evidence_bar.py` | `7E7EC20DB47D4F1BB64F364AE1AB2CA41852DD68E0C9F896C0608873B9B26A9D` |
| `golf-offshoot/src/golf_offshoot/learning_lane_15m/critic.py` | `ECC4EB55D75A2BE1D94CECA0440030876E73A6F70DD01F4DF6E7DBD82866E190` |
| `golf-offshoot/src/golf_offshoot/learning_lane_15m/watch.py` | `44DFC0036F75C3E369A713942295D0580A9862739201AF8C9D278994284710D0` |
| `golf-offshoot/src/golf_offshoot/learning_lane_15m/paths.py` | `C543D98DB589C9822DA73F712C03A2EC22F0E3BDCFF6F5EA5630B4E225CD476C` |
| `golf-offshoot/docs/HONER_15M_PROMOTION.md` | `7FD9E8B24F6E8467E5735DB7690B39967500EFE23C4C79861A5E56775DCE5E40` |
| `golf-offshoot/src/golf_offshoot/learning_lane_15m/consult_honer.py` | `D4698C7A86D94B8380FBCFB9283A795287D650FD2D63A3F6048F6E07C41E98D3` |
| `golf-offshoot/src/golf_offshoot/learning_lane_15m/paper.py` | `F52AB86F81793482543C0E70180CD5F76E9F000EA5BD0B10B3D467597FF68447` |
| `golf-offshoot/docs/LEARNING_LANE_15M_LAB_PROPOSED_02.md` | `460F59A369241E107F7FD48A22898F24D4456338618A7927D73D7AEBDC0368E2` |
| `golf-offshoot/docs/LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_02.md` | `1071B9F7402EA0807147F64731456B80030310ED9FB2F6FF5ECD3009CC303119` |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR_CRITIC_16.md` | `1F513FBDFB9839C82B763488333A5A65A79898DAA9E3067422CD4574C21142E7` |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR_OPERATOR_ANSWER_15.md` | `1474732761FBDC334B6C75EE25AE437408A5D1C5428C4CA12DE9C7F503C025F5` |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR_CRITIC_15.md` | `DF4187028075C127392CC6A73F3F362E06C7C2DB087163441375FA5C03A46541` |

**Honer catalog/rules starvation hashes — remain after this attack. Not attacked.** Catalog/rules digests are unchanged since `86e0cce`. Honer evidence-bar files moved in `98f7eaa` (same drop-read-once fire); recorded, not attacked.

| File | SHA-256 |
|---|---|
| `golf-offshoot/docs/HONER_15M_CATALOG.json` | `CFAF1E50975B230B17103C16170C282F123FB842E349AE90990AC51C2AD220D6` |
| `golf-offshoot/docs/HONER_15M_RULES.json` | `E6EF7CEFCF300B14A1B5FC3F66F79F136121317E07728912AE568367F30C7C3E` |
| `golf-offshoot/docs/HONER_15M_EVIDENCE_BAR.md` | `CED34B6C3AE34AD426B849F4A2FF782564B18665CFF489FA8B49429BFA28F170` |
| `golf-offshoot/docs/HONER_15M_EVIDENCE_BAR.json` | `C35AF511DB856350BBBE65477F8F48142299ABA2B3E662E6961B6DA184E1381F` |

No `honer_consult.json`, `series_fee.json`, or `fee_schedule_probe.json` on this tree under `golf-offshoot/data/learning_lane_15m/latest/` or `/workspace/kalshi_15m_exports/latest/` (`/workspace` exists; the export root does not). I did not call `artifact_root_15m()` / `latest_dir_15m()` and did not create that directory.

Hashes recomputed at the end of the attack and unchanged: the text I attacked did not move under me.

---

## Posture

I did **not** open a window outcome file — no `paper/*.json`, no `settlements/*.json`, no `latest/journal.json`, no `rule_decisions.json`. I did not call `score_rule`, `write_critic_findings`, `gym_fee_tick`, `latest_dir_15m`, or `mark_roles_served`. I did not run the digest generator. I did not start or stop a hub. I did not fetch `https://kalshi.com/docs/kalshi-fee-schedule.pdf`. `watch.json` is not on this tree.

The package import pulls `pydantic`, which is not installed. Numbers below come from the bar, `critic.py` as text, the fee-probe file, and the commit record.

I did not edit the bar, the JSON, the registry, `consult_honer.py`, `critic.py`, `evidence_bar.py`, `DESK.md` (except the worker Status/thread this fire is required to write), or `AGENT_LEAVE_OFF.md` until closeout. I did not set `binding: true`. I did not pin a fee-schedule hash. I did not write a placeholder. I did not set `consult_enabled`.

---

# The one-sentence version

**`98f7eaa` dropped `founder_read_once` from bind — two `binding_conditions`, no `(3)` in `binding_rule`, JSON `unreachable_because` struck "condition 3 is unmet" — and left MD `:238` still saying condition 3 is unmet.**

---

## What I accept as closed on the prior text (not re-filed)

The drop-read-once amend did the thing the Founder GO named on the bind face. I am not re-opening bind-as-three-conditions as if unanswered. I hunted residue that would be **new on these bytes**.

| Drop-read-once change | What I verified on these hashes | Closed as to the prior sentence? |
|---|---|---|
| Bind is (1) Critic+Operator and (2) critic-invariants | MD `:9–14`: "This draft becomes binding only after both" then two numbered gates; "Founder read-once is **not** a bind condition." JSON `:48` `binding_rule` has no `(3)`. JSON `binding_conditions` has **two** rows (`critic_answered`, `critic_invariants_pass`). Grep of both files for `Founder reads it once` / `(3) Founder` is empty. `id` `founder_read_once` is absent from `binding_conditions`. | **Yes, as to the bind list.** Residue of MD `:238` still *citing* an unmet condition 3 is objection 1. |
| Ninth check `bind_has_no_founder_read_once` | MD `:48` / `:306` name nine method checks; ninth is that id. JSON `:382` `founder_2026_09_09_no_read_once`. `critic.py` `CHECKS` (`:946–956`) has nine members; ninth is `check_bind_has_no_founder_read_once`. Needles (`:843–844`) are `(3)\s*Founder read-once` on `binding_rule` and `Founder reads it once` on the markdown. | **Yes, as to the check existing and not seeing the dropped numbered gate.** It does not read `condition 3 is unmet`. That leftover is objection 1, not a demand to edit `critic.py`. |
| ANSWER 15 leftover half-pass citation | Still on MD `:47` / JSON `:286` / `:291–293` / ratchet `:324` / JSON `:381`. CRITIC 16 closed that as to the ANSWER 15 hashes. Still true of these hashes. | **Yes.** Not re-filed. |

Registry digest is unchanged (`BBD87E52…`); `trials_to_date` is 1; one log row, kind `declaration`; `R-SKIP-2TO1-FAVORITE.execution` true; `R-SKIP-COINFLIP.execution` false; `verifiably_preregistered` false on both selection rows. `binding` false. Consult off. I did not enable it.

---

## Objection 1 — MD `:238` still says condition 3 is unmet after these hashes dropped that bind condition

### **UPHELD.**

`98f7eaa` struck condition 3 from the bind list. These hashes have two `binding_conditions`. JSON `:48` `binding_rule` ends at (2). JSON `:124` `unreachable_because` was amended in the same commit: it dropped the clause `condition 3 is unmet`. Grep of the JSON for `condition 3` is **empty**.

MD `:238` — the Established-unreachable sentence, the same sentence the JSON copy restates — still says:

> The bar is not binding; condition 2 fails on the unpinned fee hash and on findings that do not cover these bytes; condition 3 is unmet; and `favorite_odds=2` is **not verifiably pre-registered**.

Grep of the markdown for `condition 3 is unmet` is **1** (that line). There is no third bind condition on these hashes for that clause to be unmet *of*. Leave-off on this checkout names what condition 3 was: `founder_read_once`. CRITIC 03 / ANSWER 03 used the same name for that gate.

The ninth check does not catch this. `check_bind_has_no_founder_read_once` (`critic.py:847–896`) fails on `binding_conditions` id `founder_read_once`, on `binding_rule` matching `(3) Founder read-once`, or on markdown containing `Founder reads it once`. MD `:238` matches none of those needles. A suite green on the ninth check is therefore possible while the Established face still treats a deleted bind condition as live and unmet.

I am not asking to put `founder_read_once` back. I am not asking to set `binding: true`. I am not asking to edit `critic.py`. This is the citation the amendment broke on one face and fixed on the other.

**Concrete change demanded.** State that MD `:238` still says "condition 3 is unmet" after these hashes dropped that bind condition — JSON `binding_conditions` has two rows, `binding_rule` has no `(3)`, and JSON `:124` `unreachable_because` already struck the phrase — **or** strike that clause. Do not restore the id. Do not bind. Do not fetch the PDF.

**What would prove me wrong.** Show MD `:238` does not contain `condition 3 is unmet`, or show `binding_conditions` still has a third condition, or show JSON `:124` still contains that phrase so the faces agree. The hashes I attacked have the leftover on the markdown only.

---

# Considered and not filed

- **Bind-as-three-conditions as if unanswered.** The bind list on these hashes is two. Not re-filed. The leftover is the Established-unreachable citation, not a re-open of the dropped gate.
- **These hashes now contain "Founder read-once is not a bind condition," so the ninth check PASS is true of the bind list.** That is the amend. Filing the successful drop as a new defect would pad.
- **Re-demand a `critic.py` needle for `condition 3 is unmet`.** Neighbor of objection 1. Editing `critic.py` is Systems; this Job forbids it. The demand is a face-statement or a strike.
- **Desk assign prefixes `2ACB998B…` / `B1044CCE…` do not match these files.** Clerical on the assign, not a bar face lie. Recorded above. Not filed against the bar.
- **Honer evidence-bar files moved in `98f7eaa`.** Job says catalog/rules hashes remain after. Catalog/rules unchanged (`CFAF1E50…` / `E6EF7CEF…`). Honer bars recorded, not attacked.
- **CRITIC 16 / ANSWER 15 leftover half-pass.** Still named on the face. Closed as to those hashes. Not re-filed.
- **The machine detail still says `latest/series_fee.json`.** Disclosed on `:47` / JSON `:286`. ANSWER 14 named both resolved paths. Not a second path finding.
- **`load_series_fee_snapshot` on invalid JSON is `{}`.** Disclosed. Closed as to CRITIC 14 item 1.
- **`expected_fee_type` / `expected_fee_multiplier` default to quadratic / 1 when omitted** (`critic.py:780–785`). Live bytes have both keys. Neighbor of a fail-open already declined. Not filed.
- **The historical 429 still sitting on `fee_hurdle`.** Disclosed (`schedule_fetch_status` 429 at 17:01:17). Not a second 429 finding.
- **Unpinned fee hash / the 429 itself.** Disclosed. Standing named fail. I will not write a placeholder. I will not fetch the PDF.
- **Last findings (`ran_at` 2026-09-08T12:02:45−04:00) still review `5F2AA5F5…` / `2611C255…` / `CD25DD72…` and do not include `series_fee_regime_matches` or `bind_has_no_founder_read_once`.** Disclosed. Condition 2 unmet. Not a new findings finding.
- **`WATCHED` still five factory artifacts.** Disclosed. Probe / series_fee / PROPOSED 02 notes unpaid, not new residue.
- **AND-skip / in-memory consult tag / flag-write / missing δ.** ANSWER 12 face remains. Not re-filed.
- **`WATCHED.lab_proposed` frozen on `_01`.** Disclosed, unpaid, CRITIC 03. Not re-filed.
- **`favorite_odds=2` / clause-(2) leftover ordinals / keyword greens / δ-check / vacuous greens.** Prior critics; already answered or disclosed. Not re-filed.
- **Honer catalog/rules starvation (`86e0cce`).** Job says those hashes remain after. Recorded, not attacked.
- **Copied `delta_above_detection_floor` still fails `alpha_first_look` vs current α_k.** Named on the face; owed to Systems. Not re-filed.
- **X2 lived honoring unproven / `currently_reachable` false.** Already answered. No new verb. Objection 1 is the leftover condition-3 *citation*, not a demand to flip reachable.
- **"Do not quote 6 of 8"** still on `:48` after the suite became nine. A do-not-quote of an old count, not a claim that there are eight. Not filed.
- **Scoring, eligible counts, opening the tape.** Forbidden this Job.
- **Enabling consult, binding, arming, lifting HOLD, reviving `R-SKIP-COINFLIP`, probing the fee PDF.** Forbidden this Job.

---

**Closing.** I proposed no rule, scored no rule, ADMITted nothing, PARKed nothing, and did not Soften, Harden or Kill anything. I did not set `binding: true`, did not pin a fee-schedule hash, and did not write a placeholder for one. I did not enable consult. I opened no window outcome file. I did not fetch the PDF. I did not edit the bar, the registry, the compositor, or `critic.py`. Honer catalog/rules hashes remain unreviewed. Trading is **NOT ARMED**.

One objection, UPHELD. Condition 1 stays unmet for these bytes until Operator records this attack in a separate turn. Binding stays `false` as I found it. Condition 2 is not met on these bytes. Condition 3 is not a bind condition on these bytes.

Operator answers this. Handoff → `operator`.
