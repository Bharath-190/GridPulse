"""Contract and Spark transformation tests for GridPulse Silver."""

import importlib.util
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

pyspark = pytest.importorskip("pyspark")
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    DoubleType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "silver_transform.py"
SPEC = importlib.util.spec_from_file_location("gridpulse_silver_transform", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


@pytest.fixture(scope="module")
def spark():
    session = (
        SparkSession.builder.master("local[1]")
        .appName("GridPulse-Silver-Tests")
        .config("spark.driver.host", "127.0.0.1")
        .config("spark.driver.bindAddress", "127.0.0.1")
        .config("spark.ui.enabled", "false")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )
    # getOrCreate() may reuse an existing SparkSession; enforce UTC on it too.
    session.conf.set("spark.sql.session.timeZone", "UTC")
    assert session.conf.get("spark.sql.session.timeZone") == "UTC"
    yield session
    session.stop()


def _inverter_schema():
    return StructType(
        [
            StructField("site_id", StringType(), False),
            StructField("device_name", StringType(), False),
            StructField("event_ts_utc", TimestampType(), False),
            *[StructField(name, DoubleType(), True) for name in MODULE.INVERTER_MEASUREMENTS],
        ]
    )


def test_eight_inverter_measurements_are_tracked_for_completeness():
    assert len(MODULE.INVERTER_MEASUREMENTS) == 8
    assert "active_power_kw" in MODULE.INVERTER_MEASUREMENTS
    assert "cumulative_energy_kwh" in MODULE.INVERTER_MEASUREMENTS


def test_hourly_source_contract_has_23_fields():
    assert len(MODULE.HOURLY_COLUMNS) == 23
    assert "datetime_utc" in MODULE.HOURLY_COLUMNS
    assert "ghi_wm2" in MODULE.HOURLY_COLUMNS
    assert "capacity_factor" in MODULE.HOURLY_COLUMNS


def test_range_checks_are_flags_not_filter_rules():
    assert MODULE.RANGE_CHECKS["humidity_pct"] == (0.0, 100.0)
    assert MODULE.RANGE_CHECKS["capacity_factor"] == (0.0, 1.0)
    assert "temp_c" not in MODULE.RANGE_CHECKS
    assert "wind_speed_kmh" not in MODULE.RANGE_CHECKS


def test_expected_five_minute_coverage_is_twelve_samples_per_hour():
    assert 60 // 5 == 12
    import inspect
    source = inspect.getsource(MODULE.aggregate_five_minute_to_hourly)
    assert 'F.col("raw_sample_count") == 12' in source


def test_hourly_join_is_full_outer_and_comparison_is_guarded():
    import inspect
    source = inspect.getsource(MODULE.build_silver_site_hourly_performance)
    assert '"full_outer"' in source
    assert 'F.col("active_power_sample_count") == 12' in source


def test_inverter_silver_preserves_zero_nulls_and_quality_flags(spark):
    # TimestampType fixtures must be timezone-aware; naive datetimes are
    # interpreted in the host timezone by PySpark before Spark sees them.
    start = datetime(2025, 1, 1, 0, 0, tzinfo=timezone.utc)
    rows = [
        ("site_a", "inv-1", start, 0.0, 1.0, 1.0, 10.0, 25.0, 50.0, 1.0, 96.0),
        ("site_a", "inv-1", start + timedelta(minutes=5), -0.1, 1.0, 1.0, 10.0, 25.0, 50.0, 1.0, 96.0),
        ("site_a", "inv-1", start + timedelta(minutes=10), 4.0, None, 1.0, 10.0, 25.0, 50.0, 1.0, 96.0),
    ]
    frame = spark.createDataFrame(rows, schema=_inverter_schema())
    result = MODULE.build_silver_inverter(frame).orderBy("event_ts_utc").collect()

    assert result[0]["active_power_kw"] == 0.0
    assert result[0]["active_power_negative_flag"] is False
    assert result[0]["measurement_null_count"] == 0
    assert result[0]["data_quality_status"] == "complete"

    assert result[1]["active_power_negative_flag"] is True
    assert result[1]["data_quality_status"] == "review"

    assert result[2]["dc_input_power_kw"] is None
    assert result[2]["measurement_null_count"] == 1
    assert result[2]["data_quality_status"] == "partial"


def test_hourly_aggregation_distinguishes_complete_and_partial_hours(spark):
    # Use aware UTC values so the host timezone cannot shift the test hours.
    start = datetime(2025, 1, 1, 0, 0, tzinfo=timezone.utc)
    rows = []
    for index in range(12):
        rows.append(
            (
                "site_a", "inv-1", start + timedelta(minutes=5 * index),
                10.0, 11.0, 25.0, 50.0, 1.0, 96.0,
            )
        )
    for index in range(3):
        rows.append(
            (
                "site_a", "inv-1", start + timedelta(hours=1, minutes=5 * index),
                8.0, 9.0, 26.0, 50.0, 1.0, 96.0,
            )
        )

    schema = StructType(
        [
            StructField("site_id", StringType(), False),
            StructField("device_name", StringType(), False),
            StructField("event_ts_utc", TimestampType(), False),
            StructField("active_power_kw", DoubleType(), True),
            StructField("dc_input_power_kw", DoubleType(), True),
            StructField("inverter_temp_c", DoubleType(), True),
            StructField("grid_freq_hz", DoubleType(), True),
            StructField("power_factor", DoubleType(), True),
            StructField("efficiency_pct", DoubleType(), True),
        ]
    )
    aggregate_frame = spark.createDataFrame(rows, schema=schema)
    aggregated = MODULE.aggregate_five_minute_to_hourly(aggregate_frame)
    # Keep timestamp interpretation inside Spark. The test fixture uses
    # timezone-aware UTC datetimes, and the Spark session is explicitly UTC.
    # Collecting TimestampType as Python datetime can expose host-local time.
    labeled = aggregated.selectExpr(
        "date_format(event_hour_utc, 'yyyy-MM-dd HH:mm:ss') AS utc_hour",
        "raw_sample_count",
        "raw_coverage_status",
        "raw_data_coverage_pct",
        "five_minute_mean_active_power_kw",
    )
    by_hour = {row["utc_hour"]: row.asDict() for row in labeled.collect()}

    complete = by_hour["2025-01-01 00:00:00"]
    partial = by_hour["2025-01-01 01:00:00"]
    assert complete["raw_sample_count"] == 12
    assert complete["raw_coverage_status"] == "complete_12"
    assert complete["raw_data_coverage_pct"] == 100.0
    assert complete["five_minute_mean_active_power_kw"] == 10.0

    assert partial["raw_sample_count"] == 3
    assert partial["raw_coverage_status"] == "partial"
    assert partial["raw_data_coverage_pct"] == 25.0

def test_publisher_daylight_zero_conflict_is_flagged_and_values_are_preserved(spark):
    """A publisher zero must not be treated as comparable when complete raw
    telemetry shows generation in daylight; the same zero at night is valid.
    """
    daylight_start = datetime(2026, 3, 29, 9, 0, tzinfo=timezone.utc)
    night_start = datetime(2026, 3, 29, 22, 0, tzinfo=timezone.utc)
    raw_rows = []
    for start in (daylight_start, night_start):
        for index in range(12):
            raw_rows.append(
                (
                    "site_b", "inv-1", start + timedelta(minutes=5 * index),
                    31.0, None, None, None, None, None, None, None,
                )
            )
    raw_frame = spark.createDataFrame(raw_rows, schema=_inverter_schema())
    raw_hourly = MODULE.aggregate_five_minute_to_hourly(
        MODULE.build_silver_inverter(raw_frame)
    )

    hourly_types = {
        "datetime_utc": StringType(),
        "datetime_local": StringType(),
        "inverter_status": StringType(),
    }
    hourly_fields = [
        StructField("site_id", StringType(), False),
        StructField("event_ts_utc", TimestampType(), False),
    ]
    for name in MODULE.HOURLY_COLUMNS:
        dtype = hourly_types.get(name, DoubleType())
        hourly_fields.append(StructField(name, dtype, True))
    hourly_fields.extend([
        StructField("source_file", StringType(), True),
        StructField("source_relative_path", StringType(), True),
        StructField("source_file_sha256", StringType(), True),
        StructField("record_hash", StringType(), True),
        StructField("ingested_at_utc", TimestampType(), True),
    ])
    hourly_schema = StructType(hourly_fields)

    base_values = {
        "active_power_kw": 0.0,
        "dc_input_power_kw": None,
        "daily_energy_kwh": None,
        "cumulative_energy_kwh": None,
        "inverter_temp_c": None,
        "grid_freq_hz": None,
        "power_factor": None,
        "efficiency_pct": None,
        "inverter_status": None,
        "is_generating": 0.0,
        "temp_c": 18.0,
        "humidity_pct": 40.0,
        "cloud_cover_pct": 10.0,
        "wind_speed_kmh": 5.0,
        "dni_wm2": 500.0,
        "dhi_wm2": 100.0,
        "precip_mm": 0.0,
        "solar_azimuth_deg": 150.0,
        "capacity_factor": 0.0,
    }
    hourly_rows = []
    for start, ghi, elevation in (
        (daylight_start, 410.0, 46.3),
        (night_start, 0.0, 0.0),
    ):
        values = {
            **base_values,
            "datetime_utc": start.strftime("%Y-%m-%d %H:%M:%S"),
            "datetime_local": start.strftime("%Y-%m-%d %H:%M:%S+0000"),
            "ghi_wm2": ghi,
            "solar_elevation_deg": elevation,
        }
        row = ["site_b", start]
        row.extend(values[name] for name in MODULE.HOURLY_COLUMNS)
        row.extend(["publisher.csv", "site_b/publisher.csv", "abc123", "hash1", start])
        hourly_rows.append(tuple(row))

    hourly_frame = spark.createDataFrame(hourly_rows, schema=hourly_schema)
    silver_hourly = MODULE.build_silver_hourly_conditions(hourly_frame)

    performance = MODULE.build_silver_site_hourly_performance(
        silver_hourly, raw_hourly
    )
    labeled = performance.selectExpr(
        "date_format(event_hour_utc, 'yyyy-MM-dd HH:mm:ss') AS utc_hour",
        "*",
    )
    results = {row["utc_hour"]: row.asDict() for row in labeled.collect()}
    daylight = results["2026-03-29 09:00:00"]
    night = results["2026-03-29 22:00:00"]

    # Daylight zero conflicts are highlighted, but neither measurement is lost.
    assert daylight["publisher_hourly_active_power_kw"] == 0.0
    assert daylight["five_minute_mean_active_power_kw"] == 31.0
    assert daylight["active_power_mean_abs_delta_kw"] == 31.0
    assert daylight["publisher_zero_conflict_with_raw_generation_flag"] is True
    assert daylight["publisher_operational_null_count"] == 8
    assert daylight["publisher_operational_fields_missing_flag"] is True
    assert daylight["daylight_context_flag"] is True
    assert daylight["active_power_comparison_eligible_flag"] is False
    assert daylight["hour_alignment_status"] == "publisher_zero_conflicts_with_raw_generation"

    # The same measurements at night are not automatically treated as a conflict.
    assert night["publisher_hourly_active_power_kw"] == 0.0
    assert night["five_minute_mean_active_power_kw"] == 31.0
    assert night["publisher_zero_conflict_with_raw_generation_flag"] is False
    assert night["publisher_operational_fields_missing_flag"] is False
    assert night["daylight_context_flag"] is False
    assert night["active_power_comparison_eligible_flag"] is True
    assert night["hour_alignment_status"] == "comparable_complete_hour"
