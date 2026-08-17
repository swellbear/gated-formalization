# Claim Graph

**Date:** 2026-08-17  
**Scope:** portfolio-wide + real-claim intakes (CoreWeave + Zitron Nvidia $500B + FOMC June 2026 SEP **hard stop**) + FL property-tax **hard stop** + FOMC Sep 2026 UFFR-change **hard stop** (`leave unnamed`) + oil-futures **hard stop (residuals live)**  
**Maintainer note:** Three claim-shape lock clusters Active (001–004 uniqueness+preferability; 005–008 numerical+should; 009–011 forecast-extension). Real-claim intakes: `APP-CRWV`, `APP-ZITRON`; synthetic twin scaling still saturated.

*Optional overview. Individual worksheets remain the source of truth.*

---

## Nodes

| Node ID | Type | Short label | Status / FD (if known) |
|---------|------|-------------|------------------------|
| APP-MWI | Application | `2026-08_many-worlds-unitarity-preferability` | Provisional closed; Amb ≈ 5.5 |
| APP-AV | Application | `2026-08_av-e2e-vs-modular-preferability` | Stable Provisional closed; Amb ≈ 4 |
| APP-GWT | Application | `2026-08_llm-global-workspace-consciousness` | Live remnant Provisional-stable; Amb ≈ 2.5 |
| APP-CDS | Application | `2026-08_cds-med-device-ad-segment-preferability` | Stable Provisional (proxy-scoped) |
| APP-MS | Application | `2026-08_microservices-alone-cascading-preferability` | Stable Provisional; Amb ≈ 8; FD 1 |
| APP-SVL | Application | `2026-08_serverless-alone-ops-preferability` | Stable Provisional; Amb ≈ 8; FD 1 |
| APP-GQL | Application | `2026-08_graphql-alone-overfetch-preferability` | Stable Provisional; Amb ≈ 8; FD 1 |
| APP-CASH | Application | `2026-08_cash-alone-privacy-preferability` | Stable Provisional; Amb ≈ 8; FD 1 (cross-domain) |
| APP-TERM | Application | `2026-08_term-limits-alone-accountability-preferability` | Stable Provisional; Amb ≈ 8; FD 1 (cross-domain #2) |
| APP-EFUND | Application | `2026-08_emergency-fund-6mo-should` | Stable Provisional; Amb ≈ 7; FD 1 |
| APP-NPS | Application | `2026-08_nps-50-should-expand` | Stable Provisional; Amb ≈ 7; FD 1 |
| APP-BRIDGE | Application | `2026-08_bridge-rating-should-close` | Stable Provisional; Amb ≈ 7; FD 1 (NS cross-domain) |
| APP-HEAT | Application | `2026-08_heatwave-next-summer-should-prepare` | Stable Provisional; Amb ≈ 7; FD 1 |
| APP-HOL | Application | `2026-08_holiday-sales-up-should-hire` | Stable Provisional; Amb ≈ 7; FD 1 |
| APP-CRWV | Application | `2026-08_coreweave-ceo-gpu-longer-life` | **Hard stop sealed**; A-ATTR L7; N-INSTANCE + color; F-LIFE fails C_SCOPE |
| APP-ZITRON | Application | `2026-08_zitron-nvidia-500b-financing-thesis` | **Hard stop sealed**; D-ANN+D-MOU; VF/CONC/SUSTAIN frozen not met; L8 Street FY; L9 MSFT OpenAI $24.1B; L10 capex scale + Cloud mix + non-lab presence; bubble not cleared; CR **keep original wording**; UX+CX executed (alts not adopted); Squawk OUT |
| APP-FOMC-SEP | Application | `2026-08_fomc-june-2026-sep` | **Hard stop sealed**; L1–L17; Amb ≈ 1; 2026 F-ML not established (L13 + L17 SPF); July 29 OUT; CR offered not run (keep original default); UX/CX offered not run |
| APP-FL-PTAX | Application | `2026-08_fl-property-tax-abolish-10y` | **Hard stop sealed**; Rank 1 + live official law; D-LAW admitted; Amb 2; P-BaseCase untested (`leave unnamed`); CR offered not run |
| APP-FOMC-UFFR | Application | `2026-08_fomc-sep-2026-uffr-change` | **Hard stop sealed**; Rank 3 `Q3+O2+L1+M3+B1`; Amb 2.5; P-NN-TEST **not established**; C2 `leave unnamed`; F-PRINT parked; CR offered not run |
| APP-OIL-FT | Application | `2026-08_oil-futures-predictive-model` | **Hard stop (residuals live)**; Rank 4 split; D-EXIST-MET-FT; **F-SRC-CME-TAPE**; Yahoo stand-in baseline; Amb 1.5; F-SKILL/V-VALUE not established; **R-F-SKILL** pursue; V-SRC leave unnamed; UX/CX/CR **declined** |
| LOCK-2026-08-001 | Lock | Comparison class before uniqueness (O) | Active |
| LOCK-2026-08-002 | Lock | Preferability needs named virtues/metrics | Active |
| LOCK-2026-08-003 | Lock | Amb drop / scope lock ≠ clearance | Active |
| LOCK-2026-08-004 | Lock | Hybrid/spectrum FD on “alone” | Active (broadened) |
| LOCK-2026-08-005 | Lock | Numerical bar freeze (C/H/legs) | Active |
| LOCK-2026-08-006 | Lock | Should not entailed by bar alone | Active |
| LOCK-2026-08-007 | Lock | Descriptive/bar ≠ elevation clearance | Active |
| LOCK-2026-08-008 | Lock | QI/scale-factor ≠ should proof | Active |
| LOCK-2026-08-009 | Lock | Forecast soft-modal + window freeze | Active |
| LOCK-2026-08-010 | Lock | Forecast Amb drop ≠ clearance | Active |
| LOCK-2026-08-011 | Lock | History ≠ forward should/potential | Active |

---

## Edges

| From | To | Relation | Notes |
|------|----|----------|-------|
| APP-MS | APP-AV | shares_anchor_class | engineering alone/preferability |
| APP-SVL | APP-MS | shares_anchor_class | batch |
| APP-GQL | APP-SVL | shares_anchor_class | batch |
| APP-CASH | APP-GQL | shares_anchor_class | alone⇒preferable shape (cross-domain) |
| APP-CASH | APP-CDS | shares_anchor_class | preferability metrics kinship |
| APP-MS | LOCK-2026-08-001 | imports_lock | |
| APP-MS | LOCK-2026-08-002 | imports_lock | |
| APP-MS | LOCK-2026-08-003 | imports_lock | |
| APP-MS | LOCK-2026-08-004 | imports_lock | |
| APP-SVL | LOCK-2026-08-001 | imports_lock | |
| APP-SVL | LOCK-2026-08-002 | imports_lock | |
| APP-SVL | LOCK-2026-08-003 | imports_lock | |
| APP-SVL | LOCK-2026-08-004 | imports_lock | |
| APP-GQL | LOCK-2026-08-001 | imports_lock | |
| APP-GQL | LOCK-2026-08-002 | imports_lock | |
| APP-GQL | LOCK-2026-08-003 | imports_lock | |
| APP-GQL | LOCK-2026-08-004 | imports_lock | |
| APP-CASH | LOCK-2026-08-001 | imports_lock | cross-domain clean |
| APP-CASH | LOCK-2026-08-002 | imports_lock | cross-domain clean |
| APP-CASH | LOCK-2026-08-003 | imports_lock | cross-domain clean |
| APP-CASH | LOCK-2026-08-004 | imports_lock | analogue then 004 folded |
| APP-TERM | LOCK-2026-08-001 | imports_lock | cross-domain #2 clean |
| APP-TERM | LOCK-2026-08-002 | imports_lock | |
| APP-TERM | LOCK-2026-08-003 | imports_lock | |
| APP-TERM | LOCK-2026-08-004 | imports_lock | Active broadened — clean |
| LOCK-2026-08-005 | APP-SIM | derived_from | sell-in-may / scorekept cluster |
| LOCK-2026-08-006 | APP-SIM | derived_from | sell-in-may / scorekept |
| LOCK-2026-08-007 | APP-SIM | derived_from | sell-in-may seasonality vs Sharpe |
| LOCK-2026-08-008 | APP-SIM | derived_from | debt QI |
| APP-EFUND | LOCK-2026-08-003 | imports_lock | |
| APP-EFUND | LOCK-2026-08-005 | imports_lock | |
| APP-EFUND | LOCK-2026-08-006 | imports_lock | |
| APP-EFUND | LOCK-2026-08-007 | imports_lock | |
| APP-EFUND | LOCK-2026-08-008 | imports_lock | |
| APP-NPS | LOCK-2026-08-003 | imports_lock | |
| APP-NPS | LOCK-2026-08-005 | imports_lock | |
| APP-NPS | LOCK-2026-08-006 | imports_lock | |
| APP-NPS | LOCK-2026-08-007 | imports_lock | |
| APP-NPS | LOCK-2026-08-008 | imports_lock | |
| APP-NPS | APP-EFUND | shares_anchor_class | numerical+should batch |
| APP-BRIDGE | LOCK-2026-08-005 | imports_lock | NS cross-domain |
| APP-BRIDGE | LOCK-2026-08-006 | imports_lock | |
| APP-BRIDGE | LOCK-2026-08-007 | imports_lock | |
| APP-HEAT | LOCK-2026-08-009 | imports_lock | forecast-extension |
| APP-HEAT | LOCK-2026-08-010 | imports_lock | |
| APP-HEAT | LOCK-2026-08-011 | imports_lock | |
| APP-HOL | LOCK-2026-08-009 | imports_lock | |
| APP-HOL | LOCK-2026-08-010 | imports_lock | |
| APP-HOL | LOCK-2026-08-011 | imports_lock | |
| APP-HOL | APP-HEAT | shares_anchor_class | forecast-extension batch |
| APP-CRWV | LOCK-2026-08-003 | imports_lock | real-claim; Amb≠clearance |
| APP-CRWV | LOCK-2026-08-009 | imports_lock | soft-modal + window |
| APP-CRWV | LOCK-2026-08-010 | imports_lock | forecast Amb≠clearance |
| APP-CRWV | LOCK-2026-08-011 | imports_lock | contract/history ≠ full elevation |
| APP-CRWV | APP-HEAT | shares_anchor_class | forecast-extension (process) |
| APP-CRWV | APP-HOL | shares_anchor_class | forecast-extension (process) |
| APP-ZITRON | LOCK-2026-08-003 | imports_lock | Amb≠clearance; VF-BAR freeze ≠ C-VENDOR clearance |
| APP-ZITRON | LOCK-2026-08-009 | imports_lock | soft evaluative / forward path |
| APP-ZITRON | LOCK-2026-08-010 | imports_lock | posed ≠ clearance |
| APP-ZITRON | LOCK-2026-08-011 | imports_lock | announcement/anecdote ≠ full elevation |
| APP-ZITRON | APP-CRWV | shares_anchor_class | markets Amb≠clearance process kinship (Zitron Squawk OUT under restart; CoreWeave still Squawk-primary) |
| APP-FOMC-SEP | LOCK-2026-08-003 | imports_lock | Amb≠clearance; census freeze ≠ forecast clearance |
| APP-FOMC-SEP | LOCK-2026-08-009 | imports_lock | most-likely / appropriate-policy soft-modal |
| APP-FOMC-SEP | LOCK-2026-08-010 | imports_lock | posed ≠ clearance |
| APP-FOMC-SEP | LOCK-2026-08-011 | imports_lock | printed SEP ≠ realized path / Committee vote |
| APP-FOMC-SEP | APP-ZITRON | shares_anchor_class | real-claim markets; claimed-table vs elevation |
| APP-FL-PTAX | LOCK-2026-08-003 | imports_lock | Amb≠clearance; question recorded ≠ answer established |
| APP-FL-PTAX | LOCK-2026-08-009 | imports_lock | likely + 10y window freeze (offered) |
| APP-FL-PTAX | LOCK-2026-08-010 | imports_lock | posed ≠ clearance |
| APP-FL-PTAX | LOCK-2026-08-011 | imports_lock | current-law census ≠ forward likely |
| APP-FL-PTAX | APP-HEAT | shares_anchor_class | “likely” + window (process; no should here) |
| APP-FL-PTAX | APP-FOMC-SEP | shares_anchor_class | forecast Amb≠clearance; named-class leftover after lock |
| APP-FOMC-UFFR | LOCK-2026-08-003 | imports_lock | Amb≠clearance; 33¢ print ≠ P-NonNegligible met; conflicted venue ≠ sole modal affirmation |
| APP-FOMC-UFFR | LOCK-2026-08-009 | imports_lock | forward window (Sep 15–16 2026 statement) |
| APP-FOMC-UFFR | LOCK-2026-08-010 | imports_lock | posed rules ≠ clearance |
| APP-FOMC-UFFR | LOCK-2026-08-011 | imports_lock | June SEP / prior statement ≠ Sep upper-bound change |
| APP-FOMC-UFFR | APP-FOMC-SEP | shares_anchor_class | FOMC process kinship; **different object** (UFFR change vs SEP inventory; funds-rate was off June F-ML) |
| APP-FOMC-UFFR | APP-FL-PTAX | shares_anchor_class | contract/question intake; unnamed class / wait-for-print |
| APP-OIL-FT | LOCK-2026-08-003 | imports_lock | Amb≠clearance; existence-met ≠ skill-met; leave-unnamed ≠ refute |
| APP-OIL-FT | LOCK-2026-08-009 | imports_lock | forecast soft-modal + named protocol (next-session CL log-return) |
| APP-OIL-FT | LOCK-2026-08-010 | imports_lock | lock / Amb drop ≠ clearance of skill, value, or blended slogan |
| APP-OIL-FT | LOCK-2026-08-011 | imports_lock | nearby spot/monthly prints ≠ next-session CL skill |
| APP-OIL-FT | APP-FOMC-UFFR | shares_anchor_class | leave unnamed ≠ refute (process; different object) |
| APP-OIL-FT | APP-SIM | shares_anchor_class | costs before a value bar (process; V-EITHER unused here) |

---

## Residual judgment / known missing edges

- Cross-domain probe succeeded for 001–003; LOCK-004 folded Active for hybrid/spectrum domains.  
- Real-claim `APP-CRWV` validates forecast locks on live markets commentary; attribution≠life clearance.  
- Real-claim `APP-ZITRON` hard-stopped under newsletter+monologue primary (Squawk OUT); MoU≠vendor/circular/70%/bubble clearance; claimed citations ≠ bar met; CR **keep original wording**; UX+CX executed (alts not adopted).  
- Real-claim `APP-FOMC-SEP` **hard stop sealed** (2026 F-ML test **not established** after L13 brochure + L17 SPF Q2 2026; Amb ≈ 1; G8 not locked); July 29 OUT; CR/UX/CX offered not run; default keep original wording; print-match ≠ clearance.  
- `APP-OIL-FT` **hard stop (residuals live)** (2026-08-17): Rank 4 nested split; D-EXIST-MET-FT (futures-target only); Yahoo `CL=F` stand-in baseline scored; F-SKILL/V-VALUE not established; Amb 1.5; Amb ≠ clearance; Phase 2 not entered; UX/CX/CR **declined**.

---

## Ready for next step?

- [x] Update after new application  
- [x] Update after new lock  
- [ ] Freeze  
- [ ] Archive  
