# Plain-language card

**Application:** `2026-08_oil-futures-predictive-model`  
**Date / checkpoint:** 2026-08-17 · named horses scored (L-PULSE-HORSES-1)

---

## What we’re doing

We named two recipes and tested what we could. A simple model that uses yesterday’s night and day moves **did not beat** “assume no change” for the whole trip. A tiny overnight improvement is **not** a pass. The published curve method **could not run**: Yahoo does not keep expired months, so there is no historical CL1–CL18. This is not a trade.

## What we need from you

Nothing required. Optional: wait for official CME (or another real curve tape), or name a different recipe.

**Preferred reply:** click A / B / C. Typed: `leave skill not shown` · `live CME / curve tape …` · `name horse …`

## What a “yes” / this update means

The lagged-return recipe is **on the card and scored**. Kearney–Shang stayed **unscored** because the curve stand-in failed. Naming and scoring is not a pass.

## What this does *not* mean

That a model beats last settlement. That nighttime is now shown. That anyone should trade. That an oil offshoot is cleared.

---

## Details (technical record — secondary)

| Item | Value |
|------|--------|
| Claim-freeze / claim under test | Rank 4 F-CC + L-SESS; **H-LAG-WF** scored; **H-KS-FTS** not run |
| Amb | **1.0** (**≠ clearance**) — leftover is V-SRC |
| Locks / package IDs | Rank 4; D-EXIST-MET-FT; V-COST-V2; L-STANDIN-Y-CLF; **L-STANDIN-Y-CHAIN**; **H-LAG-WF**; L-PULSE-HORSES-1 |
| Method verdict label (if any) | Stable Provisional (split) — hard stop (residuals live) |
| H-LAG last-500 vs 0 | F-ON 0.01283 / 0.01291 (tiny dip) · F-DAY 0.02670 / 0.02663 (loss) · F-CC 0.02888 / 0.02869 (loss) |
| Artifact pointers | `Lock_Horses_Lag_KS.md` · `PULSE_Horses_Standin.md` · `data/horse_scores.json` |

---

*Standing rule: Dual-audience communication. Glossary: `docs/READER_GLOSSARY.md`.*
