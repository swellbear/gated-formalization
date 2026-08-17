# Dissertation — Application Findings

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Claim family / parent (if any):** none. No successor started.  
**Closeout verdict:** **Stable Provisional (split) — hard stop (residuals live)**  
**Amb at closeout:** **1.0**

**Tags** (see `docs/TRACKER_TAXONOMY.md`): Domain `markets` · Claim-shape `forecast-extension`, `descriptive-census` · Pattern `R-dependence`

**Related applications (max 4):** sell-in-may (costs before a value bar) · SpaceX-600 (lock ≠ clearance) · FOMC Sep (leave unnamed ≠ refute) · FOMC June SEP (print-match ≠ clearance). Process kinship only; **no conclusion inheritance**.

---

## 1. Plain-language summary

The question was whether a predictive model for oil futures can be built. That sentence was graded as three separate jobs, not one blended yes.

A specified forecasting recipe for listed crude **futures**, other than last-price no-change, has been written. That is all existence means here. Recipes that forecast the real or spot price of oil stay outside that freeze. The list of academic and practitioner recipes is existence evidence only — not a pick of one paper as “the” model.

Walk-forward skill on next-session CL log-returns versus last settlement is **not shown**. Yahoo `CL=F` is a **stipulated stand-in**. A named two-horse CFTC managed-money hunt (**L-HUNT-COT**) **failed at discovery** (both net and week-change **lost** vs no-change). A named two-horse Trump Truth Social hunt (**L-HUNT-DJT**) **failed at discovery** (both week/month averages **tied** no-change; daily scores on older oil-session dates were all zero). Overnight-gap **fade** (**H-GAP-FADE**) had a **small F-DAY** confirm edge; F-CC was locked to no-change — it **does not promote**. Continuation **lost** discovery F-DAY. A named eight-horse pretell hunt (**L-HUNT-PRETELL**) **failed at discovery**. Two sparse horses (**H-SPARSE-CAL**, **H-SPARSE-VOL**) were scored. The calendar horse’s last-500 F-CC dip is **0.000004** and **loses** on last 750 — it **does not promote**. The vol-state horse **lost** on F-CC. A lagged-return horse (**H-LAG-WF**) also **lost** on F-CC. Kearney–Shang **not run**.

After-cost paper trading value is **not shown**. Paper costs are now **V2** (fees plus $10/contract each way). The paper book was left unnamed. That is not a proof that every book fails.

This is not trading advice. A clearer, lower-ambiguity question is not a working predictor. The blended slogan is not cleared.

---

## 2. Original claim and context

**Original claim (verbatim):**  
Can a predictive model for oil futures be built?

**Source / domain context:** Operator question (2026-08-17). Crude oil futures as listed contracts (NYMEX CL / ICE Brent). Not a request to implement a trading model in this repo.

**Claim type:** Mixed — **D-EXIST** descriptive construction/existence; **F-SKILL** descriptive walk-forward skill elevation; **V-VALUE** performance elevation (not a “should trade”). LOCK-006 not imported.

**Parent or successor relationship (if any):** none. CR toward a skill-only or existence-only successor wording was **declined, not run**. Default: keep original wording.

---

## 3. How it was examined

**Method path:** Phase 1 only. … → **L-SCREEN-Y-PROMOTE** → horses **H-SPARSE-CAL** / **H-SPARSE-VOL**; pulse **L-PULSE-SPARSE-1** (neither promotes) → **L-HUNT-PRETELL**; pulse **L-PULSE-PRETELL-1** (no survivor) → **L-HUNT-GAP**; pulse **L-PULSE-GAP-1** (FADE small F-DAY; no promote) → **L-HUNT-DJT**; pulse **L-PULSE-DJT-1** (no survivor) → **L-HUNT-COT**; pulse **L-PULSE-COT-1** (no survivor). No Phase 2. No UX/CX/CR/QI run. Yahoo not used as live.

**Governing lock / freeze (if any):** Rank 4 `D-EXIST ⊂ F-SKILL ⊂ V-VALUE`. D-EXIST: `O1+M1+S1+C3+T2+H3+E3` (futures-target; no-change OUT as the model exhibit). F-SKILL: NYMEX CL front-month, next-session log-return, walk-forward RMSE vs last settlement. V-VALUE: after-cost paper P/L vs the curve under **V2** (listed fees + 1 tick/side). V-EITHER is historical.

