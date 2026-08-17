# Lock Record — F-SRC named (CME CL open/settle tape)

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Operator selection:** `ok proceed` with the recommended `name source class …`  
**App-local lock ID:** **F-SRC-CME-TAPE**  
**Status:** **IN FORCE as the named skill vehicle.** Pulse ran. Bars **not established**. Prior F-SRC **leave unnamed** seal is **lifted for this class only** (not a refute undo).

---

## 0. Plain-language framing

**What was decided:**  
The skill test will use **CME’s official NYMEX CL front-month daily open and official settlement**, with a **stated roll rule**. First job: measure how jumpy **night**, **day**, and the **whole trip** each are versus “assume no change.” Optionally, re-score Kearney–Shang’s curve method on **that same tape** with RMSE, all three windows separate.

**What this settles:**  
Which public class is on the card. Naming is **not** a pass.

**What this does *not* settle:**  
That skill is shown. That Kearney–Shang wins. That anyone should trade. Yahoo/`CL=F` is **not** this class unless you later **stipulate** a stand-in.

---

## Named source class (quote this)

**CME NYMEX Light Sweet Crude Oil (CL) front-month official daily open and official daily settlement, roll-aware under roll rule R1 below.**  
**Primary test:** baseline decomposition — no-change forecast `0` on **F-ON**, **F-DAY**, and **F-CC**; report RMSE (and sample) on each window separately.  
**Optional horse:** Kearney & Shang (2020) functional time series on generic **CL1–CL18**, **re-scored** as RMSE on log-returns on this same open/settle tape, all three windows separate — not their published MAE/MCS, not a silent pass.

**Roll rule R1 (stated):**  
Front-month = the CL contract CME treats as the **lead/front** for that session’s official settlement. Log-returns use official stamps on **that** contract. When the front designation changes between session *t−1* settlement and session *t* open: **drop** that overnight (**F-ON**) and that close-to-close (**F-CC**) observation (roll jump ≠ economic return). **F-DAY** on a roll day uses open and settlement of the **new** front only (same contract). Do **not** treat a back-adjusted Panama **price level** as official settlement.

---

## Locked content

**Scope:** **Under Rank 4 + L-SESS + F-SRC-CME-TAPE**.

| ID | Rule |
|----|------|
| **F-SRC** | **Named** as above. Not EIA STEO. Not USO. Not Yahoo unless later stipulated. |
| **G8** | **Named** for this pulse: (1) no-change baseline RMSE on three windows; (2) optional Kearney–Shang FTS re-score on the same tape. Not an open architecture zoo. |
| **Live vs stand-in** | **Live = official CME open + settlement.** Vendor generic / Yahoo / `CL=F` = **stand-in** unless stipulated. **Not stipulated this turn.** |
| **F-COMBO** | Still **parked**. Not in this pulse. |

---

## What this does *not* do

- Does **not** establish F-CC, F-ON, F-DAY, F-COMBO, or V-VALUE.  
- Does **not** license trading.  
- Does **not** stipulate a stand-in tape.  
- Does **not** enter Phase 2.

**Lock-time Amb warning:** Naming the vehicle drops leftover-ambiguity on F-SRC/G8. **Amb drop ≠ clearance.**

---

## Reopen / next tape action

Obtain the live CME open/settle series (e.g. DataMine EOD) **or** operator `stipulate stand-in …` with a named vendor generic and a roll note. Then re-run the same formulas. Honest **established** still **stops**.
