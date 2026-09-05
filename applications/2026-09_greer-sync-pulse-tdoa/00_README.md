# Greer-style sync-pulse TDOA — reading guide

**Application ID:** `2026-09_greer-sync-pulse-tdoa`  
**Opened:** 2026-09-05  

Open **Amb scaffold**. Founder **CLAIM LOCK** recorded. First pulse is **after** Method Operator admit — **not this fold**.

**NEW Amb:** Greer-style GPS-denied locate via dedicated sync-pulse reference nodes + mobile TDOA (contrast prior art [US10135667B1](https://patents.google.com/patent/US10135667B1/en) — method practice / explore the idea; **not** copy claims for product).

This is **not** a locator. This is **not** a trained map. Training is **not** established. This is **not** RF fingerprinting. This is **not** GPS / DGPS as the mobile fix. This is **not** skill-met. This is **not** rithm. This is **not** a product claim copied from the named patent. Opening the scaffold does **not** show a TDOA fix and is **not** clearance. Proposed first-pulse checks are **not** admitted yet. Lab **HOLD** until Method Operator admit of the first pulse.

The cell-tower Amb (`2026-09_cell-tower-geometry`) is **PARKED** and is **not** reopened as live. The BIA→weight portfolio is **CLOSED**. This app does **not** reopen either.

## Claim (Founder lock — replace any prior draft wording)

On a laptop-feasible sim/prototype path, a ≥3-reference simultaneous-sync TDOA estimator (GPS/DGPS used only to place/time refs; never as the mobile fix) can recover mobile position with median error ≤ **X** on a held-out path inside a GPS-denied box — **without RF fingerprint training**.

**X:** TBD after first cheap peek (sim geometry vs hardware).

## Intent / reverse framing

Not opportunistic cellular fingerprinting. Not GPS-crowdsourced mast maps. Not using GPS/DGPS as the phone / mobile fix. This Amb asks whether dedicated synchronized reference nodes plus mobile TDOA can place a receiver inside a GPS-denied box on a laptop-feasible sim/prototype path.

**Prior-art contrast (bibliographic only):** US10135667B1, Kerry L. Greer, *System and method for increased indoor position tracking accuracy* (2018). Named so the idea can be practiced / explored under this method. **Do not** copy patent claims for a product. **Do not** paste claim language into this folder.

## Honest fog (named; not cleared)

1. **Spectrum / hardware vs sim-only.** A laptop-feasible path may stay sim/prototype. Licensed spectrum or dedicated radios may be required before a hardware **X** can be posed. That is fog, not a free ride.
2. **Clock resolution.** Simultaneous-sync TDOA lives or dies on clock / sync assumptions. Resolution is unnamed until the first peek.
3. **Multipath.** A GPS-denied box is a hard radio environment. Multipath can break a clean ≥3-ref geometry story.

## Eval rules (if later admitted)

- GPS / DGPS, if used at all, **place and time the reference nodes only**. They are **never** the mobile fix.
- Estimator class is ≥3-reference **simultaneous-sync TDOA**. **No** RF fingerprint training.
- Path must stay **laptop-feasible** sim/prototype unless a later gate says otherwise.
- Metric: median error on a held-out path inside a GPS-denied box. **X** stays TBD until after the first cheap peek (sim geometry vs hardware).
- This is **not** a fingerprinting claim and **not** a patent-product claim.

## Next pulse (proposed; after admit; not this fold)

After Method Operator **admit**, first pulse = **name fog** + **2–3 cheap checks** (public refs, sync assumptions, measurement availability). Laptop/CPU only. **Not a model.** See [`PROPOSED_PULSE.md`](PROPOSED_PULSE.md).

## Reading order

1. [`STATUS.md`](STATUS.md) — where we are
2. [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md) — the open lines
3. [`PROPOSED_PULSE.md`](PROPOSED_PULSE.md) — Lab’s cheap checks (awaiting admit)
4. [`DIGESTION_FROM_CELL_TOWER.md`](DIGESTION_FROM_CELL_TOWER.md) — what the last string taught
5. [`RESIDUAL_BRANCH_MENU.md`](RESIDUAL_BRANCH_MENU.md) — decision log
6. [`notes.md`](notes.md) — one-line pointer
