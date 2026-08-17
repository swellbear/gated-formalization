# Quantitative Evidence Rubric — futures-target method map

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Bar under test (quote freeze):** F-SKILL — walk-forward RMSE vs last-settlement no-change on NYMEX CL front-month **next-session log-return**.  
**Source / artifact:** `MAP_Futures_Target_Forecasting_Methods.md` (L-MAP-FT)

---

| # | Check | Result |
|---|-------|--------|
| 1 | **Sample definition** — series, window, return/quantity concept stated? | **Partial** — nearest papers state generic CL or NYMEX/IPE crude futures and a window; **not** locked settlement-to-settlement next-session **log-return** as the reported series |
| 2 | **Costs / taxes / frictions** — included, excluded, or N/A (state which)? | **N/A** for F-SKILL RMSE. Bredin Sharpe / trading rules **excluded** from this bar (V-VALUE; V1/V2 unused) |
| 3 | **Significance vs point estimate** — test/interval, or point estimate only? | **Test** in Kearney–Shang (MCS) and Baruník–Malinská (MCS); Chantziara qualitative “small power”; Coppola OOS vs RW; Bredin “significantly reduce” vs no-change (from abstract) |
| 4 | **Matched comparison** — same locks / same instance on both sides of the bar? | **No** — do **not** collapse to MAE-beat-RW (2009–15), monthly NS RMSE, or 1-month VECM. Score every locked slot |
| 5 | **Sensitivity to sample window** — noted, tested, or untested? | **Noted** — Kearney–Shang 250/500/750-day OOS; Baruník–Malinská edge **shrinks** at long horizon/maturity; Chantziara little power across markets |
| 6 | **Print-match ≠ clearance** — same print (or subset) treated as kinship, not bar-met? | **Yes** — “FTS MAE < RW” and “NN 1-month RMSE < RW” are kinship, not F-SKILL-met |

---

## Already-included legs (mandatory for numerical / workbook bars)

| Leg | In base bar test? | Notes |
|-----|-------------------|-------|
| Last-settlement no-change | Y | F-SKILL **baseline**; not the D-EXIST model |
| Listed futures curve as L₀ prices | Y | Using the curve to forecast **spot** is a different job (OUT) |
| Daily PC / FTS / monthly NS / VECM as **existence** | Y | Already inside D-EXIST-MET-FT / L-D-SUITE |
| Futures **volatility** HAR/GARCH | N | Different object |
| After-cost P/L / Sharpe | N | V-VALUE |

**If asked “what about Kearney–Shang beating the random walk?”:** Already in this rubric as **partial kinship** — not an omitted F-SKILL pass.

---

**Conflicted-source?** Non-conflicted for the peer-reviewed families; conflicted ML/GitHub unused for affirmation.

**Bar decision supported by this artifact?** **Not establish** (F-SKILL). **Not refute** of all recipes. **HOLD/REJECT** as a submitted F-SRC class.

**Establishment-stop drill (if named-class pulse):** Would honest `04` declare established? **No.**

**Comparability note:** Same rubric as L-HUNT-PROVEN. This map **adds futures-target cards**; it does not reverse the hunt’s “no freeze-matching proven series submitted.”

---

*Standing rule: Quantitative evidence quality bar + already-included legs.*
