# GridPulse — Source Data Audit

Automated structural and data-quality audit.

Total files in source repository: 76

## 1. Repository inventory

- **.git/**: 40 files
- **site_a/**: 19 files
- **site_b/**: 14 files

## 2. Hourly datasets

### SITE_A

- File size: 1993.3 KB
- Rows: 13,031
- Columns: 23
- Duplicate complete rows: 0
- Invalid UTC timestamps: 0
- Duplicate UTC timestamps: 0
- UTC range: 2025-01-03 22:00:00+00:00 to 2026-06-30 20:00:00+00:00
- Expected hourly slots: 13,031
- Missing hourly slots: 0
- Local/UTC conversion mismatches: 0
- Invalid local timestamps: 0

#### Missing values
- `active_power_kw`: 260 (2.00%)
- `dc_input_power_kw`: 4,927 (37.81%)
- `daily_energy_kwh`: 4,927 (37.81%)
- `cumulative_energy_kwh`: 4,927 (37.81%)
- `inverter_temp_c`: 4,927 (37.81%)
- `grid_freq_hz`: 4,927 (37.81%)
- `power_factor`: 4,927 (37.81%)
- `efficiency_pct`: 4,927 (37.81%)
- `inverter_status`: 4,927 (37.81%)
- `is_generating`: 260 (2.00%)
- `temp_c`: 262 (2.01%)
- `humidity_pct`: 262 (2.01%)
- `cloud_cover_pct`: 262 (2.01%)
- `wind_speed_kmh`: 262 (2.01%)
- `ghi_wm2`: 262 (2.01%)
- `dni_wm2`: 262 (2.01%)
- `dhi_wm2`: 262 (2.01%)
- `precip_mm`: 262 (2.01%)
- `capacity_factor`: 260 (2.00%)

#### Numeric measurements
- `active_power_kw`: min=0.0, max=55.0
- `dc_input_power_kw`: min=0.0, max=56.2827
- `daily_energy_kwh`: min=0.0, max=421.85
- `cumulative_energy_kwh`: min=202230.87, max=325989.39
- `inverter_temp_c`: min=-2.05, max=67.8833
- `grid_freq_hz`: min=0.0, max=50.0692
- `power_factor`: min=0.0, max=1.0
- `efficiency_pct`: min=0.0, max=98.58
- `is_generating`: min=0.0, max=1.0
- `temp_c`: min=-13.4, max=34.6
- `humidity_pct`: min=19.0, max=100.0
- `cloud_cover_pct`: min=0.0, max=100.0
- `wind_speed_kmh`: min=0.0, max=28.3
- `ghi_wm2`: min=0.0, max=945.0
- `dni_wm2`: min=0.0, max=897.6
- `dhi_wm2`: min=0.0, max=400.0
- `precip_mm`: min=0.0, max=8.6
- `solar_elevation_deg`: min=0.0, max=68.4354
- `solar_azimuth_deg`: min=0.0033, max=359.9904
- `capacity_factor`: min=0.0, max=1.0
- Active power above 50 kW: 98
- Negative active power: 0
- Capacity factor outside [0, 1]: 0

### SITE_B

- File size: 1455.3 KB
- Rows: 9,504
- Columns: 23
- Duplicate complete rows: 0
- Invalid UTC timestamps: 0
- Duplicate UTC timestamps: 0
- UTC range: 2025-04-30 21:00:00+00:00 to 2026-05-31 20:00:00+00:00
- Expected hourly slots: 9,504
- Missing hourly slots: 0
- Local/UTC conversion mismatches: 0
- Invalid local timestamps: 0

#### Missing values
- `active_power_kw`: 170 (1.79%)
- `dc_input_power_kw`: 3,581 (37.68%)
- `daily_energy_kwh`: 3,581 (37.68%)
- `cumulative_energy_kwh`: 3,581 (37.68%)
- `inverter_temp_c`: 3,581 (37.68%)
- `grid_freq_hz`: 3,581 (37.68%)
- `power_factor`: 3,581 (37.68%)
- `efficiency_pct`: 3,581 (37.68%)
- `inverter_status`: 3,581 (37.68%)
- `is_generating`: 170 (1.79%)
- `temp_c`: 170 (1.79%)
- `humidity_pct`: 170 (1.79%)
- `cloud_cover_pct`: 170 (1.79%)
- `wind_speed_kmh`: 170 (1.79%)
- `ghi_wm2`: 170 (1.79%)
- `dni_wm2`: 170 (1.79%)
- `dhi_wm2`: 170 (1.79%)
- `precip_mm`: 170 (1.79%)
- `capacity_factor`: 170 (1.79%)

#### Numeric measurements
- `active_power_kw`: min=0.0, max=53.0712
- `dc_input_power_kw`: min=0.0, max=54.1303
- `daily_energy_kwh`: min=0.0, max=406.67
- `cumulative_energy_kwh`: min=0.0, max=275930.97
- `inverter_temp_c`: min=-1.2, max=63.25
- `grid_freq_hz`: min=0.0, max=50.0675
- `power_factor`: min=0.0, max=1.0
- `efficiency_pct`: min=0.0, max=98.5125
- `is_generating`: min=0.0, max=1.0
- `temp_c`: min=-13.4, max=34.6
- `humidity_pct`: min=19.0, max=100.0
- `cloud_cover_pct`: min=0.0, max=100.0
- `wind_speed_kmh`: min=0.0, max=28.3
- `ghi_wm2`: min=0.0, max=945.0
- `dni_wm2`: min=0.0, max=895.1
- `dhi_wm2`: min=0.0, max=400.0
- `precip_mm`: min=0.0, max=8.6
- `solar_elevation_deg`: min=0.0, max=68.4354
- `solar_azimuth_deg`: min=0.0274, max=359.9904
- `capacity_factor`: min=0.0, max=1.0
- Active power above 50 kW: 17
- Negative active power: 0
- Capacity factor outside [0, 1]: 0

### Schema comparison
- Same columns: True
- Only in Site A: []
- Only in Site B: []

## 3. Raw Excel exports

### SITE_A
- Excel files: 18

#### site_a_2025-01.xlsx
- Rows: 3,463
- Timestamp suffix records: 0
- Timestamp parse failures after suffix removal: 0
- Exact duplicate raw timestamps: 0
- Duplicate parsed local times: 0
- Time range: 2025-01-04 07:45:00 to 2025-01-31 18:05:00

#### site_a_2025-02.xlsx
- Rows: 3,805
- Timestamp suffix records: 0
- Timestamp parse failures after suffix removal: 0
- Exact duplicate raw timestamps: 0
- Duplicate parsed local times: 0
- Time range: 2025-02-01 00:00:00 to 2025-02-28 18:35:00

#### site_a_2025-03.xlsx
- Rows: 4,746
- Timestamp suffix records: 324
- Timestamp parse failures after suffix removal: 0
- Exact duplicate raw timestamps: 0
- Duplicate parsed local times: 0
- Time range: 2025-03-01 00:00:00 to 2025-03-31 20:20:00

#### site_a_2025-04.xlsx
- Rows: 5,167
- Timestamp suffix records: 5,167
- Timestamp parse failures after suffix removal: 0
- Exact duplicate raw timestamps: 0
- Duplicate parsed local times: 0
- Time range: 2025-04-01 00:00:00 to 2025-04-30 21:00:00

#### site_a_2025-05.xlsx
- Rows: 5,864
- Timestamp suffix records: 5,864
- Timestamp parse failures after suffix removal: 0
- Exact duplicate raw timestamps: 0
- Duplicate parsed local times: 0
- Time range: 2025-05-01 00:00:00 to 2025-05-31 21:40:00

#### site_a_2025-06.xlsx
- Rows: 5,966
- Timestamp suffix records: 5,966
- Timestamp parse failures after suffix removal: 0
- Exact duplicate raw timestamps: 0
- Duplicate parsed local times: 0
- Time range: 2025-06-01 00:00:00 to 2025-06-30 21:55:00

#### site_a_2025-07.xlsx
- Rows: 6,112
- Timestamp suffix records: 6,112
- Timestamp parse failures after suffix removal: 0
- Exact duplicate raw timestamps: 0
- Duplicate parsed local times: 0
- Time range: 2025-07-01 00:00:00 to 2025-07-31 21:30:00

#### site_a_2025-08.xlsx
- Rows: 5,659
- Timestamp suffix records: 5,659
- Timestamp parse failures after suffix removal: 0
- Exact duplicate raw timestamps: 0
- Duplicate parsed local times: 0
- Time range: 2025-08-01 00:00:00 to 2025-08-31 20:30:00

#### site_a_2025-09.xlsx
- Rows: 4,814
- Timestamp suffix records: 4,814
- Timestamp parse failures after suffix removal: 0
- Exact duplicate raw timestamps: 0
- Duplicate parsed local times: 0
- Time range: 2025-09-01 00:00:00 to 2025-09-30 19:35:00

#### site_a_2025-10.xlsx
- Rows: 4,388
- Timestamp suffix records: 3,578
- Timestamp parse failures after suffix removal: 0
- Exact duplicate raw timestamps: 0
- Duplicate parsed local times: 0
- Time range: 2025-10-01 00:00:00 to 2025-10-31 17:50:00

#### site_a_2025-11.xlsx
- Rows: 3,739
- Timestamp suffix records: 0
- Timestamp parse failures after suffix removal: 0
- Exact duplicate raw timestamps: 0
- Duplicate parsed local times: 0
- Time range: 2025-11-01 00:00:00 to 2025-11-30 17:15:00

#### site_a_2025-12.xlsx
- Rows: 3,645
- Timestamp suffix records: 0
- Timestamp parse failures after suffix removal: 0
- Exact duplicate raw timestamps: 0
- Duplicate parsed local times: 0
- Time range: 2025-12-01 00:00:00 to 2025-12-31 17:30:00

#### site_a_2026-01.xlsx
- Rows: 4,081
- Timestamp suffix records: 0
- Timestamp parse failures after suffix removal: 0
- Exact duplicate raw timestamps: 0
- Duplicate parsed local times: 0
- Time range: 2026-01-01 00:00:00 to 2026-01-31 18:00:00

#### site_a_2026-02.xlsx
- Rows: 3,767
- Timestamp suffix records: 0
- Timestamp parse failures after suffix removal: 0
- Exact duplicate raw timestamps: 0
- Duplicate parsed local times: 0
- Time range: 2026-02-01 00:00:00 to 2026-02-28 18:45:00

#### site_a_2026-03.xlsx
- Rows: 4,750
- Timestamp suffix records: 484
- Timestamp parse failures after suffix removal: 0
- Exact duplicate raw timestamps: 0
- Duplicate parsed local times: 0
- Time range: 2026-03-01 00:00:00 to 2026-03-31 20:20:00

#### site_a_2026-04.xlsx
- Rows: 5,212
- Timestamp suffix records: 5,212
- Timestamp parse failures after suffix removal: 0
- Exact duplicate raw timestamps: 0
- Duplicate parsed local times: 0
- Time range: 2026-04-01 00:00:00 to 2026-04-30 20:55:00

#### site_a_2026-05.xlsx
- Rows: 5,883
- Timestamp suffix records: 5,883
- Timestamp parse failures after suffix removal: 0
- Exact duplicate raw timestamps: 0
- Duplicate parsed local times: 0
- Time range: 2026-05-01 00:00:00 to 2026-05-31 21:35:00

#### site_a_2026-06.xlsx
- Rows: 6,083
- Timestamp suffix records: 6,083
- Timestamp parse failures after suffix removal: 0
- Exact duplicate raw timestamps: 0
- Duplicate parsed local times: 0
- Time range: 2026-06-01 00:00:00 to 2026-06-30 21:50:00

#### Site-level summary
- Total Excel rows: 87,144
- Total timestamp parse failures: 0
- Repeated parsed local timestamps across files: 0

### SITE_B
- Excel files: 13

#### site_b_2025-05.xlsx
- Rows: 5,874
- Timestamp suffix records: 5,874
- Timestamp parse failures after suffix removal: 0
- Exact duplicate raw timestamps: 0
- Duplicate parsed local times: 0
- Time range: 2025-05-01 00:00:00 to 2025-05-31 21:40:00

#### site_b_2025-06.xlsx
- Rows: 5,975
- Timestamp suffix records: 5,975
- Timestamp parse failures after suffix removal: 0
- Exact duplicate raw timestamps: 0
- Duplicate parsed local times: 0
- Time range: 2025-06-01 00:00:00 to 2025-06-30 21:55:00

#### site_b_2025-07.xlsx
- Rows: 6,030
- Timestamp suffix records: 6,030
- Timestamp parse failures after suffix removal: 0
- Exact duplicate raw timestamps: 0
- Duplicate parsed local times: 0
- Time range: 2025-07-01 00:00:00 to 2025-07-31 21:30:00

#### site_b_2025-08.xlsx
- Rows: 5,575
- Timestamp suffix records: 5,575
- Timestamp parse failures after suffix removal: 0
- Exact duplicate raw timestamps: 0
- Duplicate parsed local times: 0
- Time range: 2025-08-01 05:40:00 to 2025-08-31 20:30:00

#### site_b_2025-09.xlsx
- Rows: 4,817
- Timestamp suffix records: 4,817
- Timestamp parse failures after suffix removal: 0
- Exact duplicate raw timestamps: 0
- Duplicate parsed local times: 0
- Time range: 2025-09-01 00:00:00 to 2025-09-30 19:35:00

#### site_b_2025-10.xlsx
- Rows: 4,395
- Timestamp suffix records: 3,584
- Timestamp parse failures after suffix removal: 0
- Exact duplicate raw timestamps: 0
- Duplicate parsed local times: 0
- Time range: 2025-10-01 00:00:00 to 2025-10-31 17:50:00

#### site_b_2025-11.xlsx
- Rows: 3,925
- Timestamp suffix records: 0
- Timestamp parse failures after suffix removal: 0
- Exact duplicate raw timestamps: 0
- Duplicate parsed local times: 0
- Time range: 2025-11-01 00:00:00 to 2025-11-30 17:20:00

#### site_b_2025-12.xlsx
- Rows: 3,648
- Timestamp suffix records: 0
- Timestamp parse failures after suffix removal: 0
- Exact duplicate raw timestamps: 0
- Duplicate parsed local times: 0
- Time range: 2025-12-01 00:00:00 to 2025-12-31 17:30:00

#### site_b_2026-01.xlsx
- Rows: 3,753
- Timestamp suffix records: 0
- Timestamp parse failures after suffix removal: 0
- Exact duplicate raw timestamps: 0
- Duplicate parsed local times: 0
- Time range: 2026-01-01 00:00:00 to 2026-01-31 18:00:00

#### site_b_2026-02.xlsx
- Rows: 3,760
- Timestamp suffix records: 0
- Timestamp parse failures after suffix removal: 0
- Exact duplicate raw timestamps: 0
- Duplicate parsed local times: 0
- Time range: 2026-02-01 00:00:00 to 2026-02-28 18:45:00

#### site_b_2026-03.xlsx
- Rows: 4,753
- Timestamp suffix records: 484
- Timestamp parse failures after suffix removal: 0
- Exact duplicate raw timestamps: 0
- Duplicate parsed local times: 0
- Time range: 2026-03-01 00:00:00 to 2026-03-31 20:20:00

#### site_b_2026-04.xlsx
- Rows: 5,194
- Timestamp suffix records: 5,194
- Timestamp parse failures after suffix removal: 0
- Exact duplicate raw timestamps: 0
- Duplicate parsed local times: 0
- Time range: 2026-04-01 00:00:00 to 2026-04-30 21:00:00

#### site_b_2026-05.xlsx
- Rows: 5,981
- Timestamp suffix records: 5,981
- Timestamp parse failures after suffix removal: 0
- Exact duplicate raw timestamps: 0
- Duplicate parsed local times: 0
- Time range: 2026-05-01 00:00:00 to 2026-05-31 21:40:00

#### Site-level summary
- Total Excel rows: 63,680
- Total timestamp parse failures: 0
- Repeated parsed local timestamps across files: 0

## 4. Archived forecast datasets

- Archived forecast directory not found locally.