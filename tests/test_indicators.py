"""Tests for indicator definitions and threshold inclusivity."""

import pandas as pd

from climate_site_risk.indicators import compute_monthly_indicators
from climate_site_risk.models import Thresholds


def test_monthly_indicators_use_inclusive_thresholds() -> None:
    """Values equal to the configured limits count as threshold days."""
    timeseries = pd.DataFrame(
        {
            "site_id": ["A", "A", "A"],
            "site_name": ["Alpha", "Alpha", "Alpha"],
            "time": pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"]),
            "tmax_c": [34.0, 35.0, 36.0],
            "precip_mm": [0.0, 20.0, 5.0],
        }
    )

    result = compute_monthly_indicators(timeseries, Thresholds())

    assert result.loc[0, "heat_days"] == 2
    assert result.loc[0, "heavy_rain_days"] == 1
    assert result.loc[0, "dry_days"] == 1
    assert result.loc[0, "stress_days"] == 2

