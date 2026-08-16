from options_offshoot.leftover import format_leftover_callout, inventory_item
from options_offshoot.models.enums import RunMode, SourceKind
from options_offshoot.models.schemas import FieldRun


def test_leftover_has_four_sections():
    run = FieldRun(
        field_id="spx_this_friday",
        run_id="t",
        mode=RunMode.INGEST,
        inventory=[
            inventory_item(
                "polygon_quotes",
                used=True,
                missing=False,
                source="polygon",
                kind=SourceKind.REAL_LIVE,
                n=3,
            ),
            inventory_item(
                "earnings_narrative",
                used=False,
                missing=True,
                notes="forbidden in theta",
            ),
        ],
    )
    text = format_leftover_callout(run)
    assert "== already used ==" in text
    assert "== still unconstrained ==" in text
    assert "== on held tickets ==" in text
    assert "== do not stuff into theta ==" in text
    assert "none held" in text
    assert "earnings_narrative" in text
    assert "GPF gates" in text or "not GPF" in text
