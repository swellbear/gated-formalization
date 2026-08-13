# Anchor & Claim-Type Template

**Date:** 2026-08-12  
**Domain / Source material:** Operator-pasted prediction-market resolution rules (verbatim); displayed brackets and market URL **not** in the paste  
**Application ID / short name:** `2026-08_fomc-sep-2026-uffr-change`

---

## L₀ — Objective Anchors

1. The FOMC sets a **target range** for the federal funds rate; that range has a published **upper bound**.  
2. This intake defines the market object as the **change in that upper bound**, in **basis points**, versus the level **prior to** the September 2026 FOMC meeting.  
3. The text names resolution sources: the FOMC **statement** after the meeting scheduled **September 15–16, 2026** (Fed calendar), and the Fed **openmarket** page.  
4. The paste includes a **round-up-to-nearest-25** rule for changes not in “displayed options,” and a **fallback**: no statement by the end of the **next** scheduled meeting → **“No change.”**  
5. **Displayed options were not in the original paste.** Operator later named `https://polymarket.com/event/fed-decision-in-september-762` (Rank 3 O2). Fetch 2026-08-12: five brackets (50+ dec / 25 dec / No change / 25 inc / 50+ inc).  
6. As of **2026-08-12**, the September 15–16 2026 FOMC statement **does not yet exist**.  
7. Related app `2026-08_fomc-june-2026-sep` is a **different** claim (June 17 SEP inventory). Funds-rate was **off** that F-ML bar. **No conclusion inheritance.**  
8. Rank 3 locked `Q3+O2+L1+M3+B1` (`Lock_Rank3_Q3O2L1M3B1.md`). D-OPTIONS and D-PRICE (conflicted page print) **admitted**. **P-NN-TEST:** P-NonNegligible **not established** on this vehicle. Operator **`leave unnamed`** (C2 unfilled) 2026-08-12.

---

## Candidate Claim or Layer Element

**Intake (verbatim — not rewritten as a slogan):**

The FED interest rates are defined in this market by the upper bound of the target federal funds range. The decisions on the target federal funds range are made by the Federal Open Market Committee (FOMC) meetings.

This market will resolve to the amount of basis points the upper bound of the target federal funds rate is changed by versus the level it was prior to the Federal Reserve's September 2026 meeting.

If the target federal funds rate is changed to a level not expressed in the displayed options, the change will be rounded up to the nearest 25 and will resolve to the relevant bracket. (e.g. if there's a cut/increase of 12.5 bps it will be considered to be 25 bps)

The resolution source for this market is the FOMC’s statement after its meeting scheduled for September 15-16, 2026 according to the official calendar: https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm.

The level and change of the target federal funds rate is also published at the official website of the Federal Reserve at https://www.federalreserve.gov/monetarypolicy/openmarket.htm.

This market may resolve as soon as the FOMC’s statement for their September meeting with relevant data is issued. If no statement is released by the end date of the next scheduled meeting, this market will resolve to the "No change" bracket.

**Not established:** any winning bracket; that the September meeting will cut/hike/hold; 67¢ as P-BaseCase; any bracket as P-NonNegligible **met**; June SEP medians as this path.

**Locked Rank 3:** Q3 Odds + O2 operator URL + L1 Sep statement as print source + M3 live-shot sizes + B1 pre-meeting in-force. Record: `Lock_Rank3_Q3O2L1M3B1.md`.

**Candidate / admitted units:**  
- **D-OPTIONS** — **admitted:** five displayed brackets on the named Polymarket event.  
- **D-PRICE** — **admitted** as conflicted page print of Yes ¢ at fetch (scenario presence / pitch curve, **not** bar-met).  
- **P-NN-TEST** — **admitted as evaluation:** P-NonNegligible **not established** on this vehicle. Independent class **unnamed** (`leave unnamed`).  
- **D-RULES** — contract text (page matches paste); not separately pulsed this cycle.  
- **F-PRINT** — parked until Sep 15–16 2026 FOMC statement.

---

## Pre-Classification (required)

- [ ] **Descriptive**
- [ ] **Normative / Strategic**
- [x] **Mixed** — split as follows:
  - Descriptive part: **D-OPTIONS** / **D-PRICE** — **admitted** (brackets + conflicted ¢ print). **D-RULES** — contract as written.  
  - Forecast / odds part: **Q3** vehicle locked; **M3 P-NonNegligible** locked as bar height; **P-NN-TEST not established**; independent class **`leave unnamed`**. **F-PRINT** park-until-statement.  
  - Normative/Strategic part: **none** in the paste (no should).

**Notes:** Do **not** convert 67¢ into “the FOMC will hold.” Do **not** import June SEP. Venue is named (operator URL); Kalshi/CME FedWatch remain **different classes**.

### Soft-modal fork

| Term in claim | Candidate bar (circle when locking) |
|---------------|-------------------------------------|
| “will resolve” (contract) | D-RULES census / not a modal forecast |
| implied “what prints” | P-Logical / P-NonNegligible / P-BaseCase / **park-until-statement (F-PRINT)** |
| Rank 3 published price | **M3 P-NonNegligible (LOCKED)** — live-shot sizes, not expected path. Bar locked ≠ bar met. |

**Near-vacuity warning:** P-Logical that *some* 25 bp-rounded change occurs is near-vacuous. M3 is locked; do **not** weaken it back to P-Logical. Conflicted market cannot be sole affirmation of a modal bar.

---

## Ready for Gate Scoring?

- [x] Yes — Cycle 0 of contract as intake; current Amb sheet `02_Gate_Scoring_Sheet_after_M3.md`.  
- [ ] No

**Stop (hard stop sealed):** P-NonNegligible **not established** (`leave unnamed` on C2). F-PRINT untested. Original wording kept. Optional modes offered, not run. **Amb ≠ clearance.** Leave-unnamed ≠ unlikely.
