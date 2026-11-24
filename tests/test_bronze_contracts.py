"""Lightweight contract tests for the GridPulse Bronze ingestion module."""

import importlib.util
from datetime import datetime, timezone

import pandas as pd
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "bronze_ingest.py"
SPEC = importlib.util.spec_from_file_location("gridpulse_bronze_ingest", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def test_required_excel_columns_are_unique():
    assert len(MODULE.EXCEL_COLUMNS) == len(set(MODULE.EXCEL_COLUMNS))
    assert "Start Date/Time" in MODULE.EXCEL_COLUMNS


def test_hourly_schema_has_expected_fields():
    assert len(MODULE.HOURLY_COLUMNS) == 23
    assert "datetime_utc" in MODULE.HOURLY_COLUMNS
    assert "ghi_wm2" in MODULE.HOURLY_COLUMNS


def test_source_timezone_is_bucharest():
    assert MODULE.TIMEZONE_NAME == "Europe/Bucharest"


def test_payload_hash_is_stable():
    payload = {"site_id": "site_a", "active_power_kw": 12.5}
    assert MODULE.payload_hash(payload) == MODULE.payload_hash(payload)


def test_float_cleaner_preserves_zero_and_nulls_missing():
    assert MODULE.clean_float(0) == 0.0
    assert MODULE.clean_float(None) is None



def test_excel_local_timestamps_resolve_to_timezone_aware_utc():
    raw = pd.Series([
        "2025-03-19 07:30:00",       # Bucharest standard time: UTC+02:00
        "2025-07-19 07:30:00 DST",   # Bucharest daylight time: UTC+03:00
    ], dtype="string")

    local_text, suffix, local_naive, utc_values = MODULE.resolve_excel_timestamps(raw)

    standard = utc_values.iloc[0].to_pydatetime()
    daylight = utc_values.iloc[1].to_pydatetime()

    assert standard == datetime(2025, 3, 19, 5, 30, tzinfo=timezone.utc)
    assert daylight == datetime(2025, 7, 19, 4, 30, tzinfo=timezone.utc)
    assert standard.tzinfo is not None and standard.utcoffset().total_seconds() == 0
    assert daylight.tzinfo is not None and daylight.utcoffset().total_seconds() == 0
    assert local_text.tolist() == ["2025-03-19 07:30:00", "2025-07-19 07:30:00"]
    assert suffix.isna().iloc[0]
    assert suffix.iloc[1] == "DST"
    assert local_naive.notna().all()


def test_ambiguous_fall_back_time_uses_dst_suffix_or_standard_fallback():
    raw = pd.Series([
        "2025-10-26 03:30:00 DST",
        "2025-10-26 03:30:00 EET",
        "2025-10-26 03:30:00",
    ], dtype="string")

    _, _, _, utc_values = MODULE.resolve_excel_timestamps(raw)
    resolved = [value.to_pydatetime() for value in utc_values]

    assert resolved[0] == datetime(2025, 10, 26, 0, 30, tzinfo=timezone.utc)
    assert resolved[1] == datetime(2025, 10, 26, 1, 30, tzinfo=timezone.utc)
    assert resolved[2] == datetime(2025, 10, 26, 1, 30, tzinfo=timezone.utc)


def test_nonexistent_spring_forward_local_time_is_not_silently_shifted():
    raw = pd.Series(["2025-03-30 03:30:00 DST"], dtype="string")
    _, _, _, utc_values = MODULE.resolve_excel_timestamps(raw)
    assert pd.isna(utc_values.iloc[0])


def test_ingestion_clock_returns_aware_utc_datetime():
    value = MODULE.utc_now_aware()
    assert value.tzinfo is not None
    assert value.utcoffset().total_seconds() == 0



def test_timezone_aware_utc_datetime_serializes_to_utc_epoch_for_spark():
    import calendar
    from pyspark.sql.types import TimestampType

    value = datetime(2025, 3, 19, 5, 30, tzinfo=timezone.utc)
    expected_microseconds = calendar.timegm(value.utctimetuple()) * 1_000_000
    expected_microseconds += value.microsecond

    assert TimestampType().toInternal(value) == expected_microseconds
