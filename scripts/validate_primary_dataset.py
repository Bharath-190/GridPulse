#!/usr/bin/env python3
"""Read-only structural validation for the GridPulse primary source dataset."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable

import pandas as pd

REQUIRED_HOURLY_COLUMNS = {
    "datetime_utc",
    "active_power_kw",
    "dc_input_power_kw",
    "daily_energy_kwh",
    "cumulative_energy_kwh",
    "inverter_temp_c",
    "grid_freq_hz",
    "power_factor",
    "efficiency_pct",
    "inverter_status",
    "temp_c",
    "humidity_pct",
    "cloud_cover_pct",
    "wind_speed_kmh",
    "ghi_wm2",
    "dni_wm2",
    "dhi_wm2",
    "precip_mm",
    "solar_elevation_deg",
    "capacity_factor",
}


def find_raw_exports(site_dir: Path) -> list[Path]:
    raw_dir = site_dir / "raw"
    if not raw_dir.is_dir():
        return []
    return sorted([*raw_dir.glob("*.xlsx"), *raw_dir.glob("*.xls")])


def validate_site(root: Path, site_name: str) -> tuple[bool, list[str]]:
    site_dir = root / site_name
    issues: list[str] = []
    hourly_file = site_dir / f"{site_name}_hourly_weather.csv"
    raw_files = find_raw_exports(site_dir)

    if not site_dir.is_dir():
        return False, [f"Missing folder: {site_dir}"]
    if not hourly_file.is_file():
        issues.append(f"Missing hourly file: {hourly_file.name}")
    if not raw_files:
        issues.append(f"No monthly raw Excel exports found under {site_name}/raw/")

    if hourly_file.is_file():
        try:
            frame = pd.read_csv(hourly_file, nrows=5)
            missing = sorted(REQUIRED_HOURLY_COLUMNS - set(frame.columns))
            if missing:
                issues.append("Hourly file missing required columns: " + ", ".join(missing))
            if "datetime_utc" in frame.columns:
                parsed = pd.to_datetime(frame["datetime_utc"], utc=True, errors="coerce")
                if parsed.isna().any():
                    issues.append("Some of the first five datetime_utc values cannot be parsed")
        except Exception as exc:  # report parser and filesystem failures
            issues.append(f"Could not read {hourly_file.name}: {exc}")

    print(f"\n{site_name}:")
    print(f"  Hourly file: {'FOUND' if hourly_file.is_file() else 'MISSING'}")
    print(f"  Raw Excel exports: {len(raw_files)}")
    return not issues, issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dataset-dir",
        type=Path,
        default=Path("data/external/PV-Generation-Dataset"),
        help="Path to the cloned publisher repository",
    )
    args = parser.parse_args()
    root = args.dataset_dir.expanduser().resolve()
    print(f"Checking dataset directory: {root}")
    if not root.exists():
        print("ERROR: dataset directory does not exist. Run the download script first.")
        return 2

    results = [validate_site(root, site) for site in ("site_a", "site_b")]
    issues = [issue for _, site_issues in results for issue in site_issues]
    if issues:
        print("\nValidation issues:")
        for issue in issues:
            print(f"  - {issue}")
        return 1
    print("\nPASS: both sites have hourly data and raw Excel exports.")
    print("Note: this is a structural check only; schema, units, and timestamp semantics still require profiling.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
