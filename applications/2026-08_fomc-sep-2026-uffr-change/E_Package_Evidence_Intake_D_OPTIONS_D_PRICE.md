# Package-Satisfying Evidence Intake — D-OPTIONS / D-PRICE (Polymarket page)

**Date:** 2026-08-12  
**Application:** `2026-08_fomc-sep-2026-uffr-change`  
**Locked package / scope label:** Rank 3 Q3+O2+L1+B1; **M unset**  
**Target dependent(s):** O2 displayed options; descriptive price print  
**Named-class pulse?** **Yes** for **page census** (brackets + published ¢). **No** for modal-bar met (M unset).

---

## 0. Named-class pulse

| Check | Value |
|-------|--------|
| Freeze line (quoted) | Rank 3 Q3+O2: named market’s published price is the odds **vehicle**; displayed options from operator URL. M **unset** — do not score P-BaseCase/P-NonNegligible. |
| Named source class | Polymarket `https://polymarket.com/event/fed-decision-in-september-762` — event **Fed Decision in September?**; published **Yes ¢** and displayed **%** per listed bracket. |
| Named enough? | **Yes** for page census — operator named this URL; public event page + matching upper-bound-change object. |
| Non-circular? | **Partial** — the page **is** the brochure that posed the contract. Usable to census **what it displays**. **Circular** if used as sole proof that a bracket **is** the expected path. |
| Schema match | **Yes** for O2 (five brackets listed). **N/A** for M (unset). **No** for F-PRINT (statement does not exist). |
| Conflicted-source flag completed (§2)? | **Yes** |
| **Establishment-stop drill:** Would honest `04` declare **established**? | **No** for P-BaseCase/P-NonNegligible (M unset; even if M2 were locked, conflicted venue cannot be **sole** affirmation). **No** for F-PRINT. Census of displayed ¢ is not bar-met. If this were scored as establishing “No change is the expected path” → **stop**. It is not. |

---

## 1. Lock schema
| Slot | Required by lock | Value in this artifact |
|------|------------------|------------------------|
| Object | Upper-bound **change** vs pre-Sep meeting | Page rules match operator paste |
| Brackets O2 | Displayed options | 50+ dec / 25 dec / No change / 25 inc / 50+ inc |
| Odds vehicle | Published Yes ¢ / % | See table |
| M | P-BaseCase or P-NonNegligible | **Unset** |
| F-PRINT live | Sep FOMC statement | **Not this page** |
| OR-slots | M singled / either-accepted? | **No** — incomplete |

**Schema match?** **Yes** for O2 census. **Incomplete** for odds-bar test.

---

## 2. Artifact summary
**Source / citation:** https://polymarket.com/event/fed-decision-in-september-762 (fetched 2026-08-12; page “as of August 13, 2026”)

**What it reports (concise):**

| Bracket | Yes ¢ | Header % |
|---------|-------|----------|
| 50+ bps decrease | 0.6¢ | <1% |
| 25 bps decrease | 1.1¢ | 1.0% |
| No change | 67¢ | 67% |
| 25 bps increase | 33¢ | 33% |
| 50+ bps increase | 0.5¢ | <1% |

Rules text on the page matches the operator paste (upper bound; Sep 15–16 2026 statement; round up to 25; fallback No change). Headline volume ~$29,875,182.

**Sample / setup limits:** Five separate binaries; ¢ need not sum to 100. Header % vs Yes ¢ can differ (50+ decrease). Snapshot, not a time-average.

### Conflicted-source flag (mandatory)
- [ ] **Non-conflicted**
- [x] **Conflicted / interest-aligned** — Other: **prediction-market trading venue** (prices are bets, not a disinterested forecast series)

**If conflicted:** May support **scenario presence / design kinship / pitch curves only**. Must **not** be the sole basis for affirming a locked modal bar or establishing the original slogan.

### Quantitative bar?
Not until M is locked. No `E_Quantitative_Evidence_Rubric` this cycle.

---

## 3. Provisional gate intent
- [x] Aim **ADMIT** as **D-OPTIONS** (bracket list) + **D-PRICE** as **conflicted page print** (what ¢ were displayed)  
- [ ] Aim **HOLD**  
- [ ] Aim **REJECT**

**ADMIT bar:** Page lists those five brackets and those Yes ¢ at fetch.  
**HOLD bar:** M still unset for any “expected path” reading.  
**REJECT triggers:** Using 67¢ as P-BaseCase met; using page as Sep statement; importing June SEP.

---

## 4. Scoped-result honesty
Findings, if admitted, hold **under:** Rank 3 Q3+O2+L1+B1, this URL, this fetch vintage.  
**Partial / claim-adjacent?** **Yes** — page census, not the September print, not bar-met.  
**Must not be promoted to:** FOMC will hold; 67% **is** P-BaseCase; 33% hike is “likely”; June SEP path.

---

## 5. Next
- [x] Proceed to `04_Material_Admission_D_OPTIONS_D_PRICE.md`  
- [ ] Stop — evidence insufficient even for HOLD  

---

*Standing-rule package-satisfying evidence intake. Domain-general.*
