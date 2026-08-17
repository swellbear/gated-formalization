# Pulse result — Yahoo CL=F stand-in session RMSE vs no-change

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Layer ID:** **L-PULSE-STANDIN-1**  
**Locks:** `Lock_Standin_Yahoo_CLF.md` · `Lock_FSRC_Named_CME_Tape.md`  
**Live vs stand-in:** **Stand-in stipulated.** Yahoo `CL=F` Open/Close. **Not** official CME settlement. **No print scored to met.**

---

## 0. Plain-language framing

**What we did:** You allowed Yahoo `CL=F` as a weaker tape. We downloaded daily Open and Close, treated Close as settlement, and measured how wrong “assume the move is zero” is on **night**, **day**, and the **whole trip**.

**What this settles:** Baseline RMSE **numbers** on a **stand-in** tape. Skill is still **not shown** (no model was scored against this baseline). Not a trade.

---

## 1. Sample

| Item | Value |
|------|--------|
| Source | Yahoo chart API `CL=F` daily (`interval=1d`) |
| Artifact | `data/clf_yahoo_standin.csv` · `data/clf_yahoo_standin_fetch.json` |
| Raw bars | 6603 (2000-08-23 … 2026-08-17) |
| CSV rows | **6520** after dropping 80 null, 2 non-positive (incl. Apr 2020), 1 in-progress 2026-08-17 bar |
| Used range | **2000-08-23 … 2026-08-14** |
| `front_id` | constant `CL=F` — **R1 never fires** |
| Declared OOS | last **500** sessions: **2024-08-20 … 2026-08-14** |
| Sensitivity | last 250 (2025-08-18 … 2026-08-14) and last 750 (2023-08-22 … 2026-08-14) |

Same-contract identity on this generic: `r_CC = r_ON + r_DAY` (max abs error last 500: ~1e-16).

---

## 2. Results — RMSE of a 0 forecast (stand-in)

Primary window = last 500 sessions.

| Window | RMSE (500) | n | RMSE (250) | RMSE (750) | RMSE (full 6519) |
|--------|------------|---|------------|------------|------------------|
| **F-ON** | **0.01291** | 500 | 0.01672 | 0.01088 | 0.01068 |
| **F-DAY** | **0.02663** | 500 | 0.03093 | 0.02396 | 0.02383 |
| **F-CC** | **0.02869** | 500 | 0.03436 | 0.02569 | 0.02623 |
| Kearney–Shang FTS | **Not run** | — | — | — | needs CL1–CL18 |

On this stand-in tape, **day RMSE is larger than overnight**, not smaller. Do **not** promote that to “daytime is easier” or F-DAY-met. Yahoo Open/Close ≠ official open/settle.

**Vs last-settlement no-change:** These numbers **are** that baseline. Beating it was **not scored**.

---

## 3. Fetch log

| Attempt | Outcome |
|---------|---------|
| Yahoo v8 chart `CL=F` `interval=1d` `period1=2000-01-01` | HTTP 200; 6603 bars; used |
| Yahoo v7 download CSV | HTTP 401; unused |
| CME DataMine | Still not in hand; not this pulse |

Fetched **2026-08-17T19:22:36Z**. Exchange meta: NYM / FUTURE.

---

## 4. Establishment-stop drill

**Would honest `04` declare F-ON / F-DAY / F-CC / F-SKILL established?** **No.**

A baseline RMS on a stand-in tape is not P-NonNegligible skill vs last settlement. A horse that beats these RMSEs was not run. Stand-in ≠ live.

**Would honest `04` declare those bars refuted?** **No.** Measuring the baseline does not prove every model fails.

---

## 5. Script

`scripts/cl_session_rmse.py` on `data/clf_yahoo_standin.csv`.

---

*Not trading advice. Stand-in ≠ live. Numbers ≠ skill-met.*
