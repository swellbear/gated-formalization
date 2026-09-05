# First pulse — cheap data / measurement peek (Operator-gated)

**Date:** 2026-09-05  
**Application:** `2026-09_cell-tower-geometry`  
**String:** first-pulse peek **ADMITTED**  
**Named gap:** can a geometry / path-loss test even be posed from public traces + honest mast maps?  
**Ledger:** [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md)  
**Digestion:** [`DIGESTION_FIRST_PULSE.md`](DIGESTION_FIRST_PULSE.md)

Lab invented ranked peek probes. Lab does **not** self-admit. Lab scratch was **not** readable on this fold VM. Record below is the gated fact set copied from the Method Operator gate (honest docs / schema / license peek; no bulk dump; no estimator).

**What this is not:** A geometry locator. Claim clearance. Training established. GPS replacement. MLS / OpenCelliD fingerprinting. Reopening BIA→weight. Rithm. Estimator invent (not this fold).

---

## 0. Plain-language framing

**What this is:** Three cheap checks that ask whether the locked claim is even measurable on the public record. Docs / schema / column peeks. No estimator.

**What this settles (gated):** Public traces with cell IDs + GPS eval labels **exist**. Regulatory mast lists are the honest map; OpenCelliD / MLS stay fog (ablation only). Timing Advance is present in the EU primary packs — **not** fail-closed. Provisional **X = 300 m**. Peek succeed is **not** claim clearance.

**What this is not:** Not a trained map. Not a reason to commit OpenCelliD / FCC dumps. Not GPS replacement. Not claim clearance. Not invent of a locator.

---

## 1. Lab peek (copied from the gate)

**Target:** public traces with phone-visible cell IDs (+ optional RSSI / TA) and GPS only as held-out eval labels; a mast map whose lineage is not GPS-crowdsourced; whether TA (or equivalent ranging) is present.

**Result (gated):**

| Peek | Result |
|------|--------|
| 1 — Trace peek | **PASS** — public traces with cell IDs + GPS eval labels exist |
| 2 — Mast-source honesty | **MIXED** — prefer regulatory masts; OpenCelliD / MLS = fog (ablation only); CID↔ASRN join **PARKED** |
| 3 — TA / ranging peek | **PASS** — TA present in Edinburgh / Vienna / DoNext; **not** fail-closed on TA absence |

Peek succeed ≠ claim clearance. Soften rows below are **docs only**.

---

## 2. Peek1 — traces (PASS)

| # | Cite | What is there | Gate |
|---|------|---------------|------|
| 1 | Vienna LTE / 5G traces — Zenodo concept [DOI 10.5281/zenodo.18322065](https://doi.org/10.5281/zenodo.18322065); **CC-BY 4.0**; `timing_advance` | Public drive / walk traces with cell IDs + GPS eval labels + TA | **Primary.** **ADMIT PASS.** |
| 2 | DoNext Dortmund — [DOI 10.17877/tudodata-2026-t6mypo](https://doi.org/10.17877/tudodata-2026-t6mypo); **CC-BY 4.0**; `ta` | Public traces with cell IDs + GPS eval labels + TA | **Primary.** **ADMIT PASS.** |
| 3 | Edinburgh Melrose MNRUL (~102k); `ta`; research / non-commercial | Large public-ish pack with TA | **Soften secondary** — license is research/non-commercial, not a substitute for the CC-BY primaries |
| 4 | Malaysia GNetTrack | Cell IDs + GPS + RSSI; **no TA documented** | **Soften / RSSI-only** — not a primary; Soften/Kill if this were the live pack |

This fold does **not** download or commit the packs.

---

## 3. Peek2 — mast-source honesty (MIXED)

| Source | What it can supply | Gate |
|--------|--------------------|------|
| FCC ASR `r_tower.zip` | Structure lat / lon (regulatory) | **Prefer.** Usable structure coordinates. **No CID.** |
| Austrian Senderkataster | Regulatory mast list | **Prefer** (EU geography). |
| OpenCelliD / MLS | GPS-crowdsourced cell→location fog | **Ablation only.** Do **not** treat as honesty for “no GPS in the map lineage.” |

**Named leftover:** ASR has **no CID**. **CID↔ASRN join PARKED** — do **not** close it with a crowdsourced GPS join.

**Geography:** **EU packs first.** US ASR stays **Soften** until the join is honesty-cleared.

---

## 4. Peek3 — TA / ranging (PASS)

TA (or documented equivalent) is present in **Edinburgh / Vienna / DoNext**. The fail-closed limb (“TA missing **and** no honest weaker bar”) does **not** fire.

RSSI-only (Malaysia GNetTrack) stays **Soften**. If a later pack is RSSI-only, Soften/Kill the 300 m bar — do **not** silently keep **X = 300 m**.

---

## 5. Operator gate (authoritative)

**Peek1 PASS.** Public traces with cell IDs + GPS eval labels exist.  
Primary: Vienna (Zenodo CC-BY 4.0, `timing_advance`) + DoNext Dortmund (CC-BY 4.0, `ta`) — DOI 10.5281/zenodo.18322065 concept; DoNext 10.17877/tudodata-2026-t6mypo.  
Soften secondary: Edinburgh Melrose MNRUL (~102k, `ta`) — research/non-commercial.  
Soften/RSSI-only: Malaysia GNetTrack (no TA documented).

**Peek2 MIXED.** Prefer regulatory masts (FCC ASR `r_tower.zip` structure lat/lon; Austrian Senderkataster). OpenCelliD/MLS = GPS-crowdsourced fog (ablation only). Gap: ASR has no CID — CID↔ASRN join **PARKED** (no crowdsourced GPS join).

**Peek3 PASS.** TA present in Edinburgh/Vienna/DoNext — not fail-closed on TA absence.

**Provisional X locked:** **300 m** urban median error bar, with TA + non-fog masts. Soften/Kill if RSSI-only or fog-as-honesty.

**Eval protocol locked:** GPS = held-out eval labels only; no fingerprint/radio-map training.

**Geography:** EU packs first; US ASR Soften until join honesty-cleared.

**Next (not this fold):** invent 2–3 ranked pure geometry/path-loss estimators — **no invent in this fold**.

**BIA→weight stays CLOSED.**

**Hard NO**

- Do **not** train a fingerprint / radio-map model.
- Do **not** use GPS as a training feature or fingerprint target.
- Do **not** commit large binary datasets or trained weights.
- Do **not** claim GPS replacement (~2–5 m).
- Do **not** treat OpenCelliD / MLS as the honest mast map.
- Do **not** close CID↔ASRN with a crowdsourced GPS join.
- Do **not** invent estimators on this fold.
- Do **not** write skill-met / elevated language.
- Do **not** reopen the BIA→weight portfolio.

---

## 6. Unchanged strings

- BIA→weight portfolio remains **CLOSED** (human #59; animal parks stay).
- Collatz playground remains **done** (#45). Lab HOLD there.
- Track B invent remains **paused**.
- llm-gwt R-REPL remains **parked**.

---

*Docs only. Peek succeed ≠ claim clearance. Provisional X ≠ a scored locator. Not a trained map. Not GPS replacement. Not rithm. Lab does not self-admit. Lab scratch was not on this VM; summary copied from the Operator gate.*
