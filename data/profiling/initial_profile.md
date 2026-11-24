# GridPulse — Initial Data Profiling

Dataset directory: `/home/bharath/Projects/GridPulse/data/external/PV-Generation-Dataset`
Files discovered: 33

## site_a/raw/site_a_2025-01.xlsx — 5 min

- Rows: 3,463
- Columns: 13
- Duplicate rows: 0

### Column profile

| Column | Data type | Missing | Unique |
|---|---|---:|---:|
| Site Name | object | 0.00% | 1 |
| Installer | object | 0.00% | 1 |
| Device Name | object | 0.00% | 1 |
| Start Date/Time | object | 0.00% | 3,463 |
| Active Power (kW) | float64 | 0.00% | 3,008 |
| Total Input Power (kW) | float64 | 0.00% | 3,024 |
| Daily Energy (kWh) | float64 | 0.00% | 2,807 |
| Total PV Yield (kWh) | float64 | 0.00% | 3,174 |
| Internal Temperature (°C) | float64 | 0.00% | 442 |
| Grid Frequency (Hz) | float64 | 0.00% | 18 |
| Power Factor | float64 | 0.00% | 11 |
| Conversion Efficiency (%) | float64 | 0.00% | 531 |
| Inverter Status | object | 0.00% | 6 |

### Date/time candidates

- **Start Date/Time**: 3,463/3,463 parseable values
  - Range: 2025-01-04 07:45:00 to 2025-01-31 18:05:00

### Sample records

```text
Site Name Installer            Device Name     Start Date/Time  Active Power (kW)  Total Input Power (kW)  Daily Energy (kWh)  Total PV Yield (kWh)  Internal Temperature (°C)  Grid Frequency (Hz)  Power Factor  Conversion Efficiency (%)             Inverter Status
   Site A Installer Logger/50KTL-M0(SiteA) 2025-01-04 07:45:00                0.0                     0.0                 0.0             202230.87                        6.5                  0.0           0.0                        0.0       Standby: initializing
   Site A Installer Logger/50KTL-M0(SiteA) 2025-01-04 07:50:00                0.0                     0.0                 0.0             202230.87                        6.3                 50.0           0.0                        0.0 Standby: detecting sunlight
   Site A Installer Logger/50KTL-M0(SiteA) 2025-01-04 07:55:00                0.0                     0.0                 0.0             202230.87                        6.3                 50.0           0.0                        0.0 Standby: detecting sunlight
```

## site_a/raw/site_a_2025-02.xlsx — 5 min

- Rows: 3,805
- Columns: 13
- Duplicate rows: 0

### Column profile

| Column | Data type | Missing | Unique |
|---|---|---:|---:|
| Site Name | object | 0.00% | 1 |
| Installer | object | 0.00% | 1 |
| Device Name | object | 0.00% | 1 |
| Start Date/Time | object | 0.00% | 3,805 |
| Active Power (kW) | float64 | 0.00% | 3,271 |
| Total Input Power (kW) | float64 | 0.00% | 3,281 |
| Daily Energy (kWh) | float64 | 0.00% | 2,925 |
| Total PV Yield (kWh) | float64 | 0.00% | 3,502 |
| Internal Temperature (°C) | float64 | 0.00% | 477 |
| Grid Frequency (Hz) | float64 | 0.00% | 20 |
| Power Factor | float64 | 0.00% | 14 |
| Conversion Efficiency (%) | float64 | 0.00% | 637 |
| Inverter Status | object | 0.00% | 5 |

### Date/time candidates

- **Start Date/Time**: 3,805/3,805 parseable values
  - Range: 2025-02-01 00:00:00 to 2025-02-28 18:35:00

### Sample records

```text
Site Name Installer            Device Name     Start Date/Time  Active Power (kW)  Total Input Power (kW)  Daily Energy (kWh)  Total PV Yield (kWh)  Internal Temperature (°C)  Grid Frequency (Hz)  Power Factor  Conversion Efficiency (%)             Inverter Status
   Site A Installer Logger/50KTL-M0(SiteA) 2025-02-01 00:00:00                0.0                     0.0                 0.0             207334.86                       15.1                 0.00           0.0                        0.0        Standby: no sunlight
   Site A Installer Logger/50KTL-M0(SiteA) 2025-02-01 07:30:00                0.0                     0.0                 0.0             207334.86                       11.5                 0.00           0.0                        0.0       Standby: initializing
   Site A Installer Logger/50KTL-M0(SiteA) 2025-02-01 07:35:00                0.0                     0.0                 0.0             207334.86                       11.5                49.98           0.0                        0.0 Standby: detecting sunlight
```

## site_a/raw/site_a_2025-03.xlsx — 5 min

- Rows: 4,746
- Columns: 13
- Duplicate rows: 0

### Column profile

| Column | Data type | Missing | Unique |
|---|---|---:|---:|
| Site Name | object | 0.00% | 1 |
| Installer | object | 0.00% | 1 |
| Device Name | object | 0.00% | 1 |
| Start Date/Time | object | 0.00% | 4,746 |
| Active Power (kW) | float64 | 0.00% | 4,008 |
| Total Input Power (kW) | float64 | 0.00% | 4,037 |
| Daily Energy (kWh) | float64 | 0.00% | 3,719 |
| Total PV Yield (kWh) | float64 | 0.00% | 4,426 |
| Internal Temperature (°C) | float64 | 0.00% | 455 |
| Grid Frequency (Hz) | float64 | 0.00% | 25 |
| Power Factor | float64 | 0.00% | 17 |
| Conversion Efficiency (%) | float64 | 0.00% | 686 |
| Inverter Status | object | 0.00% | 7 |

### Date/time candidates

- **Start Date/Time**: 4,422/4,746 parseable values
  - Range: 2025-03-01 00:00:00 to 2025-03-30 00:00:00

### Sample records

```text
Site Name Installer            Device Name     Start Date/Time  Active Power (kW)  Total Input Power (kW)  Daily Energy (kWh)  Total PV Yield (kWh)  Internal Temperature (°C)  Grid Frequency (Hz)  Power Factor  Conversion Efficiency (%)             Inverter Status
   Site A Installer Logger/50KTL-M0(SiteA) 2025-03-01 00:00:00                0.0                     0.0                 0.0             212277.75                       13.6                 0.00           0.0                        0.0        Standby: no sunlight
   Site A Installer Logger/50KTL-M0(SiteA) 2025-03-01 07:10:00                0.0                     0.0                 0.0             212277.75                       12.5                 0.00           0.0                        0.0       Standby: initializing
   Site A Installer Logger/50KTL-M0(SiteA) 2025-03-01 07:15:00                0.0                     0.0                 0.0             212277.75                       12.5                49.98           0.0                        0.0 Standby: detecting sunlight
```

## site_a/raw/site_a_2025-04.xlsx — 5 min

- Rows: 5,167
- Columns: 13
- Duplicate rows: 0

### Column profile

| Column | Data type | Missing | Unique |
|---|---|---:|---:|
| Site Name | object | 0.00% | 1 |
| Installer | object | 0.00% | 1 |
| Device Name | object | 0.00% | 1 |
| Start Date/Time | object | 0.00% | 5,167 |
| Active Power (kW) | float64 | 0.00% | 4,437 |
| Total Input Power (kW) | float64 | 0.00% | 4,487 |
| Daily Energy (kWh) | float64 | 0.00% | 4,214 |
| Total PV Yield (kWh) | float64 | 0.00% | 4,857 |
| Internal Temperature (°C) | float64 | 0.00% | 476 |
| Grid Frequency (Hz) | float64 | 0.00% | 26 |
| Power Factor | float64 | 0.00% | 16 |
| Conversion Efficiency (%) | float64 | 0.00% | 668 |
| Inverter Status | object | 0.00% | 6 |

### Date/time candidates

- **Start Date/Time**: 5,167/5,167 parseable values
  - Range: 2025-04-01 00:00:00 to 2025-04-30 21:00:00

### Sample records

```text
Site Name Installer            Device Name         Start Date/Time  Active Power (kW)  Total Input Power (kW)  Daily Energy (kWh)  Total PV Yield (kWh)  Internal Temperature (°C)  Grid Frequency (Hz)  Power Factor  Conversion Efficiency (%)             Inverter Status
   Site A Installer Logger/50KTL-M0(SiteA) 2025-04-01 00:00:00 DST                0.0                     0.0                 0.0              218859.1                       19.0                 0.00           0.0                        0.0        Standby: no sunlight
   Site A Installer Logger/50KTL-M0(SiteA) 2025-04-01 07:00:00 DST                0.0                     0.0                 0.0              218859.1                       16.8                 0.00           0.0                        0.0       Standby: initializing
   Site A Installer Logger/50KTL-M0(SiteA) 2025-04-01 07:05:00 DST                0.0                     0.0                 0.0              218859.1                       16.8                50.04           0.0                        0.0 Standby: detecting sunlight
```

## site_a/raw/site_a_2025-05.xlsx — 5 min

- Rows: 5,864
- Columns: 13
- Duplicate rows: 0

### Column profile

