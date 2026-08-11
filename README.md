# Gated Progressive Formalization — Operator Toolkit

A disciplined method for converting messy conceptual material (informal theories, advocacy arguments, metaphors, design rationales, etc.) into better-constrained models.

This repository is an **operator toolkit**: documentation + reusable worksheets + application logs. It is not yet software. Residual evaluative judgment remains essential and is kept explicit.

## Quick Start — Running a New Application

1. Copy `applications/_template_application/` to a new folder named `YYYY-MM_short-name/`.
2. Fill the worksheets in order:
   - `01_Anchor_and_ClaimType_Template.md`
   - `02_Gate_Scoring_Sheet.md`
   - (If Amb is high) `03_Gap_Extraction_and_Ranking.md`
   - (For each candidate material) `04_Material_Admission_Check.md`
3. Re-score after any incorporation of new material.
4. Record the final verdict and any residual judgment notes.
5. If the run reveals a failure mode (blocked something later supported, or allowed something later collapsed), add an entry to `logs/failure_mode_log.md`.

See `workflow.md` for the full repeatable checklist.

## Repository Structure

```
docs/               Core method + operational upgrade (living markdown + archival PDFs)
templates/          Blank worksheets
exemplars/          Classical sound-argument starters (to be expanded)
applications/       One folder per live run + a copyable template
logs/               Failure-mode log
workflow.md         Step-by-step operator checklist
README.md           This file
```

## Core Idea (one paragraph)

Start from hard-to-dispute anchors. Admit new formal layers only when they pass explicit gates (Consistency, Agreement, Productivity, bounded Ambiguity) plus higher-level review. When a gate fails—especially Ambiguity—extract the specific free parameters, search for material that constrains them, admit only material that clears a relevance + consistency check, then re-score. High residual Ambiguity after serious search means the claim remains provisional / under-determined, **not** that it has been proven false. The method surfaces shortcomings and turns them into a research agenda; it does not eliminate judgment or guarantee objective truth.

## Key Documents

- `docs/00_method_overview.md` — living core method
- `docs/01_operational_upgrade.md` — sharpened gates, claim-type pre-classification, checklists, calibration
- `docs/thesis_final.pdf` — archival frozen Complete Thesis (vFinal consolidated working paper)
- `docs/operational_upgrade.pdf` — archival frozen operational upgrade

## Status

Method is operational. Two live applications have been completed (computational sketch of conscience; opinion article on democratic socialism). Templates and scoring rules were upgraded after those runs. Further applications should use the current worksheets and contribute calibration + failure-mode data.

## License / Use

Working methodological toolkit. Use, adapt, and log results. Residual judgment remains the responsibility of the operator.
