# Locking Scaffolding — G1 / G2 / G6 (contract, horizon, metric ride along)

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Dominant blocker ID(s):** **G1** object · **G2** “can” · **G6** success metric/baseline  
**Dependents blocked:** **G3** contract · **G4** target · **G5** horizon · **G7** protocol · **G8** model class (G1/G6-dependent)

**Explicit dependency statement:**  
G8 and any architecture or literature census are currently blocked primarily by the unset status of G1 and G6. G3–G7 stay under-determined largely because G1 is free: an existence job does not need a tight metric; a skill or value job does. Rectification: lock a coherent package below, then re-open only in-scope dependents.

**Original claim (verbatim, for deviation comparison):**  
Can a predictive model for oil futures be built?

---

## 0. Plain-language framing (required)

**What decision is being made right now:**  
Choosing what “can,” “predictive model,” and “oil futures” mean so the next test is one question, not three.

**Why this decision is required before further work:**  
Without that freeze, a Python script, a famous oil-price paper, and a trading desk P/L can all be waved as “yes” or “no” at different jobs.

**What becomes testable once the decision is made:**  
Only the job in the chosen package — existence census, skill vs a named baseline, or after-cost value — on a named contract and window.

**What still cannot be settled by this decision alone:**  
That anyone should trade; that this repo will implement a model; that a clearer question is a proved claim. Locking only makes the sentence **gradable**. **Amb drop ≠ clearance.**

---

## 1. Decision points

| Point ID | Question (plain language) |
|----------|---------------------------|
| **O** (G1) | What job is the sentence doing? |
| **M** (G2) | How strong is “can”? |
| **S** (G6) | What counts as “predictive”? |
| **C** (G3) | Which listed oil-futures contract? |
| **T** (G4) | What number is forecast? |
| **H** (G5) | By when does the print count? |
| **E** (G7) | How is the test scored? |

## 2. Options per decision point

*(Prefer literature / benchmarks / deployed systems. Plain language first.)*

### Point O — Job (object)

| Option ID | What it means in ordinary terms | Provenance |
|-----------|---------------------------------|------------|
| **O1 Existence** | A specified forecasting mapping for some oil-futures price can be written, or already has been. | Literal “can be built” |
| **O2 Skill** | A mapping that beats a named naive baseline out of sample on a locked contract/window. | Ordinary reading of “predictive” as having forecast skill |
| **O3 Value** | A mapping that would have produced economic value after costs (paper or live). | Trading-desk reading; **not in the sentence** |

### Point M — “Can”

| Option ID | What it means in ordinary terms | Provenance |
|-----------|---------------------------------|------------|
| **M1 P-Logical** | Not a contradiction — a very low bar, often near-empty if unbounded. | Weak modal |
| **M2 P-NonNegligible** | A real, not-tiny feasibility shot — still not “this is the expected path.” | Ordinary “can we actually do this?” |
| **M3 P-BaseCase** | The expected/central path is that such a model works. | Stronger than “can” |

### Point S — Success / “predictive”

| Option ID | What it means in ordinary terms | Provenance |
|-----------|---------------------------------|------------|
| **S1 Any mapping** | A specified input→forecast recipe counts, even if it does not beat a baseline. | Construction reading |
| **S2 vs last price** | Out-of-sample RMSE (and optionally direction) **beats no-change / last settlement**. | Standard naive oil/asset baseline |
| **S3 vs curve** | Beats the listed futures curve as the market’s own forecast. | Stronger finance test |
| **S4 After-cost P/L** | Positive paper economic value after costs/slippage on a locked book. | Trading test |

### Point C — Contract

| Option ID | What it means in ordinary terms | Provenance |
|-----------|---------------------------------|------------|
| **C1 WTI front-month** | NYMEX Light Sweet Crude Oil futures (**CL**), **front-month** settlements, roll-aware. | Most-cited US crude futures object |
| **C2 Brent** | ICE Brent crude futures, front-month, roll-aware. | Global benchmark rival |
| **C3 Class** | Any liquid crude-oil futures as a class (WTI or Brent). | Closest to unnamed “oil futures” |

### Point T — Target