| Column | Data type | Missing | Unique |
|---|---|---:|---:|
| Site Name | object | 0.00% | 1 |
| Installer | object | 0.00% | 1 |
| Device Name | object | 0.00% | 1 |
| Start Date/Time | object | 0.00% | 5,864 |
| Active Power (kW) | float64 | 0.00% | 4,886 |
| Total Input Power (kW) | float64 | 0.00% | 4,923 |
| Daily Energy (kWh) | float64 | 0.00% | 4,674 |
| Total PV Yield (kWh) | float64 | 0.00% | 5,461 |
| Internal Temperature (°C) | float64 | 0.00% | 464 |
| Grid Frequency (Hz) | float64 | 0.00% | 24 |
| Power Factor | float64 | 0.00% | 19 |
| Conversion Efficiency (%) | float64 | 0.00% | 688 |
| Inverter Status | object | 0.00% | 7 |

### Date/time candidates

- **Start Date/Time**: 5,864/5,864 parseable values
  - Range: 2025-05-01 00:00:00 to 2025-05-31 21:40:00

### Sample records

```text
Site Name Installer            Device Name         Start Date/Time  Active Power (kW)  Total Input Power (kW)  Daily Energy (kWh)  Total PV Yield (kWh)  Internal Temperature (°C)  Grid Frequency (Hz)  Power Factor  Conversion Efficiency (%)             Inverter Status
   Site A Installer Logger/50KTL-M0(SiteA) 2025-05-01 00:00:00 DST                0.0                     0.0                 0.0             227007.74                       27.3                 0.00           0.0                        0.0        Standby: no sunlight
   Site A Installer Logger/50KTL-M0(SiteA) 2025-05-01 06:00:00 DST                0.0                     0.0                 0.0             227007.74                       20.3                 0.00           0.0                        0.0       Standby: initializing
   Site A Installer Logger/50KTL-M0(SiteA) 2025-05-01 06:05:00 DST                0.0                     0.0                 0.0             227007.74                       20.3                49.98           0.0                        0.0 Standby: detecting sunlight
```

## site_a/raw/site_a_2025-06.xlsx — 5 min

- Rows: 5,966
- Columns: 13
- Duplicate rows: 0

### Column profile

| Column | Data type | Missing | Unique |
|---|---|---:|---:|
| Site Name | object | 0.00% | 1 |
| Installer | object | 0.00% | 1 |
| Device Name | object | 0.00% | 1 |
| Start Date/Time | object | 0.00% | 5,966 |
| Active Power (kW) | float64 | 0.00% | 5,186 |
| Total Input Power (kW) | float64 | 0.00% | 5,137 |
| Daily Energy (kWh) | float64 | 0.00% | 4,817 |
| Total PV Yield (kWh) | float64 | 0.00% | 5,636 |
| Internal Temperature (°C) | float64 | 0.00% | 422 |
| Grid Frequency (Hz) | float64 | 0.00% | 24 |
| Power Factor | float64 | 0.00% | 15 |
| Conversion Efficiency (%) | float64 | 0.00% | 693 |
| Inverter Status | object | 0.00% | 7 |

### Date/time candidates

- **Start Date/Time**: 5,966/5,966 parseable values
  - Range: 2025-06-01 00:00:00 to 2025-06-30 21:55:00

### Sample records

```text
Site Name Installer            Device Name         Start Date/Time  Active Power (kW)  Total Input Power (kW)  Daily Energy (kWh)  Total PV Yield (kWh)  Internal Temperature (°C)  Grid Frequency (Hz)  Power Factor  Conversion Efficiency (%)             Inverter Status
   Site A Installer Logger/50KTL-M0(SiteA) 2025-06-01 00:00:00 DST                0.0                     0.0                 0.0             235402.57                       29.7                 0.00           0.0                        0.0        Standby: no sunlight
   Site A Installer Logger/50KTL-M0(SiteA) 2025-06-01 05:30:00 DST                0.0                     0.0                 0.0             235402.57                       22.7                 0.00           0.0                        0.0       Standby: initializing
   Site A Installer Logger/50KTL-M0(SiteA) 2025-06-01 05:35:00 DST                0.0                     0.0                 0.0             235402.57                       22.5                50.02           0.0                        0.0 Standby: detecting sunlight
```

## site_a/raw/site_a_2025-07.xlsx — 5 min

- Rows: 6,112
- Columns: 13
- Duplicate rows: 0

### Column profile

| Column | Data type | Missing | Unique |
|---|---|---:|---:|
| Site Name | object | 0.00% | 1 |
| Installer | object | 0.00% | 1 |
| Device Name | object | 0.00% | 1 |
| Start Date/Time | object | 0.00% | 6,112 |
| Active Power (kW) | float64 | 0.00% | 5,158 |
| Total Input Power (kW) | float64 | 0.00% | 5,221 |
| Daily Energy (kWh) | float64 | 0.00% | 4,898 |
| Total PV Yield (kWh) | float64 | 0.00% | 5,673 |
| Internal Temperature (°C) | float64 | 0.00% | 441 |
| Grid Frequency (Hz) | float64 | 0.00% | 22 |
| Power Factor | float64 | 0.00% | 13 |
| Conversion Efficiency (%) | float64 | 0.00% | 697 |
| Inverter Status | object | 0.00% | 6 |

### Date/time candidates

- **Start Date/Time**: 6,112/6,112 parseable values
  - Range: 2025-07-01 00:00:00 to 2025-07-31 21:30:00

### Sample records

```text
Site Name Installer            Device Name         Start Date/Time  Active Power (kW)  Total Input Power (kW)  Daily Energy (kWh)  Total PV Yield (kWh)  Internal Temperature (°C)  Grid Frequency (Hz)  Power Factor  Conversion Efficiency (%)             Inverter Status
   Site A Installer Logger/50KTL-M0(SiteA) 2025-07-01 00:00:00 DST                0.0                     0.0                 0.0             246023.73                       37.0                 0.00           0.0                        0.0        Standby: no sunlight
   Site A Installer Logger/50KTL-M0(SiteA) 2025-07-01 05:25:00 DST                0.0                     0.0                 0.0             246023.73                       30.4                 0.00           0.0                        0.0       Standby: initializing
   Site A Installer Logger/50KTL-M0(SiteA) 2025-07-01 05:30:00 DST                0.0                     0.0                 0.0             246023.73                       30.2                50.01           0.0                        0.0 Standby: detecting sunlight
```

## site_a/raw/site_a_2025-08.xlsx — 5 min

- Rows: 5,659
- Columns: 13
- Duplicate rows: 0

### Column profile

| Column | Data type | Missing | Unique |
|---|---|---:|---:|
| Site Name | object | 0.00% | 1 |
| Installer | object | 0.00% | 1 |
| Device Name | object | 0.00% | 1 |
| Start Date/Time | object | 0.00% | 5,659 |
| Active Power (kW) | float64 | 0.00% | 4,819 |
| Total Input Power (kW) | float64 | 0.00% | 4,820 |
| Daily Energy (kWh) | float64 | 0.00% | 4,501 |
| Total PV Yield (kWh) | float64 | 0.00% | 5,205 |
| Internal Temperature (°C) | float64 | 0.00% | 457 |
| Grid Frequency (Hz) | float64 | 0.00% | 22 |
| Power Factor | float64 | 0.00% | 16 |
| Conversion Efficiency (%) | float64 | 0.00% | 646 |
| Inverter Status | object | 0.00% | 7 |

### Date/time candidates

- **Start Date/Time**: 5,659/5,659 parseable values
  - Range: 2025-08-01 00:00:00 to 2025-08-31 20:30:00

### Sample records

```text
Site Name Installer            Device Name         Start Date/Time  Active Power (kW)  Total Input Power (kW)  Daily Energy (kWh)  Total PV Yield (kWh)  Internal Temperature (°C)  Grid Frequency (Hz)  Power Factor  Conversion Efficiency (%)             Inverter Status
   Site A Installer Logger/50KTL-M0(SiteA) 2025-08-01 00:00:00 DST                0.0                     0.0                 0.0             255699.05                       30.9                 0.00           0.0                        0.0        Standby: no sunlight
   Site A Installer Logger/50KTL-M0(SiteA) 2025-08-01 05:55:00 DST                0.0                     0.0                 0.0             255699.05                       25.0                 0.00           0.0                        0.0       Standby: initializing
   Site A Installer Logger/50KTL-M0(SiteA) 2025-08-01 06:00:00 DST                0.0                     0.0                 0.0             255699.05                       25.0                50.01           0.0                        0.0 Standby: detecting sunlight
```

## site_a/raw/site_a_2025-09.xlsx — 5 min

- Rows: 4,814
- Columns: 13
- Duplicate rows: 0

### Column profile

| Column | Data type | Missing | Unique |
|---|---|---:|---:|
| Site Name | object | 0.00% | 1 |
| Installer | object | 0.00% | 1 |
| Device Name | object | 0.00% | 1 |
| Start Date/Time | object | 0.00% | 4,814 |
| Active Power (kW) | float64 | 0.00% | 4,192 |
| Total Input Power (kW) | float64 | 0.00% | 4,195 |
| Daily Energy (kWh) | float64 | 0.00% | 3,861 |
| Total PV Yield (kWh) | float64 | 0.00% | 4,509 |
| Internal Temperature (°C) | float64 | 0.00% | 456 |
| Grid Frequency (Hz) | float64 | 0.00% | 19 |
| Power Factor | float64 | 0.00% | 20 |
| Conversion Efficiency (%) | float64 | 0.00% | 653 |
| Inverter Status | object | 0.00% | 7 |

