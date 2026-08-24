# Exploration queue — spot 21-day trend (Track B)

**Date:** 2026-08-24  
**Lock:** `Lock_Hunt_Spot_Trend.md` (**L-SPOT-QUEUE**) · this pulse `Lock_Hunt_Spot_Logit.md`  
**Machine register:** `data/spot_trend_queue.json`  
**Status:** **C-SPOT-LOGIT** scored. Discovery survivors **FULL** both boards; confirm **lost** continuation every window. Named queue **empty**.

---

## 0. Plain-language framing

**What we’re doing:** Keep a written list of *kinds* of idea to try on the same spot-trend question, and a list of ideas that already failed. One kind at a time. The recent exam is never where we invent a new rule.

**What we need from you:** Optional: leave, name a different futures recipe on Yahoo, or explicitly name a new spot class.

**What this does *not* mean:** A bot that watches confirm misses and rewrites the fit. Unburning burned rules. Changing 21 days.

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

## This pulse (scored) — **C-SPOT-LOGIT** / **L-HUNT-SPOT-LOGIT**

| ID | Role | Result |
|----|------|--------|
| **H-SPOT-LOGIT-FULL** | Expanding logistic: intercept + sign + \|r21\| | Discovery beat both boards; confirm **lose** all windows both boards. Do **not** retune. |
| **H-SPOT-LOGIT-SIGN** | Expanding logistic: intercept + sign | Discovery tie with FULL (not a loss). Not sent to confirm. |
| Continuation | **Baseline, not a horse** | |

**Burned (do not retune / do not unburn):** H-SPOT-FLIP-HOLD, H-SPOT-REV, H-SPOT-INV-CONT, H-SPOT-INV-FADE on **WTI** and **Brent**; **H-SPOT-CROSS-B2W** on **WTI**. Do **not** retune **H-SPOT-CROSS-W2B** or **H-SPOT-LOGIT-FULL**.

---

## Next classes (named, not scored this pulse)

| Queue ID | Class | Why it is a different class |
|----------|-------|------------------------------|
| *(none)* | — | Named Track B queue empty |

**Already run:** **C-SPOT-LOGIT** (**L-PULSE-SPOT-LOGIT-1**). **C-SPOT-CROSS**. **C-SPOT-INV**. **L-PULSE-SPOT-1**.

**Not queued (refused):** change 21; remix confirm losses into a new feature; unburn; invent a spot class after scores without a new operator pick.

---

*Failed confirm after a discovery beat is an allowed useful negative. The project learns. The horse does not peek.*
