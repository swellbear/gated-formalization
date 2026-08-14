"""Full one-player reports: ranges, reliability, market, flags, explainability.

The compact ranking table is `format_table`. This module is the long card.
"""

from __future__ import annotations

from golf_offshoot.free_parameters.catalog import CATALOG_BY_ID
from golf_offshoot.models.enums import Horizon
from golf_offshoot.models.schemas import FieldSnapshot, PlayerInputs, PlayerOutput
from golf_offshoot.models.strategy import PositionMark, StrategyAction, StrategyPosition
from golf_offshoot.ranking.display import format_table

_HORIZON_ORDER = (
    Horizon.WIN,
    Horizon.TOP_5,
    Horizon.TOP_10,
    Horizon.TOP_20,
    Horizon.MAKE_CUT,
)


def input_snapshot(player: PlayerInputs) -> dict:
    """Stable subset of raw inputs for a full report (not the whole board)."""
    return {
        "player_id": player.player.player_id,
        "name": player.player.name,
        "owgr": player.player.owgr,
        "is_lesser_known": player.player.is_lesser_known,
        "talent_prior": player.talent_prior,
        "talent_prior_sd": player.talent_prior_sd,
        "sg": {
            "ott": player.sg.ott,
            "app": player.sg.app,
            "arg": player.sg.arg,
            "putt": player.sg.putt,
            "total": player.sg.total,
            "driving_distance_yd": player.sg.driving_distance_yd,
            "driving_accuracy_pct": player.sg.driving_accuracy_pct,
        },
        "course_history_rounds": player.course_history_rounds,
        "course_history_sg": player.course_history_sg,
        "recent_form_sg": player.recent_form_sg,
        "short_term_trend": player.short_term_trend,
        "weather_fit": player.weather_fit,
        "health_flag": player.health_flag,
        "narrative_momentum": player.narrative_momentum,
        "live_score_to_par": player.live_score_to_par,
        "live_holes_completed": player.live_holes_completed,
        "live_made_cut": player.live_made_cut,
        "withdrawn": player.withdrawn,
    }


def _fmt_p(v: float | None) -> str:
    if v is None:
        return "n/a"
    return f"{v:.3f}"


def _fmt_signed(v: float | None) -> str:
    if v is None:
        return "n/a"
    return f"{v:+.3f}"