### Date/time candidates

- **Start Date/Time**: 4,814/4,814 parseable values
  - Range: 2025-09-01 00:00:00 to 2025-09-30 19:35:00

### Sample records

```text
Site Name Installer            Device Name         Start Date/Time  Active Power (kW)  Total Input Power (kW)  Daily Energy (kWh)  Total PV Yield (kWh)  Internal Temperature (°C)  Grid Frequency (Hz)  Power Factor  Conversion Efficiency (%)             Inverter Status
   Site A Installer Logger/50KTL-M0(SiteA) 2025-09-01 00:00:00 DST                0.0                     0.0                 0.0             265449.95                       27.6                 0.00           0.0                        0.0        Standby: no sunlight
   Site A Installer Logger/50KTL-M0(SiteA) 2025-09-01 06:35:00 DST                0.0                     0.0                 0.0             265449.95                       25.7                 0.00           0.0                        0.0       Standby: initializing
   Site A Installer Logger/50KTL-M0(SiteA) 2025-09-01 06:40:00 DST                0.0                     0.0                 0.0             265449.95                       25.7                49.98           0.0                        0.0 Standby: detecting sunlight
```

## site_a/raw/site_a_2025-10.xlsx — 5 min

- Rows: 4,388
- Columns: 13
- Duplicate rows: 0

### Column profile

| Column | Data type | Missing | Unique |
|---|---|---:|---:|
| Site Name | object | 0.00% | 1 |
| Installer | object | 0.00% | 1 |
| Device Name | object | 0.00% | 1 |
| Start Date/Time | object | 0.00% | 4,388 |
| Active Power (kW) | float64 | 0.00% | 3,715 |
| Total Input Power (kW) | float64 | 0.00% | 3,719 |
| Daily Energy (kWh) | float64 | 0.00% | 3,391 |
| Total PV Yield (kWh) | float64 | 0.00% | 4,030 |
| Internal Temperature (°C) | float64 | 0.00% | 423 |
| Grid Frequency (Hz) | float64 | 0.00% | 19 |
| Power Factor | float64 | 0.00% | 12 |
| Conversion Efficiency (%) | float64 | 0.00% | 644 |
| Inverter Status | object | 0.00% | 7 |

### Date/time candidates

- **Start Date/Time**: 3,578/4,388 parseable values
  - Range: 2025-10-01 00:00:00 to 2025-10-26 00:00:00

### Sample records

```text
Site Name Installer            Device Name         Start Date/Time  Active Power (kW)  Total Input Power (kW)  Daily Energy (kWh)  Total PV Yield (kWh)  Internal Temperature (°C)  Grid Frequency (Hz)  Power Factor  Conversion Efficiency (%)             Inverter Status
   Site A Installer Logger/50KTL-M0(SiteA) 2025-10-01 00:00:00 DST                0.0                     0.0                 0.0             273103.89                       22.1                 0.00           0.0                        0.0        Standby: no sunlight
   Site A Installer Logger/50KTL-M0(SiteA) 2025-10-01 07:10:00 DST                0.0                     0.0                 0.0             273103.89                       15.9                49.99           0.0                        0.0 Standby: detecting sunlight
   Site A Installer Logger/50KTL-M0(SiteA) 2025-10-01 07:15:00 DST                0.0                     0.0                 0.0             273103.89                       15.7                50.00           0.0                        0.0 Standby: detecting sunlight
```

## site_a/raw/site_a_2025-11.xlsx — 5 min

- Rows: 3,739
- Columns: 13
- Duplicate rows: 0

### Column profile

| Column | Data type | Missing | Unique |
|---|---|---:|---:|
| Site Name | object | 0.00% | 1 |
| Installer | object | 0.00% | 1 |
| Device Name | object | 0.00% | 1 |
| Start Date/Time | object | 0.00% | 3,739 |
| Active Power (kW) | float64 | 0.00% | 2,892 |
| Total Input Power (kW) | float64 | 0.00% | 2,922 |
| Daily Energy (kWh) | float64 | 0.00% | 2,415 |
| Total PV Yield (kWh) | float64 | 0.00% | 3,378 |
| Internal Temperature (°C) | float64 | 0.00% | 406 |
| Grid Frequency (Hz) | float64 | 0.00% | 16 |
| Power Factor | float64 | 0.00% | 16 |
| Conversion Efficiency (%) | float64 | 0.00% | 779 |
| Inverter Status | object | 0.00% | 5 |

### Date/time candidates

- **Start Date/Time**: 3,739/3,739 parseable values
  - Range: 2025-11-01 00:00:00 to 2025-11-30 17:15:00

### Sample records

```text
Site Name Installer            Device Name     Start Date/Time  Active Power (kW)  Total Input Power (kW)  Daily Energy (kWh)  Total PV Yield (kWh)  Internal Temperature (°C)  Grid Frequency (Hz)  Power Factor  Conversion Efficiency (%)             Inverter Status
   Site A Installer Logger/50KTL-M0(SiteA) 2025-11-01 00:00:00                0.0                     0.0                 0.0             278543.14                       20.1                 0.00           0.0                        0.0        Standby: no sunlight
   Site A Installer Logger/50KTL-M0(SiteA) 2025-11-01 06:45:00                0.0                     0.0                 0.0             278543.14                       15.7                 0.00           0.0                        0.0       Standby: initializing
   Site A Installer Logger/50KTL-M0(SiteA) 2025-11-01 06:50:00                0.0                     0.0                 0.0             278543.14                       15.5                50.03           0.0                        0.0 Standby: detecting sunlight
```

## site_a/raw/site_a_2025-12.xlsx — 5 min

- Rows: 3,645
- Columns: 13
- Duplicate rows: 0

### Column profile

| Column | Data type | Missing | Unique |
|---|---|---:|---:|
| Site Name | object | 0.00% | 1 |
| Installer | object | 0.00% | 1 |
| Device Name | object | 0.00% | 1 |
| Start Date/Time | object | 0.00% | 3,645 |
| Active Power (kW) | float64 | 0.00% | 2,816 |
| Total Input Power (kW) | float64 | 0.00% | 2,847 |
| Daily Energy (kWh) | float64 | 0.00% | 2,314 |
| Total PV Yield (kWh) | float64 | 0.00% | 3,264 |
| Internal Temperature (°C) | float64 | 0.00% | 369 |
| Grid Frequency (Hz) | float64 | 0.00% | 14 |
| Power Factor | float64 | 0.00% | 14 |
| Conversion Efficiency (%) | float64 | 0.00% | 784 |
| Inverter Status | object | 0.00% | 7 |

### Date/time candidates

- **Start Date/Time**: 3,645/3,645 parseable values
  - Range: 2025-12-01 00:00:00 to 2025-12-31 17:30:00

### Sample records

```text
Site Name Installer            Device Name     Start Date/Time  Active Power (kW)  Total Input Power (kW)  Daily Energy (kWh)  Total PV Yield (kWh)  Internal Temperature (°C)  Grid Frequency (Hz)  Power Factor  Conversion Efficiency (%)       Inverter Status
   Site A Installer Logger/50KTL-M0(SiteA) 2025-12-01 00:00:00                0.0                     0.0                 0.0              281010.4                       14.1                  0.0           0.0                        0.0  Standby: no sunlight
   Site A Installer Logger/50KTL-M0(SiteA) 2025-12-01 07:30:00                0.0                     0.0                 0.0              281010.4                       12.9                  0.0           0.0                        0.0 Standby: initializing
   Site A Installer Logger/50KTL-M0(SiteA) 2025-12-01 07:35:00                0.0                     0.0                 0.0              281010.4                       12.9                  0.0           0.0                        0.0 Standby: initializing
```

## site_a/raw/site_a_2026-01.xlsx — 5 min

- Rows: 4,081
- Columns: 13
- Duplicate rows: 0

### Column profile

| Column | Data type | Missing | Unique |
|---|---|---:|---:|
| Site Name | object | 0.00% | 1 |
| Installer | object | 0.00% | 1 |
| Device Name | object | 0.00% | 1 |
| Start Date/Time | object | 0.00% | 4,081 |
| Active Power (kW) | float64 | 0.00% | 2,922 |
| Total Input Power (kW) | float64 | 0.00% | 2,922 |
| Daily Energy (kWh) | float64 | 0.00% | 2,441 |
| Total PV Yield (kWh) | float64 | 0.00% | 3,359 |
| Internal Temperature (°C) | float64 | 0.00% | 362 |
| Grid Frequency (Hz) | float64 | 0.00% | 21 |
| Power Factor | float64 | 0.00% | 19 |
| Conversion Efficiency (%) | float64 | 0.00% | 750 |
| Inverter Status | object | 0.00% | 6 |

### Date/time candidates

- **Start Date/Time**: 4,081/4,081 parseable values
  - Range: 2026-01-01 00:00:00 to 2026-01-31 18:00:00

### Sample records

