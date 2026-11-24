from pathlib import Path
import re
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/external/PV-Generation-Dataset"
REPORT = ROOT / "reports/source_data_audit.md"

report = [
    "# GridPulse — Source Data Audit",
    "",
    "Automated structural and data-quality audit.",
    "",
]

def add(text=""):
    report.append(str(text))

def pct(value, total):
    return f"{100 * value / total:.2f}%" if total else "N/A"

if not DATA.exists():
    raise SystemExit(f"Dataset directory not found: {DATA}")

all_files = [p for p in DATA.rglob("*") if p.is_file()]

add(f"Total files in source repository: {len(all_files)}")
add("")

# --------------------------------------------------
# 1. Repository inventory
# --------------------------------------------------

add("## 1. Repository inventory")
add("")

for directory in sorted(p for p in DATA.iterdir() if p.is_dir()):
    files = [p for p in directory.rglob("*") if p.is_file()]
    add(f"- **{directory.name}/**: {len(files)} files")

add("")

# --------------------------------------------------
# 2. Hourly CSV validation
# --------------------------------------------------

add("## 2. Hourly datasets")
add("")

schemas = {}

for site in ("site_a", "site_b"):
    path = DATA / site / f"{site}_hourly_weather.csv"

    if not path.exists():
        add(f"### {site}: MISSING")
        add("")
        continue

    df = pd.read_csv(path, low_memory=False)
    schemas[site] = set(df.columns)

    add(f"### {site.upper()}")
    add("")
    add(f"- File size: {path.stat().st_size / 1024:.1f} KB")
    add(f"- Rows: {len(df):,}")
    add(f"- Columns: {len(df.columns)}")
    add(f"- Duplicate complete rows: {df.duplicated().sum():,}")

    if "datetime_utc" not in df:
        add("- ERROR: datetime_utc column missing")
        add("")
        continue

    utc = pd.to_datetime(df["datetime_utc"], utc=True, errors="coerce")
    invalid = utc.isna().sum()

    add(f"- Invalid UTC timestamps: {invalid:,}")
    add(f"- Duplicate UTC timestamps: {utc.duplicated().sum():,}")

    valid = utc.dropna()

    if not valid.empty:
        add(f"- UTC range: {valid.min()} to {valid.max()}")

        expected = pd.date_range(
            valid.min(), valid.max(), freq="h"
        )
        actual = pd.DatetimeIndex(valid.unique())
        missing = expected.difference(actual)

        add(f"- Expected hourly slots: {len(expected):,}")
        add(f"- Missing hourly slots: {len(missing):,}")

        if len(missing):
            add("- First missing timestamps:")
            for ts in missing[:10]:
                add(f"  - {ts}")

    if "datetime_local" in df:
        local_utc = pd.to_datetime(
            df["datetime_local"], utc=True, errors="coerce"
        )

        comparable = utc.notna() & local_utc.notna()
        mismatch = (utc[comparable] != local_utc[comparable]).sum()

        add(f"- Local/UTC conversion mismatches: {mismatch:,}")
        add(
            f"- Invalid local timestamps: "
            f"{pd.to_datetime(df['datetime_local'], utc=True, errors='coerce').isna().sum():,}"
        )

    add("")
    add("#### Missing values")

    missing_columns = df.isna().sum()
    for col, count in missing_columns.items():
        if count:
            add(f"- `{col}`: {count:,} ({pct(count, len(df))})")

    add("")
    add("#### Numeric measurements")

    numeric = df.select_dtypes(include="number")

    for col in numeric.columns:
        if numeric[col].notna().any():
            add(
                f"- `{col}`: min={numeric[col].min()}, "
                f"max={numeric[col].max()}"
            )

    if "active_power_kw" in df:
        over = (df["active_power_kw"] > 50).sum()
        negative = (df["active_power_kw"] < 0).sum()

        add(f"- Active power above 50 kW: {over:,}")
        add(f"- Negative active power: {negative:,}")

    if "capacity_factor" in df:
        outside = (
            (df["capacity_factor"] < 0) |
            (df["capacity_factor"] > 1)
        ).sum()
        add(f"- Capacity factor outside [0, 1]: {outside:,}")

    add("")

