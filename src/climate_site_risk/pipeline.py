"""End-to-end orchestration for the climate site indicator use case."""

from pathlib import Path

from climate_site_risk.extraction import extract_site_timeseries
from climate_site_risk.indicators import compute_monthly_indicators
from climate_site_risk.models import Thresholds
from climate_site_risk.reporting import create_indicator_chart, write_run_summary
from climate_site_risk.validation import (
    load_and_validate_sites,
    load_dataset,
    require_valid_dataset,
)


def run_pipeline(
    dataset_path: Path,
    sites_path: Path,
    output_dir: Path,
    thresholds: Thresholds | None = None,
) -> dict[str, Path]:
    """Validate inputs, calculate indicators, and write decision-ready outputs."""
    active_thresholds = thresholds or Thresholds()
    dataset = load_dataset(dataset_path)
    report = require_valid_dataset(dataset)
    sites = load_and_validate_sites(sites_path)

    timeseries = extract_site_timeseries(dataset, sites)
    indicators = compute_monthly_indicators(timeseries, active_thresholds)

    output_dir.mkdir(parents=True, exist_ok=True)
    timeseries_path = output_dir / "site_timeseries.csv"
    indicators_path = output_dir / "monthly_site_indicators.csv"
    chart_path = output_dir / "site_indicator_comparison.png"
    summary_path = output_dir / "run_summary.json"

    timeseries.to_csv(timeseries_path, index=False)
    indicators.to_csv(indicators_path, index=False)
    create_indicator_chart(indicators, chart_path)
    write_run_summary(
        summary_path,
        {
            "dataset": dataset_path.name,
            "sites_file": sites_path.name,
            "site_count": int(sites.shape[0]),
            "daily_record_count": int(timeseries.shape[0]),
            "monthly_record_count": int(indicators.shape[0]),
            "period_start": str(timeseries["time"].min().date()),
            "period_end": str(timeseries["time"].max().date()),
            "thresholds": {
                "heat_c": active_thresholds.heat_c,
                "heavy_rain_mm": active_thresholds.heavy_rain_mm,
                "dry_day_mm": active_thresholds.dry_day_mm,
            },
            "validation_warnings": list(report.warnings),
        },
    )

    return {
        "timeseries": timeseries_path,
        "indicators": indicators_path,
        "chart": chart_path,
        "summary": summary_path,
    }

