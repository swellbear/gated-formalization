from golf_offshoot.data_feeds.base import FallbackChain, unavailable_quality
from golf_offshoot.data_feeds.mocks import MockTalentFeed, UnreachablePrimary
from golf_offshoot.models.enums import SourceKind


def test_fallback_when_primary_fails():
    chain = FallbackChain(
        [
            UnreachablePrimary(),
            MockTalentFeed({"p01": (1.0, 0.4)}),
        ]
    )
    payload, q, name = chain.fetch()
    assert payload is not None
    assert "p01" in payload
    assert name == "mock_talent"
    assert q.score > 0
    assert q.source_kind == SourceKind.MOCK


def test_unavailable_quality_is_explicit():
    q = unavailable_quality("strokes_gained", "no vendor")
    assert q.missing is True
    assert q.source_kind == SourceKind.UNAVAILABLE
    assert q.score == 0.0
