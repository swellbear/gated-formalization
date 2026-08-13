from datetime import datetime, timezone

from golf_offshoot.bayesian_engine.updates import update_theta
from golf_offshoot.config import NARRATIVE_ABS_CAP
from golf_offshoot.models.enums import FactorStatus
from golf_offshoot.models.schemas import DataQuality, FreeParameterState


def _q(score: float) -> DataQuality:
    return DataQuality(
        score=score,
        source_name="t",
        as_of=datetime.now(timezone.utc),
        n_observations=10,
    )


def _board(**kwargs) -> dict[str, FreeParameterState]:
    base = {
        "talent_prior": FreeParameterState(
            factor_id="talent_prior",
            status=FactorStatus.CONSTRAINED,
            standardized_evidence=1.0,
            quality=_q(0.9),
            n_obs=40,
            importance=0.7,
        )
    }
    base.update(kwargs)
    return base


def test_weak_quality_moves_less_than_strong():
    strong = FreeParameterState(
        factor_id="recent_form",
        status=FactorStatus.CONSTRAINED,
        standardized_evidence=2.0,
        quality=_q(0.95),
        n_obs=12,
        importance=0.5,
    )
    weak = strong.model_copy(update={"quality": _q(0.10)})
    t_strong = update_theta(1.0, 0.4, _board(recent_form=strong))
    t_weak = update_theta(1.0, 0.4, _board(recent_form=weak))
    d_strong = abs(t_strong.mean - 1.0)
    d_weak = abs(t_weak.mean - 1.0)
    assert d_strong > d_weak * 2


def test_narrative_is_capped():
    nar = FreeParameterState(
        factor_id="narrative_momentum",
        status=FactorStatus.PARTIALLY_CONSTRAINED,
        standardized_evidence=8.0,
        quality=_q(1.0),
        n_obs=1,
        importance=0.2,
    )
    t = update_theta(0.0, 0.5, _board(narrative_momentum=nar))
    nar_c = next(c for c in t.contributions if c.factor_id == "narrative_momentum")
    assert abs(nar_c.delta_theta) <= NARRATIVE_ABS_CAP + 1e-9
