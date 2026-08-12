# Residual Branch Menu

**App:** `2026-08_fomc-june-2026-sep`  
**Updated:** 2026-08-12  
**Closeout status:** **hard stop sealed** — parent closeout intact. **Named-class pulse** executed R-FML-INDEP → L17 (SPF Q2 2026; not established). Not Phase 2. Not a silent `authorize branch` of G8/R-REALIZE/R-REV.  
**Rule:** Offering ≠ running. Parent verdict unchanged. Click an ID for instance-specific explainers.

**Glossary:** [`docs/READER_GLOSSARY.md`](../../docs/READER_GLOSSARY.md)

**Live vs stand-in:** Live = June 17, 2026 SEP PDF/HTML. **OUT:** July 29 FOMC statement (not a residual in this package unless you elevate it).

**Amb ≈ 1** (Gap 8 realization still open). F-ML-BAR **not established** on 2026 medians (L13 brochure test; **L17** SPF Q2 2026 comparison). Amb ≠ clearance.

---

## 0. Plain-language framing

**What we’re doing:** Listing leftover open items after hard stop. You can still authorize a branch, freeze realization as “later,” or leave them parked.

**What we need from you:** Nothing unless you want a branch. Click an ID for what it means *in this app*.

**What authorizing a branch means:** A scoped continuation on this same claim package — not a rewrite of what is already established / not established.

**What this does *not* mean:** Automatic Phase 2; that 2026 inflation will be 3.6%; importing the July 29 statement; advice.

---

## 1. Index (clickable)

