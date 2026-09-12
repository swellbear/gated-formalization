# Hub desk

Lock for the local operator shell at `127.0.0.1:8765` (`python -m golf_offshoot shell`). Founder screenshots are judged against this file. Hub-ui reads it first.

## What it is

One hub process, many Kalshi lanes, `?lane=<id>`. Golf and 15-min Kalshi are the first two registrations. A later family is another registration of the same shell.

Shared chrome: tokens, header, session strip, blotter region, Glance vs Cockpit, in-place watch patch. Each lane brings its own book, session fields, blotter columns, optional meters, and optional organs.

Omitted `?lane=` is golf. A registered id opens that desk. `golf_kalshi` is an alias for golf (the data folder name). An explicit unknown id is a miss slot.

## Home

At 1920×1080, Home is one header row (~40px) + one session row (~48px) + this lane’s blotter. The ticket table (or 15m trial glance + this-window + last-thing) is visible without scrolling.

- **Glance** is the default.
- **Cockpit** is thinking / learning / tape.
- Catalog is a drawer. Series market rows load when the series is opened.

Other views hide Home. View is `data-view`, stored per lane in `sessionStorage`.

## Session strip

Slots the shell always has a place for: watch, Eastern clock, bankroll, P/L, open count, closed count, halt. A lane may add fees, meters, or a one-line mix.

Golf Home also shows Fast / week / slow meters and the mix one-liner. Meter caps are `sizing_bank` targets for the live book, not the seed $50/$100/$50 card. The mix line includes last-tick skip counts from `last_tick.json` even when tickets are open. Full hunt copy stays in Cockpit (Scoreboard). Golf Farm / Honer stay idle shells: they point at Home / Scoreboard tape and do not say the book is empty when tickets exist.

15m Home is a one-line trial glance + this-window + Factory last-thing and money. Disagreements and “What it is / where it stands” fold closed. The full learning card stays on Lab — Home is not a verdict. This-window heading is **one clock** while `consult_enabled` is not true; Honer search/exam are labeled observation. Factory Scoreboard / Ops spine title is **fill-all baseline** when the executing row does not `selects`, and **live 70** only when a selecting rule is on the chair. The paper-window PNG is Scoreboard. Spine, clock legend, and journal sit in Cockpit or Ops. 15m Farm’s first column is the notebook, parked/score-owed/collecting, skip rate and failed clauses, and n/70. Kind/params/date sit beside it. No farm pnl column.

Golf **Live/entry $** is dollar EV after fee (`edge_after_fee`), not a 3pp fraction. Format two decimals. Quotes under 2¢ show `thin`; the quote stays in Quote. Do not retune mark math for the column.

Golf Scoreboard is the closed-ticket tape (the 15m strip analog): when, player, result, after-fee P/L. Halt log sits under it. Home blotter stays open tickets. Session Closed is the count.

## Numbers

Session and blotter bind existing collectors: `collect_board`, `ledger.json`, watch, last_tick, this-window, Factory standing. Missing is `—` or a status line. Empty golf blotter is “no open tickets”.

## Look

One token sheet (`desk.css`):

`--bg`, `--panel`, `--ink`, `--muted`, `--line`, `--up`, `--down`, `--halt`, `--watch`, `--mono`, `--sans`

Money and tickers use `--mono` and `tabular-nums`. Labels use `--sans`. Header is one compact bar. Quiet `PAPER` chip. Labels and values.

## Switcher

The switcher loops the registry. Two to seven lanes are tabs. Clicking a lane is `GET /?lane=<id>`.

## Watch

`/api/watch?lane=<id>` returns that lane’s session and blotter from disk. The page swaps `#desk-session` and `#desk-blotter` when the fragment hash changes. Clock, tab, scroll, and open catalog rows stay. A hub process restart is a full reload.

## Voice

Labels and values. Empty board is status, not policy.
