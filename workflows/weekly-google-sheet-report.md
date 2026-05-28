# Weekly Google Sheet Report Workflow

## Purpose

Use this workflow when the user asks the agent to generate a weekly performance report in Google Sheets.

The workflow composes two skills:

1. `skills/ads-analysis/`
2. `skills/google-sheets-reporting/`

## Trigger Examples

- 「幫我產上週 Google Ads / Meta Ads / GA4 週報到 Google Sheet」
- 「請做一份 weekly performance report，輸出成 Google Sheet」
- 「幫我把跨平台成效分析整理到 Google Sheets」

## Workflow

1. Run Environment Gate
   - Confirm `APP_ENV`.
   - Confirm `DATA_SOURCE_CONFIG` or `config/data-sources.yml`.
   - Identify enabled sources allowed for the current environment.
   - In production, reject CSV fixtures, Mock MCP, public samples, `test/`, `data/`, and sources without `production_allowed: true`.
   - If no allowed source exists, stop and report the data gap.

2. Determine scope
   - Confirm date range, timezone, currency, platforms, account / property scope.
   - If date range is missing, ask before proceeding unless the user explicitly gave a default.

3. Fetch source data
   - Use native MCP connectors when available and allowed by Environment Gate.
   - Use BigQuery / SQL / CSV only as read-only analytics sources and only when allowed by Environment Gate.
   - If tools, credentials, or allowed sources are missing, stop and report the data gap.

4. Run analysis
   - Use `skills/ads-analysis/SKILL.md`.
   - Apply relevant `modes/analyses/` files first, then relevant `modes/platforms/` files.
   - Write the full Markdown analysis artifact to `output/` using `templates/analysis-output.md`.
   - Produce structured output matching `skills/ads-analysis/output.schema.json`.

5. Validate structured output
   - Confirm metadata, data sources, analysis trace, platform summary, findings, recommended actions, and data gaps exist.
   - Ensure observations are data-backed.
   - Ensure findings include reasoning basis and user-reviewable evidence or formulas.
   - Ensure recommendations that modify ad accounts are marked as requiring approval.

6. Generate Google Sheet
   - Use `skills/google-sheets-reporting/SKILL.md`.
   - Create a new Sheet unless the user supplied a target Sheet to update.
   - Write only report data and analysis, not secrets.

7. Verify report
   - Verify tabs created or updated.
   - Verify row counts for key tabs.
   - Verify date range and scope are visible in `Config` and `Executive Summary`.
   - Verify source selection, rules applied, field mapping, metric formulas, assumptions, and decision log are visible in `Analysis Trace`.

8. Return result
   - Provide Google Sheet link.
   - Summarize date range, platform scope, row counts, and data gaps.

## Safety

- Never perform ad account write actions in this workflow.
- Write actions in Google Sheets are limited to report creation or report updates.
- Any recommended change to campaign, budget, bid, targeting, creative, tracking, or status must stay in `Recommended Actions` and require separate approval.
