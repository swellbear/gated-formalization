# Decision Layer + Dynamic Strategy System

Optional, advisory-only. Lives in `src/golf_offshoot/strategy/` plus schemas in `src/golf_offshoot/models/strategy.py`. The per-bet `decision/` screen (pass / consider / strong_consider) still runs; this layer **constructs and manages a book**.

**Never auto-bets.** `StrategyConfig.enabled=False` (default) is pure analysis.

## A. Where it lives

```
golf-offshoot/src/golf_offshoot/
  decision/          existing screens (unchanged contract)
  strategy/
    engine.py        on/off facade, journal helper, formatter
    builder.py       pre-tournament construction
    live.py          Thursday→Sunday actions
    cashout.py       optional user-typed cash-out vs remaining winner EV
    path.py          entry vs live edge, runners, collapse
    correlation.py   cut-risk / weather / style / talent-band
    sizing.py        Kelly × uncertainty × reliability × risk × mode
    status.py        heat controls + status summary
    explanations.py  plain-language “why this action”
  models/strategy.py schemas
```

Pipeline: `GolfOffshootPipeline(..., strategy_config=...)` and `run(..., open_book=..., strategy_config=...)`. Audit freeze: `AuditRecord.strategy` + `user_strategy_decisions`.

## B. Core schemas

- `StrategyConfig` — enabled, mode, risk, bankroll, allowed bet types, `DrawdownControls`
- `StrategyPosition` — user-recorded or **proposed** stake (proposed ≠ booked)
- `PortfolioState` — bankroll, open positions, realized P/L today/event
- `PositionMark` — entry vs live edge, MTM, runner / collapsed / improved
- `StrategyAction` — hold / reduce / exit / add / reallocate / new_bet / no_action + `reason`
- `StrategyRecommendation` — actions, proposed positions, marks, concentrations, status
- `StrategyStatusSummary` — exposure, unrealized, biggest concentration, posture
- `UserStrategyDecision` — accept/reject log; `placed_by_user=True`

## C. Pre-tournament construction

Uses ranked outputs + market edge + reliability. Candidates must pass the existing decision screen. Size = fractional Kelly on a **range-haircut** probability × quality × risk × mode, capped by single-position and total-exposure limits. Cut-risk stacking is skipped. Output is `NEW_BET` suggestions, not tickets.

## D. Live recommendations

For each open position: mark entry vs live edge, then

| Situation | Typical action |
|-----------|----------------|
| User-typed cash-out ≥ remaining winner EV (plus mode buffer) | EXIT (take the quote) |
| User-typed cash-out below remaining winner EV | HOLD (do not sell early); ADD still possible if live edge improved |
| Original edge collapsed (no cash-out quote) | EXIT (Press may REDUCE) |
| Cooling-off | HOLD / REDUCE only — no ADD / NEW_BET |
| Runner + Protect Profits (no cash-out quote) | REDUCE (lock) |
| Live edge improved + Press | ADD (unless range/reliability block) |
| Better name not in book, at cap | REALLOCATE from worst live edge |
| Fresh edge, capacity left | NEW_BET |

`--cash-out "Name=12.40"` is optional and case-by-case. It is a number you copy from Open Bets, not a public coupon field. Without it, MTM stays `stake × entry_decimal / live_decimal`. Applied paper reduce/exit without a typed quote books an estimated cash-out (odds-ratio MTM on the sold slice, 20% haircut on the gap; labeled estimated). A cash-out EXIT does not auto-redeploy; new names still must clear screens.

## E. Path, realized vs unrealized, correlation

- **Path:** a position that has already run (MTM ≥ 25% of stake) is not treated like a fresh edge of similar size.
- **Edges:** `PositionMark.entry_edge` vs `live_edge`; collapse if live < 30% of entry or negative; improved if live ≥ entry + 1.5pp.
- **Unrealized P/L:** MTM ≈ `stake × entry_decimal / live_posted_decimal` when posted odds exist; otherwise `1 / implied_fair`. A typed cash-out quote for that snapshot replaces MTM with that dollar amount.
- **Cash-out vs hold:** expected full payout ≈ live Win% × stake × lock decimal. Stay Selective sells only if the quote beats that EV by 10% **or** beats the high end of the Win interval, whichever is stricter (capped at max win payout). Protect Profits sells if quote ≥ central EV. Press requires a fatter quote. Missing quote: this comparison is skipped.
- **Correlation:** share of book in high cut-risk / make-cut, weather-sensitive names, same-style SG cluster, talent band.

## F. How modes change behavior

| Mode | Bias |
|------|------|
| **Protect Profits** | Smaller size; REDUCE runners; do not ADD into a live move |
| **Press Edges** | Larger size; HOLD/ADD runners when live edge improved; slightly higher cut-stack tolerance |
| **Stay Selective** | Mid size; act only on strong remaining edges |

Risk preference (conservative / normal / aggressive) scales size and exposure caps independently of mode.

## G. Assumptions and open questions

**Assumptions**

- Open positions are **user-recorded**. The engine never writes a `BetRecord`.
- MTM uses live posted decimal when present, otherwise a de-juiced implied ratio, unless the operator types a cash-out quote for that live snapshot.
- Style correlation is cosine similarity on the four SG categories, not a fitted copula.
- Cooling-off uses realized P/L the user (or a future feed) puts on `PortfolioState`.
- Default strategy layer is **off**.
- Leftover callout after live/ingest/pressure-test is display-only (used vs unconstrained vs held-ticket residual); see [PARKED_LEFTOVER_CALLOUT.md](PARKED_LEFTOVER_CALLOUT.md).

**Open**

1. Per-round “which round just finished” for the “after Round 1” wording (today: live mode).
2. Whether make-cut and win books should have separate exposure caps.
3. Fitted finish copula vs current θ / SG / cut-risk slices.
4. Authenticated Open Bets scrape (not planned; type the quote instead).

CLI: `python -m golf_offshoot strategy --bankroll 2000 --mode press_edges --live`
