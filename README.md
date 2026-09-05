# Gated Progressive Formalization — Operator Toolkit

A disciplined method for converting messy conceptual material (informal theories, advocacy arguments, metaphors, design rationales, etc.) into better-constrained models.

**New here? Start with the [Plain-Language Overview](docs/PLAIN_LANGUAGE_OVERVIEW.md), [Glossary](docs/GLOSSARY.md), and [First Run Guide](docs/FIRST_RUN_GUIDE.md).** Accessibility is standard practice.

This repository is an **operator toolkit**: documentation + reusable worksheets + application logs. Live decisions use an **in-chat clickable picker** (a click is the reply). Residual evaluative judgment remains essential and is kept explicit.

## Quick Start — Running a New Application

1. Copy `applications/_template_application/` to a new folder named `YYYY-MM_short-name/`.
2. **Canonical method rules:** `.cursor/rules/applications-gated-method.mdc` (sole full standing-rule text). Checklist: `workflow.md`.
3. Fill worksheets in order (`templates/`):
   - `01_Anchor_and_ClaimType_Template.md`
   - `02_Gate_Scoring_Sheet.md`
   - (If Amb is high) `03_Gap_Extraction_and_Ranking.md`
   - (For each candidate material) `04_Material_Admission_Check.md`
   - (No-admit cycles) `Compact_No_Admit_Readout.md`
   - (Dominant blocker) `R_Locking_Scaffolding.md`
   - (Package evidence) `E_Package_Evidence_Intake.md`
   - (Closeout) `05_Original_Claim_Assessment.md`
4. Re-score after incorporation; use **compact no-admit** when Amb is unchanged.
5. Record final verdict + Original-Claim Assessment; log failure modes in `logs/failure_mode_log.md`.

See `workflow.md` for the operator checklist.

Before a brand-new claim, write up what the last one taught you: [`docs/DIGESTION_HABIT.md`](docs/DIGESTION_HABIT.md).

## Repository Structure

```
docs/               Core method + operational upgrade (living markdown + archival PDFs)
templates/          Blank worksheets (core cycle + optional toolbox)
ui/                 Optional catalog demo for choice wording (`catalog.json`); not the live decision UI
exemplars/          Classical sound-argument starters (to be expanded)
applications/       One folder per live run + a copyable template
locks/              Lock Library entries (filled from templates/08_…; often empty early)
logs/               Failure-mode log
TRACKER_*.md        Portfolio / residual / pattern / claim-graph trackers (repo root)
.cursor/rules/      Canonical standing rule (applications-gated-method.mdc)
workflow.md         Operator checklist (pointer + steps; not a second full rule copy)
README.md           This file
```

## Core Idea (one paragraph)

Start from hard-to-dispute anchors. Admit new formal layers only when they pass explicit gates (Consistency, Agreement, Productivity, bounded Ambiguity) plus higher-level review. When a gate fails—especially Ambiguity—extract the specific free parameters, search for material that constrains them, admit only material that clears a relevance + consistency check, then re-score. High residual Ambiguity after serious search means the claim remains provisional / under-determined, **not** that it has been proven false. The method surfaces shortcomings and turns them into a research agenda; it does not eliminate judgment or guarantee objective truth.

## Key Documents

- `.cursor/rules/applications-gated-method.mdc` — canonical standing rule
- `docs/00_method_overview.md` — living core method
- `docs/01_operational_upgrade.md` — sharpened gates, claim-type, checklists, calibration, optional toolbox (§§9–14)
- `workflow.md` — operator checklist (pointer to optional toolbox in Reminders)
- `docs/DIGESTION_HABIT.md` — before a brand-new claim, write up what the last one taught you (habit, not a scoring rule)
- `ui/choice-presenter/catalog.json` — wording catalog for in-chat choices (HTML/canvas demo is optional; does not score)
- `TRACKER_CLAIM_GRAPH.md` — portfolio claim-graph instance (optional overview)
- `docs/thesis_final.pdf` — archival frozen Complete Thesis (vFinal consolidated working paper)
- `docs/operational_upgrade.pdf` — archival frozen operational upgrade
- `docs/PROBABILITY_OBJECT_PILOT.md` — probability-object **pilot** (**not canon**; not standing rule)

## Status

Method is operational. Live applications include computational sketch of conscience, opinion-article run, Many-Worlds preferability, and AV E2E-vs-modular preferability. Further applications should use current worksheets and contribute calibration + failure-mode data.

## License / Use

Working methodological toolkit. Use, adapt, and log results. Residual judgment remains the responsibility of the operator.
