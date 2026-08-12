# Dissertation — Application Findings

**Mandatory closeout deliverable** for every closed application (or closed claim family). Faithful to admitted layers, failures, locks, and closeout. Main body readable by a non-technical audience; technically precise (no silent softening of negative results). Scoped vs unrestricted conclusions explicit. Parent/successor relationships stated when relevant.

**Date:** 2026-08-11  
**Application:** `2026-08_av-e2e-vs-modular-preferability`  
**Claim family / parent (if any):** None (standalone Mixed claim; no Claim-Revision successor opened)  
**Closeout verdict:** **Stable Provisional** (Amb ≈ **4**)  
**Amb at closeout:** ≈ **4**

---

## 1. Plain-language summary

This run asked whether end-to-end neural networks are **preferable** to modular perception–planning–control stacks for autonomous driving **because** they **alone** avoid cascading errors from hand-engineered interfaces and can keep improving with data and scale in a way modular stacks **structurally cannot**.

What held up is modest and structural: architecture choice is a **spectrum** (modular / hybrid / more end-to-end), not a clean binary; modular stacks **can** learn from data; “cascading” interface errors and end-to-end compounding/shift errors are **different kinds** of problems; and bare “preferable” is not fixed by descriptive facts alone. Under an operator-chosen comparison package (**P-Strong-Both**), two relative technical questions (scaling and error budgets) become **well-posed** — but those questions remain **empirically open**.

What did **not** hold up is the persuasive package as written. Modular stacks do **not** “structurally cannot” improve with data. End-to-end does **not** uniquely (“alone”) solve the cascading-interface problem. Avoiding hand-engineered interfaces does **not** **eliminate** cascading failures — it relocates or changes where failure shows up. Unrestricted preferability was never locked or established.

**Bottom line:** The original claim is **not** well-constrained. Strong slogans are unsupported or negatively constrained. Low Amb after locks is **not** clearance. Closeout is **Stable Provisional**, not resolution.

---

## 2. Original claim and context

**Original claim (verbatim):**

> End-to-end neural networks are preferable to modular (perception–planning–control) architectures for autonomous driving because they alone avoid cascading errors from hand-engineered interfaces and can continue to improve with data and scale in a way that modular stacks structurally cannot.

**Source / domain context:** Autonomous driving architecture debate — end-to-end neural mappings from sensors to controls/waypoints versus modular pipelines with separately engineered perception, prediction/planning, and control connected by explicit interfaces. Hybrids are common in practice.

**Claim type:** Mixed  
- Descriptive: uniqueness of cascading-avoidance; E2E improvement with data/scale; modular “structurally cannot”; “alone.”  
- Normative/Strategic: therefore E2E is **preferable**.

**Parent or successor relationship (if any):** None opened. Closeout kept original wording (revision fork left unchecked). No successor application started.

---

## 3. How it was examined

**Method path:**

1. **Phase 1** — Anchors, Mixed split, gap ranking, Material Admission Checks. Strong clauses were constrained away: spectrum lock; modular-with-learning falsifies structural impossibility; preferability is multi-criterial; cascading is relocation not elimination; “alone” not forced; global preferability without ODD/metrics/comparison class is not well-posed. Amb fell from ~12 to ~6.
2. **Phase 2 Attempt 1** — Joint-optimization asymmetry and error-budget taxonomy admitted weakly; general relative scaling (R1) and error-magnitude (R2) questions marked **intractable while R4 unset**. Amb ≈ 5.
3. **Corrective closeout** — Explicit inter-parameter rule: R1/R2 blocked primarily by unset **R4** (architecture pair + ODD + metrics + matching). Preferability criteria (**R3**) left open and not entered.
4. **R4 locking-scaffolding** — Ranked packages with relevance warnings. Every package was claim-adjacent at best; none restores “alone,” elimination, structural-cannot, or bare preferability.
5. **Operator lock: P-Strong-Both** — Spectrum pair hybrid mid-level vs more-E2E (A3); metrics C5 > C6 > C1; ODD and matching left as OR-slots (B1|B2, D5|D1).
6. **Phase 2 Attempt 2 (under P-Strong-Both only)** — R1/R2 become well-posed scoped questions; A3 joint-opt restated as mechanism candidate; empirical closure of R1 and R2 marked **intractable without package-satisfying evidence**. Amb ≈ 4.
7. **Original-Claim Assessment Closeout** — Application closed Stable Provisional; keep original wording; research agenda only unless further authorization.

