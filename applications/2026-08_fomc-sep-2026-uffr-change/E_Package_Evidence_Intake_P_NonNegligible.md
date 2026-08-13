# Package-Satisfying Evidence Intake — P-NonNegligible (M3) bar test

**Date:** 2026-08-12  
**Application:** `2026-08_fomc-sep-2026-uffr-change`  
**Locked package / scope label:** Rank 3 `Q3+O2+L1+M3+B1`  
**Target dependent(s):** G5 odds bar — P-NonNegligible (live-shot sizes)  
**Named-class pulse?** **Yes** — same named Polymarket event already used for D-OPTIONS/D-PRICE. No new fetch.

---

## 0. Named-class pulse

| Check | Value |
|-------|--------|
| Freeze line (quoted) | Rank 3 M3: published prices are read as **live-shot sizes**, not as the expected / central path. Vehicle = named market’s published Yes ¢ / % for the same upper-bound-change event. |
| Named source class | Polymarket `https://polymarket.com/event/fed-decision-in-september-762` — event **Fed Decision in September?**; published **Yes ¢** and displayed **%** per listed bracket (fetch 2026-08-12). |
| Named enough? | **Yes** for this vehicle — operator named this URL. Rival venues are different classes, not a reason to treat this one as unnamed. |
| Non-circular? | **No** for **modal affirmation** — the page **is** the brochure that posed the contract and the prices. Usable to census **what it displayed** (already D-PRICE). **Circular** as sole proof that a bracket **is** a live shot. |
| Schema match | **Yes** for object/brackets/vintage. **Partial** for M3 met: prices exist; conflicted-source blocks sole affirmation. |
| Conflicted-source flag completed (§2)? | **Yes** |
| **Establishment-stop drill:** Would honest `04` declare **established**? | **No** — conflicted venue cannot be sole support for affirming P-NonNegligible. If this were scored as establishing “25 bp increase is a live shot” or “no change is a live shot” → **stop**. It is not. Continue (not-established). |

---

## 1. Lock schema

| Slot | Required by lock | Value in this artifact |
|------|------------------|------------------------|
| Object | Upper-bound **change** vs pre-Sep meeting | Page rules match operator paste |
| Brackets O2 | Five displayed options | 50+ dec / 25 dec / No change / 25 inc / 50+ inc |
| Odds vehicle | Published Yes ¢ / % | 0.6 / 1.1 / 67 / 33 / 0.5 ¢ |
| M | **M3 P-NonNegligible** | Locked; bar-met is this test |
| F-PRINT live | Sep FOMC statement | **Not this page** |
| OR-slots | M singled? | **Yes** — M3 |

**Schema match?** **Yes** for running the bar test. **No** for treating D-PRICE as bar-met.

---

## 2. Artifact summary

**Source / citation:** https://polymarket.com/event/fed-decision-in-september-762 (fetched 2026-08-12; page “as of August 13, 2026”). Same artifact as `E_Package_Evidence_Intake_D_OPTIONS_D_PRICE.md`.

**What it reports:** Five Yes prices as listed. Not a Fed statement.

### Conflicted-source flag (mandatory)

- [ ] **Non-conflicted**
- [x] **Conflicted / interest-aligned**
  - [x] Other: **trading venue / prediction market** — prices are interest-aligned with trading; not a disinterested forecast series

**If conflicted:** May support **scenario presence / pitch curves only**. Must **not** be the sole basis for affirming P-NonNegligible.

---

## 3. Provisional gate intent (before full `04`)

- [ ] Aim **ADMIT** as constraining the dependent under this package (bar **met**)
- [x] Aim **ADMIT** the **test result**: bar **not established**
- [ ] Aim **HOLD**
- [ ] Aim **REJECT**

**ADMIT bar for this freeze:** A **non-conflicted** matched series’ published central statistic shows a non-vanishing live shot at a named bracket.  
**HOLD / not-established:** Only conflicted pitch curve available.  
**REJECT triggers:** Using this page as the September print; using 67¢ as P-BaseCase; inventing Kalshi/CME as this class.

---

## 4. Scoped-result honesty

Findings hold **under Rank 3 M3 only.**  
**Partial / claim-adjacent?** Yes — page print ≠ FOMC print; live-shot **bar** ≠ expected path.  
**Must not be promoted to:** the FOMC will hold / hike / cut; 33¢ **is** a cleared live shot; 67¢ is the expected path; June SEP path.
