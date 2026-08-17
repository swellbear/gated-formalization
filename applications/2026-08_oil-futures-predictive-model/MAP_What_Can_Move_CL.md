# Map — has anyone listed what can actually move next-session CL?

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Layer ID:** **L-MAP-DRV** (evaluation census — not F-SKILL-met; not a named F-SRC class)  
**Freeze quoted:** Rank 4 **F-SKILL** = NYMEX **CL front-month**, **next-session log-return**, walk-forward **RMSE vs last-settlement no-change**.  
**Operator question (plain):** Has anyone made a comprehensive exhaustive list of what can actually move what we are looking at?  
**Scope:** **Under Rank 4 only.** Does **not** fill F-SRC. Do **not** invent a class.

**Glossary:** [`docs/READER_GLOSSARY.md`](../../docs/READER_GLOSSARY.md)

---

## 0. Plain-language framing

**What we’re doing:** Checking whether a complete catalog exists of things that move **tomorrow’s CL (or Brent) futures change versus today’s official close**.

**Short answer:** **No.** There are useful **bucket lists**, **event calendars**, and **one-news event studies**. There is **not** a comprehensive exhaustive list of what can move the locked object. There is also **not** a standing public series that turns such a list into next-session log-return skill versus last settlement.

**What this does *not* settle:** That oil is unexplainable. That skill is established or refuted. That anyone should trade.

---

## 1. Why “exhaustive” is the wrong shape for this object

Tomorrow’s futures number can jump on **anything new** that was not already in today’s settlement: a pipeline fire, a war headline, an OPEC leak, a hurricane track, a dollar spike, a big inventory miss.

That set is **open-ended**. A list of *kinds* of things (supply, demand, inventories, geopolitics, finance) can be written. A list of *every future headline that could move CL* cannot. Baumeister & Kilian (2016) is literally titled that oil prices **still surprise** us after forty years of better understanding.

Two jobs get mixed:

| Job | Everyday meaning | Same as F-SKILL? |
|-----|------------------|------------------|
| **After-the-fact explanation** | “The price jumped because inventories came in heavy.” | **No** — that is contemporaneous |
| **Before-the-session forecast** | Using only what was known at last settlement, beat “no change tomorrow.” | **Yes — this freeze** |

A perfect diary of what *did* move the market today is still not a forecast of tomorrow.

---

## 2. What actually exists (not exhaustive)

| ID | Family | What it is | Object | Exhaustive of next-session CL movers? | Vs last-settlement forecast skill |
|----|--------|------------|--------|----------------------------------------|-----------------------------------|
| **D-BUCKET** | EIA “What drives crude oil prices?” | **Seven buckets**, updated as a guide: spot context; non-OPEC supply; OPEC supply; inventories; financial markets; OECD demand; non-OECD demand | Crude **prices** (monthly/quarterly charts), not next-session CL log-return | **No** — taxonomy, not a closed inventory of headlines | **OUT** of F-SKILL |
| **D-SHOCK** | Kilian (2009) / Kilian–Murphy (2014) | **Three (then four) shock types**: oil supply; global activity demand; oil-specific / precautionary demand; inventories as a window on expected tightness | Usually **monthly real / spot** oil | **No** — a structural grouping. Rival identifications exist (e.g. Baumeister–Hamilton) | Nearby for **spot** existence; **OUT** of next-session CL |
| **D-SURPRISE** | Baumeister & Kilian (2016) JEP | Narrative of major episodes 1973–2014 **and** why prices keep surprising | Real oil-price history | **Opposite of exhaustive completeness** | Explains forecast difficulty; not a mover checklist that clears skill |
| **D-CAL** | CME / broker “key reports” lists | **Scheduled** items: EIA weekly; API weekly; OPEC meetings; refinery reports; weather; “world events” | Trading calendar | **No** — known dates only; “world events” is an unbounded residual | Calendar ≠ walk-forward RMSE |
| **D-EVENT** | Inventory / OPEC **event studies** on **WTI futures** | Ye & Karali (2016); Geman & Li (2018); related EIA-surprise papers; Demirer & Kutan (2010) on OPEC/SPR | **Intraday or announcement-day** CL/WTI futures | **No** — one (or a few) scheduled prints | **Contemporaneous:** surprise **moves** price at the print. **Typically does not forecast** the remaining return after the print. **Not** next-session vs last settlement |
| **D-KITCHEN** | Macro / positioning predictor menus | USD, equities, rates, VIX, CFTC “speculation” indexes, GPR, etc. (the “Fund” horse in Kearney–Shang 2020; mixed speculation papers) | Mix of weekly/daily **futures or commodity** returns | **No** — a menu, never claimed complete | In L-MAP-FT, the macro horse was **not** a freeze-matching standing series; directional CL1 stayed near a coin |

**Spot / real-price driver lists stay OUT of the F-SKILL match column** (same rule as L-MAP-FT).

