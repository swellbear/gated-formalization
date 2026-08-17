# Package-Satisfying Evidence Intake — proven-only public-series search

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Locked package / scope label:** **Under Rank 4 (D-EXIST ⊂ F-SKILL ⊂ V-VALUE) only**  
**Target dependent(s):** D-SRC / F-SKILL (operator: search now; **submit only if a proven oil-futures forecaster**)  
**Named-class pulse?** Attempted hunt — **No class submitted** (filter not met)

---

## 0. Named-class pulse

| Check | Value |
|-------|--------|
| Freeze line (quoted) | **F-SKILL:** real shot a specified recipe beats last-settlement RMSE, walk-forward, NYMEX **CL front-month**, **next-session log-return**. **D-EXIST:** named forecast recipe **other than** last-settlement no-change (operator B). Operator this turn: submit a class **only if proven**. |
| Named source class (specific series + matching locks) | **None submitted.** “Some papers” / “EIA STEO” / “the futures curve” / Alquist–Kilian evaluations **fail matching locks** and/or the proven filter. |
| Named enough? | **No** for a freeze-matching proven series — **stop** (`name source class …` still available; this hunt does not invent one) |
| Non-circular? | Search is not the Rank 4 brochure. Using **NYMEX last settlement as the model** would be circular with the F-SKILL baseline / operator B. |
| Schema match | **No** for every candidate vs F-SKILL (see §1). Partial kinship on nearby **spot / monthly** questions is **not** collapsed to bar-met. |
| Conflicted-source flag completed (§2)? | Yes |
| **Establishment-stop drill:** Would honest `04` declare **established**? | **No** (F-SKILL). **No** (D-EXIST as *proven*). If a later honest `04` would say established → stop; this hunt does not. |

---

## 1. Lock schema (must match freeze)

| Slot | Required by lock | Value in hunted artifacts |
|------|------------------|---------------------------|
| Object | Forecast **CL futures** next-session **log-return** | Typical literature: **spot** WTI/Brent, or monthly average, or using futures to forecast **spot** |
| Baseline | Last-settlement **no-change** (RMSE) | Often no-change of **spot**; or random walk of monthly price |
| Horizon | **Next session** | Usually 1–12 **months** |
| Protocol | Walk-forward OOS | Mixed; many in-sample or one-off papers |
| “Proven” | F-SKILL **met** (operator filter) | **Not shown** on matching slots |
| D-EXIST exhibit | Named recipe ≠ no-change | EIA STEO is a recipe but **spot/monthly**; operator forbade submit unless proven |

**Schema match?** **No** — do not collapse the bar to “someone forecast oil prices.”

---

## 2. Artifact summary

**Source / citation (hunt, not submitted as class):**

1. **EIA Short-Term Energy Outlook (STEO)** — [EIA crude-oil price forecast handbook](https://www.eia.gov/analysis/handbook/pdf/STEO_Crude_Oil_Price.pdf): monthly average **Brent and WTI spot** forecasts (pooling + regression + analyst judgment). Live STEO pages compare WTI **spot** to a NYMEX **futures curve** as a comparator, not as a scored CL next-session RMSE bake-off.  
2. **Alquist & Kilian (2010)** / **Alquist, Kilian & Vigfusson, Fed IFDP 1022 (2011)** — oil **futures as forecasts of future spot**; often **not** more accurate than no-change in MSPE, especially short horizons; modest/sensitive gains at ~12 months in some updates.  
3. One-off academic papers on WTI **futures returns** / ML (e.g. term-structure / LSTM writeups) — **not** a standing public series; mixed OOS; not named-enough in the SPF sense.

**What it reports:** Nearby oil-price forecastability is a live research topic. That is **kinship**, not freeze-met.

**Sample / setup limits:** Horizons, spot vs futures, monthly vs daily, and “futures as predictor of spot” vs “model of next CL return” do not match.

### Conflicted-source flag (mandatory)
- [x] **Non-conflicted** for EIA handbook + Fed/JAE academic evaluations (disinterested public research / official outlook methods)  
- [x] **Conflicted / interest-aligned** — **Other:** vendor/ML “beat the market” writeups and unpaid strategy pitches — **not** used as sole affirmation  

**If conflicted:** not used to affirm P-NonNegligible / proven.

### Quantitative bar?
Yes — F-SKILL RMSE vs last-settlement. Rubric: `E_Quantitative_Evidence_Rubric_Proven_Search.md`.

---

## 3. Provisional gate intent (before full `04`)
- [ ] Aim **ADMIT** as constraining the dependent under this package  
- [x] Aim **HOLD** / **REJECT as submitted class** — no proven freeze-matching series to name  
- [x] Aim **REJECT** (fails matching locks for “proven oil futures forecaster”)

**ADMIT bar for this freeze:** A **named public series** whose published central evaluation **matches every F-SKILL slot** and would support proven skill vs last-settlement next-session CL log-return.  
**HOLD bar:** Nearby spot/monthly kinship without collapsing slots.  
**REJECT triggers:** Schema No; operator proven-filter fail; inventing a class; print-match.

---

## 4. Scoped-result honesty
Findings, if admitted, hold **under:** this hunt only — **no class named**.  
**Partial / claim-adjacent?** Yes — literature on **spot** oil and **futures-as-spot-forecast** is adjacent.  
**Must not be promoted to:** D-EXIST established; F-SKILL established; V-VALUE; “should trade”; EIA STEO as a proven CL next-session model.

---

*Standing rule: package evidence intake + named-class pulse. Print-match ≠ clearance.*
