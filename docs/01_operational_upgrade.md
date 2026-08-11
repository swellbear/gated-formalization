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

## 3. Sharper Prod (Productivity)

A consequence counts only if it is:
1. New relative to anchors and prior layers
2. Non-trivial (not a near-paraphrase)
3. Checkable in principle against observation, data, or further constrained inference

**Scoring**
- 0 productive consequences → fails Prod
- 1 → minimum pass
- 2+ independent productive consequences → strong Prod

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

Use the four worksheets in `/templates`:
- `01_Anchor_and_ClaimType_Template.md`
- `02_Gate_Scoring_Sheet.md`
- `03_Gap_Extraction_and_Ranking.md`
- `04_Material_Admission_Check.md`

Copy them into each new application folder.

---
*This upgrade implements the highest-leverage improvements identified after the first two live applications. New runs should follow these rules and contribute further calibration data.*
