# Claim Graph

**Date:** 2026-08-12  
**Scope:** portfolio-wide (engineering batch + cash-privacy cross-domain probe)  
**Maintainer note:** APP-CASH added; LOCK-004 marked Under review (generality wording). Calibration 2026-08-C3.

*Optional overview. Individual worksheets remain the source of truth.*

---

## Nodes

| Node ID | Type | Short label | Status / FD (if known) |
|---------|------|-------------|------------------------|
| APP-MWI | Application | `2026-08_many-worlds-unitarity-preferability` | Provisional closed; Amb ≈ 5.5 |
| APP-AV | Application | `2026-08_av-e2e-vs-modular-preferability` | Stable Provisional closed; Amb ≈ 4 |
| APP-GWT | Application | `2026-08_llm-global-workspace-consciousness` | Live remnant Provisional-stable; Amb ≈ 2.5 |
| APP-CDS | Application | `2026-08_cds-med-device-ad-segment-preferability` | Stable Provisional (proxy-scoped) |
| APP-MS | Application | `2026-08_microservices-alone-cascading-preferability` | Stable Provisional; Amb ≈ 8; FD 1 |
| APP-SVL | Application | `2026-08_serverless-alone-ops-preferability` | Stable Provisional; Amb ≈ 8; FD 1 |
| APP-GQL | Application | `2026-08_graphql-alone-overfetch-preferability` | Stable Provisional; Amb ≈ 8; FD 1 |
| APP-CASH | Application | `2026-08_cash-alone-privacy-preferability` | Stable Provisional; Amb ≈ 8; FD 1 (cross-domain) |
| APP-TERM | Application | `2026-08_term-limits-alone-accountability-preferability` | Stable Provisional; Amb ≈ 8; FD 1 (cross-domain #2) |
| LOCK-2026-08-001 | Lock | Comparison class before uniqueness (O) | Active |
| LOCK-2026-08-002 | Lock | Preferability needs named virtues/metrics | Active |
| LOCK-2026-08-003 | Lock | Amb drop / scope lock ≠ clearance | Active |
| LOCK-2026-08-004 | Lock | Hybrid/spectrum FD on “alone” | **Active** (broadened) |

---

## Edges

| From | To | Relation | Notes |
|------|----|----------|-------|
| APP-MS | APP-AV | shares_anchor_class | engineering alone/preferability |
| APP-SVL | APP-MS | shares_anchor_class | batch |
| APP-GQL | APP-SVL | shares_anchor_class | batch |
| APP-CASH | APP-GQL | shares_anchor_class | alone⇒preferable shape (cross-domain) |
| APP-CASH | APP-CDS | shares_anchor_class | preferability metrics kinship |
| APP-MS | LOCK-2026-08-001 | imports_lock | |
| APP-MS | LOCK-2026-08-002 | imports_lock | |
| APP-MS | LOCK-2026-08-003 | imports_lock | |
| APP-MS | LOCK-2026-08-004 | imports_lock | |
| APP-SVL | LOCK-2026-08-001 | imports_lock | |
| APP-SVL | LOCK-2026-08-002 | imports_lock | |
| APP-SVL | LOCK-2026-08-003 | imports_lock | |
| APP-SVL | LOCK-2026-08-004 | imports_lock | |
| APP-GQL | LOCK-2026-08-001 | imports_lock | |
| APP-GQL | LOCK-2026-08-002 | imports_lock | |
| APP-GQL | LOCK-2026-08-003 | imports_lock | |
| APP-GQL | LOCK-2026-08-004 | imports_lock | |
| APP-CASH | LOCK-2026-08-001 | imports_lock | cross-domain clean |
| APP-CASH | LOCK-2026-08-002 | imports_lock | cross-domain clean |
| APP-CASH | LOCK-2026-08-003 | imports_lock | cross-domain clean |
| APP-CASH | LOCK-2026-08-004 | imports_lock | analogue then 004 folded |
| APP-TERM | LOCK-2026-08-001 | imports_lock | cross-domain #2 clean |
| APP-TERM | LOCK-2026-08-002 | imports_lock | |
| APP-TERM | LOCK-2026-08-003 | imports_lock | |
| APP-TERM | LOCK-2026-08-004 | imports_lock | Active broadened — clean |

---

## Residual judgment / known missing edges

- Cross-domain probe succeeded for 001–003; LOCK-004 needs wording review for non-architecture hybrids.  
- No further engineering same-shape siblings recommended until LOCK-004 decision.

---

## Ready for next step?

- [x] Update after new application  
- [x] Update after new lock  
- [ ] Freeze  
- [ ] Archive  
