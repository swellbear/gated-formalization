# Optional Modes Menu

**Mandatory to produce at endpoint / hard-stop closeout when any optional mode applies.**  
**Offering ≠ running.** Parent closeout / verdict unchanged until the operator authorizes a mode.

**Date:**  
**Application:**  
**Closeout status:**  

**Glossary:** `docs/READER_GLOSSARY.md`

---

## 0. Plain-language framing

**What we’re doing:** Listing optional next steps that *could* run after closeout if you authorize them.  

**What we need from you:** Nothing unless you want one. Click an ID for what that mode means *in this app*.  

**What authorizing means:** Runs that mode only (UX / CX / CR / QI as named). Does **not** silently rewrite the parent closeout.  

**What this does *not* mean:** Automatic Phase 2; advice; changing what was already established / not established.

**How this differs from residuals:** Residual branches reopen a *scoped gap* on the same claim package. Optional modes are separate post-closeout tools (explore uses, contrastive alternatives, revise wording, quantitative implication).

---

## 1. Applicability triage (required)

Mark each mode **Offer** / **N/A** with one-line why. Do **not** hide applicable modes.

| Mode | Offer / N/A | Why (this app) |
|------|-------------|----------------|
| **UX** Use-Exploration | | Results exist → usually **Offer** after endpoint/closeout |
| **CX** Contrastive Recommendation | | Offer when some core **established** and a stronger elevation / should / uniqueness **not** established |
| **CR** Claim-Revision | | Offer when revise-vs-keep fork applies (strong language mostly unsupported) **or** operator may want cleaner successor wording |
| **QI** Quantitative Implication | | Offer only after a **failed numerical instance** bar (C≥H / Sharpe-style); else **N/A** |

---

## 2. Index (clickable)

| ID | One-line | Status |
|----|----------|--------|
| [UX](#ux) | Explore possible *uses* of findings (not advice) | offered / declined / ran / N/A |
| [CX](#cx) | Propose alternative claims that fit established core better | offered / declined / ran / N/A |
| [CR](#cr) | Ranked successor wordings of *this* claim lineage | offered / declined / ran / N/A |
| [QI](#qi) | Scale-factor / counterfactual benefit after failed numerical bar | offered / declined / ran / N/A |

**Authorize grammar (show these one-liners):**  
`run UX` · `decline UX` · `run CX` · `decline CX` · `run CR` · `decline CR` · `run QI` · `decline QI` · `decline optional modes`

---

## 3. Cards (required for every Offer or N/A row)

Use explicit anchors: `<a id="ux"></a>`, etc.

<a id="ux"></a>
### UX — Use-Exploration

| Field | Content |
|-------|---------|
| **Applicability** | Offer / N/A — (why) |
| **What it is** | Instance-specific exploration of how findings could be *used*, guided by original claim intent |
| **What authorizing does** | Produce `UX_Use_Exploration.md` exhibit; rank 2–4 use options with mandatory “not advice / not established” labels |
| **What success changes** | Documentation only — **verdict / Amb / established unchanged** |
| **What it does *not* do** | Forecasts, should, investment advice, slogan clearance |
| **Effort** | low / medium |
| **How to authorize** | `run UX` |
| **How to decline** | `decline UX` |

<a id="cx"></a>
### CX — Contrastive Recommendation

| Field | Content |
|-------|---------|
| **Applicability** | Offer / N/A — (why) |
| **What it is** | 1–3 *different* alternative claims/rules that fit the established core and avoid the failed elevation |
| **What authorizing does** | Minimal gated check each alternative; rank by fit / low new Amb; exhibit `CX_…` |
| **What success changes** | Contrastive recommendations on record — **does not overwrite parent closeout** |
| **What it does *not* do** | Silent rewrite of original claim; new evidence search unless authorized |
| **Effort** | medium |
| **How to authorize** | `run CX` |
| **How to decline** | `decline CX` |

<a id="cr"></a>
### CR — Claim-Revision Scaffolding

| Field | Content |
|-------|---------|
| **Applicability** | Offer / N/A — (why) |
| **What it is** | Ranked *successor wordings* of this claim lineage (same family), dropping unsupported strong language |
| **What authorizing does** | Run CR scaffolding; operator still picks which successor (if any) |
| **What success changes** | Candidate successors offered — parent FD/closeout stay on record |
| **What it does *not* do** | Auto-start a new app; invent a single revision silently |
| **Effort** | low / medium |
| **How to authorize** | `run CR` |
| **How to decline** | `decline CR` |

<a id="qi"></a>
### QI — Quantitative Implication & Counterfactual Benefit

| Field | Content |
|-------|---------|
| **Applicability** | Offer / N/A — (why) |
| **What it is** | After a **failed numerical instance**, report scale-factor / shortfall / conditioned benefit under same locks |
| **What authorizing does** | QI path A and/or B per template — implication labels only |
| **What success changes** | Implications documented — **does not upgrade failed instance into claim support** |
| **What it does *not* do** | Prove the original should/elevation; apply when no numerical instance bar failed |
| **Effort** | medium |
| **How to authorize** | `run QI` |
| **How to decline** | `decline QI` |

---

## 4. Operator decision log

| Date | Action |
|------|--------|
| | Menu offered at closeout — awaiting operator |

---

*Standing rule: Optional-mode offering at closeout. Offering ≠ running. See `.cursor/rules/applications-gated-method.mdc`.*
