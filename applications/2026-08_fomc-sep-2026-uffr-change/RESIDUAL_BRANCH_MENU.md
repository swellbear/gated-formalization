# Residual Branch Menu

**App:** `2026-08_fomc-sep-2026-uffr-change`  
**Updated:** 2026-08-12  
**Closeout status:** **hard stop sealed**. Parent split intact. C1 P-NN-TEST executed. Independent class unnamed (`leave unnamed`). F-PRINT parked. Not Phase 2.  
**Rule:** Offering ≠ running. Parent verdict unchanged.

**Glossary:** [`docs/READER_GLOSSARY.md`](../../docs/READER_GLOSSARY.md)  
**Optional modes (separate):** [`OPTIONAL_MODES_MENU.md`](OPTIONAL_MODES_MENU.md)

**Live vs stand-in:** Live F-PRINT = FOMC statement after Sep 15–16 2026. **OUT** for the print: this Polymarket page; June SEP.

**Amb = 2.5.** P-NonNegligible **not established**. Amb ≠ clearance.

---

## 0. Plain-language framing

**What we’re doing:** Listing leftovers after Phase 1. The second live-shot series was left unnamed on purpose. The September statement still does not exist.

**What we need from you:** Nothing unless you want to name a matching series later, wait for the statement, or authorize a branch.

**What authorizing a branch means:** A scoped continuation on this same Rank 3 M3 package — not a rewrite of the ¢ census, and not “hike is unlikely.”

**What this does *not* mean:** Automatic Phase 2; that a hold is the path; that 33¢ is a cleared live shot; June SEP carry-over.

---

## 1. Index (clickable)

