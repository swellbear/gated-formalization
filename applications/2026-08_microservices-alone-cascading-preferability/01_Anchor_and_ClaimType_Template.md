# Anchor & Claim-Type Template

**Date:** 2026-08-12  
**Domain / Source material:** Common engineering slogan — microservices vs monoliths / cascading failure  
**Application ID / short name:** `2026-08_microservices-alone-cascading-preferability`

---

## L₀ — Objective Anchors

1. Software systems are commonly described along an architecture spectrum including monoliths, modular monoliths, SOA, and microservices (industry practice; not a theorem).  
2. Distributed systems can fail partially; failures can propagate across service boundaries (cascading failure is a recognized failure mode).  
3. Monoliths concentrate process/deploy failure modes differently than multi-service deployments; neither pattern is failure-free in practice.  
4. Preferability of architecture is typically multi-criterial (latency, ops cost, team topology, consistency, failure isolation, etc.).

---

## Candidate Claim or Layer Element

**Full statement:**

`Microservices architecture is preferable to monoliths because microservices alone avoid cascading failures; therefore teams should prefer microservices.`

---

## Pre-Classification (required)

- [x] **Mixed** — split:
  - **Descriptive contrast (D):** Microservices and monoliths organize failure domains differently; cascading failure is a real distributed-systems risk.  
  - **Uniqueness / alone elevation (O):** Microservices **alone** avoid cascading failures (vs monoliths / other architectures).  
  - **Preferability elevation (P):** Therefore microservices are **preferable** / teams **should** prefer them.

### Soft-modal fork

| Term | Candidate bar |
|------|----------------|
| alone / only | Uniqueness vs comparison class C₀; spectrum / hybrid forms (LOCK-004) |
| preferable / should / therefore | Preferability under named virtues V (LOCK-002); not entailed by uniqueness alone |

---

## Imported locks / patterns (Cons-checked locally)

```
Imported pattern from `2026-08_av-e2e-vs-modular-preferability` / `2026-08_many-worlds-unitarity-preferability` / `2026-08_cds-med-device-ad-segment-preferability`, re-validated here.
- What was imported: LOCK-2026-08-001 (comparison class before O); LOCK-2026-08-002 (P needs virtues); LOCK-2026-08-003 (Amb drop ≠ clearance); LOCK-2026-08-004 (design spectra / FD on “alone”)
- Re-validation under current claim: Anchors 1–4 compatible; no Cons conflict with treating architecture as spectrum or requiring named C₀/V before scoring O/P.
- Not inherited: verdicts, Amb scores, or admitted layers from source apps.
```

---

## Ready for Gate Scoring?

- [x] Yes — Mixed split + lock imports recorded  
