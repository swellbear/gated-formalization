# Plain-language card

**Application:** `2026-08_oil-futures-predictive-model`  
**Date / checkpoint:** 2026-08-17 · Yahoo-screen / live-CME promote rule (L-SCREEN-Y-PROMOTE)

---

## What we’re doing

We will keep testing new recipes on the Yahoo tape we already have. We will **not** move to official CME unless a named recipe **beats “assume no change” on the whole trip** (last 500 sessions, and it must not lose on 250 and 750). A tiny overnight blip does **not** count. The lagged-return model already **failed** that test. This is not a trade.

## What we need from you

Nothing required. Optional: name another front-only recipe to test on Yahoo, or leave skill not shown.

**Preferred reply:** click A / B / C. Typed: `leave skill not shown` · `name horse …` · `leave screen rule`

## What a “yes” / this update means

The order of work is frozen. Yahoo first. Live CME only as **confirmation** of the same recipe after the whole-trip gate. Naming the rule is not a pass.

## What this does *not* mean

That a model beats last settlement. That we will now buy DataMine. That anyone should trade. That an oil offshoot is cleared.

---

## Details (technical record — secondary)

| Item | Value |
|------|--------|
| Claim-freeze / claim under test | Rank 4 F-CC; **L-SCREEN-Y-PROMOTE** |
| Amb | **1.0** (**≠ clearance**) |
| Locks / package IDs | Rank 4; L-STANDIN-Y-CLF; **L-SCREEN-Y-PROMOTE**; H-LAG-WF (does not promote) |
| Promotion gate | F-CC RMSE < 0 on last 500 **and** F-CC ≤ 0 on last 250 and 750 |
| H-LAG vs gate | **Fail** (F-CC loss) |
| Artifact pointers | `Lock_Screen_Yahoo_Promote.md` · `04_Material_Admission_Screen_Promote.md` |

---

*Standing rule: Dual-audience communication. Glossary: `docs/READER_GLOSSARY.md`.*
