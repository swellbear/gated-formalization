# Map — published methods whose target is listed crude **futures**

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Layer ID:** **L-MAP-FT** (evaluation census — not F-SKILL-met; not a named F-SRC class)  
**Freeze quoted:** Rank 4 **F-SKILL** = NYMEX **CL front-month**, **next-session log-return**, walk-forward **RMSE vs last-settlement no-change**. C3 either-accepted: WTI **or** Brent futures as a class.  
**Scope:** **Under Rank 4 only.** Existence (**D-EXIST-MET-FT**) stays separate. This map does **not** fill F-SRC. Do **not** invent a class.

**Glossary:** [`docs/READER_GLOSSARY.md`](../../docs/READER_GLOSSARY.md)

---

## 0. Plain-language framing

**What we’re doing:** Listing published forecasting recipes whose **left-hand side is a listed crude futures price** (WTI/CL or Brent), and scoring them against the locked skill test: next-session or one-step **log-return** versus last settlement, under a proper walk-forward.

**What this settles:** A census of what has actually been evaluated on futures (not spot). Which claimed edges survive walk-forward, which shrink, and which slots of the skill freeze remain untested.

**What this does *not* settle:** That skill is established or refuted. That anyone should trade. That a nearby MAE or monthly holding-period result is the locked RMSE bar. Spot/real-price papers stay outside existence.

**Honesty:** Print-match ≠ clearance. Partial match: every locked slot scored; the bar is **not** shrunk to the matching subset.

---

## 1. How to read the freeze (one line)

Last settlement as a **no-change** forecast of tomorrow’s CL (or Brent) **log-return** is the baseline. A published method counts as a freeze **match** only if it forecasts that same object, on a walk-forward, with RMSE (or an equivalent squared-error loss) against that baseline.

Most of the oil-forecasting literature does a **different job**: it uses the futures **curve as an input** to forecast **spot** or **real** oil. Those papers are kinship, already hunted, and stay **OUT** of this map’s “match” column.

---

## 2. Index of families (futures-target only)

| ID | Family | Typical target | Next-session / one-step **log-return vs last settlement**? | Walk-forward vs no-change | Reported edge vs no-change | Freeze vs F-SKILL |
|----|--------|----------------|-------------------------------------------------------------|---------------------------|----------------------------|-------------------|
| **M-DAILY-PC** | Daily term-structure PCs | Daily **changes** of NYMEX / IPE crude futures | **Partial** (daily futures changes; not locked log-return RMSE) | Yes (OOS) | **Shrinks / little power** | Nearby — **not a match** |
| **M-DAILY-FTS** | Functional curve + expanding window | Daily generic **CL1–CL18** prices / log-returns | **Partial** (one-day-ahead CL1 included; MAE/MASE, not locked RMSE) | Yes (expanding, daily re-estimate) | In-sample MAE beats RW; OOS FTS in MCS superior set; **direction ~50%** | Closest kinship — **not freeze-met** |
| **M-NS-M** | Nelson–Siegel + AR/NN on the **monthly** curve | Constant-maturity WTI **futures prices**, 1–12 **months** ahead | **No** (monthly, multi-month horizon) | Mixed (OOS / MCS vs RW) | Authors: NN beats AR/VAR/RW at 1-month on RMSE; gains **fade** at long maturity / long horizon | Schema fail on H1 |
| **M-NS-RET** | NS factors → **holding-period futures returns** | WTI futures returns vs no-change | **Unconfirmed as next-session** (range of horizons / maturities; typical design is holding-period, not session) | Yes (OOS vs no-change claimed) | Authors: error reduction vs no-change; Sharpe claims are **V-VALUE-adjacent**, not the RMSE bar | Partial / nearby |
| **M-VECM** | Spot–futures cointegration | 1-month futures (and spot) **price movements** | **No** (1-month, mixed spot) | Yes vs random walk | Authors: VECM beats RW **in-sample strongly; OOS on 1-month futures** | Nearby — different horizon |
| **M-AFFINE** | Gibson–Schwartz / Cortazar–Schwartz | Today’s curve / valuation | **No** (fit, not next-session return skill) | Usually in-sample fit | Fit quality ≠ walk-forward log-return skill | Existence kinship only |
| **M-VOL** | GARCH / HAR-RV on **futures** | **Variance** of futures, not the mean return | **No** (wrong object) | Often rolling OOS vs RW on **vol** | Vol edges often **hold** OOS vs RW-on-variance | **OUT** of F-SKILL |
| **M-ML-1** | One-off LSTM/ARIMA / GitHub | Often unlabeled “WTI” (spot or futures) | Usually **No** | Often a single 70/30 split, not walk-forward vs last settlement | Mixed; conflicted; not a standing series | **Not submitted** (same as L-HUNT-PROVEN) |

**Spot / real-price recipes (Alquist–Kilian; IFDP 1022; Baumeister–Kilian; EIA STEO; closing-price no-change for *average spot*):** **OUT** of this map’s match column. Already recorded as nearby. Short-horizon futures-as-spot often **fails** no-change; that is not this freeze.

---

## 3. Cards (what was actually evaluated)