**Key artifacts:** `Lock_Rank4_Nested_Split.md` · `Lock_D_EXIST_Established_Futures_Target.md` · `Lock_FSRC_Named_CME_Tape.md` · `PULSE_Baseline_Session_RMSE.md` · `Lock_FSRC_Leave_Unnamed.md` (superseded) · `Lock_VSRC_Leave_Unnamed.md` · `Lock_VCOST_Either.md` (superseded as singleton) · `Lock_VCOST_V2.md` · `Lock_Session_Split.md` · `04_Material_Admission_FSRC_Named.md` · `RESIDUAL_BRANCH_MENU.md` · `OPTIONAL_MODES_MENU.md` · this closeout pack.

---

## 4. What was established

| Finding | Scope |
|---------|--------|
| Rank 4 meanings (three jobs; “can” heights; contract/metric/horizon per leg) | Under Rank 4 — definitional, not slogan clearance |
| **D-EXIST:** a specified non-no-change mapping for listed WTI or Brent **futures** has been written | **Under Rank 4, futures-target only** (**D-EXIST-MET-FT**) |
| V-COST **V2** (fees + $10/contract/side) | Named schedule — not V-VALUE-met |
| Proven-only hunt executed; no freeze-matching proven public series submitted | **L-HUNT-PROVEN** (evaluation) |
| V-VALUE-TEST-0: no named book | Evaluation: bar not met (not a refute) |
| **F-SRC-CME-TAPE:** CME official CL open/settle + roll R1 named as the skill vehicle | Vehicle only — not skill-met |
| **L-SESS:** night / day / combo as separate scoreboards | Meanings only — not skill-met |
| **L-PULSE-TAPE-0:** named-class pulse executed; live tape absent | Evaluation: RMSE not computed; Yahoo not used |
| **L-SCREEN-Y-PROMOTE:** Yahoo screen; live CME only if F-CC beats 0 on last 500 and does not lose on 250/750 | Protocol only — H-LAG does not promote; not skill-met |

---

## 5. What was not established

| Item | Status |
|------|--------|
| F-SKILL: real shot of beating last-settlement RMSE, walk-forward, next-session CL log-return | **not established** (COT no survivor; DJT no survivor; FADE small F-DAY / F-CC tie; pretell no survivor; CAL tiny 500 / fails 750; VOL and H-LAG lost on F-CC; H-KS not run; stand-in; not a refute) — **live residual** |
| V-VALUE: real shot of after-cost paper P/L vs the curve | **not established** (V-SRC `leave unnamed`; **V2 named**; no book) — **not a refute** |
| Directional accuracy that survives transaction costs | **not shown** |
| Any decision or trading value; “should trade” | **not shown** (no should in the claim; LOCK-006 not imported) |
| Spot / real-price recipes as inside D-EXIST | **OUT** of the existence freeze (nearby kinship) |
| One paper from the menu as “the” recipe | **not picked** |
| F-ON / F-DAY RMSE vs no-change | **stand-in baseline computed** on Yahoo `CL=F` (not live CME; not skill-met) |
| Kearney–Shang FTS RMSE re-score on this tape | **not run** (Yahoo month chain ≠ historical CL1–CL18; 54 true-front dates) |
| Yahoo / `CL=F` as live CME | **rejected** as live; **stipulated** as stand-in |
| Blended slogan “a predictive oil-futures model works” | **not cleared** |

---

## 6. Forced deviations and scope limits

**Forced-deviation terms (if any):** None required. Rank 3 / D-EXIST is Minimal deviation. F-SKILL is Moderate. V-VALUE is a marked Substantial elevation, not FD-extraction of the slogan.

**Scoped vs unrestricted:** All findings hold **under Rank 4** only. D-EXIST-MET-FT is **not** unrestricted support for “the model predicts” or “the model makes money.”

**What the lock/package could not settle relative to the original wording:** Whether “predictive” as ordinary success (beats last price; survives costs) holds. The original one-liner does not name a contract, horizon, metric, or cost rule; Rank 4 named those per leg. Skill class is named; a **stand-in** baseline is scored; live tape still missing. Value vehicle remains unnamed.

