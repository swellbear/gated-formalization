# Pulse result — baseline session RMSE vs no-change

**Date:** 2026-08-17  
**Application:** `2026-08_oil-futures-predictive-model`  
**Layer ID:** **L-PULSE-TAPE-0**  
**Named class:** `Lock_FSRC_Named_CME_Tape.md`  
**Live vs stand-in:** **Live tape not in hand.** No stand-in stipulated. **No numeric bar scored to met.**

---

## 0. Plain-language framing

**What we tried:** Download CME official CL front-month **open** and **settlement**, apply roll rule R1, compute how wrong “assume the move is zero” is on **night**, **day**, and the **whole trip**. If the same tape included CL1–CL18, optionally re-score Kearney–Shang with RMSE.

**What happened:** Official CME historical settlements are **licensed (DataMine)**. A public CME fetch from this environment **did not** return a usable series (HTTP/2 stream error; no file). We did **not** substitute Yahoo/`CL=F`. Kearney–Shang optional horse **not run** (needs the live curve tape).

**What this settles:** The class is named. This pulse is **not established** (cannot compute the locked RMSE without the tape). Not a refute of all recipes. Not a trade.

---

## 1. Formulas (ready when the tape exists)

Same-contract stamps; drop roll-jump rows per R1.

```
r_ON,t  = ln(Open_t / Settle_{t-1})
r_DAY,t = ln(Settle_t / Open_t)
r_CC,t  = ln(Settle_t / Settle_{t-1})
```

When the open sits between consecutive settlements on the **same** contract: `r_CC,t ≈ r_ON,t + r_DAY,t`.

No-change forecast = `0`.  
`RMSE_w = sqrt( mean( r_w^2 ) )` on the walk-forward (or pre-declared holdout) sample.  
A zero forecast has no fitted parameters; still **declare** the OOS window in advance (recommended: last 500 sessions after a burn-in, plus 250/750 sensitivity — same spirit as Kearney–Shang).

---

## 2. Results this pulse

| Window | RMSE vs no-change | n | Notes |
|--------|-------------------|---|--------|
| **F-ON** | **Not computed** | — | Live open/settle absent |
| **F-DAY** | **Not computed** | — | Live open/settle absent |
| **F-CC** | **Not computed** | — | Live settle-to-settle absent |
| Kearney–Shang FTS RMSE (optional) | **Not run** | — | Needs CL1–CL18 on the same official tape |

**Walk-forward:** Not executed (no series).  
**Vs last-settlement no-change:** The baseline **is** that forecast; beating it was not scored.

---

## 3. Fetch log (honest)

| Attempt | Outcome |
|---------|---------|
| CME DataMine historical EOD | Paid entitlement; no API ID in this environment |
| `https://www.cmegroup.com/markets/energy/crude-oil/light-sweet-crude.html` | curl HTTP/2 INTERNAL_ERROR; empty body |
| Yahoo / `CL=F` / generic vendor | **Not used** (stand-in, not stipulated) |

---

## 4. Establishment-stop drill

**Would honest `04` declare F-ON / F-DAY / F-CC / F-SKILL established?** **No.**

No numbers. A missing tape is not a pass. Print-match of Kearney–Shang 2009–15 MAE is still kinship.

**Would honest `04` declare those bars refuted?** **No.** Not computed ≠ every model fails.

---

## 5. Script (dormant until a live or stipulated CSV exists)

`scripts/cl_session_rmse.py` — expects columns `date,open,settle,front_id` (ISO date, floats, contract code). Applies R1 when `front_id` changes. Does not fetch the web.

---

*Not trading advice. Naming ≠ clearance. Stand-in not silently used.*
