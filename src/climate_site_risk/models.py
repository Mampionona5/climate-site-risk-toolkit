"""Shared domain models."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Thresholds:
    """Operational thresholds used to count climate stress days."""

    heat_c: float = 35.0
    heavy_rain_mm: float = 20.0
    dry_day_mm: float = 1.0

    def __post_init__(self) -> None:
        """Reject physically inconsistent threshold values."""
        if self.heavy_rain_mm <= self.dry_day_mm:
            raise ValueError("heavy_rain_mm doit être supérieur à dry_day_mm")

