"""Input-contract validation for datasets and site tables."""

from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import xarray as xr

REQUIRED_COORDINATES = ("time", "latitude", "longitude")
REQUIRED_VARIABLES = ("tmax_c", "precip_mm")
REQUIRED_SITE_COLUMNS = ("site_id", "site_name", "latitude", "longitude")


@dataclass(frozen=True, slots=True)
class ValidationReport:
    """Structured validation outcome suitable for CLI and programmatic use."""

    errors: tuple[str, ...]
    warnings: tuple[str, ...]

    @property
    def is_valid(self) -> bool:
        """Return whether validation found no blocking errors."""
        return not self.errors


def load_dataset(path: Path) -> xr.Dataset:
    """Load a NetCDF dataset into memory and close the underlying file handle."""
    with xr.open_dataset(path) as opened:
        return opened.load()


def validate_dataset(dataset: xr.Dataset) -> ValidationReport:
    """Validate the minimum dataset contract required by the pipeline."""
    errors: list[str] = []
    warnings: list[str] = []

    for coordinate in REQUIRED_COORDINATES:
        if coordinate not in dataset.coords:
            errors.append(f"Coordonnée manquante : {coordinate}")

    for variable in REQUIRED_VARIABLES:
        if variable not in dataset.data_vars:
            errors.append(f"Variable manquante : {variable}")

    if errors:
        return ValidationReport(tuple(errors), tuple(warnings))

    if dataset.sizes["time"] == 0:
        errors.append("La coordonnée temporelle est vide")
    if not dataset.indexes["time"].is_unique:
        errors.append("La coordonnée temporelle contient des doublons")
    if not dataset.indexes["latitude"].is_unique:
        errors.append("La coordonnée de latitude contient des doublons")
    if not dataset.indexes["longitude"].is_unique:
        errors.append("La coordonnée de longitude contient des doublons")

    for variable in REQUIRED_VARIABLES:
        missing_count = int(dataset[variable].isnull().sum().item())
        if missing_count:
            warnings.append(f"{variable} contient {missing_count} valeurs manquantes")

    return ValidationReport(tuple(errors), tuple(warnings))


def load_and_validate_sites(path: Path) -> pd.DataFrame:
    """Load a site CSV and raise a clear error when its contract is invalid."""
    sites = pd.read_csv(path)
    missing_columns = [column for column in REQUIRED_SITE_COLUMNS if column not in sites.columns]
    if missing_columns:
        raise ValueError(f"Colonnes de sites manquantes : {', '.join(missing_columns)}")
    if sites.empty:
        raise ValueError("Le tableau des sites est vide")
    if sites["site_id"].isna().any() or sites["site_id"].duplicated().any():
        raise ValueError("Les valeurs site_id doivent être présentes et uniques")

    for coordinate in ("latitude", "longitude"):
        sites[coordinate] = pd.to_numeric(sites[coordinate], errors="raise")
    if not sites["latitude"].between(-90, 90).all():
        raise ValueError("La latitude d'un site doit être comprise entre -90 et 90")
    if not sites["longitude"].between(-180, 180).all():
        raise ValueError("La longitude d'un site doit être comprise entre -180 et 180")

    return sites.loc[:, list(REQUIRED_SITE_COLUMNS)].copy()


def require_valid_dataset(dataset: xr.Dataset) -> ValidationReport:
    """Return the report or raise one exception containing every validation error."""
    report = validate_dataset(dataset)
    if not report.is_valid:
        raise ValueError("Jeu de données climatiques invalide : " + "; ".join(report.errors))
    return report

