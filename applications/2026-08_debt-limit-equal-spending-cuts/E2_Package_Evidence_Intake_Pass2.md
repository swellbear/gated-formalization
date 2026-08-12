# Package-Satisfying Evidence Intake — Pass 2

**Date:** 2026-08-11  
**Application:** `2026-08_debt-limit-equal-spending-cuts`  
**Locked package / scope label:** **Under P-Score-Strict+R2 only**  
**Target:** Empirical/historical instance of debt-limit action paired with official scored spending reductions  

---

## Artifact C — Fiscal Responsibility Act of 2023 (P.L. 118-5 / H.R. 3746)

### 1. Lock schema match
| Slot | Required | In artifact |
|------|----------|-------------|
| E2 | Official score | **Yes** — CBO letter (May 30, 2023) on H.R. 3746 |
| S2 | Disc. + mandatory | **Partial** — savings dominated by discretionary caps; mandatory ~$10B net |
| S3 | Exclude net interest from balance test | **Usable** — CBO separates ~$1.3T discretionary outlay cuts vs ~$188B interest; non-interest path identifiable |
| S6 | Anti-gimmick | **Partial / tension** — statutory caps with **exceptions** (disaster, etc.); later-year “caps” partly point-of-order only |
| B1 | Current-law baseline | **Yes** — relative to CBO May 2023 baseline |
| R2 | Borrowing headroom from suspension | **Not cleanly met** — FRA **suspends** limit through Jan 1, 2025 then resets; CBO does **not** publish a single R2 “headroom dollars that cuts must equal” matched to the Steube-style test. Scored deficit reduction (~$1.5T with interest) is **not** the same quantity as suspension headroom. |
| X1 | No exceptions | **No** — cap exceptions and political compromise structure |

**Schema match?** **Partial** — strong on E2/B1 and non-interest discretionary scoring; **fails** clean R2 equality test and X1/S2 fullness.

### 2. Artifact summary
**Sources:** CBO letter on H.R. 3746; CBO pub. 59260; public FRA summaries.  
**Reports:** Debt-limit suspension paired with discretionary funding caps; CBO: ~$1.5T lower deficits over 2023–2033 vs May baseline if caps bind; ~$1.3T lower discretionary outlays; small mandatory/revenue effects; interest savings separate.  
**Limits:** Not designed as Steube dollar-for-dollar headroom match; headroom during suspension not scored as R2 target here.

### 3. Gate intent
- [ ] ADMIT as full P-Score-Strict+R2 pass/fail instance  
- [x] **HOLD** / narrow historical analogue only  
- [ ] REJECT entirely  

**ADMIT bar (full instance):** Explicit R2 headroom figure + non-interest disc+mandatory cuts ≥ headroom under B1/S6/X1 — **not met**.  
**HOLD bar:** Documented CBO-scored pairing of limit suspension with large discretionary savings — **met**.

### 4. Scoped honesty
**Under P-Score-Strict+R2** as **analogue only**.  
**Must not promote to:** Proof original claim; proof FRA “balances” under R2; clearance of FD1–FD5.

---

## Artifact D — Budget Control Act of 2011 (P.L. 112-25)

### 1. Lock schema match
| Slot | In artifact |
|------|-------------|
| E2 | **Yes** — CBO estimates of BCA |
| S2 | **Partial** — mainly discretionary caps + later sequester affecting defense/nondefense/Medicare |
| S3 | **Tension** — headline “at least $2.1T” often **includes** debt-service; non-interest split exists in CRS/CBO breakdowns but political “match” used totals with interest |
| S6 | **Partial** — complex triggers, joint committee failure → sequester |
| B1 | **Yes** — CBO baselines (with noted baseline variants) |
| R2 | **Partial / different metric** — staged debt-limit **increases** (~$2.1–$2.4T cumulative), not suspension headroom; savings target set to rough parity with increase **including** interest in headline framing |
| X1 | **No** — multi-step procedures, disapproval paths, automatic mechanisms |

**Schema match?** **Partial** — famous “pair limit with deficit reduction” precedent; **not** a clean P-Score-Strict+R2 (R2 headroom, S3, X1) instance.

### 2. Summary
**Sources:** CBO BCA analyses; CRS R42013.  
**Reports:** Debt-limit increase mechanism paired with discretionary caps and ≥$1.2T joint-committee/sequester deficit reduction; CBO ~$917B (pre-committee) + ≥$1.2T further.  
**Limits:** Different R construction; interest in headline totals; not Steube meta-rule.

### 3. Gate intent
- [x] **HOLD** as historical analogue only — not full lock satisfaction

### 4. Scoped honesty
Same as Artifact C.

---

## Artifact E — Search for clean R2-equal instance
No additional public package found that states: suspension/increase **headroom $H** and CBO non-interest disc+mandatory cuts **≥ H** under current-law with no material exceptions.

**Schema match?** **No** → insufficient even for HOLD as full instance.
