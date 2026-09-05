# Cell-tower geometry — reading guide

**Application ID:** `2026-09_cell-tower-geometry`  
**Opened:** 2026-09-05  

Open **Amb scaffold / awaiting admit**. Separate Amb: can a phone’s location be recovered from **public mast maps + radio observations** by geometry / path-loss — **without** training on GPS-labeled fingerprints?

This is **not** a trained map. Training is **not** established. This is **not** GPS replacement. This is **not** MLS / OpenCelliD fingerprinting. This is **not** rithm. The BIA→weight Amb portfolio is **CLOSED** (human ship demo + kill of the accurate-weight claim). This app does **not** reopen it. Proposed first-pulse checks are **not** admitted yet. Lab **HOLD** until Method Operator admit.

## Claim (locked wording)

From public mast coordinates + phone-visible cell IDs (and optional RSSI / Timing Advance), a pure geometry / path-loss estimator can hit median error ≤ X meters on held-out drives — **without training on GPS-labeled fingerprints**.

**X:** TBD after first public-trace peek. Non-heroic urban bar likely 100–500 m median. Fail closed if Timing Advance (or equivalent ranging) is unavailable in public traces and RSSI+ID alone cannot clear a stated weaker bar.

## Intent / reverse framing

Not the usual MLS / OpenCelliD path (GPS drives → fingerprint DB → cell→location). This Amb asks whether location is recoverable from **public mast maps + radio observations** via geometry / path-loss, without fingerprint training. Evaluation may use GPS only as held-out ground truth labels for scoring — never as training features or fingerprint targets.

## Honest fog (named)

1. OpenCelliD / Mozilla Location Service mast positions are largely GPS-crowdsourced — testing “no GPS in the map lineage” pushes toward regulatory lists (e.g. FCC ASR), which are sparser/messier and may not match the radio site heard.
2. Ceiling is coarse location / GPS-fallback territory, not GPS replacement (~2–5 m). Rural sparse towers → huge uncertainty.
3. Without TA / multi-tower ranging, RSSI+cell-ID alone is weak.

## Eval rules (if later admitted)

- GPS labels are **held-out scoring only**. They are not training features and not fingerprint targets.
- Estimator class is geometry / path-loss from mast coordinates + radio observations (cell ID, optional RSSI / TA). **No** GPS-labeled fingerprint training.
- Metric: median error in meters on held-out drives. **X** stays TBD until after the first public-trace peek.
- Fail closed if TA (or equivalent ranging) is missing **and** RSSI+ID alone cannot clear a stated weaker bar.
- This is **not** a GPS-replacement claim.

## Next pulse (proposed; not admitted)

After Method Operator **admit**, first pulse = cheap data / measurement peek on laptop/CPU only. **Not a model.** Three targeted checks: public traces with cell IDs + GPS eval labels; mast-source honesty (FCC ASR vs OpenCelliD); whether TA exists. See [`PROPOSED_PULSE.md`](PROPOSED_PULSE.md).

## Reading order

1. [`STATUS.md`](STATUS.md) — where we are
2. [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md) — the open lines
3. [`PROPOSED_PULSE.md`](PROPOSED_PULSE.md) — Lab’s 3 checks (awaiting admit)
4. [`DIGESTION_FROM_BIA.md`](DIGESTION_FROM_BIA.md) — what the last string taught
5. [`RESIDUAL_BRANCH_MENU.md`](RESIDUAL_BRANCH_MENU.md) — decision log
6. [`notes.md`](notes.md) — one-line pointer