```text
Site Name Installer            Device Name     Start Date/Time  Active Power (kW)  Total Input Power (kW)  Daily Energy (kWh)  Total PV Yield (kWh)  Internal Temperature (°C)  Grid Frequency (Hz)  Power Factor  Conversion Efficiency (%)             Inverter Status
   Site A Installer Logger/50KTL-M0(SiteA) 2026-01-01 00:00:00                0.0                     0.0                 0.0             283432.18                        4.6                  0.0           0.0                        0.0        Standby: no sunlight
   Site A Installer Logger/50KTL-M0(SiteA) 2026-01-01 07:45:00                0.0                     0.0                 0.0             283432.18                        1.0                  0.0           0.0                        0.0       Standby: initializing
   Site A Installer Logger/50KTL-M0(SiteA) 2026-01-01 07:50:00                0.0                     0.0                 0.0             283432.18                        1.0                 50.0           0.0                        0.0 Standby: detecting sunlight
```

## site_a/raw/site_a_2026-02.xlsx — 5 min

- Rows: 3,767
- Columns: 13
- Duplicate rows: 0

### Column profile

| Column | Data type | Missing | Unique |
|---|---|---:|---:|
| Site Name | object | 0.00% | 1 |
| Installer | object | 0.00% | 1 |
| Device Name | object | 0.00% | 1 |
| Start Date/Time | object | 0.00% | 3,767 |
| Active Power (kW) | float64 | 0.00% | 2,990 |
| Total Input Power (kW) | float64 | 0.00% | 3,021 |
| Daily Energy (kWh) | float64 | 0.00% | 2,587 |
| Total PV Yield (kWh) | float64 | 0.00% | 3,412 |
| Internal Temperature (°C) | float64 | 0.00% | 455 |
| Grid Frequency (Hz) | float64 | 0.00% | 18 |
| Power Factor | float64 | 0.00% | 14 |
| Conversion Efficiency (%) | float64 | 0.00% | 799 |
| Inverter Status | object | 0.00% | 6 |

### Date/time candidates

- **Start Date/Time**: 3,767/3,767 parseable values
  - Range: 2026-02-01 00:00:00 to 2026-02-28 18:45:00

### Sample records

```text
Site Name Installer            Device Name     Start Date/Time  Active Power (kW)  Total Input Power (kW)  Daily Energy (kWh)  Total PV Yield (kWh)  Internal Temperature (°C)  Grid Frequency (Hz)  Power Factor  Conversion Efficiency (%)       Inverter Status
   Site A Installer Logger/50KTL-M0(SiteA) 2026-02-01 00:00:00                0.0                     0.0                 0.0             285981.33                        9.9                  0.0           0.0                        0.0  Standby: no sunlight
   Site A Installer Logger/50KTL-M0(SiteA) 2026-02-01 07:40:00                0.0                     0.0                 0.0             285981.33                        8.8                  0.0           0.0                        0.0 Standby: initializing
   Site A Installer Logger/50KTL-M0(SiteA) 2026-02-01 07:45:00                0.0                     0.0                 0.0             285981.33                        8.8                  0.0           0.0                        0.0 Standby: initializing
```

## site_a/raw/site_a_2026-03.xlsx — 5 min

- Rows: 4,750
- Columns: 13
- Duplicate rows: 0

### Column profile

| Column | Data type | Missing | Unique |
|---|---|---:|---:|
| Site Name | object | 0.00% | 1 |
| Installer | object | 0.00% | 1 |
| Device Name | object | 0.00% | 1 |
| Start Date/Time | object | 0.00% | 4,750 |
| Active Power (kW) | float64 | 0.00% | 4,152 |
| Total Input Power (kW) | float64 | 0.00% | 4,148 |
| Daily Energy (kWh) | float64 | 0.00% | 3,887 |
| Total PV Yield (kWh) | float64 | 0.00% | 4,446 |
| Internal Temperature (°C) | float64 | 0.00% | 496 |
| Grid Frequency (Hz) | float64 | 0.00% | 23 |
| Power Factor | float64 | 0.00% | 12 |
| Conversion Efficiency (%) | float64 | 0.00% | 605 |
| Inverter Status | object | 0.00% | 6 |

### Date/time candidates

- **Start Date/Time**: 4,266/4,750 parseable values
  - Range: 2026-03-01 00:00:00 to 2026-03-29 00:00:00

### Sample records

```text
Site Name Installer            Device Name     Start Date/Time  Active Power (kW)  Total Input Power (kW)  Daily Energy (kWh)  Total PV Yield (kWh)  Internal Temperature (°C)  Grid Frequency (Hz)  Power Factor  Conversion Efficiency (%)             Inverter Status
   Site A Installer Logger/50KTL-M0(SiteA) 2026-03-01 00:00:00                0.0                     0.0                 0.0             289125.36                        8.3                 0.00           0.0                        0.0        Standby: no sunlight
   Site A Installer Logger/50KTL-M0(SiteA) 2026-03-01 06:55:00                0.0                     0.0                 0.0             289125.36                        7.3                 0.00           0.0                        0.0       Standby: initializing
   Site A Installer Logger/50KTL-M0(SiteA) 2026-03-01 07:00:00                0.0                     0.0                 0.0             289125.36                        7.3                50.02           0.0                        0.0 Standby: detecting sunlight
```

## site_a/raw/site_a_2026-04.xlsx — 5 min

- Rows: 5,212
- Columns: 13
- Duplicate rows: 0

### Column profile

| Column | Data type | Missing | Unique |
|---|---|---:|---:|
| Site Name | object | 0.00% | 1 |
| Installer | object | 0.00% | 1 |
| Device Name | object | 0.00% | 1 |
| Start Date/Time | object | 0.00% | 5,212 |
| Active Power (kW) | float64 | 0.00% | 4,494 |
| Total Input Power (kW) | float64 | 0.00% | 4,546 |
| Daily Energy (kWh) | float64 | 0.00% | 4,283 |
| Total PV Yield (kWh) | float64 | 0.00% | 4,903 |
| Internal Temperature (°C) | float64 | 0.00% | 478 |
| Grid Frequency (Hz) | float64 | 0.00% | 25 |
| Power Factor | float64 | 0.00% | 14 |
| Conversion Efficiency (%) | float64 | 0.00% | 631 |
| Inverter Status | object | 0.00% | 7 |

### Date/time candidates

- **Start Date/Time**: 5,212/5,212 parseable values
  - Range: 2026-04-01 00:00:00 to 2026-04-30 20:55:00

### Sample records

```text
Site Name Installer            Device Name         Start Date/Time  Active Power (kW)  Total Input Power (kW)  Daily Energy (kWh)  Total PV Yield (kWh)  Internal Temperature (°C)  Grid Frequency (Hz)  Power Factor  Conversion Efficiency (%)             Inverter Status
   Site A Installer Logger/50KTL-M0(SiteA) 2026-04-01 00:00:00 DST                0.0                     0.0                 0.0             297039.25                       20.1                 0.00           0.0                        0.0        Standby: no sunlight
   Site A Installer Logger/50KTL-M0(SiteA) 2026-04-01 06:55:00 DST                0.0                     0.0                 0.0             297039.25                       15.7                 0.00           0.0                        0.0       Standby: initializing
   Site A Installer Logger/50KTL-M0(SiteA) 2026-04-01 07:00:00 DST                0.0                     0.0                 0.0             297039.25                       15.5                50.04           0.0                        0.0 Standby: detecting sunlight
```

## site_a/raw/site_a_2026-05.xlsx — 5 min

- Rows: 5,883
- Columns: 13
- Duplicate rows: 0

### Column profile

| Column | Data type | Missing | Unique |
|---|---|---:|---:|
| Site Name | object | 0.00% | 1 |
| Installer | object | 0.00% | 1 |
| Device Name | object | 0.00% | 1 |
| Start Date/Time | object | 0.00% | 5,883 |
| Active Power (kW) | float64 | 0.00% | 5,071 |
| Total Input Power (kW) | float64 | 0.00% | 5,119 |
| Daily Energy (kWh) | float64 | 0.00% | 4,784 |
| Total PV Yield (kWh) | float64 | 0.00% | 5,550 |
| Internal Temperature (°C) | float64 | 0.00% | 479 |
| Grid Frequency (Hz) | float64 | 0.00% | 20 |
| Power Factor | float64 | 0.00% | 19 |
| Conversion Efficiency (%) | float64 | 0.00% | 636 |
| Inverter Status | object | 0.00% | 6 |

### Date/time candidates

- **Start Date/Time**: 5,883/5,883 parseable values
  - Range: 2026-05-01 00:00:00 to 2026-05-31 21:35:00

### Sample records

```text
Site Name Installer            Device Name         Start Date/Time  Active Power (kW)  Total Input Power (kW)  Daily Energy (kWh)  Total PV Yield (kWh)  Internal Temperature (°C)  Grid Frequency (Hz)  Power Factor  Conversion Efficiency (%)             Inverter Status
   Site A Installer Logger/50KTL-M0(SiteA) 2026-05-01 00:00:00 DST                0.0                     0.0                 0.0             306118.15                       17.3                 0.00           0.0                        0.0        Standby: no sunlight
   Site A Installer Logger/50KTL-M0(SiteA) 2026-05-01 06:05:00 DST                0.0                     0.0                 0.0             306118.15                       14.9                 0.00           0.0                        0.0       Standby: initializing
   Site A Installer Logger/50KTL-M0(SiteA) 2026-05-01 06:10:00 DST                0.0                     0.0                 0.0             306118.15                       14.7                50.01           0.0                        0.0 Standby: detecting sunlight
```

