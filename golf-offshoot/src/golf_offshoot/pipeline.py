"""End-to-end tournament run. Pre-tournament and live modes.

Never places bets. Always keeps ranges, reliability, and open questions.
"""

from __future__ import annotations

from pathlib import Path

from golf_offshoot.audit.journal import build_audit, data_snapshot_hash, diff_runs, save_audit
from golf_offshoot.bayesian_engine.engine import BayesianEngine
from golf_offshoot.bayesian_engine.simulate import SimConfig
from golf_offshoot.clustering.similars import apply_player_borrow, comparable_borrows
from golf_offshoot.decision.layer import advise_field
from golf_offshoot.field_effects.interaction import apply_field_interactions
from golf_offshoot.flags.bias import favorite_longshot_flags, flag_player
from golf_offshoot.free_parameters.board import build_player_board
from golf_offshoot.market.odds import build_market_snapshot
from golf_offshoot.models.enums import BetType, RunMode
from golf_offshoot.models.schemas import (
    AuditRecord,
    FieldSnapshot,
    HumanOverride,
    MarketSnapshot,
    Tournament,
    TournamentRunResult,
)
from golf_offshoot.models.strategy import PortfolioState, StrategyConfig
from golf_offshoot.ranking.display import rank_field
from golf_offshoot.strategy.engine import run_strategy


class GolfOffshootPipeline:
    def __init__(
        self,
        engine: BayesianEngine | None = None,
        snapshot_dir: Path | None = None,
        apply_decisions: bool = True,
        strategy_config: StrategyConfig | None = None,
    ) -> None:
        self.engine = engine or BayesianEngine()
        self.snapshot_dir = snapshot_dir
        self.apply_decisions = apply_decisions
        self.strategy_config = strategy_config if strategy_config is not None else StrategyConfig(enabled=False)

    def prepare_field(self, tournament: Tournament, field: FieldSnapshot) -> FieldSnapshot:
        """Start broad, borrow if thin, apply field interactions, constrain boards."""
        borrows = comparable_borrows(field.players)
        apply_player_borrow(field.players, borrows)
        for p in field.players:
            p.factors = build_player_board(p, tournament.course.course_type, field.mode)
        apply_field_interactions(field.players, tournament.course)
        # rebuild boards so field_interaction + borrowed form are in states
        for p in field.players:
            p.factors = build_player_board(p, tournament.course.course_type, field.mode)
            # re-apply field_interaction after rebuild
        apply_field_interactions(field.players, tournament.course)
        field.notes = (field.notes + f" borrows={len(borrows)}").strip()
        return field

    def apply_overrides(self, field: FieldSnapshot, overrides: list[HumanOverride]) -> None:
        for ov in overrides:
            for p in field.players:
                if p.player.player_id != ov.player_id:
                    continue
                if ov.factor_id and ov.factor_id in p.factors:
                    st = p.factors[ov.factor_id]
                    st.standardized_evidence += ov.delta_theta
                    st.notes = (st.notes + f" override: {ov.reason}").strip()
                else:
                    p.talent_prior += ov.delta_theta
                    p.talent_prior_sd = max(0.2, p.talent_prior_sd)

    def run(
        self,
        tournament: Tournament,
        field: FieldSnapshot,
        market_quotes=None,
        previous: AuditRecord | None = None,
        overrides: list[HumanOverride] | None = None,
        persist: bool = True,
        strategy_config: StrategyConfig | None = None,
        open_book: PortfolioState | None = None,
    ) -> TournamentRunResult:
        field = self.prepare_field(tournament, field)
        if overrides:
            self.apply_overrides(field, overrides)

        bundles, thetas, warnings = self.engine.run(tournament, field)

        market: MarketSnapshot | None = None
        if market_quotes is not None:
            market = build_market_snapshot(tournament.tournament_id, market_quotes)

        flags: dict[str, list[str]] = {}
        by_id = {p.player.player_id: p for p in field.players}
        for pid, th in thetas.items():
            flags[pid] = flag_player(by_id[pid], th, bundles[pid])
        for g in favorite_longshot_flags(bundles, market):
            warnings.append(g)

        borrow_notes = {}
        field_notes = {}
        for p in field.players:
            fi = p.factors.get("field_interaction")
            if fi and fi.notes:
                field_notes[p.player.player_id] = fi.notes
            cb = p.factors.get("comparable_player_borrow")
            if cb and cb.n_obs:
                borrow_notes[p.player.player_id] = [cb.notes or "borrowed strength"]

        prev_theta = {}
        if previous:
            prev_theta = {o.player_id: o.probabilities.theta_mean for o in previous.outputs}

        ranked = rank_field(
            field,
            bundles,
            thetas,
            market=market,
            flags=flags,
            borrow_notes=borrow_notes,
            field_notes=field_notes,
            prev_theta=prev_theta,
        )

        if self.apply_decisions:
            odds = {}
            if market:
                for q in market.quotes:
                    if q.bet_type == BetType.WIN and q.decimal_odds:
                        odds[q.player_id] = q.decimal_odds
            advice = {a.player_id: a for a in advise_field(ranked, BetType.WIN, odds)}
            for row in ranked:
                row.decision = advice.get(row.player_id)

        cfg = strategy_config if strategy_config is not None else self.strategy_config
        strategy = run_strategy(
            ranked,
            cfg,
            run_mode=field.mode,
            field=field,
            book=open_book,
        )

        snap = {
            "tournament": tournament.model_dump(mode="json"),
            "field": field.model_dump(mode="json"),
        }
        delta = []
        audit = build_audit(
            tournament.tournament_id,
            field.mode,
            ranked,
            data_snapshot_hash(snap),
            overrides=overrides,
            previous_run_id=previous.run_id if previous else None,
            delta_notes=delta,
            alpha=self.engine.alpha,
        )
        audit.strategy = strategy
        if previous:
            audit.delta_notes = diff_runs(previous, audit)
            warnings.extend(audit.delta_notes[:12])

        if persist and self.snapshot_dir:
            save_audit(audit, self.snapshot_dir)

        return TournamentRunResult(
            run_id=audit.run_id,
            tournament=tournament,
            mode=field.mode,
            ranked=ranked,
            market=market,
            audit=audit,
            warnings=warnings,
            never_auto_bet=True,
            strategy=strategy,
        )

    def rerun_live(
        self,
        tournament: Tournament,
        field: FieldSnapshot,
        previous: AuditRecord,
        market_quotes=None,
        open_book: PortfolioState | None = None,
        strategy_config: StrategyConfig | None = None,
    ) -> TournamentRunResult:
        field.mode = RunMode.LIVE
        return self.run(
            tournament,
            field,
            market_quotes=market_quotes,
            previous=previous,
            open_book=open_book,
            strategy_config=strategy_config,
        )
