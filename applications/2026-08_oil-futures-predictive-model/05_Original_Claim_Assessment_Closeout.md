# Original-Claim Assessment (Closeout)

**Date:** 2026-09-01  
**Application:** `2026-08_oil-futures-predictive-model`  
**Closeout verdict:** **Stable Provisional (split) — hard stop (residuals live)**  
**Amb at closeout:** **1.0** (after V-COST-V2; 1.5 after Yahoo stand-in pulse; 2.5 after F-SRC-CME-TAPE; 5.5 at first hygiene seal)

**Amb ≠ clearance (mandatory):** Amb measures under-specification. Amb 1.0 does **not** mean a predictive oil-futures model works, that skill or after-cost value is established or refuted, or that anyone should trade. A named cost schedule is not a value pass. A stand-in baseline is not a pass.  
**Locked bar status (if any):** D-EXIST (P-Logical, futures-target) — **established**. F-SKILL (P-NonNegligible, next-session CL log-return vs last settlement) — **not established** (Yahoo stand-in **baseline** scored; leftover **live**; not a refute). V-VALUE (P-NonNegligible after-cost paper P/L) — **not established** (V-SRC `leave unnamed`; **V2 named**; not a refute).

**Original claim (verbatim):**  
Can a predictive model for oil futures be built?

---

## 1. Status of the original claim

### Constrained (include scope if scoped)
| Content | Scope (unrestricted / under package __) |
|---------|----------------------------------------|
| Three jobs, not one blended yes: existence ⊂ skill ⊂ after-cost value | Under Rank 4 |
| Existence = a specified non-no-change mapping for listed WTI or Brent **futures** can be written | Under Rank 4 + **D-EXIST-MET-FT** |
| Skill protocol = NYMEX CL front-month, next-session **log-return**, walk-forward RMSE vs last settlement (**F-CC**); **L-SESS** requires separate **F-ON** / **F-DAY** exhibits; combo is a third test | Under Rank 4 F-SKILL + L-SESS (bars **not met**) |
| Value protocol = after-cost paper P/L vs the curve on the same CL next-session book; **V2** (fees + $10/contract/side) | Under Rank 4 V-VALUE + **V-COST-V2** (bar **not met**) |
| No-change / last settlement = F-SKILL **baseline**, not the D-EXIST **model** | Under Rank 4 (operator B) |
| Recipe menu = existence evidence only; not a singleton pick | Under L-D-SUITE / D-EXIST-MET-FT |

### Negatively constrained / false as originally stated
| Original strong language | Status |
|--------------------------|--------|
| Blended “a predictive oil-futures model works / can be built” as one yes | **Not cleared.** Split into three legs; only existence-met (futures-target) |
| Spot / real-price recipes as the existence exhibit | **OUT** of D-EXIST (nearby kinship) |
| EIA STEO / listed curve / Alquist–Kilian spot evaluations as F-SKILL | **Not this freeze** (hunt executed; schema fail) |
| Existence-met = skill-met | **False as a collapse** |
| Unnamed skill = no model can beat last price | **Not a refute** |
| Anyone should (or should not) trade | **Not shown** (no should in the claim) |

