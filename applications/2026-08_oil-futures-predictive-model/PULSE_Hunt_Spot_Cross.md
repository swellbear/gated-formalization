# Pulse result — EIA spot WTI ↔ Brent 21-day cross-bench overlay (Track B queue)

**Date:** 2026-08-24  
**Application:** `2026-08_oil-futures-predictive-model`  
**Layer ID:** **L-PULSE-SPOT-CROSS-1**  
**Locks:** `Lock_Hunt_Spot_Cross.md` · `Lock_Hunt_Spot_Trend.md` · `QUEUE_Spot_Trend_Exploration.md`  
**Live vs stand-in:** existing FRED EIA spot reprints. **Not** a dollar spread. **Not** NYMEX CL. **No print scored to F-SKILL-met.**

---

## 0. Plain-language framing

**What we did:** You asked to try the next idea on the same cash 21-day question: use WTI’s last 21-day up/down label as the call for Brent’s next 21 days, and the reverse. Each oil keeps its own scoreboard. The computer could pick **one** per oil only if that oil’s named cross-call already beat “the trend continues” on **older** days. On **WTI**, using Brent’s label **lost**. On **Brent**, using WTI’s label **beat** the older exam, so that one rule went to the recent exam and also beat continuation there on the three locked windows. The 250-day recent window was a **one-hit** margin. Burned rules were **not** brought back. 21 days was **not** changed. The recent exam was **not** used to train.

**What this settles:** Numeric discovery (and, on Brent only, confirm) hit-rates for this two-horse overlay. WTI-met ≠ Brent-met. Not a trade.

---

## 1. Vehicle (not a fail)

Reuse of existing `eia_spot_wti.csv` / `eia_spot_brent.csv`. Peer sign on all **500** discovery dates both boards (threshold 250 — **not** vehicle-fail). Clock: latest peer print with date **≤ t**, then carry. Flat/missing → continuation. Do **not** retune. Do **not** switch to a dollar spread or fade-of-peer after scores. Burned FLIP-HOLD / REV / INV **not** scored.

---

## 2. Discovery (locked before last-500 confirm)

Cutoff: issue dates **≤ 2023-08-21**. Scoreboard: last **500** eligible of that prefix (same dates as Track B pulses 1–2). Train arm: **N/A**.

### WTI (2021-08-24 … 2023-08-21) — horse **H-SPOT-CROSS-B2W**

Continuation: **0.508** (254 / 500).

| Horse | Hits | Hit-rate | Beats continuation? |
|-------|------|----------|---------------------|
| **H-SPOT-CROSS-B2W** | 247 | 0.494 | **no** |

**Survivor:** **none.** Confirm **skipped**. Row **burned**.

### Brent (2021-08-27 … 2023-08-21) — horse **H-SPOT-CROSS-W2B**

Continuation: **0.506** (253 / 500).

| Horse | Hits | Hit-rate | Beats continuation? |
|-------|------|----------|---------------------|
| **H-SPOT-CROSS-W2B** | 264 | 0.528 | **yes** |

**Survivor:** **H-SPOT-CROSS-W2B**. Confirm **ran** (this board only).

Do **not** pick B2W as least-bad on WTI. WTI-met ≠ Brent-met.

---

## 3. Confirm (Brent survivor only)

Horse **H-SPOT-CROSS-W2B** vs continuation. Last eligible prints of the **full** file. Confirm **never** trains. WTI confirm **not** run.

| Window | First … last | Horse | Continuation | Strictly greater? |
|--------|--------------|-------|--------------|-------------------|
| last **500** | 2024-07-24 … 2026-07-20 | **0.544** (272 / 500) | 0.522 (261 / 500) | **yes** (+11) |
| last **250** | 2025-07-21 … 2026-07-20 | **0.528** (132 / 250) | 0.524 (131 / 250) | **yes** (**+1** — tiny) |
| last **750** | 2023-07-28 … 2026-07-20 | **0.545** (409 / 750) | 0.525 (394 / 750) | **yes** (+15) |

Last **750** **overlaps** the discovery prefix (inherited confirm rule; not a re-hunt). Parent freeze: **tiny ≠ met**. The 250-day window is a **one-hit** margin.

**L-SCREEN-Y-PROMOTE:** **does not apply**.

Do **not** retune W2B after these numbers. Do **not** change 21. Do **not** unburn B2W. Do **not** add a dollar spread or fade-of-peer after scores.

---

## 4. Establishment-stop drill

**Would honest `04` declare unrestricted spot 21-day skill established (both boards)?** **No.** WTI failed discovery.

**Would honest `04` declare Brent-scoped P-NonNegligible skill established?** **No.** Confirm 250 is a one-hit margin (**tiny ≠ met**). Point estimate only. Stand-in reprints. Same-day peer sign is not a lead–lag theorem.

**Would honest `04` declare F-SKILL established?** **No.** This pulse did not score next-session CL RMSE.

**Would honest `04` declare those bars refuted?** **No.** A WTI miss is not “Brent never tracks WTI,” and a Brent point-beat is not “WTI leads Brent.”

Stop was **not** hit. Do **not** auto-declare bar-met. Do **not** auto-open DataMine.

---

## 5. Exploration queue (after scores)

Burned (add): **H-SPOT-CROSS-B2W** on **WTI**. FLIP-HOLD / REV / INV stay burned. **H-SPOT-CROSS-W2B** is a **Brent discovery survivor** (not burned; not a license to remix).

Next (not scored): **C-SPOT-LOGIT**.

---

## 6. Scripts / artifacts

- `scripts/spot_cross_hunt.py`  
- `data/spot_cross_hunt_scores.json` · `data/spot_trend_queue.json`  
- Reproduce: `python3 scripts/spot_cross_hunt.py --stage discovery` then (Brent survivor only) `python3 scripts/spot_cross_hunt.py --stage confirm`

---

*Not trading advice. Cross-bench ≠ spread. Tiny 250 ≠ met. Confirm is not a training arm. WTI-met ≠ Brent-met.*
