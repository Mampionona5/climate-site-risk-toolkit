"""End-to-end test using only synthetic local inputs."""

import json
from pathlib import Path

import pandas as pd

from climate_site_risk.pipeline import run_pipeline
from climate_site_risk.sample_data import create_sample_inputs


def test_sample_pipeline_creates_expected_outputs(tmp_path: Path) -> None:
    """The public pipeline should create complete and internally consistent outputs."""
    dataset_path, sites_path = create_sample_inputs(tmp_path / "inputs")

    outputs = run_pipeline(dataset_path, sites_path, tmp_path / "outputs")

    assert all(path.exists() and path.stat().st_size > 0 for path in outputs.values())
    indicators = pd.read_csv(outputs["indicators"])
    assert indicators["site_id"].nunique() == 3
    assert len(indicators) == 36

    summary = json.loads(outputs["summary"].read_text(encoding="utf-8"))
    assert summary["site_count"] == 3
    assert summary["daily_record_count"] == 1098
    assert summary["period_start"] == "2024-01-01"
    assert summary["period_end"] == "2024-12-31"