<a id="m-daily-pc"></a>
### M-DAILY-PC — Chantziara & Skiadopoulos (2008)

| Field | Content |
|-------|---------|
| **Cite** | Chantziara, T., Skiadopoulos, G., 2008. *Energy Economics* 30(3), 962–985. |
| **Object** | Daily evolution of the **term structure of petroleum futures**: NYMEX crude, heating oil, gasoline; **IPE crude** (Brent lineage). |
| **Method** | Principal components of the curve; also univariate / VAR. Forecast **subsequent daily changes** of futures prices. |
| **Walk-forward / OOS** | Yes — in-sample **and** out-of-sample. |
| **Vs last settlement / no-change** | Compared with standard time-series benchmarks; authors’ own conclusion is **small forecasting power** both in- and out-of-sample. |
| **Holds or shrinks** | **Shrinks to little / none.** Spillover across products is detected; that is not next-session CL log-return skill. |
| **Freeze slots** | C3 **partial** (NYMEX crude + IPE crude). H1 **partial** (daily, not locked “next-session log-return”). E1 walk-forward **yes**. S2 RMSE-vs-settlement **not the reported loss**. |
| **Must not be promoted to** | F-SKILL-met. “Brent is forecastable daily.” |

<a id="m-daily-fts"></a>
### M-DAILY-FTS — Kearney & Shang (2020)

| Field | Content |
|-------|---------|
| **Cite** | Kearney, F., Shang, H.L., 2020. *European Financial Management* 26(1), 238–257. (working paper: QUB / arXiv:1901.02248) |
| **Object** | Daily CME generic **CL1–CL9, CL12, CL18**, Jan 2009–Dec 2015. Explicit **futures** curve, not spot. |
| **Method** | Functional time series (exponential smoothing on functional PCs). Benchmarks: Chantziara-style discrete PCs; Andreasson-style macro factors; **random walk without drift**. |
| **Walk-forward / OOS** | **Expanding window, re-estimated daily.** Training through Dec 2013; 500-day OOS (also 250 / 750 as robustness). |
| **Vs last settlement / no-change** | RW without drift is the naïve price benchmark; MASE scales OOS error by **in-sample** RW. Loss: **MAE** (and MME, directional MCPDC), not locked **RMSE on log-return**. |
| **Holds or shrinks** | **In-sample:** PC/FTS/Fund MAE beat RW (overall MAE 0.0129 vs RW 0.0188). Directional hit rate **~52–54%** — barely above a coin. **OOS:** authors report FTS in the Hansen MCS superior set for one-day-ahead curve forecasts. Direction remains near 50% on CL1 in the OOS excerpt (~0.55 FTS vs ~0.51 PC vs ~0.46 Fund — not a stable directional edge). |
| **Freeze slots** | C3 **yes** (CL front / generics). H1 **partial** (one-day-ahead, not quoted as settlement-to-settlement **log-return** RMSE). E1 **yes** (expanding daily). Window **narrow** (2009–15). Not a standing public series. |
| **Must not be promoted to** | F-SKILL-met. “MAE beat RW in 2009–15” ≠ locked RMSE bar. MCS on curve MAE ≠ next-session log-return skill. |

<a id="m-ns-m"></a>
### M-NS-M — Baruník & Malinská (2016) and DNS kin

| Field | Content |
|-------|---------|
| **Cite** | Baruník, J., Malinská, B., 2016. *Applied Energy* 164, 366–379 (arXiv:1504.04819). Kin: Grønborg & Lunde (CREATE 2013-36) DNS on oil futures; Hevia / Garratt-style NS **fill** of missing futures used inside **spot** combinations. |
| **Object** | NYMEX WTI **futures** term structure. Baruník–Malinská: **monthly** closing prices, cubic-spline constant maturities, 1990–2014. |
| **Method** | Dynamic Nelson–Siegel factors; forecast factors with focused time-delay neural net vs AR(1) / VAR(1) / **random walk**. |
| **Walk-forward / OOS** | OOS + Hansen MCS. Horizons: **1, 3, 6, 12 months** — not next session. |
| **Holds or shrinks** | Authors: FTDNN lowest average RMSE at 1-month (4.40 vs AR 4.71 vs RW 4.77). At **longer maturities and longer horizons**, AR and even RW **re-enter** the MCS — the edge **shrinks**. |
| **Freeze slots** | C3 **yes** (WTI futures). H1 **no**. One-step here means **one month**. |
| **Must not be promoted to** | Next-session CL skill. NS-as-missing-value-fill in Baumeister-style **spot** combinations is a **different job**. |

<a id="m-ns-ret"></a>
### M-NS-RET — Bredin, O’Sullivan & Spencer (2021)