| Option ID | What it means in ordinary terms | Provenance |
|-----------|---------------------------------|------------|
| **T1 Log-return** | Next-horizon log return of consecutive front-month settlements (roll-aware). | Standard return target |
| **T2 Price level** | Next-horizon settlement **price**. | Level forecast |
| **T3 Direction** | Up vs down only. | Weaker / more gameable |

### Point H — Horizon

| Option ID | What it means in ordinary terms | Provenance |
|-----------|---------------------------------|------------|
| **H1 Next session** | Forecast issued using information available before the next daily settlement. | Short-horizon skill test |
| **H2 Next month** | One calendar-month ahead on the locked contract. | Common energy-outlook horizon |
| **H3 Open** | No deadline. | Couples with M1 toward vacuity |

### Point E — Evaluation

| Option ID | What it means in ordinary terms | Provenance |
|-----------|---------------------------------|------------|
| **E1 Walk-forward** | Out-of-sample walk-forward (or expanding window) on official settlements; in-sample fit **does not** meet the bar. | Anti-overfit |
| **E2 In-sample OK** | A fit on the same sample used to build the model counts. | Cheap; usually not “predictive” |
| **E3 Census only** | No numeric bake-off; ask whether a specified public forecasting product/recipe exists. | Existence job |

**Incoherent / weak combos (do not package as top ranks):**  
O1+S4 (existence scored as trading P/L); O2+S1 (skill job with no skill metric); O3+E3 (value job with census-only scoring); **O1+O2+O3 as one object** (three jobs blended into a single yes/no — **not** a legal “either” OR-slot); M1+H3+S1 (near-vacuous); swapping **spot** WTI for futures without marking a claim revision; treating EIA/IEA **spot or average-price** outlooks as automatically meeting a **CL futures** freeze (print-match ≠ clearance).

**Combination repair (not a blend):** A+B+C may be locked only as **named nested legs** (Rank 4 / Rank 4-AC). “Formally accept either” is for true alternatives (e.g. WTI or Brent on a census), **not** for treating existence, skill, and trading-value as one claim.

---

## 3–5. Ranked packages (most → least powerful for resolving dependents)

### Rank 1 — Locked-skill feasibility (`O2+M2+S2+C1+T1+H1+E1`)

**What this package concretely means:**  
Ask whether there is a **real (not-tiny) shot** that a **fully specified** forecasting recipe can be built that, on **NYMEX CL front-month** **next-session log returns**, **walk-forward**, **beats last-settlement / no-change on RMSE** (direction accuracy may be reported; it does not replace RMSE). “Built” = specified mapping + training/evaluation rule, not a live desk, and not “this chat implements it.”

**If chosen, the next phase can check:**  
Whether a **named** public evaluation (once the operator names a source class) meets or misses that bar — or whether the bar is not established. In-sample R² and spot-oil papers do not automatically count.

**It still cannot settle (vs original claim):**  
After-cost trading value; beating the futures curve; that one *should* trade; that a model will work next week.

**Relevance warning:** Partial — adds contract, horizon, RMSE-vs-last-price, and walk-forward **not in the claim text**. This is what makes “predictive” testable without swapping in a trading book.

**Objective claim-deviation assessment** *(compare to original claim wording only)*  
1. **Strong-language preservation:** “Can” kept as a real-shot feasibility bar (not “will” / not “should”). “Predictive model” kept but **operationalized**. “Oil futures” narrowed to CL front-month. “Built” kept as specification/construction, not live deployment.  
2. **Problem-identity check:** Same family (feasibility of a forecasting model for oil futures). Not a trading-P/L substitution.  
3. **Scope / baseline / metric shift:** Adds CL, next-session log-return, RMSE vs last price, walk-forward.  
4. **Deviation summary:** **Moderate deviation**

**OR-slots:** none — complete singleton. (Brent would be a different package / later residual.)

---

### Rank 2 — After-cost value vs the curve (`O3+M2+S4+C1+T1+H1+E1`, curve as already-included competitor)

**What this package concretely means:**  
Ask whether there is a **real shot** that a specified recipe would have produced **positive paper economic value after costs** on **CL front-month**, next-session, walk-forward — with the listed curve / no-change as the competitor the book must beat, not a silent extra leg.

**If chosen, the next phase can check:**  
A locked paper-trading protocol (costs/slippage must be named before any establish/refute admit). Conflicted vendor backtests cannot solely affirm the bar.

