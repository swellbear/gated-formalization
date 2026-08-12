# Package-Satisfying Evidence Intake — Pass 1

**Date:** 2026-08-11  
**Application:** `2026-08_debt-limit-equal-spending-cuts`  
**Locked package / scope label:** **Under P-Score-Strict+R2 only**  
**Target dependent(s):** Empirical instance of balance test (L3c reopen); optional alignment of H.R.10078 drafting with lock slots  

---

## Artifact A — H.R.10078 / “Dollar-for-Dollar Deficit Reduction Act” press description (meta-rule bill)

### 1. Lock schema match
| Slot | Required by lock | Value in this artifact |
|------|------------------|------------------------|
| E (metric) | E2 official score | Requires CBO cost estimate public 24h before vote — **partial** (process, not a completed score of a limit+cuts package) |
| S | S2+S3+S6 | Press: prohibits counting **net interest** toward cuts; bans shifting costs outside 10-year window (anti-gimmick) — **aligns S3/S6**; S2 (mandatory+discretionary) **not specified** in press |
| B | B1 current-law | **Not specified** |
| R | R2 borrowing headroom | **Not specified** (says equal/greater cuts vs limit action generally; no headroom methodology) |
| X | X1 no exceptions | **Not specified** in press |
| OR-slots | R2 locked | N/A |

**Schema match?** **Partial** — meta-rule design features overlap S3/S6 and CBO visibility; **not** an instance score of headroom vs cuts for a concrete limit action.

### 2. Artifact summary
**Source:** Rep. Steube press release, Aug 2026 — Dollar-for-Dollar Deficit Reduction Act / H.R.10078 purpose description.  
https://steube.house.gov/press-releases/rep-steube-introduces-dollar-for-dollar-deficit-reduction-act-to-force-congress-to-cut-spending-before-raising-the-debt-limit/  
**Reports:** Requires matching equal **or greater** spending cuts over **current year + following 10 years**; points of order; CBO estimate 24h public; Treasury near-limit notice; bans interest counting and out-of-window shifts.  
**Limits:** Press summary, not enrolled scored instance; “equal or greater” and “current year + 10” differ slightly from lock’s decade E2/R2 formulation.

### 3. Provisional gate intent
- [ ] ADMIT as empirical balance instance  
- [x] Aim **HOLD** / narrow design-alignment only  
- [ ] REJECT as instance evidence  

**ADMIT bar for instance:** Named limit action + R2 headroom estimate + CBO-style scored non-interest outlay cuts under B1 with S2/S6 — **not met**.  
**HOLD bar:** Documentable overlap of bill’s stated anti-gimmick/interest/CBO features with lock slots — **met partially**.  
**REJECT triggers for instance claim:** Treating press advocacy as proof of balance or unrestricted irresponsibility.

### 4. Scoped-result honesty
**Under:** P-Score-Strict+R2 (design note only).  
**Partial / claim-adjacent?** Yes.  
**Must not be promoted to:** FD1 must; unrestricted FD4; FD5 should-not-enact; empirical proof that unpaired increases fail the lock.

### 5. Next
- [x] Proceed to formal `04` (narrow HOLD/ADMIT design alignment; REJECT instance)

---

## Artifact B — Concrete debt-limit action with package-satisfying score

### 1. Lock schema match
**No artifact found** in this pass that reports R2 headroom + E2/B1/S2/S3/S6 scored cuts for a specific increase/suspension.

**Schema match?** **No**

### 3. Provisional gate intent
- [x] Aim **REJECT** / stop — insufficient even for HOLD as instance evidence

### 5. Next
- [x] Stop for Artifact B — evidence insufficient even for HOLD  
- Reopen condition unchanged: supply package-satisfying scored instance via new intake.
