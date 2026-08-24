# Pulse result — EIA spot expanding-window logistic (Track B queue)

**Date:** 2026-08-24  
**Application:** `2026-08_oil-futures-predictive-model`  
**Layer ID:** **L-PULSE-SPOT-LOGIT-1**  
**Locks:** `Lock_Hunt_Spot_Logit.md` · `Lock_Hunt_Spot_Trend.md` · `QUEUE_Spot_Trend_Exploration.md`  
**Live vs stand-in:** existing FRED EIA spot reprints. **Not** NYMEX CL. **No print scored to F-SKILL-met.**

---

## 0. Plain-language framing

**What we did:** You asked to try the next idea on the same cash 21-day question: fit a simple logistic rule on **older** days only (sign of the last 21 days, and how large that move was), then call the next 21. One rule used both ingredients; the other used the sign alone. Both beat “the trend continues” on the **older** exam for WTI and for Brent, so the fuller rule (tie-break) went to the recent exam. On the recent exam it **lost** to continuation on every locked window, for both oils. Burned rules were **not** brought back. 21 days was **not** changed. The recent exam was **not** used to train or retune.

**What this settles:** Numeric discovery and confirm hit-rates for this two-horse drawer. Discovery survivors **failed confirm**. Not a trade.

---

## 1. Vehicle (not a fail)

Reuse of existing spot CSVs. Successful fits on all **500** discovery dates both boards (threshold 250 — **not** vehicle-fail). Train = eligible *u* with `outcome_date < t`; min train **50**. Burned FLIP-HOLD / REV / INV / B2W **not** scored. W2B **not** remixed.

---

## 2. Discovery (locked before last-500 confirm)

Cutoff: issue dates **≤ 2023-08-21**. Scoreboard: last **500** eligible of that prefix. Train arm: **used** (expanding past-only).

### WTI (2021-08-24 … 2023-08-21)

Continuation: **0.508** (254 / 500).

| Horse | Hits | Hit-rate | Beats continuation? |
|-------|------|----------|---------------------|
| **H-SPOT-LOGIT-FULL** | 266 | 0.532 | **yes** |
| **H-SPOT-LOGIT-SIGN** | 266 | 0.532 | **yes** (tie) |

**Survivor:** **H-SPOT-LOGIT-FULL** (tie keeps FULL).

### Brent (2021-08-27 … 2023-08-21)

Continuation: **0.506** (253 / 500).

| Horse | Hits | Hit-rate | Beats continuation? |
|-------|------|----------|---------------------|
| **H-SPOT-LOGIT-FULL** | 275 | 0.550 | **yes** |
| **H-SPOT-LOGIT-SIGN** | 275 | 0.550 | **yes** (tie) |

**Survivor:** **H-SPOT-LOGIT-FULL** (tie keeps FULL).

WTI-met ≠ Brent-met for later confirm; both sent their own FULL survivor.

---

## 3. Confirm (FULL on both boards)

Confirm **never** trains. Walk-forward refit under the frozen recipe only.

### WTI — **H-SPOT-LOGIT-FULL**

| Window | First … last | Horse | Continuation | Strictly greater? |
|--------|--------------|-------|--------------|-------------------|
| last **500** | 2024-07-16 … 2026-07-20 | **0.430** (215 / 500) | 0.552 (276 / 500) | **no** |
| last **250** | 2025-07-18 … 2026-07-20 | **0.476** (119 / 250) | 0.572 (143 / 250) | **no** |
| last **750** | 2023-07-14 … 2026-07-20 | **0.463** (347 / 750) | 0.557 (418 / 750) | **no** |

### Brent — **H-SPOT-LOGIT-FULL**

| Window | First … last | Horse | Continuation | Strictly greater? |
|--------|--------------|-------|--------------|-------------------|
| last **500** | 2024-07-24 … 2026-07-20 | **0.442** (221 / 500) | 0.522 (261 / 500) | **no** |
| last **250** | 2025-07-21 … 2026-07-20 | **0.496** (124 / 250) | 0.524 (131 / 250) | **no** |
| last **750** | 2023-07-28 … 2026-07-20 | **0.465** (349 / 750) | 0.525 (394 / 750) | **no** |

Discovery beat ≠ confirm beat. Do **not** retune features / min-train / solver after these numbers. Do **not** change 21. Do **not** unburn. Do **not** swap SIGN in after confirm.

**L-SCREEN-Y-PROMOTE:** **does not apply**.

---

## 4. Establishment-stop drill

**Would honest `04` declare spot 21-day skill established?** **No.** Confirm loses continuation on every window both boards.

**Would honest `04` declare F-SKILL established?** **No.** This pulse did not score next-session CL RMSE.

**Would honest `04` declare those bars refuted?** **No.** A confirm loss is not “logistic cannot work on oil,” and it is not a futures refute.

Stop was **not** hit. Do **not** auto-declare bar-met. Do **not** auto-open DataMine.

---

## 5. Exploration queue (after scores)

Burned (prior rows stay). SIGN tied FULL on discovery (not a discovery loss). FULL failed confirm both boards — do **not** retune. Track B named queue is **empty** after this class.

---

## 6. Scripts / artifacts

- `scripts/spot_logit_hunt.py`  
- `data/spot_logit_hunt_scores.json` · `data/spot_trend_queue.json`  
- Reproduce: `python3 scripts/spot_logit_hunt.py --stage discovery` then `python3 scripts/spot_logit_hunt.py --stage confirm`

---

*Not trading advice. Discovery survivor ≠ confirm pass. Confirm is not a training arm. Tiny ≠ met still in force; here confirm is a clear loss.*