**It still cannot settle:** That live trading would work; that one should trade; existence of *some* model.

**Relevance warning:** **Weak overlap** with bare “can a model be built.” This is the interesting finance question and a **different job**.

**Objective claim-deviation assessment**  
1. **Strong-language preservation:** “Can” kept as real-shot; “built” shifted toward **deployable edge**. “Predictive” replaced by **after-cost value**.  
2. **Problem-identity check:** **Substitutes** a trading-edge question for construction/feasibility.  
3. **Scope / baseline / metric shift:** Adds costs, P/L, curve competitor.  
4. **Deviation summary:** **Substantial deviation** / borderline **problem substitution**

**OR-slots if selected:** cost schedule must be singled (e.g. stated round-turn + slippage) or formally “either” accepted before dependents proceed.

---

### Rank 3 — Existence census (`O1+M1+S1+C3+T2+H3+E3`)

**What this package concretely means:**  
Ask only whether a **specified** forecasting mapping for **some liquid crude-oil futures** (WTI or Brent as a class) **can be written or already exists**. No skill bake-off. “Can” = not a contradiction.

**If chosen, the next phase can check:**  
A census of named public forecasting products/recipes aimed at crude futures (not a silent spot swap). Likely **near-vacuous**: such recipes exist as a class of artifacts; that does **not** show skill or value.

**It still cannot settle:** Whether any model is useful, beats last price, beats the curve, or should be traded.

**Relevance warning:** Closest to the **words**; weakest as a **test**. High risk of a cheap “yes” that drops “predictive” as success.

**Objective claim-deviation assessment**  
1. **Strong-language preservation:** “Can be built” kept weak; “predictive” reduced to job-description (a model whose task is forecasting). “Oil futures” kept as a class.  
2. **Problem-identity check:** Same proposition as the bare sentence (construction/existence).  
3. **Scope / baseline / metric shift:** Minimal; leaves horizon/metric open by design.  
4. **Deviation summary:** **Minimal deviation**

**OR-slots:** C3 “either WTI or Brent as class” is **formally accepted either** inside this package (existence for the class, not a bake-off on one ticker).

---

### Rank 4 — Nested split A+B+C (`D-EXIST` ⊂ `F-SKILL` ⊂ `V-VALUE`)

**What this package concretely means:**  
Keep all three jobs **on the record**, scored **separately**. Do not collapse them into one yes.

| Leg | Everyday job | Mechanics (from Ranks 3 / 1 / 2) |
|-----|----------------|----------------------------------|
| **D-EXIST** | Can a forecasting recipe be written / already exist? | Rank 3: `O1+M1+S1+C3+T2+H3+E3` |
| **F-SKILL** | Real shot it beats last-price RMSE, walk-forward, CL front-month, next session? | Rank 1: `O2+M2+S2+C1+T1+H1+E1` |
| **V-VALUE** | Real shot of after-cost paper value vs the curve on the same CL next-session book? | Rank 2: `O3+M2+S4+C1+T1+H1+E1` |

**Already-included legs (mandatory):** D-EXIST sits inside F-SKILL (a skill test needs a specified mapping). F-SKILL sits inside V-VALUE (a value test needs a forecast rule). Asking “what about existence?” after a skill miss does **not** reopen a missing census — it is already a separate leg.

**If chosen, the next phase can check:**  
Each leg on its own freeze. A later `04` may establish, leave open, or refute **one** leg without moving the others.

**It still cannot settle (vs original claim):**  
That the bare one-liner is a single cleared “yes.” That anyone should trade. Cost schedule for V-VALUE still an OR-slot.

**Relevance warning:** D-EXIST is the wording-faithful core. F-SKILL operationalizes “predictive.” V-VALUE is a **marked elevation**, not the original sentence.

**Objective claim-deviation assessment**  
1. **Strong-language preservation:** “Can be built” preserved on D-EXIST. “Predictive” preserved as F-SKILL. Trading-value is **added**, not read back into the slogan.  
2. **Problem-identity check:** Same family **only if** D-EXIST remains the claim-under-test and F-SKILL / V-VALUE stay labeled elevations. Blending three yeses into one slogan would be problem substitution.  
3. **Scope / baseline / metric shift:** Adds CL skill protocol and a costed book as extra legs.  
4. **Deviation summary:** **Per leg** — D-EXIST Minimal · F-SKILL Moderate · V-VALUE Substantial / elevation. Package as a whole is a **split**, not a new blended slogan.

