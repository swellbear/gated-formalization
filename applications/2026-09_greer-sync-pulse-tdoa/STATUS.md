# STATUS — Operator “where am I?”

**Update every cycle.** Keep short. Full narrative stays in notes / worksheets.  
**Glossary:** `docs/READER_GLOSSARY.md`

**Application:** `2026-09_greer-sync-pulse-tdoa`  
**Updated:** 2026-09-05  

### Plain status

**SYNC1 Soften** is on the record (Kill **not** triggered). **GEOM0 HARDEN** and prior **MULTIPATH1 Soften** still stand. Provisional **sim X = 0.50 m** remains, scoped to **near-ideal sync + NLOS** (LOS / mild/intermittent NLOS only). Near-ideal `σ_sync ≲ 0.3 ns` → median **0.382 m** ≤ X; `σ_sync` = 1 ns scrapes **0.513 m**; `≥ 3 ns` / 3 ns path drift **fails X**. **X is median-not-p90** (1 ns p90 ≈ **1.16 m**). **Hardware X PARKED.** Cell-tower **PARKED.** BIA **CLOSED.** Lab **HOLD.** This is **not** a locator. This is **not** claim clearance. This is **not** training. This is **not** skill-met. This is **not** rithm. Do **not** invent fingerprint / ML / RF to rescue loose sync. GPS is **never** the mobile fix. US10135667B1 is a custom-beacon substrate note only — **not** a carrier-mast Amb.

**Founder DIGEST:** Geometry+Chan is feasible under ideal sync; provisional sim X=0.50 m is median@1ns RX noise and only honest under mild NLOS + near-ideal inter-ref sync (σ_sync≲0.3 ns); strong multipath or σ_sync≳1 ns / path drift fail Chan alone; remaining live fog = sync fidelity + multipath (not hyperbolic geometry); contrast Greer US10135667B1 remains custom-beacon substrate, not carrier-mast Amb. Lab HOLD; optional later combined mild-NLOS+0.3ns sync or drift-compensation textbook pulses parked until Founder/user reopens. Hardware X PARKED.

---

