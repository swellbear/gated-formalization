# Operator guide

Paper/mock only. The system **never auto-trades**. This offshoot sits beside Gated Progressive Formalization. It does not import golf-offshoot, Amb, gates, or `applications/`.

## Commands

```bash
cd options-offshoot
pip install -e ".[dev]"
pytest
python -m options_offshoot demo
python -m options_offshoot fields
python -m options_offshoot ingest --field spx_this_friday
python -m options_offshoot live --field earnings_us_week
python -m options_offshoot live --field spx_this_friday --quotes ibkr --lock-paper
python -m options_offshoot live --field spx_this_friday --compare-method
python -m options_offshoot paper-ledger --field spx_this_friday
python -m options_offshoot paper-deposit --field spx_this_friday --amount 500
python -m options_offshoot paper-withdraw --field spx_this_friday --amount 100
python -m options_offshoot paper-settle --field spx_this_friday
```

`--quotes` defaults to **polygon**. IBKR only when `--quotes ibkr` or `OPTIONS_QUOTES=ibkr`. IBKR is market data only — no orders. `--cash-out "O:AAPL...=1.50"` is a typed per-share bid. `--no-apply-paper` skips mock apply. Demo does not mint a lived lock.

Operating ingest/live need `MASSIVE_API_KEY` or `POLYGON_API_KEY` in `.env`. Demo is mock data.

Open PDFs in Edge, Chrome, or Adobe — not as source in the editor.

## How to read a table

1. Field freeze first (which tape).
2. Sort is **vs-ask** (model fair minus ask). Deep in-the-money calls will look like a favorite if you sort on P(ITM) — do not.
3. `n/a` = no real ask, too wide a spread, or below the size floor. Listed is not available.
4. Range `[low-high]` is uncertainty on **this snapshot**, not a day min/max.
5. Read leftover: used vs unconstrained vs held. HOLD with no bid is ride to expiry, not “edge intact.”
6. Fair, bid, ask are **per share**. Dollars = per-share × multiplier × whole lots.

## Paper

Independent $20k books: lived, A-replay, B-guts, B-nerves, B-full. Lived lock identity is `locked_at` + hash. `--compare-method` does not lock lived and does not write the lived ledger. Whole lots only. Settle at expiry: `n = floor(stake / (entry_ask * multiplier))`; value = intrinsic × multiplier × n; P/L = value − stake. Never auto-trade.

## Do not

- Merge bankrolls across fields.
- Allocate $20k to whichever index table looks fattest.
- Retune `t` because one expiry felt smart.
- Stuff earnings narrative, listed IV, r, dividends, or jumps into theta.
- Relabel Massive last_quote as IBKR.