**Governing lock / freeze (if any):** **R4 = P-Strong-Both** (`R4_Lock_P-Strong-Both.md`). Relevance: **partial / claim-adjacent**. Amb drop from locking ≠ clearance.

**Key artifacts:** `01_Anchor_and_ClaimType_Template.md`; `03_Gap_Extraction_and_Ranking.md`; `04a`–`04o`; `R4_Locking_Scaffolding_Choice_Set.md`; `R4_Lock_P-Strong-Both.md`; `02e_Corrective_Closeout_Interparam_Dependency.md`; `02f_Phase2_Attempt2_P-Strong-Both.md`; `Original_Claim_Assessment_Closeout.md`; `final_verdict.md`; `admitted_layers.md`; `notes.md`.

---

## 4. What was established

*(Only what admitted material actually constrained. Mark scope: unrestricted vs under lock/package.)*

| Finding | Scope |
|---------|--------|
| Architecture comparison is a **spectrum** (modular / hybrid / more-E2E); binary exclusive partition not assumed | **Unrestricted** (L1a) |
| Preferability is **multi-criterial** — a fork; not fixed by descriptive premises alone | **Unrestricted** (L1c); **R3 never entered** |
| Global preferability without ODD / metrics / comparison class is not well-posed | **Unrestricted** (L2c); then dependents scoped under **P-Strong-Both** |
| Interface-composition vs E2E compounding/shift errors are **distinct categories** | **Unrestricted** taxonomy (L3b) |
| Differentiable joint optimization across hard cuts is a **design asymmetry** (mechanism candidate, weak) | **Unrestricted** weak (L3a); restated for A3 under package (L4b) |
| Under **P-Strong-Both**, R1/R2 are **well-posed** scoped technical questions | **Under P-Strong-Both only** (L4a) |
| R1 empirical closure needs package-satisfying C5/C1 evidence | **Under P-Strong-Both** (L4c) — intractability-of-closure, not a positive scaling result |
| R2 empirical closure needs package-satisfying C6 evidence | **Under P-Strong-Both** (L4d) — same |

**Scoped-result honesty:** Findings under P-Strong-Both are **not** unrestricted support for the original claim.

---

## 5. What was not established

| Item | Status |
|------|--------|
| Modular stacks **structurally cannot** improve with data/scale | **Refuted** as stated (L1b) — modular-with-learning can improve |
| E2E **alone** avoids the cascading-interface problem | **Not established** / uniqueness fails (L2b) |
| Avoiding hand-engineered interfaces **eliminates** cascading errors | **Refuted** as elimination claim (L2a) — relocates/changes loci; compounding/shift remain |
| Unrestricted **preferability** of E2E over modular | **Not established** — R3 never locked; no admitted preferability layer |
| Relative scaling advantage as **unrestricted** established fact | **HOLD** (`04g`) — not admitted |
| Empirical R1 (C5/C1 scaling under P-Strong-Both) | **Open** — well-posed; evidence-blocked |
| Empirical R2 (C6 error budgets under P-Strong-Both) | **Open** — well-posed; evidence-blocked |
| Original persuasive package as a whole | **Not established** — essentially all strong language unsupported as unrestricted claim |

---

## 6. Forced deviations and scope limits

**Forced-deviation terms (if any):** The original wording’s **alone**, **avoid cascading** (as elimination), **structurally cannot**, and bare **preferable** could not be tested in non-derivative form that preserves them. Locking-scaffolding found **no Minimal-deviation** package that still tests those exclusivity slogans; every realistic package is at best **partial / claim-adjacent**. Those terms remain first-class failures of the claim text relative to available anchors and comparison tools — not merely “more data needed.”

