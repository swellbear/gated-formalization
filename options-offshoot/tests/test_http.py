from options_offshoot.data_feeds.http import cache_key, url_without_api_key


def test_cache_key_strips_apikey():
    a = "https://api.polygon.io/v3/snapshot/options/AAPL?expiration_date=2026-08-21&apiKey=SECRET"
    b = "https://api.polygon.io/v3/snapshot/options/AAPL?expiration_date=2026-08-21&apiKey=OTHER"
    assert "SECRET" not in url_without_api_key(a)
    assert "apiKey" not in url_without_api_key(a).lower()
    assert cache_key(a) == cache_key(b)
    assert cache_key(a) != cache_key("https://api.polygon.io/v3/snapshot/options/MSFT")
