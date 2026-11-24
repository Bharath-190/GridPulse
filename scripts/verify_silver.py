#!/usr/bin/env python3
"""Read-only persistence and reconciliation checks for GridPulse Silver."""

from __future__ import annotations

import logging
from pathlib import Path

from pyspark.sql import functions as F
from silver_transform import make_spark

ROOT = Path(__file__).resolve().parents[1]
SILVER = ROOT / "data" / "silver" / "delta"

EXPECTED_COUNTS = {
    "silver_inverter_telemetry_5m": 150_824,
    "silver_site_hourly_conditions": 22_535,
    "silver_site_hourly_performance": 22_535,
}

KEYS = {
    "silver_inverter_telemetry_5m": ["site_id", "device_name", "event_ts_utc"],
    "silver_site_hourly_conditions": ["site_id", "event_ts_utc"],
    "silver_site_hourly_performance": ["site_id", "event_hour_utc"],
}


def main() -> int:
    logging.basicConfig(level=logging.INFO)
    spark = make_spark()
    failures: list[str] = []

    try:
        tables = {}
        print("\n=== SILVER TABLE COUNTS ===")
        for name, expected in EXPECTED_COUNTS.items():
            path = SILVER / name
            if not (path / "_delta_log").is_dir():
                failures.append(f"Missing Delta table: {name}")
                continue
            frame = spark.read.format("delta").load(str(path))
            tables[name] = frame
            actual = frame.count()
            print(f"{name}: {actual:,} rows (expected {expected:,})")
            if actual != expected:
                failures.append(f"{name}: expected {expected}, found {actual}")

        if len(tables) != 3:
            raise RuntimeError("One or more Silver Delta tables could not be loaded")

        print("\n=== KEY INTEGRITY ===")
        for name, frame in tables.items():
            keys = KEYS[name]
            null_expr = None
            for key in keys:
                cond = F.col(key).isNull()
                null_expr = cond if null_expr is None else (null_expr | cond)
            null_rows = frame.filter(null_expr).count()
            duplicate_groups = (
                frame.groupBy(*keys).count().filter(F.col("count") > 1).count()
            )
            print(
                f"{name}: null-key rows={null_rows}, "
                f"duplicate key groups={duplicate_groups}"
            )
            if null_rows:
                failures.append(f"{name} has {null_rows} rows with NULL business keys")
            if duplicate_groups:
                failures.append(f"{name} has {duplicate_groups} duplicate business-key groups")

        inverter = tables["silver_inverter_telemetry_5m"]
        conditions = tables["silver_site_hourly_conditions"]
        performance = tables["silver_site_hourly_performance"]

        print("\n=== DATA QUALITY DISTRIBUTIONS ===")
        for label, frame, field in (
            ("Five-minute telemetry", inverter, "data_quality_status"),
            ("Hourly conditions", conditions, "data_quality_status"),
            ("Hourly raw coverage", performance, "raw_coverage_status"),
            ("Hourly alignment", performance, "hour_alignment_status"),
        ):
            print(f"{label}:")
            frame.groupBy(field).count().orderBy(field).show(truncate=False)

        conflict_count = performance.filter(
            F.col("publisher_zero_conflict_with_raw_generation_flag")
        ).count()
        operational_gap_count = performance.filter(
            F.col("publisher_operational_fields_missing_flag")
        ).count()
        print(f"Publisher zero-vs-generation conflict hours: {conflict_count}")
        print(f"Publisher daylight operational-gap hours: {operational_gap_count}")

        bad_conflict_rows = performance.filter(
            F.col("publisher_zero_conflict_with_raw_generation_flag")
            & (
                (F.col("hour_alignment_status") != "publisher_zero_conflicts_with_raw_generation")
                | F.col("active_power_mean_abs_delta_kw").isNull()
                | F.col("active_power_comparison_eligible_flag")
            )
        ).count()
        bad_eligible_rows = performance.filter(
            F.col("active_power_comparison_eligible_flag")
            & (
                (F.col("hour_alignment_status") != "comparable_complete_hour")
                | F.col("active_power_mean_abs_delta_kw").isNull()
                | F.col("publisher_zero_conflict_with_raw_generation_flag")
            )
        ).count()
        unexpected_noncomparable_deltas = performance.filter(
            (F.col("hour_alignment_status") != "comparable_complete_hour")
            & (~F.col("publisher_zero_conflict_with_raw_generation_flag"))
            & F.col("active_power_mean_abs_delta_kw").isNotNull()
        ).count()

        print("\n=== SOURCE-CONFLICT INTEGRITY ===")
        print(f"Invalid conflict rows: {bad_conflict_rows}")
        print(f"Invalid comparison-eligible rows: {bad_eligible_rows}")
        print(f"Unexpected deltas on other non-comparable rows: {unexpected_noncomparable_deltas}")
        if bad_conflict_rows:
            failures.append("Source-conflict flags/status/deltas are inconsistent")
        if bad_eligible_rows:
            failures.append("Comparison-eligible flags/status/deltas are inconsistent")
        if unexpected_noncomparable_deltas:
            failures.append("Unexpected deltas exist on non-comparable, non-conflict rows")

        print("\n=== COMPARISON METRICS (ELIGIBLE HOURS ONLY) ===")
        (
            performance
            .filter(F.col("active_power_comparison_eligible_flag"))
            .groupBy("site_id")
            .agg(
                F.count("*").alias("eligible_hours"),
                F.avg("active_power_mean_abs_delta_kw").alias("mean_abs_delta_kw"),
                F.expr("percentile_approx(active_power_mean_abs_delta_kw, 0.95)")
                .alias("p95_abs_delta_kw"),
                F.max("active_power_mean_abs_delta_kw").alias("max_abs_delta_kw"),
            )
            .orderBy("site_id")
            .show(truncate=False)
        )

        if failures:
            print("\nVALIDATION FAILED:")
            for failure in failures:
                print(f" - {failure}")
            return 1

        print("\nALL SILVER PERSISTENCE AND SOURCE-CONFLICT CHECKS PASSED.")
        return 0
    finally:
        spark.stop()


if __name__ == "__main__":
    raise SystemExit(main())
