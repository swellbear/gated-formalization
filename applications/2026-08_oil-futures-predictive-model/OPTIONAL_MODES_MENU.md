# Optional Modes Menu

**Mandatory to produce at endpoint / hard-stop closeout when any optional mode applies.**  
**Offering ≠ running.** Parent closeout / verdict unchanged until the operator authorizes a mode.

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Closeout status:** **hard stop (residuals live)** — UX/CX/CR **declined, not run** (operator **C** `decline optional modes`)

**Glossary:** [`docs/READER_GLOSSARY.md`](../../docs/READER_GLOSSARY.md)  
**Residuals (separate):** [`RESIDUAL_BRANCH_MENU.md`](RESIDUAL_BRANCH_MENU.md)

---

## 0. Plain-language framing

**What we’re doing:** Recording the optional-mode offer that was listed at closeout. Operator **C** declined it. The cards stay as the audit trail of what those modes would have meant.

**What we need from you:** Nothing on this menu. Operator **C** declined optional modes. Click an ID only if you want the record of what those modes would have meant.

**What authorizing means:** Runs that mode only (UX / CX / CR as named). Does **not** silently rewrite the parent closeout. Does **not** invent a skill class.

**What this does *not* mean:** Automatic Phase 2; trading advice; changing what was already established / not established; clearing the blended slogan.

**How this differs from residuals:** Residual branches reopen a *scoped gap* on the same Rank 4 package (especially the live skill leftover). Optional modes are separate post-closeout tools (explore uses, contrastive alternatives, revise wording).

---

## 1. Applicability triage (required)

| Mode | Offer / N/A | Why (this app) |
|------|-------------|----------------|
| **UX** Use-Exploration | **Offer** | Existence is established (futures-target); skill and value are not shown — uses of *that* split, not a trade |
| **CX** Contrastive Recommendation | **Offer** | Established core (a futures-target recipe has been written) + elevations not established (skill / after-cost value). Alternatives can fit the split without smuggling “the model works” |
| **CR** Claim-Revision | **Offer** | Original one-liner blends three jobs. Operator may want a cleaner successor (existence-only, or skill-only) labeled as such. Default: **keep original wording** |
| **QI** Quantitative Implication | **N/A** | No failed C≥H / Sharpe-style numerical *instance* bar. Unnamed skill is not a QI path |

---

## 2. Index (clickable)

| ID | One-line | Status |
|----|----------|--------|
| [UX](#ux) | Explore possible *uses* of findings (not advice) | **declined** |
| [CX](#cx) | Alternative claims that fit the existence core without a fake skill/value bar | **declined** |
| [CR](#cr) | Ranked successor wordings (existence-only or skill-only, labeled) | **declined** |
| [QI](#qi) | Scale-factor after failed numerical instance | **N/A** |

**Authorize grammar (show these one-liners):**  
`run UX` · `decline UX` · `run CX` · `decline CX` · `run CR` · `decline CR` · `decline optional modes`

---

## 3. Cards (required for every Offer or N/A row)

<a id="ux"></a>
### UX — Use-Exploration

| Field | Content |
|-------|---------|
| **Applicability** | **Offer** — “a futures-target recipe has been written; skill and after-cost value are not shown” can be used as documentation, not as a trade |
| **What it is** | Instance-specific exploration of how this run’s findings could be used, guided by the original question |
| **What authorizing does** | Produce `UX_Use_Exploration.md`; rank 2–4 use options with “not advice / not established” labels |
| **What success changes** | Documentation only — **verdict / Amb / established unchanged** |
| **What it does *not* do** | Forecasts; “should trade”; treating unnamed skill as unlikely; filling F-SRC |
| **Effort** | Low–medium |
| **How to authorize** | `run UX` |
| **How to decline** | `decline UX` |

<a id="cx"></a>
### CX — Contrastive Recommendation

| Field | Content |
|-------|---------|
| **Applicability** | **Offer** — existence established (futures-target); skill and value not established |
| **What it is** | 1–3 *different* claims that fit the established core (e.g. “a specified futures-target mapping exists”; “spot-oil papers are a nearby kinship, not this freeze”) and avoid a fake skill or trading-value call |
| **What authorizing does** | Minimal gated check each alternative; exhibit `CX_…` — **does not overwrite parent record** |
| **What success changes** | Contrastive alternatives on file |
| **What it does *not* do** | Silent rewrite; treating L-D-SUITE as F-SRC; inventing a skill class |
| **Effort** | Medium |
| **How to authorize** | `run CX` |
| **How to decline** | `decline CX` |

<a id="cr"></a>
### CR — Claim-Revision Scaffolding

| Field | Content |
|-------|---------|
| **Applicability** | **Offer** — original one-liner blends existence / skill / value; Rank 4 named the split; operator may want successor wording labeled as such |
| **What it is** | Ranked *successor wordings* of this lineage (existence-only, or skill-only with a named protocol) |
| **What authorizing does** | Run CR scaffolding; you still pick which successor (if any). Does **not** auto-start a new app |
| **What success changes** | Candidate successors offered — parent Rank 4 / D-EXIST-MET-FT / leave-unnamed seals stay on record |
| **What it does *not* do** | Auto-clear skill or value; fold spot/real-price recipes into D-EXIST without labeling a freeze change |
| **Effort** | Medium |
| **How to authorize** | `run CR` |
| **How to decline** | `decline CR` |

<a id="qi"></a>
### QI — Quantitative Implication & Counterfactual Benefit

| Field | Content |
|-------|---------|
| **Applicability** | **N/A** — no failed numerical instance bar; unnamed skill is not a QI path |
| **What it is** | After a failed C≥H / Sharpe-style instance, report scale-factor / shortfall |
| **What authorizing does** | N/A |
| **What success changes** | N/A |
| **What it does *not* do** | Does not apply to an unmet modal bar or an unnamed vehicle |
| **Effort** | — |
| **How to authorize** | N/A |
| **How to decline** | N/A |

---

## 4. Operator decision log

| Date | Action |
|------|--------|
| 2026-08-17 | Menu offered at hard-stop closeout. `leave unnamed` is **not** `run CR`. Default keep original wording. Offering ≠ running. |
| 2026-08-17 | Operator **C** → `decline optional modes`. UX/CX/CR **declined, not run**. QI remains **N/A**. Parent closeout / Amb / established unchanged. |

---

*Standing rule: Optional-mode offering at closeout. Offering ≠ running. See `.cursor/rules/applications-gated-method.mdc`.*
