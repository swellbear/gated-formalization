# Material Admission Check — operator-named D-EXIST suite (establishment-stop)

**Date:** 2026-08-17  
**Parent application:** `2026-08_oil-futures-predictive-model`  
**Targeted gap:** **D-EXIST** / **D-SRC** — specified forecasting mapping for some liquid crude futures, **not** last-settlement no-change as the exhibit  
**Linked:** `03_Gap_Extraction_and_Ranking.md` · `Lock_Rank4_Nested_Split.md`  
**Intake:** `E_Package_Evidence_Intake_D_EXIST_Named_Suite.md`  
**Quote freeze:** Rank 4 D-EXIST `O1+M1+S1+C3+T2+H3+E3`. No-change **OUT** (operator B).

---

## Candidate Material Summary

**Source(s):** Operator (2026-08-17), answering the existence leftover by naming a suite of fully specified recipes and explicitly setting last-price / end-of-period no-change aside as the exhibit.

**Key content / finding:**

| ID | Named lineage | Freeze vs C3 (WTI/Brent **futures** as object) | Role if used |
|----|---------------|-----------------------------------------------|--------------|
| **S-CURVE** | Futures-curve recipes (raw quote, Nelson–Siegel fill, end-of-period vs average; optional inflation adjust when targeting **real** price) | **Match** when the forecast target is **futures**. **Nearby** when the target is **spot** (Alquist–Kilian / IFDP kinship already hunted) | Specified mapping |
| **S-VAR** | Oil-market VAR / BVAR (Baumeister–Kilian lineage: real oil price, activity, production, inventories; lag 12; expanding/rolling; SV/quantile extensions) | **Nearby** in the canonical real/**spot** target. **Match** only for a stated **futures-target** variant | Specified mapping for *oil prices*; not automatically C3 |
| **S-CRACK** | Product-spread / crack-spread regressions on real oil price or futures | **Partial** — spot-spread → real price is nearby; futures-left-hand-side would match if named | Specified mapping |
| **S-ENS** | Ensemble of AR/ARMA/ARIMA / SES / Holt / Holt–Winters with named combination rules | **Unnamed singleton** until a public paper + **series** (CL vs spot) is singled | Specified *style*; vehicle fork |
| **S-ARGUS** | Commercial forward-curve fill (liquid quotes → gap fill → no-arbitrage strip) | Operator already: **valuation/curve**, not a pure forecast of future realisations | Specified **procedure**; weak as “predictive model” exhibit |

**Operator caveats (recorded, not used to erase existence):** no recipe dominates every horizon/sample; short-horizon often favours futures-based or simple bivariate methods; correctly built no-change remains a hard benchmark; many published improvements shrink under that benchmark; residual judgment in model selection, vintages, and loss. Those are **F-SKILL / V-VALUE** facts.

**Does not claim here:** F-SKILL-met. V-VALUE-met. Trading advice.

---

## Admission Criteria

### 1. Relevance
- [x] Yes — this is a D-EXIST exhibit class, and it respects no-change **OUT**
- [x] Partially — much of the suite targets **real/spot** oil, which is not C3 unless the freeze is widened

**Explanation:** Relevant as existence of **written recipes**. Not relevant as silent F-SKILL clearance. Not relevant as “oil in general” replacing **futures**.

### 2. Cons
- [x] Yes — if admitted as a named-suite census and/or as D-EXIST-met **only** on a freeze-matching futures-target exhibit  
- [ ] No if admitted as F-SKILL-met, V-VALUE-met, or as C3 while treating spot VARs as the same object

**Any conflicts:** Clash with L₀ and with **L-HUNT-PROVEN** if futures-as-spot-forecast papers are relabeled as next-session CL skill. No clash with L₀ if existence of specified mappings is all that is claimed.

---

## Admission Decision

- [x] **ADMIT** as **named-suite census** (D-SRC is a menu, not blank; no-change remains OUT)  
- [ ] **ADMIT** D-EXIST **established** — **withheld** (establishment-stop; vehicle fork)  
- [ ] **ADMIT** F-SKILL **established** — **rejected** (operator’s own benchmark caveats; hunt already not-established)  
- [x] **REJECT** collapsing spot/real-price lineages into C3 without an operator freeze change  
- [x] **REJECT** Argus-style fill as the D-EXIST **predictive** exhibit (operator already distinguished)  
- [ ] **HOLD** the naming (not received)

**Locked as:** **L-D-SUITE** — operator named a suite; **D-EXIST not auto-established**.

**Amb effect:** **Unchanged 7.5.** A menu is not a singleton. Leave-unnamed on V-SRC already taught: naming/leaving a vehicle without a singled freeze-match does not drop Amb. **Amb ≠ clearance.**

---

## Establishment-stop drill (mandatory)

**Would honest `04` declare established?** **Yes** — on D-EXIST as written — **if** the operator singles (or formally accepts as either) at least one **fully specified, futures-target, non-no-change** recipe as the exhibit.

Under S1 + M1 + C3, “a codeable mapping whose object is listed WTI or Brent futures already exists in the literature/toolkits” is the existence bar. The operator’s futures-curve-as-forecast-of-**futures** clause is that exhibit. Skipping the drill because the suite is mixed is not the method. **Hit case → stop.** Do **not** auto-declare bar-met.

**Would honest `04` declare F-SKILL established?** **No.** Operator caveats + **L-HUNT-PROVEN**. Print-match of nearby spot results ≠ F-SKILL-met.

---

## Post-Incorporation Action

- [x] Intake recorded  
- [x] **Stop for operator** — authorize D-EXIST-met on the futures-target subset, keep census-only, or widen the object to include spot/real-price recipes (a freeze change)  
- [ ] Do not enter Phase 2  
- [ ] Do not implement a trading model

---

## Residual Judgment Notes

- Operator B already refused the cheap no-change exhibit. This suite is the stricter *kind* of exhibit they asked for. That does not license auto-clearance.  
- “Specified” ≠ “beats no-change.” The operator said both; keep both.  
- Commercial curve methodologies can exist as written procedures without being predictive models of future realisations.
