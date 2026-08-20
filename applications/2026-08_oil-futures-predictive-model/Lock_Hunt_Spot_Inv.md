# Lock Record — EIA weekly crude inventory surprise overlay (Track B queue)

**Date:** 2026-08-20  
**Application:** `2026-08_oil-futures-predictive-model`  
**Operator selection:** **B** — chip the next queued spot class (**C-SPOT-INV**)  
**App-local lock IDs:** **L-HUNT-SPOT-INV** · **L-STANDIN-EIA-INV** · **H-SPOT-INV-CONT** · **H-SPOT-INV-FADE**  
**Status:** **IN FORCE as protocol + named drawer (cap = these two horses).** Written **before** last-500 confirm scores. Same 21-day spot object as `Lock_Hunt_Spot_Trend.md`. Do **not** unburn H-SPOT-FLIP-HOLD / H-SPOT-REV. Do **not** change 21. Confirm is **one** survivor per scoreboard (or none). F-SKILL stays **leave skill not shown**.

---

## 0. Plain-language framing

**What was decided:**  
Keep the same cash WTI / Brent 21-day question. Add the public weekly U.S. crude **stockpile** report. “Surprise” here is **not** a Wall Street poll. It is: this week’s change in those stockpiles, minus the average of the previous four weekly changes. If stockpiles came in tighter than that recent pace, one rule calls **up** for the next 21 days; the other calls **down**. The computer may pick **one** per oil, only if it already beat “the trend continues” on **older** days. The two rules that already failed are **not** brought back.

**What this settles:**  
The inventory series, the naive-surprise formula, the Wednesday-release clock, the two-horse cap, and that 21 and the burned rows stay frozen.

**What this does *not* settle:**  
That inventories “drive” oil. That this matches a Bloomberg survey surprise. That skill is shown. That anyone should trade.

---

## Named protocol (quote this)

**Scope:** **Under Rank 4 (F-SKILL parked) + L-HUNT-SPOT-TREND + L-STANDIN-EIA-SPOT + L-SPOT-ARMS + L-SPOT-QUEUE + L-HUNT-SPOT-INV + L-STANDIN-EIA-INV**.

Parent object, 21-day label, flip (descriptive), skill target, continuation baseline, skip mask, discovery cutoff, confirm windows, and three arms are **inherited** from `Lock_Hunt_Spot_Trend.md`. This pulse only names a **new two-horse overlay**.

**WTI-met ≠ Brent-met.** Same two scoreboards.

### 1. Inventory archive (L-STANDIN-EIA-INV)

**Series:** EIA weekly **U.S. ending stocks of crude oil excluding SPR** (**PET.WCESTUS1.W**).

**Named fallback:** FRED **WCESTUS1** (EIA-sourced reprint) if the EIA file fails.

**OUT of this pulse (frozen):** Cushing-only stocks; gasoline / distillate / total products; SPR; API Tuesday estimates; Bloomberg / Reuters survey consensus; “percent of capacity.” Do **not** add those after hit-rate.

**Vehicle fail:** fetch fails, or weekly reports whose release falls in the discovery **spot** span **< 30**, or either spot board still **< 250** discovery-eligible issue dates → stop.

### 2. Naive surprise (not a Street poll)

On weekly report *w* (need at least five stock prints):

- `Δ_w` = stocks_w − stocks_{w−1}  
- `expected_w` = mean of `Δ_{w−4} … Δ_{w−1}` (four **previous** week-changes; current week **out**)  
- `surprise_w` = `Δ_w − expected_w`

| Sign | Meaning |
|------|---------|
| **< 0** | Draw surprise (tighter / smaller build than the last four changes) |
| **> 0** | Build surprise |
| **= 0** | No surprise (including not enough history) |

Print-match ≠ Bloomberg surprise. This is a **named naive** residual, not “the” inventory surprise.

### 3. Clock

EIA Weekly Petroleum Status Report: week **ending Friday**, typical release **Wednesday ~10:30 ET**.

**Release date** = the Wednesday after that Friday (Friday + 5 calendar days). If the file dates Saturday, treat Friday as the prior day, then +5.

**Known as of** spot issue date *t*: latest report whose **release date ≤ calendar day before *t*** (`release_date ≤ t−1`). Same-Wednesday 10:30 **never** enters that day’s spot print.

Carry the last known surprise forward until the next known report (silent weeks keep the last surprise; they are **not** zeroed).

Before the first known report, surprise = **0**.

### 4. Horses (cap 2)

Same eligible issue dates as Track B (index ≥ 22; sign_t and sign_{t−1} and next-21 truth in {Up, Down}). Continuation = sign_t (baseline, not a horse).

| ID | Skill call at *t* |
|----|-------------------|
| **H-SPOT-INV-CONT** | Surprise **< 0** → **Up**; surprise **> 0** → **Down**; surprise **= 0** → continuation |
| **H-SPOT-INV-FADE** | Surprise **< 0** → **Down**; surprise **> 0** → **Up**; surprise **= 0** → continuation |

Do **not** score H-SPOT-FLIP-HOLD or H-SPOT-REV (burned). Do **not** blend with DJT / COT / gap. Do **not** change 21. Train arm = **N/A** (no fitted coefficients).

Ties (both beat, equal hit-rate): keep **H-SPOT-INV-CONT** (earlier in this lock).

### 5. Discovery / confirm

Inherited. Discovery cutoff **2023-08-21**; last **500** eligible of that prefix; pick one only if **strictly beats** continuation; else **no survivor**. Confirm that one horse (or skip) on last **500 / 250 / 750**. Confirm never trains. Yahoo promote **does not apply**. Honest **established** still **stops**.

Discovery **before** confirm. `--stage discovery` must not compute confirm windows.

### 6. Queue

**C-SPOT-INV** is this pulse (no longer queued). Still queued, **not scored:** **C-SPOT-CROSS**, **C-SPOT-LOGIT**. Burned FLIP-HOLD / REV stay burned.

---

## What this does *not* do

- Does **not** establish F-SKILL, V-VALUE, or spot-trend skill by existing.  
- Does **not** claim Street consensus surprise.  
- Does **not** unburn the first two horses or retune 21.  
- Does **not** license a trade, Phase 2, or DataMine.

**Lock-time Amb warning:** Running this hunt does **not** drop V-SRC leftover-ambiguity. **Amb ≠ clearance.**

---

## Reopen

`leave skill not shown` · next queued **C-SPOT-CROSS** (do **not** unburn INV rows after scores; do **not** change 21) · `name horse …` on Yahoo (different **CL** recipe) · `leave screen rule`. Honest **established** still **stops**.
