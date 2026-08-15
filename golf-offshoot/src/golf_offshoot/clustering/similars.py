"""Comparable players and venue clusters — borrow strength when data is thin."""

from __future__ import annotations

import numpy as np

from golf_offshoot.config import THIN_SAMPLE_N
from golf_offshoot.models.schemas import (
    ComparableBorrow,
    Course,
    PlayerInputs,
    VenueCluster,
)


def _player_vector(p: PlayerInputs, *, honest: bool = False) -> np.ndarray:
    """Fixed 8-d vector so mixed SG coverage still cosine-compares."""
    sg = p.sg
    sg_ok = sg.quality is not None and not sg.quality.missing
    dist = 0.0 if sg.driving_distance_yd is None else (sg.driving_distance_yd - 295.0) / 15.0
    acc = 0.0 if sg.driving_accuracy_pct is None else (sg.driving_accuracy_pct - 60.0) / 10.0
    if sg_ok:
        ott, app, arg, putt = sg.ott, sg.app, sg.arg, sg.putt
    elif honest:
        ott = app = arg = putt = float("nan")
    else:
        ott = app = arg = putt = 0.0
    recent = p.recent_form_sg
    if p.recent_sg is not None and p.recent_sg.quality is not None and not p.recent_sg.quality.missing:
        recent = p.recent_sg.total
    elif honest and recent is None:
        recent = float("nan")
    return np.array(
        [p.talent_prior, float(recent or 0.0) if recent == recent else float("nan"), dist, acc, ott, app, arg, putt],
        dtype=float,
    )


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    mask = np.isfinite(a) & np.isfinite(b)
    if mask.sum() < 2:
        return 0.0
    aa, bb = a[mask], b[mask]
    na, nb = np.linalg.norm(aa), np.linalg.norm(bb)
    if na < 1e-9 or nb < 1e-9:
        return 0.0
    return float(np.dot(aa, bb) / (na * nb))


def comparable_borrows(
    field: list[PlayerInputs],
    k: int = 6,
    min_sim: float = 0.15,
    *,
    honest: bool = False,
) -> dict[str, ComparableBorrow]:
    vecs = [_player_vector(p, honest=honest) for p in field]
    out: dict[str, ComparableBorrow] = {}
    for i, p in enumerate(field):
        if p.course_history_rounds >= THIN_SAMPLE_N and not p.player.is_lesser_known:
            continue
        sims: list[tuple[float, int]] = []
        for j, q in enumerate(field):
            if i == j:
                continue
            s = cosine(vecs[i], vecs[j])
            if s >= min_sim:
                sims.append((s, j))
        sims.sort(reverse=True)
        sims = sims[:k]
        if not sims:
            continue
        raw = np.array([s for s, _ in sims])
        w = raw / raw.sum()
        shrink = 0.55 if p.player.is_lesser_known else 0.35
        if p.course_history_rounds == 0:
            shrink += 0.15
        neighbor_ids = [field[j].player.player_id for _, j in sims]
        out[p.player.player_id] = ComparableBorrow(
            player_id=p.player.player_id,
            neighbor_ids=neighbor_ids,
            weights=[float(x) for x in w],
            shrinkage=min(0.75, shrink),
            reason="thin own-sample; shrink toward similar talent/form (and SG when real)",
        )
    return out


def apply_player_borrow(
    field: list[PlayerInputs],
    borrows: dict[str, ComparableBorrow],
    *,
    honest: bool = False,
) -> None:
    """Blend course_history / form toward neighbors. Mutates factor boards if present."""
    by_id = {p.player.player_id: p for p in field}
    for pid, b in borrows.items():
        p = by_id[pid]
        neighbor_form = []
        neighbor_hist = []
        for nid, w in zip(b.neighbor_ids, b.weights):
            n = by_id.get(nid)
            if not n:
                continue
            if n.recent_form_sg is not None:
                neighbor_form.append(w * n.recent_form_sg)
            if n.course_history_sg is not None:
                neighbor_hist.append(w * n.course_history_sg)
        if neighbor_form and p.recent_form_sg is not None:
            p.recent_form_sg = (1 - b.shrinkage) * p.recent_form_sg + b.shrinkage * sum(neighbor_form)
        elif neighbor_form and p.recent_form_sg is None and not honest:
            p.recent_form_sg = sum(neighbor_form)
        if neighbor_hist and (p.course_history_rounds < THIN_SAMPLE_N):
            blended = sum(neighbor_hist)
            if p.course_history_sg is None:
                p.course_history_sg = blended
            else:
                p.course_history_sg = (1 - b.shrinkage) * p.course_history_sg + b.shrinkage * blended


def course_feature_vector(course: Course) -> np.ndarray:
    type_code = hash(course.course_type.value) % 7 / 7.0
    return np.array(
        [
            course.yardage / 7500.0,
            course.tightness,
            course.wind_exposure,
            course.firmness,
            course.rough_severity,
            course.green_speed,
            course.altitude_m / 2000.0,
            1.0 if course.coastal else 0.0,
            type_code,
        ],
        dtype=float,
    )


def build_venue_clusters(courses: list[Course], n_clusters: int = 4) -> list[VenueCluster]:
    """Cheap k-means-ish split on course features (no sklearn)."""
    if not courses:
        return []
    k = min(n_clusters, len(courses))
    X = np.stack([course_feature_vector(c) for c in courses])
    rng = np.random.default_rng(0)
    centers = X[rng.choice(len(X), size=k, replace=False)]
    labels = np.zeros(len(X), dtype=int)
    for _ in range(12):
        d = ((X[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)
        labels = d.argmin(axis=1)
        for j in range(k):
            if np.any(labels == j):
                centers[j] = X[labels == j].mean(axis=0)
    clusters: list[VenueCluster] = []
    for j in range(k):
        members = [courses[i].course_id for i in range(len(courses)) if labels[i] == j]
        clusters.append(
            VenueCluster(
                cluster_id=f"venue-{j}",
                name=f"venue cluster {j}",
                course_ids=members,
                centroid={f"d{i}": float(v) for i, v in enumerate(centers[j])},
            )
        )
    return clusters
