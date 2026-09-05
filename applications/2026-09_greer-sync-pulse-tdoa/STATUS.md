# STATUS — Operator “where am I?”

**Update every cycle.** Keep short. Full narrative stays in notes / worksheets.  
**Glossary:** `docs/READER_GLOSSARY.md`

**Application:** `2026-09_greer-sync-pulse-tdoa`  
**Updated:** 2026-09-05  

### Plain status

**JOINT1 Soften** is on the record (Kill **not** triggered; Aim A **partial**). **GEOM0 HARDEN**, **MULTIPATH1 Soften**, and prior **SYNC1 Soften** (Chan-alone) still stand. Provisional **sim X = 0.50 m** remains. Named sync Soften budget is now **`σ_sync ≲ 3 ns` under JOINT1** (path-shared / fixed_trial: **0.231 m** @ 1 ns; **0.439 m** @ 3 ns ≤ X) + prior mild-NLOS. Chan scrape at 1 ns is **restored**. `σ_sync` = 10 ns fails (**1.816 m**). Drift 3 ns/path still breaks X (JOINT1 **0.919 m** — shared-τ misspecified vs ramp). **Not** multipath-robust. **Not** drift-robust. **X is median-not-p90** (1 ns p90 ≈ **1.16 m**). **Hardware X PARKED.** Next (**not this fold**): **DRIFT1**. Cell-tower **PARKED.** BIA **CLOSED.** This is **not** a locator. This is **not** claim clearance. This is **not** training. This is **not** skill-met. This is **not** rithm. Do **not** invent fingerprint / ML / RF. GPS is **never** the mobile fix. US10135667B1 is owner-requested **collaboration framing** (bibliographic; custom-beacon substrate) — **no claim-language copy**; **not** a carrier-mast Amb.

---

| Field | Value |
|-------|--------|
| **Closure state** | **open** — **GEOM0 HARDEN** + **MULTIPATH1 Soften** + **SYNC1 Soften** + **JOINT1 Soften** on record; provisional **sim X = 0.50 m** remains under **JOINT1 sync + NLOS** scope (**median**-not-p90); hardware **X PARKED**; **DRIFT1** named next (not run); not hard stop; no closeout hygiene this fold |
| **Phase** | Amb open / JOINT1 Soften recorded; **DRIFT1** named (not this fold; **no RF / ML**) |
| **Amb** | geometry leftover **HARDENED**. Multipath leftover **Soften** (LOS + mild/intermittent NLOS only). Sync leftover **Soften** — Chan-alone near-ideal `σ_sync ≲ 0.3 ns`; **widened** to `σ_sync ≲ 3 ns` **under JOINT1**. Live leftover includes **drift** (shared-τ vs ramp) + **multipath**. **Sim X = 0.50 m** (provisional; scoped; **median**-based @ 1 ns; 1 ns p90 ≈ **1.16 m**). Hardware **X PARKED** |
| **Locks in force** | Founder **CLAIM LOCK** · fog peek C1/C2/C3 · **GEOM0 HARDEN** · **MULTIPATH1 Soften** · **SYNC1 Soften** · **JOINT1 Soften** · sim-only path · provisional **sim X = 0.50 m** (median @ 1 ns RX; honest only under mild NLOS + `σ_sync ≲ 3 ns` under JOINT1; **median-not-p90**; **not** multipath-robust; **not** drift-robust) · GPS/DGPS never the mobile fix · no RF fingerprint / ML invent · US10135667B1 owner-requested collaboration framing (bibliographic; **no claim-language copy**) |
| **Next authorization needed** | **DRIFT1** pulse (**not this fold**). **Not** auto-clearance; **not** a locator; **not** RF/ML invent; **not** skill-met; **not** drift-robust from JOINT1. Lab does **not** self-admit |
| **Related apps surfaced** | `2026-09_cell-tower-geometry` — Amb **PARKED** (Founder STOP / user pivot; peek #61 + X=300 m on record; **not live**); this app does **not** reopen it as live · `2026-09_human-bia-weight` — string **CLOSE** / scale-accuracy **KILL** (#59); BIA portfolio **CLOSED**; this app does **not** reopen it |
| **Optional modes** | none yet (open; not endpoint) |

**Ledger:** [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md)  
**JOINT1 score (gated):** [`SCORE_JOINT1.md`](SCORE_JOINT1.md)  
**JOINT1 digestion:** [`DIGESTION_JOINT1.md`](DIGESTION_JOINT1.md)  
**SYNC1 score (gated, prior):** [`SCORE_SYNC_1.md`](SCORE_SYNC_1.md)  
**SYNC1 digestion (prior):** [`DIGESTION_SYNC_1.md`](DIGESTION_SYNC_1.md)  
**MULTIPATH1 score (gated, prior):** [`SCORE_MULTIPATH1.md`](SCORE_MULTIPATH1.md)  
**MULTIPATH1 digestion (prior):** [`DIGESTION_MULTIPATH1.md`](DIGESTION_MULTIPATH1.md)  
**#0 score (gated):** [`SCORE_GEOMETRY_0.md`](SCORE_GEOMETRY_0.md)  
**#0 digestion:** [`DIGESTION_GEOMETRY_0.md`](DIGESTION_GEOMETRY_0.md)  
**Peek + gate:** [`PROPOSED_PULSE.md`](PROPOSED_PULSE.md)  
**Peek digestion:** [`DIGESTION_FIRST_PULSE.md`](DIGESTION_FIRST_PULSE.md)  
**Incoming digestion:** [`DIGESTION_FROM_CELL_TOWER.md`](DIGESTION_FROM_CELL_TOWER.md)  
**Decision log:** [`RESIDUAL_BRANCH_MENU.md`](RESIDUAL_BRANCH_MENU.md)

**What this fold does not do:** no DRIFT1 run; no RF / ML / fingerprint rescue; no hardware campaign; no weights; no big datasets committed; no copy of US10135667B1 claim language; no GPS/DGPS-as-mobile-fix claim; no skill-met / elevated language; no reading **0.50 m** as a p90 bar, a multipath-robust bar, or a drift-robust bar; no unpark of hardware **X**; no reopen of cell-tower as live; no reopen of the BIA→weight portfolio (human #59 CLOSE; poultry #47 / cattle #49 / sheep #51 / companion #53 stay parked).

**Run constraint:** JOINT1 used **path-shared joint clocks** (shared-τ) under **fixed_trial** `σ_sync`. This fold is **docs only** — Lab scratch was **not** on the VM; metrics copied from the Operator gate. No GPU. No trained models. No hardware campaign. No bulk dataset download into the repo.

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

**Gates:** C1 **SUCCEED**. C2 **SUCCEED**. C3 **SUCCEED**. **GEOM0 HARDEN**. **MULTIPATH1 Soften**. **SYNC1 Soften**. **JOINT1 Soften** (Kill not triggered; Aim A partial). Provisional **sim X = 0.50 m** remains under **JOINT1 sync + NLOS** scope (**median**-not-p90; 1 ns p90 ≈ **1.16 m**). Hardware **X PARKED**. Soften / HARDEN is **not** claim clearance. GPS-denied TDOA locate is **not** established. Training is **not** established. Skill-met is **not** claimed. Cell-tower stays **PARKED**. BIA stays **CLOSED**.

---

*Mandatory under standing rule. Mirror a one-line pointer at top of `notes.md`.*
