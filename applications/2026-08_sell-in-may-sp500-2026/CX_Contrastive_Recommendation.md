# Contrastive Recommendation — Sell in May / S&P / 2026

**Date:** 2026-08-12  
**Application:** `2026-08_sell-in-may-sp500-2026`  
**Authorization:** **Yes** — operator instruction authorized one run using only in-hand evidence/locks after adding the mode to the standing rule  

**Original claim (verbatim):**  
“Because the S&P 500 has historically delivered substantially lower average returns from May through October than from November through April, an investor should be out of the S&P 500 (or in cash/T-bills) for the May–October window; following this rule improves risk-adjusted outcomes relative to buy-and-hold over the long run and should be followed for the current May–October 2026 period.”

**Endpoint / closeout status:** Phase 2 Attempt 1 endpoint (not yet formal closeout). Rank 1 lock. Amb ≈ 2.5. Original packaged elevations **not** established.

---

## 0. Plain-language framing

**What was established:**  
Under Rank 1 / H2 (^SP500TR workbook): May–Oct average total returns are **substantially lower** than Nov–Apr (gap **≈ 3.52 pp** ≥ 2.0 pp threshold). Seasonality pattern is real on the locked sample.

**What failed (elevation):**  
(1) “Out for May–Oct” as default **should** (S3).  
(2) “Improves risk-adjusted outcomes vs buy-and-hold” (Sharpe under F3) — **fails** on workbook (pre-tax and after-tax proxy).  
(3) “Should be followed for May–Oct **2026**” — not established (tracks failed should; averages ≠ dated forecast).

**What this mode will do:**  
Propose alternatives that keep the established seasonality core and drop the failed performance/obligation elevations; minimal gate each with **only** locks/evidence already in hand.

**What this mode will not do:**  
Overwrite Rank 1 findings, FD1–FD5, or admitted layers; start Claim-Revision; fetch new data.

---

## 1. Extract

| Established core | Failed elevation(s) |
|------------------|---------------------|
| G1*: H2 seasonality gap established (~3.52 pp) | G4*: Sharpe improves vs B&H — not established (fails) |
| Lower strategy vol is real but insufficient for Sharpe win | G5*: S3 default “should” — not established |
| L1a/L1c: history ≠ should; averages ≠ 2026 entailment | G6*: 2026 “should” — not established |

**Governing locks / evidence in hand:**  
`Lock_Rank1_Full_Claim_Strict.md`; `P2_Attempt1_H2_Workbook_Numbers.md`; `P2_Attempt1_Rank1_H2_Readout.md`; L1a–e, L2a–d, L3a–c.

---

## 2. Alternative claims (1–3)

### Alt A — Descriptive seasonality only

**Wording:**  
“Under post-1980s S&P 500 total-return data, average returns from May through October have been substantially lower than average returns from November through April (on the order of several percentage points for the six-month windows).”

### Alt B — Awareness without obligatory exit

**Wording:**  
“Investors should treat the historical May–October vs November–April S&P 500 return gap as a documented seasonal fact when planning, without treating a mechanical full exit to T-bills as a default policy that improves risk-adjusted results versus buy-and-hold.”

### Alt C — Preference-framed de-risking (not performance edge)

**Wording:**  
“An investor who independently prefers lower equity exposure in May–October may hold T-bills in that window for risk-preference reasons; that choice should not be justified as a long-run Sharpe improvement over buy-and-hold after costs and taxes.”

---

## 3. Minimal gated check (per alternative)

### Alt A — Descriptive seasonality only

| Check | Result |
|-------|--------|
| Claim-type | **Descriptive** |
| Key free parameters | Sample/ops already locked (H2) — Low residual; “several pp” qualitative vs exact 3.52 — Low |
| Cons w/ admitted layers | **Pass** — matches L3a / G1* established; avoids G4–G6 |
| Higher-level review | **Pass** — no overclaim |
| New Amb | **Low** |
| Minimal verdict | **Better-fit provisional** |

**Why better than original elevation:** States only what the workbook established; drops “because → should,” Sharpe improvement, and 2026 obligation.  
**Still open:** Exact wording of “substantially” if taken outside Rank 1; out-of-sample future seasons.

### Alt B — Awareness without obligatory exit

| Check | Result |
|-------|--------|
| Claim-type | **Mixed** (descriptive fact + soft “should treat as fact,” explicitly **anti**-default-exit) |
| Key free parameters | Soft “should treat as fact” (educational) — Med; audience — Low |
| Cons w/ admitted layers | **Pass** — consistent with G1* established + G4*/G5* not established + L1a |
| Higher-level review | **Pass with caution** — still uses “should,” but as awareness, not exit obligation |
| New Amb | **Med** (educational “should” still soft-modal) |
| Minimal verdict | **Better-fit provisional** |

**Why better:** Keeps seasonality; explicitly rejects the failed mechanical-exit / Sharpe elevation.  
**Still open:** How strong “should treat as fact” is; not a full investor-education curriculum.

### Alt C — Preference-framed de-risking

| Check | Result |
|-------|--------|
| Claim-type | **Normative/Strategic** (preference + negative performance claim) |
| Key free parameters | “Independently prefers” (subjective) — Med; negative Sharpe claim locked to Rank 1 F3 evidence — Low under that scope |
| Cons w/ admitted layers | **Pass** — matches G4* failure; does not assert S3 |
| Higher-level review | **Pass with caution** — preference clause is not forced by data; negative Sharpe claim is scoped |
| New Amb | **Med** |
| Minimal verdict | **Better-fit provisional** (scoped) |

**Why better:** Separates risk preference from the failed “improves Sharpe / must exit” package.  
**Still open:** Whose preferences; tax situation; whether any non-Sharpe metric could still motivate exit for some investors (not claimed here).

---

## 4. Ranking (best fit / least new Amb first)

1. **Alt A** — Descriptive seasonality only (best Cons; least new Amb; closest to established core)  
2. **Alt B** — Awareness without obligatory exit (keeps a mild “should,” but aligned with failures)  
3. **Alt C** — Preference-framed de-risking (honest about G4* failure; adds preference Amb)

---

## 5. Plain-language report

The workbook supports a **seasonality fact**, not the original **exit / Sharpe-improvement / do-it-in-2026** package.

- **Best contrastive fit:** Alt A — say the historical gap plainly.  
- **If you want a recommendation tone without the failed elevation:** Alt B — know the pattern; don’t treat mechanical T-bill exit as a default Sharpe-improving policy.  
- **If someone still wants a May–Oct cash sleeve:** Alt C — frame it as **preference**, not as beating buy-and-hold on Rank 1 Sharpe after costs/taxes.

**Original Rank 1 endpoint findings and FD1–FD5 stay on the record.** These alternatives are contrastive options, not a silent rewrite and not an automatic Claim-Revision selection.

---

## 6. Non-silent rule (affirm)

- [x] Original endpoint / FD findings remain on the record.
- [x] No new search — used only in-hand Rank 1 workbook and admissions.
- [x] Distinct from Claim-Revision Scaffolding and QI.

---

*Contrastive Recommendation complete for this authorization. Stop.*
