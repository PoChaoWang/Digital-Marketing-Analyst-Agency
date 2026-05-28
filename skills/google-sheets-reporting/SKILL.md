# Google Sheets Reporting Skill

## Purpose

Use this skill when the user asks to create, update, or format a Google Sheet report from an ads analysis result.

This skill does not independently invent or reinterpret advertising performance. It consumes structured output from `skills/ads-analysis/` and writes a report to Google Sheets.

## Required Reading

Always read:

- `CLAUDE.md`
- `DATA_CONTRACT.md`
- `templates/google-sheet-weekly-report.md`
- `skills/google-sheets-reporting/sheet.schema.json`

When used after an analysis step, also use:

- `skills/ads-analysis/output.schema.json`
- `workflows/weekly-google-sheet-report.md`

## Inputs

Required:

- Structured ads analysis output matching `skills/ads-analysis/output.schema.json`
- Target behavior: create new Google Sheet or update existing Google Sheet
- Sheet title or target Google Sheet URL / ID

Optional:

- Existing template Sheet URL / ID
- Folder destination
- Locale
- Currency formatting
- Whether to include raw detail tabs

## Google Sheets Access Rules

- Use available Google Sheets / Google Drive tools in the runtime.
- Do not assume exact MCP tool names.
- If Google Sheets tools are unavailable, produce a clear export plan and do not pretend the Sheet was created.
- Before updating an existing Sheet, confirm the target file identity if there is any ambiguity.
- Do not write secrets, tokens, private keys, customer credentials, or hidden config values to the Sheet.

## Sheet Tabs

Create or update these tabs when data is available:

- `Config`
- `Analysis Trace`
- `Executive Summary`
- `Platform Summary`
- `Campaign Detail`
- `GA4 Onsite Quality`
- `Findings`
- `Recommended Actions`
- `Data Gaps`
- `Change Approval`

## Reporting Steps

1. Validate the analysis output has required metadata, sources, analysis trace, findings, actions, and data gaps.
2. Confirm create vs update behavior.
3. Create or open the Google Sheet.
4. Create missing tabs.
5. Write metadata, analysis trace, and data tables.
6. Apply practical formatting: frozen header rows, filters, currency/percent formats, severity/risk columns.
7. Verify expected tabs and row counts.
8. Return the Sheet link, date range, scope, and any data gaps.

## Safety

- Writing a Google Sheet report is allowed when requested because it writes a report artifact, not an ad account.
- Do not execute ad platform write actions.
- Recommended actions that would modify ad accounts must remain marked `requires_approval: true`.
- Keep raw exports in `exports/` or `data/`; final reports belong in `reports/` or Google Drive.
