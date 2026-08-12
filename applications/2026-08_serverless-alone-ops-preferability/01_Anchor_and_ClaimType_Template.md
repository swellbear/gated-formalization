# Anchor & Claim-Type Template

**Date:** 2026-08-12  
**Application ID:** `2026-08_serverless-alone-ops-preferability`

## L₀ — Objective Anchors
1. Compute can be provisioned as always-on VMs/containers, managed PaaS, serverless/FaaS, or hybrids (industry practice).  
2. Operational burden (patching, capacity, idle cost) differs by model; none is zero-ops in practice (observability, IAM, cold starts, vendor limits remain).  
3. Preferability of runtime model is multi-criterial (latency, cost, control, lock-in, team skills, compliance).

## Candidate claim
`Serverless (FaaS) is preferable to always-on servers/VMs because serverless alone eliminates operational burden; therefore teams should prefer serverless.`

## Pre-Classification
- [x] **Mixed:** D (ops models differ) / O (alone eliminates ops burden) / P (therefore preferable/should)

| Term | Bar |
|------|-----|
| alone / eliminates | Uniqueness vs C₀; spectrum/hybrid (LOCK-004) |
| preferable / should | Named virtues V (LOCK-002) |

## Imported locks
```
Imported pattern from AV / MWI / CDS / microservices sibling, re-validated here.
- Imported: LOCK-2026-08-001…004
- Re-validation: Anchors compatible; Cons OK for C₀/V/Amb≠clearance/spectrum discipline.
- Not inherited: source verdicts / Amb / layers.
```
- [x] Ready for gate scoring
