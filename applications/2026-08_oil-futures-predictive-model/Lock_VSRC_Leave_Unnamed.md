# Lock Record — V-SRC leave unnamed

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Operator selection:** **B** → `leave unnamed` (value-leg book / V-SRC)  
**Status:** **SEALED unnamed.** Not a pulse vehicle. Reopen only with `name source class …` that matches Rank 4 V-VALUE.

---

## 0. Plain-language framing

**What decision was made:**  
Do not invent a public paper book for the after-cost value test.

**Why it was required:**  
Costs are allowed as either listed fees or fees plus a one-tick fill, but there is still no named recipe. The proven-only hunt submitted no freeze-matching class.

**What this settles:**  
The value-leg vehicle stays empty. After-cost value stays **not shown** (`V-VALUE-TEST-0`).

**What this does *not* settle:**  
That every oil-futures book fails. That anyone should (or should not) trade. Existence or forecast skill. Which of V1/V2 would have been used on a later book.

**Amb:** Unchanged at **7.5**. Leaving a class unnamed does **not** drop leftover-ambiguity. **Amb ≠ clearance.**

---

## Locked content

| ID | Rule |
|----|------|
| **V-SRC** | **Unnamed.** No public recipe/book named for V-VALUE. |
| **V-VALUE** | **Not established** (not a refute of all books). |
| **V1 / V2** | Still unused. Either-lock remains; unused because unused. |

**Scope:** **Under Rank 4 (D-EXIST ⊂ F-SKILL ⊂ V-VALUE) only**, **Under V-COST either**, **Under V-SRC leave unnamed**.

**Do not treat as this class:** EIA STEO, the listed futures curve as a next-session CL return model, Alquist–Kilian / Fed IFDP spot-forecast papers, vendor/ML one-offs, last-settlement no-change.

---

## Reopen

`name source class …` with a **specific public series + matching locks** (NYMEX CL front-month, next-session, walk-forward, after-cost paper P/L vs the curve). That later test must still **name V1 or V2**. Naming ≠ bar-met. Honest **established** still stops.

---

## Dependents

- **V-VALUE** stays not established until a named-enough non-circular book is pulsed. This seal is **not** a refute of all books.  
- **At lock time:** **D-SRC** was unnamed for now (next ask after this seal). **Later (same day):** operator named a suite and authorized **D-EXIST-MET-FT** (`Lock_D_EXIST_Established_Futures_Target.md`). This V-SRC seal does **not** reopen or undo that.  
- **F-SRC** remains unnamed (live ask after D-EXIST-MET-FT). No Phase 2. No invented class.
