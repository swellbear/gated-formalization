# Operational Upgrade — Sharpened Rules & Tools (Living Version)

*Living markdown version of the operational improvements. Use these rules and the templates/ worksheets for all new applications.*

## 1. Claim-Type Pre-Classification (Required)

Before scoring gates, flag every major claim or layer element as:

- **Descriptive** (factual, causal, structural)
- **Normative / Strategic** (value, advocacy, prescription, framing recommendation)
- **Mixed** (split into parts)

Record the flag. Descriptive claims are held to tighter factual constraint; normative/strategic claims are expected to carry higher residual Amb unless tightly linked to constrained descriptive premises.

## 2. Sharper Amb (Ambiguity / Under-determination)

**Counting rule**  
A free parameter is any of:
- (a) an unspecified functional form or quantitative weight that materially affects predictions
- (b) an alternative reading of a key term or causal link still equally compatible with all current anchors and admitted material
- (c) a scope or boundary condition left open that changes the claim’s implications

Count each distinct free parameter once.

**Severity weighting**
- High-severity (changes core prediction or classification) → weight **2**
- Medium-severity (changes secondary predictions or scope) → weight **1**
- Low-severity (stylistic or peripheral) → weight **0.5**

**Interpretation bands (guidance)**
- Weighted sum ≤ 2 → generally low enough for admission (if other gates pass)
- Sum 3–5 → provisional / borderline
- Sum ≥ 6 → high Amb — block expansion of the formal layer

## 3. Sharper Prod (Productivity) — secondary gate

A consequence counts only if it is:
1. New relative to anchors and prior layers
2. Non-trivial (not a near-paraphrase)
3. Checkable in principle against observation, data, or further constrained inference

**Scoring**
- 0 productive consequences → fails Prod
- 1 → minimum pass
- 2+ independent productive consequences → strong Prod

**Needle rule:** Do not invent Prod by restating the claim, listing hoped-for implications, or counting consequences that presuppose still-open free parameters.

**Agree (secondary):** Change Agree only when independent careful readings (or distinct careful passes) actually converge or diverge on the *same* constrained claim. Do not treat rhetorical fluency or single-pass confidence as Agree.

**Primary vs secondary:** Cons, Amb, and redefinition / meaning-shift checks carry the run. Agree and Prod are scored but secondary.

## 3b. Claim-freeze

At Phase 1 endpoint (and before Phase 2 or Experimental Generation on a gap), lock each open free parameter in **one sentence** stating what the parameter *is*. Candidates that claim to close a gap must **quote** that sentence. Changing the freeze line is a claim change, not Amb reduction.

## 3c. Intractability checklist

Before declaring a gap currently intractable, record: literature/source classes searched; candidate classes tried; recurring failure pattern named; what would reopen the gap.

## 4. Scored Gap-Ranking Checklist

For each gap score 0–2 on:
- **Impact** — how many other free parameters or core predictions a constraint would affect
- **Anchor connection** — directness of link to existing anchors
- **Measurability** — feasibility of finding constraining material

Sum the three scores. Attack highest-sum gaps first. Record scores. This reduces arbitrariness; it does not prove “most important.”

## 5. Classical Sound-Argument Exemplars (Guidance)

Build domain-specific exemplar sets from arguments that historically closed important free parameters. For each exemplar record: the prior free parameter, the constraining material, and the resulting Amb reduction. Use only to condition relevance judgment — never as automatic proof.

Starter categories used so far: developmental constraints on innate vs learned contributions; public-record / administrative-procedure constraints; electoral-geography constraints on claims of national political capture.

## 6. Calibration Notes from Existing Runs

**Conscience sketch**
- Moving G from open vector to three named components produced a clear reduction in Amb and was correctly treated as progress without full clearance.
- Amb remained the binding gate. Illustrative thresholds (τ_c ≈ 0.95, τ_a ≈ 0.80) felt usable.

**News-article application (democratic socialism opinion piece)**
- Pre-classifying claims as descriptive vs normative/strategic would have made Cons and Amb scoring cleaner.
- Two search cycles reduced Amb on factual sub-claims (electoral geography, database scale, platform content) while correctly leaving stronger interpretive claims provisional.
- Supports treating “provisional after serious search” as a stable, honest status.

## 7. Failure-Mode Log Structure

