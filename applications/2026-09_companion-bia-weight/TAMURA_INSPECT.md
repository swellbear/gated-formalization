# Tamura 2026 *PLOS ONE* — inspect (summary)

**Date:** 2026-09-05  
**Application:** `2026-09_companion-bia-weight`  
**Paper:** Tamura J, Itami T, Kato K, Sugita C, Oyama N, Yamashita K (2026) Comparison of clip and needle electrodes for multifrequency bioimpedance analysis in anesthetized dogs. *PLoS One* 21(8): e0355338. [DOI 10.1371/journal.pone.0355338](https://doi.org/10.1371/journal.pone.0355338)  
**License:** CC-BY (PLOS).  
**Named gap asked:** public row-level canine/feline BIA (R/X/Z) + **live** body weight under an open license.

Lab scratch `TAMURA_INSPECT.md` was **not** on this fold VM. This is the inspect **summary** folded with the Operator + Founder gate.

---

## Verdict

**inspected-fail** for the named joint table.

Soften **existence/intent only**: a 2026 open-access canine MF-BIA study exists; it is **not** a joinable live-W + R/X/Z row table.

---

## What was inspected

- **n=7** intact adult Beagles (4 male, 3 female).
- Trunk MF-BIA at 5 / 50 / 250 kHz; clip vs needle; sternal vs left-lateral; three electrode paths.
- Data-availability line: “All relevant data are within the manuscript and its Supporting Information files.”
- **S1 Table** (caption): per-dog MF-BIA parameters and analysis status (R0, Rinf, Xmax, PAmax, path/condition). **Not** paired live body weight.
- **Body weight** in the article is **prose-only**: 8.9–15.5 kg; 12.9 ± 2.2 kg (mean ± SD). No per-dog W column to join to S1.
- **SI mislink:** the S1 DOI [`10.1371/journal.pone.0355338.s001`](https://doi.org/10.1371/journal.pone.0355338.s001) did not serve a usable file on inspect (HTTP 406). The generic supplementary `article/file` URL 404’d. S2’s HTML caption lacked a working `s002` link. Do **not** treat SI as a recovered joint deposit.

---

## Why this is not succeed

| Named-gap slot | Tamura 2026 |
|----------------|-------------|
| Row-level BIA (R/X/Z or Cole–Cole) | Intent / SI caption — **not** a verified joint file on inspect |
| Paired **live** body weight | **Prose range/mean only** |
| Open license on a joinable table | Article is CC-BY; the **joint table is not there** |
| n holdout-capable | **n=7** — still not training-scale even if BW had been in S1 |

Soften existence/intent only. **Not** full SUCCEED. **Not** a reason to invent per-dog weights from 8.9–15.5 kg.

---

*Docs only. Inspected-fail ≠ refute of every future Tamura file. Do not reconstruct BW rows from the prose range.*
