# Greer Amb — TABLED (2026-09-06)

**Status:** TABLED by user. No Greer send. Lab invent HOLD. Reopen only if user asks.

**Repo:** `applications/2026-09_greer-sync-pulse-tdoa` on `swellbear/gated-formalization` (master)  
**Local working copy:** `/workspace/greer_tdoa_lab/` (sims, PREPs, PROPOSED boards, raw metrics/plots)

**Patent:** Kerry L. Greer — US10135667B1 — https://patents.google.com/patent/US10135667B1/en

---

## Disposition at park

| Item | State |
|------|--------|
| Abstract + claims ingest | ADMITTED (DIGEST Soften Amb) |
| Suite A1→A4 | Softened; suite DIGEST Soften Amb ADMITTED (~#83) |
| `GREER_WRITEUP_SEND.md` | Soften send-candidate on master (~#84); **cleaned plain language**; **send HOLD** |
| Outreach SMS draft | See `OUTREACH_TEXT_DRAFT.md` — not sent |
| Lab invent | HOLD |
| Next pulse | None opened |

---

## Soften stack (one screen)

1. **Bar:** ~1 m patent-facing; 0.50 m perfect-ref sim only; DGPS RN floor ~0.4–0.5 m named  
2. **Sync:** Soften under relative-clock estimator + ~2.5–3 ns differential residual; commodity 10–50 ns kills  
3. **Multipath:** Mild/intermittent leading-edge only; persistent ~2–3 m bias fails ~1 m  
4. **Waveform jitter:** 50 kHz phase-flip detection ≫ 1 ns; Soften timing budget; RF PARKED  

---

## Read order on reopen

1. This file + repo `STATUS.md`  
2. `ABSTRACT_INGEST_SUMMARY.md` / `SOURCE_US10135667B1.md`  
3. `DIGESTION_A1A4_SUITE.md`  
4. `GREER_WRITEUP_SEND.md` + `OUTREACH_TEXT_DRAFT.md`  
5. Boards: `PROPOSED_A1`…`A4`, earlier GEOM0→GATE1 as needed  
6. `raw/` metrics + plots; `run_*.py` for reproduce  

---

## Do not on reopen

- Don’t re-skim the patent — ingest already done  
- Don’t send Greer without user OK  
- Don’t blur claim-language copy vs primary-source ingest  
