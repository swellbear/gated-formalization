# R4 Locking Scaffolding — Ranked + Relevance-Annotated Choice Set

**Application:** `2026-08_av-e2e-vs-modular-preferability`  
**Date:** 2026-08-11  
**Status:** AWAITING OPERATOR SELECTION  

**Original claim (core assertions to track for relevance):**  
E2E is **preferable** to modular because E2E **alone** (i) **avoids cascading errors** from hand-engineered interfaces and (ii) **can continue to improve with data/scale** in a way modular stacks **structurally cannot**.

**Dependency:** R1 and R2 are currently blocked primarily by the unset status of R4.  
**Phase 1 already constrained:** “alone,” “avoid cascading (elimination),” and “structurally cannot” are **negatively constrained**. Preferability **(P)** was never entered (R3).

**Global relevance warning:** Every package below reopens **scoped technical dependents** (R1 and/or R2). **None** restores or vindicates the original packaged claim’s strong uniqueness / structural-impossibility / bare preferability assertions. Selecting a package is **not** selecting “prove the original claim.”

---

## Decision points (A–D) — options unchanged

**A** Architecture pair: A1 modular PPC vs neural E2E · A2 modular vs hybrid · A3 hybrid mid-level vs more-E2E · A4 BC-E2E vs modular-learning · A5 other  

**B** ODD: B1 highway · B2 urban robotaxi · B3 campus · B4 suburban · B5 named benchmark-proxy · B6 other  

**C** Metrics: C1 safety proxies · C2 completion · C3 open-loop imitation · C4 comfort · C5 scaling curves · C6 error-budget split · C7 debuggability · C8 other  

**D** Matching: D1 fully matched stacks · D2 public benchmark protocol · D3 closed-loop sim suite · D4 confounded fleet · D5 in-codebase ablation · D6 other  

---

## Ranked packages (most → least powerful for R1/R2) + relevance warnings

### Rank 1 — **P-Strong-Both**
- **Lock:** A3 + (B2 or B1) + C5 > C6 > C1 + D5 (or D1)
- **Power justification:** Tightest matching + direct R1 (C5) and R2 (C6) metrics; lowest confounding.
- **Relevance warning:** **Partial / claim-adjacent.** Tests relative scaling and error-budget magnitudes for a **hybrid vs more-E2E** pair — **not** “alone,” **not** cascading-*elimination*, **not** modular *structural impossibility*, **not** global preferability. Strongest for dependents; **weak overlap with the original slogan’s exclusivity package.**

### Rank 2 — **P1-R1**
- **Lock:** A3 + (B2 or B5-sim) + C5 > C1 + (D5 or D3)
- **Power justification:** Best dedicated R1 reopen (scaling + closed-loop under strong matching).
- **Relevance warning:** **Partial.** Addresses only the *relative* data/scale improvement question (already weaker than “structurally cannot”). Does **not** establish uniqueness, cascading-avoidance-as-elimination, or preferability. R2 untouched unless later extended.

### Rank 3 — **P2-R2**
- **Lock:** A1 + (B1 or B2) + C6 > C1 + (D1 or D3) with dual failure tags
- **Power justification:** Best dedicated R2 reopen (interface vs compounding budgets under matched ODD).
- **Relevance warning:** **Partial / adjacent.** Speaks to error *loci and magnitudes*, not “E2E alone avoids cascading errors.” A1 looks closer to the original binary rhetoric but still cannot revive uniqueness or preferability under Phase 1 locks.

### Rank 4 — **P-Sim-Matched**
- **Lock:** (A1 or A3) + B5-named-sim + (C1 or C2) ± C5 + D3
- **Power justification:** Replicable closed-loop public/sim anchor; good matching; metrics often less direct than C5/C6.
- **Relevance warning:** **Partial.** Sim-ODD results do not license unrestricted real-fleet preferability or the original exclusivity claims.

### Rank 5 — **P3-Benchmark**
- **Lock:** A4 + B5-named-dataset + C3 (± C2) + D2
- **Power justification:** Strong literature substrate; weak alignment with closed-loop R1 freeze; poor for R2.
- **Relevance warning:** **Weak overlap with original claim.** Open-loop imitation success is **not** the original preferability / cascading / structural-scaling package. Tractable but easy to over-read — **do not treat as addressing the original claim.**

### Rank 6 — **P4-Exploratory**
- **Lock:** Any A + any B + C1 + D4
- **Power justification:** Weakest — high confounding; agenda framing only.
- **Relevance warning:** **Weak / non-closing.** Must not be presented as resolving R1/R2 or supporting the original claim.

---

## Operator response template

```
R4 lock selection:
Package: P-Strong-Both / P1-R1 / P2-R2 / P-Sim-Matched / P3-Benchmark / P4-Exploratory

À-la-carte (if not using a package):
- A__  B__  C__>C__>C__  D__

I acknowledge scoped-result honesty: findings under this lock will not be silently promoted to general support for the original claim.
Notes:
```

**Stopped — awaiting your selection.**
