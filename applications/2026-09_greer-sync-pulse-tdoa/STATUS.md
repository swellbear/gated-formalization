# STATUS — Operator “where am I?”

**Update every cycle.** Keep short. Full narrative stays in notes / worksheets.  
**Glossary:** `docs/READER_GLOSSARY.md`

**Application:** `2026-09_greer-sync-pulse-tdoa`  
**Updated:** 2026-09-05  

### Plain status

**REOPEN** (solve framing — **not** park forever). **Collaboration-with-owner:** Greer (patent owner, US10135667B1) **requested** they solve his problem. The later deliverable is **for him by request**, **not** an unsolicited write-up. **Do not** invent product claim-language copy. **Solve-target (kept):** sync fragility for Greer-style GPS-denied sync-beacon locate. Either **(A)** keep provisional **sim X = 0.50 m** under a **named** sync Soften when `σ_sync` goes beyond 0.3 ns / drift **without** fingerprint / ML invent, **or (B)** detect from measurements alone when sync left the near-ideal band and Soften / widen **X** / refuse a point fix. Founder **may re-aim** when Greer’s success criteria arrive. Baseline standing **preserved:** **GEOM0 HARDEN**; **MULTIPATH1 Soften** (mild-NLOS scope); **SYNC1 Soften** (`σ_sync ≲ 0.3 ns`). **Hardware X PARKED.** GPS **refs only**. **Not** a remake of commercial RTLS. Lab **HOLD lifted for the invent board only.** First pulse after REOPEN (**not this fold**): Lab invents 2–3 cheap-check options for (A)/(B); Founder ranks. Multipath wave-2 **after** the sync string clears or parks. This is **not** a locator. This is **not** claim clearance. This is **not** training. This is **not** skill-met. This is **not** rithm.

**Founder DIGEST (baseline preserved):** Geometry+Chan is feasible under ideal sync; provisional sim X=0.50 m is median@1ns RX noise and only honest under mild NLOS + near-ideal inter-ref sync (σ_sync≲0.3 ns); strong multipath or σ_sync≳1 ns / path drift fail Chan alone; remaining live fog = sync fidelity + multipath (not hyperbolic geometry); contrast Greer US10135667B1 remains custom-beacon substrate, not carrier-mast Amb. Hardware X PARKED. The prior HOLD / “park until reopen” clause is what this fold **fires**.

---

