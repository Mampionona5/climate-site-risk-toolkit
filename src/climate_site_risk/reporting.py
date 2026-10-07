"""Human-readable visual and machine-readable pipeline reporting."""

import json
import os
import tempfile
from pathlib import Path
from typing import Any

_MATPLOTLIB_CACHE = Path(tempfile.gettempdir()) / "climate_site_risk_matplotlib"
_MATPLOTLIB_CACHE.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(_MATPLOTLIB_CACHE))

import matplotlib  # noqa: E402
import pandas as pd  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


def create_indicator_chart(indicators: pd.DataFrame, output_path: Path) -> None:
    """Create a compact annual comparison chart from monthly indicators."""
    annual = (
        indicators.groupby(["site_id", "site_name"], as_index=False)
        .agg(heat_days=("heat_days", "sum"), heavy_rain_days=("heavy_rain_days", "sum"))
        .sort_values("heat_days", ascending=True)
    )
    labels = annual["site_name"].tolist()
    positions = range(len(annual))

    figure, axes = plt.subplots(1, 2, figsize=(10, 4.8), constrained_layout=True)
    axes[0].barh(positions, annual["heat_days"], color="#D95F43")
    axes[0].set_title("Jours dépassant le seuil de chaleur")
    axes[0].set_yticks(list(positions), labels)
    axes[0].set_xlabel("Jours")

    axes[1].barh(positions, annual["heavy_rain_days"], color="#2D728F")
    axes[1].set_title("Jours dépassant le seuil de fortes pluies")
    axes[1].set_yticks(list(positions), labels)
    axes[1].set_xlabel("Jours")

    figure.suptitle("Indicateurs climatiques par site", fontsize=14, fontweight="bold")
    figure.savefig(output_path, dpi=160)
    plt.close(figure)


def write_run_summary(output_path: Path, payload: dict[str, Any]) -> None:
    """Write deterministic, readable run metadata as JSON."""
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