## site_a/raw/site_a_2026-06.xlsx — 5 min

- Rows: 6,083
- Columns: 13
- Duplicate rows: 0

### Column profile

| Column | Data type | Missing | Unique |
|---|---|---:|---:|
| Site Name | object | 0.00% | 1 |
| Installer | object | 0.00% | 1 |
| Device Name | object | 0.00% | 1 |
| Start Date/Time | object | 0.00% | 6,083 |
| Active Power (kW) | float64 | 0.00% | 5,105 |
| Total Input Power (kW) | float64 | 0.00% | 5,152 |
| Daily Energy (kWh) | float64 | 0.00% | 4,809 |
| Total PV Yield (kWh) | float64 | 0.00% | 5,605 |
| Internal Temperature (°C) | float64 | 0.00% | 436 |
| Grid Frequency (Hz) | float64 | 0.00% | 22 |
| Power Factor | float64 | 0.00% | 15 |
| Conversion Efficiency (%) | float64 | 0.00% | 677 |
| Inverter Status | object | 0.00% | 7 |

### Date/time candidates

- **Start Date/Time**: 6,083/6,083 parseable values
  - Range: 2026-06-01 00:00:00 to 2026-06-30 21:50:00

### Sample records

```text
Site Name Installer            Device Name         Start Date/Time  Active Power (kW)  Total Input Power (kW)  Daily Energy (kWh)  Total PV Yield (kWh)  Internal Temperature (°C)  Grid Frequency (Hz)  Power Factor  Conversion Efficiency (%)             Inverter Status
   Site A Installer Logger/50KTL-M0(SiteA) 2026-06-01 00:00:00 DST                0.0                     0.0                 0.0             316069.51                       30.2                 0.00           0.0                        0.0        Standby: no sunlight
   Site A Installer Logger/50KTL-M0(SiteA) 2026-06-01 05:30:00 DST                0.0                     0.0                 0.0             316069.51                       24.2                 0.00           0.0                        0.0       Standby: initializing
   Site A Installer Logger/50KTL-M0(SiteA) 2026-06-01 05:35:00 DST                0.0                     0.0                 0.0             316069.51                       24.2                49.99           0.0                        0.0 Standby: detecting sunlight
```

## site_a/site_a_hourly_weather.csv

- Rows: 13,031
- Columns: 23
- Duplicate rows: 0

### Column profile

| Column | Data type | Missing | Unique |
|---|---|---:|---:|
| datetime_utc | object | 0.00% | 13,031 |
| datetime_local | object | 0.00% | 13,031 |
| active_power_kw | float64 | 2.00% | 6,938 |
| dc_input_power_kw | float64 | 37.81% | 6,948 |
| daily_energy_kwh | float64 | 37.81% | 5,728 |
| cumulative_energy_kwh | float64 | 37.81% | 7,119 |
| inverter_temp_c | float64 | 37.81% | 3,654 |
| grid_freq_hz | float64 | 37.81% | 460 |
| power_factor | float64 | 37.81% | 425 |
| efficiency_pct | float64 | 37.81% | 3,409 |
| inverter_status | object | 37.81% | 7 |
| is_generating | float64 | 2.00% | 2 |
| temp_c | float64 | 2.01% | 451 |
| humidity_pct | float64 | 2.01% | 81 |
| cloud_cover_pct | float64 | 2.01% | 101 |
| wind_speed_kmh | float64 | 2.01% | 238 |
| ghi_wm2 | float64 | 2.01% | 905 |
| dni_wm2 | float64 | 2.01% | 4,231 |
| dhi_wm2 | float64 | 2.01% | 363 |
| precip_mm | float64 | 2.01% | 61 |
| solar_elevation_deg | float64 | 0.00% | 6,575 |
| solar_azimuth_deg | float64 | 0.00% | 13,000 |
| capacity_factor | float64 | 2.00% | 4,241 |

### Date/time candidates

- **datetime_utc**: 13,031/13,031 parseable values
  - Range: 2025-01-03 22:00:00 to 2026-06-30 20:00:00
- **datetime_local**: 13,031/13,031 parseable values
  - Range: 2025-01-04 00:00:00+02:00 to 2026-06-30 23:00:00+03:00

### Sample records

```text
       datetime_utc           datetime_local  active_power_kw  dc_input_power_kw  daily_energy_kwh  cumulative_energy_kwh  inverter_temp_c  grid_freq_hz  power_factor  efficiency_pct inverter_status  is_generating  temp_c  humidity_pct  cloud_cover_pct  wind_speed_kmh  ghi_wm2  dni_wm2  dhi_wm2  precip_mm  solar_elevation_deg  solar_azimuth_deg  capacity_factor
2025-01-03 22:00:00 2025-01-04 00:00:00+0200              0.0                NaN               NaN                    NaN              NaN           NaN           NaN             NaN             NaN            0.0     NaN           NaN              NaN             NaN      NaN      NaN      NaN        NaN                  0.0           359.0225              0.0
2025-01-03 23:00:00 2025-01-04 01:00:00+0200              0.0                NaN               NaN                    NaN              NaN           NaN           NaN             NaN             NaN            0.0     0.1          68.0             73.0             8.7      0.0      0.0      0.0        0.0                  0.0            32.9826              0.0
2025-01-04 00:00:00 2025-01-04 02:00:00+0200              0.0                NaN               NaN                    NaN              NaN           NaN           NaN             NaN             NaN            0.0     0.6          63.0             46.0             9.1      0.0      0.0      0.0        0.0                  0.0            57.1433              0.0
```

## site_b/raw/site_b_2025-05.xlsx — 5 min

- Rows: 5,874
- Columns: 13
- Duplicate rows: 0

### Column profile

| Column | Data type | Missing | Unique |
|---|---|---:|---:|
| Site Name | object | 0.00% | 1 |
| Installer | object | 0.00% | 1 |
| Device Name | object | 0.00% | 1 |
| Start Date/Time | object | 0.00% | 5,874 |
| Active Power (kW) | float64 | 0.00% | 4,858 |
| Total Input Power (kW) | float64 | 0.00% | 4,868 |
| Daily Energy (kWh) | float64 | 0.00% | 4,666 |
| Total PV Yield (kWh) | float64 | 0.00% | 5,428 |
| Internal Temperature (°C) | float64 | 0.00% | 404 |
| Grid Frequency (Hz) | float64 | 0.00% | 23 |
| Power Factor | float64 | 0.00% | 17 |
| Conversion Efficiency (%) | float64 | 0.00% | 663 |
| Inverter Status | object | 0.00% | 8 |

### Date/time candidates

- **Start Date/Time**: 5,874/5,874 parseable values
  - Range: 2025-05-01 00:00:00 to 2025-05-31 21:40:00

### Sample records

```text
Site Name Installer          Device Name         Start Date/Time  Active Power (kW)  Total Input Power (kW)  Daily Energy (kWh)  Total PV Yield (kWh)  Internal Temperature (°C)  Grid Frequency (Hz)  Power Factor  Conversion Efficiency (%)             Inverter Status
   Site B Installer Logger/50K-M0(SiteB) 2025-05-01 00:00:00 DST                0.0                     0.0                 0.0             190913.34                       25.7                 0.00           0.0                        0.0        Standby: no sunlight
   Site B Installer Logger/50K-M0(SiteB) 2025-05-01 06:00:00 DST                0.0                     0.0                 0.0             190913.34                       20.3                 0.00           0.0                        0.0       Standby: initializing
   Site B Installer Logger/50K-M0(SiteB) 2025-05-01 06:05:00 DST                0.0                     0.0                 0.0             190913.34                       20.1                49.98           0.0                        0.0 Standby: detecting sunlight
```

## site_b/raw/site_b_2025-06.xlsx — 5 min

- Rows: 5,975
- Columns: 13
- Duplicate rows: 0

### Column profile

| Column | Data type | Missing | Unique |
|---|---|---:|---:|
| Site Name | object | 0.00% | 1 |
| Installer | object | 0.00% | 1 |
| Device Name | object | 0.00% | 1 |
| Start Date/Time | object | 0.00% | 5,975 |
| Active Power (kW) | float64 | 0.00% | 5,135 |
| Total Input Power (kW) | float64 | 0.00% | 5,138 |
| Daily Energy (kWh) | float64 | 0.00% | 4,831 |
| Total PV Yield (kWh) | float64 | 0.00% | 5,633 |
| Internal Temperature (°C) | float64 | 0.00% | 384 |
| Grid Frequency (Hz) | float64 | 0.00% | 21 |
| Power Factor | float64 | 0.00% | 21 |
| Conversion Efficiency (%) | float64 | 0.00% | 638 |
| Inverter Status | object | 0.00% | 7 |

### Date/time candidates

- **Start Date/Time**: 5,975/5,975 parseable values
  - Range: 2025-06-01 00:00:00 to 2025-06-30 21:55:00

### Sample records