**OR-slots:** V-VALUE cost schedule must be **singled** or formally “either” accepted before that leg’s dependents proceed. D-EXIST and F-SKILL have no extra OR-slots (C3 either-class is inside D-EXIST only).

**Lock-time honesty:** Establishing D-EXIST does **not** establish F-SKILL or V-VALUE. Failing V-VALUE does **not** refute D-EXIST. Amb drop from naming three legs ≠ clearance of any leg.

---

### Rank 4-AC — Nested split A+C only (`D-EXIST` ⊂ `F-SKILL`; V-VALUE out)

**What this package concretely means:**  
Same as Rank 4 **without** the trading-value elevation. Existence census plus locked-skill feasibility. After-cost P/L stays **out of package** unless a later residual is authorized.

**If chosen, the next phase can check:**  
D-EXIST and F-SKILL only.

**It still cannot settle:** After-cost value; “should trade.”

**Relevance warning:** Drops B (Rank 2). That is a scope choice, not a finding that value is false.

**Objective claim-deviation assessment**  
1. **Strong-language preservation:** “Can” + “predictive” kept as two legs; no trading smuggle.  
2. **Problem-identity check:** Same family as the original plus the Rank 1 operationalization.  
3. **Scope / baseline / metric shift:** Same as Rank 1 on the skill leg; census kept separate.  
4. **Deviation summary:** **Minimal** on D-EXIST; **Moderate** on F-SKILL.

**OR-slots:** none.

---

## 6. Choice prompt

**Plain-language card (fill before the code block):**

- **What we’re doing:** Choosing how to fix meanings so the next tests are fair and clear.  
- **What we need from you:** Pick **one** package (or list à-la-carte options).  
- **What a “yes” means:** We freeze those definitions and only then check evidence under them.  
- **What this does *not* mean:** Picking a package does **not** prove the original claim; it only sets the grading rules. (Lower ambiguity after a lock ≠ clearance.)

**Status:** **SELECTED** — Rank 4 (operator **A**, 2026-08-17). **D-EXIST established (futures-target only)** (`Lock_D_EXIST_Established_Futures_Target.md`). V-COST either. V-SRC leave unnamed. F-SKILL/V-VALUE **not established**. Live ask: F-SRC.

```
Package: Rank 4 — Nested split A+B+C (D-EXIST ⊂ F-SKILL ⊂ V-VALUE)

OR-slots (required if any alternatives remain):
  - [ ] Pick single: V-COST ____
  - [x] Formally accept either: { V1 fees-only , V2 fees + 1 tick/side }
  - [ ] OPEN: V-VALUE cost schedule (V-COST)
```

**Details (secondary):** `lock Rank 4` · `lock Rank 4-AC` · `lock Rank 1` · `lock Rank 2` · `lock Rank 3` · `no lock yet`

**Lean Default note (not a silent pick):** If the operator wants A, B, and C **all on the record**, Rank 4 is the only coherent combination (split, not blend). Rank 4-AC is the combination without the trading substitution. Singleton Ranks 1–3 remain available. This note does **not** select a package.

**Dependents may re-open only after selection + OR-slot resolution/acceptance.**

**Lock-time Amb warning (mandatory):**  
Selecting a package typically **drops Amb by fixing meanings** (job, “can,” contract, metric, horizon). **That Amb drop does not establish** the original claim or any locked feasibility/skill/value bar. **Low Amb after lock ≠ clearance.**

---

## 7. Forced-deviation extraction (mandatory if no Minimal-deviation package)

**Condition met?** Every realistic package is Moderate deviation or higher (no Minimal deviation): **No**

Rank 3 / D-EXIST is **Minimal deviation**. Rank 1 / F-SKILL is Moderate. Rank 2 / V-VALUE is Substantial / elevation. Rank 4 does **not** erase those per-leg labels.

No FD carry-forward is required by the “no Minimal package” rule. If Rank 1, 2, 4, or 4-AC is selected, scoped-result honesty still applies: findings hold **under the chosen leg/package**, not as unrestricted support for the bare one-liner.

---

*Domain-general template. See `.cursor/rules/applications-gated-method.mdc`.*