```
Date | Domain | Claim/layer summary | Gate outcome | Later evidence
| Direction of error (blocked-but-later-supported / allowed-but-later-collapsed)
| Notes on which rule or judgment contributed | Adjustment made (if any)
```

Populate whenever a run later reveals mis-calibration.

## 8. Templates

**Core cycle** (copy into each new application folder as needed):
- `01_Anchor_and_ClaimType_Template.md`
- `02_Gate_Scoring_Sheet.md`
- `03_Gap_Extraction_and_Ranking.md`
- `04_Material_Admission_Check.md`
- `05_Original_Claim_Assessment.md` (closeout)

**Optional toolbox** (instance-triggered; never mandatory for every run — see §§9–14):
- `05_Calibration_and_Rule_Diff.md` (learning loop)
- `06_Time_Triggered_Residual.md`
- `07_FD_Index.md`
- `08_Lock_Library_Entry.md`
- `09_Machine_JSON_Block.md` (schema + example; usually not copied per app)
- `10_Claim_Graph.md`

**Note on `05_`:** Two different worksheets share the `05_` prefix — `05_Original_Claim_Assessment.md` (closeout) and `05_Calibration_and_Rule_Diff.md` (post-run learning). Do not conflate them; rename later only if confusion persists across more runs.

## 9. Calibration & Rule Diff (Learning Loop)

After one or more application runs, the operator converts observations and any failure-mode entries into an explicit, versioned **rule diff**. The diff is a learning signal only; it is **never** applied automatically. Use the worksheet `templates/05_Calibration_and_Rule_Diff.md`.

Minimal process:

1. Fill the header (date, cycle ID, applications reviewed, failure-mode entries considered).
2. Record observed frictions/surprises and what worked cleanly.
3. Write concrete “Change X to Y because Z” or “No change …” proposals — only for rules that actually surfaced.
4. Later, fill the Operator decision log (Accept / Modify / Reject).
5. Only after decisions are recorded, fold accepted changes into this living document (or hold / discard).

**Constraints:** Do not invent speculative improvements. Residual judgment about whether a friction is real enough to change a rule remains explicit and is recorded in the decision log.

## 10. Time-Triggered Residuals

Record free parameters that keep a claim provisional because they can only be constrained by future data or observation. Worksheet: `templates/06_Time_Triggered_Residual.md`. Instance-triggered only — never mandatory. Especially natural for market residuals, experimental outcomes still in progress, longitudinal results, and similar future-data gaps. When constraining material arrives, it must still pass the normal Material Admission Check (`templates/04_Material_Admission_Check.md`) before any re-scoring.

## 11. Formalization Degree (FD) Index

A lightweight, comparable index of how constrained / formalized a claim currently is, derived from existing gate scores. Worksheet: `templates/07_FD_Index.md`. Optional summary heuristic only — never replaces the full gate scoring sheet; residual judgment stays explicit (including required override space on the worksheet). Useful for portfolio overview and tracking progress across cycles.

## 12. Lock Library

Record tightly constrained free parameters or admitted layers stable enough to reuse as starting constraints in related future applications. Entry template: `templates/08_Lock_Library_Entry.md`. Store each filled entry as `locks/LOCK-YYYY-MM-NNN.md` (one file per lock). Locks are created only after residual judgment decides something is lock-worthy — never automatic. The library becomes useful only after repeated locks accumulate; early applications may have zero entries. Importing a lock into a new application still requires ordinary consistency checking with that application’s anchors.

## 13. Machine JSON Block

Emit an optional machine-readable status summary when an external consumer needs one. Schema and worked example: `templates/09_Machine_JSON_Block.md`. Optional only — use only when an external tool requires it. Summary heuristic; never replaces residual judgment or the full human worksheets.

## 14. Claim Graph

Maintain a lightweight graph of dependencies among applications, locks, shared anchors, or prior layers when portfolio lineage becomes hard to track by hand. Worksheet: `templates/10_Claim_Graph.md`. Live portfolio instance: `TRACKER_CLAIM_GRAPH.md` (repo root, with the other `TRACKER_*` files). Optional — most single applications never need it. Individual application worksheets remain the source of truth; the graph is a secondary overview. Residual judgment about which dependencies matter stays explicit.

---
*This upgrade implements the highest-leverage improvements identified after the first two live applications. New runs should follow these rules and contribute further calibration data.*
