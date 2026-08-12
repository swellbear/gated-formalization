# Operator Workflow — New Application Checklist

Use this checklist for every new claim, theory fragment, or argument you run through the method.

**Canonical method (full rules):** `.cursor/rules/applications-gated-method.mdc`  
Do not treat this file as a second full copy of the standing rule — checklist + pointers only.

**Quick map:** Phase 1 (autonomous while Amb drops / gaps descriptive; **soft-modal fork** early when needed) → Phase 2 (authorized; **accuracy not substantiation**) → optional Experimental Generation → closeout with **Original-Claim Assessment** (**Amb ≠ clearance**) → optional **Claim-Revision Scaffolding** → optional **QI** → optional **Application Thesis Tracker** (per-app longitudinal watchlist).  
Also in force when applicable: inter-parameter dependencies; locking-scaffolding (incl. **lock-time Amb warning**); scoped-result honesty; package evidence intake (**conflicted-source rule**); scenario passes (**already-included legs**); soft-modal fork; compact no-admit; revision-vs-continuation fork; Claim-Revision Scaffolding; QI mode; **Application Thesis Tracker** (app-attached; thesis watchlist over time).  
**Cons / Amb / redefinition** primary; **Agree / Prod** secondary. High Amb after serious search = Provisional, not false. **Low Amb ≠ claim cleared.**

## 1. Setup
- [ ] Create folder `applications/YYYY-MM_short-name/`
- [ ] Copy templates `01`–`05` (+ `R_Locking_Scaffolding`, `CR_Claim_Revision_Scaffolding`, `QI_Quantitative_Implication_Counterfactual_Benefit`, `T_Application_Thesis_Tracker`, `E_Package_Evidence_Intake`, `S_Scenario_Pass`, `Compact_No_Admit_Readout` as needed)
- [ ] Note the date and a short description of the source material

## 2. Anchors & Claim-Type Pre-Classification
- [ ] Fill `01_Anchor_and_ClaimType_Template.md`
- [ ] List only hard-to-dispute anchors
- [ ] State the candidate claim / layer clearly
- [ ] Flag **Descriptive** / **Normative/Strategic** / **Mixed** (split if mixed)
- [ ] If soft modals (potential / could / should / …) carry strength: flag **soft-modal fork** early
- [ ] Confirm ready for gate scoring

## 3. Initial Gate Scoring (Phase 1 start)
- [ ] Fill `02_Gate_Scoring_Sheet.md` (Cons/Amb primary; Agree/Prod secondary — crisp needle rules)
- [ ] Higher-level review
- [ ] Verdict + reliability estimate
- [ ] Readout; if continuation criteria hold, proceed to gap ranking / Cycle 1

## 4. If Amb High or Provisional / Not Admissible
- [ ] Fill `03_Gap_Extraction_and_Ranking.md` (include claim-freeze lines)

## 5. Gap-Directed Search & Material Admission (Phase 1 cycle)
- [ ] Fresh `04` per candidate; relevance + Cons; ADMIT / REJECT / HOLD

## 6. Re-score (end of Phase 1 cycle)
- [ ] Update gate sheet if anything admitted / Amb changed
- [ ] **Full readout** if admit / Amb change / agenda shift
- [ ] **Compact no-admit** otherwise (`Compact_No_Admit_Readout.md`) — mandatory; no padded narrative
- [ ] Continue Phase 1 autonomously **or** stop for Phase 1 endpoint (agenda + claim-freeze + dependencies + Phase 2 class)

## 7. Phase 2 (only if authorized and domain-applicable)
- [ ] **Accuracy posture** — improve established / not established / refuted; do not optimize for substantiating the slogan
- [ ] Quote claim-freeze; formal `04`s; no silent claim narrowing
- [ ] Dependencies / locking-scaffolding / OR-slots / scoped honesty as required by canonical rule
- [ ] Package evidence → `E_Package_Evidence_Intake.md` (incl. **conflicted-source flag**) then `04`
- [ ] Scenario / multi-leg passes → list **already-included legs** (`S_Scenario_Pass.md`)
- [ ] Intractability checklist before “currently intractable”
- [ ] Stop for authorization between significant attempts
- [ ] State locked-bar status explicitly; remember **Amb ≠ clearance**

