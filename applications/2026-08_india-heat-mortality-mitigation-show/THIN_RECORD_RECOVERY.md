# Thin-record recovery protocol

**Use when** an application is `incomplete-record` (verdict-only / missing `01`–`05`). Do **not** reopen elevations until recovery steps below are done or explicitly waived.

**Application:**  
**Date:**  

---

## Order (do not skip ahead)

1. [ ] **Recover claim text** — verbatim original claim (or document that it is permanently lost)
2. [ ] **Recover / backfill worksheets** — at least `01`, gate sheet, admitted layers, closeout-equivalent
3. [ ] **Rebuild STATUS.md + Thesis_Tracker.md** from recovered artifacts
4. [ ] **Only then** authorize elevation residuals (ELEV-*, FP-*, etc.)

## Waivers (if any)

| Step waived | Operator reason |
|-------------|-----------------|
|             |                 |

## Stop conditions

- Elevations attempted before steps 1–2 → **HOLD**; do not ADMIT elevation layers.
- Claim text permanently lost → mark in STATUS; any new work is a **new application** with reconstructed claim, not silent salvage.

---

*Standing rule: thin-record recovery. See pattern `incomplete-record`.*
