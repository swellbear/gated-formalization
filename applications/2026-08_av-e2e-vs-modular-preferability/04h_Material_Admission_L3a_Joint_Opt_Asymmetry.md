# Material Admission Check — L3a Differentiable Joint-Opt Asymmetry (weak)

**Date:** 2026-08-11  
**Parent application:** `2026-08_av-e2e-vs-modular-preferability`  
**Targeted gap:** R1  
**Claim-freeze quoted:** Whether, for a specified spectrum pair and ODD/metrics, E2E shows a *relative* closed-loop scaling / joint-optimization advantage vs modular-with-learning (not structural impossibility).

---

## Candidate Material Summary

**Source(s):** Standard differentiable programming / AV stack design; compatible with L1a–L1b.  
**Key content / finding (concise):** Where a modular stack hard-cuts the pipeline with a **non-differentiable** hand-engineered interface, *joint* gradient-based optimization across that cut is unavailable without surrogates, relaxation, or learned interfaces. More fully differentiable E2E (or hybrid) designs can, in principle, jointly optimize across that path. This is a **design asymmetry**, not an empirical proof that E2E achieves better closed-loop scaling under any fixed ODD/metrics.

---

## Admission Criteria

### 1. Relevance to Targeted Gap
- [ ] Yes  
- [ ] No  
- [x] Partially  

**Explanation:** Clarifies a mechanism that *could* underwrite a relative advantage; does not settle whether the advantage obtains for any specified spectrum pair + ODD/metrics (freeze still open empirically).

### 2. Consistency (Cons)
- [x] Yes  
- [ ] No  

**Any conflicts:** None with L1b (modules can still train and improve locally). Does not revive “structurally cannot.”

---

## Admission Decision

- [x] **ADMIT** (weak mechanism / design asymmetry only)  
- [ ] **REJECT**  
- [ ] **HOLD**  

**If admitted, expected effect on Amb:** −0.5 to −1 on R1 mystery; residual Amb remains for whether asymmetry yields net closed-loop gains.  
**If admitted, expected effect on Prod:** Forces future R1 work to state spectrum pair + whether interfaces are differentiable + metrics.

---

## Higher-level review
No silent upgrade from “can jointly optimize across the cut” to “preferable” or “scales better in deployment.”

---

## Residual Judgment Notes
Borderline relevance → admitted only at the weak reading; empirical superiority explicitly not included.
