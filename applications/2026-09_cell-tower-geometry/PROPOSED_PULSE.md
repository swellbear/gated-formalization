# First pulse — cheap data / measurement peek (PROPOSED; Operator-gated)

**Date:** 2026-09-05  
**Application:** `2026-09_cell-tower-geometry`  
**String:** Amb scaffold / awaiting admit  
**Named gap:** can a geometry / path-loss test even be posed from public traces + honest mast maps?  
**Ledger:** [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md)

Lab invents ranked peek probes. Lab does **not** self-admit. **Do not run** until Method Operator admit. After admit: laptop / CPU only. **Not a model.** Do **not** download big datasets into the repo. Do **not** train.

**What this is not:** A geometry locator. Training established. GPS replacement. MLS / OpenCelliD fingerprinting. Reopening BIA→weight. Rithm.

---

## 0. Plain-language framing

**What this is:** Three cheap checks that would tell us whether the locked claim is even measurable on the public record. Docs / schema / column peeks. No estimator.

**What this would settle (if admitted and run):** Whether public traces exist, whether the mast map can be honest about GPS lineage, and whether Timing Advance (or equivalent ranging) is present. **X** stays TBD until after that peek.

**What this is not:** Not a trained map. Not a reason to commit OpenCelliD / FCC dumps. Not GPS replacement. Not claim clearance.

---

## 1. Ranked probes (proposed)

| Rank | Probe | Why | Cost | Kill vs succeed |
|------|-------|-----|------|-----------------|
| 1 | **Trace peek** — name a public drive / walk source that already has phone-visible cell IDs, with GPS only as held-out eval labels. Record schema, license, and whether RSSI and/or TA columns exist. Docs / codebook only; no bulk dump. | Without traces, the claim cannot be scored. | Low (web / docs; laptop) | Kill = no usable public traces → **DATA-BLOCKED park**. Succeed = citable URL + schema + license with cell IDs + GPS eval labels (**not** claim clearance). |
| 2 | **Mast-source honesty** — compare what a regulatory list (e.g. FCC ASR) can actually supply vs OpenCelliD / MLS. Say plainly whether “no GPS in the map lineage” is testable, or whether the usable map is GPS-crowdsourced. | OpenCelliD / MLS positions are largely GPS-crowdsourced. That smuggles GPS into the map. | Low (docs / sample pages; laptop) | Kill = only crowdsourced maps are usable → lineage fog stays. Succeed = a regulatory list is usable **and** can be matched to the site heard (may still be sparse / messy). |
| 3 | **TA / ranging peek** — in the named traces (or their docs), does Timing Advance or an equivalent ranging field appear? If not, write a weaker RSSI+ID-only bar or record **fail closed**. | Without TA / multi-tower ranging, RSSI+cell-ID alone is weak. | Low (schema / column list) | Kill = TA missing **and** no honest weaker bar can be stated → **fail closed**. Succeed = TA present, **or** a weaker bar is written down for a later test. |

---

## 2. Hard NO (even after admit)

- Do **not** train a fingerprint model.
- Do **not** use GPS as a training feature or fingerprint target.
- Do **not** commit large binary datasets or trained weights.
- Do **not** claim GPS replacement (~2–5 m).
- Do **not** reopen the BIA→weight portfolio.

---

## 3. Unchanged strings

- BIA→weight portfolio remains **CLOSED** (human #59; animal parks stay).
- Collatz playground remains **done** (#45). Lab HOLD there.
- Track B invent remains **paused**.
- llm-gwt R-REPL remains **parked**.

---

*Docs only. Proposed ≠ admitted. Peek succeed ≠ claim clearance. Not a trained map. Not GPS replacement. Not rithm. Lab does not self-admit.*