```text
Site Name Installer          Device Name         Start Date/Time  Active Power (kW)  Total Input Power (kW)  Daily Energy (kWh)  Total PV Yield (kWh)  Internal Temperature (°C)  Grid Frequency (Hz)  Power Factor  Conversion Efficiency (%)       Inverter Status
   Site B Installer Logger/50K-M0(SiteB) 2025-06-01 00:00:00 DST                0.0                     0.0                 0.0             199035.88                       26.9                  0.0           0.0                        0.0  Standby: no sunlight
   Site B Installer Logger/50K-M0(SiteB) 2025-06-01 05:25:00 DST                0.0                     0.0                 0.0             199035.88                       22.1                  0.0           0.0                        0.0 Standby: initializing
   Site B Installer Logger/50K-M0(SiteB) 2025-06-01 05:30:00 DST                0.0                     0.0                 0.0             199035.88                       21.9                  0.0           0.0                        0.0 Standby: initializing
```

## site_b/raw/site_b_2025-07.xlsx — 5 min

- Rows: 6,030
- Columns: 13
- Duplicate rows: 0

### Column profile

| Column | Data type | Missing | Unique |
|---|---|---:|---:|
| Site Name | object | 0.00% | 1 |
| Installer | object | 0.00% | 1 |
| Device Name | object | 0.00% | 1 |
| Start Date/Time | object | 0.00% | 6,030 |
| Active Power (kW) | float64 | 0.00% | 5,167 |
| Total Input Power (kW) | float64 | 0.00% | 5,154 |
| Daily Energy (kWh) | float64 | 0.00% | 4,829 |
| Total PV Yield (kWh) | float64 | 0.00% | 5,641 |
| Internal Temperature (°C) | float64 | 0.00% | 404 |
| Grid Frequency (Hz) | float64 | 0.00% | 22 |
| Power Factor | float64 | 0.00% | 19 |
| Conversion Efficiency (%) | float64 | 0.00% | 641 |
| Inverter Status | object | 0.00% | 8 |

### Date/time candidates

- **Start Date/Time**: 6,030/6,030 parseable values
  - Range: 2025-07-01 00:00:00 to 2025-07-31 21:30:00

### Sample records

```text
Site Name Installer          Device Name         Start Date/Time  Active Power (kW)  Total Input Power (kW)  Daily Energy (kWh)  Total PV Yield (kWh)  Internal Temperature (°C)  Grid Frequency (Hz)  Power Factor  Conversion Efficiency (%)             Inverter Status
   Site B Installer Logger/50K-M0(SiteB) 2025-07-01 00:00:00 DST                0.0                     0.0                 0.0              209681.1                       35.3                 0.00           0.0                        0.0        Standby: no sunlight
   Site B Installer Logger/50K-M0(SiteB) 2025-07-01 05:25:00 DST                0.0                     0.0                 0.0              209681.1                       29.8                 0.00           0.0                        0.0       Standby: initializing
   Site B Installer Logger/50K-M0(SiteB) 2025-07-01 05:30:00 DST                0.0                     0.0                 0.0              209681.1                       29.8                50.01           0.0                        0.0 Standby: detecting sunlight
```

## site_b/raw/site_b_2025-08.xlsx — 5 min

- Rows: 5,575
- Columns: 13
- Duplicate rows: 0

### Column profile

| Column | Data type | Missing | Unique |
|---|---|---:|---:|
| Site Name | object | 0.00% | 1 |
| Installer | object | 0.00% | 1 |
| Device Name | object | 0.00% | 1 |
| Start Date/Time | object | 0.00% | 5,575 |
| Active Power (kW) | float64 | 0.00% | 4,871 |
| Total Input Power (kW) | float64 | 0.00% | 4,843 |
| Daily Energy (kWh) | float64 | 0.00% | 4,516 |
| Total PV Yield (kWh) | float64 | 0.00% | 5,256 |
| Internal Temperature (°C) | float64 | 0.00% | 424 |
| Grid Frequency (Hz) | float64 | 0.00% | 20 |
| Power Factor | float64 | 0.00% | 22 |
| Conversion Efficiency (%) | float64 | 0.00% | 607 |
| Inverter Status | object | 0.00% | 7 |

### Date/time candidates

- **Start Date/Time**: 5,575/5,575 parseable values
  - Range: 2025-08-01 05:40:00 to 2025-08-31 20:30:00

### Sample records

```text
Site Name Installer          Device Name         Start Date/Time  Active Power (kW)  Total Input Power (kW)  Daily Energy (kWh)  Total PV Yield (kWh)  Internal Temperature (°C)  Grid Frequency (Hz)  Power Factor  Conversion Efficiency (%)      Inverter Status
   Site B Installer Logger/50K-M0(SiteB) 2025-08-01 05:40:00 DST                0.0                     0.0                 0.0                   0.0                       24.9                  0.0           0.0                        0.0 Standby: no sunlight
   Site B Installer Logger/50K-M0(SiteB) 2025-08-01 05:45:00 DST                0.0                     0.0                 0.0                   0.0                       24.8                  0.0           0.0                        0.0 Standby: no sunlight
   Site B Installer Logger/50K-M0(SiteB) 2025-08-01 05:50:00 DST                0.0                     0.0                 0.0                   0.0                       24.8                  0.0           0.0                        0.0 Standby: no sunlight
```

## site_b/raw/site_b_2025-09.xlsx — 5 min

- Rows: 4,817
- Columns: 13
- Duplicate rows: 0

### Column profile

| Column | Data type | Missing | Unique |
|---|---|---:|---:|
| Site Name | object | 0.00% | 1 |
| Installer | object | 0.00% | 1 |
| Device Name | object | 0.00% | 1 |
| Start Date/Time | object | 0.00% | 4,817 |
| Active Power (kW) | float64 | 0.00% | 4,162 |
| Total Input Power (kW) | float64 | 0.00% | 4,202 |
| Daily Energy (kWh) | float64 | 0.00% | 3,816 |
| Total PV Yield (kWh) | float64 | 0.00% | 4,516 |
| Internal Temperature (°C) | float64 | 0.00% | 414 |
| Grid Frequency (Hz) | float64 | 0.00% | 19 |
| Power Factor | float64 | 0.00% | 18 |
| Conversion Efficiency (%) | float64 | 0.00% | 602 |
| Inverter Status | object | 0.00% | 8 |

### Date/time candidates

- **Start Date/Time**: 4,817/4,817 parseable values
  - Range: 2025-09-01 00:00:00 to 2025-09-30 19:35:00

### Sample records

```text
Site Name Installer          Device Name         Start Date/Time  Active Power (kW)  Total Input Power (kW)  Daily Energy (kWh)  Total PV Yield (kWh)  Internal Temperature (°C)  Grid Frequency (Hz)  Power Factor  Conversion Efficiency (%)             Inverter Status
   Site B Installer Logger/50K-M0(SiteB) 2025-09-01 00:00:00 DST                0.0                     0.0                 0.0             228593.58                       27.2                 0.00           0.0                        0.0        Standby: no sunlight
   Site B Installer Logger/50K-M0(SiteB) 2025-09-01 06:35:00 DST                0.0                     0.0                 0.0             228593.58                       25.8                 0.00           0.0                        0.0       Standby: initializing
   Site B Installer Logger/50K-M0(SiteB) 2025-09-01 06:40:00 DST                0.0                     0.0                 0.0             228593.58                       25.6                49.98           0.0                        0.0 Standby: detecting sunlight
```

## site_b/raw/site_b_2025-10.xlsx — 5 min

- Rows: 4,395
- Columns: 13
- Duplicate rows: 0

### Column profile

| Column | Data type | Missing | Unique |
|---|---|---:|---:|
| Site Name | object | 0.00% | 1 |
| Installer | object | 0.00% | 1 |
| Device Name | object | 0.00% | 1 |
| Start Date/Time | object | 0.00% | 4,395 |
| Active Power (kW) | float64 | 0.00% | 3,744 |
| Total Input Power (kW) | float64 | 0.00% | 3,750 |
| Daily Energy (kWh) | float64 | 0.00% | 3,383 |
| Total PV Yield (kWh) | float64 | 0.00% | 4,061 |
| Internal Temperature (°C) | float64 | 0.00% | 333 |
| Grid Frequency (Hz) | float64 | 0.00% | 18 |
| Power Factor | float64 | 0.00% | 17 |
| Conversion Efficiency (%) | float64 | 0.00% | 643 |
| Inverter Status | object | 0.00% | 6 |

### Date/time candidates

- **Start Date/Time**: 3,584/4,395 parseable values
  - Range: 2025-10-01 00:00:00 to 2025-10-26 00:00:00

### Sample records

```text
Site Name Installer          Device Name         Start Date/Time  Active Power (kW)  Total Input Power (kW)  Daily Energy (kWh)  Total PV Yield (kWh)  Internal Temperature (°C)  Grid Frequency (Hz)  Power Factor  Conversion Efficiency (%)             Inverter Status
   Site B Installer Logger/50K-M0(SiteB) 2025-10-01 00:00:00 DST                0.0                     0.0                 0.0             235848.34                       20.2                 0.00           0.0                        0.0        Standby: no sunlight
   Site B Installer Logger/50K-M0(SiteB) 2025-10-01 07:10:00 DST                0.0                     0.0                 0.0             235848.34                       16.0                 0.00           0.0                        0.0       Standby: initializing
   Site B Installer Logger/50K-M0(SiteB) 2025-10-01 07:15:00 DST                0.0                     0.0                 0.0             235848.34                       15.8                50.02           0.0                        0.0 Standby: detecting sunlight
```

