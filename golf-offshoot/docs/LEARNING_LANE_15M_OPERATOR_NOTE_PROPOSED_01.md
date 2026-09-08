# Operator note — RUN-ONLY of Lab PROPOSED 01 (fee hurdle)

**Verdict:** **RUN-ONLY** · Operator · 2026-09-07 21:40 EDT
**Not an ADMIT.** Not Softened. Not a dated record. Not a dashboard figure.
**Lane:** `learning_lane_15m` · series `KXBTC15M` only · `lab_admits=false` · Trading **NOT ARMED**
**Candidate:** [`LEARNING_LANE_15M_LAB_PROPOSED_01.md`](LEARNING_LANE_15M_LAB_PROPOSED_01.md)

This note is the only place the fee-accurate numbers may live. They do not go in `manifest.json`, the digest, the hub, `records[]`, or any dated record. The hurdle is a **cost**, not a signal: not an edge, not a hit rate, not evidence about method quality, and not evidence toward lifting the Founder HOLD.

---

## Ruling (this is the decision)

1. **The test runs.** It is deterministic, adds no loop code, quarantines output here, and carries four live falsifiers. The 21:05 "park it, do not schedule" instruction is superseded.
2. **Reading Kalshi's public fee schedule is inside public-read-only posture.** It is a documentation read of a Kalshi-hosted PDF. No key, no account, no login, no `/portfolio` `/orders` `/deposit` path. `assert_public_read_url` is an API-path guard and does not apply to this document URL. **F1 does not fire.**
3. **No fee-accurate figure is displayed on the dashboard.** Lab recommended that; Founder agreed; Operator so rules.

---

## Source for `k`

| | |
|---|---|
| URL | `https://kalshi.com/docs/kalshi-fee-schedule.pdf` |
| Retrieved | 2026-09-07 21:38 EDT |
| Also listed | `https://kalshi.com/fee-schedule` (same schedule; KXBTC15M is not named) |
| Formula | `fees = round up(M × 0.07 × C × P × (1 − P))` |
| `k` | **0.07** |
| `M` | **1** — default. `KXBTC15M` is not in the Non-Standard Fees table (nearby names `KXBTCMAX150` and `KXBTCY` are; this series is not) |
| Settlement fee | **None.** The document says "There is no settlement fee." Entry-side only |
| Rounding used here | Lab's stated rule: **round up to the cent** after `k × stake × (1 − mark)`. The PDF's "centicent" rule is noted and not used, so the hurdle is slightly **worse** than a finer rounding would print |
| Paper fill treated as | Immediately matched (mechanical YES at the posted mark). Taker formula, not maker |

If a later public schedule names a different `k` or a `KXBTC15M` override, this note is stale and must be re-run. Do not keep using 0.07 by habit.

---

## Arithmetic (lineage A settled books on this tree, 2026-09-07 21:38 EDT)

n = **24** settled `paper/KXBTC15M-*.json` with a `settled_at`. Stake is $1.00 on every fill. Lineage B's published `+1.67` is not in this table and is not summed into it.

| Window | Mark | Recorded pnl | Raw fee | Fee (ceil ¢) | Fee-accurate pnl |
|---|---:|---:|---:|---:|---:|
| `071545` | 0.9835 | +0.02 | 0.001155 | 0.01 | +0.01 |
| `071600` | 0.7050 | +0.42 | 0.020650 | 0.03 | +0.39 |
| `071615` | 0.6350 | −1.00 | 0.025550 | 0.03 | −1.03 |
| `071630` | 0.4650 | −1.00 | 0.037450 | 0.04 | −1.04 |
| `071645` | 0.6050 | −1.00 | 0.027650 | 0.03 | −1.03 |
| `071700` | 0.3850 | +1.60 | 0.043050 | 0.05 | +1.55 |
| `071715` | 0.6450 | +0.55 | 0.024850 | 0.03 | +0.52 |
| `071730` | 0.3350 | −1.00 | 0.046550 | 0.05 | −1.05 |
| `071745` | 0.5150 | −1.00 | 0.033950 | 0.04 | −1.04 |
| `071800` | 0.4950 | −1.00 | 0.035350 | 0.04 | −1.04 |
| `071815` | 0.4150 | −1.00 | 0.040950 | 0.05 | −1.05 |
| `071830` | 0.4250 | −1.00 | 0.040250 | 0.05 | −1.05 |
| `071845` | 0.4050 | −1.00 | 0.041650 | 0.05 | −1.05 |
| `071900` | 0.5150 | +0.94 | 0.033950 | 0.04 | +0.90 |
| `071915` | 0.4850 | +1.06 | 0.036050 | 0.04 | +1.02 |
| `071930` | 0.5750 | −1.00 | 0.029750 | 0.03 | −1.03 |
| `071945` | 0.4550 | +1.20 | 0.038150 | 0.04 | +1.16 |
| `072000` | 0.5550 | +0.80 | 0.031150 | 0.04 | +0.76 |
| `072015` | 0.4250 | −1.00 | 0.040250 | 0.05 | −1.05 |
| `072030` | 0.3850 | −1.00 | 0.043050 | 0.05 | −1.05 |
| `072045` | 0.4750 | +1.11 | 0.036750 | 0.04 | +1.07 |
| `072100` | 0.5550 | +0.80 | 0.031150 | 0.04 | +0.76 |
| `072115` | 0.4550 | +1.20 | 0.038150 | 0.04 | +1.16 |
| `072130` | 0.5950 | +0.68 | 0.028350 | 0.03 | +0.65 |

| | |
|---|---|
| Total stake | **$24.00** |
| Total raw fee | **$0.8058** |
| Total fee (ceil ¢) | **$0.94** |
| Fee / stake | **3.92%** |
| Per-fill fee | **$0.01 … $0.05** (none is $0.00) |
| Mean ceil-cent fee | **$0.039** |

**Hurdle.** At the $1 unit, any later selection rule on this lane has to beat about **four cents a fill** (more on cheap marks, less on marks near 1.0) before a positive paper pnl means anything against this omitted cost. That is bookkeeping. It is not a method result.

---

## Falsifiers

| # | Fired? | Why |
|---|---|---|
| F1 | **No** | `k` was read off the public Kalshi PDF above |
| F2 | **No** | No fill rounded to $0.00; minimum ceil-cent fee is $0.01 |
| F3 | **No** | Total fee is 3.92% of stake, not < 1% |
| F4 | **No** | Fee-accurate pnl is strictly worse than recorded pnl on every window |

No falsifier fired. The test is **complete as RUN-ONLY**, not closed on a falsifier, and **not admitted**. Nothing is invented. Golf idle stays ON. HOLD stands.
