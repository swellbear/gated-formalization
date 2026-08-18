# Data feeds

## Contract

Operating path needs a **real bid and ask**, or the row is `n/a`.

Named REST vendor is **Massive** (Polygon.io rebrand, Oct 2025). Same keys. Host `https://api.massive.com` (legacy `api.polygon.io` still works). Docs: https://massive.com/docs/rest/llms.txt

Do **not** use Massive MCP, websocket, or the Python SDK on the operating path. Thin HTTP only. Never auto-trade.

| Need | Source | If missing |
|------|--------|------------|
| Options chain + OI/volume/specs | `GET /v3/snapshot/options/{ticker}` (Options Starter+) | leftover; not a fake mid |
| Contract index / nearest expiry | `GET /v3/reference/options/contracts` (all Options plans) | leftover |
| Venue ask/bid you would lift/hit | Massive `last_quote` if the plan includes quotes; else IBKR overlay when asks are missing or `--quotes ibkr` | leftover; never invent mid from `day.close`; Massive last_quote is **not** IBKR |
| Spot | `GET /v2/aggs/ticker/{ticker}/prev` daily close | leftover: not NBBO; stocks snapshot 403 |
| Realized vol | `GET /v2/aggs/ticker/{ticker}/range/1/day/...` | A may use default σ (flag `default_sigma`); honest path unconstrained |
| Earnings calendar | `GET /benzinga/v1/earnings` (Benzinga expansion) | Frozen file + leftover **not this week's earnings** |
| S&P-style universe | Operator freeze `data/fields/spx_this_friday.txt` | leftover **operator freeze of N, not the S&P** |

Key: `MASSIVE_API_KEY` or `POLYGON_API_KEY` in `options-offshoot/.env`. Never commit `.env`. Do not paste the key into chat.

Option chain snapshot is **not** on Options Basic. `last_quote` / `/v3/quotes` are **not** on Starter (need Options Advanced). Starter 15-minute delay is chain/OI/day recency, not delayed NBBO. Our max-stale is 15 minutes for cached HTTP. Do not invent an ask from `day.close`.

IBKR: optional extra `pip install ib-insync`. **Market data only. No `placeOrder`.** When Massive `last_quote` is missing (Starter has chain, not quotes), overlay IBKR bid/ask. **15-minute delayed IBKR is admitted** with leftover (not live OPRA, not Massive Advanced). Live OPRA used if TWS has it. Start TWS/Gateway with API enabled.

**Refuse on operating path:** Yahoo, HTML scrape, open web, Wikipedia, Massive MCP as a hunter, websocket.

HTTP cache: ingest 600s, live 45s, vol 6h. Quotes older than 15 minutes are unavailable. Cache key hashes the URL **without** `apiKey`. Paginate `next_url` (cap leftover “chain truncated”).
