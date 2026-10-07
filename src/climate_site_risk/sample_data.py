"""Generate safe, deterministic sample inputs for local execution."""

from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr


def create_sample_inputs(output_dir: Path, seed: int = 42) -> tuple[Path, Path]:
    """Create one year of reproducible gridded climate data and fictional sites."""
    output_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)

    time = pd.date_range("2024-01-01", "2024-12-31", freq="D")
    latitude = np.linspace(43.5, 44.5, 8)
    longitude = np.linspace(2.8, 4.2, 10)
    shape = (time.size, latitude.size, longitude.size)

    day_angle = 2 * np.pi * (np.arange(time.size) - 172) / 366
    seasonal_heat = 27 + 9 * np.cos(day_angle)
    spatial_heat = (latitude.max() - latitude)[None, :, None] * 1.2
    temperature_noise = rng.normal(0, 2.0, size=shape)
    tmax_c = seasonal_heat[:, None, None] + spatial_heat + temperature_noise

    wet_season = 1.0 + 0.45 * np.cos(day_angle + np.pi / 3)
    precip_mm = rng.gamma(shape=1.3, scale=5.0, size=shape) * wet_season[:, None, None]
    dry_mask = rng.random(shape) < 0.42
    precip_mm[dry_mask] = 0.0

    dataset = xr.Dataset(
        data_vars={
            "tmax_c": (
                ("time", "latitude", "longitude"),
                tmax_c.astype("float32"),
                {"units": "degree_Celsius", "long_name": "daily maximum temperature"},
            ),
            "precip_mm": (
                ("time", "latitude", "longitude"),
                precip_mm.astype("float32"),
                {"units": "mm/day", "long_name": "daily precipitation"},
            ),
        },
        coords={"time": time, "latitude": latitude, "longitude": longitude},
        attrs={
            "title": "Jeu d'exemple climatique reproductible",
            "source": "Généré localement, sans données observées ni projections",
            "random_seed": seed,
        },
    )

    dataset_path = output_dir / "climate_sample.nc"
    dataset.to_netcdf(dataset_path, engine="scipy")

    sites = pd.DataFrame(
        [
            {"site_id": "SITE_A", "site_name": "Pôle Nord", "latitude": 44.2, "longitude": 3.25},
            {
                "site_id": "SITE_B",
                "site_name": "Dépôt central",
                "latitude": 44.0,
                "longitude": 3.55,
            },
            {
                "site_id": "SITE_C",
                "site_name": "Clinique Sud",
                "latitude": 43.7,
                "longitude": 3.9,
            },
        ]
    )
    sites_path = output_dir / "sites.csv"
    sites.to_csv(sites_path, index=False)
    return dataset_path, sites_path

