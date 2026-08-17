# Quantitative Evidence Rubric — proven-only public-series search

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Bar under test (quote freeze):** F-SKILL — walk-forward RMSE vs last-settlement no-change on NYMEX CL front-month **next-session log-return**. Operator filter: submit a class only if **proven**.  
**Source / artifact:** Hunt of EIA STEO methods, Alquist–Kilian / Fed IFDP 1022, and nearby WTI futures-return papers (none submitted as class).

---

| # | Check | Result |
|---|-------|--------|
| 1 | **Sample definition** — series, window, return/quantity concept stated? | **Partial** — candidates state *a* oil price series, usually **spot** or monthly average, not locked CL next-session log-return |
| 2 | **Costs / taxes / frictions** — included, excluded, or N/A (state which)? | **N/A** for F-SKILL RMSE (V-VALUE still OR-slot). Hunt did not score after-cost P/L |
| 3 | **Significance vs point estimate** — test/interval, or point estimate only? | **Test** in Alquist–Kilian / IFDP (MSPE vs no-change) — on **spot**, not this freeze |
| 4 | **Matched comparison** — same locks / same instance on both sides of the bar? | **No** — do **not** collapse to the matching subset (monthly spot MSPE ≠ next-session CL log-return RMSE) |
| 5 | **Sensitivity to sample window** — noted, tested, or untested? | **Noted** in IFDP 1022 (short-horizon futures vs no-change sensitive; 12-month modest/fragile) |
| 6 | **Print-match ≠ clearance** — same print (or subset) treated as kinship, not bar-met? | **Yes** — “futures sometimes help forecast spot” is kinship, not F-SKILL-met |

---

## Already-included legs (mandatory for numerical / workbook bars)

| Leg | In base bar test? | Notes |
|-----|-------------------|-------|
| Last-settlement no-change | Y | F-SKILL **baseline**; operator B: **not** the D-EXIST model |
| Listed futures curve as market prices | Y | L₀; using the curve to forecast **spot** is a **different job** |
| EIA STEO monthly average spot | N | Different object/horizon |
| After-cost P/L | N | V-VALUE; V-COST later either-accepted; unused here |

**If asked “what about the futures curve?”:** Already in L₀ / F-SKILL baseline family — not a proven extra model of next-session CL returns.

---

**Conflicted-source?** Non-conflicted for EIA methods + Fed/JAE evaluations; conflicted vendor/ML pitches unused for affirmation.

**Bar decision supported by this artifact?** **Not establish** (F-SKILL). **Not refute** of all possible recipes. **HOLD/REJECT** as a submitted proven class.

**Establishment-stop drill (if named-class pulse):** Would honest `04` declare established? **No.**

**Comparability note:** Same rubric as other markets numerical bars.

---

*Standing rule: Quantitative evidence quality bar + already-included legs.*
