# Lock Record — stipulated curve stand-in (Yahoo NYMEX month chain)

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Operator selection:** `ok proceed` with recommended `stipulate curve stand-in Yahoo NYMEX month chain as CL1–CL18`  
**App-local lock ID:** **L-STANDIN-Y-CHAIN**  
**Status:** **IN FORCE as the attempted curve stand-in.** Fetch ran. **Historical freeze-matching CL1–CL18 not obtained.** Kearney–Shang **not run**. Does **not** replace live CME generics.

---

## 0. Plain-language framing

**What was decided:**  
Try Yahoo’s listed WTI month contracts, stacked by expiration, as a stand-in curve.

**What this settles:**  
Which curve proxy was attempted. Yahoo expired months **404**. The nearest *still-listed* contract is **not** historical CL1.

**What this does *not* settle:**  
That a curve tape exists for Kearney–Shang. That skill is shown.

---

## Named stand-in (quote this)

**Yahoo Finance NYMEX CL calendar months `CL{FGHJKMNQUVXZ}{YY}.NYM` daily Open/Close, ranked by delivery as CL1…CL18.**  
**Badge:** **stand-in** — not CME generics.  
**Roll note:** Homemade frontness among *currently listed* months. Expired symbols 404, so dates before ~2026-06 relabel far leftovers as “CL1.” Those rows are **not** freeze-matching CL1–CL18.

**Fetch (2026-08-17):** 60 symbols tried; **38** live (CLQ26.NYM … CLZ29.NYM); **22** 404 (including all 2025 months and 2026 F–N). True-front dates with 18 tenors: **54** (2026-06-01 … 2026-08-17). Need 750 (250 burn-in + 500 OOS). **Gate fail.**

---

## What this does *not* do

- Does **not** establish H-KS-FTS, F-SKILL, or V-VALUE.  
- Does **not** convert leftover far-month history into CL1.  
- Does **not** license trading.

**Lock-time Amb warning:** Attempting a stand-in does **not** drop Amb. **Amb ≠ clearance.**

---

## Reopen

A freeze-matching historical CL1–CL18 tape (live CME, or another stipulated source that actually has expired fronts). Nasdaq CHRIS was tried in this environment (**403** / feed deprecated). Honest **established** still **stops**.
