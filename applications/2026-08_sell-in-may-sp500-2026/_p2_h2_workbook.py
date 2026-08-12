"""
Phase 2 Attempt 1 — Rank 1 H2 workbook
Lock: H2 (S&P TR post-1986), R1 T-bill May-Oct, F3 proxy, M1 Sharpe
Calendar: last trading day April exit; last trading day October re-enter
"""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

OUT = Path("applications/2026-08_sell-in-may-sp500-2026/P2_Attempt1_H2_Workbook_Numbers.md")

# --- data ---
sp = yf.download("^SP500TR", start="1986-01-01", progress=False, auto_adjust=True)
if sp.empty:
    # Fallback: SPY total-return proxy via adjusted close from late 1993
    sp = yf.download("SPY", start="1993-01-29", progress=False, auto_adjust=True)
    series_name = "SPY adj-close (TR proxy; starts 1993)"
else:
    series_name = "^SP500TR"

# yfinance multiindex columns sometimes
if isinstance(sp.columns, pd.MultiIndex):
    close = sp["Close"]
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
else:
    close = sp["Close"] if "Close" in sp.columns else sp["Adj Close"]

close = close.dropna().astype(float)
close.name = "px"

# 3M T-bill secondary market rate (^IRX is discount yield; use as rough T-bill income proxy annualized %)
irx = yf.download("^IRX", start="1986-01-01", progress=False, auto_adjust=True)
if isinstance(irx.columns, pd.MultiIndex):
    irx_c = irx["Close"]
    if isinstance(irx_c, pd.DataFrame):
        irx_c = irx_c.iloc[:, 0]
else:
    irx_c = irx["Close"]
irx_c = irx_c.dropna().astype(float) / 100.0  # to decimal annualized

# Align
df = pd.DataFrame({"sp": close}).join(irx_c.rename("tbill_ann"), how="left")
df["tbill_ann"] = df["tbill_ann"].ffill()

# Daily T-bill simple return approx
df["tbill_daily"] = (1.0 + df["tbill_ann"]) ** (1.0 / 252.0) - 1.0
df["sp_ret"] = df["sp"].pct_change()

# --- seasonality G1*: six-month windows ---
# Nov-Apr window ending year Y: from last TD Oct (Y-1) close to last TD Apr Y close
# May-Oct window year Y: from last TD Apr Y close to last TD Oct Y close

def last_td_in_month(idx: pd.DatetimeIndex, year: int, month: int):
    m = idx[(idx.year == year) & (idx.month == month)]
    return m.max() if len(m) else None


idx = df.index
years = range(1987, idx.max().year + 1)  # need prior Oct for first Nov-Apr

winter_rets = []  # Nov-Apr
summer_rets = []  # May-Oct
rows = []

for y in years:
    oct_prev = last_td_in_month(idx, y - 1, 10)
    apr = last_td_in_month(idx, y, 4)
    oct = last_td_in_month(idx, y, 10)
    if oct_prev is None or apr is None or oct is None:
        continue
    if oct_prev not in df.index or apr not in df.index or oct not in df.index:
        continue
    # only post-1986 publication sample: start with windows beginning Nov 1986
    if oct_prev < pd.Timestamp("1986-10-01"):
        continue
    w = df.loc[apr, "sp"] / df.loc[oct_prev, "sp"] - 1.0
    s = df.loc[oct, "sp"] / df.loc[apr, "sp"] - 1.0
    winter_rets.append(w)
    summer_rets.append(s)
    rows.append({"year": y, "winter_nov_apr": w, "summer_may_oct": s, "gap_w_minus_s": w - s})

season = pd.DataFrame(rows)
g1_winter_mean = float(np.mean(winter_rets)) if winter_rets else float("nan")
g1_summer_mean = float(np.mean(summer_rets)) if summer_rets else float("nan")
g1_gap = g1_winter_mean - g1_summer_mean
g1_pass = g1_gap >= 0.02

# --- strategy vs B&H annual Nov1-Oct31 style years ---
# Position: equity from day after Oct exit through Apr exit; T-bill from day after Apr exit through Oct exit
# Implement: at close of last TD Apr -> 0 equity; at close last TD Oct -> 1 equity

pos = pd.Series(index=df.index, dtype=float)
# default: start unknown; set chronologically
equity = 0.0  # start before first Oct 1986 signal — begin after first October
first = True
for dt in df.index:
    if dt.month == 10 and last_td_in_month(idx, dt.year, 10) == dt:
        equity = 1.0
    elif dt.month == 4 and last_td_in_month(idx, dt.year, 4) == dt:
        equity = 0.0
    pos.loc[dt] = equity

# returns: use previous day position for today's return (signal at close)
pos_lag = pos.shift(1)
# Before first signal, treat as buy-and-hold equity for fairness from sample start after first Oct
first_oct = last_td_in_month(idx, 1986, 10)
if first_oct is not None:
    pos_lag.loc[:first_oct] = 1.0

strat_ret = pos_lag * df["sp_ret"] + (1.0 - pos_lag) * df["tbill_daily"]
bh_ret = df["sp_ret"]

