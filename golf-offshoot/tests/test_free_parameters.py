from golf_offshoot.free_parameters.catalog import CATALOG, REQUIRED_FACTOR_IDS, get_def
from golf_offshoot.free_parameters.ranking import importance, ranked_parameters
from golf_offshoot.models.enums import CourseType, RunMode


def test_required_factors_present():
    ids = {d.factor_id for d in CATALOG}
    for rid in REQUIRED_FACTOR_IDS:
        assert rid in ids


def test_course_type_reorders_importance():
    weather = get_def("weather_suitability")
    bogey = get_def("bogey_avoidance")
    assert importance(weather, CourseType.LINKS) > importance(weather, CourseType.PARKLAND)
    assert importance(bogey, CourseType.MAJOR_SETUP) > importance(bogey, CourseType.PARKLAND)
    park = ranked_parameters(CourseType.PARKLAND)
    assert park[0][0].factor_id == "talent_prior"


def test_live_factors_parked_pre_tournament():
    pre = {d.factor_id for d, *_ in ranked_parameters(CourseType.PARKLAND, RunMode.PRE_TOURNAMENT)}
    live = {d.factor_id for d, *_ in ranked_parameters(CourseType.PARKLAND, RunMode.LIVE)}
    assert "live_position" not in pre
    assert "live_position" in live
