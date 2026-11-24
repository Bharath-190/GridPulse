#!/usr/bin/env python3
"""Fetch optional hourly ERA5 weather context for anonymized site coordinates.

Use only approximate coordinates supplied by the data publisher. Do not treat
these records as exact on-site weather measurements.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

import pandas as pd
import requests

API_URL = "https://archive-api.open-meteo.com/v1/archive"
HOURLY_VARIABLES = [
    "temperature_2m",
    "relative_humidity_2m",
    "precipitation",
    "cloud_cover",
    "wind_speed_10m",
    "wind_speed_100m",
    "shortwave_radiation",
    "direct_radiation",
    "diffuse_radiation",
    "direct_normal_irradiance",
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--latitude", type=float, required=True)
    parser.add_argument("--longitude", type=float, required=True)
    parser.add_argument("--start", required=True, help="YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="YYYY-MM-DD")
    parser.add_argument("--site-id", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    start = pd.to_datetime(args.start, errors="raise").date()
    end = pd.to_datetime(args.end, errors="raise").date()
    if end < start:
        parser.error("--end must be on or after --start")

    params = {
        "latitude": args.latitude,
        "longitude": args.longitude,
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "hourly": ",".join(HOURLY_VARIABLES),
        "timezone": "UTC",
        "timeformat": "iso8601",
        "models": "era5",
        "format": "csv",
    }

    try:
        response = requests.get(API_URL, params=params, timeout=90)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"ERROR: Open-Meteo request failed: {exc}", file=sys.stderr)
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(response.content)
    print(f"Saved weather response to {args.output}")
    print("Attribution required: Weather data by Open-Meteo.com (CC BY 4.0).")
    print("Coordinates are approximate; label these as regional reanalysis context.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