| ID | One-line | Class | Named source class | Disposition |
|----|----------|-------|--------------------|-------------|
| [R-FML-2026](#r-fml-2026) | Test F-ML-BAR on 2026 GDP/U/PCE/core medians | Empirically resolvable | June 17 SEP Table 1 (brochure; circular for clearance) | **executed → L13; not established** (not a refute) |
| [R-G8-SCOPE](#r-g8-scope) | Freeze realization as out of scope *now* | Definition freeze | **unnamed** (operator lock, not a fetch) | Not authorized (default) |
| [R-REALIZE](#r-realize) | Compare 2026–28 actuals to submitted medians | Empirically resolvable | 2026–28 Q4 actuals under L4 defs (BEA/BLS prints) | **park-until-trigger** |
| [R-FML-INDEP](#r-fml-indep) | Independent expected-path vs 2026 medians | Empirically resolvable | Philadelphia Fed SPF published median, L4 defs | **executed → L17 SPF Q2 2026; not established** (not a refute) |
| [R-FML-2027-28](#r-fml-2027-28) | Test F-ML-BAR on 2027 and 2028 medians | Empirically resolvable | Same June 17 SEP brochure as L13 (not a new class) | **park-90d** (diminishing returns after L13) |
| [R-REV](#r-rev) | Narrow original wording to supported census core | Claim-revision path | **unnamed** / CR path (operator) | Not authorized (default) |
| [R-JULY29](#r-july29) | Elevate July 29 statement into this package | Parked / OUT | July 29 FOMC statement **if** L₀ elevated | **drop** unless you elevate L₀ |

**Authorize (open):** `authorize branch R-G8-SCOPE` · `authorize branch R-REALIZE` · `authorize branch R-FML-2027-28` · `authorize branch R-REV` · `lock G8 realization-later` · `decline residual menu`

**Also offered (separate):** optional modes — [`OPTIONAL_MODES_MENU.md`](OPTIONAL_MODES_MENU.md). Offering ≠ running.

---

## 2. Cards

<a id="r-fml-2026"></a>
### R-FML-2026

| Field | Content |
|-------|---------|
| **Class** | Empirically resolvable (executed) |
| **Named source class** | June 17, 2026 SEP Table 1 / already-admitted L3–L10. Brochure; circular for F-ML clearance. |
| **What it is** | Whether 2026 medians GDP **2.2** / U **4.3** / PCE **3.6** / core PCE **3.3** meet F-ML-BAR (P-BaseCase). Funds-rate off this bar. |
| **Why offered here** | L2 froze the bar; L5 admitted the cells as *submitted*; meeting the bar was the leftover evaluation. |
| **What authorizing does** | Already ran: rubric + `04m`. |
| **What success / failure changes** | **Not established** for all four. Not a refute (no rival expected-path admitted). |
| **What it does *not* do** | Does not prove 2026 inflation will *not* be 3.6%. Does not test 2027–28. Does not put funds 3.8 under F-ML. |
| **Effort** | Medium (done) |
| **Disposition** | **Executed 2026-08-12 → L13.** Brochure + L11 policy-mix block identification; PCE extra: +0.9 vintage jump and 17/18 upside risk. |
| **How to authorize** | Already run. Independent-class reopen was [R-FML-INDEP](#r-fml-indep) → L17 (still not established). Do not re-read Table 1. |

<a id="r-g8-scope"></a>
### R-G8-SCOPE

| Field | Content |
|-------|---------|
| **Class** | Definition freeze |
| **Named source class** | **unnamed** — operator lock (`lock G8 realization-later`), not a public fetch. |
| **What it is** | Gap 8: 2026–28 realization is **not in scope now**. June 17 submission is not a 2026–28 outcome. |
| **Why offered here** | Last open Amb slot (W=1). Draft freeze already used; not locked. |
| **What authorizing does** | Lock G8 as later/out-of-scope-now. Amb **1 → 0**. Does **not** admit 2026–28 actuals. |
| **What success changes** | Realization FP closed as *not this package’s present object*. |
| **What failure / absence changes** | Amb stays ≈ 1; [R-REALIZE](#r-realize) can still park until prints exist. |
| **What it does *not* do** | Does not meet F-ML-BAR; does not skip [R-REALIZE](#r-realize) forever; Amb 0 ≠ clearance. |
| **Effort** | Low |
| **Disposition** | Not authorized (default) |
| **How to authorize** | `authorize branch R-G8-SCOPE` or `lock G8 realization-later` |

<a id="r-realize"></a>
### R-REALIZE

| Field | Content |
|-------|---------|
| **Class** | Empirically resolvable |
| **Named source class** | Printed 2026–28 actuals under L4 defs (Q4/Q4 GDP and PCE; Q4-average unemployment). **Named enough**; data does **not** exist yet → `park-until-trigger` (not “operator admits a series”). |
| **What it is** | After the fact, compare printed 2026–28 actuals (Q4/Q4 GDP and PCE; Q4-average unemployment — L4) to L5 medians. |
| **Why offered here** | Original package includes forecast-extension; Gap 8 is whether matching actuals is in-scope *now* (no). |
| **What authorizing does** | Later empirical slot under L4/L5/L15. One year at a time (G5). |
| **What success / failure changes** | May record hit/miss vs submitted medians. **Does not** by itself meet F-ML-BAR (realization ≠ “was the expected path on June 17”). |
| **What it does *not* do** | Does not import July 29; does not treat a hit as Committee-forecast clearance. |
| **Effort** | Low once Q4 prints exist; high if done now (no 2026 Q4 yet as of this menu). |
| **Disposition** | **park-until-trigger** |
| **How to authorize** | `authorize branch R-REALIZE` when 2026 Q4 actuals exist (or sooner if you want a premature HOLD) |

<a id="r-fml-indep"></a>
### R-FML-INDEP

| Field | Content |
|-------|---------|
| **Class** | Empirically resolvable |
| **Named source class** | Philadelphia Fed SPF, published central statistic (**median**), same L4 2026 GDP/U/PCE/core defs where SPF publishes them. **Named enough** (rule example). Tealbook / nowcast = different classes. |
| **What it is** | A **non-SEP** matched expected-path (same Q4/Q4 2026 GDP/U/PCE/core definitions) to test whether June medians **are** the economy’s central path. |
| **Why offered here** | L13 failed for brochure circularity and policy-mix; reopen condition was a new source class, not Table 1 again. |
| **What authorizing does** | Already ran as a **named-class pulse** (SPF Q2 2026 median under L4/L2). Intake + rubric + `04q`. Not Phase 2. |
| **What success / failure changes** | **Not established** for all four. PCE/core Q4/Q4 **print-match** (3.6 / 3.3); GDP **concept mismatch** (SPF annual-average 2.2 vs SEP Q4/Q4 2.2; SPF Q4 SAAR 1.6); unemployment SPF 2026Q4 **4.5** vs SEP **4.3**. Vintage: SPF ≤ May 12 vs SEP June 17. **Not a refute.** |
| **What it does *not* do** | Does not auto-clear because inflation printed 3.6. Does not put funds-rate on this bar. Does not convert annual-average GDP into Q4/Q4. Does not fetch Tealbook or a nowcast. |
| **Effort** | Medium (done) |
| **Disposition** | **Executed 2026-08-12 → L17.** Named class = Philadelphia Fed SPF Q2 2026 published **medians** of 33. Later SPF vintage (Q3 2026, when released) is a possible closer-vintage reopen — **not auto-run**. |
| **How to authorize** | Already run. Later vintage: say so in plain language (new pulse / `name source class …` if the class changes). |

<a id="r-fml-2027-28"></a>
### R-FML-2027-28

| Field | Content |
|-------|---------|
| **Class** | Empirically resolvable |
| **Named source class** | Same June 17 SEP brochure / L5 medians as L13, scoped to 2027 and 2028 (G5). Not a new independent class. Diminishing returns → `park-90d`. |
| **What it is** | Same F-ML-BAR test as L13, for **2027** and **2028** medians separately (L15). |
| **Why offered here** | L13 was 2026-only; G5 forbids copying that result automatically. |
| **What authorizing does** | Two scoped tests. Brochure + policy-mix blockers from L13 still apply. |
| **What success / failure changes** | Likely **not established** for the same identification reasons; PCE vintage-jump extra was 2026-specific. |
| **What it does *not* do** | Does not meet F-ML by being a later year. Does not test longer-run (L12). |
| **Effort** | Medium (diminishing returns) |
| **Disposition** | **park-90d** unless you want it now |
| **How to authorize** | `authorize branch R-FML-2027-28` |

<a id="r-rev"></a>
### R-REV

| Field | Content |
|-------|---------|
| **Class** | Claim-revision path |
| **Named source class** | **unnamed** / not a fetch — operator `run CR` or `authorize branch R-REV`. |
| **What it is** | Narrow the original claim (entire June SEP as most-likely outcomes / appropriate paths / LR convergence) to the **supported census core** (what 18 people submitted, how to read the tables, bars frozen and unmet). |
| **Why offered here** | Strong forecast-extension language is **not established** as P-BaseCase. Overlaps optional mode CR. |
| **What authorizing does** | Claim-Revision scaffolding — ranked successors; you still pick keep-original vs a successor. **Does not rewrite parent record silently.** |
| **What success changes** | Partner-facing wording matches established core; FD-smuggle risk drops. |
| **What it does *not* do** | Does not meet F-ML-BAR by rewording. Does not start a successor app until you pick one. |
| **Effort** | Low–medium |
| **Disposition** | Not authorized (default) |
| **How to authorize** | `authorize branch R-REV` or `run CR` |

<a id="r-july29"></a>
### R-JULY29

| Field | Content |
|-------|---------|
| **Class** | Parked / OUT of package |
| **Named source class** | July 29, 2026 FOMC statement — **OUT** unless explicitly elevated into L₀. |
| **What it is** | July 29, 2026 FOMC **statement** (hold 3.50–3.75; “will deliver price stability”; 9–3). Different document, later date. |
| **Why listed here** | So it is not smuggled as a residual “to finish” C-APPROP-as-vote or 2026-on-target. |
| **What authorizing does** | Would **elevate** it into L₀ — a package change, not a quiet admit. |
| **What it does *not* do** | Does not become in-package by being on this menu. |
| **Effort** | n/a until elevated |
| **Disposition** | **drop** unless you explicitly elevate July 29 into this package |
| **How to authorize** | Not a normal branch. Say so in plain language if you want a **new** package or an L₀ elevation. |

---

## 3. Definition-blocked (lock first, then branch)

| Residual ID | What must be locked first | Then branch could… |
|-------------|---------------------------|--------------------|
| [R-G8-SCOPE](#r-g8-scope) | Realization in-scope-now vs later (this freeze) | [R-REALIZE](#r-realize) stays a later empirical slot |
| C-APPROP-as-vote | July 29 (or another vote record) **in** L₀ | Score dots vs a Committee decision — **not** available while July 29 is OUT |
| F-LR as dated year | A dated longer-run horizon (substantial vs SEP A6) | Test “2.0 in year T” — not the current F-LR object |

---

## 4. Not branchable by the method (normative / preference)

| Residual ID | Why not branchable |
|-------------|--------------------|
| “Should the FOMC have been more hawkish?” | Normative policy advice; not this claim package |
| Median *ought* to be treated as the Committee forecast | FD watch; method will not bless the smuggle |

---

## 5. Parked / no near-term path

| Residual ID | Disposition | Trigger / note |
|-------------|-------------|----------------|
| [R-REALIZE](#r-realize) | park-until-trigger | 2026 Q4 actuals under L4 definitions |
| [R-FML-INDEP](#r-fml-indep) | **executed → drop** | L17 SPF Q2 2026; not established; later vintage not auto-run |
| [R-FML-2027-28](#r-fml-2027-28) | park-90d | Same brochure/policy-mix as L13; L17 does not copy onto 2027–28; revisit ~2026-11-12 |
| [R-JULY29](#r-july29) | drop | OUT unless L₀ elevation |

---

## 6. Operator decision log

| Date | Action |
|------|--------|
| 2026-08-12 | Menu **offered** (operator `residual menu`). No branch authorized (default). Optional-modes menu drafted alongside. July 29 remains OUT. |
| 2026-08-12 | Operator `closeout` — hard stop sealed. Default **keep original wording**. No new branch run. G8 not locked. Amb stays ≈ 1. |
| 2026-08-12 | **Named-class pulse** R-FML-INDEP → L17 SPF Q2 2026. F-ML-BAR still **not established**. Not a refute. Not Phase 2. G8 still not locked. Parent closeout intact. |
| 2026-08-12 | **Post-rule review (gates 1–7):** named-enough pass; print-match ≠ met pass; no bar-collapse pass; establishment-stop **No**; seal-time park of this leftover was a closeout-default miss (now executed/drop, not resurrected to pursue). Named source class filled on all residual cards. |

---

*Standing rule: Residual-branch offering + clickable cards. Offering ≠ running. See `.cursor/rules/applications-gated-method.mdc`.*
