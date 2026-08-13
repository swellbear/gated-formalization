from golf_offshoot.data_feeds.base import FallbackChain
from golf_offshoot.data_feeds.mocks import MockTalentFeed, UnreachablePrimary


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
