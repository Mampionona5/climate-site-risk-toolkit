"""Extract climate time series at the nearest grid cell for each site."""

import pandas as pd
import xarray as xr


def extract_site_timeseries(dataset: xr.Dataset, sites: pd.DataFrame) -> pd.DataFrame:
    """Return one daily record per site using nearest-coordinate selection."""
    frames: list[pd.DataFrame] = []

    for site in sites.itertuples(index=False):
        selected = dataset[["tmax_c", "precip_mm"]].sel(
            latitude=float(site.latitude),
            longitude=float(site.longitude),
            method="nearest",
        )
        frame = selected.to_dataframe().reset_index()
        frame["site_id"] = site.site_id
        frame["site_name"] = site.site_name
        frame["site_latitude"] = float(site.latitude)
        frame["site_longitude"] = float(site.longitude)
        frame = frame.rename(
            columns={"latitude": "grid_latitude", "longitude": "grid_longitude"}
        )
        frames.append(frame)

    columns = [
        "site_id",
        "site_name",
        "site_latitude",
        "site_longitude",
        "grid_latitude",
        "grid_longitude",
        "time",
        "tmax_c",
        "precip_mm",
    ]
    return pd.concat(frames, ignore_index=True).loc[:, columns]

