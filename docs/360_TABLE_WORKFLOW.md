# 360 Table Workflow

This workflow makes recurring period comparison more direct:

```text
raw MCP / CSV sources -> exports/360_table.csv -> period compare JSON -> AI insight
```

The older `recipes/*.yml` files remain useful as extraction specs, field contracts, and validation references. The 360 table becomes the standard intermediate table for flexible analysis.

## Script Language Policy

- Production data cleaning, 360 table build, and period comparison use Python + SQL.
- `scripts/run-recipe.mjs` remains legacy / development-only for Mock MCP and older recipe validation.
- New production analysis scripts should follow the Python + SQL pattern unless there is a clear reason not to.

## Build 360 Table

The cleaning logic lives in SQL:

```text
sql/build_360_table.sql
```

The runner loads CSV or MCP-staged CSV files into SQLite staging tables, applies the SQL, and writes:

```text
exports/360_table.csv
```

Example using development CSV fixtures:

```bash
python3 scripts/combine_to_360_table.py \
  --google-ads-csv test/csv/google_ads_raw.csv \
  --meta-ads-csv test/csv/meta_ads_raw.csv \
  --ga4-csv test/csv/ga4_raw.csv \
  --out exports/360_table.csv
```

Example with an override:

```bash
python3 scripts/combine_to_360_table.py \
  --google-ads-csv data/google_ads.csv \
  --meta-ads-csv data/meta_ads.csv \
  --ga4-csv data/ga4.csv \
  --priority-overrides config/priority-overrides.example.yml \
  --out exports/360_table.csv
```

## Grain

The 360 table uses this grain:

```text
date + platform + campaign_name + ad_group_name + ad_name
```

GA4 mapping:

- `utm_campaign` -> `campaign_name`
- `utm_id` -> `ad_group_name`
- `utm_content` -> `ad_name`

## Source Priority

Default priority:

```text
MCP > CSV
```

Override format:

```yaml
priority_overrides:
  - date: 2026-05-20
    platform: meta_ads
    prefer: csv
    reason: "MCP missing late imported conversions"
```

Output source metadata:

- `source_type`: `mcp` or `csv`
- `platform_name`: source name such as `google_ads_mcp_production` or `manual_csv_fallback`
- `source_file`: CSV file path for CSV rows
- `source_priority`: `default_mcp`, `default_csv`, `user_override_mcp`, or `user_override_csv`
- `loaded_at`: load timestamp

## GA4 Metric Policy

For calculations involving order, conversion, revenue, or conversion value, use GA4 fields:

- CVR uses `ga4_conversions / clicks`
- CPA uses `spend / ga4_conversions`
- ROAS uses `ga4_revenue / spend`
- ROI uses `(ga4_revenue - spend) / spend`

Platform `conversions` and `revenue` remain in the 360 table for audit and discrepancy checks, but they are not the default truth source for these metrics.

## Period Compare

After building `exports/360_table.csv`, run:

```bash
python3 scripts/period_compare_360_table.py \
  --input exports/360_table.csv \
  --current-start 2026-05-26 \
  --current-end 2026-06-01 \
  --previous-start 2026-05-19 \
  --previous-end 2026-05-25 \
  --out exports/period_compare.json
```

The script outputs JSON for AI interpretation. Chat responses should summarize the result and link to output artifacts instead of pasting full analysis.
