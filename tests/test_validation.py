"""Tests for explicit dataset-contract failures."""

import numpy as np
import pandas as pd
import xarray as xr

from climate_site_risk.validation import validate_dataset


def test_validation_reports_missing_variable() -> None:
    """A dataset without precipitation should fail with an actionable message."""
    dataset = xr.Dataset(
        {"tmax_c": (("time", "latitude", "longitude"), np.ones((1, 1, 1)))},
        coords={
            "time": pd.date_range("2024-01-01", periods=1),
            "latitude": [44.0],
            "longitude": [3.0],
        },
    )

    report = validate_dataset(dataset)

    assert not report.is_valid
    assert "Variable manquante : precip_mm" in report.errors

