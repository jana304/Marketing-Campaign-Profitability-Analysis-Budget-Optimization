# Marketing Campaigns & Conversions Dataset v1.0.0

A deterministic synthetic performance-marketing dataset with campaign windows, channel-specific funnel behavior, and attribution practice.

This is synthetic educational data generated to model a fictional business. It does not represent a real company or establish industry benchmarks.

## Contents

- `campaigns`: 120 rows
- `daily_spend`: 11,240 rows
- `leads`: 261,684 rows
- `conversions`: 39,696 rows

The source CSV ZIP preserves normalized source tables. SQLite contains the same
tables. XLSX and Parquet contain an analysis-ready denormalized view. Starter
examples demonstrate safe read-only exploration.

## Reproducibility

Built by `datasets/generate.py` with version `1.0.0` and seed
`2025090503`. See `manifest.json` for row profiles, reference outputs,
validation checks, file sizes, and SHA-256 checksums.

## License

See `LICENSE.txt`. Limitations from the catalog:
- This is synthetic educational data generated to model a fictional business. It does not represent a real company or establish industry benchmarks.
- Synthetic attribution is last-touch.
- Offline and view-through conversions are excluded.
- No PII is included.
