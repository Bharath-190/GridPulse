from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/external/PV-Generation-Dataset"
REPORT = ROOT / "reports/raw_hourly_reconciliation.md"

report = [
    "# GridPulse — Raw to Hourly Reconciliation",
    "",
    "Timezone: Europe/Bucharest",
    "",
]

def add(value=""):
    report.append(str(value))

for site in ("site_a", "site_b"):
    add(f"## {site.upper()}")
    add("")

    raw_frames = []

    for path in sorted((DATA / site / "raw").glob("*.xlsx")):
        df = pd.read_excel(path, header=3)

        raw = df["Start Date/Time"].astype("string").str.strip()

        suffix = raw.str.extract(
            r"(?i)\b(DST|EEST|EET)\s*$",
            expand=False
        ).str.upper()

        cleaned = raw.str.replace(
            r"(?i)\s+(?:DST|EEST|EET)\s*$",
            "",
            regex=True
        )

        local_naive = pd.to_datetime(cleaned, errors="coerce")

        # DST/EEST identifies the summer occurrence of
        # an ambiguous local timestamp. EET/no suffix
        # identifies standard time.
        ambiguous = suffix.isin(["DST", "EEST"]).to_numpy()

        local_aware = local_naive.dt.tz_localize(
            "Europe/Bucharest",
            ambiguous=ambiguous,
            nonexistent="NaT"
        )

        utc = local_aware.dt.tz_convert("UTC")

        raw_frames.append(pd.DataFrame({
            "timestamp_raw": raw,
            "timestamp_local": local_naive,
            "timestamp_utc": utc,
            "active_power_kw": pd.to_numeric(
                df["Active Power (kW)"], errors="coerce"
            ),
            "source_file": path.name,
        }))

    raw_df = pd.concat(raw_frames, ignore_index=True)

    add(f"- Raw Excel records: {len(raw_df):,}")
    add(f"- Invalid local timestamps: {raw_df.timestamp_local.isna().sum():,}")
    add(f"- Unresolved timezone timestamps: {raw_df.timestamp_utc.isna().sum():,}")
    add(f"- Duplicate UTC timestamps: {raw_df.timestamp_utc.duplicated().sum():,}")
    add("")

    valid = raw_df.dropna(subset=["timestamp_utc"]).copy()
    valid = valid.sort_values("timestamp_utc")

    # Inspect raw sampling intervals.
    intervals = valid["timestamp_utc"].diff().dropna()

    add("### Raw sampling intervals")
    add("")
    add(f"- Five-minute intervals: {(intervals == pd.Timedelta(minutes=5)).sum():,}")
    add(f"- Other intervals: {(intervals != pd.Timedelta(minutes=5)).sum():,}")
    add(f"- Largest observed interval: {intervals.max()}")
    add("")

    add("Most common intervals:")
    for interval, count in intervals.value_counts().head(8).items():
        add(f"- {interval}: {count:,}")
    add("")

    # Aggregate raw readings by UTC hour.
    valid["hour_utc"] = valid["timestamp_utc"].dt.floor("h")

    raw_hourly = valid.groupby("hour_utc").agg(
        raw_mean_kw=("active_power_kw", "mean"),
        raw_max_kw=("active_power_kw", "max"),
        raw_last_kw=("active_power_kw", "last"),
        raw_reading_count=("active_power_kw", "count"),
    )

    hourly_path = DATA / site / f"{site}_hourly_weather.csv"
    hourly = pd.read_csv(hourly_path, low_memory=False)

    hourly["hour_utc"] = pd.to_datetime(
        hourly["datetime_utc"], utc=True, errors="coerce"
    )

    hourly["hourly_power_kw"] = pd.to_numeric(
        hourly["active_power_kw"], errors="coerce"
    )

    comparison = hourly[
        ["hour_utc", "hourly_power_kw"]
    ].merge(
        raw_hourly,
        on="hour_utc",
        how="inner"
    )

    add("### Hourly power reconciliation")
    add("")
    add(f"- Matching hours: {len(comparison):,}")
    add("")

    comparison = comparison.dropna(
        subset=["hourly_power_kw"]
    )

    for column in ("raw_mean_kw", "raw_max_kw", "raw_last_kw"):
        pairs = comparison.dropna(subset=[column, "hourly_power_kw"])

        if pairs.empty:
            add(f"- {column}: insufficient matching readings")
            continue

        mae = (
            pairs["hourly_power_kw"] - pairs[column]
        ).abs().mean()

        correlation = pairs["hourly_power_kw"].corr(pairs[column])

        add(
            f"- {column}: MAE={mae:.5f} kW; "
            f"correlation={correlation:.5f}; "
            f"pairs={len(pairs):,}"
        )

    add("")

REPORT.parent.mkdir(parents=True, exist_ok=True)
REPORT.write_text("\n".join(report), encoding="utf-8")

print("Reconciliation completed.")
print(f"Report saved: {REPORT}")
