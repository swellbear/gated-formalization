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
| Original edge collapsed | EXIT (Press may REDUCE) |
| Cooling-off | HOLD / REDUCE only — no ADD / NEW_BET |
| Runner + Protect Profits | REDUCE (lock) |
| Live edge improved + Press | ADD (unless range/reliability block) |
| Better name not in book, at cap | REALLOCATE from worst live edge |
| Fresh edge, capacity left | NEW_BET |

## E. Path, realized vs unrealized, correlation

- **Path:** a position that has already run (MTM ≥ 25% of stake) is not treated like a fresh edge of similar size.
- **Edges:** `PositionMark.entry_edge` vs `live_edge`; collapse if live < 30% of entry or negative; improved if live ≥ entry + 1.5pp.
- **Unrealized P/L:** MTM ≈ `stake × entry_decimal / live_decimal`.
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
- MTM uses a simple decimal-odds ratio (not a full exchange cash-out model).
- Style correlation is cosine similarity on the four SG categories, not a fitted copula.
- Cooling-off uses realized P/L the user (or a future feed) puts on `PortfolioState`.
- Default strategy layer is **off**.

**Open**

1. Exchange cash-out / lay prices vs book decimal for true MTM.
2. Per-round “which round just finished” for the “after Round 1” wording (today: live mode).
3. Whether make-cut and win books should have separate exposure caps.
4. Fitted finish copula vs current θ / SG / cut-risk slices.

CLI: `python -m golf_offshoot strategy --bankroll 2000 --mode press_edges --live`
