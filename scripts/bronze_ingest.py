#!/usr/bin/env python3
"""GridPulse Phase 2: idempotent Bronze ingestion into local Delta Lake.

Reads the publisher's monthly XLSX exports and hourly weather-enriched CSVs.
Raw source files are never modified. Valid records are merged into Delta tables;
rows whose local timestamps cannot be safely resolved are retained in a
quarantine Delta table.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
from delta import configure_spark_with_delta_pip
from delta.tables import DeltaTable
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import (
    DoubleType,
    IntegerType,
    LongType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_ROOT = PROJECT_ROOT / "data" / "external" / "PV-Generation-Dataset"
BRONZE_ROOT = PROJECT_ROOT / "data" / "bronze" / "delta"
TIMEZONE_NAME = "Europe/Bucharest"

INVERTER_PATH = BRONZE_ROOT / "bronze_inverter_telemetry_5m"
HOURLY_PATH = BRONZE_ROOT / "bronze_site_hourly_weather"
QUARANTINE_PATH = BRONZE_ROOT / "bronze_quarantine_records"
MANIFEST_PATH = BRONZE_ROOT / "bronze_ingestion_manifest"

EXCEL_COLUMNS = [
    "Site Name",
    "Installer",
    "Device Name",
    "Start Date/Time",
    "Active Power (kW)",
    "Total Input Power (kW)",
    "Daily Energy (kWh)",
    "Total PV Yield (kWh)",
    "Internal Temperature (°C)",
    "Grid Frequency (Hz)",
    "Power Factor",
    "Conversion Efficiency (%)",
    "Inverter Status",
]

HOURLY_COLUMNS = [
    "datetime_utc", "datetime_local", "active_power_kw",
    "dc_input_power_kw", "daily_energy_kwh", "cumulative_energy_kwh",
    "inverter_temp_c", "grid_freq_hz", "power_factor", "efficiency_pct",
    "inverter_status", "is_generating", "temp_c", "humidity_pct",
    "cloud_cover_pct", "wind_speed_kmh", "ghi_wm2", "dni_wm2",
    "dhi_wm2", "precip_mm", "solar_elevation_deg", "solar_azimuth_deg",
    "capacity_factor",
]

EXCEL_NUMERIC_MAP = {
    "active_power_kw": "Active Power (kW)",
    "dc_input_power_kw": "Total Input Power (kW)",
    "daily_energy_kwh": "Daily Energy (kWh)",
    "cumulative_energy_kwh": "Total PV Yield (kWh)",
    "inverter_temp_c": "Internal Temperature (°C)",
    "grid_freq_hz": "Grid Frequency (Hz)",
    "power_factor": "Power Factor",
    "efficiency_pct": "Conversion Efficiency (%)",
}

HOURLY_NUMERIC_COLUMNS = [c for c in HOURLY_COLUMNS if c not in {
    "datetime_utc", "datetime_local", "inverter_status"
}]

INVERTER_SCHEMA = StructType([
    StructField("site_id", StringType(), False),
    StructField("site_name", StringType(), True),
    StructField("installer", StringType(), True),
    StructField("device_name", StringType(), True),
    StructField("timestamp_raw", StringType(), True),
    StructField("timestamp_local", StringType(), True),
    StructField("timezone_suffix", StringType(), True),
    StructField("timezone_resolution", StringType(), True),
    StructField("event_ts_utc", TimestampType(), False),
    *[StructField(name, DoubleType(), True) for name in EXCEL_NUMERIC_MAP],
    StructField("inverter_status", StringType(), True),
    StructField("source_file", StringType(), False),
    StructField("source_relative_path", StringType(), False),
    StructField("source_row_number", LongType(), False),
    StructField("source_file_sha256", StringType(), False),
    StructField("record_hash", StringType(), False),
    StructField("ingestion_batch_id", StringType(), False),
    StructField("ingested_at_utc", TimestampType(), False),
])

QUARANTINE_SCHEMA = StructType([
    StructField("site_id", StringType(), False),
    StructField("dataset_type", StringType(), False),
    StructField("source_relative_path", StringType(), False),
    StructField("source_file_sha256", StringType(), False),
    StructField("source_row_number", LongType(), False),
    StructField("timestamp_raw", StringType(), True),
    StructField("rejection_reason", StringType(), False),
    StructField("raw_payload_json", StringType(), False),
    StructField("record_hash", StringType(), False),
    StructField("ingestion_batch_id", StringType(), False),
    StructField("ingested_at_utc", TimestampType(), False),
])

MANIFEST_SCHEMA = StructType([
    StructField("dataset_type", StringType(), False),
    StructField("site_id", StringType(), False),
    StructField("source_relative_path", StringType(), False),
    StructField("source_file_name", StringType(), False),
    StructField("source_file_sha256", StringType(), False),
    StructField("file_size_bytes", LongType(), False),
    StructField("file_modified_at_utc", TimestampType(), False),
    StructField("rows_read", LongType(), False),
    StructField("records_written", LongType(), False),
    StructField("records_quarantined", LongType(), False),
    StructField("ingestion_batch_id", StringType(), False),
    StructField("processed_at_utc", TimestampType(), False),
])


def utc_now_aware() -> datetime:
    """Return a timezone-aware UTC datetime for Spark TimestampType.

    PySpark serializes naive Python datetimes using the host machine's local
    timezone. Keeping UTC values timezone-aware prevents an unintended shift
    when the project runs on a machine outside UTC (for example, Asia/Kolkata).
    """
    return datetime.now(timezone.utc)


def resolve_excel_timestamps(
    timestamp_raw: pd.Series,
) -> tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
    """Resolve Excel wall-clock strings to timezone-aware UTC timestamps.

    The Excel exports contain Europe/Bucharest local wall-clock time. A DST
    suffix selects the daylight-saving occurrence for ambiguous fall-back
    timestamps; EET or no suffix selects standard time for ambiguous values.
    The returned UTC series remains timezone-aware until PySpark serializes it.
    """
    suffix = timestamp_raw.str.extract(
        r"(?i)\b(DST|EEST|EET)\s*$", expand=False
    ).str.upper()
    timestamp_local_text = timestamp_raw.str.replace(
        r"(?i)\s+(?:DST|EEST|EET)$", "", regex=True
    )
    local_naive = pd.to_datetime(timestamp_local_text, errors="coerce")
    is_dst = suffix.isin(["DST", "EEST"]).fillna(False).to_numpy()
    local_aware = local_naive.dt.tz_localize(
        TIMEZONE_NAME,
        ambiguous=is_dst,
        nonexistent="NaT",
    )
    utc_aware = local_aware.dt.tz_convert("UTC")
    return timestamp_local_text, suffix, local_naive, utc_aware


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def clean_string(value: Any) -> str | None:
    if value is None or pd.isna(value):
        return None
    value = str(value).strip()
    return value if value else None


def clean_float(value: Any) -> float | None:
    if value is None or pd.isna(value):
        return None
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    # Preserve missing values as NULL, not IEEE NaN.
    return result if pd.notna(result) else None


def json_safe(value: Any) -> Any:
    if value is None or pd.isna(value):
        return None
    if isinstance(value, (pd.Timestamp, datetime)):
        return value.isoformat()
    if hasattr(value, "item"):
        value = value.item()
    if isinstance(value, float) and pd.isna(value):
        return None
    return value


def payload_hash(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, default=str, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def relative_source_path(path: Path) -> str:
    return path.resolve().relative_to(DATASET_ROOT.resolve()).as_posix()


def delta_exists(path: Path) -> bool:
    return (path / "_delta_log").is_dir()


def merge_delta(
    spark: SparkSession,
    frame: DataFrame,
    target_path: Path,
    keys: list[str],
    hash_column: str = "record_hash",
) -> None:
    """Create a Delta table or upsert rows by business key and payload hash."""
    if frame.limit(1).count() == 0:
        return

    target = str(target_path)
    if not delta_exists(target_path):
        target_path.parent.mkdir(parents=True, exist_ok=True)
        frame.write.format("delta").mode("errorifexists").save(target)
        return

    condition = " AND ".join([f"t.`{key}` = s.`{key}`" for key in keys])
    changed = f"NOT (t.`{hash_column}` <=> s.`{hash_column}`)"
    (
        DeltaTable.forPath(spark, target)
        .alias("t")
        .merge(frame.alias("s"), condition)
        .whenMatchedUpdateAll(condition=changed)
        .whenNotMatchedInsertAll()
        .execute()
    )


def load_manifest_map(spark: SparkSession) -> dict[tuple[str, str], str]:
    if not delta_exists(MANIFEST_PATH):
        return {}
    rows = (
        spark.read.format("delta").load(str(MANIFEST_PATH))
        .select("dataset_type", "source_relative_path", "source_file_sha256")
        .collect()
    )
    return {
        (r["dataset_type"], r["source_relative_path"]): r["source_file_sha256"]
        for r in rows
    }


def register_manifest(
    spark: SparkSession,
    *,
    dataset_type: str,
    site_id: str,
    path: Path,
    file_hash: str,
    rows_read: int,
    records_written: int,
    records_quarantined: int,
    batch_id: str,
) -> None:
    stat = path.stat()
    row = (
        dataset_type,
        site_id,
        relative_source_path(path),
        path.name,
        file_hash,
        int(stat.st_size),
        datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc),
        int(rows_read),
        int(records_written),
        int(records_quarantined),
        batch_id,
        utc_now_aware(),
    )
    frame = spark.createDataFrame([row], MANIFEST_SCHEMA)
    merge_delta(
        spark, frame, MANIFEST_PATH,
        ["dataset_type", "source_relative_path"],
        hash_column="source_file_sha256",
    )


def make_quarantine_row(
    *, site_id: str, source_path: Path, file_hash: str,
    source_row_number: int, timestamp_raw: str | None,
    rejection_reason: str, raw_payload: dict[str, Any],
    batch_id: str, ingested_at: datetime,
) -> tuple[Any, ...]:
    safe_payload = {k: json_safe(v) for k, v in raw_payload.items()}
    raw_json = json.dumps(safe_payload, sort_keys=True, default=str)
    record_hash = payload_hash({
        "site_id": site_id,
        "source_relative_path": relative_source_path(source_path),
        "source_row_number": source_row_number,
        "raw_payload": safe_payload,
        "rejection_reason": rejection_reason,
    })
    return (
        site_id, "inverter_telemetry_5m", relative_source_path(source_path),
        file_hash, source_row_number, timestamp_raw, rejection_reason,
        raw_json, record_hash, batch_id, ingested_at,
    )


def process_excel_file(
    spark: SparkSession,
    site_id: str,
    path: Path,
    file_hash: str,
    batch_id: str,
) -> tuple[int, int, int]:
    df = pd.read_excel(path, header=3, engine="openpyxl")
    missing_columns = sorted(set(EXCEL_COLUMNS) - set(df.columns))
    if missing_columns:
        raise ValueError(f"{path.name}: missing required columns: {missing_columns}")

    # Keep the source string verbatim for lineage. Excel timestamps are
    # Europe/Bucharest local wall-clock values, not UTC values.
    timestamp_raw = df["Start Date/Time"].astype("string").str.strip()
    timestamp_local_text, suffix, local_naive, utc_aware = (
        resolve_excel_timestamps(timestamp_raw)
    )

    batch_time = utc_now_aware()
    valid_rows: list[tuple[Any, ...]] = []
    quarantine_rows: list[tuple[Any, ...]] = []

    for idx, row in df.iterrows():
        original_raw_ts = clean_string(timestamp_raw.iloc[idx])
        local_value = clean_string(timestamp_local_text.iloc[idx])
        suffix_value = clean_string(suffix.iloc[idx])
        utc_value = utc_aware.iloc[idx]
        excel_row_number = int(idx) + 5  # header=3 => physical header row 4

        raw_payload = {col: row[col] for col in EXCEL_COLUMNS}

        if pd.isna(utc_value):
            parsed_ok = not pd.isna(local_naive.iloc[idx])
            reason = (
                "nonexistent_local_time_or_dst_transition"
                if parsed_ok else "unparseable_local_timestamp"
            )
            quarantine_rows.append(make_quarantine_row(
                site_id=site_id,
                source_path=path,
                file_hash=file_hash,
                source_row_number=excel_row_number,
                timestamp_raw=original_raw_ts,
                rejection_reason=reason,
                raw_payload=raw_payload,
                batch_id=batch_id,
                ingested_at=batch_time,
            ))
            continue

        # Do not strip tzinfo here. TimestampType treats naive Python datetimes
        # as host-local time, which shifts UTC values on non-UTC machines.
        timestamp_utc = utc_value.to_pydatetime()
        if timestamp_utc.tzinfo is None or timestamp_utc.utcoffset().total_seconds() != 0:
            raise ValueError("Resolved Excel timestamp is not timezone-aware UTC")
        numeric_values = {
            target: clean_float(row[source])
            for target, source in EXCEL_NUMERIC_MAP.items()
        }
        record_payload = {
            "site_id": site_id,
            "device_name": clean_string(row["Device Name"]),
            "event_ts_utc": timestamp_utc.isoformat(),
            "timestamp_raw": original_raw_ts,
            **numeric_values,
            "inverter_status": clean_string(row["Inverter Status"]),
        }
        record_hash = payload_hash(record_payload)

        if suffix_value in ("DST", "EEST"):
            resolution = "source_dst_marker"
        elif suffix_value == "EET":
            resolution = "source_standard_marker"
        else:
            resolution = "standard_if_ambiguous_unsuffixed"

        valid_rows.append((
            site_id,
            clean_string(row["Site Name"]),
            clean_string(row["Installer"]),
            clean_string(row["Device Name"]),
            original_raw_ts,
            local_value,
            suffix_value,
            resolution,
            timestamp_utc,
            *[numeric_values[name] for name in EXCEL_NUMERIC_MAP],
            clean_string(row["Inverter Status"]),
            path.name,
            relative_source_path(path),
            excel_row_number,
            file_hash,
            record_hash,
            batch_id,
            batch_time,
        ))

    if valid_rows:
        valid_frame = spark.createDataFrame(valid_rows, INVERTER_SCHEMA)
        merge_delta(
            spark, valid_frame, INVERTER_PATH,
            ["site_id", "device_name", "event_ts_utc"],
        )

    if quarantine_rows:
        quarantine_frame = spark.createDataFrame(quarantine_rows, QUARANTINE_SCHEMA)
        merge_delta(
            spark, quarantine_frame, QUARANTINE_PATH,
            ["dataset_type", "source_relative_path", "source_row_number"],
        )

    return len(df), len(valid_rows), len(quarantine_rows)


def build_hourly_frame(
    spark: SparkSession,
    site_id: str,
    path: Path,
    file_hash: str,
    batch_id: str,
) -> tuple[DataFrame, int]:
    # Read as strings first to preserve original CSV timestamp text and apply
    # explicit numeric casts consistently across both sites.
    source = (
        spark.read.option("header", "true")
        .option("mode", "FAILFAST")
        .option("encoding", "UTF-8")
        .csv(str(path))
    )
    missing_columns = sorted(set(HOURLY_COLUMNS) - set(source.columns))
    if missing_columns:
        raise ValueError(f"{path.name}: missing required CSV columns: {missing_columns}")

    source = source.select(*HOURLY_COLUMNS)
    source = source.withColumn(
        "event_ts_utc",
        F.to_timestamp(F.col("datetime_utc"), "yyyy-MM-dd HH:mm:ss"),
    )
    invalid_count = source.filter(F.col("event_ts_utc").isNull()).count()
    if invalid_count:
        raise ValueError(
            f"{path.name}: {invalid_count} invalid datetime_utc values; "
            "refusing to silently drop hourly records"
        )

    for column in HOURLY_NUMERIC_COLUMNS:
        cleaned = F.lower(F.trim(F.col(column)))
        source = source.withColumn(
            column,
            F.when(
                F.col(column).isNull() | (cleaned == "") | cleaned.isin("nan", "null", "na"),
                F.lit(None).cast(DoubleType()),
            ).otherwise(F.col(column).cast(DoubleType())),
        )

    payload_columns = [F.coalesce(F.col(c).cast("string"), F.lit("<NULL>")) for c in HOURLY_COLUMNS]
    source = (
        source
        .withColumn("site_id", F.lit(site_id))
        .withColumn("source_file", F.lit(path.name))
        .withColumn("source_relative_path", F.lit(relative_source_path(path)))
        .withColumn("source_file_sha256", F.lit(file_hash))
        .withColumn("record_hash", F.sha2(F.concat_ws("|", *payload_columns), 256))
        .withColumn("ingestion_batch_id", F.lit(batch_id))
        .withColumn("ingested_at_utc", F.current_timestamp())
    )
    return source, source.count()


def process_hourly_file(
    spark: SparkSession,
    site_id: str,
    path: Path,
    file_hash: str,
    batch_id: str,
) -> tuple[int, int, int]:
    frame, rows_read = build_hourly_frame(spark, site_id, path, file_hash, batch_id)
    merge_delta(spark, frame, HOURLY_PATH, ["site_id", "event_ts_utc"])
    return rows_read, rows_read, 0


def make_spark() -> SparkSession:
    builder = (
        SparkSession.builder
        .appName("GridPulse-Bronze-Ingestion")
        .master("local[2]")
        .config("spark.driver.host", "127.0.0.1")
        .config("spark.driver.bindAddress", "127.0.0.1")
        .config("spark.sql.session.timeZone", "UTC")
        .config("spark.sql.shuffle.partitions", "4")
        .config("spark.default.parallelism", "2")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.databricks.delta.schema.autoMerge.enabled", "false")
    )
    return configure_spark_with_delta_pip(builder).getOrCreate()


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest GridPulse source files into Bronze Delta tables.")
    parser.add_argument("--force", action="store_true", help="Reprocess all source files, even if unchanged.")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    log = logging.getLogger("gridpulse.bronze")

    if not DATASET_ROOT.is_dir():
        log.error("Dataset root not found: %s", DATASET_ROOT)
        return 2

    inverter_files = sorted((DATASET_ROOT / "site_a" / "raw").glob("*.xlsx")) + sorted(
        (DATASET_ROOT / "site_b" / "raw").glob("*.xlsx")
    )
    hourly_files = [
        (site, DATASET_ROOT / site / f"{site}_hourly_weather.csv")
        for site in ("site_a", "site_b")
    ]
    hourly_files = [(site, path) for site, path in hourly_files if path.is_file()]

    if not inverter_files:
        log.error("No monthly Excel files found under site_a/raw or site_b/raw.")
        return 2
    if len(hourly_files) != 2:
        log.error("Expected both hourly CSV files; found %d.", len(hourly_files))
        return 2

    batch_id = str(uuid.uuid4())
    log.info("Starting Bronze batch %s", batch_id)
    log.info("Found %d monthly Excel files and %d hourly CSV files.", len(inverter_files), len(hourly_files))
    BRONZE_ROOT.mkdir(parents=True, exist_ok=True)

    spark = None
    totals = {"excel_rows": 0, "inverter_written": 0, "quarantined": 0,
              "hourly_rows": 0, "files_processed": 0, "files_skipped": 0}

    try:
        spark = make_spark()
        spark.sparkContext.setLogLevel("WARN")
        manifest = load_manifest_map(spark)

        for path in inverter_files:
            site_id = path.parent.parent.name
            rel = relative_source_path(path)
            file_hash = sha256_file(path)
            key = ("inverter_telemetry_5m", rel)
            if not args.force and delta_exists(INVERTER_PATH) and manifest.get(key) == file_hash:
                log.info("SKIP unchanged: %s", rel)
                totals["files_skipped"] += 1
                continue

            log.info("INGEST Excel: %s", rel)
            rows_read, written, quarantined = process_excel_file(
                spark, site_id, path, file_hash, batch_id
            )
            register_manifest(
                spark,
                dataset_type="inverter_telemetry_5m",
                site_id=site_id,
                path=path,
                file_hash=file_hash,
                rows_read=rows_read,
                records_written=written,
                records_quarantined=quarantined,
                batch_id=batch_id,
            )
            manifest[key] = file_hash
            totals["excel_rows"] += rows_read
            totals["inverter_written"] += written
            totals["quarantined"] += quarantined
            totals["files_processed"] += 1
            log.info("  rows=%d valid=%d quarantined=%d", rows_read, written, quarantined)

        for site_id, path in hourly_files:
            rel = relative_source_path(path)
            file_hash = sha256_file(path)
            key = ("site_hourly_weather", rel)
            if not args.force and delta_exists(HOURLY_PATH) and manifest.get(key) == file_hash:
                log.info("SKIP unchanged: %s", rel)
                totals["files_skipped"] += 1
                continue

            log.info("INGEST hourly CSV: %s", rel)
            rows_read, written, quarantined = process_hourly_file(
                spark, site_id, path, file_hash, batch_id
            )
            register_manifest(
                spark,
                dataset_type="site_hourly_weather",
                site_id=site_id,
                path=path,
                file_hash=file_hash,
                rows_read=rows_read,
                records_written=written,
                records_quarantined=quarantined,
                batch_id=batch_id,
            )
            manifest[key] = file_hash
            totals["hourly_rows"] += rows_read
            totals["files_processed"] += 1
            log.info("  rows=%d written=%d", rows_read, written)

        log.info("========== BRONZE INGESTION SUMMARY ==========")
        for key, value in totals.items():
            log.info("%s: %s", key, f"{value:,}" if isinstance(value, int) else value)

        for label, path in (
            ("bronze_inverter_telemetry_5m", INVERTER_PATH),
            ("bronze_site_hourly_weather", HOURLY_PATH),
            ("bronze_quarantine_records", QUARANTINE_PATH),
            ("bronze_ingestion_manifest", MANIFEST_PATH),
        ):
            if delta_exists(path):
                count = spark.read.format("delta").load(str(path)).count()
                log.info("Delta table %s: %s rows", label, f"{count:,}")

        log.info("Bronze ingestion completed. Batch ID: %s", batch_id)
        return 0

    except Exception:
        log.exception("Bronze ingestion failed. Source files were not modified.")
        return 1
    finally:
        if spark is not None:
            spark.stop()


if __name__ == "__main__":
    raise SystemExit(main())
