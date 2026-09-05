# Residual-Branch Menu — cell-tower geometry

**Open scaffold.** Offering ≠ running. This is **not** a closeout menu, **not** a trained map, and **not** a GPS-replacement claim.

**Date:** 2026-09-05  
**Application:** `2026-09_cell-tower-geometry`  
**Status:** Amb scaffold / awaiting admit  

**Glossary:** `docs/READER_GLOSSARY.md`  
**Ledger:** [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md)  
**Proposed pulse:** [`PROPOSED_PULSE.md`](PROPOSED_PULSE.md)

---

## 0. Plain-language framing

**What we’re doing:** Opening a new Amb. Lab proposes three cheap peeks for public traces, mast-map honesty, and Timing Advance. Method Operator admits, rejects, or parks.

**What we need from you:** Admit (or reject / park) this Amb and the ranked peeks. No peek is admitted yet. Lab HOLD.

**What this does *not* mean:** A geometry locator. Training started or established. GPS replacement. MLS / OpenCelliD fingerprinting. Auto-admit. Reopening BIA→weight. Reopening Track B. Reopening llm-gwt R-REPL. Reopening Collatz invent (#45 playground is done; Lab HOLD there).

---

## 1. Named leftover (this string)

| ID | One-line | Class | Disposition |
|----|----------|-------|-------------|
| geometry-pathloss-median-X | Public masts + cell IDs (optional RSSI / TA) → median error ≤ X m without fingerprint training | Definition-blocked until admit + **X** freeze; then empirically resolvable only after the peek | **open** — last check: none; **X** TBD; fail closed if no TA and RSSI+ID cannot clear a weaker bar |
| public-traces-cellid-gps-eval | Public traces with cell IDs + GPS eval labels (schema / license peek) | Empirically resolvable **after** Operator admits Rank 1 | **open** — last check: none; kill = DATA-BLOCKED; succeed = URL + schema + license |
| mast-lineage-honesty | FCC ASR vs OpenCelliD / MLS — is “no GPS in the map lineage” testable? | Empirically resolvable **after** Operator admits Rank 2 | **open** — last check: none |
| ta-or-equivalent-ranging | Timing Advance (or equivalent) present in public traces? | Empirically resolvable **after** Operator admits Rank 3 | **open** — last check: none; missing TA + no weaker bar → fail closed |

No other empirically resolvable residuals on this fold.

---

## 2. Other strings (stay paused / closed / done)

| String | Disposition | Note |
|--------|-------------|------|
| BIA→weight portfolio (`2026-09_human-bia-weight` + animal parks) | **CLOSED** (#59 KILL; #47/#49/#51 DATA-BLOCKED; #53 Soften) | Human ship demo stays method-practice only. This app does **not** reopen any BIA app |
| Collatz playground (`2026-09_collatz-shortcut-map`) | **done** (#45) | Playground invent complete; Lab HOLD there; **not** a proof. This app does **not** reopen it |
| Track B invent (oil spot) | **paused** | Unchanged; this app does **not** reopen it |
| llm-gwt R-REPL | **parked** | Unchanged; do not chase GPU / weights / keys |

---

## 3. Operator decision log

| Date | Action |
|------|--------|
| 2026-09-05 | Founder opens this string as a **new** Amb (not a BIA sequel). Lab proposing three cheap peeks. Method Operator gates. BIA→weight portfolio **CLOSED**. Collatz playground **done** (#45). Track B **paused**. llm-gwt R-REPL stays **parked**. Last check: none. Geometry location is **not** established. Training is **not** established. Not rithm. GPS replacement is **not** claimed. |

---

*Standing habit: [`docs/NAMED_GAP_LEDGER_HABIT.md`](../../docs/NAMED_GAP_LEDGER_HABIT.md). Invents that do not point at the ledger line do not run.*
