# Lock Record — Trump Truth Social oil-sentiment hunt

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Operator selection:** `Lets make this happen. For 1-5 use your best judgment`  
**App-local lock IDs:** **L-HUNT-DJT** · **L-STANDIN-DJT-TRUTH** · **H-DJT-WEEK** · **H-DJT-MONTH**  
**Status:** **IN FORCE as protocol + named drawer (cap = these two horses).** Written **before** last-500 confirm scores. Confirm is **one** survivor (or none). F-SKILL **not** auto-established.

---

## 0. Plain-language framing

**What was decided:**  
Score Donald Trump’s **Truth Social** posts that mention oil, mark each as likely to push crude **up**, **down**, or **neither**, average those marks over a **week** or a **month**, and see whether that average beats “assume no change” on the next whole oil session. The computer may pick **one** of those two windows, only if it already beat no-change on **older** sessions. Year / six-month / single-day averages are **not** in this test.

**What this settles:**  
The archive, the oil filter, the up/down/flat rule, the clock, and the two-horse cap.

**What this does *not* settle:**  
That Trump moves oil. That skill is shown. That anyone should trade. That speeches or White House remarks were included.

---

## Named protocol (quote this)

**Scope:** **Under Rank 4 + L-SESS + F-SRC-CME-TAPE + L-STANDIN-Y-CLF + L-SCREEN-Y-PROMOTE + L-HUNT-DJT + L-STANDIN-DJT-TRUTH**.

This is a **capped named drawer**, not an unbounded “score all public statements.” Cap = **these two horses**. Do **not** expand after seeing scores. Do **not** hunt on last 500. Do **not** retune the lexicon after RMSE. Do **not** mix in speeches or White House transcripts this pulse.

### 1. Archive (L-STANDIN-DJT-TRUTH)

Trump’s own Truth Social posts, dated, from the public CNN dump  
`https://ix.cnn.io/data/truth-social/truth_archive.json`  
Fallback: `https://stilesdata.com/trump-truth-social-archive/truth_archive.json`.

Fields: `created_at`, `content`, `url`. Strip HTML. Skip empty / media-only posts.

**Named limitation:** Truth Social launched **Feb 2022**. Discovery last-500 starts **2021-08-25**, so early discovery days may be silent. White House remarks would be empty in 2021–2023 (out of office). Speeches / WH transcripts **OUT**. Third-party scrape, not an official statement archive.

### 2. Oil-adjacent

A post counts only if stripped text matches at least one token in `data/djt_oil_lexicon.json` → `oil_adjacent` (case-insensitive). Bare “energy” / “electricity” / “nuclear” **OUT**. Borderline **OUT**.

### 3. Positive / Negative / Flat (crude **price** direction, not pro-industry)

Mechanical lexicon in the same JSON. **Not** an LLM.

| Score | Meaning | JSON key |
|-------|---------|----------|
| **+1** | bullish crude price (tighter supply / fill SPR / sanctions-as-oil / OPEC cut) | `bullish_price` |
| **−1** | bearish crude price (more drilling / SPR release / OPEC increase) | `bearish_price` |
| **0** | oil-adjacent but neither list, **or both** lists fire | — |

Do **not** retune after seeing scores.

### 4. Clock

Post calendar date = **UTC** date of `created_at` (named limitation vs ET).

| Window | Issued | Sentiment ending |
|--------|--------|------------------|
| **F-ON / F-CC** | t−1 settle | CL date **t−2** |
| **F-DAY** | t open | CL date **t−1** |

Silent day (no oil-adjacent post) → daily score **0** (no carry-forward).

### 5. Two horses (cap)

Daily score on a CL date = mean of that UTC day’s oil-adjacent post scores (or 0 if none).

| ID | Signal |
|----|--------|
| **H-DJT-WEEK** | Mean of daily scores over last **5** CL sessions through the lagged date |
| **H-DJT-MONTH** | Mean of daily scores over last **21** CL sessions through the lagged date |

Year / 6-month / calendar-day averages **OUT**.

OLS: expanding, intercept, min train **250**. F-ON/F-CC: `[1, r_ON,t−1, r_DAY,t−1, s]`. F-DAY: `[1, r_ON,t, r_DAY,t−1, s]`. Rank-deficient or n_train < 250 → **0**. Missing CL y/x → skip (same as H-LAG). Sentiment always defined (0 on silence).

### Discovery / confirm

| Slot | Rule |
|------|------|
| **Discovery cutoff** | CL sessions **≤ 2023-08-21** |
| **Discovery scoreboard** | F-CC RMSE vs 0 on last **500** of that prefix |
| **Selection** | Lowest F-CC RMSE **only if** it **strictly beats** 0. If neither → **no survivor** |
| **Ties** | Keep **H-DJT-WEEK** (earlier in this lock) |
| **Confirm** | That **one** horse (or skip). Last **500 / 250 / 750** vs 0. No runner-up |
| **Promote** | Still **L-SCREEN-Y-PROMOTE**. Yahoo win ≠ live ≠ F-SKILL-met |
| **Vehicle fail** | Fetch fails or discovery-window oil-adjacent count too thin to form a series → stop; do not invent speeches |
| **Establishment-stop** | Honest `04` that would say **established** still **stops**. No DataMine auto-open |

---

## What this does *not* do

- Does **not** establish F-SKILL, F-ON, F-DAY, F-CC, or V-VALUE.  
- Does **not** say Trump moves oil.  
- Does **not** include rallies, interviews, or White House remarks.  
- Does **not** license trading, start an oil offshoot, or enter Phase 2.

**Lock-time Amb warning:** Running this hunt does **not** drop leftover-ambiguity on V-SRC. **Amb ≠ clearance.**

---

## Reopen

`leave skill not shown` · `name horse …` (a **different** recipe; do **not** add year/6-month/day windows after scores; do **not** retune the lexicon) · `leave screen rule`. Live CME **only if** **L-SCREEN-Y-PROMOTE** fires. Honest **established** still **stops**.
