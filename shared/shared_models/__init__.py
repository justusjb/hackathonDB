"""Shared Pydantic models for HackathonDB services."""

__version__ = "0.1.0"

# Import all models to expose them at the package level
from .models import (
    EmailSubmission,
    HackathonSubmission,
    Coordinates,
    Location,
    DateRange,
    HackathonStatus,
    HackathonBase,
    Hackathon
)

# Define what's available when using `from shared_models import *`
__all__ = [
    "EmailSubmission",
    "HackathonSubmission",
    "Coordinates",
    "Location",
    "DateRange",
    "HackathonStatus",
    "HackathonBase",
    "Hackathon"
]