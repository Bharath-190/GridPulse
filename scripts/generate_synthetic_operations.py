#!/usr/bin/env python3
"""Generate clearly labelled synthetic asset and maintenance reference data."""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

SITES = [
    {"site_id": "SITE_A", "country": "Romania", "region": "Southwestern Romania", "nominal_inverter_capacity_kw": 50, "coverage_start": "2025-01-04", "coverage_end": "2026-06-30"},
    {"site_id": "SITE_B", "country": "Romania", "region": "Southwestern Romania", "nominal_inverter_capacity_kw": 50, "coverage_start": "2025-05-01", "coverage_end": "2026-05-31"},
]

ASSET_TYPES = [
    ("inverter", 1),
    ("transformer", 1),
    ("weather_monitoring_unit", 1),
    ("communications_gateway", 1),
    ("pv_array_block", 2),
]

MAINTENANCE_TYPES = ["inspection", "cleaning", "firmware_update", "thermal_check", "communications_check", "corrective_repair"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("data/synthetic"))
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--events-per-asset", type=int, default=3)
    args = parser.parse_args()
    if args.events_per_asset < 0:
        parser.error("--events-per-asset must be >= 0")

    rng = np.random.default_rng(args.seed)
    output = args.output_dir
    output.mkdir(parents=True, exist_ok=True)

    site_rows = []
    for site in SITES:
        site_rows.append({
            **site,
            "source_dataset": "upb-nlp/PV-Generation-Dataset",
            "site_details_origin": "publisher_documentation",
            "record_origin": "reference_metadata",
            "is_synthetic": False,
            "coordinate_precision_note": "Approximate region only; exact site coordinates are anonymized",
        })
    pd.DataFrame(site_rows).to_csv(output / "site_reference.csv", index=False)

    assets = []
    for site in SITES:
        prefix = site["site_id"].replace("_", "")
        for asset_type, count in ASSET_TYPES:
            for number in range(1, count + 1):
                asset_id = f"SYN-{prefix}-{asset_type.upper()}-{number:02d}"
                assets.append({
                    "asset_id": asset_id,
                    "site_id": site["site_id"],
                    "asset_type": asset_type,
                    "asset_label": f"Illustrative {asset_type.replace('_', ' ')} {number}",
                    "nominal_rating_kw": site["nominal_inverter_capacity_kw"] if asset_type == "inverter" else np.nan,
                    "commissioned_date": str(rng.choice(pd.date_range("2021-01-01", "2024-12-31", freq="D").strftime("%Y-%m-%d"))),
                    "manufacturer": "SIMULATED",
                    "model": "SIMULATED",
                    "record_origin": "synthetic",
                    "is_synthetic": True,
                    "scenario_version": "0.1.0",
                })

    asset_frame = pd.DataFrame(assets)
    asset_frame.to_csv(output / "synthetic_asset_registry.csv", index=False)

    event_rows = []
    for asset in assets:
        site = next(item for item in SITES if item["site_id"] == asset["site_id"])
        start = pd.Timestamp(site["coverage_start"])
        end = pd.Timestamp(site["coverage_end"])
        days = max(1, (end - start).days)
        for idx in range(args.events_per_asset):
            event_day = start + pd.Timedelta(days=int(rng.integers(0, days + 1)))
            duration_hours = round(float(rng.choice([0.5, 1, 2, 4, 8, 12, 24])), 2)
            event_rows.append({
                "event_id": f"SYN-EVT-{asset['asset_id']}-{idx + 1:03d}",
                "site_id": asset["site_id"],
                "asset_id": asset["asset_id"],
                "event_timestamp_utc": event_day.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "maintenance_type": str(rng.choice(MAINTENANCE_TYPES)),
                "event_severity": str(rng.choice(["low", "medium", "high"], p=[0.55, 0.35, 0.10])),
                "downtime_hours": duration_hours,
                "estimated_cost_eur": round(float(rng.uniform(50, 1800)), 2),
                "event_status": str(rng.choice(["completed", "investigated", "scheduled"], p=[0.7, 0.2, 0.1])),
                "record_origin": "synthetic",
                "is_synthetic": True,
                "scenario_version": "0.1.0",
            })

    pd.DataFrame(event_rows).to_csv(output / "synthetic_maintenance_events.csv", index=False)
    print(f"Wrote {output / 'site_reference.csv'}")
    print(f"Wrote {output / 'synthetic_asset_registry.csv'} ({len(assets)} synthetic assets)")
    print(f"Wrote {output / 'synthetic_maintenance_events.csv'} ({len(event_rows)} synthetic events)")
    print("WARNING: asset inventory and maintenance events are simulated scenario data, not measured site records.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
