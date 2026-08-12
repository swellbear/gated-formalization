# Anchor & Claim-Type Template

**Date:** 2026-08-12  
**Application ID:** `2026-08_graphql-alone-overfetch-preferability`

## L₀ — Objective Anchors
1. APIs are commonly designed as REST, GraphQL, gRPC, or hybrids/BFFs (industry practice).  
2. Over-fetching and under-fetching are recognized REST pain points; GraphQL query shaping addresses payload selection — other costs appear (N+1, complexity, caching, authz).  
3. Preferability of API style is multi-criterial (payload efficiency, caching, tooling, team skills, schema evolution, security).

## Candidate claim
`GraphQL is preferable to REST because GraphQL alone avoids over-fetching; therefore APIs should prefer GraphQL.`

## Pre-Classification
- [x] **Mixed:** D (fetch shapes differ) / O (alone avoids over-fetch) / P (therefore preferable/should)

| Term | Bar |
|------|-----|
| alone / avoids | Uniqueness vs C₀; spectrum (LOCK-004) |
| preferable / should | Named V (LOCK-002) |

## Imported locks
```
Imported pattern from AV / MWI / CDS / microservices / serverless, re-validated here.
- LOCK-2026-08-001…004 · Cons OK · verdicts not inherited.
```
- [x] Ready for gate scoring
