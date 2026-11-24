#!/usr/bin/env python3
"""Read-only inspection of Site B around remaining DST-transition discrepancies."""
from pathlib import Path
from pyspark.sql import functions as F

from silver_transform import make_spark

ROOT = Path(__file__).resolve().parents[1]
BRONZE = ROOT / "data" / "bronze" / "delta"
INVERTER_PATH = BRONZE / "bronze_inverter_telemetry_5m"
HOURLY_PATH = BRONZE / "bronze_site_hourly_weather"


def require_columns(frame, table_name, required):
    missing = sorted(set(required) - set(frame.columns))
    if missing:
        raise RuntimeError(f"{table_name} is missing required columns: {missing}; found={frame.columns}")


def main():
    spark = make_spark()
    spark.conf.set("spark.sql.session.timeZone", "UTC")
    try:
        print(f"Spark session timezone: {spark.conf.get('spark.sql.session.timeZone')}")
        inverter = spark.read.format("delta").load(str(INVERTER_PATH))
        publisher = spark.read.format("delta").load(str(HOURLY_PATH))

        require_columns(
            inverter,
            "bronze_inverter_telemetry_5m",
            ["site_id", "event_ts_utc", "active_power_kw", "timestamp_local"],
        )
        require_columns(
            publisher,
            "bronze_site_hourly_weather",
            ["site_id", "event_ts_utc", "active_power_kw"],
        )

        print("\n=== BRONZE COUNTS ===")
        print(f"Five-minute telemetry rows: {inverter.count():,}")
        print(f"Publisher hourly rows: {publisher.count():,}")

        print("\n=== SOURCE SCHEMAS ===")
        print("Five-minute telemetry:")
        inverter.printSchema()
        print("Publisher hourly:")
        publisher.printSchema()

        inv_b = inverter.filter(F.col("site_id") == "site_b")
        pub_b = publisher.filter(F.col("site_id") == "site_b")

        raw_aggs = [
            F.count(F.lit(1)).alias("raw_sample_count"),
            F.avg("active_power_kw").alias("raw_mean_power_kw"),
            F.min("timestamp_local").cast("string").alias("raw_first_local"),
            F.max("timestamp_local").cast("string").alias("raw_last_local"),
        ]
        if "timezone_suffix" in inv_b.columns:
            raw_aggs.append(F.sort_array(F.collect_set("timezone_suffix")).alias("raw_suffixes"))
        if "timezone_resolution" in inv_b.columns:
            raw_aggs.append(F.sort_array(F.collect_set("timezone_resolution")).alias("raw_resolutions"))

        raw_hourly = (
            inv_b
            .withColumn("event_hour_utc", F.date_trunc("hour", F.col("event_ts_utc")))
            .groupBy("event_hour_utc")
            .agg(*raw_aggs)
        )

        pub_aggs = [
            F.count(F.lit(1)).alias("publisher_rows"),
            F.avg("active_power_kw").alias("publisher_power_kw"),
        ]
        if "datetime_local" in pub_b.columns:
            pub_aggs.append(F.first(F.col("datetime_local").cast("string"), ignorenulls=True).alias("publisher_local"))
        pub_hourly = (
            pub_b
            .withColumn("event_hour_utc", F.date_trunc("hour", F.col("event_ts_utc")))
            .groupBy("event_hour_utc")
            .agg(*pub_aggs)
        )

        print("\n=== SITE B HOURLY ALIGNMENT: 2025-10-26 UTC ===")
        joined = raw_hourly.join(pub_hourly, "event_hour_utc", "full_outer")
        day1 = joined.filter(
            (F.col("event_hour_utc") >= F.to_timestamp(F.lit("2025-10-26 00:00:00")))
            & (F.col("event_hour_utc") < F.to_timestamp(F.lit("2025-10-27 00:00:00")))
        )
        day1.orderBy("event_hour_utc").show(40, truncate=False)

        print("\n=== SITE B HOURLY ALIGNMENT: 2026-03-29 UTC ===")
        day2 = joined.filter(
            (F.col("event_hour_utc") >= F.to_timestamp(F.lit("2026-03-29 00:00:00")))
            & (F.col("event_hour_utc") < F.to_timestamp(F.lit("2026-03-30 00:00:00")))
        )
        day2.orderBy("event_hour_utc").show(40, truncate=False)

        print("\n=== FIVE-MINUTE RECORDS AROUND FALL-BACK (LOCAL 2025-10-26) ===")
        inv_b.filter(
            (F.col("event_ts_utc") >= F.to_timestamp(F.lit("2025-10-25 21:00:00")))
            & (F.col("event_ts_utc") < F.to_timestamp(F.lit("2025-10-26 04:00:00")))
        ).select(
            "event_ts_utc", "timestamp_local", "timezone_suffix",
            "timezone_resolution", "active_power_kw"
        ).orderBy("event_ts_utc").show(100, truncate=False)

        print("\n=== FIVE-MINUTE RECORDS AROUND SPRING-FORWARD (LOCAL 2026-03-29) ===")
        inv_b.filter(
            (F.col("event_ts_utc") >= F.to_timestamp(F.lit("2026-03-28 21:00:00")))
            & (F.col("event_ts_utc") < F.to_timestamp(F.lit("2026-03-29 04:00:00")))
        ).select(
            "event_ts_utc", "timestamp_local", "timezone_suffix",
            "timezone_resolution", "active_power_kw"
        ).orderBy("event_ts_utc").show(100, truncate=False)

        print("\n=== HIGH-DISCREPANCY HOURS ON BOTH DATES ===")
        joined.filter(
            (F.col("event_hour_utc") >= F.to_timestamp(F.lit("2025-10-26 00:00:00")))
            & (F.col("event_hour_utc") < F.to_timestamp(F.lit("2025-10-27 00:00:00")))
            | (F.col("event_hour_utc") >= F.to_timestamp(F.lit("2026-03-29 00:00:00")))
            & (F.col("event_hour_utc") < F.to_timestamp(F.lit("2026-03-30 00:00:00")))
        ).withColumn(
            "abs_delta_kw", F.abs(F.col("raw_mean_power_kw") - F.col("publisher_power_kw"))
        ).filter(F.col("abs_delta_kw") > 1.0).orderBy(
            F.desc("abs_delta_kw")
        ).show(50, truncate=False)

        print("\nRead-only diagnostic complete. No Delta data was modified.")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
