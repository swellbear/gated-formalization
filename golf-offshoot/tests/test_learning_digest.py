import hashlib

from golf_offshoot.learning_lane_15m.digest import (
    CAVEATS_BANNER,
    caveats_path,
    collect_figures,
    digest_path,
    write_digest,
)


def test_generator_concatenates_caveats_and_does_not_rewrite_them(tmp_path=None):
    caveats = caveats_path()
    before = caveats.read_bytes()
    before_hash = hashlib.sha256(before).hexdigest()
    write_digest()
    after = caveats.read_bytes()
    assert hashlib.sha256(after).hexdigest() == before_hash
    body = digest_path().read_text(encoding="utf-8")
    assert CAVEATS_BANNER in body
    assert "Unmeasured is not lost and not losses." in body
    figures = collect_figures()
    assert str(figures["bankroll"]) in body
    assert str(figures["betting_pnl"]) in body
    assert str(figures["events_n"]) in body
    assert "KXBTC15M-26SEP072245" in body
