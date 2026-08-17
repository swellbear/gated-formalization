# Dissertation — Application Findings

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Claim family / parent (if any):** none. No successor started.  
**Closeout verdict:** **Stable Provisional (split) — hard stop (residuals live)**  
**Amb at closeout:** **2.5**

**Tags** (see `docs/TRACKER_TAXONOMY.md`): Domain `markets` · Claim-shape `forecast-extension`, `descriptive-census` · Pattern `R-dependence`

**Related applications (max 4):** sell-in-may (costs before a value bar) · SpaceX-600 (lock ≠ clearance) · FOMC Sep (leave unnamed ≠ refute) · FOMC June SEP (print-match ≠ clearance). Process kinship only; **no conclusion inheritance**.

---

## 1. Plain-language summary

The question was whether a predictive model for oil futures can be built. That sentence was graded as three separate jobs, not one blended yes.

A specified forecasting recipe for listed crude **futures**, other than last-price no-change, has been written. That is all existence means here. Recipes that forecast the real or spot price of oil stay outside that freeze. The list of academic and practitioner recipes is existence evidence only — not a pick of one paper as “the” model.

Walk-forward skill on next-session CL log-returns versus last settlement is **not shown**. The public source class is **named** (CME official CL open and settlement). The official tape was **not obtained**; Yahoo was **not** used. Night/day RMSE was not computed. That leftover stays live.

After-cost paper trading value is **not shown**. The paper book was left unnamed. That is not a proof that every book fails.

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

**Method path:** Phase 1 only. Cycle 0 (Amb 12) → Rank 4 nested split locked → no-change held out as the existence exhibit → proven-only hunt submitted no F-SKILL class → V-COST either → V-VALUE no-recipe not established → V-SRC leave unnamed → named recipe suite → operator authorized D-EXIST established (futures-target only) → F-SRC leave unnamed → closeout → optional modes declined → L-MAP-FT / L-MAP-DRV / L-SESS → **F-SRC-CME-TAPE** named; pulse **L-PULSE-TAPE-0** executed (tape missing). No Phase 2. No UX/CX/CR/QI run. Yahoo not used as live.

**Governing lock / freeze (if any):** Rank 4 `D-EXIST ⊂ F-SKILL ⊂ V-VALUE`. D-EXIST: `O1+M1+S1+C3+T2+H3+E3` (futures-target; no-change OUT as the model exhibit). F-SKILL: NYMEX CL front-month, next-session log-return, walk-forward RMSE vs last settlement. V-VALUE: after-cost paper P/L vs the curve; V-COST either (V1 fees-only or V2 fees + 1 tick/side); each later test must name which.

**Key artifacts:** `Lock_Rank4_Nested_Split.md` · `Lock_D_EXIST_Established_Futures_Target.md` · `Lock_FSRC_Named_CME_Tape.md` · `PULSE_Baseline_Session_RMSE.md` · `Lock_FSRC_Leave_Unnamed.md` (superseded) · `Lock_VSRC_Leave_Unnamed.md` · `Lock_VCOST_Either.md` · `Lock_Session_Split.md` · `04_Material_Admission_FSRC_Named.md` · `RESIDUAL_BRANCH_MENU.md` · `OPTIONAL_MODES_MENU.md` · this closeout pack.

---

## 4. What was established

| Finding | Scope |
|---------|--------|
| Rank 4 meanings (three jobs; “can” heights; contract/metric/horizon per leg) | Under Rank 4 — definitional, not slogan clearance |
| **D-EXIST:** a specified non-no-change mapping for listed WTI or Brent **futures** has been written | **Under Rank 4, futures-target only** (**D-EXIST-MET-FT**) |
| V-COST either (V1 or V2; later tests must name which) | Meanings only — not V-VALUE-met |
| Proven-only hunt executed; no freeze-matching proven public series submitted | **L-HUNT-PROVEN** (evaluation) |
| V-VALUE-TEST-0: no named book | Evaluation: bar not met (not a refute) |
| **F-SRC-CME-TAPE:** CME official CL open/settle + roll R1 named as the skill vehicle | Vehicle only — not skill-met |
| **L-SESS:** night / day / combo as separate scoreboards | Meanings only — not skill-met |
| **L-PULSE-TAPE-0:** named-class pulse executed; live tape absent | Evaluation: RMSE not computed; Yahoo not used |

