# STATUS — Operator “where am I?”

**Update every cycle.** Keep short. Full narrative stays in notes / worksheets.  
**Glossary:** `docs/READER_GLOSSARY.md`

**Application:** `2026-09_greer-sync-pulse-tdoa`  
**Updated:** 2026-09-05  

### Plain status

**GATE1 Soften** is on the record (Kill not triggered; aim B Succeed). Detect-only refuse OR (G1a_DRIFT1 residual ∨ G1b raw LORO): FA ≈ **0.10** in-band; TD high out-of-band (σ=10 ≈ **0.828**; unmatched drift3 = **1.000**). **Not** a magic accuracy repair. **DRIFT1 HARDEN**, **JOINT1 Soften**, **SYNC1 Soften**, **MULTIPATH1 Soften**, and **GEOM0 HARDEN** still stand. Provisional **sim X = 0.50 m** remains. **Hardware X PARKED.** Greer-facing write-up is **on disk**: Founder-polished [`GREER_WRITEUP.md`](GREER_WRITEUP.md) is **PRIMARY** — **HOLD send** until Founder / user OK. Lab audit: [`GREER_WRITEUP_DRAFT.md`](GREER_WRITEUP_DRAFT.md). **Lab HOLD invent** pending Greer criteria / user send OK. Multipath later. Cell-tower **PARKED.** BIA **CLOSED.** This is **not** a locator. This is **not** claim clearance. This is **not** training. This is **not** skill-met. This is **not** rithm. Do **not** invent fingerprint / ML / RF. GPS is **never** the mobile fix. US10135667B1 is owner-requested **collaboration framing** (bibliographic; custom-beacon substrate) — **no claim-language copy**; **not** a carrier-mast Amb.

---