| ID | One-line | Class | Named source class | Disposition |
|----|----------|-------|--------------------|-------------|
| [R-D-OPTIONS](#r-d-options) | What brackets does the named page display? | Empirically resolvable | Polymarket `fed-decision-in-september-762` | **executed → admitted** |
| [R-D-PRICE](#r-d-price) | What Yes ¢ did that page print at fetch? | Empirically resolvable | Same page (conflicted) | **executed → admitted** (pitch curve, not bar-met) |
| [R-P-NN-TEST](#r-p-nn-test) | Do those ¢ meet M3 on this vehicle? | Empirically resolvable | C1 Polymarket (conflicted) | **executed → not established** |
| [R-P-NN](#r-p-nn) | Independent affirmation of live shots? | Empirically resolvable | **unnamed** (operator `leave unnamed`; C2 unfilled) | **park-until-trigger** |
| [R-F-PRINT](#r-f-print) | What upper-bound **change** will the Sep statement print? | Empirically resolvable | FOMC statement after Sep 15–16 2026 (named; data not yet existent) | **park-until-trigger** |

**Authorize (open):** `name source class C2: …` (reopens [R-P-NN](#r-p-nn)) · `decline residual menu`

**Also offered (separate):** [`OPTIONAL_MODES_MENU.md`](OPTIONAL_MODES_MENU.md). Offering ≠ running.

---

## 2. Cards

<a id="r-d-options"></a>
### R-D-OPTIONS

| Field | Content |
|-------|---------|
| **Class** | Empirically resolvable (executed) |
| **Named source class** | Polymarket event **Fed Decision in September?** (`https://polymarket.com/event/fed-decision-in-september-762`), fetch 2026-08-12 |
| **What it is** | The five displayed brackets (O2) |
| **Why offered here** | Rank 3 required the option list from the named URL |
| **What authorizing does** | Already ran: `04_Material_Admission_D_OPTIONS_D_PRICE.md` |
| **What success / failure changes** | **Admitted:** 50+ dec / 25 dec / No change / 25 inc / 50+ inc |
| **What it does *not* do** | Does not pick a winner or meet M3 |
| **Effort** | Low (done) |
| **Disposition** | **Executed 2026-08-12** |
| **How to authorize** | Already run |

<a id="r-d-price"></a>
### R-D-PRICE

| Field | Content |
|-------|---------|
| **Class** | Empirically resolvable (executed) |
| **Named source class** | Same Polymarket page; published Yes ¢ / displayed % |
| **What it is** | Conflicted page print of prices at fetch |
| **Why offered here** | Q3 vehicle is that published price; census ≠ bar-met |
| **What authorizing does** | Already ran with D-OPTIONS |
| **What success / failure changes** | **Admitted** as scenario presence / pitch curve: 0.6 / 1.1 / 67 / 33 / 0.5 ¢ |
| **What it does *not* do** | Does not affirm P-NonNegligible or P-BaseCase |
| **Effort** | Low (done) |
| **Disposition** | **Executed 2026-08-12** |
| **How to authorize** | Already run |

<a id="r-p-nn-test"></a>
### R-P-NN-TEST

| Field | Content |
|-------|---------|
| **Class** | Empirically resolvable (executed) |
| **Named source class** | C1 — same Polymarket event (conflicted) |
| **What it is** | Whether M3 P-NonNegligible is **met** on this vehicle |
| **Why offered here** | M3 locked; named class already on the card |
| **What authorizing does** | Already ran: `04_Material_Admission_P_NonNegligible.md` |
| **What success / failure changes** | **Not established** for all five brackets. Not a refute |
| **What it does *not* do** | Does not say outcomes are impossible; does not make 67¢ the expected path |
| **Effort** | Low (done) |
| **Disposition** | **Executed 2026-08-12** |
| **How to authorize** | Already run |

<a id="r-p-nn"></a>
### R-P-NN

| Field | Content |
|-------|---------|
| **Class** | Empirically resolvable |
| **Named source class** | **unnamed**. Operator 2026-08-12: `leave unnamed`. C1 **REJECT** as sole affirmation. C2 not filled (`R_Source_Class_Choice_Set.md`) |
| **What it is** | Whether a **non-C1-sole** public series affirms a live shot at a named bracket under Rank 3 M3 |
| **Why offered here** | Conflicted venue cannot be the only support for the locked modal bar |
| **What authorizing does** | Only a later `name source class C2: …` that **matches** Rank 3 object/window/bar would enable a named-class pulse |
| **What success / failure changes** | A matching pulse could establish / not-establish / refute P-NonNegligible. Establishment still stops for operator. Leave-unnamed ≠ unlikely |
| **What it does *not* do** | Does not license Kalshi/CME FedWatch slogans, June SEP, or C1 as sole affirmation |
| **Effort** | High until a matching series exists; then medium |
| **Disposition** | **park-until-trigger** |
| **How to authorize** | `name source class C2: [exact series]` when a matching class exists. Not `authorize branch` of C1 |

**Trigger:** A public series is named that publishes a central statistic on the **same Sep 2026 upper-bound-change object** (same meeting; same 25 bp brackets or a mapped equivalent) and is usable for affirmation (not this trading page as sole proof). Kalshi / CME FedWatch / “the market” / June SEP as slogans do **not** fire this trigger.

<a id="r-f-print"></a>
### R-F-PRINT

| Field | Content |
|-------|---------|
| **Class** | Empirically resolvable (data not yet existent) |
| **Named source class** | FOMC **statement** after the meeting scheduled Sep 15–16 2026 (L1). Supporting locator: Fed openmarket.htm. Fallback in the contract: no statement by end of the **next** scheduled meeting → “No change” |
| **What it is** | The upper-bound **change** vs the pre-meeting in-force level (B1), mapped to a displayed 25 bp bracket |
| **Why offered here** | That print is the market’s resolution object; it is not this page’s ¢ |
| **What authorizing does** | After the statement exists, a named-class pulse on L1 (not a silent C2 swap) |
| **What success / failure changes** | Could establish which bracket **printed**. Does not retroactively meet M3 from ¢ |
| **What it does *not* do** | Does not treat this Polymarket page or June SEP as the statement |
| **Effort** | Low once the statement exists |
| **Disposition** | **park-until-trigger** |
| **How to authorize** | Fires when the Sep 15–16 2026 FOMC statement (or the contract fallback clock) exists. Not `name source class C2` |

**Trigger:** FOMC statement after the September 15–16 2026 meeting is issued, **or** the contract fallback clock (no statement by end of the next scheduled meeting).

---

## 3. Definition-blocked

None remaining. Rank 3 M3 and live F-PRINT vehicle are locked.

---

## 4. Not branchable by the method (normative / preference)

None in the paste (no should).

---

## 5. Parked / no near-term path

| Residual ID | Disposition | Trigger / note |
|-------------|-------------|----------------|
| [R-P-NN](#r-p-nn) | park-until-trigger | Matching Rank 3 series named as C2; C1 does not count as sole affirmation |
| [R-F-PRINT](#r-f-print) | park-until-trigger | Sep 15–16 2026 FOMC statement (or fallback clock) |

---

## 6. Operator decision log

| Date | Action |
|------|--------|
| 2026-08-12 | Rank 3 + URL; then `live shots` = M3 |
| 2026-08-12 | `leave unnamed` — R-P-NN parked; no second pulse; no CR |
| 2026-08-12 | Phase 1 endpoint — menus offered, not run |  
| 2026-08-12 | **hard stop sealed** — original wording kept; optional modes still offered not run |

---

*Standing rule: Residual-branch offering + clickable cards. See `.cursor/rules/applications-gated-method.mdc`.*
