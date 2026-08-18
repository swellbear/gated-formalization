# Thesis Tracker (Layer 2)

**Per-application status card.** Working copy while the run is open; mandatory complete at closeout.

**Application:** `2026-08_oil-futures-predictive-model`  
**Last reviewed:** 2026-08-17  
**Status:** **Stable Provisional (split) — hard stop (residuals live)** · Phase 1 closeout · D-EXIST-MET-FT · **F-SRC-CME-TAPE** · **L-SCREEN-Y-PROMOTE** · L-SESS  

**Tags** (see `docs/TRACKER_TAXONOMY.md`):  
- Domain: `markets`  
- Claim-shape: `forecast-extension`, `descriptive-census`  
- Pattern: `R-dependence` (V-VALUE ← V-SRC; F-SKILL ← horse vs Yahoo stand-in under **L-SCREEN-Y-PROMOTE**)

---

## 1. Claim

**Original (verbatim):**

Can a predictive model for oil futures be built?

**Successor / Rank lock (if any):** **Rank 4** nested split — D-EXIST ⊂ F-SKILL ⊂ V-VALUE. **D-EXIST-MET-FT**. V-COST **V2**. **F-SRC-CME-TAPE**. **L-SCREEN-Y-PROMOTE**. V-SRC leave unnamed. CR **declined**, not run; default keep original wording.

**Parent / successor relationship:** none

---

## 2. Verdict and Amb path

**Verdict:** **Stable Provisional (split) — hard stop (residuals live)** — D-EXIST established (futures-target only); F-SKILL and V-VALUE not

**Amb path (brief):** 12 → 9 → 7.5 → 5.5 after D-EXIST-MET-FT → 2.5 after F-SRC-CME-TAPE → 1.5 after L-STANDIN-Y-CLF → **1.0** after V-COST-V2

**Amb ≠ clearance:** Amb 1.0 is V-SRC only. Naming V2 does not mean a model made money after costs. A stand-in baseline does not mean a model beats last price.

---

## 3. Established

- L₀ market-structure anchors.
- Rank 4 **meanings** (not slogan clearance).
- **L-HUNT-PROVEN** (search executed; no proven class submitted).
- V-COST **either** — **superseded** 2026-08-17 as singleton by **V-COST-V2**.
- **V-COST-V2** — listed fees + 1 tick/side ($10/contract/side); not V-VALUE-met.
- V-SRC **leave unnamed** (vehicle sealed empty; not a refute).
- F-SRC **leave unnamed** — **superseded** 2026-08-17 by **F-SRC-CME-TAPE**.
- **F-SRC-CME-TAPE** — named CME official open/settle + R1; optional FTS.
- **L-PULSE-TAPE-0** — live-tape pulse executed; RMSE not computed.
- **L-SCREEN-Y-PROMOTE** — Yahoo screen; live CME only if F-CC beats 0 on last 500 and does not lose on 250/750; H-LAG does not promote.
- **L-MAP-FT** — futures-target method census executed (evaluation; not F-SKILL-met; not a class pick).
- **L-MAP-DRV** — mover-list census executed (exhaustive next-session list **does not exist**; not F-SKILL-met; not a class pick).
- **L-SESS** — night/day/combo protocol locked (meanings; not skill-met).
- **L-MAP-SESS** — overnight/day literature kinship (USO half-hour ≠ F-ON/F-DAY).
- **D-EXIST-MET-FT** — specified non-no-change mapping for listed crude **futures** exists (menu ≠ singleton; spot/real-price OUT).

---

## 4. Not established / negatively constrained

- F-SKILL **not established** (H-LAG-WF lost on F-CC; H-KS not run; not a refute of all recipes).
- F-ON / F-DAY / F-CC **H-LAG** last 500: 0.01283 / 0.02670 / 0.02888 vs 0-forecast 0.01291 / 0.02663 / 0.02869; **not** skill-met.
- Kearney–Shang optional re-score **not run**.
- V-VALUE **not established** (V-VALUE-TEST-0; V-SRC `leave unnamed`; **V2 named**; not a refute of all books).
- Directional accuracy after costs / decision or trading value **not shown**.
- Spot/real-price recipes as inside D-EXIST — **OUT**.
- Blended slogan — **not cleared**.
- No trading advice.

---

## 5. Forced deviations

None required (D-EXIST remains Minimal). V-VALUE is a marked elevation (Substantial), not FD-extraction of the slogan.

---

## 6. Residuals that would reopen the case

