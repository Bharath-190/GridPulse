#!/usr/bin/env python3
"""Diagnose the large Silver publisher-vs-five-minute active-power deltas.

Read-only: this script does not modify Bronze or Silver Delta tables.
"""
from pathlib import Path

from pyspark.sql import functions as F

from silver_transform import make_spark

ROOT = Path(__file__).resolve().parents[1]
PERFORMANCE_PATH = ROOT / "data" / "silver" / "delta" / "silver_site_hourly_performance"
INVERTER_PATH = ROOT / "data" / "silver" / "delta" / "silver_inverter_telemetry_5m"


def add_metrics(frame):
    difference = F.col("publisher_power") - F.col("raw_power")
    return frame.withColumn("abs_delta_kw", F.abs(difference)).withColumn(
        "squared_delta_kw", F.pow(difference, 2)
    )


def show_metrics(frame, title):
    print(f"\n=== {title} ===")
    (
        frame.groupBy("site_id")
        .agg(
            F.count("*").alias("paired_hours"),
            F.avg("abs_delta_kw").alias("mae_kw"),
            F.expr("percentile_approx(abs_delta_kw, 0.50)").alias("median_abs_delta_kw"),
            F.expr("percentile_approx(abs_delta_kw, 0.95)").alias("p95_abs_delta_kw"),
            F.max("abs_delta_kw").alias("max_abs_delta_kw"),
            F.sqrt(F.avg("squared_delta_kw")).alias("rmse_kw"),
            F.corr("publisher_power", "raw_power").alias("correlation"),
        )
        .orderBy("site_id")
        .show(truncate=False)
    )


def main():
    if not (PERFORMANCE_PATH / "_delta_log").is_dir():
        raise FileNotFoundError(f"Silver performance Delta table not found: {PERFORMANCE_PATH}")
    if not (INVERTER_PATH / "_delta_log").is_dir():
        raise FileNotFoundError(f"Silver inverter Delta table not found: {INVERTER_PATH}")

    spark = make_spark()
    try:
        perf = spark.read.format("delta").load(str(PERFORMANCE_PATH))
        inverter = spark.read.format("delta").load(str(INVERTER_PATH))

        print("Spark session timezone:", spark.conf.get("spark.sql.session.timeZone"))

        print("\n=== INVERTER DEVICE INVENTORY ===")
        (
            inverter.groupBy("site_id")
            .agg(
                F.countDistinct("device_name").alias("distinct_devices"),
                F.collect_set("device_name").alias("device_names"),
                F.min("active_power_kw").alias("min_active_power_kw"),
                F.max("active_power_kw").alias("max_active_power_kw"),
            )
            .orderBy("site_id")
            .show(truncate=False)
        )

        comparable = perf.filter(
            (F.col("hour_alignment_status") == "comparable_complete_hour")
            & F.col("publisher_hourly_active_power_kw").isNotNull()
            & F.col("five_minute_mean_active_power_kw").isNotNull()
        )

        base = comparable.select(
            "site_id",
            "event_hour_utc",
            F.col("publisher_hourly_active_power_kw").alias("publisher_power"),
            F.col("five_minute_mean_active_power_kw").alias("raw_power"),
            F.col("weather_ghi_wm2").alias("ghi_wm2"),
            F.col("weather_solar_elevation_deg").alias("solar_elevation_deg"),
            F.col("active_power_mean_abs_delta_kw").alias("stored_abs_delta_kw"),
        )
        baseline = add_metrics(base)
        show_metrics(baseline, "CURRENT SAME-HOUR COMPARISON")

        print("\n=== LARGEST SAME-HOUR DIFFERENCES ===")
        (
            baseline.select(
                "site_id", "event_hour_utc", "publisher_power", "raw_power",
                "abs_delta_kw", "ghi_wm2", "solar_elevation_deg",
            )
            .orderBy(F.desc("abs_delta_kw"))
            .show(25, truncate=False)
        )

        print("\n=== TIME-SHIFT SCAN ===")
        print("Offset means: shifted raw timestamp = original raw hour + offset.")
        publisher = perf.filter(
            F.col("publisher_hour_present")
            & F.col("publisher_hourly_active_power_kw").isNotNull()
        ).select(
            "site_id",
            F.col("event_hour_utc").alias("match_hour"),
            F.col("publisher_hourly_active_power_kw").alias("publisher_power"),
            F.col("weather_ghi_wm2").alias("ghi_wm2"),
        )

        raw_complete = perf.filter(
            F.col("raw_telemetry_hour_present")
            & (F.col("raw_sample_count") == 12)
            & (F.col("active_power_sample_count") == 12)
            & F.col("five_minute_mean_active_power_kw").isNotNull()
        )

        shift_results = []
        for offset in range(-3, 4):
            if offset == 0:
                shifted_hour = F.col("event_hour_utc")
            elif offset > 0:
                shifted_hour = F.col("event_hour_utc") + F.expr(f"INTERVAL {offset} HOURS")
            else:
                shifted_hour = F.col("event_hour_utc") - F.expr(f"INTERVAL {abs(offset)} HOURS")

            raw = raw_complete.select(
                "site_id",
                shifted_hour.alias("match_hour"),
                F.col("five_minute_mean_active_power_kw").alias("raw_power"),
            )
            paired = publisher.join(raw, ["site_id", "match_hour"], "inner")
            paired = add_metrics(paired)
            paired = paired.withColumn("raw_hour_offset_hours", F.lit(offset))

            all_hours = (
                paired.groupBy("site_id")
                .agg(
                    F.count("*").alias("all_paired_hours"),
                    F.avg("abs_delta_kw").alias("all_hours_mae_kw"),
                    F.corr("publisher_power", "raw_power").alias("all_hours_correlation"),
                )
            )
            daylight = (
                paired.filter(F.col("ghi_wm2") > 20.0)
                .groupBy("site_id")
                .agg(
                    F.count("*").alias("daylight_paired_hours"),
                    F.avg("abs_delta_kw").alias("daylight_mae_kw"),
                    F.corr("publisher_power", "raw_power").alias("daylight_correlation"),
                )
            )
            combined = all_hours.join(daylight, "site_id", "left").withColumn(
                "raw_hour_offset_hours", F.lit(offset)
            )
            shift_results.append(combined)

        result = shift_results[0]
        for additional in shift_results[1:]:
            result = result.unionByName(additional)
        result.orderBy("site_id", "raw_hour_offset_hours").show(100, truncate=False)

        print("\nInterpretation guide:")
        print("- If offset 0 has low MAE and high correlation, inspect the stored delta calculation or validation aggregation.")
        print("- If a non-zero offset is clearly better, investigate timezone conversion / hour-boundary semantics before rebuilding Silver.")
        print("- If no offset is good, inspect raw measurement mapping, units, and source coverage for the affected site.")
        print("- This diagnostic is read-only; it does not change any Delta data.")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
