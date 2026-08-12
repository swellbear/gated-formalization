# Dissertation — Application Findings

**Application:** `2026-08_microservices-alone-cascading-preferability`  
**Closeout verdict:** Stable Provisional  
**Amb at closeout:** ≈ 8  
**FD:** 1  

## Plain-language findings

Teams often hear: “Use microservices — they alone stop cascading failures, so they’re the better choice.”  

This run checked that slogan under Gated Progressive Formalization.

**What held (scoped):** You must say *compared to what* (we locked an evaluation set: monolith, modular monolith, SOA, microservices). Real systems are usually hybrids; “alone” needs forced-deviation questions (shared databases, call chains, shared platforms).  

**What did not hold:** That microservices uniquely avoid cascading failure, or that uniqueness would make them preferable / what teams *should* choose. Preferability needs named tradeoff metrics; uniqueness alone does not license “therefore better.”  

**Bottom line:** Slogan package **not established**. Local progress (naming the comparison set, admitting spectrum) is **not** clearance of the big claim.

## Technical appendix

- Claim-type: Mixed (D / O / P).  
- Imports: LOCK-2026-08-001…004 with Cons re-validation.  
- Cycle 0 Amb = 12 → after L1–L2 ≈ 8.  
- Admissions: L1 C₀ evaluation lock; L2 spectrum/FD descriptive.  
- Patterns: `uniqueness-preferability`, `design-spectrum`, `forced-deviation`, `comparison-class-unset` (class named for eval only), `R-dependence` (P blocked on V).  
- Related apps (process only): AV E2E; many-worlds; CDS preferability.  
