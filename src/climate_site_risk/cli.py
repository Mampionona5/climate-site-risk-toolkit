"""Command-line interface for sample generation, validation, and pipeline execution."""

import argparse
import json
import sys
from pathlib import Path

from climate_site_risk.models import Thresholds
from climate_site_risk.pipeline import run_pipeline
from climate_site_risk.sample_data import create_sample_inputs
from climate_site_risk.validation import load_dataset, validate_dataset


def build_parser() -> argparse.ArgumentParser:
    """Build the command tree without causing side effects."""
    parser = argparse.ArgumentParser(
        prog="climate-site-risk",
        description="Créer des indicateurs lisibles à partir de données climatiques maillées.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    sample_parser = subparsers.add_parser("sample", help="Générer un jeu d'exemple reproductible")
    sample_parser.add_argument("--output-dir", type=Path, default=Path("sample_data"))
    sample_parser.add_argument("--seed", type=int, default=42)

    validate_parser = subparsers.add_parser("validate", help="Valider un jeu de données NetCDF")
    validate_parser.add_argument("--dataset", type=Path, required=True)

    run_parser = subparsers.add_parser("run", help="Exécuter le pipeline complet")
    run_parser.add_argument("--dataset", type=Path, required=True)
    run_parser.add_argument("--sites", type=Path, required=True)
    run_parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    run_parser.add_argument("--heat-threshold", type=float, default=35.0)
    run_parser.add_argument("--heavy-rain-threshold", type=float, default=20.0)
    run_parser.add_argument("--dry-day-threshold", type=float, default=1.0)
    return parser


def main(argv: list[str] | None = None) -> None:
    """Execute a CLI command and return a non-zero status for invalid input."""
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "sample":
            dataset_path, sites_path = create_sample_inputs(args.output_dir, seed=args.seed)
            print(f"Fichier créé : {dataset_path}")
            print(f"Fichier créé : {sites_path}")
            return

        if args.command == "validate":
            report = validate_dataset(load_dataset(args.dataset))
            payload = {
                "valid": report.is_valid,
                "errors": report.errors,
                "warnings": report.warnings,
            }
            print(json.dumps(payload))
            if not report.is_valid:
                raise SystemExit(1)
            return

        thresholds = Thresholds(
            heat_c=args.heat_threshold,
            heavy_rain_mm=args.heavy_rain_threshold,
            dry_day_mm=args.dry_day_threshold,
        )
        outputs = run_pipeline(args.dataset, args.sites, args.output_dir, thresholds)
        for name, path in outputs.items():
            print(f"{name} : {path}")
    except (FileNotFoundError, OSError, ValueError) as error:
        print(f"Erreur : {error}", file=sys.stderr)
        raise SystemExit(2) from error

