# Residual-Branch Menu — cell-tower geometry

**Open scaffold.** Offering ≠ running. This is **not** a closeout menu, **not** a trained map, and **not** a GPS-replacement claim.

**Date:** 2026-09-05  
**Application:** `2026-09_cell-tower-geometry`  
**Status:** first-pulse peek **ADMITTED**; provisional **X = 300 m**; CID↔ASRN join **PARKED**  

**Glossary:** `docs/READER_GLOSSARY.md`  
**Ledger:** [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md)  
**Peek + gate:** [`PROPOSED_PULSE.md`](PROPOSED_PULSE.md)  
**Peek digestion:** [`DIGESTION_FIRST_PULSE.md`](DIGESTION_FIRST_PULSE.md)

---

## 0. Plain-language framing

**What we’re doing:** Recording the Method Operator gate on the first-pulse peek. Public traces exist. Regulatory masts are preferred. TA is present. **X = 300 m** is provisional. Peek succeed is **not** claim clearance.

**What we need from you:** **none for this peek.** Lab HOLD on invent. Next pulse (not this fold) = invent 2–3 ranked pure geometry / path-loss estimators under Operator.

**What this does *not* mean:** A geometry locator. Training started or established. GPS replacement. MLS / OpenCelliD fingerprinting. Claim clearance. Skill-met. Reopening BIA→weight. Reopening Track B. Reopening llm-gwt R-REPL. Reopening Collatz invent (#45 playground is done; Lab HOLD there).

---

## 1. Named leftover (this string)

| ID | One-line | Class | Disposition |
|----|----------|-------|-------------|
| geometry-pathloss-median-X | Public masts + cell IDs (optional RSSI / TA) → median error ≤ **300 m** without fingerprint training | Empirically resolvable **after** estimator invent; **X** provisional | **open** — last check: 2026-09-05 Operator **ADMIT** provisional **X = 300 m** (urban median; TA + non-fog masts); Soften/Kill if RSSI-only or fog-as-honesty; peek succeed ≠ claim clearance |
| public-traces-cellid-gps-eval | Public traces with cell IDs + GPS eval labels (schema / license peek) | Peek settled | **killed** / **PASS** — last check: 2026-09-05 Peek1 **PASS**; primary Vienna + DoNext (CC-BY 4.0, TA); Edinburgh Soften secondary; Malaysia Soften/RSSI-only |
| mast-lineage-honesty | Regulatory masts vs OpenCelliD / MLS — is “no GPS in the map lineage” testable? | Peek restated **MIXED** | **restated** / **MIXED** — last check: 2026-09-05 prefer FCC ASR + Austrian Senderkataster; OpenCelliD / MLS ablation only |
| cid-asrn-join | Non-crowdsourced CID ↔ ASR / Senderkataster match | Parked — ASR has no CID | **paused** / **PARKED** — last check: 2026-09-05; **no** crowdsourced GPS join |
| us-asr-geography | US ASR on the same bar as EU packs | Soften until join honesty-cleared | **paused** / **Soften** — last check: 2026-09-05; **EU packs first** |
| ta-or-equivalent-ranging | Timing Advance (or equivalent) present in public traces? | Peek settled | **hardened** — last check: 2026-09-05 Peek3 **PASS**; TA in Edinburgh / Vienna / DoNext; **not** fail-closed |
| ranked-geometry-estimators | 2–3 ranked pure geometry / path-loss estimators on the admitted EU packs | Empirically resolvable **after** Operator admits the next pulse | **open** / **awaiting next pulse** — **not this fold**; Lab does **not** invent here |

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
| 2026-09-05 | Method Operator **ADMIT** first-pulse peek. **Peek1 PASS** — primary Vienna (Zenodo CC-BY 4.0, `timing_advance`; concept [DOI 10.5281/zenodo.18322065](https://doi.org/10.5281/zenodo.18322065)) + DoNext Dortmund (CC-BY 4.0, `ta`; [DOI 10.17877/tudodata-2026-t6mypo](https://doi.org/10.17877/tudodata-2026-t6mypo)); Soften secondary Edinburgh Melrose MNRUL (~102k, `ta`, research/non-commercial); Soften/RSSI-only Malaysia GNetTrack (no TA documented). **Peek2 MIXED** — prefer FCC ASR `r_tower.zip` structure lat/lon + Austrian Senderkataster; OpenCelliD/MLS = GPS-crowdsourced fog (ablation only); CID↔ASRN join **PARKED** (no crowdsourced GPS join); US ASR **Soften**; EU packs first. **Peek3 PASS** — TA in Edinburgh/Vienna/DoNext; not fail-closed. Provisional **X = 300 m** urban median (TA + non-fog masts); Soften/Kill if RSSI-only or fog-as-honesty. Eval protocol locked: GPS = held-out eval labels only; no fingerprint/radio-map training. Next (not this fold): invent 2–3 ranked pure geometry/path-loss estimators. BIA→weight stays **CLOSED**. Lab scratch not on this VM; peek summary copied from the Operator gate into [`PROPOSED_PULSE.md`](PROPOSED_PULSE.md). Peek succeed ≠ claim clearance. Geometry location is **not** established. Training is **not** established. Not rithm. GPS replacement is **not** claimed. |

---

*Standing habit: [`docs/NAMED_GAP_LEDGER_HABIT.md`](../../docs/NAMED_GAP_LEDGER_HABIT.md). Invents that do not point at the ledger line do not run.*
