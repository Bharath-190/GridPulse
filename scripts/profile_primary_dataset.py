from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/external/PV-Generation-Dataset"
OUT = ROOT / "data/profiling/initial_profile.md"

if not DATA.exists():
    raise SystemExit(f"Dataset directory not found: {DATA}")

OUT.parent.mkdir(parents=True, exist_ok=True)

files = sorted(
    list(DATA.rglob("*.csv")) +
    list(DATA.rglob("*.xlsx"))
)

report = [
    "# GridPulse — Initial Data Profiling",
    "",
    f"Dataset directory: `{DATA}`",
    f"Files discovered: {len(files)}",
    "",
]

def profile_frame(df, name):
    report.extend([
        f"## {name}",
        "",
        f"- Rows: {len(df):,}",
        f"- Columns: {len(df.columns)}",
        f"- Duplicate rows: {df.duplicated().sum():,}",
        "",
        "### Column profile",
        "",
        "| Column | Data type | Missing | Unique |",
        "|---|---|---:|---:|",
    ])

    for col in df.columns:
        missing = df[col].isna().mean() * 100
        unique = df[col].nunique(dropna=True)

        report.append(
            f"| {col} | {df[col].dtype} | "
            f"{missing:.2f}% | {unique:,} |"
        )

    report.extend(["", "### Date/time candidates", ""])

    candidates = [
        c for c in df.columns
        if any(x in str(c).lower()
               for x in ["date", "time", "timestamp"])
    ]

    if not candidates:
        report.append("No obvious date/time columns detected.")
    else:
        for col in candidates:
            parsed = pd.to_datetime(df[col], errors="coerce")
            valid = parsed.notna().sum()

            report.append(
                f"- **{col}**: {valid:,}/{len(df):,} "
                f"parseable values"
            )

            if valid:
                report.append(
                    f"  - Range: {parsed.min()} to {parsed.max()}"
                )

    report.extend(["", "### Sample records", ""])
    report.append("```text")
    report.append(df.head(3).to_string(index=False))
    report.append("```")
    report.append("")

for file in files:
    print(f"Profiling: {file.relative_to(DATA)}")

    try:
        if file.suffix.lower() == ".csv":
            df = pd.read_csv(file, low_memory=False)
            profile_frame(df, str(file.relative_to(DATA)))

        elif file.suffix.lower() == ".xlsx":
            excel = pd.ExcelFile(file)

            for sheet in excel.sheet_names:
                df = pd.read_excel(excel, sheet_name=sheet, header=3)
                profile_frame(
                    df,
                    f"{file.relative_to(DATA)} — {sheet}"
                )

    except Exception as exc:
        report.extend([
            f"## ERROR: {file.relative_to(DATA)}",
            "",
            f"Could not profile: `{exc}`",
            "",
        ])
        print(f"ERROR: {exc}")

OUT.write_text("\n".join(report), encoding="utf-8")

print("\nProfiling completed.")
print(f"Report saved to: {OUT}")
