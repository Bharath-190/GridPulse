#!/usr/bin/env python3
"""Read-only investigation of Excel-vs-hourly timestamp semantics in GridPulse.

Compares three interpretations of the Excel timestamp:
  A. Current Bronze event_ts_utc (localized in Europe/Bucharest)
  B. timestamp_local treated as a UTC wall-clock value
  C. timestamp_local matched to publisher datetime_local wall-clock value

No Delta tables are written or modified.
"""
from pathlib import Path
from pyspark.sql import functions as F
from silver_transform import make_spark

ROOT = Path(__file__).resolve().parents[1]
BRONZE = ROOT / "data" / "bronze" / "delta"
RAW_PATH = BRONZE / "bronze_inverter_telemetry_5m"
HOURLY_PATH = BRONZE / "bronze_site_hourly_weather"


def summarize_pairs(pairs, label):
    delta = F.col("publisher_power") - F.col("raw_power")
    scored = pairs.withColumn("abs_error_kw", F.abs(delta)).withColumn(
        "sq_error_kw", F.pow(delta, 2)
    )
    print(f"\n=== {label} ===")
    (
        scored.groupBy("site_id")
        .agg(
            F.count("*").alias("paired_hours"),
            F.avg("abs_error_kw").alias("mae_kw"),
            F.expr("percentile_approx(abs_error_kw, 0.50)").alias("median_abs_error_kw"),
            F.expr("percentile_approx(abs_error_kw, 0.95)").alias("p95_abs_error_kw"),
            F.max("abs_error_kw").alias("max_abs_error_kw"),
            F.sqrt(F.avg("sq_error_kw")).alias("rmse_kw"),
            F.corr("publisher_power", "raw_power").alias("correlation"),
        )
        .orderBy("site_id")
        .show(truncate=False)
    )
    return scored


def make_hourly_raw(raw, timestamp_col, hour_alias):
    keyed = raw.withColumn(hour_alias, F.date_trunc("hour", F.col(timestamp_col)))
    return (
        keyed.groupBy("site_id", hour_alias)
        .agg(
            F.countDistinct(timestamp_col).alias("sample_count"),
            F.avg("active_power_kw").alias("raw_power"),
            F.min("active_power_kw").alias("raw_min_kw"),
            F.max("active_power_kw").alias("raw_max_kw"),
        )
        .filter((F.col("sample_count") == 12) & F.col("raw_power").isNotNull())
    )


def show_examples(pairs, label):
    print(f"\n--- Largest discrepancies: {label} ---")
    delta = F.abs(F.col("publisher_power") - F.col("raw_power"))
    (
        pairs.withColumn("abs_error_kw", delta)
        .select("site_id", "match_hour", "publisher_power", "raw_power", "abs_error_kw")
        .orderBy(F.desc("abs_error_kw"))
        .show(12, truncate=False)
    )