**Scoped vs unrestricted:**

- **Unrestricted (Phase 1):** spectrum; modular can learn; preferability fork; cascading relocated; alone not forced; scope evaluation lock; weak joint-opt asymmetry; error taxonomy.
- **Under P-Strong-Both only:** well-posedness of R1/R2; A3 mechanism restatement; empirical intractability without matched evidence.
- **Never elevated:** unrestricted preferability; uniqueness; cascading-elimination; modular structural impossibility.

**What the lock/package could not settle relative to the original wording:** Whether E2E is preferable; whether E2E alone avoids cascading interface errors; whether modular stacks structurally cannot scale; any global slogan reading of the packaged claim. It only opens relative A3 scaling/error-budget questions under named ODD/metrics/matching (with OR-slot debt still unpaid).

**OR-slot debt at closeout:** B ∈ {B1, B2} and D ∈ {D5, D1} not singled and not formally either-accepted. Further dependent work requires picking singles or formally accepting “either.”

---

## 7. Quantitative results (if any)

None as pass/fail numerical clearances of the original claim.

**Amb path (definitional / constraint scores, not proofs):**

| Stage | Amb |
|-------|-----|
| Cycle 0 | 12 |
| Phase 1 endpoint | ≈ 6 |
| Phase 2 Attempt 1 / corrective | ≈ 5 |
| P-Strong-Both + Attempt 2 / closeout | ≈ **4** |

**Amb ≠ clearance:** Amb ≈ 4 means remaining free parameters are reduced after locks and negatives; it does **not** mean preferability, uniqueness, or empirical R1/R2 wins are established.

---

## 8. Revisions, implications, and alternatives

**Claim-Revision Scaffolding:** Not run. Closeout fork: **Keep original wording** (default); Revise claim left unchecked.

**QI / Contrastive Recommendation / Experimental Generation:** Not authorized / not run for this application.

**Continuation options on record** (from `Original_Claim_Assessment_Closeout.md`): package-satisfying evidence pass under P-Strong-Both; alternate locking package; explicit claim revision to a scoped relative-advantage thesis; enter R3 after/with evidence; Experimental Generation under package anchors; hard stop with research agenda only (default).

Original claim text and Phase 1 negatives remain on the record. Scoped package work does not overwrite them.

---

## 9. Final status of the original claim

**Verdict:** **Stable Provisional**. Original claim **not** well-constrained. Closeout is **not** silent resolution.

**Amb ≠ clearance:** Amb ≈ **4** at closeout. Locked preferability / uniqueness / elimination / structural-cannot bars: **not established** or **refuted**. Empirical R1/R2 under P-Strong-Both: **not established** (open, evidence-blocked). Low Amb after R4 lock does **not** clear the original slogan.

**Locked-bar status summary:**

| Bar / term | Status |
|------------|--------|
| Preferable (P) / R3 | Not entered; unsupported |
| Alone | Negatively constrained |
| Cascading elimination | Negatively constrained |
| Modular structurally cannot | False as stated |
| Relative R1/R2 under P-Strong-Both | Well-posed; empirically open |

**Continuation / hard-stop note:** Application **closed**. Awaiting further authorization only if continuing (evidence pass, revision, R3, Experimental Generation, etc.). Default: hard stop with research agenda.

---

## 10. What would still be needed

Concrete reopen / continuation conditions (not vague “more research”):

1. **Package-satisfying evidence** — Admit or produce studies matching **A3** + named **B1 or B2** + **C5/C6/C1** + **D5 or D1**, after OR-slots are singled or formally either-accepted; then reassess empirical R1 and/or R2 **under P-Strong-Both only**.
2. **Optional R3 lock** — Preferability criteria, if (P) is to be evaluated; without empirical R1/R2 wins, preferability still will not follow from Phase 1 negatives alone.
3. **Optional explicit claim revision** — New or marked-revised application dropping alone / structural-cannot / bare preferability in favor of a scoped relative A3 thesis.
4. **Optional Experimental Generation** — Separate batch authorization under P-Strong-Both anchors; will not restore original strong language without smuggling.

