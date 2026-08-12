# Locking Scaffolding — Dominant Blocker Choice Set

**Date:**  
**Application:**  
**Dominant blocker ID(s):**  
**Dependents blocked:**  

**Explicit dependency statement:**  

**Original claim (verbatim, for deviation comparison):**



---

## 0. Plain-language framing (required)

**What decision is being made right now:**  

**Why this decision is required before further work:**  

**What becomes testable once the decision is made:**  

**What still cannot be settled by this decision alone:**  

---

## 1. Decision points
| Point ID | Question (plain language) |
|----------|---------------------------|
|          |                           |

## 2. Options per decision point
*(Prefer literature / benchmarks / deployed systems. Plain language first.)*

### Point __
| Option ID | What it means in ordinary terms | Provenance |
|-----------|---------------------------------|------------|
|           |                                 |            |

---

## 3–5. Ranked packages (most → least powerful)

### Rank __ — Package name: ________

**What this package concretely means:**  
*(baseline, what counts, how strict / how gameable)*  

**If chosen, the next phase can check:**  

**It still cannot settle (vs original claim):**  

**Relevance warning (if partial/weak overlap):**  

**Objective claim-deviation assessment** *(compare to original claim wording only)*  
1. **Strong-language preservation:**  
2. **Problem-identity check:**  
3. **Scope / baseline / metric shift:**  
4. **Deviation summary:** Minimal deviation / Moderate deviation / Substantial deviation / Problem substitution  

*(Repeat for each ranked package.)*

---

## 6. Choice prompt

**Plain-language card (fill before the code block):**

- **What we’re doing:** Choosing how to fix meanings so the next tests are fair and clear.  
- **What we need from you:** Pick **one** package (or list à-la-carte options).  
- **What a “yes” means:** We freeze those definitions and only then check evidence under them.  
- **What this does *not* mean:** Picking a package does **not** prove the original claim; it only sets the grading rules. (Lower ambiguity after a lock ≠ clearance.)

Pick **one** package by **ordinary name**, **or** list à-la-carte option IDs.

```
Package: ________

OR à-la-carte:
- Point __ = Option __
- ...

OR-slots (required if any alternatives remain):
  - [ ] Pick single: ____
  - [ ] Formally accept either: { ____ , ____ }
```

**Details (secondary):** package IDs / option codes as listed above.

**Dependents may re-open only after selection + OR-slot resolution/acceptance.**

**Lock-time Amb warning (mandatory):**  
Selecting a package typically **drops Amb by fixing meanings**. That Amb drop does **not** establish the original claim or any locked upside/evaluative bar. **Low Amb after lock ≠ clearance.**

---

## 7. Forced-deviation extraction (mandatory if no Minimal-deviation package)

**Condition met?** Every realistic package is Moderate deviation or higher (no Minimal deviation): Yes / No  

If **Yes**:
1. **Extracted terms/clauses that force deviation:**  
2. **Record as under-specified or over-strong in the claim as written:**  
3. **Carry forward IDs for claim-freeze / research agenda:**  
4. **Closeout note (draft):** these terms could not be tested in non-derivative form; that is a property of the claim text relative to available anchors/tools, not merely temporary lack of data.

---

*Domain-general template. See `.cursor/rules/applications-gated-method.mdc`.*