def main():
    if not (RAW_PATH / "_delta_log").is_dir():
        raise FileNotFoundError(RAW_PATH)
    if not (HOURLY_PATH / "_delta_log").is_dir():
        raise FileNotFoundError(HOURLY_PATH)

    spark = make_spark()
    try:
        print("Spark session timezone:", spark.conf.get("spark.sql.session.timeZone"))
        raw = spark.read.format("delta").load(str(RAW_PATH))
        hourly = spark.read.format("delta").load(str(HOURLY_PATH))

        required_raw = {"site_id", "event_ts_utc", "timestamp_local", "timezone_suffix", "timezone_resolution", "active_power_kw"}
        required_hourly = {"site_id", "event_ts_utc", "datetime_local", "active_power_kw", "ghi_wm2", "solar_elevation_deg"}
        missing_raw = sorted(required_raw - set(raw.columns))
        missing_hourly = sorted(required_hourly - set(hourly.columns))
        if missing_raw or missing_hourly:
            raise ValueError(f"Missing columns: raw={missing_raw}, hourly={missing_hourly}")

        print("\n=== SOURCE TIMESTAMP SUFFIX AND RESOLUTION ===")
        raw.groupBy("site_id", "timezone_suffix", "timezone_resolution").count().orderBy(
            "site_id", "timezone_suffix", "timezone_resolution"
        ).show(100, truncate=False)

        print("\n=== RAW TIMESTAMP EXAMPLES (CURRENT UTC VS SOURCE WALL CLOCK) ===")
        (
            raw.select(
                "site_id", "timestamp_raw", "timestamp_local", "timezone_suffix",
                "timezone_resolution", "event_ts_utc", "active_power_kw",
            )
            .filter(
                F.to_date("event_ts_utc").isin(
                    "2025-03-19", "2026-04-08", "2025-03-20"
                )
            )
            .orderBy("site_id", "event_ts_utc")
            .show(60, truncate=False)
        )

        # The CSV's local timestamp includes a numeric offset (e.g. +0300).
        # Its first 19 characters are the local wall-clock representation.
        publisher = hourly.select(
            "site_id",
            F.date_trunc("hour", F.col("event_ts_utc")).alias("publisher_utc_hour"),
            F.date_trunc(
                "hour", F.to_timestamp(F.substring("datetime_local", 1, 19), "yyyy-MM-dd HH:mm:ss")
            ).alias("publisher_local_hour"),
            F.col("active_power_kw").alias("publisher_power"),
            "datetime_local", "ghi_wm2", "solar_elevation_deg",
        ).filter(F.col("publisher_power").isNotNull())

        # A: Existing Bronze UTC key, which currently localizes Excel timestamps.
        raw_a = make_hourly_raw(raw, "event_ts_utc", "match_hour")
        pairs_a = publisher.join(
            raw_a.select("site_id", F.col("match_hour").alias("publisher_utc_hour"), "raw_power", "sample_count"),
            ["site_id", "publisher_utc_hour"], "inner"
        ).select("site_id", F.col("publisher_utc_hour").alias("match_hour"), "publisher_power", "raw_power", "sample_count")
        scored_a = summarize_pairs(pairs_a, "A — current localized Bronze UTC vs publisher UTC")
        show_examples(pairs_a, "A — current localized UTC")

        # Parse the preserved local wall-clock as a timestamp while Spark session TZ is UTC.
        raw_with_wall = raw.withColumn(
            "source_wall_clock_as_utc",
            F.to_timestamp("timestamp_local", "yyyy-MM-dd HH:mm:ss")
        )
        invalid_wall = raw_with_wall.filter(F.col("source_wall_clock_as_utc").isNull()).count()
        print(f"\nUnparseable timestamp_local rows: {invalid_wall}")

        # B: Test whether the Excel wall-clock may actually be UTC already.
        raw_b = make_hourly_raw(raw_with_wall, "source_wall_clock_as_utc", "match_hour")
        pairs_b = publisher.join(
            raw_b.select("site_id", F.col("match_hour").alias("publisher_utc_hour"), "raw_power", "sample_count"),
            ["site_id", "publisher_utc_hour"], "inner"
        ).select("site_id", F.col("publisher_utc_hour").alias("match_hour"), "publisher_power", "raw_power", "sample_count")
        scored_b = summarize_pairs(pairs_b, "B — Excel wall-clock treated as UTC vs publisher UTC")
        show_examples(pairs_b, "B — wall-clock treated as UTC")

        # C: Match source wall-clock to publisher local wall-clock directly.
        raw_c = make_hourly_raw(raw_with_wall, "source_wall_clock_as_utc", "match_hour")
        pairs_c = publisher.join(
            raw_c.select("site_id", F.col("match_hour").alias("publisher_local_hour"), "raw_power", "sample_count"),
            ["site_id", "publisher_local_hour"], "inner"
        ).select("site_id", F.col("publisher_local_hour").alias("match_hour"), "publisher_power", "raw_power", "sample_count")
        scored_c = summarize_pairs(pairs_c, "C — Excel local wall-clock vs publisher local wall-clock")
        show_examples(pairs_c, "C — local wall-clock comparison")

        print("\n=== INTERPRETATION NOTES ===")
        print("A should be trusted only if the source Excel time is truly Europe/Bucharest local time.")
        print("B is a hypothesis test, not an automatic correction: it tests whether the Excel clock is already UTC.")
        print("C tests whether the source and publisher local wall-clock labels agree directly.")
        print("Compare pair counts, MAE, correlation and individual examples; do not select a time interpretation from MAE alone.")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
