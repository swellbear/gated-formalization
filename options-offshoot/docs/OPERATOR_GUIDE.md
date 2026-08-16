# Operator guide

Paper/mock only. The system **never auto-trades**. This offshoot sits beside Gated Progressive Formalization. It does not import golf-offshoot, Amb, gates, or `applications/`.

## Ready only for observation

Use it to freeze a **predeclared field**, list contracts that have a real ask, and paper a $20,000 book **per field per path**. Do not treat P(ITM) as a rank. Do not shop the `fields` index.

## Commands

```bash
cd options-offshoot
pip install -e ".[dev]"
pytest
python -m options_offshoot demo
python -m options_offshoot fields
python -m options_offshoot ingest --field spx_this_friday
python -m options_offshoot live --field earnings_us_week
```

Operating ingest/live need `POLYGON_API_KEY` in `.env`. Demo is mock data.

Open PDFs in Edge, Chrome, or Adobe — not as source in the editor.

## How to read a table

1. Field freeze first (which tournament).
2. Sort is **vs-ask** (model fair minus ask). Deep in-the-money calls will look like a favorite if you sort on P(ITM) — do not.
3. `n/a` = no real ask, too wide a spread, or below the size floor. Listed is not available.
4. Range `[low-high]` is uncertainty on **this snapshot**, not a day min/max.
5. Read the leftover callout: used vs unconstrained vs held.

## Paper

Independent $20k books: lived, A-replay, B-guts, B-nerves, B-full. HOLD with no live ask rides to **expiry**. That is not a cash-out. Never auto-trade.

## Do not

- Merge bankrolls across fields.
- Allocate $20k to whichever index table looks fattest.
- Retune `t` because one expiry felt smart.
- Stuff earnings narrative or blog IV into the model.
