import hashlib
import shutil

from golf_offshoot.learning_lane_15m.digest import (
    CAVEATS_BANNER,
    CAVEATS_REL,
    MANIFEST_REL,
    caveats_path,
    collect_figures,
    digest_path,
    write_digest,
)


def _scratch_repo(tmp_path):
    """A throwaway repo root seeded with the real caveats and manifest.

    The generator writes the SOURCE digest, which is the published spine. A
    test that lets it write the real tree silently republishes figures nobody
    reviewed — so the write goes to scratch and only reads touch the repo.
    """
    for rel in (CAVEATS_REL, MANIFEST_REL):
        src = caveats_path().parent.parent.parent / rel
        dest = tmp_path / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if src.is_file():
            shutil.copyfile(src, dest)
    return tmp_path


def test_generator_concatenates_caveats_and_does_not_rewrite_them(tmp_path):
    scratch = _scratch_repo(tmp_path)
    real_caveats = caveats_path()
    before_hash = hashlib.sha256(real_caveats.read_bytes()).hexdigest()
    scratch_caveats = caveats_path(root=scratch)
    scratch_before = hashlib.sha256(scratch_caveats.read_bytes()).hexdigest()

    write_digest(root=scratch)

    # The generator may never write, rewrite, reorder or drop the caveats.
    assert hashlib.sha256(real_caveats.read_bytes()).hexdigest() == before_hash
    assert hashlib.sha256(scratch_caveats.read_bytes()).hexdigest() == scratch_before
    body = digest_path(root=scratch).read_text(encoding="utf-8")
    assert CAVEATS_BANNER in body
    assert "Unmeasured is not lost and not losses." in body
    figures = collect_figures(root=scratch)
    assert str(figures["bankroll"]) in body
    assert str(figures["betting_pnl"]) in body
    assert str(figures["events_n"]) in body
    assert "KXBTC15M-26SEP072245" in body
    assert "KXBTC15M-26SEP100515" in body
    assert "KXBTC15M-26SEP100315" in body


def test_the_generator_never_writes_the_published_digest_from_a_scratch_root(tmp_path):
    scratch = _scratch_repo(tmp_path)
    published = digest_path()
    before = published.read_bytes() if published.is_file() else None

    write_digest(root=scratch)

    after = published.read_bytes() if published.is_file() else None
    assert after == before
