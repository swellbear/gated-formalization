# Optional Modes Menu

**App:** `2026-08_fomc-june-2026-sep`  
**Updated:** 2026-08-12  
**Closeout status:** **hard stop sealed** — **modes offered, not run**  
**Rule:** Offering ≠ running. Parent verdict unchanged until you authorize a mode.

**Glossary:** [`docs/READER_GLOSSARY.md`](../../docs/READER_GLOSSARY.md)  
**Residuals (separate):** [`RESIDUAL_BRANCH_MENU.md`](RESIDUAL_BRANCH_MENU.md)

---

## 0. Plain-language framing

**What we’re doing:** Listing optional tools that *could* run if you authorize them. Not required to close examination.

**What we need from you:** Nothing unless you want one.

**What authorizing means:** Runs only that mode. Does not rewrite what is established / not established.

**What this does *not* mean:** Automatic Phase 2; that 3.6% will happen; investment or policy advice.

**How this differs from residuals:** Residual branches reopen a *scoped gap* on this package. Optional modes are separate tools (uses, contrastive alternatives, revise wording, quantitative implication).

---

## 1. Applicability triage

| Mode | Offer / N/A | Why (this app) |
|------|-------------|----------------|
| **UX** Use-Exploration | **Offer** | Results exist: census vehicle + meaning freezes + 2026 F-ML test not established |
| **CX** Contrastive Recommendation | **Offer** | Established descriptive core (what the SEP prints) + failed elevation (P-BaseCase met; vote; 2026-on-target) |
| **CR** Claim-Revision | **Offer** | Revise-vs-keep applies; overlaps [R-REV](RESIDUAL_BRANCH_MENU.md#r-rev) |
| **QI** Quantitative Implication | **N/A** | No failed C≥H / Sharpe-style numerical *instance* bar. Unmet P-BaseCase is a modal bar, not a QI path |

---

## 2. Index (clickable)

| ID | One-line | Status |
|----|----------|--------|
| [UX](#ux) | Explore possible *uses* of findings (not advice) | **offered** |
| [CX](#cx) | Alternative claims that fit the census core without the failed elevation | **offered** |
| [CR](#cr) | Ranked successor wordings of this SEP claim | **offered** |
| [QI](#qi) | Scale-factor after failed numerical instance | **N/A** |

**Authorize grammar:**  
`run UX` · `decline UX` · `run CX` · `decline CX` · `run CR` · `decline CR` · `decline optional modes`

---

## 3. Cards

<a id="ux"></a>
### UX — Use-Exploration

| Field | Content |
|-------|---------|
| **Applicability** | **Offer** — census + unmet forecast bars are findings that can be *used* as documentation, not as a 2026 call |
| **What it is** | Instance-specific exploration of how this run’s findings could be used, guided by the original SEP-inventory claim |
| **What authorizing does** | Produce `UX_Use_Exploration.md`; rank 2–4 use options with “not advice / not established” labels |
| **What success changes** | Documentation only — **verdict / Amb / established unchanged** |
| **What it does *not* do** | Forecasts; “should the FOMC…”; treating 3.6% as the expected path |
| **Effort** | Low–medium |
| **How to authorize** | `run UX` |
| **How to decline** | `decline UX` |

<a id="cx"></a>
### CX — Contrastive Recommendation

| Field | Content |
|-------|---------|
| **Applicability** | **Offer** — printed SEP census is established; “these medians *are* the expected path / the vote / 2026 on-target” is not |
| **What it is** | 1–3 *different* claims that fit the established core (e.g. census-only wording; “SEP posed most-likely submissions”) and avoid the failed elevation |
| **What authorizing does** | Minimal gated check each alternative; exhibit `CX_…` — **does not overwrite parent record** |
| **What success changes** | Contrastive alternatives on file |
| **What it does *not* do** | Silent rewrite; new search unless authorized; import July 29 |
| **Effort** | Medium |
| **How to authorize** | `run CX` |
| **How to decline** | `decline CX` |

<a id="cr"></a>
### CR — Claim-Revision Scaffolding

| Field | Content |
|-------|---------|
| **Applicability** | **Offer** — original claim is the whole SEP inventory including most-likely / appropriate / LR convergence; F-ML-BAR not established |
| **What it is** | Ranked successor wordings (same lineage), dropping unsupported “will / is the expected path / Committee forecasts” |
| **What authorizing does** | CR scaffolding; you still pick keep-original vs a successor. Overlaps [R-REV](RESIDUAL_BRANCH_MENU.md#r-rev) |
| **What success changes** | Candidate successors offered — parent FD/L13 stay on record |
| **What it does *not* do** | Auto-start a new app; clear F-ML-BAR by rewording |
| **Effort** | Low–medium |
| **How to authorize** | `run CR` |
| **How to decline** | `decline CR` |

<a id="qi"></a>
### QI — Quantitative Implication & Counterfactual Benefit

| Field | Content |
|-------|---------|
| **Applicability** | **N/A** — L13 is an unmet modal bar (P-BaseCase), not a failed C≥H / Sharpe instance |
| **What it is** | After a failed numerical instance, scale-factor / shortfall under the same locks |
| **What authorizing does** | Would not apply on this package as currently locked |
| **What it does *not* do** | Upgrade “not established” into a should or a 2026 call |
| **Effort** | n/a |
| **How to authorize** | Do not `run QI` on this app unless a later numerical instance bar is locked and fails |
| **How to decline** | n/a (already N/A) |

---

## 4. Operator decision log

| Date | Action |
|------|--------|
| 2026-08-12 | Menu **drafted/offered** with residual menu. No mode run. QI N/A. |
| 2026-08-12 | Operator `closeout` — hard stop sealed. Modes still **offered, not run**. Default keep original wording (CR not executed). |

---

*Standing rule: Optional-mode offering. Offering ≠ running. See `.cursor/rules/applications-gated-method.mdc`.*
