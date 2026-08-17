# Pulse result — Trump Truth Social oil-sentiment hunt (Yahoo stand-in)

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Layer ID:** **L-PULSE-DJT-1**  
**Locks:** `Lock_Hunt_DJT.md` · `Lock_Screen_Yahoo_Promote.md` · `Lock_Standin_Yahoo_CLF.md`  
**Live vs stand-in:** **Stand-in.** **No print scored to met.**

---

## 0. Plain-language framing

**What we did:** You asked the computer to score Trump’s own Truth Social posts that mention oil as “likely up,” “likely down,” or “neither,” then average those marks over a **week** or a **month**, and pick at most one of those two windows — only if it already beat “assume no change” on **older** whole trips. Year / six-month / single-day averages were **not** in this test. Neither window beat no-change on that older exam (they **tied** it). So **no winner was sent** to the recent exam. We did **not** retune the word list after seeing that, and we did **not** add speeches.

**What this settles:** Numeric discovery RMSE for the locked two-horse drawer, plus a named coverage fact: on older oil-session dates the daily score was **always zero**. Hunt **failed at discovery**. Promote does **not** fire. Skill is still **not shown**. Not a trade.

---

## 1. Vehicle (not a fail)

CNN dump `https://ix.cnn.io/data/truth-social/truth_archive.json` fetched. **28,548** posts with text, **2022-02-14 … 2026-08-17** (Truth Social launch). Fallback unused.

| Count | Value |
|-------|-------|
| Oil-adjacent posts (whole dump) | **345** |
| Oil-adjacent in discovery session span (≤ 2023-08-21) | **53** (threshold 30 — **not** vehicle-fail) |
| Of those, on a discovery CL session date | **34** |
| Of those, not on a CL session date (weekend/holiday UTC) | **19** |
| Discovery P/N/F in span | **+1: 0** · **−1: 3** · **flat: 50** |
| P/N/F on discovery CL session dates | **+1: 0** · **−1: 0** · **flat: 34** |
| Discovery CL days with nonzero daily score | **0** |

The three −1 posts landed on non-session UTC dates. Frozen clock: weekend posts do **not** attach to the next session. Silent CL day = **0**. Frozen lexicon: oil-adjacent but neither (or both) lists = **0**. Do **not** retune. Do **not** invent White House remarks.

---

## 2. Discovery (locked before last-500 confirm)

Prefix: CL sessions **≤ 2023-08-21** (n = **5769** return sessions). Scoreboard: last **500** of that prefix (**2021-08-25 … 2023-08-21**). Walk-forward OLS, min train 250. Sentiment lag: F-ON/F-CC use t−2; F-DAY uses t−1.

Because every discovery CL daily score is **0**, the extra column is constant. Rank-deficient OLS → forecast **0**. Both horses **equal** no-change.

Discovery F-CC RMSE of 0: **0.026705**.

| Horse | F-CC RMSE | vs 0 | Beats 0? |
|-------|-----------|------|----------|
| **H-DJT-WEEK** | 0.026705 | 0.026705 | **no** (tie) |
| **H-DJT-MONTH** | 0.026705 | 0.026705 | **no** (tie) |

Exact F-CC: horse **0.02670533649743393** = 0 **0.02670533649743393**. F-ON 0.00733254 = 0. F-DAY 0.02584659 = 0.

**Survivor:** **none.** Reason: no horse **strictly** beat 0 on discovery F-CC. A tie is **not** a beat. Do **not** pick the least-bad.

---

## 3. Confirm

**Skipped.** No discovery survivor. Last 250 / 500 / 750 were **not** used to pick a horse. Do **not** re-hunt this confirm window. Do **not** add year / 6-month / day averages after scores. Do **not** retune `data/djt_oil_lexicon.json`.

**L-SCREEN-Y-PROMOTE:** **does not fire** (no named confirm horse).

---

## 4. Establishment-stop drill

**Would honest `04` declare F-SKILL / F-CC / F-ON / F-DAY established?** **No.**

A frozen Truth Social oil filter that is **all zeros** on discovery session dates is not P-NonNegligible skill. Equal-to-0 ≠ beat-0. Failed discovery ≠ a promote. Cap remains these two rows. Speeches / WH remarks stay **OUT**.

**Would honest `04` declare those bars refuted?** **No.** A finite drawer miss does not refute every recipe. It also does **not** say Trump “doesn’t move oil” in some other corpus or clock.

---

## 5. Scripts / artifacts

- `scripts/fetch_djt_truth.py` · `scripts/cl_djt_hunt.py`  
- `data/djt_oil_lexicon.json` · `data/djt_truth_posts.csv` · `data/djt_truth_fetch.json` · `data/djt_hunt_scores.json`  
- Reproduce: `python3 scripts/fetch_djt_truth.py` then `python3 scripts/cl_djt_hunt.py` from this application folder.

---

*Not trading advice. Stand-in ≠ live. No survivor ≠ pick the least-bad. All-zero session series ≠ retune the lexicon. Do not re-hunt confirm. Cap remains these two rows.*
