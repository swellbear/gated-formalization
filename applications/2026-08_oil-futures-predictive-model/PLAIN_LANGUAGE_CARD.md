# Plain-language card

**Application:** `2026-08_oil-futures-predictive-model`  
**Date / checkpoint:** 2026-08-17 · sparse calendar + vol-state horses (L-PULSE-SPARSE-1)

---

## What we’re doing

We scored two recipes that usually predict “no change.” One speaks up on EIA/FOMC calendar days. The other speaks up after a large prior whole-trip move. **Neither** beat last settlement by enough to move to official CME. The calendar one had a **tiny** whole-trip dip on last 500 and **lost** on last 750. This is not a trade.

## What we need from you

Nothing required. Optional: leave skill not shown, or name a **different** front-only recipe (do not grow this pair into a zoo).

**Preferred reply:** click A / B / C. Typed: `leave skill not shown` · `name horse …` · `leave screen rule`

## What a “yes” / this update means

Those two recipes are on the card and scored. Naming and scoring is **not** a pass. Live CME still only if the whole-trip gate fires. It did **not**.

## What this does *not* mean

That a model beats last settlement. That the tiny calendar dip is skill. That we will now buy DataMine. That anyone should trade.

---

## Details (technical record — secondary)

| Item | Value |
|------|--------|
| Claim-freeze / claim under test | Rank 4 F-CC; **L-SCREEN-Y-PROMOTE** |
| Amb | **1.0** (**≠ clearance**) |
| Locks / package IDs | **H-SPARSE-CAL**; **H-SPARSE-VOL**; L-SCREEN-Y-PROMOTE |
| CAL vs gate | **Fail** (tiny 500 beat; **loss** on 750) |
| VOL vs gate | **Fail** (F-CC loss on 500/250/750) |
| Artifact pointers | `Lock_Horses_Sparse.md` · `PULSE_Horses_Sparse.md` · `04_Material_Admission_Sparse.md` |

---

*Standing rule: Dual-audience communication. Glossary: `docs/READER_GLOSSARY.md`.*