if "site_a" in schemas and "site_b" in schemas:
    add("### Schema comparison")
    add(f"- Same columns: {schemas['site_a'] == schemas['site_b']}")
    add(
        f"- Only in Site A: "
        f"{sorted(schemas['site_a'] - schemas['site_b'])}"
    )
    add(
        f"- Only in Site B: "
        f"{sorted(schemas['site_b'] - schemas['site_a'])}"
    )
    add("")

# --------------------------------------------------
# 3. Raw Excel exports
# --------------------------------------------------

add("## 3. Raw Excel exports")
add("")

for site in ("site_a", "site_b"):
    files = sorted((DATA / site / "raw").glob("*.xlsx"))

    add(f"### {site.upper()}")
    add(f"- Excel files: {len(files)}")
    add("")

    total_rows = 0
    total_parse_failures = 0
    normalized_timestamps = []

    for file in files:
        try:
            df = pd.read_excel(file, header=3)

            total_rows += len(df)

            if "Start Date/Time" not in df:
                add(f"- ERROR: {file.name}: timestamp column missing")
                continue

            raw = df["Start Date/Time"].astype("string").str.strip()

            suffix_mask = raw.str.contains(
                r"(?i)\b(?:DST|EEST|EET)$",
                regex=True,
                na=False,
            )

            cleaned = raw.str.replace(
                r"(?i)\s+(?:DST|EEST|EET)$",
                "",
                regex=True,
            )

            parsed = pd.to_datetime(cleaned, errors="coerce")
            failures = int(parsed.isna().sum())
            total_parse_failures += failures

            duplicate_raw = int(raw.duplicated().sum())
            collision = int(parsed.duplicated().sum())

            normalized_timestamps.extend(
                parsed.dropna().tolist()
            )

            add(f"#### {file.name}")
            add(f"- Rows: {len(df):,}")
            add(f"- Timestamp suffix records: {suffix_mask.sum():,}")
            add(f"- Timestamp parse failures after suffix removal: {failures:,}")
            add(f"- Exact duplicate raw timestamps: {duplicate_raw:,}")
            add(f"- Duplicate parsed local times: {collision:,}")

            if parsed.notna().any():
                add(
                    f"- Time range: {parsed.min()} "
                    f"to {parsed.max()}"
                )

            add("")

        except Exception as exc:
            add(f"- ERROR reading {file.name}: {exc}")
            add("")

    combined = pd.Series(normalized_timestamps)

    add("#### Site-level summary")
    add(f"- Total Excel rows: {total_rows:,}")
    add(f"- Total timestamp parse failures: {total_parse_failures:,}")
    add(
        f"- Repeated parsed local timestamps across files: "
        f"{combined.duplicated().sum():,}"
    )
    add("")

# --------------------------------------------------
# 4. Archived forecast files
# --------------------------------------------------

add("## 4. Archived forecast datasets")
add("")

forecast_dir = DATA / "archived_forecasts"

if forecast_dir.exists():
    forecast_files = sorted(forecast_dir.glob("*.csv"))
    add(f"- Archived forecast CSV files: {len(forecast_files)}")

    for file in forecast_files:
        add(
            f"- `{file.name}` "
            f"({file.stat().st_size / 1024:.1f} KB)"
        )
else:
    add("- Archived forecast directory not found locally.")

# --------------------------------------------------
# 5. Write report
# --------------------------------------------------

REPORT.parent.mkdir(parents=True, exist_ok=True)
REPORT.write_text("\n".join(report), encoding="utf-8")

print("Source data audit completed.")
print(f"Report: {REPORT}")
print(f"Total source files: {len(all_files)}")
print(f"Hourly schemas found: {len(schemas)}")
