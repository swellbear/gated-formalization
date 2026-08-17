# Gate Scoring Sheet — Cycle 0 (unconstrained slogan)

> **Plain language.** First structured pass on how well-posed and consistent the claim is. A clearer question is not a proved claim.

**Date:** 2026-08-17  
**Application / Claim being scored:** Can a predictive model for oil futures be built?  
**Linked Anchor & Claim-Type sheet:** `01_Anchor_and_ClaimType_Template.md`  

---

## 1. Cons (Consistency)

**In plain language:** Does this reading clash with the starting facts?

**Score:** **High** (compatible as an open feasibility question)

**Notes / contradictions found:**  
Nothing in L₀ rules out writing a forecasting procedure, or rules in a useful/profitable one. Clash appears only if the slogan is *forced* as “already a live trading edge” or as “spot oil, not futures.” Those are over-reads, not Cons failures of the text.

**Compatible with all L₀ anchors and prior admitted layers?**  
- [x] Yes  
- [ ] No — list conflicts:

**Imported locks Cons:** LOCK-003 / 009 / 010 / 011 do not contradict L₀. They constrain how later elevations may be scored.

---

## 2. Agree (Agreement / Stability) — secondary

**In plain language:** Would careful re-readings of the *same* constrained sentence settle on the same meaning?

**Score:** **Low**

**Notes:** Careful readings diverge on whether this is (i) an existence/construction census, (ii) a skill-vs-baseline feasibility claim, or (iii) an after-cost trading-edge claim. “Oil futures,” “predictive,” and “built” each have rival ordinary readings. Fluency of the one-liner is not Agree.

**Needle rule:** Change Agree only when independent careful readings actually converge or diverge on the *same* constrained claim.

---

## 3. Prod (Productivity) — secondary

**In plain language:** Does this claim add new checkable consequences beyond repeating the slogan?

**Number of new, non-trivial, checkable consequences:** **0** (until object, modal bar, contract, horizon, and metric are locked)

**List them:**  
None that do not presuppose still-open free parameters. Candidate consequences (a named mapping exists; a walk-forward RMSE beats last-price; a paper P/L survives costs) each smuggle a different lock.

**Scoring guide reminder:** 0 → fails Prod.

**Needle rule:** Do not invent Prod by listing hoped-for models.

**Primary gates reminder:** Cons, Amb, and redefinition carry the run; Agree and Prod are secondary.

---

## 4. Amb (Ambiguity / Under-determination)

**In plain language:** What leftover choices are still unset? A smaller total means the question is clearer — not that the claim is true.

**Free-parameter list with severity weights:**

| Free Parameter | Severity (High=2 / Med=1 / Low=0.5) | Weight |
|----------------|-------------------------------------|--------|
| **G1** Object: existence/construction vs out-of-sample skill vs after-cost economic value | High | 2 |
| **G2** “Can” modal bar (P-Logical / P-NonNegligible / P-BaseCase) | High | 2 |
| **G3** Contract identity (WTI CL / Brent / unnamed class; which tenor) | High | 2 |
| **G4** Target (settlement price, return, direction-only, curve/spread) | Med | 1 |
| **G5** Horizon (next session, next month, open) | Med | 1 |
| **G6** Success metric + baseline (any mapping vs RMSE/direction vs last price vs futures curve vs after-cost P/L) | High | 2 |
| **G7** Evaluation protocol (in-sample fit vs walk-forward; live series vs stand-in) | Med | 1 |
| **G8** Model class / feature recipe (**G1-dependent** — only well-posed after object + metric lock) | Med | 1 |

**Weighted sum:** **12**

**Interpretation guide:** ≥ 6 → high Amb — block expansion.

**Amb ≠ clearance:** This score measures under-specification. It does **not** mean a predictive oil-futures model is impossible, unwise, or already working.

**Notes:**  
G8 is blocked primarily by G1/G6 (inter-parameter dependency). Rectification: lock a package on G1–G7, then re-open G8 as a scoped technical leftover if the object is skill or value. Existence-object scopes G8 out (any specified mapping counts).

---

## 5. Higher-Level Review

**In plain language:** Is the claim quietly changing meaning or mixing kinds of question?

**Result:**  
- [ ] Pass  
- [x] **Pass with caution**  
- [ ] Fail  

**Notes (overclaim, category error, silent meaning shifts):**  
Category risk: converting “can be built” into “can beat the market,” “can beat the futures curve,” or “should be traded.” Redefinition risk: swapping **futures** for **spot** oil, or “predictive model” for “any script that prints a number,” without saying so. Print-match risk later: a paper that forecasts *spot* WTI, or an in-sample R², is kinship — not bar-met for a locked futures walk-forward test.

---

## Final Verdict

**In plain language:** Gate verdict for the layer as stated — not a press-release “yes.”

- [ ] **Admissible**
- [x] **Provisional** (high Amb 12; object / “can” / success bar unset; Prod 0 until locks)
- [ ] **Not admissible**

**Reliability estimate of this scoring pass:** **High** — this is a structural under-specification finding, not a forecast score and not a model bake-off.  
**Any revisions to earlier layers required?** No.

---

## Next Action

**In plain language:** Name the leftover choices that block a fair test; do not pick the lock silently.

- [ ] Stop / remain provisional  
- [x] Extract gaps and proceed to Gap Extraction & Ranking Sheet  
- [x] Other: **locking-scaffolding** for dominant blockers G1/G2/G6 (contract/horizon ride along). **Stop for operator** on object + modal-bar package pick.
