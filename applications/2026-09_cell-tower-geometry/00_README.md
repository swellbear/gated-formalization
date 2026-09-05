# Cell-tower geometry — reading guide

**Application ID:** `2026-09_cell-tower-geometry`  
**Opened:** 2026-09-05  

**PARKED** 2026-09-05 (Founder STOP / user pivot). Cheap checks A→B **halted mid-flight**. Peek #61 + provisional **X = 300 m** remain **on record**. The Amb is **not live**.

Separate Amb (on record, not live): can a phone’s location be recovered from **public mast maps + radio observations** by geometry / path-loss — **without** training on GPS-labeled fingerprints? Peek1 **PASS**. Peek2 **MIXED** (CID↔ASRN join **PARKED**). Peek3 **PASS**. Provisional **X = 300 m** urban median, with TA + non-fog masts.

This is **not** a trained map. Training is **not** established. This is **not** GPS replacement. This is **not** MLS / OpenCelliD fingerprinting. This is **not** skill-met. This is **not** rithm. Peek succeed is **not** claim clearance. The BIA→weight Amb portfolio is **CLOSED**. This app does **not** reopen it. Do **not** reopen this Amb as live. Successor (separate folder, not this Amb): [`../2026-09_greer-sync-pulse-tdoa/`](../2026-09_greer-sync-pulse-tdoa/). Lab **HOLD**.

## Claim (locked wording)

From public mast coordinates + phone-visible cell IDs (and optional RSSI / Timing Advance), a pure geometry / path-loss estimator can hit median error ≤ **300 m** on held-out drives — **without training on GPS-labeled fingerprints**.

**X:** **300 m** urban median (provisional). Soften/Kill if the live pack is RSSI-only or fog-as-honesty (OpenCelliD / MLS as the mast map). Fail closed does **not** fire on TA absence — TA is present in Edinburgh / Vienna / DoNext.

## Intent / reverse framing

Not the usual MLS / OpenCelliD path (GPS drives → fingerprint DB → cell→location). This Amb asks whether location is recoverable from **public mast maps + radio observations** via geometry / path-loss, without fingerprint training. Evaluation may use GPS only as held-out ground truth labels for scoring — never as training features or fingerprint targets.

## Honest fog (named)

1. OpenCelliD / Mozilla Location Service mast positions are GPS-crowdsourced fog — **ablation only**. Prefer regulatory lists (FCC ASR `r_tower.zip` structure lat/lon; Austrian Senderkataster). ASR has **no CID** — CID↔ASRN join **PARKED** (no crowdsourced GPS join). US ASR **Soften** until that join is honesty-cleared. **EU packs first.**
2. Ceiling is coarse location / GPS-fallback territory, not GPS replacement (~2–5 m). Rural sparse towers → huge uncertainty.
3. TA is present in the EU primary packs. RSSI-only (Malaysia GNetTrack) stays Soften — do not silently keep the 300 m bar on an RSSI-only pack.

## Eval rules (locked at peek)

- GPS labels are **held-out scoring only**. They are not training features and not fingerprint targets.
- Estimator class is geometry / path-loss from mast coordinates + radio observations (cell ID, optional RSSI / TA). **No** GPS-labeled fingerprint training.
- Metric: median error in meters on held-out drives. Provisional bar: **X = 300 m** urban median, with TA + non-fog masts.
- Soften/Kill **X** if RSSI-only or fog-as-honesty.
- This is **not** a GPS-replacement claim.

## Next pulse (halted)

Cheap checks A→B **halted mid-flight**. Do **not** invent estimators in this folder. Peek #61 facts stay in [`PROPOSED_PULSE.md`](PROPOSED_PULSE.md).

## Reading order

1. [`STATUS.md`](STATUS.md) — where we are (**PARKED**; not live)
2. [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md) — the parked / on-record lines
3. [`DIGESTION_PARK.md`](DIGESTION_PARK.md) — Founder STOP / user pivot
4. [`PROPOSED_PULSE.md`](PROPOSED_PULSE.md) — peek #61 on record (A→B halted)
5. [`DIGESTION_FIRST_PULSE.md`](DIGESTION_FIRST_PULSE.md) — what the peek taught
6. [`DIGESTION_FROM_BIA.md`](DIGESTION_FROM_BIA.md) — what the last string taught
7. [`RESIDUAL_BRANCH_MENU.md`](RESIDUAL_BRANCH_MENU.md) — decision log
8. [`notes.md`](notes.md) — one-line pointer