---

## 7. Quantitative results (if any)

Stand-in baseline, **H-LAG-WF**, **H-SPARSE-CAL**, **H-SPARSE-VOL**, **L-HUNT-PRETELL**, **H-GAP-FADE** / **H-GAP-CONT**, **L-HUNT-DJT**, **L-HUNT-COT** — **not** bar-met. Paper costs **V2**. No named book, so V-VALUE still unused.

Yahoo `CL=F` last **500** sessions (2024-08-20 … 2026-08-14):

| Window | RMSE 0 | H-LAG-WF | H-SPARSE-CAL | H-SPARSE-VOL |
|--------|--------|----------|--------------|--------------|
| F-ON | 0.01291 | 0.01283 (tiny) | 0.01288 (tiny) | 0.01284 (tiny) |
| F-DAY | 0.02663 | 0.02670 (loss) | 0.026632 (tiny) | 0.02668 (loss) |
| F-CC | 0.02869 | 0.02888 (loss) | 0.02868990 (tiny; **fails** 750) | 0.02885 (loss) |

Promote gate: **none fire**. **L-HUNT-COT** discovery F-CC: both lose vs 0 = 0.026705 (closest H-COT-NET 0.026796); **no survivor**. **L-HUNT-DJT** discovery F-CC: both horses **tie** 0 = 0.026705; session-day scores all zero; **no survivor**. **H-GAP-FADE** confirm last-500 F-DAY 0.026584 vs 0 0.026634 (small); F-CC **tie**. **L-HUNT-PRETELL** discovery F-CC: all eight lose vs 0 = 0.026705; **no survivor**. H-KS-FTS **not run**. Tiny ≠ met. Day win ≠ promote. Equal-to-0 ≠ beat-0.

---

## 8. Revisions, implications, and alternatives

UX / CX / CR **declined, not run** (operator **C** `decline optional modes`). QI **N/A** (no failed numerical instance bar; unnamed skill is not a QI path). See [`OPTIONAL_MODES_MENU.md`](OPTIONAL_MODES_MENU.md). Original wording remains on record.

---

## 9. Final status of the original claim

**Verdict:** **Stable Provisional (split) — hard stop (residuals live)**

**Amb ≠ clearance:** Amb **1.0** is leftover V-SRC only. Live-vs-stand-in closed as Yahoo stipulated. V-COST named **V2**. Low leftover-ambiguity after locks does **not** mean skill, value, or the blended slogan is established.

**Locked-bar status summary:** D-EXIST **established** (futures-target only). F-SKILL **not established** (COT no survivor; DJT no survivor; FADE small F-DAY / F-CC tie; pretell hunt no survivor; CAL tiny 500 / fails 750; VOL and H-LAG lost on F-CC; H-KS not run). V-VALUE **not established**.

