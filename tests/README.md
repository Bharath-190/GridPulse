# Validation checklist

After source download:

- [ ] Both site folders exist.
- [ ] Both hourly weather CSV files exist.
- [ ] Monthly raw XLSX files exist for both sites.
- [ ] Hourly timestamps parse as UTC.
- [ ] 5-minute raw readings are parsed without treating Excel preamble rows as data.
- [ ] Nighttime zeros are retained.
- [ ] Missing timestamps around daylight-saving transitions remain missing.
- [ ] Weather columns are labelled as reanalysis estimates.
- [ ] Site A and Site B are kept distinguishable in every table.
- [ ] Synthetic asset/maintenance tables are kept separate and carry `is_synthetic=true`.
- [ ] Hourly aggregates calculated from raw data are compared with publisher-provided hourly files.
