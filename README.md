# GridPulse — Data Collection Starter Kit

**Project:** Renewable Energy Intelligence & Data Engineering Platform  
**Version:** 0.1.0 — data acquisition preparation  
**Status:** Source research completed; raw source files are not bundled in this kit.

GridPulse will ingest real photovoltaic (PV) generation records, enrich them with weather context, create quality-controlled Delta tables, and publish operational analytics. Synthetic maintenance and asset data will be kept visibly separate from observed measurements.

## Primary dataset selected

**Two-Site Solar PV Inverter & Weather Dataset (Romania)**  
Source: https://github.com/upb-nlp/PV-Generation-Dataset  
License: CC BY 4.0 (attribution required)  
Citation: Linca, N.-R., Rebedea, T.-E., Ruseti, S., and Dascalu, M. (2026). *Two-Site Solar PV Inverter & Weather Dataset (Romania).* https://github.com/upb-nlp/PV-Generation-Dataset

The dataset contains two real, anonymized, grid-connected 50 kW solar PV installations in southwestern Romania. Site A covers 2025-01-04 through 2026-06-30; Site B covers 2025-05-01 through 2026-05-31. Original inverter data is recorded every five minutes. The repository also provides hourly weather-enriched CSV files and archived weather forecasts.

Use the raw monthly Excel exports for our Bronze ingestion exercise. Use the hourly weather-enriched CSV as a cross-check and optional analytics input, not as a replacement for our own transformations.

## Get the source data

### Linux / macOS / EndeavourOS

From this directory:

```bash
bash scripts/download_primary_dataset.sh
```

### Windows PowerShell

From this directory:

```powershell
.\scripts\download_primary_dataset.ps1
```

The scripts use Git sparse checkout to retrieve only `site_a/` and `site_b/` from the upstream dataset repository. This avoids downloading its separate forecasting toolkit and unrelated materials.

Expected result:

```text
data/external/PV-Generation-Dataset/
├── site_a/
│   ├── site_a_hourly_weather.csv
│   └── raw/*.xlsx
└── site_b/
    ├── site_b_hourly_weather.csv
    └── raw/*.xlsx
```

If Git sparse checkout is not available, clone the source repository normally and copy the two site folders into `data/external/PV-Generation-Dataset/`.

## Generate synthetic operational reference data

Asset inventory and maintenance history are **synthetic**, not source measurements. Generate these only for pipeline demonstrations:

```bash
python -m pip install -r requirements-data.txt
python scripts/generate_synthetic_operations.py --output-dir data/synthetic --seed 42
```

This creates synthetic plant/asset registry and maintenance event files. All synthetic rows include `record_origin=synthetic` and `is_synthetic=true` so they cannot be mistaken for measured data.

## Validate the downloaded data

```bash
python scripts/validate_primary_dataset.py --dataset-dir data/external/PV-Generation-Dataset
```

The validator checks the expected folder layout, required hourly columns, date parsing, frequency, and the availability of raw Excel exports. It does not modify source files.

## Proposed data lake layout

```text
data/
├── external/       # downloaded source data; do not edit
├── raw/            # optional local landing copies
├── bronze/         # raw ingested Delta tables + source metadata
├── silver/         # standardized and quality-checked Delta tables
├── gold/           # business-ready aggregates and KPIs
└── synthetic/      # clearly labelled simulated operations data
```

The production implementation will use cloud object storage and Databricks volumes/catalogs. This local folder is for development, inspection, and reproducible tests only.

## Important modelling rules

1. Do not label reanalysis weather as on-site sensor measurements. The source repository states that its hourly weather fields are Open-Meteo historical reanalysis estimates.
2. Do not invent plant coordinates. The published coordinates are deliberately rounded to approximately 0.1 degrees for anonymization.
3. Treat daylight-saving-time gaps as missing source observations, not as zero generation.
4. Keep legitimate nighttime zero-power observations; they are not missing values.
5. Do not infer a hardware failure from a single zero-power reading. Consider solar elevation, weather, inverter status, and surrounding time windows.
6. Synthetic asset and maintenance rows must remain traceable via `is_synthetic` and `record_origin`.
7. Never commit large raw datasets, credentials, API keys, or private cloud configuration to Git.

## Project environment

Recommended local development environment:

- Python 3.11
- Git
- Java 17 only if local Spark is used
- PySpark for local transformation tests (Databricks Runtime will provide Spark in the cloud)
- `pandas`, `openpyxl`, `pyarrow`, `requests`, `PyYAML`

Cloud phase (later): Databricks workspace, object storage (AWS S3 or equivalent), Unity Catalog, and a small SQL warehouse. We will verify current free-tier and cloud pricing before enabling any paid resources.

## Source attribution

Include the dataset's CC BY 4.0 attribution in the project README, dashboard credits, and any report that presents its measurements. See `docs/DATA_SOURCES.md` for source notes and additional candidate sources.