| Field | Value |
|-------|--------|
| **Closure state** | **open** — **GEOM0 HARDEN** + **MULTIPATH1 Soften** + **SYNC1 Soften** + **JOINT1 Soften** + **DRIFT1 HARDEN** + **GATE1 Soften** on record; provisional **sim X = 0.50 m** remains under **JOINT1 fixed-offset + named DRIFT1 batch α + GATE1 refuse-belt + NLOS** scope (**median**-not-p90); hardware **X PARKED**; write-up on disk (**HOLD send**); Lab **HOLD** invent; not hard stop; no closeout hygiene this fold |
| **Phase** | Amb open / GATE1 Soften recorded; Greer write-up on disk (**HOLD send**); Lab **HOLD** invent pending Greer criteria / user send OK (**no RF / ML**) |
| **Amb** | geometry leftover **HARDENED**. Multipath leftover **Soften** (LOS + mild/intermittent NLOS only; **later**). Sync leftover **Soften** — Chan-alone near-ideal `σ_sync ≲ 0.3 ns`; **widened** to `σ_sync ≲ 3 ns` **under JOINT1** (fixed offsets). Path-drift leftover **HARDENED** under named **DRIFT1** batch α. Refuse leftover **Soften** (GATE1 belt; FA≈0.10; TD high). Live leftover includes **multipath** (later) + **Greer criteria**. **Sim X = 0.50 m** (provisional; scoped; **median**-based @ 1 ns; 1 ns p90 ≈ **1.16 m**). Hardware **X PARKED** |
| **Locks in force** | Founder **CLAIM LOCK** · fog peek C1/C2/C3 · **GEOM0 HARDEN** · **MULTIPATH1 Soften** · **SYNC1 Soften** · **JOINT1 Soften** · **DRIFT1 HARDEN** · **GATE1 Soften** · sim-only path · provisional **sim X = 0.50 m** (median @ 1 ns RX; honest only under mild NLOS + `σ_sync ≲ 3 ns` under JOINT1 + named DRIFT1 batch α + GATE1 refuse-belt; **median-not-p90**; **not** multipath-robust; **not** free per-epoch realtime; **not** hardware) · GPS/DGPS never the mobile fix · no RF fingerprint / ML invent · US10135667B1 owner-requested collaboration framing (bibliographic; **no claim-language copy**) · **HOLD send** of Greer write-up until user OK |
| **Next authorization needed** | **user send OK** for [`GREER_WRITEUP.md`](GREER_WRITEUP.md) (Founder PRIMARY). Lab **HOLD** invent pending Greer criteria. **Not** auto-clearance; **not** a locator; **not** RF/ML invent; **not** skill-met. Lab does **not** self-admit |
| **Related apps surfaced** | `2026-09_cell-tower-geometry` — Amb **PARKED** (Founder STOP / user pivot; peek #61 + X=300 m on record; **not live**); this app does **not** reopen it as live · `2026-09_human-bia-weight` — string **CLOSE** / scale-accuracy **KILL** (#59); BIA portfolio **CLOSED**; this app does **not** reopen it |
| **Optional modes** | none yet (open; not endpoint) |

**Ledger:** [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md)  
**Founder write-up (PRIMARY; HOLD send):** [`GREER_WRITEUP.md`](GREER_WRITEUP.md)  
**Lab audit draft:** [`GREER_WRITEUP_DRAFT.md`](GREER_WRITEUP_DRAFT.md)  
**GATE1 score (gated):** [`SCORE_GATE1.md`](SCORE_GATE1.md)  
**GATE1 digestion:** [`DIGESTION_GATE1.md`](DIGESTION_GATE1.md)  
**DRIFT1 score (gated, prior):** [`SCORE_DRIFT1.md`](SCORE_DRIFT1.md)  
**DRIFT1 digestion (prior):** [`DIGESTION_DRIFT1.md`](DIGESTION_DRIFT1.md)  
**JOINT1 score (gated, prior):** [`SCORE_JOINT1.md`](SCORE_JOINT1.md)  
**JOINT1 digestion (prior):** [`DIGESTION_JOINT1.md`](DIGESTION_JOINT1.md)  
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

**What this fold does not do:** no send to Greer; no Lab invent; no RF / ML / fingerprint rescue; no hardware campaign; no weights; no big datasets committed; no copy of US10135667B1 claim language; no GPS/DGPS-as-mobile-fix claim; no skill-met / elevated language; no reading **0.50 m** as a p90 bar, a multipath-robust bar, a free per-epoch realtime bar, or a GATE1-repaired bar; no unpark of hardware **X**; no reopen of cell-tower as live; no reopen of the BIA→weight portfolio (human #59 CLOSE; poultry #47 / cattle #49 / sheep #51 / companion #53 stay parked).

**Run constraint:** GATE1 used **detect-only refuse OR** (DRIFT1 residual ∨ raw LORO). This fold is **docs only** — Lab scratch was **not** on the VM; metrics copied from the Operator gate. Founder write-up decoded from Operator-provided base64. No GPU. No trained models. No hardware campaign. No bulk dataset download into the repo.

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

**Gates:** C1 **SUCCEED**. C2 **SUCCEED**. C3 **SUCCEED**. **GEOM0 HARDEN**. **MULTIPATH1 Soften**. **SYNC1 Soften**. **JOINT1 Soften** (Kill not triggered; Aim A partial). **DRIFT1 HARDEN** (named batch α budget; SYNC1 drift breakers restore). **GATE1 Soften** (Kill not triggered; aim B Succeed; FA≈0.10; TD high). Provisional **sim X = 0.50 m** remains under **JOINT1 fixed-offset + named DRIFT1 batch α + GATE1 refuse-belt + NLOS** scope (**median**-not-p90; 1 ns p90 ≈ **1.16 m**). Hardware **X PARKED**. Soften / HARDEN is **not** claim clearance. GPS-denied TDOA locate is **not** established. Training is **not** established. Skill-met is **not** claimed. Cell-tower stays **PARKED**. BIA stays **CLOSED**. Write-up **HOLD send**. Lab **HOLD** invent.

---

*Mandatory under standing rule. Mirror a one-line pointer at top of `notes.md`.*
