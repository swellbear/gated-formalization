# Locking Scaffolding — V-COST OR-slot (V-VALUE only)

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Dominant blocker ID(s):** **V-COST**  
**Dependents blocked:** **V-VALUE** (and **V-SRC**)

**Explicit dependency statement:**  
V-VALUE **was** blocked primarily by the unset cost schedule. **V-EITHER is now selected** (`Lock_VCOST_Either.md`). D-SRC stays **unnamed for now** — that does **not** clear D-EXIST or F-SKILL. A cost lock does **not** supply a named recipe; V-VALUE-TEST-0 is **not established** for lack of a specified book.

**Original claim (verbatim, for deviation comparison):**  
Can a predictive model for oil futures be built?

**Operator this turn:** **C** → `lock V-COST either`. Series hunt remains unsubmitted. V-SRC is the live unnamed leftover.

---

## 0. Plain-language framing (required)

**What decision is being made right now:**  
How to count costs when asking whether a paper oil-futures book would have made money after frictions.

**Why this decision is required before further work:**  
Without a cost rule, “after-cost value” can mean “ignore frictions” or “eat realistic slippage,” which are different tests.

**What becomes testable once the decision is made:**  
Whether a **named** specified recipe, on NYMEX CL front-month next-session, walk-forward, beats the curve **after the locked costs**. No recipe is named yet.

**What still cannot be settled by this decision alone:**  
That a model works; that anyone should trade; D-EXIST or F-SKILL. **Amb drop from locking costs ≠ clearance.**

---

## 1. Decision points

| Point ID | Question (plain language) |
|----------|---------------------------|
| **V** (V-COST) | What frictions come out of paper P/L? |

## 2. Options per decision point

### Point V — Cost schedule

| Option ID | What it means in ordinary terms | Provenance |
|-----------|---------------------------------|------------|
| **V1 Fees-only** | Subtract **listed** exchange / clearing / NFA-style fees as published for CL. **No** slippage. | Common backtest; easy to game |
| **V2 Fees + 1 tick/side** | Those listed fees **plus** **1 CL tick slippage each way**. One tick on CL is **$0.01/barrel × 1,000 barrels = $10 per contract** per side (round-turn slippage **$20**/contract before fees). | CME CL tick size; conservative retail-ish friction |
| **V-EITHER** | Formally accept **either** V1 or V2. Later tests must **say which** was used. | Standing OR-slot rule |

**Incoherent / weak:** Inventing a live broker commission in dollars without a named fee schedule; treating V-COST as proof of V-VALUE; using options/OTC oil instead of CL.

---

## 3–5. Ranked packages (most → least powerful for resolving V-VALUE)

### Rank 1 — Fees + 1 tick/side (`V2`)

**What this package concretely means:**  
Paper P/L must survive listed CL fees **and** $10/contract slippage in and $10 out. Harder bar; less “free lunch” from assuming fills at the settlement.

**If chosen, the next phase can check:**  
V-VALUE under V2 **if** a specified recipe/book is named. With no recipe, honest test is **not established**, not a refute of all models.

**It still cannot settle:** Live trading; “should trade”; D-EXIST/F-SKILL.

**Relevance warning:** Adds friction not in the original one-liner (already a Substantial elevation as V-VALUE).

**Objective claim-deviation assessment**  
1. **Strong-language preservation:** Original “can be built” unchanged; V-VALUE stays an elevation.  
2. **Problem-identity check:** Still the Rank 4 value leg, not a new slogan.  
3. **Scope / baseline / metric shift:** Adds 1-tick/side slippage.  
4. **Deviation summary:** **Minimal** vs Rank 4 V-VALUE text; still **Substantial** vs the bare original claim.

---

### Rank 2 — Fees-only (`V1`)

**What this package concretely means:**  
Only published listed fees. Fills assumed at the settlement used in the book. Easier, more gameable.

**If chosen, the next phase can check:**  
V-VALUE under V1 if a recipe is named.

**It still cannot settle:** Slippage; live trading; skill; existence.

**Relevance warning:** Optimistic vs a real fill.

**Objective claim-deviation assessment**  
1. **Strong-language preservation:** Same as Rank 1 on the slogan.  
2. **Problem-identity check:** Same value leg, weaker friction.  
3. **Scope / baseline / metric shift:** Fees without slippage.  
4. **Deviation summary:** **Minimal** vs Rank 4 V-VALUE; **Substantial** vs the bare claim.

---

### Rank 3 — Either (`V-EITHER`)

**What this package concretely means:**  
Both V1 and V2 are allowed. Incomplete as a singleton until a later test picks one or reports both.

**If chosen, the next phase can check:**  
Only after each test names V1 or V2 (or reports both).

**Deviation summary:** **Minimal** vs Rank 4 (explicit OR-slot). Lock of V-VALUE remains **incomplete** as a singleton.

---

## 6. Choice prompt

**Status:** **SELECTED** — **V-EITHER** (operator **C**, 2026-08-17). Lock record: `Lock_VCOST_Either.md`.

**Plain-language card (at selection):**

- **What we’re doing:** Choosing how costs are counted for the after-cost value leg.  
- **What we need from you:** Pick **one** cost rule.  
- **What a “yes” means:** We freeze that friction rule. We do **not** thereby prove a profitable model.  
- **What this does *not* mean:** That anyone should trade; that existence or skill is established; that a recipe has been named.

```
V-COST: V-EITHER — formally accept either V1 or V2
  [ ] V2 — listed fees + 1 tick/side ($10 per side)
  [ ] V1 — listed fees only (no slippage)
  [x] V-EITHER — formally accept either V1 or V2
```

**Details:** `lock V-COST V2` · `lock V-COST V1` · `lock V-COST either` **(selected)**

**Lock-time Amb warning:** Selecting a cost rule typically **drops leftover-ambiguity by fixing meanings**. That drop **does not establish** V-VALUE or the original slogan. **Low Amb after lock ≠ clearance.**

**Lean Default note (not a silent pick):** V2 is the more powerful friction freeze for an investor-relevant paper book. This note did **not** select a package. Operator **C** selected either.

---

## 7. Forced-deviation extraction

**Condition met?** No new FD from this OR-slot alone (V-VALUE was already Substantial vs the original wording).

---

*D-SRC remains unnamed for now. Live ask after V-SRC leave unnamed. Reopen D-SRC with `name source class …` / `leave unnamed` / `endpoint only`.*
