# Calibration & Rule Diff — 2026-08-C3 (cross-domain probe)

**Date:** 2026-08-12  
**Calibration cycle ID:** 2026-08-C3  
**Applications reviewed:** `2026-08_cash-alone-privacy-preferability` (cross-domain after engineering batch)  
**Failure-mode log entries:** none

---

## 1. Observed frictions / surprises

- LOCK-001…003 transferred cleanly outside engineering.  
- LOCK-004 (design/architecture spectra) still *worked* as hybrid/spectrum discipline for payments, but only as an **analogue** — wording is narrower than the useful practice.  
- No new free-parameter shape; Amb 12→≈8; honest Stable Provisional; FD 1.

---

## 2. What worked cleanly

- Same Phase-1 thin hard-stop template cross-domain.  
- Amb≠clearance and preferability-needs-V held without soft clearance.

---

## 3. Proposed rule diff

1. **No change to Amb weights.**  
2. **No change to LOCK-001…003.**  
3. **Change LOCK-004 reuse guidance (when accepted):** broaden from “design/architecture” to “domains that are typically hybrid/spectrum,” keeping FD-on-alone requirement — because cash-privacy needed the analogue explicitly.  
4. **No Amb-math redesign.**

---

## 4. Operator decision log

| # | Proposal | Decision | Reason | Date |
|---|----------|----------|--------|------|
| 1 | No Amb weight change | Accept | Probe matched engineering Amb path | 2026-08-12 |
| 2 | Keep LOCK-001…003 | Accept | Clean transfer | 2026-08-12 |
| 3 | Broaden LOCK-004 reuse guidance | Accept (pending edit) | Marked Under review; apply wording when operator folds | 2026-08-12 |
| 4 | No Amb-math change | Accept | Hold | 2026-08-12 |

---

## 5. Ready for next step?

- [ ] Ready to fold LOCK-004 wording into lock file / ops doc now  
- [x] Hold fold of living Amb rules — only LOCK-004 Under review pending explicit wording edit  
- [ ] Discard  

**Next operator action (optional):** Authorize “edit LOCK-004 reuse guidance to hybrid/spectrum domains generally,” then return Status to Active.
