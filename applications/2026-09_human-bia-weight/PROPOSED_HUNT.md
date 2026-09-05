# Step-1 hunt — public human BIA + weight (PROPOSED; Operator/Founder-gated)

**Date:** 2026-09-05  
**Application:** `2026-09_human-bia-weight`  
**String:** step-1 data hunt  
**Named gap:** public row-level human BIA + weight under reusable public terms  
**Ledger:** [`NAMED_GAP_LEDGER.md`](NAMED_GAP_LEDGER.md)

Lab invents ranked hunt probes. Lab does **not** self-admit. Lab scratch was **not** on this fold VM. Record below is the gated fact set copied from the Operator + Founder gate (honest hunt; primary SUCCEED; Soften secondaries logged, not substitutes).

**What this is not:** A trained BIA→weight map. Training established. Skill-met. Livestock transfer. Farm / commercial weighing solved. Rithm. Soften secondaries as the succeed table.

---

## 0. Plain-language framing

**What this is:** Lab hunted for a public, row-level human table that pairs bioimpedance (R / Xc / Z / phase angle **or** BIA device features) with body weight (or mass) under reusable public terms suitable to train/evaluate. Operator + Founder gated.

**What this settles:** The named Step-1 gap **SUCCEED**s. Primary corpus is NHANES 1999–2004 **BIX↔BMX** (CDC public-use XPT) under the NCHS Data User Agreement. Operator confirmed: no explicit ban on ML train/eval; intended cheap sklearn holdout framed as statistical analysis → **Succeed, not Soften**.

**What this is not:** Not a trained map. Not training established. Not skill-met. Not livestock transfer. Not farm livestock continuous-weighing solved (that Amb stays **separate**). Not commercial / farm weighing solved. Not rithm. Not a reopen of poultry #47, cattle #49, sheep #51, or companion #53. Soften secondaries are **logged, not substitutes**.

---

## 1. Lab hunt (copied from the gate)

**Target:** public, row-level **human** BIA + paired body weight, under **reusable public terms**.

**Result (gated):** **SUCCEED** on the primary corpus.

| Slice | Result |
|-------|--------|
| Primary: NHANES 1999–2004 BIX↔BMX | **SUCCEED** — public-use XPT; SEQN join; raw R/Xc + weight; usable n |
| Soften secondaries | **logged, not substitutes** — PhysioNet QDE; Senegal Zenodo Z50+Wt; BIAID / UK Biobank / BIAdata |
| Training / holdout invent | **gated after this hunt** — S1 HARDEN / S2 Soften / S3 HOLD; see [`SCORE_S1_PROPOSED.md`](SCORE_S1_PROPOSED.md) |

Soften secondaries below are **docs only**. They do **not** replace the NHANES succeed table.

---

## 2. Primary corpus (SUCCEED)

| Field | Gated record |
|-------|----------------|
| Corpus | NHANES 1999–2004 **BIX↔BMX** (CDC public-use XPT) |
| Docs (example) | [BIX_C 2003–2004 codebook](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2003/DataFiles/BIX_C.htm) |
| Schema | **SEQN** join; **BIXS\*** resistance + **BIXC\*** reactance (**50** frequencies, 5 kHz–1 MHz) + **BMXWT** (+ **BMXHT** / **BMXBMI**) |
| Proven join n | **4278** — `BIX_C ∩ BMX_C` non-missing `BIXS050K` + `BIXC050K` + `BMXWT` |
| Stacked 1999–2004 | **~13221** |
| License | [NCHS Data User Agreement](https://www.cdc.gov/nchs/policy/data-user-agreement.html) — statistical reporting / analysis only; **no re-identification**. **Not CC-BY.** |

**DUA caveats (required on the record):**

- Use is **statistical reporting and analysis only**.
- **No** attempt to learn the identity of any person or establishment.
- **Not** CC-BY.
- Operator confirmed: **no explicit ban** on ML train/eval.
- Intended next use was a **cheap sklearn holdout** framed as statistical analysis → **Succeed, not Soften**. That holdout is now gated ([`SCORE_S1_PROPOSED.md`](SCORE_S1_PROPOSED.md)).

This fold does **not** download, join, or train on the XPT files.

---

## 3. Soften secondaries (logged, not substitutes)

| # | Named in the gate | What it is | Gate |
|---|-------------------|------------|------|
| 1 | PhysioNet QDE | Tiny public Z @ 1 MHz + weight change (dehydration task). [physionet.org/content/qde/1.0.0](https://www.physionet.org/content/qde/1.0.0/) · [DOI 10.13026/c23082](https://doi.org/10.13026/c23082) | **Soften secondary** — not the succeed table |
| 2 | Senegal Zenodo Z50+Wt CC0 | Public Z50 + weight, CC0 | **Soften secondary** — not the succeed table |
| 3 | BIAID / UK Biobank / BIAdata | Human BIA corpora | **Access-walled** — Soften (walls), not succeed |

These do **not** substitute for NHANES BIX↔BMX. They do **not** reopen livestock parks.

---

## 4. Operator + Founder gate (authoritative)

**ADMIT SUCCEED** Step-1 named gap: public row-level human BIA + weight under reusable public terms.

Primary corpus: NHANES 1999–2004 BIX↔BMX (CDC public-use XPT). Schema, proven join n, stacked n, and DUA as above. Operator confirmed: no explicit ban on ML train/eval; intended cheap sklearn holdout framed as statistical analysis → **Succeed, not Soften**.

Soften secondaries are **logged, not substitutes**.

**Scope lock:** method practice only. Animal parks (poultry / cattle / sheep / companion) stay. **No livestock transfer claim.**

**Hard NO / not yet**

- Training is **not** established. Do **not** start training docs as established.
- This is **not** skill-met beyond the Step-1 data gap.
- Livestock transfer is **not** claimed.
- Farm livestock continuous-weighing stays a **separate** Amb.
- Farm / commercial weighing is **not** solved.
- Do **not** invent rows.
- Poultry #47, cattle #49, sheep #51, and companion #53 stay **parked**. This hunt does **not** reopen them.

**Next string (after the hunt fold):** invent → test a cheap sklearn holdout vs **mean** and **height-only** baselines. That string **ran**. Operator **ADMIT S1 HARDEN**; S2 Soften/park; S3 HOLD/park. Metrics: [`SCORE_S1_PROPOSED.md`](SCORE_S1_PROPOSED.md). Digestion: [`DIGESTION_S1_HOLDOUT.md`](DIGESTION_S1_HOLDOUT.md).

---

## 5. Unchanged strings

- Poultry BIA→weight step-1 remains **parked** (#47 DATA-BLOCKED).
- Cattle BIA→weight step-1 remains **parked** (#49 DATA-BLOCKED).
- Sheep BIA→weight step-1 remains **parked** (#51 DATA-BLOCKED).
- Companion BIA→weight remains **parked** (#53 Soften n=13 + training-scale DATA-BLOCKED).
- Farm livestock continuous-weighing remains a **separate** Amb.
- Collatz playground remains **done** (#45). Lab HOLD there.
- Track B invent remains **paused**.
- llm-gwt R-REPL remains **parked**.

---

*Docs only. SUCCEED is the Step-1 data gap only. DUA ≠ CC-BY. Soften secondary ≠ substitute. Not a trained map. Not skill-met. Not livestock transfer. Not commercial weighing. Not rithm. Lab does not self-admit.*
