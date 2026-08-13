# Dissertation — Application Findings

**Date:** 2026-08-12  
**Application:** `2026-08_fomc-sep-2026-uffr-change`  
**Claim family / parent (if any):** none (market-rules intake; no successor started). Related **FOMC June SEP** is a **different object** — no conclusion inheritance.  
**Closeout verdict:** **Stable Provisional (hard stop)**  
**Amb at closeout:** **2.5**

**Tags** (see `docs/TRACKER_TAXONOMY.md`): Domain `markets` · Claim-shape `forecast-extension`, `descriptive-census` · Pattern — (none forced)

**Related applications (max 4):** FOMC June SEP (different object; funds-rate off that bar) · FL property-tax (unnamed class / leave-unnamed) · sell-in-may (forecast locks) · SpaceX (modal + wait). Process kinship only; **no conclusion inheritance**.

---

## 1. Plain-language summary

The intake was a prediction-market **contract**: it pays on how much the **upper bound** of the Fed’s target funds range **changes** at the September 2026 meeting, versus the level just before that meeting. The named page listed five brackets. At fetch it showed about **67¢ no change** and **33¢ +25 bp**.

You chose to read those prices as **live-shot sizes**, not as “the” expected path. A trading market cannot be the only proof that any bracket is a real shot, so that bar is **not established**. You left a second series unnamed on purpose. That is **not** a finding that a hike is unlikely or that a hold is the path.

The September FOMC **statement** has not printed. That print is a separate leftover.

Bottom line: the page’s brackets and ¢ are recorded; no rate call is cleared.

---

## 2. Original claim and context

**Original claim (verbatim):**  
The FED interest rates are defined in this market by the upper bound of the target federal funds range. The decisions on the target federal funds range are made by the Federal Open Market Committee (FOMC) meetings.

This market will resolve to the amount of basis points the upper bound of the target federal funds rate is changed by versus the level it was prior to the Federal Reserve's September 2026 meeting.

