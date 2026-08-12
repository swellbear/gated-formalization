# Machine JSON Block

**Purpose:** When an external tool needs a machine-readable summary of an application’s current status, emit this JSON block. Optional only — never replaces the human worksheets or residual judgment.

---

## Schema (`schema_version`: `"1.0"`)

```json
{
  "application_id": "string",
  "date": "YYYY-MM-DD",
  "claim_type": "Descriptive | Normative-Strategic | Mixed",
  "overall_verdict": "Admissible | Provisional | Not admissible",
  "amb_weighted_sum": 0,
  "amb_band": "low | provisional_borderline | high",
  "fd_score": 0,
  "fd_band": "low_formalization | borderline | moderately_constrained | well_constrained",
  "prod": "0 | 1 | 2+",
  "cons": "pass | soft_tension | fail",
  "agree": "pass | low | fail",
  "higher_level": "pass | pass_with_caution | fail",
  "remaining_free_parameters_count": 0,
  "time_triggered_residuals": 0,
  "lock_ids_used": [],
  "worksheet_pointers": {
    "anchors": "string",
    "gate_scoring": "string",
    "gaps": "string",
    "fd_index": "string",
    "other": []
  },
  "residual_judgment_note": "string",
  "schema_version": "1.0"
}
```

**Field notes (stable):**  
- `amb_band`: `low` (≤2), `provisional_borderline` (3–5), `high` (≥6).  
- `fd_score` / `fd_band`: from `templates/07_FD_Index.md` when computed; omit or null only if FD was not run.  
- `time_triggered_residuals`: count of open time-triggered residuals (`0` if none).  
- `lock_ids_used`: imported Lock Library IDs (empty array if none).

---

## Worked example (Cycle 0)

Source: `applications/2026-08_many-worlds-unitarity-preferability` — Cycle 0 gate sheet (2026-08-11). Amb = 12 binding; Provisional. FD via §11 heuristic: Amb≥6 base 2; Prod 2+ (+1); Cons soft tension (−1); Agree low (−0.5); higher-level caution (−0.5) → **FD = 1**.

```json
{
  "application_id": "2026-08_many-worlds-unitarity-preferability",
  "date": "2026-08-11",
  "claim_type": "Mixed",
  "overall_verdict": "Provisional",
  "amb_weighted_sum": 12,
  "amb_band": "high",
  "fd_score": 1,
  "fd_band": "low_formalization",
  "prod": "2+",
  "cons": "soft_tension",
  "agree": "low",
  "higher_level": "pass_with_caution",
  "remaining_free_parameters_count": 7,
  "time_triggered_residuals": 0,
  "lock_ids_used": [],
  "worksheet_pointers": {
    "anchors": "01_Anchor_and_ClaimType_Template.md",
    "gate_scoring": "02_Gate_Scoring_Sheet.md",
    "gaps": "03_Gap_Extraction_and_Ranking.md",
    "fd_index": null,
    "other": [
      "05_Calibration_and_Rule_Diff.md"
    ]
  },
  "residual_judgment_note": "Amb binding on uniqueness (O) and preferability (P); descriptive extras nearer L0; soft Cons on postulate-counting / only⇒preferable; no expansion of full claim.",
  "schema_version": "1.0"
}
```

---

## Usage notes

- Emit only when an external consumer needs a machine-readable status snapshot.
- The block is a **summary heuristic** of current gate posture — not evidence, not clearance, not a ranking of truth.
- Residual judgment, free-parameter detail, and admission rationale stay in the human worksheets.
- Keep `schema_version` stable; change fields rarely and bump the version when you do.
- Re-emit after a meaningful gate re-score or status change; do not treat stale JSON as live truth.
