# Lock Record — Rank 3 complete (`Q3+O2+L1+M3+B1`)

**Date:** 2026-08-12  
**Application:** `2026-08_fomc-sep-2026-uffr-change`  
**Operator selection:** Rank 3 + URL, then **`live shots`** = **M3 P-NonNegligible**  
**Prior:** `Lock_Rank3_incomplete_M.md` (M OR-slot). This record **completes** the package.  
**Status:** **LOCK COMPLETE** — OR-slot resolved as singleton **M3**.

---

## Locked package

| Point | Lock |
|-------|------|
| **Q (G1)** | **Q3 Odds** — named market’s **published price** is the odds vehicle for the **same** upper-bound-change event |
| **O (G2)** | **O2 Operator-supply** — venue + displayed options from `https://polymarket.com/event/fed-decision-in-september-762` (fetched 2026-08-12) |
| **L (G4)** | **L1 Statement** — live source for **F-PRINT** remains the FOMC statement after Sep 15–16 2026 (not this page; not June SEP) |
| **B (G3)** | **B1 Pre-meeting in-force** — upper bound in force immediately before that meeting |
| **M (G5)** | **M3 P-NonNegligible** — published prices are read as **live-shot sizes**, not as “the” expected / central path |

**Named source class (odds vehicle):** Polymarket event **Fed Decision in September?** (`fed-decision-in-september-762`). Published figures: displayed **Yes** prices (¢) and displayed **%** per bracket. Do not invent mean vs median. Rival venues (Kalshi, CME FedWatch) are **different classes**.

**Displayed options (O2, from fetch):**

| Bracket | Displayed Yes | Displayed % (header) |
|---------|---------------|----------------------|
| 50+ bps decrease | 0.6¢ | <1% (card also shows 1%) |
| 25 bps decrease | 1.1¢ | 1.0% |
| No change | 67¢ | 67% |
| 25 bps increase | 33¢ | 33% |
| 50+ bps increase | 0.5¢ | <1% |

**Vintage:** Event page “as of August 13, 2026”; fetch this cycle 2026-08-12. Volume headline ~$29.9M. Separate Yes/No markets; ¢ need not sum to 100.

**Deviation:** Moderate (odds fork). Contract text on the page matches the operator paste.

---

## Scope label

**Under Rank 3 (`Q3+O2+L1+M3+B1`) only.**

M3 does **not** promote 67¢ into P-BaseCase. Highest Yes is **not** locked as the expected path. Do **not** silently strengthen live shots into “the Fed will hold.”

---

## Lock-time Amb warning

Fixing M3 **drops Amb** by setting the odds **bar height**. That does **not** establish that any bracket **is** a live shot. **Low Amb ≠ clearance.** Conflicted-source: a trading market must **not** be the sole support for affirming P-NonNegligible.

---

## Dependents now in scope

- **Odds bar (P-NonNegligible):** runnable as a named-class pulse on the locked vehicle. Honest met → establishment-stop. Conflicted-only → HOLD affirmation / not established.  
- **F-PRINT:** still park until Sep 15–16 2026 FOMC statement (L1).  
- **D-OPTIONS / D-PRICE:** already admitted as census / conflicted print — not bar-met.

## Not settled by this lock

That the FOMC will hold, hike, or cut; that 33¢ **is** a cleared live shot; that 67¢ is the expected path; June SEP; this page as the September statement.