### Free parameters remaining
| ID | Status / freeze |
|----|-----------------|
| [R-F-SKILL](RESIDUAL_BRANCH_MENU.md#r-f-skill) | Skill class named; **L-HUNT-CL-SEAS** no survivor (do not pick least-bad ANN); **L-HUNT-CL-INV** no survivor (do not pick least-bad WOW); **L-HUNT-COT** no survivor; **L-HUNT-DJT** no survivor; **H-GAP-FADE** small F-DAY / F-CC **tie**; **L-HUNT-PRETELL** no survivor; **H-SPARSE-CAL** tiny 500 / **fails** 750; **H-SPARSE-VOL** and **H-LAG-WF** F-CC **loss**; H-KS not run; **not established**. `pursue`. Reopen: frozen **C-CL-DOW** |
| [R-SPOT-TREND](RESIDUAL_BRANCH_MENU.md#r-spot-trend) | **L-PULSE-SPOT-1** / **INV-1** no survivor; **CROSS-1** WTI fail / Brent tiny 250 ≠ met; **LOGIT-1** discovery beat / confirm **lose** all windows both boards; named queue **empty**. `executed → not established`. Reopen: `leave` · Yahoo horse · name **new** spot class (do not retune FULL; do not unburn; do not change 21) |
| [R-F-COMBO](RESIDUAL_BRANCH_MENU.md#r-f-combo) | Switching rule **unnamed**. `park-until-trigger`. Rule in advance; F-ON and F-DAY already scored separately |
| [R-V-VALUE](RESIDUAL_BRANCH_MENU.md#r-v-value) | After-cost book **unnamed**. `park-until-trigger`. Later book must match **V2** |
| [R-G8](RESIDUAL_BRANCH_MENU.md#r-g8) | **Executed → admitted meanings** (baseline scored; optional FTS not run) |
| [R-LIVE-STANDIN](RESIDUAL_BRANCH_MENU.md#r-live-standin) | **Executed** (Yahoo `CL=F` stipulated). Reopen live **only if** **L-SCREEN-Y-PROMOTE** fires |

### Forced-deviation terms (if extraction was triggered)
None required. Rank 4 D-EXIST is Minimal deviation. F-SKILL is Moderate. V-VALUE is a marked Substantial elevation, not FD-extraction of the slogan.

### Strong language still unsupported
Any claim that a model beats last settlement out of sample; that a paper book makes money after costs; that one named paper is “the” recipe; that spot-oil results clear this freeze; that anyone should trade.

**Scoped vs unrestricted:** Scoped findings are **not** unrestricted support for the original one-liner as a working predictor. D-EXIST-MET-FT is not skill or value.

---

## 2. Continuation options

| Option | Expected buy | Still leaves open |
|--------|--------------|-------------------|
| `leave skill not shown` | None required | F-SKILL stays not established (stand-in baseline on record) |
| `name horse …` | Score a named **front-only** recipe on Yahoo under **L-SCREEN-Y-PROMOTE** | Does not auto-meet V-VALUE; Yahoo win ≠ live clearance; do **not** pick least-bad WOW after CL-INV; do **not** add percent-of-OI or other trader groups after COT scores |
| `leave screen rule` | Keep **L-SCREEN-Y-PROMOTE** | Live CME still gated |
| `name source class …` matching V-VALUE | Named paper book **under V2** | Does not auto-meet F-SKILL |
| `run CR` / successor (existence-only or skill-only) | Different question, labeled | **Declined** 2026-08-17; Rank 4 leftover unchanged |
| `run UX` / `run CX` | Documentation / alternatives | **Declined** 2026-08-17; parent verdict unchanged |

---

## 3. Revision vs continuation fork

Original one-liner is a blended “can.” Rank 4 named the split without rewriting the sentence. CR was **offered**, then **declined**. Default remains: **keep original wording**.

- [ ] **Revise claim** — then run **Claim-Revision Scaffolding** before a successor  
- [x] **Keep original wording** — research agenda / scoped dependents only (default; CR **declined**, not run)

**Default if no further authorization:** keep original wording + **hard stop (residuals live)** with this assessment. Skill leftover stays **live** (`pursue`; CL-INV no survivor; do not pick least-bad WOW). Spot-trend drawer executed (**not established**; LOGIT confirm lose; queue empty).

---

## Closeout statement

Application **closed** as **Stable Provisional (split) — hard stop (residuals live)**. **L-SCREEN-Y-PROMOTE** in force. **L-HUNT-CL-INV** scored; discovery F-CC **both lose** (0 = 0.026705; closest WOW 0.026803); **no survivor**; confirm skipped; promote does not fire; do **not** pick least-bad; F-SKILL **not established**. **L-HUNT-SPOT-LOGIT** scored; discovery beat both boards; confirm **lose** all windows both boards; named Track B queue **empty**; spot-trend **not established**. **L-HUNT-SPOT-CROSS** scored; WTI **no survivor**; Brent W2B confirm point-beats but last-250 **tiny (+1)** ≠ met. **L-HUNT-SPOT-INV** scored; **no survivor**. **L-HUNT-SPOT-TREND** scored; **no survivor** either board. **L-HUNT-COT** scored; **no survivor**. **L-HUNT-DJT** scored; **no survivor**. **H-GAP-FADE** small F-DAY; **does not promote**. **L-HUNT-PRETELL** scored; **no survivor**. **H-SPARSE-CAL** / **H-SPARSE-VOL** scored; **neither promotes**. Leftover stays **live** (`pursue`). Phase 2 not entered. Amb **1.0**. Not a trade.

Awaiting further authorization (`leave skill not shown` · `name horse …` (**different** CL recipe on Yahoo; do **not** pick least-bad WOW) · name a **new** spot class · `leave screen rule`). Live CME **only if** the F-CC gate fires. Optional modes **declined**.

---

*Required at closeout under standing rule. See `.cursor/rules/applications-gated-method.mdc`.*