| ID | Residual | Concrete reopen condition |
|----|----------|---------------------------|
| [R-D-EXIST](RESIDUAL_BRANCH_MENU.md#r-d-exist) | D-EXIST exhibit | **Executed → admitted** (futures-target). Reopen only if freeze changes (e.g. include spot) |
| [R-HUNT](RESIDUAL_BRANCH_MENU.md#r-hunt) | Proven F-SKILL class hunt | **Executed → not established** |
| [R-MAP](RESIDUAL_BRANCH_MENU.md#r-map) | Futures-target published-method map | **Executed → evaluation** (L-MAP-FT). Does not fill F-SRC |
| [R-DRV](RESIDUAL_BRANCH_MENU.md#r-drv) | Exhaustive mover-list census | **Executed → evaluation** (L-MAP-DRV). Exhaustive list absent; does not fill F-SRC |
| [R-SESS](RESIDUAL_BRANCH_MENU.md#r-sess) | Night vs day vs whole-trip protocol | **Executed → admitted meanings** (L-SESS). Does not meet skill |
| [R-V-VALUE-TEST-0](RESIDUAL_BRANCH_MENU.md#r-v-value-test-0) | Named after-cost book | **Executed → not established** |
| [R-F-SKILL](RESIDUAL_BRANCH_MENU.md#r-f-skill) | Named class for F-SKILL (F-CC + F-ON/F-DAY exhibits) | **H-LAG-WF** scored, **lost** on F-CC. Does **not** promote. H-KS not run. **not established**. Reopen: other horse on Yahoo |
| [R-LIVE-STANDIN](RESIDUAL_BRANCH_MENU.md#r-live-standin) | Live CME vs stand-in | **Executed** (Yahoo `CL=F` stipulated). Reopen live **only if** **L-SCREEN-Y-PROMOTE** fires |
| [R-F-COMBO](RESIDUAL_BRANCH_MENU.md#r-f-combo) | Named switching rule | **park-until-trigger**. Rule in advance; F-ON and F-DAY already scored separately |
| [R-V-VALUE](RESIDUAL_BRANCH_MENU.md#r-v-value) | Named recipe/book for V-VALUE | **Leave unnamed**. `park-until-trigger`. Reopen: `name source class …` matching V-VALUE **under V2** |
| [R-G8](RESIDUAL_BRANCH_MENU.md#r-g8) | Model class under F-SKILL | **Executed → admitted meanings** (baseline + optional FTS) |

---

## 7. Action implications

**Stop saying:** That EIA STEO or the futures curve is a proven next-session CL model; that spot/12-month results clear this freeze; that anyone should trade; that existence-met is skill-met; that one paper was picked as “the” recipe; that unnamed skill means no model can beat last price.

**Keep saying:** A specified non-no-change futures-target recipe has been written. Yahoo is a **stand-in**; the baseline is **not** a pass. Screen on Yahoo; live CME only if the whole-trip gate fires. Paper costs are **V2**; that is not a value pass. Skill and after-cost value are not established.

**Test next (only if authorized):** `leave skill not shown` · `name horse …` on Yahoo. Live CME only if the F-CC promotion gate fires.

---

## 8. Exhibits

- `01_Anchor_and_ClaimType_Template.md`
- `02_Gate_Scoring_Sheet.md`
- `02_Gate_Scoring_After_Rank4.md`
- `03_Gap_Extraction_and_Ranking.md`
- `04_Material_Admission_D_EXIST_Construction.md`
- `Lock_Rank4_Nested_Split.md`
- `R_Locking_Scaffolding.md`
- `MULTI_ELEVATION_SPLIT.md`
- `04_Material_Admission_Proven_Class_Search.md`
- `E_Package_Evidence_Intake_Proven_Search.md`
- `V_COST_OR_Slot.md`
- `Lock_VCOST_Either.md`
- `Lock_VCOST_V2.md`
- `04_Material_Admission_VCOST_V2.md`
- `02_Gate_Scoring_After_V2.md`
- `02_Gate_Scoring_After_VCOST.md`
- `04_Material_Admission_V_VALUE_No_Recipe.md`
- `Lock_VSRC_Leave_Unnamed.md`
- `02_Gate_Scoring_After_VSRC_Unnamed.md`
- `E_Package_Evidence_Intake_D_EXIST_Named_Suite.md`
- `04_Material_Admission_D_EXIST_Named_Suite.md`
- `Lock_D_EXIST_Established_Futures_Target.md`
- `04_Material_Admission_D_EXIST_Established.md`
- `02_Gate_Scoring_After_DEXIST.md`
- `Lock_FSRC_Leave_Unnamed.md`
- `02_Gate_Scoring_After_FSRC_Unnamed.md`
- `MAP_Futures_Target_Forecasting_Methods.md`
- `E_Package_Evidence_Intake_FT_Method_Map.md`
- `E_Quantitative_Evidence_Rubric_FT_Method_Map.md`
- `04_Material_Admission_FT_Method_Map.md`
- `02_Gate_Scoring_After_FT_Map.md`
- `MAP_What_Can_Move_CL.md`
- `E_Package_Evidence_Intake_FT_Driver_Map.md`
- `E_Quantitative_Evidence_Rubric_FT_Driver_Map.md`
- `04_Material_Admission_FT_Driver_Map.md`
- `02_Gate_Scoring_After_FT_Driver_Map.md`
- `Lock_Session_Split.md`
- `MAP_Session_Split.md`
- `E_Package_Evidence_Intake_Session_Split.md`
- `E_Quantitative_Evidence_Rubric_Session_Split.md`
- `04_Material_Admission_Session_Split.md`
- `Lock_FSRC_Named_CME_Tape.md`
- `PULSE_Baseline_Session_RMSE.md`
- `E_Package_Evidence_Intake_FSRC_Named.md`
- `E_Quantitative_Evidence_Rubric_FSRC_Named.md`
- `04_Material_Admission_FSRC_Named.md`
- `02_Gate_Scoring_After_FSRC_Named.md`
- `Lock_Standin_Yahoo_CLF.md`
- `PULSE_Standin_Yahoo_CLF_RMSE.md`
- `E_Package_Evidence_Intake_Standin_Yahoo.md`
- `E_Quantitative_Evidence_Rubric_Standin_Yahoo.md`
- `04_Material_Admission_Standin_Yahoo.md`
- `02_Gate_Scoring_After_Standin_Yahoo.md`
- `Lock_Screen_Yahoo_Promote.md`
- `04_Material_Admission_Screen_Promote.md`
- `02_Gate_Scoring_After_Screen_Promote.md`
- `Lock_Standin_Yahoo_Curve.md`
- `PULSE_Horses_Standin.md`
- `04_Material_Admission_Horses.md`
- `02_Gate_Scoring_After_Horses.md`
- `data/horse_scores.json`
- `data/clf_yahoo_month_chain.csv`
- `05_Original_Claim_Assessment_Closeout.md`
- `DISSERTATION.md`
- `SHARE_PACK.md`
- `EXECUTIVE_BRIEF.md`
- `RESIDUAL_BRANCH_MENU.md`
- `OPTIONAL_MODES_MENU.md`
- `final_verdict.md`

---

## 9. Pointers

- Dissertation: [`DISSERTATION.md`](DISSERTATION.md)
- Closeout / verdict: [`05_Original_Claim_Assessment_Closeout.md`](05_Original_Claim_Assessment_Closeout.md) · [`final_verdict.md`](final_verdict.md)
- Share pack: [`SHARE_PACK.md`](SHARE_PACK.md)
- Parent / successor: —
- Key admissions / locks: Rank 4; **D-EXIST-MET-FT**; **V-COST-V2**; **F-SRC-CME-TAPE**; **L-STANDIN-Y-CLF**; **L-SCREEN-Y-PROMOTE**; V-SRC leave unnamed; L-PULSE-STANDIN-1 (baseline not met); F-SKILL/V-VALUE not established

---

## 10. Tags (detail)

| Kind | Tags |
|------|------|
| Domain | `markets` |
| Claim-shape | `forecast-extension`, `descriptive-census` |
| Pattern | `R-dependence` (V-VALUE ← V-SRC; F-SKILL ← horse vs Yahoo stand-in under **L-SCREEN-Y-PROMOTE**) |

---

## 11. Related applications (0–4)

| App ID | One-line reason |
|--------|-----------------|
| `2026-08_sell-in-may-sp500-2026` | Costs before a value bar (process only) |
| `2026-08_spacex-600-dollar-stock` | Soft-modal can/potential + lock-before-test (process only) |
| `2026-08_fomc-sep-2026-uffr-change` | Leave unnamed ≠ refute (process only) |
| `2026-08_fomc-june-2026-sep` | Print-match ≠ clearance (process only) |

*Related apps inform process only — no conclusion inheritance.*

---

*Layer 2. See `TRACKER_PORTFOLIO.md`, `TRACKER_RESIDUAL_QUEUE.md`, `TRACKER_PATTERN_MAP.md`.*
