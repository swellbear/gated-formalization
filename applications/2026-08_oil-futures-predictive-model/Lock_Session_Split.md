# Lock Record — session split (night / day / combo protocol)

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Operator selection:** agreed to research **both** windows **separately**, then a **combo only after** both are scored; `ok proceed`  
**App-local lock ID:** **L-SESS**  
**Status:** **IN FORCE for meanings.** Does **not** establish F-ON, F-DAY, F-CC, F-COMBO, or V-VALUE. **Not** a trading strategy. **Later (same day):** F-SRC named as **F-SRC-CME-TAPE**; this lock’s “F-SRC still unnamed” lines are historical. Meanings remain in force.

---

## 0. Plain-language framing

**What was decided:**  
There are two different games. We will **score them on two scoreboards**, then — only if we still want it — a **third** written combo rule.

1. **Night piece** — from today’s official close to the next official **open**.  
2. **Day piece** — from that **open** to the same day’s official **close**.  
3. **Whole trip** — today’s official close to tomorrow’s official close (this is still the original skill test). Night plus day **add up** to the whole trip (in log-returns).  
4. **Combo** — a switching rule written **before** seeing the answers. Not allowed to replace 1–3.

**What this settles:**  
What the next skill tests **are**. Getting out before the close and back in after the open is the **day** book. It is **not** a clever way to pass the whole-trip test.

**What this does *not* settle:**  
That daytime is easier. That anyone should trade. That a source class has been named. That skill or after-cost value is shown.

---

## Locked content

**Scope:** **Under Rank 4 (D-EXIST ⊂ F-SKILL ⊂ V-VALUE) only**, **Under F-SRC leave unnamed**, **Under L-SESS**.

Parent **F-SKILL** is **unchanged:** NYMEX **CL front-month**, **next-session settlement-to-settlement log-return**, walk-forward **RMSE vs last-settlement no-change**. That parent is labeled **F-CC** here (close-to-close).

| ID | Window | Baseline (no-change) | Job |
|----|--------|----------------------|-----|
| **F-CC** | Official **settlement** → next official **settlement** | Overnight+day log-return = 0 | Original F-SKILL. **Not replaced.** |
| **F-ON** | Official **settlement** → next official printed **open** | Overnight log-return = 0 | Night piece. Game B is **out** of this window. |
| **F-DAY** | Official printed **open** → same-day official **settlement** | Day log-return = 0 | Day piece. Game B (**out pre-close, in post-open**) lives here. |
| **F-COMBO** | A **named** switching rule across F-ON / F-DAY / flat, written **before** the out-of-sample window | Same RMSE-vs-0 idea on the **rule’s** returned path | **Third** object. Parked until 1–2 are scored **and** the rule is named. |

**Stamps:** NYMEX CL front-month, **roll-aware**. **Close** = official daily **settlement**. **Open** = official printed daily **open** on the same series. A Globex halt clock (e.g. 4–5pm CT) or a high-frequency “RTH only” clock is **not** silently the same; using it requires a later named class that **quotes** those stamps (schema fail if it doesn’t).

**Additivity:** On a series where the open sits between consecutive settlements, `r_CC ≈ r_ON + r_DAY` (logs). Scoring one piece is **not** scoring the sum.

**Protocol (all skill pieces):** walk-forward; RMSE vs the table’s no-change; in-sample fit does **not** meet the bar. Direction may be reported; it does not replace RMSE.

**Order (mandatory):**  
1. Score **F-ON** and **F-DAY** **separately** (and keep reporting **F-CC**).  
2. Only then may **F-COMBO** be tested, and only if the switching rule was written **in advance**.  
3. After-cost P/L on any of these books is **V-VALUE**, not a skill pass. The day book and any combo that enters/exits daily must count **those** round-turns. Each value test still **names V1 or V2**.

**F-SRC:** still **unnamed**. This lock does **not** name a series. A later `name source class …` that matches F-SKILL must be able to support **F-CC**, and — when the pulse runs — **must report F-ON and F-DAY as separate exhibits**. Naming a day-only USO/ETF half-hour paper is **not** F-CC.

---

## What this does *not* do

- Does **not** establish skill on any window.  
- Does **not** establish after-cost value.  
- Does **not** license trading.  
- Does **not** treat “research both, then combine” as already passed.  
- Does **not** let a combo inherit a pass from one winning half after the fact.  
- Does **not** undo D-EXIST-MET-FT, F-SRC leave unnamed, or V-SRC leave unnamed.  
- Does **not** enter Phase 2.  
- Does **not** invent a class.

**Lock-time Amb warning:** Fixing the three windows drops leftover-ambiguity on “is daytime the same question as next close?” **Amb drop ≠ clearance.** This pass **holds Amb at 5.5** (F-SRC still unnamed; combo parked as a trigger, not a new scored vehicle).

---

## Honesty lines (add to later `04`s)

10. Establishing **F-DAY** does **not** establish **F-CC** or **F-ON**.  
11. Establishing **F-ON** does **not** establish **F-CC** or **F-DAY**.  
12. **F-COMBO** is not a shortcut. It is a third test.  
13. USO/ETF half-hour momentum, EIA announcement-day jumps, and “substantial trading profits” in those papers are **kinship**, not these RMSE bars.  
14. Daily in-and-out **costs** belong on the day/combo **value** books; they are not optional.

---

## Dependents

- **F-SKILL / F-CC** — still **not established**; F-SRC unnamed; leftover **live**.  
- **F-ON / F-DAY** — protocol locked; **not established**; wait on a matching named class (same F-SRC reopen).  
- **F-COMBO** — **park-until-trigger** (named rule + F-ON and F-DAY already scored separately + walk-forward).  
- **V-VALUE** — still unnamed book; if the book is day-only or combo, round-turns follow the book.

---

## Reopen

- Skill pieces: `name source class …` matching NYMEX CL front-month, official open/settlement stamps, walk-forward RMSE vs the matching no-change.  
- Combo: `name source class …` with the **switching rule written in advance**.  
Naming ≠ bar-met. Honest established still **stops**. Do **not** invent a class.