## site_b/raw/site_b_2025-11.xlsx — 5 min

- Rows: 3,925
- Columns: 13
- Duplicate rows: 0

### Column profile

| Column | Data type | Missing | Unique |
|---|---|---:|---:|
| Site Name | object | 0.00% | 1 |
| Installer | object | 0.00% | 1 |
| Device Name | object | 0.00% | 1 |
| Start Date/Time | object | 0.00% | 3,925 |
| Active Power (kW) | float64 | 0.00% | 2,915 |
| Total Input Power (kW) | float64 | 0.00% | 2,942 |
| Daily Energy (kWh) | float64 | 0.00% | 2,392 |
| Total PV Yield (kWh) | float64 | 0.00% | 3,380 |
| Internal Temperature (°C) | float64 | 0.00% | 322 |
| Grid Frequency (Hz) | float64 | 0.00% | 16 |
| Power Factor | float64 | 0.00% | 18 |
| Conversion Efficiency (%) | float64 | 0.00% | 720 |
| Inverter Status | object | 0.00% | 7 |

### Date/time candidates

- **Start Date/Time**: 3,925/3,925 parseable values
  - Range: 2025-11-01 00:00:00 to 2025-11-30 17:20:00

### Sample records

```text
Site Name Installer          Device Name     Start Date/Time  Active Power (kW)  Total Input Power (kW)  Daily Energy (kWh)  Total PV Yield (kWh)  Internal Temperature (°C)  Grid Frequency (Hz)  Power Factor  Conversion Efficiency (%)             Inverter Status
   Site B Installer Logger/50K-M0(SiteB) 2025-11-01 00:00:00                0.0                     0.0                 0.0             241076.77                       19.3                 0.00           0.0                        0.0        Standby: no sunlight
   Site B Installer Logger/50K-M0(SiteB) 2025-11-01 06:45:00                0.0                     0.0                 0.0             241076.77                       15.9                 0.00           0.0                        0.0       Standby: initializing
   Site B Installer Logger/50K-M0(SiteB) 2025-11-01 06:50:00                0.0                     0.0                 0.0             241076.77                       15.9                50.03           0.0                        0.0 Standby: detecting sunlight
```

## site_b/raw/site_b_2025-12.xlsx — 5 min

- Rows: 3,648
- Columns: 13
- Duplicate rows: 0

### Column profile

| Column | Data type | Missing | Unique |
|---|---|---:|---:|
| Site Name | object | 0.00% | 1 |
| Installer | object | 0.00% | 1 |
| Device Name | object | 0.00% | 1 |
| Start Date/Time | object | 0.00% | 3,648 |
| Active Power (kW) | float64 | 0.00% | 2,799 |
| Total Input Power (kW) | float64 | 0.00% | 2,820 |
| Daily Energy (kWh) | float64 | 0.00% | 2,287 |
| Total PV Yield (kWh) | float64 | 0.00% | 3,244 |
| Internal Temperature (°C) | float64 | 0.00% | 269 |
| Grid Frequency (Hz) | float64 | 0.00% | 14 |
| Power Factor | float64 | 0.00% | 25 |
| Conversion Efficiency (%) | float64 | 0.00% | 755 |
| Inverter Status | object | 0.00% | 6 |

### Date/time candidates

- **Start Date/Time**: 3,648/3,648 parseable values
  - Range: 2025-12-01 00:00:00 to 2025-12-31 17:30:00

### Sample records

```text
Site Name Installer          Device Name     Start Date/Time  Active Power (kW)  Total Input Power (kW)  Daily Energy (kWh)  Total PV Yield (kWh)  Internal Temperature (°C)  Grid Frequency (Hz)  Power Factor  Conversion Efficiency (%)       Inverter Status
   Site B Installer Logger/50K-M0(SiteB) 2025-12-01 00:00:00                0.0                     0.0                 0.0             243322.25                       15.9                  0.0           0.0                        0.0  Standby: no sunlight
   Site B Installer Logger/50K-M0(SiteB) 2025-12-01 07:30:00                0.0                     0.0                 0.0             243322.25                       14.5                  0.0           0.0                        0.0 Standby: initializing
   Site B Installer Logger/50K-M0(SiteB) 2025-12-01 07:35:00                0.0                     0.0                 0.0             243322.25                       14.5                  0.0           0.0                        0.0 Standby: initializing
```

## site_b/raw/site_b_2026-01.xlsx — 5 min

- Rows: 3,753
- Columns: 13
- Duplicate rows: 0

### Column profile

| Column | Data type | Missing | Unique |
|---|---|---:|---:|
| Site Name | object | 0.00% | 1 |
| Installer | object | 0.00% | 1 |
| Device Name | object | 0.00% | 1 |
| Start Date/Time | object | 0.00% | 3,753 |
| Active Power (kW) | float64 | 0.00% | 2,876 |
| Total Input Power (kW) | float64 | 0.00% | 2,859 |
| Daily Energy (kWh) | float64 | 0.00% | 2,351 |
| Total PV Yield (kWh) | float64 | 0.00% | 3,338 |
| Internal Temperature (°C) | float64 | 0.00% | 264 |
| Grid Frequency (Hz) | float64 | 0.00% | 21 |
| Power Factor | float64 | 0.00% | 13 |
| Conversion Efficiency (%) | float64 | 0.00% | 758 |
| Inverter Status | object | 0.00% | 6 |

### Date/time candidates

- **Start Date/Time**: 3,753/3,753 parseable values
  - Range: 2026-01-01 00:00:00 to 2026-01-31 18:00:00

### Sample records

```text
Site Name Installer          Device Name     Start Date/Time  Active Power (kW)  Total Input Power (kW)  Daily Energy (kWh)  Total PV Yield (kWh)  Internal Temperature (°C)  Grid Frequency (Hz)  Power Factor  Conversion Efficiency (%)             Inverter Status
   Site B Installer Logger/50K-M0(SiteB) 2026-01-01 00:00:00                0.0                     0.0                 0.0             245358.24                        4.8                  0.0           0.0                        0.0        Standby: no sunlight
   Site B Installer Logger/50K-M0(SiteB) 2026-01-01 07:45:00                0.0                     0.0                 0.0             245358.24                        2.8                  0.0           0.0                        0.0       Standby: initializing
   Site B Installer Logger/50K-M0(SiteB) 2026-01-01 07:50:00                0.0                     0.0                 0.0             245358.24                        2.8                 50.0           0.0                        0.0 Standby: detecting sunlight
```

## site_b/raw/site_b_2026-02.xlsx — 5 min

- Rows: 3,760
- Columns: 13
- Duplicate rows: 0

### Column profile

| Column | Data type | Missing | Unique |
|---|---|---:|---:|
| Site Name | object | 0.00% | 1 |
| Installer | object | 0.00% | 1 |
| Device Name | object | 0.00% | 1 |
| Start Date/Time | object | 0.00% | 3,760 |
| Active Power (kW) | float64 | 0.00% | 2,931 |
| Total Input Power (kW) | float64 | 0.00% | 2,928 |
| Daily Energy (kWh) | float64 | 0.00% | 2,475 |
| Total PV Yield (kWh) | float64 | 0.00% | 3,393 |
| Internal Temperature (°C) | float64 | 0.00% | 323 |
| Grid Frequency (Hz) | float64 | 0.00% | 18 |
| Power Factor | float64 | 0.00% | 22 |
| Conversion Efficiency (%) | float64 | 0.00% | 773 |
| Inverter Status | object | 0.00% | 8 |

### Date/time candidates

- **Start Date/Time**: 3,760/3,760 parseable values
  - Range: 2026-02-01 00:00:00 to 2026-02-28 18:45:00

### Sample records

```text
Site Name Installer          Device Name     Start Date/Time  Active Power (kW)  Total Input Power (kW)  Daily Energy (kWh)  Total PV Yield (kWh)  Internal Temperature (°C)  Grid Frequency (Hz)  Power Factor  Conversion Efficiency (%)       Inverter Status
   Site B Installer Logger/50K-M0(SiteB) 2026-02-01 00:00:00                0.0                     0.0                 0.0             247427.69                       11.0                  0.0           0.0                        0.0  Standby: no sunlight
   Site B Installer Logger/50K-M0(SiteB) 2026-02-01 07:45:00                0.0                     0.0                 0.0             247427.69                       10.6                  0.0           0.0                        0.0 Standby: initializing
   Site B Installer Logger/50K-M0(SiteB) 2026-02-01 07:50:00                0.0                     0.0                 0.0             247427.69                       10.6                  0.0           0.0                        0.0 Standby: initializing
```

## site_b/raw/site_b_2026-03.xlsx — 5 min

- Rows: 4,753
- Columns: 13
- Duplicate rows: 0

### Column profile

