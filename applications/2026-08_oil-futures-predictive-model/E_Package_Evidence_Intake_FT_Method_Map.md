# Package-Satisfying Evidence Intake — futures-target method map

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Locked package / scope label:** **Under Rank 4 (D-EXIST ⊂ F-SKILL ⊂ V-VALUE) only**  
**Target dependent(s):** **F-SKILL** / live leftover [R-F-SKILL](RESIDUAL_BRANCH_MENU.md#r-f-skill) — operator asked for a **map**, not `name source class …`  
**Named-class pulse?** **No** — census of published families; F-SRC remains unnamed

---

## 0. Named-class pulse

| Check | Value |
|-------|--------|
| Freeze line (quoted) | **F-SKILL:** NYMEX CL front-month, next-session **log-return**, walk-forward RMSE vs last-settlement no-change (`O2+M2+S2+C1+T1+H1+E1`). C3 either WTI or Brent futures. |
| Named source class (specific series + matching locks) | **Unnamed.** Map is a **menu of families**, not one series. |
| Named enough? | **No** for a pulse. If No → do not auto-pulse a bar-met call. Census still runs as evaluation. |
| Non-circular? | Yes vs Rank 4 brochure. Not last-settlement no-change as the *model*. |
| Schema match | **Partial** overall. Closest kinship: Kearney–Shang (2020) daily CL generics, expanding-window one-day-ahead vs RW. Still not locked RMSE-on-log-return. |
| Conflicted-source flag completed (§2)? | Yes |
| **Establishment-stop drill:** Would honest `04` declare **established**? | **No.** If **Yes → stop.** Score the honest `04`, not “MAE lined up.” |

Do **not** invent a class (do not silently pick Kearney–Shang or Bredin as F-SRC).

---

## 1. Lock schema (must match freeze)

| Slot | Required by lock | Value in this artifact |
|------|------------------|------------------------|
| Object (C1 / C3) | NYMEX CL front-month (WTI or Brent as class) | Several papers use generic CL1 or NYMEX/IPE crude futures; many others use **spot** (OUT) |
| Horizon (H1) | Next-session | Daily one-step in M-DAILY-*; **monthly / multi-month** in M-NS-M; holding-period **range** in M-NS-RET |
| Metric (S2) | Walk-forward **RMSE** vs last settlement | MAE/MASE/MCS/MSPE/Sharpe in the nearest papers — **not** the locked loss |
| Protocol (E1) | Walk-forward | Expanding daily (Kearney–Shang); OOS (Chantziara, Coppola, Baruník–Malinská); often 70/30 in ML one-offs |
| Baseline | Last-settlement no-change | RW / no-change present in the nearest papers |
| Modal height | P-NonNegligible skill | Not scored to met |

**Schema match?** **Partial** — score every slot; do **not** collapse the bar to the matching subset.

---

## 2. Artifact summary

**Source / citation:** Public literature census 2026-08-17. Primary map: `MAP_Futures_Target_Forecasting_Methods.md`. Key futures-target cites: Chantziara & Skiadopoulos (2008); Coppola (2008); Baruník & Malinská (2016); Kearney & Shang (2020); Bredin, O’Sullivan & Spencer (2021). Volatility and spot-using-futures families recorded as OUT / nearby.

**What it reports:** Published methods whose **explicit target is listed crude futures** exist (already D-EXIST). Evaluations of **next-session log-return RMSE vs last settlement** as a freeze-matching standing series were **not** found. Daily curve papers either report **little OOS power** (PCs) or **MAE/MCS edges** on a 2009–15 window with directional accuracy near 50% (FTS). Monthly NS papers are a **different horizon**. Vol papers are a **different object**.

**Sample / setup limits:** No new proprietary bake-off. Bredin et al. full daily RMSE table not re-scored (SSRN body gated); scored from published abstract/WP summary only.

### Conflicted-source flag (mandatory)
- [x] **Non-conflicted** — peer-reviewed academic evaluations (Chantziara, Coppola, Baruník–Malinská, Kearney–Shang, Bredin)
- [x] **Conflicted / interest-aligned** — **Other:** GitHub / vendor / one-off ML notebooks — usable as design kinship only, **not** sole F-SKILL affirmation (same rule as L-HUNT-PROVEN)

**If conflicted:** May support scenario presence / design kinship. Must **not** solely affirm P-NonNegligible.

### Quantitative bar?
**Yes, attempted vs F-SKILL.** Rubric: `E_Quantitative_Evidence_Rubric_FT_Method_Map.md`. Result: **not establish**.

---

## 3. Provisional gate intent (before full `04`)

- [x] Aim **ADMIT** as **evaluation census** (L-MAP-FT) constraining what has been tested  
- [ ] Aim **ADMIT** F-SKILL **established** — **rejected**  
- [x] Aim **REJECT** naming any family as the submitted F-SRC class on this turn  
- [ ] Aim **HOLD** the census (it ran)

**ADMIT bar for this freeze:** A freeze-matching named series + honest established still stops.  
**HOLD bar:** n/a for the census itself.  
**REJECT triggers:** Collapsing MAE/MCS/Sharpe/spot-MSPE into F-SKILL-met; inventing a class.

---

## 4. Scoped-result honesty

Findings, if admitted, hold **under:** Rank 4; this map’s family IDs; futures-target only.  
**Partial / claim-adjacent?** Yes — daily MAE vs RW; monthly NS RMSE; 1-month VECM; vol vs RW.  
**Must not be promoted to:** F-SKILL established; V-VALUE; “should trade”; blended slogan; F-SRC = Kearney–Shang.

---

## 5. Next

Stop for operator on whether to **leave F-SRC unnamed** (map only) or **`name source class …`** for a later pulse. Naming ≠ bar-met. Do not enter Phase 2. Do not invent a class.

---

*Standing rule: Package-satisfying evidence intake. Print-match ≠ clearance. Establishment-stop drill required.*