| Field | Value |
|-------|--------|
| **Closure state** | **open** — **REOPEN** sync-fragility solve-target; **GEOM0 HARDEN** + **MULTIPATH1 Soften** + **SYNC1 Soften** on record; DIGEST baseline **preserved**; provisional **sim X = 0.50 m** remains under **sync + NLOS** scope (**median**-not-p90); hardware **X PARKED**; Lab HOLD **lifted for invent board only**; not hard stop; no closeout hygiene this fold |
| **Phase** | Amb open / Founder **REOPEN** (solve framing; invent board **authorized, not run**; **no RF / ML**) |
| **Amb** | geometry leftover **HARDENED**. Multipath leftover **Soften** (LOS + mild/intermittent NLOS only). Sync leftover **Soften** (near-ideal `σ_sync ≲ 0.3 ns`) now a **live solve-target** — (A) named Soften beyond 0.3 ns / drift **or** (B) detect-from-measurements / widen **X** / refuse a point fix. Live fog remains **sync fidelity** first (multipath wave-2 after sync clears or parks). **Sim X = 0.50 m** (provisional; scoped; **median**-based @ 1 ns; 1 ns p90 ≈ **1.16 m**). Hardware **X PARKED** |
| **Locks in force** | Founder **CLAIM LOCK** · fog peek C1/C2/C3 · **GEOM0 HARDEN** · **MULTIPATH1 Soften** · **SYNC1 Soften** · Founder **REOPEN** solve-target (A)/(B) · **collaboration-with-owner** (Greer requested; deliverable by request, not unsolicited) · sim-only path · provisional **sim X = 0.50 m** (median @ 1 ns RX; honest only under mild NLOS + near-ideal sync; **median-not-p90**) · GPS/DGPS never the mobile fix · no RF fingerprint / ML invent · **no invented product claim-language copy** · US10135667B1 bibliographic / owner-request note only · Founder may re-aim when Greer’s success criteria arrive · **not** commercial RTLS remake |
| **Next authorization needed** | **none this fold** — invent board is **authorized** (Lab invents 2–3 cheap-check options for (A)/(B); Founder ranks; **not run here**). Founder **may re-aim** when Greer’s success criteria arrive. Multipath wave-2 stays **parked** until the sync string clears or parks. **Not** auto-clearance; **not** a locator; **not** RF/ML invent; **not** skill-met; **not** an unsolicited write-up; **not** invented product claim-language; **not** a remake of commercial RTLS. Lab does **not** self-admit |
| **Related apps surfaced** | `2026-09_cell-tower-geometry` — Amb **PARKED** (Founder STOP / user pivot; peek #61 + X=300 m on record; **not live**); this app does **not** reopen it as live · `2026-09_human-bia-weight` — string **CLOSE** / scale-accuracy **KILL** (#59); BIA portfolio **CLOSED**; this app does **not** reopen it |
| **Optional modes** | none yet (open; not endpoint) |

**Ledger:** [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md)  
**REOPEN digestion:** [`DIGESTION_REOPEN_SYNC.md`](DIGESTION_REOPEN_SYNC.md)  
**SYNC1 score (gated):** [`SCORE_SYNC_1.md`](SCORE_SYNC_1.md)  
**SYNC1 digestion (DIGEST baseline preserved):** [`DIGESTION_SYNC_1.md`](DIGESTION_SYNC_1.md)  
**MULTIPATH1 score (gated, prior):** [`SCORE_MULTIPATH1.md`](SCORE_MULTIPATH1.md)  
**MULTIPATH1 digestion (prior):** [`DIGESTION_MULTIPATH1.md`](DIGESTION_MULTIPATH1.md)  
**#0 score (gated):** [`SCORE_GEOMETRY_0.md`](SCORE_GEOMETRY_0.md)  
**#0 digestion:** [`DIGESTION_GEOMETRY_0.md`](DIGESTION_GEOMETRY_0.md)  
**Peek + gate:** [`PROPOSED_PULSE.md`](PROPOSED_PULSE.md)  
**Peek digestion:** [`DIGESTION_FIRST_PULSE.md`](DIGESTION_FIRST_PULSE.md)  
**Incoming digestion:** [`DIGESTION_FROM_CELL_TOWER.md`](DIGESTION_FROM_CELL_TOWER.md)  
**Decision log:** [`RESIDUAL_BRANCH_MENU.md`](RESIDUAL_BRANCH_MENU.md)

**What this fold does not do:** no invent of the 2–3 cheap-check options (next pulse, not this fold); no RF / ML / fingerprint rescue of loose sync; no remake of commercial RTLS; no unsolicited write-up; no invented product claim-language copy; no hardware campaign; no weights; no big datasets committed; no copy of US10135667B1 claim language; no GPS/DGPS-as-mobile-fix claim; no skill-met / elevated language; no reading **0.50 m** as a p90 bar or a multipath-robust bar; no unpark of hardware **X**; no start of multipath wave-2; no reopen of cell-tower as live; no reopen of the BIA→weight portfolio (human #59 CLOSE; poultry #47 / cattle #49 / sheep #51 / companion #53 stay parked).

**Run constraint:** this fold is **docs-only framing**. No pulse is scored. No Lab scratch on this VM. SYNC1 / MULTIPATH1 / GEOM0 metrics stay as gated. No GPU. No trained models. No hardware campaign. No bulk dataset download into the repo.

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

**Gates:** C1 **SUCCEED**. C2 **SUCCEED**. C3 **SUCCEED**. **GEOM0 HARDEN**. **MULTIPATH1 Soften**. **SYNC1 Soften** (Kill not triggered). Founder / Operator **REOPEN** sync-fragility solve-target (A)/(B). **Collaboration-with-owner** (Greer requested; deliverable by request, not unsolicited). Founder may re-aim when Greer’s success criteria arrive. DIGEST baseline **preserved**. Provisional **sim X = 0.50 m** remains under **sync + NLOS** scope (**median**-not-p90; 1 ns p90 ≈ **1.16 m**). Hardware **X PARKED**. REOPEN / Soften / HARDEN is **not** claim clearance. GPS-denied TDOA locate is **not** established. Training is **not** established. Skill-met is **not** claimed. Commercial RTLS remake is **not** this Amb. Cell-tower stays **PARKED**. BIA stays **CLOSED**.

---

*Mandatory under standing rule. Mirror a one-line pointer at top of `notes.md`.*
