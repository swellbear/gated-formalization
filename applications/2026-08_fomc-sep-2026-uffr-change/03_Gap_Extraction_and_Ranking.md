# Gap Extraction & Ranking Sheet

**Date:** 2026-08-12  
**Parent application / claim:** `2026-08_fomc-sep-2026-uffr-change`  
**Linked Gate Scoring Sheet:** `02_Gate_Scoring_Sheet.md` (Cycle 0) · `02_Gate_Scoring_Sheet_after_Rank3_incomplete.md` · `02_Gate_Scoring_Sheet_after_M3.md` (Amb 2.5)

---

## Identified Gaps (Free Parameters)

### Gap 1 — Speech act
**Description:** Census the resolution **contract**, forecast the September **print**, or treat a **market price** as an odds bar.

**Claim-freeze:** **LOCKED Rank 3 Q3** — named market’s published price is the odds vehicle. F-PRINT remains a separate leftover.

**Impact:** 2 · **Anchor:** 2 · **Measurability:** 2 · **Sum:** 6

### Gap 2 — Displayed options / market identity
**Description:** Brackets and venue URL are not in the paste. Rounding-to-nearest-25 is undefined without the displayed set, except as a rule-schema.

**Claim-freeze:** **LOCKED Rank 3 O2** — five brackets on `fed-decision-in-september-762` (fetch 2026-08-12).

**Impact:** 2 · **Anchor:** 1 · **Measurability:** 2 · **Sum:** 5

### Gap 3 — Baseline “prior to September meeting”
**Description:** Which published upper bound counts as the pre-meeting level (last statement before Sep 15–16 vs openmarket.htm snapshot).

**Claim-freeze:** **LOCKED Rank 3 B1** — upper bound in force immediately before the Sep 15–16 2026 meeting.

**Impact:** 1 · **Anchor:** 2 · **Measurability:** 2 · **Sum:** 5

### Gap 4 — Live vs stand-in
**Description:** September FOMC statement vs openmarket.htm vs calendar vs this paste as the live vehicle.

**Claim-freeze:** **LOCKED Rank 3 L1** — FOMC statement after the Sep 15–16 2026 meeting. This page is not the print.

**Impact:** 2 · **Anchor:** 2 · **Measurability:** 2 · **Sum:** 6

### Gap 5 — Forecast modal / wait
**Description:** If F-PRINT is under test now, which bar: expected path, live shot, or park until the statement exists.

**Claim-freeze:** **LOCKED Rank 3 M3** — prices = live-shot sizes, not expected path. **P-NN-TEST not established** on Polymarket. Independent class **`leave unnamed`**. F-PRINT remains park-until-statement.

**Impact:** 2 · **Anchor:** 1 · **Measurability:** 2 · **Sum:** 5

### Gap 6 — Fallback clock
**Description:** “End date of the next scheduled meeting” if no September statement.

**Claim-freeze (draft-in-use):** No relevant statement by the end date of the **next** scheduled FOMC meeting after Sep 15–16 2026 → **No change**.

**Impact:** 1 · **Anchor:** 2 · **Measurability:** 2 · **Sum:** 5

---

## Claim-freeze register (quote before later pulses)

| Gap ID | One-sentence freeze lock |
|--------|--------------------------|
| G1 | **LOCKED Rank 3 Q3:** Named market’s published price is the odds **vehicle** for the same upper-bound-change event. |
| G2 | **LOCKED Rank 3 O2:** Displayed options = five brackets on `fed-decision-in-september-762` (fetch 2026-08-12). |
| G3 | **LOCKED Rank 3 B1:** Baseline = upper bound in force immediately before the Sep 15–16 2026 meeting. |
| G4 | **LOCKED Rank 3 L1:** Live F-PRINT = FOMC statement after that meeting (not this page; not June SEP). |
| G5 | **LOCKED Rank 3 M3:** Prices = live-shot sizes, not expected path. Bar locked ≠ bar met. **P-NN-TEST** not established on C1. Independent class **unnamed** (`leave unnamed` 2026-08-12). F-PRINT remains park-until-statement. |
| G6 | *(draft-in-use)* No statement by end of next scheduled meeting → No change (page = paste). |

*Later candidates must quote the freeze line. Changing a freeze line is a claim change, not progress. M3 locked ≠ live shot met.*

---

## Priority Order

1. Gap 1 — Speech act (dominant)  
2. Gap 4 — Live vs stand-in  
3. Gap 2 — Displayed options / market identity  
4. Gap 5 — Forecast modal / wait  
5. Gap 3 — Baseline  
6. Gap 6 — Fallback (draft-already-in-use candidate)

**Rectification (Phase 1 endpoint + closeout):** operator selected Rank 3 + named URL, then **M3**, then **`leave unnamed`**, then **`closeout`**. Hard stop sealed. G1–G5 locked. D-OPTIONS + D-PRICE admitted. P-NN-TEST **not established**. C2 unfilled. F-PRINT parked.

---

## Search Plan

**Targeted gap:** None runnable now. Independent class **unnamed** (`leave unnamed`). F-PRINT waits on L1 statement.  
**Source classes:** C1 Polymarket **REJECT** as sole affirmation. C2 not filled. Do **not** invent Kalshi/CME FedWatch as this class. Do **not** import June SEP.  
**Notes:** Reopen P-NN only with `name source class C2: …`. F-PRINT trigger = Sep 15–16 2026 statement (or fallback clock).

---

## Ready for Material Search & Admission Checks?

- [x] D-OPTIONS / D-PRICE — done (`04_Material_Admission_D_OPTIONS_D_PRICE.md`)  
- [x] Odds bar on C1 — done (`04_Material_Admission_P_NonNegligible.md`); **not established**  
- [x] Odds bar on C2 — **stopped** (`leave unnamed`)  
- [ ] F-PRINT — parked until Sep statement
