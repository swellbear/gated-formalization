# Copy gate — US10135667B1 abstract ingest + A1/A2 honesty numbers

**Date:** 2026-09-05  
**Application:** `2026-09_greer-sync-pulse-tdoa`  
**Verdict:** **PASS** — abstract + bibliographic only. **No claim-language product copy.**

This gate is required because the owner asked us to ingest the published abstract as the Amb spine, then name A1/A2 honesty classes. Ingest + Soften is **not** a license to paste claims or to write a product embodiment (including a 1PPS / F9T product).

## What may sit in this folder

| Allowed | Where | Why |
|---------|-------|-----|
| Bibliographic identifiers (number, title, inventor, dates, public URL) | [`SOURCE.md`](SOURCE.md) | Citation |
| **Published abstract** (verbatim block) | [`SOURCE.md`](SOURCE.md) | The admitted SOURCE |
| Short paraphrase of abstract leftovers (A1–A4; link/map parked) | ingest / STATUS / ledger | Amb spine |
| Operator-named description-typical numbers: patent-facing **≤1 m xy**; **DGPS ~0.4–0.5 m** / **RN floor** | ingest / A1 / STATUS / ledger | Success-bar + A1 Soften; **not** claim text |
| Operator-named public timing classes: differential **~2.5 ns (F9T-class)**; commodity **20–50 ns**; common-view **~10 ns**; absolute-only **~5–15 ns**; public residuals **ns–tens-of-ns** | A2 score / digestion / STATUS / ledger | A2 Soften (conditional); **not** claim text; **not** a product used |
| Operator-named Chan ~**1.14 m** @ ~2.5 ns | A2 score / digestion | Kill bare Chan; copied from the gate |
| Operator-named **brutal lock** paraphrase: patent simultaneous-via-DGPS-1PPS ≠ commercial 1PPS reality | A2 / STATUS / ledger | Honesty lock; **not** claim quote; **not** product copy |

## Hard NO

- Do **not** paste, quote, or reconstruct **claim** text (independent or dependent).
- Do **not** write product copy that practices claim language (“a system comprising … as claimed”).
- Do **not** write a 1PPS / F9T / DGPS product embodiment.
- Do **not** paste long description / figure / waveform / link-budget blocks.
- Do **not** treat abstract ingest or A1/A2 Soften as claim clearance or as a product embodiment of US10135667B1.
- Do **not** collapse patent simultaneous-via-DGPS-1PPS into commercial 1PPS reality.
- Do **not** send the prior write-up as if it were a patent-hard-problem digest. Prior write-up = **sync-fragility evidence only**.

## Check (this fold)

- [`SOURCE.md`](SOURCE.md) holds the published abstract + bibliographic table. **Claims absent.**
- [`PROPOSED_ABSTRACT_INGEST.md`](PROPOSED_ABSTRACT_INGEST.md) and [`ABSTRACT_INGEST_SUMMARY.md`](ABSTRACT_INGEST_SUMMARY.md) paraphrase leftovers. **No claim quotes.**
- [`SCORE_A1.md`](SCORE_A1.md) / [`SCORE_A2.md`](SCORE_A2.md) use Operator-named bars and public timing classes. **No claim quotes.** **No** 1PPS product copy.
- **≤1 m xy**, **DGPS ~0.4–0.5 m**, **F9T-class ~2.5 ns**, commodity / common-view / absolute-only classes, and the brutal lock appear as Operator-named honesty, **not** as claim language.
- [`GREER_WRITEUP.md`](GREER_WRITEUP.md) banner restates **sync-fragility evidence only**. Body is not rewritten into claim-product copy.

**PASS.** Still **not** claim clearance.
