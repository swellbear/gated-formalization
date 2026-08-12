# Gate Scoring Sheet

**Date:** 2026-08-12  
**Application / Claim being scored:** Microservices preferable because alone avoid cascading failures; therefore prefer microservices  
**Linked Anchor & Claim-Type sheet:** `01_Anchor_and_ClaimType_Template.md`  
**Pass:** Cycle 0 (pre-admission)

---

## 1. Cons (Consistency)

**Score:** Moderate (soft tension)

**Notes / contradictions found:**

- Soft pass for weak descriptive contrast: failure-domain organization differs; cascading failure is real (anchors 2–3).  
- Tension on **(O):** “Alone avoid cascading failures” conflicts with known partial-failure propagation across services, shared data stores, and mesh/network dependencies; hybrids and modular monoliths blur the binary.  
- Tension on **(P):** “Therefore preferable / should” slides from a contested uniqueness claim to multi-criterial preferability without named virtues (LOCK-002).

**Compatible with all L₀ anchors and prior admitted layers?**  
- [ ] Yes  
- [x] No — soft conflict if “alone…therefore preferable” is read as settled by architecture labels alone.

---

## 2. Agree (Agreement / Stability) — secondary

**Score:** Low  

Industry and operators split on microservices vs monoliths; “alone avoids cascading failure” is especially unstable across careful passes.

---

## 3. Prod (Productivity) — secondary

**Number of new, non-trivial, checkable consequences:** 2  

1. Explicit comparison-class census C₀ for architecture options before scoring “alone.”  
2. Named preferability metrics V (failure isolation, ops cost, consistency, team topology, …) that can disagree.

---

## 4. Amb (Ambiguity / Under-determination)

| Free Parameter | Severity | Weight |
|----------------|----------|--------|
| Comparison class for “alone / preferable vs” (monolith, modular monolith, SOA, …) | High | 2 |
| Preferability virtues/metrics V and weights | High | 2 |
| What counts as “cascading failure” and evidence that microservices uniquely avoid it | High | 2 |
| Spectrum / hybrid purity of “microservices” (LOCK-004 FD) | High | 2 |
| Whether uniqueness (if any) entails preferability | Med | 1 |
| Scope (org size, domain, consistency requirements) | Med | 1 |
| Shared infrastructure (DB, bus, mesh) as hidden coupling | Med | 1 |
| Ops / latency / cost tradeoffs vs isolation | Med | 1 |

**Weighted sum:** 12  

**Band:** ≥6 high — block expansion of full uniqueness+preferability package.

**Amb ≠ clearance:** Even if C₀ is later named, that poses the uniqueness question; it does not clear **(O)** or **(P)** (LOCK-003).

---

## 5. Higher-Level Review

- [x] Pass with caution  

Overclaim: packages contested uniqueness + normative leap. Silent shift risk: treating real hybrid deployments as pure “microservices alone.”

---

## Final Verdict

- [x] **Provisional** (Amb-blocked)

**Why:** Amb = 12 binding on **(O)/(P)**; Cons soft tension; Agree low. Descriptive contrast nearer L₀. No elevation of “microservices alone avoid cascading failure therefore preferable.”

**Reliability:** Moderate — single-operator short pass; engineering literature large and partisan.

**Imported locks in force as process constraints:** LOCK-2026-08-001…004 (not as domain clearance).