| Column | Data type | Missing | Unique |
|---|---|---:|---:|
| Site Name | object | 0.00% | 1 |
| Installer | object | 0.00% | 1 |
| Device Name | object | 0.00% | 1 |
| Start Date/Time | object | 0.00% | 4,753 |
| Active Power (kW) | float64 | 0.00% | 4,136 |
| Total Input Power (kW) | float64 | 0.00% | 4,179 |
| Daily Energy (kWh) | float64 | 0.00% | 3,838 |
| Total PV Yield (kWh) | float64 | 0.00% | 4,438 |
| Internal Temperature (°C) | float64 | 0.00% | 394 |
| Grid Frequency (Hz) | float64 | 0.00% | 23 |
| Power Factor | float64 | 0.00% | 20 |
| Conversion Efficiency (%) | float64 | 0.00% | 577 |
| Inverter Status | object | 0.00% | 7 |

### Date/time candidates

- **Start Date/Time**: 4,269/4,753 parseable values
  - Range: 2026-03-01 00:00:00 to 2026-03-29 00:00:00

### Sample records

```text
Site Name Installer          Device Name     Start Date/Time  Active Power (kW)  Total Input Power (kW)  Daily Energy (kWh)  Total PV Yield (kWh)  Internal Temperature (°C)  Grid Frequency (Hz)  Power Factor  Conversion Efficiency (%)             Inverter Status
   Site B Installer Logger/50K-M0(SiteB) 2026-03-01 00:00:00                0.0                     0.0                 0.0             250171.47                        9.1                 0.00           0.0                        0.0        Standby: no sunlight
   Site B Installer Logger/50K-M0(SiteB) 2026-03-01 06:55:00                0.0                     0.0                 0.0             250171.47                        8.5                 0.00           0.0                        0.0       Standby: initializing
   Site B Installer Logger/50K-M0(SiteB) 2026-03-01 07:00:00                0.0                     0.0                 0.0             250171.47                        8.3                50.01           0.0                        0.0 Standby: detecting sunlight
```

## site_b/raw/site_b_2026-04.xlsx — 5 min

- Rows: 5,194
- Columns: 13
- Duplicate rows: 0

### Column profile

| Column | Data type | Missing | Unique |
|---|---|---:|---:|
| Site Name | object | 0.00% | 1 |
| Installer | object | 0.00% | 1 |
| Device Name | object | 0.00% | 1 |
| Start Date/Time | object | 0.00% | 5,194 |
| Active Power (kW) | float64 | 0.00% | 4,541 |
| Total Input Power (kW) | float64 | 0.00% | 4,551 |
| Daily Energy (kWh) | float64 | 0.00% | 4,280 |
| Total PV Yield (kWh) | float64 | 0.00% | 4,894 |
| Internal Temperature (°C) | float64 | 0.00% | 415 |
| Grid Frequency (Hz) | float64 | 0.00% | 23 |
| Power Factor | float64 | 0.00% | 17 |
| Conversion Efficiency (%) | float64 | 0.00% | 613 |
| Inverter Status | object | 0.00% | 5 |

### Date/time candidates

- **Start Date/Time**: 5,194/5,194 parseable values
  - Range: 2026-04-01 00:00:00 to 2026-04-30 21:00:00

### Sample records

```text
Site Name Installer          Device Name         Start Date/Time  Active Power (kW)  Total Input Power (kW)  Daily Energy (kWh)  Total PV Yield (kWh)  Internal Temperature (°C)  Grid Frequency (Hz)  Power Factor  Conversion Efficiency (%)             Inverter Status
   Site B Installer Logger/50K-M0(SiteB) 2026-04-01 00:00:00 DST                0.0                     0.0                 0.0             257415.68                       16.8                 0.00           0.0                        0.0        Standby: no sunlight
   Site B Installer Logger/50K-M0(SiteB) 2026-04-01 06:50:00 DST                0.0                     0.0                 0.0             257415.68                       15.8                 0.00           0.0                        0.0       Standby: initializing
   Site B Installer Logger/50K-M0(SiteB) 2026-04-01 06:55:00 DST                0.0                     0.0                 0.0             257415.68                       15.8                49.98           0.0                        0.0 Standby: detecting sunlight
```

## site_b/raw/site_b_2026-05.xlsx — 5 min

- Rows: 5,981
- Columns: 13
- Duplicate rows: 0

### Column profile

| Column | Data type | Missing | Unique |
|---|---|---:|---:|
| Site Name | object | 0.00% | 1 |
| Installer | object | 0.00% | 1 |
| Device Name | object | 0.00% | 1 |
| Start Date/Time | object | 0.00% | 5,981 |
| Active Power (kW) | float64 | 0.00% | 5,089 |
| Total Input Power (kW) | float64 | 0.00% | 5,088 |
| Daily Energy (kWh) | float64 | 0.00% | 4,775 |
| Total PV Yield (kWh) | float64 | 0.00% | 5,534 |
| Internal Temperature (°C) | float64 | 0.00% | 438 |
| Grid Frequency (Hz) | float64 | 0.00% | 20 |
| Power Factor | float64 | 0.00% | 21 |
| Conversion Efficiency (%) | float64 | 0.00% | 612 |
| Inverter Status | object | 0.00% | 7 |

### Date/time candidates

- **Start Date/Time**: 5,981/5,981 parseable values
  - Range: 2026-05-01 00:00:00 to 2026-05-31 21:40:00

### Sample records

```text
Site Name Installer          Device Name         Start Date/Time  Active Power (kW)  Total Input Power (kW)  Daily Energy (kWh)  Total PV Yield (kWh)  Internal Temperature (°C)  Grid Frequency (Hz)  Power Factor  Conversion Efficiency (%)             Inverter Status
   Site B Installer Logger/50K-M0(SiteB) 2026-05-01 00:00:00 DST                0.0                     0.0                 0.0             266065.41                       17.0                 0.00           0.0                        0.0        Standby: no sunlight
   Site B Installer Logger/50K-M0(SiteB) 2026-05-01 06:05:00 DST                0.0                     0.0                 0.0             266065.41                       14.7                 0.00           0.0                        0.0       Standby: initializing
   Site B Installer Logger/50K-M0(SiteB) 2026-05-01 06:10:00 DST                0.0                     0.0                 0.0             266065.41                       14.5                50.02           0.0                        0.0 Standby: detecting sunlight
```

## site_b/site_b_hourly_weather.csv

- Rows: 9,504
- Columns: 23
- Duplicate rows: 0

### Column profile

| Column | Data type | Missing | Unique |
|---|---|---:|---:|
| datetime_utc | object | 0.00% | 9,504 |
| datetime_local | object | 0.00% | 9,504 |
| active_power_kw | float64 | 1.79% | 5,042 |
| dc_input_power_kw | float64 | 37.68% | 5,077 |
| daily_energy_kwh | float64 | 37.68% | 4,267 |
| cumulative_energy_kwh | float64 | 37.68% | 5,194 |
| inverter_temp_c | float64 | 37.68% | 2,923 |
| grid_freq_hz | float64 | 37.68% | 413 |
| power_factor | float64 | 37.68% | 387 |
| efficiency_pct | float64 | 37.68% | 2,747 |
| inverter_status | object | 37.68% | 8 |
| is_generating | float64 | 1.79% | 2 |
| temp_c | float64 | 1.79% | 449 |
| humidity_pct | float64 | 1.79% | 80 |
| cloud_cover_pct | float64 | 1.79% | 101 |
| wind_speed_kmh | float64 | 1.79% | 236 |
| ghi_wm2 | float64 | 1.79% | 890 |
| dni_wm2 | float64 | 1.79% | 3,359 |
| dhi_wm2 | float64 | 1.79% | 357 |
| precip_mm | float64 | 1.79% | 55 |
| solar_elevation_deg | float64 | 0.00% | 4,848 |
| solar_azimuth_deg | float64 | 0.00% | 9,494 |
| capacity_factor | float64 | 1.79% | 3,357 |

### Date/time candidates

- **datetime_utc**: 9,504/9,504 parseable values
  - Range: 2025-04-30 21:00:00 to 2026-05-31 20:00:00
- **datetime_local**: 9,504/9,504 parseable values
  - Range: 2025-05-01 00:00:00+03:00 to 2026-05-31 23:00:00+03:00

### Sample records

```text
       datetime_utc           datetime_local  active_power_kw  dc_input_power_kw  daily_energy_kwh  cumulative_energy_kwh  inverter_temp_c  grid_freq_hz  power_factor  efficiency_pct      inverter_status  is_generating  temp_c  humidity_pct  cloud_cover_pct  wind_speed_kmh  ghi_wm2  dni_wm2  dhi_wm2  precip_mm  solar_elevation_deg  solar_azimuth_deg  capacity_factor
2025-04-30 21:00:00 2025-05-01 00:00:00+0300              0.0                0.0               0.0              190913.34             25.7           0.0           0.0             0.0 Standby: no sunlight            0.0     NaN           NaN              NaN             NaN      NaN      NaN      NaN        NaN                  0.0           345.1277              0.0
2025-04-30 22:00:00 2025-05-01 01:00:00+0300              0.0                NaN               NaN                    NaN              NaN           NaN           NaN             NaN                  NaN            0.0     NaN           NaN              NaN             NaN      NaN      NaN      NaN        NaN                  0.0             1.6934              0.0
2025-04-30 23:00:00 2025-05-01 02:00:00+0300              0.0                NaN               NaN                    NaN              NaN           NaN           NaN             NaN                  NaN            0.0    10.7          75.0             30.0             6.9      0.0      0.0      0.0        0.0                  0.0            18.1303              0.0
```
