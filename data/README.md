# Manual CSV Fallback Data

Use this directory only when MCP / warehouse access is unavailable and the user explicitly wants to analyze manually exported CSV files.

## Important Rules

- Do not commit customer CSV exports.
- Do not put secrets, tokens, account credentials, or private keys here.
- Production must not silently fall back to this directory.
- The user must explicitly provide or enable the CSV fallback source in `config/data-sources.yml`.
- Every report must label this as `csv_export` or `manual`, not as native MCP data.

## File Names

CSV file names do not need to follow one fixed pattern. Different teams export files with different names.

Recommended names are still helpful:

```text
google_ads_YYYY-MM-DD_to_YYYY-MM-DD.csv
meta_ads_YYYY-MM-DD_to_YYYY-MM-DD.csv
ga4_YYYY-MM-DD_to_YYYY-MM-DD.csv
```

If file names are inconsistent, source selection should rely on:

- explicit user-provided file path, or
- `config/data-sources.yml` allowlist entry, or
- platform-specific required column validation.

Do not blindly analyze every CSV in this directory.

## Required Column Hints

Google Ads / Meta Ads campaign CSV should include:

- `date`
- `platform`
- `campaign_name`
- `impressions`
- `clicks`
- `spend`
- `currency`
- `conversions`
- `conversion_value`

GA4 landing page CSV should include:

- `date`
- `source`
- `medium`
- `campaign`
- `sessions`
- `users`
- `engaged_sessions`
- `key_events`
- `conversions`
- `revenue`
- `currency`
- `landing_page`
