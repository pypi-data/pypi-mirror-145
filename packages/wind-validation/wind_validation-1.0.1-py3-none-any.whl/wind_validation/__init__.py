"""
wind_validation: A tool for validating wind resource models
"""
from ._version import version as __version__

from .validation import validate
from .reporting import create_report

__all__ = ["validate", "create_report"]