---

## 5. What was not established

| Item | Status |
|------|--------|
| F-SKILL: real shot of beating last-settlement RMSE, walk-forward, next-session CL log-return | **not established** (**F-SRC-CME-TAPE** named; live tape absent; pulse not computed) — **not a refute**; **live residual** |
| V-VALUE: real shot of after-cost paper P/L vs the curve | **not established** (V-SRC `leave unnamed`; V1/V2 unused) — **not a refute** |
| Directional accuracy that survives transaction costs | **not shown** |
| Any decision or trading value; “should trade” | **not shown** (no should in the claim; LOCK-006 not imported) |
| Spot / real-price recipes as inside D-EXIST | **OUT** of the existence freeze (nearby kinship) |
| One paper from the menu as “the” recipe | **not picked** |
| F-ON / F-DAY RMSE vs no-change | **not computed** (live open/settle absent) |
| Kearney–Shang FTS RMSE re-score on this tape | **not run** |
| Yahoo / `CL=F` as live CME | **rejected** this pulse |
| Blended slogan “a predictive oil-futures model works” | **not cleared** |

---

## 6. Forced deviations and scope limits

**Forced-deviation terms (if any):** None required. Rank 3 / D-EXIST is Minimal deviation. F-SKILL is Moderate. V-VALUE is a marked Substantial elevation, not FD-extraction of the slogan.

**Scoped vs unrestricted:** All findings hold **under Rank 4** only. D-EXIST-MET-FT is **not** unrestricted support for “the model predicts” or “the model makes money.”

**What the lock/package could not settle relative to the original wording:** Whether “predictive” as ordinary success (beats last price; survives costs) holds. The original one-liner does not name a contract, horizon, metric, or cost rule; Rank 4 named those per leg. Skill class is now named; the live tape is still missing. Value vehicle remains unnamed.

---

## 7. Quantitative results (if any)

None as bar-met numbers. CL tick identity (market structure, not a broker quote): $0.01/bbl × 1000 bbl = **$10**/contract/side (**$20** round-turn slippage before fees) under V2. V1/V2 were unused because no named book. Named-class pulse **L-PULSE-TAPE-0** did **not** compute RMSE (live CME open/settle absent; Yahoo not used). Print-match of nearby spot/monthly results or Kearney–Shang MAE was **not** used as F-SKILL clearance.

---

## 8. Revisions, implications, and alternatives

UX / CX / CR **declined, not run** (operator **C** `decline optional modes`). QI **N/A** (no failed numerical instance bar; unnamed skill is not a QI path). See [`OPTIONAL_MODES_MENU.md`](OPTIONAL_MODES_MENU.md). Original wording remains on record.

---

## 9. Final status of the original claim

**Verdict:** **Stable Provisional (split) — hard stop (residuals live)**

**Amb ≠ clearance:** Amb **2.5** is leftover live-vs-stand-in (1) + V-SRC (1) + V-COST (0.5). Naming the tape dropped F-SRC and G8. Low leftover-ambiguity after locks does **not** mean skill, value, or the blended slogan is established.

**Locked-bar status summary:** D-EXIST **established** (futures-target only). F-SKILL **not established** (class named; tape missing). V-VALUE **not established**.