def format_player_report(
    row: PlayerOutput,
    *,
    inputs: PlayerInputs | None = None,
    positions: list[StrategyPosition] | None = None,
    marks: list[PositionMark] | None = None,
    actions: list[StrategyAction] | None = None,
) -> str:
    """Long-form card for one player. Paper slices are optional."""
    lines: list[str] = []
    lesser = ""
    if inputs and inputs.player.is_lesser_known:
        lesser = "  [lesser-known]"
    lines.append(f"=== {row.name} ({row.player_id})  rank {row.rank}{lesser} ===")

    pos_list = positions or []
    mark_by_pos = {m.position_id: m for m in (marks or [])}
    acts = actions or []
    if pos_list:
        lines.append("Paper:")
        for pos in pos_list:
            mark = mark_by_pos.get(pos.position_id)
            tag = "proposed" if pos.proposed else "recorded"
            lines.append(
                f"  {pos.bet_type.value}  stake {pos.stake:.2f} @ {pos.decimal_odds:.2f}  "
                f"entry edge {_fmt_signed(pos.entry_edge)}  ({tag})"
            )
            if mark:
                path = []
                if mark.is_runner:
                    path.append("runner")
                if mark.original_edge_collapsed:
                    path.append("collapsed")
                if mark.live_edge_improved:
                    path.append("improved")
                path_s = ",".join(path) if path else "intact"
                lines.append(
                    f"    live edge {_fmt_signed(mark.live_edge)}  "
                    f"model {_fmt_p(mark.entry_model_p)} → {_fmt_p(mark.live_model_p)}  "
                    f"MTM {mark.mtm_value:.2f}  uPnL {mark.unrealized_pnl:+.2f}  path {path_s}"
                )
            matching = [
                a
                for a in acts
                if a.position_id == pos.position_id
                or (a.player_id == pos.player_id and a.bet_type == pos.bet_type)
            ]
            for a in matching:
                extra = f"  Δ{a.suggested_stake_delta:+.2f}" if a.suggested_stake_delta else ""
                warn = f"  ⚠ {a.uncertainty_warning}" if a.uncertainty_warning else ""
                lines.append(f"    strategy {a.kind.value}{extra} — {a.reason}{warn}")
                lines.append("    never auto-bet; confirmation required")

    lines.append("Probabilities (central [low–high]):")
    for h in _HORIZON_ORDER:
        hp = row.probabilities.p(h)
        lines.append(f"  {h.value:<10} {hp.central:.3f} [{hp.low:.2f}–{hp.high:.2f}]")
    bundle = row.probabilities
    if bundle.scenario_optimistic or bundle.scenario_pessimistic:
        opt = bundle.scenario_optimistic.get("win")
        pes = bundle.scenario_pessimistic.get("win")
        if opt is not None or pes is not None:
            lines.append(
                f"  scenarios   win optimistic {_fmt_p(opt)} / pessimistic {_fmt_p(pes)}"
            )
    lines.append(
        f"  theta       {bundle.theta_mean:.2f} ± {bundle.theta_sd:.2f}"
    )

    rel = row.reliability
    lines.append(
        f"Reliability: {rel.score:.2f}  "
        f"density={rel.data_density:.2f}  quality={rel.data_quality:.2f}  "
        f"stability={rel.input_stability:.2f}"
    )
    for reason in rel.reasons:
        lines.append(f"  - {reason}")

    if row.edge_by_bet or row.market_implied_by_bet:
        lines.append("Market:")
        keys = sorted(set(row.edge_by_bet) | set(row.market_implied_by_bet))
        for k in keys:
            lines.append(
                f"  {k:<10} implied {_fmt_p(row.market_implied_by_bet.get(k))}  "
                f"edge {_fmt_signed(row.edge_by_bet.get(k))}"
            )

    flags = ",".join(row.flags) if row.flags else "(none)"
    lines.append(f"Flags: {flags}")
    lines.append("Open questions:")
    if row.open_questions:
        for q in row.open_questions:
            lines.append(f"  - {q}")
    else:
        lines.append("  - (none listed)")

    if inputs:
        sg = inputs.sg
        lines.append("Inputs:")
        lines.append(
            f"  talent {inputs.talent_prior:.2f} ± {inputs.talent_prior_sd:.2f}  "
            f"OWGR {inputs.player.owgr if inputs.player.owgr is not None else 'n/a'}  "
            f"venue rounds {inputs.course_history_rounds}"
        )
        lines.append(
            f"  SG ott {sg.ott:+.2f} app {sg.app:+.2f} arg {sg.arg:+.2f} "
            f"putt {sg.putt:+.2f} total {sg.total:+.2f}"
        )
        if sg.driving_distance_yd is not None or sg.driving_accuracy_pct is not None:
            dist = f"{sg.driving_distance_yd:.0f}yd" if sg.driving_distance_yd is not None else "n/a"
            acc = f"{sg.driving_accuracy_pct:.1f}%" if sg.driving_accuracy_pct is not None else "n/a"
            lines.append(f"  driving {dist} / {acc} accuracy")
        extras = []
        if inputs.recent_form_sg is not None:
            extras.append(f"form {inputs.recent_form_sg:+.2f}")
        if inputs.short_term_trend is not None:
            extras.append(f"trend {inputs.short_term_trend:+.2f}")
        if inputs.weather_fit is not None:
            extras.append(f"weather {inputs.weather_fit:+.2f}")
        if inputs.health_flag:
            extras.append(f"health {inputs.health_flag:+.2f}")
        if extras:
            lines.append("  " + "  ".join(extras))
        if inputs.live_score_to_par is not None:
            lines.append(
                f"  live {inputs.live_score_to_par:+.1f} through "
                f"{inputs.live_holes_completed} holes"
            )

    expl = row.explain
    lines.append("Explain:")
    if expl:
        lines.append(f"  {expl.narrative}")
        contrib = sorted(expl.contributions, key=lambda c: abs(c.delta_theta), reverse=True)
        shown = [c for c in contrib if abs(c.delta_theta) >= 0.01 or c.factor_id == "talent_prior"][:10]
        if shown:
            lines.append("  contributions:")
            for c in shown:
                name = CATALOG_BY_ID[c.factor_id].name if c.factor_id in CATALOG_BY_ID else c.factor_id
                lines.append(
                    f"    {name}: {c.delta_theta:+.3f}θ  evidence={c.evidence:+.2f}  "
                    f"q={c.quality:.2f}  importance={c.importance:.2f}  {c.status.value}"
                )
        if expl.borrowed_strength:
            lines.append("  borrowed: " + "; ".join(expl.borrowed_strength))
        if expl.field_interaction_note:
            lines.append(f"  field: {expl.field_interaction_note}")
    else:
        lines.append("  (no explainability attached)")

    if row.decision:
        d = row.decision
        lines.append(
            f"Decision: {d.action.value}  {d.bet_type.value}  "
            f"kelly cap {d.suggested_kelly_fraction:.3f}  never_auto_bet={d.never_auto_bet}"
        )
        for r in d.reasons:
            lines.append(f"  - {r}")
    return "\n".join(lines)


def format_player_reports(
    rows: list[PlayerOutput],
    field: FieldSnapshot | None = None,
    *,
    positions_by_player: dict[str, list[StrategyPosition]] | None = None,
    marks: list[PositionMark] | None = None,
    actions: list[StrategyAction] | None = None,
) -> str:
    by_id = {p.player.player_id: p for p in field.players} if field else {}
    pos_map = positions_by_player or {}
    mark_list = marks or []
    act_list = actions or []
    blocks = []
    for row in rows:
        pid = row.player_id
        pos = pos_map.get(pid, [])
        pos_ids = {p.position_id for p in pos}
        row_marks = [m for m in mark_list if m.player_id == pid or m.position_id in pos_ids]
        row_acts = [
            a
            for a in act_list
            if a.player_id == pid or (a.position_id and a.position_id in pos_ids)
        ]
        blocks.append(
            format_player_report(
                row,
                inputs=by_id.get(pid),
                positions=pos,
                marks=row_marks,
                actions=row_acts,
            )
        )
    return "\n\n".join(blocks)


def paper_table(rows: list[PlayerOutput]) -> str:
    """Compact table limited to the rows already filtered to the paper."""
    if not rows:
        return "(no paper players)"
    return format_table(rows, n=len(rows))
