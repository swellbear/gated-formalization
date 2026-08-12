# Locking Scaffolding — TSLA “buy cheaper” timing

**Date:** 2026-08-12  
**Application:** `2026-08_voo-to-cash-tsla-cheaper`  
**Dominant blockers:** G2 (reference R), G3 (horizon H), G4 (modal bar M)  
**Dependents blocked:** Any admit that waiting in cash to buy TSLA cheaper is a supported plan; G5 warrant test

**Explicit dependency:** Evidence on whether TSLA gets “cheaper” is blocked until R, H, and M are locked.

**Claim under test (strategic part):**  
Speaker may increase cash with the idea to buy some TSLA **cheaper** (than a reference), within a horizon, under a modal bar.

**Original quote (verbatim):**  
“I just sold some VOO which was up by 47% and selling at $708 a share Im back down to 50% cash. I may trend more to cash soon with the idea to buy some tsla cheaper.”

**Operator posture:** Chose path **2 — lock the timing claim**. Packages proposed (agent defaults); selection required before evidence.

---

## 0. Plain-language framing

**What decision is being made right now:**  
What “buy Tesla cheaper” actually means — cheaper than what, by when, and how strong a claim it is.

**Why required:**  
Without that, any “validation” guesses the grading rules after the fact.

**What becomes testable:**  
Whether Tesla’s price path meets the locked dip rule in the locked window — as possibility, intent, or non-negligible path (depending on package).

**What this decision alone cannot settle:**  
Whether selling VOO was wise; whether more cash is optimal; whether the speaker *should* buy Tesla; investment advice.

---

## 1. Decision points

| Point | Plain question |
|-------|----------------|
| **R** | Cheaper than what? |
| **H** | By when? |
| **M** | How strong is the claim? |

---

## 2. Options

### R — Reference

| ID | Ordinary meaning |
|----|------------------|
| **R1** | Cheaper than **today’s TSLA price** at lock time (T0 close) |
| **R2** | At least **10% below** T0 TSLA close |
| **R3** | At least **20% below** T0 TSLA close |
| **R4** | Below a **named limit price** the operator states (e.g. $X) |

### H — Horizon

| ID | Ordinary meaning |
|----|------------------|
| **H1** | Within **90 days** of T0 |
| **H2** | Within **12 months** of T0 |
| **H3** | Open-ended (“eventually”) — near-vacuous; weak package only |

### M — Modal bar

| ID | Ordinary meaning |
|----|------------------|
| **M1** | **Intent only** — speaker plans to try; not a market forecast |
| **M2** | **Possible** — a dip to R within H is not ruled out (very weak) |
| **M3** | **Non-negligible path** — a serious (not vanishingly thin) path to R within H under ordinary market reasoning |
| **M4** | **Likely / base case** — more likely than not TSLA prints ≤ R within H |

---

## 3–5. Ranked packages

### Rank 1 — **Dip Plan (10% / 90 days / non-negligible)** *(recommended)*

**Composition:** **R2 + H1 + M3**

**Ordinary meaning:** “There is a serious path for TSLA to trade at least 10% below today’s price within 90 days,” and cash is being held with that idea in mind.

**Next phase can check:** Whether that path is established / not established / refuted under ordinary evidence (vol, levels, no crystal ball). Past VOO gain still does not auto-warrant it.

**Cannot settle:** Advice to buy; VOO sale quality; open-ended “eventually cheaper.”

**Deviation vs quote:** Minimal–Moderate — makes “cheaper” and “soon” concrete; “may” → non-negligible path (stronger than bare possibility).

**Objective claim-deviation (vs quote’s S2):**  
1. Strong language: “cheaper” / “soon” operationalized; “may”/“idea” → M3 (strengthened).  
2. Problem identity: still a TSLA dip-timing idea.  
3. Scope shift: 10% / 90d fixed.  
4. **Moderate deviation** (modal strengthened from vague “idea”).

---

### Rank 2 — **Intent Card (today / 90 days / intent only)**

**Composition:** **R1 + H1 + M1**

**Ordinary meaning:** Speaker intends to buy if TSLA is below today’s price within 90 days — a **plan statement**, not a forecast that the dip will happen.

**Next phase can check:** Consistency of the plan; **not** whether the market will deliver the dip.

**Cannot settle:** Market timing success.

**Deviation:** **Substantial** if read as validating a market call; **Minimal** if read as locking an intent-only claim.

**Relevance warning:** Weak overlap with “validate the buy-cheaper idea” as a market claim.

---

### Rank 3 — **Deep Dip Likely (20% / 12 months / likely)**

**Composition:** **R3 + H2 + M4**

**Ordinary meaning:** TSLA is **more likely than not** to print ≥20% below T0 within a year.

**Next phase can check:** A strong forecast bar (hard to establish without heavy assumptions).

**Cannot settle:** Easily — high bar; likely **not established**.

**Deviation:** **Substantial** (much stronger than the quote).

---

### Rank 4 — **Eventually Possible** *(not recommended)*

**Composition:** **R1 + H3 + M2**

**Near-vacuous.** Almost always “possible” that a volatile name prints below today someday.

**Deviation:** Problem-light / near-vacuous — **Substantial** relative to useful testing.

---

## 6. Choice prompt

**Plain-language card**

- **What we’re doing:** Freezing what “buy TSLA cheaper” means.  
- **What we need from you:** Pick one package (or à-la-carte).  
- **What a “yes” means:** We only set the grading rules; we do **not** prove the trade.  
- **What this does *not* mean:** Lower ambiguity after the lock ≠ a good investment.

```
Package: Dip Plan (10% / 90 days / non-negligible)   ← recommended

OR à-la-carte:
- R = R1 / R2 / R3 / R4 (if R4, state $____)
- H = H1 / H2 / H3
- M = M1 / M2 / M3 / M4
```

**Details (secondary):** R2+H1+M3 = Rank 1; T0 = lock date (2026-08-12 unless you set another).

**Lock-time warning:** Picking a package drops Amb by fixing meanings. That does **not** establish that TSLA will get cheaper or that cash-for-TSLA is wise.

---

## 7. Forced-deviation extraction

**Vs quote:** Rank 1 is Moderate (modal strengthened). Rank 2 can be Minimal for intent-only. No Minimal package that both matches the quote’s soft “idea” **and** yields a serious market test — hence Rank 1 recommended for path 2.

**FD-Carry:** Bare “cheaper” / “soon” / “idea” without R/H/M — under-specified in the quote as written.

---

## 8. Proposed selection

**Recommended:** Rank 1 — **Dip Plan (R2+H1+M3)**  
Reply **`lock Rank 1`** to adopt, or name another package / à-la-carte.
