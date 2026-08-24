# Exploration queue — spot 21-day trend (Track B)

**Date:** 2026-08-24  
**Lock:** `Lock_Hunt_Spot_Trend.md` (**L-SPOT-QUEUE**) · this pulse `Lock_Hunt_Spot_Logit.md`  
**Machine register:** `data/spot_trend_queue.json`  
**Status:** **C-SPOT-LOGIT** is the active pulse. Confirm still unseen at lock time for LOGIT.

---

## 0. Plain-language framing

**What we’re doing:** Keep a written list of *kinds* of idea to try on the same spot-trend question, and a list of ideas that already failed. One kind at a time. The recent exam is never where we invent a new rule.

**What we need from you:** Nothing this pulse. Optional later: leave, or name a different futures recipe.

**What this does *not* mean:** A bot that watches misses and rewrites itself. Unburning burned rules. Changing 21 days. Remxing the Brent CROSS survivor into this fit.

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

## This pulse (active) — **C-SPOT-LOGIT** / **L-HUNT-SPOT-LOGIT**

| ID | Role |
|----|------|
| **H-SPOT-LOGIT-FULL** | Expanding-window logistic: intercept + sign_num + \|r21\|; call by P≥0.5 |
| **H-SPOT-LOGIT-SIGN** | Same clock; intercept + sign_num only |
| Continuation | **Baseline, not a horse** |

**Burned (do not retune / do not unburn):** H-SPOT-FLIP-HOLD, H-SPOT-REV, H-SPOT-INV-CONT, H-SPOT-INV-FADE on **WTI** and **Brent**; **H-SPOT-CROSS-B2W** on **WTI**. Do **not** retune **H-SPOT-CROSS-W2B**.

---

## Next classes (named, not scored this pulse)

| Queue ID | Class | Why it is a different class |
|----------|-------|------------------------------|
| *(none)* | — | Queue empty after this class |

**Already run:** **C-SPOT-CROSS** (**L-PULSE-SPOT-CROSS-1**). **C-SPOT-INV** (**L-PULSE-SPOT-INV-1**; no survivor). First pulse **L-PULSE-SPOT-1** also no survivor. **C-SPOT-LOGIT** is this pulse.

**Not queued (refused):** change 21; peer/inventory remix into the logit; unburn burned rows; retune W2B; invent a new spot class after scores without a new operator pick.

---

*Failed discovery is an allowed useful negative. The project learns. The horse does not peek.*
