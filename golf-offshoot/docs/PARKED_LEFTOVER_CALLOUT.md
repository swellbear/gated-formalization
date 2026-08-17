# Leftover callout after live / strategy

**Status:** DONE  
Shipped 2026-08-17. Display only. No new feeds. Do not stuff leftovers into theta.

Parked 2026-08-14 so this event’s locked paper book was not disturbed. Do not re-lock paper. Do not change theta, screens, or ticket size in this patch.

This is **not** a Gated Progressive Formalization residual-branch menu. No Amb, gates, `authorize branch`, or anything under `applications/`.

## Why

Leftovers (what the model used vs what it did not vs what you still own) are scattered across source inventory, per-row `Open:` lines, and the operator guide. A single block after `live` / `ingest` strategy output makes residual judgment usable without importing GPF.

## Contract (display only)

`format_leftover_callout(result, open_book=None) -> str` in `golf_offshoot.ranking.leftover`. Printed **after** `format_recommendation` on operating `live` and `ingest` (ingest has no strategy block; leftover still prints). The same block is copied into the pressure-test markdown. ASCII only.

Derive from existing `source_inventory`, run mode, and paper positions. **No new feeds.**

Four sections, fixed wording:

1. **Already used** — ESPN field / to-par / holes completed when live; as-of SG if inventory says present; Bovada posted if quotes exist.
2. **Still unconstrained** — agronomy, tee/wave, injury unless ESPN WD, narrative forced to 0, unmatched SG names. Pull from inventory impact/notes, not a second catalog.
3. **On held tickets** — live + open paper only. One line per open name: Win% is banked to-par plus remaining holes from current theta. A “hot round” / “looking good” is the operator’s residual, not extra theta. Ingest with no book: omit or print none held.
4. **Do not stuff into theta** — overrides stay documented (`HumanOverride` + audit) or they do not happen. **Do not** add a live delta-theta CLI in this same patch.

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
