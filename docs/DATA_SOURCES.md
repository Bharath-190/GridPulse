# GridPulse — Data sources and provenance register

Last reviewed: 2026-11-24

## 1. Primary measured-data source — Two-Site Solar PV Inverter & Weather Dataset

- Publisher/repository: University Politehnica of Bucharest NLP group (`upb-nlp`).
- URL: https://github.com/upb-nlp/PV-Generation-Dataset
- License: Creative Commons Attribution 4.0 International (CC BY 4.0), as stated in the source README.
- Citation: Linca, N.-R., Rebedea, T.-E., Ruseti, S., and Dascalu, M. (2026). *Two-Site Solar PV Inverter & Weather Dataset (Romania).* https://github.com/upb-nlp/PV-Generation-Dataset
- Coverage: Site A, 2025-01-04 to 2026-06-30 (18 months); Site B, 2025-05-01 to 2026-05-31 (13 months).
- Assets: two independent, unaffiliated grid-connected 50 kW PV installations in southwestern Romania, both with Huawei SUN2000 string inverters.
- Original resolution: five-minute inverter exports.
- Included derived data: hourly generation joined to historical weather and solar position.
- Key measured fields: active AC power, DC input power, daily energy, cumulative energy, inverter temperature, grid frequency, power factor, conversion efficiency, and inverter status.
- Weather fields: temperature, humidity, cloud cover, wind speed, GHI, DNI, DHI, precipitation.
- Important caveat: source weather is Open-Meteo historical reanalysis, not an on-site weather station. Solar-radiation values are estimates; the source states there is no irradiance sensor ground truth.
- Important caveat: coordinates are anonymized/rounded. Do not present them as exact plant coordinates.
- Important caveat: daylight-saving transitions create missing hourly timestamps in the raw source exports. Missing observations must not be changed to zero.

Recommended use in GridPulse:
- Bronze: raw monthly XLSX exports with source-file metadata.
- Silver: standardized 5-minute observations, timestamp normalization, quality flags, and deduplication.
- Gold: daily energy, capacity factor, inverter efficiency, availability proxies, and weather-adjusted performance summaries.
- Validation: reconcile hourly aggregates from our Silver records against the publisher's hourly CSV.

## 2. Optional independent weather enrichment — Open-Meteo Historical Weather API

- Documentation: https://open-meteo.com/en/docs/historical-weather-api
- API: https://archive-api.open-meteo.com/v1/archive
- Coverage: ERA5 from 1940; ERA5-Land from 1950; hourly variables include temperature, humidity, precipitation, cloud cover, wind speed/direction, and solar radiation.
- Data license: CC BY 4.0; attribution required.
- Free hosted API: non-commercial use; check the provider's current terms before commercial/high-volume use.

Recommended use: optional independent weather backfill/check. Because source site coordinates are anonymized, this should be presented as regional/grid-cell weather context, not precise site-station weather.

## 3. Optional large-scale PV asset source — NREL PVDAQ / OEDI

- Data.gov catalogue: https://catalog.data.gov/dataset/photovoltaic-data-acquisition-pvdaq-public-datasets
- OEDI data lake: https://data.openei.org/submissions/4568
- Documentation: https://github.com/openEDI/documentation/blob/main/pvdaq.md
- Access helper: https://github.com/NatLabRockies/pvdaq_access
- Dataset DOI: https://doi.org/10.25984/1846021
- Contents: multi-site PV performance time series, system/site metadata, inverter/meter metadata and sensor metrics. Some systems include irradiance, temperature, wind and precipitation sensors.
- Scale warning: the complete data lake is very large; some 2023 Solar Data Prize submissions can be tens or hundreds of GB. Do not download the whole archive. Select a regular PVDAQ system or a specific prize-site dataset and time window only after inspecting metadata and expected size.
- License/provenance: public availability is confirmed in the U.S. government catalogue, but verify the dataset's applicable reuse terms and cite the DOI before redistributing records. The BSD-3-Clause license in `pvdaq_access` applies to the downloader software, not automatically to the underlying measurements.

Recommended use: Phase 2/advanced extension for broader site diversity after the first pipeline works.

## 4. Optional grid-level reference — Open Power System Data (OPSD)

- Dataset: https://data.open-power-system-data.org/time_series/
- GitHub: https://github.com/Open-Power-System-Data/time_series
- License for repository materials: MIT; review the data package documentation and its source-specific conditions before redistribution.
- Published package: time series of load, wind/solar generation, and prices aggregated by country/control area/bidding zone. The 2020-10-06 package covers 32 European countries and its newest records run through mid-2020.
- Romania fields listed by the package include `RO_solar_generation_actual`, `RO_wind_onshore_generation_actual`, and `RO_load_actual_entsoe_transparency`.
- Limitation: this package's period does not overlap the primary PV site data (2025–2026). Use it only as a separate historical grid-context dataset; do not join it row-by-row to the 2025–2026 site telemetry.

## 5. Not selected for the core build — Kaggle Solar Power Generation Data

- URL: https://www.kaggle.com/datasets/anikannal/solar-power-generation-data
- Scope: two Indian solar plants, 15-minute inverter generation and plant-level sensor data over 34 days.
- Licence shown by Kaggle: `Data files © Original Authors` (not a standard permissive open-data license).
- Decision: useful for experimentation, but not selected for the distributable core dataset because the rights are less clear and the history is short. Do not mirror or redistribute it without permission from the original rights holder.

## Data governance policy

- Store `source_name`, `source_url`, `source_version_or_retrieval_date`, `record_origin`, and `is_synthetic` in data manifests and/or Bronze metadata.
- Preserve original source files unchanged.
- Store transformations separately; never overwrite raw data.
- Store source-level license and attribution in the repository.
- Keep synthetic scenarios in their own folder and tables. Never blend them into observed metrics without an explicit filter or label.
