# Plain-language card

**Application:** `2026-08_oil-futures-predictive-model`  
**Date / checkpoint:** 2026-08-17 · Yahoo `CL=F` stand-in pulse (L-PULSE-STANDIN-1)

---

## What we’re doing

You allowed Yahoo crude (`CL=F`) as a **weaker** tape. We measured night vs day vs the whole trip against “assume no change.” Those are **baseline sizes**, not a model that beats last price. Yahoo is **not** official CME settlement. Skill is still **not shown**. This is not a trade.

## What we need from you

Nothing required. Optional: wait for official CME stamps and re-score, or name a recipe to test **against** these baselines.

**Preferred reply:** click A / B / C. Typed: `leave skill not shown` · `live CME only` · `name horse …`

## What a “yes” / this update means

The tape fork is closed as **stand-in**. Night/day/whole-trip RMSEs exist on Yahoo Open/Close. Naming a stand-in is not a pass.

## What this does *not* mean

That a model beats last settlement. That daytime is easier (on this tape the day piece is **larger**). That anyone should trade. That an oil offshoot is cleared.

---

## Details (technical record — secondary)

| Item | Value |
|------|--------|
| Claim-freeze / claim under test | Rank 4 F-CC + L-SESS F-ON/F-DAY; F-SRC-CME-TAPE; L-STANDIN-Y-CLF |
| Amb | **1.5** (**≠ clearance**) |
| Locks / package IDs | Rank 4; D-EXIST-MET-FT; L-SESS; F-SRC-CME-TAPE; L-STANDIN-Y-CLF; L-PULSE-STANDIN-1 |
| Method verdict label (if any) | Stable Provisional (split) — hard stop (residuals live) |
| Live vs stand-in | **Stand-in stipulated** (Yahoo `CL=F` Open/Close) |
| Last-500 RMSE vs 0 | F-ON 0.01291 · F-DAY 0.02663 · F-CC 0.02869 (n=500) |
| Artifact pointers | `Lock_Standin_Yahoo_CLF.md` · `PULSE_Standin_Yahoo_CLF_RMSE.md` · `04_Material_Admission_Standin_Yahoo.md` |

---

*Standing rule: Dual-audience communication. Glossary: `docs/READER_GLOSSARY.md`.*
