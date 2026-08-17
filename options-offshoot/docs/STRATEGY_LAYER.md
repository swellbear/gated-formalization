# Strategy layer (advice only)

Never auto-trades. Never a broker order. Mock paper apply is not a ticket.

Lives in `src/options_offshoot/strategy/`. Default mode `stay_selective`, risk `conservative`, frozen in method law.

## Actions

| Kind | When |
|------|------|
| NEW | vs-ask (or path screen) clears `t`; whole lots under caps |
| HOLD | live mark exists and edge intact; **or** no venue bid (unmarked ride to expiry — not “edge intact”) |
| SELL / EXIT | typed `--cash-out` or live **bid** beats hold-to-expiry value |
| ADD | live vs-ask improved vs entry; not in Protect Profits |
| REDUCE | Protect Profits on a runner (MTM already up) |
| REALLOCATE | at total cap, from worst live vs-ask to a name that clears; inside the field |

NEW/ADD lift the **ask**. SELL/EXIT/REDUCE use the **bid** or typed cash-out. Mid is never a cash-out.

Stay Selective cash-out: bid proceeds must beat remaining expected payoff × multiplier × n by **10%**. Protect Profits: bid ≥ central EV. Press: 20% buffer. No bid → do not invent a sell.

## Caps (law, not Kelly)

- `max_single_position_frac=0.05`
- `max_same_underlying_frac=0.10` (two strikes on one ticker are one stack)
- `max_total_exposure_frac=0.40`
- conservative haircut `0.70`
- round **down** to whole lots; leftover **can't size** if one lot exceeds room

## Trigger page

SELL → REALLOCATE → PARTIAL SELL → ADD → NEW → HOLD (omit empty). HOLD has no dollars.

Auto-apply mock paper when the **actionable** set changes. HOLD-only does not. `--no-apply-paper` skips. Demo does not mint a lived lock.

## CLI

`live` / `ingest` always print advice. `--mode stay_selective|protect_profits|press_edges`. `--cash-out "contract_id=1.50"`.