# Sample from first day after Oct 1986
start = first_oct
if start is not None:
    strat_ret = strat_ret.loc[start:].iloc[1:]
    bh_ret = bh_ret.loc[start:].iloc[1:]
pos_lag_s = pos_lag.reindex(strat_ret.index)

# Pre-tax Sharpe (daily -> annualized)
rf_daily = df["tbill_daily"].reindex(strat_ret.index)


def sharpe(r, rf):
    ex = r - rf
    ex = ex.dropna()
    if len(ex) < 50 or ex.std() == 0:
        return float("nan")
    return float(np.sqrt(252) * ex.mean() / ex.std())


sharpe_strat = sharpe(strat_ret, rf_daily)
sharpe_bh = sharpe(bh_ret, rf_daily)

# CAGR / vol
def cagr(r):
    r = r.dropna()
    if len(r) == 0:
        return float("nan")
    wealth = (1 + r).prod()
    years_n = len(r) / 252.0
    return float(wealth ** (1 / years_n) - 1) if years_n > 0 else float("nan")


def ann_vol(r):
    r = r.dropna()
    return float(r.std() * math.sqrt(252)) if len(r) else float("nan")


cagr_s, cagr_b = cagr(strat_ret), cagr(bh_ret)
vol_s, vol_b = ann_vol(strat_ret), ann_vol(bh_ret)

# F3 proxy: tax drag on switches — approximate short-term tax on equity gains realized at April exits
# Method: each April exit, tax = tau * max(0, gain since prior October entry) / equity_value, applied as wealth haircut
# Track lot from Oct entry price; on Apr exit pay tax on gain; remaining redeployed to T-bills conceptually via return stream haircut that day

TAU = 0.32  # ordinary/short-term federal+state rough proxy
COST = 0.001  # 10 bps round-trip per switch (half on exit, half on entry) = 0.05% each side -> use 0.001 total per switch event pair / 2

strat_after = strat_ret.copy()
# Apply costs on switch days
for y in range(1987, idx.max().year + 1):
    apr = last_td_in_month(idx, y, 4)
    oct = last_td_in_month(idx, y, 10)
    for sw in (apr, oct):
        if sw is not None and sw in strat_after.index:
            # one-way cost 5 bps
            strat_after.loc[sw] = (1.0 + strat_after.loc[sw]) * (1.0 - 0.0005) - 1.0

# Tax haircut on April exits: need path of equity prices between Oct and Apr
wealth_path_note = []
# Rebuild after-tax strategy by simulating wealth
w = 1.0
w_bh = 1.0
entry_px = None
in_eq = False
after_tax_rets = []
bh_rets_list = []
dates = list(strat_ret.index)
for i, dt in enumerate(dates):
    # detect if this day is switch close day
    is_apr = dt.month == 4 and last_td_in_month(idx, dt.year, 4) == dt
    is_oct = dt.month == 10 and last_td_in_month(idx, dt.year, 10) == dt
    r_sp = float(df.loc[dt, "sp_ret"]) if dt in df.index else 0.0
    r_tb = float(df.loc[dt, "tbill_daily"]) if dt in df.index else 0.0
    # position entering day = lag
    # Use same pos_lag
    p = float(pos_lag_s.loc[dt]) if dt in pos_lag_s.index and not math.isnan(pos_lag_s.loc[dt]) else 0.0
    r = p * r_sp + (1 - p) * r_tb
    # cost on switch days
    if is_apr or is_oct:
        r = (1 + r) * (1 - 0.0005) - 1
    w *= 1 + r
    # tax on April exit: tax unrealized gain from last October entry on the equity sleeve
    if is_apr and entry_px is not None:
        px = float(df.loc[dt, "sp"])
        gain_frac = max(0.0, px / entry_px - 1.0)
        # equity sleeve was 100% until exit — tax on gain portion of wealth
        tax = TAU * gain_frac * (entry_px / px)  # tax relative to end wealth if gain on full NAV
        # simpler: tax = tau * max(0, w_equity_gain). With 100% equity into the day:
        # approximate tax_amount / w_before_tax_on_gain = tau * gain_frac / (1+gain_frac)
        tax_frac_of_nav = TAU * gain_frac / (1.0 + gain_frac) if gain_frac > 0 else 0.0
        w *= 1.0 - tax_frac_of_nav
        r_eff = (1 + r) * (1.0 - tax_frac_of_nav) - 1.0
    else:
        r_eff = r
    if is_oct:
        entry_px = float(df.loc[dt, "sp"])
        in_eq = True
    if is_apr:
        in_eq = False
        entry_px = None
    after_tax_rets.append(r_eff)
    w_bh *= 1 + r_sp
    bh_rets_list.append(r_sp)

