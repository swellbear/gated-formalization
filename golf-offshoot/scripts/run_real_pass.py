"""Real operating pass: pressure-test St. Jude with live odds + SG. No calibration."""

from __future__ import annotations

import sys

from golf_offshoot.calibration.artifacts import load_weights
from golf_offshoot.data_feeds.http import package_data_dir
from golf_offshoot.models.enums import RunMode
from golf_offshoot.models.schemas import SourceInventoryItem
from golf_offshoot.operating import run_operating, run_strategy_modes, write_pressure_report
from golf_offshoot.ranking.display import format_table


ST_JUDE = "401811962"


def main() -> int:
    print("=== CALIBRATION SKIPPED ===", flush=True)
    print(
        "No as-of SG/odds panel for historical events; finish-only refit is forbidden.",
        flush=True,
    )

    print("=== PRE-TOURNAMENT PRESSURE TEST ===", flush=True)
    pre = run_operating(
        event_id=ST_JUDE,
        mode=RunMode.PRE_TOURNAMENT,
        sims=2200,
        enable_strategy=True,
        persist=True,
        refresh=False,
    )
    print(
        f"{pre.tournament.name} has_cut={pre.tournament.has_cut} n={len(pre.ranked)} run={pre.run_id}",
        flush=True,
    )
    print(f"odds_quotes={pre.audit.extra.get('odds_quotes')} overround={pre.audit.extra.get('overround')}", flush=True)
    print(f"sg={pre.audit.extra.get('sg_players')}/{pre.audit.extra.get('sg_field')}", flush=True)
    print(format_table(pre.ranked, n=12), flush=True)
    modes = run_strategy_modes(pre, bankroll=2000.0)
    for k, v in modes.items():
        print(f"--- {k} ---", flush=True)
        print(v, flush=True)

    print("=== LIVE SNAPSHOT ===", flush=True)
    live = run_operating(
        event_id=ST_JUDE,
        mode=RunMode.LIVE,
        sims=1400,
        enable_strategy=True,
        persist=True,
        refresh=False,
    )
    print(format_table(live.ranked, n=8, baseline=pre.ranked), flush=True)
    live_modes = run_strategy_modes(live, bankroll=2000.0)
    for k, v in live_modes.items():
        print(f"--- live {k} ---", flush=True)
        print(v, flush=True)

    inv_raw = pre.audit.extra.get("source_inventory") or []
    inv = [SourceInventoryItem.model_validate(x) for x in inv_raw]
    report = write_pressure_report(
        pre,
        inventory=inv,
        strategy_blocks=modes,
        live=live,
        calib_summary=load_weights(),
        path=package_data_dir().parent / "docs" / "PRESSURE_TEST_2026_ST_JUDE.md",
        live_strategy_blocks=live_modes,
    )
    print(f"wrote {report}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
