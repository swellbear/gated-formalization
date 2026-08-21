# Exploration queue — spot 21-day trend (Track B)

**Date:** 2026-08-21  
**Lock:** `Lock_Hunt_Spot_Trend.md` (**L-SPOT-QUEUE**) · this pulse `Lock_Hunt_Spot_Cross.md`  
**Machine register:** `data/spot_trend_queue.json`  
**Status:** **C-SPOT-CROSS** is the active pulse. Confirm still unseen at lock time for CROSS.

---

## 0. Plain-language framing

**What we’re doing:** Keep a written list of *kinds* of idea to try on the same spot-trend question, and a list of ideas that already failed. One kind at a time. The recent exam is never where we invent a new rule.

**What we need from you:** Nothing this pulse. Optional later: next queued class, or leave.

**What this does *not* mean:** A bot that watches misses and rewrites itself. Unburning burned rules. Changing 21 days.

---

## Rules (frozen)

1. **One class, two horses max** per pulse.  
2. Freeze the rule **before** discovery. Discovery **before** confirm.  
3. Pick one only if it **strictly beats continuation**. Else **no survivor**. Do not pick least-bad.  
4. **Burned** rows are not remixed after hit-rate.  
5. Confirm last 500 / 250 / 750 **never** trains.  
6. Train arm = past-only at *t*, and only inside a recipe written in advance.  
7. Wrong object (CL RMSE, Truth Social, CFTC, overnight gap) stays **out** of this queue.

---

## This pulse (active) — **C-SPOT-CROSS** / **L-HUNT-SPOT-CROSS**

| ID | Role |
|----|------|
| **H-SPOT-CROSS-B2W** | Brent’s 21-day sign as the call on the **WTI** board |
| **H-SPOT-CROSS-W2B** | WTI’s 21-day sign as the call on the **Brent** board |
| Continuation | **Baseline, not a horse** |

**Burned (do not retune / do not unburn):** H-SPOT-FLIP-HOLD, H-SPOT-REV, H-SPOT-INV-CONT, and H-SPOT-INV-FADE on **WTI** and on **Brent**.

---

## Next classes (named, not scored this pulse)

| Queue ID | Class | Why it is a different class |
|----------|-------|------------------------------|
| **C-SPOT-LOGIT** | Expanding-window logistic on past-only sign + abs return | First use of the train arm with fitted coefficients |

**Already run:** **C-SPOT-INV** (**L-PULSE-SPOT-INV-1**; no survivor). First pulse **L-PULSE-SPOT-1** also no survivor. **C-SPOT-CROSS** is this pulse.

**Not queued (refused):** change 21 to 5/63/252 after scores; dollar-spread / crack / fade-of-peer after scores; Cushing-only; Bloomberg consensus; percent-of-OI; DJT lexicon; COT remix; gap remix; unburn FLIP-HOLD/REV/INV.

---

*Failed discovery is an allowed useful negative. The project learns. The horse does not peek.*
