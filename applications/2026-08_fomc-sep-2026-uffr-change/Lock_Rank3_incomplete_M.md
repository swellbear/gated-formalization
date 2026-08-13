# Lock Record — Rank 3 (incomplete: M OR-slot)

**Superseded 2026-08-12:** operator `live shots` = **M3**. Complete package: `Lock_Rank3_Q3O2L1M3B1.md`. This file is the audit trail of the open OR-slot only.

**Date:** 2026-08-12  
**Application:** `2026-08_fomc-sep-2026-uffr-change`  
**Operator selection:** **Rank 3** + URL `https://polymarket.com/event/fed-decision-in-september-762`  
**Status:** **SUPERSEDED** — M later locked as M3. Historical: Point **M** was an open OR-slot.

---

## Locked so far

| Point | Lock |
|-------|------|
| **Q (G1)** | **Q3 Odds** — named market’s **published price** is the odds vehicle for the **same** upper-bound-change event |
| **O (G2)** | **O2 Operator-supply** — venue + displayed options from that URL (fetched 2026-08-12) |
| **L (G4)** | **L1 Statement** — live source for the **print** leftover remains the FOMC statement after Sep 15–16 2026 (not this page; not June SEP) |
| **B (G3)** | **B1 Pre-meeting in-force** — upper bound in force immediately before that meeting |
| **M (G5)** | **UNSET** — M2 P-BaseCase / M3 P-NonNegligible |

**Named source class (odds vehicle):** Polymarket event **Fed Decision in September?** (`fed-decision-in-september-762`). Published figures on the event page: displayed **Yes** prices (¢) and displayed **%** per bracket. Do not invent mean vs median. Rival venues (Kalshi, CME FedWatch) are **different classes**.

**Displayed options (O2, from fetch):**

| Bracket | Displayed Yes | Displayed % (header) |
|---------|---------------|----------------------|
| 50+ bps decrease | 0.6¢ | <1% (card also shows 1%) |
| 25 bps decrease | 1.1¢ | 1.0% |
| No change | 67¢ | 67% |
| 25 bps increase | 33¢ | 33% |
| 50+ bps increase | 0.5¢ | <1% |

**Vintage:** Event page description “as of August 13, 2026”; fetch this cycle 2026-08-12. Volume headline ~$29.9M. These are **separate Yes/No markets**; ¢ need not sum to 100.

**Deviation:** Moderate (odds fork). Contract text on the page matches the operator paste.

---

## Scope label

**Under Rank 3 (Q3+O2+L1+B1; M unset) only.**

---

## Lock-time Amb warning

Fixing the venue and brackets **drops Amb**. That does **not** establish that “No change” (or any bracket) is the expected path or a live shot. **Low Amb ≠ clearance.** Conflicted-source: a trading market must **not** be the sole support for affirming a locked modal bar.

---

## Open OR-slot (mandatory stop)

Pick **one**:

- **M2 P-BaseCase** — the market’s published prices are read as an **expected / central path** (ordinary: highest Yes = base case).  
- **M3 P-NonNegligible** — prices are read as **live-shot** sizes, not as “the” expected path.

```
lock M2
OR
lock M3
OR
Formally accept either: { M2 , M3 }
```

Until then: **no** P-BaseCase/P-NonNegligible pulse. Prices may be censused as **what the page printed**, not as bar-met.

---

## Dependents

- **D-OPTIONS / D-PRICE** (page census): runnable as descriptive print of brackets + ¢ — **not** bar-met.  
- **F-PRINT:** park until Sep 15–16 2026 FOMC statement (L1).  
- **Odds bar:** blocked on M.

## Not settled

That the FOMC will hold, hike, or cut; that 67¢ **is** P-BaseCase; June SEP; this page as the September statement.
