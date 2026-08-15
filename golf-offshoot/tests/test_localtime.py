from datetime import datetime, timezone

from golf_offshoot.localtime import filename_stamp, format_eastern, isoformat_now, now
from golf_offshoot.strategy.paper_book import format_paper_time


def test_format_eastern_converts_august_utc_to_edt():
    dt = datetime(2026, 8, 15, 17, 40, tzinfo=timezone.utc)
    assert format_eastern(dt) == "2026-08-15 13:40 EDT"
    assert format_paper_time(dt) == "2026-08-15 13:40 EDT"


def test_format_eastern_converts_january_utc_to_est():
    dt = datetime(2026, 1, 15, 17, 40, tzinfo=timezone.utc)
    assert format_eastern(dt) == "2026-01-15 12:40 EST"


def test_format_eastern_accepts_iso_utc_string():
    assert format_eastern("2026-08-15T17:40:00+00:00") == "2026-08-15 13:40 EDT"
    assert format_eastern("2026-08-15T17:40:00Z") == "2026-08-15 13:40 EDT"


def test_filename_stamp_is_eastern_and_sorts_after_legacy_z():
    dt = datetime(2026, 8, 15, 17, 40, tzinfo=timezone.utc)
    assert filename_stamp(dt) == "20260815_ET134000"
    winter = datetime(2026, 1, 15, 17, 40, tzinfo=timezone.utc)
    assert filename_stamp(winter) == "20260115_ET124000"
    # Same calendar day: new Eastern stems must sort after old UTC-Z stems.
    assert "20260815T174049Z" < "20260815_ET134000"


def test_storage_now_is_eastern():
    assert now().tzinfo is not None
    assert now().tzname() in {"EDT", "EST"}
    dt = datetime(2026, 8, 15, 17, 40, tzinfo=timezone.utc)
    assert isoformat_now(dt).startswith("2026-08-15T13:40:00")
    assert isoformat_now(dt).endswith("-04:00")
