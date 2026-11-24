from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/external/PV-Generation-Dataset"
REPORT = ROOT / "reports/hourly_coverage.md"

report = ["# GridPulse — Hourly Coverage Analysis", ""]

def add(value=""):
    report.append(str(value))

for site in ("site_a", "site_b"):
    add(f"## {site.upper()}")

    frames = []

    for path in sorted((DATA / site / "raw").glob("*.xlsx")):
        df = pd.read_excel(path, header=3)

        raw_time = df["Start Date/Time"].astype("string").str.strip()

        suffix = raw_time.str.extract(
            r"(?i)\b(DST|EEST|EET)\s*$",
            expand=False
        ).str.upper()

        cleaned = raw_time.str.replace(
            r"(?i)\s+(?:DST|EEST|EET)$",
            "",
            regex=True
        )

        local = pd.to_datetime(cleaned, errors="coerce")

        utc = local.dt.tz_localize(
            "Europe/Bucharest",
            ambiguous=suffix.isin(["DST", "EEST"]).to_numpy(),
            nonexistent="NaT"
        ).dt.tz_convert("UTC")

        frames.append(pd.DataFrame({
            "timestamp_utc": utc,
            "active_power_kw": pd.to_numeric(
                df["Active Power (kW)"], errors="coerce"
            )
        }))

    raw = pd.concat(frames, ignore_index=True).dropna(
        subset=["timestamp_utc"]
    )

    raw["hour_utc"] = raw["timestamp_utc"].dt.floor("h")
    raw["minute_slot"] = raw["timestamp_utc"].dt.minute
    raw["on_grid"] = raw["minute_slot"] % 5 == 0

    agg = raw.groupby("hour_utc").agg(
        reading_count=("timestamp_utc", "size"),
        power_count=("active_power_kw", "count"),
        unique_slots=("minute_slot", "nunique"),
        on_grid_count=("on_grid", "sum"),
        raw_mean_kw=("active_power_kw", "mean")
    )

    hourly = pd.read_csv(
        DATA / site / f"{site}_hourly_weather.csv"
    )

    hourly["hour_utc"] = pd.to_datetime(
        hourly["datetime_utc"], utc=True
    )

    hourly["hourly_power_kw"] = pd.to_numeric(
        hourly["active_power_kw"], errors="coerce"
    )

    result = hourly[
        ["hour_utc", "hourly_power_kw"]
    ].merge(
        agg, on="hour_utc", how="left"
    )

    result["reading_count"] = result["reading_count"].fillna(0)
    result["power_count"] = result["power_count"].fillna(0)
    result["unique_slots"] = result["unique_slots"].fillna(0)
    result["on_grid_count"] = result["on_grid_count"].fillna(0)

    complete = (
        (result["reading_count"] == 12)
        & (result["power_count"] == 12)
        & (result["unique_slots"] == 12)
        & (result["on_grid_count"] == 12)
    )

    result["coverage"] = np.select(
        [
            result["reading_count"] == 0,
            complete,
            result["reading_count"] > 12
        ],
        ["no_raw_data", "complete_12", "over_12"],
        default="partial"
    )

    add("")
    add("### Coverage categories")

    for category, count in result["coverage"].value_counts().items():
        add(f"- {category}: {count:,}")

    add("")
    add("### Aggregation error by coverage")

    for category in ["complete_12", "partial", "over_12"]:
        subset = result[
            result["coverage"].eq(category)
        ].dropna(subset=["hourly_power_kw", "raw_mean_kw"])

        if subset.empty:
            add(f"- {category}: no comparable records")
            continue

        mae = (
            subset["hourly_power_kw"] - subset["raw_mean_kw"]
        ).abs().mean()

        add(
            f"- {category}: {len(subset):,} pairs, "
            f"MAE={mae:.6f} kW"
        )

    add("")

REPORT.parent.mkdir(parents=True, exist_ok=True)
REPORT.write_text("\n".join(report), encoding="utf-8")

print(f"Coverage analysis saved: {REPORT}")