# Material Admission Check — proven-only public-series hunt

**Date:** 2026-08-17  
**Parent application:** `2026-08_oil-futures-predictive-model`  
**Targeted gap:** D-SRC / F-SKILL — operator authorized a search and **only submitting if it is a proven oil futures forecaster**  
**Linked:** `03_Gap_Extraction_and_Ranking.md` · `Lock_Rank4_Nested_Split.md`  
**Intake:** `E_Package_Evidence_Intake_Proven_Search.md`  
**Rubric:** `E_Quantitative_Evidence_Rubric_Proven_Search.md`

**Quote freeze:** F-SKILL = next-session CL front-month log-return, walk-forward RMSE vs last-settlement. D-EXIST exhibit ≠ that no-change baseline (operator B). This hunt’s submission filter = **proven** (F-SKILL-met), not mere existence of an outlook page.

---

## Candidate Material Summary

**Source(s):** Public web hunt 2026-08-17 (EIA STEO methods handbook; Alquist & Kilian 2010 / Fed IFDP 1022; nearby WTI futures-return / ML papers). No new proprietary dataset.

**Key content / finding (accuracy-first):**

| Candidate | What it is | Freeze match | Proven on F-SKILL? | Submit as class? |
|-----------|------------|--------------|--------------------|------------------|
| EIA STEO | Standing public **monthly average spot** Brent/WTI outlook | **No** (spot, monthly, judgment mix) | **No** | **No** |
| NYMEX / CL curve | Listed futures prices (already L₀) | Curve-as-spot-forecast ≠ next-session CL **return** vs last settlement | **No** (would smuggle the baseline / a different job) | **No** |
| Alquist–Kilian / IFDP 1022 | Public **evaluation** of futures as **spot** forecasts vs no-change | **No** (spot; monthly horizons; mixed/short-horizon fail) | **No** | **No** (an evaluation paper is not a proven forecaster series) |
| One-off WTI futures-return / ML papers | Scattered OOS claims | **Partial** object at best; not a standing named series | **Not established** on locked slots | **No** |

**Not refute:** This hunt does **not** say no model could ever beat last-settlement on the locked protocol. It says **no freeze-matching proven public series was found to submit.**

---

## Admission Criteria

### 1. Relevance to Targeted Gap
- [x] Yes — the hunt was aimed at D-SRC / proven F-SKILL  
- [ ] No  
- [x] Partially — artifacts constrain **nearby** spot/monthly questions  

**Explanation:** Relevant as a **negative search**. Not relevant as a silent swap to “spot oil is somewhat forecastable some years.”

### 2. Consistency (Cons)
- [x] Yes  
- [ ] No  

**Any conflicts:** **Conflict if admitted as proven class / F-SKILL-met / D-EXIST-met.** No conflict if admitted as **search executed, no class submitted.**

---

## Admission Decision

- [x] **ADMIT** the hunt as evaluation: **no proven freeze-matching public series submitted**  
- [ ] **ADMIT** F-SKILL **established** — **rejected**  
- [ ] **ADMIT** D-EXIST **established** via EIA STEO — **rejected** (spot/monthly; fails proven filter; operator B wants a predictive model, not any outlook)  
- [x] **REJECT** naming EIA STEO / NYMEX curve / Alquist–Kilian as the **submitted** class under this filter  
- [ ] **HOLD** the hunt (not run)

**Locked as:** **L-HUNT-PROVEN** — search executed; D-SRC remains **unnamed**; F-SKILL **not established**.

**Amb effect:** Unchanged at **9**. **Amb ≠ clearance.**

**Prod effect:** Proven-filter hunt is executed, not pending. Remaining: operator may still `name source class …` (weaker than proven), `leave unnamed`, or move to V-COST.

---

## Establishment-stop drill (mandatory)

**Would honest `04` declare established?** **No** (F-SKILL). **No** (D-EXIST as proven).

Do **not** auto-declare a live-shot skill bar because some paper beat a random walk on **spot** or at **12 months**. Print-match ≠ clearance. Partial match: every locked slot scored; bar **not** shrunk.

---

## Post-Incorporation Action

- [x] Record hunt (`E_Package_Evidence_Intake_Proven_Search.md` + rubric)  
- [x] D-SRC still unnamed (operator proven-filter; none submitted)  
- [x] Stop for operator — do not invent a class

---

## Residual Judgment Notes

- “Oil futures” in the literature usually means **using futures to forecast spot**, not a model of **next CL return**. That is problem substitution if smuggled as F-SKILL.  
- EIA STEO is a real public forecasting **product** (existence kinship) and still **fails** the operator’s **proven** filter and the CL next-session freeze.  
- Conflicted ML/vendor bake-offs were not used to affirm.
