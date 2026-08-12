# Calibration & Rule Diff — Batch 2026-08-C2

**Date:** 2026-08-12  
**Calibration cycle ID:** 2026-08-C2  
**Applications reviewed:**  

| Short name | Date |
|------------|------|
| `2026-08_microservices-alone-cascading-preferability` (prior sibling; lock import path) | 2026-08-12 |
| `2026-08_serverless-alone-ops-preferability` (batch 1/3) | 2026-08-12 |
| `2026-08_graphql-alone-overfetch-preferability` (batch 2/3) | 2026-08-12 |

**Failure-mode log entries considered:** none  
**Batch authorization:** up to 3 siblings; early pause after 2 consecutive keep-rule closes; sibling 3 not opened.

---

## 1. Observed frictions / surprises

- No new free-parameter *shape* outside LOCK-001…004 across serverless and graphql.  
- Transfer worked: day-one lock import → Amb 12→≈8 on C₀+spectrum only; O/P stayed blocked; FD=1 both times.  
- Diminishing returns hit immediately (two consecutive keep-rule / no new lock / no new pattern) → pause criterion (b) fired; third sibling skipped.  
- Soft Cons + Agree low + HL caution repeated — expected, not a new failure mode.

---

## 2. What worked cleanly

- LOCK-001…004 as pre-loaded freezes shortened Phase 1 to a thin hard-stop template.  
- Honest Stable Provisional with Amb≠clearance held under agent-drafted thin closeouts.  
- Early-pause rule prevented coverage theater.

---

## 3. Proposed rule diff

1. **No change to Amb weights/bands** — current rule remains appropriate.  
2. **No change to LOCK-001…004 wording** — transfer success; no Under-review needed.  
3. **No change to claim-type / provisional-as-honest-status** — working.  
4. **No change to living gap-sheet override practice yet** — still Hold from 2026-08-C1; batch did not add new evidence requiring fold.

**Note:** Learning signal only; never auto-applied.

---

## 4. Operator decision log

| # | Proposal | Decision | Reason | Date |
|---|----------|----------|--------|------|
| 1 | No change Amb weights | Accept | Transfer success under current bands | 2026-08-12 |
| 2 | No change LOCK-001…004 | Accept | Re-validated; no new shape | 2026-08-12 |
| 3 | No change provisional discipline | Accept | Honest closes | 2026-08-12 |
| 4 | Hold gap-override living fold | Accept | Still need broader runs / C1 Hold | 2026-08-12 |

---

## 5. Ready for next step?

- [ ] Ready to fold accepted changes into living rules  
- [x] Hold — need cross-domain probe before more same-shape engineering siblings  
- [ ] Discard this calibration cycle  
