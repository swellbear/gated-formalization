# Exploration queue — spot 21-day trend (Track B)

**Date:** 2026-08-20  
**Lock:** `Lock_Hunt_Spot_Trend.md` (**L-SPOT-QUEUE**)  
**Machine register:** `data/spot_trend_queue.json`  
**Status:** Protocol in force **before** confirm scores. This file does **not** score queued classes.

---

## 0. Plain-language framing

**What we’re doing:** Keep a written list of *kinds* of idea to try on the same spot-trend question, and a list of ideas that already failed. One kind at a time. The recent exam is never where we invent a new rule.

**What we need from you:** Nothing this pulse. Optional later: authorize the next queued class, or leave skill not shown.

**What this does *not* mean:** A bot that watches misses and rewrites itself. A kitchen sink of DJT / COT / gaps. A pass because we tried many things.

---

## Rules (frozen)

1. **One class, two horses max** per pulse (this pulse already named).  
2. Freeze the rule **before** discovery. Discovery **before** confirm.  
3. Pick one only if it **strictly beats continuation**. Else **no survivor**. Do not pick least-bad.  
4. **Burned** rows are not remixed after hit-rate.  
5. Confirm last 500 / 250 / 750 **never** trains.  
6. Train arm = past-only at *t*, and only inside a recipe written in advance.  
7. Wrong object (CL RMSE, Truth Social, CFTC, overnight gap) stays **out** of this queue.

---

## This pulse (active)

| ID | Role |
|----|------|
| **H-SPOT-FLIP-HOLD** | One-print hold (call sign as of *t−1*) |
| **H-SPOT-REV** | Always opposite of sign as of *t* |
| Continuation | **Baseline, not a horse** |

**Burned (fill after discovery, not before):** none at lock time.

---

## Next classes (named, not scored this pulse)

| Queue ID | Class | Why it is a different class |
|----------|-------|------------------------------|
| **C-SPOT-INV** | EIA weekly inventory surprise overlay | Different public series; same 21-day target |
| **C-SPOT-CROSS** | WTI sign as Brent call (and reverse) | Cross-bench, not a window retune |
| **C-SPOT-LOGIT** | Expanding-window logistic on past-only sign + abs return | First use of the train arm with fitted coefficients |

Do **not** score these until a later lock quotes this table and freezes that class’s horses.

**Not queued (refused):** change 21 to 5/63/252 after scores; percent-of-OI; DJT lexicon; COT remix; gap remix; “blend the two horses.”

---

*Failed discovery is an allowed useful negative. The project learns. The horse does not peek.*
