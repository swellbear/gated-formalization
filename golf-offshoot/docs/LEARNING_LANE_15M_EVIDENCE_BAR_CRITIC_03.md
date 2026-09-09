# Soften Critic — attack on unreviewed watched artifacts after PROPOSED 02 RUN-ONLY (CRITIC 03)

**Role:** Soften Critic · **Date:** 2026-09-08 · **Lane:** `learning_lane_15m` · series `KXBTC15M` only
**Branch:** `cursor/part-a-clerical-trust-boundary` at `a97800b` (CoS assign). Bar bytes last touched at `5dc4f24`. Registry row last touched at `0daae90`.

**Session separation.** This session did not draft the bar, did not write CRITIC 01 or CRITIC 02, did not write the Turn 3 admit pass (`5dc4f24`), did not declare `R-SKIP-2TO1-FAVORITE` (`e9fab5a`), and did not RUN-ONLY it (`0daae90`).

**This is an attack, not a verdict.** Operator answers each objection in a turn that is not this one. Nothing here is a Soften, an ADMIT, a RUN-ONLY, a park, a score, or a proposal. No rule was scored. `R-SKIP-COINFLIP` was not revived and its band was not retuned. `binding` stays `false` exactly as I found it. Trading is **NOT ARMED**.

**Why this file exists.** Desk Job 2026-09-08 17:15 ET: attack the unreviewed watched artifacts after PROPOSED 02 RUN-ONLY — evidence-bar hashes since last findings, and the rule registry row `R-SKIP-2TO1-FAVORITE`. Written objections only.

The last `critic-invariants` findings artifact (`LEARNING_LANE_15M_CRITIC_FINDINGS.json`, `ran_at` 2026-09-08T12:02:45−04:00) still reviews the **pre–Turn 3** bar and the **pre–PROPOSED 02** registry. Those hashes do not cover the bytes on disk now.

---

## Artifacts attacked, by SHA-256