---

## 3. Cards

<a id="d-bucket"></a>
### D-BUCKET — EIA seven factors

Public EIA guide: [What drives crude oil prices](https://www.eia.gov/finance/markets/crudeoil/). Seven **key factors**, not “everything that can happen tomorrow.” Physical barrels (OPEC / non-OPEC supply, OECD / non-OECD demand, inventories) plus **financial markets**. Useful as a map of *kinds*. **Not** a next-session CL log-return catalog.

<a id="d-shock"></a>
### D-SHOCK — Kilian-style shocks

Kilian (2009) *AER*: not all oil-price moves are the same kind of shock. Later work adds inventories / speculative demand. This is the academic **bucket** system for **monthly real oil**. It is why “oil went up” is an incomplete sentence. It is **not** an exhaustive list of next-session CL headlines, and it is **not** this freeze.

<a id="d-surprise"></a>
### D-SURPRISE — “still surprise us”

Baumeister & Kilian (2016) *JEP*: even with better models of *kinds* of shocks, oil still surprises. That is evidence **against** treating any published list as exhaustive for forecasting.

<a id="d-cal"></a>
### D-CAL — scheduled-news calendars

CME’s WTI page lists EIA, API, OPEC, refinery reports, weather, world events. Brokers repeat the same. These are **diaries of known dates**. The leftover category “world events” is exactly the unbounded part. A calendar is not a proof that those prints forecast tomorrow’s log-return versus last settlement.

<a id="d-event"></a>
### D-EVENT — announcement-day studies (closest “does X move CL?”)

| Cite | What they show | What they do **not** show |
|------|----------------|---------------------------|
| Ye & Karali (2016), *Energy Economics* 59 | API and EIA **inventory surprises** have an **immediate inverse** effect on crude **futures** returns (build surprise → price down) and raise volatility; EIA effects larger/longer than API | That last week’s surprise forecasts **next session** vs last settlement |
| Geman & Li (2018), *Journal of Energy Markets* | WTI futures react in minutes; price often **reverts** after the first reaction (~25 minutes in their sample) | A standing next-session RMSE bake-off |
| Related EIA-surprise / jump papers (e.g. Hong–Luo-style high-frequency tests) | Jumps cluster **at** 10:30 ET Wednesday; **after** the print, the surprise often has **no** power for later same-day nearby returns (consistent with news already in the price) | F-SKILL. Some pre-announcement leakage findings are a **different** (and contested) object |
| Demirer & Kutan (2010) | Spot and futures around **OPEC and SPR** announcements | Not next-session log-return RMSE vs last settlement |

**Plain takeaway:** the best-studied “this actually moves CL” item is **the inventory *surprise***, at the moment it hits. That is **explanation of a jump**, not the locked forecast bar.

<a id="d-kitchen"></a>
### D-KITCHEN — grab-bags of other series

Papers throw in the dollar, stocks, interest rates, fear indexes, trader-positioning reports, geopolitical-risk indexes. None of those papers claim the list is complete. Speculation-as-driver remains **contested**. Kearney–Shang’s macro horse was a **benchmark**, not a complete mover census, and was **not** submitted here as F-SRC.

---

## 4. What remains untested (on the locked skill freeze)

1. An **exhaustive** list of next-session CL movers — **not found; not a well-posed finite object**.  
2. A **finite, pre-specified** information set, known at last settlement, that walk-forward **beats last-settlement RMSE** on next-session CL log-return as a standing public series — **still untested** (same leftover as L-MAP-FT / L-HUNT-PROVEN).  
3. Treating D-EVENT inventory surprises as **that** series — **schema fail** unless the freeze is changed to contemporaneous announcement-day returns.  
4. The same on **ICE Brent** next-session settlement log-return.

**Not untested:** That **kinds** of oil-price drivers can be named. That **scheduled** EIA/API/OPEC prints exist. That inventory **surprises** move WTI futures **when they print**.

---

## 5. Establishment-stop drill

**Would honest `04` declare F-SKILL established on this map?** **No.**

A taxonomy or an announcement-day jump is not next-session log-return RMSE vs last settlement. Print-match ≠ clearance.

**Would honest `04` declare F-SKILL refuted because no exhaustive list exists?** **No.** Open-ended news is why no-change is a hard baseline. It is not a proof that no subset of known information can ever beat it.

**F-SRC:** stays **unnamed**. EIA seven factors / Kilian shocks / Ye–Karali inventory surprises are **not** silently picked as the skill class.

---

## 6. Operator decision log

| Date | Action |
|------|--------|
| 2026-08-17 | Operator asked whether anyone has a comprehensive exhaustive list of what can move the locked object. Recorded as **L-MAP-DRV**. Answer: **no exhaustive list**. F-SKILL **not established**. F-SRC **not filled**. |

---

*Evaluation census under Rank 4. Not trading advice. Not blended-slogan clearance.*