**Continuation / hard-stop note:** Hygiene sealed. Optional modes declined. Skill leftover stays **live** ([R-F-SKILL](RESIDUAL_BRANCH_MENU.md#r-f-skill)). Tape leftover **executed** as stand-in ([R-LIVE-STANDIN](RESIDUAL_BRANCH_MENU.md#r-live-standin)); reopen live **only if** **L-SCREEN-Y-PROMOTE** fires. Phase 2 not entered. Next: `leave skill not shown` · `name horse …` (**different**; do **not** add percent-of-OI or other trader groups after scores) · `leave screen rule`. **Do not** auto-open DataMine.

---

## 10. What would still be needed

- A **horse** scored against the stand-in F-ON / F-DAY / F-CC baselines that still **stops** if honest `04` would say established. A Yahoo **F-CC** beat **promotes** to live confirmation; it is **not** itself F-SKILL-met. Link: [R-F-SKILL](RESIDUAL_BRANCH_MENU.md#r-f-skill).  
- Official CME open/settle to **replace** the stand-in **only if** **L-SCREEN-Y-PROMOTE** fires: [R-LIVE-STANDIN](RESIDUAL_BRANCH_MENU.md#r-live-standin).  
- Separately, a named paper book matching V-VALUE **under V2**: [R-V-VALUE](RESIDUAL_BRANCH_MENU.md#r-v-value).  
- Do **not** treat Yahoo RMSE as live CME, or EIA STEO / Alquist–Kilian / the existence menu as “the” skill class.

---

## 11. Technical appendix

### Amb path

| Stage | Amb | Note |
|-------|-----|------|
| Cycle 0 unconstrained | **12** | Object / “can” / metric unset |
| After Rank 4 | **9** | Meanings locked; vehicles/costs open |
| After V-COST either | **7.5** | V-COST 2 → 0.5; V-VALUE-TEST-0 not established |
| V-SRC leave unnamed | **7.5** | Unchanged (leave-unnamed does not drop Amb) |
| After D-EXIST-MET-FT | **5.5** | D-SRC 2 → 0 |
| F-SRC leave unnamed / closeout | **5.5** | Unchanged |
| L-MAP-FT census | **5.5** | Unchanged (menu ≠ named class) |
| L-MAP-DRV census | **5.5** | Unchanged (no exhaustive list ≠ named class) |
| L-SESS protocol | **5.5** | Unchanged (window meanings ≠ named class) |
| F-SRC-CME-TAPE pulse | **2.5** | F-SRC 2→0; G8 1→0; live-vs-stand-in still 1 |
| L-STANDIN-Y-CLF pulse | **1.5** | Live-vs-stand-in 1→0; Yahoo baseline scored; skill not met |
| V-COST-V2 named | **1.0** | V-COST 0.5→0; V-VALUE still not met (no named book) |
| L-PULSE-HORSES-1 | **1.0** | Unchanged; H-LAG lost on F-CC; H-KS not run |
| L-SCREEN-Y-PROMOTE | **1.0** | Unchanged; Yahoo screen; live CME only on F-CC beat; H-LAG does not promote |
| L-PULSE-SPARSE-1 | **1.0** | Unchanged; CAL tiny 500 / fails 750; VOL F-CC loss; neither promotes |
| L-PULSE-PRETELL-1 | **1.0** | Unchanged; eight tell horses; discovery F-CC all lose; no survivor |
| L-PULSE-GAP-1 | **1.0** | Unchanged; FADE small F-DAY confirm; F-CC tie; does not promote |
| L-PULSE-DJT-1 | **1.0** | Unchanged; two Truth Social horses; discovery F-CC both tie 0; no survivor |
| L-PULSE-COT-1 | **1.0** | Unchanged; two CFTC MM horses; discovery F-CC both lose; no survivor |

### Admitted layers (index)

| ID | One-line | Pointer |
|----|----------|---------|
| Rank 4 | Nested split meanings | `Lock_Rank4_Nested_Split.md` |
| D-EXIST-MET-FT | Existence established, futures-target only | `Lock_D_EXIST_Established_Futures_Target.md` |
| L-D-SUITE | Named recipe menu; existence evidence only | `04_Material_Admission_D_EXIST_Named_Suite.md` |
| L-HUNT-PROVEN | Hunt executed; no proven F-SKILL class | `04_Material_Admission_Proven_Class_Search.md` |
| V-EITHER | Cost either (historical OR-slot; superseded as singleton) | `Lock_VCOST_Either.md` |
| V-COST-V2 | Named paper-cost schedule (fees + 1 tick/side); not value-met | `Lock_VCOST_V2.md` |
| V-VALUE-TEST-0 | No named book; value not established | `04_Material_Admission_V_VALUE_No_Recipe.md` |
| V-SRC unnamed | Leave unnamed; not a refute | `Lock_VSRC_Leave_Unnamed.md` |
| F-SRC unnamed | Leave unnamed; later superseded | `Lock_FSRC_Leave_Unnamed.md` |
| L-MAP-FT | Futures-target method census; skill not met | `04_Material_Admission_FT_Method_Map.md` |
| L-MAP-DRV | Mover-list census; exhaustive next-session list absent | `04_Material_Admission_FT_Driver_Map.md` |
| L-SESS | Night/day/combo protocol; skill not met | `04_Material_Admission_Session_Split.md` |
| L-MAP-SESS | Overnight/day literature kinship; USO ≠ CL | `MAP_Session_Split.md` |
| F-SRC-CME-TAPE | Named CME open/settle class | `Lock_FSRC_Named_CME_Tape.md` |
| L-PULSE-TAPE-0 | Pulse executed; tape missing; skill not met | `04_Material_Admission_FSRC_Named.md` |
| L-STANDIN-Y-CLF | Yahoo `CL=F` stipulated stand-in | `Lock_Standin_Yahoo_CLF.md` |
| L-PULSE-STANDIN-1 | Stand-in baseline RMSE; skill not met | `04_Material_Admission_Standin_Yahoo.md` |
| V-COST-V2 | Named paper-cost schedule; not value-met | `Lock_VCOST_V2.md` |
| L-STANDIN-Y-CHAIN | Yahoo month chain attempted; historical CL1–CL18 fail | `Lock_Standin_Yahoo_Curve.md` |
| H-LAG-WF / H-KS-FTS | Named horses; H-LAG scored (F-CC loss); H-KS not run | `Lock_Horses_Lag_KS.md` |
| L-PULSE-HORSES-1 | Horse pulse; skill not met | `04_Material_Admission_Horses.md` |
| L-SCREEN-Y-PROMOTE | Yahoo screen; live CME only if F-CC beats 0 on last 500 and 250/750 | `Lock_Screen_Yahoo_Promote.md` |
| H-SPARSE-CAL / H-SPARSE-VOL | Named sparse horses; neither promotes | `Lock_Horses_Sparse.md` |
| L-PULSE-SPARSE-1 | Sparse pulse; skill not met | `04_Material_Admission_Sparse.md` |
| L-HUNT-PRETELL / L-STANDIN-Y-TELLS | Named finite tell hunt; no discovery survivor | `Lock_Hunt_Pretell.md` |
| L-PULSE-PRETELL-1 | Pretell pulse; skill not met | `04_Material_Admission_Pretell.md` |
| H-GAP-FADE / H-GAP-CONT | Named day-gap horses; FADE small F-DAY; no promote | `Lock_Horses_Gap.md` |
| L-PULSE-GAP-1 | Gap pulse; skill not met | `04_Material_Admission_Gap.md` |
| L-HUNT-DJT / L-STANDIN-DJT-TRUTH | Named Truth Social oil-sentiment hunt; no discovery survivor | `Lock_Hunt_DJT.md` |
| L-PULSE-DJT-1 | DJT pulse; skill not met | `04_Material_Admission_DJT.md` |
| L-HUNT-COT / L-STANDIN-CFTC-COT | Named CFTC managed-money hunt; no discovery survivor | `Lock_Hunt_COT.md` |
| L-PULSE-COT-1 | COT pulse; skill not met | `04_Material_Admission_COT.md` |

### Key artifacts

- `DISSERTATION.md` · `SHARE_PACK.md` · `EXECUTIVE_BRIEF.md` · `05_Original_Claim_Assessment_Closeout.md` · `final_verdict.md` · `RESIDUAL_BRANCH_MENU.md` · `OPTIONAL_MODES_MENU.md` · `MAP_Futures_Target_Forecasting_Methods.md` · `MAP_What_Can_Move_CL.md` · `Lock_Session_Split.md` · `MAP_Session_Split.md` · `Lock_FSRC_Named_CME_Tape.md` · `PULSE_Baseline_Session_RMSE.md` · `Lock_VCOST_V2.md` · `Lock_Screen_Yahoo_Promote.md` · `Lock_Horses_Sparse.md` · `PULSE_Horses_Sparse.md` · `Lock_Hunt_Pretell.md` · `PULSE_Hunt_Pretell.md` · `Lock_Horses_Gap.md` · `PULSE_Horses_Gap.md` · `Lock_Hunt_DJT.md` · `PULSE_Hunt_DJT.md` · `Lock_Hunt_COT.md` · `PULSE_Hunt_COT.md`

### Failure-mode / tracker pointers (if any)

- Pattern `R-dependence`: F-SKILL ← live tape after F-SRC named; V-VALUE ← V-SRC. Lesson: do not pretend empirical closure while the vehicle or the tape is missing.  
- Print-match ≠ clearance; lock ≠ clearance; leave-unnamed ≠ refute.

---

*Generated under standing rule: Application Dissertation Deliverable. See `.cursor/rules/applications-gated-method.mdc`. Stubs ≠ hard stop.*