| Field | Value |
|-------|--------|
| **Closure state** | **open** — **GEOM0 HARDEN** + **MULTIPATH1 Soften** + **SYNC1 Soften** on record; provisional **sim X = 0.50 m** remains under **sync + NLOS** scope (**median**-not-p90); hardware **X PARKED**; Lab **HOLD**; not hard stop; no closeout hygiene this fold |
| **Phase** | Amb open / Lab **HOLD** (optional later textbook pulses parked until Founder / user reopens; **no RF / ML**) |
| **Amb** | geometry leftover **HARDENED**. Multipath leftover **Soften** (LOS + mild/intermittent NLOS only). Sync leftover **Soften** (near-ideal `σ_sync ≲ 0.3 ns`). Live fog remains **sync fidelity + multipath** (not hyperbolic geometry). **Sim X = 0.50 m** (provisional; scoped; **median**-based @ 1 ns; 1 ns p90 ≈ **1.16 m**). Hardware **X PARKED** |
| **Locks in force** | Founder **CLAIM LOCK** · fog peek C1/C2/C3 · **GEOM0 HARDEN** · **MULTIPATH1 Soften** · **SYNC1 Soften** · sim-only path · provisional **sim X = 0.50 m** (median @ 1 ns RX; honest only under mild NLOS + near-ideal sync; **median-not-p90**) · GPS/DGPS never the mobile fix · no RF fingerprint / ML invent · US10135667B1 prior-art / custom-beacon note only |
| **Next authorization needed** | **none this fold** — Lab **HOLD**. Optional later combined mild-NLOS + 0.3 ns sync, or drift-compensation textbook pulses, stay **parked** until Founder / user reopens. **Not** auto-clearance; **not** a locator; **not** RF/ML invent; **not** skill-met. Lab does **not** self-admit |
| **Related apps surfaced** | `2026-09_cell-tower-geometry` — Amb **PARKED** (Founder STOP / user pivot; peek #61 + X=300 m on record; **not live**); this app does **not** reopen it as live · `2026-09_human-bia-weight` — string **CLOSE** / scale-accuracy **KILL** (#59); BIA portfolio **CLOSED**; this app does **not** reopen it |
| **Optional modes** | none yet (open; not endpoint) |

**Ledger:** [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md)  
**SYNC1 score (gated):** [`SCORE_SYNC_1.md`](SCORE_SYNC_1.md)  
**SYNC1 digestion:** [`DIGESTION_SYNC_1.md`](DIGESTION_SYNC_1.md)  
**MULTIPATH1 score (gated, prior):** [`SCORE_MULTIPATH1.md`](SCORE_MULTIPATH1.md)  
**MULTIPATH1 digestion (prior):** [`DIGESTION_MULTIPATH1.md`](DIGESTION_MULTIPATH1.md)  
**#0 score (gated):** [`SCORE_GEOMETRY_0.md`](SCORE_GEOMETRY_0.md)  
**#0 digestion:** [`DIGESTION_GEOMETRY_0.md`](DIGESTION_GEOMETRY_0.md)  
**Peek + gate:** [`PROPOSED_PULSE.md`](PROPOSED_PULSE.md)  
**Peek digestion:** [`DIGESTION_FIRST_PULSE.md`](DIGESTION_FIRST_PULSE.md)  
**Incoming digestion:** [`DIGESTION_FROM_CELL_TOWER.md`](DIGESTION_FROM_CELL_TOWER.md)  
**Decision log:** [`RESIDUAL_BRANCH_MENU.md`](RESIDUAL_BRANCH_MENU.md)

**What this fold does not do:** no new TDOA invent after SYNC1; no RF / ML / fingerprint rescue of loose sync; no hardware campaign; no weights; no big datasets committed; no copy of US10135667B1 claim language; no GPS/DGPS-as-mobile-fix claim; no skill-met / elevated language; no reading **0.50 m** as a p90 bar or a multipath-robust bar; no unpark of hardware **X**; no reopen of cell-tower as live; no reopen of the BIA→weight portfolio (human #59 CLOSE; poultry #47 / cattle #49 / sheep #51 / companion #53 stay parked).

**Run constraint:** SYNC1 used **frozen Chan 1994**; `σ_t` = 1 ns; **same refs / L-path** as #0. This fold is **docs only** — Lab scratch was **not** on the VM; metrics copied from the Operator gate. No GPU. No trained models. No hardware campaign. No bulk dataset download into the repo.

**Endpoint** = examination done; verdict frozen. This fold is **open**. Do **not** label hard stop.

---

## Closeout checklist (required before **hard stop**)

Not claimed this fold. Boxes stay open.

- [ ] `Original_Claim_Assessment` / closeout
- [ ] `DISSERTATION.md`
- [ ] `EXECUTIVE_BRIEF.md`
- [ ] **`SHARE_PACK.md`**
- [ ] Layer 2 `Thesis_Tracker.md`
- [ ] Layer 1 `TRACKER_PORTFOLIO.md` row updated
- [ ] Layer 3 residual dispositions set
- [ ] Residual-branch menu if residuals remain
- [ ] **Optional-modes menu**
- [ ] `TRACKER_PATTERN_MAP.md` if new pattern
- [ ] `logs/calibration_log.md` if pattern ≥3 apps
- [ ] UX/CX/CR/QI exhibits only if authorized and run
- [ ] `STATUS.md` set to hard stop
- [ ] `final_verdict.md`

**Gates:** C1 **SUCCEED**. C2 **SUCCEED**. C3 **SUCCEED**. **GEOM0 HARDEN**. **MULTIPATH1 Soften**. **SYNC1 Soften** (Kill not triggered). Provisional **sim X = 0.50 m** remains under **sync + NLOS** scope (**median**-not-p90; 1 ns p90 ≈ **1.16 m**). Hardware **X PARKED**. Soften / HARDEN is **not** claim clearance. GPS-denied TDOA locate is **not** established. Training is **not** established. Skill-met is **not** claimed. Cell-tower stays **PARKED**. BIA stays **CLOSED**.

---

*Mandatory under standing rule. Mirror a one-line pointer at top of `notes.md`.*
