# Leftover callout after live / strategy

**Status:** DONE  
**Shipped:** 2026-08-17 (after St. Jude 2026 date gate). Display only. Did not re-lock paper. Did not change θ, screens, or ticket size.

This is **not** a Gated Progressive Formalization residual-branch menu. No Amb, gates, `authorize branch`, or anything under `applications/`.

## What shipped

`format_leftover_callout(result, open_book=None) -> str` prints after `format_recommendation` on operating `live` and `ingest`. The same block is in the pressure-test markdown. ASCII only.

Four sections:

1. **Already used** — ESPN field / to-par / holes completed when live; as-of SG if inventory says present; Bovada posted if quotes exist.
2. **Still unconstrained** — agronomy, tee/wave, injury unless ESPN WD, narrative forced to 0, unmatched SG names. Pulled from inventory impact/notes, not a second catalog.
3. **On held tickets** — live + open paper only. One line per open name: Win% is banked to-par plus remaining holes from current θ. A “hot round” / “looking good” is the operator’s residual, not extra θ. Ingest with no book: none held.
4. **Do not stuff into θ** — overrides stay documented (`HumanOverride` + audit) or they do not happen. No live Δθ CLI in this patch.

See the live/ingest terminal block (and pressure-test `## Leftover callout`).