Absent those, the application stays closed as Stable Provisional with original wording retained.

---

## 11. Technical appendix

### Amb path

| Stage | Amb | Note |
|-------|-----|------|
| Cycle 0 | 12 | Original packaged claim |
| Phase 1 endpoint | ≈ 6 | Strong clauses constrained away |
| Phase 2 Attempt 1 | ≈ 5 | R1/R2 R4-dependent |
| Corrective + scaffolding | ≈ 5 | Ranked packages + relevance warnings |
| P-Strong-Both lock + Attempt 2 | ≈ **4** | R1/R2 well-posed; empirically open |
| Closeout | ≈ **4** | Original-Claim Assessment; Stable Provisional |

### Admitted layers (index)

| ID | One-line | Pointer |
|----|----------|---------|
| L1a | Architecture spectrum (not exclusive binary) | `04a_Material_Admission_L1a_Architecture_Spectrum.md` |
| L1b | Modular-with-learning; “structurally cannot” false | `04b_Material_Admission_L1b_Modular_Learning.md` |
| L1c | Preferability multi-criterial fork | `04c_Material_Admission_L1c_Preferability_Criteria_Fork.md` |
| L2a | Cascading relocated, not eliminated | `04d_Material_Admission_L2a_Cascading_Errors_Relocation.md` |
| L2b | “Alone” uniqueness not forced | `04e_Material_Admission_L2b_Alone_Not_Forced.md` |
| L2c | Scope / evaluation lock (ODD/metrics/class) | `04f_Material_Admission_L2c_Scope_Evaluation_Lock.md` |
| HOLD | Relative scaling as unrestricted fact | `04g_Material_Admission_HOLD_Relative_Scaling_Advantage.md` |
| L3a | Joint-opt asymmetry (weak) | `04h_Material_Admission_L3a_Joint_Opt_Asymmetry.md` |
| L3b | Error-budget taxonomy | `04i_Material_Admission_L3b_Error_Budget_Taxonomy.md` |
| L3c | General R1 intractable while R4 unset | `04j_Material_Admission_L3c_R1_Intractability.md` |
| L3d | General R2 intractable while R4 unset | `04k_Material_Admission_L3d_R2_Intractability.md` |
| L4a | R1/R2 well-posed under P-Strong-Both | `04l_Material_Admission_L4a_Scoped_Wellposedness.md` |
| L4b | A3 mechanism under package | `04m_Material_Admission_L4b_A3_Mechanism_Under_Package.md` |
| L4c | R1 empirical intractability under package | `04n_Material_Admission_L4c_R1_Empirical_Intractability_Under_Package.md` |
| L4d | R2 empirical intractability under package | `04o_Material_Admission_L4d_R2_Empirical_Intractability_Under_Package.md` |

### Key artifacts

- `Original_Claim_Assessment_Closeout.md` — canonical closeout
- `final_verdict.md` — Stable Provisional stamp
- `R4_Lock_P-Strong-Both.md` — governing package lock
- `R4_Locking_Scaffolding_Choice_Set.md` — ranked packages + relevance warnings
- `02e_Corrective_Closeout_Interparam_Dependency.md` — R1/R2 ↔ R4 dependency
- `02f_Phase2_Attempt2_P-Strong-Both.md` / `02g_Gate_Scoring_Phase2_Attempt2_Under_Package.md`
- `admitted_layers.md`, `notes.md`

### Failure-mode / tracker pointers (if any)

- No Application Thesis Tracker opened.
- Failure-mode log follow-up not required for this dissertation; Phase 1 negatives and package-adjacent lock are the durable method lessons on record inside the application folder.

---

*Generated under standing rule: Application Dissertation Deliverable. See `.cursor/rules/applications-gated-method.mdc`.*
