# GridPulse — initial architecture decisions

## Data flow

```text
Publisher source repository
        |
        v
Immutable landing zone (raw monthly XLSX + source hourly CSV)
        |
        v
BRONZE: raw source rows + ingestion metadata + source lineage
        |
        v
SILVER: standardized timestamps, typed numeric fields, deduplication,
        data-quality results and quarantined invalid rows
        |
        +------------------------------+
        |                              |
        v                              v
Observed site telemetry          Synthetic operations tables
        |                         (separate provenance)
        +---------------+--------------+
                        |
                        v
GOLD: site-day KPIs, inverter efficiency, capacity-factor trends,
      availability proxy, production deviations, weather context
                        |
                        v
Databricks SQL / dashboard
```

## Initial business questions

1. What is the daily and monthly energy yield for each site?
2. How does inverter efficiency vary with DC input power and temperature?
3. How do irradiance, cloud cover and ambient temperature relate to generation?
4. How often is the inverter in a non-generating status during daylight?
5. Which intervals should be reviewed for abnormal generation or status changes?
6. What would a synthetic maintenance work-order workflow look like, and how would its KPIs be displayed separately from observed data?

## Metric definitions to lock before implementation

- **Energy (kWh):** integrate/aggregate power over interval duration; do not sum instantaneous kW as if it were energy.
- **Capacity factor (inverter-normalized):** interval AC power / 50 kW inverter nominal AC rating, clipped to the source convention. Label it explicitly as inverter-normalized.
- **Inverter conversion efficiency:** use the source's `efficiency_pct` where valid; recompute DC-to-AC efficiency only after verifying units and interval semantics.
- **Availability proxy:** daylight periods with expected operating conditions but non-generating or fault-like status. This is a diagnostic proxy, not contractual availability.
- **Energy loss estimate:** do not publish until a defensible baseline/expected-power model and uncertainty note exist.

## Why the local-first plan

First validate source schema, units, time semantics, and data quality locally. Then implement transformations in Spark and move execution to Databricks. This avoids paying for cloud compute while schema assumptions are still changing.
