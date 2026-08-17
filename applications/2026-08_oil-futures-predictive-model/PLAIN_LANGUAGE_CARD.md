# Plain-language card

**Application:** `2026-08_oil-futures-predictive-model`  
**Date / checkpoint:** 2026-08-17 · named CME tape pulse (L-PULSE-TAPE-0)

---

## What we’re doing

You named the official CL **open and settlement** tape. We tried to measure night vs day vs the whole trip against “assume no change.” We could **not** get CME’s official history from here (it is licensed). We did **not** fake it with Yahoo. Kearney–Shang was **not** re-scored. Skill is still **not shown**. This is not a trade.

## What we need from you

Whether to wait for / supply **official CME** open and settlement, or to **stipulate a stand-in** vendor series (that is a weaker tape, and must be labeled).

**Preferred reply:** click A / B / C. Typed: `live CME only` · `stipulate stand-in …` · `leave tape pending`

## What a “yes” / this update means

The skill **class is named**. The **test did not run** (no stamps). Naming is not a pass. Ambiguity dropped because the vehicle is named, not because skill worked.

## What this does *not* mean

That a model beats last settlement. That daytime is easier. That Kearney–Shang passed. That anyone should trade.

---

## Details (technical record — secondary)

| Item | Value |
|------|--------|
| Claim-freeze / claim under test | Rank 4 F-CC + L-SESS F-ON/F-DAY; F-SRC-CME-TAPE |
| Amb | **2.5** (**≠ clearance**) |
| Locks / package IDs | Rank 4; D-EXIST-MET-FT; L-SESS; F-SRC-CME-TAPE; L-PULSE-TAPE-0 |
| Method verdict label (if any) | Stable Provisional (split) — hard stop (residuals live) |
| Live vs stand-in | **Live tape not in hand; stand-in not stipulated** |
| Artifact pointers | `Lock_FSRC_Named_CME_Tape.md` · `PULSE_Baseline_Session_RMSE.md` · `04_Material_Admission_FSRC_Named.md` |

---

*Standing rule: Dual-audience communication. Glossary: `docs/READER_GLOSSARY.md`.*