at = pd.Series(after_tax_rets, index=dates)
bh2 = pd.Series(bh_rets_list, index=dates)
# B&H tax: Rank-1 F3 compares taxable switcher vs B&H; B&H may defer — use pre-tax B&H as baseline (favorable to strategy comparison honesty: strategy bears tax, B&H deferral advantage)
sharpe_strat_at = sharpe(at, rf_daily.reindex(at.index))
sharpe_bh2 = sharpe(bh2, rf_daily.reindex(bh2.index))
cagr_at = cagr(at)
cagr_bh2 = cagr(bh2)

# B&H with deferred tax realization only at end (long-term rate 20%)
TAU_LT = 0.20
# terminal tax on cumulative gain
term_gain = max(0.0, w_bh - 1.0)
w_bh_at = w_bh - TAU_LT * term_gain
# approximate B&H after-tax CAGR from after-tax terminal wealth
n_years = len(bh2) / 252.0
cagr_bh_at = float(w_bh_at ** (1 / n_years) - 1) if n_years > 0 else float("nan")

lines = []
lines.append("# P2 Attempt 1 — H2 Workbook Numbers")
lines.append("")
lines.append(f"**Generated:** {pd.Timestamp.utcnow().strftime('%Y-%m-%d %H:%M')} UTC")
lines.append(f"**Series:** {series_name}")
lines.append(f"**Price start/end:** {close.index.min().date()} → {close.index.max().date()}")
lines.append(f"**N winter/summer windows:** {len(season)}")
lines.append("")
lines.append("## G1* Seasonality (H2)")
lines.append("")
lines.append(f"| Metric | Value |")
lines.append(f"|--------|-------|")
lines.append(f"| Mean Nov–Apr (winter) | {g1_winter_mean:.4%} |")
lines.append(f"| Mean May–Oct (summer) | {g1_summer_mean:.4%} |")
lines.append(f"| Gap (winter − summer) | {g1_gap:.4%} |")
lines.append(f"| Threshold | ≥ 2.00 pp |")
lines.append(f"| **G1* threshold met?** | **{'YES' if g1_pass else 'NO'}** |")
lines.append("")
if len(season):
    lines.append(f"| Median gap | {season['gap_w_minus_s'].median():.4%} |")
    lines.append(f"| % years winter > summer | {(season['gap_w_minus_s'] > 0).mean():.1%} |")
    lines.append("")
lines.append("## G4* Strategy vs buy-and-hold")
lines.append("")
lines.append("### Pre-tax (costs 5 bps/side on switch days only in after-tax block)")
lines.append("")
lines.append(f"| Metric | Strategy (R1) | Buy & hold |")
lines.append(f"|--------|---------------|------------|")
lines.append(f"| CAGR | {cagr_s:.4%} | {cagr_b:.4%} |")
lines.append(f"| Ann. vol | {vol_s:.4%} | {vol_b:.4%} |")
lines.append(f"| Sharpe (ex T-bill) | {sharpe_strat:.3f} | {sharpe_bh:.3f} |")
lines.append("")
lines.append("### F3 proxy (τ_ST=32% on April exit gains; 5 bps/side costs; B&H terminal τ_LT=20% on cumulative gain for CAGR only)")
lines.append("")
lines.append(f"| Metric | Strategy after-tax proxy | B&H |")
lines.append(f"|--------|--------------------------|-----|")
lines.append(f"| CAGR | {cagr_at:.4%} | pre-tax {cagr_bh2:.4%} / terminal-LT {cagr_bh_at:.4%} |")
lines.append(f"| Sharpe (ex T-bill) | {sharpe_strat_at:.3f} | {sharpe_bh2:.3f} (B&H stream pre-tax daily) |")
lines.append("")
lines.append(f"**G4* (strategy Sharpe > B&H Sharpe under F3 spirit)?** Strategy AT Sharpe {sharpe_strat_at:.3f} vs B&H Sharpe {sharpe_bh2:.3f} → **{'YES' if sharpe_strat_at > sharpe_bh2 else 'NO'}** on this proxy.")
lines.append("")
lines.append("## Method notes / limitations")
lines.append("")
lines.append("- T-bill daily return from ^IRX discount yield transformed to effective daily — approximate.")
lines.append("- F3 tax model is a **proxy**, not a full Form-8949 simulation (lots, wash sales, state tax, Medicare surtax omitted).")
lines.append("- B&H Sharpe uses pre-tax daily equity returns (deferred realization); favors honesty that switcher pays interim tax.")
lines.append("- If ^SP500TR unavailable historically, SPY adj-close proxy noted in Series line.")
lines.append("")

# save season csv snippet
season_path = Path("applications/2026-08_sell-in-may-sp500-2026/P2_Attempt1_seasonality_by_year.csv")
season.to_csv(season_path, index=False)
lines.append(f"By-year seasonality CSV: `{season_path.name}`")

OUT.write_text("\n".join(lines), encoding="utf-8")
print(OUT.read_text(encoding="utf-8"))
print("---")
print("G1_pass", g1_pass, "gap", g1_gap)
print("Sharpe strat/bh", sharpe_strat, sharpe_bh)
print("Sharpe AT strat/bh", sharpe_strat_at, sharpe_bh2)
print("series", series_name)
