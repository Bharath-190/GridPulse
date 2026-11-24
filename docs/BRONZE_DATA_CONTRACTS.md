# GridPulse Bronze Data Contracts

## Scope

This phase ingests the publisher's 31 monthly inverter XLSX exports and two
hourly weather-enriched CSVs. Source files under `data/external/` are read-only
inputs and are never edited by the ingestion job.

## Delta tables

### `bronze_inverter_telemetry_5m`

One row per `(site_id, device_name, event_ts_utc)`.

| Field | Meaning |
|---|---|
| `site_id` | `site_a` or `site_b` |
| `timestamp_raw` | Original `Start Date/Time` text, including any timezone suffix |
| `timestamp_local` | Local wall-clock text with a recognized suffix removed for parsing |
| `timezone_suffix` | Source suffix: `DST`, `EEST`, `EET`, or NULL |
| `timezone_resolution` | Documented interpretation used for local-to-UTC conversion |
| `event_ts_utc` | Canonical UTC event timestamp |
| `active_power_kw` | Inverter active power, kW |
| `dc_input_power_kw` | Total DC input power, kW |
| `daily_energy_kwh` | Source daily energy register, kWh |
| `cumulative_energy_kwh` | Source total PV yield register, kWh |
| `inverter_temp_c` | Inverter internal temperature, °C |
| `grid_freq_hz` | Grid frequency, Hz |
| `power_factor` | Source power factor |
| `efficiency_pct` | Source conversion efficiency, percent |
| `inverter_status` | Original inverter status text |
| `source_file` | Original monthly workbook filename |
| `source_relative_path` | Path relative to the publisher dataset root |
| `source_row_number` | Physical Excel row number; header is row 4, data starts row 5 |
| `source_file_sha256` | SHA-256 of the full source workbook |
| `record_hash` | SHA-256 of normalized source values for change detection |
| `ingestion_batch_id` | Unique ID for this ingestion invocation |
| `ingested_at_utc` | UTC ingestion timestamp |

### `bronze_site_hourly_weather`

One row per `(site_id, event_ts_utc)`. All 23 publisher CSV fields are retained,
including the original `datetime_utc` and `datetime_local` strings. Numeric
measurements are explicitly cast to nullable doubles. `event_ts_utc` is the
canonical typed timestamp parsed from `datetime_utc` under a UTC Spark session.
Source-file path, SHA-256, record hash, batch ID, and ingestion timestamp are
added for lineage.

### `bronze_ingestion_manifest`

One row per processed source file and dataset type. The manifest stores the
SHA-256 fingerprint, file size, modified time, row counts, ingestion batch, and
processing time. Unchanged files are skipped on subsequent runs unless
`--force` is supplied.

### `bronze_quarantine_records`

Rows whose local timestamp cannot be parsed or represents a nonexistent local
wall time are retained here with the original row payload and rejection reason.
Other nullable measurements are not rejected simply because they are missing.

## Timezone policy

The source site timezone is `Europe/Bucharest`. The original timestamp text is
always retained. `DST` and `EEST` are interpreted as the daylight-saving
occurrence when resolving ambiguous local wall times. `EET` denotes standard
time. When a suffix is absent, standard time is selected for an ambiguous
wall-clock timestamp. Nonexistent local wall times are quarantined, not silently
shifted. All Delta event timestamps are stored with Spark's session timezone set
to UTC.

This policy is a source interpretation and must remain auditable; any later
change to publisher timestamp semantics requires a data-contract version change.

## Idempotency and updates

The file manifest skips files whose SHA-256 has not changed. New or changed
files are processed and merged using the business keys above. Rows with the
same business key and same record hash are left unchanged. Rows with the same
business key but a different record hash are updated. Removed source rows are
not automatically deleted from Bronze; source deletion reconciliation is out
of scope for this first ingestion version.

## Important measurement semantics

- `active_power_kw` is power, not energy.
- `daily_energy_kwh` and `cumulative_energy_kwh` are source energy registers.
- A complete observed five-minute hour has 12 unique readings; partial hours
  are retained and flagged in later Silver processing.
- Never sum hourly averages of kW and label the result as kWh without applying
  the interval duration and checking coverage.
- Missing sensor fields remain NULL. Zero is a real measured value and is not
  treated as missing.
- The inverter's 50 kW rated-power reference is not a hard rejection limit;
  observed readings above 50 kW are retained for engineering review.

## Output paths

- `data/bronze/delta/bronze_inverter_telemetry_5m/`
- `data/bronze/delta/bronze_site_hourly_weather/`
- `data/bronze/delta/bronze_ingestion_manifest/`
- `data/bronze/delta/bronze_quarantine_records/` (created if needed)
