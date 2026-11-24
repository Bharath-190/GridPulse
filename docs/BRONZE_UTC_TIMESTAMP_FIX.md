# Bronze UTC timestamp correction

## Finding

The Excel timestamp wall-clock labels match the publisher CSV's `datetime_local` field. The Bronze code converted these Bucharest local values to UTC, then stripped timezone information with `tz_localize(None)` before passing the values to PySpark.

PySpark treats naive Python `datetime` objects as host-local timestamps. On a host configured for Asia/Kolkata, a naive value representing 05:30 UTC is interpreted as 05:30 IST, which is 00:00 UTC. The uploaded diagnostic showed exactly this 5-hour-30-minute displacement for the sample `2025-03-19 07:30:00` Bucharest local time: expected 05:30 UTC, stored 00:00 UTC.

## Code change

The corrected ingestion path keeps the Pandas UTC timestamps timezone-aware and passes aware UTC `datetime` instances to Spark's `TimestampType`. The same rule is applied to Python-created ingestion and manifest timestamps. Spark-generated `current_timestamp()` values remain under the Spark session timezone, which is explicitly UTC.

## Rebuild requirement

This correction changes event timestamp keys. Existing wrong-key Bronze inverter rows must not be left in place or merged with corrected keys. Back up `data/bronze/delta`, then remove the old Delta directory and perform a fresh ingestion. All source data is re-read; the original raw dataset is left untouched.
