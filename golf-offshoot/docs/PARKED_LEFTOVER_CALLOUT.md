# Parked: leftover callout after live / strategy

**Status:** PARKED  
**Do not implement until:** 2026 FedEx St. Jude Championship (ESPN `401811962`) is official final, and not before **2026-08-17** (America/New_York) unless the operator is already doing post-event settle/scoring.  
**Then:** implement this **before** other new golf-offshoot features (settle/scoring of this event may run first if that is the explicit ask).  
**When shipped:** set **Status: DONE** on this page (hook and rule go quiet).

Parked 2026-08-14 so this event’s locked paper book is not disturbed. Do not re-lock paper. Do not change θ, screens, or ticket size in this patch.

This is **not** a Gated Progressive Formalization residual-branch menu. No Amb, gates, `authorize branch`, or anything under `applications/`.

## Why

Leftovers (what the model used vs what it did not vs what you still own) are scattered across source inventory, per-row `Open:` lines, and the operator guide. A single block after `live` / `ingest` strategy output makes residual judgment usable without importing GPF.

## Contract (display only)

Add `format_leftover_callout(result, open_book=None) -> str`. Print it **after** `format_recommendation` on operating `live` and `ingest`. Copy the same block into the pressure-test markdown. ASCII only.

Derive from existing `source_inventory`, run mode, and paper positions. **No new feeds.**

Four sections, fixed wording:

1. **Already used** — ESPN field / to-par / holes completed when live; as-of SG if inventory says present; Bovada posted if quotes exist.
2. **Still unconstrained** — agronomy, tee/wave, injury unless ESPN WD, narrative forced to 0, unmatched SG names. Pull from inventory impact/notes, not a second catalog.
3. **On held tickets** — live + open paper only. One line per open name: Win% is banked to-par plus remaining holes from current θ. A “hot round” / “looking good” is the operator’s residual, not extra θ. Ingest with no book: omit or print none held.
4. **Do not stuff into θ** — overrides stay documented (`HumanOverride` + audit) or they do not happen. **Do not** add a live Δθ CLI in this same patch.

## Refuse in this patch

- Filling `narrative_momentum`, tee pairing, agronomy, or injury wire
- Changing weights, screens, paper sizing, or locked St. Jude tickets
- GPF residual branches / Amb / gates
- Making unconstrained factors look constrained

## Tests

Fixture inventory + tiny paper book:

- ingest omits the ticket section (or prints none held)
- live with two open names prints those two
- wording does not claim agronomy or narrative were used

## Done when

- `format_leftover_callout` exists and is wired on operating live/ingest (+ pressure-test report)
- tests above pass
- this file’s **Status** line is **DONE**
- operator guide has a one-line pointer to the live block (replace this parked page’s “implement” language)
