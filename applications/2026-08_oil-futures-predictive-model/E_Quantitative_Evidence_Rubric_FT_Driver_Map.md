# Quantitative Evidence Rubric — mover-list census

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Bar under test (quote freeze):** F-SKILL — walk-forward RMSE vs last-settlement no-change on NYMEX CL front-month **next-session log-return**.  
**Census question:** Does a comprehensive exhaustive list of movers of that object exist?  
**Source / artifact:** `MAP_What_Can_Move_CL.md` (L-MAP-DRV)

---

| # | Check | Result |
|---|-------|--------|
| 1 | **Sample definition** — series, window, return/quantity concept stated? | **No** for an exhaustive next-session CL mover universe (open-ended). **Yes** for D-EVENT papers’ own samples (intraday / announcement-day WTI futures around EIA/API) |
| 2 | **Costs / taxes / frictions** — included, excluded, or N/A (state which)? | **N/A** for the census. Event-study trading-rule asides are **excluded** from F-SKILL (V-VALUE) |
| 3 | **Significance vs point estimate** — test/interval, or point estimate only? | **Test** in Ye–Karali / Geman–Li (announcement-window returns and vol). Census of “is there an exhaustive list?” is **not** a significance test |
| 4 | **Matched comparison** — same locks / same instance on both sides of the bar? | **No** — contemporaneous inventory surprise ≠ next-session log-return RMSE vs last settlement. Score every locked slot |
| 5 | **Sensitivity to sample window** — noted, tested, or untested? | **Noted** in event studies (API vs EIA; recession subsamples; pre- vs post-print). Untested as F-SKILL window |
| 6 | **Print-match ≠ clearance** — same print (or subset) treated as kinship, not bar-met? | **Yes** — “EIA surprise moves CL at 10:30 ET” is kinship, not F-SKILL-met |

---

## Already-included legs (mandatory for numerical / workbook bars)

| Leg | In base bar test? | Notes |
|-----|-------------------|-------|
| Last-settlement no-change | Y | F-SKILL **baseline** |
| EIA STEO / monthly spot outlooks | Y | Already OUT in L-HUNT-PROVEN |
| Kilian / Baumeister–Kilian **spot/real** VARs | Y | Nearby existence; OUT of F-SKILL |
| Kearney–Shang macro (“Fund”) horse | Y | Already on L-MAP-FT as not freeze-met |
| Inventory **surprise** at the print | N | Different horizon (contemporaneous). Kinship only unless freeze changes |

**If asked “what about EIA inventories moving oil every Wednesday?”:** Already in this rubric as **D-EVENT kinship** — not an omitted F-SKILL pass.

---

**Conflicted-source?** Non-conflicted for EIA taxonomy + peer-reviewed event studies; broker calendars unused for affirmation.

**Bar decision supported by this artifact?** **Not establish** (F-SKILL). **Census answer:** exhaustive list **does not exist**. **Not refute** of all recipes. **HOLD/REJECT** as a submitted F-SRC class.

**Establishment-stop drill (if named-class pulse):** Would honest `04` declare established? **No.**

**Comparability note:** Same freeze as L-MAP-FT / L-HUNT-PROVEN. This map **adds mover-list cards**; it does not reverse “no freeze-matching proven series submitted.”

---

*Standing rule: Quantitative evidence quality bar + already-included legs.*
