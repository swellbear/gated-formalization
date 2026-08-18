# Known limitations

- Pricing is a terminal-spot Monte Carlo with one σ. Not a vol surface. r=0 and no dividends stay **leftover**, not a finished model.
- Calendar DTE, not remaining session hours. Earnings jumps and American early exercise are unconstrained.
- Operator freeze files are not a live index reconstitution. If N is not the S&P, leftover says so. Not Wikipedia.
- Illiquid strikes stay n/a. Listed ≠ available. Do not invent a bid from last.
- Honesty ≠ better. B-guts can lose more paper.
- Index is a map. Shopping the fattest table is forbidden.
- No hunter. News, blogs, “should be in” stay unconstrained.
- Does not import GPF or golf-offshoot. Does not auto-trade. IBKR never places an order.
- Settle is expiry. Marks are not the result.
- n=1 tape. Do not move `t` from one expiry.
- IBKR overlay needs TWS/Gateway. 15-minute delayed bid/ask is admitted (leftover: not live OPRA, not Massive Advanced). Tests mock it. CI does not require Gateway.
- Option chain snapshot is Options Starter+. `last_quote` / `/v3/quotes` stay omitted/403 without Advanced. Do not pay Advanced just for delay — use IBKR delayed. No invented mid. Massive MCP / websocket are not on the operating path.
