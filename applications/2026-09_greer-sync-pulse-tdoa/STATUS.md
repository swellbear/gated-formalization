# STATUS — Operator “where am I?”

**Update every cycle.** Keep short. Full narrative stays in notes / worksheets.  
**Glossary:** `docs/READER_GLOSSARY.md`

**Application:** `2026-09_greer-sync-pulse-tdoa`  
**Updated:** 2026-09-05  

### Plain status

**MULTIPATH1 Soften** is on the record (Kill not triggered; after fog peek **ADMITTED** and **#0 HARDEN**). Provisional **sim X = 0.50 m** stays **LOCKED** with an **NLOS scope annotation**: poseable under LOS + mild / intermittent NLOS (baseline median **0.364 m**; `random_k=1` `b=0.5` → **0.476 m**; `epoch_f=0.25` `b=1` → **0.452 m**); **not** poseable under strong persistent multipath (`b≥1–2 m` → **0.73–4.7+ m**) with frozen Chan alone. Do **not** claim a multipath-robust 0.50 m. **No** fingerprint rescue. **X** remains **median-not-p90** (p90 ≈ **1.16 m** @ 1 ns LOS). **Hardware X PARKED.** Next pulse (**not this fold**): **sync-imperfection**. This is **not** a locator. This is **not** claim clearance. This is **not** training. This is **not** skill-met. This is **not** rithm. GPS is **never** the mobile fix. Cell-tower stays **PARKED**. BIA→weight stays **CLOSED**. US10135667B1 is a prior-art note only.

---

| Field | Value |
|-------|--------|
| **Closure state** | **open** — fog peek **ADMITTED**; **#0 HARDEN**; **MULTIPATH1 Soften**; provisional **sim X = 0.50 m** locked (**NLOS-scoped**; **median**-not-p90); hardware **X PARKED**; not hard stop; no closeout hygiene this fold |
| **Phase** | Amb open / MULTIPATH1 **gated Soften**; next invent only if Founder / Operator opens **sync-imperfection** (**not this fold**; **no RF / ML**) |
| **Amb** | geometry leftover **HARDENED** (#0). Multipath leftover **Soften** / **NLOS-scoped** (not Kill; not multipath-robust). Named leftover still open: sync-imperfection. **Sim X = 0.50 m** (provisional; LOS + mild / intermittent NLOS; **median**-not-p90; 1 ns p90 ≈ **1.16 m**). Hardware **X PARKED** |
| **Locks in force** | Founder **CLAIM LOCK** · fog peek C1/C2/C3 · **#0 HARDEN** · **MULTIPATH1 Soften** · sim-only path · provisional **sim X = 0.50 m** (**NLOS-scoped**; **median**-not-p90; frozen Chan 1994; `σ_t`=1 ns; positive range-bias; same refs/L-path as #0) · GPS/DGPS never the mobile fix · no RF fingerprint training / no fingerprint rescue · US10135667B1 prior-art note only |
| **Next authorization needed** | **none for this Soften** — Lab **HOLD** on running sync-imperfection here. Next pulse (**admitted**, not this fold) = **sync-imperfection**. **Not** auto-clearance; **not** a locator; **not** RF/ML invent; **not** skill-met. Lab does **not** self-admit |
| **Related apps surfaced** | `2026-09_cell-tower-geometry` — Amb **PARKED** (Founder STOP / user pivot; peek #61 + X=300 m on record; **not live**); this app does **not** reopen it as live · `2026-09_human-bia-weight` — string **CLOSE** / scale-accuracy **KILL** (#59); BIA portfolio **CLOSED**; this app does **not** reopen it |
| **Optional modes** | none yet (open; not endpoint) |

**Ledger:** [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md)  
**MULTIPATH1 score (gated):** [`SCORE_MULTIPATH1.md`](SCORE_MULTIPATH1.md)  
**MULTIPATH1 digestion:** [`DIGESTION_MULTIPATH1.md`](DIGESTION_MULTIPATH1.md)  
**#0 score:** [`SCORE_GEOMETRY_0.md`](SCORE_GEOMETRY_0.md)  
**#0 digestion:** [`DIGESTION_GEOMETRY_0.md`](DIGESTION_GEOMETRY_0.md)  
**Peek + gate:** [`PROPOSED_PULSE.md`](PROPOSED_PULSE.md)  
**Peek digestion:** [`DIGESTION_FIRST_PULSE.md`](DIGESTION_FIRST_PULSE.md)  
**Incoming digestion:** [`DIGESTION_FROM_CELL_TOWER.md`](DIGESTION_FROM_CELL_TOWER.md)  
**Decision log:** [`RESIDUAL_BRANCH_MENU.md`](RESIDUAL_BRANCH_MENU.md)

**What this fold does not do:** no new TDOA invent after MULTIPATH1; no RF / ML / fingerprint rescue; no hardware campaign; no weights; no big datasets committed; no copy of US10135667B1 claim language; no GPS/DGPS-as-mobile-fix claim; no skill-met / elevated language; no unpark of hardware **X**; no claim of a multipath-robust 0.50 m; no reading **0.50 m** as a p90 bar; no run of sync-imperfection; no reopen of cell-tower as live; no reopen of the BIA→weight portfolio (human #59 CLOSE; poultry #47 / cattle #49 / sheep #51 / companion #53 stay parked).

**Run constraint:** MULTIPATH1 stayed on the #0 board (frozen Chan; `σ_t`=1 ns; positive range-bias; same refs/L-path). This fold is **docs only** — Lab scratch was **not** on the VM; metrics copied from the Operator gate. No GPU. No trained models. No hardware campaign. No bulk dataset download into the repo.

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

**Gates:** C1 **SUCCEED**. C2 **SUCCEED**. C3 **SUCCEED**. **#0 HARDEN**. **MULTIPATH1 Soften** (Kill not triggered). Provisional **sim X = 0.50 m** (**NLOS-scoped**; **median**-not-p90; 1 ns p90 ≈ **1.16 m**). Hardware **X PARKED**. Peek succeed / HARDEN / Soften is **not** claim clearance. GPS-denied TDOA locate is **not** established. Training is **not** established. Skill-met is **not** claimed. Cell-tower stays **PARKED**. BIA stays **CLOSED**.

---

*Mandatory under standing rule. Mirror a one-line pointer at top of `notes.md`.*
