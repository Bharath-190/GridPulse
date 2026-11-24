# GridPulse Silver Data Contracts

## Purpose

Silver converts the validated Bronze Delta snapshots into consistent,
query-ready datasets. It preserves the publisher's observations and lineage,
adds quality metadata without deleting suspicious records, and provides
coverage-aware hourly comparisons between the monthly five-minute workbooks
and the publisher's hourly weather-enriched CSVs.

All timestamps used for joins and grouping are UTC. The source's original
local-time strings remain available in Bronze and in the retained hourly
source fields.

## Output tables

### `silver_inverter_telemetry_5m`

Grain: one row per `(site_id, device_name, event_ts_utc)`.

This table retains Bronze measurements and file/row lineage. It adds:

- `event_date_utc`, `event_hour_utc` for date and hour filtering.
- `measurement_null_count` across the eight numeric inverter measurements.
- `measurement_completeness_pct` across those same eight fields.
- `active_power_negative_flag` as a review flag; the record is retained.
- `data_quality_status`: `review`, `partial`, or `complete`.

Missing readings remain NULL. Zero remains a valid measurement. A row with
other missing sensor fields is not rejected.

### `silver_site_hourly_conditions`

Grain: one row per `(site_id, event_ts_utc)` from the publisher's hourly CSV.

All 23 publisher fields and Bronze source lineage are retained. The table adds
UTC date/hour columns, `numeric_null_count`, individual `*_range_violation_flag`
columns for the configured basic bounds, `range_violation_count`, and
`data_quality_status`.

Range checks are non-destructive. They only flag suspicious observations;
they do not filter, clip, or replace values. No fixed temperature or wind-speed
bounds are imposed because those require site/sensor context.

### `silver_site_hourly_performance`

Grain: one row per `(site_id, event_hour_utc)` across the union of publisher
hourly records and hours found in five-minute inverter telemetry.

The table is a **full outer join**. This preserves both publisher hours with no
matching five-minute records and five-minute telemetry hours with no matching
publisher hourly record.

Important columns:

- `publisher_hourly_active_power_kw`: active power from the publisher hourly CSV.
- `five_minute_mean_active_power_kw`: arithmetic mean of available five-minute
  active-power readings in the UTC hour.
- `raw_sample_count`: number of distinct five-minute UTC timestamps observed.
- `raw_record_count`: number of five-minute source records in the hour.
- `active_power_sample_count`: number of those records with non-NULL active power.
- `raw_data_coverage_pct`: `min(raw_sample_count / 12, 1) * 100`.
- `raw_coverage_status`: `no_raw_data`, `partial`, `complete_12`, or `overfull`.
- `active_power_mean_abs_delta_kw`: absolute difference between publisher
  hourly active power and five-minute mean, populated only when the hour has 12
  distinct timestamps, 12 non-NULL active-power values, and a non-NULL publisher
  active-power value.
- `hour_alignment_status`: identifies absent publisher hours, absent raw data,
  complete comparison candidates, source-conflict hours, complete raw hours
  missing publisher power, complete timestamp hours missing some power values,
  partial hours, and overfull hours.
- `daylight_context_flag`: true when publisher solar elevation exceeds 5 degrees
  or GHI is at least 100 W/m². This is context for review, not proof of generation.
- `publisher_operational_null_count`: number of NULL values among eight publisher
  inverter-operational fields (DC power, daily/cumulative energy, inverter
  temperature, grid frequency, power factor, efficiency, and inverter status).
- `publisher_operational_fields_missing_flag`: true when at least six of those
  eight fields are NULL during daylight context.
- `publisher_zero_conflict_with_raw_generation_flag`: true when a complete raw
  hour has a five-minute mean above 1 kW, the publisher reports exactly 0 kW,
  and daylight context is present. This marks disagreement; it does not decide
  which source is correct.
- `active_power_comparison_eligible_flag`: false for incomplete comparisons and
  for the zero-vs-generation conflict described above.

`active_power_mean_abs_delta_kw` remains populated for complete matched hours,
including flagged conflicts, so the discrepancy remains measurable and
traceable. Gold reconciliation metrics must filter to
`active_power_comparison_eligible_flag = true` and report excluded conflict
hours separately. Neither source measurement is overwritten or discarded.

The source profiling found that a complete five-minute hour normally has 12
unique readings. `complete_12` means timestamp coverage only; a separate
`active_power_sample_count` shows whether all 12 power values are present.

The five-minute mean is a mean of available readings. It is not itself energy.
No kWh value is calculated by summing kW samples. Energy modeling is deferred
to a separate Gold/business-metrics phase with its assumptions documented.

## Data quality principles

1. Never drop rows solely because a nullable sensor value is missing.
2. Never convert NULL to zero.
3. Never silently clip values to a range.
4. Do not treat 50 kW rated power as a hard maximum or rejection threshold.
5. Keep five-minute observations and publisher hourly values separately named.
6. Compare the two active-power sources only on complete 12-timestamp hours
   that are also marked comparison-eligible.
7. Explicitly flag daylight zero-vs-generation conflicts; never silently choose
   one source as ground truth.
8. Do not use partial-hour means as though they represented a full hour.
9. Preserve source paths and hashes to support lineage and reconciliation.

## Refresh semantics

Silver tables are deterministic full-refresh materializations of the current
Bronze Delta tables. Each run replaces the Silver snapshots so that changed or
removed Bronze rows cannot leave stale Silver records. Bronze source history
and ingestion manifests remain untouched. This strategy is appropriate for the
current dataset size and can later be replaced by partition-aware incremental
processing if scale requires it.

## Paths

- `data/silver/delta/silver_inverter_telemetry_5m/`
- `data/silver/delta/silver_site_hourly_conditions/`
- `data/silver/delta/silver_site_hourly_performance/`