**Continuation / hard-stop note:** Hygiene sealed. Optional modes declined. Skill leftover stays **live** ([R-F-SKILL](RESIDUAL_BRANCH_MENU.md#r-f-skill)). Tape leftover **pursue** ([R-LIVE-STANDIN](RESIDUAL_BRANCH_MENU.md#r-live-standin)). Phase 2 not entered. Next: `live CME only` / `stipulate stand-in …` / `leave tape pending`.

---

## 10. What would still be needed

- Official CME CL front-month **open and settlement** (or a stipulated stand-in) so F-ON / F-DAY / F-CC RMSE can be computed — then a pulse that still **stops** if honest `04` would say established. Link: [R-LIVE-STANDIN](RESIDUAL_BRANCH_MENU.md#r-live-standin) · [R-F-SKILL](RESIDUAL_BRANCH_MENU.md#r-f-skill). The L-MAP-FT census is **not** that tape.  
- Separately, a named paper book matching V-VALUE, stating V1 or V2: [R-V-VALUE](RESIDUAL_BRANCH_MENU.md#r-v-value).  
- Do **not** fill the tape with unstipulated Yahoo/`CL=F`, EIA STEO, Alquist–Kilian spot evaluations, or the existence menu as “the” skill class.

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

### Admitted layers (index)

| ID | One-line | Pointer |
|----|----------|---------|
| Rank 4 | Nested split meanings | `Lock_Rank4_Nested_Split.md` |
| D-EXIST-MET-FT | Existence established, futures-target only | `Lock_D_EXIST_Established_Futures_Target.md` |
| L-D-SUITE | Named recipe menu; existence evidence only | `04_Material_Admission_D_EXIST_Named_Suite.md` |
| L-HUNT-PROVEN | Hunt executed; no proven F-SKILL class | `04_Material_Admission_Proven_Class_Search.md` |
| V-EITHER | Cost either; tests must name V1 or V2 | `Lock_VCOST_Either.md` |
| V-VALUE-TEST-0 | No named book; value not established | `04_Material_Admission_V_VALUE_No_Recipe.md` |
| V-SRC unnamed | Leave unnamed; not a refute | `Lock_VSRC_Leave_Unnamed.md` |
| F-SRC unnamed | Leave unnamed; later superseded | `Lock_FSRC_Leave_Unnamed.md` |
| L-MAP-FT | Futures-target method census; skill not met | `04_Material_Admission_FT_Method_Map.md` |
| L-MAP-DRV | Mover-list census; exhaustive next-session list absent | `04_Material_Admission_FT_Driver_Map.md` |
| L-SESS | Night/day/combo protocol; skill not met | `04_Material_Admission_Session_Split.md` |
| L-MAP-SESS | Overnight/day literature kinship; USO ≠ CL | `MAP_Session_Split.md` |
| F-SRC-CME-TAPE | Named CME open/settle class | `Lock_FSRC_Named_CME_Tape.md` |
| L-PULSE-TAPE-0 | Pulse executed; tape missing; skill not met | `04_Material_Admission_FSRC_Named.md` |

### Key artifacts

- `DISSERTATION.md` · `SHARE_PACK.md` · `EXECUTIVE_BRIEF.md` · `05_Original_Claim_Assessment_Closeout.md` · `final_verdict.md` · `RESIDUAL_BRANCH_MENU.md` · `OPTIONAL_MODES_MENU.md` · `MAP_Futures_Target_Forecasting_Methods.md` · `MAP_What_Can_Move_CL.md` · `Lock_Session_Split.md` · `MAP_Session_Split.md` · `Lock_FSRC_Named_CME_Tape.md` · `PULSE_Baseline_Session_RMSE.md`

### Failure-mode / tracker pointers (if any)

- Pattern `R-dependence`: F-SKILL ← live tape after F-SRC named; V-VALUE ← V-SRC. Lesson: do not pretend empirical closure while the vehicle or the tape is missing.  
- Print-match ≠ clearance; lock ≠ clearance; leave-unnamed ≠ refute.

---

*Generated under standing rule: Application Dissertation Deliverable. See `.cursor/rules/applications-gated-method.mdc`. Stubs ≠ hard stop.*