| Field | Content |
|-------|---------|
| **Cite** | Bredin, D., O’Sullivan, C., Spencer, S., 2021. *Energy Economics* 100, 105350. Working paper: “Information in the Term Structure of WTI Crude Oil Futures,” SSRN 3547395. |
| **Object** | **WTI futures holding-period returns**; NS factors from the WTI curve. |
| **Method** | NS (including time-varying decay); LASSO with macro and oil-market predictors. Benchmark: **no-change**. |
| **Walk-forward / OOS** | Authors: OOS exercises; error reduction vs no-change “across a range of return horizons and futures contract maturities.” |
| **Holds or shrinks** | **Claimed to hold** vs no-change in the authors’ OOS. They also report trading-rule Sharpe vs buy-and-hold / historical mean — that is **not** the F-SKILL RMSE bar (and is V-VALUE-adjacent; costs not the locked V1/V2). |
| **Freeze slots** | C3 **yes**. H1 **not shown as next-session** from the public abstract/WP summary (horizons described as a **range**, with extra in-sample gains at **medium** horizon). Full daily settlement-to-settlement RMSE table was **not** independently re-scored here (SSRN body gated). |
| **Must not be promoted to** | F-SKILL-met. Sharpe ≠ RMSE vs last settlement. Naming this paper as “the” class would still be an operator pick. |

<a id="m-vecm"></a>
### M-VECM — Coppola (2008)

| Field | Content |
|-------|---------|
| **Cite** | Coppola, A., 2008. *Journal of Futures Markets* 28(1), 34–56. |
| **Object** | Oil **spot and futures** movements via cost-of-carry cointegration. |
| **Method** | VECM; random walk benchmark. |
| **Walk-forward / OOS** | Yes. Authors: VECM **outperforms RW out-of-sample for 1-month futures** price movements; in-sample futures information explains a sizable share of moves. |
| **Holds or shrinks** | **Holds in that paper** at the **1-month futures** horizon vs RW; not scored here as next-session log-return RMSE. |
| **Freeze slots** | C3 **partial** (1-month futures). H1 **no**. Mixed spot–futures object. |
| **Must not be promoted to** | Next-session CL skill. |

<a id="m-affine"></a>
### M-AFFINE — Schwartz / Cortazar–Schwartz (valuation)

| Field | Content |
|-------|---------|
| **Cite** | Gibson & Schwartz (1990); Schwartz (1997); Cortazar & Schwartz (2003), *Energy Economics* 25, 215–238. |
| **Object** | Listed oil **futures curve** as a function of latent spot / convenience yield / long-term return. |
| **Job** | **Fit and value** today’s curve (and options). Not a published next-session log-return bake-off vs last settlement. |
| **Freeze** | D-EXIST kinship (a specified mapping exists). F-SKILL **untested** on these models as return forecasts. |

<a id="m-vol"></a>
### M-VOL — futures **volatility** (not the return)

| Field | Content |
|-------|---------|
| **Cite** | Sadorsky (2006); Sévi (2014) *EJOR*; HAR-RV extensions (Haugom et al.; Degiannakis–Filis). |
| **Object** | Variance / realized vol of **crude oil futures** (often front-month WTI). |
| **Vs RW** | GARCH/HAR-type forecasts often **beat a random walk on volatility** out of sample. Sévi: jump/semivariance decompositions **help in-sample and shrink OOS**. |
| **Freeze** | **Wrong object.** Vol skill is not F-SKILL (mean next-session log-return RMSE). |

---

## 4. What remains untested (on the locked skill freeze)

These slots were **not** found as a freeze-matching published evaluation:

1. **NYMEX CL front-month**, **next-session log-return**, walk-forward **RMSE vs last settlement**, as a standing public series (not a one-off notebook).  
2. The same protocol on **ICE Brent** front-month settlement log-return. IPE daily *curve-change* tests (M-DAILY-PC) are the nearest Brent kinship and reported **little OOS power**.  
3. **Replication** of M-DAILY-FTS outside 2009–2015, on settlement log-return RMSE rather than curve MAE/MASE.  
4. **M-NS-RET** re-scored at **h = 1 session** (if the authors’ “range of horizons” even includes it).  
5. Any of the above with **V1 or V2** costs (that is V-VALUE, still unnamed).

**Not untested:** That futures-target **recipes exist** (D-EXIST-MET-FT). That no-change is a hard short-horizon benchmark in the **spot** literature. That **volatility** of oil futures is somewhat forecastable.

---

## 5. Establishment-stop drill

**Would honest `04` declare F-SKILL established on this map?** **No.**

Closest kinship (M-DAILY-FTS) is still a **partial** schema match. Scoring every slot and refusing to collapse the bar to “one-day CL MAE beat RW in 2009–15.” Print-match ≠ clearance.

**Would honest `04` declare F-SKILL refuted?** **No.** M-DAILY-PC’s “little power” is not a refute of every later protocol. Leave-unnamed ≠ unlikely.

**F-SRC:** stays **unnamed**. This menu is not a silent pick of Kearney–Shang or Bredin as “the” class.

---

## 6. Operator decision log

| Date | Action |
|------|--------|
| 2026-08-17 | Operator asked for a map of published **futures-target** methods, focused on next-session / one-step log-return vs last settlement, walk-forward hold-or-shrink, and untested slots. Recorded as **L-MAP-FT**. F-SKILL **not established**. F-SRC **not filled**. |

---

*Evaluation census under Rank 4. Not trading advice. Not blended-slogan clearance.*
