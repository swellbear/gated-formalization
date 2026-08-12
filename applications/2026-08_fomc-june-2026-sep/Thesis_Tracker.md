# Thesis Tracker (Layer 2)

**Application:** `2026-08_fomc-june-2026-sep`  
**Last reviewed:** 2026-08-12  
**Status:** Stable Provisional (split) — **hard stop sealed**

**Tags** (see `docs/TRACKER_TAXONOMY.md`):  
- Domain: `markets`  
- Claim-shape: `descriptive-census`, `forecast-extension`  
- Pattern: `forced-deviation`

---

## 1. Claim

**Original (verbatim):**  
The June 17, 2026 SEP is a published package of FOMC participants’ projections of **most likely** GDP, unemployment, inflation, and **appropriate** federal-funds paths for 2026–2028 and the longer run (inventory in [`CLAIM_INVENTORY.md`](CLAIM_INVENTORY.md)). July 29 OUT.

**Successor / Rank lock (if any):** None. CR **offered, not run**. Default **keep original wording**.

**Parent / successor relationship:** None.

---

## 2. Verdict and Amb path

**Verdict:** Stable Provisional (split) — hard stop.

**Amb path (brief):** Cycle 0 ≈ 11 → L1 9 → L2 7 → L3–L10 stay 7 → L11 5 → L12 4 → L13 stay 4 → L14 3 → L15 2 → L16 **1**. G8 not locked at closeout.

**Amb ≠ clearance:** Amb ≈ 1 is Gap 8 still open plus unmet bars, not a finding that 2026 PCE 3.6 is the expected path.

---

## 3. Established

- L1 forecast object; L2 P-BaseCase **meaning** (bar not met)  
- L3–L10 census vehicle (identity, definitions, submitted cells, 2021–25 actuals, revisions, dots/hists, uncertainty tallies, RMSE fans with caveats)  
- L11 C-APPROP individual-mandate **meaning**; L12 F-LR **meaning**  
- L13 2026 F-ML-BAR **test executed**  
- L14 median of 18 (17 for 2028); L15 year-slots; L16 D-UNCERT ≠ D-RMSE

---

## 4. Not established / negatively constrained

- F-ML-BAR met (2026 tested, not established, not a refute; 2027–28 untested)  
- C-APPROP as vote or realized path  
- F-LR as dated unconditional or 2026-on-target  
- Median as Committee forecast  
- RMSE fan as current FOMC uncertainty; 17/18 as 70% interval; CPI RMSE as PCE  
- 2026–28 realization; July 29; commitment object; funds-rate dots as F-ML

---

## 5. Forced deviations

Median → Committee forecast; SEP → will happen; P-BaseCase freeze → bar met; L13 not-established → 2026 medians refuted; LR 2% → 2026 on-target; RMSE fan → current FOMC uncertainty; 17/18 → 70% interval; CPI RMSE → PCE; Amb 1 → clearance; July 29 on residual menu → in-package.

---

## 6. Residuals that would reopen the case

| ID | Residual | Concrete reopen condition |
|----|----------|---------------------------|
| [R-FML-2026](RESIDUAL_BRANCH_MENU.md#r-fml-2026) | 2026 F-ML-BAR test | **Executed** — not established; re-open only via R-FML-INDEP |
| [R-G8-SCOPE](RESIDUAL_BRANCH_MENU.md#r-g8-scope) | Freeze realization out of scope now | `lock G8 realization-later` (Amb 1→0; ≠ clearance) |
| [R-REALIZE](RESIDUAL_BRANCH_MENU.md#r-realize) | 2026–28 actuals vs L5 medians | 2026 Q4 prints under L4 defs; hit ≠ F-ML met |
| [R-FML-INDEP](RESIDUAL_BRANCH_MENU.md#r-fml-indep) | Non-SEP matched expected-path | Operator admits independent series under same locks |
| [R-FML-2027-28](RESIDUAL_BRANCH_MENU.md#r-fml-2027-28) | F-ML-BAR on 2027 and 2028 | Authorize; diminishing returns |
| [R-REV](RESIDUAL_BRANCH_MENU.md#r-rev) | Narrow to census core | `run CR`; rewording ≠ bar clearance |
| [R-JULY29](RESIDUAL_BRANCH_MENU.md#r-july29) | Elevate July 29 into L₀ | Explicit package change; else **drop** |

---

## 7. Action implications

**Stop saying:** “The Fed forecasts 3.6%”; “dots are the decision”; “on target this year”; “Amb 1 means cleared.”

**Keep saying:** Eighteen submissions; median of those submissions; census ≠ expected-path clearance; 17/18 flagged upside PCE risk.

**Test next (only if authorized):** R-FML-INDEP or R-REALIZE after 2026 Q4 prints. Optional: `run UX` / `run CX` / `run CR`.

---

## 8. Exhibits

- [`CLAIM_INVENTORY.md`](CLAIM_INVENTORY.md) · [`04a`](04a_Material_Admission_OBJECT_FORECAST.md)–[`04p`](04p_Material_Admission_G7_Tallies_Neq_RMSE.md)  
- [`E_Quantitative_Evidence_Rubric_F_ML_2026.md`](E_Quantitative_Evidence_Rubric_F_ML_2026.md)  
- [`RESIDUAL_BRANCH_MENU.md`](RESIDUAL_BRANCH_MENU.md) · [`OPTIONAL_MODES_MENU.md`](OPTIONAL_MODES_MENU.md)  
- UX/CX/CR **offered, not run**; QI **N/A**

---

## 9. Pointers

- Dissertation: [`DISSERTATION.md`](DISSERTATION.md)  
- Closeout / verdict: [`05_Original_Claim_Assessment_Closeout.md`](05_Original_Claim_Assessment_Closeout.md) · [`final_verdict.md`](final_verdict.md) · [`SHARE_PACK.md`](SHARE_PACK.md)  
- Parent / successor: none  
- Key admissions / locks: [`admitted_layers.md`](admitted_layers.md)

---

## 10. Tags (detail)

| Kind | Tags |
|------|------|
| Domain | `markets` |
| Claim-shape | `descriptive-census`, `forecast-extension` |
| Pattern | `forced-deviation` |

---

## 11. Related applications (0–4)

| App ID | One-line reason |
|--------|-----------------|
| `2026-08_zitron-nvidia-500b-financing-thesis` | Claimed-table vs elevation; Amb≠clearance; brochure cannot clear itself |
| `2026-08_coreweave-ceo-gpu-longer-life` | Real-claim forecast locks (LOCK-009–011) |
| `2026-08_sell-in-may-sp500-2026` | Markets elevation; descriptive core ≠ forward clearance |

*Related apps inform process only — no conclusion inheritance.*

---

*Layer 2. See `TRACKER_PORTFOLIO.md`, `TRACKER_RESIDUAL_QUEUE.md`, `TRACKER_PATTERN_MAP.md`.*
