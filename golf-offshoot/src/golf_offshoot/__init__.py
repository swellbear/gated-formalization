"""Golf Betting Offshoot — uncertainty-aware golf analysis.

This package is a **separate system**. It does not import, score, or mutate
the Gated Progressive Formalization method, templates, locks, or application folders.
"""

from golf_offshoot.config import MODEL_VERSION

__version__ = "0.2.0"
__model_version__ = MODEL_VERSION

__all__ = ["__version__", "__model_version__"]