Computed independently via the same newline-normalised `read_text` → UTF-8 digest `critic.artifact_digest` uses (copied, not imported: this tree's package import pulls `pydantic`, which is not installed in this fire). Byte hash equals the normalised hash on every file below (0 CRLF pairs).

| File | SHA-256 (bytes = normalised) | Last findings hash | Unreviewed? |
|---|---|---|---|
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR.md` | `70772F9640BB0F5614169BF1D02A655C88B5060EDADE85F5461FC50307075B05` | `5F2AA5F5…` | **Y** — Turn 3 bytes; CRITIC 02 attacked `C220AF0E…` / `5F2AA5F5…` |
| `golf-offshoot/docs/LEARNING_LANE_15M_EVIDENCE_BAR.json` | `231B2835D0574D22F449F69735A676EA3F332D10A5207985701912CB4FBFE83B` | `2611C255…` | **Y** — same Turn 3 gap |
| `golf-offshoot/docs/LEARNING_LANE_15M_RULES.json` | `8A70A827F7E8BE34482A3E82DAE2B9928F6A76CEAF748997BAFE1C9DE35225F8` | `CD25DD72…` | **Y** — `R-SKIP-2TO1-FAVORITE` + `execution=true` |
| `docs/agents/DESK.md` `## Honesty checklist` | `609217EEA041280196679D7A142A490B394EBFD26BC3E286C6401B72D5614F0F` | `07055605…` | **Y** — restamp names PROPOSED 02 |
| `golf-offshoot/docs/LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md` | `83D4463B4BB55D327485E3874A4BF3DAA54727D7ED37F56C124C6E8913DAF0B4` | `83D4463B…` | N — still the watched `lab_proposed` path |

**Not in `WATCHED`** (see objection 5). Recorded so the next findings file cannot pretend they were reviewed:

| File | SHA-256 |
|---|---|
| `golf-offshoot/docs/LEARNING_LANE_15M_LAB_PROPOSED_02.md` | `904DB245F4597D77AFF3379B6FEC347EBBEEE7F5DEF828619D3DCFCF487E3520` |
| `golf-offshoot/docs/LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_02.md` | `26D1B7FF593BC580145541918A7488FA62AC14996E3DCF2105F30D23FBFE4995` |

Bar git blobs at `5dc4f24` equal HEAD (`94ba0a8a…` / `0b76c0e9…`). Operator did not edit the bar when flipping execution (`0daae90` stat has no bar path). The unreviewed bar hashes are the Turn 3 amendment CRITIC 02 never saw, now also stale about the registry.

Hashes recomputed at the end of the attack and unchanged: the text I attacked did not move under me.

---

## Posture

I did **not** open a window outcome file — no `paper/*.json`, no `settlements/*.json`, no `latest/journal.json`. I did not call `score_rule`, `write_critic_findings`, or `mark_roles_served`. I did not run the digest generator. I did not start or stop a hub.

Numbers below come from the bar, the registry, the commit record, the published RUN-ONLY fee table in `LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md` (a documentation artifact, not a window file), and arithmetic I can do without the tape.

I did not edit the bar, the JSON, the registry, `critic.py`, `DESK.md` (except the worker Status/thread this fire is required to write), or `AGENT_LEAVE_OFF.md` until closeout. I did not set `binding: true`. I did not pin a fee-schedule hash.

---

# The one-sentence version

**The executing selection rule is `R-SKIP-2TO1-FAVORITE`, and the bar's machine copy still says no post-flip selection rule exists; the only pre-registration record of the new parameter is a `note` field; and `WATCHED.lab_proposed` still points at PROPOSED 01, so the Critic body cannot see the candidate this Job named.**

---

## Objection 1 — The bar's face denies the executing rule

### **UPHELD.**

`LEARNING_LANE_15M_EVIDENCE_BAR.md:210` and `LEARNING_LANE_15M_EVIDENCE_BAR.json:78` both state: **"No selection rule declared after the flip exists."** `currently_reachable` is `false` for that reason (JSON `:77–79`).

The registry on the same tree, same branch, now contains exactly that rule:

| | |
|---|---|
| id | `R-SKIP-2TO1-FAVORITE` |
| `declared_at` | `2026-09-08T16:53:00-04:00` |
| First-naming commit | `e9fab5a` (`2026-09-08T20:56:05+00:00` = 16:56:05 EDT) |
| `execution` | `true` (flipped `0daae90`, Operator note 17:11 EDT) |
| After the flip? | Yes. Flip of `decide()` into the paper path is `0a480d4`. Declaration is later the same afternoon. |

Operator already wrote the contradiction down and chose not to fix it (`LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_02.md:71`): "The bar still says 'No selection rule declared after the flip exists' … That sentence is now stale as to existence of a post-`0a480d4` selecting row; updating it would re-owe Soften Critic. This fire does not edit the bar."

So the false sentence is intentional. A bar that is the governing source for Established, and that leaves a known-false existence claim on its face to avoid a Critic owe, is not a governing source. CoS assigned this owe anyway. The sentence is still there.

`currently_reachable: false` can remain false for other reasons that are still true: the bar is not binding, condition 2 fails on the unpinned fee hash, condition 3 is unmet, and pre-registration of this new parameter has not been recorded on the bar (objection 3). **Those are not the reasons the bar gives.** The reason it gives is an existence claim the registry refutes.

**Concrete change demanded.** Rewrite `unreachable_because` / `:210` so they no longer assert non-existence of a post-flip selecting row. Name `R-SKIP-2TO1-FAVORITE` on the face. Keep `currently_reachable: false` only with reasons that are still true. Do not flip it to true in the same turn — binding, the fee hash, and Founder read-once are still unmet, and I have not established pre-registration.

**What would prove me wrong.** Show that `R-SKIP-2TO1-FAVORITE` is not a selection rule, or that it was declared before `0a480d4`, or that `execution` is not `true`. The registry row at the hash above contradicts all three.

---

## Objection 2 — Binding condition 1 is marked met for other bytes

### **UPHELD.**

`LEARNING_LANE_15M_EVIDENCE_BAR.json:17–20` sets `binding_conditions[0].met: true` for the CRITIC 02 + ANSWER 02 pair. CRITIC 02 attacked bar hashes `C220AF0E…` / `6B8013DA…` (normalised `5F2AA5F5…` / `2611C255…`). The bytes proposed to bind now are `70772F96…` / `231B2835…`.

The bar's own rule at `:18` and `LEARNING_LANE_15M_EVIDENCE_BAR.md:17`: **"Amending this bar re-owes the Critic on the new text."** Turn 3 (`5dc4f24`) amended the bar in the same Operator fire that answered CRITIC 02. That is the same gap CRITIC 02 opened against CRITIC 01: condition 1 marked met for a previous version. Operator disclosed the re-owe and then left `met: true` on the new bytes.

This file is the attack on those bytes (and on the registry). It does not make condition 1 met. Operator must answer it in a later turn. If Operator amends the bar again while answering, condition 1 is again unmet for the resulting bytes.

**Concrete change demanded.** Set `critic_answered.met` to `false` on any bar whose normalised digest is not the digest named in the last completed attack+answer pair. After this file is answered, the new pair's hashes go in the condition block. Do not treat an answer that amends the bar as closing condition 1 on the amended text.

**What would prove me wrong.** Show that CRITIC 02's reviewed hashes equal `70772F96…` and `231B2835…`. They equal `5F2AA5F5…` and `2611C255…`.

---

## Objection 3 — Pre-registration of `favorite_odds=2` lives in a `note` field

### **UPHELD** as a missing bar record, **not** as a proven peek.

The bar's pre-registration test (`LEARNING_LANE_15M_EVIDENCE_BAR.md:159–166`, JSON `:213–215`) needs (1) the commit SHA and timestamp of the registry entry that first names the parameter, and (2) that this timestamp predates the earliest window whose mark informed the parameter, **including marks published anywhere on this tree**. A `note` field asserting blind choice "**is not accepted as proof**" (`:161`, Hard NO `:301`).

`preregistration.rules` (`LEARNING_LANE_15M_EVIDENCE_BAR.json:216–231`) lists **only** `R-SKIP-COINFLIP`. The executing selection rule is absent.

What exists instead:

- Registry `note` (`LEARNING_LANE_15M_RULES.json:61`): "The free parameter is the integer prior favorite_odds=2 … No window mark informed the parameter. First naming e9fab5a."
- Lab PROPOSED 02 §5: the same claim, plus "I did not open those mark tables to choose it."
- Operator note `:39`: "Does not fire" on informing marks, citing a tree search after the fact.

That is exactly the self-certification the bar refuses for the other selection rule.

**What I verified without opening a window file.**

- First git appearance of `favorite_odds` or `R-SKIP-2TO1-FAVORITE` is `e9fab5a`. I did not find an earlier naming.
- `declared_at` `16:53:00−04:00` precedes the commit by **3 minutes 5 seconds** (`e9fab5a` 16:56:05 EDT). Same shape as the coinflip row's 51-second commit lag; not an 8-hour gap.
- The published RUN-ONLY fee table (`LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md:44–67`, landed `2fea8d8` at 2026-09-07T21:49:37−04:00) lists 24 marks. **2 of 24** are ≥ 2/3: `0.9835` (`071545`) and `0.7050` (`071600`). Gap from that publish to `e9fab5a` is **19h 06m 28s**.
- I did not compute a contrast, a skip rate on later tape, or any pnl. I did not open those books.

Under the bar's information-not-intent standard, those two marks existed on this tree before the parameter was named. That is **weaker** than the coinflip case (8/24 inside a band with no conventional prior). `favorite_odds=2` as "the first integer odds strictly above evens" is a named prior that does not require the tape. I am **not** claiming the parameter fails the same way `(0.45, 0.55)` failed. I am claiming the bar has not applied its own test to the rule that is now executing.

**Concrete change demanded.** Add a `preregistration.rules` row for `R-SKIP-2TO1-FAVORITE` / `favorite_odds=2` with: first-naming commit `e9fab5a`, timestamps, the 2/24 count from the already-published fee table (or a stated reason those marks are not informing), and an explicit `verifiably_preregistered` true or false. A `note` on the registry is not that row.

**What would prove me wrong.** That row, already on the bar I hashed. It is not there. A commit predating `2fea8d8` that names `favorite_odds=2` would also kill the information-availability half; I did not find one.

---

## Objection 4 — The bar's face still says `trials_to_date` stays 0; the next look's α is not 0.025

### **UPHELD.**

`LEARNING_LANE_15M_EVIDENCE_BAR.md:220–224`: "`trials_to_date` stays 0. This turn does not increment it." JSON `:132` repeats it. The registry I hashed has `trials_to_date: 1` and a `trials_log` declaration row for `R-SKIP-2TO1-FAVORITE` (`LEARNING_LANE_15M_RULES.json:8–18`). That increment is what the bar *asked* for (`:222`, `record_trial` on declaration). The face was not updated.

`score_rule` reads `trials_to_date` from the registry (`rules.py:504–505`) and computes `alpha_k(k)` with `k = trials_to_date + 1` (`rules.py:176–183`). After this declaration, the next look is **k = 2**, α = `0.05 / (2 · 3)` = **0.008333**, not the face's `alpha_first_look: 0.025` (`LEARNING_LANE_15M_EVIDENCE_BAR.json:126`).

The scorer will use 0.008333. A reader of the bar's face will use 0.025. Those are different tests. I do not object to spending the first α slot on a declaration — that is the amended rule. I object to advertising the spent slot as the one this rule will be scored under.

**Concrete change demanded.** Restate `trials_to_date` on the bar's face as the registry value (1), and state the next look's k and α given that value. Keep `alpha_first_look: 0.025` only as the schedule's first term, labeled historical.

**What would prove me wrong.** Show the registry still reads `trials_to_date: 0`, or show `score_rule` ignores the registry and uses `alpha_first_look`. I read both files; neither is true.

---

## Objection 5 — `WATCHED.lab_proposed` is frozen on PROPOSED 01

### **UPHELD.**

`critic.py:44` and `WATCHED` (`:66–72`) pin `lab_proposed` to `LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_01.md`. That file's hash is **unchanged** since the 12:02 findings (`83D4463B…`). `artifact_unreviewed` therefore does not fire on PROPOSED 02.

The candidate this Job named lives in:

- `LEARNING_LANE_15M_LAB_PROPOSED_02.md`
- `LEARNING_LANE_15M_OPERATOR_NOTE_PROPOSED_02.md`
- the registry row (watched — this is why the Job could fire at all)

A later edit to the PROPOSED 02 notes cannot re-owe Soften Critic. The trigger that was built so "editing a bar re-owes the Critic on the new text and cannot be cleared by editing something else" (`critic.py:16–18`) does not apply to the second Lab/Operator pair. This attack had to be CoS-assigned. The machine will not assign the next one.

Compounding it, `LEARNING_LANE_15M_LAB_PROPOSED_02.md:50–56` and `:86` still describe `execution=false` after Operator flipped the row (`0daae90` touched the header, not those lines). The proposing artifact now disagrees with the registry about the flag the paper loop reads. Because that file is not watched, `critic-invariants` will never notice.

**Concrete change demanded.** Watch the current Lab PROPOSED and its Operator note, not a hardcoded `_01` path — or watch a single stable path that always names the latest pair. Until that exists, say on the findings artifact that PROPOSED 02 notes are outside `WATCHED`. Reconcile the leftover `execution=false` sentences in the Lab file with the registry, or label them as the proposing-turn state.

**What would prove me wrong.** Show `WATCHED` already includes `LAB_PROPOSED_02` / `OPERATOR_NOTE_PROPOSED_02`, or show `unreviewed()` lists them. `critic.py:44` and the 12:02 `reviewed` block name `_01` only.

---

## Objection 6 — The declaration-to-flip interval is unlabeled on the governing artifacts

### **UPHELD.**

Operator's note (`:60–61`) correctly says replay of windows that closed after `declared_at` and before the flip is still replay, not lived, and that this turn does not treat replay as lived.

The bar and the registry — the artifacts a later `score_rule` / L2 check will read — do **not** name that interval.

Clocks only (no book opened):

| Event | Time (EDT) |
|---|---|
| `declared_at` | 2026-09-08 16:53:00 |
| First-naming commit `e9fab5a` | 16:56:05 |
| Operator flip (note) | 17:11:00 |
| Flip commit `0daae90` | 17:14:46 |

KXBTC15M closes on the quarter-hour. Any window whose `close` is strictly after 16:53:00 and at or before 17:11:00 is eligible for this rule as **replay**. I am not asserting which window ids exist or what they paid. I am asserting the clocks create at least the 17:00 close as a candidate for that class.

L2 "must be lived" (`LEARNING_LANE_15M_EVIDENCE_BAR.md:206`, JSON `:112`). If a later score silently treats every post-`declared_at` window as lived because `execution` is now true, the flip timing rule (`:80`, `:213–214`) is unenforceable.

**Concrete change demanded.** Record on the registry row and on the bar's replay/lived section: lived paper for this rule begins at the flip commit `0daae90` / 17:11:00−04:00, not at `declared_at`. Name the close-time interval that remains replay. A later L1/L2 score that includes a window from that interval as lived fails the bar.

**What would prove me wrong.** Show `declared_at` ≥ flip time (no interval), or show the registry/bar already names the flip as the lived start. The row I hashed names `declared_at` and a note that execution flipped; it does not name the replay interval.

---

# Considered and not filed

- **FEE-AS-SIGNAL.** Taker fee `k · stake · (1 − P)` is smallest at the marks this rule skips. On the published 24-row table the two skip-eligible marks are the two cheapest fees (`0.01` at 0.9835, `0.03` at 0.7050). Opposite region from the burned class. Operator's "does not fire" stands. I do not invert it by reading later tape.
- **RETUNE-COINFLIP-BAND / THRESH / oil burns.** Different parameter, different skip region, `class_is_burned("SKIP-2TO1-FAVORITE")` is false in the committed test. Re-naming MAG is still MAG; this is not that.
- **`favorite_odds=2` as a conventional prior.** I filed the missing bar row (objection 3), not a claim that "first integer odds above evens" is a tape quantile. 2/24 on a published table is not 8/24 inside a fitted band.
- **Keyword greens / δ-check / vacuous greens.** CRITIC 02; Operator overruled the keyword half against the checker at `0a480d4`. I did not re-run the scratch tree. I do not re-file a sustained-and-answered attack.
- **Unpinned fee hash.** Already on the bar's face as the standing condition-2 blocker. Recording another 429 does not add a check.
- **Operator's "no new loop code" at the flip.** `_express_selection` / `favorite_threshold` landed in `e9fab5a` (Lab). At `0daae90` the expression already existed. The RUN-ONLY gate is about that turn.
- **Scoring, eligible counts, or opening the tape.** Forbidden this Job. Nothing here needs a post-declaration outcome.
- **Honesty-stamp bankroll 90.98 / `crew_tick` clause from 14:42.** The section hash moved because the restamp named PROPOSED 02. The derived boxes are not mine to reopen. The 14:42 `crew_tick` clause is stale next to Status=assigned; that is CoS restamp residue, not a bar or registry defect I need in order to attack this Job.

---

**Closing.** I proposed no rule, scored no rule, ADMITted nothing, PARKed nothing, and did not Soften, Harden or Kill anything. I did not set `binding: true`, did not pin a fee-schedule hash, and did not write a placeholder for one. I opened no window outcome file. I did not edit the bar, the registry, or `critic.py`. Trading is **NOT ARMED**.

Six objections, all UPHELD. One of them (3) is upheld as a missing record, not as a proven peek.

Operator answers these. Handoff → `operator`.
