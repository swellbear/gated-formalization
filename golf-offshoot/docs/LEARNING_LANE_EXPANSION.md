# Learning-lane expansion

**This file is the SoT for opening another Kalshi series.**  
Park row 7, the protocol, leave-off, and the 15m lane doc point here. They do not restate the procedure. The 15m evidence bar already says Established does not license series expansion; this file is the lift checklist, not a bar amendment.

The Founder HOLD of 2026-09-07 stands: no series other than `KXBTC15M` until Founder lifts it. **This file does not lift that HOLD.** Writing it, citing it, or making `decide()` generic is not evidence toward lifting it.

## Expansion rule

Lifting the HOLD opens a **new lane**. It does not add a ticker to `learning_lane_15m`.

## What the new lane must have before any paper fill

- Its own public-read adapter (ticker parse, allowed series, settle SOURCE citation)
- Its own data root
- Its own digest + caveats
- Its own evidence bar and JSON
- Its own rule registry and burned-class list
- Its own fee-schedule pin (a later Kalshi PDF, a different `k`, or a series override is a different pin)
- Its own wake / ledger / paper / settlements

Trading ARMED, if ever, is per-lane and stays false until that lane’s own bind + lived L2 + Founder read-once.

## What may be reused

The role machine: wake, runner, clerical whitelist, `JUDICIAL_NEVER`, serve-on-proof, the critic *engine*, and the Operator / Lab / Critic protocol.

## What may not be reused

This lane’s ADMITs, RUN-ONLY notes as if they were evidence, skip bands, rule ids, δ, sd, n, power curve, calibration windows, holdout clock, or `CRITIC_01` / `CRITIC_02` answers.

A new bar needs a new attack from a session that did not draft it. Established on `KXBTC15M` does not license the new series, money, or keys.

## Different duration is a different lane

Weeklies, dailies, or a different clock are not `learning_lane_15m` with a longer window. They get their own n, calendar rule, and settle SOURCE.

## Books do not merge

No shared ledger. No combined bankroll. No lineage A/B mix across series. No second series on this lane’s globs or `PRIMARY_SERIES`.

## `decide()` stays generic in shape and single-series in data

Dispatch on declared `kind` and parameters, not `id == "R-SKIP-COINFLIP"`. Do not revive a burned class under a new name on the new lane. Generic shape is owed when it serves *this* series. It is not a reason to collect another series.

## Do not collect the new series “to get ready”

Marks on the tree before the rule and bar exist are informing marks. That is how `R-SKIP-COINFLIP` lost Established on L1.

## Preconditions to lift the HOLD

All of these, on **this** lane first:

1. The paper book obeys `rules.decide()`.
2. `fee_adjust()` is real and tested.
3. `trials_to_date` is mechanical.
4. The evidence bar is binding, or every failure is named on its face with Operator’s reason for binding anyway.
5. The factory has completed at least one lived declare → skip/fill → score cycle on `KXBTC15M` without Founder driving it.
6. The running hub is on that code.

“Digest matches ledger” and “the loop looks honest” are not the lift.

## Who

Only Founder lifts the HOLD. Operator, CoS, Lab, and a later bot reading a tidy tick cannot.

Lifting the HOLD is not arming and not a second hub. A second series does not share this lane’s process tree or publish surface until its own adapter and roots exist.

## Clone test

Adding a series to `ALLOWED_SERIES` / `PRIMARY_SERIES`, or globbing a second ticker into this lane’s paper/settle paths, is a red build until the new lane package exists.

Do not keep a backlog of future tickers in this file. A named ticker here reads as permission.
