# Plain-language card

**Application:** `2026-08_oil-futures-predictive-model`  
**Date / checkpoint:** 2026-08-24 · EIA spot expanding-window logistic (L-PULSE-SPOT-LOGIT-1)

---

## What we’re doing

We let the computer fit a simple rule on **older** cash 21-day days only (whether the last 21 days were up or down, and how large that move was), then asked whether that beat “whatever just happened will happen again.” It beat the older exam for WTI and Brent, but **lost** the recent exam on every locked window for both oils. Burned rules stayed burned. This is not futures skill and not a trade.

## What we need from you

Nothing required. Optional: leave, name a **different** futures recipe on Yahoo, or explicitly name a new spot idea (unnamed ideas stop).

**Preferred reply:** click A / B / C. Typed: `leave skill not shown` · `name horse …` · `name source class …`

## What a “yes” / this update means

The first train-arm spot drawer is on the card. A discovery beat that loses confirm is **not** a pass. The named Track B queue is now **empty**.

## What this does *not* mean

That a fitted “oil model” works. That anyone should trade. That we should rewrite the fit after the recent misses.

---

## Details (technical record — secondary)

| Item | Value |
|------|--------|
| Claim-freeze / claim under test | Rank 4 F-SKILL **parked**; **L-HUNT-SPOT-LOGIT** vs continuation |
| Amb | **1.0** (**≠ clearance**) |
| Locks / package IDs | **H-SPOT-LOGIT-FULL**; **H-SPOT-LOGIT-SIGN** |
| Discovery | WTI **0.532** vs 0.508; Brent **0.550** vs 0.506; survivor **FULL** both |
| Confirm | FULL **loses** 500/250/750 both boards |
| Artifact pointers | `Lock_Hunt_Spot_Logit.md` · `PULSE_Hunt_Spot_Logit.md` · `04_Material_Admission_Spot_Logit.md` |

---

*Standing rule: Dual-audience communication. Glossary: `docs/READER_GLOSSARY.md`.*
