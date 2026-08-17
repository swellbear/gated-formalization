# Package-Satisfying Evidence Intake — named CME tape pulse

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Locked package / scope label:** **Under Rank 4 + L-SESS + F-SRC-CME-TAPE**  
**Target dependent(s):** F-SKILL / F-ON / F-DAY / F-CC  
**Named-class pulse?** **Yes**

---

## 0. Named-class pulse

| Check | Value |
|-------|--------|
| Freeze line (quoted) | F-CC = Rank 4 F-SKILL; F-ON / F-DAY per L-SESS; RMSE vs no-change; walk-forward |
| Named source class | CME NYMEX CL front-month official daily **open** and **settlement**, roll rule **R1**; baseline 0-forecast RMSE on three windows; optional Kearney–Shang FTS re-score on the same tape |
| Named enough? | **Yes** (public exchange stamps + matching locks). Tape **not obtained** this pulse. |
| Non-circular? | Yes — not the Rank 4 brochure; no-change is the **baseline**, not the D-EXIST model |
| Schema match | **Yes** for the class definition. **No computed sample** (live tape absent) |
| Conflicted-source flag completed (§2)? | Yes |
| **Establishment-stop drill:** Would honest `04` declare **established**? | **No.** |

Do **not** invent a stand-in. Do **not** treat Kearney–Shang 2020 MAE as this pulse.

---

## 1. Lock schema

| Slot | Required | This artifact |
|------|----------|---------------|
| Object | NYMEX CL front-month | Named CME CL. Not in hand |
| Horizon | F-ON / F-DAY / F-CC | Named. Not computed |
| Metric | RMSE vs 0 | Named. Not computed |
| Protocol | Walk-forward / pre-declared holdout | Declared (last 500 + 250/750). Not executed |
| Baseline | No-change | The object of the baseline decomposition |
| Optional FTS | Kearney–Shang on same tape | **Not run** (no CL1–CL18 official curve) |

**Schema match?** Class **yes**. Numeric skill **not scored**.

---

## 2. Artifact summary

**Source / citation:** Operator-named class 2026-08-17; CME DataMine is the live vendor of official settlements; fetch log in `PULSE_Baseline_Session_RMSE.md`.

**What it reports:** Live official open/settle history **not obtained**. Stand-in **not used**. Optional FTS **not run**. Skill bars **not established**.

### Conflicted-source flag (mandatory)
- [x] **Non-conflicted** — exchange official stamps are the intended live series  
- [ ] **Conflicted / interest-aligned** — n/a this pulse (no vendor backtest scored)

### Quantitative bar?
Yes vs F-ON/F-DAY/F-CC. Rubric: `E_Quantitative_Evidence_Rubric_FSRC_Named.md`. Result: **not establish** (no sample).

---

## 3. Provisional gate intent

- [x] Aim **ADMIT** F-SRC-CME-TAPE (named vehicle) + L-PULSE-TAPE-0 (pulse executed, bars not met)  
- [ ] Aim **ADMIT** F-SKILL established — **rejected**  
- [x] Aim **REJECT** scoring Yahoo/`CL=F` as live  

---

## 4. Scoped-result honesty

Hold **under:** Rank 4 + L-SESS + this named class.  
**Must not be promoted to:** F-SKILL-met; “daytime is easier”; a trade; Kearney–Shang-met.

---

## 5. Next

Stop for **live vs stand-in**: provide CME official tape **or** `stipulate stand-in …`. Do not invent. Combo still parked. No Phase 2.

---

*Standing rule: Package-satisfying evidence intake. Print-match ≠ clearance.*
