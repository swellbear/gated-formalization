# Material Admission Check — futures-target method map

**Date:** 2026-08-17  
**Parent application:** `2026-08_oil-futures-predictive-model`  
**Targeted gap:** **F-SKILL** / live [R-F-SKILL](RESIDUAL_BRANCH_MENU.md#r-f-skill) — map of published methods whose explicit target is listed crude **futures**  
**Linked:** `03_Gap_Extraction_and_Ranking.md` · `Lock_Rank4_Nested_Split.md` · `Lock_FSRC_Leave_Unnamed.md`  
**Intake:** `E_Package_Evidence_Intake_FT_Method_Map.md`  
**Rubric:** `E_Quantitative_Evidence_Rubric_FT_Method_Map.md`  
**Map:** `MAP_Futures_Target_Forecasting_Methods.md`

**Quote freeze:** F-SKILL = next-session CL front-month log-return, walk-forward RMSE vs last-settlement. D-EXIST-MET-FT already in force (futures-target). F-SRC **leave unnamed** unless the operator names a class.

---

## Candidate Material Summary

**In plain language:** A public census of forecasting papers whose left-hand side is WTI/CL or Brent **futures**, scored against the locked skill test. It is not a new fitted model, and it is not a pick of one paper as “the” skill class.

**Source(s):** Peer-reviewed futures-target evaluations (Chantziara & Skiadopoulos 2008; Coppola 2008; Baruník & Malinská 2016; Kearney & Shang 2020; Bredin et al. 2021) plus recorded OUT families (spot-using-futures; futures **volatility**; one-off ML).

**Key content / finding (concise):**

| Result | Status |
|--------|--------|
| Futures-target recipes exist | Already **D-EXIST-MET-FT** — not re-litigated |
| Freeze-matching next-session log-return RMSE vs last settlement, as a standing series | **Not found** |
| Daily PC forecast of futures **changes** | OOS power **small** (Chantziara) |
| Daily FTS/PC vs RW on generic CL curve | MAE/MCS kinship on 2009–15; direction ~50%; **not** locked RMSE |
| Monthly NS curve forecasts | Different **horizon**; NN edge vs RW **shrinks** at long horizon/maturity |
| NS → holding-period **returns** vs no-change | Authors claim OOS error reduction; **not** confirmed as next-session RMSE |
| VECM vs RW | Authors: OOS win on **1-month futures**, not next session |
| Vol of futures vs RW | Often holds — **wrong object** |

---

## Admission Criteria

### 1. Relevance to Targeted Gap
- [x] Yes — the map is aimed at F-SKILL’s published-method neighborhood  
- [ ] No  
- [x] Partially — several families constrain **nearby** horizons/losses, not every locked slot  

**Explanation:** Relevant as a **negative-plus-kinship census**. Not relevant as silent F-SKILL clearance or as filling F-SRC.

### 2. Consistency (Cons)
- [x] Yes  
- [ ] No  

**Any conflicts:** **Conflict if admitted as F-SKILL-met or as a named F-SRC class.** No conflict if admitted as **L-MAP-FT: map executed, bar not met, class still unnamed.**

---

## Admission Decision

- [x] **ADMIT** the map as evaluation: **L-MAP-FT**  
- [ ] **ADMIT** F-SKILL **established** — **rejected**  
- [x] **REJECT** naming Kearney–Shang / Bredin / Chantziara / Baruník–Malinská / Coppola as the **submitted** F-SRC class on this turn  
- [ ] **HOLD** the map (not run)

**Locked as:** **L-MAP-FT** — census executed; F-SRC remains **unnamed**; F-SKILL **not established** (not a refute).

**Amb effect:** Unchanged at **5.5**. A map is not a named vehicle. **Amb ≠ clearance.**

**Prod effect:** Live residual still the skill test. Operator may `name source class …` or leave unnamed.

---

## Establishment-stop drill (mandatory)

**Would honest `04` declare established?** **No** (F-SKILL).

Do **not** auto-declare a live-shot skill bar because one paper’s one-day MAE beat a random walk on generic CL prices in 2009–15, or because a monthly NS net beat RW at one month. Print-match ≠ clearance. Partial match: every locked slot scored; bar **not** shrunk.

---

## Post-Incorporation Action

- [x] Record map + intake + rubric  
- [x] F-SRC still unnamed  
- [x] Stop for operator — do not invent a class; do not enter Phase 2  

---

## Residual Judgment Notes

- “Oil futures forecasting” in journals usually means **futures → spot** or **vol of futures**. The futures-**target** subset is thin.  
- Closest kinship (Kearney–Shang) is still a **partial** match. Treating it as bar-met would be a silent lock pick.  
- Chantziara’s “little power” is not a refute of the locked protocol.  
- Bredin Sharpe numbers are **not** V-VALUE under V1/V2.

---

*Standing rule: Material admission. Amb drop ≠ clearance. Establishment-stop on would-be-met bars.*
