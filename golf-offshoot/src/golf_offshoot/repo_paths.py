"""Repo root without importing the paper book or pydantic.

Cloud CoS must be able to stamp ``last_cos_*`` without installing golf-offshoot
extras. ``operator_surface.observability`` imports settle/paper at module
load; this module does not.
"""

from __future__ import annotations

from pathlib import Path


def repo_root() -> Path:
    """gated-formalization repo root (parent of ``golf-offshoot/``)."""
    return Path(__file__).resolve().parents[3]
