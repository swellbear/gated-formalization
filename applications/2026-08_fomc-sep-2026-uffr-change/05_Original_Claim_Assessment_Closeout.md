# Original-Claim Assessment (Closeout)

**Date:** 2026-08-12  
**Application:** `2026-08_fomc-sep-2026-uffr-change`  
**Closeout verdict:** **Stable Provisional (hard stop)**  
**Amb at closeout:** **2.5**

**Amb ≠ clearance (mandatory):** Amb measures under-specification. Amb 2.5 does **not** mean the original contract is a cleared forecast, or that P-NonNegligible is established or refuted.  
**Locked bar status (if any):** P-NonNegligible (live-shot sizes) — **not established** (C1 P-NN-TEST executed, conflicted sole source; independent class **unnamed**, `leave unnamed`). P-BaseCase — **not the locked bar**. F-PRINT — **untested** (statement does not exist yet).

**Original claim (verbatim):**  
The FED interest rates are defined in this market by the upper bound of the target federal funds range. The decisions on the target federal funds range are made by the Federal Open Market Committee (FOMC) meetings.

This market will resolve to the amount of basis points the upper bound of the target federal funds rate is changed by versus the level it was prior to the Federal Reserve's September 2026 meeting.

If the target federal funds rate is changed to a level not expressed in the displayed options, the change will be rounded up to the nearest 25 and will resolve to the relevant bracket. (e.g. if there's a cut/increase of 12.5 bps it will be considered to be 25 bps)

The resolution source for this market is the FOMC’s statement after its meeting scheduled for September 15-16, 2026 according to the official calendar: https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm.

The level and change of the target federal funds rate is also published at the official website of the Federal Reserve at https://www.federalreserve.gov/monetarypolicy/openmarket.htm.

This market may resolve as soon as the FOMC’s statement for their September meeting with relevant data is issued. If no statement is released by the end date of the next scheduled meeting, this market will resolve to the "No change" bracket.

---

## 1. Status of the original claim

### Constrained (include scope if scoped)
| Content | Scope (unrestricted / under package __) |
|---------|----------------------------------------|
| Object = change in the **upper bound** of the target funds range vs pre-September 2026 meeting, in bp | Under Rank 3 + L₀ |
| Live print source = FOMC statement after Sep 15–16 2026 (not this page; not June SEP) | Under Rank 3 L1 |
| Baseline = upper bound in force immediately before that meeting | Under Rank 3 B1 |
| Displayed brackets = 50+ dec / 25 dec / No change / 25 inc / 50+ inc | Under Rank 3 O2 (**D-OPTIONS**) |
| Page Yes ¢ at fetch 2026-08-12: 0.6 / 1.1 / 67 / 33 / 0.5 (conflicted print) | Under Rank 3 Q3 (**D-PRICE** — pitch curve, not bar-met) |
| Published prices read as **live-shot sizes**, not the expected path | Under Rank 3 M3 (bar **height** only) |
| Round-up-to-25 and fallback-No-change recorded as contract schema | L₀ / G6 draft-in-use |

### Negatively constrained / false as originally stated
| Original strong language | Status |
|--------------------------|--------|
| “Will resolve” as a filled-in winning bracket today | **Not** a forecast finding — contract language; F-PRINT untested |
| 67¢ = expected path (P-BaseCase) | **Not the locked bar** (M3). Not established as expected path |
| Any bracket **is** a live shot (P-NonNegligible met) | **Not established** (C1 conflicted; C2 unnamed). **Not a refute** |
| June SEP medians as this path | **Excluded** (different object; funds-rate was off that F-ML bar) |
| This Polymarket page as the September statement | **Excluded** (L1) |

### Free parameters remaining
| ID | Status / freeze |
|----|-----------------|
| [R-P-NN](RESIDUAL_BRANCH_MENU.md#r-p-nn) | Independent P-NN affirmation **unnamed**. `park-until-trigger`: `name source class C2`. C1 does not fire as sole affirmation |
| [R-F-PRINT](RESIDUAL_BRANCH_MENU.md#r-f-print) | Sep upper-bound **change** untested. `park-until-trigger`: Sep 15–16 2026 FOMC statement (or fallback clock) |

### Forced-deviation terms (if extraction was triggered)
None. Ranks 1 and 2 were **Minimal deviation**. Rank 3 (chosen) is Moderate (odds fork) but FD extraction requires every realistic package Moderate+.

### Strong language still unsupported
Any claim that the FOMC will hold, hike, or cut; that 33¢ **is** a live shot; that 67¢ is the expected path. Rank 3 added an odds reading not in the paste; that reading’s bar was **not met**.

**Scoped vs unrestricted:** Scoped findings are **not** unrestricted support for a rate call. D-PRICE does not answer who wins. Leave-unnamed does not mean “unlikely.”

---

## 2. Continuation options

| Option | Expected buy | Still leaves open |
|--------|--------------|-------------------|
| `name source class C2: …` matching Rank 3 | Named-class pulse of P-NonNegligible on an independent series | Establishment-stop if honest `04` would say established |
| Wait for Sep 15–16 2026 statement ([R-F-PRINT](RESIDUAL_BRANCH_MENU.md#r-f-print)) | Print census of the change | Does not retroactively meet M3 from ¢ |
| `run CR` / successor (print-only or different venue) | Different question, labeled | Rank 3 leftover unchanged |
| `run UX` / `run CX` | Documentation / alternatives | Parent verdict unchanged |
| Leave parked | None | P-NN stays not established; F-PRINT untested |

---

## 3. Revision vs continuation fork

Original paste is **resolution rules**, not a slogan that a bracket will win. Rank 3’s odds fork is Moderate deviation; CR is **offered**, not required. Default: **keep original wording** (the pasted rules).

- [ ] **Revise claim** — then run **Claim-Revision Scaffolding** before a successor  
- [x] **Keep original wording** — research agenda / scoped dependents only (default; CR offered, not run)

**Default if no further authorization:** keep original wording + hard stop with agenda / this assessment.

---

## Closeout statement

Application **closed** as **Stable Provisional (hard stop)**. Original contract **not** silently converted into a rate call. P-NonNegligible **not established**. F-PRINT **untested**. D-OPTIONS / D-PRICE admitted. Awaiting further authorization only if continuing (`name source class C2`, statement trigger, or optional modes).

---

*Required at closeout under standing rule. See `.cursor/rules/applications-gated-method.mdc`.*
