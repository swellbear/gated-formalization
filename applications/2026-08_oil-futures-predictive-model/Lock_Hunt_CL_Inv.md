# Lock Record — EIA weekly crude inventory overlay on Yahoo CL (F-SKILL screen)

**Date:** 2026-08-24  
**Application:** `2026-08_oil-futures-predictive-model`  
**Operator selection:** **C** — next best different CL horse on Yahoo (`whatever you think is next best CL`)  
**App-local lock IDs:** **L-HUNT-CL-INV** · **L-STANDIN-EIA-INV-CL** · **H-CL-INV-SURP** · **H-CL-INV-WOW**  
**Status:** **IN FORCE as protocol + named drawer (cap = these two horses).** Written **before** last-500 confirm scores. Confirm is **one** survivor (or none). F-SKILL **not** auto-established. Unparks F-SKILL scoring on this object only (parent Rank 4 still split).

---

## 0. Plain-language framing

**What was decided:**  
Go back to the futures skill leftover on the Yahoo stand-in tape. The next different recipe uses the public weekly U.S. crude **stockpile** report (same series already fetched for Track B), not as a cash 21-day call, but as an extra number in a next-session CL forecast versus “assume no change.” One horse uses a naive “surprise” (this week’s change minus the average of the prior four changes). The other uses the raw week-over-week change. The computer may pick **one**, only if it already beat no-change on **older** whole sessions. Burned CL horses (lag, sparse, gap, pretell, DJT, COT) are **not** retuned.

**What this settles:**  
The inventory series, two features, the EIA Wednesday-release clock into F-ON/F-DAY/F-CC lags, the two-horse cap, and discovery/confirm under **L-SCREEN-Y-PROMOTE**.

**What this does *not* settle:**  
That inventories “drive” oil. That a Wednesday print edge is the locked next-session test. That skill is shown. That anyone should trade. That Track B spot results transfer.

---

## Named protocol (quote this)

**Scope:** **Under Rank 4 + L-SESS + F-SRC-CME-TAPE + L-STANDIN-Y-CLF + L-SCREEN-Y-PROMOTE + L-HUNT-CL-INV + L-STANDIN-EIA-INV-CL**.

This is a **capped named drawer**, not an unbounded inventory kitchen sink. Cap = **these two horses**. Do **not** expand after seeing scores. Do **not** hunt on last 500. Do **not** switch to Cushing-only, products, SPR, API, or Bloomberg consensus after RMSE. Do **not** retune lag / sparse / gap / pretell / DJT / COT. Do **not** remix Track B spot horses into this F-CC object.

### 1. Archive (L-STANDIN-EIA-INV-CL)

**Series:** EIA weekly **U.S. ending stocks of crude oil excluding SPR** (**PET.WCESTUS1.W**). Reuse `data/eia_weekly_crude_exspr.csv` (same vehicle as Track B inventory pulse).

**CL tape:** Yahoo `CL=F` Open/Close stand-in (`data/clf_yahoo_standin.csv`).

**OUT of this pulse (frozen):** Cushing-only; gasoline / distillate / products; SPR; API Tuesday; Bloomberg / Reuters survey consensus; percent-of-capacity; spot 21-day hit-rate as the scoreboard.

**Vehicle fail:** inventory fetch missing, or weekly reports with release in the discovery CL span **< 30**, or CL discovery pool too thin for last-500 F-CC → stop.

### 2. Features (two horses)

On weekly report *w* (need at least five stock prints for surprise):

- `Δ_w` = stocks_w − stocks_{w−1}  
- `expected_w` = mean of `Δ_{w−4} … Δ_{w−1}`  
- `surprise_w` = `Δ_w − expected_w` (0 if not enough history)

| ID | Signal `s` (OLS feature) |
|----|--------------------------|
| **H-CL-INV-SURP** | Latest known **surprise**, carried forward |
| **H-CL-INV-WOW** | Latest known **Δ** (week-over-week change), carried forward |

OLS scale: divide `s` by **10000** (`1e4`). Frozen. Naive surprise ≠ Bloomberg surprise.

### 3. Clock

EIA Weekly Petroleum Status Report: week ending Friday; typical release **Wednesday**.

**Release date** = Wednesday after that Friday (Friday + 5 calendar days) as stored in the CSV.

**Known as of** calendar date *d*: latest report with `release_date ≤ d`. Carry forward until the next known release.

| Window | Issued | Inventory known as of |
|--------|--------|----------------------|
| **F-ON / F-CC** | t−1 settle | CL date **t−2** |
| **F-DAY** | t open | CL date **t−1** |

Same lag pattern as COT. A Wednesday 10:30 release does **not** enter that Wednesday’s F-CC via t−2.

Before the first known report, `s` = **0**.

### 4. OLS

Expanding, intercept, min train **250**. F-ON/F-CC: `[1, r_ON,t−1, r_DAY,t−1, s]`. F-DAY: `[1, r_ON,t, r_DAY,t−1, s]`. Rank-deficient or n_train < 250 → **0**. Missing CL y/x → skip (same as H-LAG / COT).

### 5. Discovery / confirm

| Slot | Rule |
|------|------|
| **Discovery cutoff** | CL sessions **≤ 2023-08-21** |
| **Discovery scoreboard** | F-CC RMSE vs 0 on last **500** of that prefix |
| **Selection** | Lowest F-CC RMSE **only if** it **strictly beats** 0. If neither → **no survivor** |
| **Ties** | Keep **H-CL-INV-SURP** (earlier in this lock) |
| **Confirm** | That **one** horse (or skip). Last **500 / 250 / 750** vs 0. No runner-up |
| **Promote** | **L-SCREEN-Y-PROMOTE**: last-500 F-CC **strictly beats** 0 **and** last-250 and last-750 F-CC **≤** 0. Yahoo win ≠ live ≠ F-SKILL-met |
| **Establishment-stop** | Honest `04` that would say **established** still **stops**. No DataMine auto-open |

Discovery **before** confirm. `--phase discovery` must not compute confirm windows.

---

## What this does *not* do

- Does **not** establish F-SKILL, F-ON, F-DAY, F-CC, or V-VALUE by existing.  
- Does **not** claim Street consensus surprise.  
- Does **not** clear Track B spot skill.  
- Does **not** license a trade, Phase 2, or DataMine.

**Lock-time Amb warning:** Running this hunt does **not** drop V-SRC leftover-ambiguity. **Amb ≠ clearance.**

---

## Reopen

`leave skill not shown` · `name horse …` (a **different** CL recipe; do **not** add Cushing/API/Bloomberg after scores; do **not** retune burned drawers) · `leave screen rule`. Live CME **only if** **L-SCREEN-Y-PROMOTE** fires. Honest **established** still **stops**.
