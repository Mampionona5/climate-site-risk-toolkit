"""Transparent indicator calculations for extracted site time series."""

import pandas as pd

from climate_site_risk.models import Thresholds


def compute_monthly_indicators(
    timeseries: pd.DataFrame,
    thresholds: Thresholds,
) -> pd.DataFrame:
    """Aggregate daily site values into monthly operational indicators."""
    working = timeseries.copy()
    working["time"] = pd.to_datetime(working["time"], errors="raise")
    working["month"] = working["time"].dt.to_period("M").astype(str)
    working["is_heat_day"] = working["tmax_c"] >= thresholds.heat_c
    working["is_heavy_rain_day"] = working["precip_mm"] >= thresholds.heavy_rain_mm
    working["is_dry_day"] = working["precip_mm"] < thresholds.dry_day_mm
    working["is_stress_day"] = working["is_heat_day"] | working["is_heavy_rain_day"]

    indicators = (
        working.groupby(["site_id", "site_name", "month"], as_index=False)
        .agg(
            observations=("time", "count"),
            mean_tmax_c=("tmax_c", "mean"),
            heat_days=("is_heat_day", "sum"),
            total_precip_mm=("precip_mm", "sum"),
            heavy_rain_days=("is_heavy_rain_day", "sum"),
            dry_days=("is_dry_day", "sum"),
            stress_days=("is_stress_day", "sum"),
        )
        .sort_values(["site_id", "month"])
        .reset_index(drop=True)
    )
    indicators["mean_tmax_c"] = indicators["mean_tmax_c"].round(2)
    indicators["total_precip_mm"] = indicators["total_precip_mm"].round(2)
    return indicators