If the target federal funds rate is changed to a level not expressed in the displayed options, the change will be rounded up to the nearest 25 and will resolve to the relevant bracket. (e.g. if there's a cut/increase of 12.5 bps it will be considered to be 25 bps)

The resolution source for this market is the FOMC’s statement after its meeting scheduled for September 15-16, 2026 according to the official calendar: https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm.

The level and change of the target federal funds rate is also published at the official website of the Federal Reserve at https://www.federalreserve.gov/monetarypolicy/openmarket.htm.

This market may resolve as soon as the FOMC’s statement for their September meeting with relevant data is issued. If no statement is released by the end date of the next scheduled meeting, this market will resolve to the "No change" bracket.

**Source / domain context:** Operator-pasted resolution rules (2026-08-12). Displayed brackets and URL were missing from the first paste; operator later named `https://polymarket.com/event/fed-decision-in-september-762`. June 17 SEP inventory is a **different** claim.

**Claim type:** Mixed — **D-OPTIONS** / **D-PRICE** (page census) + odds bar (M3) + **F-PRINT** (future statement). No “should” in the paste.

**Parent or successor relationship (if any):** none. CR toward print-only or another venue was **offered, not run**.

---

## 3. How it was examined

**Method path:** Phase 1 only. Cycle 0 recorded the contract (Amb 9). Operator locked **Rank 3** + named URL. Operator locked **M3** (live shots). Named-class pulse admitted **D-OPTIONS** / **D-PRICE** and executed **P-NN-TEST** (not established). Source-class choice set **REJECT**ed C1 as sole affirmation. Operator **`leave unnamed`**. Phase 1 endpoint, then closeout. No Phase 2. No UX/CX/CR/QI run.

**Governing lock / freeze (if any):** Rank 3 `Q3+O2+L1+M3+B1` — odds vehicle; five brackets from the named URL; Sep statement as print source; live-shot sizes not expected path; pre-meeting in-force baseline.

**Key artifacts:** `Lock_Rank3_Q3O2L1M3B1.md` · `E_Package_Evidence_Intake_D_OPTIONS_D_PRICE.md` · `04_Material_Admission_D_OPTIONS_D_PRICE.md` · `E_Package_Evidence_Intake_P_NonNegligible.md` · `04_Material_Admission_P_NonNegligible.md` · `R_Source_Class_Choice_Set.md` · `Phase1_Endpoint_Readout.md` · `RESIDUAL_BRANCH_MENU.md` · `OPTIONAL_MODES_MENU.md` · this closeout pack.

---

## 4. What was established

| Finding | Scope |
|---------|--------|
| Rank 3 meanings (odds vehicle / brackets / live print source / live-shot bar height / baseline) | Under Rank 3 — definitional, not a rate call |
| Five displayed brackets on the named Polymarket event | Under Rank 3 O2 (**D-OPTIONS**), fetch 2026-08-12 |
| Page printed Yes ¢ 0.6 / 1.1 / 67 / 33 / 0.5 (and displayed %) | Under Rank 3 Q3 (**D-PRICE** — conflicted pitch curve) |
| P-NN-TEST on C1: bar **not met** for any bracket | Under Rank 3 M3 (**evaluation**, not bar-met) |
| Page rules text matches the operator paste | Same vintage |

---

## 5. What was not established

| Item | Status |
|------|--------|
| P-NonNegligible: any named bracket is a live shot | **not established** (C1 conflicted; C2 `leave unnamed`) — **not a refute** |
| P-BaseCase: no change (or any bracket) is the expected path | **not the locked bar**; not established |
| F-PRINT: September upper-bound **change** | **untested** (statement does not exist) |
| The FOMC will hold / hike / cut | **open** (no cleared rate call) |
| C1 as sole P-NonNegligible affirmation | **REJECT** (conflicted-source) |
| June SEP as this path | **excluded** (different object) |
| Kalshi / CME FedWatch as this class | **unnamed** (not invented) |

---

## 6. Forced deviations and scope limits

**Forced-deviation terms (if any):** None. Ranks 1 and 2 were Minimal deviation. Rank 3 is a **Moderate** odds fork (chosen), but FD extraction was not triggered.

**Scoped vs unrestricted:** All content findings are **under Rank 3 M3 + named Polymarket census**. They are not unrestricted support for a hold/hike/cut.

**What the lock/package could not settle relative to the original wording:** Who wins the market; whether any bracket is a cleared live shot; what the September statement will print. The freeze made the odds bar testable on this page; conflicted-source blocked affirmation; the operator left a second class unnamed.

---

## 7. Quantitative results (if any)

Page print only (not a numerical instance bar; not bar-met):

| Bracket | Yes ¢ | Header % |
|---------|-------|----------|
| 50+ bps decrease | 0.6¢ | <1% (card also shows 1%) |
| 25 bps decrease | 1.1¢ | 1.0% |
| No change | 67¢ | 67% |
| 25 bps increase | 33¢ | 33% |
| 50+ bps increase | 0.5¢ | <1% |

Vintage: fetch 2026-08-12; page “as of August 13, 2026.” Separate binaries; ¢ need not sum to 100. Header % vs Yes ¢ mismatch on 50+ decrease **recorded, not collapsed**. No ¢ cutoff invented for “non-vanishing.” Volume headline ~$29.9M is not a bar.

---

## 8. Revisions, implications, and alternatives

UX, CX, and CR were **offered, not run** ([`OPTIONAL_MODES_MENU.md`](OPTIONAL_MODES_MENU.md)). QI **N/A** (no failed numerical instance bar). Experimental Generation not authorized.

Original contract wording **kept** (default). Do not invent exhibit content for unrun modes.

---

## 9. Final status of the original claim

**Verdict:** **Stable Provisional (hard stop).** Split: D-OPTIONS / D-PRICE admitted; P-NonNegligible not established; F-PRINT untested.

**Amb ≠ clearance:** Amb 9 → 2.5 because venue, brackets, and M3 were frozen. Composition then kept Amb at 2.5 (independent class unnamed). That path does **not** answer hold/hike/cut.

**Locked-bar status summary:** P-NonNegligible **not established**. P-BaseCase not the locked bar. F-PRINT untested.

**Continuation / hard-stop note:** Hard stop sealed. [R-P-NN](RESIDUAL_BRANCH_MENU.md#r-p-nn) and [R-F-PRINT](RESIDUAL_BRANCH_MENU.md#r-f-print) remain `park-until-trigger` (not `pursue`). Optional modes remain offered. No auto Phase 2.

---

## 10. What would still be needed

Concrete reopen for live shots: `name source class C2: [exact series]` that publishes a central statistic on the **same Sep 2026 upper-bound-change object** and is usable for affirmation. C1 / Kalshi / CME FedWatch / June SEP as slogans **do not** fire. See [R-P-NN](RESIDUAL_BRANCH_MENU.md#r-p-nn).

Concrete reopen for the print: FOMC statement after Sep 15–16 2026 (or the contract fallback clock). See [R-F-PRINT](RESIDUAL_BRANCH_MENU.md#r-f-print).

Optional, not required: `run UX` · `run CX` · `run CR`.

---

## 11. Technical appendix

### Amb path

| Stage | Amb | Note |
|-------|-----|------|
| Cycle 0 | 9 | Contract intake; meanings unset |
| Rank 3 incomplete (M unset) | 2.5 | Venue + brackets locked; M OR-slot open |
| M3 + P-NN-TEST | 2.5 | M locked; independent class enters as High 2 (composition change) |
| `leave unnamed` / closeout | 2.5 | Disposition park-until-trigger; Amb not dropped by leaving unnamed |

### Admitted layers (index)

| ID | One-line | Pointer |
|----|----------|---------|
| Rank 3 lock | Q3+O2+L1+M3+B1 | `Lock_Rank3_Q3O2L1M3B1.md` |
| **D-OPTIONS** | Five displayed brackets | `04_Material_Admission_D_OPTIONS_D_PRICE.md` |
| **D-PRICE** | Conflicted Yes ¢ print | same |
| **P-NN-TEST** | M3 not established on C1 | `04_Material_Admission_P_NonNegligible.md` |

### Key artifacts

- `01_Anchor_and_ClaimType_Template.md`  
- `02_Gate_Scoring_Sheet_after_M3.md`  
- `03_Gap_Extraction_and_Ranking.md`  
- `R_Source_Class_Choice_Set.md`  
- `Phase1_Endpoint_Readout.md`  
- `05_Original_Claim_Assessment_Closeout.md`  
- `SHARE_PACK.md` · `EXECUTIVE_BRIEF.md`  
- `RESIDUAL_BRANCH_MENU.md` · `OPTIONAL_MODES_MENU.md`

### Failure-mode / tracker pointers (if any)

- LOCK-003 / 010: Amb drop ≠ clearance; brochure ¢ ≠ bar-met  
- LOCK-011: June SEP / prior statement ≠ Sep upper-bound change  
- Conflicted-source: trading venue cannot solely affirm P-NonNegligible  
- Unnamed class: `leave unnamed` ≠ unlikely  
- Print-match ≠ clearance (not fired as a hit; C1 failed affirmation)

---

*Generated under standing rule: Application Dissertation Deliverable. See `.cursor/rules/applications-gated-method.mdc`. Stubs ≠ hard stop.*