## 7b. Experimental Generation (only if batch-authorized)
- [ ] Follow canonical Experimental Generation Mode in `.mdc` (≤3 default; separation; audit; red-team; Amb-net; near-miss)

## 8. Close the Run
- [ ] Fill `05_Original_Claim_Assessment.md` (status + **Amb ≠ clearance** + locked-bar status + continuation options + **revision vs continuation fork** when required)
- [ ] Final verdict; phase status; scoped vs unrestricted distinction
- [ ] Failure-mode cadence → `logs/failure_mode_log.md` if there is anything to learn

## 8b. Claim-Revision Scaffolding (only if revision path authorized)
- [ ] Follow canonical Claim-Revision Scaffolding in `.mdc` (`CR_Claim_Revision_Scaffolding.md`)
- [ ] Ranked successor claims + deviation labels; parent closeout / FD findings stay on record
- [ ] Do **not** select a revision or start a new application until operator picks an option
- [ ] Distinct from Experimental Generation (existing-claim free parameters vs successor claims)

## 8c. Quantitative Implication & Counterfactual Benefit (only if authorized after failed numerical instance)
- [ ] Plain-language framing first (`QI_Quantitative_Implication_Counterfactual_Benefit.md`)
- [ ] Operator picks: full path (A+B) / scale-factor only (A) / neither
- [ ] If A: report scale factor, shortfall, counterfactual quantity under same locks (implication label)
- [ ] If B: extract/freeze benefit; evaluate conditioned claim through ordinary gates; report supported vs open
- [ ] Do **not** upgrade failed instance into support for the original/revision claim
- [ ] Distinct from Experimental Generation and Claim-Revision Scaffolding

## 8d. Application Thesis Tracker (only if authorized for that app)
- [ ] Open `Thesis_Tracker.md` from `T_Application_Thesis_Tracker.md` in the **application folder**
- [ ] Derive **app-specific** watchlist from that claim’s locks / bars / FD / reopen / legs
- [ ] Seed snapshot + baseline timeline; append on material status changes
- [ ] Does **not** overwrite closeout; not a repo-wide dashboard

## Reminders
- Canonical detail lives only in `.cursor/rules/applications-gated-method.mdc`.
- Compact no-admit is mandatory for no-change cycles.
- Package OR-slots must be singled or formally “either”-accepted before dependents proceed.
- Locking-scaffolding must open with plain-language framing and include an objective claim-deviation assessment (fixed dimensions/labels) for every package.
- If **no Minimal-deviation package** exists, run **forced-deviation extraction**: name the claim terms that force deviation; carry them as first-class agenda/freeze items and into the Original-Claim Assessment (non-derivative testing impossible — property of claim text, not mere missing data).
- Closeout is not silent resolution of the original claim.
- **Low Amb ≠ claim cleared**; locked bars need established / not established / refuted.
- Phase 2 defaults to **accuracy**, not substantiation-seeking.
- Soft-modal fork early when potential/could/should/etc. carry claim strength.
- Conflicted sources cannot solely affirm locked modal bars.
- Scenario passes must list **already-included legs**.
- Lock selection: Amb drop from fixing meanings ≠ clearance (lock-time warning).
- Application Thesis Tracker is per-app, authorization-gated, and thesis-watchlist shaped for that claim.
- Claim-Revision Scaffolding is authorization-gated; does not silently replace the original claim.
- Quantitative Implication & Counterfactual Benefit is authorization-gated after a failed numerical instance test; implications/counterfactuals ≠ proof of the claim.
