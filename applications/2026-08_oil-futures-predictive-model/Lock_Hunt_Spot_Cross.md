# Lock Record — EIA spot WTI ↔ Brent 21-day cross-bench overlay (Track B queue)

**Date:** 2026-08-21  
**Application:** `2026-08_oil-futures-predictive-model`  
**Operator selection:** **B** — chip the next queued spot class (**C-SPOT-CROSS**)  
**App-local lock IDs:** **L-HUNT-SPOT-CROSS** · **H-SPOT-CROSS-B2W** · **H-SPOT-CROSS-W2B**  
**Status:** **IN FORCE as protocol + named drawer (cap = these two horses).** Written **before** last-500 confirm scores. Same 21-day spot object as `Lock_Hunt_Spot_Trend.md`. Do **not** unburn H-SPOT-FLIP-HOLD / H-SPOT-REV / H-SPOT-INV-CONT / H-SPOT-INV-FADE. Do **not** change 21. Confirm is **one** survivor per scoreboard (or none). F-SKILL stays **leave skill not shown**.

---

## 0. Plain-language framing

**What was decided:**  
Keep the same cash WTI / Brent 21-day question. This pulse asks a cross-bench question: use **WTI’s** last 21-day up/down label as the call for **Brent’s** next 21 days, and the reverse. Each oil still has its own scoreboard. The computer may pick **one** per oil, only if that oil’s named cross-call already beat “the trend continues” on **older** days. Burned rules stay burned. 21 days stays 21.

**What this settles:**  
Which horse lives on which board, how the other oil’s sign is dated, the two-horse cap, and that 21 and the burned rows stay frozen.

**What this does *not* settle:**  
That WTI “leads” Brent (or the reverse). That a dollar spread or crack is a horse. That skill is shown. That anyone should trade.

---

## Named protocol (quote this)

**Scope:** **Under Rank 4 (F-SKILL parked) + L-HUNT-SPOT-TREND + L-STANDIN-EIA-SPOT + L-SPOT-ARMS + L-SPOT-QUEUE + L-HUNT-SPOT-CROSS**.

Parent object, 21-day label, flip (descriptive), skill target, continuation baseline, skip mask, discovery cutoff, confirm windows, and three arms are **inherited** from `Lock_Hunt_Spot_Trend.md`. This pulse only names a **new two-horse overlay**. Reuse the existing EIA spot CSVs. No new fetch class.

**WTI-met ≠ Brent-met.** Same two scoreboards.

### 1. Cross-bench overlay (not a spread)

On a home-board issue date *t*:

**Peer sign** = the 21-day Up/Down/Flat label of the **other** oil, taken from the latest peer print whose **calendar date ≤ *t***. Same-day completed prints are allowed (parallel to continuation using the home print at *t*). Silent peer days **carry** the last known peer sign; they are **not** zeroed and **not** treated as Flat.

If there is no peer history yet, or the peer sign is **Flat**, the horse calls **continuation** (home sign at *t*).

**OUT of this pulse (frozen):** WTI–Brent **dollar spread** as a horse; crack / products; futures (CL / ICE); fade-of-peer (opposite of the peer sign); rolling average of the peer; a one-print hold of the peer (*t−1* only — that is burned FLIP-HOLD’s clock, not this class). Do **not** add those after hit-rate.

**Vehicle fail:** either spot board still **< 250** discovery-eligible issue dates, **or** fewer than **250** of that board’s discovery last-500 have a peer sign in {Up, Down} → stop. Do not invent a lag or a spread after scores.

### 2. Horses (cap 2)

Same eligible issue dates as Track B (index ≥ 22; sign_t and sign_{t−1} and next-21 truth in {Up, Down}). Continuation = home sign_t (baseline, not a horse).

Each horse is **board-specific**. Scoring the tautology (WTI’s own sign as the WTI call) is **OUT** — that *is* continuation.

| ID | Home board | Skill call at *t* |
|----|------------|-------------------|
| **H-SPOT-CROSS-B2W** | **WTI** | Brent peer sign if in {Up, Down}; else continuation |
| **H-SPOT-CROSS-W2B** | **Brent** | WTI peer sign if in {Up, Down}; else continuation |

Do **not** score H-SPOT-FLIP-HOLD, H-SPOT-REV, H-SPOT-INV-CONT, or H-SPOT-INV-FADE (burned). Do **not** blend with DJT / COT / gap. Do **not** change 21. Train arm = **N/A** (no fitted coefficients).

Ties: one horse per board, so tie-break **N/A**. If that horse does not strictly beat continuation → **no survivor** for that board.

### 3. Discovery / confirm

Inherited. Discovery cutoff **2023-08-21**; last **500** eligible of that prefix; pick the board’s horse only if it **strictly beats** continuation; else **no survivor**. Confirm that one horse (or skip) on last **500 / 250 / 750**. Confirm never trains. Yahoo promote **does not apply**. Honest **established** still **stops**.

Discovery **before** confirm. `--stage discovery` must not compute confirm windows.

### 4. Queue

**C-SPOT-CROSS** is this pulse (no longer queued). Still queued, **not scored:** **C-SPOT-LOGIT**. Burned FLIP-HOLD / REV / INV-CONT / INV-FADE stay burned.

---

## What this does *not* do

- Does **not** establish F-SKILL, V-VALUE, or spot-trend skill by existing.  
- Does **not** claim a lead–lag theorem.  
- Does **not** unburn prior horses or retune 21.  
- Does **not** license a trade, Phase 2, or DataMine.

**Lock-time Amb warning:** Running this hunt does **not** drop V-SRC leftover-ambiguity. **Amb ≠ clearance.**

---

## Reopen

`leave skill not shown` · next queued **C-SPOT-LOGIT** (do **not** unburn CROSS rows after scores; do **not** change 21) · `name horse …` on Yahoo (different **CL** recipe) · `leave screen rule`. Honest **established** still **stops**.
