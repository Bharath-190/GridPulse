#!/usr/bin/env python3
"""
Read-only audit of Silver hourly performance keys.

Compares:
1. Distinct hours in five-minute inverter telemetry.
2. Distinct hours in publisher hourly conditions.
3. Their expected full outer union.
4. Actual keys in silver_site_hourly_performance.

Does not modify Bronze or Silver Delta tables.
"""

import sys
from pathlib import Path

from pyspark.sql import functions as F

# Make scripts/ importable without modifying production modules.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from silver_transform import make_spark  # noqa: E402


SILVER_ROOT = PROJECT_ROOT / "data" / "silver" / "delta"

TABLES = {
    "telemetry": "silver_inverter_telemetry_5m",
    "conditions": "silver_site_hourly_conditions",
    "performance": "silver_site_hourly_performance",
}

KEYS = ["site_id", "event_hour_utc"]


def load_table(spark, table_name):
    path = SILVER_ROOT / table_name

    if not (path / "_delta_log").is_dir():
        raise FileNotFoundError(
            f"Silver Delta table not found: {path}"
        )

    print(f"Loading: {table_name}")
    return spark.read.format("delta").load(str(path))


def main():
    spark = make_spark()

    try:
        print("\n=== SPARK CONFIGURATION ===")
        print(
            "Session timezone:",
            spark.conf.get("spark.sql.session.timeZone")
        )

        print("\n=== LOADING SILVER TABLES ===")

        telemetry = load_table(
            spark, TABLES["telemetry"]
        )

        conditions = load_table(
            spark, TABLES["conditions"]
        )

        performance = load_table(
            spark, TABLES["performance"]
        )

        # Validate required columns before running the audit.
        required = {
            "telemetry": {"site_id", "event_ts_utc"},
            "conditions": {"site_id", "event_ts_utc"},
            "performance": {"site_id", "event_hour_utc"},
        }

        frames = {
            "telemetry": telemetry,
            "conditions": conditions,
            "performance": performance,
        }

        for name, frame in frames.items():
            missing_columns = required[name] - set(frame.columns)

            if missing_columns:
                raise ValueError(
                    f"{name} is missing columns: "
                    f"{sorted(missing_columns)}"
                )

        # Five-minute readings aggregated into UTC hour keys.
        raw_hours = (
            telemetry
            .groupBy(
                "site_id",
                F.date_trunc(
                    "hour", F.col("event_ts_utc")
                ).alias("event_hour_utc")
            )
            .agg(
                F.count("*").alias("raw_sample_count")
            )
        )

        # Publisher hourly records represented as UTC hour keys.
        publisher_hours = (
            conditions
            .select(
                "site_id",
                F.date_trunc(
                    "hour", F.col("event_ts_utc")
                ).alias("event_hour_utc")
            )
            .distinct()
        )

        # Identify hours present in only one source.
        raw_only = raw_hours.join(
            publisher_hours,
            KEYS,
            "left_anti"
        )

        publisher_only = publisher_hours.join(
            raw_hours.select(*KEYS),
            KEYS,
            "left_anti"
        )

        # Expected full outer union of both source key sets.
        expected = (
            raw_hours
            .select(*KEYS)
            .unionByName(publisher_hours)
            .distinct()
        )

        # Actual distinct keys in Silver performance.
        actual = performance.select(*KEYS).distinct()

        # Identify missing and unexpected performance keys.
        missing = expected.join(
            actual,
            KEYS,
            "left_anti"
        )

        unexpected = actual.join(
            expected,
            KEYS,
            "left_anti"
        )

        # Count source and output records.
        print("\n=== FULL OUTER JOIN KEY AUDIT ===")

        print(
            "Five-minute telemetry rows:",
            telemetry.count()
        )

        print(
            "Publisher hourly rows:",
            conditions.count()
        )

        print(
            "Silver performance rows:",
            performance.count()
        )

        print(
            "Distinct raw telemetry hours:",
            raw_hours.count()
        )

        print(
            "Distinct publisher hours:",
            publisher_hours.count()
        )

        print(
            "Raw-only hours:",
            raw_only.count()
        )

        print(
            "Publisher-only hours:",
            publisher_only.count()
        )

        print(
            "Expected union hours:",
            expected.count()
        )

        print(
            "Actual performance hours:",
            actual.count()
        )

        print(
            "Missing performance keys:",
            missing.count()
        )

        print(
            "Unexpected performance keys:",
            unexpected.count()
        )

        print("\n=== RAW-ONLY HOURS ===")
        raw_only.orderBy(
            "event_hour_utc"
        ).show(50, truncate=False)

        print("\n=== PUBLISHER-ONLY HOURS ===")
        publisher_only.orderBy(
            "event_hour_utc"
        ).show(50, truncate=False)

        print("\n=== MISSING PERFORMANCE KEYS ===")
        missing.orderBy(
            "event_hour_utc"
        ).show(50, truncate=False)

        print("\n=== UNEXPECTED PERFORMANCE KEYS ===")
        unexpected.orderBy(
            "event_hour_utc"
        ).show(50, truncate=False)

        print("\n=== PERFORMANCE STATUS COUNTS ===")
        performance.groupBy(
            "hour_alignment_status"
        ).count().orderBy(
            "hour_alignment_status"
        ).show(truncate=False)

        expected_count = expected.count()
        actual_count = actual.count()
        missing_count = missing.count()
        unexpected_count = unexpected.count()

        print("\n=== AUDIT RESULT ===")

        if (
            expected_count == actual_count
            and missing_count == 0
            and unexpected_count == 0
        ):
            print(
                "PASS: Silver performance contains exactly "
                "the expected union of source hours."
            )
        else:
            print(
                "FAIL: Silver performance keys do not match "
                "the expected source-hour union."
            )

    finally:
        spark.stop()


if __name__ == "__main__":
    main()
