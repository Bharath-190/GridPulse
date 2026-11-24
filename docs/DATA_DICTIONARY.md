# Initial data dictionary

## Source hourly file — `site_a_hourly_weather.csv` / `site_b_hourly_weather.csv`

| Field | Meaning | Unit / notes |
|---|---|---|
| `datetime_utc` | Start of the hourly interval | UTC timestamp |
| `datetime_local` | Local interval start | Local timestamp with UTC offset |
| `active_power_kw` | AC active power delivered to grid | kW; main output measure |
| `dc_input_power_kw` | DC input power from PV strings | kW |
| `daily_energy_kwh` | Energy since local midnight | kWh; resets daily |
| `cumulative_energy_kwh` | Lifetime cumulative yield | kWh |
| `inverter_temp_c` | Inverter internal temperature | °C |
| `grid_freq_hz` | Grid frequency | Hz |
| `power_factor` | Power factor | Dimensionless |
| `efficiency_pct` | Inverter conversion efficiency | Percent |
| `inverter_status` | Vendor status text | Categorical |
| `is_generating` | Any positive power in the hour | Boolean / 0 or 1 |
| `temp_c` | Ambient temperature | °C; Open-Meteo reanalysis |
| `humidity_pct` | Relative humidity | Percent; reanalysis |
| `cloud_cover_pct` | Total cloud cover | Percent; reanalysis |
| `wind_speed_kmh` | Wind speed at 10 m | km/h; reanalysis |
| `ghi_wm2` | Global horizontal irradiance | W/m²; reanalysis estimate |
| `dni_wm2` | Direct normal irradiance | W/m²; reanalysis estimate |
| `dhi_wm2` | Diffuse horizontal irradiance | W/m²; reanalysis estimate |
| `precip_mm` | Hourly precipitation | mm |
| `solar_elevation_deg` | Solar elevation at interval midpoint | Degrees |
| `solar_azimuth_deg` | Solar azimuth at interval midpoint | Degrees |
| `capacity_factor` | AC power divided by 50 kW inverter nominal rating | 0–1, clipped by publisher |

The source README documents the full hourly schema and limitations. Do not assume `capacity_factor` means whole-plant capacity factor; it is normalized by the inverter nominal AC rating.

## Raw monthly XLSX export

The raw files contain four non-data/header rows followed by five-minute measurements; the publisher's README documents the vendor export layout. Parser implementation will be validated on actual source files before fixing `skiprows` or column mappings in production.

| Source column | Meaning |
|---|---|
| `Start Date/Time` | Reading start timestamp |
| `Active Power (kW)` | AC active power |
| `Total Input Power (kW)` | DC input power |
| `Daily Energy (kWh)` | Daily accumulated energy |
| `Total PV Yield (kWh)` | Lifetime cumulative energy |
| `Internal Temperature (°C)` | Inverter temperature |
| `Grid Frequency (Hz)` | Grid frequency |
| `Power Factor` | Power factor |
| `Conversion Efficiency (%)` | Inverter conversion efficiency |
| `Inverter Status` | Status string |

## Synthetic-only tables

`synthetic_asset_registry` and `synthetic_maintenance_events` are scenario data designed by GridPulse. Every row must carry:

- `record_origin = 'synthetic'`
- `is_synthetic = true`
- `scenario_version`

These rows are not part of the source dataset and must not be represented as actual reported maintenance or physical equipment inventory.
