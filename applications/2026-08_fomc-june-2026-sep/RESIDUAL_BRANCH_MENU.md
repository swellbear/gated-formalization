# Residual Branch Menu

**App:** `2026-08_fomc-june-2026-sep`  
**Updated:** 2026-08-12  
**Closeout status:** **hard stop sealed** — **menu offered, no branch run** (except R-FML-2026 already executed at L13)  
**Rule:** Offering ≠ running. Parent verdict unchanged. Click an ID for instance-specific explainers.

**Glossary:** [`docs/READER_GLOSSARY.md`](../../docs/READER_GLOSSARY.md)

**Live vs stand-in:** Live = June 17, 2026 SEP PDF/HTML. **OUT:** July 29 FOMC statement (not a residual in this package unless you elevate it).

**Amb ≈ 1** (Gap 8 realization still open). F-ML-BAR **not established** on 2026 medians (L13). Amb ≠ clearance.

---

## 0. Plain-language framing

**What we’re doing:** Listing leftover open items after hard stop. You can still authorize a branch, freeze realization as “later,” or leave them parked.

**What we need from you:** Nothing unless you want a branch. Click an ID for what it means *in this app*.

**What authorizing a branch means:** A scoped continuation on this same claim package — not a rewrite of what is already established / not established.

**What this does *not* mean:** Automatic Phase 2; that 2026 inflation will be 3.6%; importing the July 29 statement; advice.

---

## 1. Index (clickable)

| ID | One-line | Class | Disposition |
|----|----------|-------|-------------|
| [R-FML-2026](#r-fml-2026) | Test F-ML-BAR on 2026 GDP/U/PCE/core medians | Empirically resolvable | **executed → L13; not established** (not a refute) |
| [R-G8-SCOPE](#r-g8-scope) | Freeze realization as out of scope *now* | Definition freeze | Not authorized (default) |
| [R-REALIZE](#r-realize) | Compare 2026–28 actuals to submitted medians | Empirically resolvable | **park-until-trigger** |
| [R-FML-INDEP](#r-fml-indep) | Independent expected-path vs 2026 medians | Empirically resolvable | **park-until-trigger** |
| [R-FML-2027-28](#r-fml-2027-28) | Test F-ML-BAR on 2027 and 2028 medians | Empirically resolvable | **park-90d** (diminishing returns after L13) |
| [R-REV](#r-rev) | Narrow original wording to supported census core | Claim-revision path | Not authorized (default) |
| [R-JULY29](#r-july29) | Elevate July 29 statement into this package | Parked / OUT | **drop** unless you elevate L₀ |

**Authorize (open):** `authorize branch R-G8-SCOPE` · `authorize branch R-REALIZE` · `authorize branch R-FML-INDEP` · `authorize branch R-FML-2027-28` · `authorize branch R-REV` · `lock G8 realization-later` · `decline residual menu`

**Also offered (separate):** optional modes — [`OPTIONAL_MODES_MENU.md`](OPTIONAL_MODES_MENU.md). Offering ≠ running.

---

## 2. Cards

<a id="r-fml-2026"></a>
### R-FML-2026

| Field | Content |
|-------|---------|
| **Class** | Empirically resolvable (executed) |
| **What it is** | Whether 2026 medians GDP **2.2** / U **4.3** / PCE **3.6** / core PCE **3.3** meet F-ML-BAR (P-BaseCase). Funds-rate off this bar. |
| **Why offered here** | L2 froze the bar; L5 admitted the cells as *submitted*; meeting the bar was the leftover evaluation. |
| **What authorizing does** | Already ran: rubric + `04m`. |
| **What success / failure changes** | **Not established** for all four. Not a refute (no rival expected-path admitted). |
| **What it does *not* do** | Does not prove 2026 inflation will *not* be 3.6%. Does not test 2027–28. Does not put funds 3.8 under F-ML. |
| **Effort** | Medium (done) |
| **Disposition** | **Executed 2026-08-12 → L13.** Brochure + L11 policy-mix block identification; PCE extra: +0.9 vintage jump and 17/18 upside risk. |
| **How to authorize** | Already run. Re-open only via [R-FML-INDEP](#r-fml-indep) (new source class), not by re-reading Table 1. |

<a id="r-g8-scope"></a>
### R-G8-SCOPE

| Field | Content |
|-------|---------|
| **Class** | Definition freeze |
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
| **What it is** | A **non-SEP** matched expected-path (same Q4/Q4 2026 GDP/U/PCE/core definitions) to test whether June medians **are** the economy’s central path. |
| **Why offered here** | L13 failed for brochure circularity and policy-mix; reopen condition was a new source class, not Table 1 again. |
| **What authorizing does** | New evidence intake + quantitative rubric vs F-ML-BAR. Conflicted-source rules still apply. |
| **What success / failure changes** | May establish, leave not established, or refute 2026 medians as P-BaseCase. |
| **What it does *not* do** | Does not auto-clear by fetching any forecast that happens to print 3.6. Does not put funds-rate on this bar. |
| **Effort** | Medium–high (need a matched independent series under the same locks) |
| **Disposition** | **park-until-trigger** (operator names / admits a non-SEP expected-path source) |
| **How to authorize** | `authorize branch R-FML-INDEP` |

<a id="r-fml-2027-28"></a>
### R-FML-2027-28

| Field | Content |
|-------|---------|
| **Class** | Empirically resolvable |
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
| [R-FML-INDEP](#r-fml-indep) | park-until-trigger | Operator-admitted non-SEP matched expected-path |
| [R-FML-2027-28](#r-fml-2027-28) | park-90d | Same brochure/policy-mix as L13; revisit ~2026-11-12 |
| [R-JULY29](#r-july29) | drop | OUT unless L₀ elevation |

---

## 6. Operator decision log

| Date | Action |
|------|--------|
| 2026-08-12 | Menu **offered** (operator `residual menu`). No branch authorized (default). Optional-modes menu drafted alongside. July 29 remains OUT. |
| 2026-08-12 | Operator `closeout` — hard stop sealed. Default **keep original wording**. No new branch run. G8 not locked. Amb stays ≈ 1. |

---

*Standing rule: Residual-branch offering + clickable cards. Offering ≠ running. See `.cursor/rules/applications-gated-method.mdc`.*
