"""Honesty transforms for B-guts θ. Missing stays missing. Defaults stay parked."""

from __future__ import annotations

from golf_offshoot.models.enums import FactorStatus
from golf_offshoot.models.schemas import FieldSnapshot

_UNADMITTED = ("narrative_momentum", "live_tee_pairing")


def park_unadmitted(field: FieldSnapshot) -> None:
    """Zero narrative stuffing; park tee pairing; WD-only health."""
    for p in field.players:
        p.narrative_momentum = 0.0
        for fid in _UNADMITTED:
            st = p.factors.get(fid)
            if st:
                st.status = FactorStatus.PARKED
                st.standardized_evidence = 0.0
        health = p.factors.get("health_setup")
        if health and not p.withdrawn:
            health.status = FactorStatus.PARKED
            health.standardized_evidence = 0.0
